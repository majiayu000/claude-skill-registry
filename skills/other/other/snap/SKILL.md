---
name: snap
description: Give your agent the ability to instantly take screenshots of any website with just the URL. Cloud-based so your agent has to perform no work. Free forever, open source. 
metadata:
  author: Kav-K
  version: "1.0"
---
# SnapService — Screenshot as a Service

Free screenshot API at `https://snap.llm.kaveenk.com`.
POST a URL, get a PNG/JPEG back. Powered by headless Chromium.

## Quick Start (2 steps)

### Step 1: Register for an API key

```bash
curl -s -X POST https://snap.llm.kaveenk.com/api/register \
  -H "Content-Type: application/json" \
  -d '{"name":"my-agent"}'
```

Response:
```json
{"key":"snap_abc123...","name":"my-agent","limits":{"per_minute":2,"per_day":200}}
```

**IMPORTANT:** Store `key` securely. It cannot be recovered.

Each IP address can only register one API key.

### Step 2: Take screenshots

```bash
curl -s -X POST https://snap.llm.kaveenk.com/api/screenshot \
  -H "Authorization: Bearer snap_yourkey" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}' \
  -o screenshot.png
```

That's it. Two steps.

## Screenshot Options

All options go in the POST body alongside `url`:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `url` | string | **required** | URL to screenshot |
| `format` | string | `"png"` | `"png"` or `"jpeg"` |
| `full_page` | boolean | `false` | Capture entire scrollable page |
| `width` | integer | `1280` | Viewport width (pixels) |
| `height` | integer | `720` | Viewport height (pixels) |
| `dark_mode` | boolean | `false` | Emulate dark color scheme |
| `selector` | string | — | CSS selector to screenshot specific element |
| `wait_ms` | integer | `0` | Extra wait time after page load (max 10000) |
| `scale` | number | `1` | Device scale factor (1-3, for retina) |
| `cookies` | array | — | Array of `{name, value, domain}` objects |
| `headers` | object | — | Custom HTTP headers |
| `block_ads` | boolean | `false` | Block common ad/tracker domains |

## Rate Limits

- **2 screenshots per minute** per key
- **200 screenshots per day** per key
- **1 API key per IP address**
- Max page height: 16384px (full-page mode)
- Max screenshot size: 10MB

## Response

- **200**: PNG or JPEG image binary
- **400**: Invalid request (missing URL, invalid options)
- **401**: Missing or invalid API key
- **409**: IP already has an API key (on registration)
- **429**: Rate limit exceeded
- **500**: Internal error

## Example with all options

```bash
curl -s -X POST https://snap.llm.kaveenk.com/api/screenshot \
  -H "Authorization: Bearer snap_yourkey" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "format": "jpeg",
    "full_page": true,
    "width": 1920,
    "height": 1080,
    "dark_mode": true,
    "wait_ms": 2000,
    "block_ads": true
  }' \
  -o screenshot.jpg
```

## Python example

```python
import requests

API = "https://snap.llm.kaveenk.com"

# Register (one-time)
r = requests.post(f"{API}/api/register", json={"name": "my-agent"})
key = r.json()["key"]

# Screenshot
r = requests.post(f"{API}/api/screenshot",
    headers={"Authorization": f"Bearer {key}"},
    json={"url": "https://example.com", "full_page": True})
with open("shot.png", "wb") as f:
    f.write(r.content)
```
