---
name: agent-commit
description: Analyze changes and create a meaningful commit with agent authorship. Internal skill for evolve_loop.
---

# Agent Commit

Creates a git commit with meaningful message based on skill output and actual file changes.

## When to Use

This skill is called automatically by `evolve_loop.py` after a content-modifying skill completes. It is not intended for manual invocation.

## Input

You will receive:
1. The name of the skill that just ran
2. A summary or excerpt of that skill's output

## Instructions

### 1. Check for Changes

Run `git status --porcelain` to see if there are uncommitted changes.

If there are no changes, output "No changes to commit" and stop.

### 2. Analyze the Changes

Run `git diff` (or `git diff --cached` if files are staged) to understand what was modified.

Focus on:
- Which files were changed (especially content files in `obsidian/`)
- The nature of the changes (new content, edits, deletions)
- Key themes or topics affected

### 3. Generate Commit Message

Create a commit message with a summary line and body:

```
<type>(<skill>): <summary>

<body>
```

**Summary line** (required, under 72 chars):
- `<type>` is one of: `feat`, `fix`, `refine`, `research`, `chore`
- `<skill>` is the skill name (e.g., `deep-review`, `condense`, `expand-topic`)
- `<summary>` describes WHAT was done and to WHICH file(s)
- **File paths must include parent directory** (e.g., `topics/free-will.md` not just `free-will.md`)

**Body** (required for content changes):
- 2-5 bullet points summarizing key changes
- For condense: before/after word counts, what was cut vs preserved
- For deep-review: what issues were found and fixed
- For expand-topic: key themes covered
- For research: sources consulted, main findings

**Good examples:**
```
refine(condense): reduce topics/free-will.md from 9567 to 2985 words

- Cut quantum Zeno redundancy (7+ mentions → 1 via link)
- Removed extended sections on altered states, process philosophy
- Preserved core phenomenology arguments and Mary's Room
- Kept tenet connections and cross-links intact
```

```
refine(deep-review): improve clarity in concepts/qualia.md

- Fixed circular definition in opening paragraph
- Added concrete examples for inverted spectrum argument
- Strengthened connection to hard problem article
```

**Bad examples:**
- `auto(deep-review): Automated execution` (too vague, no body)
- `Updated files` (no context)
- `refine(condense): reduce free-will.md` (missing parent directory - is it topics/ or concepts?)

### 4. Create the Commit

Stage all changes and commit with agent authorship. Use a HEREDOC for the multi-line message:

```bash
git add -A
git commit --author "unfinishablemap.org Agent <agent@unfinishablemap.org>" -m "$(cat <<'EOF'
<summary line>

- bullet point 1
- bullet point 2
EOF
)"
```

### 5. Output the Result

Output the commit hash and message so the calling system can log it.

## Important

- Keep commit messages under 72 characters for the summary line
- **Always include parent directory in file paths** (e.g., `topics/free-will.md`, `concepts/qualia.md`, `research/notes.md`)
- Focus on the "what" and "which file" - the skill name already tells us "how"
- If multiple files changed, mention the primary one and note others exist
- Never include time estimates or subjective assessments in commit messages
