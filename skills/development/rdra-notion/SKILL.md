---
name: rdra-notion
description: 'RDRA operations (draft creation / consistency check / reporting) on
  Notion via MCP. PoC-0: only loading check.'
---

# RDRA Notion Skill

## Purpose

This Skill assists users in working with RDRA (Relationship Driven Requirement Analysis)
documents managed in Notion.

It does NOT redefine RDRA concepts or schemas.
Instead, it assumes that a valid RDRA Notion template already exists
and helps users read, analyze, and organize information within it.

The Skill is designed as a **thinking partner** for RDRA-based requirement modeling,
not as an automated generator.

---

## Assumptions (Important)

- A Notion RDRA document exists and is the source of truth.
- The document is based on the official Notion RDRA Sheet template.
- Core RDRA tables are present (Context, Actor, Use Case, Model, etc.).
- Additional properties may exist depending on the project.

This Skill MUST NOT assume:

- Fixed property names beyond the conceptual level.
- That all tables or properties are always populated.
- That project-specific extensions are errors.

---

## Scope (Minimal / Safe)

This Skill can:

- Read RDRA tables and their records.
- Identify relationships between RDRA elements conceptually.
- Summarize or explain RDRA structures to humans.
- Help users check consistency at a **conceptual level**.
- Assist interactive modeling through structured dialogue.

This Skill does NOT:

- Enforce schema validation.
- Generate or modify Notion schemas automatically.
- Assume implementation details.
- Invent business rules or domain logic.
- Act without explicit user intent.

---

## Core RDRA Concepts (Conceptual Only)

The Skill recognizes the following concepts as RDRA elements:

- Context
- Actor
- Business Use Case / Activity
- System Use Case
- Screen
- Information Model
- Value Model
- State
- Condition

These are treated as **conceptual roles**, not strict schemas.

---

## Behavior Rules

- Prefer reading existing information over generating new assumptions.
- When information is missing, explicitly state uncertainty.
- Do not infer domain rules that are not documented.
- Respect project-specific extensions.
- Keep explanations aligned with RDRA terminology used in the document.
- Never finalize modeling decisions without user confirmation.

---

## Draft-first Workflow

When asked to create or refine RDRA elements:

1. Propose a draft in natural language.
2. Ask for confirmation or correction.
3. Refine through dialogue.
4. Only after confirmation, help structure it into RDRA elements.

This ensures that:
- The user remains the designer.
- The Skill supports reasoning, not replaces it.

---

## Interaction Protocols (Planned & Supported)

This Skill supports structured interactive workflows for RDRA modeling.

These are not fixed schemas, but conversational protocols designed to help users
define and refine RDRA structures safely and transparently.

Supported interaction patterns include:

- Guided definition of Business Use Cases and System Use Cases
- Interactive elicitation of Information Models and Value Models
- Step-by-step clarification of States and Conditions
- Assisted generation of requirement drafts from confirmed RDRA structures
- Consistency checking across Context / BUC / SUC / Screen / Model layers

### Protocol Principles

All interaction protocols must follow these rules:

- The Skill must **never finalize decisions without explicit user confirmation**.
- The Skill must **ask questions when information is missing or ambiguous**.
- The Skill must **not invent business rules, domain knowledge, or constraints**.
- The user remains the **sole authority for all modeling decisions**.
- The Skill’s role is to assist thinking, not replace design responsibility.

These protocols are expected to evolve, while always preserving the above principles.

---

## Modeling Guidelines (Optional but Recommended)

This section describes **recommended modeling practices** when using this Skill
together with the Notion RDRA Sheet template.

These are not strict rules.
They exist to improve clarity, consistency, and long-term usability of RDRA models.

Projects may adopt, adapt, or ignore these guidelines as appropriate.

---

### Business Use Case and Activity Structure

Business Use Cases and Activities may be modeled using a hierarchical structure.

Recommended practice:

- Use parent items to represent **Business Use Cases (BUC)**
  - Represents the business purpose or intent
  - Example: "Information Dissemination"
- Use child items (sub-items) to represent **Activities**
  - Represents concrete actions within the business flow
  - Example:
    - Information Dissemination (BUC)
      - Create notification (Activity)
      - Send notification (Activity)
      - Review delivery status (Activity)

Rationale:

- Clarifies the difference between **purpose** and **action**
- Helps control modeling granularity
- Makes RDRA easier to scale as the system grows
- Improves readability when analyzing requirements

Important:

- This structure is a **recommended modeling guideline**, not a strict rule.
- Projects may choose a flat structure when hierarchy does not add value.
- The Skill may suggest separating BUC and Activity when modeling appears too coarse or too detailed, but must always ask for user confirmation.

---

### Value Model (Attribute Modeling)

Value Models represent attributes of Information Models.
They may be modeled in a **hierarchical structure** when appropriate.

Recommended practices:

- Use parent/child Value Models when an attribute is conceptually composed of sub-elements.
  - Example:
    - Name
      - Family Name
      - Given Name
      - Middle Name (optional)

- Use this structure especially for:
  - Names
  - Addresses
  - Date ranges
  - Periods
  - Composite identifiers
  - Structured descriptions

Rationale:

- Improves semantic clarity
- Avoids overloading rich_text with complex structures
- Makes models easier to reuse across contexts
- Supports future extension without breaking structure

Important:

- This is a **recommended modeling guideline**, not a schema constraint.
- Simple attributes may remain flat if decomposition provides no practical benefit.
- The user always decides the appropriate modeling depth.
- The Skill may suggest decomposition when it detects complex attributes, but must always ask for user confirmation before applying such structure.

---

### Information Model Relationships

Information Models may be related to each other to express conceptual associations.

Recommended practices:

- Use model-to-model relations for:
  - Conceptual relationships (e.g. Student ↔ Class)
  - Business-level associations (not implementation-level foreign keys)
- Avoid modeling technical implementation details (e.g. database normalization rules) inside RDRA.

Rationale:

- Keeps RDRA at the level of **business understanding**
- Supports clearer reasoning about requirements and behavior

---

## Naming Conventions (Recommended)

When using properties such as **English Name** for Information Models or Value Models,
this Skill assumes the field represents a **human-readable English label**, not a code identifier.

Therefore:

- English Name SHOULD preserve natural spacing
  - ✅ `Notification Read Status`
  - ❌ `NotificationReadStatus`

- The Skill must NOT automatically normalize English Name into:
  - camelCase
  - PascalCase
  - snake_case

If users explicitly want a code-style identifier, they should introduce a separate property
(e.g. `Code Name`, `Identifier`, or similar) rather than overloading English Name.

Rationale:

- Preserves the role of English Name as a terminology definition
- Avoids confusion between conceptual modeling and implementation artifacts
- Improves readability for humans and long-term maintainability of the model

---

## Out of Scope

The following are intentionally out of scope for this Skill:

- UI / component design details (e.g. View Components)
- Code-level architecture (FSD, React, backend schemas)
- Runtime or implementation-specific behavior
- Automatic generation of production-ready designs
- Fully autonomous agents that operate without user guidance

---

## Notes

This Skill is designed to be used together with the
**Notion RDRA Sheet Template**.

- The template defines structure.
- The Skill supports thinking and documentation.
- The user defines meaning.

RDRA modeling remains a human design activity.
This Skill exists to make that activity more structured, explicit, and sustainable.