---
name: extract
description: 'Extract decisions and learnings from Claude session transcripts. Triggers: "extract learnings", "process pending", SessionStart hook.'
user-invocable: false
metadata:
  tier: background
  dependencies: []
  internal: true
---

# Extract Skill

**Typically runs automatically via SessionStart hook.**

Process pending learning extractions from previous sessions.

## How It Works

The SessionStart hook runs:
```bash
ao extract
```

This checks for queued extractions and outputs prompts for Claude to process.

## Manual Execution

Given `/extract`:

### Step 1: Check for Pending Extractions

```bash
ao extract 2>/dev/null
```

Or check the pending queue:
```bash
cat .agents/ao/pending.jsonl 2>/dev/null | head -5
```

### Step 1.5: Without ao CLI — Manual Extraction

If ao CLI is not available, process the pending queue manually:

```bash
if ! command -v ao &>/dev/null; then
  echo "ao CLI not available — running manual extraction"

  # Check for pending queue
  if [ -f .agents/ao/pending.jsonl ] && [ -s .agents/ao/pending.jsonl ]; then
    echo "Found pending extractions:"
    cat .agents/ao/pending.jsonl

    # For each pending entry, check for corresponding forge output
    # Forge outputs live in .agents/forge/
    for forge_file in .agents/forge/*.md; do
      [ -f "$forge_file" ] || continue
      echo "Processing: $forge_file"
    done
  else
    echo "No pending extractions found."
  fi

  # After processing, check .agents/forge/ for unprocessed candidates
  FORGE_COUNT=$(ls .agents/forge/*.md 2>/dev/null | wc -l | tr -d ' ')
  if [ "$FORGE_COUNT" -gt 0 ]; then
    echo "$FORGE_COUNT forge candidates found — review and extract learnings manually."
    echo "For each candidate in .agents/forge/:"
    echo "  1. Read the candidate file"
    echo "  2. Extract actionable learnings using the template in Step 3"
    echo "  3. Write to .agents/learnings/YYYY-MM-DD-<topic>.md"
    echo "  4. High-confidence items (>= 0.7) can be promoted directly"
  fi
fi
```

For each forge candidate, extract learnings using the same template format defined in Step 3 of this skill. Write results to `.agents/learnings/`. After processing, clear the pending queue:

```bash
# Clear processed entries
> .agents/ao/pending.jsonl
echo "Pending queue cleared"
```

### Step 2: Process Each Pending Item

For each queued session:
1. Read the session summary
2. Extract actionable learnings
3. Write to `.agents/learnings/`

### Step 3: Write Learnings

**Write to:** `.agents/learnings/YYYY-MM-DD-<session-id>.md`

```markdown
# Learning: <Short Title>

**ID**: L1
**Category**: <debugging|architecture|process|testing|security>
**Confidence**: <high|medium|low>

## What We Learned

<1-2 sentences describing the insight>

## Why It Matters

<1 sentence on impact/value>

## Source

Session: <session-id>
```

### Step 3.5: Validate Learnings

After writing learning files, validate each has required fields:

1. **Scan newly written files:**
```bash
ls -t .agents/learnings/YYYY-MM-DD-*.md 2>/dev/null | head -5
```

2. **For each file, check required fields:**
   - **Heading:** File must start with `# Learning: <title>` (non-empty title)
   - **Category:** Must contain `**Category**: <value>` where value is one of: `debugging`, `architecture`, `process`, `testing`, `security`
   - **Confidence:** Must contain `**Confidence**: <value>` where value is one of: `high`, `medium`, `low`
   - **Content:** Must contain a `## What We Learned` section with at least one non-empty line after the heading

3. **Report validation results:**
   - For each valid learning: "✓ <filename>: valid"
   - For each invalid learning: "⚠ <filename>: missing <field>" (list each missing field)

4. **Do NOT delete or retry invalid learnings.** Log the warning and proceed. Invalid learnings are still better than no learnings — the warning helps identify extraction quality issues over time.

### Step 4: Clear the Queue

```bash
ao extract --clear 2>/dev/null
```

### Step 5: Report Completion

Tell the user:
- Number of learnings extracted
- Key insights
- Location of learning files

## The Knowledge Loop

```
Session N ends:
  → ao forge --last-session --queue
  → Session queued in pending.jsonl

Session N+1 starts:
  → ao extract (this skill)
  → Claude processes the queue
  → Writes to .agents/learnings/
  → Validates required fields
  → Loop closed
```

## Key Rules

- **Runs automatically** - usually via hook
- **Process the queue** - don't leave extractions pending
- **Be specific** - actionable learnings, not vague observations
- **Close the loop** - extraction completes the knowledge cycle

## Examples

### SessionStart Hook Invocation

**Hook triggers:** `session-start.sh` runs at session start

**What happens:**
1. Hook calls `ao extract 2>/dev/null`
2. CLI outputs queued session IDs and prompts
3. Agent processes each pending extraction
4. Agent writes learnings to `.agents/learnings/<date>-<session>.md`
5. Agent validates required fields and reports results
6. Hook calls `ao extract --clear` to empty queue

**Result:** Prior session knowledge automatically extracted at session start without user action.

### Manual Extraction Trigger

**User says:** `/extract` or "extract learnings from last session"

**What happens:**
1. Agent checks pending queue with `ao extract`
2. Agent reads session summaries from queue
3. Agent extracts decisions, learnings, failures
4. Agent writes to `.agents/learnings/` with proper structure
5. Agent validates fields (category, confidence, content)
6. Agent clears queue and reports completion

**Result:** Pending extractions processed manually, queue cleared, learnings indexed.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| No pending extractions found | Queue empty or ao CLI unavailable | Check `.agents/ao/pending.jsonl` exists; verify ao CLI installed |
| Invalid learning warning | Missing category/confidence/content | Review learning file, add missing fields; DO NOT delete |
| extraction --clear fails | CLI not available or permission error | Manually truncate `.agents/ao/pending.jsonl` as fallback |
| Duplicate extractions | Queue not cleared after processing | Always run `ao extract --clear` after writing learnings |
