---
name: search-conversations
description: Search past Claude Code conversations. Use when user says "search conversations", "find that chat", "what did we discuss", "where did we talk about", "look up past session", "find conversation about X", "search history", "what did I ask about", "remember when we", "that discussion about". Also triggers on past-tense questions referencing prior work or possessives without context.
---

# search-conversations

## Extraction

```bash
python3 ~/.claude/skills/search-conversations/scripts/extract_conversations.py --days 3
```

| Option | Effect |
|--------|--------|
| `--days N` | Days from last activity (not today) |
| `--from-today` | Days from today instead |
| `--all-projects` | Cross-project (implies --from-today) |
| `--project /path` | Filter to specific project |
| `--compact` | No metadata, more conversation |
| `--min-exchanges N` | Skip sessions with < N exchanges |
| `--ids abc,def` | Fetch specific conversations |
| `--paths /path.jsonl` | Direct file paths |

**Output**: Default shows files, tools, errors + conversation. `--compact` omits metadata.

**Time modes**: `--days N` counts from last activity (useful when returning to old projects). `--all-projects` or `--from-today` counts from today (calendar-based).

## Workflow

1. **Identify the lens** from user intent (see Routing table below)

2. **Extract recent context** using the script with lens-appropriate parameters:
   ```bash
   python3 ~/.claude/skills/search-conversations/scripts/extract_conversations.py --days N [flags]
   ```
   Use the Parameters table to select `--days`, flags, and any supplementary data to gather.

3. **Apply lens questions** to analyze the extracted conversations

4. **Deepen the search** using what you learned from the initial extraction:
   - Extract additional timeframes with the script (`--days 30`, `--all-projects`)
   - Search for specific keywords, project names, or patterns that surfaced:
     ```bash
     qmd search "keyword from context" -c conversations -n 15 --files
     ```
   - Extract those specific paths: `python3 ... --paths /found/conv.jsonl`

   This step surfaces older context, related discussions, or cross-project patterns that complement the initial extraction.

**Keep index updated**: Run `qmd update` periodically to index new sessions.

---

## Lenses

### Routing

| User Says | Lens |
|-----------|------|
| "where were we", "recap" | restore-context |
| "what I learned", "reflect" | extract-learnings |
| "gaps", "struggling" | find-gaps |
| "mentor", "review process" | review-process |
| "retro", "project review" | run-retro |
| "decisions", "CLAUDE.md" | extract-decisions |
| "bad habits", "antipatterns" | find-antipatterns |

### Parameters

| Lens | Days | Flags | Also Gather |
|------|------|-------|-------------|
| restore-context | 3 | — | `git status`, `git log -10` |
| extract-learnings | 14 | `--all-projects --compact` | — |
| find-gaps | 30 | `--all-projects --compact` | — |
| review-process | 14 | `--all-projects --compact` | recent git log |
| run-retro | 30 | `--project /path` | full git history |
| extract-decisions | 90 | `--project /path` | — |
| find-antipatterns | 30 | `--all-projects --compact` | — |

`--min-exchanges 2` or `3` filters out short sessions and reduces noise.

### Core Questions

| Lens | Ask |
|------|-----|
| restore-context | What's unfinished? What were the next steps? |
| extract-learnings | Where did understanding shift? What mistakes became lessons? |
| find-gaps | What topics recur? Where is guidance needed repeatedly? |
| review-process | Is there planning before coding? Is debugging systematic? |
| run-retro | How did the solution evolve? What worked? What was painful? |
| extract-decisions | What trade-offs were discussed? What was rejected and why? |
| find-antipatterns | What mistakes repeat? What confusions persist? |

**Follow-ups**: find-gaps → suggest `learn-anything`. extract-decisions → suggest `/updateclaudemd`.

### Supplementary Search Patterns

When recent extraction doesn't surface enough, use these qmd queries to find specific sessions:

| Lens | Query |
|------|-------|
| extract-learnings | `qmd search "learned realized understand clicked" -c conversations -n 15 --files` |
| find-gaps | `qmd search "confused struggling help with don't understand" -c conversations -n 15 --files` |
| extract-decisions | `qmd search "decided chose instead of trade-off because" -c conversations -n 15 --files` |
| find-antipatterns | `qmd search "again same mistake repeated forgot" -c conversations -n 15 --files` |

---

## Synthesis

### Principles

1. **Prioritize significance** — 3-5 key findings, not exhaustive lists
2. **Be specific** — file paths, dates, project names
3. **Make it actionable** — every finding suggests a response
4. **Show evidence** — quotes or references
5. **Keep it scannable** — clear structure, no walls of text

### Structure

```markdown
## [Analysis Type]: [Scope]

### Summary
[2-3 sentences]

### Findings
[Organized by whatever fits: categories, timeline, severity]

### Patterns
[Cross-cutting observations]

### Recommendations
[Actionable next steps]
```

### Length

Default: 300-500 words. Expand only when data warrants it.
