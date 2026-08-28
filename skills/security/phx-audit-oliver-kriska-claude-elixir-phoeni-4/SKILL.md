---
name: phx-audit
description: Project health audit and health check — architecture, performance, tests,
  dependencies, code quality. Use when assessing overall project health, before releases,
  or after refactors.
---

# Project Health Audit

Comprehensive project-wide health assessment across five independent concern tracks.

## Usage

```
/phx-audit              # Full audit (default)
/phx-audit --quick      # 2-3 minute pulse check
/phx-audit --focus=security   # Deep dive single area
/phx-audit --focus=performance
/phx-audit --since abc123   # Incremental audit since commit
/phx-audit --since HEAD~10  # Audit last 10 commits
```

## When to Use

- **Quarterly** health checks
- **Before major releases**
- **After large refactors**
- **New team member onboarding** (understand codebase health)

## Iron Laws

1. **Complete every selected track before synthesizing** — partial results make
   cross-category scores misleading
2. **Scope each track to concrete directories and checks** — vague project-wide
   analysis produces generic findings
3. **Never compare scores across projects** — track trends only within the same
   codebase
4. **Run quick mode before full mode** — catch basic failures before expensive
   analysis

## Portable Audit Workflow

1. Create `.claude/audit/reports/` and `.claude/audit/summaries/`.
2. Run the quick checks below. Stop and report a blocker when the project cannot
   compile or its test command cannot start.
3. Complete five tracks: architecture, performance, security, tests, and
   dependencies. Native generic workers may run independent tracks in parallel
   when the runtime provides them; otherwise run every track sequentially in
   this session. Never require named custom agents.
4. Write one evidence-focused report per track under `.claude/audit/reports/`.
   Report issues only, cite paths and lines, and use one summary line for a
   clean area.
5. After all selected reports exist, deduplicate findings, identify
   cross-category correlations, calculate scores using
   `references/scoring-methodology.md`, and write
   `.claude/audit/summaries/project-health-{date}.md`.

If two or more optional workers fail or hit limits, finish the missing tracks
sequentially. Never present an incomplete track as audited.

## Output Format

Report an executive health score, per-category scores for Architecture,
Performance, Security, Tests, and Dependencies, critical issues, top
recommendations, and an Immediate/Short-term/Long-term action plan.

## Quick Mode (`--quick`)

Only run essential checks (~2-3 minutes):

Run `mix compile --warnings-as-errors`, then `mix hex.audit && mix deps.audit`,
then `mix xref graph --format stats`, then `mix test --trace 2>&1 | tail -20`.

Skip: Full security scan, N+1 analysis, test quality metrics, architecture deep dive.

## Focus Mode (`--focus=area`)

Run only the selected concern track with its deeper checks:

| Focus | Extra checks |
|-------|--------------|
| `security` | Full OWASP review, Sobelow, manual authorization patterns |
| `performance` | Query plans, N+1 inventory, profiling evidence |
| `architecture` | Full xref graph, coupling matrix, cohesion |
| `tests` | Coverage by context, isolation, flaky-test indicators |
| `deps` | Vulnerabilities, licenses, maintenance status |

## Incremental Mode (`--since <commit>`)

Analyze only changes since a specific commit. Useful for pre-merge checks:

Run `git diff --name-only <commit>...HEAD` to identify changed files, then run targeted audits on changed files only (skips full project scan).

Combines with other flags: `/phx-audit --since HEAD~5 --focus=security`

## Relationship to Other Commands

| Command | Scope | Frequency |
|---------|-------|-----------|
| `/phx-review` | Changed files (diff) | Every PR |
| `/phx-audit` | Entire project | Quarterly |
| `/phx-boundaries` | Context structure | On-demand |
| `/phx-verify` | Compile/test pass | Anytime |

## References

- `references/scoring-methodology.md` - How scores are calculated
- `references/architecture-checks.md` - Detailed architecture criteria
