---
name: ds-verify
description: "This skill should be used when the user asks to 'verify analysis results', 'check reproducibility', 'validate data science output', 'confirm completion', or as Phase 5 of the /ds workflow (final). Enforces reproducibility demonstration and user acceptance before completion claims."
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

# Verification Gate

Final verification with reproducibility checks and user acceptance interview.

<EXTREMELY-IMPORTANT>
## The Iron Law of DS Verification

**NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION. This is not negotiable.**

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

**If you catch yourself thinking "I can skip verification," STOP - you're about to lie.**
</EXTREMELY-IMPORTANT>

## Red Flags - STOP Immediately If You Think:

| Thought | Why It's Wrong | Do Instead |
|---------|----------------|------------|
| "Results should be the same" | Your "should" isn't verification | Re-run and compare |
| "I ran it earlier" | Your earlier run isn't fresh | Run it again now |
| "It's reproducible" | Your claim requires evidence | Demonstrate reproducibility |
| "User will be happy" | Your assumption isn't their acceptance | Ask explicitly |
| "Outputs look right" | Your visual inspection isn't verified | Check against criteria |

## The Verification Gate

Before making ANY completion claim:

```
1. RE-RUN    → Execute fresh, not from cache
2. CHECK     → Compare outputs to success criteria
3. REPRODUCE → Same inputs → same outputs
4. ASK       → User acceptance interview
5. CLAIM     → Only after steps 1-4
```

**Skipping any step is not verification.**

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

For notebooks:
```bash
# notebook-reproduce: Clear and re-run all cells from scratch
jupyter nbconvert --execute --inplace notebook.ipynb

# notebook-reproduce-with-seed: Execute notebook with fixed random seed for reproducibility
papermill notebook.ipynb output.ipynb -p seed 42
```

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
- Clean up `.claude/` files
- Start a new analysis with `/ds`
