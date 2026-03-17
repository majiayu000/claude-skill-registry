---
name: Troubleshooter
description: Debugging, error diagnosis, and problem resolution. USE WHEN user mentions bugs, errors, crashes, exceptions, not working, broken, debugging, fix, issue, problem, stack trace, logs, or asks why something isn't working correctly.
---

# Troubleshooter Skill

AI-powered debugging and problem diagnosis for identifying, analyzing, and resolving software issues with focus on systematic investigation, root cause analysis, and effective fixes.

## What This Skill Does

This skill provides expert-level troubleshooting guidance including error analysis, log interpretation, debugging strategies, root cause investigation, and fix implementation. It combines diagnostic best practices with practical, actionable solutions.

**Key Capabilities:**
- **Error Analysis**: Stack trace interpretation, exception diagnosis, error message decoding
- **Log Investigation**: Log parsing, pattern recognition, timeline reconstruction
- **Root Cause Analysis**: 5 Whys, fishbone diagrams, fault tree analysis
- **Debugging Strategies**: Breakpoints, watch expressions, step-through debugging
- **Performance Issues**: Bottleneck identification, memory leaks, slow queries
- **Integration Problems**: API failures, network issues, dependency conflicts

## Core Principles

### The Debugging Mindset
- **Reproduce First**: Can't fix what you can't see
- **Isolate Variables**: Change one thing at a time
- **Question Assumptions**: The bug is rarely where you think
- **Read the Error**: The message usually tells you what's wrong
- **Trust But Verify**: Check that fixes actually work

### Problem-Solving Hierarchy
1. **Understand** - What should happen vs. what is happening?
2. **Reproduce** - Can you make it happen consistently?
3. **Isolate** - Where exactly does it break?
4. **Identify** - What is the root cause?
5. **Fix** - What's the minimal change needed?
6. **Verify** - Does the fix work without side effects?

## Troubleshooting Workflow

### 1. Gather Information
```
Collect diagnostic data:
├── Error Messages (exact text, stack traces)
├── Logs (application, system, network)
├── Reproduction Steps (when, how, conditions)
├── Environment (OS, versions, configuration)
└── Recent Changes (deployments, updates, configs)
```

### 2. Analyze Symptoms
```
Classify the problem:
├── Type (crash, hang, incorrect output, performance)
├── Frequency (always, intermittent, once)
├── Scope (all users, specific users, specific conditions)
├── Timing (immediate, delayed, random)
└── Impact (critical, degraded, cosmetic)
```

### 3. Form Hypotheses
Generate and rank potential causes:
- Likelihood (how probable based on evidence)
- Testability (how easy to prove/disprove)
- Impact (if true, how significant)

### 4. Test & Fix
- Validate hypothesis with minimal test
- Implement fix if confirmed
- Verify fix in all affected scenarios
- Monitor for regression

## Common Error Categories

### Runtime Errors
| Error Type | Common Causes | Investigation |
|------------|---------------|---------------|
| **NullPointer/None** | Uninitialized variable, missing data | Check object chain, add null checks |
| **IndexOutOfBounds** | Wrong array size, off-by-one | Print collection sizes, check loops |
| **TypeError** | Wrong type passed, casting failure | Add type logging, check function signatures |
| **KeyError/AttrError** | Missing key/attribute | Print available keys, check data shape |
| **ImportError** | Missing dependency, wrong path | Check virtualenv, verify PYTHONPATH |

### Logic Errors
| Error Type | Common Causes | Investigation |
|------------|---------------|---------------|
| **Wrong Output** | Incorrect algorithm, bad data | Add intermediate prints, unit test |
| **Infinite Loop** | Missing exit condition | Add iteration counter, check conditions |
| **Race Condition** | Shared state, timing issues | Add locks, logging with timestamps |
| **Memory Leak** | Unclosed resources, circular refs | Profile memory, check cleanup |

### Integration Errors
| Error Type | Common Causes | Investigation |
|------------|---------------|---------------|
| **Connection Failed** | Wrong host/port, firewall | Test connectivity, check DNS |
| **Timeout** | Slow response, network issues | Increase timeout, check latency |
| **Auth Failed** | Wrong credentials, expired token | Verify creds, check expiration |
| **Parse Error** | Malformed response, wrong format | Log raw response, validate schema |

## Debugging Techniques

### Print/Log Debugging
```python
# Strategic logging for investigation
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def process_order(order):
    logger.debug(f"Processing order: {order.id}")
    logger.debug(f"Order items: {order.items}")
    logger.debug(f"Order total before discount: {order.subtotal}")
    
    try:
        discount = calculate_discount(order)
        logger.debug(f"Calculated discount: {discount}")
    except Exception as e:
        logger.error(f"Discount calculation failed: {e}", exc_info=True)
        raise
    
    final_total = order.subtotal - discount
    logger.debug(f"Final total: {final_total}")
    return final_total
```

### Binary Search Debugging
```
When you have a large codebase or change history:

1. Identify a known-good state (code worked here)
2. Identify the bad state (code broken here)
3. Test the midpoint
4. If broken, search first half; if working, search second half
5. Repeat until you find the breaking change

For git:
$ git bisect start
$ git bisect bad          # Current commit is broken
$ git bisect good abc123  # This commit was working
# Git checks out midpoint, you test, mark good/bad
```

### Rubber Duck Debugging
```
Explain the problem out loud (to yourself, a duck, or colleague):

1. "I expect this function to return the user's email"
2. "It receives the user_id parameter which is 123"
3. "It queries the database with SELECT email FROM users WHERE id = ..."
4. "Wait - I'm using user_id but the column is called id, not user_id!"

Often the act of explaining reveals the issue.
```

### Divide and Conquer
```python
# Isolate the failing component
def complex_function(data):
    step1_result = step1(data)
    print(f"After step1: {step1_result}")  # Works? ✓
    
    step2_result = step2(step1_result)
    print(f"After step2: {step2_result}")  # Works? ✓
    
    step3_result = step3(step2_result)
    print(f"After step3: {step3_result}")  # FAILS HERE! ✗
    
    return step4(step3_result)

# Now focus investigation on step3
```

## Stack Trace Analysis

### Python Stack Trace
```python
Traceback (most recent call last):
  File "app.py", line 45, in main           # ← Entry point
    result = process_data(data)
  File "processor.py", line 23, in process_data  # ← Called function
    cleaned = clean_input(raw)
  File "utils.py", line 12, in clean_input  # ← Where error occurred
    return data.strip().lower()
AttributeError: 'NoneType' object has no attribute 'strip'
                ↑ The actual error message
```
**Reading Strategy:** Start from the BOTTOM - that's where the error is. Work UP to understand the call chain.

### JavaScript Stack Trace
```javascript
TypeError: Cannot read property 'name' of undefined
    at getUserName (user.js:15:22)      // ← Immediate error location
    at displayProfile (profile.js:42:8)  // ← Caller
    at handleClick (app.js:88:3)         // ← Event handler
```

### Java Stack Trace
```java
java.lang.NullPointerException
    at com.app.Service.processUser(Service.java:45)  // ← Error here
    at com.app.Controller.handleRequest(Controller.java:23)
    at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
    ... 23 more  // Internal framework frames, usually ignore
```

## Log Analysis

### Effective Log Patterns
```
# Use structured logging
[2024-01-15T10:23:45.123Z] [ERROR] [user-123] [order-service] 
  message="Payment failed" 
  order_id=456 
  error_code="CARD_DECLINED"
  duration_ms=2340
```

### Log Investigation Commands
```bash
# Find errors in last hour
grep "ERROR" app.log | tail -100

# Count error types
grep "ERROR" app.log | awk '{print $4}' | sort | uniq -c | sort -rn

# Find all logs for specific request
grep "request_id=abc123" *.log

# Timeline of events for a user
grep "user_id=456" app.log | sort -k1

# Watch logs in real-time
tail -f app.log | grep --line-buffered "ERROR\|WARN"
```

### Correlation Across Systems
```
1. Get the timestamp of the error
2. Get request/correlation ID if available
3. Search all related services' logs for that ID
4. Build a timeline:
   
   10:23:45.100 [API Gateway] Received request req-123
   10:23:45.150 [User Service] Validating user for req-123
   10:23:45.200 [Order Service] Creating order for req-123
   10:23:45.800 [Payment Service] TIMEOUT processing req-123 ← ROOT CAUSE
   10:23:45.850 [Order Service] Payment failed for req-123
   10:23:45.900 [API Gateway] Returning 500 for req-123
```

## Root Cause Analysis

### The 5 Whys Technique
```
Problem: Application crashed in production

Why? → The database connection pool was exhausted
Why? → Connections weren't being returned to the pool  
Why? → Exception handlers weren't closing connections
Why? → The error handling code was copied without the cleanup
Why? → No code review caught the missing cleanup ← ROOT CAUSE

Fix: Add connection cleanup in finally block + add code review checklist item
```

### Fishbone Diagram (Ishikawa)
```
                    People           Process
                      │                 │
                      │  Untrained      │  No code review
                      │  developer      │  Poor testing
                      │       ↘         ↙
                       ╔═══════════════════╗
                       ║   APPLICATION     ║
                       ║     CRASH         ║
                       ╚═══════════════════╝
                      │       ↗         ↖
                      │  Missing         │  Legacy 
                      │  logging         │  framework
                      │                  │
                 Technology          Environment
```

## Performance Troubleshooting

### Identifying Bottlenecks
```python
# Simple timing decorator
import time
from functools import wraps

def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.3f}s")
        return result
    return wrapper

@timed
def slow_function():
    # Find what's slow
    pass
```

### Common Performance Issues
| Issue | Symptoms | Solution |
|-------|----------|----------|
| **N+1 Query** | Many DB queries, slow list pages | Use JOIN or batch fetch |
| **Memory Leak** | Growing memory, eventual crash | Profile, check unclosed resources |
| **Missing Index** | Slow queries, high CPU | Add database indexes |
| **Sync in Async** | Blocked event loop, timeouts | Use async libraries |
| **Large Payload** | Slow responses, timeout | Paginate, compress, lazy load |

### Profiling Commands
```bash
# Python CPU profiling
python -m cProfile -s cumtime script.py

# Python memory profiling  
python -m memory_profiler script.py

# Node.js profiling
node --prof app.js
node --prof-process isolate-*.log > profile.txt

# Database query analysis
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
```

## Debugging Tools by Language

### Python
```bash
# Interactive debugger
python -m pdb script.py

# In code
import pdb; pdb.set_trace()  # Python 3.6
breakpoint()                  # Python 3.7+

# Commands
n     # next line
s     # step into
c     # continue
p var # print variable
l     # list source
w     # where (stack trace)
```

### JavaScript/Node.js
```bash
# Chrome DevTools
node --inspect script.js
# Then open chrome://inspect

# VS Code debugging
# Add launch.json configuration

# In code
debugger;  // Breakpoint when DevTools open
```

### Common IDE Debugging
```
1. Set breakpoint (click line number)
2. Start debug mode (F5 or debug button)
3. When stopped:
   - Inspect variables in watch/locals
   - Step over (F10) - execute line
   - Step into (F11) - enter function
   - Step out (Shift+F11) - exit function
   - Continue (F5) - run to next breakpoint
```

## When to Use This Skill

**Trigger Phrases:**
- "Why isn't this working..."
- "I'm getting an error..."
- "This crashes when..."
- "Help me debug..."
- "How do I fix..."
- "Something's broken..."
- "The logs show..."
- "It works locally but not in production..."

**Example Requests:**
1. "I'm getting a NullPointerException, here's the stack trace..."
2. "My API returns 500 but I don't know why"
3. "The application is slow, how do I find the bottleneck?"
4. "Tests pass locally but fail in CI"
5. "Why does this work in Python 3.9 but not 3.11?"
6. "Help me understand this error message"

## Troubleshooting Checklist

Before escalating or giving up:

- [ ] **Read the error message carefully** - It usually says what's wrong
- [ ] **Can you reproduce it?** - Consistent reproduction is crucial
- [ ] **What changed recently?** - Check git log, deployments, configs
- [ ] **Is it environment-specific?** - Works locally but not in prod?
- [ ] **Checked the logs?** - Look before, during, and after the error
- [ ] **Googled the exact error?** - Someone's probably seen this before
- [ ] **Simplified the problem?** - Can you reproduce with minimal code?
- [ ] **Asked for a second opinion?** - Fresh eyes often see what you miss

## Quick Diagnostic Commands

```bash
# Check if service is running
curl -v http://localhost:8080/health

# Test database connectivity
psql -h localhost -U user -d dbname -c "SELECT 1"

# Check port in use
netstat -tlnp | grep 8080  # Linux
lsof -i :8080              # macOS

# Check disk space
df -h

# Check memory
free -h                    # Linux
vm_stat                    # macOS

# Check recent file changes
find . -type f -mmin -30   # Modified in last 30 min

# Check process resource usage
top -p $(pgrep -f "python app.py")
```

## Integration with Other Skills

- **Architect**: Design issues often cause recurring bugs
- **Tester**: Tests help isolate and prevent bugs
- **Code Review**: Fresh eyes catch issues you miss
- **Performance**: Many bugs manifest as performance issues

---

*Skill designed for Thanos + Antigravity integration*
