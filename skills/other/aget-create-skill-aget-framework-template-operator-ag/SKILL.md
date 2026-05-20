---
name: aget-create-skill
description: Create new AGET skills following S-V-O naming and standard templates. Use when developing new /aget-* skills with proper vocabulary, specs, and traceability.
disable-model-invocation: true
---

# /aget-create-skill

Create a new AGET skill following the standard development process per SOP_SKILL_DEVELOPMENT.md.

## Input

$ARGUMENTS

## Mode Detection

| Input Pattern | Mode | Behavior |
|---------------|------|----------|
| Empty or blank | **Interactive** | Prompt for skill name |
| `<skill-name>` | **Explicit** | Create skill with provided name |

## Skill Creation Process

### Step 1: Name Validation

Validate the skill name follows S-V-O convention:

| Pattern | Valid | Examples |
|---------|-------|----------|
| `/aget-<verb>-<object>` | ✓ Default | `/aget-create-skill`, `/aget-check-health` |
| `/aget-<verb>` | ✓ Intransitive | `/aget-learn`, `/aget-checkpoint` |
| `/aget-<phrasal-verb>` | ✓ Exception | `/aget-wake-up`, `/aget-wind-down` |
| Other patterns | ✗ Invalid | `/aget-skill-create` (O-V not S-V-O) |

**Check for existing skill**:
```bash
ls .claude/skills/ | grep -q "<name>"
```

If skill exists, STOP and report conflict.

### Step 2: Determine Skill Number

Check `specs/skills/INDEX.md` for next available SKILL-XXX number.

Current registry:
- SKILL-001 through SKILL-005: Existing
- SKILL-006: Reserved for /aget-create-project
- SKILL-007: This skill (/aget-create-skill)
- SKILL-008+: Available

### Step 3: Create Skill Specification

Create `specs/skills/SKILL-XXX_<name>.md` with:

1. Purpose section
2. Requirements (R-SKILL-XXX-001, etc.) in EARS format
3. Test cases
4. Traceability section

### Step 4: Create SKILL.md

1. Create directory: `.claude/skills/<name>/`
2. Copy structure from `templates/skill/SKILL.template.md`
3. Fill in required fields:

**Required frontmatter**:
```yaml
---
name: <name>
description: <one-line description>
---
```

**For skills with side effects** (file writes, git operations):
```yaml
disable-model-invocation: true
```

**Instruction format** (per L561 - Instruction Asymmetry):
- Use PROHIBITIVE form: "NEVER", "SHALL NOT", "DO NOT"
- Avoid affirmative form (~0% compliance)

### Step 5: Update Index

Add entry to `specs/skills/INDEX.md`:

```markdown
| SKILL-XXX | [<name>](SKILL-XXX_<name>.md) | ACTIVE | <primary finding> |
```

### Step 6: Report

Output summary of created artifacts:
- Skill spec location
- SKILL.md location
- Index update status

## Output Format

```markdown
## Skill Created: /aget-<name>

**Artifacts**:
- Spec: specs/skills/SKILL-XXX_<name>.md
- Implementation: .claude/skills/<name>/SKILL.md
- Index: specs/skills/INDEX.md (updated)

**Next Steps**:
1. Test skill invocation: `/aget-<name>`
2. Verify behavior matches spec
3. Create L-doc if significant learnings
```

## Constraints

These are INVIOLABLE - you MUST NOT violate these constraints:

1. **NEVER** create a skill with non-S-V-O name without documented exception
2. **NEVER** overwrite an existing skill without explicit confirmation
3. **NEVER** create SKILL.md without valid frontmatter (name, description)
4. **NEVER** use affirmative constraints - use prohibitive form per L561
5. **DO** check for existing skills before creating
6. **DO** use templates/skill/SKILL.template.md as base
7. **DO** include Traceability section in SKILL.md
8. **DO** update specs/skills/INDEX.md after creation

## Rationale

Per AGET theoretical grounding:
- **Stigmergy** (Grasse): Skill artifacts enable cross-session coordination
- **Extended Mind** (Clark/Chalmers): Templates and SOPs extend agent skill-creation capability
- **Evidence-First Design** (L289): Specs before implementation
- **Instruction Asymmetry** (L561): Prohibitive instructions for governance

This skill implements the "template-driven skill creation" pattern per SOP_SKILL_DEVELOPMENT.md.

## Traceability

| Link | Reference |
|------|-----------|
| Vocabulary | Agent_Skill, AGET_Skill, Tool (CLI_VOCABULARY.md v1.32.0) |
| Requirements | R-SKILL-001 through R-SKILL-006 (CLI_SUBSYSTEM_SPEC.md v1.11.0) |
| Skill Spec | SKILL-007 |
| SOP | SOP_SKILL_DEVELOPMENT.md |
| Template | templates/skill/SKILL.template.md |
| L-docs | L474, L557, L561, L582, L583 |
| Project | PROJECT_PLAN_AGET_CREATE_SKILL.md |
