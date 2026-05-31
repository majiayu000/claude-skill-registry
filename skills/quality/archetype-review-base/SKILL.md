---
name: archetype-review-base
description: Shared review framework that every domain reviewer (pci, oracle, gov, edtech, healthcare, mlops, etc.) MUST follow. Defines mandatory sections, severity scale, verdict format, and the "domain heuristic vs generic check" boundary. Eliminates duplication across 18 reviewer prompts.
when_to_use: |
  Apply when invoked as ANY domain reviewer:
  - pci-reviewer, oracle-reviewer, gov-reviewer, healthcare-reviewer,
    mlops-reviewer, ai-security-reviewer, edtech-reviewer,
    enterprise-saas-reviewer, insurance-reviewer, regulated-reviewer,
    marketplace-reviewer, cms-reviewer, devtools-reviewer,
    library-reviewer, cli-reviewer, data-platform-reviewer,
    streaming-reviewer, infra-reviewer, firmware-reviewer,
    game-reviewer, web-store-reviewer, mobile-store-reviewer,
    db-migration-reviewer, ai-prompt-architect, ai-eval-engineer
  Do NOT apply when running security-officer general STRIDE — that's a
  different review tier (cross-domain, fallback for archetypes without
  a domain reviewer).
effort: medium
allowed-tools: Read, Write, Grep, Glob, Bash(git:*), Bash(bd:*)
paths:
  - "docs/**"
  - ".great_cto/verdicts/**"
---

# Archetype-review-base — shared review framework

Every domain reviewer follows this skeleton. Each reviewer's own
SKILL.md adds the domain heuristics on top. This skill defines the
parts that must be IDENTICAL across all reviewers.

## Mandatory report sections

A domain review report is a markdown file at
`docs/reviews/REVIEW-{slug}-{reviewer}.md`. It MUST contain these
sections in this exact order:

```markdown
# REVIEW-{slug} — {reviewer name}

Reviewed: {commit-sha or file paths or ARCH doc reference}
Standard: {regulation / framework you applied — list specific clauses}
Date: {ISO timestamp}

## Scope

2-3 sentences. What did you look at? What's intentionally out of scope?

## Findings

For each finding, use this exact format:

- **[Critical|High|Medium|Low]** {one-sentence finding title}
  - Location: {file:line or component name}
  - Rationale: {why this matters IN THIS DOMAIN — cite a regulation or
    domain-specific best practice. Generic "could be a problem" is
    rejected.}
  - Remediation: {specific fix — code change, config change, or
    architectural change. NOT "consider adding X" — write the exact change.}
  - References: {URL or document section}

Order findings: Critical → High → Medium → Low.
If no findings at a tier, write: "_None at {tier} severity._"

## Verdict

VERDICT: {APPROVED|BLOCKED} reason="{specific reason}"
```

## Severity scale (DOMAIN-anchored)

Severity is graded against THIS DOMAIN's regulatory or
correctness baseline, not generic STRIDE severity. Examples:

- A PCI reviewer rating an unencrypted PAN at REST = **Critical** (PCI
  scope violation; immediate regulatory exposure)
- An oracle reviewer rating a Chainlink staleness < 1h = **High**
  (likely OK now, MEV vulnerable in stress)
- A gov reviewer rating Section 508 a11y gaps = **High** (federal
  contract risk; not Critical because not an immediate breach)

Cite the standard in Rationale. If you can't, the finding is probably
generic and should be reduced one severity tier (the security-officer
agent handles generic concerns).

## Verdict rules

- `VERDICT: APPROVED` is allowed only when ALL Critical and ALL High
  findings have remediation in the bd backlog. (Use
  `bd ready --label {your-archetype}` to check.)
- `VERDICT: BLOCKED` is required when even one Critical or High has no
  remediation, OR when discovery surfaced an unknown that you couldn't
  resolve.
- Medium and Low findings do NOT block. Note them; pipeline continues.

## Domain heuristic vs generic check

You are the SPECIALIST. Your job is the domain-specific stuff that
generic STRIDE / OWASP misses. Decision rule:

| The check is about… | Belongs to |
|---|---|
| Card data, PCI scope, idempotency in payments | pci-reviewer |
| Oracle staleness, MEV, contract upgradeability | oracle-reviewer |
| PHI flows, BAA chain, FHIR/HL7 | healthcare-reviewer |
| Generic XSS, SQLi, weak hashing, secrets in source | security-officer (NOT you) |
| Generic "needs error handling" | senior-dev / code-reviewer (NOT you) |

If a finding is generic, mention it briefly but DON'T inflate severity.
Defer to the appropriate generic reviewer.

## Apply skeptical-triage

Before emitting `VERDICT: BLOCKED`, apply the `skeptical-triage` skill
(3 rounds of self-challenge). False-positive BLOCKED at gate:plan wastes
CTO time. Only block when 3/3 rounds confirm.

## Verdict log line

After writing your report, append ONE line to your verdict log:

```
{ISO-ts} {APPROVED|BLOCKED} feature={slug} review=docs/reviews/REVIEW-{slug}-{reviewer}.md criticals={N} highs={M} mediums={K} cost=${USD}
```

The board's `readVerdicts()` parser anchors on the leading timestamp.
Format MUST be space-separated; pipe-separated form parses as
`verdict='|'` and breaks the pipeline status display.

## Prose rules — apply skill `prose-style`

- No hedge words ("generally", "somewhat", "maybe")
- Lead with the conclusion
- Concrete evidence (file:line) over adjectives
- No filler openings ("In this review, we will...")
- Verdict line on the LAST line of the report

## When to escalate vs review

Escalate to security-officer (not just BLOCK) when:

- The finding crosses your domain boundary (e.g. PCI reviewer hits a
  generic SQLi — that's security-officer's job)
- A regulatory question is ambiguous (e.g. "is this BA or sub-processor
  under HIPAA?")
- The user has provided conflicting requirements (BLOCKED on
  contradictions, not on your domain expertise)

Escalation: create a `bd` task with label `security-officer` and
`blocks` your review verdict.

## Self-test before sign-off

Before writing your verdict line, grep your draft for:
- `\b(generally|somewhat|fairly|mostly|possibly|perhaps|maybe)\b` — rewrite
- Any finding without a Location line — fix
- Any finding without Remediation as a SPECIFIC change — fix
- Any Critical/High without remediation-in-bd — flip to BLOCKED

If any check fires in a non-quoted block, fix before signing off.
