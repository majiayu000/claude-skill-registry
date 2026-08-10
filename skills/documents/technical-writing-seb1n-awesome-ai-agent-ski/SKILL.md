---
name: technical-writing
description: Write clear, concise, and accurate technical documentation including API references, user guides, tutorials, changelogs, and architecture docs, tailored to the target audience. Use when the user requests technical writing or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# Technical Writing

This skill enables an AI agent to produce high-quality technical documentation across a range of formats — API references, user guides, getting-started tutorials, changelogs, architecture decision records, and more. The agent analyzes the target audience, structures information logically, applies consistent formatting standards, and ensures every document is accurate, scannable, and actionable.

## Workflow

1. **Identify Document Type and Audience**
   Determine which type of document is needed (API reference, tutorial, user guide, changelog, architecture doc) and who will read it (beginner developers, experienced engineers, end users, stakeholders). Adjust vocabulary, depth, and assumed prerequisites accordingly. A tutorial for beginners should explain every step; an API reference for senior engineers should be terse and precise.

2. **Gather Source Material**
   Collect all relevant inputs: source code, existing documentation, design documents, user stories, API schemas (OpenAPI/Swagger), commit histories, or stakeholder interviews. Identify the authoritative source for each piece of information to ensure accuracy. Note any gaps that need clarification.

3. **Design the Document Structure**
   Create an outline following the conventions of the document type. API references use a consistent per-endpoint template. Tutorials follow a step-by-step progression. Architecture docs follow a decision-record format (context, decision, consequences). Plan where code examples, tables, and callout boxes will appear.

4. **Write the Content**
   Draft the document using clear, direct language. Prefer active voice and short sentences. Lead each section with the most important information. Include complete, runnable code examples that readers can copy and execute. Use consistent terminology and define acronyms on first use. Format according to the chosen standard (Markdown, reStructuredText, AsciiDoc).

5. **Add Navigation and Cross-References**
   Insert a table of contents for long documents, anchor links between related sections, and links to prerequisite or follow-up documentation. Add "Next steps" sections at the end of tutorials.

6. **Review for Accuracy and Completeness**
   Verify all code examples compile or run correctly. Confirm API endpoint paths, parameters, and response schemas match the actual implementation. Check that every tutorial step produces the described result. No placeholder text or TODO items should remain.

## Usage

Provide the agent with:

- **Document type** — API reference, tutorial, user guide, changelog, architecture decision record, README
- **Subject** — the feature, API, tool, or system to document
- **Audience** — skill level and role of the intended readers
- **Source material** — code files, schemas, design docs, or a description of the feature
- **Format** — Markdown, reStructuredText, AsciiDoc, or HTML

Example prompt: "Write an API reference for the /users endpoint. The audience is third-party developers. Here is the OpenAPI spec: [attached file]."

## Examples

### Example 1: API Endpoint Reference

**Input:** "Document the POST /api/v1/webhooks endpoint. Creates a webhook subscription. Requires Bearer token auth. Body: `url` (string, required), `events` (string[], required), `secret` (string, optional). Returns 201 or 422."

**Output:**

> ## POST /api/v1/webhooks
>
> Creates a new webhook subscription. Requires a Bearer token in the `Authorization` header.
>
> | Field | Type | Required | Description |
> |-------|------|----------|-------------|
> | `url` | string | Yes | HTTPS endpoint URL to receive payloads. |
> | `events` | string[] | Yes | Event types to subscribe to (e.g., `["order.created"]`). |
> | `secret` | string | No | HMAC-SHA256 signing secret. Auto-generated if omitted. |
>
> ```bash
> curl -X POST https://api.example.com/api/v1/webhooks \
>   -H "Authorization: Bearer sk_live_abc123" \
>   -H "Content-Type: application/json" \
>   -d '{"url":"https://myapp.com/hooks","events":["order.created"]}'
> ```
>
> **201 Created:** `{"id":"wh_9a8b7c6d","url":"https://myapp.com/hooks","events":["order.created"],"active":true}`
>
> **422 Error:** `{"error":{"code":"validation_error","details":[{"field":"url","message":"URL must use HTTPS."}]}}`

### Example 2: Getting-Started Tutorial

**Input:** "Write a getting-started tutorial for our Python SDK (`acme-sdk`). Install, authenticate, and list projects."

**Output:**

> # Getting Started with the Acme Python SDK
>
> ## Prerequisites
> - Python 3.9+ and an Acme API key (found at **Settings > API Keys**)
>
> ## Step 1: Install the SDK
> ```bash
> pip install acme-sdk
> ```
>
> ## Step 2: Set Your API Key
> ```bash
> export ACME_API_KEY="sk_live_your_key_here"
> ```
>
> ## Step 3: List Your Projects
> ```python
> import os
> from acme_sdk import AcmeClient
>
> client = AcmeClient(api_key=os.environ["ACME_API_KEY"])
> for project in client.projects.list():
>     print(f"{project.id}: {project.name}")
> ```
>
> Expected output:
> ```
> proj_abc123: My First Project
> proj_def456: Marketing Site
> ```
>
> ## Next Steps
> - [Create a project](/docs/projects/create) programmatically
> - [Set up webhooks](/docs/webhooks) for real-time events

## Best Practices

- **Lead with the action.** Start each section with what the reader needs to do, not background context. Put explanations after the instruction.
- **Provide complete, runnable code.** Every code example should work as-is when copied. Include imports, variable declarations, and expected output.
- **Use consistent templates.** API references should follow the same structure for every endpoint. Tutorials should follow the same step format throughout.
- **Write scannable content.** Use headings, tables, bullet points, and code blocks so readers can find information quickly without reading every paragraph.
- **Version your documentation.** Tie docs to specific software versions. Clearly indicate which version introduced a feature or deprecated an API.
- **Test your instructions.** Walk through every step in a tutorial to confirm it produces the described result.

## Edge Cases

- **Undocumented behavior:** If source code reveals behavior not described in any spec, document it as "current behavior" and flag it for the engineering team to confirm as intentional.
- **Multiple audiences for one document:** Use a layered approach — put essentials first with expandable "Advanced" sections or links to deeper docs.
- **Rapidly changing APIs:** Note the version or date prominently and include a disclaimer that the interface may change.
- **Missing source material:** Explicitly list what information is missing and request it rather than guessing.
- **Non-English documentation:** Follow the technical writing conventions of that language's developer community rather than translating English conventions literally.
