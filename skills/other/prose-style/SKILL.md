---
name: prose-style
description: Reusable writing-style contract for agent outputs (reports, ARCH docs, verdicts, threat models). Forces direct prose with concrete evidence, no marketing voice, no hedge words. The single most-referenced skill across the pipeline — used by 28 agents.
when_to_use: |
  Apply to every agent that writes a human-readable artefact:
  - architect ARCH-*.md, ADR-*.md
  - pm PLAN-*.md
  - qa-engineer QA-*.md reports
  - security-officer CSO audit reports
  - 18 reviewer agents' REVIEW-*.md outputs
  - threat-models TM-*.md
  Do NOT apply to:
  - Raw code (use language-native style guides instead)
  - Verdict log lines (machine-parsed, format is fixed)
  - Beads task titles/descriptions (length-bounded, plain text)
effort: low
allowed-tools: Read, Write
paths:
  - "docs/**"
  - ".great_cto/verdicts/**"
---

# Prose style — writing contract for agent reports

great_cto reports are read by busy CTOs at 3pm on a Tuesday. They scan for
facts, decisions, and what needs their attention. Marketing voice and
hedge words waste their time.

## Five rules

### 1. Lead with the conclusion

Bad:
> After reviewing the architecture document and considering various
> trade-offs, including but not limited to scalability, security, and
> maintainability, we believe that the proposed approach is generally
> acceptable but has some areas that could potentially be improved.

Good:
> Approved with 2 changes required: (a) move PII encryption to KMS, (b)
> add idempotency key on webhook handler. Details below.

### 2. Concrete evidence, not adjectives

Bad: "Performance is acceptable."
Good: "p99 latency 142ms over 50K requests (k6 run 2026-05-12 14:00 UTC, `tests/load/api.js`). SLO is 200ms."

Bad: "Security looks good."
Good: "No findings at Critical or High. 2 Medium: hardcoded log level in `src/logger.ts:14`, missing CORS header in `src/middleware/cors.ts:8`."

### 3. No hedge words

Banned: *generally, somewhat, fairly, mostly, kind of, sort of, more or
less, in some cases, often, sometimes, occasionally, possibly, perhaps,
maybe, could potentially, might want to consider*.

Replace with specifics or omit. If you genuinely don't know, say "uncertain
because <reason>" — that's information.

### 4. No filler openings

Banned:
- "In this document, we will discuss..."
- "It's important to note that..."
- "First and foremost..."
- "At the end of the day..."
- "It goes without saying..."

If a sentence can be deleted without losing information, delete it.

### 5. Verdict line on the last line

Every terminal report ends with one of:

```
VERDICT: APPROVED — <one-line summary>
VERDICT: DONE — <one-line summary>
VERDICT: BLOCKED reason="<specific blocker>"
VERDICT: FAIL reason="<specific failure>"
```

This is parsed by the board's `readVerdicts()` function. Format is
machine-readable — no flourishes.

## Templates

### Reviewer report

```markdown
# REVIEW-<feature> — <reviewer name>

Reviewed: <commit-sha or file paths>
Standard: <regulation / framework you applied>

## Findings
- [Critical|High|Med|Low] <one-sentence finding>
  - location: <path:line>
  - rationale: <why this matters in this domain>
  - remediation: <specific fix>

## Verdict
VERDICT: APPROVED|BLOCKED reason="<short>"
```

### Architecture / ADR

```markdown
# ARCH-<feature> | ADR-<NNN>

Date: <ISO>
Status: proposed | accepted | superseded

## Context
2-4 sentences. What problem, what constraint.

## Decision
Imperative single sentence: "Use X for Y."

## Consequences
- Positive: <bullets>
- Negative: <bullets>
- Reversible? yes/no — if no, document migration cost

## Alternatives considered
<bullets with one-line dismissal reason each>
```

## Anti-patterns to grep for

Before writing the verdict line, search your draft for:

```
\b(generally|somewhat|fairly|mostly|kind of|sort of|possibly|perhaps|maybe)\b
```

If a hit is in a non-quoted sentence, rewrite it to be concrete or delete it.

## Why this matters

The board's `readVerdicts()` parses every report. Marketing voice breaks
the parser. Hedge-word reports waste the reader's time. Specifics let the
CTO trust the agent's judgment.
