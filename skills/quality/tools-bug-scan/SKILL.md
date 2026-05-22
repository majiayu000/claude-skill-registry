---
name: tools-bug-scan
description: Run the repository-native bug scanner (`pnpm bug-scan` / `pnpm bug-scan:changed`), summarize findings by severity and rule, and propose concrete next fixes or targeted rescans.
operating_mode: AUDIT + RECOMMENDATIONS
trigger_conditions: bug scan, static scan, risky patterns, code safety sweep, run bug-scan, scan changed files
related_skills: lp-do-build, ops-ci-fix, lp-do-fact-find
---

# Bug Scan Tool

Use this skill when the user wants a fast, deterministic bug-pattern sweep using the in-repo scanner.

## Commands

- Full/targeted scan:
  - `pnpm bug-scan [path ...]`
- Changed-files scan:
  - `pnpm bug-scan:changed`
- Machine-readable output:
  - `pnpm bug-scan -- --format=json [path ...]`
  - `pnpm bug-scan -- --changed --format=json`
  - `pnpm bug-scan -- --changed --format=json --fail-on=none --business-scope=<BIZ> --idea-artifact=docs/plans/<slug>/bug-scan-findings.user.json`
- Rule discovery and tuning:
  - `pnpm bug-scan:rules`
  - `pnpm bug-scan -- --changed --fail-on=critical`
  - `pnpm bug-scan -- --only-rules=<ruleA,ruleB>`
  - `pnpm bug-scan -- --skip-rules=<ruleA,ruleB>`
  - `pnpm bug-scan -- --write-baseline=tools/bug-scan-baseline.json --fail-on=none`
  - `pnpm bug-scan -- --baseline=tools/bug-scan-baseline.json`

## Default Workflow

1. Choose scope:
   - If user asks for changed work, run `pnpm bug-scan:changed`.
   - If user provides files/directories, pass them to `pnpm bug-scan`.
   - If unspecified, prefer changed-files first to keep signal high.
2. Run scanner once.
3. If findings exist, summarize by:
   - severity counts (`critical`, `warning`)
   - rule IDs
   - top file locations (`path:line:column`)
4. Recommend a concrete next action set:
   - immediate fixes for `critical`
   - optional cleanup queue for `warning`
   - exact rerun command after fixes
5. If the scan is part of post-build reflection, write the idea artifact into the active plan directory so `startup-loop:generate-process-improvements` can ingest findings as idea candidates.

## Output Contract

Always report:

- Scan scope used.
- Finding totals by severity.
- Top findings with file references.
- Exit status implication:
  - `0` = no findings
  - `1` = findings present

## Guardrails

- Do not install external scanners or mutate hooks/shell profiles in this skill.
- Do not fail the task if scanner reports findings; report and propose fix order.
- If scanner command fails for runtime/tooling reasons, report the error and suggest the minimal unblocking command.

## Escalation

Escalate to planning (`lp-do-fact-find` / `lp-do-build`) when:

- the same rule repeatedly appears across many files,
- findings indicate systemic pattern debt,
- user asks to convert findings into an implementation plan.
