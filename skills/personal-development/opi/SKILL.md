---
name: opi
description: |
  Extract learnings from recent git commits and current conversation. Analyzes fixes,
  refactors, and corrections to propose entries for learnings files.

  Use when:
  - User says "/opi" or "opi"
  - "What did we learn?"
  - "Extract learnings"
  - "Update learnings"
  - End of session reflection

  Triggers: "opi", "learn", "oppia", "mitä opittiin", "extract learnings"
---

# Opi - Learning Extractor

Automatically extract learnings from recent work to improve future Claude sessions.

## Workflow

### Step 1: Gather Sources

Run these commands to collect learning material:

```bash
# Recent commits (last 20)
git log --oneline -20

# Today's commits with details
git log --since="midnight" --format="%h %s"

# Commits with "fix", "korjaus", "refactor"
git log --oneline -50 | grep -iE "(fix|korja|refactor|bugfix)"
```

### Step 2: Analyze Fix Commits

For each fix/refactor commit, examine what changed:

```bash
git show <commit-hash> --stat
git show <commit-hash> -- "*.tsx" "*.ts"  # Code changes
```

Look for patterns:
- **What was wrong?** (the bug/issue)
- **What fixed it?** (the solution)
- **Why?** (root cause)

### Step 3: Check Current Conversation

Review current conversation for:
- User corrections ("ei, tee näin..." / "no, do it this way...")
- Failed attempts that were fixed
- Non-obvious solutions discovered
- Repeated patterns

### Step 4: Categorize Learnings

Determine where each learning belongs:

| Learning Type | Destination |
|--------------|-------------|
| React/TypeScript pattern | `.claude/LEARNINGS.md` |
| Supabase/DB pattern | `.claude/LEARNINGS.md` |
| CI/CD specific | `ci-doctor/references/learnings.md` |
| Lint specific | `lint-fixer/references/learnings.md` |
| Test specific | `test-writer/references/learnings.md` |
| Skill-specific | `[skill]/references/learnings.md` |

### Step 5: Propose Learnings

Format each learning proposal:

```markdown
## Proposed Learning

**Source:** commit abc123 / conversation
**Category:** [Global / Skill-specific]
**File:** [target file path]

### [Issue Title]
- **Pattern:** What triggers this
- **Wrong:** ❌ The incorrect approach
- **Right:** ✅ The correct approach
- **Why:** Root cause
```

### Step 6: Get Approval & Write

1. Present all proposed learnings to user
2. User approves/rejects each
3. Write approved learnings to appropriate files
4. Commit changes

## Learning Quality Criteria

Only propose learnings that are:

- [ ] **Non-obvious** - Claude wouldn't know this without being told
- [ ] **Actionable** - Can be applied in future situations
- [ ] **Specific** - Has concrete wrong/right examples
- [ ] **Recurring** - Likely to come up again

Skip:
- Typo fixes
- One-off configuration issues
- Project-specific constants
- Things Claude already knows

## Example Session

```
User: /opi

Claude: Let me analyze recent commits...

Found 3 potential learnings:

1. **useCallback for useEffect deps** (commit a1b2c3)
   - Source: AdminTranslationsPage infinite loop fix
   - File: .claude/LEARNINGS.md
   - Pattern: Functions in useEffect deps cause re-renders

2. **GitHub API dismiss format** (commit d4e5f6)
   - Source: CodeQL alert dismissal
   - File: ci-doctor/references/learnings.md
   - Pattern: Use "false positive" not "false_positive"

3. **Controlled Tabs state** (conversation)
   - Source: Feedback popup tab fix
   - File: .claude/LEARNINGS.md
   - Pattern: Radix Tabs need value+onValueChange for control

Add these learnings? [Y/n for each]
```

## Commands Reference

```bash
# Commits since specific date
git log --since="2025-01-10" --oneline

# Commits by pattern
git log --all --oneline | grep -i "fix"

# Show specific commit
git show <hash> --name-only

# Diff for a commit
git diff <hash>^..<hash>
```
