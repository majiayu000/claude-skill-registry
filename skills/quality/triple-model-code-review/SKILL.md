---
name: triple-model-code-review
description: |
  Launch three independent AI code reviewers (Opus, Gemini, Codex) to QA/QC code or notebooks.
  Each reviewer writes findings to separate markdown files, then orchestrator synthesizes.
  Use for critical code review, bug investigation, or quality assurance tasks.

  Triggers: triple review, three model review, independent code review, QAQC, quality assurance,
  multi-model analysis, cross-validation, bug investigation, critical review
---

# Triple Model Code Review

## Overview

This skill launches three independent AI subagents (Opus, Gemini, Codex) to perform parallel code review. Each agent writes findings to markdown files in a workspace directory, then the orchestrator synthesizes a final report.

## When to Use

- Critical bug investigation requiring multiple perspectives
- QA/QC of important notebooks or modules
- Validation of complex logic
- Cross-checking findings before major changes
- When high confidence in analysis is required

## Usage

```
/triple_model_code_review [target] [focus_area]
```

**Examples**:
- `/triple_model_code_review examples/720_precipitation_methods_comprehensive.ipynb "plotting logic"`
- `/triple_model_code_review ras_commander/hdf/HdfResultsPlan.py "return type consistency"`
- `/triple_model_code_review ras_commander/precip/ "API contract validation"`

## Workflow

1. **Create Workspace**: `workspace/{task}QAQC/{opus,gemini,codex,final}-analysis/`

2. **Launch 3 Parallel Subagents**:
   - **Opus** (general-purpose, model=opus): Deep reasoning, architecture analysis
   - **Gemini** (code-oracle-gemini): Large context, multi-file pattern analysis
   - **Codex** (code-oracle-codex): Code archaeology, API contract analysis

3. **Each Agent**:
   - Reads target files independently
   - Writes `qaqc-report.md` to their subfolder
   - Returns file path only (no large text in response)

4. **Orchestrator Synthesizes**:
   - Reads all three reports
   - Identifies consensus findings
   - Creates `FINAL_QAQC_REPORT.md` with agreement matrix

## Subagent Prompts

### Opus Subagent

```
You are conducting an independent QA/QC analysis of [TARGET].

## Critical Issue
[DESCRIBE THE PROBLEM]

## Your Task
1. Read and analyze the target files
2. Identify root cause of the issue
3. Document specific line numbers and code evidence
4. Provide recommended fixes

## Output
Write comprehensive analysis to: workspace/[TASK]QAQC/opus-analysis/qaqc-report.md

Return ONLY the file path when complete.
```

### Gemini Subagent

```
You are conducting an independent QA/QC analysis using large context capabilities.

## Critical Issue
[DESCRIBE THE PROBLEM]

## Your Task
1. Read ALL relevant files in the target area
2. Trace data flow from source to symptom
3. Document column/type confusion if applicable
4. Provide method-by-method analysis

## Output
Write analysis to: workspace/[TASK]QAQC/gemini-analysis/qaqc-report.md

Return ONLY the file path when complete.
```

### Codex Subagent

```
You are conducting deep code analysis for QA/QC.

## Critical Issue
[DESCRIBE THE PROBLEM]

## Your Task
1. Deep analysis of target code
2. Code archaeology - how was bug introduced
3. API contract analysis - promises vs delivery
4. Test cases that would catch this bug

## Output
Write analysis to: workspace/[TASK]QAQC/codex-analysis/qaqc-report.md

Return ONLY the file path when complete.
```

## Output Structure

```
workspace/{task}QAQC/
├── opus-analysis/
│   └── qaqc-report.md      # Deep reasoning analysis
├── gemini-analysis/
│   └── qaqc-report.md      # Large context analysis
├── codex-analysis/
│   └── qaqc-report.md      # Code archaeology analysis
└── final-synthesis/
    └── FINAL_QAQC_REPORT.md  # Consensus findings
```

## Report Template

### Individual Reports

```markdown
# QA/QC Analysis Report: [Target]

**Analyst**: [Model Name]
**Date**: YYYY-MM-DD
**Target**: [file/folder]
**Status**: [CRITICAL/HIGH/MEDIUM/LOW]

## 1. Summary of Findings
## 2. Root Cause Analysis
## 3. Code Evidence (with line numbers)
## 4. Impact Assessment
## 5. Recommended Fixes
## 6. Verification Steps
```

### Final Synthesis

```markdown
# Final QA/QC Synthesis Report

## Executive Summary
## Consensus Bug List
## Agreement Matrix (which reviewers found what)
## Required Fixes (with exact code changes)
## Verification Criteria
```

## Best Practices

1. **Be Specific**: Give clear problem description to all three agents
2. **Parallel Launch**: Launch all three agents in single message for speed
3. **File-Based Communication**: Agents write files, return paths only
4. **Consensus Focus**: Weight findings by agreement across reviewers
5. **Preserve Evidence**: Keep all reports in workspace for audit trail

## Example Session

```
User: /triple_model_code_review examples/720_precipitation_methods_comprehensive.ipynb "incremental vs cumulative confusion"

Claude: Creating workspace and launching 3 independent reviewers...

[Launches Opus, Gemini, Codex in parallel]

All three reviewers identified the same bugs:
- Line 810: DataFrame passed instead of column
- Line 1396: DataFrame passed instead of column
- Lines 1777-1789: np.cumsum on DataFrame

Reports saved to workspace/notebook720QAQC/
```

## See Also

- **Subagent Output Pattern**: `.claude/rules/subagent-output-pattern.md`
- **Agent Integration Testing**: `.claude/rules/testing/agent-integration-testing.md`
- **Orchestrator Pattern**: Root `CLAUDE.md` - Orchestrator section
