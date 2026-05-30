import ipaddress
import os
import socket
from typing import Literal
from urllib.parse import urlparse

from pydantic import BaseModel

Status = Literal["ok", "warn", "fail"]


def validate_url_not_internal(url: str) -> None:
    """Reject URLs that resolve to private/loopback/link-local addresses (SSRF guard).

    Disabled when ``WEBUI_SSRF_GUARD=0`` (useful for local dev where downstream
    services run on localhost).
    """
    if os.environ.get("WEBUI_SSRF_GUARD", "1") == "0":
        return
    parsed = urlparse(url)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL has no hostname")
    try:
        addr = ipaddress.ip_address(hostname)
    except ValueError:
        try:
            resolved = socket.getaddrinfo(hostname, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
        except socket.gaierror:
            return
        for family, _type, _proto, _canon, sockaddr in resolved:
            addr = ipaddress.ip_address(sockaddr[0])
            if addr.is_private or addr.is_loopback or addr.is_link_local:
                raise ValueError(f"URL resolves to non-routable address {addr}")
        return
    if addr.is_private or addr.is_loopback or addr.is_link_local:
        raise ValueError(f"URL points to non-routable address {addr}")


class CheckResult(BaseModel):
    name: str
    status: Status
    message: str
    details: str | None = None


class PreflightResult(BaseModel):
    status: Status
    message: str
    details: str | None = None
    checks: list[CheckResult] = []


def aggregate(checks: list[CheckResult]) -> PreflightResult:
    if any(c.status == "fail" for c in checks):
        agg = "fail"
    elif any(c.status == "warn" for c in checks):
        agg = "warn"
    else:
        agg = "ok"
    msg = f"{sum(1 for c in checks if c.status == 'ok')}/{len(checks)} ok"
    return PreflightResult(status=agg, message=msg, checks=checks)
