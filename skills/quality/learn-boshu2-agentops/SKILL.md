---
name: learn
description: 'Optionally analyze collections of durable verdicts for recurring evidence after the critical path. Triggers: "learn from verdicts", "mine validation history".'
practices:
- continuous-learning
- evidence-based-engineering
hexagonal_role: supporting
consumes:
- verdict.v2
produces:
- learning-observations
context_rel:
- kind: customer-of
  with: validate
skill_api_version: 1
user-invocable: true
metadata:
  graph_root: false
  tier: execution
  dependencies: []
  capabilities: [analyze_verdict_collections]
  effects: [write_advisory_observations]
  canonical_status: canonical
  disposition: keep_off_path
output_contract: advisory learning observations
---

# Learn

Learn is an optional, off-path consumer of durable `verdict.v2` collections.
It may summarize recurring evidence and propose a candidate deterministic check
for later human or caller evaluation.

Learn does not run during RPI, validate a subject, alter a verdict, mutate a
plan, promote a rule, choose continuation, or emit a lifecycle receipt. Missing
Learn output never changes whether a candidate is valid.

When invoked, bind every observation to verdict and finding digests, distinguish
repeated objectives from repeated reviews of one objective, disclose the sample
size, and stop at advisory evidence.
