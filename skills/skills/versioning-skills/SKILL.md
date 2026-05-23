---
name: versioning-skills
description: REQUIRED for all skill development. Automatically version control every skill file modification for rollback/comparison. Use after init_skill.sh, after every str_replace/create_file, and before packaging.
metadata:
  version: 1.1.0
---

# Versioning Skills

Use git to track changes during skill development. Initialize repos after creating skills, commit after each logical change, and use git commands to compare versions or revert mistakes.

## When Creating a New Skill

After running init_skill.sh, immediately initialize git:

```bash
cd /home/claude/skill-name
git init
git add .
git commit -m "Initial commit: skill structure"
```

## When Editing Skills

After each logical change (adding a section, fixing an example, refactoring), commit:

```bash
cd /home/claude/skill-name
git add .
git commit -m "Add: validation workflow pattern"
```

**Commit message patterns:**
- `"Add [feature]: description"` - New functionality
- `"Fix [issue]: description"` - Bug fixes  
- `"Update [section]: description"` - Content changes
- `"Refactor [component]: description"` - Structural changes
- `"Remove [feature]: description"` - Deletions

## When User Asks "What Changed?"

**CRITICAL: Never display diffs inline - redirect to files and provide links.**

**ALSO CRITICAL: Only create diffs/changelogs when user explicitly asks "what changed?" or "show differences"**

**Don't preemptively create:**
- CHANGELOG.md files
- Change documentation
- "Here's what I modified" summaries

**Why:** The updated code/docs ARE the documentation. Creating separate changelogs wastes tokens and duplicates information.

**When user asks, show commit history:**

```bash
cd /home/claude/skill-name
git log --oneline
```

Save diff to file (prevents token waste):

```bash
cd /home/claude/skill-name
git diff <commit-hash-1> <commit-hash-2> > /mnt/user-data/outputs/changes.diff
```

Then provide: `[View changes](computer:///mnt/user-data/outputs/changes.diff)`

For multiple diffs:

```bash
# Changed files list
git diff --name-only <commit-1> <commit-2> > /mnt/user-data/outputs/changed-files.txt

# Full diff
git diff <commit-1> <commit-2> > /mnt/user-data/outputs/full-diff.diff

# Summary stats
git diff --stat <commit-1> <commit-2> > /mnt/user-data/outputs/diff-stats.txt
```

**Wrong:** `git diff <commit-1> <commit-2>` (displays in stdout, wastes tokens)
**Right:** `git diff <commit-1> <commit-2> > /mnt/user-data/outputs/diff.txt` (file + link)

## Reverting Commits or Discarding Work

**Undo last commit (keep uncommitted changes):**
```bash
cd /home/claude/skill-name
git reset --soft HEAD~1
```

**Undo last commit (discard all changes):**
```bash
git reset --hard HEAD~1
```

**Revert specific commit (creates new commit, preserves history):**
```bash
git revert <commit-hash>
```

**Discard uncommitted edits (restore to last commit):**
```bash
git restore .
```

Prefer `git revert` over `git reset --hard` to preserve history.

## When Testing Experimental Changes

Create a branch before risky modifications:

```bash
cd /home/claude/skill-name

# Create and switch to experiment branch
git checkout -b experiment-new-approach

# Make changes, test
# ... edit files ...
git add .
git commit -m "Experiment: alternative validation"

# If successful, merge back
git checkout main
git merge experiment-new-approach
git branch -d experiment-new-approach

# If failed, abandon and return to main
git checkout main
git branch -D experiment-new-approach
```

## When Comparing Two Skill Versions

If user uploads or provides two versions:

```bash
cd /home/claude
mkdir -p compare

# Extract both versions
unzip /mnt/user-data/uploads/skill-v1.zip -d compare/v1
unzip /mnt/user-data/uploads/skill-v2.zip -d compare/v2

# Initialize git in each
cd compare/v1 && git init && git add . && git commit -m "Version 1"
cd ../v2 && git init && git add . && git commit -m "Version 2"

# Compare
cd ../v1
git diff --no-index . ../v2
```

Or use diff directly without git:

```bash
diff -ur compare/v1 compare/v2
```

## When Packaging Skills

Before zipping, verify clean state:

```bash
cd /home/claude/skill-name
git status  # Should show no uncommitted changes
git log --oneline  # Review history

# Package (excludes .git automatically with -x)
cd /home/claude
zip -r /mnt/user-data/outputs/skill-name.zip skill-name/ -x "*.git*"
```

## Workflow Integration

**During skill creation:**
1. Run init_skill.sh
2. Immediately: `git init && git add . && git commit -m "Initial structure"`
3. Edit SKILL.md
4. Commit: `git add . && git commit -m "Add: core documentation"`
5. Continue editing → commit after each major change

**During skill editing:**
1. Make change with str_replace or bash
2. Test if needed
3. Commit: `git add <file> && git commit -m "Fix: corrected example"`
4. Repeat

**Before delivery:**
1. Review history: `git log --oneline`
2. Verify clean: `git status`
3. Package with -x to exclude .git

## Configuration

Set git identity once per session to avoid prompts:

```bash
git config --global user.name "Claude"
git config --global user.email "skill-dev@claude.ai"
```

## Common Issues

**"not a git repository"**
→ Run `git init` first

**"nothing to commit"**  
→ No changes made, or forgot `git add`

**Commit message editor opens**
→ Always use `-m "message"` with commit

## Best Practices

Commit after each logical change, not every keystroke. Use descriptive commit messages in present tense. Create branches for experimental changes. Use `git log --oneline` frequently to track progress.

## Limitations

Git repos in /home/claude reset between sessions. Version control only persists within a single development session. Network restrictions prevent push/pull to remote repos.
