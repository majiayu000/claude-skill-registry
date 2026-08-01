---
name: pm-pipeline
description: Read ops/derivation-manifest.md for vocabulary.
---

---
name: pm-pipeline
description: Show the state of the processing queue — what is in inbox, what is mid-pipeline (documented but not linked), what is complete. Manage queue entries: advance, stall, remove. The pipeline control center. Triggers on "/pm-pipeline", "show queue", "pipeline status", "what's in progress", "queue status".
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
context: fork
---

## Runtime Configuration (Step 0)

Read `ops/derivation-manifest.md` for vocabulary.
Read `ops/config.yaml` for queue configuration.

---

## EXECUTE NOW

**Target: $ARGUMENTS**

Parse immediately:
- If empty: show current pipeline state
- If "advance [item]": move named item to next pipeline phase
- If "stall [item]": mark item as stalled with reason
- If "clear [item]": mark item as complete and move to archive
- If "add [source]": add new source to inbox

**START NOW.**

---

## Philosophy

**The pipeline is the heartbeat. Stalled items are clots.**

Every sprint output, security audit, and team report enters the pipeline at inbox/ and moves through: inbox → documented → linked → updated → complete. A healthy system processes items within 2-3 sessions. Stalled items mean decisions are trapped — available in the source but not yet in the knowledge graph where they can inform future coordination.

/pm-pipeline makes the pipeline visible. It is not just a queue manager — it is a health indicator. A full inbox with nothing moving is a warning sign. A deep backlog in "documented but not linked" means /pm-link is being skipped.

---

## Pipeline Stages

| Stage | Location | What it means |
|-------|----------|--------------|
| INBOX | `inbox/` | Source material received, not yet processed |
| DOCUMENTED | Queue entry: phase=documented | `/pm-document` run, decisions created, not yet linked |
| LINKED | Queue entry: phase=linked | `/pm-link` run, connections added, older decisions not yet updated |
| UPDATED | Queue entry: phase=updated | `/pm-update` run, full pipeline complete |
| COMPLETE | `ops/queue/archive/` | Fully processed |

---

## Workflow

### 1. Read Current State

```bash
# Check inbox
ls inbox/ 2>/dev/null
echo "---"

# Check queue
cat ops/queue/queue.json 2>/dev/null

# Check archive (how many completed)
ls ops/queue/archive/ 2>/dev/null | wc -l
```

### 2. Assess Pipeline Health

For each item in the queue:
- How long has it been at its current stage? (check `added_at` and `last_updated`)
- What is blocking advancement?
- Is there a pattern of items stalling at the same stage?

### 3. Compute Wait Times

Items in pipeline longer than:
- 1 session: normal
- 2 sessions: yellow flag
- 3+ sessions: red flag (stalled)

### 4. Suggest Next Actions

For each stalled item, suggest the specific command to advance it.

---

## Queue Entry Format

```json
{
  "id": "sprint-5-output-2026-02-19",
  "source": "docs/Reports/SPRINT_5_OUTPUT.md",
  "phase": "inbox",
  "added_at": "2026-02-19",
  "last_updated": "2026-02-19",
  "decisions_created": [],
  "notes": ""
}
```

Phase progression: `inbox` → `documented` → `linked` → `updated` → `complete`

---

## Output Format

```
## Pipeline Status — YYYY-MM-DD

### Stage 1: INBOX (N items)
- sprint-5-output.md — added 2026-02-19 — Action: /pm-document sprint-5-output.md
- security-audit-2026-02-19.md — added 2026-02-19 — Action: /pm-document security-audit-2026-02-19.md

### Stage 2: DOCUMENTED (N items)
- [item] — documented 2026-02-18, decisions: [[d1]], [[d2]] — Action: /pm-link d1

### Stage 3: LINKED (N items)
- [item] — linked 2026-02-17 — Action: /pm-update [decisions that affect older ones]

### Stage 4: UPDATED (N items — moving to complete)
- [item] — pipeline complete, archiving

### Stage 5: COMPLETE (N items archived)

---

### Pipeline Health
- Items stalled >2 sessions: N [WARN if > 0]
- Most common stall stage: [stage name]
- Bottleneck: [diagnosis if pattern detected]

### Recommended Next Actions
1. /pm-document [item] — clears N inbox items
2. /pm-link [decisions] — advances N items from documented
```

---

## Advancing Items

When the user says "advance [item]":
1. Read the current queue entry for that item
2. Determine what work is needed to advance to the next phase
3. Update the queue entry's `phase` and `last_updated`
4. Write the updated queue.json
5. Confirm what the next action is

When the user says "clear [item]":
1. Move the queue entry to `ops/queue/archive/`
2. Remove from queue.json
3. Confirm completion
