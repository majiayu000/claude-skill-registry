---
name: writing-design-documents
description: Use when adapting requirements to system-specific design during Phase 2 - interactive whiteboard workflow, design decisions with rationale, and MVP-filtered architecture evaluation
---

# Writing Design Documents

Adapt generic requirements to your specific system through interactive research, decision-making, and documented design.

**Announce at start:** "I'm using the writing-design-documents skill to create the design."

## When to Use

Use this skill when:
- **Heavy bridge:** Greenfield features, system integration, API design — many architectural decisions needed
- **Medium bridge:** Brownfield enhancement, platform migration — some decisions needed

**Do NOT use** for:
- **Light bridge:** Ports, refactors — use `writing-spec-documents` directly (design absorbed into spec)
- **Thin bridge:** Bug fixes, deprecation — use `writing-spec-documents` only
- Phase 1 discovery/requirements (use `writing-requirements-documents`)
- Phase 4 implementation planning (use `writing-plans`)

### Bridge Weight Quick Reference

| Weight | Scenarios | This Skill |
|--------|-----------|------------|
| Heavy | Greenfield, integration, API design | **Required** |
| Medium | Brownfield, migration | Recommended |
| Light | Port, refactor | Skip (use spec) |
| Thin | Bug fix, deprecation | Skip (use spec) |

## Inputs

Before starting, ensure you have:

1. **PRD with FRs** — requirements document from Phase 1 (block-anchored FRs)
2. **Phase 1 Whiteboard** — discovery context (optional but useful)
3. **Source system research** — if porting/adapting existing code (read actual code, not just docs)

## Interactive Workflow

Design is interactive. You research, present findings, and ask the user to decide. The whiteboard captures everything.

### Step 1: Research Baseline

**Read actual code and config, not just documentation.**

- Read source system files (if porting) — verify assumptions against real code
- Read target system files — understand existing conventions, patterns, infrastructure
- Build verified component inventories (file, lines, language, dependencies)

**Key principle:** Documentation lies. Code doesn't. When source docs say "imports utils.js" but the code uses stdlib only — trust the code.

### Step 2: Build Whiteboard Interactively

Present findings incrementally and ask decisions at each point:

1. Present source baseline → user confirms/corrects
2. Present target baseline → user confirms/corrects
3. For each design decision:
   - Present the problem (gap between source and target)
   - Present 2-3 options with your recommendation
   - Use `AskUserQuestion` with recommended option first
   - Capture choice + rationale in whiteboard

**The whiteboard IS the gap analysis AND solutions hypothesis.** Do NOT create separate `gap-analysis.md` or `solutions-hypothesis.md` files — they add overhead without value.

### Step 3: Capture Design Decisions

Each decision in the whiteboard follows this format:

```markdown
### Decision N: [Short Title]

**Choice:** [What was decided]
**Rationale:** [Why this over alternatives]
**Impact:** [What changes as a result]
**Future:** [If MVP deferral, what comes later]
```

**Ask questions only about genuinely open items** — don't re-ask things already decided in Phase 1/PRD.

### Step 4: Architecture Evaluation

After whiteboard is complete:

1. **REQUIRED:** Run `evaluate-against-architecture-principles` skill on the design
2. **REQUIRED:** Filter findings through MVP lens (see Findings Prioritization below)
3. Present filtered findings to user
4. Incorporate "Fix now" items into design

### Step 5: Write Formal Design Document

Transform whiteboard into structured design doc (see Design Document Structure below).

## Whiteboard Structure

Save to: `{{feature-dir}}/2-design-phase/phase2-design-whiteboard.md`

```markdown
# Phase 2 Design Whiteboard — [Feature Name]

**Feature**: [name]
**Phase**: 2 (Research & Design)
**Date**: [date]
**Status**: Active

---

## Baseline: Source System
### Component Inventory (Verified)
[Table: Component | File | Lines | Language | Dependencies]
### Key Architecture Insight
[Core design pattern of source system]

---

## Baseline: Target System
### [System Name] Infrastructure (Actual)
[Verified inventory of target conventions, patterns, infrastructure]

---

## Design Decisions
### Decision 1: [Title]
**Choice:** ...
**Rationale:** ...
[repeat for each decision]

---

## Component Architecture (Target)
[Directory tree showing new + modified files]

---

## Risk Assessment
[Table: Risk | Severity | Mitigation]

---

## Resolved Open Items
[Numbered list of items resolved during design]

---

## References
- **PRD**: [PRD](../path-to-prd.md)
- **Phase 1 Whiteboard**: [Phase 1 Whiteboard](../1-elicit-discover-sense-make-problem-frame/whiteboard-phase1.md)
```

## Phase 2 Artifacts (Bridge-Dependent)

What you produce depends on bridge weight:

| Bridge | Whiteboard | Design Doc | Spec Doc |
|--------|------------|------------|----------|
| Heavy/Medium | Required | Required | Required |
| Light/Thin | Required | Skip | Required |

### Whiteboard (Always)
- **Purpose:** Decision anchor — immutable history of choices made
- **Stability:** Append-only — never modify past decisions
- **Contains:** Research findings, decisions with rationale, draft ACs

### Design Doc (Heavy/Medium only)
- **Purpose:** WHY rationale — documents decision history formally
- **Stability:** Stable — survives spec changes
- **When to create:** Greenfield, integration, API design — many architectural decisions
- **When to skip:** Ports, refactors — whiteboard + spec sufficient

### Spec Doc (Always — use `writing-spec-documents` skill)
- **Purpose:** Current HOW — concrete implementation instructions
- **Stability:** Living — evolves during sequencing/implementation
- **Contains:** Component specs, interfaces, data schemas, port instructions
- **Traceability:** References whiteboard decisions via anchors

**Relationship:** Whiteboard anchors decisions. Design doc formalizes rationale (when needed). Spec doc prescribes implementation.

## Draft AC Validation

Phase 1 whiteboards may contain draft ACs (`^AC-draft-N`). Phase 2 must validate ALL of them.

### Process

1. List every draft AC from Phase 1 whiteboard
2. Review each against design decisions made in Phase 2
3. Mark status: ✅ Validated | ⚠️ Revised | ❌ Dropped
4. Document revision rationale inline

### Format in Whiteboard

```markdown
## Draft AC Validation

**Observation Capture (FR1):**

- AC-draft-1: ✅ Validated
- AC-draft-2: ✅ Validated
- AC-draft-3: ⚠️ REVISED — capture ALL tools (not filtered list) per Decision 2
- AC-draft-4: ✅ Validated

**Performance (NFR1):**

- AC-draft-25: ✅ Validated — jq rewrite supports <100ms target
```

**Why:** Draft ACs inform sequencing. Unvalidated ACs create downstream confusion.

## Design Document Structure

Save to: `{{feature-dir}}/{{feature-name}}-design.md` (feature root, NOT nested in `2-design-phase/`)

```markdown
# Design Document — [Feature Name]

**Feature**: [name]
**Phase**: 2 (Research & Design)
**Date**: [date]
**Status**: Draft
**Inputs**: [PRD](../{{feature-name}}-prd.md), [Phase 2 Whiteboard](./2-design-phase/phase2-design-whiteboard.md)

---

## Design Overview
[Numbered list of adaptations — what's being built/changed]

---

## Component Design
### N. [Component Name] — [Short Description]
**Design Decision:** [Decision N: Title](./2-design-phase/phase2-design-whiteboard.md#decision-n-title)
**Location:** [file path]
**Language:** [language]
**Behavior:**
[Numbered steps of what the component does]
**Key adaptations from source:** [if porting]
[Repeat for each component]

---

## Integration Points
[What changes in the existing system — settings, config, gitignore, etc.]

---

## Interface Contracts
[Table: From | To | Channel | Format]

---

## Data Flows
### Flow N: [Name]
[ASCII flow diagram]
**Satisfies:** [FRN](../{{feature-name}}-prd.md#frn)
[Repeat for each major data flow]

---

## File Inventory
### New Files
[Table: File | Type | Lines (est) | Port From]
### Modified Files
[Table: File | Change]

---

## References
- **PRD**: [PRD](../{{feature-name}}-prd.md)
- **Phase 2 Whiteboard**: [Whiteboard](./2-design-phase/phase2-design-whiteboard.md)
```

## Findings Prioritization (MVP Lens)

After running `evaluate-against-architecture-principles`, filter findings:

1. **Cross-reference** each finding against the design's own risk assessment
2. **Apply MVP lens:** Is this blocking the system from working, or is it hardening?
3. **Categorize:**
   - **Fix now** — Violates core functionality, blocks MVP, or creates data loss risk
   - **Fix post-MVP** — Improves robustness, adds polish, or prevents theoretical issues
4. **Present filtered list** to user, not raw evaluation output

## Output Locations

| Artifact | Location | Notes |
|----------|----------|-------|
| Phase 2 Whiteboard | `{{feature-dir}}/2-design-phase/phase2-design-whiteboard.md` | Stays in phase folder |
| Design Document | `{{feature-dir}}/{{feature-name}}-design.md` | Feature root (not nested) |
| Pruned files | Delete separate gap-analysis.md, solutions-hypothesis.md if created | Whiteboard replaces these |

## Mandatory Validation Checklist

After writing design documentation, create TodoWrite todos for:

1. [ ] Verify all design decisions have Choice + Rationale + Impact
2. [ ] Verify component design sections have Location + Language + Behavior
3. [ ] Verify data flows trace to PRD FRs using markdown links
4. [ ] Verify file inventory lists ALL new and modified files
5. [ ] Run `evaluate-against-architecture-principles` on design doc
6. [ ] Filter architecture findings through MVP lens
7. [ ] Run `citation-manager validate <design-doc-path>`
8. [ ] Fix any broken links reported by citation-manager
9. [ ] Re-run validation until zero errors

**You MUST run both architecture evaluation and citation-manager validate.** Non-negotiable.

## Common Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|----------------|-----|
| Creating separate gap-analysis.md | Whiteboard captures gaps interactively | Use whiteboard sections |
| Creating separate solutions-hypothesis.md | Whiteboard captures hypotheses with decisions | Use whiteboard decisions |
| Researching docs instead of code | Documentation can be stale or wrong | Read actual source files |
| Re-asking Phase 1 decisions | Wastes user time on settled questions | Only ask genuinely open items |
| Skipping architecture evaluation | Design may violate principles | Always run before finalizing |
| Presenting raw evaluation output | Overwhelms with non-actionable items | Filter through MVP lens first |
| Nesting design doc in 2-design-phase/ | Design doc is a feature-level artifact | Save to feature root |
| Design decisions without rationale | Can't understand "why" later | Always document Choice + Rationale |
| Using tables for linkable items | Obsidian `^anchor` doesn't work on table rows | Use bullet lists with anchors for items needing traceability |

## Red Flags

- Tables containing items that need to be linked (use bullet lists with `^anchor` instead)
- Creating more than 2 artifacts (whiteboard + design doc)
- Design decisions without documented rationale
- Component designs without file locations
- Data flows that don't trace to FRs
- Skipping source code research (reading only docs)
- Asking the user about things already decided in Phase 1
- Presenting unfiltered architecture evaluation findings
- "I'll validate links later"

## Integration with Other Skills

**Inputs from:**
- `writing-requirements-documents` — PRD with FRs (Phase 1 output)

**Used during:**
- `evaluate-against-architecture-principles` — validate design, then filter through MVP lens

**Outputs to:**
- `writing-spec-documents` — whiteboard decisions feed spec traceability
- `writing-plans` — design doc + spec feed Phase 4 implementation planning

**Referenced by:**
- `enforcing-development-workflow` — Phase 2 skill (Heavy/Medium bridge)

**Alternative for Light/Thin bridge:**
- Skip this skill, use `writing-spec-documents` directly with whiteboard

---

**Remember:** The whiteboard is your working document. Build it interactively with the user. The design doc is the formal output. Don't create extra files — the whiteboard replaces gap analysis and solutions hypothesis documents.
