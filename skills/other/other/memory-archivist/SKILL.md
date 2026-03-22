---
name: memory-archivist
description: Cross-reference and synthesise daily memory files into patterns, insights, and carry-forward items. Use when asked to review memory, generate weekly synthesis, find forgotten tasks, detect decision patterns, or audit what was carried forward vs dropped. Also triggers on "what did I decide about X", "what's still pending", "weekly review", "memory synthesis", "what patterns do you see".
---

# Memory Archivist

Memory is sacred. This skill turns raw daily journals into structured wisdom.

## What This Skill Does

1. **Cross-reference** — Read all `memory/*.md` files and find connections between days
2. **Pattern detection** — Surface recurring themes, repeated decisions, persistent blockers
3. **Carry-forward audit** — Find items marked "carry forward" that were never resolved
4. **Weekly synthesis** — Generate a weekly summary from daily files
5. **Scar-to-decision mapping** — Track how USER.md scars influence actual decisions over time

## Trigger Patterns

- "review my memory", "memory synthesis", "weekly review"
- "what's still pending", "what did I forget"
- "what patterns do you see", "recurring themes"
- "what did I decide about [topic]"
- "carry forward audit", "dropped items"
- "synthesise this week"

## On Trigger — Execute in Order

### Step 1: Gather Memory Files

```bash
# List all memory files sorted by date
ls -1 ~/.openclaw/workspace/memory/*.md 2>/dev/null | sort
```

Read the most recent 7 files (or all if fewer than 7 exist). Use the `read` tool, not exec.

### Step 2: Extract Structured Data

From each daily file, extract:

| Field | Section to scan |
|-------|----------------|
| **Decisions** | "Key Decisions Made Today" |
| **Carry-forward** | "Carry Forward" |
| **888_HOLD** | "888_HOLD Items Pending" |
| **Floors active** | "Floors Active This Session" |
| **Context** | "Session Context" |

### Step 3: Cross-Reference

For each carry-forward item, check if it appears as resolved in any later day's decisions.

Build a table:

```markdown
| Carry-Forward Item | First Mentioned | Resolved? | Resolution Date | Days Open |
```

Flag any item open longer than 3 days as ⚠️ STALE.

### Step 4: Detect Patterns

Scan across all files for:

- **Repeated topics** — same subject appearing in 3+ daily files
- **Recurring blockers** — carry-forward items that keep reappearing
- **Floor patterns** — which floors are consistently active vs rarely active
- **Decision velocity** — how many decisions per day (trending up/down?)

### Step 5: Generate Synthesis

Output format depends on the request:

**Weekly synthesis** → Write to `memory/weekly-YYYY-WXX.md`:

```markdown
# Weekly Synthesis — YYYY-WXX (arifOS_bot)

## Period
YYYY-MM-DD to YYYY-MM-DD

## Key Decisions This Week
1. ...

## Carry-Forward Audit
| Item | Status | Days Open |
|------|--------|-----------|

## Patterns Detected
- ...

## 888_HOLD Items (Active)
- ...

## Floor Activity
F1: X sessions | F2: X sessions | ...

## Recommendation
<one-line suggestion for next week based on patterns>
```

**Ad-hoc query** ("what did I decide about X") → Search all memory files for the topic, return chronological trail of mentions with dates.

**Carry-forward audit** → Return the open items table only.

### Step 6: Seal to VAULT999

After generating synthesis, seal via arifOS MCP:

```bash
arifos seal
```

Or via HTTP:
```bash
curl -sf -X POST http://arifosmcp_server:8080/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"seal_vault","arguments":{"session_id":"memory-archivist","context":"weekly synthesis sealed"}}}'
```

This commits the synthesis to the immutable VAULT999 ledger. Memory is sacred — sealed memory is permanent.

### Step 7: Log the Synthesis

Append to `logs/audit.jsonl`:

```json
{"ts":"<ISO>","event":"memory_synthesis","source":"memory-archivist","files_scanned":<n>,"patterns_found":<n>,"stale_items":<n>,"sealed":true,"agent":"arifOS_bot"}
```

## Scheduling (Cron)

Run the archivist nightly at 00:30 MYT (16:30 UTC), after the git-sync backup at 00:00 MYT:

```bash
# Add to host crontab (not container — container restarts clear cron)
30 16 * * * cd /opt/arifos/data/openclaw/workspace && bash skills/memory-archivist/scripts/scan-carry-forward.sh memory/ >> logs/archivist.log 2>&1
```

For the full agent-driven synthesis (weekly), trigger manually or via HEARTBEAT.md on every 8th heartbeat (~4 hours):
- "Run memory archivist" or "weekly review"

## Constraints

- **Read-only on memory files.** Never edit existing `memory/*.md` files. Only create new synthesis files.
- **F1 Amanah.** All synthesis is additive. Nothing is deleted or overwritten.
- **F7 Humility.** If a pattern has low confidence (appears only twice), mark it as tentative.
- **F4 Clarity.** Output must reduce confusion. Tables over prose. One insight per line.
