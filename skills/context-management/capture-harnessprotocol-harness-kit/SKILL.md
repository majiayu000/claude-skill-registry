---
name: capture
description: Use when user invokes /capture to capture information from the current conversation into a staging file for later reflection and knowledge graph processing. Accepts no arguments (auto-extract), specific facts as text, or filter keywords like "decisions" or "technical". Do NOT use when the user wants to write directly to knowledge files — use direct file editing instead.
disable-model-invocation: true
---

# Session Staging

## Overview

Capture information from the current conversation into a staging file for the daily reflection pipeline to consume and write to the knowledge graph.

**Core principles:**
1. **Token-conscious** — 3-8 bullets, max 20 words each
2. **Complementary to Stop hook** — captures nuance and specificity the auto-summary misses
3. **Append-only** — never modify existing entries in the staging file
4. **Confirm what was staged** — always show the user exactly what was written

## Argument Types

| Argument | Behavior |
|----------|----------|
| (none) | Auto-extract 3-8 most important facts from the conversation |
| Specific text | Stage the provided facts as bullets |
| `decisions` | Extract only decisions made this session |
| `technical` | Extract only technical facts and implementation details |

## Workflow (MANDATORY — follow in order)

### Step 1: Parse Input

Classify the argument:
- **No argument** → auto-extract mode
- **Exactly the word `decisions`** → filter to decisions only
- **Exactly the word `technical`** → filter to technical facts only
- **Anything else** → treat as specific facts provided by the user

### Step 2: Resolve Staging File

Check in order:
1. `scripts/session-staging.md` in the project root (current working directory)
2. `~/.claude/session-staging.md` as fallback

If the resolved file does not exist, create it with this header:

```markdown
# Session Staging

Facts staged here are consumed by the daily reflection and written to the knowledge graph.
```

### Step 3: Extract or Formulate Bullets

Based on argument type, produce 3-8 bullets. Each bullet: max 20 words, factual, specific.

**Auto-extract (no argument):** Scan the conversation for the most important facts — decisions made, technical details learned, status changes, new entities or tools introduced. Prefer concrete facts over vague summaries.

**Specific facts (user-provided text):** Convert the user's text into clean bullet points. If they already gave you bullets, clean and tighten them. If they gave you prose, extract the key facts.

**`decisions` filter:** Extract only explicit decisions made in this session — architectural choices, plans confirmed, approaches selected. Skip observations, status updates, and technical details.

**`technical` filter:** Extract only technical facts — implementation details, APIs used, data structures, file paths, commands, schemas, and configuration. Skip process, decisions, and context.

Get the current timestamp via Bash:
```bash
date '+%Y-%m-%d %H:%M'
```

### Step 4: Append to Staging File

Use **Bash** with `>>` to append — do NOT use Write (overwrites the whole file) or Edit (find-replace, not true append):

```bash
{
  echo ""
  echo "## YYYY-MM-DD HH:MM"
  echo "<!-- source: manual -->"
  echo "- bullet 1"
  echo "- bullet 2"
} >> /path/to/staging-file.md
```

The `<!-- source: manual -->` marker tells the Stop hook that manual staging already happened today, enabling deduplication.

### Step 5: Confirm

Display what was staged to the user. Show the exact bullets that were written. Keep it brief — no need to re-explain what staging does.

## Scope Controls

- Max 8 bullets per entry
- Max 20 words per bullet
- Append-only — never modify existing entries
- Current conversation only — do not pull from memory, graph, or files

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using Write or Edit to append | Write overwrites. Edit is find-replace, not append. Use Bash `>>`. |
| Exceeding 8 bullets | Pick the most important facts. Cut the rest. |
| Omitting `<!-- source: manual -->` | The Stop hook uses this marker for deduplication. Always include it. |
| Writing summaries instead of bullet facts | "Decided to use SQLite for storage" not "We had a productive discussion about databases." |
| Staging vague observations | "SQLite chosen over Postgres for local-first storage" not "database discussion happened." |
