---
name: lp-do-assessment-04-candidate-names
description: Full naming pipeline orchestrator (ASSESSMENT-04). Runs four parts in sequence: (1) produce <YYYY-MM-DD>-naming-generation-spec.md from ASSESSMENT docs, (2) agent generates 250 scored candidates, (3) RDAP batch check all .com domains, (4) filter to available names and produce ranked shortlist. Delivers a final operator-ready shortlist of domain-verified, scored brand name candidates.
---

# lp-do-assessment-04-candidate-names — Candidate Names Pipeline (ASSESSMENT-04)

Load: ../_shared/assessment/assessment-base-contract.md

Orchestrates the complete four-part naming pipeline from a standing start to a domain-verified, ranked shortlist. The operator receives a shortlist where every name has a confirmed available .com and a multi-dimension quality score.

## When to use

Use when a brand name is open (not yet committed) and the business has completed ASSESSMENT-03 (product option selected). Run on user instruction:

```
/lp-do-assessment-04-candidate-names --business <BIZ>
```

Rerunnable. If a spec and/or candidates file already exist from a prior round, the pipeline resumes from the correct part rather than starting over — see §Resume logic below.

---

## Execution

### Parts 1–3: Spec, Generate, RDAP Check

Load: modules/part-1-3.md

### Parts 4–5: Rank and Render HTML

Load: modules/part-4-5.md

---

## Resume logic

If the pipeline is interrupted or rerun, check which parts are already complete:

| Condition | Resume from |
|-----------|-------------|
| No spec exists | Part 1 |
| Spec exists, no candidates file | Part 2 |
| Candidates file exists, no RDAP file | Part 3 |
| RDAP file exists, no shortlist `.md` | Part 4 |
| Shortlist `.md` exists, no `.html` | Part 5 |
| Shortlist `.html` exists | Pipeline complete — await operator review |

When resuming from Part 2 after a new round (new eliminated names added to spec), use a new date-stamped candidates filename so prior rounds are preserved.

---

## Quality Gate and New Round Logic

Load: modules/quality-gate.md

---

## Completion message

Present the top 10 from the shortlist inline in the conversation, preceded by the score key:

> **Score key:** D = Distinctiveness · W = Wordmark quality · P = Phonetics (IT+EN) · E = Expansion headroom · I = ICP resonance · Score = sum out of 25
>
> **Naming pipeline complete — <BIZ> Round N**
> N domain-verified names found from 250 candidates. Top 10:
>
> | Rank | Name | Score | D | W | P | E | I | .com domain |
> |------|------|-------|---|---|---|---|---|-------------|
> | 1 | ... | ... | ... | ... | ... | ... | ... | available |
> | ... |
>
> Full shortlist (top 20) saved to:
> - `naming-shortlist-<date>.user.md` (source of truth)
> - `naming-shortlist-<date>.user.html` (formatted view — open in browser)
>
> To select a name, say which one. To reject and try again, say "none of these work" — optionally tell me why and I'll encode it as a constraint for the next round.

---

## Integration

**Upstream (ASSESSMENT-03):** Runs after `/lp-do-assessment-03-solution-selection` produces a product decision record.

**Downstream (ASSESSMENT-06):** `/lp-do-assessment-06-distribution-profiling` runs after the operator confirms a working name from the shortlist.
