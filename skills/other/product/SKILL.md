---
name: product
description: 'Create or refine PRODUCT.md while separating evidence, aspiration, users, value, and non-goals. Triggers: "product", "create PRODUCT.md", "product boundary".'
practices: [lean-startup, ddd-bounded-context]
hexagonal_role: domain
consumes: []
produces: [PRODUCT.md]
context_rel:
- kind: supplier-to
  with: plan
skill_api_version: 1
user-invocable: true
metadata:
  tier: product
  dependencies: []
  capabilities: [shape_product_boundary]
  effects: [write_product_document]
  canonical_status: canonical
  disposition: keep_specialist
output_contract: PRODUCT.md
---

# Product

Create or refine a product contract with the user's authority.

The contract works because it forces every claim into evidence or labeled
aspiration; if a reader cannot tell which is which, the document has failed.

1. Inspect existing product, README, goals, release, and evidence sources.
2. Ask only for decisions that cannot be grounded safely from those sources.
3. State mission, users, pains, value, differentiation, non-goals, proven facts,
   assumptions, evidence gaps, and success signals.
4. Label aspiration and measurement honestly.
5. Preserve an existing PRODUCT.md unless the user authorizes replacement.
6. Return the document to the caller; Plan may use it as intent context.

Named failure mode — **aspiration laundering**: an unproven hope written in the
proven-facts section; once laundered, every downstream plan inherits a false
premise.

Anti-pattern: rewriting a healthy PRODUCT.md wholesale because the session has
fresh opinions. Corrective: refine only the sections the user asked to change
and preserve the rest byte-for-byte.

Product does not select work, invoke a loop, repair itself, validate itself, or
choose delivery.
