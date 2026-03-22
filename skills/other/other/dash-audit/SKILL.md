---
name: dash-audit
description: Audit Dash apps for callback hazards, state flow risks, layout and accessibility issues, and Dash-specific UX regressions. Use when the user asks for a Dash callback review, Dash UI audit, Dash web-interface audit, or a read-first remediation plan for a Dash app. Do not use for generic React or Next.js UI review.
---

# Dash Audit

Use this skill for read-first Dash audits. It owns Dash callback review, Dash UI/state review, and prioritized remediation guidance.

## Workflow

1. Read the repo `AGENTS.md`.
2. Run `/home/bjorn/.codex/skill-support/bin/ui-audit-preflight dash-callback-map --cwd <repo> --out <json>`.
3. Read only the Dash references you need:
   - `references/dash-callbacks.md` for callback graph and state hazards.
   - `references/dash-ui.md` for layout, responsiveness, accessibility, and interaction review.
4. Inspect only the files surfaced by the preflight plus any directly implicated layout, component, or callback modules.
5. Report grouped findings with the highest-risk callback and regression issues first.
6. If the user asks for fixes, keep remediation scoped and verify the affected path with repo-native commands.

## Use When

- The task is a Dash callback audit.
- The task is a Dash web UI, state, or layout review.
- The user wants a read-first remediation plan for a Dash app.

## Do Not Use When

- The task is a general web or Next.js UI audit.
- The task is platform architecture with no Dash review need.
- The task is only backend, dependency, or docs work.

## Outputs

- executive summary
- grouped findings by category and file
- prioritized fixes
- callback graph or regression-risk notes when useful
- scorecard or risk summary when useful
