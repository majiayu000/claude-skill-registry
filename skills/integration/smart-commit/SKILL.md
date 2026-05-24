---
name: smart-commit
description: This skill should be used when user asks to commit changes to git repository. Triggers on Ukrainian/English phrases like "закоміть зміни", "commit changes", "створи коміт", "зроби коміт", or any request to create git commits. Creates atomic commits with semantic file grouping using conventional commit format.
---

# Smart Commit

**CRITICAL: Always use SubTask for file analysis to keep main context clean. NOT MAIN AGENT!**

## Overview

Intelligently analyze git changes by delegating file reading and diff analysis to subtasks using the Task tool, detect semantic relationships between changes, and create atomic commits that are independently functional.

Only ask for clarification when explicitly requested by the user.

## Workflow

### 1. Get List of Changed Files

Run git commands to see what changed:

```bash
git status
git diff --name-only
git ls-files --others --exclude-standard
```

### 2. Analyze Changes Using Task Tool

**CRITICAL: You MUST use the Task tool with subagent_type=General Purpose to analyze files in parallel subtasks.**

For each changed file, launch a subtask using:

```
SubTask tool with:
- subagent_type: "General Purpose"
- description: "Analyze file diff"
- prompt: "Analyze git diff for [filename]. Extract:
  1. Changed symbols (functions, classes, components, types)
  2. Change type (feat, fix, refactor, test, docs)
  3. Related files (imports, tests)
  Return compact JSON: {symbols: [...], type: '...', related: [...]}"
```

Launch ALL file analysis tasks in PARALLEL (single message with multiple Task calls).

After all subtasks complete, collect results and group files by:
- **Shared symbols**: Files changing same functions/classes = one group
- **Test + Implementation**: Tests with code they test = one group
- **Logical area**: Fallback to directory-based grouping (first 2 path levels)

### 3. Security Check

**NEVER commit sensitive files:**
- `.env` files (except `.env.example`)
- `credentials.json`, `*.key`, `*.pem`
- Files with "secrets" or "private" in name

Flag these as "⚠️ SENSITIVE FILES - DO NOT COMMIT"

### 4. Group Files Intelligently

Based on subtask analysis results, group files:

1. **Find shared symbols**: If files A and B both change function `extractKnowledge` = same group
2. **Match tests with code**: `test_extractor.py` + `extractor.py` = same group
3. **Merge related areas**: All `.artifacts/` together, all `.claude/skills/` together, all `.zip` together
4. **Keep atomic**: Each group must be independently committable

### 5. Create Logical Commits

For each group of files (excluding sensitive):

1. **Stage the group**: git add [files from group]
2. **Check diff**: git diff --cached to understand changes
3. **Create commit message**:
   - Format: {type}({scope}): {description}
   - **Types**: feat, fix, refactor, perf, style, docs, test, chore, ci, revert
   - **Scopes**: backend, frontend, bot, worker, nginx, db, docker, deps, config, ci
   - Description: Clear, concise summary (50 chars max)
   - **Breaking changes**: Add ! after scope, example: feat(api)!: redesign auth
   - **NO** "Generated with Claude" footer
   - **NO** Co-Authored-By lines

4. **Commit**: git commit -m "message"

### 6. Beads Integration (Multi-level Refs)

If working on a Beads issue, add `Refs:` footer with full hierarchy:

```bash
# Check if in Beads context
bd show PR-XX --json 2>/dev/null
```

**Get issue hierarchy:**
```bash
# For task PR-7 with parent Story PR-2 and Epic PR-1:
bd show PR-7 --json | jq -r '.parent_id // empty'
# Returns: PR-2

bd show PR-2 --json | jq -r '.parent_id // empty'
# Returns: PR-1
```

**Add Refs footer:**
```
feat(backend): implement knowledge extraction

Refs: PR-7, PR-2, PR-1
```

- First ref = current task
- Next refs = parent hierarchy (story, epic)
- Only add if Beads issue exists and is relevant to changes
- Skip if no active Beads context

**Commit format with refs:**
```bash
git commit -m "$(cat <<'EOF'
feat(backend): implement knowledge extraction

Refs: PR-7, PR-2, PR-1
EOF
)"
```

### 7. Behavior

**Default (no user clarification requested):**
- Automatically group and commit without asking
- Use conventional commit format
- Create separate commits per logical group

**When user requests clarification:**
- Show proposed groups and commit messages
- Ask for approval before committing
- Allow user to adjust grouping

### 8. Intelligent Grouping Strategy

**Semantic relationships** (not hardcoded paths):

1. **Test + Implementation**: Tests grouped with code they test (shared symbols)
2. **Related symbols**: Files changing same functions/classes/components
3. **Logical area**: Fallback grouping by directory context (first 2 levels)
4. **Sensitive files**: Always detected and flagged separately

**Detection methods**:
- Diff analysis to extract changed symbols (functions, classes, exports)
- Keyword detection (fix, feat, refactor, perf, etc.) from changes
- File type semantics (test files, docs, config)
- Import/type relationship tracking

## Example

**User request**: "commit changes"

**Skill workflow**:
1. Get changed files list (git commands)
2. Launch subtasks to analyze diffs for each file
3. Collect symbol/keyword analysis from subtasks
4. Group intelligently:
   - Group 1: `backend/services/extractor.py` + `backend/tests/test_extractor.py` (shared symbols)
   - Group 2: `frontend/components/TopicSelector.tsx` + `frontend/types/topic.ts` (related changes)
   - Group 3: All `.artifacts/` files (same category)
   - Group 4: All `.claude/skills/` files (skills together)
   - Group 5: `docs/architecture/knowledge.md` (standalone docs)
5. Create 5 atomic commits without asking
6. Done

**User request**: "commit changes, ask me first"

**Skill workflow**:
1. Analyze as above using subtasks
2. Show proposed groups and commit messages
3. Wait for user approval
4. Create commits

## Notes

- **Keep commits atomic** - each group should be independently reviewable
- **No footers** - only commit header line
- **Follow existing commit style** - check `git log` for project patterns
- **Don't ask by default** - only when user explicitly requests clarification