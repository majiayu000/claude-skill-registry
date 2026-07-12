---
name: idea-genie
description: 'Generate an evidence-grounded opportunity portfolio for an open-ended product or engineering question. Triggers: "generate ideas from repository evidence", "what should we build next", "find supported opportunities".'
practices:
- bdd-gherkin
- lean-startup
- design-by-contract
hexagonal_role: domain
consumes:
- repo-context
- task-question
produces:
- idea-portfolio.v1
context_rel:
- kind: customer-of
  with: research
- kind: customer-of
  with: behavior-first-planning
- kind: supplier-to
  with: discovery
skill_api_version: 1
user-invocable: true
context:
  window: fork
  intent:
    mode: task
  sections:
    exclude:
    - HISTORY
  intel_scope: topic
metadata:
  tier: execution
  dependencies:
  - research
output_contract: idea-portfolio.v1 JSON validated by skills/idea-genie/scripts/validate-output.sh
---

# Idea Genie

Turn an open-ended question into a small, evidenced opportunity portfolio. This
skill explores; it does not select work, create beads, or write Discovery's BDD
intent packet.

## Constraints

- Keep this lane exploratory because `discovery` owns selection, BDD shaping,
  and tracker persistence.
- Cite repository or executable evidence for observations to prevent assumptions
  from masquerading as facts.
- Stop on novelty saturation because fixed idea quotas manufacture unsupported
  work.

## Workflow

1. State the question, constraints, non-goals, and evidence sources. Use
   `research` when the repository facts are not already available.
2. Record observations as claims with repository or executable evidence. Put
   unverified beliefs in `assumptions`; never blend them into observations.
3. Propose candidate mechanisms. Give every candidate its own evidence,
   overlap result against live skills, CLI capabilities, and tracked work, plus
   one Given/When/Then scenario.
4. Run another novelty pass. Merge equivalents and discard unsupported ideas.
   Stop when the pass yields zero materially new candidates, not when an
   arbitrary count is reached.
5. Write `idea-portfolio.v1`, run `scripts/validate-output.sh`, and hand the
   artifact to `discovery`. Discovery alone shapes and persists executable BDD
   intent.

If every candidate overlaps existing work or lacks support, emit
`status: no-new-work`, an empty candidate list, and observations showing why.
An honest empty portfolio is a successful result.

## Output Specification

- **Artifact directory:** `.agents/ideas/<run-id>/`
- **Filename convention:** `idea-portfolio.json`
- **Format:** `idea-portfolio.v1` JSON with the schema fields below.
- **Validation command:** `skills/idea-genie/scripts/validate-output.sh <portfolio.json>`
- **Downstream handoff:** pass the validated artifact path to `discovery`; only discovery
  shapes and persists executable BDD intent.

Required fields are `schema_version`, `status`, `observations`, `assumptions`,
`candidates`, and `termination`. Candidate portfolios require cited evidence,
an explicit `overlaps` array, and a complete scenario. Termination records the
reason and `novel_candidates_last_pass: 0`.

The validator is the machine boundary:

```bash
skills/idea-genie/scripts/validate-output.sh <portfolio.json>
```

Executable behavior: [references/idea-genie.feature](references/idea-genie.feature).

## Quality

- Every observation has a nonempty evidence pointer and assumptions remain
  explicitly separate.
- Every candidate carries overlap results and a complete Given/When/Then
  scenario, or the artifact honestly reports `no-new-work`.
- The named validator passes before the artifact path is handed to `discovery`.
