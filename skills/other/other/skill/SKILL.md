---
name: api-proxy
description: Routes API requests through the user's residential proxy to bypass cloud IP blocks. TWO use cases - (1) Runtime fallback when direct curl/fetch fails with 403/blocked errors, use fetch.py for quick retry. (2) Template for building new skills that need proxy routing, copy proxy_helper.py into the new skill.
---

# API Proxy Skill

Routes requests through residential IP via `proxy.address.here.com`.

## Runtime Fallback (ad-hoc)

When a direct request fails with 403 or IP blocking, retry through the proxy:

```bash
# Simple GET
python3 /mnt/skills/user/api-proxy/scripts/fetch.py "https://api.example.com/endpoint"

# POST with body
python3 /mnt/skills/user/api-proxy/scripts/fetch.py "https://api.example.com/endpoint" POST '{"key": "value"}'
```

Returns JSON response or `{"error": "message"}` on failure.

## Template Mode (building skills)

When creating skills that need proxy routing:

1. Copy `proxy_helper.py` into the new skill's `scripts/` folder
2. Import and use:

```python
from proxy_helper import proxy_get, proxy_request

data = proxy_get("https://api.example.com/endpoint")

data = proxy_request(
    url="https://api.example.com/endpoint",
    method="POST",
    headers={"Authorization": "Bearer xyz"},
    body='{"key": "value"}'
)
```

## Proxy Details

```
URL: https://proxy.address.here.com/proxy
Token: your_token_here
```

## Currently Whitelisted Domains

- `reddit.com`, `www.reddit.com`, `oauth.reddit.com`

New domains require user to add them to `ALLOWED_DOMAINS` env var and restart the container.

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| 403 from proxy | Domain not whitelisted | Ask user to whitelist |
| 503 from proxy | Rate limited | Retry after delay |
| 504 from proxy | Upstream timeout | Increase timeout |
| Connection refused | Container/tunnel down | Check status |