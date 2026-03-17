---
name: stealth-browser
description: Ultimate stealth browser automation with anti-detection, Cloudflare bypass, CAPTCHA solving, persistent sessions, and silent operation. Use for any web automation requiring bot detection evasion, login persistence, headless browsing, or bypassing security measures. Triggers on "bypass cloudflare", "solve captcha", "stealth browse", "silent automation", "persistent login", "anti-detection", or any task needing undetectable browser automation. When user asks to "login to X website", automatically use headed mode for login, then save session for future headless reuse.
---

# Stealth Browser Automation

Silent, undetectable web automation combining multiple anti-detection layers.

## Quick Login Workflow (IMPORTANT)

When user asks to login to any website:

1. **Open in headed mode** (visible browser for manual login):
```bash
python scripts/stealth_session.py -u "https://target.com/login" -s sitename --headed
```

2. **User logs in manually** in the visible browser

3. **Save session** after login confirmed:
```bash
python scripts/stealth_session.py -u "https://target.com" -s sitename --headed --save
```

4. **Future use** - load saved session (headless):
```bash
python scripts/stealth_session.py -u "https://target.com" -s sitename --load
```

Sessions stored in: `~/.clawdbot/browser-sessions/<sitename>.json`

## 执行策略 (IMPORTANT)

### 1. 先静默后显示
- 优先使用 headless 模式静默尝试
- 如果失败或需要验证码，再切换到 headed 显示模式
- 避免打扰用户操作

### 2. 断点续传
长任务使用 `task_runner.py` 管理状态：
```python
from task_runner import TaskRunner
task = TaskRunner('my_task')
task.set_total(100)
for i in items:
    if task.is_completed(i):
        continue  # 跳过已完成
    # 处理...
    task.mark_completed(i)
task.finish()
```

### 3. 超时处理
- 默认单页超时: 30秒
- 长任务每50项保存一次进度
- 失败自动重试3次

### 4. 记录尝试
所有登录尝试记录在: `~/.clawdbot/browser-sessions/attempts.json`

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Stealth Browser                     │
├─────────────────────────────────────────────────────┤
│  Layer 1: Anti-Detection Engine                      │
│  - puppeteer-extra-plugin-stealth                   │
│  - Browser fingerprint spoofing                     │
│  - WebGL/Canvas/Audio fingerprint masking           │
├─────────────────────────────────────────────────────┤
│  Layer 2: Challenge Bypass                          │
│  - Cloudflare Turnstile/JS Challenge               │
│  - hCaptcha / reCAPTCHA integration                │
│  - 2Captcha / Anti-Captcha API                     │
├─────────────────────────────────────────────────────┤
│  Layer 3: Session Persistence                       │
│  - Cookie storage (JSON/SQLite)                    │
│  - localStorage sync                               │
│  - Multi-profile management                        │
├─────────────────────────────────────────────────────┤
│  Layer 4: Proxy & Identity                         │
│  - Rotating residential proxies                    │
│  - User-Agent rotation                             │
│  - Timezone/Locale spoofing                        │
└─────────────────────────────────────────────────────┘
```

## Setup

### Install Core Dependencies

```bash
npm install -g puppeteer-extra puppeteer-extra-plugin-stealth
npm install -g playwright
pip install undetected-chromedriver DrissionPage
```

### Optional: CAPTCHA Solvers

Store API keys in `~/.clawdbot/secrets/captcha.json`:
```json
{
  "2captcha": "YOUR_2CAPTCHA_KEY",
  "anticaptcha": "YOUR_ANTICAPTCHA_KEY",
  "capsolver": "YOUR_CAPSOLVER_KEY"
}
```

### Optional: Proxy Configuration

Store in `~/.clawdbot/secrets/proxies.json`:
```json
{
  "rotating": "http://user:pass@proxy.provider.com:port",
  "residential": ["socks5://ip1:port", "socks5://ip2:port"],
  "datacenter": "http://dc-proxy:port"
}
```

## Quick Start

### 1. Stealth Session (Python - Recommended)

```python
# scripts/stealth_session.py - use for maximum compatibility
import undetected_chromedriver as uc
from DrissionPage import ChromiumPage

# Option A: undetected-chromedriver (Selenium-based)
driver = uc.Chrome(headless=True, use_subprocess=True)
driver.get("https://nowsecure.nl")  # Test anti-detection

# Option B: DrissionPage (faster, native Python)
page = ChromiumPage()
page.get("https://cloudflare-protected-site.com")
```

### 2. Stealth Session (Node.js)

```javascript
// scripts/stealth.mjs
import puppeteer from 'puppeteer-extra';
import StealthPlugin from 'puppeteer-extra-plugin-stealth';

puppeteer.use(StealthPlugin());

const browser = await puppeteer.launch({
  headless: 'new',
  args: [
    '--disable-blink-features=AutomationControlled',
    '--disable-dev-shm-usage',
    '--no-sandbox'
  ]
});

const page = await browser.newPage();
await page.goto('https://bot.sannysoft.com'); // Verify stealth
```

## Core Operations

### Open Stealth Page

```bash
# Using agent-browser with stealth profile
agent-browser --profile ~/.stealth-profile open https://target.com

# Or via script
python scripts/stealth_open.py --url "https://target.com" --headless
```

### Bypass Cloudflare

```python
# Automatic CF bypass with DrissionPage
from DrissionPage import ChromiumPage

page = ChromiumPage()
page.get("https://cloudflare-site.com")
# DrissionPage waits for CF challenge automatically

# Manual wait if needed
page.wait.ele_displayed("main-content", timeout=30)
```

For stubborn Cloudflare sites, use FlareSolverr:

```bash
# Start FlareSolverr container
docker run -d --name flaresolverr -p 8191:8191 ghcr.io/flaresolverr/flaresolverr

# Request clearance
curl -X POST http://localhost:8191/v1 \
  -H "Content-Type: application/json" \
  -d '{"cmd":"request.get","url":"https://cf-protected.com","maxTimeout":60000}'
```

### Solve CAPTCHAs

```python
# scripts/solve_captcha.py
import requests
import json
import time

def solve_recaptcha(site_key, page_url, api_key):
    """Solve reCAPTCHA v2/v3 via 2Captcha"""
    # Submit task
    resp = requests.post("http://2captcha.com/in.php", data={
        "key": api_key,
        "method": "userrecaptcha",
        "googlekey": site_key,
        "pageurl": page_url,
        "json": 1
    }).json()
    
    task_id = resp["request"]
    
    # Poll for result
    for _ in range(60):
        time.sleep(3)
        result = requests.get(f"http://2captcha.com/res.php?key={api_key}&action=get&id={task_id}&json=1").json()
        if result["status"] == 1:
            return result["request"]  # Token
    return None

def solve_hcaptcha(site_key, page_url, api_key):
    """Solve hCaptcha via Anti-Captcha"""
    resp = requests.post("https://api.anti-captcha.com/createTask", json={
        "clientKey": api_key,
        "task": {
            "type": "HCaptchaTaskProxyless",
            "websiteURL": page_url,
            "websiteKey": site_key
        }
    }).json()
    
    task_id = resp["taskId"]
    
    for _ in range(60):
        time.sleep(3)
        result = requests.post("https://api.anti-captcha.com/getTaskResult", json={
            "clientKey": api_key,
            "taskId": task_id
        }).json()
        if result["status"] == "ready":
            return result["solution"]["gRecaptchaResponse"]
    return None
```

### Persistent Sessions

```python
# scripts/session_manager.py
import json
import os
from pathlib import Path

SESSIONS_DIR = Path.home() / ".clawdbot" / "browser-sessions"
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

def save_cookies(driver, session_name):
    """Save cookies to JSON"""
    cookies = driver.get_cookies()
    path = SESSIONS_DIR / f"{session_name}_cookies.json"
    path.write_text(json.dumps(cookies, indent=2))
    return path

def load_cookies(driver, session_name):
    """Load cookies from saved session"""
    path = SESSIONS_DIR / f"{session_name}_cookies.json"
    if path.exists():
        cookies = json.loads(path.read_text())
        for cookie in cookies:
            driver.add_cookie(cookie)
        return True
    return False

def save_local_storage(page, session_name):
    """Save localStorage"""
    ls = page.evaluate("() => JSON.stringify(localStorage)")
    path = SESSIONS_DIR / f"{session_name}_localStorage.json"
    path.write_text(ls)
    return path

def load_local_storage(page, session_name):
    """Restore localStorage"""
    path = SESSIONS_DIR / f"{session_name}_localStorage.json"
    if path.exists():
        data = path.read_text()
        page.evaluate(f"(data) => {{ Object.entries(JSON.parse(data)).forEach(([k,v]) => localStorage.setItem(k,v)) }}", data)
        return True
    return False
```

### Silent Automation Workflow

```python
# Complete silent automation example
from DrissionPage import ChromiumPage, ChromiumOptions

# Configure for stealth
options = ChromiumOptions()
options.headless()
options.set_argument('--disable-blink-features=AutomationControlled')
options.set_argument('--disable-dev-shm-usage')
options.set_user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

page = ChromiumPage(options)

# Navigate with CF bypass
page.get("https://target-site.com")

# Wait for any challenges
page.wait.doc_loaded()

# Interact silently
page.ele("@id=username").input("user@email.com")
page.ele("@id=password").input("password123")
page.ele("@type=submit").click()

# Save session for reuse
page.cookies.save("~/.clawdbot/browser-sessions/target-site.json")
```

## Proxy Rotation

```python
# scripts/proxy_rotate.py
import random
import json
from pathlib import Path

def get_proxy():
    """Get random proxy from pool"""
    config = json.loads((Path.home() / ".clawdbot/secrets/proxies.json").read_text())
    proxies = config.get("residential", [])
    return random.choice(proxies) if proxies else config.get("rotating")

# Use with DrissionPage
options = ChromiumOptions()
options.set_proxy(get_proxy())
page = ChromiumPage(options)
```

## User Input Required

To complete this skill, provide:

1. **CAPTCHA API Keys** (optional but recommended):
   - 2Captcha key: https://2captcha.com
   - Anti-Captcha key: https://anti-captcha.com
   - CapSolver key: https://capsolver.com

2. **Proxy Configuration** (optional):
   - Residential proxy provider credentials
   - Or list of SOCKS5/HTTP proxies

3. **Target Sites** (for pre-configured sessions):
   - Which sites need login persistence?
   - What credentials should be stored?

## Files Structure

```
stealth-browser/
├── SKILL.md
├── scripts/
│   ├── stealth_session.py      # Main stealth browser wrapper
│   ├── solve_captcha.py        # CAPTCHA solving utilities
│   ├── session_manager.py      # Cookie/localStorage persistence
│   ├── proxy_rotate.py         # Proxy rotation
│   └── cf_bypass.py            # Cloudflare-specific bypass
└── references/
    ├── fingerprints.md         # Browser fingerprint details
    └── detection-tests.md      # Sites to test anti-detection
```

## Testing Anti-Detection

```bash
# Run these to verify stealth is working:
python scripts/stealth_open.py --url "https://bot.sannysoft.com"
python scripts/stealth_open.py --url "https://nowsecure.nl"
python scripts/stealth_open.py --url "https://arh.antoinevastel.com/bots/areyouheadless"
python scripts/stealth_open.py --url "https://pixelscan.net"
```

## Integration with agent-browser

For simple tasks, use agent-browser with a persistent profile:

```bash
# Create stealth profile once
agent-browser --profile ~/.stealth-profile --headed open https://login-site.com
# Login manually, then close

# Reuse authenticated session (headless)
agent-browser --profile ~/.stealth-profile snapshot
agent-browser --profile ~/.stealth-profile click @e5
```

For Cloudflare or CAPTCHA-heavy sites, use Python scripts instead.

## Best Practices

1. **Always use headless: 'new'** not `headless: true` (less detectable)
2. **Rotate User-Agents** matching browser version
3. **Add random delays** between actions (100-500ms)
4. **Use residential proxies** for sensitive targets
5. **Save sessions** after successful login
6. **Test on bot.sannysoft.com** before production use
