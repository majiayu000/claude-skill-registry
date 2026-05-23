---
name: expert-council
description: 'Alias for /council --mode=debate — adversarial named-persona debate. Triggers: "expert council", "dueling council", "council of <names>". Kept one release.'
practices:
- llm-eval-harness
hexagonal_role: domain
skill_api_version: 1
user-invocable: true
context:
  window: inherit
  intent:
    mode: task
  sections:
    exclude: [HISTORY]
  intel_scope: topic
metadata:
  tier: judgment
  dependencies: [council]
  stability: experimental
  replaced_by: council
---
# /expert-council — alias for /council --mode=debate

`expert-council` has been **absorbed into the `council` skill** as its `debate`
mode. The adversarial named-persona duel — independent verdicts → 0–1000
cross-scoring → mandatory reveal → ranked decision with dissent — is now
`/council --mode=debate`.

This thin alias is kept for one release. **Invoke `/council --mode=debate`
directly.**

## Routing

| You typed | Runs |
|-----------|------|
| `/expert-council <question>` | `/council --mode=debate <question>` |
| `/expert-council` (slate of named experts) | `/council --mode=debate` — persona slate confirmed in Phase 1 |

When invoked, route immediately to `/council --mode=debate` with the same
arguments. Do not run a separate workflow.

## Where the behavior lives now

The full debate-mode contract — persona slate, the duel, the mandatory reveal,
and the score matrix — lives in the `council` skill. Read `skills/council/SKILL.md`
(its `## Debate mode` section) and follow its reference documents from there.

## See Also

- [council](../council/SKILL.md) — the family skill; `--mode=debate` is this skill's successor
