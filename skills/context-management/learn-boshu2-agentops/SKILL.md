---
name: learn
description: 'Capture knowledge manually into the flywheel. Save a decision, pattern, lesson, or constraint for future sessions. Triggers: "learn", "remember this", "save this insight", "I learned something", "note this pattern".'
metadata:
  tier: knowledge
  dependencies: []
---

# Learn Skill

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

Capture knowledge manually for future sessions. Fast path to feed the knowledge flywheel without running a full retrospective.

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--global` | off | Write to `~/.claude/patterns/` instead of `.agents/knowledge/pending/`. Use for knowledge that applies across all projects. |

> **When to use `--global`:** Use for knowledge that applies across all your projects (e.g., language patterns, tooling preferences, debugging techniques). Use default (no flag) for repo-specific knowledge (e.g., architecture decisions, local conventions).

## Execution Steps

Given `/learn [content]`:

### Step 1: Get the Learning Content

**If content provided as argument:** Use it directly.

**If no argument:** Ask the user via AskUserQuestion: "What did you learn or want to remember?" Then collect the content in free text.

### Step 2: Classify the Knowledge Type

Use AskUserQuestion to ask which type:
```
Tool: AskUserQuestion
Parameters:
  questions:
    - question: "What type of knowledge is this?"
      header: "Type"
      multiSelect: false
      options:
        - label: "decision"
          description: "A choice that was made and why"
        - label: "pattern"
          description: "A reusable approach or technique"
        - label: "learning"
          description: "Something new discovered (default)"
        - label: "constraint"
          description: "A rule or limitation to remember"
        - label: "gotcha"
          description: "A pitfall or trap to avoid"
```

**Default to "learning" if user doesn't choose.**

### Step 3: Generate Slug

Create a slug from the content:
- Take the first meaningful words (skip common words like "use", "the", "a")
- Lowercase
- Replace spaces with hyphens
- Max 50 characters
- Remove special characters except hyphens

**Check for collisions:**
```bash
# If file exists, append -2, -3, etc.
slug="<generated-slug>"
counter=2
if [[ "$GLOBAL" == "true" ]]; then
  base_dir="$HOME/.claude/patterns"
else
  base_dir=".agents/knowledge/pending"
fi
while [ -f "${base_dir}/$(date +%Y-%m-%d)-${slug}.md" ]; do
  slug="<generated-slug>-${counter}"
  ((counter++))
done
```

### Step 4: Create Knowledge Directory

```bash
# If --global: write to global patterns (cross-repo)
# Otherwise: write to local knowledge (repo-specific)
if [[ "$GLOBAL" == "true" ]]; then
  mkdir -p ~/.claude/patterns
else
  mkdir -p .agents/knowledge/pending
fi
```

### Step 5: Write Knowledge File

**Path:**
- Default: `.agents/knowledge/pending/YYYY-MM-DD-<slug>.md`
- With `--global`: `~/.claude/patterns/YYYY-MM-DD-<slug>.md`

**Format:**
```markdown
---
type: <classification>
source: manual
date: YYYY-MM-DD
---

# Learning: <short title>

**ID**: L1
**Category**: <classification>
**Confidence**: medium

## What We Learned

<content>

## Source

Manual capture via /learn
```

**Example:**
```markdown
---
type: pattern
source: manual
date: 2026-02-16
---

# Learning: Token Bucket Rate Limiting
**ID**: L1
**Category**: pattern
**Confidence**: high

## What We Learned

Use token bucket pattern for rate limiting instead of fixed windows. Allows burst traffic while maintaining average rate limit. Implementation: bucket refills at constant rate, requests consume tokens, reject when empty.

Key advantage: smoother user experience during brief bursts.

## Source

Manual capture via /learn
```

### Step 6: Integrate with ao CLI (if available)

Check if ao is installed:
```bash
if command -v ao &>/dev/null; then
  echo "✓ Knowledge saved to <path>"
  echo ""
  echo "To move this into cached memory now:"
  echo "  ao pool ingest <path>"
  echo "  ao pool list --status pending"
  echo "  ao pool stage <candidate-id>"
  echo "  ao pool promote <candidate-id>"
  echo ""
  echo "Or let hooks run close-loop automation."
else
  echo "✓ Knowledge saved to <path>"
  echo ""
  echo "Note: Install ao CLI to enable automatic knowledge flywheel."
fi
```

**Do NOT auto-run promotion commands.** The user should decide when to stage/promote.

**Note:** If `--global` is set, skip ao CLI integration. Global patterns are file-based only and are found via grep search in `/research`, `/knowledge`, and `/inject`.

### Step 7: Confirm to User

Tell the user:
```
Learned: <one-line summary from content>

Saved to: .agents/knowledge/pending/YYYY-MM-DD-<slug>.md
Type: <classification>

This capture is queued for flywheel ingestion; once promoted it is available via /research and /inject.
```

## Key Rules

- **Be concise** - This is for quick captures, not full retrospectives
- **Preserve user's words** - Don't rephrase unless they ask
- **Use simple slugs** - Clear, descriptive, lowercase-hyphenated
- **Ingest-compatible format** - Include `# Learning:` block with category/confidence
- **No auto-promotion** - User controls quality pool workflow

## Examples

### Quick Pattern Capture

**User says:** `/learn "use token bucket for rate limiting"`

**What happens:**
1. Agent has content from argument
2. Agent asks for classification via AskUserQuestion
3. User selects "pattern"
4. Agent generates slug: `token-bucket-rate-limiting`
5. Agent creates `.agents/knowledge/pending/2026-02-16-token-bucket-rate-limiting.md`
6. Agent writes frontmatter + content
7. Agent checks for ao CLI, informs user about `ao pool ingest` + stage/promote options
8. Agent confirms: "Learned: Use token bucket for rate limiting. Saved to .agents/knowledge/pending/2026-02-16-token-bucket-rate-limiting.md"

### Interactive Capture

**User says:** `/learn`

Agent asks for content and type, generates slug `never-eval-hooks`, creates `.agents/knowledge/pending/2026-02-16-never-eval-hooks.md`, confirms save.

### Gotcha Capture

**User says:** `/learn "bd dep add A B means A depends on B, not A blocks B"`

Agent classifies as "gotcha", generates slug `bd-dep-direction`, creates file in pending, confirms save.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Slug collision | Same topic on same day | Append `-2`, `-3` counter automatically |
| Content too long | User pasted large block | Accept it. /learn has no length limit. Suggest /retro for structured extraction if very large. |
| ao pool ingest/stage fails | Candidate ID mismatch or ao not installed | Show exact next commands (`ingest`, `list`, `stage`, `promote`) and confirm file was saved |
| Duplicate knowledge | Same insight already captured | Check existing files with grep before writing. If duplicate, tell user and show existing path. |

## The Flywheel

Manual captures feed the same flywheel as automatic extraction:
```
/learn → .agents/knowledge/pending/ → ao pool ingest → .agents/learnings/ → /inject + feedback-loop
```

This skill is for quick wins. For deeper reflection, use `/retro`.
