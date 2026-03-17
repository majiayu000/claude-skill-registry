---
description: >-
  Systematic, hypothesis-driven debugging workflow with triage-based track routing.
  Use when asked to "fix this bug", "debug this", "why is this failing",
  "this is broken", "investigate this error", "track down this issue",
  or any debugging situation. Supports --deep flag to force full investigation.
user-invocable: true
---

# Bug Killer — Hypothesis-Driven Debugging Workflow

Execute a systematic debugging workflow that enforces investigation before fixes. Every bug gets a hypothesis journal, evidence gathering, and root cause confirmation before any code changes.

**CRITICAL: Complete ALL 5 phases.** The workflow is not complete until Phase 5: Wrap-up & Report is finished. After completing each phase, immediately proceed to the next phase without waiting for user prompts.

## Phase Overview

1. **Triage & Reproduction** — Understand, reproduce, route to quick or deep track
2. **Investigation** — Gather evidence with language-specific techniques
3. **Root Cause Analysis** — Confirm root cause through hypothesis testing
4. **Fix & Verify** — Fix with proof, regression test, quality check
5. **Wrap-up & Report** — Document trail, capture learnings

---

## Phase 1: Triage & Reproduction

**Goal:** Understand the bug, reproduce it, and decide the investigation track.

### 1.1 Parse Context

Extract from `$ARGUMENTS` and conversation context:
- **Bug description**: What's failing? Error messages, symptoms
- **Reproduction steps**: How to trigger the bug (test command, user action, etc.)
- **Environment**: Language, framework, test runner, relevant config
- **Prior attempts**: Has the user already tried fixes? What didn't work?
- **Deep flag**: If `--deep` is present, skip triage and go directly to deep track (jump to Phase 2 deep track)

### 1.2 Reproduce the Bug

Attempt to reproduce before investigating:

1. If a failing test was mentioned, run it:
   ```bash
   # Run the specific test to confirm the failure
   <test-runner> <test-file>::<test-name>
   ```
2. If an error was described, find and trigger it
3. If neither, search for related test files and run them

**Capture the exact error output** — this is your primary evidence.

If the bug cannot be reproduced:
- Ask the user for more context via the `question` tool
- Check if it's environment-specific or intermittent
- Note "not yet reproduced" in the hypothesis journal

### 1.3 Form Initial Hypothesis

Based on the error message and context, form your first hypothesis:

```markdown
### H1: [Title]
- Hypothesis: [What you think is causing the bug]
- Evidence for: [What supports this — error message, stack trace, etc.]
- Evidence against: [Anything that contradicts it — if none yet, say "None yet"]
- Test plan: [Specific steps to confirm or reject]
- Status: Pending
```

### 1.4 Route to Track

**Quick-fix signals** (ALL must be true):
- Clear, specific error message pointing to exact location
- Localized to 1-2 files (not spread across the codebase)
- Obvious fix visible from reading the error location
- No concurrency, timing, or state management involved

**Deep-track signals** (ANY one triggers deep track):
- Bug spans 3+ files or modules
- Root cause unclear from the error message alone
- Intermittent or environment-dependent failure
- Involves concurrency, timing, shared state, or async behavior
- User already tried fixes that didn't work
- Generic error message (e.g., "null reference" without clear origin)
- Stack trace points to library/framework code rather than application code

**Present your assessment** via the `question` tool:
- Summarize the bug and your initial hypothesis
- Recommend quick or deep track with justification
- Options: "Quick track (Recommended)" / "Deep track" / "Deep track" / "Quick track" — depending on your assessment
- Let the user override your recommendation

**Track escalation rule:** If during quick track execution, 2 hypotheses are rejected, automatically escalate to deep track. Preserve all hypothesis journal entries when escalating.

---

## Phase 2: Investigation

**Goal:** Gather evidence systematically, guided by language-specific techniques.

### 2.1 Load Language Reference

Detect the primary language of the bug's context and load the appropriate reference inline from the sections below.

| Language | Reference Section |
|----------|-----------------|
| Python | See "Python Debugging Reference" section below |
| TypeScript / JavaScript | See "TypeScript/JavaScript Debugging Reference" section below |
| Other / Multiple | See "General Debugging Reference" section below |

Always also reference the "General Debugging Reference" section as a supplement when using a language-specific section.

### 2.2 Quick Track Investigation

For quick-track bugs, investigate directly:

1. **Read the error location** — the file and function where the error occurs
2. **Read the immediate callers** — 1-2 files up the call chain
3. **Check recent changes** — `git log --oneline -5 -- <file>` for the affected files
4. **Update hypothesis** — does the evidence support H1? Add evidence for/against

Proceed to Phase 3 (quick track).

### 2.3 Deep Track Investigation

For deep-track bugs, use parallel exploration agents:

1. **Plan exploration areas** — identify 2-3 focus areas based on the bug:
   - Focus 1: The error site and immediate code path
   - Focus 2: Data flow and state management leading to the error
   - Focus 3: Related subsystems, configuration, or external dependencies

2. **Launch code-explorer agents:**

   Spawn 2-3 code-explorer agents using the `task` tool with `command: "code-explorer"`:

   ```
   Use task tool with command: "code-explorer"

   Prompt for each agent:
   Bug context: [description of the bug and error]
   Focus area: [specific area for this agent]

   Investigate this focus area in relation to the bug:
   - Find all relevant files
   - Trace the execution/data path
   - Identify where behavior diverges from expected
   - Note any suspicious patterns, recent changes, or known issues
   - Report structured findings
   ```

   Launch agents in parallel for independent focus areas.

3. **Synthesize exploration results:**
   - Collect findings from all agents
   - Identify convergence (multiple agents pointing to same area)
   - Update hypothesis journal with new evidence
   - Form additional hypotheses if evidence warrants (aim for 2-3 total)

Proceed to Phase 3 (deep track).

---

## Phase 3: Root Cause Analysis

**Goal:** Confirm the root cause through systematic hypothesis testing.

### 3.1 Quick Track Root Cause

For quick-track bugs:

1. **Verify the hypothesis:**
   - Read the specific code identified in Phase 2
   - Trace the logic step-by-step
   - Confirm that the hypothesized cause produces the observed error

2. **If confirmed** (Status → Confirmed):
   - Update H1 with confirming evidence
   - Proceed to Phase 4

3. **If rejected** (Status → Rejected):
   - Update H1 with evidence against and reason for rejection
   - Form a new hypothesis (H2) based on what you learned
   - Investigate H2 following Phase 2 quick track steps
   - **If H2 is also rejected → escalate to deep track**
   - Preserve all journal entries, continue with Phase 2 deep track

### 3.2 Deep Track Root Cause

For deep-track bugs:

1. **Prepare hypotheses for testing:**
   - You should have 2-3 hypotheses from Phase 2
   - Each needs a concrete test plan (how to confirm or reject)

2. **Launch bug-investigator agents:**

   Spawn 1-3 bug-investigator agents using the `task` tool with `command: "bug-investigator"` to test hypotheses in parallel:

   ```
   Use task tool with command: "bug-investigator"

   Prompt for each agent:
   Bug context: [description of the bug and error]

   Hypothesis to test: [specific hypothesis]
   Test plan:
   1. [Step 1 — e.g., run this specific test with these arguments]
   2. [Step 2 — e.g., check git blame for this function]
   3. [Step 3 — e.g., trace the data from input to error site]

   Report your findings with verdict (confirmed/rejected/inconclusive),
   evidence, and recommendations.
   ```

   Launch agents in parallel when they test independent hypotheses.

3. **Evaluate results:**
   - Update hypothesis journal with each agent's findings
   - If one hypothesis is confirmed → proceed to Phase 4
   - If all are rejected/inconclusive → apply 5 Whys technique:

     Take the strongest "inconclusive" finding and ask "why?" iteratively:
     ```
     Observed: [what actually happens]
     Why? → [first-level cause]
     Why? → [second-level cause]
     Why? → [root cause]
     ```
   - Form new hypotheses from 5 Whys analysis and repeat investigation

4. **If stuck after 2 rounds of investigation:**
   - Present all findings to the user via the `question` tool
   - Share the hypothesis journal
   - Ask for additional context or direction
   - Options: "Continue investigating", "Try a different angle", "Provide more context"

---

## Phase 4: Fix & Verify

**Goal:** Fix the root cause and prove the fix works.

### 4.1 Design the Fix

Before writing any code:

1. **Explain the root cause** — state clearly what's wrong and why
2. **Explain the fix** — describe what will change and WHY it addresses the root cause
3. **Identify affected files** — list every file that needs modification
4. **Consider side effects** — could this fix break other behavior?

### 4.2 Implement the Fix

1. **Read all files** that will be modified before making changes
2. **Apply the fix** using the `edit` tool — minimal, focused changes
3. **Match existing patterns** — follow the codebase's conventions

### 4.3 Run Tests

1. **Run the originally failing test** — it should now pass:
   ```bash
   <test-runner> <test-file>::<test-name>
   ```

2. **Run related tests** — tests in the same file and nearby test files:
   ```bash
   <test-runner> <test-directory>
   ```

3. If tests fail:
   - Determine if the failure is related to the fix or pre-existing
   - If related, revise the fix (do NOT revert to a different approach without updating the hypothesis journal)
   - If pre-existing, note it but don't let it block the fix

### 4.4 Write Regression Test

Write a test that would have caught this bug:

1. The test should fail WITHOUT the fix (verifying it tests the right thing)
2. The test should pass WITH the fix
3. The test should be minimal — test the specific behavior that was broken
4. Place it in the appropriate test file following project conventions

### 4.5 Deep Track: Quality Check and Related Issues

**Deep track only — skip on quick track.**

1. **Load code-quality skill:**

   Invoke: skill({ name: "code-quality" })

   Review the fix against code quality principles.

2. **Check for related issues:**
   - Search for the same pattern elsewhere in the codebase:
     ```
     Grep for the pattern that caused the bug
     ```
   - If the same bug exists in other locations, report them to the user
   - Ask via the `question` tool: "Fix all related instances now?" / "Fix only the reported bug" / "Create tasks for related fixes"

---

## Phase 5: Wrap-up & Report

**Goal:** Document the investigation trail and capture learnings.

### 5.1 Bug Fix Summary

Present to the user:

```markdown
## Bug Fix Summary

### Bug
[One-line description of the bug]

### Root Cause
[What was actually wrong and why]

### Fix Applied
[What was changed, with file:line references]

### Tests
- [Originally failing test]: Now passing
- [Regression test added]: [test name and location]
- [Related tests]: All passing

### Track
[Quick / Deep] [Escalated from quick: Yes/No]
```

### 5.2 Hypothesis Journal Recap

Present the complete hypothesis journal showing the investigation trail:

```markdown
### Investigation Trail

#### H1: [Title]
- Status: Confirmed / Rejected
- [Key evidence summary]

#### H2: [Title] (if applicable)
- Status: Confirmed / Rejected
- [Key evidence summary]

[... additional hypotheses ...]
```

### 5.3 Project Learnings

Load the `project-learnings` skill to evaluate whether this bug reveals project-specific knowledge worth capturing:

Invoke: skill({ name: "project-learnings" })

Follow its workflow to evaluate the finding. Common debugging discoveries that qualify:
- Surprising API behavior specific to this project
- Undocumented conventions that caused the bug
- Architectural constraints that aren't obvious from the code

### 5.4 Deep Track: Future Recommendations

**Deep track only:**

If the investigation revealed broader concerns, present recommendations:
- Architecture improvements to prevent similar bugs
- Missing test coverage areas
- Documentation gaps
- Monitoring or alerting suggestions

### 5.5 Next Steps

Offer the user options via the `question` tool:
- "Commit the fix" — proceed to commit workflow
- "Review the changes" — show a diff of all modifications
- "Run full test suite" — run the complete test suite to verify no regressions
- "Done" — wrap up the session

---

## Hypothesis Journal

The hypothesis journal is the core artifact of this workflow. Maintain it throughout all phases.

### Format

```markdown
## Hypothesis Journal — [Bug Title]

### H1: [Descriptive Title]
- **Hypothesis:** [What's causing the bug — be specific]
- **Evidence for:** [Supporting observations with file:line references]
- **Evidence against:** [Contradicting observations]
- **Test plan:** [Concrete steps to confirm or reject]
- **Status:** Pending / Confirmed / Rejected
- **Notes:** [Additional context, timestamps, agent findings]

### H2: [Descriptive Title]
[Same format]
```

### Rules

- **Minimum hypotheses:** 1 on quick track, 2-3 on deep track
- **Never delete entries** — rejected hypotheses are valuable context
- **Update incrementally** — add evidence as you find it, don't wait
- **Be specific** — "the data is wrong" is not a hypothesis; "processOrder receives dollars but expects cents" is

---

## Track Reference

| Aspect | Quick Track | Deep Track |
|--------|-------------|------------|
| Investigation | Read error location + 1-2 callers | 2-3 code-explorer agents in parallel |
| Hypotheses | Minimum 1 | Minimum 2-3 |
| Root cause testing | Manual verification | 1-3 bug-investigator agents in parallel |
| Fix validation | Run failing + related tests | Tests + code-quality skill + related issue scan |
| Auto-escalation | After 2 rejected hypotheses | N/A |
| Typical complexity | Off-by-one, typo, wrong argument, missing null check | Race condition, state corruption, multi-file logic error |

---

## Agent Coordination

### Code Explorers (Phase 2, deep track)

Use the `task` tool with `command: "code-explorer"`:
```
task({
  command: "code-explorer",
  prompt: "...",
  description: "Explore [focus area] for bug investigation"
})
```

These are Sonnet-model read-only agents that explore codebase areas. Give each a distinct focus area related to the bug. They report structured findings.

### Bug Investigators (Phase 3, deep track)

Use the `task` tool with `command: "bug-investigator"`:
```
task({
  command: "bug-investigator",
  prompt: "...",
  description: "Test hypothesis: [hypothesis title]"
})
```

These are Sonnet-model agents with bash access for running tests and git commands, but no write/edit — they investigate and report evidence, they don't fix code. Give each a specific hypothesis to test.

### Error Handling

- If an agent fails, continue with remaining agents' results
- If all agents fail in a phase, fall back to manual investigation
- Never block on a single agent — partial results are better than no results

---

## Error Recovery

If any phase fails:
1. Explain what went wrong and what you've learned so far
2. Present the hypothesis journal as-is
3. Ask the user how to proceed via the `question` tool:
   - "Retry this phase"
   - "Skip to fix" (if you have enough evidence)
   - "Provide more context"
   - "Abort"

---

## Python Debugging Reference

Language-specific debugging techniques, common pitfalls, and diagnostic tools for Python codebases.

### pytest Debugging Flags

| Flag | Purpose | When to Use |
|------|---------|-------------|
| `-x` | Stop on first failure | Isolating the first broken test |
| `--tb=long` | Full traceback | Need complete call stack |
| `--tb=short` | Abbreviated traceback | Quick scan of failures |
| `--pdb` | Drop into debugger on failure | Interactive investigation |
| `--lf` | Re-run only last failed tests | Iterating on a fix |
| `-s` | Disable output capture | See print/logging output |
| `-k "pattern"` | Run tests matching pattern | Focus on specific tests |
| `-v` | Verbose output | See individual test names |
| `--no-header` | Suppress header | Cleaner output for parsing |
| `--tb=no` | No traceback | Quick pass/fail check |

#### Combining Flags

```bash
# Reproduce and investigate: stop at first failure, full trace, show output
pytest -x --tb=long -s path/to/test_file.py

# Re-run failures with debugger
pytest --lf --pdb

# Run specific test with verbose output
pytest -xvs -k "test_specific_function" path/to/test_file.py
```

### Traceback Analysis

#### Reading Python Tracebacks

Python tracebacks read **bottom-to-top** — the actual error is at the bottom, the call chain above.

```
Traceback (most recent call last):          ← oldest frame
  File "app/main.py", line 42, in handle    ← your code (relevant)
    result = service.process(data)
  File "app/service.py", line 18, in process  ← your code (relevant)
    return transformer.apply(data)
  File "venv/lib/.../transformer.py", line 7  ← library code (context)
    raise ValueError("invalid input")
ValueError: invalid input                    ← actual error (start here)
```

#### Frame Identification

| Frame Pattern | Type | Action |
|---------------|------|--------|
| Your project paths (`app/`, `src/`, `lib/`) | Your code | Primary investigation target |
| `venv/`, `site-packages/` | Library code | Check what you passed in |
| `<frozen importlib>`, `<string>` | Python internals | Usually skip |

#### Key Questions at Each Frame

1. What arguments were passed to this function?
2. What state was the object in at this point?
3. Is the data type what the function expects?

### Common Exception Types

| Exception | Typical Cause | Investigation Strategy |
|-----------|---------------|------------------------|
| `AttributeError` | Wrong type, None where object expected, typo | Check the object's actual type with `type()`, trace where it was assigned |
| `KeyError` | Missing dict key, wrong key name | Print available keys, check data source |
| `TypeError` | Wrong argument types, wrong number of args | Compare function signature with call site |
| `ImportError` / `ModuleNotFoundError` | Missing package, circular import, wrong path | Check `sys.path`, verify package installed, check for circular deps |
| `ValueError` | Correct type but invalid value | Check input data, trace where value originates |
| `IndexError` | List/tuple index out of range | Check collection length, off-by-one |
| `FileNotFoundError` | Wrong path, missing file | Print `os.getcwd()`, check relative vs absolute |
| `PermissionError` | File/directory permissions | Check file ownership and mode |
| `RecursionError` | Infinite recursion | Check base case, print recursion depth |
| `StopIteration` | Exhausted iterator, bare `next()` | Use `next(iter, default)` or check before consuming |
| `UnicodeDecodeError` | Wrong encoding assumption | Check file encoding, use `errors='replace'` to diagnose |

### Python Gotchas

#### Mutable Default Arguments

```python
# BUG: shared list across all calls
def append_to(item, target=[]):
    target.append(item)
    return target

# FIX: use None sentinel
def append_to(item, target=None):
    if target is None:
        target = []
    target.append(item)
    return target
```

#### Late Binding Closures

```python
# BUG: all functions return 4 (last value of i)
functions = [lambda: i for i in range(5)]

# FIX: capture with default argument
functions = [lambda i=i: i for i in range(5)]
```

#### Circular Imports

Symptoms: `ImportError`, `AttributeError` on module attribute, partially initialized module.

Investigation:
1. Check import order — which module loads first?
2. Move imports inside functions (lazy import) as a quick fix
3. Restructure to break the cycle for a proper fix

#### None Comparisons

```python
# BUG: can fail with objects that override __eq__
if value == None:

# FIX: use identity check
if value is None:
```

#### Integer Division

```python
# Python 3: this is float division
result = 7 / 2   # 3.5

# Integer division requires //
result = 7 // 2  # 3
```

#### String Immutability and Identity

```python
# BUG: 'is' checks identity, not equality
if name is "admin":  # unreliable

# FIX: use == for value comparison
if name == "admin":
```

### Diagnostic Logging

#### Targeted Debug Logging

```python
import logging

logger = logging.getLogger(__name__)

# Temporary diagnostic (remove after fixing)
logger.debug("process_order called: order_id=%s, items=%d, total=%s",
             order.id, len(order.items), order.total)
```

#### Quick Diagnostic Print

For rapid investigation (remove before committing):

```python
# Print with context
print(f"DEBUG [{__name__}:{line}] variable={variable!r} type={type(variable)}")

# Print collection contents
print(f"DEBUG keys={list(data.keys())}")
print(f"DEBUG len={len(items)}, first={items[0] if items else 'EMPTY'}")
```

#### Logging Configuration for Debugging

```python
# Enable debug logging for specific module
logging.getLogger("app.service").setLevel(logging.DEBUG)

# See all SQL queries (SQLAlchemy)
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
```

### Performance Investigation

#### cProfile Quick Start

```bash
# Profile a script
python -m cProfile -s cumulative script.py

# Profile a specific function in tests
python -m cProfile -s tottime -m pytest -x test_slow.py
```

#### Targeted Profiling

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()
# ... code to profile ...
profiler.disable()

stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)  # top 20 functions
```

### Git Bisect with pytest

```bash
# Start bisect
git bisect start

# Mark current (broken) as bad
git bisect bad

# Mark known good commit
git bisect good <commit-hash>

# Automate with pytest
git bisect run pytest -x path/to/failing_test.py

# When done
git bisect reset
```

### Environment Investigation

```bash
# Check Python version
python --version

# Check installed package version
pip show <package-name>

# List all installed packages
pip list

# Check for conflicting dependencies
pip check

# Verify virtual environment is active
which python
echo $VIRTUAL_ENV
```

---

## TypeScript/JavaScript Debugging Reference

Language-specific debugging techniques, common pitfalls, and diagnostic tools for TypeScript and JavaScript codebases.

### Test Runner Debugging Flags

#### Jest

| Flag | Purpose | When to Use |
|------|---------|-------------|
| `--verbose` | Show individual test results | See which specific tests pass/fail |
| `--bail` | Stop on first failure | Isolating the first broken test |
| `--detectOpenHandles` | Detect open async handles | Tests hang or don't exit |
| `--runInBand` | Run serially (no workers) | Debugging race conditions between tests |
| `--testPathPattern="pattern"` | Run matching test files | Focus on specific test file |
| `-t "pattern"` | Run matching test names | Focus on specific test case |
| `--no-cache` | Disable transform cache | Stale cache causing issues |
| `--forceExit` | Force exit after tests | Tests hang due to open handles |
| `--testTimeout=10000` | Set timeout (ms) | Async tests timing out |

#### Vitest

| Flag | Purpose | When to Use |
|------|---------|-------------|
| `--reporter=verbose` | Detailed output | See individual test results |
| `--bail 1` | Stop on first failure | Isolating failures |
| `--run` | Run once (no watch) | CI or single-run debugging |
| `--testNamePattern="pattern"` | Run matching tests | Focus on specific test |
| `--no-threads` | Disable worker threads | Debugging thread-related issues |
| `--inspect` | Enable Node inspector | Interactive debugging |

#### Combining Flags

```bash
# Reproduce and investigate: stop at first failure, verbose, serial
npx jest --bail --verbose --runInBand path/to/test.spec.ts

# Re-run with open handle detection
npx jest --bail --detectOpenHandles --forceExit

# Vitest single test with inspection
npx vitest run --bail 1 --reporter=verbose path/to/test.spec.ts
```

### Async/Await Pitfalls

#### Missing await

```typescript
// BUG: test passes even when assertion should fail — promise not awaited
it('fetches data', () => {
  const result = fetchData();  // missing await
  expect(result).toBeDefined(); // tests the Promise object, not the result
});

// FIX: await the async operation
it('fetches data', async () => {
  const result = await fetchData();
  expect(result).toBeDefined();
});
```

#### Unhandled Promise Rejections

```typescript
// BUG: error swallowed silently
async function process() {
  riskyOperation(); // missing await — rejection goes unhandled
}

// FIX: await and handle
async function process() {
  await riskyOperation(); // now rejection propagates properly
}
```

#### Promise.all Error Handling

```typescript
// BUG: first rejection cancels everything, others may leak
try {
  await Promise.all([taskA(), taskB(), taskC()]);
} catch (e) {
  // only catches the first rejection
}

// FIX: use Promise.allSettled when you need all results
const results = await Promise.allSettled([taskA(), taskB(), taskC()]);
const failures = results.filter(r => r.status === 'rejected');
```

#### Timer-Based Tests

```typescript
// BUG: real timers make tests slow and flaky
it('debounces input', async () => {
  await new Promise(r => setTimeout(r, 500)); // real delay
});

// FIX: use fake timers
it('debounces input', () => {
  jest.useFakeTimers();
  triggerInput();
  jest.advanceTimersByTime(500);
  expect(handler).toHaveBeenCalled();
  jest.useRealTimers();
});
```

### Common TypeScript/JavaScript Gotchas

#### `this` Binding

```typescript
// BUG: 'this' is undefined in callback
class Handler {
  name = "handler";
  handle() {
    console.log(this.name); // undefined when called as callback
  }
}
const h = new Handler();
button.onClick(h.handle); // 'this' is lost

// FIX: arrow function or bind
class Handler {
  name = "handler";
  handle = () => {  // arrow preserves 'this'
    console.log(this.name);
  }
}
```

#### Closure/Scope in Loops

```typescript
// BUG: all callbacks reference the same variable
for (var i = 0; i < 5; i++) {
  setTimeout(() => console.log(i), 100); // prints 5,5,5,5,5
}

// FIX: use let (block-scoped)
for (let i = 0; i < 5; i++) {
  setTimeout(() => console.log(i), 100); // prints 0,1,2,3,4
}
```

#### Type Narrowing Gotchas

```typescript
// BUG: typeof null === 'object'
function process(value: string | object | null) {
  if (typeof value === 'object') {
    value.toString(); // crashes if null
  }
}

// FIX: check null explicitly first
function process(value: string | object | null) {
  if (value === null) return;
  if (typeof value === 'object') {
    value.toString(); // safe
  }
}
```

#### Equality Comparisons

```typescript
// BUG: type coercion surprises
0 == ""     // true
0 == false  // true
"" == false // true
null == undefined // true

// FIX: always use strict equality
0 === ""     // false
0 === false  // false
```

#### Array/Object Reference vs Value

```typescript
// BUG: arrays/objects compared by reference
[1, 2] === [1, 2]  // false
{ a: 1 } === { a: 1 }  // false

// FIX: deep comparison
JSON.stringify(a) === JSON.stringify(b)  // quick but order-sensitive
// or use lodash.isEqual, util.isDeepStrictEqual
```

#### Optional Chaining and Nullish Coalescing

```typescript
// BUG: || treats 0 and "" as falsy
const port = config.port || 3000;  // 0 becomes 3000

// FIX: use ?? for null/undefined only
const port = config.port ?? 3000;  // 0 stays 0
```

### Stack Trace Analysis

#### Node.js Stack Traces

```
Error: Connection refused
    at TCPConnectWrap.afterConnect [as oncomplete] (net.js:1141)  ← Node internal
    at Connection.connect (node_modules/pg/lib/connection.js:38)   ← library
    at Pool._connect (node_modules/pg/lib/pool.js:89)              ← library
    at db.query (src/database.ts:45)                                ← your code
    at UserService.findById (src/services/user.ts:22)              ← your code
    at GET /api/users/:id (src/routes/users.ts:15)                 ← entry point
```

Read top-to-bottom (opposite of Python). Your code is typically in the middle frames.

#### Async Stack Traces

Node.js may lose async context in stack traces. Enable `--async-stack-traces` or use `--enable-source-maps` for TypeScript.

```bash
# Better async traces
node --async-stack-traces dist/app.js

# TypeScript source maps in traces
node --enable-source-maps dist/app.js
```

### Console Debugging Patterns

#### Structured Output

```typescript
// Object inspection
console.dir(complexObject, { depth: null, colors: true });

// Table format for arrays of objects
console.table(users.map(u => ({ id: u.id, name: u.name, role: u.role })));

// Call stack at this point
console.trace("reached here");

// Group related logs
console.group("Processing order #123");
console.log("Items:", order.items.length);
console.log("Total:", order.total);
console.groupEnd();
```

#### Conditional Debugging

```typescript
// Only log when condition is true
console.assert(items.length > 0, "Items array is empty!", { items });

// Count how many times a code path is hit
console.count("cache-miss");
console.count("cache-hit");
```

### Node.js Inspector

#### Starting the Inspector

```bash
# Inspect a script
node --inspect-brk dist/app.js

# Inspect tests (Jest)
node --inspect-brk node_modules/.bin/jest --runInBand

# Inspect tests (Vitest)
npx vitest --inspect --no-threads
```

Open `chrome://inspect` in Chrome to connect to the debugger.

### Common Error Patterns

| Error | Typical Cause | Investigation Strategy |
|-------|---------------|------------------------|
| `TypeError: Cannot read properties of undefined` | Accessing property on undefined value | Trace back to where the variable was assigned, check for missing data |
| `TypeError: X is not a function` | Wrong type, missing import, wrong module export | Check imports, verify the export exists |
| `ReferenceError: X is not defined` | Typo, missing import, scope issue | Check spelling, verify import path |
| `SyntaxError: Unexpected token` | Malformed JSON, wrong file extension, missing transpilation | Check the file content at the indicated position |
| `ERR_MODULE_NOT_FOUND` | Wrong import path, missing package | Verify path, check `node_modules` |
| `ECONNREFUSED` | Service not running, wrong port | Check if the target service is up |
| `EADDRINUSE` | Port already in use | `lsof -i :PORT` to find the process |
| `MaxListenersExceededWarning` | Event listener leak | Track where listeners are added without removal |
| `JavaScript heap out of memory` | Memory leak, large data processing | Profile with `--max-old-space-size`, check for retained references |
| `ETIMEOUT` / `ESOCKETTIMEDOUT` | Network timeout, slow service | Check network, increase timeout, add retry |

### TypeScript-Specific Investigation

```bash
# Check what TypeScript compiles to
npx tsc --noEmit --pretty  # type check without emitting

# See generated JavaScript for a file
npx tsc --outDir /tmp/debug --sourceMap path/to/file.ts

# Check TypeScript version
npx tsc --version

# Verify tsconfig resolution
npx tsc --showConfig
```

---

## General Debugging Reference

Language-agnostic debugging strategies, systematic investigation methods, and common bug categories.

### Systematic Debugging Methods

#### Binary Search for Bugs

Narrow the problem space by half at each step:

1. Identify the full code path from input to incorrect output
2. Place a diagnostic check at the midpoint
3. Determine which half contains the bug
4. Repeat in the failing half until the exact location is found

Works for: data transformation pipelines, middleware chains, multi-step processes.

#### Git Bisect

Automate binary search through commit history:

```bash
git bisect start
git bisect bad                    # current commit is broken
git bisect good <known-good-sha> # this commit was working

# Automated: let a test command drive the search
git bisect run <test-command>     # returns 0 = good, non-0 = bad

git bisect reset                  # when done
```

Best for: regressions where you know "it used to work."

#### Delta Debugging

Minimize the input that triggers the bug:

1. Start with the full failing input
2. Remove half the input — does it still fail?
3. If yes, keep the smaller input and repeat
4. If no, restore and try removing the other half
5. Continue until you find the minimal failing case

Works for: large inputs, complex configurations, test case reduction.

#### Rubber Duck Debugging

Explain the problem out loud (or in writing), step by step:

1. State what the code is supposed to do
2. Walk through the actual execution, line by line
3. At each step, explain what the state should be vs. what it is
4. The discrepancy often reveals itself during the explanation

#### 5 Whys

Drill past symptoms to root causes:

```
Bug: Users see a 500 error on checkout
Why? → The payment API call throws a timeout
Why? → The request takes >30 seconds
Why? → The order total calculation is O(n²)
Why? → It recalculates item prices for each item pair
Why? → The discount logic compares every item against every other item
Root cause: Quadratic discount calculation algorithm
```

Stop when the answer is something you can directly fix.

### Reading Stack Traces

#### Universal Patterns

| Element | What It Tells You |
|---------|-------------------|
| Error type/name | Category of failure (null access, type mismatch, etc.) |
| Error message | Specific details about what went wrong |
| File path + line number | Where the error was thrown |
| Function/method name | What was executing when it failed |
| Frame ordering | The call chain that led to the error |

#### What Stack Traces CAN'T Tell You

- **Why** the wrong value got there (you need to trace backwards)
- **When** the state became corrupted (may have happened much earlier)
- **Where** in async code the real problem is (async gaps in traces)
- **Whether** a caught-and-rethrown error lost its original context

#### Investigation Strategy

1. Read the **error message** first — it often contains the key clue
2. Find **your code** in the trace (skip framework/library frames)
3. Read the **immediate caller** — what arguments were passed?
4. Check the **state** at that point — are variables what you expect?
5. Trace **backwards** from the error to where the data originated

### Bug Categories

#### Off-by-One Errors

**Symptoms:** Missing first/last element, array index out of bounds, fencepost errors.

**Check for:**
- `<` vs `<=` in loop conditions
- 0-based vs 1-based indexing confusion
- Inclusive vs exclusive range boundaries
- Empty collection edge case (length 0)

#### Null/Undefined/None Errors

**Symptoms:** Null reference exceptions, "undefined is not a function," AttributeError.

**Check for:**
- Uninitialized variables
- Missing return values (functions that implicitly return null/undefined)
- Optional fields accessed without guards
- API responses with unexpected null fields
- Database queries returning no results

#### Race Conditions

**Symptoms:** Intermittent failures, works in debugger but fails normally, order-dependent results.

**Check for:**
- Shared mutable state accessed concurrently
- Missing locks/synchronization
- Read-then-write without atomicity
- Callback ordering assumptions
- File system operations assuming sequential access

#### Resource Leaks

**Symptoms:** Slow degradation, eventual crashes, "too many open files," memory growth.

**Check for:**
- File handles not closed (missing `close()` / `with` / `using`)
- Database connections not returned to pool
- Event listeners added but never removed
- Timers/intervals not cleared
- Temporary files not cleaned up

#### State Corruption

**Symptoms:** Inconsistent data, works sometimes but not always, cascade of errors after a specific action.

**Check for:**
- Mutation of shared objects
- Missing deep copies (aliased references)
- Partial updates (crash between related writes)
- Cache invalidation issues
- Global/singleton state modified by multiple code paths

### Diagnostic Logging Strategy

#### Targeted Logging

Log at decision points and data boundaries:

```
[ENTRY] function_name called with: key_arg=value
[BRANCH] taking path X because condition=value
[DATA] received from external: summary_of_data
[EXIT] function_name returning: summary_of_result
```

#### Logging Anti-Patterns

| Anti-Pattern | Problem | Better Approach |
|-------------|---------|-----------------|
| Logging everything | Noise hides signal | Log at boundaries and decision points |
| Logging sensitive data | Security risk | Redact or hash sensitive fields |
| Logging inside tight loops | Performance impact, massive output | Log summary after loop, or sample every Nth iteration |
| Logging without context | "Error occurred" is useless | Include function name, key parameters, state |
| Leaving debug logs in code | Clutters production output | Use conditional debug level, remove before commit |

#### Effective Diagnostic Pattern

1. **Before the suspected area:** Log inputs and state
2. **At decision points:** Log which branch was taken and why
3. **After the suspected area:** Log outputs and state
4. **Compare:** Are the inputs/outputs what you expect at each point?

### Investigation Checklist

Before proposing a fix, verify you can answer:

#### Understanding the Bug
- [ ] Can you reproduce the bug reliably?
- [ ] What is the expected behavior vs actual behavior?
- [ ] When did this start happening? (regression or latent bug?)
- [ ] Does it happen always, sometimes, or in specific conditions?

#### Root Cause Identification
- [ ] Have you identified the specific line(s) causing the issue?
- [ ] Do you understand WHY those lines produce the wrong result?
- [ ] Is this the root cause, or a symptom of a deeper issue?
- [ ] Could this same root cause affect other code paths?

#### Fix Validation
- [ ] Does the fix address the root cause, not just the symptom?
- [ ] Could the fix introduce new bugs? (side effects, changed behavior)
- [ ] Are there existing tests that should have caught this?
- [ ] Does the fix handle all edge cases for this code path?

#### Broader Impact
- [ ] Are there similar patterns elsewhere that might have the same bug?
- [ ] Does the fix require updates to documentation or configuration?
- [ ] Could this be a regression? If so, what change introduced it?
- [ ] Is a new test needed to prevent this from recurring?
