---
name: review-conversation
description: >
  Review SPARTA conversation transcripts and grading with full transparency.
  Use when asked to review conversations, show transcripts, compare student
  vs teacher grades, inspect persona evaluations, or export sessions for
  human annotation. Replaces the black-box opacity of raw JSONL session files
  with rich turn-by-turn rendering including entity gate decisions, QRA
  citations, self-grade iterations, and persona evaluation reasoning.
allowed-tools:
  - Bash
  - Read
triggers:
  - "review conversation"
  - "show conversation transcript"
  - "compare student teacher grades"
  - "inspect persona evaluation"
  - "export conversation markdown"
  - "conversation disagreements"
  - "review sparta session"
  - "find conversation where"
  - "show me a conversation"
  - "which conversations"
metadata:
  short-description: "Transparent conversation transcript viewer with grading"
  version: "3.0.0"
provides:
  - review-conversation
composes:
  - sparta-stress-test
  - memory
  - task-monitor
  - create-figure
  - analytics
---

# Review Conversation

Transparent conversation transcript viewer for SPARTA stress test sessions.
Every turn, grade, and evaluation visible — no black boxes.

## Quick Start

```bash
# List available session files
./run.sh files

# Show summary of latest session file
./run.sh list

# Show full transcript of session #3
./run.sh show -n 3

# Show specific session by ID
./run.sh show -i stress_20260222_175146

# Show only disagreements (student vs teacher)
./run.sh compare

# Export to markdown for human annotation
./run.sh export -o review.md

# NDJSON stream for automation
./run.sh json-stream
```

## Commands

| Command | Description |
|---------|-------------|
| `files` | List available session JSONL files with sizes and counts |
| `list [file]` | Summary table: all sessions with grades, agreement, resolution |
| `show [file]` | Full transcript with turn-by-turn metadata and grading |
| `compare [file]` | Filter to only student-teacher disagreements |
| `export [file]` | Export sessions as annotated markdown |
| `json-stream [file]` | NDJSON output with merged shadow/delta data |
| `find [file]` | **Structured search** with filters + free-text (agent-human collaboration) |
| `search <query>` | **Semantic search** via `/memory recall` (BM25 + embedding + multi-hop) |
| `ingest [file]` | Learn session summaries to `/memory` for semantic search |
| `brief [file]` | Plain markdown for in-chat display (no Rich/ANSI) |
| `flow [file]` | **Mermaid conversation flow diagrams** with inline grading metadata |
| `data [file]` | Export JSON for `/create-figure` (radar, heatmap, bar charts) |

## Show Options

| Flag | Description |
|------|-------------|
| `-n, --index N` | Show session N (1-based) |
| `-i, --id PREFIX` | Show session matching ID prefix |
| `--no-metadata` | Hide turn-level metadata (grades, evaluations) |
| `--no-teacher` | Hide student-vs-teacher comparison |
| `--dir PATH` | Override sessions directory |
| `--shadow PATH` | Override shadow.jsonl path |
| `--deltas PATH` | Override shadow_deltas.jsonl path |

## What You See Per Turn

For **persona turns** (Margaret/Jennifer asking):
- Speaker, action type (QUERY/FOLLOW_UP), timestamp
- Persona evaluation verdict: SATISFACTORY / INCOMPLETE / WRONG / FLAW_CAUGHT / FLAW_MISSED
- Evaluation reasoning (why the persona accepted or rejected)

For **system turns** (SPARTA answering):
- Full response text with entity gate decisions
- Self-grade: letter grade + composite score + iteration count
- QRA citation count
- Issues flagged during self-grading
- Rationale from semantic grader

## What You See Per Session

- **Session grade**: 8-dimension rubric breakdown with visual bars
- **Student vs Teacher comparison**: side-by-side grades, confidence, model names
- **Agreement signal**: AGREE (green) or DISAGREE (red)
- **Improvement delta**: first → final score, outer/inner iteration counts
- **QRA citation metrics**: verified/total, grounding average

## Data Sources

| File | Location | Content |
|------|----------|---------|
| `sessions_*.jsonl` | `sparta-stress-test/results/sessions/` | Full conversation transcripts |
| `shadow.jsonl` | `~/.pi/assistant/` | Teacher grades + agreement |
| `shadow_deltas.jsonl` | `~/.pi/assistant/` | Improvement tracking per session |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SESSIONS_DIR` | `../sparta-stress-test/results/sessions/` | Sessions directory |
| `SHADOW_JSONL_PATH` | `~/.pi/assistant/shadow.jsonl` | Shadow entries |
| `SHADOW_DELTA_PATH` | `~/.pi/assistant/shadow_deltas.jsonl` | Improvement deltas |

## Semantic Search via /memory (`search`, `ingest`)

Composes with `/memory` for BM25 + semantic embedding + multi-hop graph traversal.
Far superior to bespoke text search for natural language queries.

### Workflow

```bash
# 1. After a stress test, ingest sessions to /memory
./run.sh ingest

# 2. Search semantically (natural language)
./run.sh search "conversations where Brandon missed a fake control"
./run.sh search "GPS spoofing questions that got resolved"
./run.sh search "low-scoring sessions with iteration improvement"

# 3. Or use --semantic on find (combines structured filters + semantic)
./run.sh find --semantic "fake control missed" --grade F
```

### How It Works

| Layer | What It Does |
|-------|-------------|
| **BM25** | Keyword matching against ingested session summaries |
| **Semantic embedding** | Dense vector similarity for meaning-based recall |
| **Multi-hop traversal** | Graph edges connecting related sessions, controls, personas |

`ingest` extracts problem/solution pairs from each session and stores them
with tags (`grade_A`, `difficulty_complex`, `resolution_resolved`, etc.)
for filtered recall.

### Graceful Degradation

If `/memory` is unavailable (no ArangoDB, no embedding service), semantic
commands return empty results and fall back to structured filters. The skill
never crashes — it just loses the semantic layer.

## Agent-Human Collaboration (`find`)

The `find` command is the primary collaboration surface. When the human asks
a question about conversations, the agent translates it into structured filters:

```bash
# "Show me a conversation where Brandon didn't flag a non-existent control"
./run.sh find --eval flaw_missed --resolution no_coverage

# "Show me where Margaret failed the first response but iteration saved it to 90%"
./run.sh find --first-eval "!satisfactory" --min-composite 0.9

# "Which complex questions got fully resolved?"
./run.sh find --difficulty complex --resolution resolved

# "Find conversations about SV-SP-1"
./run.sh find --text "SV-SP-1"

# "Show disagreements on flawed questions"
./run.sh find --difficulty flawed --disagree

# "How many F-grade sessions are there?"
./run.sh find --grade F --format count

# "Show low-scoring sessions in Rich detail"
./run.sh find --max-composite 0.5 --format show
```

### Find Filters

| Flag | Description |
|------|-------------|
| `-g, --grade A\|B\|C\|F` | Filter by session grade |
| `-r, --resolution` | `resolved`, `partial`, `no_coverage`, `ambiguous` |
| `-e, --eval` | Persona evaluation: `satisfactory`, `incomplete`, `wrong`, `flaw_caught`, `flaw_missed`. Prefix `!` to negate |
| `--first-eval` | First persona evaluation only (supports `!` negation) |
| `--min-composite` | Minimum final composite score (0.0-1.0) |
| `--max-composite` | Maximum final composite score (0.0-1.0) |
| `-d, --difficulty` | `simple`, `medium`, `complex`, `flawed`, `ambiguous` |
| `-p, --persona` | Filter by persona name |
| `--min-turns` | Minimum turn count (higher = more iteration) |
| `-t, --text` | Free-text search across all turn content, evaluations, rationales |
| `-s, --semantic` | **Semantic search** via `/memory recall` (BM25 + embedding + multi-hop). Use for natural language queries |
| `--agree/--disagree` | Filter by teacher agreement |
| `-f, --format` | Output: `brief` (markdown), `show` (Rich), `count` (just count) |

All filters are AND-combined. Default output is `brief` (pasteable markdown).

### Translation Guide for Agents

When the human asks in natural language, translate to filters:

| Human Says | Agent Runs |
|------------|------------|
| "Where did Brandon miss a fake control?" | `find --eval flaw_missed` |
| "Sessions where iteration improved the answer" | `find --first-eval "!satisfactory" --min-composite 0.8` |
| "Failed conversations" | `find --grade F` or `find --max-composite 0.5` |
| "Where do student and teacher disagree?" | `find --disagree` or `compare` |
| "Conversations about GPS spoofing" | `find --semantic "GPS spoofing"` or `search "GPS spoofing"` |
| "Complex questions that were answered well" | `find --difficulty complex --grade A` |
| "How many ambiguous questions are there?" | `find --difficulty ambiguous --format count` |

## Agent In-Chat Display (`brief`)

The `brief` command outputs plain markdown (no Rich/ANSI codes) that agents
can paste directly into chat:

```bash
# Summary table (paste in chat)
./run.sh brief

# Single session compact view
./run.sh brief -n 3
./run.sh brief -i stress_20260222
```

## Visualization with /create-figure (`data`)

Export JSON files that `/create-figure` consumes directly:

```bash
# Export all chart data
./run.sh data -o /tmp/charts/

# Then visualize with /create-figure
cd .pi/skills/create-figure
./run.sh radar --input /tmp/charts/radar.json --output radar.pdf
./run.sh heatmap --input /tmp/charts/heatmap.json --output heatmap.pdf
./run.sh metrics --input /tmp/charts/grade_distribution.json --type bar

# Export only radar chart data
./run.sh data -c radar -o /tmp/charts/
```

JSON files produced:
- `radar.json` — 8-dimension rubric scores per session (for radar charts)
- `heatmap.json` — difficulty x grade distribution (for heatmaps)
- `grade_distribution.json` — grade letter counts (for bar charts)
- `resolution_distribution.json` — resolution outcome counts (for bar/pie)
- `agreement.json` — agreed/disagreed/no_teacher counts (for bar/pie)

For deeper analytics, pipe `json-stream` output to `/analytics`:
```bash
./run.sh json-stream > sessions.jsonl
cd .pi/skills/analytics
./run.sh describe sessions.jsonl
./run.sh chart sessions.jsonl --name grade --for-figure
```

## Integration with /sparta-stress-test

Run a stress test, then immediately review:

```bash
# Run 25 conversations
cd .pi/skills/sparta-stress-test
./run.sh run --count 25

# Review results
cd .pi/skills/review-conversation
./run.sh list
./run.sh compare
./run.sh show -n 1
```
