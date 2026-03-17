---

name: fastapi
description: FastAPI is a modern, high-performance Python web framework for building APIs with automatic validation, documentation, and async support.
version: 0.133.1
ecosystem: python
license: MIT
generated_with: gpt-4.1
---

## Imports

```python
import fastapi
from fastapi import FastAPI, APIRouter, Request, Response, HTTPException, status
from fastapi import Depends, Body, Query, Path, Header, Cookie, Form, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer, HTTPBasic
```

## Core Patterns

### Creating a FastAPI application ✅ Current
```python
from fastapi import FastAPI

app = FastAPI(title="My API", version="1.0.0", debug=True)
```
* Create your main application instance with `FastAPI`. You can set metadata like `title`, `version`, and `debug`.

### Dependency Injection with Depends ✅ Current
```python
from fastapi import FastAPI, Depends

app = FastAPI()

def common_parameters(q: str | None = None):
    return {"q": q}

@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons
```
* Use `Depends` to inject dependencies or shared logic into endpoints.
* Dependencies can be functions or classes.

---

### Using Pydantic models for request bodies ✅ Current
```python
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    return item
```
* Use Pydantic models (subclassing `BaseModel`) to define and validate complex request bodies.

---

### Reading a cookie parameter with Cookie and Annotated ✅ Current
```python
from typing import Annotated
from fastapi import FastAPI, Cookie

app = FastAPI()

@app.get("/get-cookie/")
async def get_cookie(my_cookie: Annotated[str, Cookie()]):
    return {"my_cookie": my_cookie}
```
* Use `Cookie()` in an `Annotated` type hint to declare a cookie parameter.
* Optional cookies can use `str | None` and a default value.

---

### File uploads with File and UploadFile ✅ Current
```python
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    return {"filename": file.filename, "size": len(content)}
```
* Use `File()` and `UploadFile` for handling file uploads in endpoints.

---

### Handling form data with Form ✅ Current
```python
from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}
```
* Use `Form()` to receive form-encoded data in POST requests.

---

### Raising HTTP errors with HTTPException ✅ Current
```python
from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient
import httpx  # Required for TestClient

app = FastAPI()

@app.get("/resource/{id}")
async def get_resource(id: int):
    if id != 42:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    return {"id": id}

client = TestClient(app)

def test_get_resource():
    # Test for existing resource
    resp = client.get("/resource/42")
    assert resp.status_code == 200
    data = resp.json()
    assert "id" in data and data["id"] == 42

    # Test for missing resource (should raise HTTP 404)
    resp2 = client.get("/resource/1")
    assert resp2.status_code == 404
    data2 = resp2.json()
    assert "detail" in data2 and "Resource not found" in data2["detail"]

test_get_resource()
```
* Use `HTTPException` to return error responses with custom status codes and details.
* When testing with `fastapi.testclient.TestClient`, ensure the `httpx` dependency is installed.

---

### Securing endpoints with OAuth2PasswordBearer ✅ Current
```python
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```
* Use security utilities like `OAuth2PasswordBearer` for authentication and authorization schemes.

---

## Configuration

- **FastAPI instance options**: Set `title`, `version`, `description`, `debug`, etc. when creating `FastAPI()`.
- **Router configuration**: Use `APIRouter` for grouping endpoints, with `prefix`, `tags`, and `dependencies` options.
- **Default response class**: Set with `default_response_class` in `FastAPI` or `APIRouter`.
- **Environment variables**: Not required for core FastAPI itself, but may be used by dependencies or for configuration management.
- **Startup and shutdown events**: Register with `on_startup` and `on_shutdown` parameters or use the `@app.on_event` decorator.

## Pitfalls

### Wrong: Missing async in endpoint using await
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/data")
def get_data():
    data = await some_async_call()
    return data
```
*Fails: `await` can only be used inside async functions.*

### Right: Use async def for endpoints using await
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/data")
async def get_data():
    data = await some_async_call()
    return data
```
*Always declare endpoints as `async def` if you use `await`.*

---

### Wrong: Missing type hints for parameters
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id, q=None):
    return {"item_id": item_id, "q": q}
```
*Fails: FastAPI cannot validate or document types without type hints.*

### Right: Provide type hints for all parameters
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```
*Type hints are required for validation and OpenAPI documentation.*

---

### Wrong: Using mutable default in Pydantic model
```python
from pydantic import BaseModel

class Item(BaseModel):
    tags: list = []
```
*Fails: Mutable defaults can lead to shared state between instances.*

### Right: Use default_factory for mutable defaults
```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    tags: list = Field(default_factory=list)
```
*Always use `default_factory` for lists, dicts, or other mutable types.*

---

## References

- [Homepage](https://github.com/fastapi/fastapi)
- [Documentation](https://fastapi.tiangolo.com/)
- [Repository](https://github.com/fastapi/fastapi)
- [Issues](https://github.com/fastapi/fastapi/issues)
- [Changelog](https://fastapi.tiangolo.com/release-notes/)

## Migration from v0.100.0

- **Breaking change:** The official FastAPI CLI was introduced, replacing previous uvicorn-based recommendations for app startup.
- **Migration:**  
  - For development:  
    **Before:**  
    ```shell
    uvicorn main:app --reload
    ```
    **After:**  
    ```shell
    fastapi dev main.py
    ```
  - For production:  
    **Before:**  
    ```shell
    uvicorn main:app
    ```
    **After:**  
    ```shell
    fastapi run main.py
    ```
- Most endpoint and model code remains compatible. Review [Changelog](https://fastapi.tiangolo.com/release-notes/) for full migration details.

## API Reference

- **FastAPI(\*\*, title, description, version, debug, ...)** – Create the main application instance. Key params: `title`, `version`, `description`, `debug`.
- **APIRouter(\*\*, prefix, tags, dependencies, ...)** – Create groups of routes with shared config.
- **@app.get(path), @app.post(path), ...** – Decorators to define HTTP endpoints.
- **Depends(dependency, use_cache=True)** – Declare dependencies for injection in endpoints.
- **Query(default, \*\*, ...)** – Declare and validate query parameters.
- **Path(default, \*\*, ...)** – Declare and validate path parameters.
- **Header(default, \*\*, ...)** – Declare and validate HTTP headers.
- **Cookie(default, \*\*, alias, validation_alias, ...)** – Declare, alias, and validate cookie parameters.
- **Body(default, \*\*, ...)** – Declare and validate request bodies.
- **Form(default, \*\*, ...)** – Receive form data.
- **File(default, \*\*, ...)** – Receive file uploads.
- **UploadFile(filename, content_type, ...)** – Handle uploaded files efficiently.
- **HTTPException(status_code, detail, headers=None)** – Raise HTTP error responses.
- **Request(scope, ...)** – Access the incoming HTTP request object.
- **Response(content, status_code=200, ...)** – Custom response handling.
- **status** – HTTP status codes (re-exported from starlette).
- **OAuth2PasswordBearer(tokenUrl, ...)** – OAuth2 password flow security utility.
- **OAuth2PasswordRequestForm** – Pydantic model for OAuth2 login forms.
- **HTTPBearer, HTTPBasic** – Security utilities for different authentication schemes.
