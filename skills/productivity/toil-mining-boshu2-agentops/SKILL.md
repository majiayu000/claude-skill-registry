---
name: toil-mining
description: 'Mine caller-supplied usage history for repeated toil and emit ranked evidence. Triggers: "mine toil", "find repeated operational work".'
practices:
- sre
- lean-startup
hexagonal_role: supporting
consumes: []
produces:
- result.json
context_rel:
- kind: supplier-to
  with: automation-shape-routing
skill_api_version: 1
user-invocable: false
context:
  window: fork
  intent:
    mode: task
  sections:
    exclude:
    - HISTORY
  intel_scope: topic
metadata:
  capabilities: [toil_mining]
  effects: []
  canonical_status: canonical
  disposition: keep_specialist
  tier: meta
  dependencies: []
  stability: experimental
output_contract: ranked evidence report under .agents/toil-mining/
---
# Toil Mining — rank repeated friction

Mine explicitly supplied session, shell, RTK, or CASS history without modifying
the sources. The result is evidence for a caller; this skill does not file work,
schedule automation, or mutate a tracker.

## Procedure

1. Record the input sources, time window, filters, and query.
2. Normalize repeated human actions while excluding machine echoes and generated
   repetitions.
3. Cluster equivalent actions and preserve representative evidence references.
4. Score each cluster from measured frequency and observed pain such as elapsed
   time, failure count, interruption, or token cost.
5. Emit a ranked report and stop.

Each candidate must contain a measured count, source references, confidence in
the clustering, pain evidence, and the smallest plausible automation shape.
Separate observations from recommendations.

## Output

Write `.agents/toil-mining/YYYY-MM-DD-candidates.md` only when the caller asks for
a local artifact; otherwise return the report inline. Include checked and
not-checked sources. Do not include owners, priorities, claims, queues, or a next
action.

## References

- [Automation shape routing](../automation-shape-routing/SKILL.md)
- [CASS](../cass/SKILL.md)
