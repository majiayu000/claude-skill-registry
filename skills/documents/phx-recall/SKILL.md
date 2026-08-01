---
name: phx-recall
description: Recall prior work from past sessions — how a bug was fixed, what was
  decided, where a pattern lives. Use when asked 'have we done this before' or 'how
  did I fix X' in Elixir/Phoenix work. ccrider MCP when available, else git + solution
  docs.
---

# Recall — Session & History Archaeology

Search three evidence layers, cheapest first, to answer "have we solved
this before?". Stop at the first layer that answers the question.

## Usage

```
$phx-recall how did we fix the LiveView form that saved silently?
$phx-recall what did we decide about the billing context boundaries?
$phx-recall which library did we pick for rate limiting and why?
```

## Iron Laws

1. **Cheapest layer first** — solution docs (local grep) → git history →
   session transcripts. Don't fetch sessions when a solution doc answers
2. **ONE ccrider fetch = ONE subagent** — `get_session_messages` responses
   are 3–15KB each. Spawn a subagent per session that writes a summary
   file and exits; NEVER batch multiple session fetches into one context
3. **Cite the evidence** — every claim names its source (solution doc
   path, commit hash, or session date + match snippet). No vague "we did
   this once"
4. **Graceful degradation, stated plainly** — if ccrider MCP is absent,
   say so once and use the fallback layers; never error out

## Workflow

### Layer 1: Compound Solution Docs (always)

Run Grep with keywords from the question over `.claude/solutions/`.
Treat a hit here as the best answer — it was written for exactly this
purpose. Present it and stop unless the user wants more.

### Layer 2: Git Archaeology (always available)

```bash
git log --oneline --grep="{keyword}" -i -20      # commit messages
git log -S "{code-symbol}" --oneline -10          # when a symbol changed
git log --follow --oneline -10 -- {file}          # one file's history
git show {hash} --stat                            # inspect a candidate
```

Use `-S` (pickaxe) when the question names code; `--grep` when it names
intent. Show matching commits with one-line context each.

### Layer 3: Session Transcripts (ccrider MCP, gated)

Check for `mcp__ccrider__*` tools (load via ToolSearch if deferred).

**If absent**: report "ccrider MCP not connected — answered from solution
docs + git history" and stop after Layers 1–2.

**If present**:

1. `mcp__ccrider__search_sessions` with the question's key phrases —
   returns ranked hits with session IDs and snippets
2. Present the top 3–5 hits (date, snippet) and pick the most relevant
   (or ask, if genuinely ambiguous)
3. Per selected session, spawn ONE subagent: "Fetch session {id} via
   `mcp__ccrider__get_session_messages`, extract only what answers
   '{question}', write ≤30 lines to `.claude/recall/{id}.md`" (Iron Law 2)
4. Read the summary files, synthesize the answer with citations

### Step 4: Answer + Compound

Present the answer with its evidence trail. If the recalled knowledge was
NOT already in `.claude/solutions/`, offer `$phx-compound` so the next
recall stops at Layer 1.

## Integration

```text
"have we done this before?" → $phx-recall
   Layer 1 .claude/solutions/ ──hit──► answer + cite
   Layer 2 git log --grep/-S  ──hit──► answer + cite
   Layer 3 ccrider sessions (gated) ─► answer + cite → offer $phx-compound
```

## References

- `references/archaeology-patterns.md` — git pickaxe recipes, ccrider query patterns, subagent prompt template
