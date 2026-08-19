---
name: iso-24495-2
description: Sector-specific Plain Language standard for legal communication (ISO 24495-2:2025). Applied during contract drafting, license review, and legal/compliance writing.
metadata:
  version: "0.5.0"
  iso-standard: "ISO 24495-2:2025"
  iso-status: "published"
---

# ISO 24495-2:2025 - Plain Language (Legal Communication)

Extends ISO 24495-1:2023 for legal documents, contractual provisions, licenses, and regulatory compliance.

## Scope & Execution Boundaries

1. **Thinking Block Exemption:**
   - Internal reasoning and legal analysis within thinking blocks (`<thought>`, `<thinking>`) are **100% exempt** from plain language constraints.
   - Reason exhaustively within thinking blocks. Apply plain language rules strictly to final user-facing legal text.

2. **Legal Enforceability Primacy:**
   - Plain language simplification must **never** alter legal rights, liabilities, or contractual enforceability. If a term of art is legally required to avoid ambiguity, retain it and provide a plain explanation.

---

## Quantitative Rules & Hard Constraints (User-Facing Output)

1. **Modal Verb Standardisation:**
   - Use **must** for mandatory obligations (*"The User must pay..."*).
   - Use **must not** for prohibitions (*"The User must not copy..."*).
   - Use **may** for discretionary permissions, as in "the User may end the agreement".
   - **Banned Words:** Never use *"shall"*, *"should"*, *"hereby"*, *"hereinafter"*, *"wherefore"*, or *"parties of the first part"*.

2. **Explicit Subject Actor Identification:**
   - Every obligation sentence MUST explicitly name the subject actor (*"The Licensee must notify..."* rather than *"Notice must be provided..."*).

3. **Conditional Clause Formatting:**
   - Format multi-condition legal clauses as structured itemised lists:
     - **Trigger / Prerequisite:** What condition initiates the rule.
     - **Obligation / Action:** What action must or may be taken.
     - **Consequence:** What occurs upon non-compliance.

---

## Contrastive Examples

### Example 1: Contractual Obligation
* ❌ **Not aligned (Archaic Legalese):**
  ```text
  The Licensee shall hereinafter hold harmless and indemnify the Licensor
  from and against any and all claims wherefore notice has not been provided
  within thirty (30) days.
  ```
* ✅ **ISO 24495-2 Aligned:**
  > **Indemnification Notice Requirement:**
  > 1. **Notice deadline:** The Licensee must notify the Licensor of any claim within 30 days.
  > 2. **Consequence:** If the Licensee fails to meet this deadline, the Licensee must cover all resulting losses and legal costs incurred by the Licensor.

---

## Pre-Output Self-Audit Checklist

Before outputting legal text, audit against these checks:
- [ ] **No legalese:** Are terms like *"shall"*, *"hereinafter"*, and *"hereby"* eliminated?
- [ ] **Modal verbs:** Are obligations expressed using only *must*, *must not*, or *may*?
- [ ] **Explicit subjects:** Is every obligation attached to a clearly named actor?
- [ ] **Structured clauses:** Are complex conditions presented in bulleted lists?
- [ ] **Legal accuracy:** Is legal enforceability preserved?
