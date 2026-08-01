---
name: mine-transcripts
description: Mine real human conversations from CLI agents for bridge classifier training.
---

---
name: mine-transcripts
description: >
  Mine real human CLI conversation transcripts into labeled training data for
  bridge/classifier improvement.
triggers:
  - mine transcripts
  - extract training data
  - mine conversations
allowed-tools:
  - Bash
  - Read
metadata:
  short-description: Mine CLI transcripts for classifier training

provides:
  - mine-transcripts
composes: [, task-monitor]
---

# mine-transcripts

Mine real human conversations from CLI agents for bridge classifier training.

## Purpose

Train the bridge classifier on REAL human communication patterns, not synthetic templates. This enables personas like Embry to find the RIGHT experts when using /ask.

**Two-tier training approach:**
1. **Developer (Graham)** - baseline attunement to real communication patterns
2. **Client** - specific adaptation to individual users

## Integration

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATA SOURCES                                 │
├─────────────────────────────────────────────────────────────────┤
│  ~/.claude/projects/     Claude CLI conversations              │
│  ~/.codex/history.jsonl  Codex CLI (pure human input!)         │
│  ~/.codex/sessions/      Codex session transcripts             │
│  ~/.gemini/              Gemini CLI (if exists)                │
│  ~/.pi/                  Pi CLI (if exists)                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    /mine-transcripts                            │
├─────────────────────────────────────────────────────────────────┤
│  1. Extract real human messages (filter system prompts)        │
│  2. Label with /taxonomy bridge extraction                     │
│  3. Detect emotional state (satisfied/frustrated)              │
│  4. Deduplicate against /memory                                │
│  5. Store unique examples for classifier training              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              /create-classifier (bridge classifier)            │
│                              │                                  │
│                              ▼                                  │
│                      persona_router.py                          │
│                              │                                  │
│                              ▼                                  │
│                    Embry /asks the RIGHT personas               │
└─────────────────────────────────────────────────────────────────┘
```

## Dependencies

- **/taxonomy** - Bridge label extraction (Precision, Resilience, Fragility, Corruption, Loyalty, Stealth)
- **/memory** - Deduplication against existing lessons, optional storage
- **/episodic-archiver** - Emotional context from archived sessions
- **/scheduler** - Nightly runs

## Usage

```bash
# Mine from all CLI agents
./run.sh mine --all-agents

# Mine with deduplication against existing training data
./run.sh mine --all-agents --dedupe

# Mine and store to memory (creates lessons)
./run.sh mine --all-agents --store-memory

# Analyze coverage of existing training data
./run.sh analyze data/mined.jsonl

# Export for human review
./run.sh export --sample 500 --output for_review.jsonl
```

## Output

Training data in JSONL format:
```json
{"text": "the font size is too small for 10ft viewing", "labels": ["Precision", "Fragility"]}
{"text": "perfect, that fixed the issue!", "labels": ["Resilience", "Loyalty"]}
```

## Emotional Context

Messages are enriched with emotional detection:
- **Satisfied** signals → Resilience, Loyalty bridges
- **Frustrated** signals → Fragility bridge
- **High satisfaction** → Both Resilience AND Loyalty

This helps the classifier understand that "works great!" indicates system resilience and good collaboration (Loyalty).

## Scheduler Integration

Registered as `transcript-mining-nightly`:
- Runs at 4:30am daily
- Deduplicates against existing training data
- Feeds into `bridge-classifier-retrain` at 5am

## Triggers

- `mine transcripts`
- `extract training data`
- `mine conversations`
- Nightly via /scheduler
