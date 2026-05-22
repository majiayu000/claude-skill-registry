---
name: doc-editing
description: Use when the user asks to edit, polish, or rewrite documentation or long-form prose to improve clarity and structural quality, aiming for publishable text without tone drift or unnecessary structural churn.
---

# Doc Editing

Edit documentation and long-form prose to be clear, precise, and easy to scan.

## Response Contract

- Deliverable: apply the edits to the target document.
- Chat output: Do not restate the document content in the chat.

## Document Model

Definitions used to reason about documents and edits.

### Semantic Layers

A document can contain two kinds of description.

- **Meta description**
  Constraints on how the document should be written or edited, such as audience, scope, tone, formatting expectations, and must-not-change constraints.

- **Content description**
  Subject matter that belongs in the document, including anything the user explicitly requests to be included as part of the document.

### Structure Forms

A document can be organized using two structural forms.

- **Module structure**
  The document is divided into modules by responsibility. Each responsibility has a stable home.

- **Enumeration structure**
  Within one responsibility, items are listed as peers under a single framing.

## Editing Standards

Apply these standards throughout the edit. Each standard is single-sourced here and referenced elsewhere by its ID.

- **layers.distinct — Keep layers distinct**
  Keep meta description distinct from content description unless meta-level material is explicitly part of the subject matter. If the user explicitly requests that meta-level material be included in the document as content, treat it as content.

- **meaning.preserve — Preserve meaning**
  Preserve the document’s meaning, claims, and intent while improving clarity and structure.

- **facts.no_new — No new facts**
  Do not introduce new factual content, new claims, or new conclusions that are not present in the source text or explicitly provided by the user.

- **structure.modules — Stable responsibility modules**
  Use module structure to assign each major responsibility a stable home. Keep module boundaries clear and headings responsibility-oriented. Place meta-level material that is included as content into a deliberate, clearly bounded module.

- **structure.enumerations — Peer enumerations only**
  Use enumeration structure only to list peers within one responsibility. If a list mixes responsibilities, restructure it into module structure.

- **meta.constraints — Enforce meta constraints**
  Treat meta description constraints as hard constraints. When a potential improvement would violate a meta constraint, prefer preserving the constraint and choose the least-invasive alternative that still improves clarity.

## Workflow

Use a repeatable editing pass.

1. Identify the document’s subject and extract meta description constraints. Apply `layers.distinct` and `meta.constraints`.
2. Confirm what must be preserved and what additions, if any, the user explicitly requested. Apply `meaning.preserve` and `facts.no_new`.
3. Establish or repair module structure for major responsibilities, align headings to responsibilities, and relocate material to its responsible module. Apply `structure.modules`.
4. Normalize enumerations within each module; convert mixed-responsibility lists into module structure. Apply `structure.enumerations` and `structure.modules`.
5. Edit prose for clarity and precision without changing intent or adding facts. Apply `meaning.preserve` and `facts.no_new`.
6. Do a final pass for internal consistency and constraint compliance.
7. Run acceptance checks.

## Acceptance Criteria

A revision is complete only if all checks pass.

- **Response**: Output satisfies the Response Contract.
- **Standards satisfied**: `layers.distinct`, `meaning.preserve`, `facts.no_new`, `structure.modules`, `structure.enumerations`, `meta.constraints`.
