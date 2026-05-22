---
name: selenium-testing
description: Browser automation with Selenium WebDriver for Python. (project)
---

# Selenium Testing

## When to Use

- Browser automation, visual testing
- Mentions: "selenium", "webdriver", "screenshot"

## Canonical Repo Rules

For Skriptoteket-specific login/env conventions, follow:

- `.agent/rules/075-browser-automation.md`

## Run

```bash
pdm run python -m scripts.<module>
```

## Quick Pattern

```python
import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def _read_dotenv(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}

    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        values[key.strip()] = value.strip()
    return values


dotenv = _read_dotenv(Path(os.environ.get("DOTENV_PATH", ".env")))


def _get_config_value(*, key: str, default: str | None = None) -> str | None:
    return os.environ.get(key) or dotenv.get(key) or default


base_url = _get_config_value(key="BASE_URL", default="http://127.0.0.1:8000") or "http://127.0.0.1:8000"
email = _get_config_value(key="PLAYWRIGHT_EMAIL") or _get_config_value(key="BOOTSTRAP_SUPERUSER_EMAIL")
password = _get_config_value(key="PLAYWRIGHT_PASSWORD") or _get_config_value(
    key="BOOTSTRAP_SUPERUSER_PASSWORD"
)

if not email or not password:
    raise SystemExit(
        "Missing credentials. Either set PLAYWRIGHT_EMAIL/PLAYWRIGHT_PASSWORD (recommended for prod) "
        "or BOOTSTRAP_SUPERUSER_EMAIL/BOOTSTRAP_SUPERUSER_PASSWORD (dev). "
        "Provide them in DOTENV_PATH (default: .env) or export them in your shell."
    )

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
driver.set_window_size(1440, 900)

# Login
driver.get(f"{base_url}/login")
driver.find_element(By.NAME, "email").send_keys(email)
driver.find_element(By.NAME, "password").send_keys(password)
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(., 'Inloggad som')]")))

# Screenshot
Path(".artifacts").mkdir(parents=True, exist_ok=True)
driver.get(f"{base_url}/admin/tools")
driver.save_screenshot(".artifacts/selenium-admin-tools.png")
driver.quit()
```

## HTMX Caveat

Use explicit `WebDriverWait` with `EC.url_contains()` instead of implicit waits.

## Context7

Use `mcp__context7__get-library-docs` with `/seleniumhq/selenium` for API details.
