---
name: ac-stop-hook-analyzer
description: Analyze context and decide on continuation via Stop hook. Use when determining if work should continue, analyzing completion status, making continuation decisions, or implementing the Two-Claude pattern.
---

# AC Stop Hook Analyzer

Analyze context to decide on continuation (Two-Claude Pattern).

## Purpose

Implements the Analyzer role in the Two-Claude Pattern, using Opus 4.5 to intelligently decide whether to continue autonomous operation.

## Quick Start

```python
from scripts.stop_hook_analyzer import StopHookAnalyzer

analyzer = StopHookAnalyzer(project_dir)
decision = await analyzer.should_continue()
# Returns: {"decision": "block", "reason": "Continue with api-003"}
```

## Decision Logic

- Check completion against objective
- Analyze remaining features
- Validate safety limits
- Return continue/stop decision

## API Reference

See `scripts/stop_hook_analyzer.py` for full implementation.
