---
name: codebase-review
description: Holistic read-only codebase health review to find architecture drift, dead code, test gaps, and doc gaps.
---

# Codebase Review

Strategic read-only review of the codebase. Produce actionable findings. No fixes.

## Inputs

Scope (domains or systems to focus on). Target branch (default `main`).

## Review-aware

Before starting: check if `<slug>.findings.md` exists for this scope. If it does, build on prior findings rather than starting over.

## Workflow

1. **Load context** — Read AGENTS.md for invariants and authoritative systems. Check GitHub activity (`gh issue list --state open`, `gh pr list`) to identify hotspots.

2. **Sample strategically** — Focus on:
   - Recent churn areas (from git log)
   - Systems flagged in open issues or PRs
   - Determinism violations (anything outside logistics_tick/combat_tick)
   - Duplicated systems or ambiguous authority
   - Autoload/UI coupling
   - Dead code or unreferenced assets
   - Test coverage gaps on critical paths

3. **Report** — Group findings by severity (Critical/Major/Minor) with `path:line` and impact description.

4. **Track findings** — For Critical and Major findings, create GitHub issues via `/issue`. For AIDE framework findings, use `/issue` with appropriate labels.

## Reference

- Project invariants: AGENTS.md
- Coding patterns: `docs/CODING_GUIDELINES.md`
- Testing requirements: `docs/TESTING_POLICY.md`
