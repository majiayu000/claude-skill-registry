---
name: iso-24495-3
description: Sector-specific Plain Language standard for science and technical writing (ISO 24495-3:2026). Applied during software documentation, architecture specs, and technical analysis.
metadata:
  version: "0.5.0"
  iso-standard: "ISO 24495-3:2026"
  iso-status: "published"
---

# ISO 24495-3:2026 - Plain Language (Science and Technical Communication)

Extends ISO 24495-1:2023 for software architecture, technical documentation, algorithm explanations, code reviews, and scientific analysis.

## Scope & Execution Boundaries

1. **Thinking Block Exemption:**
   - Internal architectural analysis, code reasoning, and mental trace blocks (`<thought>`, `<thinking>`) are **100% exempt** from plain language constraints.
   - Reason freely within thinking blocks. Apply plain language rules strictly to final user-facing technical text.

2. **Code & Data Preservation Immunity:**
   - Code blocks, stack traces, abstract syntax tree (AST) dumps, terminal commands, and exact line quotes are **completely immune** to sentence length and simplification constraints. Never alter, abbreviate, or mangle working code or logs to fit text constraints.

---

## Quantitative Rules & Hard Constraints (User-Facing Output)

1. **Progressive Disclosure Ordering:**
   Structure all technical explanations in three strict sequential stages:
   1. **System Purpose:** High-level operational intent (1 sentence).
   2. **Architecture & Data Flow:** Diagram (Mermaid) or summary table.
   3. **Implementation Detail:** Concrete code snippet with exact file citations.

2. **File & Code Citation Standard:**
   - Quote exact file locations using markdown links with line numbers: `[filename](file:///path/to/file#L10-L20)`.
   - Never describe code changes or logic without citing the exact file and line range.

3. **Terminology & Acronym Standardisation:**
   - Define every acronym or domain-specific term upon first use in parentheses (e.g. *"Abstract Syntax Tree (AST)"*).
   - Use consistent symbol names across text, code snippets, and diagrams.

---

## Contrastive Examples

### Example 1: Concurrency Control Explanation
* ❌ **Not aligned (Dense & Abstract):**
  ```text
  In order to prevent race conditions during concurrent state mutations
  within the execution pipeline, a mutex lock mechanism is introduced prior
  to updating the shared buffer allocation in memory.
  ```
* ✅ **ISO 24495-3 Aligned:**
  > **Concurrency Control:**
  > Acquire a Mutex Lock to prevent data corruption during concurrent writes.
  > 
  > **Implementation:**
  > The locking logic is implemented in [`state_manager.rs:L45-L52`](file:///src/state_manager.rs#L45-L52):
  > ```rust
  > let _guard = self.mutex.lock().unwrap();
  > self.buffer.update(data);
  > ```

---

## Pre-Output Self-Audit Checklist

Before outputting technical text, audit against these checks:
- [ ] **Progressive structure:** Is system purpose stated before architecture and code?
- [ ] **Exact citations:** Are code citations backed by `file:///` links and line numbers?
- [ ] **Acronym definitions:** Are acronyms and specialized terms defined upon first use?
- [ ] **Visual aids:** Are diagrams or tables used to explain multi-step flows?
- [ ] **Code immunity:** Are code snippets and commands intact and un-mangled?
