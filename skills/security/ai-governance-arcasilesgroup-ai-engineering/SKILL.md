---
name: ai-governance
description: "Use when validating compliance, ownership, risk lifecycle, or framework integrity for regulated industries. Modes: compliance | ownership | risk | integrity."
effort: max
argument-hint: "all|compliance|ownership|risk|integrity|--report"
tags: [governance, compliance, ownership, risk, integrity, enterprise]
---


# Governance

Compliance validation for regulated industries. Modes: `compliance` (quality gates), `ownership` (boundary verification), `risk` (decision-store lifecycle), `integrity` (framework consistency). Default: compliance.

## When to Use

- Governance audit, pre-release check, post-install verification.
- NOT for code quality -- use `/ai-quality`.
- NOT for security scanning -- use `/ai-security`.

## Modes

### compliance -- Quality Gate Validation

Validate that rules in `framework-contract.md` are enforced.

1. **Hook enforcement** -- verify required hooks exist in `.git/hooks/`, are executable, contain no `--no-verify` escapes.
2. **Check coverage** -- for each stack in `enforcement.checks`, confirm tool is configured and callable.
3. **Non-negotiables** -- walk `standards.non_negotiables`, trace enforcement chain: manifest -> hook -> CLAUDE.md.
4. **CI workflows** -- verify `enforcement.ci.required_workflows` exist under `.github/workflows/`.
5. **Security contract** -- gitleaks in pre-commit, semgrep in pre-push, dependency audit per stack.

### ownership -- Boundary Validation

Verify files live in correct ownership zones.

1. **Zone mapping** -- load `ownership.model` from manifest. Build zones: framework-managed, team-managed, project-managed, system-managed.
2. **File placement** -- scan `.ai-engineering/`, verify each file maps to exactly one zone.
3. **Modification history** -- `git log` framework-managed files, confirm only framework commits touched them.
4. **Update rule compliance** -- team/project paths never overwritten by automation.

### risk -- Risk Acceptance Lifecycle

Sub-modes: `accept`, `resolve`, `renew`.

**Accept**: record time-limited risk in `decision-store.json`.
- Classify finding, determine severity, register with mandatory `follow_up_action`.
- Auto-expiry: Critical 15d, High 30d, Medium 60d, Low 90d.

**Resolve**: close after remediation.
- Validate fix committed, scan clean, no regression.
- Mark `remediated` (preserved for audit trail, not deleted).

**Renew**: extend before expiry (max 2 renewals).
- Check eligibility (`renewal_count < 2`). Require justification.
- Create new decision with `renewed_from` reference.

### integrity -- Framework Consistency

Validate manifest claims match disk reality.

1. **Manifest counters** -- compare `governance_surface.agents.total` and `skills.total` against actual file counts.
2. **Agent-skill references** -- verify every path in agent `references.skills` resolves to an existing SKILL.md.
3. **State file schemas** -- confirm `state/` files are valid JSON/NDJSON with required keys.
4. **Command file existence** -- verify each SKILL.md has valid YAML frontmatter.

### `--report` -- Formal Report

Generate structured compliance report suitable for audit:

```markdown
# Governance Report: [mode]

## Score: N/100
## Verdict: PASS (>=90) | WARN (>=70) | FAIL (<70)

## Findings
| # | Severity | Category | Description | Location | Remediation |

## Gate Check
- Blocker: N (threshold: 0)
- Critical: N (threshold: 0)
```

Scoring: start at 100. Deduct: blocker -25, critical -15, major -5, minor -1. Floor at 0.

## Quick Reference

```
/ai-governance              # compliance mode (default)
/ai-governance all          # all modes
/ai-governance risk accept  # accept a new risk
/ai-governance risk resolve # close a remediated risk
/ai-governance integrity    # framework consistency check
/ai-governance --report     # generate formal report
```

## Common Mistakes

- Running governance mid-implementation -- best between phases or before releases.
- Accepting risk without `follow_up_action` -- mandatory field.
- Exceeding 2 renewals -- remediation becomes mandatory.

## Integration

- CLI layer: `ai-eng validate --category <mode>`, `ai-eng doctor`, `ai-eng maintenance risk-status`.
- Risk acceptances block pre-push when expired.
- Release gate (`/ai-release`) checks governance status.

## References

- `.ai-engineering/manifest.yml` -- governance non-negotiables and quality thresholds.
- `state/decision-store.json` -- risk acceptance records.
$ARGUMENTS
