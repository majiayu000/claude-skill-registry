---
name: release-health-gates
description: 'Standardizes release approvals with GitHub-aware checklists. Use when
  preparing releases, validating deployment gates, conducting release reviews, embedding
  release gate snippets in PRs. Do not use when weekly status updates - use github-initiative-pulse.
  DO NOT use when: code reviews - use pensive review skills.'
category: governance
tags:
- release
- github
- readiness
- quality
- governance
dependencies: []
tools:
- minister-tracker
provides:
  governance:
  - release-gates
  - rollout-scorecards
  reporting:
  - deployment-comment
  - qa-handshake
usage_patterns:
- release-train
- hotfix-review
- stakeholder-briefing
complexity: intermediate
estimated_tokens: 700
progressive_loading: true
modules:
- modules/quality-signals.md
- modules/deployment-readiness.md
---

# Release Health Gates

## Purpose

Standardize release approvals by expressing gates as GitHub-aware checklists. Ensure code, docs, comms, and observability items are green before deployment.

## Gate Categories

1. **Scope & Risk** – Are all blocking issues closed or deferred with owners?
2. **Quality Signals** – Are required checks, tests, and soak times satisfied?
3. **Comms & Docs** – Are docs merged and release notes posted?
4. **Operations** – Are runbooks, oncall sign-off, and rollback plans ready?

## Workflow

1. Load skill to access gate modules.
2. Attach Release Gate section to deployment PR.
3. Use tracker data to auto-fill blockers and highlight overdue tasks.
4. Update comment as gates turn green; require approvals for any waivers.

## Outputs

- Release Gate markdown snippet (embed in PR/issue).
- QA Handshake summary referencing GitHub Checks.
- Rollout scorecard that persists in tracker data for retros.

## Exit Criteria

- All release gates evaluated and documented.
- Any blocking gates have waiver approvals recorded.
- Deployment PR contains embedded Release Gate snippet.
- Rollout scorecard saved for post-release retrospective.
## Troubleshooting

### Common Issues

**Command not found**
Ensure all dependencies are installed and in PATH

**Permission errors**
Check file permissions and run with appropriate privileges

**Unexpected behavior**
Enable verbose logging with `--verbose` flag
