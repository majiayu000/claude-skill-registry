---
name: debugging-systematic
description: Apply systematic root cause analysis and debugging methodologies to diagnose and fix bugs, test failures, and unexpected behavior. Use when encountering production issues, investigating test failures, diagnosing performance problems, tracing error sources through call stacks, analyzing logs and stack traces, reproducing inconsistent bugs, debugging race conditions, investigating memory leaks, or applying scientific method to problem-solving before proposing fixes.
---

# Systematic Debugging - Root Cause Analysis Framework

## When to use this skill

- Encountering bugs or unexpected application behavior
- Investigating test failures and flaky tests
- Diagnosing production issues and outages
- Tracing error sources through complex call stacks
- Analyzing logs, stack traces, and error messages
- Reproducing intermittent or hard-to-replicate bugs
- Debugging race conditions and timing issues
- Investigating memory leaks or performance degradation
- Root cause analysis before proposing fixes
- Debugging integration issues between services
- Investigating data corruption or inconsistencies
- Applying scientific method to systematic problem-solving

## When to use this skill

- Encountering bugs, test failures, unexpected behavior, or production issues - BEFORE proposing fixes.
- When working on related tasks or features
- During development that requires this expertise

**Use when**: Encountering bugs, test failures, unexpected behavior, or production issues - BEFORE proposing fixes.

## Core Philosophy

**Never guess at fixes.** Always understand the root cause first.

```
❌ Bad: "Let's try adding a timeout here"
✅ Good: "The timeout is occurring because X. Here's proof: [evidence]"
```

## Four-Phase Framework

### Phase 1: Root Cause Investigation
**Goal**: Understand exactly what's happening and why

```
1. Reproduce the issue reliably
   - Minimal reproduction case
   - Consistent reproduction steps
   - Document environment/conditions

2. Gather evidence
   - Error messages (full stack traces)
   - Logs (with timestamps and context)
   - State at failure point
   - Input data that triggers issue

3. Form hypothesis
   - Based on evidence, not guesswork
   - Specific and testable
   - Includes mechanism of failure
```

**Example**:
```
Bug: User authentication fails intermittently

Investigation:
1. Reproduced: Fails every ~10th login attempt
2. Evidence: 
   - Error: "Invalid token signature"
   - Logs show token created at 14:32:15, validated at 14:32:17
   - Server logs show time drift between auth & API servers
3. Hypothesis: Clock skew causing token validation failures
   - Auth server: 14:32:15
   - API server: 14:32:10 (5 seconds behind)
   - Token "not yet valid" due to nbf (not before) claim
```

### Phase 2: Pattern Analysis
**Goal**: Understand if this is isolated or systemic

```
1. Check for similar issues
   - Same error in other places?
   - Same pattern in related code?
   - Recurring in error logs?

2. Identify scope
   - One function or entire subsystem?
   - One user or all users?
   - One environment or all?

3. Find common factors
   - Timing (time of day, duration)?
   - Data characteristics?
   - Execution path?
```

### Phase 3: Hypothesis Testing
**Goal**: Prove understanding with experiments

```
1. Design tests that prove/disprove hypothesis
2. Add instrumentation if needed
3. Run experiments systematically
4. Document results
```

**Example Tests**:
```typescript
// Hypothesis: Clock skew causes token failures

// Test 1: Artificially set server clocks in sync
// Result: No failures in 100 attempts ✓

// Test 2: Increase token nbf tolerance to 10 seconds  
// Result: No failures in 100 attempts ✓

// Test 3: Log exact time delta when failures occur
// Result: All failures show 4-6 second clock difference ✓

// Conclusion: Hypothesis confirmed
```

### Phase 4: Implementation
**Goal**: Fix root cause, not symptoms

```
1. Address root cause
   - Fix underlying issue
   - Not just surface symptoms
   
2. Add safeguards
   - Validation
   - Error handling
   - Monitoring

3. Verify fix
   - Reproducer no longer triggers issue
   - Related edge cases handled
   - No new issues introduced
```

## Debugging Techniques

### 1. **Binary Search Debugging**
For "it broke somewhere between working and now":

```bash
# Git bisect example
git bisect start
git bisect bad HEAD        # Current broken state
git bisect good v1.2.0     # Last known working

# Git will checkout commits for testing
# Test each: git bisect good / git bisect bad
# Automatically finds breaking commit
```

### 2. **Differential Debugging**
Compare working vs. broken:

```
Working environment:
- Node 18.16.0
- Dependency A v2.1.0
- Feature flag X: off

Broken environment:  
- Node 18.17.0  ← Suspect
- Dependency A v2.1.0
- Feature flag X: off

Test: Change Node version → Bug disappears → Root cause found
```

### 3. **Instrumentation**
Add strategic logging:

```typescript
// Not enough information
function processUser(user) {
  const result = complexOperation(user);
  return result; // Fails sometimes, why?
}

// Rich instrumentation
function processUser(user) {
  logger.debug('processUser start', { 
    userId: user.id, 
    userState: user.state,
    timestamp: Date.now() 
  });
  
  const result = complexOperation(user);
  
  logger.debug('processUser complete', { 
    userId: user.id, 
    resultStatus: result.status,
    duration: Date.now() - start 
  });
  
  return result;
}
```

### 4. **Rubber Duck Debugging**
Explain the problem out loud:

```
"When a user clicks login, we:
1. Hash their password ← Wait, are we using the same salt?
2. Compare to database
3. ... oh. We changed the salt algorithm last week."
```

### 5. **Time Travel Debugging**
Use debugger to step backwards:

```
Modern debuggers (rr, WinDbg, Chrome DevTools) can:
- Record execution
- Replay backwards
- Find exact moment state became invalid
```

## Common Root Causes

### 1. **Race Conditions**
```typescript
// Symptom: Intermittent failures, works in debugger
// Root cause: Async operations completing in wrong order

// Bad
let userData = null;
fetchUser().then(data => userData = data); // Async
sendEmail(userData.email); // Runs before fetch completes! ❌

// Fixed  
const userData = await fetchUser();
sendEmail(userData.email); // ✓
```

### 2. **Shared Mutable State**
```typescript
// Symptom: Tests pass individually, fail together
// Root cause: Tests sharing state

// Bad - shared state
const cache = {}; // Global
test('test1', () => { cache.foo = 'bar'; });
test('test2', () => { expect(cache.foo).toBeUndefined(); }); // Fails! ❌

// Fixed - isolated state
test('test1', () => { 
  const cache = {}; 
  cache.foo = 'bar'; 
});
test('test2', () => { 
  const cache = {}; 
  expect(cache.foo).toBeUndefined(); 
}); // ✓
```

### 3. **Incorrect Assumptions**
```typescript
// Symptom: Crashes with certain inputs
// Root cause: Assumed data always present

// Bad - assumes email exists
function sendWelcome(user) {
  sendEmail(user.email); // Crashes if email is null ❌
}

// Fixed - validate assumptions
function sendWelcome(user) {
  if (!user?.email) {
    logger.warn('Cannot send welcome email', { userId: user.id });
    return;
  }
  sendEmail(user.email); // ✓
}
```

### 4. **Off-by-One Errors**
```typescript
// Symptom: Array index errors, missing last item
// Root cause: Loop boundary wrong

// Bad
for (let i = 0; i < array.length - 1; i++) { // Misses last element ❌
  process(array[i]);
}

// Fixed
for (let i = 0; i < array.length; i++) { // ✓
  process(array[i]);
}
// Or better: array.forEach(process);
```

### 5. **Timezone Issues**
```typescript
// Symptom: Date calculations wrong for some users
// Root cause: Not handling timezones

// Bad
const deadline = new Date('2024-01-01'); // Midnight in what timezone? ❌

// Fixed
const deadline = new Date('2024-01-01T00:00:00Z'); // Explicit UTC
// Or use library: dayjs.utc('2024-01-01')
```

## Debugging Checklist

```
□ Can you reproduce the issue reliably?
□ Do you have the full error message and stack trace?
□ Do you know the exact input that triggers the issue?
□ Have you checked recent changes (git log)?
□ Have you verified your assumptions with logging?
□ Have you isolated the failing component?
□ Do you understand WHY it fails (not just WHERE)?
□ Have you tested your fix against the reproducer?
□ Have you added tests to prevent regression?
□ Have you checked for similar issues elsewhere?
```

## When to Ask for Help

Ask when:
- Stuck after 2+ hours of systematic investigation
- Issue involves unfamiliar subsystem
- Reproducer is inconsistent

**But first, prepare**:
```markdown
## Issue Description
[What's broken]

## Reproduction Steps
1. [Exact steps]
2. [Expected vs actual]

## Investigation So Far
- [What I've tried]
- [What I've ruled out]
- [Current hypothesis]

## Evidence
- [Logs, errors, screenshots]
- [Minimal code reproducer]

## Environment
- OS, versions, configuration
```

## Anti-Patterns to Avoid

### ❌ **Shotgun Debugging**
```
"Let me try changing this... and this... and this..."
→ You don't know what actually fixed it
```

### ❌ **printf Debugging Overload**
```
Adding print statements everywhere without a plan
→ Noise obscures signal
```

### ❌ **Assuming It's Not Your Code**
```
"Must be a framework bug"
→ 95% of the time, it's your code
```

### ❌ **Fixing Symptoms, Not Root Cause**
```
Bug: Crashes with large files
Bad fix: Add try/catch to hide error ❌
Good fix: Implement streaming to handle large files ✓
```

## Advanced Techniques

### Core Dump Analysis
```bash
# When process crashes
gdb program core
(gdb) bt          # backtrace
(gdb) info locals # local variables
(gdb) frame 3     # inspect frame
```

### Network Debugging
```bash
# Capture traffic
tcpdump -i any -w capture.pcap

# Analyze with Wireshark
wireshark capture.pcap

# Or use Charles Proxy, mitmproxy
```

### Performance Profiling
```typescript
// Node.js
node --prof app.js
node --prof-process isolate-*.log

// Chrome DevTools
// Performance tab → Record → Analyze flame graph
```

## Resources

- [Debugging Guide by Julia Evans](https://jvns.ca/debugging-attitude/)
- [The Art of Debugging by Norman Matloff](https://www.amazon.com/Art-Debugging-GDB-DDD-Eclipse/dp/1593271743)
- [Effective Debugging by Diomidis Spinellis](https://www.spinellis.gr/debugging/)

---

**Remember**: Debugging is a skill. The more systematic your approach, the faster you'll find root causes and the fewer bugs you'll introduce with "fixes" that don't address the real problem.
