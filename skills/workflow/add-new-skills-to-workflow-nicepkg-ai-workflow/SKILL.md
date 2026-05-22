---
name: add-new-skills-to-workflow
description: Add new skills to an existing workflow and update all related documentation. Use when user wants to add skills from GitHub URLs to a workflow (e.g., "add this skill to the workflow", "为工作流添加技能"). Triggers on adding skills to workflows, updating workflow documentation after skill additions.
---

# Add New Skills to Workflow

Add skills from GitHub to an existing workflow and update all related documentation.

## Workflow

### Step 1: Download Skills

Use skill-downloader to download skills from GitHub:

```bash
python .claude/skills/skill-downloader/scripts/download_from_github.py <repo-url> <skill-path> --output <workflow-path>/.claude/skills/
```

**Parse GitHub URL:**
- `https://github.com/user/repo/blob/main/path/to/skill` → repo: `https://github.com/user/repo`, skill-path: `path/to/skill`
- `https://github.com/user/repo/tree/main/.claude/skills/my-skill` → repo: `https://github.com/user/repo`, skill-path: `.claude/skills/my-skill`

**Example:**
```bash
# For URL: https://github.com/XIYO/zheon/blob/main/.claude/skills/slidev
python .claude/skills/skill-downloader/scripts/download_from_github.py https://github.com/XIYO/zheon .claude/skills/slidev --output ./workflows/talk-to-slidev-workflow/.claude/skills/

# Use --force to overwrite existing
python .claude/skills/skill-downloader/scripts/download_from_github.py <repo> <path> --output <target> --force
```

### Step 2: Read Downloaded Skill

Read the downloaded `SKILL.md` to understand:
- Skill name and description
- What category it belongs to
- How it fits into the workflow pipeline

### Step 3: Update skill-source.json

Add the new skill entry to `workflows/<name>/.claude/skill-source.json`:

```json
{
  "skill-name": {
    "source": "https://github.com/user/repo",
    "path": "path/to/skill"
  }
}
```

### Step 4: Update Documentation

Update these files (all that exist for the workflow):

| File | Updates Required |
|------|------------------|
| `workflows/<name>/.claude/skill-source.json` | Add new skill source entry |
| `workflows/<name>/README.md` | Skill count, skill table, pipeline |
| `workflows/<name>/README_cn.md` | Same as above (Chinese) |
| `workflows/<name>/AGENTS.md` | Available skills list, recommended sequences |
| `website/content/en/workflows/<name>.mdx` | Skill count, skill table, pipeline |
| `website/content/zh/workflows/<name>.mdx` | Same as above (Chinese) |
| `README.md` (root) | Skill count in workflow table |
| `README_cn.md` (root) | Same as above (Chinese) |

### Documentation Update Checklist

1. **Skill Count**: Update total count (e.g., "18 skills" → "20 skills")
   - Quick install comment
   - Section header
   - Description text

2. **Skill Table**: Add new skill row in appropriate category
   ```markdown
   | `skill-name` | Brief description of what it does |
   ```

3. **Pipeline**: Add skill to relevant stage if applicable
   ```
   Stage X: Category
   ├── existing-skill → Description
   └── new-skill → Description
   ```

4. **AGENTS.md**: Add to available skills and update recommended sequences

5. **Root README**: Update skill count in workflow overview table

## Example: Adding Skills to talk-to-slidev-workflow

**Given:** Add `slidev` and `slidev-presentations` skills

**Step 1:** Download
```bash
python .claude/skills/skill-downloader/scripts/download_from_github.py https://github.com/XIYO/zheon .claude/skills/slidev --output ./workflows/talk-to-slidev-workflow/.claude/skills/
python .claude/skills/skill-downloader/scripts/download_from_github.py https://github.com/clearfunction/cf-devtools skills/slidev-presentations --output ./workflows/talk-to-slidev-workflow/.claude/skills/
```

**Step 2:** Read downloaded skills to understand their purpose

**Step 3:** Update skill-source.json with new skill entries

**Step 4:** Update all 8 files:
- Update skill-source.json with source info
- Update skill count
- Add new category with skill table
- Update pipeline to reference new skills
- Update AGENTS.md skill lists and sequences
- Update root README skill count
