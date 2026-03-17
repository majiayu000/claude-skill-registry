---
name: verify
description: Fast parallel verification before PR. Use when "verify", "review my changes", "is this ready", "pre-review", "check before PR", or after loop completes.
model: opus
---

# Role

VERIFY. Spawn parallel specialist agents to assess changed code across
independent quality dimensions. Aggregate findings into a gate decision.
Fast pre-flight, not thorough audit.

## Principles

1. **Parallel over sequential** — Specialist agents run simultaneously.
   Each dimension is independent. No agent needs another's output.
2. **Changed files only** — Scope to `git diff` output. Never review
   the entire codebase. Smaller scope = faster, more precise findings.
3. **Observable evidence required** — Every finding must cite a file,
   line, or command output. "Looks risky" without evidence = discard.
4. **BLOCKERs are non-negotiable** — SHIP gate cannot open with active
   BLOCKERs. User can override explicitly, but the gate signals BLOCK.
5. **Complement, don't repeat** — Loop reviews against spec + mustNot
   (internal consistency). Verify reviews against external quality
   (security, performance, standards). No overlap.

## Process

1. **Scope** — Collect changed files:

   Run `git diff --name-only HEAD` (unstaged + staged). If empty
   (changes already committed), fall back to `git diff --name-only
   main...HEAD` (branch diff). If a shape context exists, read
   criteria[] and mustNot[] for context — but verify does NOT check
   against them (that's loop's job).

   If no changes detected in either diff: report "Nothing to verify"
   and stop.

   Announce: `[VERIFY] Scanning {N} changed files across 4 dimensions`

2. **Spawn specialists** — 4 parallel agents via Task tool.

   Each agent receives: changed file list + file contents + dimension
   instructions. Each produces findings as:
   `{severity} — {file}:{line} — {finding} — {evidence}`

   digraph verify {
     rankdir=LR
     scope -> correctness
     scope -> security
     scope -> performance
     scope -> standards
     correctness -> aggregate
     security -> aggregate
     performance -> aggregate
     standards -> aggregate
     aggregate -> gate
   }

   **Correctness** — "Do the changes work as intended?"
   Task(prompt="[changed files + contents]
   Check: types compile, tests pass (run them), logic errors,
   edge cases, error handling gaps. Run `tsc --noEmit` and
   test commands if available. Report findings as
   BLOCKER/WARNING/SUGGESTION with file:line evidence.",
   subagent_type="general-purpose")

   **Security** — "Do the changes introduce vulnerabilities?"
   Task(prompt="[changed files + contents]
   Check: injection (SQL, XSS, command), auth gaps, secrets in
   code, unsafe deserialization, SSRF, path traversal. Read
   CHANGED files only. Report findings as
   BLOCKER/WARNING/SUGGESTION with file:line evidence.",
   subagent_type="general-purpose")

   **Performance** — "Do the changes degrade performance?"
   Task(prompt="[changed files + contents]
   Check: N+1 queries, unbounded loops, missing pagination,
   large bundle imports, unnecessary re-renders, missing
   memoization. Measure where possible (bundle size, query count).
   Report findings as BLOCKER/WARNING/SUGGESTION with evidence.",
   subagent_type="general-purpose")

   **Standards** — "Do the changes follow project conventions?"
   Task(prompt="[changed files + CLAUDE.md conventions]
   Check: naming conventions, file organization, import patterns,
   error handling patterns, design system usage, accessibility.
   Compare against CLAUDE.md rules and dominant codebase patterns.
   Report findings as BLOCKER/WARNING/SUGGESTION with evidence.",
   subagent_type="general-purpose")

3. **Aggregate** — Collect findings from all agents. Deduplicate
   (same file:line, same concern = merge). Sort: BLOCKERs first,
   then WARNINGs, then SUGGESTIONs.

   Gate decision:

   | Condition | Gate | Action |
   |-----------|------|--------|
   | Any BLOCKER | **BLOCK** | Must fix before PR |
   | WARNINGs only | **FIX** | Recommend addressing |
   | SUGGESTIONs only | **SHIP** | Good to go |
   | No findings | **SHIP** | Clean |

4. **Report** — Emit verification card:

   ```
   [VERIFY] Gate: {SHIP/FIX/BLOCK} | Files: {N} | Findings: {B}B {W}W {S}S
   ```

   Per finding (grouped by dimension):
   `{severity} — {file}:{line} — {finding}`

   If BLOCK: list BLOCKERs with remediation hints.
   If FIX: list WARNINGs, note they're advisory.
   If SHIP: one-line confirmation.

   Footer: `satisfaction: {0-100} | confidence: {high/med/low} | basis: execution`
   Score: 100 - (BLOCKERs×25 + WARNINGs×5 + SUGGESTIONs×1), floor 0.

## Boundaries

Verify assesses external quality of changed code. It does NOT:

- Check against spec or criteria (that's loop's review phase)
- Fix issues (report only — user or loop handles remediation)
- Review unchanged code (scope is git diff only)
- Replace human review (pre-flight, not final authority)
- Run on its own without changes (no changes = no verify)

## Handoff

Verify is a terminal assessment — it returns the gate decision to the
user. No outbound Skill() calls.

- BLOCK → user fixes or invokes loop for remediation
- FIX → user decides, then proceeds to PR
- SHIP → user creates PR
