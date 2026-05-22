---
name: vscode-bug-hunter
description: This skill provides systematic bug detection and discovery capabilities for VS Code extensions. Use when searching for hidden bugs, analyzing code for potential issues, investigating suspicious behavior, performing code audits, or proactively finding bugs before they manifest. Covers static analysis patterns, dynamic analysis techniques, code smell detection, and systematic codebase investigation.
---

# VS Code Bug Hunter

## Overview

This skill enables systematic discovery and detection of bugs in VS Code extensions before they cause problems in production. It provides structured workflows for proactively finding issues through static analysis, pattern matching, code auditing, and systematic investigation techniques.

## When to Use This Skill

- Proactively searching for bugs in extension code
- Auditing code for potential issues before release
- Investigating suspicious behavior patterns
- Analyzing code for memory leaks, race conditions, or security vulnerabilities
- Performing systematic code reviews
- Finding bugs that haven't manifested yet
- Preparing for release by identifying hidden issues

## Bug Hunting vs Debugging

| Bug Hunting (This Skill) | Debugging (vscode-extension-debugger) |
|--------------------------|--------------------------------------|
| Proactive discovery | Reactive fixing |
| Find bugs before they manifest | Fix bugs after they occur |
| Static and dynamic analysis | Error investigation |
| Code auditing | Stack trace analysis |
| Pattern-based detection | Reproduction-based fixing |

## Bug Detection Workflow

### Phase 1: Reconnaissance

Gather intelligence about the codebase before hunting.

#### 1.1 Map the Codebase Structure

```bash
# Find all TypeScript files
find src -name "*.ts" | head -20

# Identify key components
grep -r "export class" src/ --include="*.ts" | head -20

# Find entry points
grep -r "activate\|deactivate" src/ --include="*.ts"
```

#### 1.2 Identify High-Risk Areas

High-risk areas are more likely to contain bugs:

| Area | Risk Level | Reason |
|------|------------|--------|
| Async operations | High | Race conditions, unhandled rejections |
| Event handlers | High | Memory leaks, missing dispose |
| WebView communication | High | Message timing, state sync |
| File I/O | Medium | Error handling, permissions |
| User input processing | Medium | Validation, injection |
| Configuration handling | Medium | Type mismatches, defaults |
| UI rendering | Low | Visual issues, layout |

#### 1.3 Review Recent Changes

```bash
# Recent commits - often contain fresh bugs
git log --oneline -20

# Files changed recently
git diff --name-only HEAD~10

# Diff for specific file
git diff HEAD~5 -- src/path/to/suspicious/file.ts
```

### Phase 2: Static Analysis

Analyze code without executing it.

#### 2.1 Pattern-Based Bug Detection

Search for known bug patterns:

**Memory Leak Patterns**
```typescript
// Pattern: Event listener without dispose
// Search: addEventListener|on\w+\s*\(
// Risk: Memory leak if listener not removed

// Pattern: setInterval/setTimeout without clear
// Search: setInterval|setTimeout
// Risk: Timer continues after disposal

// Pattern: Missing dispose registration
// Search: vscode\.\w+\.on\w+\(
// Risk: Event handler leaks
```

**Race Condition Patterns**
```typescript
// Pattern: Shared mutable state without lock
// Search: private \w+ = (?!readonly)
// Risk: Concurrent modification

// Pattern: Check-then-act without atomicity
// Search: if \(.*\)\s*\{[^}]*await
// Risk: State may change between check and act

// Pattern: Promise without await in loop
// Search: for.*\{[^}]*(?<!await)\s+\w+\([^)]*\)
// Risk: Uncontrolled concurrency
```

**Null/Undefined Patterns**
```typescript
// Pattern: Optional chaining missing
// Search: \.\w+\.\w+\.\w+(?!\?)
// Risk: Null reference in chain

// Pattern: Type assertion without check
// Search: as \w+(?!\s*\|)
// Risk: Runtime type mismatch

// Pattern: Array access without bounds check
// Search: \[\d+\]|\[.*\](?!\?)
// Risk: Index out of bounds
```

#### 2.2 Automated Search Commands

```bash
# Find potential memory leaks
grep -rn "addEventListener\|setInterval\|setTimeout" src/ --include="*.ts"

# Find missing error handling
grep -rn "catch\s*{\s*}" src/ --include="*.ts"

# Find TODO/FIXME comments (often mark known issues)
grep -rn "TODO\|FIXME\|HACK\|BUG\|XXX" src/ --include="*.ts"

# Find console.log (should be removed in production)
grep -rn "console\.\(log\|debug\|info\)" src/ --include="*.ts"

# Find async functions without try-catch
grep -rn "async.*{" src/ --include="*.ts" | head -20
```

#### 2.3 TypeScript Compiler Analysis

```bash
# Strict type checking
npx tsc --noEmit --strict

# Find implicit any
npx tsc --noEmit --noImplicitAny

# Check for unused variables
npx tsc --noEmit --noUnusedLocals --noUnusedParameters
```

### Phase 3: Semantic Analysis

Understand code behavior beyond syntax.

#### 3.1 Control Flow Analysis

Trace execution paths to find issues:

```typescript
// Identify all entry points to a function
// Search for: functionName(

// Trace data flow through function
// What inputs can reach this code path?
// What state can this code modify?

// Find unreachable code
// Code after return/throw/break/continue
```

#### 3.2 State Analysis

Track state changes:

```typescript
// Questions to ask:
// 1. What state does this component manage?
// 2. What operations modify this state?
// 3. Can state become inconsistent?
// 4. Is state properly initialized?
// 5. Is state properly cleaned up?
```

#### 3.3 Lifecycle Analysis

Verify proper lifecycle management:

```typescript
// For each resource:
// 1. Where is it created?
// 2. Where is it disposed?
// 3. Can disposal be skipped?
// 4. Is disposal order correct?
// 5. Are references cleared after disposal?
```

### Phase 4: Dynamic Analysis

Analyze code behavior during execution.

#### 4.1 Runtime Monitoring

Add temporary instrumentation:

```typescript
// Wrap suspicious function to monitor calls
const original = object.suspiciousMethod;
object.suspiciousMethod = function(...args) {
  console.log('[MONITOR] suspiciousMethod called with:', args);
  const result = original.apply(this, args);
  console.log('[MONITOR] suspiciousMethod returned:', result);
  return result;
};
```

#### 4.2 Memory Profiling

```typescript
// Track object creation
const instances = new WeakSet();
const originalConstructor = SuspiciousClass;
SuspiciousClass = class extends originalConstructor {
  constructor(...args) {
    super(...args);
    instances.add(this);
    console.log('[MEMORY] New instance created, count:', instances.size);
  }
};
```

#### 4.3 Performance Profiling

```typescript
// Measure function execution time
const start = performance.now();
await suspiciousOperation();
const duration = performance.now() - start;
console.log(`[PERF] Operation took ${duration}ms`);
```

### Phase 5: Hypothesis Testing

Form and test hypotheses about potential bugs.

#### 5.1 Hypothesis Formation

```
Template:
IF [condition/action]
THEN [expected buggy behavior]
BECAUSE [root cause theory]

Example:
IF rapid terminal creation requests are made
THEN duplicate terminals may be created
BECAUSE there is no atomic lock on the creation operation
```

#### 5.2 Test Design

```typescript
// Design test to confirm hypothesis
describe('Bug Hypothesis: Rapid terminal creation causes duplicates', () => {
  it('should handle concurrent creation requests', async () => {
    const manager = new TerminalManager();

    // Trigger the suspected bug condition
    const results = await Promise.all([
      manager.createTerminal(),
      manager.createTerminal(),
      manager.createTerminal()
    ]);

    // Verify expected behavior
    const uniqueIds = new Set(results.map(t => t.id));
    expect(uniqueIds.size).toBe(results.length);
  });
});
```

## Bug Categories Reference

### Category 1: Resource Leaks

**Memory Leaks**
- Event listeners not removed
- Timers not cleared
- References not nullified
- Closures capturing large objects

**Handle Leaks**
- File handles not closed
- WebView panels not disposed
- Terminal processes not killed
- Watchers not stopped

### Category 2: Concurrency Issues

**Race Conditions**
- Check-then-act patterns
- Shared mutable state
- Non-atomic operations
- Missing synchronization

**Deadlocks**
- Circular dependencies
- Nested locks
- Resource contention

### Category 3: State Issues

**Invalid State**
- Uninitialized variables
- Stale state references
- Inconsistent state transitions
- Missing state validation

**State Corruption**
- Concurrent modification
- Partial updates
- Missing rollback on failure

### Category 4: Error Handling Issues

**Missing Error Handling**
- Uncaught exceptions
- Unhandled promise rejections
- Silent failures
- Missing validation

**Incorrect Error Handling**
- Swallowed errors
- Wrong error type caught
- Incomplete cleanup on error

### Category 5: Security Issues

**Injection Vulnerabilities**
- Command injection
- Path traversal
- XSS in WebView

**Information Disclosure**
- Sensitive data in logs
- Error messages revealing internals
- Debug information in production

## Quick Reference Commands

### Find Memory Leaks
```bash
grep -rn "addEventListener\|on.*=.*function" src/ --include="*.ts" | grep -v "dispose\|remove"
```

### Find Missing Error Handling
```bash
grep -rn "\.then\(" src/ --include="*.ts" | grep -v "\.catch\("
```

### Find Potential Race Conditions
```bash
grep -rn "async.*{" src/ --include="*.ts" -A 5 | grep -E "if.*\{|while.*\{"
```

### Find Security Issues
```bash
grep -rn "eval\|innerHTML\|child_process\|exec\(" src/ --include="*.ts"
```

### Find Code Smells
```bash
grep -rn "any\|@ts-ignore\|@ts-nocheck" src/ --include="*.ts"
```

## Investigation Workflow Summary

1. **Reconnaissance**: Map codebase, identify high-risk areas
2. **Static Analysis**: Search for known bug patterns
3. **Semantic Analysis**: Understand control flow and state
4. **Dynamic Analysis**: Monitor runtime behavior
5. **Hypothesis Testing**: Form and test bug theories
6. **Documentation**: Record findings for fixing

## Resources

For detailed reference documentation:
- `references/detection-patterns.md` - Comprehensive bug pattern catalog
- `references/analysis-tools.md` - Static and dynamic analysis tool guide
- `references/investigation-checklist.md` - Systematic investigation procedures
