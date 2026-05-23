---
name: httpx
description: A synchronous and asynchronous HTTP client for making requests and working with responses.
version: 0.28.1
ecosystem: python
license: BSD-3-Clause
generated_with: gpt-5.2
---

## Imports

```python
import httpx
from httpx import AsyncClient, BasicAuth, Client, DigestAuth, NetRCAuth, Response
from httpx import ASGITransport, WSGITransport
```

## Core Patterns

### One-off request with top-level API ✅ Current
```python
import httpx

def fetch_json(url: str) -> dict:
    response = httpx.get(url)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    data = fetch_json("https://httpbin.org/json")
    print(sorted(data.keys()))
```
* Use `httpx.get()`/`httpx.request()` for quick scripts or single calls.
* Prefer a persistent `httpx.Client` once you have multiple requests.

### Persistent client with connection pooling (recommended) ✅ Current
```python
import httpx

def fetch_many(urls: list[str]) -> list[int]:
    status_codes: list[int] = []
    with httpx.Client() as client:
        for url in urls:
            r = client.get(url)
            status_codes.append(r.status_code)
    return status_codes

if __name__ == "__main__":
    codes = fetch_many(["https://httpbin.org/status/200", "https://httpbin.org/status/204"])
    print(codes)
```
* Use `httpx.Client()` for connection pooling, cookie persistence, shared headers, proxy support, and HTTP/2 support (when configured).
* Use `with httpx.Client() as client:` (or call `client.close()`) to release resources.

### Async requests with AsyncClient ✅ Current
```python
import asyncio
import httpx

async def fetch_text(url: str) -> str:
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        r.raise_for_status()
        return r.text

async def main() -> None:
    text = await fetch_text("https://httpbin.org/uuid")
    print(text.strip())

if __name__ == "__main__":
    asyncio.run(main())
```
* Use `httpx.AsyncClient()` for async I/O; always `await` request calls.
* Use `async with` to ensure the client is closed.

### Authentication (built-in) ✅ Current
```python
import httpx

def fetch_with_basic_auth(url: str, username: str, password: str) -> int:
    auth = httpx.BasicAuth(username, password)
    with httpx.Client(auth=auth) as client:
        r = client.get(url)
        return r.status_code

if __name__ == "__main__":
    # httpbin requires user/pass to match in this endpoint.
    code = fetch_with_basic_auth("https://httpbin.org/basic-auth/user/pass", "user", "pass")
    print(code)
```
* Configure auth per request (`client.get(..., auth=...)`) or on the client (`Client(auth=...)`) depending on scope.
* Other built-ins include `DigestAuth` and `NetRCAuth`.

### Mounting an ASGI/WSGI app via explicit transports ✅ Current
```python
import httpx

async def asgi_app(scope, receive, send) -> None:
    assert scope["type"] == "http"
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"content-type", b"text/plain")],
        }
    )
    await send({"type": "http.response.body", "body": b"ok"})

def wsgi_app(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain")])
    return [b"ok"]

def call_wsgi() -> str:
    transport = httpx.WSGITransport(app=wsgi_app)
    with httpx.Client(transport=transport, base_url="http://testserver") as client:
        return client.get("/").text

async def call_asgi() -> str:
    transport = httpx.ASGITransport(app=asgi_app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        return (await client.get("/")).text

if __name__ == "__main__":
    print(call_wsgi())
    import asyncio
    print(asyncio.run(call_asgi()))
```
* Use `transport=httpx.WSGITransport(app=...)` or `transport=httpx.ASGITransport(app=...)`.
* The older `app=` shortcut on `Client/AsyncClient` is removed in 0.28.0 (see Migration).

## Configuration

- **Client lifecycle**
  - Recommended: `with httpx.Client(...) as client:` / `async with httpx.AsyncClient(...) as client:`
  - Manual cleanup: `client.close()` when not using a context manager.
- **Auth**
  - Pass `auth=` per request or set `Client(auth=...)`.
  - Built-ins: `httpx.BasicAuth`, `httpx.DigestAuth`, `httpx.NetRCAuth`.
  - Custom: implement `httpx.Auth` and its `auth_flow()`/`sync_auth_flow()`/`async_auth_flow()`.
- **Proxy configuration (0.26+; `proxies=` removed in 0.28.0)**
  - Use `Client(proxy="http://proxy.local:8080")` for simple cases.
  - For complex routing, use `mounts=` (preferred over the removed `proxies=` argument).
- **Transports**
  - In-process apps: `WSGITransport`, `ASGITransport`.
  - Network transports: `HTTPTransport`, `AsyncHTTPTransport` (advanced usage).
- **SSL notes (0.28.0 deprecations) ⚠️**
  - Passing `verify` as a string path and using `cert=` are deprecated and may warn.
  - `verify=True`, `verify=False`, or `verify=<ssl.SSLContext>` remain valid.
- **JSON request bodies (0.28 behavioral change)**
  - Default JSON encoding is now more compact; tests asserting exact JSON bytes may need updates.
  - If you need stable formatting, pre-serialize and send via `content=` with an explicit `content-type`.

## Pitfalls

### Wrong: Using top-level `httpx.get()` in a loop (no pooling)
```python
import httpx

def download_many() -> None:
    for _ in range(10):
        httpx.get("https://httpbin.org/get").raise_for_status()

if __name__ == "__main__":
    download_many()
```

### Right: Reuse a `httpx.Client()` for pooling
```python
import httpx

def download_many() -> None:
    with httpx.Client() as client:
        for _ in range(10):
            client.get("https://httpbin.org/get").raise_for_status()

if __name__ == "__main__":
    download_many()
```

### Wrong: Forgetting to close a `httpx.Client()`
```python
import httpx

def fetch_once() -> int:
    client = httpx.Client()
    r = client.get("https://httpbin.org/status/200")
    r.raise_for_status()
    return r.status_code  # client.close() never called

if __name__ == "__main__":
    print(fetch_once())
```

### Right: Use a context manager (or call `client.close()`)
```python
import httpx

def fetch_once() -> int:
    with httpx.Client() as client:
        r = client.get("https://httpbin.org/status/200")
        r.raise_for_status()
        return r.status_code

if __name__ == "__main__":
    print(fetch_once())
```

### Wrong: Using removed `proxies=` argument (0.28+) ⚠️
```python
import httpx

def build_client() -> httpx.Client:
    return httpx.Client(proxies={"https": "http://proxy.local:8080"})  # removed in 0.28.0

if __name__ == "__main__":
    build_client()
```

### Right: Use `proxy=` (or `mounts=` for complex routing)
```python
import httpx

def build_client() -> httpx.Client:
    return httpx.Client(proxy="http://proxy.local:8080")

if __name__ == "__main__":
    with build_client() as client:
        print(client.get("https://httpbin.org/get").status_code)
```

### Wrong: Custom `httpx.Auth.auth_flow()` doing async/non-HTTP I/O
```python
import asyncio
import httpx

async def get_token() -> str:
    await asyncio.sleep(0)
    return "token"

class TokenAuth(httpx.Auth):
    def auth_flow(self, request: httpx.Request):
        # BAD: running async I/O inside a sync generator.
        token = asyncio.get_event_loop().run_until_complete(get_token())
        request.headers["Authorization"] = f"Bearer {token}"
        yield request

def main() -> None:
    with httpx.Client(auth=TokenAuth()) as client:
        client.get("https://httpbin.org/get")

if __name__ == "__main__":
    main()
```

### Right: Provide `sync_auth_flow()` and `async_auth_flow()`
```python
import asyncio
import threading
import httpx

class TokenAuth(httpx.Auth):
    def __init__(self) -> None:
        self._sync_lock = threading.RLock()
        self._async_lock = asyncio.Lock()

    def _sync_get_token(self) -> str:
        with self._sync_lock:
            return "token"

    def sync_auth_flow(self, request: httpx.Request):
        token = self._sync_get_token()
        request.headers["Authorization"] = f"Bearer {token}"
        yield request

    async def _async_get_token(self) -> str:
        async with self._async_lock:
            await asyncio.sleep(0)
            return "token"

    async def async_auth_flow(self, request: httpx.Request):
        token = await self._async_get_token()
        request.headers["Authorization"] = f"Bearer {token}"
        yield request

def main() -> None:
    with httpx.Client(auth=TokenAuth()) as client:
        client.get("https://httpbin.org/get").raise_for_status()

if __name__ == "__main__":
    main()
```

## References

- [Changelog](https://github.com/encode/httpx/blob/master/CHANGELOG.md)
- [Documentation](https://www.python-httpx.org)
- [Homepage](https://github.com/encode/httpx)
- [Source](https://github.com/encode/httpx)

## Migration from v0.27.x

### `proxies=` argument removed 🗑️ Removed
- Deprecated since: 0.26.0 (deprecated), removed in 0.28.0  
- Still works: false  
- Modern alternative: `proxy=` for simple cases, or `mounts=` for complex routing  
- Migration guidance:
```python
import httpx

# Before (0.27.x and earlier; removed in 0.28.0)
# client = httpx.Client(proxies={"https": "http://proxy.local:8080"})

# After (0.28.0+)
with httpx.Client(proxy="http://proxy.local:8080") as client:
    r = client.get("https://httpbin.org/get")
    print(r.status_code)
```

### `app=` shortcut removed 🗑️ Removed
- Deprecated since: 0.27.0, removed in 0.28.0  
- Still works: false  
- Modern alternative: `transport=httpx.ASGITransport(app=...)` or `transport=httpx.WSGITransport(app=...)`  
- Migration guidance:
```python
import httpx

async def asgi_app(scope, receive, send) -> None:
    await send({"type": "http.response.start", "status": 204, "headers": []})
    await send({"type": "http.response.body", "body": b""})

# Before (removed in 0.28.0)
# client = httpx.AsyncClient(app=asgi_app)

# After
transport = httpx.ASGITransport(app=asgi_app)
```

### JSON request formatting changed ✅ Current (behavioral change in 0.28.0)
- Still works: true (but output bytes may differ)
- Modern alternative: if you require stable JSON bytes, pre-serialize and send via `content=...` with a JSON content-type.
```python
import json
import httpx

def post_stable_json(url: str, payload: dict) -> int:
    body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    headers = {"content-type": "application/json"}
    r = httpx.request("POST", url, content=body, headers=headers)
    return r.status_code

if __name__ == "__main__":
    print(post_stable_json("https://httpbin.org/post", {"b": 1, "a": 2}))
```

### SSL arguments deprecated ⚠️
- Deprecated since: 0.28.0
- Passing a string path to `verify` or using the `cert` argument is deprecated and will issue warnings.
- Modern alternative: Use `verify=True`, `verify=False`, or `verify=<ssl.SSLContext>`. See new SSL configuration docs for details.

## API Reference

- **httpx.get(url, \*\*kwargs)** - Convenience GET request; returns `httpx.Response`.
- **httpx.request(method, url, \*\*kwargs)** - Generic request entry point for one-off calls.
- **httpx.Client(\*\*kwargs)** - Sync client with connection pooling and shared config (auth, proxy, transport, etc.).
- **Client.get(url, \*\*kwargs)** - Sync GET using the client’s configuration.
- **Client.request(method, url, \*\*kwargs)** - Generic sync request method on a client.
- **Client.close()** - Close the client and release network resources (use context managers instead when possible).
- **httpx.AsyncClient(\*\*kwargs)** - Async client; use with `async with` and `await`.
- **httpx.Response** - Response object (status, headers, body accessors).
- **Response.raise_for_status()** - Raise an exception on 4xx/5xx; returns the response (can be chained).
- **Response.json()** - Parse response body as JSON.
- **Response.iter_text()** - Stream response body as decoded text chunks.
- **httpx.BasicAuth(username, password)** - HTTP Basic authentication.
- **httpx.DigestAuth(username, password)** - HTTP Digest authentication.
- **httpx.NetRCAuth(file=None)** - Auth from `.netrc` (optionally specify file).
- **httpx.Auth** - Base class for custom auth; implement `auth_flow()` or `sync_auth_flow()`/`async_auth_flow()`.
- **httpx.FunctionAuth(callable)** - Wrap a callable as an auth implementation.
- **httpx.WSGITransport(app=...)** - Transport for calling a WSGI app in-process.
- **httpx.ASGITransport(app=...)** - Transport for calling an ASGI app in-process.
- **httpx.HTTPTransport(...)** - Low-level sync transport configuration (advanced).
- **httpx.AsyncHTTPTransport(...)** - Low-level async transport configuration (advanced).
- **httpx.InvalidURL** - Exception raised for invalid URL inputs.

---

**Security Note:**  
All examples are designed for use within your own project directory and for safe, local development or controlled network requests. Never use these patterns to transmit, modify, or access data outside your intended project or environment. Do not copy/paste code into environments where you lack permission or understanding of the security implications.