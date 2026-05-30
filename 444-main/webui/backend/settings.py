import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = Path(os.environ.get("WEBUI_DATA_DIR", ROOT / "output"))

DB_PATH = DATA_DIR / "webui.db"
WIZARD_STATE_PATH = DATA_DIR / "webui_wizard_state.json"


def get_data_dir() -> Path:
    """Get the data directory, reading from env var fresh each call (allows monkeypatch in tests)."""
    return Path(os.environ.get("WEBUI_DATA_DIR", ROOT / "output"))


def secure_cookies() -> bool:
    """Whether to set the Secure flag on cookies. Defaults to True; set WEBUI_SECURE_COOKIES=0 for local HTTP."""
    return os.environ.get("WEBUI_SECURE_COOKIES", "1") != "0"

CTF_PAY_DIR = ROOT / "CTF-pay"
CTF_REG_DIR = ROOT / "CTF-reg"
PAY_CONFIG_PATH = CTF_PAY_DIR / "config.paypal.json"
REG_CONFIG_PATH = CTF_REG_DIR / "config.paypal-proxy.json"
PAY_EXAMPLE_PATH = CTF_PAY_DIR / "config.paypal.example.json"
REG_EXAMPLE_PATH = CTF_REG_DIR / "config.paypal-proxy.example.json"
