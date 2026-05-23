---
name: python-debugging
description: Python debugging methodology and problem-solving framework. Use when investigating exceptions, async issues, logging problems, or MCP integration failures in Python code.
---

# Python Debugging Methodology

Systematic problem-solving framework for Python code debugging.

## When to Use This Skill

- Investigating exceptions and stack traces
- Debugging asynchronous code (async/await)
- Resolving logging configuration issues
- Troubleshooting MCP server communication errors
- Diagnosing test failures (pytest, unittest)
- Analyzing performance problems

## Debugging Workflow (推論プロセス)

### 1. Interpret Error Messages

**Objective**: Extract actionable information from error output

**Error message anatomy**:
```
Traceback (most recent call last):
  File "script.py", line 42, in main        ← Calling context
    result = process_data(input)            ← Line that triggered error
  File "utils.py", line 15, in process_data ← Where exception was raised
    return data['key']                      ← Failing operation
KeyError: 'key'                             ← Exception type and message
```

**Questions to answer**:
- What is the exception type? (KeyError, AttributeError, TypeError, etc.)
- What was the last successful operation?
- What input triggered the failure?

### 2. Read Stack Traces

**Objective**: Understand execution path to failure point

**Reading strategy**:

**Top-down** (most common):
- Start from outermost frame (entry point)
- Trace execution flow downward
- Understand calling context

**Bottom-up** (for root cause):
- Start from innermost frame (where exception was raised)
- Identify the specific operation that failed
- Trace why inputs were invalid

**Focus points**:
- Function arguments at each level
- Local variables at failure point
- Library code vs application code boundaries

### 3. Reproduce Consistently

**Objective**: Create minimal failing test case

**Simplification steps**:
1. Isolate the failing function
2. Extract minimal input that triggers failure
3. Remove dependencies (use mocks if needed)
4. Create standalone script (~10 lines)

**Example**:
```python
# Minimal reproducer
data = {'wrong_key': 123}
result = data['key']  # KeyError
```

### 4. Form Hypotheses

**Objective**: List plausible causes based on exception type

**Hypothesis by exception type**:

| Exception | Common Causes | Investigation Strategy |
|-----------|---------------|------------------------|
| **KeyError** | Missing dict key, typo | Print dict.keys(), check spelling |
| **AttributeError** | Wrong object type, typo | Print type(obj), check method name |
| **TypeError** | Wrong argument type, arity mismatch | Print type(args), check function signature |
| **ValueError** | Invalid value range, format error | Print actual value, check constraints |
| **IndexError** | List/string index out of bounds | Print len(sequence), check index calculation |
| **ImportError** | Module not installed, wrong path | Check pip list, sys.path |
| **JSONDecodeError** | Malformed JSON, encoding issue | Print raw string, validate JSON syntax |

**For asynchronous code**:
- Is await missing? (RuntimeWarning: coroutine never awaited)
- Is blocking I/O used in async function?
- Are multiple tasks accessing shared state?

**For MCP/RPC issues**:
- Is JSON-RPC request malformed?
- Is server process running?
- Are method names spelled correctly?
- Is timeout too short?

### 5. Select Debugging Strategy

**Objective**: Choose appropriate tool for the problem

**Decision tree**:

```
Is the error location obvious from stack trace?
├─ Yes → Use print() or logging
│        Fast iteration, minimal setup
└─ No → Use pdb debugger
         Interactive inspection needed

Is the problem in async code?
├─ Yes → Use logging with timestamps
│        await points are not debugger-friendly
└─ No → pdb works well

Is it a test failure?
├─ Yes → pytest --pdb
│        Drops into debugger at failure point
└─ No → Standard debugging approach
```

### 6. Apply Debugging Tool

**Objective**: Gather evidence to confirm/reject hypothesis

**Tool selection**:

**print() / logging**: Quick hypothesis testing
```python
print(f"DEBUG: variable={variable}, type={type(variable)}")
```

**pdb**: Interactive investigation
```python
import pdb; pdb.set_trace()  # Breakpoint here
```

**logging**: Persistent diagnostics
```python
logger.debug(f"Processing {count} items")
logger.warning(f"Unexpected value: {value}")
```

## Debugging Strategy Selection

### When to Use print()

**Use for**:
- Quick value inspection
- Hypothesis: "If I print X here, I'll see Y"
- Short-lived debugging sessions

**Limitations**:
- Clutters code
- Must re-run for each new hypothesis
- No interactive inspection

### When to Use pdb

**Use for**:
- Multiple hypotheses to test
- Need to inspect many variables
- Control flow is unclear
- Complex data structures

**Basic commands**:
```
(Pdb) l          # List code around current line
(Pdb) n          # Next line (step over)
(Pdb) s          # Step into function
(Pdb) c          # Continue to next breakpoint
(Pdb) p variable # Print variable value
(Pdb) pp obj     # Pretty-print object
(Pdb) w          # Where am I? (stack trace)
```

### When to Use logging

**Use for**:
- Production code debugging
- Long-running processes
- Intermittent failures
- Timeline reconstruction

**Configuration**:
```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

## Error Pattern Recognition

### Common Python Patterns

**Pattern: "NoneType has no attribute X"**
```python
# Cause: Function returned None instead of expected object
result = get_data()  # Returns None on error
result.process()     # AttributeError: 'NoneType' has no attribute 'process'

# Investigation: Why did get_data() return None?
```

**Pattern: "Dictionary changed size during iteration"**
```python
# Cause: Modifying dict while iterating
for key in data:
    if condition:
        del data[key]  # RuntimeError

# Fix: Iterate over copy
for key in list(data.keys()):
    if condition:
        del data[key]
```

**Pattern: "JSON decode error: Expecting value"**
```python
# Cause: Empty or non-JSON response
response = requests.get(url)
data = response.json()  # JSONDecodeError if response is HTML or empty

# Investigation: Print response.text to see actual content
```

### Async/Await Patterns

**Pattern: "Coroutine was never awaited"**
```python
# Wrong: Calling async function without await
result = async_function()  # Returns coroutine object, doesn't execute

# Right: Await the coroutine
result = await async_function()
```

**Pattern: "Event loop already running"**
```python
# Cause: Nested asyncio.run() calls
async def outer():
    asyncio.run(inner())  # Error: loop already running

# Fix: Just await
async def outer():
    await inner()
```

## Hypothesis Testing Techniques

### Binary Search Debugging

Narrow down the failing region:

```python
# Add checkpoints to partition code
def process_data(data):
    print("CHECKPOINT 1: Input valid")  # Check 1
    
    intermediate = transform(data)
    print("CHECKPOINT 2: Transform OK")  # Check 2
    
    result = finalize(intermediate)
    print("CHECKPOINT 3: Finalize OK")  # Check 3
    
    return result

# Run: Which checkpoint is NOT printed? Problem is before it.
```

### Differential Analysis

Compare working vs failing cases:

```python
# Working case
process_data({'key': 'value'})  # ✓ Success

# Failing case  
process_data({'wrong_key': 'value'})  # ✗ KeyError

# Insight: Code assumes 'key' always exists
# Fix: Add default or validation
```

### Isolation Testing

Test components independently:

```python
# Hypothesis: Function X works correctly in isolation
def test_function_x():
    input_data = {'key': 'value'}
    result = function_x(input_data)
    assert result == expected_value

# If test passes: Problem is in calling context or inputs
# If test fails: Problem is in function_x implementation
```

## Logging Strategies

### Log Level Guidelines

| Level | When to Use | Example |
|-------|-------------|---------|
| **DEBUG** | Detailed diagnosis, temporary | `logger.debug(f"Processing item {i}/{total}")` |
| **INFO** | Important events, milestones | `logger.info("MCP server started on port 8000")` |
| **WARNING** | Recoverable issues, deprecations | `logger.warning("Timeout, retrying...")` |
| **ERROR** | Errors that need attention | `logger.error("Failed to connect to DSIM")` |
| **CRITICAL** | System failure, requires immediate action | `logger.critical("License server unreachable")` |

### Structured Logging

Include context in log messages:

```python
# Good: Context-rich logging
logger.info(f"Test {test_name} compilation completed in {duration}s")

# Bad: Ambiguous logging  
logger.info("Compilation completed")
```

### Async Code Logging

Log await points to trace execution:

```python
async def process_request(request_id):
    logger.debug(f"[{request_id}] Starting")
    
    data = await fetch_data()
    logger.debug(f"[{request_id}] Data fetched")
    
    result = await process(data)
    logger.debug(f"[{request_id}] Processing complete")
    
    return result
```

## MCP Server Debugging

### Common MCP Issues

**Pattern: "Method not found"**
```python
# Cause: Typo in method name or not registered
# Investigation: Check server tool registry, verify spelling
```

**Pattern: "Connection refused"**
```python
# Cause: Server not running or wrong port
# Investigation: Check server process, verify port number
```

**Pattern: "Timeout waiting for response"**
```python
# Cause: Server hung, processing too slow, timeout too short
# Investigation: Check server logs, increase timeout, add progress logging
```

### MCP Debugging Workflow

1. **Verify server is running**
   ```python
   # Check process list for MCP server
   # Check server startup logs
   ```

2. **Check request format**
   ```python
   logger.debug(f"Sending request: {json.dumps(request, indent=2)}")
   ```

3. **Monitor server response**
   ```python
   logger.debug(f"Received response: {json.dumps(response, indent=2)}")
   ```

4. **Validate JSON-RPC structure**
   - Is "jsonrpc": "2.0" present?
   - Is "method" spelled correctly?
   - Are "params" in correct format?

## Test Debugging

### pytest Integration

**Run test with debugger**:
```bash
pytest test_file.py::test_function --pdb
# Drops into pdb on first failure
```

**Add breakpoint in test**:
```python
def test_processing():
    data = load_test_data()
    import pdb; pdb.set_trace()  # Inspect here
    result = process(data)
    assert result == expected
```

### Debugging Test Isolation

**Problem**: Test passes alone, fails in suite

**Investigation**:
- Check for shared state (module-level variables)
- Check for fixture side effects
- Run tests in different orders to isolate interaction

## Common Pitfalls

### Don't Ignore Warnings

```python
# RuntimeWarning: coroutine 'func' was never awaited
# ↑ This WILL cause bugs, fix immediately
```

### Don't Assume Exception Type

```python
# Wrong: Catching generic exception
try:
    data = json.loads(text)
except:  # Catches everything, including KeyboardInterrupt
    pass

# Right: Catch specific exception
try:
    data = json.loads(text)
except json.JSONDecodeError as e:
    logger.error(f"Invalid JSON: {e}")
```

### Don't Debug in Production

```python
# Wrong: Leaving debug code in production
import pdb; pdb.set_trace()  # Will hang production server

# Right: Use logging with appropriate level
logger.debug("Debug information")  # Only in dev mode
```

## Integration with Other Skills

- **mcp-workflow**: Use when debugging MCP server integration issues
- **dsim-debugging**: Coordinate when Python MCP server controls DSIM simulator
- **uvm-verification**: Debug UVM test invocation from Python scripts

## Summary

Python debugging is systematic problem-solving:

1. **Interpret** error messages for exception type and context
2. **Read** stack traces to understand execution path
3. **Reproduce** with minimal test case
4. **Form** hypotheses based on exception patterns
5. **Select** appropriate debugging tool (print/pdb/logging)
6. **Test** hypotheses systematically

Key principle: **Understand the error, then investigate the cause**. Don't guess—use evidence from stack traces, logs, and debugger inspection.
