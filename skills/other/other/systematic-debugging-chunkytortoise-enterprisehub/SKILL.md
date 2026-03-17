---
name: Systematic Debugging
description: This skill should be used when the user asks to "debug this issue", "find the root cause", "investigate the bug", "systematic debugging", "troubleshoot the problem", or needs help with systematic problem-solving and root cause analysis.
version: 1.0.0
---

# Systematic Debugging: 4-Phase Root Cause Analysis

## Overview

Systematic debugging follows a structured 4-phase approach to identify, isolate, and resolve issues efficiently. This methodology prevents the common debugging trap of random changes and ensures comprehensive problem-solving with reproducible results.

## The 4-Phase Debugging Process

### Phase 1: REPRODUCE - Isolate the Problem

Establish a reliable way to reproduce the issue consistently.

**Objectives:**
- Create minimal reproduction case
- Document exact steps to trigger the bug
- Identify environmental factors
- Establish success/failure criteria

**Key Questions:**
- What exactly happens vs. what should happen?
- Under what conditions does it occur?
- Can you reproduce it consistently?
- What's the minimal case that shows the problem?

### Phase 2: GATHER - Collect Evidence

Systematically collect all available information about the issue.

**Data Sources:**
- Error messages and stack traces
- Log files and application output
- System metrics and performance data
- User reports and behavioral patterns
- Code changes and deployment history

**Evidence Types:**
- **Direct evidence**: Error messages, exceptions, failures
- **Circumstantial evidence**: Timing, environment, patterns
- **Historical evidence**: When did it start? What changed?

### Phase 3: HYPOTHESIZE - Generate Theories

Develop testable theories about the root cause based on evidence.

**Hypothesis Framework:**
- **Input hypothesis**: Problem in data or user input
- **Logic hypothesis**: Bug in business logic or algorithms
- **Environment hypothesis**: System, infrastructure, or configuration issue
- **Integration hypothesis**: Problem in external dependencies or APIs

**Validation Criteria:**
- Each hypothesis must be testable
- Evidence should support or refute the theory
- Prioritize hypotheses by probability and impact

### Phase 4: TEST - Validate and Fix

Test each hypothesis systematically and implement verified solutions.

**Testing Approach:**
- Test hypotheses in order of likelihood
- Change one variable at a time
- Document test results
- Verify fix resolves the original issue

## Debugging Toolbox

### Code-Level Debugging

**Print/Log Debugging:**
```python
# Strategic print statements
print(f"DEBUG: Variable x = {x}, type = {type(x)}")
print(f"DEBUG: Function entry - params: {locals()}")
```

**Interactive Debuggers:**
```bash
# Python
python -m pdb script.py
breakpoint()  # Python 3.7+

# JavaScript/Node.js
node --inspect-brk script.js
debugger;  // Breakpoint in code
```

**Assertion Debugging:**
```python
# Validate assumptions
assert user_id is not None, f"User ID should not be None at this point"
assert len(items) > 0, f"Items list should not be empty: {items}"
```

### System-Level Debugging

**Log Analysis:**
```bash
# Search for patterns
grep -i "error" /var/log/application.log
tail -f /var/log/application.log | grep "user_id=123"

# Analyze timing patterns
awk '{print $4}' access.log | sort | uniq -c
```

**Performance Analysis:**
```bash
# CPU and Memory
top -p $(pgrep python)
ps aux | grep "my_application"

# Network debugging
netstat -tulpn | grep :8080
curl -v http://localhost:8080/api/health
```

**Database Debugging:**
```sql
-- Query performance
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- Lock analysis
SELECT * FROM pg_locks WHERE NOT granted;

-- Slow query log analysis
SELECT query, mean_time, calls FROM pg_stat_statements ORDER BY mean_time DESC;
```

## Common Bug Patterns

### Logic Errors

**Off-by-One Errors:**
```python
# Bug: Missing last element
for i in range(len(array) - 1):  # Should be len(array)
    process(array[i])

# Fix: Include all elements
for i in range(len(array)):
    process(array[i])
```

**Null/Undefined Handling:**
```javascript
// Bug: Doesn't handle null case
function processUser(user) {
    return user.name.toUpperCase();  // Crashes if user is null
}

// Fix: Add null checks
function processUser(user) {
    return user?.name?.toUpperCase() || 'Unknown';
}
```

### Timing and Concurrency Issues

**Race Conditions:**
```python
# Bug: Race condition in counter
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        temp = self.count
        temp += 1
        self.count = temp  # Not atomic

# Fix: Use proper synchronization
import threading

class Counter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.count += 1
```

**Async/Await Issues:**
```javascript
// Bug: Not awaiting async function
async function fetchData() {
    const result = api.getData();  // Missing await
    return result.id;  // Tries to access property on Promise
}

// Fix: Proper async handling
async function fetchData() {
    const result = await api.getData();
    return result.id;
}
```

### Resource Management Issues

**Memory Leaks:**
```python
# Bug: Circular references
class Parent:
    def __init__(self):
        self.children = []

    def add_child(self, child):
        child.parent = self  # Circular reference
        self.children.append(child)

# Fix: Use weak references
import weakref

class Parent:
    def __init__(self):
        self.children = []

    def add_child(self, child):
        child.parent = weakref.ref(self)
        self.children.append(child)
```

## Debugging Strategies by Context

### Web Application Debugging

**Client-Side Issues:**
1. Check browser console for JavaScript errors
2. Inspect network tab for failed requests
3. Validate form data and API payloads
4. Test across different browsers and devices

**Server-Side Issues:**
1. Check application logs for errors
2. Monitor database query performance
3. Validate API request/response cycles
4. Check server resource utilization

### API Debugging

**Request/Response Debugging:**
```bash
# Test API endpoints
curl -X POST http://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User"}' \
  -v

# Check authentication
curl -H "Authorization: Bearer token123" \
  http://api.example.com/protected \
  -v
```

**Database Integration:**
```python
# Add query logging
import logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
```

### Performance Debugging

**Profiling Code:**
```python
# Python profiling
import cProfile
cProfile.run('main()')

# Line-by-line profiling
from line_profiler import LineProfiler
profiler = LineProfiler()
profiler.add_function(my_function)
profiler.run('main()')
```

**Memory Profiling:**
```python
# Memory usage tracking
import tracemalloc
tracemalloc.start()

# Your code here

current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage: {current / 1024 / 1024:.1f} MB")
print(f"Peak memory usage: {peak / 1024 / 1024:.1f} MB")
tracemalloc.stop()
```

## Debugging Checklist

### Phase 1: REPRODUCE
- [ ] Document exact error message or unexpected behavior
- [ ] Identify steps to reproduce consistently
- [ ] Note environmental factors (OS, browser, data)
- [ ] Create minimal test case
- [ ] Verify issue exists in different environments

### Phase 2: GATHER
- [ ] Collect all error messages and stack traces
- [ ] Review relevant log files
- [ ] Check system metrics (CPU, memory, disk)
- [ ] Identify recent changes (code, configuration, data)
- [ ] Gather user reports and patterns

### Phase 3: HYPOTHESIZE
- [ ] List possible root causes
- [ ] Prioritize hypotheses by likelihood
- [ ] Define tests for each hypothesis
- [ ] Consider both direct and indirect causes
- [ ] Review similar past issues

### Phase 4: TEST
- [ ] Test hypotheses systematically
- [ ] Change only one variable at a time
- [ ] Document test results
- [ ] Verify fix resolves original issue
- [ ] Test for regression in other areas

## Advanced Debugging Techniques

### Binary Search Debugging

When dealing with large codebases or data sets:

```bash
# Git bisect for finding regression
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
# Git will check out commits to test
git bisect run ./test_script.sh
```

### Rubber Duck Debugging

Explain the problem step-by-step to:
- Identify assumptions and gaps
- Clarify understanding
- Generate new hypotheses
- Spot overlooked details

### Collaborative Debugging

**Pair Debugging:**
- Fresh perspective on the problem
- Knowledge sharing and learning
- Faster hypothesis generation
- Reduced debugging tunnel vision

**Debug Sessions:**
- Screen sharing for real-time collaboration
- Systematic walkthrough of the issue
- Collective problem-solving

## Prevention Strategies

### Defensive Programming

**Input Validation:**
```python
def process_user_data(data):
    if not isinstance(data, dict):
        raise ValueError(f"Expected dict, got {type(data)}")

    if 'email' not in data:
        raise ValueError("Missing required field: email")

    if not data['email'] or '@' not in data['email']:
        raise ValueError(f"Invalid email format: {data['email']}")
```

**Error Handling:**
```python
def fetch_user_profile(user_id):
    try:
        response = api_client.get(f"/users/{user_id}")
        return response.json()
    except requests.exceptions.ConnectionError:
        logger.error(f"Failed to connect to API for user {user_id}")
        raise
    except requests.exceptions.Timeout:
        logger.error(f"API timeout for user {user_id}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching user {user_id}: {e}")
        raise
```

### Monitoring and Observability

**Structured Logging:**
```python
import structlog

logger = structlog.get_logger()

def process_order(order_id):
    logger.info("Processing order", order_id=order_id)
    try:
        # Process order
        logger.info("Order processed successfully", order_id=order_id)
    except Exception as e:
        logger.error("Order processing failed",
                   order_id=order_id,
                   error=str(e))
        raise
```

**Health Checks:**
```python
def health_check():
    checks = {
        "database": check_database_connection(),
        "cache": check_cache_connection(),
        "external_api": check_external_api(),
    }

    all_healthy = all(checks.values())

    return {
        "status": "healthy" if all_healthy else "unhealthy",
        "checks": checks
    }
```

## Additional Resources

### Reference Files
For detailed debugging patterns and advanced techniques, consult:
- **`references/debugging-patterns.md`** - Common debugging patterns and anti-patterns
- **`references/tool-specific-guides.md`** - Debugging guides for specific tools and frameworks
- **`references/performance-debugging.md`** - Performance debugging and profiling techniques

### Example Files
Working debugging examples in `examples/`:
- **`examples/web-app-debugging.py`** - Complete web application debugging workflow
- **`examples/api-debugging-session.py`** - API debugging scenarios
- **`examples/performance-issue-analysis.py`** - Performance debugging example

### Scripts
Debugging utility scripts in `scripts/`:
- **`scripts/debug-session-logger.sh`** - Automated debugging session logging
- **`scripts/log-analyzer.py`** - Log file analysis and pattern detection
- **`scripts/system-health-check.sh`** - Comprehensive system health validation

## Success Metrics

### Debugging Efficiency
- Time to identify root cause
- Number of hypotheses tested
- Accuracy of initial hypothesis
- Resolution time

### Quality Improvement
- Reduced bug recurrence
- Improved error handling
- Better monitoring coverage
- Enhanced system reliability

Follow the 4-phase systematic approach to debug issues efficiently and build more robust systems through better understanding of failure modes and prevention strategies.