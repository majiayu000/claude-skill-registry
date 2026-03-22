---
name: codex-execution-quality-gate
description: Run verification checks before completion using lint/test, security scanning, and optional bundle plus tech debt analysis. Use at final gate steps and block completion when mandatory failures are detected.
load_priority: on-demand
---

## TL;DR
12-priority verification chain plus environment pre-flight. Blocking: security (critical), lint (exit 1), tests (exit 1), and strict deliverable failures. Advisory: tech debt, UX audit, a11y, Lighthouse, Playwright, suggestions, impact prediction, quality trend. Run decision tree to select checks. Fix blockers before completion.

# Execution Quality Gate

## Activation

1. Activate during final `$gate` steps.
2. Activate on explicit `$codex-execution-quality-gate` or `$gate`.
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
16. Activate on `$codex-doctor` or `$doctor`.
17. Activate on `$setup-check`.
18. Activate on `$install-hooks` or "install git hooks".
19. Activate on `$install-ci` or "install CI gate".
20. Activate on `$output-guard` or `$guard` or "check if this output is too generic".
21. Activate on `$editorial-review` or `$editorial` or "make this read less like AI / more like a human deliverable".
22. Activate on `$check` or "run quick gate".
23. Activate on `$check-full` or "run full gate".
24. Activate on `$check-deploy` or "run deploy gate".

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
        |- Written deliverable quality? -> run: output_guard
        |
        `- No code -> skip quality gate
```

## Runtime Enforcement

- Advisory mode is the default: the AI must decide which gate scripts to run and report fresh evidence before completion.
- `auto_gate.py` is the single orchestration entry point when the user wants quick, full, or deploy-focused checks without remembering individual script names.
- Runtime enforcement is available through `install_hooks.py`, which installs a managed `pre-commit` hook that runs `security_scan.py` and `pre_commit_check.py` automatically before commit.
- Use `--with-lint-test` only when the team wants heavier local enforcement that also runs `run_gate.py`.
- Use `install_ci_gate.py` to generate CI enforcement for GitHub Actions or GitLab CI when the project should block pushes and pull requests in automation as well as locally.
- Hooks and CI templates are additive. They do not replace the normal gate decision tree, and uninstall should remove only the managed CodexAI block.
- If runtime enforcement is not installed, the AI must continue to self-enforce the gate manually.

## Rules

- Follow the verification order, execution flow, and blocking policy in `references/gate-execution-flow.md`.
- Blocking failures must be fixed and rerun; warning-only signals may proceed only with explicit user-facing warnings.
- Run `--help` before invoking a script, treat scripts as black-box helpers, and inspect source only for customization or bug fixing.
- Use `with_server.py` only when runtime audits need controlled startup and shutdown.
- If user says `skip gate` or `force complete`, comply and warn: "Quality gate skipped. Lint/test/security status is unknown."
- For each invoked script, capture output, summarize passes/warnings/blockers, ask whether to fix blocking errors when present, and rerun after fixes to verify.
- Xem `skills/.system/REGISTRY.md` để biết đường dẫn đầy đủ.

## Reference Files

- `references/gate-policy.md`: blocking vs warning rules for gate decisions.
- `references/improvement-suggester-spec.md`: post-task suggestion behavior and presentation protocol.
- `references/impact-predictor-spec.md`: pre-edit blast-radius analysis guidance.
- `references/quality-trend-spec.md`: periodic quality trend workflow and interpretation.
- `references/output-guard-spec.md`: heuristics for detecting generic filler and weak evidence in deliverables.
- `references/editorial-review-spec.md`: rubric for checking whether a deliverable reads like a human, accountable engineering artifact.
- `references/ux-audit-spec.md`: static UX audit checks and scoring.
- `references/accessibility-check-spec.md`: WCAG static checks and compliance scoring.
- `references/lighthouse-audit-spec.md`: Lighthouse wrapper behavior and graceful fallback.
- `references/playwright-runner-spec.md`: Playwright check/generate/run behavior.
- `references/run-gate-spec.md`: lint and test orchestration behavior for pass/fail decisions.
- `references/security-scan-spec.md`: severity-aware security scan integration and blocking criteria.
- `references/bundle-check-spec.md`: dependency and bundle signal interpretation guidance.
- `references/script-commands.md`: script CLI examples, including runtime hook and CI installers.
- `references/pre-commit-check-spec.md`: staged-file fast feedback behavior and blocker handling.
- `references/smart-test-selector-spec.md`: test selection strategy for changed files.
- `references/tech-debt-scan-spec.md`: advisory technical debt signal interpretation and prioritization.
- `references/gate-execution-flow.md`: verification order, execution steps, overrides, and output-handling rules.
- `references/output-schemas.md`: JSON status contracts for gate helper scripts, including hook and CI installers.
