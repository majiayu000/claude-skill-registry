---
name: idea-genie
description: 'Generate an evidence-grounded opportunity portfolio for an open-ended product or engineering question. Triggers: "idea genie", "what should we build", "supported opportunities".'
practices: [lean-startup, bdd-gherkin]
hexagonal_role: domain
consumes: [repo-context, task-question]
produces: [idea-portfolio.v1]
context_rel:
- kind: customer-of
  with: research
- kind: supplier-to
  with: plan
skill_api_version: 1
user-invocable: true
metadata:
  tier: execution
  dependencies: []
  capabilities: [generate_evidenced_options]
  effects: [write_idea_portfolio]
  canonical_status: canonical
  disposition: keep_strategy
output_contract: idea-portfolio.v1 JSON validated by skills/idea-genie/scripts/validate-output.sh
---

# Idea Genie

Generate a small portfolio of evidenced options. This skill explores; it does
not select, schedule, track, implement, or validate work.

1. State the question, constraints, non-goals, and sources.
2. Separate cited observations from assumptions.
3. Give each candidate its supporting evidence, overlap with existing
   capabilities, and one normal or edge scenario.
4. Run a novelty pass, merge equivalents, and discard unsupported ideas.
5. Stop when no materially new evidenced candidate appears.
6. Write and validate `idea-portfolio.v1`, then return it to the caller or Plan.

An empty `no-new-work` portfolio is valid. Plan alone may incorporate a selected
option into the existing bead or caller intent.
