---
name: check-docs
description: Check if recent changes need documentation updates and suggest which docs to update.
---

# Check Documentation Updates

Analyzes recent git commits to determine if documentation needs updating.

## When to Use

- After completing a feature/refactor
- Before creating a PR
- When user asks "should I update docs?"
- Periodically during long sessions

## How It Works

1. **Analyze Recent Commits**
   - Get commits since specified SHA or last N commits
   - Extract changed files in `backend/app/` and `frontend/src/`
   - Categorize change size (small/medium/large)

2. **Map Files to Documentation**
   - `backend/app/api/` → `docs/content/{en,uk}/api/`
   - `backend/app/models/` → `docs/content/{en,uk}/architecture/models.md`
   - `backend/app/services/` → `docs/content/{en,uk}/architecture/backend-services.md`
   - `backend/app/agents/` → `docs/content/{en,uk}/architecture/agent-system.md`
   - `backend/app/tasks/` → `docs/content/{en,uk}/architecture/background-tasks.md`
   - `frontend/src/` → `docs/content/{en,uk}/frontend/architecture.md`

3. **Categorize Change Size**
   - **Small**: ≤2 files, no feat/refactor commits
   - **Medium**: 3-5 files OR refactor commits
   - **Large**: 6+ files OR feat commits OR breaking changes

4. **Generate Report**
   - List affected areas (API routes, models, services, agents, pages, features, components)
   - Suggest documentation files to review/update
   - Mark missing docs with ⚠️
   - Provide `/docs` command hint for missing files

## Usage

**Default (last 5 commits):**
```
Use the check-docs skill
```

**Specific range:**
```
Use the check-docs skill to check commits since abc123
```

**Check last N commits:**
```
Use the check-docs skill to check last 10 commits
```

## Output Format

```
📚 Documentation Update Check

Analyzed: 3 commits, 7 files changed

Change size: medium (based on 5 files, 1 refactor commit)

Backend changes (4 files):
  - API routes (2 files)
  - Database models (2 files)

Frontend changes (3 files):
  - Pages (1 file)
  - Components (2 files)

Suggested documentation to review/update:
  ✅ docs/content/{en,uk}/api/knowledge.md
  ✅ docs/content/{en,uk}/architecture/models.md
  ⚠️ MISSING docs/content/{en,uk}/frontend/components.md

💡 Use /docs to create missing documentation
```

## Implementation Notes

- Use `git log` and `git diff` for analysis
- Don't trigger on doc-only commits
- Check if suggested docs exist (mark missing ones)
- Keep it simple - just analysis and suggestions, no automatic updates

## Integration with /docs Command

After running this skill, user can use `/docs` command to update specific files:

```
/docs docs/content/en/architecture/models.md
```

Or let /docs figure out the path:

```
/docs update models documentation
```
