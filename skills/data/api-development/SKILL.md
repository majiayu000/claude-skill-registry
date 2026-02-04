---
name: api-development
description: |
  API development workflow and best practices for career_ios_backend FastAPI project.
  Automatically invoked when user wants to develop, test, or debug API endpoints.
  Trigger keywords: "API", "endpoint", "route", "FastAPI", "Swagger", "console.html",
  "測試 API", "API 開發", "端點"

  Covers development flow, testing requirements, and console integration.
allowed-tools: [Bash, Read, Grep, Write]
---

# API Development Skill

## Purpose
Guide API development workflow for the career_ios_backend FastAPI project, ensuring all console.html APIs are properly tested and functional.

## Automatic Activation

This skill is AUTOMATICALLY activated when user mentions:
- ✅ "develop API" / "API 開發"
- ✅ "create endpoint" / "創建端點"
- ✅ "test API" / "測試 API"
- ✅ "console.html"
- ✅ "Swagger UI"
- ✅ "FastAPI route"

---

## Development Flow (Prototype Speed-First)

### Standard Workflow

```
1. Write Feature Code (AI-Assisted)
   ↓ 70% time
2. Manual Test API (Swagger UI or Console)
   ↓ Quick verification
3. Write Integration Test (Verify API works)
   ↓ 20% time
4. ruff check --fix (Auto-fix formatting)
   ↓ Auto
5. Commit (Pre-commit hooks)
   ↓ ~5s
6. Push → CI runs Integration Tests
   ↓ ~2 min
```

### Time Allocation

- **Development**: 70% of time
- **Testing**: 20% of time
- **Fixing/Refactoring**: 10% of time

**Philosophy**: Prototype phase prioritizes speed over perfection. Functional validation comes before quality optimization.

---

## Testing Requirements

### Integration Tests (Mandatory)

**CRITICAL**: All `console.html` APIs MUST have integration tests.

```bash
# Daily development: Run integration tests only
poetry run pytest tests/integration/ -v

# Full test suite (optional during development)
poetry run pytest tests/ -v

# Test specific API
poetry run pytest tests/integration/test_auth_api.py -v
```

### Current Test Coverage

**Status (2025-12-25)**:
- ✅ **106+ integration tests** covering 35+ endpoints
- ✅ All major features tested:
  - Authentication API (`test_auth_api.py`)
  - Client Management (`test_clients_api.py`)
  - Sessions/Consultations (`test_sessions_api.py`)
  - Case Management (`test_cases_api.py`)
  - Report Generation (`test_reports_api.py`)
  - RAG Features (`test_rag_*.py`)

### Requirements by Endpoint

Every API endpoint needs:

1. **At least 1 happy path test**
   - Test successful request/response
   - Verify expected data structure
   - Check status codes

2. **Authentication test** (if protected)
   - Use `auth_headers` fixture
   - Verify 401 for unauthenticated requests

3. **Console integration** (if used in console.html)
   - Verify endpoint works from console
   - Test actual user workflows

---

## Console API Verification

### All Console.html APIs Must Be Tested

**Checklist**:

```bash
# Verify test coverage
poetry run pytest tests/integration/ -v | grep -E "(test_.*_api\.py|PASSED|FAILED)"

# Current coverage (106+ tests):
✅ Authentication (login, token refresh)
✅ Client Management (CRUD, search, code generation)
✅ Session Management (CRUD, transcripts, reflections)
✅ Case Management (CRUD, timeline)
✅ Report Generation (consultation reports)
✅ RAG Features (upload, embed, search, evaluate)
```

### When Adding New Console Feature

**TDD Flow for Console APIs**:

```
1. Design API behavior
   ↓
2. Write integration test FIRST
   ↓ (test in tests/integration/)
3. Run test → RED (fails)
   ↓
4. Implement API endpoint
   ↓
5. Run test → GREEN (passes)
   ↓
6. Update console.html to use API
   ↓
7. Manual test in browser console
```

**IMPORTANT**: Test before console integration to catch bugs early.

---

## API Structure (FastAPI)

### Project Layout

```
app/
├── api/
│   ├── auth.py           # Authentication endpoints
│   ├── clients.py        # Client management
│   ├── sessions.py       # Session/consultation
│   ├── cases.py          # Case management
│   └── <feature>.py      # New feature routes
├── models/
│   ├── user.py           # SQLAlchemy models
│   ├── client.py
│   └── <feature>.py      # New feature models
├── schemas/
│   ├── client.py         # Pydantic schemas (request/response)
│   └── <feature>.py
├── services/              # Business logic (optional)
│   └── <feature>_service.py
└── main.py               # App initialization, router registration
```

### Adding New API Endpoint

**Step-by-Step**:

1. **Create route file** (if new feature)
   ```python
   # app/api/my_feature.py
   from fastapi import APIRouter, Depends

   router = APIRouter(prefix="/api/v1/my-feature", tags=["my-feature"])

   @router.get("/")
   async def list_items():
       return {"items": []}
   ```

2. **Define schemas** (Pydantic)
   ```python
   # app/schemas/my_feature.py
   from pydantic import BaseModel

   class ItemCreate(BaseModel):
       name: str
       description: str

   class ItemResponse(BaseModel):
       id: int
       name: str
   ```

3. **Register router** in `main.py`
   ```python
   from app.api import my_feature

   app.include_router(my_feature.router)
   ```

4. **Write integration test** FIRST (TDD)
   ```python
   # tests/integration/test_my_feature_api.py
   @pytest.mark.asyncio
   async def test_list_items(auth_headers):
       async with AsyncClient(app=app, base_url="http://test") as client:
           response = await client.get(
               "/api/v1/my-feature/",
               headers=auth_headers
           )
       assert response.status_code == 200
   ```

---

## Manual Testing Tools

### Swagger UI (OpenAPI Docs)

```bash
# Start development server
poetry run uvicorn app.main:app --reload

# Open Swagger UI
http://localhost:8000/docs

# Features:
- Interactive API testing
- Auto-generated from FastAPI
- Try out endpoints directly
- See request/response schemas
```

### Console.html Testing

```bash
# 1. Start backend
poetry run uvicorn app.main:app --reload

# 2. Open console.html in browser
open console.html

# 3. Test workflows:
- Login
- Create client
- Add session
- Generate report
- etc.
```

### httpx Manual Testing

```python
# Quick test script (for complex scenarios)
import httpx
import asyncio

async def test_api():
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        # Login
        response = await client.post("/api/v1/auth/login", json={
            "username": "testuser",
            "password": "testpass"
        })
        token = response.json()["access_token"]

        # Test endpoint
        response = await client.get(
            "/api/v1/clients/",
            headers={"Authorization": f"Bearer {token}"}
        )
        print(response.json())

asyncio.run(test_api())
```

---

## Authentication Patterns

### Protected Endpoints

Most endpoints require authentication:

```python
from app.core.security import get_current_user

@router.get("/protected")
async def protected_route(current_user = Depends(get_current_user)):
    return {"user": current_user.username}
```

### Testing Authenticated Endpoints

Use `auth_headers` fixture:

```python
@pytest.mark.asyncio
async def test_protected_endpoint(auth_headers):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            "/api/v1/protected",
            headers=auth_headers  # Provides valid JWT token
        )
    assert response.status_code == 200
```

### Authentication Test Pattern

```python
# Test unauthenticated access (should fail)
@pytest.mark.asyncio
async def test_endpoint_requires_auth():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/protected")
    assert response.status_code == 401  # Unauthorized
```

---

## Database Considerations

### Test Database

- Integration tests use **in-memory SQLite**
- Fixtures handle setup/teardown automatically
- See `tests/conftest.py` for database fixtures

### Database Patterns

```python
from app.db.session import get_db
from sqlalchemy.orm import Session

@router.post("/clients")
async def create_client(
    client_data: ClientCreate,
    db: Session = Depends(get_db)
):
    # Use db session for database operations
    new_client = Client(**client_data.dict())
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client
```

---

## Quality Standards (Prototype Phase)

### Must Do ✅

1. **Integration tests for all console.html APIs**
2. **Follow existing API patterns** (check similar endpoints)
3. **Use Pydantic schemas** for request/response validation
4. **Proper HTTP status codes**:
   - 200: Success
   - 201: Created
   - 400: Bad Request
   - 401: Unauthorized
   - 404: Not Found
   - 500: Server Error

### Nice-to-Have (Optional) ⚠️

- Complete type hints
- Edge case tests
- Performance optimization
- Comprehensive error messages

### Don't Do ❌

- 100% test coverage (overkill for prototype)
- Excessive mocking
- Over-engineering

**Remember**: Prototype phase prioritizes **functional validation** over perfection.

---

## Testing Commands Reference

```bash
# Run all integration tests
poetry run pytest tests/integration/ -v

# Run specific test file
poetry run pytest tests/integration/test_clients_api.py -v

# Run specific test
poetry run pytest tests/integration/test_clients_api.py::test_create_client -v

# Run tests with coverage report (optional)
poetry run pytest tests/integration/ --cov=app --cov-report=html

# Run tests matching pattern
poetry run pytest -k "client" -v
```

---

## Common Patterns

### CRUD Operations

```python
# CREATE
@router.post("/", response_model=ItemResponse, status_code=201)
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    ...

# READ (list)
@router.get("/", response_model=List[ItemResponse])
async def list_items(db: Session = Depends(get_db)):
    ...

# READ (single)
@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    ...

# UPDATE
@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    ...

# DELETE
@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    ...
```

### Error Handling

```python
from fastapi import HTTPException

@router.get("/{item_id}")
async def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
```

---

## Integration with TDD Workflow

API development follows TDD for critical features:

```
tdd-workflow skill activates:
  ↓
1. RED: Write integration test (fails)
   → tests/integration/test_<feature>_api.py
  ↓
2. GREEN: Implement API endpoint (passes)
   → app/api/<feature>.py
  ↓
3. REFACTOR: Code review and quality check
  ↓
4. git-workflow skill: Commit and push
```

**Reference**: See `tdd-workflow` skill for detailed TDD process.

---

## Troubleshooting

### "Test database not initialized"

```bash
# Check conftest.py has database fixtures
# Ensure test uses proper fixtures
@pytest.mark.asyncio
async def test_endpoint(db_session):  # Use db fixture
    ...
```

### "Import errors in tests"

```bash
# Ensure PYTHONPATH includes project root
# Run from project root directory
cd /path/to/career_ios_backend
poetry run pytest tests/integration/ -v
```

### "API endpoint not found (404)"

```bash
# Verify router is registered in main.py
# Check route prefix and path
# Start server and check Swagger UI: /docs
```

---

## Related Skills

- **tdd-workflow** - Test-first development process
- **quality-standards** - Code quality requirements
- **git-workflow** - Git commit and push workflow

---

**Skill Version**: v1.0
**Last Updated**: 2025-12-25
**Project**: career_ios_backend (Prototype Phase)
