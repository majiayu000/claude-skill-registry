---
name: FastAPI Development
description: Build async APIs with FastAPI, including endpoints, dependency injection, validation, and testing. Use when creating REST APIs, web backends, or microservices.
---

# FastAPI Development

## Quick start

Create a basic FastAPI application:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

Run with:

```bash
uvicorn main:app --reload
```

## Common patterns

### Pydantic models for validation

```python
from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.post("/items/")
async def create_item(item: Item):
    return item
```

### Dependency injection

```python
from typing import Annotated
from fastapi import Depends

async def common_parameters(
    q: str | None = None,
    skip: int = 0,
    limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}

CommonsDep = Annotated[dict, Depends(common_parameters)]

@app.get("/items/")
async def read_items(commons: CommonsDep):
    return commons
```

### Database dependencies with cleanup

```python
async def get_db():
    db = connect_to_database()
    try:
        yield db
    finally:
        db.close()

@app.get("/query/")
async def query_data(db: Annotated[dict, Depends(get_db)]):
    return {"data": "query results"}
```

### Error handling

```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id < 1:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id}
```

### Path and query validation

```python
from typing import Annotated
from fastapi import Path, Query

@app.get("/items/{item_id}")
async def read_item(
    item_id: Annotated[int, Path(gt=0, le=1000)],
    q: Annotated[str, Query(max_length=50)] = None
):
    return {"item_id": item_id, "q": q}
```

### Response models

```python
from pydantic import BaseModel

class ItemPublic(BaseModel):
    id: int
    name: str
    price: float

@app.get("/items/{item_id}", response_model=ItemPublic)
async def read_item(item_id: int):
    return ItemPublic(id=item_id, name="Laptop", price=999.99)
```

## Testing with TestClient

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_read_item():
    response = client.get("/items/42?q=test")
    assert response.status_code == 200
    assert response.json() == {"item_id": 42, "q": "test"}
```

## Requirements

```bash
pip install fastapi uvicorn
pip install "fastapi[all]"  # Includes all optional dependencies
```

## Key concepts

- **Async/await**: Use `async def` for I/O operations
- **Automatic validation**: Request/response validation with Pydantic
- **Dependency injection**: Share logic across endpoints with `Depends`
- **Type hints**: Full editor support and validation
- **Interactive docs**: Auto-generated Swagger/OpenAPI at `/docs`
- **Background tasks**: Run tasks after response using `BackgroundTasks`
