---
name: forge
description: 'Mine transcripts for knowledge - decisions, learnings, failures, patterns. Triggers: "forge insights", "mine transcripts", "extract knowledge".'
user-invocable: false
metadata:
  tier: background
  dependencies: []
  internal: true
---

# Forge Skill

**Typically runs automatically via SessionEnd hook.**

Extract knowledge from session transcripts.

## How It Works

The SessionEnd hook runs:
```bash
ao forge transcript --last-session --queue --quiet
```

This queues the session for knowledge extraction.

## Manual Execution

Given `/forge [path]`:

### Step 1: Identify Transcript

**With ao CLI:**
```bash
# Mine recent sessions
ao forge --recent

# Mine specific transcript
ao forge transcript <path>
```

**Without ao CLI:**
Look at recent conversation history and extract learnings manually.

### Step 2: Extract Knowledge Types

Look for these patterns in the transcript:

| Type | Signals | Weight |
|------|---------|--------|
| **Decision** | "decided to", "chose", "went with" | 0.8 |
| **Learning** | "learned that", "discovered", "realized" | 0.9 |
| **Failure** | "failed because", "broke when", "didn't work" | 1.0 |
| **Pattern** | "always do X", "the trick is", "pattern:" | 0.7 |

### Step 3: Write Candidates

**Write to:** `.agents/forge/YYYY-MM-DD-forge.md`

```markdown
# Forged: YYYY-MM-DD

## Decisions
- [D1] <decision made>
  - Source: <where in conversation>
  - Confidence: <0.0-1.0>

## Learnings
- [L1] <what was learned>
  - Source: <where in conversation>
  - Confidence: <0.0-1.0>

## Failures
- [F1] <what failed and why>
  - Source: <where in conversation>
  - Confidence: <0.0-1.0>

## Patterns
- [P1] <reusable pattern>
  - Source: <where in conversation>
  - Confidence: <0.0-1.0>
```

### Step 4: Index for Search

```bash
if command -v ao &>/dev/null; then
  ao forge markdown .agents/forge/YYYY-MM-DD-forge.md 2>/dev/null
else
  # Without ao CLI: auto-promote high-confidence candidates to learnings
  mkdir -p .agents/learnings .agents/ao
  for f in .agents/forge/YYYY-MM-DD-*.md; do
    [ -f "$f" ] || continue
    # Extract confidence (numeric or categorical)
    CONF=$(grep -i "confidence:" "$f" | head -1 | awk '{print $NF}')
    # Normalize categorical to numeric: high=0.9, medium=0.6, low=0.3
    case "$CONF" in
      high) CONF_NUM=0.9 ;; medium) CONF_NUM=0.6 ;; low) CONF_NUM=0.3 ;; *) CONF_NUM=$CONF ;;
    esac
    # Auto-promote if confidence >= 0.7
    if (( $(echo "$CONF_NUM >= 0.7" | bc -l) )); then
      cp "$f" .agents/learnings/
      TITLE=$(head -1 "$f" | sed 's/^# //')
      echo "{\"file\": \".agents/learnings/$(basename $f)\", \"title\": \"$TITLE\", \"keywords\": [], \"timestamp\": \"$(date -Iseconds)\"}" >> .agents/ao/search-index.jsonl
      echo "Auto-promoted (confidence $CONF): $(basename $f)"
    fi
  done
  echo "Forge indexing complete (ao CLI not available — high-confidence candidates auto-promoted)"
fi
```

### Step 5: Report Results

Tell the user:
- Number of items extracted by type
- Location of forge output
- Candidates ready for promotion to learnings

## The Quality Pool

Forged candidates enter at Tier 0:
```
Transcript → /forge → .agents/forge/ (Tier 0)
                           ↓
                   Human review or 2+ citations
                   OR auto-promote (confidence >= 0.7, ao-free fallback)
                           ↓
                   .agents/learnings/ (Tier 1)
```

## Key Rules

- **Runs automatically** - usually via hook
- **Extract, don't interpret** - capture what was said
- **Score by confidence** - not all extractions are equal
- **Queue for review** - candidates need validation

## Examples

### SessionEnd Hook Invocation

**Hook triggers:** `session-end.sh` runs when session ends

**What happens:**
1. Hook calls `ao forge transcript --last-session --queue --quiet`
2. CLI analyzes session transcript for decisions, learnings, failures, patterns
3. CLI writes session ID to `.agents/ao/pending.jsonl` queue
4. Next session start triggers `/extract` to process the queue

**Result:** Session transcript automatically queued for knowledge extraction without user action.

### Manual Transcript Mining

**User says:** `/forge <path>` or "mine this transcript for knowledge"

**What happens:**
1. Agent identifies transcript path or uses `ao forge --recent`
2. Agent scans transcript for knowledge patterns (decisions, learnings, failures, patterns)
3. Agent scores each extraction by confidence (0.0-1.0)
4. Agent writes candidates to `.agents/forge/YYYY-MM-DD-forge.md`
5. Agent indexes forge output with `ao forge markdown`
6. Agent reports extraction counts and candidate locations

**Result:** Transcript mined for reusable knowledge, candidates ready for human review or 2+ citations promotion.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| No extractions found | Transcript lacks knowledge signals or ao CLI unavailable | Check transcript contains decisions/learnings; verify ao CLI installed |
| Low confidence scores | Weak signals or vague conversation | Focus sessions on concrete decisions and explicit learnings |
| forge --queue fails | CLI not available or permission error | Manually append to `.agents/ao/pending.jsonl` with session metadata |
| Duplicate forge outputs | Same session forged multiple times | Check forge filenames before writing; ao CLI handles dedup automatically |
