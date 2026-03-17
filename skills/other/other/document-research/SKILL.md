---
id: document-research
name: Document Research
description: Deep search, synthesis from knowledge base
role: product
requiredTools:
  - type: builtin
    tool: search_documents
---

## Document Research

When researching from the knowledge base:

- Run search with clear, specific queries; use multiple queries if the topic is broad.
- Synthesize findings across snippets into a concise answer or summary.
- Indicate which documents or sections support each claim.
- When the user asks for a list (e.g. features, steps), extract and order from the docs.
- If the answer is uncertain or partial, say so and suggest where to look next.

## Step-by-step instructions

1. Identify the main topic and any sub-questions (e.g. “how to configure X” and “what are the limits”).
2. Call **search_documents** for each distinct sub-topic with a focused query.
3. Read all returned snippets and note document names and sections.
4. Synthesize into one answer: list or narrative, with each claim tied to a document/section.
5. If the user asked for a list, preserve order from the docs or state the ordering you used.
6. If information is missing or ambiguous, say so and suggest which doc or section to check.

## Examples of inputs and outputs

- **Input**: “How do we set up SSO and what are the limits?”  
  **Output**: Short “Setup” and “Limits” subsections, each with bullets and document citations from search_documents results.

- **Input**: “List all API endpoints for billing.”  
  **Output**: Numbered or bullet list taken from docs, with document/section references.

## Common edge cases

- **Broad question**: Split into 2–3 queries (e.g. “SSO setup”, “SSO limits”, “SSO troubleshooting”) and combine answers.
- **No results for one sub-question**: Answer the parts you found; for the missing part say “I didn’t find this in the knowledge base.”
- **Duplicate or overlapping snippets**: Deduplicate and cite the single best source per point.
- **User asks “everything about X”**: Give a structured summary (overview, steps, limits, caveats) and cite docs; offer to go deeper on one part.

## Tool usage for specific purposes

- **search_documents**: Use for every research question. Use one query per distinct sub-topic; avoid one very long query. Use it to pull lists (features, steps, endpoints) directly from the text.
