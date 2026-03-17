---
name: aget-propose-skill
description: Enable structured proposal of new skills before implementation. Follows 'propose -> review -> approve -> implement' governance pattern. Advisory enforcement.
version: 1.0.0
---

# /aget-propose-skill

Create a structured skill proposal before implementation. Follows governance pattern: propose → review → approve → implement.

## Purpose

Prevent unreviewed skill proliferation. Forces deliberate consideration of skill purpose, triggers, and design before investing in implementation.

## Input

$ARGUMENTS - Skill name or idea description

## Execution

### Step 1: Gather Information

Collect from user:
1. **Skill name** (must follow `aget-{verb}-{object}` pattern)
2. **Purpose** - What problem does this skill solve?
3. **Triggers** - What user actions/phrases should invoke it? (minimum 2)
4. **Category** - Governance, Creation, Monitoring, Learning, Planning, Fleet Ops?
5. **Scope** - Universal (all agents) or Agent-specific?

### Step 2: Validate Constraints

**C1: Name Format**
```
Pattern: aget-{verb}-{object}
Valid:   aget-healthcheck-evolution, aget-record-lesson
Invalid: healthcheck-evolution, aget_record_lesson, myskill
```

**C2: Uniqueness**
```bash
# Check if skill already exists
test -d .claude/skills/$SKILL_NAME && echo "EXISTS" || echo "OK"
```

**C3: Minimum Triggers**
```
Triggers provided >= 2
```

If any constraint fails, report error and stop.

### Step 3: Create Proposal

Create file at `planning/skill-proposals/PROPOSAL_{name}.md`:

```markdown
# Skill Proposal: {name}

**Date**: {YYYY-MM-DD}
**Author**: {agent}
**Status**: PROPOSED

---

## Summary

**Name**: {name}
**Category**: {category}
**Scope**: {Universal/Agent-specific}

## Purpose

{What problem does this solve?}

## Triggers

When user says:
- "{trigger 1}"
- "{trigger 2}"
- ...

## Design Notes

{Initial design considerations}

## Dependencies

{Other skills or resources needed}

## Approval

- [ ] Principal reviewed
- [ ] Design approved
- [ ] Ready for implementation

---

*Use `/aget-create-skill {name}` to implement after approval.*
```

### Step 4: Update Index (if exists)

If `planning/skill-proposals/INDEX.md` exists, add entry.

### Step 5: Report

```
Proposal created: planning/skill-proposals/PROPOSAL_{name}.md

Next steps:
1. Review proposal with principal
2. Get approval
3. Run /aget-create-skill {name} to implement
```

## Constraints

- **C1**: Name MUST follow `aget-{verb}-{object}` pattern
- **C2**: Skill MUST NOT already exist
- **C3**: MUST have at least 2 triggers
- **C4**: Advisory enforcement - no technical blocking if bypassed

## Enforcement Model

From supervisor inquiry (RQ-C):
> "Nothing prevents it technically... Compliance is voluntary + supervised."

This skill creates a proposal artifact. If an agent bypasses it and creates skills directly:
- No runtime block occurs
- Supervisor may detect via `/aget-fleet-scan` or healthchecks
- Intervention follows supervision patterns (critique + teaching)

## Related Skills

- `/aget-create-skill` - Implement approved proposals
- `/aget-create-project` - Create project plans

## Traceability

| Link | Reference |
|------|-----------|
| POC | POC-017 |
| Project | PROJECT_PLAN_AGET_UNIVERSAL_SKILLS.md |
| Source | Fleet Skill Deployment Report (supervisor) |
| Pattern | Propose → Review → Approve → Implement |

---

*aget-propose-skill v1.0.0*
*Category: Governance*
*POC-017 Phase 3*
