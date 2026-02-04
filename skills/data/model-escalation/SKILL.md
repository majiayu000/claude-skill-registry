---
name: model-escalation
description: Automatic model switching based on task complexity for OpenClaw agents. Dynamically escalates between Haiku (simple), Sonnet (medium), and Opus (complex) models. Tracks prefix consistency ([H], [S], [O]) and logs discrepancies. USE WHEN configuring multi-model agents, optimizing API costs, or implementing complexity-based model routing.
---

# Model Escalation

**Canonical implementation:** `Tools/model_escalator_v2.py`

Complexity-based model switching with prefix tracking for OpenClaw agents.

## Quick Start

```python
from Tools.model_escalator_v2 import model_escalation_hook_v2 as model_escalation_hook

# Determine model from conversation context
result = model_escalation_hook("main-session", {
    "messages": [],
    "current_message": "Explain this API integration",
    "token_count": 0,
})
session_status(model=result.model)
```

## Complexity Thresholds

| Range | Model | Prefix | Use Cases |
|-------|-------|--------|-----------|
| 0-0.25 | Haiku | [H] | Simple questions, confirmations, chat |
| 0.25-0.75 | Sonnet | [S] | Code, debugging, API integration |
| 0.75-1.0 | Opus | [O] | Architecture, complex algorithms, strategic planning |

## High Complexity Indicators (Opus)

- System architecture design
- Distributed systems
- Multi-step technical implementations
- Deep code reviews
- Strategic planning with tradeoffs
- "Implement X mechanism/system" requests

## Prefix Tracking

Ensures conversation prefix matches active model:

```python
from Tools.model_prefix_tracker import ModelPrefixTracker

tracker = ModelPrefixTracker()

# Validate and correct prefix
correction = tracker.correct_prefix(
    session_id='main',
    current_prefix='[S]',
    current_model='anthropic/claude-opus-4-5'
)
# Returns '[O]' if mismatch detected
```

Logs all discrepancies to SQLite for analysis.

## Integration with AGENTS.md

Add to your agent's AGENTS.md:

```markdown
## Model Self-Check

At response START, assess complexity:
- High (0.75+) → `session_status(model="anthropic/claude-opus-4-5")`
- Medium (0.25-0.75) → `session_status(model="anthropic/claude-sonnet-4-5")`
- Low (<0.25) → Stay on Haiku

Prefix responses with [H], [S], or [O] to match model.
```

## Configuration

Edit `scripts/config.json` to customize:

```json
{
  "thresholds": {
    "low": 0.25,
    "high": 0.75
  },
  "models": {
    "haiku": "anthropic/claude-3-5-haiku-20241022",
    "sonnet": "anthropic/claude-sonnet-4-5",
    "opus": "anthropic/claude-opus-4-5"
  },
  "cooldown_minutes": 5
}
```

## Database Schema

Prefix tracking logs stored in SQLite:

```sql
-- prefix_log table
timestamp REAL,
session_id TEXT,
detected_prefix TEXT,
actual_model TEXT,
correction_applied INTEGER
```

Query discrepancies:
```bash
sqlite3 model_prefix_state.db "SELECT * FROM prefix_log WHERE correction_applied=1;"
```
