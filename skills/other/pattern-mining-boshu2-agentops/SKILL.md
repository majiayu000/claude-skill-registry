---
name: pattern-mining
description: 'Test repeated implementation shapes against independent exemplars and a holdout before routing an earned abstraction. Triggers: "mine a recurring code pattern", "is this abstraction earned", "extract invariants from implementations".'
practices:
- design-patterns
- legacy-code-seams
- design-by-contract
hexagonal_role: supporting
consumes:
- repo-context
- task-question
produces:
- pattern-mining.v1
context_rel:
- kind: customer-of
  with: research
- kind: customer-of
  with: validate
- kind: supplier-to
  with: operationalize
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
  capabilities: [pattern_mining]
  effects: []
  canonical_status: canonical
  disposition: keep_specialist
  tier: execution
  dependencies: []
output_contract: pattern-mining.v1 JSON validated by skills/pattern-mining/scripts/validate-output.sh
---

# Pattern Mining

Decide whether repeated code demonstrates a reusable rule or only a plausible
hypothesis. Similar names and syntax are not enough; the abstraction must
survive examples it was not designed around.

## Constraints

- To prevent lineage copies from faking recurrence, use independently
  implemented exemplars with repository anchors.
- Because the candidate must generalize, form it without seeing the holdout and
  back-apply every holdout-driven refinement.
- To keep weak evidence from becoming architecture, route hypotheses to
  `no-action`; only a fully proven promotion may reach `operationalize`.

## Workflow

1. State the candidate pattern and collect independently implemented
   exemplars with repository anchors. Use `research` when coverage is unclear.
2. From the exemplars, separate required invariants, legitimate variation
   points, and incidental similarity.
3. Require at least three distinct exemplars before promotion is possible.
   Form the candidate abstraction without using the holdout.
4. Test it against every exemplar, then a separate holdout. Back-apply the
   refined abstraction to the original exemplars so the holdout fix cannot
   silently break them.
5. Emit `outcome: promote` only when the exemplar floor, holdout, and
   back-application all pass. Route that evidence to `operationalize`, which
   decides whether the eventual shape is a skill, gate, library, template, or
   no action.
6. Otherwise emit `outcome: hypothesis` with `route: no-action`. Keep the
   evidence bounded and name what additional observation would retest it.

## Output Specification

- **Artifact directory:** `.agents/patterns/<run-id>/`
- **Filename convention:** `pattern-mining.json`
- **Format:** `pattern-mining.v1` JSON containing the outcome, distinct
  exemplars, invariants, variations, incidental details, holdout result,
  back-application result, and route.
- **Validation command:** `skills/pattern-mining/scripts/validate-output.sh <pattern-mining.json>`
- **Downstream handoff:** pass a validated `promote` artifact to
  `operationalize`; retain a validated `hypothesis` artifact as bounded
  evidence with `route: no-action`.

Promotion requires at least three distinct exemplars, one separate passing
holdout, successful back-application, and at least one invariant. Any weaker
packet remains a hypothesis and cannot route to reusable packaging.

The validator is the machine boundary:

```bash
skills/pattern-mining/scripts/validate-output.sh <pattern.json>
```

This skill owns evidence for the pattern. It never creates the reusable
artifact itself and never promotes a failed or untested holdout.

Executable behavior:
[references/pattern-mining.feature](references/pattern-mining.feature).

## Quality

- Exemplars are independent and repository-anchored; copied implementations do
  not inflate the evidence floor.
- Invariants, legitimate variations, and incidental similarities stay distinct
  through holdout testing and back-application.
- The named validator passes before a promotion reaches `operationalize` or a
  hypothesis is retained as `no-action` evidence.

## Do not

- Count copies from one implementation lineage as independent exemplars.
- Hide variation by calling it incidental.
- Route a hypothesis directly to a skill, rule, gate, or library.
