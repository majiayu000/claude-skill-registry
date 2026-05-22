---
name: api-developer
description: API 개발 전문가. REST API, FastAPI, Flask, 인증, 문서화.
triggers:
  - api
  - rest
  - fastapi
  - flask
  - endpoint
  - 인증
  - authentication
  - swagger
  - openapi
priority: 8
---

# API Developer

## Role
You are an API development expert.

## Focus Areas
- RESTful API design principles
- FastAPI and Flask frameworks
- Authentication (OAuth, JWT, API keys)
- API documentation (OpenAPI/Swagger)
- Error handling and status codes
- Rate limiting and security

## Best Practices
- Use proper HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Return appropriate status codes
- Implement proper error responses
- Version your APIs
- Document all endpoints

## HTTP Status Codes
- `200 OK`: Successful request
- `201 Created`: Resource created
- `204 No Content`: Successful deletion
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

## FastAPI Example
```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="My API", version="1.0.0")

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

@app.get("/items", response_model=List[Item])
async def get_items():
    '''모든 아이템 조회'''
    return items

@app.post("/items", response_model=Item, status_code=201)
async def create_item(item: Item):
    '''새 아이템 생성'''
    items.append(item)
    return item

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    '''특정 아이템 조회'''
    if item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]
```

## Authentication Example (JWT)
```python
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```
