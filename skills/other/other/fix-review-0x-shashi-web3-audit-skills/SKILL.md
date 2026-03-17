---
id: fix-review
title: Fix Review Skill
category: methodology
difficulty: intermediate
triggers:
  - fix review
  - verify fix
  - patch review
  - fix verification
  - regression check
  - re-audit
related_skills:
  - variant-analysis/SKILL.md
  - differential-review/SKILL.md
  - severity/SKILL.md
  - methodology/SKILL.md
tags:
  - fix-review
  - verification
  - regression
  - methodology
last_updated: 2026-02-26
description: >-
  Verify that bug fixes correctly address reported vulnerabilities without
  introducing new issues. Use when reviewing protocol team fix submissions,
  during re-audit engagements, or in contest mitigation review phases on
  Sherlock and Code4rena.
---

# Fix Review Skill

## Purpose

Verify that bug fixes correctly address reported vulnerabilities without introducing new issues. A fix review is not a rubber stamp — it requires the same rigor as the original audit, focused on the change boundary and its ripple effects.

## When to Trigger

- After a protocol team submits fixes for audit findings
- During re-audit engagement for upgraded contracts
- When reviewing a PR that addresses a security issue
- Contest mitigation review phase (Sherlock, Code4rena)
- Any code change to a previously-audited contract

## Fix Review Framework

### Phase 1: Understand the Finding

Before reviewing the fix, re-read the original finding completely:

```markdown
## Pre-Review Checklist
- [ ] Finding ID and severity confirmed
- [ ] Root cause fully understood (not just the symptom)
- [ ] Impact clearly documented
- [ ] Original PoC reviewed (if available)
- [ ] All variant instances listed
```

### Phase 2: Analyze the Fix

Apply the **5-Point Fix Validation**:

#### 1. Root Cause Resolution

```
Q: Does the fix address the ROOT CAUSE, or just the symptom?

GOOD FIX (root cause):
  Finding: CEI violation in withdraw()
  Fix: Added ReentrancyGuard + nonReentrant modifier
  → Prevents ALL reentrancy, not just the specific path

BAD FIX (symptom only):
  Finding: CEI violation in withdraw()
  Fix: Moved one state update before one external call
  → May still be vulnerable via a different code path
```

#### 2. Completeness Check

```
Q: Does the fix cover ALL instances of the vulnerability?

GOOD: Applied nonReentrant to withdraw(), claim(), AND liquidate()
BAD:  Applied nonReentrant to withdraw() only (ignored variants)
```

Check against the variant analysis from the original finding.

#### 3. No New Vulnerabilities Introduced

Common patterns where fixes introduce new bugs:

| Original Fix | New Vulnerability Introduced |
|---|---|
| Added `require(amount > 0)` | Now users cannot withdraw dust amounts, funds permanently locked |
| Changed `transfer` to `safeTransfer` | ERC777 `tokensReceived` hook now enables reentrancy |
| Added `nonReentrant` modifier | Cross-contract reentrancy still possible if guard is per-contract |
| Added access control to function | Legitimate users now blocked from valid operations |
| Changed rounding direction | Opposite rounding error now created for different user type |
| Added deadline check | Deadline is in wrong units (milliseconds vs seconds) |
| Moved state update before call | Read-only reentrancy still returns stale state in view functions |

#### 4. No Regressions

```
Q: Does the fix break any existing legitimate functionality?

Check:
- [ ] All existing tests still pass
- [ ] New tests added specifically for the vulnerability
- [ ] Edge cases still handled correctly (0 amount, max amount, empty array)
- [ ] Gas impact is acceptable (new modifier doesn't make function too expensive)
- [ ] Compatibility with existing integrations preserved
```

#### 5. Minimality

```
Q: Does the fix change only what is necessary?

RED FLAGS:
- Large refactoring alongside the fix (hides changes)
- Unrelated changes bundled in the same PR
- Storage layout changes in upgradeable contracts
- New dependencies added (expanded attack surface)
- Function signatures changed (breaks composability)
```

### Phase 3: Test the Fix

#### Manual Verification

```solidity
// BEFORE (vulnerable):
function withdraw(uint256 amount) external {
    require(balances[msg.sender] >= amount, "Insufficient");
    token.safeTransfer(msg.sender, amount); // external call first
    balances[msg.sender] -= amount;          // state update second
}

// AFTER (fixed):
function withdraw(uint256 amount) external nonReentrant {
    require(balances[msg.sender] >= amount, "Insufficient");
    balances[msg.sender] -= amount;          // state update first
    token.safeTransfer(msg.sender, amount);  // external call second
}

// VERIFICATION:
// ✅ nonReentrant modifier added — prevents re-entry
// ✅ CEI pattern applied — state before interaction
// ✅ Both mitigations applied — defense in depth
// ⚠️ Check: Are claim() and liquidate() also fixed?
```

#### Reproduce Original PoC Against Fix

```solidity
// If original PoC was provided, run it against the fixed code
// Expected: PoC should FAIL (revert) after the fix

function test_reentrancy_fix() public {
    // Setup attacker contract with reentrancy callback
    AttackContract attacker = new AttackContract(vault);
    vault.deposit{value: 10 ether}();
    
    // Try the original attack
    vm.expectRevert(); // Should revert now
    attacker.attack();
    
    // Verify vault funds are intact
    assertEq(address(vault).balance, 10 ether);
}
```

#### Write Regression Tests

```solidity
// Test that legitimate functionality still works
function test_withdraw_still_works() public {
    vault.deposit{value: 5 ether}();
    vault.withdraw(3 ether);
    assertEq(vault.balances(address(this)), 2 ether);
}

// Test edge cases
function test_withdraw_zero() public {
    // Should this revert or succeed? Check spec.
    vault.deposit{value: 5 ether}();
    vault.withdraw(0);
}

function test_withdraw_full_balance() public {
    vault.deposit{value: 5 ether}();
    vault.withdraw(5 ether);
    assertEq(vault.balances(address(this)), 0);
}
```

### Phase 4: Severity Re-Assessment

After reviewing the fix, update the finding status:

| Status | Meaning |
|---|---|
| **Fixed** | Root cause fully addressed, all instances covered, no regressions |
| **Partially Fixed** | Some instances fixed, others remain; or fix is incomplete |
| **Not Fixed** | Fix does not address the root cause at all |
| **Acknowledged** | Team accepts the risk, chose not to fix (document reasoning) |
| **Disputed** | Team disagrees with finding validity (document both positions) |
| **New Issue** | Fix introduces a new, different vulnerability |

### Phase 5: Report Fix Review Results

**Template for each finding:**

```markdown
## Finding [ID]: [Title]

**Original Severity**: High
**Fix Status**: Fixed / Partially Fixed / Not Fixed / Acknowledged / Disputed

### Fix Summary
[One-sentence description of what the fix does]

### Fix Analysis
- Root cause addressed: Yes/No
- All instances covered: Yes/No (list missing instances if partial)
- New vulnerabilities: None found / [describe new issue]
- Regressions: None found / [describe regression]
- Tests added: Yes/No

### Verification
[How the fix was verified — PoC test results, code review notes]

### Recommendation (if partially/not fixed)
[What additional changes are needed]
```

## Common Fix Patterns and Their Risks

### Reentrancy Fixes

| Fix Pattern | Risk Level | Notes |
|---|---|---|
| Add `nonReentrant` modifier | Low risk | Best approach — prevents all reentrancy in that function |
| Reorder to CEI | Low risk | Good but may miss cross-function reentrancy |
| Both CEI + nonReentrant | Lowest risk | Defense in depth — recommended |
| Add mutex lock | Medium risk | Custom implementation may have bugs |
| Use `transfer()` (2300 gas) | High risk | Breaks with EIP-1884 and future gas changes |

### Access Control Fixes

| Fix Pattern | Risk Level | Notes |
|---|---|---|
| Add `onlyOwner` modifier | Low risk | Standard, but check if owner is multisig |
| Add role-based access | Low risk | Use OpenZeppelin AccessControl |
| Add `initializer` modifier | Low risk | Also call `_disableInitializers()` in constructor |
| Add `require(msg.sender == x)` | Medium risk | Inline checks are error-prone vs modifiers |

### Oracle Fixes

| Fix Pattern | Risk Level | Notes |
|---|---|---|
| Switch to Chainlink TWAP | Low risk | Ensure heartbeat and staleness checks added |
| Add staleness check | Low risk | Use `updatedAt` from `latestRoundData()` |
| Add deviation threshold | Medium risk | Must be tuned per asset — too tight = DoS, too loose = manipulation |
| Switch from spot to TWAP | Low risk | Verify TWAP window is sufficient (30 min minimum) |

### Arithmetic Fixes

| Fix Pattern | Risk Level | Notes |
|---|---|---|
| Use `mulDivUp`/`mulDivDown` | Low risk | Explicit rounding direction |
| Add dead shares / virtual offset | Low risk | For ERC4626 first depositor — check amount is sufficient |
| Add minimum deposit | Medium risk | May block legitimate small deposits |
| Switch to `SafeCast` | Low risk | Reverts on overflow instead of silent truncation |

## Upgrade-Specific Fix Review

When the fix is deployed via proxy upgrade:

```markdown
## Upgrade Safety Checklist
- [ ] Storage layout is backward-compatible (no variable reordering)
- [ ] New state variables added ONLY at the end
- [ ] No removed state variables (use `__gap` slots)
- [ ] Initializer version incremented (reinitializer(2), etc.)
- [ ] Old storage slots not reinterpreted as different types
- [ ] Immutable variables consistent between old and new impl
- [ ] Constructor calls `_disableInitializers()`
```

## Integration Points

| Skill | How It's Used |
|---|---|
| `variant-analysis/` | Check if fix covers all variant instances |
| `differential-review/` | Compare old vs new code systematically |
| `severity/` | Re-assess severity after fix |
| `methodology/` | Apply standard verification methodology |
| `checklists/` | Use protocol-specific checklist for regression |
