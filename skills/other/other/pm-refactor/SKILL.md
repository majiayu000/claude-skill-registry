---
name: pm-refactor
description: Restructure the PM knowledge system itself — split overcrowded registers, merge thin ones, rename decisions for clarity, reorganize the decisions/ folder structure. System-level maintenance for vault architecture. Requires human approval for all structural changes. Triggers on "/pm-refactor", "reorganize vault", "split register", "restructure decisions", "vault refactor".
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
context: fork
---

## Runtime Configuration (Step 0)

Read `ops/derivation-manifest.md` for vocabulary and folder conventions.
Read `ops/config.yaml` for register size thresholds.

---

## EXECUTE NOW

**Target: $ARGUMENTS**

Parse immediately:
- If empty: audit all registers for structural issues and propose changes
- If "split [register]": propose split for named register
- If "merge [register-a] [register-b]": propose merge of two thin registers
- If "rename [decision]": propose title improvement for named decision
- If "reorganize": full structural reorganization proposal

**START NOW.**

---

## Philosophy

**The PM system must be able to refactor itself. Rigidity is a brittleness, not a virtue.**

A decisions/ folder that made sense at 20 decisions may not make sense at 80. A register that covered "all testing decisions" may need to split into "QFTest automation" and "API testing" when QFTest-specific decisions proliferate. A decision title that made sense when created may become misleading after the domain evolved.

/pm-refactor is the system-level restructuring operation. It is not about individual decisions — it is about the architecture of the knowledge system. Registers, folder structure, naming conventions, the hub MOC — all of these can be refactored.

The critical constraint: /pm-refactor NEVER auto-applies structural changes. Every change is proposed and requires explicit human approval, because structural changes affect how future decisions are created and how existing decisions are navigated. A bad structural refactor can make the vault harder to use, not easier.

---

## Structural Issue Detection

### Register Size

```bash
# Count decisions in each register
for f in decisions/*-register.md; do
  count=$(rg "\[\[" "$f" 2>/dev/null | wc -l)
  echo "$(basename $f): $count"
done
```

- >35 decisions: propose split
- <3 decisions: propose merge with adjacent register

### Naming Inconsistency

```bash
# Find decisions where title doesn't follow claim format
rg "^# " decisions/ --include="*.md" -h | grep -v "because\|requires\|must\|should\|is\|was\|needs\|has\|are\|will" | head -20
```

Decisions with noun-phrase titles instead of claim-form titles should be renamed.

### Orphan Registers

```bash
# Find registers with few incoming links
for f in decisions/*-register.md; do
  name=$(basename "$f" .md)
  refs=$(rg "\[\[$name\]\]" decisions/ --include="*.md" | wc -l)
  echo "$name: $refs refs"
done
```

### Structural Gaps

Are there types of decisions that don't have a register? Check the decision type distribution:

```bash
rg "^type:" decisions/ --include="*.md" -h | sort | uniq -c
```

If tech-facts are numerous but there's no tech-facts-specific register, that's a structural gap.

---

## Proposal Format

```
## Refactor Proposal: [what to change]

### Current State
[What exists now and why it's suboptimal]

### Proposed Change
[Specific change: split register X into Y and Z, rename decision A to B, etc.]

### Impact
- Files affected: N
- Links to update: N
- Registers to update: N

### Implementation Steps
1. [Step 1 — specific file operation]
2. [Step 2 — specific file operation]
3. [Update hub MOC]
4. [Update affected decision links]

### Risk
[What could go wrong if this refactor is done incorrectly]

APPROVE? (yes/modify/reject)
```

---

## Implementation (After Approval)

For register splits:
1. Create the two new register files using templates/decision-register.md
2. Distribute existing decisions across the new registers
3. Update all decision notes' `topics` field to reference the new register
4. Update decisions/index.md to reflect new registers
5. Archive or redirect the old register

For decision renames:
1. Create new file with new name
2. Copy content from old file, update title
3. Update all wiki-links pointing to old file
4. Delete old file

For merges:
1. Identify the surviving register (usually the one with more decisions)
2. Move all decisions from smaller register to larger
3. Update topics fields
4. Archive smaller register
5. Update hub MOC

---

## Hard Constraints

- NEVER apply structural changes without explicit human approval
- NEVER delete decision notes — only archive or rename
- NEVER break wiki-links — all renames require link updates
- Update decisions/index.md after any structural change
- Run /pm-audit after completing any refactor to verify structural integrity
