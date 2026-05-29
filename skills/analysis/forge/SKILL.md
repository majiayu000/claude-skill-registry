---
name: forge
description: 'Mine transcripts for knowledge - decisions, learnings, failures, patterns. Triggers: "forge insights", "mine transcripts", "extract knowledge".'
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
ao forge index .agents/forge/YYYY-MM-DD-forge.md 2>/dev/null
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
                           ↓
                   .agents/learnings/ (Tier 1)
```

## Key Rules

- **Runs automatically** - usually via hook
- **Extract, don't interpret** - capture what was said
- **Score by confidence** - not all extractions are equal
- **Queue for review** - candidates need validation
