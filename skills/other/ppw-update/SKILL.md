---
name: ppw:update
description: Sync local skills and references from the GitHub repo. Triggers on update skills, sync skills, 更新技能, 同步技能
triggers:
  primary_intent: download latest skills from GitHub and update local files
  examples:
    - "update skills"
    - "sync skills"
    - "更新技能"
    - "同步技能"
tools:
  - Read
  - Write
  - Bash
references:
  required: []
  leaf_hints: []
input_modes:
  - command
output_contract:
  - update_report
---

## Purpose

This Skill syncs local `.claude/skills/` and `references/` from the upstream GitHub repository [Lylll9436/Paper-Polish-Workflow-skill](https://github.com/Lylll9436/Paper-Polish-Workflow-skill). It downloads the latest SKILL.md files and reference documents, compares them with local versions, and updates any changed files.

## Trigger

**Activates when the user asks to:**
- Update or sync skills from the remote repo
- 更新或同步技能包

**Example invocations:**
- "update skills"
- "sync skills from GitHub"
- "更新技能"

## Modes

| Mode | Default | Behavior |
|------|---------|----------|
| `direct` | Yes | Fetch, compare, update, report — no intermediate confirmation |
| `interactive` | | Show diff summary before applying each update |

**Default mode:** `direct`

## Workflow

### Step 0: Workflow Memory Check

- Read `.planning/workflow-memory.json`. If file missing or empty, skip to Step 1.
- Check if the last 1-2 log entries form a recognized pattern with `ppw:update` that has appeared >= threshold times in the log. See `skill-conventions.md > Workflow Memory > Pattern Detection` for the full algorithm.
- If a pattern is found, present recommendation via AskUserQuestion:
  - Question: "检测到常用流程：[pattern]（已出现 N 次）。是否直接以 direct 模式运行 ppw:update？"
  - Options: "Yes, proceed" / "No, continue normally"
- If user accepts: set mode to `direct`, skip Ask Strategy questions.
- If user declines or AskUserQuestion unavailable: continue in normal mode.

### Step 1: Pre-flight Check

- Verify `gh` CLI is available and authenticated: `gh auth status`
- Verify the upstream repo is accessible: `gh api repos/Lylll9436/Paper-Polish-Workflow-skill --jq '.full_name'`
- If either check fails, report the error and stop.
- **Record workflow:** Append `{"skill": "ppw:update", "ts": "<ISO timestamp>"}` to `.planning/workflow-memory.json`. Create file as `[]` if missing. Drop oldest entry if log length >= 50.

### Step 2: Fetch Remote File Index

- List all skill directories from the remote repo:
  ```bash
  gh api repos/Lylll9436/Paper-Polish-Workflow-skill/contents/.claude/skills --jq '.[].name'
  ```
- List all reference files from the remote repo:
  ```bash
  gh api repos/Lylll9436/Paper-Polish-Workflow-skill/contents/references --jq '.[] | .name + " " + .type'
  ```
- For reference subdirectories (type=dir), also list their contents recursively.

### Step 3: Compare and Update Skills

For each remote skill directory:

1. Fetch the remote `SKILL.md` content:
   ```bash
   gh api repos/Lylll9436/Paper-Polish-Workflow-skill/contents/.claude/skills/{skill-name}/SKILL.md --jq '.content' | base64 -d
   ```
2. Read the local `.claude/skills/{skill-name}/SKILL.md` if it exists.
3. Compare the two:
   - If local file does not exist → **NEW** skill, create directory and write file.
   - If content differs → **UPDATED**, overwrite local file.
   - If content is identical → **UNCHANGED**, skip.
4. Track results for the final report.

**In `interactive` mode:** Before applying each update, show a summary of changes and ask for confirmation.

### Step 4: Compare and Update References

For each remote reference file:

1. Fetch the remote file content via `gh api` with base64 decode.
2. Read the local `references/{filename}` if it exists.
3. Compare and apply the same NEW/UPDATED/UNCHANGED logic as Step 3.
4. For subdirectories (e.g., `references/journals/`, `references/expression-patterns/`), recurse into each file.

### Step 5: Output Report

Present a summary table:

```
## Skills Update Report

| Skill | Status |
|-------|--------|
| polish-skill | ✓ Updated |
| de-ai-skill | - Unchanged |
| new-skill | + New |

## References Update Report

| File | Status |
|------|--------|
| expression-patterns.md | ✓ Updated |
| skill-conventions.md | - Unchanged |

**Summary:** {updated_count} updated, {new_count} new, {unchanged_count} unchanged
```

## Output Contract

| Output | Format | Condition |
|--------|--------|-----------|
| Update report | Markdown table | Always produced |
| File count summary | Text | Always reported |

## Edge Cases

| Situation | Handling |
|-----------|----------|
| `gh` CLI not installed or not authenticated | Report error, suggest `gh auth login` |
| Remote repo not accessible | Report network/permission error |
| Local skill has modifications not in remote | Overwrite with remote (remote is source of truth) |
| New skill in remote not present locally | Create directory and write SKILL.md |
| Remote skill deleted but exists locally | Keep local (do not delete; report as "local-only") |
| Reference subdirectory doesn't exist locally | Create it |

## Fallbacks

| Scenario | Fallback |
|----------|----------|
| `gh api` rate limited | Wait and retry once, then report error |
| Base64 decode fails | Try `gh api` with `Accept: application/vnd.github.raw` header |
| Single file fetch fails | Skip file, continue with remaining, report in summary |

---

*Conventions: [references/skill-conventions.md](../../references/skill-conventions.md)*
