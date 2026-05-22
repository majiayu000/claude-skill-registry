---
name: documentation-protocol
description: Defines the standard operating procedure for querying Context7 to verify documentation before writing code. Use whenever working with Appwrite, Next.js, or any third-party SDK.
---

# Context7 Documentation Protocol

## When to use this skill
- Before generating any backend or framework-specific code.
- When architectural decisions involve Next.js App Router or Appwrite SDK.
- To avoid using deprecated methods from internal training data.

## Workflow
- [ ] Identify the specific library and version (e.g., Appwrite v1.6, Next.js 15).
- [ ] Run `resolve-library-id` if the ID is not already known.
- [ ] Run `query-docs` with a specific question (e.g., "latest Appwrite server side auth").
- [ ] Validate the response against the current project context.
- [ ] Implement code based strictly on the verified documentation.

## Instructions
- **Query First**: Always call `context7` tools before writing code for Appwrite or Next.js.
- **Reference IDs**: 
    - Appwrite: `/appwrite/appwrite` or `/llmstxt/appwrite_io_llms_txt`
    - Next.js: `/vercel/next.js`
- **Verify Syntax**: Check for breaking changes (e.g., Appwrite Realtime channel formats).
