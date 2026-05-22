---
name: code-refactoring-assistant
description: Analyzes codebases by impact scope (low/medium/high), generates refactoring checklists, supports interactive review, executes refactors with QA, and produces detailed optimization reports.
---

# Code Refactoring Assistant

This skill is a comprehensive tool for safe code refactoring. It analyzes codebase changes by impact scope, creates prioritized checklists, facilitates user review, executes approved refactors, performs quality assurance, and generates before/after reports with metrics.

Distinguished from priority optimizers: Focuses on *impact scope* (files/modules/deps/tests) rather than business priority, with richer interactive review (yes/no/back/feedback).

## Capabilities

- **Impact Analysis**: Assess refactoring scope (low: &lt;5 files/local; medium: 5-20 files/module; high: &gt;20 files/cross-module/deps)
- **Checklist Generation**: Structured lists grouped by impact, with risks and benefits
- **Interactive Review**: yes/no/back/other feedback per item
- **Refactor Execution**: Apply changes to files with git diffs
- **QA Validation**: Check style, tests, coverage, performance
- **Reporting**: Before/after comparisons, metrics delta, visualizations

## Input Requirements

JSON format:
- `codebase`: {`files`: [{`path`, `lines`, `deps`}], `tests`: [...], `goals`: ["improve modularity", "reduce complexity"]}
- `metrics`: Optional baseline (coverage %, perf ms)
- Data from Claude tools (Glob/Grep/Bash git status)

Quality: Accurate file lists, recent git state.

## Output Formats

- `checklist.json`: Items with id/impact/desc/risks
- `review_decisions.json`: User choices per item
- `changes.diff`: Executed diffs
- `qa_report.json`: Pass/fail metrics
- `final_report.md`: Full comparison (tables, charts)

## How to Use

@[code-refactoring-assistant] Analyze current repo for low-impact refactors to improve modularity, then review checklist.

## Scripts

- `refactoring_assistant.py`: Orchestrates 6 core classes (ImpactAnalyzer, RefactoringPlanner, ReviewInterface, RefactoringExecutor, QAValidator, RefactoringReporter)

## Best Practices

1. Start with low-impact items
2. Backup repo (git stash/branch) before execution
3. Provide test paths for accurate QA
4. Review high-impact manually
5. Iterate: Refactor → QA → Report → Re-analyze

## Limitations

- Relies on Claude tools for real file access (no direct FS write)
- Simulated execution in samples; real uses git/Bash tools
- Complex deploys need human oversight
- Python sandbox limits (no external libs beyond std)
