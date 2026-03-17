---
name: backend-api
description: Build FastAPI REST APIs with CORS, JWT auth, Pydantic validation, async endpoints, and proper error handling. Use when creating API endpoints, middleware, or backend services.
---

# FastAPI Backend API Development

## Core Pattern
```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import os

app = FastAPI(title="API")

# CORS from environment
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "").split(","),
    allow_credentials=os.getenv("CORS_ALLOW_CREDENTIALS") == "true",
    allow_methods=["*"],
    allow_headers=["*"],
)

class Request(BaseModel):
    field: str = Field(..., min_length=1)

@app.post("/api/{user_id}/endpoint")
async def endpoint(user_id: str, req: Request, current_user: str = Depends(verify_jwt)):
    if user_id != current_user:
        raise HTTPException(status_code=403, detail="User ID mismatch")
    return {"status": "ok"}
```

## Error Handling
- Use `HTTPException` with proper status codes (401, 403, 404, 500)
- Provide user-friendly error messages
- Always use async for I/O operations

## Testing
```python
from fastapi.testclient import TestClient
client = TestClient(app)
response = client.post("/api/user123/endpoint", json={"field": "value"})
assert response.status_code == 200
```