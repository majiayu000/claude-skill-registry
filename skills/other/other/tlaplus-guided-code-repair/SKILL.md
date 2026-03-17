---
name: tlaplus-guided-code-repair
description: "Automatically repair C/C++ code violations detected by TLA+ model checking. Takes a program, TLA+ specification, and TLC counterexample trace as input, then generates minimal code modifications to eliminate the violation. Use when: (1) TLC model checker reports an invariant violation, deadlock, or temporal property failure, (2) You have a counterexample trace and need to fix the corresponding code, (3) You need to understand how a TLA+ violation maps to program-level bugs, (4) You want to validate repairs by re-running TLC. Supports safety properties (invariants), liveness properties (temporal logic), and deadlock detection."
---

# TLA+ Guided Code Repair

Automatically repair C/C++ code based on TLA+ model checking violations. This skill analyzes TLC counterexamples, identifies root causes in the implementation, and generates semantically justified repairs.

## Repair Workflow

Follow this sequential process when given a TLA+ violation:

### 1. Parse the Counterexample

Use `scripts/parse_tlc_trace.py` to extract structured information from TLC output:

```bash
python scripts/parse_tlc_trace.py trace.txt
# Or for JSON output:
python scripts/parse_tlc_trace.py --json trace.txt
```

This extracts:
- Violation type (invariant, deadlock, temporal)
- Violated property name
- State trace with variable values at each step

### 2. Analyze the Violation

**Read the reference guides** to understand the violation:
- `references/repair_patterns.md` - Common violations and repair strategies
- `references/tlaplus_to_cpp_mapping.md` - How to map TLA+ to C/C++ code

**Key analysis steps:**
1. Identify which invariant/property was violated
2. Examine the state trace to find where the violation occurred
3. Determine which TLA+ action led to the violation
4. Map the TLA+ action to the corresponding C/C++ function

**Example analysis:**
```
Violation: Invariant BalanceNonNegative violated
Final state: balance = -50
Action: Withdraw (line 45 in spec)
Cause: withdraw() function allows amount > balance
```

### 3. Identify the Root Cause

Trace backwards from the violation to find the program-level bug:

**Common root causes:**
- Missing precondition checks (guards)
- Race conditions (missing synchronization)
- Incorrect lock ordering (deadlocks)
- Uninitialized variables
- Missing notifications (liveness violations)

**Mapping strategy:**
- TLA+ guards → C++ precondition checks
- TLA+ atomic actions → C++ critical sections
- TLA+ state variables → C++ member variables/globals
- TLA+ action sequences → C++ function call chains

### 4. Generate the Repair

Create a minimal, semantically justified code modification:

**Repair principles:**
- **Minimal**: Change only what's necessary to fix the violation
- **Justified**: Every change should enforce a specific TLA+ property
- **Preserving**: Don't break existing functionality

**Common repair patterns:**

**Pattern A: Add precondition check**
```cpp
// Before
void withdraw(int amount) {
    balance -= amount;  // Can violate balance >= 0
}

// After - enforces invariant: balance >= 0
bool withdraw(int amount) {
    if (amount > balance) return false;  // Guard from TLA+ spec
    balance -= amount;
    return true;
}
```

**Pattern B: Add synchronization**
```cpp
// Before - race condition
void increment() {
    counter++;
}

// After - enforces atomic action from TLA+ spec
void increment() {
    std::lock_guard<std::mutex> lock(mtx);
    counter++;
}
```

**Pattern C: Fix lock ordering**
```cpp
// Before - potential deadlock
void transfer(Account& from, Account& to, int amount) {
    std::lock_guard<std::mutex> lock1(from.mtx);
    std::lock_guard<std::mutex> lock2(to.mtx);
    // ...
}

// After - consistent ordering prevents deadlock
void transfer(Account& from, Account& to, int amount) {
    Account* first = &from < &to ? &from : &to;
    Account* second = &from < &to ? &to : &from;
    std::lock_guard<std::mutex> lock1(first->mtx);
    std::lock_guard<std::mutex> lock2(second->mtx);
    // ...
}
```

### 5. Validate the Repair

**Re-run TLC model checker** to verify the violation is fixed:

```bash
python scripts/run_tlc.py spec.tla --config spec.cfg
```

**Run existing tests** to ensure no regressions:
```bash
# Run your test suite
make test
# or
./run_tests.sh
```

**Validation checklist:**
- [ ] TLC passes without violations
- [ ] All existing tests still pass
- [ ] The repair addresses the root cause (not just symptoms)
- [ ] No new violations introduced

### 6. Explain the Repair

Provide a clear explanation of:
1. **What was violated**: Which TLA+ property failed
2. **Why it failed**: The root cause in the C++ code
3. **How the repair fixes it**: What the code change enforces
4. **Validation results**: TLC output and test results

**Example explanation:**
```
Violation: Invariant BalanceNonNegative (balance >= 0) was violated.

Root Cause: The withdraw() function at line 45 in account.cpp did not check
if the withdrawal amount exceeds the current balance, allowing negative balances.

Repair: Added precondition check `if (amount > balance) return false;` before
the balance update. This enforces the TLA+ guard condition from the Withdraw
action in the specification.

Validation: TLC model checking now passes with no violations. All 15 existing
unit tests pass. The repair is minimal and preserves existing functionality.
```

## Quick Reference

**When you receive:**
- TLC trace output → Use `parse_tlc_trace.py` to extract violation info
- Invariant violation → Check `repair_patterns.md` section 1
- Deadlock → Check `repair_patterns.md` section 2
- Temporal property violation → Check `repair_patterns.md` section 3
- Need to map TLA+ to C++ → Read `tlaplus_to_cpp_mapping.md`

**Output format:**
1. Repaired C++ code (with comments explaining changes)
2. Validation results (TLC output, test results)
3. Explanation (violation → cause → repair → justification)
