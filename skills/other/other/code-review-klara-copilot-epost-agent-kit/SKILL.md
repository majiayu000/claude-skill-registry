---
name: code-review
description: (ePost) Use when reviewing code, checking quality before commit, or auditing changed files for issues
tier: core

metadata:
  agent-affinity: [epost-code-reviewer, epost-fullstack-developer]
  keywords: [review, code-quality, security, performance, testing, verification]
  platforms: [all]
  triggers: ["/review", "code review", "review code"]
  connections:
    enhances: [review]
---

# Code Review Skill

## Purpose
Comprehensive code quality assessment and verification.

## When Active
User uses /review, asks for code review, or before committing code.

## Expertise

### Review Process
1. Scope resolution (before git diff):
   - If user provided file paths, component name, or `--files` list → **explicit scope**: use those directly, skip git diff
   - Otherwise → **implicit scope**: identify changed files via `git diff` or `git log`
2. Read the plan file if one exists — understand requirements before reviewing
3. Systematic review: structure, logic, types, performance, security
4. Categorize findings: Critical > High > Medium > Low
5. Update plan TODO status if plan exists

### Systematic Review

All code review rules are defined in `references/code-review-standards.md` with numbered IDs, severity, and pass/fail criteria.

| Category | Human Name | Rules | Scope |
|----------|-----------|-------|-------|
| SEC | Security | SEC-001..008 | OWASP Top 10, credentials, injection, auth |
| PERF | Performance | PERF-001..006 | N+1, renders, caching, bundle |
| TS | Type Safety | TS-001..006 | Unsafe any, casts, guards, generics |
| LOGIC | Logic & Correctness | LOGIC-001..006 | Null handling, edge cases, race conditions |
| DEAD | Dead Code | DEAD-001..003 | Unreachable, unused, orphaned |
| ARCH | Architecture | ARCH-001..005 | File org, boundaries, circular deps, layers |
| STATE | State Management | STATE-001..004 | Completeness, exits, guards, concurrency |

### Severity Classification
- **Critical**: Security vulnerabilities, data loss, breaking changes
- **High**: Performance issues, type safety violations, missing error handling
- **Medium**: Code smells, maintainability issues, documentation gaps
- **Low**: Style inconsistencies, minor optimizations

### Escalation Gate (Reviewer Decision)

After initial review, the reviewer decides based on findings:

| Finding | Action |
|---------|--------|
| Critical severity found | Escalate to `/audit --code` — activate `knowledge-retrieval` for deeper context before reporting |
| Task is UI code review/audit (components, tokens, design system) | Delegate to **epost-muji** — runs `/audit --ui` with klara-theme standards + INTEGRITY gate |
| Task is about a11y (accessibility, WCAG, VoiceOver, TalkBack, keyboard nav, screen reader) | Delegate to **epost-a11y-specialist** — runs `/audit --a11y` with full WCAG 2.1 AA rules |
| High severity, UI component finding | Escalate to `/audit --ui` → **epost-muji** for full component audit |
| High severity, a11y issue | Escalate to `/audit --a11y` — a11y specialist audits with WCAG rules |
| Medium/Low only | Complete inline, no escalation needed |

**Rule**: Code review is lightweight by default (no `knowledge-retrieval`). Escalate to audit only when findings warrant it. Audit always activates `knowledge-retrieval`.

### Lightweight vs. Escalated Review Scope

| Category | Lightweight (default) | Escalated (knowledge-retrieval active) |
|----------|-----------------------|---------------------------------------|
| ARCH | ARCH-001..003 (file org, boundaries, circular deps) | + ARCH-004..005 (layer violations, dependency direction) |
| LOGIC | LOGIC-001..003 (null handling, edge cases, error paths) | + LOGIC-004..006 (race conditions, off-by-one, comparison) |
| STATE | STATE-001..002 (completeness, exit states) | + STATE-003..004 (transition guards, concurrent mutations) |
| TS | TS-001..003 (unsafe any, unvalidated cast, missing guard) | + TS-004..006 (generic constraints, non-null assertions, strict null) |
| PERF | PERF-001..003 (N+1, re-renders, loops) | + PERF-004..006 (caching, bundle, lazy loading) |
| SEC | SEC-001..004 (injection, XSS, secrets, auth) | + SEC-005..008 (input validation, SSRF, deserialization, data logging) |
| Tests | Test file exists, covers changed code | + coverage gap analysis, edge case completeness |
| Standards source | code-review-standards.md only | + docs/ conventions, RAG patterns |

**Rule**: Lightweight review does NOT load knowledge-retrieval. Only categories in the "Lightweight" column are checked. If a Critical finding is detected, escalate to the full column.

### Subagent Constraint

Code-reviewer runs as a **subagent** (spawned via Agent tool). Subagents **cannot spawn further subagents**. Therefore:
- Code-reviewer does NOT dispatch muji, a11y-specialist, or any other agent
- Hybrid orchestration (muji + code-reviewer) is handled by the **main context** via `audit/SKILL.md`
- Code-reviewer is a pure reviewer: reads files, applies rules, writes report

### When Invoked with Muji Report

If the caller provides a muji report path (hybrid audit):
1. Read muji report at the provided path
2. Extract `finding_locations`: Set of file:line already flagged by muji
3. Run SEC/PERF/TS/ARCH/STATE/LOGIC/DEAD rules on the same files
4. **Dedup**: skip any file:line already in muji's finding set
5. Write report to the provided `output_path`

### Critical Escalation (self-dispatch, no Agent tool needed)

When a Critical finding is detected during review:
1. Load `knowledge-retrieval` skill (already in agent skills list)
2. Execute: L1 docs/ → L2 RAG → L4 Grep fallback
3. Document KB layers used in Methodology
4. Re-examine files with retrieved context; update findings

### RAG Lookup (when reviewing)

1. `ToolSearch("web-rag")` → discover `mcp__web-rag-system__*` tools
2. Call `status` → confirm available
3. Call `query` with module + "prior findings security architecture"
4. If unavailable: fallback to Grep on `reports/` for prior audit files
5. Append "L2-RAG" or "L2-RAG-unavailable" to methodology

### Post-Delegation Report Merging

After specialist reports arrive:
1. Read the specialist's Markdown report
2. Add a delegation section to your report: agent name, report path, verdict, finding count
3. Adjust your overall verdict: if specialist found Critical → your verdict cannot be APPROVE
4. List specialist report paths in the report's Related Documents section

**Report consolidation**: After all specialist reports are merged into your report, the final deliverable is YOUR single report file. Sub-agent reports are source material — do not surface them as separate deliverables to the user unless explicitly requested.

## Write session.json (always — after writing report.md)

Write `{session_folder}/session.json` per `audit/references/session-json-schema.md`:
- Inline review: `type: "code-review"`, `agents: [{name: "epost-code-reviewer", report: "report.md", verdict, findings}]`
- Hybrid: `type: "hybrid-audit"`, include all participating agents with their verdicts and counts

## Persist Findings (always — after writing report)

Ownership per `audit/references/output-contract.md`: code-reviewer → `.epost-data/code/`, muji → `.epost-data/ui/`, a11y → `.epost-data/a11y/`.

Persist SEC/PERF/TS/LOGIC/DEAD/ARCH/STATE findings (critical, high, medium) to `.epost-data/code/known-findings.json`:

1. Check if `.epost-data/code/known-findings.json` exists
   - If not: `mkdir -p .epost-data/code/` then create it with `{ "schemaVersion": "1.0.0", "lastUpdated": "{today}", "findings": [] }`
2. **Pre-scan for regressions**: for each finding in current pass, check if same `rule_id` + `file_pattern` exists with `resolved: true` → flag `regression: true` in report; with `resolved: false` → reference existing `id`, do not duplicate
3. For each NEW finding (severity critical/high/medium) not already open in DB:
   - Auto-increment `id` from `max(existing_ids) + 1` (start at 1 for empty)
   - Map: `module`, `rule_id`, `category` (SEC/PERF/TS/LOGIC/DEAD/ARCH/STATE), `title`, `file_pattern`, `code_pattern`, `fix_template`, `priority`, `severity`, `source` (`hybrid-audit` or `code-review`), `source_agent: "epost-code-reviewer"`, `source_report: "{report_path}"`, `first_detected_at: "{YYYY-MM-DDTHH:MM}"`
   - Append to `findings[]`
4. Save updated JSON
5. Log: "Persisted {N} code findings to `.epost-data/code/known-findings.json`" in Methodology

Schema: `code-review/references/code-known-findings-schema.md`

## Output Format

Use `references/report-template.md` for all code review reports.

Key requirements:
- **Session folder**: All output paths per `audit/references/output-contract.md`. `mkdir -p` before any write.
- **One main report per session** — `report.md` is the single surface for the user. Sub-agent `.md` files are source material.
- Header: Date, Agent, Plan (if applicable), Status
- Executive Summary first
- **Methodology** section (required): docs loaded, KB layers used, tools used, files scanned, coverage gaps
- **Delegation Log** section (required if delegation occurred): agent, scope, template, verdict, finding count
- Findings table with ID, Severity, File:Line, Issue, Fix
- Verdict: `APPROVE` | `FIX-AND-RESUBMIT` | `REDESIGN`
- Unresolved questions footer always present

### Related Skills
- `knowledge-retrieval` — activated on Critical escalation
- `knowledge-capture` — use after task to persist learnings
- `auto-improvement` — session metrics and improvement trends
