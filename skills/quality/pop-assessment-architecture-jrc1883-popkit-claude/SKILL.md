---
name: pop-assessment-architecture
description: "Validates PopKit code quality using concrete metrics for DRY, coupling, cohesion, and architectural patterns"
triggers:
  - assess architecture
  - technical review
  - code quality audit
version: 1.0.0
---

# Architecture Assessment Skill

## Purpose

Provides concrete, reproducible architecture assessment for PopKit plugins using:

- Code duplication detection
- Coupling/cohesion metrics
- Error handling coverage
- Tool usage validation

## How to Use

### Step 1: Run Automated Analysis

```bash
python skills/pop-assessment-architecture/scripts/detect_duplication.py packages/plugin/
python skills/pop-assessment-architecture/scripts/analyze_coupling.py packages/plugin/
python skills/pop-assessment-architecture/scripts/calculate_quality.py packages/plugin/
```

### Step 2: Apply Architecture Checklists

Read and apply checklists in order:

1. `checklists/dry-principles.json` - Duplication detection
2. `checklists/separation-of-concerns.json` - Module boundaries
3. `checklists/error-handling.json` - Error coverage
4. `checklists/tool-selection.json` - Appropriate tool usage

### Step 3: Generate Report

Combine automated analysis with checklist results for final architecture report.

## Standards Reference

| Standard               | File                                  | Key Checks              |
| ---------------------- | ------------------------------------- | ----------------------- |
| DRY Principles         | `standards/dry-principles.md`         | DRY-001 through DRY-008 |
| Separation of Concerns | `standards/separation-of-concerns.md` | SOC-001 through SOC-008 |
| Error Handling         | `standards/error-handling.md`         | EH-001 through EH-010   |
| Tool Selection         | `standards/tool-selection.md`         | TS-001 through TS-008   |

## Quality Metrics

| Metric                | Good | Warning | Critical |
| --------------------- | ---- | ------- | -------- |
| Code Duplication      | <5%  | 5-15%   | >15%     |
| Cyclomatic Complexity | <10  | 10-20   | >20      |
| Module Coupling       | Low  | Medium  | High     |
| Module Cohesion       | High | Medium  | Low      |
| Error Coverage        | >80% | 50-80%  | <50%     |

## SOLID Principles Checks

| Principle             | Check ID  | Description            |
| --------------------- | --------- | ---------------------- |
| Single Responsibility | SOLID-001 | One reason to change   |
| Open/Closed           | SOLID-002 | Open for extension     |
| Liskov Substitution   | SOLID-003 | Proper inheritance     |
| Interface Segregation | SOLID-004 | Minimal interfaces     |
| Dependency Inversion  | SOLID-005 | Depend on abstractions |

## Output

Returns JSON with:

- `quality_score`: 0-100 (higher = better)
- `duplication_percent`: Code duplication level
- `coupling_level`: Low/Medium/High
- `technical_debt`: List of debt items
- `refactoring_suggestions`: Prioritized improvements
