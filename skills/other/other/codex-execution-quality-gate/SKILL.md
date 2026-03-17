---
name: codex-execution-quality-gate
description: Run verification checks before completion using lint/test, security scanning, and optional bundle plus tech debt analysis. Use at final gate steps and block completion when mandatory failures are detected.
load_priority: on-demand
---

## TL;DR
11-priority verification chain plus environment pre-flight. Blocking: security (critical), lint (exit 1), tests (exit 1). Advisory: tech debt, UX audit, a11y, Lighthouse, Playwright, suggestions, impact prediction, quality trend. Run decision tree to select checks. Fix blockers before completion.

# Execution Quality Gate

## Activation

1. Activate during final `gate` steps.
2. Activate on explicit `$codex-execution-quality-gate`.
3. Run before saying work is complete.
4. Activate on `$pre-commit` or "check before commit".
5. Activate on `$smart-test` or "which tests to run".
6. Activate on `$suggest` or "suggest improvements".
7. Activate on `$impact` or "what will this affect".
8. Activate on `$quality-record` to record quality trend snapshot.
9. Activate on `$quality-report` to generate trend report.
10. Activate on `$ux-audit`.
11. Activate on `$a11y-check`.
12. Activate on `$lighthouse <url>`.
13. Activate on `$e2e check`.
14. Activate on `$e2e generate <url>`.
15. Activate on `$e2e run`.
16. Activate on `$codex-doctor`.
17. Activate on `$setup-check`.

## Decision Tree Routing

```
Task type -> Pre-flight/setup?
    |- Yes -> run: doctor
    `- No -> Code change?
        |- Yes -> What kind?
        |   |- New feature -> run: pre_commit_check + smart_test_selector + predict_impact
        |   |- Bug fix -> run: pre_commit_check + smart_test_selector
        |   |- Refactor -> run: tech_debt_scan + pre_commit_check
        |   `- UI change -> run: ux_audit + accessibility_check + pre_commit_check
        |
        |- Deploy/ship? -> run: security_scan + lighthouse_audit + playwright_runner
        |
        |- Review/audit? -> run: quality_trend + suggest_improvements + tech_debt_scan
        |
        `- No code -> skip quality gate
```

## Phase X Verification Order

| Priority | Check | Script | Blocking |
| --- | --- | --- | --- |
| P-1 | impact predictor (pre-edit advisory) | `scripts/predict_impact.py` | warning only |
| P0 | security scan | `scripts/security_scan.py` | yes for critical findings |
| P1 | lint | `scripts/run_gate.py` | yes when detected lint exits 1 |
| P2 | tests | `scripts/run_gate.py` | yes when detected tests exit 1 |
| P3 | bundle/dependency check | `scripts/bundle_check.py` | warning only |
| P4 | tech debt scan | `scripts/tech_debt_scan.py` | warning only |
| P5 | improvement suggester (post-task) | `scripts/suggest_improvements.py` | warning only |
| P6 | quality trend tracker (periodic) | `scripts/quality_trend.py` | warning only |
| P7 | UX static audit (pre-UI delivery) | `scripts/ux_audit.py` | warning only |
| P8 | accessibility static checker | `scripts/accessibility_check.py` | warning only |
| P9 | Lighthouse runtime audit | `scripts/lighthouse_audit.py` | warning only |
| P10 | Playwright setup/run helper | `scripts/playwright_runner.py` | warning only |
| P11 | server lifecycle helper (optional) | `scripts/with_server.py` | warning only |

## Execution

1. Run `run_gate.py` with project root.
2. Run `security_scan.py` with project root.
3. Optionally run `bundle_check.py` with project root.
4. Optionally run `tech_debt_scan.py` with project root.
5. Optionally run `suggest_improvements.py` after complex tasks.
6. Optionally run `predict_impact.py` before high-risk edits.
7. Optionally run `quality_trend.py --record` on periodic cadence.
8. Optionally run `ux_audit.py` before UI handoff.
9. Optionally run `accessibility_check.py` for public-facing surfaces.
10. Optionally run `lighthouse_audit.py` before deploy (requires running server URL).
11. Optionally run `playwright_runner.py` for E2E setup/check/run flows.
12. Optionally run `with_server.py` to bootstrap local server(s) before Lighthouse/Playwright checks.
13. Merge results and decide pass/fail.

### Decision Rules

- Completion allowed only if no blocking failures remain.
- Blocking failures must be fixed, then checks rerun.
- Warning-only outcomes may proceed with explicit warning to user.
- Tech debt scan is advisory in MVP and does not block completion.
- Improvement suggestions are advisory and do not block completion.
- Impact prediction is advisory and does not block completion.
- Quality trend reporting is periodic/advisory and does not block completion.
- UX static audit is advisory and does not block completion.
- Accessibility static checker is advisory and does not block completion.
- Lighthouse wrapper is advisory and must fail gracefully when tool/server is unavailable.
- Playwright wrapper is advisory and must fail gracefully when tool/setup is unavailable.
- Server lifecycle helper is advisory and should be used only when runtime checks need controlled startup/shutdown.

## Script Invocation Discipline

1. Always run `--help` before invoking a script.
2. Treat scripts as black-box helpers and prefer direct execution over source inspection.
3. Read script source only when customization or bug fixing is required.

## Script Paths

- Windows:
  `python "$env:USERPROFILE\.codex\skills\codex-execution-quality-gate\scripts\<script>.py" --project-root <path>`
- macOS/Linux:
  `python "$HOME/.codex/skills/codex-execution-quality-gate/scripts/<script>.py" --project-root <path>`

### Environment Doctor Command

- `python "$env:USERPROFILE\.codex\skills\codex-execution-quality-gate\scripts\doctor.py" --skills-root "$env:USERPROFILE\.codex\skills" --format json`
- `python "$env:USERPROFILE\.codex\skills\codex-execution-quality-gate\scripts\doctor.py" --format table`

### Tech Debt Command

- `python "$env:USERPROFILE\.codex\skills\codex-execution-quality-gate\scripts\tech_debt_scan.py" --project-root <path>`

### Pre-Commit Intelligence Command

- `python "$env:USERPROFILE\.codex\skills\codex-execution-quality-gate\scripts\pre_commit_check.py" --project-root <path>`

### Smart Test Selector Command

- `python "$env:USERPROFILE\.codex\skills\codex-execution-quality-gate\scripts\smart_test_selector.py" --project-root <path> --source staged`

### Improvement Suggester Command

- `python "$env:USERPROFILE\.codex\skills\codex-execution-quality-gate\scripts\suggest_improvements.py" --project-root <path> --source last-commit`
- In proactive mode, run after complex tasks and present top 3 suggestions.

### Impact Predictor Command

- `python "$env:USERPROFILE\.codex\skills\codex-execution-quality-gate\scripts\predict_impact.py" --project-root <path> --files <file1,file2> --depth 2`

### Quality Trend Commands

- Record:
  `python "$env:USERPROFILE\.codex\skills\codex-execution-quality-gate\scripts\quality_trend.py" --project-root <path> --record`
- Report:
  `python "$env:USERPROFILE\.codex\skills\codex-execution-quality-gate\scripts\quality_trend.py" --project-root <path> --report --days 30`

### UX Audit Command

- `python "$env:USERPROFILE\.codex\skills\codex-execution-quality-gate\scripts\ux_audit.py" --project-root <path>`

### Accessibility Check Command

- `python "$env:USERPROFILE\.codex\skills\codex-execution-quality-gate\scripts\accessibility_check.py" --project-root <path> --level AA`

### Lighthouse Audit Command

- `python "$env:USERPROFILE\.codex\skills\codex-execution-quality-gate\scripts\lighthouse_audit.py" --url <http://localhost:3000> --device mobile --runs 1`
- Requires a running URL and Lighthouse availability through `npx`.

### Playwright Runner Commands

- Check setup:
  `python "$env:USERPROFILE\.codex\skills\codex-execution-quality-gate\scripts\playwright_runner.py" --project-root <path> --mode check`
- Generate skeleton:
  `python "$env:USERPROFILE\.codex\skills\codex-execution-quality-gate\scripts\playwright_runner.py" --project-root <path> --mode generate --url <http://localhost:3000/page>`
- Run tests:
  `python "$env:USERPROFILE\.codex\skills\codex-execution-quality-gate\scripts\playwright_runner.py" --project-root <path> --mode run --browser chromium`

### Server Lifecycle Helper Command

- `python "$env:USERPROFILE\.codex\skills\codex-execution-quality-gate\scripts\with_server.py" --help`
- Example:
  `python "$env:USERPROFILE\.codex\skills\codex-execution-quality-gate\scripts\with_server.py" --server "npm run dev" --port 3000 -- python "$env:USERPROFILE\.codex\skills\codex-execution-quality-gate\scripts\lighthouse_audit.py" --url http://localhost:3000`

## Reference Files

- `references/gate-policy.md`: blocking vs warning rules for gate decisions.
- `references/improvement-suggester-spec.md`: post-task suggestion behavior and presentation protocol.
- `references/impact-predictor-spec.md`: pre-edit blast-radius analysis guidance.
- `references/quality-trend-spec.md`: periodic quality trend workflow and interpretation.
- `references/ux-audit-spec.md`: static UX audit checks and scoring.
- `references/accessibility-check-spec.md`: WCAG static checks and compliance scoring.
- `references/lighthouse-audit-spec.md`: Lighthouse wrapper behavior and graceful fallback.
- `references/playwright-runner-spec.md`: Playwright check/generate/run behavior.
- `references/run-gate-spec.md`: lint and test orchestration behavior for pass/fail decisions.
- `references/security-scan-spec.md`: severity-aware security scan integration and blocking criteria.
- `references/bundle-check-spec.md`: dependency and bundle signal interpretation guidance.
- `references/pre-commit-check-spec.md`: staged-file fast feedback behavior and blocker handling.
- `references/smart-test-selector-spec.md`: test selection strategy for changed files.
- `references/tech-debt-scan-spec.md`: advisory technical debt signal interpretation and prioritization.

## Override

If user says `skip gate` or `force complete`, comply and warn:
"Quality gate skipped. Lint/test/security status is unknown."

## Output Handling

For each script:

1. capture output
2. summarize errors/warnings/passes
3. ask whether to fix blocking errors when present
4. rerun after fixes to verify
