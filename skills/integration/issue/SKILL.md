---
name: issue
description: Create and update GitHub issues. Triggers on "create issue", "file issue", "open issue", "new issue", "report bug", "request feature", "track this", "create epic", "create theme", "update issue", "check off", "mark complete", "close issue". Infers type, labels, and milestone from conversation context.
allowed-tools: Bash(gh:*), AskUserQuestion, Grep, Read
user-invocable: true
---

# Issue Skill

Create, update, and manage GitHub issues following ZeroAE conventions. Infer as much as possible from context; only ask when ambiguous.

## Modes

This skill operates in three modes based on context:

| Mode | Trigger Phrases | Action |
|------|-----------------|--------|
| **Create** | "create issue", "file issue", "new issue", "report bug", "request feature" | Create new issue |
| **Update** | "update issue", "add to issue", "update #123" | Modify existing issue body/metadata |
| **Progress** | "check off", "mark complete", "done with", "finished" | Check checkboxes in issue body |

## Supported Issue Types

| Type | Emoji | GitHub Type | Use For |
|------|-------|-------------|---------|
| Bug | 🐛 | Bug | Defects, unexpected behavior |
| Feature | ✨ | Feature | New functionality, enhancements |
| Task | 📋 | Task | Documentation, testing, specific work items |
| Chore | 🔧 | Chore | Maintenance: refactor, deps, ci, cleanup |
| Epic | 🎯 | Epic | Major feature spanning multiple issues |
| Theme | 🎨 | Theme | Strategic initiative spanning epics |

> **Note:** For release preparation, use `/pr release <version>` to create a Release Prep PR.

## Context Inference

Before asking questions, analyze the conversation to infer:

### Type Inference (Create mode)

| Context Clues | Inferred Type |
|---------------|---------------|
| "bug", "broken", "error", "fix", "crash", "fails", "doesn't work" | Bug 🐛 |
| "add", "new", "feature", "implement", "support", "enable" | Feature ✨ |
| "docs", "documentation", "readme", "write docs" | Task 📋 |
| "test", "coverage", "add tests" | Task 📋 |
| "refactor", "cleanup", "upgrade", "deps", "ci", "chore" | Chore 🔧 |
| "epic", "major feature", "multi-issue", "spanning" | Epic 🎯 |
| "theme", "strategic", "initiative", "long-term" | Theme 🎨 |

> **Tip:** If user mentions "release", "cut release", or "release prep", redirect to `/pr release <version>`.

### Issue Number Inference (Update/Progress modes)

Detect issue references from context:
- Explicit: "#123", "issue 123", "issue #123"
- From branch name: `git branch --show-current` → extract issue number
- From recent commits: `git log -1 --format=%s` → look for "Closes #N"
- From conversation: recently discussed issue numbers

### Checkbox Inference (Progress mode)

Match completed work to checkboxes:
- Compare conversation context (commits, code changes, test results) against checkbox text
- If work clearly addresses a criterion, mark it complete
- If ambiguous, ask user to confirm

### Label Inference

Infer `area/` labels from context:
- Files mentioned → extract component (e.g., `src/cli.py` → `area/cli`)
- Topics discussed → map to area (e.g., "deployment" → `area/infra`)
- Available areas: `area/limiter`, `area/cli`, `area/infra`, `area/aggregator`, `area/ci`

### Milestone Inference

Query milestones and match by theme:
```bash
gh api repos/{owner}/{repo}/milestones --jq '.[] | "\(.title): \(.description)"'
```

---

## Create Mode

### Process

1. **Gather Context**: Analyze conversation for problem, solution, files discussed
2. **Infer or Ask**: Use inference first, batch questions if multiple fields ambiguous
3. **Build Issue Body**: Use template from [templates.md](templates.md)
4. **Confirm and Create**: Show preview, then create

```bash
gh issue create \
  --title "<emoji> <Title>" \
  --body "$(cat <<'EOF'
<body from template>
EOF
)" \
  --label "<area/label>" \
  --milestone "<milestone>"
```

5. **Set Issue Type**:
```bash
gh api -X PATCH repos/{owner}/{repo}/issues/<number> -f type=<Type>
```

---

## Update Mode

Update an existing issue's body or metadata.

### Process

1. **Identify Issue**: Infer issue number from context or ask
2. **Fetch Current State**:
```bash
gh issue view <number> --json title,body,labels,milestone
```
3. **Determine Changes**: From conversation, identify what to add/modify
4. **Preview Changes**: Show diff of what will change
5. **Apply Update**:

**Update body:**
```bash
gh issue edit <number> --body "$(cat <<'EOF'
<updated body>
EOF
)"
```

**Update metadata:**
```bash
gh issue edit <number> --add-label "<label>" --milestone "<milestone>"
```

**Update title:**
```bash
gh issue edit <number> --title "<new title>"
```

---

## Progress Mode

Check off completed checkboxes in issue body based on work done.

### Process

1. **Identify Issue**: Infer from branch, commits, or conversation
2. **Fetch Issue Body**:
```bash
gh issue view <number> --json body --jq '.body'
```
3. **Parse Checkboxes**: Find all `- [ ]` items
4. **Match to Context**: Compare each checkbox against:
   - Recent commits (`git log --oneline -10`)
   - Files changed (`git diff --name-only origin/main`)
   - Test results mentioned in conversation
   - Explicit user statements ("I finished X")
5. **Preview Changes**: Show which boxes will be checked
```
Checking off in issue #123:
- [x] Add unit tests for caching  ← matches commit "test: add caching tests"
- [x] Update documentation        ← matches changed docs/guide/caching.md
- [ ] Performance benchmarks      ← no matching work found

Proceed? [Y/n]
```
6. **Update Issue Body**: Replace `- [ ]` with `- [x]` for completed items
```bash
gh issue edit <number> --body "$(cat <<'EOF'
<body with checked boxes>
EOF
)"
```

### Checkbox Matching Rules

| Evidence | Checkbox Text | Match? |
|----------|---------------|--------|
| Commit "test: add unit tests" | "Add unit tests" | ✅ Yes |
| Changed `docs/guide/*.md` | "Update documentation" | ✅ Yes |
| User says "benchmarks done" | "Performance benchmarks" | ✅ Yes |
| No related commits/files | Any checkbox | ❌ No (ask) |

---

## Output

- **Create**: Return the new issue URL
- **Update**: Return the updated issue URL with summary of changes
- **Progress**: Return issue URL with list of checkboxes marked complete

## Reference Files

- [templates.md](templates.md) - Issue body templates for each type
- [conventions.md](conventions.md) - Label taxonomy, title formatting, milestone rules
