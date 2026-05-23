---
name: building-truth-base
description: Use when starting on a new product, joining a team, or needing a shared understanding of product, customers, and current bets.
---

# Building Truth Base

## Overview

Creates a Day-1 shared map of the product: what it is, who it serves, current roadmap themes, and top unknowns. This becomes the foundation for all other PM work.

## When to Use

- Starting a new PM role or joining a product team
- Need to establish baseline understanding
- Want to document what you've learned from onboarding
- Someone asks "what does this product actually do?"

## Core Pattern

**Step 1: Gather Context**

Follow protocol in `.claude/rules/pm-core/context-gathering.md`:
1. Detect available inputs in `inputs/roadmap_deck/`, `inputs/product_demo/`, `inputs/knowledge_base/`
2. Check for existing truth base in `outputs/truth_base/`
3. Present options to user via AskUserQuestion:
   - [List documents found: strategy decks, demos, KB articles]
   - [Show existing truth base if updating]
   - [Point me to another document]
   - [Describe the product you want me to document]
4. Read `.beads/insights.jsonl` for relevant product patterns
5. Proceed with selected context

**Step 2: Gather Available Sources**

Read all selected files in:
- `inputs/roadmap_deck/` - strategy slides, PDFs
- `inputs/product_demo/` - demo notes, walkthroughs
- `inputs/knowledge_base/` - KB articles about the product

If sources are missing, list what's needed and ask user to provide.

**Step 3: Extract Key Information**

From sources, identify:
1. What the product is (1 paragraph)
2. Who it serves (actors, personas, segments)
3. Core terminology (what do key terms mean in this context?)
4. Core workflows (user journeys, key flows)
5. Current roadmap themes (from deck)
6. Known constraints (tech debt, compliance, trust issues)

**Step 4: Identify Unknowns**

List 10-15 open questions you cannot answer from the sources. These become your investigation priorities.

**Step 5: Generate Output**

Write to `outputs/truth_base/truth-base.md` with metadata header:

```markdown
---
generated: YYYY-MM-DD HH:MM
skill: building-truth-base
sources:
  - inputs/roadmap_deck/strategy.pdf (modified: YYYY-MM-DD)
  - inputs/product_demo/demo-notes.md (modified: YYYY-MM-DD)
downstream:
  - outputs/roadmap/Qx-YYYY-charters.md
---

# Truth Base: [Product Name]

## What Is This Product?
[1 paragraph description]

## Who Does It Serve?
| Actor | Description | Key Jobs |
|-------|-------------|----------|
| ... | ... | ... |

## Core Terminology
| Term | Meaning (in this context) |
|------|---------------------------|
| ... | ... |

## Core Workflows
1. **[Workflow Name]:** [Brief description]
   - Trigger: ...
   - Steps: ...
   - Outcome: ...

## Current Roadmap Themes
| Theme | Description | Evidence |
|-------|-------------|----------|
| ... | ... | [source file] |

## Constraints & Risks
| Constraint | Impact | Source |
|------------|--------|--------|
| ... | ... | Evidence/Assumption |

## Top 15 Open Questions
1. [Question] — *Priority: High/Medium/Low*
2. ...

## Sources Used
- [file paths]

## Claims Ledger

| Claim | Status | Confidence | Source | Last Verified |
|-------|--------|------------|--------|---------------|
| ... | fact/assumption/hypothesis | high/med/low | [source:line] | YYYY-MM-DD |

### Status Definitions
| Status | Meaning | Action Required |
|--------|---------|-----------------|
| **fact** | Verified from authoritative source | None - treat as ground truth |
| **assumption** | Inferred, reasonable but unverified | Validate within 30 days |
| **hypothesis** | Speculative, needs testing | Must test before building on it |

### Confidence Criteria
| Level | Criteria |
|-------|----------|
| **high** | Multiple sources agree, recently verified, authoritative |
| **med** | Single source, somewhat dated, reasonable inference |
| **low** | Weak source, speculation, conflicting signals |
```

**Step 6: Copy to History**

Run `pm-os mirror --quiet` to copy to `history/building-truth-base/`

**Step 7: Update Staleness Tracker**

Update `nexa/state.json` and append to `outputs/audit/auto-run-log.md` with the new output and its sources.

**Step 8: Post-Skill Reflection**

Follow protocol in `.claude/rules/pm-core/post-skill-reflection.md`:
1. Extract 3-5 key learnings from building this truth base
2. Create learning entry in `history/learnings/YYYY-MM-DD-building-truth-base.md`
3. Create insight beads in `.beads/insights.jsonl`
4. Request output rating (1-5 or skip)
5. Detect and log any decisions made
6. Report capture completion to user

## Quick Reference

| Action | Location |
|--------|----------|
| Input sources | `inputs/roadmap_deck/`, `inputs/product_demo/`, `inputs/knowledge_base/` |
| Output | `outputs/truth_base/truth-base.md` |
| History | `history/building-truth-base/` |
| Downstream | Quarterly charters |

## Common Mistakes

- **Inventing product details:** Only claim what's in sources → Mark unknowns as Open Questions
- **Skipping terminology:** "Catalog" means different things → Define terms explicitly
- **Too few questions:** 3 questions isn't enough → Aim for 10-15 open questions
- **No sources cited:** "The product does X" → Always cite which file told you this

## Verification Checklist

- [ ] All source files read and listed
- [ ] Product description is 1 paragraph (not a page)
- [ ] Actors/personas table populated
- [ ] Terminology table has key domain terms
- [ ] At least 10 open questions identified
- [ ] Every claim has Evidence/Assumption tag
- [ ] Metadata header includes sources and timestamps
- [ ] Output copied to history folder
- [ ] Staleness tracker updated

## Goal-Backward Verification

**Before marking complete, run goal-backward check** (see `.claude/rules/pm-core/goal-backward-verification.md`):

**Goal:** New team member can understand product in 15 minutes.

**Observable truths (must all pass):**
- [ ] Someone unfamiliar can explain the product's value prop
- [ ] Open questions identify actual unknowns (not just padding)
- [ ] Terminology matches what the team actually uses
- [ ] Core workflows are actionable (trigger → steps → outcome)

**On failure:** Do not mark complete. Note which checks failed in Open Questions section.

## Evidence Tracking

| Claim | Status | Confidence | Source | Last Verified |
|-------|--------|------------|--------|---------------|
| [Product does X] | fact | high | inputs/roadmap_deck/strategy.pdf:12 | YYYY-MM-DD |
| [Users are Y segment] | assumption | med | inferred from KB articles | YYYY-MM-DD |
| [Integration with Z exists] | hypothesis | low | not stated in sources | - |
