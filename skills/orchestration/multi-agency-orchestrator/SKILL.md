---
name: multi-agency-orchestrator
description: "Coordinate operations across RIM, CKVC, BOM, JPAL, JLI, JAP, LAS, RMQB agencies"
---

# Multi-Agency Orchestrator
Handle Finance SSC operations across 8 agencies.

## What This Does
- Agency routing logic
- Consolidated reporting
- Intercompany elimination
- Cross-agency workflows
- Variance analysis

## Quick Example
```python
for agency in ['RIM', 'CKVC', 'BOM', 'JPAL']:
    close_month_end(agency, '2025-10')
consolidate_financials()
```

## Getting Started
"Close books for all agencies"
"Consolidate Q3 financials"
