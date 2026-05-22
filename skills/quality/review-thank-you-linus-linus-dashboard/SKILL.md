---
name: review
description: Review code quality, security, and maintainability before committing. Use when reviewing code changes, checking code quality, performing security review, or validating changes before commit.
---

# Code Review Before Commit

Review code quality, security, and maintainability before committing changes to Linus Dashboard.

---

## Your Role

Senior code reviewer ensuring quality, security, and maintainability.

**Context Required:**
1. [.aidriven/memorybank.md](.aidriven/memorybank.md)
2. [.aidriven/rules/](.aidriven/rules/) - All rule files
3. Changed files (git diff)

---

## Review Checklist

### 1. Code Quality

**Readability:**
- [ ] Functions < 50 lines
- [ ] Variables have descriptive names
- [ ] Complex logic has comments explaining WHY
- [ ] Code is self-documenting

**Structure:**
- [ ] Single responsibility per function/class
- [ ] No code duplication
- [ ] Logical organization
- [ ] Consistent style

**Type Safety:**
- [ ] All functions have type hints
- [ ] No `Any` without justification
- [ ] Return types specified
- [ ] Proper use of Optional/Union

### 2. Documentation

- [ ] Module docstrings present
- [ ] Public functions/classes documented
- [ ] Docstrings follow Google style
- [ ] Complex algorithms explained
- [ ] No outdated comments

### 3. Error Handling

- [ ] Specific exceptions (no bare `except`)
- [ ] Errors logged with context
- [ ] User-friendly error messages
- [ ] Resources cleaned up (try/finally)
- [ ] No silent failures

### 4. Async/Await

- [ ] No blocking I/O in async functions
- [ ] All async functions awaited
- [ ] `asyncio.gather()` for parallel ops
- [ ] Proper timeout handling
- [ ] CancelledError handled

### 5. Home Assistant Patterns

- [ ] Integration lifecycle correct (setup/unload)
- [ ] Data stored in `hass.data[DOMAIN][entry_id]`
- [ ] Cleanup registered with `entry.async_on_unload()`
- [ ] Entities have unique_id
- [ ] Services registered properly
- [ ] Coordinator pattern used correctly

### 6. Security

- [ ] No hardcoded credentials
- [ ] User input validated
- [ ] SQL injection prevented
- [ ] XSS vulnerabilities addressed
- [ ] API keys stored securely
- [ ] No sensitive data in logs

### 7. Performance

- [ ] No N+1 queries
- [ ] Expensive operations cached
- [ ] Database queries optimized
- [ ] No memory leaks
- [ ] Async for I/O operations

### 8. Testing

- [ ] Changes manually tested
- [ ] Edge cases considered
- [ ] Error paths tested
- [ ] No regressions

---

## Review Process

### Step 1: Get Changed Files

```bash
# See what changed
git status

# View diff
git diff

# Check specific files
git diff path/to/file.py
```

### Step 2: Analyze Changes

For each changed file:
1. Read the diff
2. Understand the purpose
3. Check against standards
4. Look for issues
5. Note improvements

### Step 3: Check Build and Tests

```bash
# TypeScript
npm run build
npm run type-check
npm run lint:check

# Run smoke tests
npm run test:smoke
```

### Step 4: Provide Feedback

**Format:**
```
File: path/to/file.py

✅ Good:
- Clear function names
- Proper type hints
- Good error handling

⚠️ Issues:
1. Line 42: Missing docstring
2. Line 78: Blocking I/O in async function
3. Line 103: Exception too broad

💡 Suggestions:
- Consider caching this result
- Extract this logic to separate function
```

---

## Common Issues to Watch For

### Python Issues

**Async/Await:**
```python
# ❌ Bad - blocking I/O
async def fetch_data():
    response = requests.get(url)  # Blocks event loop

# ✅ Good - async I/O
async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```

**Error Handling:**
```python
# ❌ Bad - bare except
try:
    do_something()
except:
    pass

# ✅ Good - specific exception
try:
    do_something()
except ValueError as err:
    _LOGGER.error("Invalid value: %s", err)
    raise
```

**Type Hints:**
```python
# ❌ Bad - no types
def process_data(data):
    return data.get("value")

# ✅ Good - with types
def process_data(data: dict[str, Any]) -> str | None:
    """Process data and return value."""
    return data.get("value")
```

### TypeScript Issues

**Type Safety:**
```typescript
// ❌ Bad - any type
function process(data: any): any {
    return data.value;
}

// ✅ Good - proper types
function process(data: DataType): string | undefined {
    return data.value;
}
```

**Null Safety:**
```typescript
// ❌ Bad - no null check
const value = entity.state.toUpperCase();

// ✅ Good - null check
const value = entity.state?.toUpperCase() ?? "unknown";
```

---

## Security Review Checklist

- [ ] No secrets in code
- [ ] API keys from config
- [ ] User input sanitized
- [ ] SQL queries parameterized
- [ ] HTML output escaped
- [ ] HTTPS for external calls
- [ ] Authentication checked
- [ ] Authorization verified

---

## Performance Review Checklist

- [ ] No synchronous I/O in async code
- [ ] Database queries optimized
- [ ] Caching used appropriately
- [ ] No unnecessary API calls
- [ ] Efficient algorithms
- [ ] Memory usage reasonable

---

## Final Review

Before approving:

**Code Quality:**
- Follows project standards
- Well-documented
- Properly typed
- Good error handling

**Functionality:**
- Implements requirements
- No obvious bugs
- Edge cases handled
- Tested manually

**Maintainability:**
- Easy to understand
- Well-structured
- Follows patterns
- Documented properly

**Security:**
- No vulnerabilities
- Input validated
- Secrets protected

---

## Review Outcome

**APPROVE** - Code meets all standards
**REQUEST CHANGES** - Issues must be fixed
**COMMENT** - Suggestions for improvement

---

## Quick Commands

```bash
# Check what changed
git diff

# Check specific file
git diff path/to/file

# See commit history
git log --oneline -10

# Run quality checks
npm run lint:check
npm run type-check
npm run build

# Run tests
npm run test:smoke
```
