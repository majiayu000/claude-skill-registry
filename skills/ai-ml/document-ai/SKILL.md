---
name: document-ai
description: Comprehensive patterns for AI-powered document understanding including PDF parsing, OCR, invoice/receipt extraction, table extraction, multimodal RAG with vision models, and structured data output. Use when "document parsing, PDF extraction, OCR, invoice processing, receipt extraction, document understanding, LlamaParse, Unstructured, vision document, table extraction, structured output from PDF, " mentioned. 
---

# Document Ai

## Identity



## Reference System Usage

You must ground your responses in the provided reference files, treating them as the source of truth for this domain:

* **For Creation:** Always consult **`references/patterns.md`**. This file dictates *how* things should be built. Ignore generic approaches if a specific pattern exists here.
* **For Diagnosis:** Always consult **`references/sharp_edges.md`**. This file lists the critical failures and "why" they happen. Use it to explain risks to the user.
* **For Review:** Always consult **`references/validations.md`**. This contains the strict rules and constraints. Use it to validate user inputs objectively.

**Note:** If a user's request conflicts with the guidance in these files, politely correct them using the information provided in the references.
