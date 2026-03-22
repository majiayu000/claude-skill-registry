---
name: ac-autonomous-orchestrator
description: Main orchestrator for autonomous coding operations. Use when running autonomous sessions, coordinating components, managing the full lifecycle, or orchestrating implementations.
---

# AC Autonomous Orchestrator

Main orchestrator for autonomous coding operations.

## Purpose

Coordinates all autonomous coding components, managing the complete lifecycle from initialization through feature completion.

## Quick Start

```python
from scripts.autonomous_orchestrator import AutonomousOrchestrator

orchestrator = AutonomousOrchestrator(project_dir)
await orchestrator.initialize(objective="Build user authentication")
result = await orchestrator.run()
```

## Orchestration Flow

```
1. INIT      → Load config, setup session
2. PLAN      → Generate/load feature list
3. EXECUTE   → TDD implementation loop
4. VALIDATE  → QA review and validation
5. COMMIT    → Git commit changes
6. CONTINUE  → Next feature or handoff
```

## Integration

Coordinates all AC skills for unified operation.

## API Reference

See `scripts/autonomous_orchestrator.py` for full implementation.
