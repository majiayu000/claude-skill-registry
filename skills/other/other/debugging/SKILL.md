---
name: debugging
description: Comprehensive debugging specialist for errors, test failures, log analysis,
  and system problems. Use when encountering issues, analyzing error logs, investigating
  system anomalies, debugging production issues, analyzing stack traces, or identifying
  root causes. Combines general debugging workflows with error pattern detection and
  log analysis.
author: Joseph OBrien
status: unpublished
updated: '2025-12-23'
version: 1.0.1
tag: skill
type: skill
---

# Debugging

This skill provides comprehensive debugging capabilities for identifying and fixing errors, test failures, unexpected behavior, and production issues. It combines general debugging workflows with specialized error analysis, log parsing, and pattern recognition.

## When to Use This Skill

- When encountering errors or exceptions in code
- When tests are failing and you need to understand why
- When investigating unexpected behavior or bugs
- When analyzing stack traces and error messages
- When debugging production issues
- When fixing issues reported by users or QA
- When analyzing error logs and stack traces
- When investigating performance issues or anomalies
- When correlating errors across multiple services
- When identifying recurring error patterns
- When setting up error monitoring and alerting
- When conducting post-mortem analysis of incidents

## What This Skill Does

1. **Error Analysis**: Captures and analyzes error messages and stack traces
2. **Log Parsing**: Extracts errors from logs using regex patterns and structured parsing
3. **Stack Trace Analysis**: Analyzes stack traces across multiple programming languages
4. **Error Correlation**: Identifies relationships between errors across distributed systems
5. **Pattern Recognition**: Detects common error patterns and anti-patterns
6. **Reproduction**: Identifies steps to reproduce the issue
7. **Isolation**: Locates the exact failure point in code
8. **Root Cause Analysis**: Works backward from symptoms to identify underlying causes
9. **Minimal Fix**: Implements the smallest change that resolves the issue
10. **Verification**: Confirms the solution works and doesn't introduce new issues
11. **Monitoring Setup**: Creates queries and alerts for error detection

## Helper Scripts

This skill includes Python helper scripts in `scripts/`:

- **`parse_logs.py`**: Parses log files and extracts errors, exceptions, and stack traces. Outputs JSON with error analysis and pattern detection.

  ```bash
  python scripts/parse_logs.py /var/log/app.log
  ```

## How to Use

### Debug an Error

```
Debug this error: TypeError: Cannot read property 'x' of undefined
```

```
Investigate why the test is failing in test_user_service.js
```

### Analyze Error Logs

```
Analyze the error logs in /var/log/app.log and identify the root cause
```

```
Investigate why the API is returning 500 errors
```

### Pattern Detection

```
Find patterns in these error logs from the past 24 hours
```

```
Correlate errors between the API service and database
```

## Debugging Process

### 1. Capture Error Information

**Error Message:**

- Read the full error message
- Note the error type (TypeError, ReferenceError, etc.)
- Identify the error location (file and line number)

**Stack Trace:**

- Analyze the call stack
- Identify the sequence of function calls
- Find where the error originated

**Context:**

- Check recent code changes
- Review related code files
- Understand the execution flow

### 2. Error Extraction (Log Analysis)

**Using Helper Script:**

The skill includes a Python helper script for parsing logs:

```bash
# Parse log file and extract errors
python scripts/parse_logs.py /var/log/app.log
```

**Manual Log Parsing Patterns:**

```bash
# Extract errors from logs
grep -i "error\|exception\|fatal\|critical" /var/log/app.log

# Extract stack traces
grep -A 20 "Exception\|Error\|Traceback" /var/log/app.log

# Extract specific error types
grep "TypeError\|ReferenceError\|SyntaxError" /var/log/app.log
```

**Structured Log Parsing:**

```javascript
// Parse JSON logs
const errors = logs
  .filter(log => log.level === 'error' || log.level === 'critical')
  .map(log => ({
    timestamp: log.timestamp,
    message: log.message,
    stack: log.stack,
    context: log.context
  }));
```

### 3. Stack Trace Analysis

**Common Patterns:**

**JavaScript/Node.js:**

```
Error: Cannot read property 'x' of undefined
    at FunctionName (file.js:123:45)
    at AnotherFunction (file.js:456:78)
```

**Python:**

```
Traceback (most recent call last):
  File "app.py", line 123, in function_name
    result = process(data)
  File "utils.py", line 45, in process
    return data['key']
KeyError: 'key'
```

**Java:**

```
java.lang.NullPointerException
    at com.example.Class.method(Class.java:123)
    at com.example.AnotherClass.call(AnotherClass.java:456)
```

### 4. Error Correlation

**Timeline Analysis:**

- Group errors by timestamp
- Identify error spikes and patterns
- Correlate with deployments or changes
- Check for cascading failures

**Service Correlation:**

- Map errors across service boundaries
- Identify upstream/downstream relationships
- Track error propagation paths
- Find common failure points

### 5. Pattern Recognition

**Common Error Patterns:**

**N+1 Query Problem:**

```
Multiple database queries in loop
Pattern: SELECT * FROM users; SELECT * FROM posts WHERE user_id = ?
```

**Memory Leaks:**

```
Gradually increasing memory usage
Pattern: Memory growth over time without release
```

**Race Conditions:**

```
Intermittent failures under load
Pattern: Errors only occur with concurrent requests
```

**Timeout Issues:**

```
Requests timing out
Pattern: Errors after specific duration (e.g., 30s)
```

### 6. Reproduce the Issue

**Reproduction Steps:**

1. Identify the exact conditions that trigger the error
2. Create a minimal test case that reproduces the issue
3. Verify the issue is consistent and reproducible
4. Document the steps clearly

**Example:**

```markdown
## Reproduction Steps

1. Navigate to `/users/123`
2. Click "Edit Profile"
3. Submit form without filling required fields
4. Error occurs: "Cannot read property 'validate' of undefined"
```

### 7. Isolate the Failure Location

**Code Analysis:**

- Read the code around the error location
- Trace the execution path
- Identify where the assumption breaks
- Check variable states and values

**Debugging Techniques:**

- Add strategic logging to track execution
- Use debugger breakpoints
- Inspect variable states
- Check function return values
- Verify data structures

### 8. Form and Test Hypotheses

**Hypothesis Formation:**

- What could cause this error?
- What assumptions might be wrong?
- What edge cases weren't considered?
- What dependencies might be missing?

**Testing Hypotheses:**

- Add logging to verify assumptions
- Test edge cases
- Check input validation
- Verify dependencies are available
- Test with different data

### 9. Root Cause Analysis

**Investigation Steps:**

1. **Start with Symptoms**: What error is occurring?
2. **Work Backward**: What changed before the error?
3. **Check Patterns**: Is this recurring or isolated?
4. **Correlate Events**: What else happened at the same time?
5. **Identify Cause**: What is the underlying issue?

**Analysis Framework:**

```markdown
## Error Analysis

**Error**: [Description]
**Frequency**: [How often]
**Timeline**: [When it started]
**Affected Services**: [Which services]
**User Impact**: [How many users affected]

**Root Cause Hypothesis**:
- [Primary hypothesis with evidence]
- [Alternative hypotheses]

**Evidence**:
- [Log entries supporting hypothesis]
- [Error patterns observed]
- [Correlation with other events]

**Recommended Actions**:
- [Immediate fix]
- [Long-term prevention]
```

### 10. Implement Minimal Fix

**Fix Principles:**

- Fix the root cause, not just symptoms
- Make the smallest change possible
- Preserve existing functionality
- Don't introduce new complexity
- Add appropriate error handling

**Fix Verification:**

- Test the fix with the reproduction case
- Verify no regressions
- Check edge cases
- Ensure error handling is appropriate
- Confirm the fix is complete

### 11. Document the Solution

**Documentation Should Include:**

- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

## Examples

### Example 1: Null Reference Error

**Input**: Error: `TypeError: Cannot read property 'name' of undefined`

**Output**:

```markdown
## Debugging Analysis

### Error Information
- **Type**: TypeError
- **Location**: `src/services/user.js:45`
- **Message**: Cannot read property 'name' of undefined

### Root Cause
The `getUser()` function returns `undefined` when a user is not found, but the code assumes it always returns a user object.

### Code Location
```javascript
// src/services/user.js:45
const user = getUser(userId);
console.log(user.name); // ❌ Error: user is undefined
```

### Fix

```javascript
// Add null check
const user = getUser(userId);
if (!user) {
  throw new Error(`User ${userId} not found`);
}
console.log(user.name); // ✅ Safe
```

### Prevention

- Always validate return values from functions that might return null/undefined
- Use optional chaining: `user?.name`
- Add TypeScript types to catch these issues at compile time

```

### Example 2: Database Connection Errors (Log Analysis)

**Input**: Error logs showing database connection failures

**Output**:

```markdown
## Error Analysis: Database Connection Failures

### Pattern Detected

**Error**: `ECONNREFUSED` errors from PostgreSQL
**Frequency**: 15 errors/minute, started 2 hours ago
**Timeline**: Errors began after deployment at 14:30

### Root Cause Analysis

**Hypothesis**: Connection pool exhaustion

**Evidence**:
- Errors correlate with high traffic period (14:30-16:30)
- Connection pool size: 10, concurrent requests: 50+
- No connection cleanup in error handlers
- Errors spike during peak usage

**Code Location**: `src/db/connection.js:45`

**Fix**:
```javascript
// Add connection cleanup
try {
  const result = await query(sql);
  return result;
} catch (error) {
  // Ensure connection is released
  await releaseConnection();
  throw error;
}
```

**Monitoring Query**:

```sql
SELECT count(*) FROM pg_stat_activity WHERE state = 'active';
```

```

## Reference Files

For detailed debugging workflows, error patterns, and techniques, load reference files as needed:

- **`references/debugging_workflows.md`** - Common debugging workflows by issue type, language-specific debugging, debugging techniques, debugging checklists, and common error patterns (database errors, memory leaks, race conditions, timeouts, authentication errors, network errors, application errors, performance errors)
- **`references/INCIDENT_POSTMORTEM.template.md`** - Incident postmortem template with timeline, root cause analysis, and action items

When debugging specific types of issues or analyzing error patterns, load `references/debugging_workflows.md` and refer to the relevant section.

## Best Practices

### Debugging Approach

1. **Start with Symptoms**: Understand what's wrong before jumping to solutions
2. **Work Backward**: Trace from error to cause
3. **Test Hypotheses**: Don't assume, verify
4. **Minimal Changes**: Fix only what's necessary
5. **Verify Fixes**: Always test that the fix works

### Log Analysis Techniques

1. **Use Structured Logging**: JSON logs are easier to parse and analyze
2. **Include Context**: Add request IDs, user IDs, timestamps to all logs
3. **Log Levels**: Use appropriate levels (error, warn, info, debug)
4. **Correlation IDs**: Use request IDs to trace errors across services
5. **Error Grouping**: Group similar errors to identify patterns

### Error Pattern Recognition

**Time-Based Patterns:**
- Errors at specific times (deployment windows, peak hours)
- Errors after specific duration (timeouts, memory leaks)
- Errors during specific events (database migrations, cache clears)

**Frequency Patterns:**
- Sudden spikes (deployment issues, traffic spikes)
- Gradual increases (memory leaks, resource exhaustion)
- Intermittent (race conditions, timing issues)

**Correlation Patterns:**
- Errors in multiple services simultaneously (infrastructure issues)
- Errors after specific user actions (application bugs)
- Errors correlated with external services (dependency issues)

### Common Debugging Patterns

**Null/Undefined Checks:**
```javascript
// Always check for null/undefined
if (!value) {
  // Handle missing value
}
```

**Error Handling:**

```javascript
try {
  // Risky operation
} catch (error) {
  // Log error with context
  console.error('Operation failed:', error);
  // Handle gracefully
}
```

**Logging:**

```javascript
// Strategic logging
console.log('Before operation:', { userId, data });
const result = await operation();
console.log('After operation:', { result });
```

**Type Checking:**

```javascript
// Verify types
if (typeof value !== 'string') {
  throw new TypeError('Expected string');
}
```

### Monitoring Setup

**Error Rate Monitoring:**

```javascript
// Track error rate over time
const errorRate = errors.length / totalRequests;
if (errorRate > 0.01) { // 1% error rate threshold
  alert('High error rate detected');
}
```

**Error Alerting:**

- Alert on error rate spikes (> 5% increase)
- Alert on new error types
- Alert on critical error patterns
- Alert on error correlation across services

### Prevention Strategies

1. **Input Validation**: Validate all inputs at boundaries
2. **Type Safety**: Use TypeScript or type checking
3. **Error Boundaries**: Catch errors at appropriate levels
4. **Testing**: Write tests for edge cases
5. **Code Review**: Review code for common pitfalls

## Related Use Cases

- Fixing production bugs
- Debugging test failures
- Investigating user-reported issues
- Analyzing error logs
- Root cause analysis
- Performance debugging
- Production incident investigation
- System reliability analysis
- Error monitoring setup
- Post-mortem analysis
- Debugging distributed systems
