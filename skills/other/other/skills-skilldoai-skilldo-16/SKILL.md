---
name: aiohttp
description: Async HTTP client/server framework for asyncio, providing ClientSession for outbound HTTP and aiohttp.web for building web servers.
version: 3.13.3
ecosystem: python
license: MIT
generated_with: gpt-5.2
---

## Imports

```python
import asyncio
import aiohttp
from aiohttp import TraceConfig, web
from aiohttp.test_utils import (
    AioHTTPTestCase,
    TestClient,
    TestServer,
    make_mocked_request,
    unused_port,
)
```

## Core Patterns

### HTTP client request with `ClientSession` ✅ Current
```python
import asyncio
import aiohttp


async def main() -> None:
    url = "https://example.com/"
    timeout = aiohttp.ClientTimeout(total=10)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url, headers={"Accept": "text/html"}) as resp:
            resp.raise_for_status()
            body = await resp.text()
            print(resp.status, len(body))


if __name__ == "__main__":
    asyncio.run(main())
```
* Use `async with aiohttp.ClientSession()` to ensure the connector and sockets are closed.
* Use `async with session.get(...) as resp` to ensure the response is released back to the connection pool.

### Client tracing with `TraceConfig` ✅ Current
```python
import asyncio
import time
from types import SimpleNamespace

import aiohttp
from aiohttp import TraceConfig


async def on_request_start(
    session: aiohttp.ClientSession,
    context: SimpleNamespace,
    params: aiohttp.TraceRequestStartParams,
) -> None:
    context.t0 = time.perf_counter()
    print("->", params.method, params.url)


async def on_request_end(
    session: aiohttp.ClientSession,
    context: SimpleNamespace,
    params: aiohttp.TraceRequestEndParams,
) -> None:
    dt = time.perf_counter() - context.t0
    print("<-", params.response.status, f"{dt:.3f}s")


async def main() -> None:
    trace_config = TraceConfig(trace_config_ctx_factory=SimpleNamespace)
    trace_config.on_request_start.append(on_request_start)
    trace_config.on_request_end.append(on_request_end)

    async with aiohttp.ClientSession(trace_configs=[trace_config]) as session:
        # Per-request context can be passed via trace_request_ctx
        async with session.get(
            "https://example.com/",
            trace_request_ctx={"request_id": "req-1"},
        ) as resp:
            await resp.read()


if __name__ == "__main__":
    asyncio.run(main())
```
* Trace callbacks are `async def on_signal(session, context, params)`; `context` comes from `TraceConfig.trace_config_ctx_factory`.
* Use `trace_request_ctx=...` to pass per-request metadata into `context` (available via `TraceConfig.trace_config_ctx(...)` internally).

### Web server routes + WebSocket handler (`aiohttp.web`) ✅ Current
```python
import asyncio
from aiohttp import web


async def index(request: web.Request) -> web.Response:
    return web.Response(text="ok")


async def websocket_echo(request: web.Request) -> web.WebSocketResponse:
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            await ws.send_str(msg.data)
        elif msg.type == web.WSMsgType.BINARY:
            await ws.send_bytes(msg.data)
        else:
            break

    return ws


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/", index)
    app.router.add_get("/ws", websocket_echo)
    return app


async def main() -> None:
    app = create_app()
    web.run_app(app, host="127.0.0.1", port=8080)


if __name__ == "__main__":
    asyncio.run(main())
```
* Handlers are `async def handler(request: web.Request) -> web.StreamResponse`.
* WebSocket pattern: `WebSocketResponse()` → `await ws.prepare(request)` → `async for msg in ws` → `await ws.send_*`.

### Async integration testing with `TestServer` + `TestClient` ✅ Current
```python
import asyncio
from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer


async def hello(request: web.Request) -> web.Response:
    return web.Response(text="hello")


async def main() -> None:
    app = web.Application()
    app.router.add_get("/", hello)

    async with TestServer(app) as server:
        async with TestClient(server) as client:
            async with client.get("/") as resp:
                text = await resp.text()
                print(resp.status, text)


if __name__ == "__main__":
    asyncio.run(main())
```
* `async with TestServer(app)` calls `start_server()` and `close()` automatically.
* `TestClient` tracks created responses and websockets and closes them on `client.close()`.

### Unit-test request object creation with `make_mocked_request` ✅ Current
```python
from aiohttp import hdrs, web
from aiohttp.test_utils import make_mocked_request


def build_request() -> web.Request:
    app = web.Application()
    req = make_mocked_request(
        "GET",
        "/",
        headers={hdrs.HOST: "example.com"},
        match_info={"id": "1"},
        app=app,
    )
    return req


if __name__ == "__main__":
    r = build_request()
    print(r.method, r.path, r.headers.get(hdrs.HOST), r.match_info["id"])
```
* Produces an `aiohttp.web.Request` suitable for unit-testing handlers/middleware without a real server.

### Client middlewares for request preprocessing ✅ Current
```python
import asyncio
from typing import Union

import aiohttp
from aiohttp import ClientHandlerType, ClientRequest, ClientResponse, hdrs


class TokenRefreshMiddleware:
    def __init__(self, token_endpoint: str, refresh_token: str) -> None:
        self.token_endpoint = token_endpoint
        self.refresh_token = refresh_token
        self.access_token: Union[str, None] = None
        self._refresh_lock = asyncio.Lock()

    async def _refresh_access_token(self, session: aiohttp.ClientSession) -> None:
        async with self._refresh_lock:
            # Refresh logic here - disable middlewares to avoid recursion
            async with session.post(
                self.token_endpoint,
                json={"refresh_token": self.refresh_token},
                middlewares=(),  # Disable middleware for this request
            ) as resp:
                resp.raise_for_status()
                data = await resp.json()
                self.access_token = data["access_token"]

    async def __call__(
        self,
        request: ClientRequest,
        handler: ClientHandlerType,
    ) -> ClientResponse:
        if not self.access_token:
            await self._refresh_access_token(request.session)
        request.headers[hdrs.AUTHORIZATION] = f"Bearer {self.access_token}"
        response = await handler(request)
        if response.status == 401:
            await self._refresh_access_token(request.session)
            request.headers[hdrs.AUTHORIZATION] = f"Bearer {self.access_token}"
            response = await handler(request)
        return response


async def main() -> None:
    token_middleware = TokenRefreshMiddleware(
        "http://localhost:8080/token", "refresh_token_value"
    )
    async with aiohttp.ClientSession(middlewares=(token_middleware,)) as session:
        async with session.get("http://localhost:8080/api/protected") as resp:
            data = await resp.json()
            print(data)


if __name__ == "__main__":
    asyncio.run(main())
```
* Middlewares have signature: `async def __call__(request: ClientRequest, handler: ClientHandlerType) -> ClientResponse`.
* Use `middlewares=()` on individual requests to disable session middlewares (prevents recursion).
* Client middlewares allow automatic token refresh, authentication injection, retry logic, etc.

### Application lifecycle with `cleanup_ctx` ✅ Current
```python
import asyncio
from contextlib import suppress
from typing import AsyncIterator

from aiohttp import web


async def background_task(app: web.Application) -> None:
    while True:
        await asyncio.sleep(1)
        print("Background task running...")


async def background_tasks(app: web.Application) -> AsyncIterator[None]:
    # Startup: create background task
    task = asyncio.create_task(background_task(app))

    yield  # Application is running

    # Cleanup: cancel and await task
    print("Cleaning up background tasks...")
    task.cancel()
    with suppress(asyncio.CancelledError):
        await task


async def handler(request: web.Request) -> web.Response:
    return web.Response(text="ok")


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/", handler)
    app.cleanup_ctx.append(background_tasks)
    return app


if __name__ == "__main__":
    app = create_app()
    web.run_app(app, host="127.0.0.1", port=8080)
```
* `cleanup_ctx` accepts async generators: code before `yield` runs on startup, code after runs on cleanup.
* Use this pattern for database connections, background tasks, or other resources tied to app lifecycle.

### Type-safe application state with `AppKey` ✅ Current
```python
from typing import List

from aiohttp import web

# Define a typed key for storing WebSocket connections
sockets_key = web.AppKey("sockets", List[web.WebSocketResponse])


async def websocket_handler(request: web.Request) -> web.WebSocketResponse:
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    # Type-safe access to app state
    request.app[sockets_key].append(ws)

    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                # Broadcast to all connected clients
                for other_ws in request.app[sockets_key]:
                    await other_ws.send_str(f"Broadcast: {msg.data}")
    finally:
        request.app[sockets_key].remove(ws)

    return ws


def create_app() -> web.Application:
    app = web.Application()
    app[sockets_key] = []  # Initialize state
    app.router.add_get("/ws", websocket_handler)
    return app
```
* `AppKey("name", Type)` provides type-safe application state storage.
* Helps catch type errors with mypy/pyright and provides better IDE autocomplete.

## Configuration

* **Client timeouts**: configure via `aiohttp.ClientTimeout(total=..., connect=..., sock_read=..., sock_connect=...)` and pass to `ClientSession(timeout=...)`.
* **Tracing**: `TraceConfig(trace_config_ctx_factory=...)`, attach callbacks to signals like `on_request_start`, `on_request_end`, `on_request_exception`, DNS/connection events, etc.
* **Web app**: create `web.Application()` and register routes via `app.router.add_get(...)` (and other HTTP methods).
* **Testing ports**: `aiohttp.test_utils.unused_port()` returns an available port for tests (best-effort; still subject to race conditions).
* **Test client cookie jar**: `TestClient` uses an internal `ClientSession` with `CookieJar(unsafe=True)` by default (test-friendly behavior).
* **Client middlewares**: pass tuple of middleware callables to `ClientSession(middlewares=...)` for request preprocessing.
* **Brotli decompression**: default maximum output size is **32 MiB per decompress call** (requires Brotli/brotlicffi >= 1.2).

## Pitfalls

### Wrong: leaking connections by not closing `ClientSession` / response
```python
import asyncio
import aiohttp


async def main() -> None:
    session = aiohttp.ClientSession()
    resp = await session.get("https://example.com/")
    _ = await resp.text()
    # forgot: await resp.release() / resp.close()
    # forgot: await session.close()


if __name__ == "__main__":
    asyncio.run(main())
```

### Right: use async context managers for both session and response
```python
import asyncio
import aiohttp


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://example.com/") as resp:
            _ = await resp.text()


if __name__ == "__main__":
    asyncio.run(main())
```

### Wrong: forgetting `await` in WebSocket handshake and sends
```python
from aiohttp import web


async def websocket_handler(request: web.Request) -> web.WebSocketResponse:
    ws = web.WebSocketResponse()
    ws.prepare(request)  # missing await

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            ws.send_str(msg.data)  # missing await
    return ws
```

### Right: await `prepare()` and `send_*()` calls
```python
from aiohttp import web


async def websocket_handler(request: web.Request) -> web.WebSocketResponse:
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            await ws.send_str(msg.data)
    return ws
```

### Wrong: `TestServer.make_url()` with an absolute URL/path
```python
import asyncio
from aiohttp import web
from aiohttp.test_utils import TestServer


async def handler(request: web.Request) -> web.Response:
    return web.Response(text="ok")


async def main() -> None:
    app = web.Application()
    app.router.add_get("/", handler)

    async with TestServer(app) as server:
        # make_url expects a relative path (e.g., "/"), not a full URL
        server.make_url("http://example.com/")  # may assert/fail


if __name__ == "__main__":
    asyncio.run(main())
```

### Right: pass a relative path to `make_url()`
```python
import asyncio
from aiohttp import web
from aiohttp.test_utils import TestServer


async def handler(request: web.Request) -> web.Response:
    return web.Response(text="ok")


async def main() -> None:
    app = web.Application()
    app.router.add_get("/", handler)

    async with TestServer(app) as server:
        url = server.make_url("/")
        print(url)


if __name__ == "__main__":
    asyncio.run(main())
```

### Wrong: assuming Unicode regex routes match raw Unicode (requoting mismatch)
```python
# This is illustrative: aiohttp requotes paths internally.
# If you rely on custom regex patterns for Unicode segments, they may not match as expected.
from aiohttp import web


async def handler(request: web.Request) -> web.Response:
    return web.Response(text="matched")


def create_app() -> web.Application:
    app = web.Application()
    # Risky if you expect raw Unicode matching; aiohttp matches against requoted/percent-encoded paths.
    app.router.add_get(r"/{name:[А-Яа-я]+}", handler)
    return app
```

### Right: prefer non-regex variable routes or match encoded form
```python
from aiohttp import web


async def handler(request: web.Request) -> web.Response:
    # Treat as text after aiohttp routing; avoid relying on raw-Unicode regex matching.
    name = request.match_info["name"]
    return web.Response(text=f"hello {name}")


def create_app() -> web.Application:
    app = web.Application()
    # Prefer a simple variable route unless you must enforce a regex.
    app.router.add_get(r"/{name}", handler)
    return app
```

### Wrong: client middleware causing infinite recursion
```python
import aiohttp
from aiohttp import ClientHandlerType, ClientRequest, ClientResponse


class BrokenMiddleware:
    async def __call__(
        self, request: ClientRequest, handler: ClientHandlerType
    ) -> ClientResponse:
        # This middleware makes another request, which triggers the middleware again
        async with request.session.get("http://localhost:8080/refresh") as resp:
            token = await resp.text()
        request.headers["Authorization"] = f"Bearer {token}"
        return await handler(request)
```

### Right: disable middlewares for requests within middleware
```python
import aiohttp
from aiohttp import ClientHandlerType, ClientRequest, ClientResponse


class CorrectMiddleware:
    async def __call__(
        self, request: ClientRequest, handler: ClientHandlerType
    ) -> ClientResponse:
        # Disable middlewares to avoid recursion
        async with request.session.get(
            "http://localhost:8080/refresh", middlewares=()
        ) as resp:
            token = await resp.text()
        request.headers["Authorization"] = f"Bearer {token}"
        return await handler(request)
```

### Wrong: forgetting to await response methods
```python
import asyncio
import aiohttp


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://example.com/") as resp:
            text = resp.text()  # Returns coroutine, not string!
            print(text)


if __name__ == "__main__":
    asyncio.run(main())
```

### Right: await all async response methods
```python
import asyncio
import aiohttp


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://example.com/") as resp:
            text = await resp.text()
            print(text)


if __name__ == "__main__":
    asyncio.run(main())
```

## References

- [Homepage](https://github.com/aio-libs/aiohttp)
- [Chat: Matrix](https://matrix.to/#/#aio-libs:matrix.org)
- [Chat: Matrix Space](https://matrix.to/#/#aio-libs-space:matrix.org)
- [CI: GitHub Actions](https://github.com/aio-libs/aiohttp/actions?query=workflow%3ACI)
- [Coverage: codecov](https://codecov.io/github/aio-libs/aiohttp)
- [Docs: Changelog](https://docs.aiohttp.org/en/stable/changes.html)
- [Docs: RTD](https://docs.aiohttp.org)
- [GitHub: issues](https://github.com/aio-libs/aiohttp/issues)
- [GitHub: repo](https://github.com/aio-libs/aiohttp)

## Migration from v3.13.2 to v3.13.3

* ✅ Current: upgrade recommended (3.13.3 includes security/vulnerability fixes).
* **Brotli/brotlicffi minimum version**: now requires `Brotli>=1.2` or `brotlicffi>=1.2`.
* **Brotli decompression limit**: default maximum output size is **32 MiB per decompress call**.
  * Migration guidance: if you process very large Brotli payloads, prefer streaming reads (`async for chunk in resp.content.iter_chunked(...)`) and incremental processing rather than expecting a single huge in-memory decompression result.
* **Packaging note**: project metadata moved from `setup.cfg` to `pyproject.toml` (update any tooling that parses `setup.cfg`).
* **Proxy auth behavior fix**: proxy authorization headers are now correctly passed on connection reuse; re-test and remove workarounds for 407 Proxy Authentication Required errors if present.
* **Cookie parser improvement**: malformed cookies no longer break parsing; parser continues with remaining cookies.
* **Content-Type header handling**: invalid Content-Type headers now return `'application/octet-stream'` per RFC 9110 instead of raising exceptions.
* **WebSocket safety**: compressed WebSocket sends are now cancellation-safe with task shielding.
* **Multipart fixes**: multipart reading no longer fails with empty body parts.

### Security Fixes in 3.13.x Series
* Proxy authorization headers not being passed on connection reuse (CVE-related)
* WebSocket continuation frame parsing without initial frame context
* Multiple improvements to parsing robustness and error handling

## API Reference

### Client APIs
- **aiohttp.ClientSession(**\*, timeout=None, trace_configs=None, headers=None, raise_for_status=False, connector=None, cookie_jar=None, middlewares=None**)** - HTTP client session managing connection pooling, cookies, and middlewares.
- **aiohttp.ClientSession.get(url, \*\*kwargs)** / **post(...)** / **request(method, url, \*\*kwargs)** - Perform HTTP requests; use as `async with session.get(...) as resp:`.
- **aiohttp.ClientSession.ws_connect(url, \*\*kwargs)** - Connect to a WebSocket server; returns `ClientWebSocketResponse`.
- **aiohttp.ClientResponse.text(encoding=None, errors="strict")** - Read response body decoded as text.
- **aiohttp.ClientResponse.json(\*\*kwargs)** - Read and parse response body as JSON.
- **aiohttp.ClientResponse.read()** - Read response body as bytes.
- **aiohttp.ClientResponse.raise_for_status()** - Raise an exception for 4xx/5xx responses.
- **aiohttp.ClientTimeout(total=None, connect=None, sock_read=None, sock_connect=None)** - Timeout configuration for requests.
- **aiohttp.ClientWebSocketResponse** - Client-side WebSocket connection with send/receive methods.
- **aiohttp.request(method, url, \*\*kwargs)** - Convenience function for one-off HTTP requests without explicit session.

### Tracing APIs
- **aiohttp.TraceConfig(trace_config_ctx_factory=types.SimpleNamespace)** - Configure client tracing hooks.
- **aiohttp.TraceConfig.on_request_start / on_request_end / on_request_exception / on_dns_resolvehost_start / on_connection_create_start / ...** - Signals (lists) to append async callbacks to.
- **aiohttp.TraceRequestStartParams** / **TraceRequestEndParams** / **TraceRequestExceptionParams** / etc. - Parameter objects passed to trace callbacks.

### Web Server APIs
- **aiohttp.web.Application()** - Web application container; holds router and app state.
- **aiohttp.web.Request** - Incoming HTTP request object with headers, query params, body, etc.
- **aiohttp.web.Response(text=None, body=None, status=200, headers=None, content_type=None)** - Basic HTTP response.
- **aiohttp.web.json_response(data, \*\*kwargs)** - Convenience function to return JSON response.
- **aiohttp.web.WebSocketResponse()** - WebSocket server response; call `await prepare(request)` then send/receive messages.
- **aiohttp.web.WSMsgType** - Enum of websocket message types (e.g., `TEXT`, `BINARY`, `CLOSE`, `PING`, `PONG`).
- **aiohttp.web.WSCloseCode** - Enum of WebSocket close codes.
- **aiohttp.web.run_app(app, host=None, port=None, \*\*kwargs)** - Run an `Application` (blocking call; typically top-level).
- **aiohttp.web.get(path, handler, \*\*kwargs)** - Route helper/decorator for GET (also available via `app.router.add_get`).
- **aiohttp.web.AppKey(name, type)** - Type-safe key for storing application state.

### Connection Management
- **aiohttp.TCPConnector(**\*, limit=100, limit_per_host=30, resolver=None, verify_ssl=True, \*\*kwargs**)** - TCP connection pooling and management.
- **aiohttp.UnixConnector(path, \*\*kwargs)** - Unix socket connector for local communication.
- **aiohttp.NamedPipeConnector(path, \*\*kwargs)** - Windows named pipe connector (Windows only).

### Authentication
- **aiohttp.BasicAuth(login, password="", encoding="latin1")** - HTTP Basic authentication helper; pass to `auth=` parameter.
- **aiohttp.DigestAuthMiddleware(username, password)** - HTTP Digest authentication client middleware.

### Cookies
- **aiohttp.CookieJar(**\*, quote_cookie=True, treat_as_secure_origin=None**)** - Cookie storage and management.
- **aiohttp.DummyCookieJar()** - Cookie jar that ignores all cookies (for testing).

### Multipart/Form Data
- **aiohttp.FormData(fields=(), quote_fields=True, charset=None)** - Multipart form data builder for file uploads.
- **aiohttp.MultipartReader(...)** - Multipart response body reader.
- **aiohttp.MultipartWriter(subtype="mixed", boundary=None)** - Multipart request body writer.
- **aiohttp.BodyPartReader** - Individual part reader within multipart response.

### Payloads
- **aiohttp.Payload** - Base payload class.
- **aiohttp.BytesPayload(value)** - Bytes payload.
- **aiohttp.StringPayload(value, encoding="utf-8", content_type="text/plain")** - String payload.
- **aiohttp.JsonPayload(value, dumps=json.dumps)** - JSON payload.
- **aiohttp.AsyncIterablePayload** - Async iterable payload for streaming.
- **aiohttp.IOBasePayload** - File-like object payload.
- **aiohttp.streamer(func)** - Decorator for creating streaming payloads.

### Testing Utilities
- **aiohttp.test_utils.TestServer(app, host="127.0.0.1", port=0, scheme="")** - Test server wrapper; `await start_server()`, `make_url(path)`, `await close()`, supports `async with`.
- **aiohttp.test_utils.TestClient(server)** - Test client bound to a `TestServer`; `.get()/.post()/.request()` and `.ws_connect()`; supports `async with`.
- **aiohttp.test_utils.AioHTTPTestCase** - unittest-based test case with automatic client/server setup via `get_application()` method.
- **aiohttp.test_utils.make_mocked_request(method, path, \*\*kwargs)** - Create mocked `web.Request` for unit testing without server.
- **aiohttp.test_utils.unused_port()** - Get an unused port number for testing (best-effort).

### Exceptions
- **aiohttp.ClientError** - Base exception for client errors.
- **aiohttp.ClientConnectionError** - Connection error exception.
- **aiohttp.ClientResponseError** - HTTP response error exception (4xx/5xx).
- **aiohttp.ContentTypeError** - Invalid content type exception.
- **aiohttp.InvalidURL** - Invalid URL exception.
- **aiohttp.WebSocketError** - WebSocket error exception.

### DNS Resolvers
- **aiohttp.DefaultResolver()** - Default DNS resolver using getaddrinfo.
- **aiohttp.AsyncResolver()** - Async DNS resolver using aiodns (requires aiodns package).
- **aiohttp.ThreadedResolver()** - Threaded DNS resolver for blocking resolution.

### HTTP Constants
- **aiohttp.HttpVersion** / **HttpVersion10** / **HttpVersion11** - HTTP version representation constants.
- **aiohttp.hdrs** - Module containing HTTP header constants (e.g., `hdrs.AUTHORIZATION`, `hdrs.CONTENT_TYPE`).

## Current Library State

### Key Features
* **Async/await native**: Built from ground up for asyncio with proper async context management.
* **Client & Server**: Full-featured HTTP client with `ClientSession` and web framework with `aiohttp.web`.
* **WebSockets**: Both client and server WebSocket support with proper message type handling.
* **Middlewares**: Client-side middleware support for request preprocessing (new in 3.13+).
* **Type safety**: `AppKey` for type-safe application state; extensive type hints throughout.
* **Testing utilities**: Comprehensive test utilities including `TestServer`, `TestClient`, and `make_mocked_request`.
* **Connection pooling**: Efficient connection reuse with configurable limits per host.
* **Tracing**: Detailed request lifecycle tracing for debugging and monitoring.
* **Streaming**: Support for streaming uploads/downloads with async iterables.
* **Security**: Regular security updates; 3.13.3 includes multiple CVE fixes.

### Conventions
* Use `async with` context managers for `ClientSession` and HTTP method calls.
* Use `await` with all async methods like `response.text()`, `response.json()`, `ws.send_str()`.
* Use `asyncio.run()` to execute async main functions (don't manage loops manually).
* WebSocket responses must call `await ws.prepare(request)` before processing messages.
* Iterate over WebSocket messages using `async for msg in ws`.
* Check message type using `web.WSMsgType` enum before processing.
* Signal handlers have signature: `async def on_signal(session, context, params)`.
* Client middlewares have signature: `async def __call__(request: ClientRequest, handler: ClientHandlerType) -> ClientResponse`.
* URL paths are automatically requoted to percent-encoding form.
* Use `middlewares=()` to disable session middlewares for specific requests.