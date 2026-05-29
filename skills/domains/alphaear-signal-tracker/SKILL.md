---
name: alphaear-signal-tracker
description: Track investment signal evolution and update logic based on new information. Use when monitoring signals and determining if they are strengthened, weakened, or falsified.
---

# AlphaEar Signal Tracker Skill

## Overview

This skill provides logic to track and update investment signals. It assesses how new market information impacts existing signals (Strengthened, Weakened, Falsified, or Unchanged).

## Capabilities

### 1. Track Signal Evolution

Use `scripts/fin_agent.py` logic (referencing the `track_signal` method pattern) to update signals.

**Key Logic:**

-   **Input**: Existing Signal State + New Information (News/Price).
-   **Process**:
    1.  Compare new info with signal thesis.
    2.  Determine impact direction (Positive/Negative/Neutral).
    3.  Update confidence and intensity.
-   **Output**: Updated Signal.

**Example Usage (Conceptual):**

```python
# This skill is currently a pattern extracted from FinAgent.
# In a future refactor, it should be a standalone utility class.
# For now, refer to `scripts/fin_agent.py`'s `track_signal` method implementation.
```

## Dependencies

-   `agno` (Agent framework)
-   `sqlite3` (built-in)

Ensure `DatabaseManager` is initialized correctly.
