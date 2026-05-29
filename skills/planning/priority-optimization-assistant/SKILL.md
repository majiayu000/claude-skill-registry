---
name: priority-optimization-assistant
description: Analyzes project tasks by priority levels, generates optimization checklists, executes selected optimizations with quality assurance, and produces detailed reports for software development and project management.
---

# Priority Optimization Assistant

This skill helps optimize projects and tasks by intelligently prioritizing issues, creating actionable checklists, offering flexible execution options, performing optimizations, and generating comprehensive reports.

## Capabilities

- **Priority Analysis**: Automatically categorizes tasks into high, medium, and low priority based on impact, urgency, effort, and dependencies.
- **Checklist Generation**: Creates detailed, actionable optimization checklists with estimated effort and expected benefits.
- **Interactive Selection**: Offers users options to execute all optimizations, by priority level, or individual items.
- **Optimization Execution**: Simulates or generates code/text optimizations, performs quality checks, and validates improvements.
- **Report Generation**: Produces professional reports with before/after comparisons, impact metrics, and next-step recommendations.

## Input Requirements

- **Project/Task Description**: Text description of the project, code issues, or tasks to optimize.
- **Current State**: Optional code snippets, file contents, or JSON list of tasks (e.g., [{"task": "Fix slow query", "details": "..."}]).
- **User Preferences**: Optional JSON with preferences like {"focus": "performance", "constraints": "time-limited"}.
- **Format**: Natural language or structured JSON.

## Output Formats

- **Interactive Menu**: Markdown table or numbered list for selection.
- **Execution Results**: Generated optimizations (code diffs, refactored snippets), quality assurance logs.
- **Report**: Markdown/PDF-ready report with sections: Summary, Checklist, Executions, Metrics, Recommendations.
- **Metrics**: Effort saved, impact score, completion status.

## How to Use

@priority-optimization-assistant Analyze this codebase for performance optimizations and create a prioritized checklist.

Provide a project description or paste code/files, then select from options like "Execute high priority only".

## Scripts

- `priority_optimization_engine.py`: Core engine with PriorityAnalyzer, OptimizationPlanner, OptimizationExecutor, and ReportGenerator classes. Orchestrates the full workflow.

## Best Practices

1. Provide detailed project context for accurate prioritization.
2. Use structured task lists for complex projects.
3. Review interactive options before execution.
4. Iterate: Use reports to refine future optimizations.
5. Combine with code-review skills for deeper analysis.

## Limitations

- Prioritization is heuristic-based; domain expertise may override.
- Executions are generative (code suggestions); manual verification needed for production.
- Best for software/dev tasks; adapt prompts for other domains.
- Does not modify files directly—outputs diffs/plans for application.
