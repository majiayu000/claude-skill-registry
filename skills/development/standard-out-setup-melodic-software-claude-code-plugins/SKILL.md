---
name: standard-out-setup
description: Add console output and logging to make errors visible to agents. Standard out is a critical leverage point - without it, agents cannot see errors or understand application state. Use when agents fail silently, when debugging agentic workflows, or when setting up a new codebase for agentic coding.
allowed-tools: Read, Edit, Grep
---

# Standard Out Setup

Guide for adding console output to make errors visible to agents. This is one of the most critical leverage points - without stdout visibility, agents operate blind.

## When to Use

- Agent failures with no visible error output
- Silent functions that return without logging
- New codebase setup for agentic coding
- Debugging why agents can't self-correct

## Why Standard Out Matters

Agents can only act on what they can see. If your application fails silently:

- Agent doesn't know something went wrong
- Agent can't identify the error
- Agent can't fix the issue
- Human intervention required (breaks autonomy)

**Standard out is often the missing link when agents fail.**

## The Pattern

### Before (Agent Can't See)

```python
def process_data(data):
    return transform(data)  # Silent - what happened?
```

```typescript
function processData(data) {
    return transform(data);  // Silent - success? failure?
}
```

### After (Agent Can See)

```python
def process_data(data):
    try:
        result = transform(data)
        print(f"SUCCESS: Processed {len(result)} items")
        return result
    except Exception as e:
        print(f"ERROR in process_data: {str(e)}")
        raise
```

```typescript
function processData(data) {
    try {
        const result = transform(data);
        console.log(`SUCCESS: Processed ${result.length} items`);
        return result;
    } catch (error) {
        console.error(`ERROR in processData: ${error.message}`);
        throw error;
    }
}
```

## What to Log

### Always Log

1. **Success with context**
   - What operation completed
   - How many items processed
   - What was created/modified

2. **Errors with detail**
   - What operation failed
   - The error message
   - Enough context to debug

3. **State changes**
   - Files created/modified/deleted
   - API calls made
   - Database operations

### Don't Over-Log

- Avoid logging every loop iteration
- Don't log sensitive data (passwords, tokens)
- Keep messages concise but informative

## Implementation Workflow

### Step 1: Identify Key Functions

Look for:

- API endpoints
- Data processing functions
- File operations
- External service calls
- Database operations

### Step 2: Add Success Logging

For each function, add output on success:

```python
print(f"SUCCESS: {operation} completed - {context}")
```

### Step 3: Add Error Logging

Wrap in try/except with error output:

```python
try:
    # operation
except Exception as e:
    print(f"ERROR in {function_name}: {str(e)}")
    raise  # Re-raise so agent sees the error
```

### Step 4: Verify Visibility

Run the application and verify:

- Can you see success messages?
- Can you see error messages when things fail?
- Is there enough context to understand what happened?

## Language-Specific Patterns

### Python

```python
import logging

# Simple print for immediate visibility
print(f"INFO: Starting {operation}")
print(f"SUCCESS: {operation} complete")
print(f"ERROR: {operation} failed - {error}")

# Or use logging for more control
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Starting {operation}")
logger.error(f"{operation} failed: {error}")
```

### TypeScript/JavaScript

```typescript
// Simple console for immediate visibility
console.log(`INFO: Starting ${operation}`);
console.log(`SUCCESS: ${operation} complete`);
console.error(`ERROR: ${operation} failed - ${error.message}`);

// Or use a logger
import { logger } from './logger';

logger.info(`Starting ${operation}`);
logger.error(`${operation} failed`, { error });
```

### Go

```go
import "log"

log.Printf("INFO: Starting %s", operation)
log.Printf("SUCCESS: %s complete", operation)
log.Printf("ERROR: %s failed - %v", operation, err)
```

## API Endpoint Pattern

This is the most common place agents need visibility:

```python
@app.post("/api/upload")
async def upload_file(file: UploadFile):
    print(f"INFO: Received upload request for {file.filename}")
    try:
        result = await process_file(file)
        print(f"SUCCESS: Uploaded {file.filename} - {len(result)} rows processed")
        return {"status": "success", "rows": len(result)}
    except Exception as e:
        print(f"ERROR: Upload failed for {file.filename} - {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
```

## Anti-Patterns to Fix

### Silent Returns

```python
# BAD
def fetch_data():
    return requests.get(url).json()

# GOOD
def fetch_data():
    print(f"INFO: Fetching data from {url}")
    response = requests.get(url)
    print(f"SUCCESS: Received {len(response.content)} bytes")
    return response.json()
```

### Bare Except Blocks

```python
# BAD - agent never sees the error
try:
    risky_operation()
except:
    pass

# GOOD - agent sees what went wrong
try:
    risky_operation()
except Exception as e:
    print(f"ERROR: risky_operation failed - {str(e)}")
    raise
```

### Empty Catch Blocks

```typescript
// BAD
try {
    riskyOperation();
} catch (e) {}

// GOOD
try {
    riskyOperation();
} catch (error) {
    console.error(`ERROR: riskyOperation failed - ${error.message}`);
    throw error;
}
```

## Verification Checklist

After adding stdout:

- [ ] Success messages appear for normal operations
- [ ] Error messages appear when operations fail
- [ ] Messages include enough context to understand what happened
- [ ] Agent can see and react to the output
- [ ] Sensitive data is not logged

## Related Memory Files

- @12-leverage-points.md - Standard out is leverage point #5
- @agent-perspective-checklist.md - Visibility checklist
- @agentic-kpis.md - Measure improvement

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
