---
name: remove-old-skills-from-workflow
description: Guide for removing skills from an existing workflow and updating all related documentation. Use when user wants to remove skills from a workflow (e.g., "remove skill", "delete skill", "移除技能", "删除技能").
---

# Remove Skills from Workflow

Guide for removing skills from an existing workflow and updating all related documentation.

## When to Use

- User wants to remove a skill from a workflow
- User says "remove skill", "delete skill", "移除技能", "删除技能"
- Cleaning up unused or deprecated skills from a workflow

## Removal Workflow

### Step 1: Identify the Skill

Search for the skill name across the workflow to understand its usage:

```bash
# Find all references to the skill
grep -r "skill-name" /path/to/workflow/
```

### Step 2: Delete Skill Folder

Remove the skill directory from the workflow:

```bash
rm -rf /path/to/workflow/.claude/skills/skill-name/
```

### Step 3: Update skill-source.json (if exists)

Remove the skill entry from `/path/to/workflow/.claude/skill-source.json`

### Step 4: Update All Related Documentation

After removing a skill, you MUST update these files:

#### Files to Update (7 files)

| File | What to Update |
|------|----------------|
| `workflows/<workflow-name>/README.md` | Skill count, skill table, pipeline stages, skill combinations |
| `workflows/<workflow-name>/README_cn.md` | Same as above (Chinese version) |
| `workflows/<workflow-name>/AGENTS.md` | Available skills list, recommended sequences |
| `website/content/en/workflows/<workflow>.mdx` | Skill count, skill table, pipeline, skill combinations |
| `website/content/zh/workflows/<workflow>.mdx` | Same as above (Chinese version) |
| `README.md` (root) | Workflow table skill count |
| `README_cn.md` (root) | Workflow table skill count (Chinese version) |

#### Documentation Update Checklist

For each documentation file, update:

- [ ] **Skill count**: Decrease the total skill count (e.g., "20 skills" → "19 skills")
- [ ] **Skill tables**: Remove the skill row from any skill listing tables
- [ ] **Pipeline/stages**: Remove skill references from pipeline diagrams or stage descriptions
- [ ] **Skill combinations**: Remove any skill chains that include the removed skill
- [ ] **Example workflows**: Remove or update examples that reference the skill

## Example

Removing `ppt-creator` skill from `talk-to-slidev-workflow`:

```bash
# 1. Search for references
grep -r "ppt-creator" workflows/talk-to-slidev-workflow/

# 2. Delete skill folder
rm -rf workflows/talk-to-slidev-workflow/.claude/skills/ppt-creator/

# 3. Update skill-source.json
# Remove the ppt-creator entry

# 4. Update documentation files
# - Update skill count from 20 to 19
# - Remove ppt-creator from skill tables
# - Remove from pipeline Stage 6
# - Remove from skill combinations table
```

## Important Notes

- Always search for skill references before removal to understand impact
- The root READMEs only need skill count updates in the workflow table
- Leave `references/skill-sources.md` unchanged (it documents ecosystem skills, not workflow-specific installations)
- If the skill is referenced in example workflows, either remove the example or update it to use alternative skills
