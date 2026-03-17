---
name: debugging
description: Systematic debugging strategies and error analysis patterns. Auto-triggers when investigating bugs, analyzing stack traces, or troubleshooting issues.
---

# Debugging Skill

## The Scientific Method of Debugging

1. **Observe**: Gather information about the bug
2. **Hypothesize**: Form theories about the cause
3. **Predict**: What should happen if hypothesis is correct?
4. **Test**: Verify the hypothesis
5. **Iterate**: Refine or reject, repeat

## Information Gathering Checklist

- [ ] Error message and full stack trace
- [ ] Steps to reproduce (exact sequence)
- [ ] Expected vs actual behavior
- [ ] Environment details (OS, versions, config)
- [ ] Recent changes (commits, deployments)
- [ ] Frequency (always, intermittent, first occurrence)
- [ ] Impact scope (one user, all users, specific conditions)

## Debugging Strategies

### Binary Search (Bisect)
```bash
# Git bisect to find breaking commit
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
# Test each commit, mark good/bad until found
```

### Rubber Duck Debugging
1. Explain the code line-by-line out loud
2. State what each line SHOULD do
3. Compare expectations to actual behavior
4. The explanation often reveals the bug

### Wolf Fence Algorithm
1. Insert a check in the middle of the code
2. Determine which half contains the bug
3. Repeat, narrowing down to the exact location

### Minimal Reproducible Example
1. Remove unrelated code
2. Simplify inputs
3. Isolate the failing case
4. Create standalone reproduction

## Common Bug Categories

### Logic Errors
- Off-by-one errors in loops
- Incorrect boolean logic
- Wrong operator (= vs ==)
- Missing null checks
- Race conditions

### State Errors
- Uninitialized variables
- Stale state/cache
- Mutation of shared state
- Incorrect order of operations

### Integration Errors
- API contract mismatches
- Serialization/deserialization issues
- Timezone handling
- Encoding problems (UTF-8)

### Resource Errors
- Memory leaks
- Connection pool exhaustion
- File handle leaks
- Deadlocks

## Debugging Tools by Language

### JavaScript/TypeScript
```javascript
// Conditional breakpoints
debugger;

// Console methods
console.log(value);
console.table(array);
console.trace();
console.time('operation');
console.timeEnd('operation');

// Chrome DevTools
// - Network tab for API calls
// - Performance tab for profiling
// - Memory tab for leak detection
```

### Python
```python
# Built-in debugger
import pdb; pdb.set_trace()

# IPython debugger (better UX)
import ipdb; ipdb.set_trace()

# Logging
import logging
logging.debug(f"Variable value: {var}")

# Profiling
import cProfile
cProfile.run('function()')
```

### General
```bash
# Trace system calls
strace -f ./program

# Network debugging
tcpdump -i any port 8080
curl -v http://localhost:8080

# Memory debugging
valgrind ./program
```

## Error Message Analysis

### Stack Trace Reading
1. Start from the bottom (root cause)
2. Find YOUR code (not library code)
3. Note the line number and function
4. Check the error type and message

### Common Patterns
```
NullPointerException → Missing null check
TypeError → Wrong type passed/returned
KeyError/IndexError → Invalid key/index access
ConnectionError → Network/service issue
TimeoutError → Operation too slow or hanging
```

## When Stuck

1. Take a break (fresh eyes help)
2. Explain the problem to someone else
3. Search error message (include quotes)
4. Check recent changes in version control
5. Question your assumptions
6. Add more logging/instrumentation
7. Try to make it worse (understanding helps)
