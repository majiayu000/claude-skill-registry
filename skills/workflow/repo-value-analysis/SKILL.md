---
name: repo-value-analysis
description: "Analyze external repositories for adoptable ideas and patterns."
user-invocable: false
argument-hint: "<repo-url-or-path>"
agent: research-coordinator-engineer
allowed-tools:
  - Agent
  - Read
  - Write
  - Bash
  - Grep
  - Glob
routing:
  triggers:
    - repo value analysis
    - does repo add value
    - analyze repo for ideas
    - what can we learn from
    - compare against repo
    - read every file in repo
  pairs_with:
    - workflow
  complexity: Complex
  category: analysis
---

# Repo Competitive Analysis Pipeline

## Overview

This skill conducts systematic 6-phase analysis of external repositories to assess their value for adoption. You dispatch parallel subagents to read and catalog every file in an external repo, inventory your own toolkit in parallel, identify genuine capability gaps, audit those gaps against your actual codebase, and produce a reality-grounded comparison report with adoption recommendations.

The pipeline enforces **full file reading** (not sampling), **parallel execution** (up to 8 agent zones simultaneously), and **mandatory audit** (every recommendation verified before reporting). Optional flags allow local analysis (`--local`), zone focus (`--zone`), and quick comparison (`--quick` skips audit).

---

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| errors, error handling | `error-handling.md` | Loads detailed guidance from `error-handling.md`. |
| Phase 2 DEEP-READ: zone agent dispatch | `phase2-agent-template.md` | Loads detailed guidance from `phase2-agent-template.md`. |
| Phase 3 INVENTORY: cataloging our system | `phase3-inventory-template.md` | Loads detailed guidance from `phase3-inventory-template.md`. |
| Phase 5 AUDIT: verifying HIGH/MEDIUM recommendations | `phase5-audit-template.md` | Loads detailed guidance from `phase5-audit-template.md`. |
| Phase 6 REPORT: final report structure | `phase6-report-template.md` | Loads detailed guidance from `phase6-report-template.md`. |

## Instructions

### Input Parsing

Before starting Phase 1, parse the user's input:
- **GitHub URL**: Extract repo name from URL (e.g., `https://github.com/org/repo` -> `repo`)
- **Local path**: Validate the path exists and contains files
- **Bare repo name**: Assume `https://github.com/{name}` if it looks like `org/repo`

Set `REPO_NAME` and `REPO_PATH` variables for use throughout the pipeline.

### Phase 1: CLONE

**Goal**: Obtain the repository and categorize its contents into zones for parallel deep-read.

**Step 1: Clone the repository**

```bash
git clone --depth 1 <url> /tmp/<REPO_NAME>
```

If `--local` flag was provided, skip cloning and use the provided path instead. This allows re-analysis of already-cloned repos without redundant network calls.

**Step 2: Count and categorize files**

Survey the repository structure:
- Count total files (excluding `.git/`)
- List top-level directories with file counts

This gives you a baseline for zone complexity and helps identify sub-repo patterns.

**Step 3: Define analysis zones**

Categorize files into zones based on directory names and file patterns. Zones organize the repo into digestible chunks:

| Zone | Typical directories/patterns | Purpose |
|------|------------------------------|---------|
| skills | `skills/`, `commands/`, `prompts/`, `templates/` | Reusable skill/prompt definitions |
| agents | `agents/`, `personas/`, `roles/` | Agent configurations |
| hooks | `hooks/`, `middleware/`, `interceptors/` | Event-driven automation |
| docs | `docs/`, `*.md` (non-config), `adr/`, `guides/` | Documentation and decisions |
| tests | `tests/`, `*_test.*`, `*.spec.*`, `__tests__/` | Test suites |
| config | Config files, CI/CD, `*.yaml`, `*.toml`, `*.json` (root) | Configuration |
| code | `scripts/`, `src/`, `lib/`, `pkg/`, `*.py`, `*.go`, `*.ts` | Source code |
| other | Everything else | Uncategorized files |

**Step 4: Cap zones for parallel feasibility**

If any zone exceeds ~100 files, split it into sub-zones by subdirectory. Each sub-zone gets its own agent in Phase 2. Cap at ~100 files per agent because:
- Agents MUST read **every file** in their zone, not sample or skim (sampling introduces bias and misses distinguishing components)
- ~100 files is feasible for a single agent within budget and timeout
- Larger zones are split, so no single agent is overwhelmed

Log the split decisions in the analysis notes for transparency.

**Gate**: Repository cloned (or local path validated). All files categorized into zones. Zone file counts recorded. No zone exceeds ~100 files (split if needed). Proceed only when gate passes.

### Phase 2: DEEP-READ (Parallel)

**Goal**: Read every file in every zone of the external repository to extract techniques, patterns, and potential capability gaps.

Dispatch 1 Agent per analysis zone (background). Each agent receives the zone name and file list, instructions to read EVERY file (not sample, not skim) to avoid sampling bias, and a structured output template.

See `references/phase2-agent-template.md` for the full agent instructions template and parallel dispatch rules.

**Gate**: All zone agents have completed (or timed out after 5 minutes each). At least 75% of agents returned results (tolerance for individual agent failure). Zone finding files exist in `/tmp/`. Proceed only when gate passes.

### Phase 3: INVENTORY (Parallel with Phase 2)

**Goal**: Catalog our own toolkit simultaneously with Phase 2 deep-read for faster wall-clock time.

Dispatch 1 Agent (in background, concurrent with Phase 2 zone agents) to inventory our system. Running this in parallel is safe because inventory is a read-only catalog of our codebase.

See `references/phase3-inventory-template.md` for the full agent instructions and parallel-execution rationale.

**Gate**: Self-inventory agent completed (or timed out after 5 minutes). `/tmp/self-inventory.md` exists and contains counts for all 4 component types. Proceed only when gate passes.

### Phase 4: SYNTHESIZE

**Goal**: Merge Phase 2 and Phase 3 findings into a draft comparison with candidate adoption recommendations.

**Step 1: Read all zone findings and inventory**

Read every `/tmp/[REPO_NAME]-zone-*.md` file and `/tmp/self-inventory.md` to build a unified picture.

**Step 2: Build comparison table**

For each capability area discovered in the external repo, document what we have vs what they have:

| Capability | Their Approach | Our Approach | Gap? |
|------------|---------------|--------------|------|
| ... | ... | ... | Yes/No/Partial |

This table is relative: "what do they have that we lack?" not "what do they have?"

**Step 3: Identify candidate recommendations**

For each genuine gap (not just a different approach to the same thing):
- Describe what they have
- Describe what we lack
- Rate value honestly: HIGH / MEDIUM / LOW
  - HIGH = addresses a real pain point or enables new capability
  - MEDIUM = nice to have, improves existing workflow
  - LOW = marginal improvement, different but not better

Resist the temptation to over-count differences as gaps. A different naming convention is not a gap worth addressing.

**Step 4: Save draft report**

Save to `research-[REPO_NAME]-comparison.md` with:
- Executive summary
- Comparison table
- Candidate recommendations with ratings
- Clear "DRAFT — pending Phase 5 audit" watermark

This draft is intentionally unaudited so you can bail out early if findings look weak.

**Gate**: Draft report saved. At least 1 candidate recommendation identified (or explicit "no gaps found" conclusion). All recommendations have value ratings. Proceed only when gate passes.

### Phase 5: AUDIT (Parallel)

**Goal**: Reality-check each HIGH and MEDIUM recommendation against our actual codebase to catch "we already have this" false positives.

For each HIGH or MEDIUM recommendation, dispatch 1 Agent (in background). Audit is what separates superficial analysis from rigorous analysis — skipping it produces unverified recommendations that erode trust.

See `references/phase5-audit-template.md` for the full audit agent instructions, coverage levels (ALREADY EXISTS / PARTIAL / MISSING), and `--quick` flag behavior.

**Gate**: All audit agents completed (or timed out after 5 minutes). At least 75% returned results. Audit files exist in `/tmp/`. Proceed only when gate passes.

### Phase 6: REPORT

**Goal**: Produce the final, reality-grounded report with recommendations verified by Phase 5 audit.

Read audit findings, adjust recommendations (ALREADY EXISTS → move to "Already Covered"; PARTIAL → focus on gaps; MISSING → keep), overwrite `research-[REPO_NAME]-comparison.md` with the final report, and remove temporary `/tmp/` files.

See `references/phase6-report-template.md` for the full 4-step workflow and final report markdown template.

**Gate**: Final report saved to `research-[REPO_NAME]-comparison.md`. Report contains comparison table, adjusted recommendations based on audit findings, and verdict. No "DRAFT" watermark remains. All recommendations have been reality-checked against Phase 5 audit findings (or marked as unaudited if --quick was used). Proceed only when gate passes.

---

## Error Handling

See `references/error-handling.md` for clone failures, large repos (10k+ files), agent timeouts, no-gaps-found outcome, and self-inventory failures.

---

## References

- `references/phase2-agent-template.md` — Phase 2 DEEP-READ agent template
- `references/phase3-inventory-template.md` — Phase 3 INVENTORY agent template
- `references/phase5-audit-template.md` — Phase 5 AUDIT agent template
- `references/phase6-report-template.md` — Phase 6 REPORT workflow and final template
- `references/error-handling.md` — Pipeline error handling
