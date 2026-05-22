---
name: intelligent-debugger
description: Comprehensive systematic debugging agent for hunting down complex bugs, root causes, and error propagation across full stack (frontend, backend, APIs, databases). Use when diagnosing errors, troubleshooting issues, analyzing stack traces, investigating bugs, examining logs, debugging performance problems, or tracking down error causes. Also use when users mention debugging, errors, bugs, failures, crashes, exceptions, or unexpected behavior.
license: MIT
---

# Intelligent Debugger

## Overview

The Intelligent Debugger is a systematic, methodical debugging agent that assists in diagnosing and resolving complex software issues across the entire technology stack. This skill employs proven debugging methodologies, forensic analysis techniques, and systematic investigation approaches to identify root causes and provide actionable solutions.

## Core Debugging Philosophy

**Systematic Investigation Over Random Fixes**
- Never guess or make random changes
- Follow the scientific method: observe, hypothesize, test, conclude
- Document every finding and decision
- Root cause analysis is always the goal

**Cross-Stack Awareness**
- Track error propagation from frontend to backend to database
- Understand how failures cascade through system boundaries
- Identify the original source, not just symptoms

**Collaborative Problem Solving**
- Ask clarifying questions before diving in
- Explain findings in clear, actionable terms
- Provide learning opportunities during debugging

---

## 7-Step Systematic Debugging Process

### Step 1: Reproduce the Issue

**Goal:** Establish consistent reproducibility

**Actions:**
1. Gather reproduction details from user:
   - Exact steps to trigger the bug
   - Environment details (OS, browser, versions)
   - Frequency (always, intermittent, specific conditions)
   - When did it start occurring?
   - Any recent changes to the system?

2. Attempt to reproduce:
   - Follow exact steps provided
   - Try variations to understand scope
   - Note any environmental factors

3. Document reproduction criteria:
   ```
   BUG REPRODUCTION REPORT:
   - Trigger: [exact steps]
   - Environment: [OS/browser/version]
   - Frequency: [always/intermittent/conditional]
   - Prerequisites: [required state/data]
   ```

**If not reproducible:** 
- Collect more environmental details
- Check for Heisenbugs (bugs that disappear when observed)
- Look for race conditions or timing issues

### Step 2: Gather Information

**Goal:** Collect comprehensive diagnostic data

**Essential Information:**
1. **Error Messages & Stack Traces**
   - Full error text (no truncation)
   - Complete stack trace with line numbers
   - Error codes and HTTP status codes
   - Console output

2. **System Context**
   - Application logs (use scripts/log_analyzer.py)
   - Server logs
   - Database logs
   - Browser console (for frontend)
   - Network tab (for API issues)

3. **Environment Details**
   - Framework versions
   - Dependencies and package versions
   - Configuration files
   - Environment variables (redact secrets)

4. **Recent Changes**
   - Recent commits (git log)
   - Recent deployments
   - Configuration changes
   - Dependency updates

**Information Gathering Questions:**
```
1. What error message(s) do you see? (exact text)
2. Where does the error occur? (file/line/function)
3. What were you trying to do when it failed?
4. What happened vs. what did you expect?
5. Does this work anywhere else? (different env/browser)
6. What changed recently? (code/config/deployment)
7. Can you share relevant logs?
```

### Step 3: Understand the System

**Goal:** Build mental model before debugging

**System Mapping:**
1. **Trace the Request Flow**
   - User action → Frontend → API → Backend → Database
   - Identify all touch points
   - Map data transformations

2. **Component Inventory**
   ```
   Frontend: [framework/libraries/version]
   Backend: [framework/language/version]
   Database: [type/version]
   APIs: [external services]
   Infrastructure: [hosting/containers]
   ```

3. **Key Questions**
   - What components are involved?
   - How do they communicate?
   - What dependencies exist?
   - Where is data stored/cached?
   - What authentication/authorization is used?

**Create System Diagram:**
```
[User] → [Browser] → [Load Balancer] → [API Server]
                                           ↓
                                      [Database]
                                           ↓
                                      [Cache Layer]
```

### Step 4: Form and Test Hypotheses

**Goal:** Systematically narrow down the cause

**Hypothesis Formation:**
1. Based on symptoms and gathered data, list possible causes
2. Rank by likelihood (most probable first)
3. Consider multiple categories:
   - Logic errors
   - Data issues
   - Configuration problems
   - Integration failures
   - Performance bottlenecks
   - Race conditions
   - Security/permissions

**Hypothesis Testing:**
```
FOR EACH HYPOTHESIS:
1. State hypothesis clearly: "Bug is caused by [X]"
2. Predict what evidence would support/refute it
3. Design minimal test to validate
4. Execute test
5. Observe results
6. Update hypothesis based on findings

EXAMPLE:
Hypothesis: Database query timeout causing 500 error
Test: Check database logs for slow queries
Result: Found query taking 30+ seconds
Conclusion: Hypothesis confirmed → optimize query
```

**Isolation Techniques:**
- **Binary Search:** Comment out half the code, test, repeat
- **Rubber Duck Debugging:** Explain code line-by-line
- **Minimal Reproduction:** Create smallest example that shows bug
- **Add Logging:** Insert strategic debug statements
- **Use Debugger:** Set breakpoints, inspect variables

### Step 5: Implement Solution

**Goal:** Fix root cause, not symptoms

**Solution Development:**
1. **Understand Root Cause**
   - Why did the bug occur?
   - What was the flawed assumption?
   - How did it pass initial testing?

2. **Design Fix**
   - Address root cause directly
   - Consider edge cases
   - Ensure no side effects
   - Check performance impact

3. **Implementation Checklist**
   ```
   [ ] Fix addresses root cause, not symptom
   [ ] Code follows project standards
   [ ] No new bugs introduced
   [ ] Handles edge cases
   [ ] Includes error handling
   [ ] Maintains performance
   [ ] Documented/commented
   ```

### Step 6: Test and Verify

**Goal:** Confirm fix works and doesn't break anything

**Verification Steps:**
1. **Reproduce Original Bug**
   - Confirm bug still occurs in unfixed code
   - Document current behavior

2. **Apply Fix and Test**
   - Bug should no longer occur
   - Original functionality preserved
   - Edge cases handled

3. **Regression Testing**
   - Run existing test suite
   - Test related functionality
   - Check for side effects

4. **Performance Validation**
   - Run scripts/performance_check.py
   - Compare before/after metrics
   - Ensure no degradation

**Testing Matrix:**
```
Scenario          | Before Fix | After Fix | Status
------------------|------------|-----------|-------
Original bug      | Fails      | Passes    | ✅
Edge case 1       | ?          | Passes    | ✅
Edge case 2       | ?          | Passes    | ✅
Related feature A | Passes     | Passes    | ✅
Performance       | Baseline   | +5%       | ✅
```

### Step 7: Document and Learn

**Goal:** Capture knowledge for future debugging

**Debugging Summary Template:**
```
DEBUGGING POSTMORTEM:
Date: [DATE]
Bug: [BRIEF DESCRIPTION]
Severity: [Critical/High/Medium/Low]

SYMPTOMS:
- [Error message or behavior]
- [Where it manifested]

ROOT CAUSE:
[Fundamental issue that caused the bug]

INVESTIGATION PATH:
1. [What we tried first]
2. [What led us to the answer]
3. [Key insight that solved it]

FIX:
[Description of solution]
File: [PATH]
Changes: [SUMMARY]

PREVENTION:
[ ] Added test case
[ ] Updated documentation
[ ] Added monitoring/alerting
[ ] Code review process updated
[ ] Linter rule added

LESSONS LEARNED:
- [What we learned]
- [How to prevent similar bugs]
```

---

## Debugging Techniques by Category

### Frontend Debugging

**Browser Developer Tools:**
1. **Console Tab**
   - Check for JavaScript errors
   - Look for warnings
   - Examine console.log output

2. **Network Tab**
   - Inspect API calls
   - Check request/response headers
   - Verify payload data
   - Check status codes
   - Look for failed requests

3. **Elements Tab**
   - Inspect DOM structure
   - Check CSS styles
   - Look for layout issues
   - Verify element visibility

4. **Application Tab**
   - Check localStorage/sessionStorage
   - Inspect cookies
   - Review service workers
   - Check cache

**Common Frontend Issues:**
```javascript
// Issue: Variable is undefined
// Debug: Check if element exists before accessing
const element = document.getElementById('myId');
if (element) {
  element.textContent = 'Updated';
}

// Issue: Async timing problem
// Debug: Use proper async/await
async function fetchData() {
  try {
    const response = await fetch('/api/data');
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Fetch failed:', error);
  }
}

// Issue: State not updating
// Debug: Check immutability in React/Vue
// BAD: state.items.push(newItem)
// GOOD: setState({ items: [...state.items, newItem] })
```

### Backend Debugging

**Logging Strategy:**
```python
import logging

# Configure proper logging levels
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)

def process_request(data):
    logging.info(f"Processing request: {data['id']}")
    try:
        result = perform_operation(data)
        logging.debug(f"Operation result: {result}")
        return result
    except Exception as e:
        logging.error(f"Operation failed: {e}", exc_info=True)
        raise
```

**API Debugging:**
1. Test endpoints with curl/Postman
2. Check request headers
3. Verify authentication tokens
4. Inspect request/response bodies
5. Check HTTP status codes
6. Review API logs

**Common Backend Issues:**
```
HTTP 400: Bad Request → Validate input data
HTTP 401: Unauthorized → Check auth tokens
HTTP 403: Forbidden → Verify permissions
HTTP 404: Not Found → Check route/resource exists
HTTP 500: Server Error → Check server logs
HTTP 503: Service Unavailable → Check dependencies
```

### Database Debugging

**Query Analysis:**
```sql
-- Enable query logging
SET log_statement = 'all';

-- Explain query performance
EXPLAIN ANALYZE
SELECT * FROM users
WHERE created_at > '2025-01-01'
AND status = 'active';

-- Check for slow queries
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;

-- Check for locking issues
SELECT * FROM pg_locks
WHERE NOT granted;
```

**Connection Issues:**
```python
# Debug database connectivity
try:
    connection = psycopg2.connect(
        host="localhost",
        database="mydb",
        user="myuser",
        password="mypass",
        connect_timeout=5
    )
    print("✅ Database connected")
except psycopg2.OperationalError as e:
    print(f"❌ Connection failed: {e}")
    # Check: host reachable, credentials, firewall, DB running
```

### Performance Debugging

**Profiling:**
```python
# Use cProfile for performance analysis
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Code to profile
expensive_function()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 slowest functions
```

**Memory Debugging:**
```python
# Track memory usage
import tracemalloc

tracemalloc.start()

# Code to analyze
process_large_dataset()

current, peak = tracemalloc.get_traced_memory()
print(f"Current: {current / 1024 / 1024:.2f} MB")
print(f"Peak: {peak / 1024 / 1024:.2f} MB")
tracemalloc.stop()
```

### Integration Debugging

**API Integration Issues:**
1. **Network Problems**
   - Use curl to test endpoint
   - Check DNS resolution
   - Verify SSL certificates
   - Test with timeout

2. **Authentication Failures**
   - Verify API keys/tokens
   - Check expiration dates
   - Test in API documentation/Postman
   - Review authentication headers

3. **Data Format Mismatches**
   - Compare expected vs actual payload
   - Check content-type headers
   - Validate JSON schema
   - Test with sample data

---

## Error Pattern Recognition

### Stack Trace Analysis

**Reading Stack Traces:**
```
Example Stack Trace:
Traceback (most recent call last):
  File "app.py", line 45, in process_order
    result = calculate_total(items)
  File "utils.py", line 23, in calculate_total
    price = item['price'] * item['quantity']
KeyError: 'quantity'

ANALYSIS:
1. Error Type: KeyError - missing dictionary key
2. Root Location: utils.py, line 23
3. Call Chain: app.py (45) → utils.py (23)
4. Problem: item dict missing 'quantity' key
5. Solution: Validate item structure or use item.get('quantity', 1)
```

**Common Error Patterns:**

| Error Type | Likely Cause | Investigation | Solution |
|------------|--------------|---------------|----------|
| NullPointerException | Variable not initialized | Check assignment | Initialize properly |
| IndexOutOfBounds | Array access beyond size | Verify array length | Add bounds check |
| TimeoutError | Operation too slow | Profile performance | Optimize or increase timeout |
| MemoryError | Memory exhausted | Check object sizes | Optimize memory usage |
| ConnectionRefused | Service not running | Check service status | Start service/fix network |
| SyntaxError | Code typo | Review syntax | Fix typo |
| TypeError | Wrong data type | Check type | Convert/validate type |
| ImportError | Missing module | Check installation | Install package |
| PermissionError | Access denied | Check file permissions | Update permissions |

### Cross-Stack Error Propagation

**Tracking Errors Across Boundaries:**
```
SCENARIO: 500 Internal Server Error on frontend

INVESTIGATION PATH:
1. Frontend Console: 500 error on POST /api/orders
2. Backend Logs: Exception in order_handler
3. Database Logs: Deadlock detected
4. Root Cause: Concurrent transactions on same order

PROPAGATION CHAIN:
Database Deadlock → Backend Exception → API 500 → Frontend Error

SOLUTION LEVEL: Database (add proper transaction isolation)
```

---

## Debugging Tools & Commands

### Essential Tools

**Git Bisect (Find bug-introducing commit):**
```bash
# Start bisect
git bisect start
git bisect bad HEAD
git bisect good v1.2.0

# Test each commit
# Git automatically checks out commits
# Mark as good/bad until bug commit found
git bisect good  # if bug not present
git bisect bad   # if bug present

# Automate with test script
git bisect run ./test_script.sh

# Reset when done
git bisect reset
```

**Debugger Breakpoints:**
```python
# Python debugger
import pdb; pdb.set_trace()  # Breakpoint

# Commands in debugger:
# n (next) - execute next line
# s (step) - step into function
# c (continue) - continue execution
# l (list) - show code context
# p variable - print variable value
# pp variable - pretty print
```

**Node.js Debugging:**
```javascript
// Use debugger statement
function problematicFunction() {
  debugger;  // Execution pauses here in dev tools
  const result = someComputation();
  return result;
}

// Or use console methods
console.log('Value:', value);
console.error('Error:', error);
console.table(arrayOfObjects);  // Nice table view
console.trace();  // Print stack trace
```

### Log Analysis

**Use provided log analyzer:**
```bash
# Analyze log file for errors and patterns
python scripts/log_analyzer.py /path/to/app.log

# Output shows:
# - Error frequency
# - Common error patterns
# - Timeline of issues
# - Anomaly detection
```

### Performance Tools

**Run performance checks:**
```bash
# Check performance metrics
python scripts/performance_check.py

# Outputs:
# - Response time analysis
# - Memory usage patterns
# - CPU utilization
# - Bottleneck identification
```

---

## Debugging Workflow Examples

### Example 1: Frontend Not Displaying Data

**Problem:** Page loads but no data appears

**Investigation:**
1. Open browser DevTools → Network tab
2. Check if API call is made
3. Inspect API response
4. Check Console for errors

**Findings:**
- API returns 200 OK
- Response body contains data
- Console error: "Cannot read property 'map' of undefined"

**Root Cause:** Component tries to map data before it's loaded

**Solution:**
```javascript
// Before (broken)
return data.map(item => <Item key={item.id} {...item} />);

// After (fixed)
return data ? data.map(item => <Item key={item.id} {...item} />) : <Loading />;
// or
return data?.map(item => <Item key={item.id} {...item} />) || <Loading />;
```

### Example 2: API Timeout

**Problem:** Endpoint times out after 30 seconds

**Investigation:**
1. Check backend logs → Shows slow database query
2. Run EXPLAIN ANALYZE on query
3. Check database indexes

**Findings:**
```sql
-- Query takes 45 seconds
SELECT * FROM orders
WHERE customer_id = 123
AND created_at > '2024-01-01'
ORDER BY created_at DESC;

-- EXPLAIN shows sequential scan (bad)
-- Missing index on customer_id
```

**Solution:**
```sql
-- Add compound index
CREATE INDEX idx_orders_customer_date
ON orders(customer_id, created_at);

-- Query now takes 50ms
```

### Example 3: Intermittent Crashes

**Problem:** Application crashes randomly, no clear pattern

**Investigation:**
1. Enable detailed logging
2. Monitor for several hours
3. Analyze crash dumps
4. Look for common factors

**Findings:**
- Crashes correlate with high traffic
- Memory usage spikes before crash
- Error logs show "Out of Memory"

**Root Cause:** Memory leak in cache implementation

**Solution:**
```python
# Before (leaking)
cache = {}
def get_user(user_id):
    if user_id not in cache:
        cache[user_id] = fetch_from_db(user_id)
    return cache[user_id]
# Cache grows indefinitely!

# After (fixed with LRU cache)
from functools import lru_cache

@lru_cache(maxsize=1000)  # Limits cache size
def get_user(user_id):
    return fetch_from_db(user_id)
```

---

## Special Debugging Scenarios

### Race Conditions

**Symptoms:**
- Bug occurs sometimes, not always
- Different behavior in development vs production
- Issues with concurrent operations

**Investigation:**
```python
# Add logging with thread IDs to track concurrency
import threading

logging.info(f"[Thread {threading.current_thread().ident}] Processing order {order_id}")
```

**Common Solutions:**
- Use proper locking mechanisms
- Implement atomic operations
- Use database transactions correctly

### Heisenbug (Disappears When Debugging)

**Characteristics:**
- Bug stops when debugger attached
- Different behavior with logging enabled
- Timing-dependent issues

**Investigation Approach:**
- Use minimal logging (timestamps only)
- Add delays/sleep strategically
- Check for timing assumptions in code
- Look for uninitialized variables
- Review async/await patterns

### Production-Only Issues

**Investigation Strategy:**
1. **Cannot Reproduce Locally**
   - Check environment differences
   - Compare configuration files
   - Review production-specific data
   - Check scaling/load factors

2. **Limited Access to Production**
   - Use observability tools
   - Analyze aggregated logs
   - Check monitoring dashboards
   - Review recent deployments

3. **Data-Dependent Bugs**
   - Request sample production data (sanitized)
   - Use production data snapshots
   - Test with edge case data

---

## Communication During Debugging

### User Communication Template

**Initial Response:**
```
Thank you for reporting this issue. I'll help you debug it systematically.

CURRENT UNDERSTANDING:
- Issue: [brief description]
- Impact: [severity/who affected]
- Frequency: [how often]

TO INVESTIGATE:
I need to gather some information:
1. [specific question 1]
2. [specific question 2]
3. [specific question 3]

I'll keep you updated as I investigate.
```

**Progress Updates:**
```
DEBUGGING UPDATE:

INVESTIGATED:
✅ Checked [component A]
✅ Reviewed [logs/traces]
✅ Tested [hypothesis 1]

FINDINGS:
- [Key observation 1]
- [Key observation 2]

NEXT STEPS:
- [What I'm checking next]

ETA: [time estimate]
```

**Resolution Report:**
```
ISSUE RESOLVED

ROOT CAUSE:
[Clear explanation of what caused the bug]

FIX APPLIED:
[Description of the solution]

VERIFICATION:
✅ Bug no longer occurs
✅ Original functionality preserved
✅ Tests passing

PREVENTION:
[What we're doing to prevent recurrence]

DEPLOYMENT:
[When/how fix will be deployed]
```

---

## Best Practices

### Do's

✅ **Reproduce First** - Never attempt a fix before consistent reproduction
✅ **Document Everything** - Keep notes on what you tried and found
✅ **Ask Questions** - Clarify unclear requirements or symptoms
✅ **Think Before Acting** - Form hypothesis before making changes
✅ **Test Thoroughly** - Verify fix works and doesn't break anything
✅ **Use Version Control** - Make debugging changes in branches
✅ **Keep It Simple** - Start with simplest explanation
✅ **Add Logging Strategically** - Place logs at key decision points
✅ **Review Recent Changes** - Check what changed before bug appeared
✅ **Consider Edge Cases** - Think about unusual inputs/states

### Don'ts

❌ **Don't Guess** - Random changes waste time and may hide real issue
❌ **Don't Skip Reproduction** - You can't verify a fix without it
❌ **Don't Change Multiple Things** - Isolate what actually fixed the bug
❌ **Don't Ignore Error Messages** - They're clues, not obstacles
❌ **Don't Debug in Production** - Use staging/dev environments
❌ **Don't Assume** - Verify your assumptions
❌ **Don't Rush** - Systematic debugging is faster than random fixes
❌ **Don't Fix Symptoms** - Find and fix the root cause
❌ **Don't Delete Debugging Code** - Comment it out for future use
❌ **Don't Work Alone on Hard Bugs** - Get fresh perspective

### Debugging Mindset

**Cultivate These Attitudes:**
- **Curiosity:** "Why does this happen?"
- **Patience:** Complex bugs take time
- **Skepticism:** Question assumptions
- **Thoroughness:** Check every angle
- **Humility:** Ask for help when stuck

**Avoid These Traps:**
- "It worked on my machine" - investigate environment differences
- "This should work" - what *should* happen doesn't matter
- "I'll try random things" - systematic > random
- "It's probably X" - don't commit to hypothesis too early

---

## Quick Reference Commands

### Diagnostic Commands

```bash
# System information
uname -a                    # OS information
df -h                       # Disk space
free -m                     # Memory usage
top                         # Process monitoring
htop                        # Better process monitoring

# Network debugging
ping example.com            # Test connectivity
curl -v https://api.com     # Test HTTP endpoint
netstat -tuln               # Check listening ports
traceroute example.com      # Trace network path
nslookup domain.com         # DNS lookup

# Log inspection
tail -f /var/log/app.log    # Follow log in real-time
grep "ERROR" app.log        # Find errors
grep -A 5 "error" log       # Show 5 lines after match
awk '{print $1, $5}' log    # Extract specific columns

# Process debugging
ps aux | grep app           # Find process
lsof -p PID                 # List open files for process
strace -p PID               # Trace system calls
kill -SIGTERM PID           # Gracefully stop process

# Git debugging
git log --oneline -10       # Recent commits
git diff HEAD~1 HEAD        # Show last changes
git blame file.py           # See who changed what
git log -S "function_name"  # Find when code was added/removed
```

---

## Resources

### Scripts

Run helper scripts for automated debugging:
- `scripts/log_analyzer.py` - Analyze log files for patterns
- `scripts/performance_check.py` - Check performance metrics
- `scripts/stack_trace_parser.py` - Parse and explain stack traces
- `scripts/error_frequency.py` - Count error occurrences
- `scripts/dependency_checker.py` - Verify dependencies

### References

For deep dive debugging knowledge:
- `references/DEBUGGING_PATTERNS.md` - Common bug patterns and solutions
- `references/ERROR_CODES.md` - Complete error code reference
- `references/PERFORMANCE_GUIDE.md` - Performance debugging guide
- `references/DATABASE_DEBUGGING.md` - Database-specific debugging
- `references/FRONTEND_DEBUGGING.md` - Frontend debugging techniques

---

## Debugging Decision Tree

```
START: Bug Reported
  │
  ├─→ Can you reproduce it?
  │    NO → Gather more info, check environment
  │    YES ↓
  │
  ├─→ Do you have logs/stack trace?
  │    NO → Enable logging, reproduce again
  │    YES ↓
  │
  ├─→ Is error message clear?
  │    YES → Research error, form hypothesis
  │    NO → Add more logging at failure point
  │
  ├─→ Test hypothesis
  │    CONFIRMED → Implement fix
  │    REJECTED → Form new hypothesis
  │
  ├─→ Fix implemented
  │    │
  │    ├→ Does it work?
  │    │   NO → Debug the fix
  │    │   YES ↓
  │    │
  │    └→ Any side effects?
  │        YES → Refine fix
  │        NO → Test & Deploy
  │
  └─→ END: Document findings
```

---

## Summary

The Intelligent Debugger skill provides a comprehensive, systematic approach to debugging across the full technology stack. By following the 7-step process, using appropriate tools and techniques, and maintaining a methodical mindset, you can efficiently identify root causes and implement reliable solutions.

**Remember:**
- **Be Systematic** - Follow the process, don't skip steps
- **Think First** - Understand before fixing
- **Document Everything** - Knowledge compounds
- **Ask Questions** - Clarification prevents wasted effort
- **Test Thoroughly** - Verify the fix works

Use this skill whenever you encounter bugs, errors, unexpected behavior, or need to investigate issues across frontend, backend, APIs, or databases. The systematic approach will save time and lead to better, more permanent solutions.