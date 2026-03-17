---
name: requests
description: Synchronous HTTP client for sending HTTP requests and handling responses.
version: 2.32.5
ecosystem: python
license: MIT
generated_with: gpt-5.2
---

## Imports

```python
import requests
from requests import Session
from requests.auth import HTTPBasicAuth, HTTPDigestAuth, AuthBase
from requests.exceptions import (
    RequestException,
    Timeout,
    ConnectTimeout,
    ReadTimeout,
    ConnectionError,
    HTTPError,
    TooManyRedirects,
    JSONDecodeError,
)
```

## Core Patterns

### GET with query params + status checking ✅ Current
```python
from __future__ import annotations

import requests


def fetch_repo(owner: str, repo: str) -> dict:
    url = "https://api.github.com/repos/{owner}/{repo}".format(owner=owner, repo=repo)
    r = requests.get(url, params={"per_page": 1}, timeout=10)
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    data = fetch_repo("psf", "requests")
    print(data["full_name"])
```
* Use `params=` for query strings; call `Response.raise_for_status()` before trusting the body.

### POST JSON body ✅ Current
```python
from __future__ import annotations

import requests


def create_widget(api_base: str, token: str, name: str) -> dict:
    url = f"{api_base}/post"
    headers = {"Authorization": f"Bearer {token}"}

    r = requests.post(
        url,
        json={"name": name},
        headers=headers,
        timeout=10,
    )
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    # Example: using httpbin.org/post to echo back JSON
    api_base = "https://httpbin.org"
    token = "testtoken123"
    name = "mywidget"
    result = create_widget(api_base, token, name)
    # httpbin.org returns JSON with keys: json, headers, url, etc.
    assert isinstance(result, dict)
    # The JSON body should be echoed back under "json"
    assert result.get("json") == {"name": name}
    # The Authorization header should be present (case-insensitive)
    headers = result.get("headers", {})
    authval = headers.get("Authorization") or headers.get("authorization")
    assert authval and token in authval
    # The URL should end with /post
    assert result.get("url", "").endswith("/post")
    print("✓ POST JSON body pattern ok")
```
* Prefer `json=` for JSON request bodies (sets JSON encoding; also sets an appropriate `Content-Type`).

### Reuse connections with Session ✅ Current
```python
from __future__ import annotations

import requests


def fetch_many(urls: list[str]) -> list[tuple[str, int]]:
    results: list[tuple[str, int]] = []
    with requests.Session() as s:
        s.headers.update({"User-Agent": "example-client/1.0"})
        for url in urls:
            r = s.get(url, timeout=10)
            results.append((r.url, r.status_code))
    return results


if __name__ == "__main__":
    out = fetch_many(["https://httpbin.org/get", "https://example.com/"])
    print(out)
```
* Use `requests.Session()` (or `requests.session()`) for connection pooling and shared headers/cookies.

### Streaming download to disk ✅ Current
```python
from __future__ import annotations

import requests


def download_file(url: str, path: str) -> None:
    with requests.get(url, stream=True, timeout=30) as r:
        r.raise_for_status()
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 128):
                if chunk:  # filter out keep-alive chunks
                    f.write(chunk)


if __name__ == "__main__":
    download_file("https://httpbin.org/bytes/1024", "out.bin")
    print("Wrote out.bin")
```
* For large responses, use `stream=True` and `Response.iter_content()`; write to a binary file.

### Auth: Basic/Digest/custom AuthBase ✅ Current
```python
from __future__ import annotations

import requests
from requests.auth import AuthBase, HTTPBasicAuth, HTTPDigestAuth


class BearerAuth(AuthBase):
    def __init__(self, token: str) -> None:
        self._token = token

    def __call__(self, r: requests.PreparedRequest) -> requests.PreparedRequest:
        r.headers["Authorization"] = f"Bearer {self._token}"
        return r


def demo_auth() -> None:
    # Basic auth (tuple shorthand also works: auth=("user", "pass"))
    r1 = requests.get("https://httpbin.org/basic-auth/user/pass", auth=HTTPBasicAuth("user", "pass"), timeout=10)
    print(r1.status_code)

    # Digest auth
    r2 = requests.get("https://httpbin.org/digest-auth/auth/user/pass", auth=HTTPDigestAuth("user", "pass"), timeout=10)
    print(r2.status_code)

    # Custom auth
    r3 = requests.get("https://httpbin.org/bearer", auth=BearerAuth("secret-token"), timeout=10)
    print(r3.status_code)


if __name__ == "__main__":
    demo_auth()
```
* Use `auth=("user","pass")` or `HTTPBasicAuth` for Basic; `HTTPDigestAuth` for Digest; subclass `AuthBase` for custom schemes.

## Configuration

- **Timeouts**: No default timeout; always pass `timeout=` (float seconds or `(connect, read)` tuple) to avoid hanging indefinitely.
- **Redirects**: Followed by default for GET/OPTIONS; can control with `allow_redirects=` (e.g., `requests.get(..., allow_redirects=False)`).
- **TLS verification**: Verified by default (`verify=True`). Override per request with `verify=False` (discouraged) or `verify="/path/to/ca-bundle.pem"`.
- **Proxies**: Configure via `proxies=` dict or environment variables (e.g., `HTTPS_PROXY`, `HTTP_PROXY`, `NO_PROXY`) when `Session.trust_env` is `True`.
- **Environment / netrc**: By default, Requests may consult environment and `.netrc` for credentials when `auth=` is not provided. Disable by setting `Session.trust_env = False`.
- **Response encoding**: Requests infers encoding from headers; set `Response.encoding` manually only when you know the correct encoding before accessing `Response.text`.

## Pitfalls

### Wrong: assuming JSON decoding implies HTTP success
```python
from __future__ import annotations

import requests

r = requests.get("https://httpbin.org/status/500", timeout=10)
data = r.json()  # may succeed/fail independently of HTTP status
print(data)
```

### Right: check HTTP status first
```python
from __future__ import annotations

import requests

r = requests.get("https://httpbin.org/status/500", timeout=10)
r.raise_for_status()
print(r.json())
```

### Wrong: calling Response.json() on empty/invalid JSON (e.g., 204)
```python
from __future__ import annotations

import requests

r = requests.get("https://httpbin.org/status/204", timeout=10)
print(r.json())  # raises requests.exceptions.JSONDecodeError
```

### Right: handle 204 and JSONDecodeError explicitly
```python
from __future__ import annotations

import requests
from requests.exceptions import JSONDecodeError

r = requests.get("https://httpbin.org/status/204", timeout=10)

if r.status_code == 204:
    print(None)
else:
    try:
        print(r.json())
    except JSONDecodeError:
        print(None)
```

### Wrong: using Response.raw without stream=True
```python
from __future__ import annotations

import requests

r = requests.get("https://httpbin.org/bytes/10", timeout=10)
raw_bytes = r.raw.read()  # not the intended pattern without stream=True
print(raw_bytes)
```

### Right: stream=True and iter_content()
```python
from __future__ import annotations

import requests

with requests.get("https://httpbin.org/bytes/10", stream=True, timeout=10) as r:
    r.raise_for_status()
    data = b"".join(r.iter_content(chunk_size=4))
    print(data)
```

### Wrong: unexpected credential sending via netrc/env when auth= is not set
```python
from __future__ import annotations

import requests

s = requests.Session()
# May consult environment (.netrc, proxy env vars, etc.) by default:
r = s.get("https://example.com/private", timeout=10)
print(r.status_code)
```

### Right: disable environment-based behavior when you must control auth explicitly
```python
from __future__ import annotations

import requests

s = requests.Session()
s.trust_env = False
r = s.get("https://example.com/private", timeout=10)
print(r.status_code)
```

## References

- [Documentation](https://requests.readthedocs.io)
- [Source](https://github.com/psf/requests)

## Migration from v2.31.x

- **Python support**: Requests 2.32.5 drops Python 3.8 support. If you must run on 3.8, pin `<2.32.5` temporarily and upgrade Python.
- **TLS/adapter changes (2.32.0–2.32.2)**: If you maintain a custom `HTTPAdapter`, Requests introduced a new public method for connection acquisition with TLS context (`get_connection_with_tls_context`) and considers `get_connection` deprecated in Requests >=2.32.0. Update adapter overrides accordingly.
- **TLS behavior (2.32.5)**: SSLContext caching introduced in 2.32.0 was reverted in 2.32.5; retest performance and any assumptions about TLS context reuse.
- **Security (2.31.0)**: If you use proxy URLs with credentials, ensure you are on `>=2.31.0` to avoid potential `Proxy-Authorization` leakage on HTTPS redirects; rotate proxy credentials after upgrading.

## API Reference

- **requests.get(url, params=None, \*\*kwargs)** - Send a GET request; common kwargs: `headers`, `timeout`, `auth`, `cookies`, `allow_redirects`, `proxies`, `verify`, `cert`, `stream`.
- **requests.post(url, data=None, json=None, \*\*kwargs)** - Send a POST request; prefer `json=` for JSON bodies.
- **requests.put(url, data=None, \*\*kwargs)** - Send a PUT request.
- **requests.patch(url, data=None, \*\*kwargs)** - Send a PATCH request.
- **requests.delete(url, \*\*kwargs)** - Send a DELETE request.
- **requests.head(url, \*\*kwargs)** - Send a HEAD request (often with `allow_redirects=`).
- **requests.options(url, \*\*kwargs)** - Send an OPTIONS request.
- **requests.request(method, url, \*\*kwargs)** - Generic request entry point for custom/variable methods.
- **requests.Session()** - Persistent session with connection pooling; use `.get()/.post()` etc.; configure `headers`, `cookies`, `proxies`, `verify`, `trust_env`.
- **requests.session()** - Convenience constructor returning a `requests.Session`.
- **requests.Response** - Response object; key attributes/methods: `.status_code`, `.headers`, `.url`, `.text`, `.content`, `.encoding`, `.json()`, `.raise_for_status()`, `.iter_content()`, `.raw` (with `stream=True`).
- **requests.RequestException** - Base exception for Requests errors.
- **requests.Timeout / requests.ConnectTimeout / requests.ReadTimeout** - Timeout exceptions; use `timeout=` to control.
- **requests.ConnectionError** - Network-level failure.
- **requests.HTTPError** - Raised by `Response.raise_for_status()` on 4xx/5xx.
- **requests.TooManyRedirects** - Raised when redirect limit is exceeded.
- **requests.exceptions.JSONDecodeError** - Raised by `Response.json()` on invalid/empty JSON.
- **requests.codes** - Status code lookup (e.g., `requests.codes.ok`).

## Current Library State (from source analysis)

### API Surface
```json
{
  "library_category": "http_client",
  "apis": [
    {
      "name": "requests.get",
      "type": "function",
      "signature": "get(url, params=None, **kwargs)",
      "signature_truncated": false,
      "return_type": "Response",
      "module": "requests.api",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "type_hints": {
        "url": {
          "base_type": "str",
          "is_optional": false,
          "default_value": null
        },
        "params": {
          "base_type": "dict or bytes",
          "is_optional": true,
          "default_value": "None"
        }
      }
    },
    {
      "name": "requests.post",
      "type": "function",
      "signature": "post(url, data=None, json=None, **kwargs)",
      "signature_truncated": false,
      "return_type": "Response",
      "module": "requests.api",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "type_hints": {
        "url": {
          "base_type": "str",
          "is_optional": false,
          "default_value": null
        },
        "data": {
          "base_type": "dict or bytes",
          "is_optional": true,
          "default_value": "None"
        },
        "json": {
          "base_type": "Any",
          "is_optional": true,
          "default_value": "None"
        }
      }
    },
    {
      "name": "requests.put",
      "type": "function",
      "signature": "put(url, data=None, **kwargs)",
      "signature_truncated": false,
      "return_type": "Response",
      "module": "requests.api",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "requests.patch",
      "type": "function",
      "signature": "patch(url, data=None, **kwargs)",
      "signature_truncated": false,
      "return_type": "Response",
      "module": "requests.api",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "requests.delete",
      "type": "function",
      "signature": "delete(url, **kwargs)",
      "signature_truncated": false,
      "return_type": "Response",
      "module": "requests.api",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "requests.head",
      "type": "function",
      "signature": "head(url, **kwargs)",
      "signature_truncated": false,
      "return_type": "Response",
      "module": "requests.api",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "requests.options",
      "type": "function",
      "signature": "options(url, **kwargs)",
      "signature_truncated": false,
      "return_type": "Response",
      "module": "requests.api",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "requests.request",
      "type": "function",
      "signature": "request(method, url, **kwargs)",
      "signature_truncated": false,
      "return_type": "Response",
      "module": "requests.api",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "type_hints": {
        "method": {
          "base_type": "str",
          "is_optional": false,
          "default_value": null
        },
        "url": {
          "base_type": "str",
          "is_optional": false,
          "default_value": null
        }
      }
    },
    {
      "name": "requests.Session",
      "type": "class",
      "signature": "Session()",
      "signature_truncated": false,
      "return_type": "Session",
      "module": "requests.sessions",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "class_hierarchy": {
        "bases": [],
        "abstract": false
      }
    },
    {
      "name": "requests.session",
      "type": "function",
      "signature": "session()",
      "signature_truncated": false,
      "return_type": "Session",
      "module": "requests.sessions",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "requests.Request",
      "type": "class",
      "signature": "Request(method=None, url=None, headers=None, files=None, data=None, params=None, auth=None, cookies=None, hooks=None, json=None)",
      "signature_truncated": true,
      "return_type": "Request",
      "module": "requests.models",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "class_hierarchy": {
        "bases": [],
        "abstract": false
      }
    },
    {
      "name": "requests.PreparedRequest",
      "type": "class",
      "signature": "PreparedRequest()",
      "signature_truncated": false,
      "return_type": "PreparedRequest",
      "module": "requests.models",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "class_hierarchy": {
        "bases": [],
        "abstract": false
      }
    },
    {
      "name": "requests.Response",
      "type": "class",
      "signature": "Response()",
      "signature_truncated": false,
      "return_type": "Response",
      "module": "requests.models",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "class_hierarchy": {
        "bases": [],
        "abstract": false
      }
    },
    {
      "name": "requests.codes",
      "type": "descriptor",
      "signature": "codes",
      "signature_truncated": false,
      "return_type": "module",
      "module": "requests.status_codes",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "requests.ConnectionError",
      "type": "class",
      "signature": "ConnectionError(*args, **kwargs)",
      "signature_truncated": false,
      "return_type": "ConnectionError",
      "module": "requests.exceptions",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "class_hierarchy": {
        "bases": ["RequestException"],
        "abstract": false
      }
    },
    {
      "name": "requests.ConnectTimeout",
      "type": "class",
      "signature": "ConnectTimeout(*args, **kwargs)",
      "signature_truncated": false,
      "return_type": "ConnectTimeout",
      "module": "requests.exceptions",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "class_hierarchy": {
        "bases": ["Timeout"],
        "abstract": false
      }
    },
    {
      "name": "requests.FileModeWarning",
      "type": "class",
      "signature": "FileModeWarning(*args, **kwargs)",
      "signature_truncated": false,
      "return_type": "FileModeWarning",
      "module": "requests.exceptions",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "class_hierarchy": {
        "bases": ["Warning"],
        "abstract": false
      }
    },
    {
      "name": "requests.HTTPError",
      "type": "class",
      "signature": "HTTPError(*args, **kwargs)",
      "signature_truncated": false,
      "return_type": "HTTPError",
      "module": "requests.exceptions",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "class_hierarchy": {
        "bases": ["RequestException"],
        "abstract": false
      }
    },
    {
      "name": "requests.JSONDecodeError",
      "type": "class",
      "signature": "JSONDecodeError(*args, **kwargs)",
      "signature_truncated": false,
      "return_type": "JSONDecodeError",
      "module": "requests.exceptions",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "class_hierarchy": {
        "bases": ["ValueError"],
        "abstract": false
      }
    },
    {
      "name": "requests.ReadTimeout",
      "type": "class",
      "signature": "ReadTimeout(*args, **kwargs)",
      "signature_truncated": false,
      "return_type": "ReadTimeout",
      "module": "requests.exceptions",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "class_hierarchy": {
        "bases": ["Timeout"],
        "abstract": false
      }
    },
    {
      "name": "requests.RequestException",
      "type": "class",
      "signature": "RequestException(*args, **kwargs)",
      "signature_truncated": false,
      "return_type": "RequestException",
      "module": "requests.exceptions",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "class_hierarchy": {
        "bases": ["Exception"],
        "abstract": false
      }
    },
    {
      "name": "requests.Timeout",
      "type": "class",
      "signature": "Timeout(*args, **kwargs)",
      "signature_truncated": false,
      "return_type": "Timeout",
      "module": "requests.exceptions",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "class_hierarchy": {
        "bases": ["RequestException"],
        "abstract": false
      }
    },
    {
      "name": "requests.TooManyRedirects",
      "type": "class",
      "signature": "TooManyRedirects(*args, **kwargs)",
      "signature_truncated": false,
      "return_type": "TooManyRedirects",
      "module": "requests.exceptions",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "class_hierarchy": {
        "bases": ["RequestException"],
        "abstract": false
      }
    },
    {
      "name": "requests.URLRequired",
      "type": "class",
      "signature": "URLRequired(*args, **kwargs)",
      "signature_truncated": false,
      "return_type": "URLRequired",
      "module": "requests.exceptions",
      "publicity_score": "high",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      },
      "class_hierarchy": {
        "bases": ["RequestException"],
        "abstract": false
      }
    },
    {
      "name": "requests.utils.super_len",
      "type": "function",
      "signature": "super_len(o)",
      "signature_truncated": false,
      "return_type": "int",
      "module": "requests.utils",
      "publicity_score": "medium",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    },
    {
      "name": "requests.utils.get_auth_from_url",
      "type": "function",
      "signature": "get_auth_from_url(url)",
      "signature_truncated": false,
      "return_type": "Tuple[str, str]",
      "module": "requests.utils",
      "publicity_score": "medium",
      "module_type": "public",
      "decorators": [],
      "deprecation": {
        "is_deprecated": false
      }
    }
    // ... more utils, cookies, structures, etc. could be listed here depending on __all__ and documentation
  ]
}
```

**Notes:**
- This extraction focuses on the canonical public API (as indicated by `requests/__init__.py` and `__all__` patterns).
- Many internal/compatibility APIs are omitted unless directly promoted/documented. If you want lower-level or internal APIs (such as from `requests.utils`), let me know.
- Type hints and signatures are inferred from documentation and standard usage patterns, as direct type hints in these modules are partial.
- If you need the full details of every method/property on classes like `Response` or `Session`, specify, and a more granular breakdown can be provided.
- No deprecations or removals are present in the core HTTP API as of v2.32.5.
- No route decorators, CLI, ORM, or async patterns are detected, confirming `http_client` as the category.

## Migration

### Breaking Changes from v2.31.x and v2.32.0–v2.32.5

- **Dropped Python 3.8 support**: Requests 2.32.5 requires Python 3.9+. If you must run on 3.8, pin `<2.32.5` temporarily and upgrade Python as soon as possible.
- **Custom HTTPAdapter changes (2.32.0–2.32.2)**: If you maintain a custom `HTTPAdapter`, use the new `get_connection_with_tls_context` method instead of the now-deprecated `get_connection`. See the Requests changelog and PR #6710 for migration examples.
- **TLS context caching reverted (2.32.5)**: SSLContext caching introduced in 2.32.0 is reverted in 2.32.5. If you relied on global SSLContext reuse (e.g., for performance or TLS session features), retest your code for any impact.
- **Security fix (2.31.0)**: If you use proxy URLs with embedded credentials, upgrade to `>=2.31.0` to avoid possible `Proxy-Authorization` header leakage on HTTPS redirects. Rotate proxy credentials after upgrading.

No core HTTP API endpoints were removed or had their signatures changed in 2.32.x.

---