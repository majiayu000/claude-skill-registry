---
description: "Use when you want to generate Architecture Decision Records from this session. Triggers on \"write ADRs\", \"document our decisions\", \"create decision records\", \"record the choices we made\". Also useful after design discussions where decisions were reached but not documented. Does NOT extract decisions alone (use adr-decision-extraction) or provide MADR template (use adr-writing). Orchestrates the full workflow: subagent extraction, user confirmation, parallel generation, and verification."
name: write-adr
disable-model-invocation: true
---

# Write ADR

Generate Architecture Decision Records (ADRs) from decisions made during the current session.

## Workflow Overview

1. **Context** - Gather repository context and existing ADRs
2. **Extract** - Analyze conversation for decisions using a subagent
3. **Confirm** - Present decisions to user for selection
4. **Write** - Generate ADRs in parallel using subagents
5. **Report** - Summarize created files and status
6. **Verify** - Validate generated ADRs against Definition of Done

### Gates (objective pass conditions)

Advance only when the **pass condition** holds. These are checkable without “I verified internally.”

| After | Pass condition |
|-------|----------------|
| Step 2 (extract) | The subagent response is **valid JSON** with a top-level `decisions` **array** (empty is OK). Each non-empty item has `id`, `title`, and at least one of `context`, `decision`, `alternatives`, or `rationale` present as a non-empty string or non-empty array. If parsing fails or the shape is wrong, **re-run extraction or fix the payload** before Step 3. |
| Step 4 (pre-allocate) | From repo root, `python plugins/beagle-analysis/skills/adr-writing/scripts/next_adr_number.py --count N` prints **exactly `N` lines** (one number per line). You have a **written mapping** (in the reply draft or notes) from each selected decision to one of those lines **before** launching any `run_in_background` ADR writer Task. |
| Step 5 (report) | Every file path in the summary table is copied from a subagent completion output (not invented). Optionally **spot-check**: `test -f <path>` for each path before marking success. |
| Step 6 (verify) | For each ADR path, opening the file shows **line 1 is `---`**, frontmatter parses as YAML, `status` and `date` are present, and the body meets the Step 6 bullets below (alternatives count, Good/Bad consequences). |

## Step 1: Gather Context

```bash
# Get current branch and recent commits
git branch --show-current
git log --oneline -5

# Check for existing ADRs
ls docs/adrs/ 2>/dev/null || echo "No ADR directory found"

# Count existing ADRs for numbering
find docs/adrs -name "*.md" 2>/dev/null | wc -l
```

This context helps the ADR writer:
- Reference related commits in the ADR
- Avoid duplicate ADRs for already-documented decisions
- Determine correct sequence numbering

## Step 2: Extract Decisions

Launch a subagent to analyze the current conversation for architectural decisions:

```text
Task(
  description: "Analyze conversation and extract architectural decisions",
  model: "sonnet",
  prompt: |
    Load the skill: Skill(skill: "beagle-analysis:adr-decision-extraction")

    Analyze the conversation for decisions that warrant ADRs:
    - Technology choices, architecture patterns, design trade-offs
    - Rejected alternatives, significant implementation approaches

    Return JSON:
    {
      "decisions": [
        {
          "id": 1,
          "title": "Use PostgreSQL for primary datastore",
          "context": "Brief context about why this came up",
          "decision": "What was decided",
          "alternatives": ["What was considered but rejected"],
          "rationale": "Why this choice was made"
        }
      ]
    }
)
```

If the subagent returns an empty `decisions` array, skip to Step 5 with message: "No architectural decisions detected in this session."

**Gate:** Meet the Step 2 row in **Gates (objective pass conditions)** before Step 3.

## Step 3: Confirm with User

**Display all extracted decisions with full details**, then ask user to select:

```text
## Detected Decisions

### 1. Use PostgreSQL for primary datastore
**Confidence:** high

**Problem:** Need ACID transactions for financial records

**Decision:** PostgreSQL for user data storage

**Alternatives discussed:**
- MongoDB
- SQLite

**Rationale:** ACID compliance, team familiarity, mature ecosystem

**Source:** Discussion about database selection in planning phase

---

### 2. Implement event sourcing for audit trail
**Confidence:** medium

**Problem:** Compliance requires complete audit history

**Decision:** Event sourcing pattern for state changes

**Alternatives discussed:**
- Database triggers
- Application-level logging

**Rationale:** Immutable audit trail, temporal queries, debugging capability

**Source:** Compliance requirements discussion

---

## Selection

Which decisions should I write ADRs for?
- Enter numbers (e.g., "1,2" or "1-2"), "all", or "none" to skip
```

**Important:** Always display the full decision details (problem, decision, alternatives, rationale) from the extraction output BEFORE asking for selection. Do not truncate to just title and context.

Parse user response:
- `"all"` - Process all decisions
- `"none"` or empty - Skip with message "No ADRs will be created."
- `"1,2"` or `"1-2"` - Process specified decisions

## Step 4: Write ADRs (Parallel)

**Pre-allocate ADR numbers before launching subagents** to prevent numbering conflicts:

```bash
# Pre-allocate numbers for all confirmed decisions (from repository root)
# Example: If user selected 3 decisions
python plugins/beagle-analysis/skills/adr-writing/scripts/next_adr_number.py --count 3
# Output:
# 0003
# 0004
# 0005
```

**Assign each pre-allocated number to its corresponding decision** before launching subagents.

**Gate:** Meet the Step 4 row in **Gates (objective pass conditions)** before the first `Task(` launch.

For each confirmed decision, launch an ADR Writer subagent in background with its **pre-assigned number**:

```text
Task(
  description: "Write ADR for: {decision.title}",
  model: "sonnet",
  run_in_background: true,
  prompt: |
    Load the skill: Skill(skill: "beagle-analysis:adr-writing")

    Write an ADR for this decision:
    ```json
    {decision JSON}
    ```

    **IMPORTANT: Use this pre-assigned ADR number: {assigned_number}**

    Instructions:
    1. Explore codebase for additional context
    2. Write MADR-formatted ADR to docs/adrs/
    3. Use the pre-assigned number {assigned_number} - DO NOT call next_adr_number.py
    4. Filename format: {assigned_number}-slugified-title.md
    5. Return created file path
)
```

**Critical:** Pass the pre-allocated number to each subagent. Subagents must NOT call `next_adr_number.py` themselves - this causes duplicate numbers when running in parallel.

All subagents run in parallel. Wait for all to complete before proceeding.

## Step 5: Report Results

**Gate:** Meet the Step 5 row in **Gates (objective pass conditions)** when building the summary (paths from subagent outputs; optional `test -f`).

Collect outputs from all subagents and present summary:

```markdown
## ADR Generation Complete

| File | Decision | Status |
|------|----------|--------|
| docs/adrs/0003-use-postgresql.md | Use PostgreSQL for primary datastore | Draft |

### Next Steps
- Review generated ADRs for accuracy
- Update status from "proposed" to "accepted" when finalized

### Gaps Requiring Investigation
- [List any decisions where subagent noted missing context]
```

If no decisions were processed:
```text
No ADRs were created. Run this command again after making architectural decisions.
```

## Step 6: Verify Generated ADRs

For each created ADR, validate against Definition of Done:

```markdown
## Verification Checklist

| ADR | E | C | A | D | R | Status |
|-----|---|---|---|---|---|--------|
| 0003-use-postgresql.md | ✓ | ✓ | ✓ | ⚠ | ✗ | Incomplete |

Legend: E=Evidence, C=Criteria, A=Agreement, D=Documentation, R=Realization
```

**Gate:** Meet the Step 6 row in **Gates (objective pass conditions)** for every created ADR.

**Verification steps:**
1. Open each generated ADR file
2. Confirm filename follows `NNNN-slugified-title.md` pattern
3. **Verify YAML frontmatter exists at file start:**
   - File MUST begin with `---`
   - Contains `status: draft` (or valid status)
   - Contains `date: YYYY-MM-DD` (actual date)
   - Ends with `---` before title
   - If frontmatter is missing, add it immediately
4. Review for `[INVESTIGATE]` prompts - these need follow-up
5. Verify at least 2 alternatives are documented
6. Confirm consequences section has both Good and Bad items

**If gaps exist:**
- Keep status as `draft` until gaps are resolved
- Use `[INVESTIGATE]` prompts to guide follow-up session
- Schedule review with stakeholders before changing to `accepted`

## Output Location

ADRs are written to `docs/adrs/` (same convention as `beagle-analysis:adr-writing`). If no ADR directory exists, create it with an initial `0000-use-madr.md` template record.

## MADR Format Reference

```markdown
---
status: draft
date: YYYY-MM-DD
---

# {TITLE}

## Context and Problem Statement

{What is the issue motivating this decision?}

## Decision Drivers

* {driver 1}
* {driver 2}

## Decision Outcome

Chosen option: "{option}", because {reason}.

### Consequences

* Good, because {positive}
* Bad, because {negative}
```
