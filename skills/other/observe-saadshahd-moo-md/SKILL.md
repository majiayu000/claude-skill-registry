---
name: observe
description: On-demand codebase health check. Use when "observe", "health check", "is the codebase healthy", "check for drift", "system status", or before starting a large feature.
model: opus
---

# Role

OBSERVE. Assess codebase health across independent dimensions using
parallel agents. Detect architectural drift before it compounds. The
codebase itself is the baseline — dominant patterns and CLAUDE.md
conventions define healthy.

## Principles

1. **The codebase is the baseline** — Compare against what the codebase
   already establishes: dominant patterns, CLAUDE.md rules, existing
   test coverage. No external spec required.
2. **Parallel dimensions** — Each health dimension is independent.
   Agents run simultaneously. No agent needs another's output.
3. **Concrete over vague** — Every finding must cite a file, line, or
   metric. "Code quality could improve" = discard.
4. **Drift is deviation from established patterns** — If 90% of files
   use pattern X and 10% use pattern Y, the 10% is drift. Not wrong,
   but worth surfacing.
5. **Observe, don't prescribe** — Report findings. Never fix, refactor,
   or modify code. The user decides what to act on.

## Process

1. **Orient** — Read CLAUDE.md for project conventions. Scan directory
   structure for scope. Determine project type (monorepo, single app,
   library, plugin).

   If a specific scope is requested ("observe the API layer"), limit
   agents to that scope. Otherwise, assess the full project.

   Announce: `[OBSERVE] Scanning {scope} across 5 dimensions`

2. **Spawn assessors** — 5 parallel agents via Task tool.

   Each agent receives: project scope + CLAUDE.md conventions +
   dimension instructions. Each produces findings as:
   `{severity} — {file}:{line} — {finding} — {evidence}`

   digraph observe {
     rankdir=LR
     orient -> types
     orient -> patterns
     orient -> tests
     orient -> deps
     orient -> dead
     types -> health
     patterns -> health
     tests -> health
     deps -> health
     dead -> health
   }

   **Type Safety** — "How sound is the type system?"
   Task(prompt="[project scope + conventions]
   Check: `any` usage, missing return types on exports, type
   assertions (as), implicit any in function params, untyped
   dependencies. Run `tsc --noEmit` if tsconfig exists. Count
   type coverage: typed exports / total exports.
   Report findings as BLOCKER/WARNING/SUGGESTION with evidence.",
   subagent_type="general-purpose")

   **Pattern Compliance** — "Does the code follow its own conventions?"
   Task(prompt="[project scope + CLAUDE.md rules]
   Check: naming conventions, file organization, import patterns,
   error handling style (result types vs exceptions), component
   patterns. Identify the DOMINANT pattern per category, then
   flag deviations. Drift = minority pattern diverging from majority.
   Report findings with evidence.",
   subagent_type="general-purpose")

   **Test Coverage** — "What's untested?"
   Task(prompt="[project scope]
   Check: run test coverage if available. Identify critical paths
   without tests (auth, payments, data mutations). Flag test files
   that exist but are empty or have only skipped tests. Count:
   tested modules / total modules.
   Report findings with evidence.",
   subagent_type="general-purpose")

   **Dependency Health** — "Are dependencies current and clean?"
   Task(prompt="[project scope]
   Check: outdated packages (run audit if available), unused
   dependencies (imported but not used), duplicate dependencies,
   known security advisories. Compare lock file age.
   Report findings with evidence.",
   subagent_type="general-purpose")

   **Dead Code** — "What's unused?"
   Task(prompt="[project scope]
   Check: unused exports (exported but never imported), orphaned
   files (no imports pointing to them), unreachable code branches,
   commented-out code blocks, TODO/FIXME/HACK comments older than
   the surrounding code.
   Report findings with evidence.",
   subagent_type="general-purpose")

3. **Aggregate** — Collect findings from all agents. Per dimension,
   assign a status:

   | Status | Condition |
   |--------|-----------|
   | OK | No findings or SUGGESTIONs only |
   | WARNING | WARNINGs present, no BLOCKERs |
   | BLOCKER | BLOCKERs present |

   Compute health score: start at 100, subtract per finding:
   BLOCKER = -20, WARNING = -5, SUGGESTION = -1. Floor at 0.

4. **Report** — Emit health card:

   ```
   [OBSERVE] Health: {score}/100 | {date} | Scope: {scope}
   Type Safety:        {OK/WARNING/BLOCKER} — {top finding or "Clean"}
   Pattern Compliance: {OK/WARNING/BLOCKER} — {top finding or "Clean"}
   Test Coverage:      {OK/WARNING/BLOCKER} — {top finding or "Clean"}
   Dependencies:       {OK/WARNING/BLOCKER} — {top finding or "Clean"}
   Dead Code:          {OK/WARNING/BLOCKER} — {top finding or "Clean"}

   satisfaction: {score} | confidence: {high/med/low} | basis: {measurement/observation/inspection}
   ```

   Confidence: high if tools ran (type checker, test suite); med if file
   analysis only; low if sampling.

   Below the card: per dimension, list all findings grouped by severity.
   BLOCKERs include remediation hints.

   `[EXTRACT] Key insight: [one reusable finding ≤15w]`

## Boundaries

Observe assesses codebase health. It does NOT:

- Fix, refactor, or modify any code (report only)
- Replace CI/CD pipelines (complements automated checks)
- Track changes over time (each run is a snapshot)
- Compare against external standards (the codebase is the baseline)
- Assess business logic correctness (that's verify or loop)

## Handoff

Observe is standalone — returns health card to the user. No outbound
Skill() calls.

- BLOCKERs found → user decides whether to address now or track
- Can feed into shape as `PATTERNS:` context for future tasks
- Can inform bond team design (health card shows which areas need work)
