---
name: why
description: 'Use when the user asks "why does X work this way", requests design rationale, a postmortem, or a data-backed threshold. Dispatches parallel read-only investigators across seven evidence categories and returns a confidence-weighted cited narrative. Not for tasks that require source or remote-system changes; not for current runtime behavior — use how.'
---

# Why

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User asks why something works this way or why an option was picked, or requests design rationale, a postmortem, or a data-backed threshold. |
| Authority | Read-only: no file, VCS, credential, paid, published, deployed, or remote mutation. Parallel investigator subagents and a synthesizer run read-only. |
| Side effect | Parallel investigator subagents and a synthesizer run read-only; the only output is the cited narrative in chat. |
| Done | Return a confidence-weighted cited narrative with direct findings, inferences, hypotheses, gaps, and sources. |
| Invocation | Model or human. Requests concerned only with current runtime behavior, rather than motivation or rationale, are outside this trigger. |

## Inputs

Establish:

- The exact decision, implementation, regression, incident, or threshold whose rationale is in question.
- The relevant component, owner, repository, service, product area, and approximate time range when known.
- Any candidate explanation supplied by the user; treat it as a hypothesis, not evidence.
- Which of these seven evidence categories are reachable through tools already available in the environment: **source control**, **issue tracker**, **long-form docs**, **real-time chat**, **infrastructure observability**, **error tracking**, and **product analytics warehouse**.

Availability means a read-only tool or authenticated MCP can actually query the category. Do not request new credentials, add an integration, or substitute a web search for an unavailable private source. Record every unavailable category explicitly.

Use this epistemic vocabulary throughout:

- Direct finding: the cited source explicitly states the claim, or the cited primary artifact directly records the event or measurement.
- Inference: the claim follows from cited findings but is not explicitly stated by a source. Show the reasoning bridge.
- Hypothesis: a plausible explanation that the evidence does not establish. State what evidence would confirm or falsify it.
- High confidence: explicit primary evidence or multiple independent, mutually consistent sources directly support the claim.
- Medium confidence: one credible direct source or several consistent indirect sources support the claim, with a material gap remaining.
- Low confidence: the claim rests on circumstantial evidence, an ambiguous recollection, or a single indirect source.

Confidence qualifies support, not importance. Chronology alone does not establish causation. Separate what happened from why it happened, distinguish contemporaneous evidence from hindsight, and prefer source-proximate records over later summaries while retaining material contradictions.

## Procedure

1. Frame the investigation. Restate the question as a neutral rationale question, define the likely decision window, and list the seven categories with status `available` or `unavailable` and the reason. Do not assume the user's candidate explanation is correct. Done when: question is framed and all seven categories are listed with status.
2. Dispatch one parallel scout batch. In one task batch, launch exactly one read-only investigator scout for each category marked available. Do not launch scouts for unavailable categories and do not combine two available categories under one scout. Give every scout the same question, entity/time scope, epistemic vocabulary, and this response schema: category and query scope; direct findings (each with a stable citation or permalink, source date, and short quoted or precisely paraphrased evidence); inferences (each linked to supporting findings, carrying High/Medium/Low confidence); hypotheses (each carrying Low confidence unless direct evidence raises it, plus confirming or falsifying evidence); contradictions and chronology; null result or access gap; sources consulted. Every scout is read-only and must report a null result rather than filling silence with general knowledge. Done when: one scout per available category is dispatched.
3. Apply the category playbook inside each scout using `references/category-playbook.md`. Done when: each scout applies its category-specific source instructions.
4. Collect the batch without erasing nulls. Build a seven-row evidence ledger. For each category record `available with evidence`, `available but no relevant evidence`, `unavailable`, or `failed read`, plus its citations or exact gap. This null accounting is required even when another category appears decisive. Done when: seven-row ledger is built with null accounting.
5. Run one read-only synthesizer. Supply the synthesizer only the framed question, the seven-row ledger, and the scouts' cited packets. Instruct it to: answer the question directly before narrating the search; preserve the Direct finding / Inference / Hypothesis labels and High/Medium/Low confidence; merge duplicate evidence without dropping citations; reconcile chronology and surface contradictions rather than choosing silently; distinguish original rationale, later rationalization, observed outcome, and current constraint; state which alternatives were considered or explicitly say none were found; account for every category and every material gap; end with a Preserve / Change / Avoid / Risk handoff grounded only in the evidence packet. Done when: synthesizer is run with complete instructions.
6. Verify the synthesis before returning it. Check that every direct finding resolves to a supplied citation, every inference names its supporting findings, every hypothesis is visibly non-factual, all seven categories appear in source coverage, and no confidence label exceeds its evidence. Remove unsupported claims; never backfill them from model memory. Done when: synthesis passes all verification checks.

## Failure and recovery

- No read access for a category: mark it `unavailable` with the reason and continue the single batch with the remaining available categories. Never request credentials or mutate configuration.
- Available scout returns no evidence: retain `available but no relevant evidence` as a meaningful null. Do not convert it into support for or against the explanation.
- A read fails: record `failed read`, the attempted scope, and the observed failure. Continue with other category results; do not launch a replacement scout that would violate the one-scout-per-available-category batch.
- Evidence conflicts: present each supported account with its date, provenance, and confidence. Prefer neither recency nor seniority by default; explain which primary evidence would resolve the conflict.
- Citation is missing or unstable: downgrade the statement to an explicitly unsupported hypothesis or omit it. Do not present an uncited recollection as a direct finding.
- The synthesizer drops labels, citations, null accounting, or the handoff: rerun the read-only synthesis over the same evidence packet with the missing output field named. Do not repeat source collection or invent evidence.
- No category yields relevant evidence: return an insufficient-evidence narrative with all seven null/gap entries and the most useful next read-only evidence to locate. Do not manufacture a rationale.
- A source contains secrets or unnecessary personal data: omit or minimally redact that material while retaining a stable citation and enough non-sensitive context to support the claim.

## Output
A cited narrative in chat with sections in order: Answer (best-supported rationale with overall High/Medium/Low confidence), What the evidence says (Direct findings, then Inferences, then Hypotheses, each with confidence and citations), Decision chronology and alternatives, Source coverage and gaps (all seven categories with status), Handoff (Preserve/Change/Avoid/Risk tied to cited evidence or marked as inference), and Sources (deduplicated stable links with category and date).
