---
name: research-merge
description: "Processes research branches from Claude Code Web sessions - merges content, moves docs to docs/research/, and creates GitHub issues. Use when /popkit:next detects research branches or when manually processing research from mobile sessions. Do NOT use for regular feature branches - only for branches matching claude/research-* or containing research documentation."
---

# Research Branch Merge

## Overview

Handles the complete workflow for processing research branches created during Claude Code Web sessions:

1. Detect research branches
2. Preview content for user approval
3. Squash-merge to main branch
4. Move docs to standardized location
5. Create GitHub issue from findings
6. Clean up remote branch

**Trigger:** Called by `pop-next-action` skill when research branches detected, or directly via `/popkit:research merge`.

## User Interaction Pattern

**ALWAYS use AskUserQuestion** for merge decisions:

```
Use AskUserQuestion tool with:
- question: "Found research branch: [topic]. How should we process it?"
- header: "Research"
- options:
  - label: "Merge and create issue"
    description: "Squash-merge, move docs, create GitHub issue, delete branch"
  - label: "Merge only"
    description: "Squash-merge content without creating issue"
  - label: "Skip for now"
    description: "Leave branch for later processing"
  - label: "Delete branch"
    description: "Discard research (cannot be undone)"
- multiSelect: false
```

## Processing Workflow

### Step 1: Detect Research Branches

Use the `research_branch_detector.py` utility:

```python
import sys
# No longer needed - install popkit-shared instead
from research_branch_detector import (
    fetch_remotes,
    get_research_branches,
    format_branch_table,
    get_branch_content_preview,
    parse_research_doc,
    generate_issue_body
)

# Fetch and detect
fetch_remotes()
branches = get_research_branches()

if not branches:
    print("No research branches detected.")
    return

# Show table
print("## Research Branches Detected\n")
print(format_branch_table(branches))
```

### Step 2: Preview Content

For each branch, show a preview before prompting:

```python
for branch in branches:
    print(f"\n### {branch.short_name}")
    print(f"**Topic:** {branch.topic}")
    print(f"**Created:** {branch.created_ago}")
    print(f"**Commits:** {branch.commit_count} ahead of master")

    if branch.doc_paths:
        print(f"\n**Documentation:**")
        for path in branch.doc_paths:
            print(f"- `{path}`")

        # Show summary preview
        previews = get_branch_content_preview(branch, max_lines=20)
        for path, content in previews.items():
            parsed = parse_research_doc(content)
            if parsed.get("summary"):
                print(f"\n**Summary:** {parsed['summary'][:200]}...")
```

### Step 3: User Decision

Use AskUserQuestion for each branch:

```
Use AskUserQuestion tool with:
- question: f"Process '{branch.topic}' research? ({branch.commit_count} commits, {len(branch.doc_paths)} docs)"
- header: "Merge"
- options:
  - label: "Merge + Issue"
    description: "Full processing: merge, organize docs, create issue"
  - label: "Merge Only"
    description: "Just merge the content"
  - label: "Skip"
    description: "Process later"
  - label: "Delete"
    description: "Discard this research"
- multiSelect: false
```

### Step 4: Execute Merge

**Branch Protection Check (Issue #142):**

Before merging, MUST check current branch:

```bash
# Get current branch
current_branch=$(git branch --show-current 2>/dev/null)

# Protected branches: main, master, develop, production
PROTECTED_BRANCHES=("main" "master" "develop" "production")

# Check if on protected branch
is_protected=false
for branch in "${PROTECTED_BRANCHES[@]}"; do
    if [ "$current_branch" = "$branch" ]; then
        is_protected=true
        break
    fi
done

# If on protected branch, BLOCK and recommend feature branch
if [ "$is_protected" = true ]; then
    echo "❌ ERROR: Cannot merge research directly into protected branch '$current_branch'"
    echo ""
    echo "Protected branch policy requires feature branch workflow."
    echo ""
    echo "Recommended steps:"
    echo "  1. Create feature branch:"
    echo "     git checkout -b feat/research-merge-[topic]"
    echo ""
    echo "  2. Re-run research merge (will merge into feature branch)"
    echo ""
    echo "  3. Push and create PR:"
    echo "     git push -u origin feat/research-merge-[topic]"
    echo "     gh pr create --title 'docs: merge [topic] research'"
    echo ""
    echo "See CLAUDE.md 'Git Workflow Principles' for details."
    exit 1
fi
```

**If on feature branch, proceed with merge:**

Based on user choice:

#### Option A: Merge + Issue (Full Processing)

```bash
# 1. Ensure clean working directory
git status --porcelain
# If dirty, prompt user to commit or stash first

# 2. Squash merge the research branch
git merge --squash origin/claude/research-[topic]-[session-id]

# 3. Organize docs (if not already in docs/research/)
mkdir -p docs/research
# Move any root-level research docs
git mv RESEARCH*.md docs/research/ 2>/dev/null || true
git mv *_RESEARCH.md docs/research/ 2>/dev/null || true

# 4. Commit with standard message
git commit -m "docs(research): merge [topic] research from web session

Merged from: [branch-name]
Created: [created-ago]

🤖 Generated with [Claude Code](https://claude.ai/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

# 5. Create GitHub issue
gh issue create --title "[Research] [Topic Title]" --body "[generated-body]" --label "research,documentation"

# 6. Delete remote branch
git push origin --delete claude/research-[topic]-[session-id]
```

#### Option B: Merge Only

```bash
git merge --squash origin/claude/research-[topic]-[session-id]
git commit -m "docs(research): merge [topic] research

Merged from: [branch-name]

🤖 Generated with [Claude Code](https://claude.ai/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

# Optionally delete branch
# Ask: "Delete the remote branch?"
```

#### Option C: Skip

No action - branch remains for future processing.

#### Option D: Delete

```bash
# Confirm deletion
# "Are you sure? This research will be permanently lost."

git push origin --delete claude/research-[topic]-[session-id]
```

### Step 5: Summary Report

After processing all branches:

```markdown
## Research Processing Complete

| Branch               | Action         | Result             |
| -------------------- | -------------- | ------------------ |
| research-claude-code | Merged + Issue | Issue #182 created |
| research-audio-hooks | Skipped        | -                  |
| research-old-test    | Deleted        | -                  |

**Next Steps:**

- Review created issues
- Run `/popkit:next` to see updated recommendations
```

## Issue Generation

### Title Format

```
[Research] {Topic Title}
```

Examples:

- `[Research] Claude Code v2.0.65 Features Integration`
- `[Research] Audio Feedback Hooks Architecture`

### Body Format

```markdown
## Summary

{Executive summary from research doc}

## Source

- **Branch:** `{full_branch_name}`
- **Created:** {created_ago}
- **Files:** {file_count} changed

## Documentation

- `docs/research/{doc_name}.md`

## Implementation Tasks

- [ ] {Task 1 from research}
- [ ] {Task 2 from research}

---

_Auto-generated from research branch by PopKit_
```

### Labels

Automatically apply:

- `research` - Marks as research output
- `documentation` - Contains documentation

Optionally detect from content:

- `enhancement` - If implementation tasks found
- `P1-high` / `P2-medium` / `P3-low` - From priority metadata

## Error Handling

| Situation               | Response                                |
| ----------------------- | --------------------------------------- |
| Dirty working directory | Prompt to commit/stash first            |
| Merge conflicts         | Show conflicts, offer manual resolution |
| gh CLI unavailable      | Skip issue creation, note in output     |
| No doc files            | Merge anyway, create minimal issue      |
| Branch already merged   | Skip, note in output                    |

## Research Document Standard

For best results, research docs should follow this format:

```markdown
# Research: [Topic Name]

**Research Date:** YYYY-MM-DD
**Status:** Research Document
**Priority:** P1-high | P2-medium | P3-low

## Executive Summary

[Brief summary of findings - becomes issue body]

## Key Findings

[Main research content]

## Implementation Tasks

- [ ] Task 1 [becomes checklist in issue]
- [ ] Task 2
- [ ] Task 3

## References

[Links and sources]
```

## Integration Points

| Component                     | Role                                    |
| ----------------------------- | --------------------------------------- |
| `pop-next-action`             | Calls this skill when branches detected |
| `research_branch_detector.py` | Core detection logic                    |
| `/popkit:next`                | Entry point for auto-detection          |
| `/popkit:routine morning`     | Can include in morning routine          |
| GitHub Issues                 | Output destination for findings         |

## Related

- `/popkit:next` - Primary entry point
- `/popkit:routine morning` - Can detect in morning check
- `hooks/utils/research_branch_detector.py` - Detection utility
- `output-styles/research-summary.md` - Output formatting
