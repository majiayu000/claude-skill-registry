---
name: codex-project-memory
description: Tracks project knowledge, decisions, and patterns across sessions
load_priority: on-demand
---

## TL;DR
10 scripts for project knowledge persistence. Decision tree: Log -> decision/feedback/skill-usage. Generate -> changelog/session-summary/handoff/growth-report. Analyze -> patterns/knowledge-graph. Maintain -> compact old context. Triggers: `$changelog`, `$growth-report`, `$session-summary`, `$log-decision`, `$compact-context`.

# Codex Project Memory

## Activation

1. Activate after complex tasks involving architecture, design decisions, or refactors.
2. Activate on explicit command `$log-decision`.
3. Activate on `$handoff` or when user asks to generate handoff context.
4. Activate on `$session-summary` or when user asks to summarize a coding session.
5. Activate on `$analyze-patterns` or "learn project style".
6. Activate on `$log-feedback` or "track my fix".
7. Activate on `$feedback-summary` for aggregated feedback recall.
8. Activate on `$skill-track` to record skill usage analytics.
9. Activate on `$skill-report` to generate skill evolution report.
10. Activate on `$build-graph` or "map project" to generate project knowledge graph.
11. Activate on `$changelog` to generate release-oriented commit summaries.
12. Activate on `$growth-report` to generate a developer growth report.
13. Activate on `$compact-context` or "clean up old sessions".

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
    |   `- Dependencies -> build_knowledge_graph.py
    |
    |- Maintain -> What?
    |   `- Compact old memory -> compact_context.py
    |
    `- Not memory -> skip
```

## Behavior

### Decision Logger

1. Collect decision details:
   - `title`
   - `decision`
   - `alternatives`
   - `reasoning`
   - `context`
2. Run `scripts/decision_logger.py` to persist the record under project `.codex/decisions/`.
3. Return created file path and confirmation summary.
4. Before making similar decisions, review existing files in `.codex/decisions/`.

### Context Handoff Generator

1. Trigger when user needs portable project context for another AI or teammate.
2. Run `scripts/generate_handoff.py`.
3. Default output: `<project-root>/.codex/handoff.md`.
4. Return output path, section count, and file size from script JSON.

### Session Summary Generator

1. Trigger when user requests end-of-session summary.
2. Run `scripts/generate_session_summary.py`.
3. Default output directory: `<project-root>/.codex/sessions/`.
4. Return output path, commit count, and changed file count from script JSON.

### Changelog Generator

1. Trigger when user asks for release notes or changelog generation.
2. Run `scripts/generate_changelog.py`.
3. Default source range: latest tag or last 30 days.
4. Return categorized markdown output and summary JSON.

### Growth Report Generator

1. Trigger when user asks for learning trends or improvement planning.
2. Run `scripts/generate_growth_report.py`.
3. Aggregate feedback, sessions, and usage analytics.
4. Return report path and prioritized improvement areas.

### Pattern Learner

1. Trigger when user asks to learn project coding conventions.
2. Run `scripts/analyze_patterns.py`.
3. Default output: `<project-root>/.codex/project-profile.json`.
4. Return generated profile with naming, structure, import style, and pattern detection.

### Feedback Tracker

1. Trigger when user asks to record AI-vs-user fix deltas.
2. Run `scripts/track_feedback.py` with category and fix context.
3. Persist entries under `<project-root>/.codex/feedback/`.
4. On `$feedback-summary`, run `scripts/track_feedback.py --aggregate` and return trend summary.

### Skill Evolution Tracker

1. Trigger when user asks to track skill performance across tasks.
2. Run `scripts/track_skill_usage.py --record` for single usage entries.
3. Run `scripts/track_skill_usage.py --report` for aggregate effectiveness analysis.
4. Use report output to identify underperforming or unused skills.

### Knowledge Graph Builder

1. Trigger when user asks for deep project structure mapping.
2. Run `scripts/build_knowledge_graph.py`.
3. Default output: `<project-root>/.codex/knowledge-graph.json`.
4. Before complex refactors, read `knowledge-graph.json` first to understand boundaries and dependencies.

### Chaining Guidance

1. Log major technical choices via `decision_logger.py`.
2. Generate release communication via `generate_changelog.py`.
3. Keep continuity via `generate_session_summary.py`.
4. Track long-term improvement via `generate_growth_report.py`.

## Script Invocation Discipline

1. Always run `--help` before invoking a script.
2. Treat scripts as black-box helpers and prefer direct execution over source inspection.
3. Read script source only when customization or bug fixing is required.

## Execution Command

### Decision Logger

- Windows:
  `python "$env:USERPROFILE\\.codex\\skills\\codex-project-memory\\scripts\\decision_logger.py" --project-root <path> --title <slug> --decision <text> --alternatives <text> --reasoning <text> --context <text>`
- macOS/Linux:
  `python "$HOME/.codex/skills/codex-project-memory/scripts/decision_logger.py" --project-root <path> --title <slug> --decision <text> --alternatives <text> --reasoning <text> --context <text>`

### Context Handoff Generator

- Windows:
  `python "$env:USERPROFILE\\.codex\\skills\\codex-project-memory\\scripts\\generate_handoff.py" --project-root <path>`
- macOS/Linux:
  `python "$HOME/.codex/skills/codex-project-memory/scripts/generate_handoff.py" --project-root <path>`

### Session Summary Generator

- Windows:
  `python "$env:USERPROFILE\\.codex\\skills\\codex-project-memory\\scripts\\generate_session_summary.py" --project-root <path> --since today`
- macOS/Linux:
  `python "$HOME/.codex/skills/codex-project-memory/scripts/generate_session_summary.py" --project-root <path> --since today`

### Changelog Generator

- Windows:
  `python "$env:USERPROFILE\\.codex\\skills\\codex-project-memory\\scripts\\generate_changelog.py" --project-root <path> --since "30 days ago"`
- macOS/Linux:
  `python "$HOME/.codex/skills/codex-project-memory/scripts/generate_changelog.py" --project-root <path> --since "30 days ago"`

### Growth Report Generator

- Windows:
  `python "$env:USERPROFILE\\.codex\\skills\\codex-project-memory\\scripts\\generate_growth_report.py" --project-root <path> --skills-root "$env:USERPROFILE\\.codex\\skills"`
- macOS/Linux:
  `python "$HOME/.codex/skills/codex-project-memory/scripts/generate_growth_report.py" --project-root <path> --skills-root "$HOME/.codex/skills"`

### Pattern Learner

- Windows:
  `python "$env:USERPROFILE\\.codex\\skills\\codex-project-memory\\scripts\\analyze_patterns.py" --project-root <path>`
- macOS/Linux:
  `python "$HOME/.codex/skills/codex-project-memory/scripts/analyze_patterns.py" --project-root <path>`

### Feedback Tracker

- Windows:
  `python "$env:USERPROFILE\\.codex\\skills\\codex-project-memory\\scripts\\track_feedback.py" --project-root <path> --file <file> --ai-version <text> --user-fix <text> --category <category>`
- macOS/Linux:
  `python "$HOME/.codex/skills/codex-project-memory/scripts/track_feedback.py" --project-root <path> --file <file> --ai-version <text> --user-fix <text> --category <category>`
- Aggregate:
  `python ".../track_feedback.py" --project-root <path> --aggregate`

### Skill Evolution Tracker

- Windows:
  `python "$env:USERPROFILE\\.codex\\skills\\codex-project-memory\\scripts\\track_skill_usage.py" --skills-root "$env:USERPROFILE\\.codex\\skills" --record --skill <skill-name> --task <task> --outcome <success|partial|failed> --notes <text>`
- Report:
  `python "$env:USERPROFILE\\.codex\\skills\\codex-project-memory\\scripts\\track_skill_usage.py" --skills-root "$env:USERPROFILE\\.codex\\skills" --report`

### Knowledge Graph Builder

- Windows:
  `python "$env:USERPROFILE\\.codex\\skills\\codex-project-memory\\scripts\\build_knowledge_graph.py" --project-root <path>`
- macOS/Linux:
  `python "$HOME/.codex/skills/codex-project-memory/scripts/build_knowledge_graph.py" --project-root <path>`

### Context Compactor

- Windows:
  `python "$env:USERPROFILE\\.codex\\skills\\codex-project-memory\\scripts\\compact_context.py" --project-root <path> --max-age-days 90 --keep-latest 5`
- macOS/Linux:
  `python "$HOME/.codex/skills/codex-project-memory/scripts/compact_context.py" --project-root <path> --max-age-days 90 --keep-latest 5`
- Dry run:
  `python ".../compact_context.py" --project-root <path> --dry-run`

## Output Contract

Success JSON:

```json
{
  "status": "logged",
  "path": "<project-root>/.codex/decisions/YYYY-MM-DD-<slug>.md",
  "title": "<title>"
}
```

Error JSON:

```json
{
  "status": "error",
  "path": "",
  "title": "<title>",
  "message": "<error details>"
}
```

### Per-Script Output Schemas

| Script | `status` on success | Key fields |
| --- | --- | --- |
| `decision_logger.py` | `"logged"` | `path`, `title` |
| `generate_session_summary.py` | `"generated"` | `path`, `commits`, `files_changed` |
| `generate_handoff.py` | `"generated"` | `path`, `sections` |
| `generate_changelog.py` | `"generated"` | `path`, `entries` |
| `generate_growth_report.py` | `"generated"` | `path`, `metrics` |
| `analyze_patterns.py` | `"generated"` | `path`, `patterns` |
| `build_knowledge_graph.py` | `"generated"` | `path`, `stats` |
| `track_feedback.py` (log) | `"logged"` | `path`, `category` |
| `track_feedback.py` (aggregate) | `"aggregated"` | `total`, `by_category` |
| `track_skill_usage.py` (record) | `"recorded"` | `skill`, `outcome` |
| `track_skill_usage.py` (report) | `"report"` | `total_entries`, `by_skill` |
| `compact_context.py` | `"compacted"` | `sessions_archived`, `feedback_archived`, `bytes_freed` |

All scripts emit `{"status": "error", "message": "..."}` on failure.

#### Detailed Examples

#### generate_session_summary.py

```json
{"status": "generated", "path": "<file>", "commits": <int>, "files_changed": <int>}
```

#### generate_handoff.py

```json
{"status": "generated", "path": "<file>", "sections": <int>, "size_bytes": <int>, "warnings": [<string>]}
```

#### generate_changelog.py

```json
{"status": "generated", "version": "<string>", "since": "<string>", "total_commits": <int>, "categories": {<object>}, "path": "<file-or-empty>", "changelog_markdown": "<markdown>"}
```

#### generate_growth_report.py

```json
{"status": "generated", "path": "<file>", "improvement_areas": <int>, "sessions_analyzed": <int>, "warnings": [<string>]}
```

#### analyze_patterns.py

```json
{"status": "generated", "path": "<file>", "profile": {<object>}, "warnings": [<string>]}
```

#### track_feedback.py

```json
{"status": "logged", "path": "<file>", "file": "<string>", "category": "<string>", "severity": "<string>"}
```

Aggregate mode:

```json
{"total_feedback": <int>, "by_category": {<object>}, "by_severity": {<object>}, "top_files": [<object>], "recent": [<object>], "patterns": "<string>"}
```

#### track_skill_usage.py

```json
{"status": "recorded", "path": "<file>", "entry": {"date": "<YYYY-MM-DD>", "skill": "<name>", "task": "<task>", "outcome": "<success|partial|failed>", "notes": "<string>", "duration_estimate": "<string>"}, "skills_root": "<path>"}
```

Report mode:

```json
{"status": "report_ready", "total_usages": <int>, "period": {"from": "<YYYY-MM-DD>", "to": "<YYYY-MM-DD>"}, "by_skill": {<object>}, "unused_skills": [<string>], "most_effective": "<string>", "least_effective": "<string>", "recommendations": [<string>], "trends": {"overall_success_rate": <float>, "direction": "<improving|stable|declining>"}, "warnings": [<string>]}
```

#### build_knowledge_graph.py

```json
{"status": "generated", "path": "<file>", "generated_at": "<iso8601>", "project_root": "<path>", "stats": {"total_files": <int>, "total_edges": <int>, "modules": <int>, "routes": <int>, "models": <int>, "circular_dependencies": <int>}, "file_dependencies": {<object>}, "module_boundaries": {<object>}, "api_routes": {<object>}, "data_models": {<object>}, "circular_dependencies": [<object>], "warnings": [<string>]}
```

#### compact_context.py

```json
{"status": "compacted", "sessions_archived": <int>, "feedback_archived": <int>, "decisions_kept": <int>, "bytes_freed": <int>}
```

## Reference

Read:
- `references/decision-journal-spec.md` for decision logging criteria and naming conventions.
- `references/handoff-spec.md` for handoff usage guidance.
- `references/session-summary-spec.md` for session summary workflow and retention guidance.
- `references/changelog-spec.md` for release-focused changelog generation rules.
- `references/growth-report-spec.md` for developer growth analytics/reporting behavior.
- `references/pattern-learner-spec.md` for project style learning behavior.
- `references/feedback-tracker-spec.md` for feedback logging and aggregate usage.
- `references/skill-evolution-spec.md` for skill usage analytics and optimization.
- `references/knowledge-graph-spec.md` for deep architecture mapping and refresh guidance.
- `references/context-compactor-spec.md` for retention policy, archive layout, and dry-run expectations.
