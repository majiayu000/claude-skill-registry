---
name: bug-hunt
description: Proactive bug-hunting workflow. Assesses codebase risk through complexity, coverage, and structural analysis, then spawns focused investigators that write reproducing tests to validate suspected bugs. Thoroughness over speed. Advisory only — produces findings and proposes tickets; does not implement fixes.
model: opus
---

# Bug Hunt — Proactive Bug Discovery

Systematically hunts for bugs before they reach users. An assessor analyzes the codebase to identify high-risk hotspots by cross-referencing code complexity, test coverage gaps, and structural risk factors. Focused hunters then deep-dive into each hotspot, writing reproducing tests to validate or invalidate suspected bugs.

**This is deliberately thorough.** Each suspected bug gets a reproducing test — no speculative reports. The goal is confirmed findings with evidence, not a noisy list of maybes.

**Advisory only.** The skill produces findings and proposes tickets; it does not implement fixes. The cognitive seam between "find bug" and "fix bug" is wide enough that mixing them under one workflow degrades both — investigation pressure shouldn't bias the hunters toward bugs they could easily fix, and remediation requires fresh reasoning the hunters aren't currently in. Tickets capture findings durably across that seam and compose with `/implement` and `/implement-project` for remediation. The reproducing tests serve as acceptance criteria — the fix is done when the test passes.

## Workflow Overview

```
┌──────────────────────────────────────────────────────┐
│                  BUG HUNT WORKFLOW                   │
├──────────────────────────────────────────────────────┤
│  1. Determine scope                                  │
│  2. Spawn assessor (risk analysis)                   │
│     └─ Output: ranked hotspot list + coverage map    │
│  3. For each hotspot:                                │
│     └─ Spawn hunter (investigation + repro tests)    │
│     └─ Prior findings passed to subsequent hunters   │
│  4. Synthesize findings                              │
│  5. Present consolidated findings to user            │
│  6. Cut tickets + commit reproducing tests           │
│     (proposed structure; operator-approved)          │
│  7. (If tickets declined) commit reproducing tests   │
│     standalone for the coverage benefit              │
└──────────────────────────────────────────────────────┘
```

## Workflow Details

### 1. Determine Scope

**Default:** Production code only. Excluded by default:
- Test code (test files, test fixtures, test helpers)
- Dev-only dependencies and tooling
- Generated code, vendored code

Inform the user of these exclusions.

**Ask the user:**
- "What is the scope of the hunt?" (entire codebase, specific module, specific area of concern)
- "Are there areas you're particularly worried about?" (recent changes, complex features, etc.)
- "Anything to skip beyond the defaults?"

User concerns influence prioritization but don't replace systematic analysis.

### 2. Risk Assessment

**Spawn a `swe-bug-assessor` agent:**

```
You are the risk assessor for a proactive bug hunt. Your analysis will guide
focused investigators who will deep-dive into the hotspots you identify.

Scope: [entire codebase | user-specified scope]
User concerns: [any areas mentioned, or "none specified"]
Exclusions: [test code, vendored code, generated code, plus any user additions]

Perform your full methodology:
1. Map the codebase — language, framework, structure, entry points
2. Coverage analysis — use instrumented coverage if available, fall back to
   manual inspection
3. Complexity analysis — identify functions with high cognitive complexity
4. Structural risk analysis — error handling gaps, input validation gaps,
   shared mutable state, resource management issues, concurrency risks,
   edge case blindness, consistency gaps
5. Git enrichment (optional) — churn hotspots, recent large changes
6. Cross-reference signals and produce a ranked hotspot list

Focus on hotspots where MULTIPLE signals converge — complex AND untested AND
structurally risky. Single-signal hotspots are lower priority.

Output your full assessment in your standard format.
```

**When the assessor reports back:** Review the hotspot list. This drives the investigation phase.

### 3. Focused Investigation — Hunters

**For each hotspot in the assessor's list (ALL priorities), spawn a dedicated `swe-bug-hunter` agent:**

```
You are a focused bug hunter investigating a specific hotspot.

## YOUR HOTSPOT
Target: [from assessor's report]
Files: [from assessor's report]
Risk signals: [from assessor's report]
Hypothesis: [from assessor's report]
Investigation approach: [from assessor's report]

## PRIOR FINDINGS (if any)
[Findings from previous hunters — confirmed bugs, patterns observed]

## YOUR MISSION
Deep-dive into this hotspot. Systematically probe for bugs. For each
suspected issue, write a reproducing test that encodes the correct expected
behavior.

- If the test FAILS: bug confirmed. Keep the test. Document the finding.
- If the test PASSES: hypothesis invalidated. Evaluate whether the test
  improves coverage:
  - Covers a previously untested path → keep it
  - Redundant with existing tests → delete it

Every confirmed finding must have a reproducing test. No speculative reports.

Note any patterns that might apply to other hotspots.
```

**Run hunters sequentially, not in parallel.** Each hunter's findings and pattern observations are passed to the next. This enables cross-hotspot pattern detection — if hunter 2 finds that error handling is broken in module A, hunter 5 (investigating module B which shares error-handling utilities) gets that context.

**Pass prior findings to each new hunter.** As findings accumulate, each subsequent hunter receives confirmed bugs and observed patterns from previous investigations.

### 4. Synthesize Findings

After all hunters have reported, synthesize:

**Cross-cutting analysis:**
- Do confirmed bugs share a common root cause or pattern?
- Are there systemic issues (e.g., a utility function used across 10 modules is buggy, but only one module was a hotspot)?
- Do coverage improvements from invalidated hypotheses reveal areas worth further investigation?

**Pattern escalation:**
- If multiple hunters report the same pattern (e.g., "error handling is inconsistent"), note this as a systemic issue even if individual instances are low severity
- Systemic patterns may warrant additional investigation or a follow-up `/refactor`

### 5. Present Consolidated Findings

Compile all findings into a single report:

```
## Bug Hunt Summary

Scope: [what was analyzed]
Assessment: [N hotspots identified across X files]
Hotspots investigated: [N]
Confirmed bugs: N (X critical, Y high, Z medium, W low)
Coverage improvements: N tests added
Systemic patterns: N

## CONFIRMED BUGS

### CRITICAL
- **[file:line — description]**
  - Bug: [concrete description]
  - Root cause: [why it exists]
  - Impact: [what happens in practice]
  - Reproducing test: [test file:test name]
  - Fix guidance: [what needs to change]

### HIGH
[same format]

### MEDIUM
[same format]

### LOW
[same format]

## SYSTEMIC PATTERNS

[Cross-cutting issues observed across multiple hotspots]
- [pattern] — observed in [locations] — suggests [recommendation]

## COVERAGE IMPROVEMENTS

[Tests added that didn't find bugs but improved coverage]
- [test name] in [file] — covers [what]

## SUSPECTED BUT UNCONFIRMED

[Issues suspected but not validated with tests — lower confidence]
- [description] — couldn't test because [reason]

## AREAS NOT INVESTIGATED

[Hotspots deprioritized or areas outside scope that may warrant future attention]
```

**Present to user interactively.** Walk through CRITICAL findings first. For each, explain the bug, the impact, and show the reproducing test. Let the user ask questions before moving on.

### 6. Cut Tickets

After presenting findings, propose a ticket structure based on the hunt's shape. Each hunt produces a different mix — concentrated CRITICALs in one module, a single systemic pattern across many modules, mostly coverage-improvements with few confirmed bugs — and the right ticket granularity depends on that shape. Rather than prescribe a fixed mapping, examine the findings and propose a structure that fits.

#### 6a. Analyze Findings and Propose Structure

Examine the consolidated findings produced in step 5:
- Count confirmed bugs by severity (CRITICAL / HIGH / MEDIUM / LOW).
- Count systemic patterns (cross-cutting issues observed across multiple hotspots).
- Count reproducing tests written (some confirm bugs; some are coverage improvements).
- Note clustering — multiple bugs in the same module or in the same defect class.

From that shape, propose a ticket structure. Common shapes:

- **Concentrated bugs:** 1 ticket per CRITICAL/HIGH bug; 1 ticket per systemic pattern; defer MEDIUM/LOW to a batch ticket.
- **Spread across severity:** 1 ticket per CRITICAL bug; batch tickets per severity for HIGH/MEDIUM/LOW.
- **Systemic-pattern-dominated:** 1 ticket per pattern with finding references; per-bug tickets only for the highest-severity outliers.
- **Mostly coverage improvements:** No bug tickets; just commit the reproducing tests as the coverage benefit (handled in step 7).
- **No confirmed bugs:** No tickets to cut. Audit report stands alone; offer test commit per step 7.

Present the proposed structure with the reasoning:

```
Proposed ticket structure for this hunt:

7 confirmed bugs (3 CRITICAL, 3 HIGH, 1 MEDIUM), 1 systemic pattern,
9 reproducing tests.

Proposed: 8 tickets + 1 test commit
  - 1 ticket per CRITICAL/HIGH bug (6 tickets)
  - 1 ticket for the systemic pattern (error-path cleanup missing in
    5 of 12 resource-reserving functions)
  - 1 batch ticket: MEDIUM bugs (1 finding)
  - Reproducing tests committed first so ticket bodies can reference
    them by path.

Approve / edit / decline?
```

Wait for the response. Three outcomes:

- **Approve:** Proceed to 6b.
- **Edit:** The operator modifies the structure (merge two tickets, split one, drop a finding). Apply edits, present revised structure, and repeat until approved.
- **Decline:** Skip to step 7 — offer to commit reproducing tests as a standalone act so the coverage benefit isn't lost.

#### 6b. Commit Reproducing Tests and Create Tickets

Commit all reproducing tests (both bug-confirming and coverage-improving) in a single commit. The commit message should reference the bug hunt and list the test files added. This commit lands first so ticket bodies can reference the test paths by name.

Then create tickets via the canonical tracker integration ([`references/trackers.md`](../../references/trackers.md)). For each ticket in the approved structure:

**Title:** `[<SEVERITY>] <concise bug summary>` (e.g., `[CRITICAL] JPY conversion loses 1 yen for odd amounts in ConvertAmount`).

**Body sections (per-bug tickets):**
- **Bug** — concrete description.
- **Root cause** — why the bug exists.
- **Impact** — what happens in practice.
- **Reproducing test** — `<test file>:<test name>` (committed in the preceding test commit). Serves as the acceptance criterion — the fix is done when the test passes.
- **Fix guidance** — what needs to change.

**For systemic-pattern tickets:**
- **Pattern** — description of the cross-cutting issue.
- **Observed in** — `file:line` locations across the codebase.
- **Recommendation** — usually a follow-up `/refactor` with appropriate scope, or `/implement-batch` if multiple touchpoints need careful coordination.
- **Individual findings** — references to the per-bug tickets if they were cut separately.

**For batch tickets:**
- One section per included finding, using the per-bug body structure.
- A brief intro paragraph explaining the batch theme.

**Labels:** Apply severity labels (`critical` / `high` / `medium` / `low`) when the tracker supports them. The implementation may also apply a `bug` umbrella label if one exists.

After all tickets are created, report the URLs to the operator and exit.

#### Orchestrator-Invoked Behavior

When `/bug-hunt` is invoked by an orchestrator, the workflow above is unchanged. The skill proposes the ticket structure to the orchestrator, which applies its own judgment per [`references/autonomy.md`](../../references/autonomy.md) — approving, editing, or declining the proposal, then deciding which of any created tickets to work in the current flow versus defer.

### 7. Commit Reproducing Tests (Fallback)

This step only runs when the operator declined ticket creation in step 6 (or when the hunt found no confirmed bugs but produced coverage-improvement tests). The reproducing tests are coverage improvements regardless of whether bugs are fixed; this step preserves that value.

Ask: "Would you like to commit the reproducing tests? They document known bugs and improve coverage."

**If yes:** Commit all reproducing tests (both bug-confirming and coverage-improving) in a single commit. Use a descriptive commit message referencing the bug hunt.

**If no:** Leave tests uncommitted for the operator to handle.

## Agent Coordination

**Sequential execution within investigation phase.** The assessor runs first, then hunters run sequentially so findings accumulate for pattern detection.

**No remediation agents.** Step 6 cuts tickets and commits reproducing tests; no `swe-sme-*` or `qa-engineer` invocations happen inside `/bug-hunt`. Remediation is handled out-of-skill by `/implement` or `/implement-project` against the cut tickets, using the reproducing tests as acceptance criteria.

**Fresh instances for every agent.** Each agent gets a clean context window dedicated entirely to its task.

**State to maintain (as orchestrator):**
- Assessor's hotspot list and coverage landscape
- Each hunter's findings (accumulating — passed to subsequent hunters)
- Running totals for the summary
- List of all test files created (for commit step)
- Current hotspot count (for progress tracking)

## Abort Conditions

**Abort investigation of a hotspot:**
- Hunter reports hotspot is clean after thorough investigation (expected and fine — skip to next)

**Abort entire workflow:**
- User interrupts
- Assessor finds no significant hotspots (positive outcome — report clean assessment)
- Critical system error

**Do NOT abort for:**
- Individual clean hotspots (continue to next)
- Test infrastructure issues on a single hotspot (report as unconfirmed, continue)
- Low-confidence findings (include in report as SUSPECTED BUT UNCONFIRMED)

## Integration with Other Skills

**`/bug-hunt` vs `/review-security`:** Different lenses on overlapping territory. `/review-security` asks "can an attacker exploit this?" `/bug-hunt` asks "will this fail for a normal user?" Run both for comprehensive pre-release assurance.

**`/bug-hunt` vs `/bug-fix`:** `/bug-hunt` is proactive — it finds bugs before they're reported. `/bug-fix` is reactive — it fixes a known, reported bug. Bug-hunt findings can feed into `/bug-fix` for thorough remediation of complex issues.

**`/bug-hunt` → `/refactor`:** Systemic patterns identified by `/bug-hunt` (e.g., "inconsistent error handling across 15 modules") may warrant a follow-up `/refactor` to fix the pattern systematically.

## Example Session

```
> /bug-hunt

What is the scope of the hunt?
> Focus on the payment processing module — we've had some edge case reports

Anything you're particularly worried about?
> Currency conversion and rounding — we support 30+ currencies now

Anything to skip beyond the defaults?
> No, defaults are fine

Starting proactive bug hunt...

[Phase 1 — Risk Assessment]
Spawning assessor...

Assessment report:
  Coverage: 67% line coverage (instrumented via go test -cover)
  Hotspots identified: 8 (3 critical, 3 high, 2 medium)

  CRITICAL-1: payment/converter.go:ConvertAmount (lines 45-112)
    Signals: 0% test coverage + deep nesting (6 levels) + floating-point
      arithmetic
    Hypothesis: Currency conversion may lose precision or handle edge
      currencies incorrectly

  CRITICAL-2: payment/checkout.go:ProcessCheckout (lines 23-89)
    Signals: Partial coverage (happy path only) + error handling
      inconsistency + 3 bug-fix commits in last month
    Hypothesis: Error paths may leave order in inconsistent state

  CRITICAL-3: payment/refund.go:CalculateRefund (lines 15-78)
    Signals: No test coverage + complex conditional logic + shared mutable
      state (order object)
    Hypothesis: Partial refund calculations may be incorrect for multi-item
      orders

  HIGH-1: payment/currency/rates.go:FetchRates (lines 30-67)
    Signals: No error path tests + external API dependency + no timeout
      handling
    ...

[Phase 2 — Focused Investigation]

Spawning hunter for CRITICAL-1 (ConvertAmount)...

  Test 1: TestConvertAmount_ZeroCurrencyPrecision — FAIL
    Bug confirmed: JPY (0-decimal currency) conversion multiplies by 100
    then divides by 100, losing the original integer value for odd amounts.
    Impact: ¥101 → ¥100 (1 yen lost per odd-amount transaction)

  Test 2: TestConvertAmount_SameCurrency — PASS
    Kept: covers previously untested identity conversion path

  Test 3: TestConvertAmount_NegativeAmount — FAIL
    Bug confirmed: Negative amounts (credits/adjustments) bypass validation
    and produce positive conversion results due to Abs() call without
    sign restoration.
    Impact: -$10.00 credit → +€8.50 charge

  Test 4: TestConvertAmount_UnknownCurrency — PASS
    Kept: covers error path for unsupported currency codes

  Findings: 2 confirmed bugs, 2 coverage improvements

Spawning hunter for CRITICAL-2 (ProcessCheckout)...

  Test 1: TestProcessCheckout_PaymentFailureCleanup — FAIL
    Bug confirmed: When payment gateway returns error after inventory was
    reserved, inventory reservation is not released. Order stuck in
    "processing" state.
    Impact: Phantom inventory holds that never clear (requires manual DB fix)

  Pattern noted: cleanup-on-error-path is missing in 3 other functions
  in this package (passed to next hunter)

  ...

[Phase 3 — Synthesis]

Confirmed bugs: 7 (3 critical, 3 high, 1 medium)
Coverage improvements: 9 tests added
Systemic pattern: Error-path cleanup is missing in 5 of 12 functions
  that reserve resources — this is a codebase-wide pattern, not isolated.

## Bug Hunt Summary
[Full report...]

Proposed ticket structure for this hunt:

7 confirmed bugs (3 CRITICAL, 3 HIGH, 1 MEDIUM), 1 systemic pattern,
9 reproducing tests.

Proposed: 8 tickets + 1 test commit
  - 1 ticket per CRITICAL/HIGH bug (6 tickets)
  - 1 ticket for the systemic pattern (error-path cleanup missing in
    5 of 12 resource-reserving functions)
  - 1 batch ticket: MEDIUM bugs (1 finding)
  - Reproducing tests committed first so ticket bodies can reference
    them by path.

Approve / edit / decline?
> Approve

Committing reproducing tests... (9 tests, 1 commit)
Creating tickets...
  #N — [CRITICAL] JPY conversion loses 1 yen for odd amounts
  #N — [CRITICAL] Negative-amount currency conversion bypasses sign
  #N — [CRITICAL] Payment failure leaves phantom inventory holds
  #N — [HIGH] FetchRates lacks timeout handling
  #N — [HIGH] Multi-item refund miscalculates partial amounts
  #N — [HIGH] Race in checkout state transition
  #N — [SYSTEMIC] Error-path cleanup missing in 5 resource-reserving
                  functions
  #N — [MEDIUM] One MEDIUM finding (batch ticket)

8 tickets created. Reproducing tests committed. Hunt complete.
```
