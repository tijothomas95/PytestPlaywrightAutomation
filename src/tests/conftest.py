import json
import pytest
from pathlib import Path

SUPPORTED_BROWSERS = {"chromium", "firefox", "webkit"}


def load_json(file_name):
    path = Path(__file__).resolve().parent.parent / file_name
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)


@pytest.fixture(scope="session")
def config(pytestconfig):
    cfg = {}

    # ---- Step 1: CLI (highest priority) ----
    cli_browser = pytestconfig.getoption("browser")
    if cli_browser:
        if isinstance(cli_browser, list):
            cli_browser = cli_browser[0]

        if cli_browser not in SUPPORTED_BROWSERS:
            raise ValueError(f"Unsupported browser: {cli_browser}")
        cfg["browser"] = cli_browser

    if pytestconfig.getoption("headed"):
        cfg["headless"] = False

    # ---- Step 2: config.json fallback ----
    if "browser" not in cfg or "headless" not in cfg:
        file_cfg = load_json("session_config.json")
        for key, value in file_cfg.items():
            cfg.setdefault(key, value)

    if "headless" not in cfg:
        cfg["headless"] = True

    # ---- Step 3: Validation ----
    if "browser" not in cfg:
        raise ValueError("No browser specified (CLI or config.json required).")
    if "headless" not in cfg:
        raise ValueError("No headless/headed setting specified (CLI or config.json required).")

    return cfg


@pytest.fixture(scope="session")
def browser_name(config):
    return config["browser"]


@pytest.fixture(scope="session")
def browser_context_args(config, browser_context_args):
    args = {**browser_context_args}
    if "viewport" in config:
        args["viewport"] = config["viewport"]
    return args


@pytest.fixture(scope="session")
def browser_type_launch_args(config):
    return {"headless": config["headless"]}

def load_env_config():
    env_path = Path(__file__).parent.parent / "env.json"
    if not env_path.exists():
        raise FileNotFoundError("env.json is required but was not found.")

    with open(env_path) as f:
        env_cfg = json.load(f)
    return env_cfg


@pytest.fixture(scope="session")
def base_url():
    env_cfg = load_env_config()
    base_url = env_cfg.get("baseURL")
    if not base_url:
        raise KeyError("env.json must define a 'baseURL'.")
    return base_url

@pytest.fixture(scope='function')
def web_page(page, base_url):
    page.goto(base_url)
    print("Base URL:", base_url)
    print("Page title:", page.title())
    return page