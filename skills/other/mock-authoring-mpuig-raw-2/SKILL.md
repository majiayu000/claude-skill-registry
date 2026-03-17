---
name: mock-authoring
description: Writing effective dry_run.py mocks for workflow testing without external dependencies
---

# Mock Authoring Skill

Use this skill to write dry_run.py files that enable workflows to run without external dependencies.

## Purpose of dry_run.py

The dry run file provides mock implementations of external operations so workflows can be tested without:
- Network calls (APIs, databases, web scraping)
- File system writes outside the workflow directory
- Environment variables or credentials
- Long-running operations

## Mock Patterns

### 1. API Response Mocking

```python
#!/usr/bin/env python3
"""Dry run with mock data."""

from raw_runtime import DryRunContext

def mock_fetch_stock_price(ctx: DryRunContext, symbol: str) -> dict:
    """Mock Yahoo Finance API response."""
    ctx.log(f"[MOCK] Fetching stock price for {symbol}")

    # Return realistic mock data
    return {
        "symbol": symbol,
        "price": 150.23,
        "change": 2.45,
        "change_percent": 1.65,
        "volume": 1234567,
        "timestamp": "2024-01-15T16:00:00Z"
    }

def mock_fetch_news(ctx: DryRunContext, query: str) -> list[dict]:
    """Mock news API response."""
    ctx.log(f"[MOCK] Fetching news for query: {query}")

    return [
        {
            "title": "Sample News Article 1",
            "url": "https://example.com/article1",
            "published": "2024-01-15T10:00:00Z",
            "summary": "This is a mock news article summary."
        },
        {
            "title": "Sample News Article 2",
            "url": "https://example.com/article2",
            "published": "2024-01-15T09:00:00Z",
            "summary": "Another mock article summary."
        }
    ]
```

### 2. Database Operation Mocking

```python
def mock_query_database(ctx: DryRunContext, sql: str) -> list[dict]:
    """Mock database query."""
    ctx.log(f"[MOCK] Executing SQL: {sql[:50]}...")

    # Return mock rows
    return [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
    ]

def mock_insert_record(ctx: DryRunContext, table: str, data: dict) -> int:
    """Mock database insert."""
    ctx.log(f"[MOCK] Inserting into {table}: {data}")
    return 123  # Mock generated ID
```

### 3. File Operation Mocking

```python
def mock_write_file(ctx: DryRunContext, path: str, content: str) -> bool:
    """Mock file write operation."""
    ctx.log(f"[MOCK] Would write {len(content)} bytes to {path}")
    # Don't actually write - just log
    return True

def mock_upload_to_s3(ctx: DryRunContext, bucket: str, key: str, data: bytes) -> str:
    """Mock S3 upload."""
    ctx.log(f"[MOCK] Would upload {len(data)} bytes to s3://{bucket}/{key}")
    return f"https://s3.amazonaws.com/{bucket}/{key}"  # Mock URL
```

### 4. Long-Running Operation Mocking

```python
def mock_train_model(ctx: DryRunContext, dataset_path: str) -> dict:
    """Mock ML model training (skip actual training)."""
    ctx.log(f"[MOCK] Would train model on {dataset_path}")
    ctx.log("[MOCK] Training skipped in dry run")

    # Return mock metrics
    return {
        "accuracy": 0.92,
        "precision": 0.89,
        "recall": 0.91,
        "model_path": "/tmp/mock_model.pkl"
    }
```

## DryRunContext Usage

```python
from raw_runtime import DryRunContext

def mock_operation(ctx: DryRunContext) -> str:
    # Log what would happen
    ctx.log("Starting mock operation")
    ctx.log("Step 1: Connect to API")
    ctx.log("Step 2: Fetch data")
    ctx.log("Step 3: Process results")

    # Return mock result
    return "mock_result"
```

## Realistic Mock Data

Mock data should be realistic enough to test workflow logic:

```python
# Good: Realistic structure and values
def mock_api_response(ctx: DryRunContext) -> dict:
    return {
        "status": "success",
        "data": [
            {"id": "abc123", "value": 42.5, "timestamp": "2024-01-15T10:00:00Z"},
            {"id": "def456", "value": 38.2, "timestamp": "2024-01-15T11:00:00Z"},
        ],
        "pagination": {"page": 1, "total_pages": 5}
    }

# Bad: Oversimplified mock
def mock_api_response(ctx: DryRunContext) -> dict:
    return {"result": "ok"}  # Too simple - doesn't match real API
```

## Error Case Mocking

Include mock error scenarios for testing error handling:

```python
def mock_api_with_error(ctx: DryRunContext, should_fail: bool = False) -> dict:
    """Mock API that can simulate failures."""
    if should_fail:
        ctx.log("[MOCK] Simulating API error")
        raise ConnectionError("Mock API connection failed")

    ctx.log("[MOCK] API call succeeded")
    return {"status": "success", "data": []}
```

## Integration with Workflow

In your workflow `run.py`:

```python
class MyWorkflow(BaseWorkflow[MyParams]):
    def __init__(self, params: MyParams, workflow_dir: Path):
        super().__init__(params, workflow_dir)

        # Check if running in dry mode
        if self.is_dry_run():
            # Import mocks
            from dry_run import mock_fetch_stock_price, mock_write_file
            self.fetch_stock_price = mock_fetch_stock_price
            self.write_file = mock_write_file
        else:
            # Use real implementations
            from tools.yahoo_finance import fetch_stock_price
            from tools.file_writer import write_file
            self.fetch_stock_price = fetch_stock_price
            self.write_file = write_file
```

## Testing Your Mocks

```bash
# Run workflow in dry mode
raw run <workflow-id> --dry

# Should complete without:
# - Network errors
# - Missing credentials
# - File system permission errors
# - Long wait times
```

## Common Mistakes

1. **Mocks that call real APIs**
   ```python
   # Bad: Still makes real network call
   def mock_fetch(ctx: DryRunContext):
       import requests
       return requests.get("https://api.example.com")  # Don't do this!

   # Good: Pure mock
   def mock_fetch(ctx: DryRunContext):
       ctx.log("[MOCK] Fetching data")
       return {"data": "mock_value"}
   ```

2. **Accessing environment variables**
   ```python
   # Bad: Requires env vars in dry run
   def mock_auth(ctx: DryRunContext):
       api_key = os.environ["API_KEY"]  # Will fail without env var

   # Good: No env var dependency
   def mock_auth(ctx: DryRunContext):
       ctx.log("[MOCK] Using mock credentials")
       return "mock_token"
   ```

3. **File system writes outside workflow directory**
   ```python
   # Bad: Writes to filesystem
   def mock_save(ctx: DryRunContext, data: str):
       with open("/tmp/output.txt", "w") as f:
           f.write(data)

   # Good: Just logs
   def mock_save(ctx: DryRunContext, data: str):
       ctx.log(f"[MOCK] Would save {len(data)} bytes to /tmp/output.txt")
   ```

## Checklist for Good Mocks

- [ ] No network calls (HTTP, database, etc.)
- [ ] No environment variable dependencies
- [ ] No file system writes outside workflow directory
- [ ] Realistic data structures matching real API responses
- [ ] Appropriate use of `ctx.log()` for observability
- [ ] Fast execution (no sleep or long operations)
- [ ] Include error cases where workflow handles errors
- [ ] Return types match real implementation
