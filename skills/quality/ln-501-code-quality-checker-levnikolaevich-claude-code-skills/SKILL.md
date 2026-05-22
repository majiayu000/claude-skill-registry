---
name: ln-501-code-quality-checker
description: Worker that checks DRY/KISS/YAGNI/architecture/guide compliance for Done implementation tasks. Reports issues; does not change statuses or create tasks.
---

# Code Quality Checker

Analyzes Done implementation tasks for code-quality issues and reports findings for the Story quality gate.

## Purpose & Scope
- Load Story and Done implementation tasks (exclude test tasks).
- Check for DRY/KISS/YAGNI violations, architecture boundary breaks, guide non-compliance, and obvious config/hardcode problems.
- Produce a verdict and structured issue list; never edits Linear or kanban.

## When to Use
- **Invoked by ln-500-story-quality-gate** Pass 1 (first gate)
- All implementation tasks in Story status = Done
- Before regression testing (ln-502) and test planning (ln-510)

## Workflow (concise)
1) Load Story (full) and Done implementation tasks (full descriptions) via Linear; skip tasks with label "tests".
2) Collect affected files from tasks (Affected Components/Existing Code Impact) and recent commits/diffs if noted.
3) Analyze code and docs:
   - Reuse existing components; avoid duplication; simplify over-engineering; keep layers clean.
   - No hardcoded creds/URLs/magic numbers; follow referenced guides.
   - Logging: structured logging on errors/warnings; log levels appropriate.
   - Comments: WHY-focused; no commented-out/dead code; public API documented.
   - Naming: conventions consistent; self-documenting names; no cryptic abbreviations.
   - Performance: no O(n^2) in loops; no N+1 queries; lazy loading where applicable.
   - Concurrency: no race conditions; proper locking; async/await correct.
4) Output verdict: PASS or ISSUES_FOUND with details (category, severity, file, recommendation). Add Linear comment with findings.

## Critical Rules
- Read guides mentioned in Story/Tasks before judging compliance.
- Language preservation in comments (EN/RU).
- Do not create tasks or change statuses; caller decides next actions.

## Definition of Done
- Story and Done implementation tasks loaded (test tasks excluded).
- Guides reviewed; affected files inspected.
- Verdict produced with structured issues (if any) and Linear comment posted.

## Reference Files
- Guides: `docs/guides/`
- Templates for context: `shared/templates/task_template_implementation.md` (or local `docs/templates/` in target project)

---
**Version:** 3.0.0 (Condensed worker flow)
**Last Updated:** 2025-12-23
