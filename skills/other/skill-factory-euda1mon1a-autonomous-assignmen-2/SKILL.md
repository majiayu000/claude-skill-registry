---
name: skill-factory
description: Create new skills with proper structure and YAML frontmatter. Use when building new slash command skills, ensuring consistent formatting, directory structure, and validation. Guides through the complete skill creation workflow.
model_tier: sonnet
parallel_hints:
  can_parallel_with: [agent-factory]
  must_serialize_with: []
  preferred_batch_size: 1
context_hints:
  max_file_context: 40
  compression_level: 1
  requires_git_context: true
  requires_db_context: false
escalation_triggers:
  - pattern: "security|auth|credential"
    reason: "Security-affecting skills require human approval"
  - pattern: "duplicate|conflict"
    reason: "Functionality conflicts need human resolution"
  - keyword: ["critical system", "agent permissions"]
    reason: "System-level changes require review"
---

# Skill Factory

> **Purpose:** Guide users through creating new Claude Code skills with proper structure
> **Created:** 2025-12-27
> **Trigger:** `/skill-factory` command

---

## When to Use

- Creating a new slash command skill
- Need to ensure proper YAML frontmatter format
- Want consistent skill structure across the project
- Building skills for agents or workflows
- Validating existing skill files

---

## Required Actions

When this skill is invoked, Claude MUST:

1. **Gather skill requirements** from the user:
   - Skill name (kebab-case, e.g., `my-new-skill`)
   - One-line description (for slash command discovery)
   - Purpose and use cases
   - Whether it needs Reference/ or Workflows/ subdirectories

2. **Validate the skill name**:
   - Must be kebab-case
   - Must not conflict with existing skills
   - Must be descriptive and discoverable

3. **Create the directory structure**:
   ```
   .claude/skills/<skill-name>/
   ├── SKILL.md           # Required: Main skill file
   ├── Reference/         # Optional: Reference documentation
   └── Workflows/         # Optional: Workflow definitions
   ```

4. **Generate SKILL.md** using the template below

5. **Validate the created skill**:
   - YAML frontmatter is valid
   - Required sections are present
   - Examples are included

---

## Skill Template

Use this template for all new skills:

```markdown
---
name: <skill-name>
description: <one-line description for slash command discovery>
---

# <Skill Title>

> **Purpose:** <what this skill does>
> **Created:** <date>
> **Trigger:** `/<skill-name>` command

---

## When to Use

<bullet list of scenarios when this skill should be used>

---

## Required Actions

When this skill is invoked, Claude MUST:

1. <action 1>
2. <action 2>
3. <action 3>

---

## Examples

<usage examples showing how the skill works>

---

## Escalation Rules

**Escalate to human when:**

<list of situations requiring human intervention>

**Can handle automatically:**

<list of situations the skill can handle independently>

---

## Related

- <related skills>
- <related documentation>
```

---

## Validation Checklist

Before completing skill creation, verify:

- [ ] **YAML Frontmatter Valid**
  - `name:` matches directory name (kebab-case)
  - `description:` is one line, under 200 characters
  - No trailing spaces or invalid YAML syntax

- [ ] **Required Sections Present**
  - Title with Purpose/Created/Trigger metadata
  - "When to Use" section with bullet points
  - "Required Actions" section with numbered steps
  - "Examples" section with concrete usage

- [ ] **Quality Standards**
  - Description is discoverable (keywords users would search)
  - Actions are specific and actionable
  - Examples demonstrate real use cases
  - Escalation rules define boundaries

- [ ] **No Conflicts**
  - Skill name doesn't duplicate existing skill
  - Functionality doesn't overlap significantly with existing skills

- [ ] **Directory Structure Correct**
  - `.claude/skills/<skill-name>/SKILL.md` exists
  - Optional subdirectories created if needed

---

## Examples

### Example 1: Create a Simple Skill

**User:** Create a skill for generating changelogs

**Claude:**
1. Gathers requirements: name=`changelog-generator`, purpose=generate changelogs from git history
2. Creates directory: `.claude/skills/changelog-generator/`
3. Generates SKILL.md with proper frontmatter
4. Validates all checklist items pass

### Example 2: Create a Skill with Reference Docs

**User:** Create a skill for ACGME compliance with reference documentation

**Claude:**
1. Gathers requirements including reference materials needed
2. Creates structure:
   ```
   .claude/skills/acgme-compliance/
   ├── SKILL.md
   └── Reference/
       ├── hour-limits.md
       └── supervision-ratios.md
   ```
3. Populates reference files as needed

### Example 3: Check Existing Skill

**User:** Validate the test-writer skill

**Claude:**
1. Reads `.claude/skills/test-writer/SKILL.md`
2. Validates YAML frontmatter
3. Checks all required sections present
4. Reports any issues found

---

## Escalation Rules

**Escalate to human when:**

1. Skill affects security (auth, credentials, secrets)
2. Skill duplicates existing functionality significantly
3. Skill requires new agent permissions
4. Unclear whether skill or agent is appropriate
5. Skill would modify critical system files

**Can handle automatically:**

1. Creating standard skill structure
2. Generating SKILL.md from template
3. Validating existing skills
4. Creating Reference/ and Workflows/ subdirectories
5. Checking for naming conflicts

---

## Integration with TOOLSMITH Agent

This skill implements part of the TOOLSMITH agent's "Create New Skill" workflow:

1. TOOLSMITH receives skill creation request
2. Invokes `/skill-factory` to generate structure
3. Validates output meets quality standards
4. Reports completion to ORCHESTRATOR

For agent creation, use the `/agent-factory` skill instead.

---

## Related

- `.claude/Agents/TOOLSMITH.md` - Agent specification for tool creation
- `.claude/skills/` - Directory containing all project skills
- `docs/development/AGENT_SKILLS.md` - Agent skills reference
- `CLAUDE.md` - Project guidelines and standards
