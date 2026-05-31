---
name: httpx
description: A next-generation HTTP client for Python with both sync and async support, perfect for modern Python applications
when_to_use: Use when you need to make HTTP requests in Python, especially with async/await, streaming, or advanced authentication
---

# HTTPX Skill

HTTPX is a fully featured HTTP client for Python that provides both synchronous and asynchronous APIs, with support for HTTP/1.1 and HTTP/2.

## Quick Start

### Basic Usage

```python
import httpx

# Simple GET request
response = httpx.get('https://api.example.com/data')
print(response.status_code)
print(response.json())

# POST request with JSON data
response = httpx.post('https://api.example.com/users', json={'name': 'Alice'})
```

### Async Usage

```python
import asyncio
import httpx

async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://api.example.com/data')
        return response.json()

result = asyncio.run(fetch_data())
```

## Common Patterns

### 1. Async Client with Connection Pooling

```python
import httpx

async def make_multiple_requests():
    async with httpx.AsyncClient() as client:
        # Reuse the same client for multiple requests
        tasks = [
            client.get('https://api.example.com/users/1'),
            client.get('https://api.example.com/users/2'),
            client.get('https://api.example.com/users/3')
        ]
        responses = await asyncio.gather(*tasks)
        return [r.json() for r in responses]
```

### 2. Authentication

```python
import httpx

# Basic Authentication
auth = httpx.BasicAuth(username='user', password='pass')
client = httpx.Client(auth=auth)

# Bearer Token Authentication
headers = {'Authorization': 'Bearer your-token-here'}
client = httpx.Client(headers=headers)

# Per-request authentication
response = client.get('https://api.example.com', auth=('user', 'pass'))
```

### 3. Streaming Downloads

```python
import httpx

# Stream large files without loading into memory
with httpx.stream('GET', 'https://example.com/large-file.zip') as response:
    with open('large-file.zip', 'wb') as f:
        for chunk in response.iter_bytes():
            f.write(chunk)

# Async streaming
async def download_large_file():
    async with httpx.AsyncClient() as client:
        async with client.stream('GET', 'https://example.com/large-file.zip') as response:
            with open('large-file.zip', 'wb') as f:
                async for chunk in response.aiter_bytes():
                    f.write(chunk)
```

### 4. Streaming Uploads

```python
import httpx

# Upload large files with streaming
async def upload_large_file():
    def generate_data():
        # Yield chunks of data
        for i in range(100):
            yield f'chunk {i}\n'.encode()

    async with httpx.AsyncClient() as client:
        response = await client.post(
            'https://api.example.com/upload',
            content=generate_data()
        )
        return response
```

### 5. Error Handling and Timeouts

```python
import httpx

# Configure timeouts
client = httpx.Client(
    timeout=httpx.Timeout(10.0, connect=5.0, read=8.0)
)

try:
    response = client.get('https://api.example.com/slow')
    response.raise_for_status()  # Raise exception for 4XX/5XX responses
except httpx.TimeoutException:
    print("Request timed out")
except httpx.HTTPStatusError as e:
    print(f"HTTP error: {e.response.status_code}")
except httpx.RequestError as e:
    print(f"Request failed: {e}")
```

### 6. Client Configuration

```python
import httpx

# Client with shared configuration
client = httpx.Client(
    base_url='https://api.example.com',
    headers={'User-Agent': 'MyApp/1.0'},
    timeout=30.0,
    follow_redirects=True
)

# All requests will use base_url and headers
response = client.get('/users')  # Makes request to https://api.example.com/users
```

### 7. Custom Authentication

```python
import httpx

class CustomAuth(httpx.Auth):
    def __init__(self, api_key):
        self.api_key = api_key

    def auth_flow(self, request):
        request.headers['X-API-Key'] = self.api_key
        yield request

# Use custom auth
auth = CustomAuth('your-secret-api-key')
client = httpx.Client(auth=auth)
```

### 8. Progress Monitoring

```python
import httpx
from tqdm import tqdm

def download_with_progress(url, filename):
    with httpx.stream('GET', url) as response:
        total = int(response.headers.get('content-length', 0))

        with tqdm(total=total, unit='B', unit_scale=True) as progress:
            with open(filename, 'wb') as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)
                    progress.update(len(chunk))
```

### 9. Retry Logic

```python
import httpx
import time

def make_request_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = httpx.get(url, timeout=10.0)
            response.raise_for_status()
            return response
        except httpx.RequestError as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

### 10. WebSocket Support (with httpx-ws)

```python
import httpx
from httpx_ws import connect_ws

async def websocket_example():
    async with httpx.AsyncClient() as client:
        async with connect_ws('wss://echo.websocket.org', client) as websocket:
            await websocket.send_text('Hello, WebSocket!')
            message = await websocket.receive_text()
            print(f"Received: {message}")
```

## Practical Code Snippets

### API Client Class

```python
import httpx
from typing import Optional, Dict, Any

class APIClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.client = httpx.Client(
            base_url=base_url,
            headers={'Authorization': f'Bearer {api_key}'},
            timeout=30.0
        )

    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[Any, Any]:
        response = self.client.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, data: Dict[Any, Any]) -> Dict[Any, Any]:
        response = self.client.post(endpoint, json=data)
        response.raise_for_status()
        return response.json()

    def close(self):
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

# Usage
with APIClient('https://api.example.com', 'your-api-key') as client:
    users = client.get('/users')
    new_user = client.post('/users', {'name': 'John', 'email': 'john@example.com'})
```

### Async API Client

```python
import httpx
from typing import Optional, Dict, Any

class AsyncAPIClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(
            base_url=base_url,
            headers={'Authorization': f'Bearer {api_key}'},
            timeout=30.0
        )

    async def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[Any, Any]:
        response = await self.client.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    async def close(self):
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

# Usage
async def main():
    async with AsyncAPIClient('https://api.example.com', 'your-api-key') as client:
        users = await client.get('/users')
        print(users)
```

## Requirements

```txt
httpx>=0.24.0
# Optional dependencies for additional features:
# httpx-ws>=0.6.0  # WebSocket support
# tqdm>=4.65.0     # Progress bars
# anyio>=3.7.0     # Alternative async runtime
# trio>=0.22.0     # Alternative async runtime
```

## Key Features

- **Sync and Async APIs**: Same interface for both synchronous and asynchronous code
- **HTTP/2 Support**: Full HTTP/2 support with multiplexing
- **Connection Pooling**: Efficient connection management
- **Streaming**: Stream requests and responses without loading everything into memory
- **Authentication**: Built-in support for Basic, Digest, Bearer token, and custom auth
- **Timeouts**: Configurable timeouts for connect, read, and overall requests
- **Redirect Handling**: Configurable redirect following
- **Cookie Handling**: Automatic cookie management
- **Proxy Support**: HTTP and HTTPS proxy support
- **SSL/TLS**: Full SSL/TLS configuration options

## Installation

```bash
uv add httpx

# For HTTP/2 support
uv add httpx[http2]

# For WebSocket support
uv add httpx-ws
```

This skill provides comprehensive HTTP client capabilities for modern Python applications, with excellent async support and production-ready features.
