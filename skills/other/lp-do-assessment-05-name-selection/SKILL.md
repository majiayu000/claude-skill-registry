---
name: lp-do-assessment-05-name-selection
description: Produce a <YYYY-MM-DD>-naming-generation-spec.md for a business. Reads ASSESSMENT stage docs, extracts ICP, product, brand personality, competitive set, and any prior eliminated names, then writes a fully-structured agent-executable spec that generates 250 scored candidate names. Part 1 of a 4-part naming pipeline (spec → generate → RDAP batch check → rank).
---

# lp-do-assessment-05-name-selection — Name Selection (ASSESSMENT-05)

Produces a `<YYYY-MM-DD>-naming-generation-spec.md` tailored to a specific business. The spec is the input to a name-generation agent that produces 250 scored candidates, which are then batch-checked for .com availability via RDAP and ranked.

This skill replaced the former naming research prompt approach (obsolete since deep research tools cannot verify domain availability).

**Upstream dependency:** Operates on ASSESSMENT-04 output. Requires at minimum: a problem statement, a product/option decision, and a brand personality sketch.

Load: ../_shared/assessment/assessment-base-contract.md

## When to use

Use when a brand name is open (not yet committed) and the business has sufficient ASSESSMENT stage context.

Run on user instruction: `/lp-do-assessment-05-name-selection --business <BIZ>`

## The four-part naming pipeline

This skill produces Part 1 only. The full pipeline is:

| Part | What | Who runs it |
|------|------|-------------|
| **1 — Spec** | This skill. Reads ASSESSMENT docs, writes `<YYYY-MM-DD>-naming-generation-spec.md` | This skill |
| **2 — Generate** | Agent reads the spec and produces 250 scored candidate names | Spawn a general-purpose agent with the spec as input |
| **3 — RDAP batch check** | Shell loop hits `https://rdap.verisign.com/com/v1/domain/<name>.com` for all 250; 404 = available, 200 = taken | Bash tool |
| **4 — Rank** | Filter to available names, sort by score, produce final shortlist | Agent or inline |

## Operating mode

**SPEC AUTHORING ONLY**

**Allowed:** read ASSESSMENT docs, synthesize context, write `<YYYY-MM-DD>-naming-generation-spec.md`.

**Not allowed:** generate candidate names, check domains, make naming recommendations.

## Required inputs (pre-flight)

Read and synthesise from:

- `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-problem-statement.user.md` — falsifiable problem, user segments
- `docs/business-os/strategy/<BIZ>/s0c-option-select.user.md` — selected product option(s), price points
- `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-brand-identity-dossier.user.md` — brand personality, positioning, visual direction
- `docs/business-os/strategy/<BIZ>/s0a-research-appendix.user.md` — segment truth, purchase triggers, competitive set
- `docs/business-os/strategy/<BIZ>/s1-readiness.user.md` — ICP confirmation, outcome contract

Also check for prior naming rounds (any `*-naming-shortlist*.user.md` files under the strategy dir). If present, extract all eliminated names into the spec's elimination list.

If any file is missing, note the gap in a preflight comment at the top of the spec but proceed with available context. Do not halt.

## Output

Save to:

```
docs/business-os/strategy/<BIZ>/assessment/naming-workbench/<YYYY-MM-DD>-naming-generation-spec.md
```

If the file already exists (a prior naming round was run), **update it in place**: add newly eliminated names to the elimination list, update the ICP section if it has changed, and increment the round note at the top. Do not overwrite a spec from scratch.

## Spec structure (mandatory sections)

The output spec must contain all of the following sections. Sections §3, §4, and §5 are business-specific and must be populated from the ASSESSMENT docs. Sections §3.3 and §5 (generation patterns and output format) are universal infrastructure — copy them verbatim from the template below, do not rewrite.

### §1–§2: Brand Context and ICP Resonance

Load: modules/part-1-2.md

### §3–§4: Scoring Rubric and Generation Patterns

Load: modules/part-3-4.md

### §5–§6: Hard Blockers, Output Format, and Quality Gate

Load: modules/part-5-6.md

## Completion message

> "Naming generation spec ready: `docs/business-os/strategy/<BIZ>/assessment/naming-workbench/<YYYY-MM-DD>-naming-generation-spec.md`. Next: spawn a general-purpose agent with this spec as input to generate 250 scored candidates. Then run the RDAP batch check. Then filter and rank."

## Integration

**Upstream (ASSESSMENT-03):** Runs after `/lp-do-assessment-03-solution-selection` produces a product decision record.

**Downstream — Part 2:** Spawn a general-purpose agent with the spec. Prompt: "Read `docs/business-os/strategy/<BIZ>/assessment/naming-workbench/<YYYY-MM-DD>-naming-generation-spec.md` in full, then generate exactly 250 brand name candidates following the spec exactly. Save to `docs/business-os/strategy/<BIZ>/assessment/naming-workbench/naming-candidates-<YYYY-MM-DD>.md`."

**Downstream — Part 3 (RDAP batch):** Extract all names from the candidates file. Run:
```bash
while IFS= read -r name; do
  status=$(curl -s -o /dev/null -w "%{http_code}" "https://rdap.verisign.com/com/v1/domain/${name}.com")
  echo "$status $name"
done < names.txt
```
Filter to 404s. For Pattern D names, check the domain string, not the spoken name.

**Downstream — Part 4 (rank):** Filter candidates table to domain-available names only. Sort by Score descending. Present top 20 as the working shortlist for operator review. Save to `docs/business-os/strategy/<BIZ>/assessment/naming-workbench/naming-shortlist-<YYYY-MM-DD>.user.md`.

**Downstream (ASSESSMENT-06):** `/lp-do-assessment-06-distribution-profiling` runs after the operator has confirmed a working name from the shortlist.
