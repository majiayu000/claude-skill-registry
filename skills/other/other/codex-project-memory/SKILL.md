---
name: codex-project-memory
description: Tracks project knowledge, decisions, and patterns across sessions
load_priority: on-demand
---

## TL;DR
11 scripts for project knowledge persistence. Decision tree: Log -> decision/feedback/skill-usage. Generate -> changelog/session-summary/handoff/growth-report. Analyze -> patterns/knowledge-graph/project-genome. Maintain -> compact old context. Triggers: `$changelog`, `$growth-report`, `$session-summary`, `$log-decision`, `$compact-context`, `$codex-genome`.

# Codex Project Memory

## Activation

1. Activate after complex tasks involving architecture, design decisions, or refactors.
2. Activate on explicit `$codex-project-memory` or `$memory`.
3. Activate on explicit command `$log-decision`.
4. Activate on `$handoff` or when user asks to generate handoff context.
5. Activate on `$session-summary` or when user asks to summarize a coding session.
6. Activate on `$analyze-patterns` or "learn project style".
7. Activate on `$log-feedback` or "track my fix".
8. Activate on `$feedback-summary` for aggregated feedback recall.
9. Activate on `$skill-track` to record skill usage analytics.
10. Activate on `$skill-report` to generate skill evolution report.
11. Activate on `$build-graph` or "map project" to generate project knowledge graph.
12. Activate on `$changelog` to generate release-oriented commit summaries.
13. Activate on `$growth-report` to generate a developer growth report.
14. Activate on `$compact-context` or "clean up old sessions".
15. Activate on `$codex-genome`, `$generate-genome`, or `$genome` to create layered project context docs.

## Decision Tree Routing

```
User intent -> Memory action?
    |- Log/record -> What?
    |   |- Decision -> decision_logger.py
    |   |- Feedback -> track_feedback.py
    |   `- Skill usage -> track_skill_usage.py
    |
    |- Generate/export -> What?
    |   |- Handoff -> generate_handoff.py
    |   |- Session recap -> generate_session_summary.py
    |   |- Changelog -> generate_changelog.py
    |   `- Growth report -> generate_growth_report.py
    |
    |- Analyze -> What?
    |   |- Patterns -> analyze_patterns.py
    |   |- Dependencies -> build_knowledge_graph.py
    |   `- Context genome -> generate_genome.py
    |
    |- Maintain -> What?
    |   `- Compact old memory -> compact_context.py
    |
    `- Not memory -> skip
```

## Rules

- Use the decision tree to choose one memory action before invoking scripts.
- Run `--help` before invoking helper scripts and treat them as black-box tools unless customization or bug fixing is required.
- Review existing files in `.codex/decisions/` before logging a similar technical choice.
- Use the default output paths and chaining guidance from `references/behavior-guide.md` unless the user requests overrides.
- Return the created path plus the headline metrics from each script JSON payload.
- Xem `skills/.system/REGISTRY.md` để biết đường dẫn đầy đủ.

## Reference Files

- `references/decision-journal-spec.md`: decision logging criteria and naming conventions.
- `references/handoff-spec.md`: handoff usage guidance.
- `references/session-summary-spec.md`: session summary workflow and retention guidance.
- `references/changelog-spec.md`: release-focused changelog generation rules.
- `references/growth-report-spec.md`: developer growth analytics and reporting behavior.
- `references/pattern-learner-spec.md`: project style learning behavior.
- `references/feedback-tracker-spec.md`: feedback logging and aggregate usage.
- `references/skill-evolution-spec.md`: skill usage analytics and optimization.
- `references/knowledge-graph-spec.md`: deep architecture mapping and refresh guidance.
- `references/context-compactor-spec.md`: retention policy, archive layout, and dry-run expectations.
- `references/behavior-guide.md`: detailed per-script behaviors, defaults, and chaining guidance.
- `references/script-commands.md`
- `references/output-schemas.md`
