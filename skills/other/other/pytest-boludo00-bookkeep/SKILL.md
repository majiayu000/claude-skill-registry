---
name: pytest
description: |
  Writes and executes backend unit and integration tests with pytest.
  Use when: writing new tests, running the test suite, debugging test failures,
  mocking external dependencies, or setting up test fixtures.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Pytest Skill

Bookkeep backend uses pytest with pytest-asyncio for testing FastAPI routers, SQLAlchemy models, and download client integrations. Tests live in `backend/tests/` with a flat structure mirroring `app/` modules.

## Quick Start

```bash
# Run all tests
cd backend && uv run pytest -v

# Run specific test file
uv run pytest tests/downloads/test_prowlarr_api.py -v

# Run specific test class
uv run pytest tests/downloads/test_qbittorrent_client.py::TestAddTorrent -v

# Run with output
uv run pytest -v -s
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Fixtures | Shared test setup | `@pytest.fixture` |
| Mocking | Isolate unit tests | `patch.object()`, `Mock()` |
| Test classes | Group related tests | `class TestClientInit:` |
| Assertions | Verify behavior | `assert result is True` |
| Exception testing | Verify errors | `pytest.raises(ValueError)` |

## Common Patterns

### Unit Test with Mocked Dependency

```python
from unittest.mock import Mock, patch

@pytest.fixture
def mock_client():
    """Create client with mocked external dependency"""
    with patch('app.downloads.clients.qbittorrent.QBClient') as mock:
        mock_instance = Mock()
        mock.return_value = mock_instance
        mock_instance.app.version = "v4.6.0"
        
        client = QBittorrentClient(host="localhost", port=8080, ...)
        yield client

def test_successful_connection(self, mock_client):
    result = mock_client.test_connection()
    assert result is True
```

### Database Integration Test

```python
@pytest.fixture(scope="function")
def db_session():
    """Fresh database session per test"""
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

def test_create_task(self, db_session, sample_book):
    task = DownloadTask(book_id=sample_book.id, format="ebook", ...)
    db_session.add(task)
    db_session.commit()
    assert task.id is not None
```

## Test File Structure

```
backend/tests/
├── downloads/
│   ├── __init__.py
│   ├── test_models.py         # Integration: database models
│   ├── test_prowlarr_api.py   # Unit: Prowlarr client
│   ├── test_qbittorrent_client.py  # Unit: qBittorrent
│   └── test_nzbget_client.py  # Unit: NZBGet
└── conftest.py                # Shared fixtures (create if needed)
```

## See Also

- [unit](references/unit.md) - Unit testing patterns
- [integration](references/integration.md) - Database and API testing
- [mocking](references/mocking.md) - Mock objects and patches
- [fixtures](references/fixtures.md) - Test fixtures and setup

## Related Skills

For database operations, see the **sqlalchemy** skill. For FastAPI router testing, see the **fastapi** skill.