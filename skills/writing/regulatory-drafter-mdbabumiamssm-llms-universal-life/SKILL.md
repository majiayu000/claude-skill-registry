---
name: regulatory-drafter
description: Drafts regulatory documents (FDA, EMA) with audit trails and specific "Thinking Block" reasoning. Use for high-stakes compliance writing.
---
# Regulatory Document Drafter

This skill generates compliant drafts for regulatory submissions, emphasizing auditability and adherence to guidelines (ICH, FDA).

## When to use this skill
- When asked to write sections of an IND, NDA, or CSR (Clinical Study Report).
- When responding to "Request for Information" (RFI) from health authorities.
- When the user requires "reasoning" or "thinking" to be visible (Anthropic style).

## How to use it
1.  **Analyze Context:**
    -   Identify the specific regulatory document type (e.g., "Module 2.5 Clinical Overview").
    -   Retrieve relevant guidelines (e.g., "FDA Draft Guidance on X").
2.  **Thinking Block (Internal Monologue):**
    -   Before writing, outline the strategy in a `<thinking>` block.
    -   Assess potential risks or claims that require citation.
3.  **Drafting:**
    -   Use formal, objective regulatory language (e.g., "The data suggest..." instead of "We proved...").
    -   Insert placeholders for data references `[Link to Table 14.2.1]`.
4.  **Audit Trail:**
    -   Append a "Compliance Check" section listing which guidelines were consulted.
