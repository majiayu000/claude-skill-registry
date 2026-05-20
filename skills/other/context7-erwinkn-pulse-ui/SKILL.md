---
name: context7
description: Fetch up-to-date library documentation using Context7 API. Use this skill when the user asks for docs, examples, or help with a specific library/framework (e.g., "look up React docs", "context7 nextjs routing", "fetch docs for fastapi").
allowed-tools: WebFetch
---

# Context7 Documentation Fetcher

This skill fetches up-to-date documentation and code examples from libraries using the Context7 API.

## Standard Workflow

Context7 requires a **two-step process**:

### Step 1: Search for the Library ID

First, search for the library to get its ID:

```
GET https://context7.com/api/v2/libs/search?libraryName=<library>&query=<context>
```

Parameters:
- `libraryName`: The library name (e.g., "react", "nextjs", "fastapi")
- `query`: Search context to help find the right library

The response contains a `results` array with library objects. Use the `id` field from the first result.

### Step 2: Get Documentation Context

Use the library ID to fetch relevant documentation:

```
GET https://context7.com/api/v2/context?libraryId=<id>&query=<question>
```

Parameters:
- `libraryId`: The ID from step 1 (e.g., "/vercel/next.js")
- `query`: Natural language question about the documentation

This returns ranked code snippets and documentation matching your query.

## Example Usage

When the user asks about a library:

1. **Search for the library**:
   Use WebFetch to call:
   ```
   https://context7.com/api/v2/libs/search?libraryName=nextjs&query=routing
   ```
   Extract the library ID from the response (e.g., "/vercel/next.js")

2. **Fetch documentation**:
   Use WebFetch to call:
   ```
   https://context7.com/api/v2/context?libraryId=/vercel/next.js&query=How to setup dynamic routes
   ```

3. **Present the results** to the user with the relevant code examples and documentation.

## Tips for Best Results

- Use specific, detailed queries rather than vague terms
- Include relevant context in the query (e.g., "useState hook with TypeScript" instead of just "state")
- The API works without an API key but has restricted rate limits

## Handling Responses

| Status | Meaning | Action |
|--------|---------|--------|
| 200 | Success | Process and present results |
| 202 | Processing | Library still indexing; inform user to try later |
| 301 | Redirect | Use the `redirectUrl` from response |
| 429 | Rate Limited | Inform user about rate limit; suggest waiting |
| 404 | Not Found | Library doesn't exist; suggest alternative search |
