---
name: niche-validator
description: Scrapes Reddit/forums to find "complaint clusters" and scores niche viability.
---

# Niche Validator

This skill validates a business idea by analyzing market pain points and complaint clusters.

## Input Variables
- [NICHE_IDEA] (The initial product or market idea)

## The Protocol
1.  **Complaint Cluster Discovery**: Search online communities (Reddit, Forums) for specific phrases like "I hate when...", "Why does X always...", "worst part about X".
2.  **Pain Point Analysis**: Categorize the complaints into themes.
3.  **Viability Scoring**: Score the niche on:
    - **Pain Intensity**: How much does it hurt? (1-10)
    - **Purchasing Power**: Does this audience spend money? (1-10)
    - **Market Size**: Is the audience reachable? (1-10)
    - **Competition Gap**: Is there an obvious lack of good solutions? (1-10)
4.  **Verdict**: Go / No-Go recommendation.

## Output Instructions
Render into `templates/niche-viability-report.md`.


## Integration & Technical Specs

### API Specification
- **ID**: `niche-validator`
- **Path**: `skills/niche-validator/templates/niche-viability-report.md`
- **Context**: Part of *Strategy & Management*

### Data Flow
- **Input**: Derived from project context and upstream skills.
- **Output**: Generates `niche-viability-report.md`.

### CLI Usage
```bash
bun scripts/cli.ts activate niche-validator
```
