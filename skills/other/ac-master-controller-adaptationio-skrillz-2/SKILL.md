---
name: ac-master-controller
description: Master controller for complete autonomous operation. Use when starting full autonomous projects, managing end-to-end workflow, controlling autonomous lifecycle, or running complete implementations.
---

# AC Master Controller

Master controller for end-to-end autonomous coding.

## Purpose

Provides the highest-level interface for autonomous coding, managing complete project implementations from spec to completion.

## Quick Start

```python
from scripts.master_controller import MasterController

controller = MasterController(project_dir)
result = await controller.run_project(
    spec="Build a REST API with user authentication",
    objective="Complete API implementation"
)
```

## Complete Workflow

```
1. SETUP    → Initialize project and config
2. SPEC     → Generate feature list from spec
3. LOOP     → Run autonomous implementation loop
4. VERIFY   → Final validation
5. REPORT   → Generate completion report
```

## API Reference

See `scripts/master_controller.py` for full implementation.
