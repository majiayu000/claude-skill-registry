---
name: gakido
description: High-performance Python HTTP client with browser impersonation and anti-bot evasion. Use when the user needs to bypass bot detection, impersonate browsers with TLS fingerprinting, make HTTP/2/3 requests, or build web scrapers that evade anti-bot systems.
---

# Gakido - Browser Impersonation HTTP Client

Gakido (餓鬼道, "the hungry ghost") is a high-performance CPython HTTP client focused on browser impersonation, anti-bot evasion, and speed.

## Installation

```bash
pip install gakido
pip install gakido[h3]     # with HTTP/3 support
pip install gakido[dev]    # development dependencies
```

Or with uv:

```bash
uv add gakido
uv add gakido[h3]
```

## Features

- 96 browser profiles (Chrome, Firefox, Safari, Edge, Opera, Brave, Vivaldi, Tor)
- JA3/Akamai-style TLS fingerprint overrides
- HTTP/1.1, HTTP/2, and HTTP/3 (QUIC) support
- Automatic compression (gzip, deflate, brotli)
- Sync + async clients with connection pooling
- Multipart uploads
- WebSocket client
- Proxy support (HTTP, SOCKS5, SOCKS5H)
- Retry with exponential backoff

## Quick Start

### Sync

```python
from gakido import Client

c = Client(impersonate="chrome_120")
r = c.get("https://example.com")
print(r.status_code, r.text[:200])
```

### Async

```python
import asyncio
from gakido.aio import AsyncClient

async def main():
    async with AsyncClient(impersonate="chrome_120") as c:
        r = await c.get("https://httpbin.org/get")
        print(r.status_code)

asyncio.run(main())
```

### TLS Fingerprint Overrides

```python
from gakido import Client, ExtraFingerprints

ja3_str = "771,4866-4867-4865-49196,0-11-10,29,0"
extra_fp = ExtraFingerprints(alpn=["http/1.1"])

c = Client(
    impersonate="chrome_120",
    tls_configuration_options={"ja3_str": ja3_str, "extra_fp": extra_fp},
)
r = c.get("https://tls.browserleaks.com/json")
print(r.json().get("ja3_hash"))
```

### HTTP/3 (QUIC)

```python
import asyncio
from gakido import AsyncClient

async def main():
    async with AsyncClient(
        impersonate="chrome_120",
        http3=True,
        http3_fallback=True,
    ) as c:
        r = await c.get("https://cloudflare.com/cdn-cgi/trace")
        print(f"HTTP/{r.http_version}: {r.status_code}")

asyncio.run(main())
```

### Proxies

```python
from gakido import Client

c = Client()
r = c.get("http://httpbin.org/ip", proxy="http://127.0.0.1:8080")
r = c.get("http://httpbin.org/ip", proxy="socks5://127.0.0.1:1080")
```

### Multipart Upload

```python
files = {"file": ("test.txt", b"hello", "text/plain")}
data = {"foo": "bar"}
with Client() as c:
    r = c.post("https://httpbin.org/post", data=data, files=files)
    print(r.json())
```

### WebSocket

```python
from gakido.websocket import WebSocket

ws = WebSocket.connect("echo.websocket.events", 443, "/", headers=[], tls=True)
ws.send_text("hello")
op, payload = ws.recv()
print(payload.decode(errors="ignore"))
ws.close()
```

### Retry with Backoff

```python
from gakido import Client

client = Client(
    max_retries=3,
    retry_base_delay=0.5,
    retry_max_delay=30.0,
    retry_jitter=True,
)
resp = client.get("http://flaky.example.com")
```

## Notes

- `force_http1=True` by default; set `force_http1=False` to allow ALPN h2
- `http3=True` enables QUIC (requires `pip install gakido[h3]`)
- `auto_decompress=True` by default

## References

- Repository: https://github.com/HappyHackingSpace/gakido
- Documentation: https://happyhackingspace.github.io/gakido/
- Antibot Benchmark: https://github.com/HappyHackingSpace/gakido/blob/main/docs/antibot-benchmark.md
