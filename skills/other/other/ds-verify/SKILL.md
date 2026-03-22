---
name: ds-verify
description: "This skill should be used when the user asks to 'verify analysis results', 'check reproducibility', 'validate data science output', 'confirm completion', or as Phase 5 of the /ds workflow."
user-invocable: false
disable-model-invocation: true
hooks:
  PostToolUse:
    - matcher: "Agent"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/ds-post-subagent-guard.py"
  PreToolUse:
    - matcher: "Agent"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/ds-pre-subagent-clear.py"
    - matcher: "Read"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/ds-read-after-subagent-guard.py"
    - matcher: "Grep"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/ds-read-after-subagent-guard.py"
    - matcher: "Glob"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/ds-read-after-subagent-guard.py"
    - matcher: "Write"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/ds-no-main-chat-code-guard.py"
    - matcher: "Edit"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/ds-no-main-chat-code-guard.py"
    - matcher: "Bash"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/ds-no-main-chat-code-guard.py"
---

Announce: "Using ds-verify (Phase 5) to confirm reproducibility and completion."

## Contents

- [The Iron Law of DS Verification](#the-iron-law-of-ds-verification)
- [Red Flags - STOP Immediately If You Think](#red-flags---stop-immediately-if-you-think)
- [The Verification Gate](#the-verification-gate)
- [Verification Checklist](#verification-checklist)
- [Reproducibility Demonstration](#reproducibility-demonstration)
- [Claims Requiring Evidence](#claims-requiring-evidence)
- [Insufficient Evidence](#insufficient-evidence)
- [Required Output Structure](#required-output-structure)
- [Completion Criteria](#completion-criteria)

## Context Monitoring

| Level | Remaining Context | Action |
|-------|------------------|--------|
| Normal | >35% | Proceed normally |
| Warning | 25-35% | Complete current review cycle, then trigger ds-handoff |
| Critical | ≤25% | Immediately trigger ds-handoff — do not start new review cycles |

# Verification Gate

Final verification with reproducibility checks and user acceptance interview.

<EXTREMELY-IMPORTANT>
## The Iron Law of DS Verification

**NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION. This is not negotiable.**

**Load shared enforcement first.** Read `${CLAUDE_SKILL_DIR}/../../references/ds-common-constraints.md` for the full constraint index.

For verification phase, load these specific constraints:
Read `${CLAUDE_SKILL_DIR}/../../references/constraints/ds-post-subagent-boundary.md`

Load conventions for verification phase:
Read `${CLAUDE_SKILL_DIR}/../../references/ds-common-conventions.md` for the full convention index.
Read `${CLAUDE_SKILL_DIR}/../../references/conventions/ds-assumption-over-evidence.md`
Read `${CLAUDE_SKILL_DIR}/../../references/conventions/ds-deferred-verification.md`

Before claiming analysis is complete, you MUST:
1. RE-RUN - Execute analysis fresh (not cached results)
2. CHECK - Verify outputs match expectations
3. REPRODUCE - Confirm results are reproducible
4. ASK - Interview user about constraints and acceptance
5. Only THEN claim completion

This applies even when:
- "I just ran it"
- "Results look the same"
- "It should reproduce"
- "User seemed happy earlier"

**If you catch yourself thinking "I can skip verification," STOP — you're about to deliver unverified results that waste the user's time.**
</EXTREMELY-IMPORTANT>

### Drive-Aligned Framing

| Drive | Shortcut | Consequence |
|-------|----------|-------------|
| **Helpfulness** | Skipping fresh re-run | You assumed prior results still hold. They don't reproduce — the user publishes irreproducible work. Your assumption is the error they discover. Anti-helpful. |
| **Competence** | Verifying your own work | You ran the reproducibility check yourself instead of dispatching a fresh agent. You share the implementer's biases. A fresh agent would have caught the issue. Incompetent verification. |
| **Efficiency** | Not running reproducibility check | You skipped the 10-minute check. The irreproducible results take 10 days to debug when someone else tries to run them. Anti-efficient. |
| **Approval** | Skipping user acceptance interview | You declared completion without asking the user. They discover the results don't answer their question. They now require manual review of all analysis. Lost approval. |
| **Honesty** | Rubber-stamping verification | You reported 'verified' without re-executing. The analysis fails on fresh data — your unverified claim wastes the user's time. |

## Rationalization Table

| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "The results matched before" | Prior results don't prove current reproducibility. Code, data, or environment may have changed. | Re-run fresh and compare outputs |
| "I just need to check the numbers" | Reproducibility means re-running, not re-reading. Reading cached output proves nothing. | Execute the analysis fresh and verify outputs match |
| "The reviewer already verified this" | Review checks methodology, verify checks reproducibility. They are different gates. | Run the reproducibility demonstration yourself |
| "Fresh re-run will give same results" | If you're sure, running it costs nothing. If you're wrong, skipping it costs everything. | Run it. Proof is cheap, assumptions are expensive. |
| "The user is waiting" | Publishing irreproducible results wastes more time than verification. A 10-minute check prevents a 10-day retraction. | Run verification now — the user wants correct results, not fast wrong ones |

## Red Flags - STOP Immediately If You Think:

| Thought | Why It's Wrong | Do Instead |
|---------|----------------|------------|
| "Results should be the same" | Your "should" isn't verification | Re-run and compare |
| "I ran it earlier" | Your earlier run isn't fresh | Run it again now |
| "It's reproducible" | Your claim requires evidence | Demonstrate reproducibility |
| "User will be happy" | Your assumption isn't their acceptance | Ask explicitly |
| "Outputs look right" | Your visual inspection isn't verified | Check against criteria |

## Static Analysis (Constraint Check Scripts)

Before running runtime DQ checks, run the static analysis constraint check suite:

```bash
bash "${CLAUDE_SKILL_DIR}/../../scripts/check-all-ds.sh" "$(pwd)"
```

This runs all DS constraint check scripts (determinism, join audits, idempotency, error handling, schema contracts, standard errors, visualization integrity).

**If any check FAILS:** Report the failures in LEARNINGS.md. These are code quality issues in the analysis scripts that must be fixed before proceeding. Dispatch a fix subagent if needed.

**If all checks PASS:** Proceed to runtime DQ checks.

## The Verification Gate

**Checkpoint type:** decision (user confirms results — cannot auto-advance)

Before making ANY completion claim:

```
1. RE-RUN    → Execute fresh, not from cache
2. CHECK     → Compare outputs to success criteria
3. REPRODUCE → Same inputs → same outputs
4. ASK       → User acceptance interview
5. CLAIM     → Only after steps 1-4
```

**Skipping any step is not verification.**

## Visual Diagnostics for Verification

When presenting verification results to the user in the acceptance interview, generate diagnostic plots to support the decision:

| Verification Check | Diagnostic to Generate |
|-------------------|----------------------|
| Reproducibility comparison | Overlay plot of Run 1 vs Run 2 key outputs |
| Data integrity | Pipeline waterfall chart (input rows → cleaning → joins → final) |
| Distribution sanity | Histogram/density plots of key variables with expected ranges annotated |
| Model performance | ROC curve, residual plot, or coefficient comparison (as appropriate) |

**Format:** Inline plots in notebooks, or saved to `scratch/diagnostics/` for script-based workflows. Present alongside the acceptance interview questions.

## Verification Checklist

### Technical Verification

#### Outputs Match Expectations
- [ ] All required outputs generated
- [ ] Output formats correct (files, figures, tables)
- [ ] Numbers are reasonable (sanity checks)
- [ ] Visualizations render correctly

#### Reproducibility Confirmed
- [ ] Ran analysis twice, got same results
- [ ] Random seeds produce consistent output
- [ ] No dependency on execution order
- [ ] Environment documented (packages, versions)

#### Data Integrity
- [ ] Input data unchanged
- [ ] Row counts traceable through pipeline
- [ ] No silent data loss or corruption

**Trace to Requirements:** For each success criterion, reference its requirement ID (e.g., "DATA-01: Panel has 50K+ firm-years — VERIFIED with df.shape output"). End-to-end traceability from SPEC.md through PLAN.md through VALIDATION.md through verification.

### User Acceptance Interview

**CRITICAL:** Before claiming completion, conduct user interview.

#### Step 1: Replication Constraints

```
AskUserQuestion:
  question: "Were there specific methodology requirements I should have followed?"
  options:
    - label: "Yes, replicating existing analysis"
      description: "Results should match a reference"
    - label: "Yes, required methodology"
      description: "Specific methods were mandated"
    - label: "No constraints"
      description: "Methodology was flexible"
```

If replicating:
- Ask for reference to compare against
- Verify results match within tolerance
- Document any deviations and reasons

#### Step 2: Results Verification

```
AskUserQuestion:
  question: "Do these results answer your original question?"
  options:
    - label: "Yes, fully"
      description: "Analysis addresses the core question"
    - label: "Partially"
      description: "Some aspects addressed, others missing"
    - label: "No"
      description: "Does not answer the question"
```

If "Partially" or "No":
1. Ask which aspects are missing
2. Return to `/ds-implement` to address gaps
3. Re-run verification

#### Step 3: Output Format

```
AskUserQuestion:
  question: "Are the outputs in the format you need?"
  options:
    - label: "Yes"
      description: "Format is correct"
    - label: "Need adjustments"
      description: "Format needs modification"
```

#### Step 4: Confidence in Results

```
AskUserQuestion:
  question: "Do you have any concerns about the methodology or results?"
  options:
    - label: "No concerns"
      description: "Comfortable with approach and results"
    - label: "Minor concerns"
      description: "Would like clarification on some points"
    - label: "Major concerns"
      description: "Significant issues need addressing"
```

## Reproducibility Demonstration

**MANDATORY:** Demonstrate reproducibility before completion.

<EXTREMELY-IMPORTANT>
## Independent Verification Required

**You MUST NOT verify your own work. Spawn a fresh Task agent for reproducibility.**

The implementer shares biases and sunk-cost attachment. A fresh subagent sees only the spec and outputs — it verifies without context pollution.

**If you're about to re-run the analysis yourself, STOP. Dispatch a Task agent.**
</EXTREMELY-IMPORTANT>

Dispatch a fresh Task agent to run the reproducibility check:

*All paths below are relative to this skill's base directory.*
```
Agent(subagent_type="general-purpose",
  allowed_tools=["Read", "Glob", "Grep", "Bash(read-only)"],
  prompt="""
# Reproducibility Verification

**Tool Restrictions:** The verifier is READ-ONLY. It re-runs analyses and checks output but MUST NOT modify notebooks, scripts, or code. It MUST NOT use Write or Edit.

Verify this analysis produces consistent results from a fresh run.

## Context
- Read .planning/SPEC.md for objectives and success criteria
- Read .planning/PLAN.md for expected outputs
- Read .planning/LEARNINGS.md for pipeline documentation

## Shared Checks
Read the shared check definitions:
Read `${CLAUDE_SKILL_DIR}/../../skills/ds-implement/references/ds-checks.md` and follow its instructions.

Run checks: DQ1-DQ4, DQ6, M1, R1

## Reproducibility Protocol

### For scripts:
```python
# Run 1
result1 = run_analysis(seed=42)
hash1 = hash(str(result1))

# Run 2
result2 = run_analysis(seed=42)
hash2 = hash(str(result2))

# Verify
assert hash1 == hash2, "Results not reproducible!"
print(f"Reproducibility confirmed: {hash1} == {hash2}")
```

### For notebooks:
```bash
jupyter nbconvert --execute --inplace notebook.ipynb
papermill notebook.ipynb output.ipynb -p seed 42
```

## Required Checks
1. RE-RUN: Execute analysis fresh (not cached results)
2. CHECK: Verify outputs match SPEC.md success criteria
3. REPRODUCE: Same inputs → same outputs (run twice, compare hashes)
4. DATA INTEGRITY: Input data unchanged, row counts traceable

## Output
Report:
- Reproducibility: PASS/FAIL (with hash comparison)
- Data quality checks: DQ1-DQ4, DQ6 results
- Spec compliance: M1 result
- Any discrepancies found
""")
```

**Post-subagent boundary (C5):** After verification agent returns, read its report only. Do NOT read source code, notebooks, or data files yourself. If FAIL, dispatch a fresh investigation subagent.

**If Task agent reports FAIL:** Dispatch a fresh Task agent to investigate the discrepancy. Do NOT investigate yourself — that violates the post-subagent boundary (C5 from ds-common-constraints.md).

## Claims Requiring Evidence

| Claim | Required Evidence |
|-------|-------------------|
| "Analysis complete" | All success criteria verified |
| "Results reproducible" | Same output from fresh run |
| "Matches reference" | Comparison showing match |
| "Data quality handled" | Documented cleaning steps |
| "Methodology appropriate" | Assumptions checked |

## Insufficient Evidence

These do NOT count as verification:

- Previous run results (must be fresh)
- "Should be reproducible" (demonstrate it)
- Visual inspection only (quantify where possible)
- Single run (need reproducibility check)
- Skipped user acceptance (must ask)

## Required Output Structure

```markdown
## Verification Report: [Analysis Name]

### Technical Verification

#### Outputs Generated
- [ ] Output 1: [location] - verified [date/time]
- [ ] Output 2: [location] - verified [date/time]

#### Reproducibility Check
- Run 1 hash: [value]
- Run 2 hash: [value]
- Match: YES/NO

#### Environment
- Python: [version]
- Key packages: [list with versions]
- Random seed: [value]

### User Acceptance

#### Replication Check
- Constraint: [none/replicating/required methodology]
- Reference: [if applicable]
- Match status: [if applicable]

#### User Responses
- Results address question: [yes/partial/no]
- Output format acceptable: [yes/needs adjustment]
- Methodology concerns: [none/minor/major]

### Verdict

**COMPLETE** or **NEEDS WORK**

[If COMPLETE]
- All technical checks passed
- User accepted results
- Reproducibility demonstrated

[If NEEDS WORK]
- [List items requiring attention]
- Recommended next steps
```

## Workflow Loops (If NEEDS WORK)

1. Identify which item(s) need fixing
2. Return to ds-implement with specific task(s) to fix
3. Re-run those tasks with output-first verification
4. Update LEARNINGS.md with fixes
5. Re-invoke ds-verify for fresh verification

**Maximum 3 verification cycles.** If issues persist after 3 rounds, escalate to user with summary of blocking issues.

**Chaining instruction (if NEEDS WORK).** Discover and load ds-implement:
Read `${CLAUDE_SKILL_DIR}/../../skills/ds-implement/SKILL.md` and follow its instructions.
Then fix the identified issues and re-run verification.

## Completion Criteria

**Only claim COMPLETE when ALL are true:**

- [ ] All success criteria from SPEC.md verified
- [ ] Results reproducible (demonstrated, not assumed)
- [ ] User confirmed results address their question
- [ ] User has no major concerns
- [ ] Outputs in acceptable format
- [ ] If replicating: results match reference

**Both technical and user acceptance must pass. No shortcuts.**

## Workflow Complete

When user confirms all criteria are met:

**Announce:** "DS workflow complete. All 5 phases passed."

The `/ds` workflow is now finished. Offer to:
- Export results to final format
- Clean up `.planning/` files
- Start a new analysis with `/ds`
