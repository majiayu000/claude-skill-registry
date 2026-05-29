---
name: pop-assessment-ux
description: "Evaluates PopKit user experience using concrete heuristics for command naming, error messages, and interaction patterns"
triggers:
  - assess ux
  - ux review
  - usability audit
version: 1.0.0
---

# UX Assessment Skill

## Purpose

Provides concrete, reproducible UX assessment for PopKit plugins using:

- Nielsen's 10 Usability Heuristics
- Command naming conventions checklist
- Error message quality standards
- AskUserQuestion usage validation

## How to Use

### Step 1: Run Automated UX Scan

```bash
python skills/pop-assessment-ux/scripts/analyze_commands.py packages/plugin/
python skills/pop-assessment-ux/scripts/analyze_errors.py packages/plugin/
python skills/pop-assessment-ux/scripts/calculate_ux_score.py packages/plugin/
```

### Step 2: Apply UX Checklists

Read and apply checklists in order:

1. `checklists/command-naming.json` - Naming conventions
2. `checklists/error-messages.json` - Error quality
3. `checklists/interaction-patterns.json` - UX consistency
4. `checklists/nielsen-heuristics.json` - 10 heuristics

### Step 3: Generate Report

Combine automated analysis with checklist results for final UX report.

## Standards Reference

| Standard             | File                                | Key Checks            |
| -------------------- | ----------------------------------- | --------------------- |
| Command Naming       | `standards/command-naming.md`       | CN-001 through CN-008 |
| Error Messages       | `standards/error-messages.md`       | EM-001 through EM-008 |
| Interaction Patterns | `standards/interaction-patterns.md` | IP-001 through IP-010 |
| Cognitive Load       | `standards/cognitive-load.md`       | CL-001 through CL-006 |

## UX Heuristics (Nielsen)

| #   | Heuristic                           | Check ID |
| --- | ----------------------------------- | -------- |
| 1   | Visibility of system status         | NH-001   |
| 2   | Match between system and real world | NH-002   |
| 3   | User control and freedom            | NH-003   |
| 4   | Consistency and standards           | NH-004   |
| 5   | Error prevention                    | NH-005   |
| 6   | Recognition rather than recall      | NH-006   |
| 7   | Flexibility and efficiency of use   | NH-007   |
| 8   | Aesthetic and minimalist design     | NH-008   |
| 9   | Help users recognize and recover    | NH-009   |
| 10  | Help and documentation              | NH-010   |

## Output

Returns JSON with:

- `ux_score`: 0-100 (higher = better)
- `heuristic_scores`: Per-heuristic ratings
- `naming_issues`: Command naming problems
- `error_issues`: Error message problems
- `recommendations`: UX improvements
