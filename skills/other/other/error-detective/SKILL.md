---
name: error-detective
description: Systematic debugging and error resolution using the TRACE framework (Trace, Read, Analyze, Check, Execute). Use when debugging errors, analyzing stack traces, investigating failures, root cause analysis, or troubleshooting production issues.
---

# Error Detective - Systematic Debugging and Error Resolution

## Overview

Error Detective is a comprehensive debugging skill that applies systematic methodologies to identify, analyze, and resolve errors efficiently. Using the TRACE framework and structured analysis techniques, this skill guides you through debugging from initial error discovery to verified resolution.

## Core Capabilities

### Stack Trace Analysis
- Parse and interpret stack traces across multiple languages
- Identify root cause vs. symptom errors
- Extract relevant file paths and line numbers
- Understand call chains and error propagation

### Error Pattern Recognition
- Categorize errors by type (syntax, runtime, logic, integration)
- Identify common error patterns and anti-patterns
- Recognize framework-specific errors
- Map errors to likely root causes

### Root Cause Analysis
- Distinguish between symptoms and underlying issues
- Follow error chains to original source
- Identify environmental vs. code issues
- Detect configuration and dependency problems

### Debugging Workflow Management
- Structured investigation process
- Hypothesis generation and testing
- Iterative refinement of understanding
- Documentation of findings and solutions

## The TRACE Framework

TRACE is a systematic five-step approach to debugging any error:

### T - Trace the Error
**Objective**: Capture complete error information and context

1. **Collect the full error message**
   - Complete stack trace (not just first few lines)
   - Error type and message
   - Timestamp and occurrence frequency
   - Environment where error occurred

2. **Identify error location**
   - Exact file and line number
   - Function or method where error occurred
   - Code context (surrounding lines)
   - Call stack from entry point to error

3. **Gather reproduction steps**
   - Minimal steps to reproduce
   - Input data or parameters used
   - Expected vs. actual behavior
   - Consistency of reproduction (always, intermittent, rare)

### R - Read the Error Message
**Objective**: Extract all information from the error itself

1. **Parse error components**
   - Error type/class (TypeError, ValueError, etc.)
   - Error message content
   - Suggested fixes (if provided)
   - Related errors or warnings

2. **Understand error semantics**
   - What the error type means in this language/framework
   - What conditions trigger this error
   - What the error message is specifically telling you
   - Any error codes or status codes

3. **Identify error category**
   - Syntax error (code won't parse)
   - Runtime error (code crashes during execution)
   - Logic error (wrong results, no crash)
   - Integration error (external system failure)
   - Performance error (timeout, resource exhaustion)

### A - Analyze the Context
**Objective**: Understand the broader context around the error

1. **Code analysis**
   - Review the failing line and surrounding code
   - Check recent changes to this code
   - Examine function/method signature and usage
   - Review related code that calls or is called by failing code

2. **Data analysis**
   - Inspect input values at point of failure
   - Check data types and structures
   - Verify data meets expected format/constraints
   - Identify edge cases or unexpected values

3. **Environment analysis**
   - Check dependencies and versions
   - Review configuration files
   - Verify environment variables
   - Confirm required resources are available (files, network, memory)

4. **State analysis**
   - Application state at time of error
   - Previous operations that led to this state
   - Shared state or global variables involved
   - Database or external system state

### C - Check for Root Cause
**Objective**: Identify the underlying issue, not just symptoms

1. **Follow the error chain**
   - Start at bottom of stack trace (first error)
   - Work up to find originating cause
   - Distinguish between error origin and error handlers
   - Identify wrapped or re-thrown errors

2. **Test hypotheses**
   - Generate specific, testable hypotheses
   - Isolate variables (change one thing at a time)
   - Use logging/debugging tools to verify assumptions
   - Document which hypotheses are confirmed or rejected

3. **Common root causes**
   - **Null/undefined values**: Missing initialization or validation
   - **Type mismatches**: Incorrect data type passed or returned
   - **Off-by-one errors**: Array/loop boundary issues
   - **Race conditions**: Timing-dependent failures
   - **Resource exhaustion**: Memory, disk, connections depleted
   - **Configuration errors**: Wrong settings or missing config
   - **Dependency issues**: Version conflicts or missing libraries
   - **Permission errors**: Insufficient access rights
   - **Network errors**: Connectivity, timeout, DNS issues
   - **Data corruption**: Invalid or unexpected data format

### E - Execute the Fix
**Objective**: Implement and verify the solution

1. **Design the fix**
   - Address root cause, not symptoms
   - Consider side effects and edge cases
   - Plan for backward compatibility if needed
   - Choose most maintainable solution

2. **Implement carefully**
   - Make minimal, targeted changes
   - Add validation and error handling
   - Include logging for future debugging
   - Document the fix and reasoning

3. **Verify thoroughly**
   - Confirm original error is resolved
   - Test with reproduction steps
   - Test edge cases and related functionality
   - Verify no new errors introduced

4. **Document and prevent**
   - Document what caused the error
   - Document the solution and why it works
   - Add tests to prevent regression
   - Update documentation or add warnings if needed

## Debugging Workflow

### Initial Assessment (5 minutes)

```
1. Read complete error message
2. Identify error type and severity
3. Check if error is reproducible
4. Assess impact (blocking, degraded, cosmetic)
5. Decide investigation priority
```

### Deep Investigation (15-30 minutes)

```
1. Apply TRACE framework systematically
2. Use debugging tools (see scripts/debug_helper.py)
3. Generate and test hypotheses
4. Document findings as you go
5. Narrow down to root cause
```

### Solution Implementation (varies)

```
1. Design fix addressing root cause
2. Implement with proper error handling
3. Add logging and validation
4. Test thoroughly
5. Document solution
```

### Verification and Prevention (10 minutes)

```
1. Verify fix with original reproduction steps
2. Test related functionality
3. Add regression tests
4. Update documentation
5. Deploy and monitor
```

## Common Error Patterns by Language

### Python

**AttributeError: 'NoneType' has no attribute 'X'**
- Root cause: Variable is None when expecting object
- Check: Initialization, function return values, API responses
- Fix: Add null checks, ensure proper initialization

**KeyError: 'key_name'**
- Root cause: Dictionary missing expected key
- Check: Data source, parsing logic, key spelling
- Fix: Use .get() with default, validate data structure

**ImportError / ModuleNotFoundError**
- Root cause: Module not installed or not in path
- Check: requirements.txt, virtual environment, PYTHONPATH
- Fix: Install missing package, fix import path

**IndentationError**
- Root cause: Inconsistent spacing (tabs vs spaces)
- Check: Editor settings, copied code
- Fix: Standardize to spaces (PEP 8), use linter

### JavaScript/TypeScript

**TypeError: Cannot read property 'X' of undefined**
- Root cause: Accessing property on undefined object
- Check: Object initialization, async timing, API responses
- Fix: Optional chaining (?.operator), null checks

**ReferenceError: X is not defined**
- Root cause: Variable used before declaration or out of scope
- Check: Variable declaration, scope, hoisting issues
- Fix: Declare variable, fix scope, check imports

**Promise rejection / Uncaught (in promise)**
- Root cause: Async operation failed without catch handler
- Check: API calls, file operations, async/await usage
- Fix: Add .catch() or try/catch with await

**SyntaxError: Unexpected token**
- Root cause: Invalid syntax, often from parsing JSON or code
- Check: JSON structure, bracket matching, semicolons
- Fix: Validate JSON, fix syntax, check for copy/paste errors

### Java

**NullPointerException**
- Root cause: Method called on null object reference
- Check: Object initialization, method return values
- Fix: Add null checks, use Optional, ensure initialization

**ClassNotFoundException**
- Root cause: Class not found in classpath
- Check: Dependencies, build configuration, package structure
- Fix: Add dependency, fix classpath, check package/class names

**ConcurrentModificationException**
- Root cause: Collection modified during iteration
- Check: Nested loops, multi-threading, iterator usage
- Fix: Use iterator.remove(), CopyOnWriteArrayList, or synchronization

## Error Severity Classification

### Critical (Fix Immediately)
- Application crashes or won't start
- Data loss or corruption
- Security vulnerabilities
- Production outages
- Payment or transaction failures

### High (Fix Soon)
- Major features broken
- Degraded performance affecting users
- Error affects multiple users
- Workarounds are complex

### Medium (Schedule Fix)
- Minor features broken
- Cosmetic issues with impact
- Errors with easy workarounds
- Edge case failures

### Low (Backlog)
- Cosmetic issues
- Minor improvements
- Rare edge cases
- Non-critical warnings

## Debugging Tools and Techniques

### Logging Best Practices

```python
import logging

# Configure structured logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Log with context
logger = logging.getLogger(__name__)
logger.debug(f"Processing item: {item_id}, user: {user_id}")
logger.error(f"Failed to process: {error}", exc_info=True)
```

### Strategic Breakpoints

1. **At error location**: Catch exact state when error occurs
2. **Before error**: Check inputs and preconditions
3. **After error**: See how error propagates
4. **At decision points**: Verify logic branches
5. **In loops**: Check iteration variables

### Print Debugging (Strategic)

```python
# Add contextual debug prints
print(f"DEBUG: function_name called with {param1=}, {param2=}")
print(f"DEBUG: variable state before operation: {var=}")
print(f"DEBUG: condition check: {condition=}, result: {result=}")
```

### Binary Search Debugging

When error location is unclear:
1. Add checkpoint in middle of code path
2. Determine if error before or after checkpoint
3. Repeat in remaining half
4. Converge on error location quickly

### Rubber Duck Debugging

Explain code line-by-line to someone (or something):
1. Forces you to examine assumptions
2. Often reveals errors during explanation
3. Clarifies complex logic
4. Identifies knowledge gaps

## Using the Debug Helper Script

The `scripts/debug_helper.py` utility provides automated assistance:

```bash
# Parse stack trace from file
python scripts/debug_helper.py parse-trace error.log

# Extract error patterns
python scripts/debug_helper.py analyze-log application.log

# Start debug session (creates log)
python scripts/debug_helper.py session start "Login error investigation"

# Add notes to session
python scripts/debug_helper.py session note "Tested with different users - same error"

# Close session with solution
python scripts/debug_helper.py session close "Fixed: Added null check for user.profile"
```

## Best Practices

### Do's

- **Read error messages completely**: Don't skip details
- **Reproduce consistently**: Ensure reliable reproduction before debugging
- **Change one thing at a time**: Isolate what fixes the problem
- **Document as you go**: Record hypotheses, tests, findings
- **Use version control**: Commit before debugging, can revert if needed
- **Add tests**: Prevent regression after fixing
- **Fix root cause**: Don't just patch symptoms
- **Share knowledge**: Document solutions for team

### Don'ts

- **Don't assume**: Verify your assumptions with data
- **Don't skip reading errors**: Error messages contain crucial information
- **Don't make multiple changes**: Can't tell what fixed it
- **Don't delete code impulsively**: Comment out first, understand why it was there
- **Don't ignore warnings**: Today's warning is tomorrow's error
- **Don't fix without understanding**: May break something else
- **Don't forget to test**: Verify fix works and doesn't introduce new issues

## Common Debugging Scenarios

### Scenario 1: "It Worked Yesterday"

**Approach:**
1. Check recent changes (git diff, git log)
2. Review dependency updates
3. Check environment changes
4. Look for time-dependent logic
5. Compare configurations between environments

**Common Causes:**
- Recent code changes
- Updated dependencies
- Configuration changes
- Database schema changes
- External API changes
- Certificate expiration

### Scenario 2: "Works on My Machine"

**Approach:**
1. Compare environments (OS, dependencies, configs)
2. Check environment variables
3. Verify file paths and permissions
4. Compare data between environments
5. Look for hardcoded assumptions

**Common Causes:**
- Different dependency versions
- Missing environment variables
- Different file paths
- Database state differences
- Operating system differences
- Missing configuration files

### Scenario 3: "Intermittent Failures"

**Approach:**
1. Identify failure pattern (timing, frequency, conditions)
2. Look for race conditions
3. Check resource availability
4. Review concurrent operations
5. Add extensive logging
6. Increase reproduction attempts

**Common Causes:**
- Race conditions
- Memory leaks
- External service instability
- Network issues
- Timing-dependent logic
- Resource exhaustion

### Scenario 4: "Error in Production Only"

**Approach:**
1. Check production-specific configuration
2. Review production data characteristics
3. Check production load/scale
4. Examine production dependencies
5. Review security/permission settings

**Common Causes:**
- Production data edge cases
- Scale/load issues
- Production-specific configuration
- Different security policies
- Firewall or network restrictions
- Production-only integrations

## Advanced Techniques

### Bisect Debugging (Git)

Find which commit introduced a bug:

```bash
git bisect start
git bisect bad                 # Current version has bug
git bisect good v1.2.0        # Version 1.2.0 was working
# Git checks out middle commit
# Test and mark as good/bad
git bisect good/bad
# Repeat until git identifies culprit commit
git bisect reset
```

### Heisenbug (Observer Effect)

Errors that disappear when debugging:

**Strategies:**
- Add logging without breakpoints
- Use production-like environment for debugging
- Review timing and concurrency issues
- Check for initialization/timing dependencies
- Use non-intrusive monitoring

### Memory Profiling

For memory leaks and performance:

```python
# Python memory profiling
import tracemalloc

tracemalloc.start()
# ... run code ...
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

for stat in top_stats[:10]:
    print(stat)
```

### Network Debugging

For API and integration errors:

**Tools:**
- Browser DevTools Network tab
- curl with verbose flag (-v)
- Postman for API testing
- Wireshark for packet inspection
- Network proxy (Charles, Fiddler)

**Check:**
- Request/response headers
- Status codes
- Request/response body
- Timing (latency, timeout)
- SSL/TLS issues

## Quick Reference

### TRACE Framework Quick Checklist

```
☐ T - TRACE
  ☐ Full error message captured
  ☐ Stack trace collected
  ☐ Reproduction steps documented
  ☐ Environment identified

☐ R - READ
  ☐ Error type identified
  ☐ Error message analyzed
  ☐ Error category determined
  ☐ Related errors checked

☐ A - ANALYZE
  ☐ Code reviewed
  ☐ Data inspected
  ☐ Environment verified
  ☐ State examined

☐ C - CHECK
  ☐ Error chain followed
  ☐ Hypotheses tested
  ☐ Root cause identified
  ☐ Assumptions verified

☐ E - EXECUTE
  ☐ Fix designed
  ☐ Fix implemented
  ☐ Fix verified
  ☐ Prevention measures added
```

### Error Priority Matrix

```
Impact →     Low        Medium       High        Critical
Frequency ↓
High         Medium     High         Critical    Critical
Medium       Low        Medium       High        Critical
Low          Low        Low          Medium      High
Rare         Backlog    Low          Medium      High
```

## Additional Resources

### Examples
- `examples/debugging_workflow.md` - Step-by-step debugging process examples
- `examples/common_errors.md` - Catalog of frequent error patterns and solutions
- `examples/stack_traces.txt` - Annotated stack trace examples with analysis

### Scripts
- `scripts/debug_helper.py` - Python debugging utilities for trace parsing and session management

### Further Learning
- Language-specific debugging documentation
- Framework error handling guides
- Profiling and performance analysis tools
- Testing and quality assurance practices

---

**Remember**: Debugging is detective work. Be systematic, be patient, and let the evidence guide you to the truth. Every error message is a clue waiting to be understood.
