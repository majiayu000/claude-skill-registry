---
name: create-skill
description: Create and validate skills. USE WHEN create skill, new skill, skill structure, canonicalize. SkillSearch('create-skill') for docs.
user-invocable: false
---

## Customization

**Before executing, check for user customizations at:**
`~/.claude/skills/CORE/user/skill_customizations/create-skill/`

If this directory exists, load and apply any PREFERENCES.md, configurations, or resources found there. These override default behavior. If the directory does not exist, proceed with skill defaults.

# create-skill

MANDATORY skill creation system for ALL skill creation requests.

## Authoritative Source

**Before creating ANY skill, READ:** `SKILL_LOGIC.md`

**Canonical example to follow:** `~/.claude/skills/blogging/SKILL.md`

## Naming Conventions (MANDATORY)

**Skill naming follows PAL's standard file naming conventions for consistency across the system.**

| Category            | Convention            | Example                 | Purpose                                  |
| :------------------ | :-------------------- | :---------------------- | :--------------------------------------- |
| **Skill directory** | `lower-kebab-case`    | `create-skill/`         | Standard IDE navigation.                 |
| **SKILL.md**        | `UPPER_SNAKE_CASE.md` | `SKILL.md`              | System protocol file (always uppercase). |
| **Workflow files**  | `lower_snake_case.md` | `create_skill.md`       | Active work files within skill.          |
| **Reference docs**  | `lower_snake_case.md` | `prosody_guide.md`      | Active work files within skill.          |
| **Tool files**      | `lower_snake_case.ts` | `manage_server.ts`      | Active work files within skill.          |
| **Help files**      | `lower_snake_case.md` | `manage_server.help.md` | Active work files within skill.          |
| **YAML name**       | `lower-kebab-case`    | `name: create-skill`    | Matches directory name for consistency.  |

**Convention Rules:**

- **Skill directories:** Use `lower-kebab-case` for standard IDE navigation
- **SKILL.md:** Always uppercase (system protocol convention)
- **All other files:** Use `lower_snake_case` (active work convention)
- **YAML name field:** Matches directory name in `lower-kebab-case`

---

## Flat Folder Structure (MANDATORY)

**CRITICAL: Keep folder structure FLAT - maximum 2 levels deep.**

### The Rule

**Maximum depth:** `skills/skill-name/category/`

### ALLOWED (2 levels max)

```
skills/skill-name/SKILL.md                    # Skill root
skills/skill-name/workflows/create.md         # Workflow - one level deep - GOOD
skills/skill-name/tools/manage.ts             # Tool - one level deep - GOOD
skills/skill-name/quick_start_guide.md       # Context file - in root - GOOD
skills/skill-name/examples.md                 # Context file - in root - GOOD
```

### FORBIDDEN (Too deep OR wrong location)

```
skills/skill-name/resources/guide.md              # Context files go in root, NOT resources/
skills/skill-name/docs/examples.md                # Context files go in root, NOT docs/
skills/skill-name/workflows/category/file.md      # THREE levels - NO
skills/skill-name/templates/primitives/file.md    # THREE levels - NO
skills/skill-name/tools/utils/helper.ts           # THREE levels - NO
```

### Allowed Subdirectories

**ONLY these subdirectories are allowed:**

- **workflows/** - Execution workflows ONLY
- **tools/** - Executable scripts/tools ONLY

**Context files (documentation, guides, references) go in the skill ROOT, NOT in subdirectories.**

### Why

1. **Discoverability** - Easy to find files
2. **Simplicity** - Less navigation overhead
3. **Speed** - Faster file operations
4. **Consistency** - Every skill follows same pattern

**If you need to organize many workflows, use clear filenames instead of subdirectories:**

- Good: `workflows/company_due_diligence.md`
- Bad: `workflows/company/due_diligence.md`

---

## Dynamic Loading Pattern (Large Skills)

**For skills with SKILL.md > 100 lines:** Use dynamic loading to reduce context on skill invocation.

### How Loading Works

**Session startup:** Only frontmatter loads for routing
**Skill invocation:** Full SKILL.md loads
**Context files:** Load only when workflows reference them

### The Pattern

**SKILL.md** = Minimal (30-50 lines) - loads on skill invocation

- YAML frontmatter with triggers
- Brief description
- Workflow routing table
- Quick reference
- Pointers to context files

**Additional .md files** = Context files - SOPs for specific aspects (loaded on-demand)

- These are Standard Operating Procedures, not just documentation
- They provide specific handling instructions
- Can reference workflows/, tools/, etc.

### CRITICAL: NO Context/ Subdirectory

**NEVER create context/ or docs/ subdirectories.**

Additional .md files ARE the context files. They live **directly in skill root**.

**WRONG:**

```
skills/art/
  SKILL.md
  context/              # NEVER CREATE THIS
    aesthetic.md
```

**CORRECT:**

```
skills/art/
  SKILL.md
  aesthetic.md          # Context file in skill root
  examples.md           # Context file in skill root
  tools.md              # Context file in skill root
```

**The skill directory IS the context.**

### Example Structure

```
skills/art/
  SKILL.md              # 40 lines - minimal routing
  aesthetic.md          # Context file - SOP for aesthetic
  examples.md           # Context file - SOP for examples
  tools.md              # Context file - SOP for tools
  workflows/            # Workflows
    essay.md
  tools/                # CLI tools
    generate.ts
```

### Minimal SKILL.md Template

```markdown
---
name: skill-name
description: Brief. USE WHEN triggers.
---

# skill-name

Brief description.

## Workflow Routing

| Trigger   | Workflow                     |
| --------- | ---------------------------- |
| "trigger" | `workflows/workflow_name.md` |

## Quick Reference

**Key points** (3-5 bullet points)

**Full Documentation:**

- Detail 1: `SkillSearch('skill-name detail1')` -> loads detail1.md
- Detail 2: `SkillSearch('skill-name detail2')` -> loads detail2.md
```

### When To Use

**Use dynamic loading for:**

- SKILL.md > 100 lines
- Multiple documentation sections
- Extensive API reference
- Detailed examples

**Don't use for:**

- Simple skills (< 50 lines)
- Pure utility wrappers

---

## Workflow Routing

| Workflow               | Trigger                               | File                              |
| :--------------------- | :------------------------------------ | :-------------------------------- |
| **create_skill**       | "create a new skill"                  | `workflows/create_skill.md`       |
| **validate_skill**     | "validate skill", "check skill"       | `workflows/validate_skill.md`     |
| **update_skill**       | "update skill", "add workflow"        | `workflows/update_skill.md`       |
| **canonicalize_skill** | "canonicalize", "fix skill structure" | `workflows/canonicalize_skill.md` |

## Examples

**Example 1: Create a new skill from scratch**

```
User: "Create a skill for managing my recipes"
→ Invokes create_skill workflow
→ Reads SKILL_LOGIC.md for structure requirements
→ Creates skill directory with lower-kebab-case naming
→ Creates SKILL.md, workflows/, tools/
→ Generates USE WHEN triggers based on intent
```

**Example 2: Fix an existing skill that's not routing properly**

```
User: "The research skill isn't triggering - validate it"
→ Invokes validate_skill workflow
→ Checks SKILL.md against canonical format
→ Verifies lower-kebab-case naming for directory
→ Verifies USE WHEN triggers are intent-based
→ Reports compliance issues with fixes
```

**Example 3: Canonicalize a skill with old naming**

```
User: "Canonicalize the daemon skill"
→ Invokes canonicalize_skill workflow
→ Renames workflow files to lower_snake_case
→ Updates routing table to match
→ Ensures Examples section exists
→ Verifies all checklist items
```
