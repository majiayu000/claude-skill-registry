---
name: premortem
description: 'Use when: an exact plan needs a verdict.'
---
# Premortem Skill

> **Question:** Is this exact plan ready to implement?
> **Boundary:** Premortem owns the only semantic plan-readiness verdict.

## Constraints

- Judge the plan, never the implementation or delivery mechanism.
- Use one fresh-context judge with `author_id != judge_id`. Model and family
  metadata are optional; no risk class requires different model families.
- Bind the verdict to the repository-relative plan path and its SHA-256. Any
  plan edit invalidates the verdict.
- Emit exactly `PASS` or `FAIL`. `PASS` has zero blockers. `FAIL` contains the
  complete nonempty blocker set in one response.
- Report only concrete, evidence-bound defects that invalidate acceptance,
  correctness, safety, dependencies, scope, or a claimed contract.
- Do not own retries, attempt maps, budgets, helper state, implementation,
  delivery, tracker closure, or operator escalation. The orchestrator chooses
  repair or replanning after reading the verdict.
- A council, mixed panel, or Dueling Idea Genies artifact may inform the judge,
  but none substitutes for this exact-plan verdict.

## Loop position

Premortem runs once after Plan freezes the final plan and before the first
implementation leaf is pulled. It consumes the plan plus its acceptance,
dependency graph, write scopes, non-goals, rollback, and deterministic planning
receipts. It produces one immutable `premortem-plan-verdict.v1` JSON artifact.

Between implementation waves, reuse the verdict while the exact plan digest is
unchanged. A materially changed plan requires an explicit orchestrator request
for a new Premortem verdict; Validate and Learn cannot invoke Premortem themselves.

## Execution

1. Resolve one current plan path. Reject a missing or stale plan rather than
   inferring intent from chat.
2. Compute the plan SHA-256 and record the plan author identity.
3. Retrieve only directly matched compiled prevention from
   `.agents/premortem-checks/*.md`, falling back to
   `.agents/findings/registry.jsonl`. Missing inputs skip silently; malformed
   entries are ignored with one concise warning.
4. Dispatch one runtime-native fresh judge. Use Council only when the operator
   explicitly requests a panel or the decision is genuinely contested.
5. Check all applicable acceptance, dependency, write-scope, migration,
   reversibility, test-shape, capability-reuse, and rollback claims. The
   detailed checklist is in
   [mandatory-checks.md](references/mandatory-checks.md).
6. Return the complete blocker set once. Cosmetic, theoretical, pre-existing,
   and out-of-scope observations are notes, not blockers.
7. Write the JSON verdict and validate both its schema and live plan digest:

   ```bash
   skills/premortem/scripts/validate-output.sh \
     .agents/council/YYYY-MM-DD-premortem-<topic>.json \
     "$(git rev-parse --show-toplevel)"
   ```

## Verdict contract

```json
{
  "schema_version": "premortem-plan-verdict.v1",
  "plan": {"path": ".agents/plans/example.md", "sha256": "<64 hex>"},
  "author_id": "planner-context",
  "judge_id": "fresh-judge-context",
  "verdict": "PASS",
  "blockers_complete": true,
  "blockers": []
}
```

For `FAIL`, each blocker has a stable `id`, a concrete `claim`, and one or more
`evidence` references. Optional `author_model` and `judge_model` objects may
record `name` and `family`; the validator deliberately does not compare family.

## Output Specification

- **Artifact path:** `.agents/council/YYYY-MM-DD-premortem-<topic>.json`
- **Schema:** [plan-verdict.schema.json](schemas/plan-verdict.schema.json)
- **Validator:** `skills/premortem/scripts/validate-output.sh <verdict> <repo-root>`
- **Downstream handoff:** `PASS` permits the orchestrator to pull the first
  implementation leaf. `FAIL` returns the complete evidence set to the
  orchestrator for one consolidated repair decision or replanning.

## Quality checklist

- The recorded plan digest matches the file the judge actually read.
- Author and judge identities differ.
- The verdict is binary and the blocker set is explicitly complete.
- Every blocker cites the plan or a deterministic evidence path.
- No optional review topology is presented as readiness authority.

## References

- [mandatory-checks.md](references/mandatory-checks.md)
- [premortem.feature](references/premortem.feature)
- [scope-mode.md](references/scope-mode.md)
- [temporal-interrogation.md](references/temporal-interrogation.md)
- [examples.md](references/examples.md)
- [write-premortem-output.md](references/write-premortem-output.md)
- [compiled-prevention.md](references/compiled-prevention.md)
