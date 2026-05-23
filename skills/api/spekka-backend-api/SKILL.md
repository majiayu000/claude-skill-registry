---
name: Backend API
description: Express-based REST API design patterns for the video rendering service. Use this when creating or modifying API endpoints in server/index.ts, handling HTTP requests/responses, implementing error handling, or setting up SSE streams for progress updates.
---

# Backend API

This Skill provides Claude Code with specific guidance on how it should handle backend API.

## When to use this skill:

- Creating new API endpoints in server/index.ts
- Modifying request handlers or route definitions
- Implementing request validation and error responses
- Setting up Server-Sent Events (SSE) for progress streaming
- Handling async operations in Express routes
- Defining JSON response formats

## Instructions

- **Express Routes**: Define routes in `server/index.ts` with clear handler separation
- **HTTP Status Codes**: Return appropriate codes: 200 (success), 201 (created), 400 (bad request), 404 (not found), 500 (server error)
- **Error Responses**: Return consistent JSON error format: `{ error: string, details?: any }`
- **Request Validation**: Validate request bodies early with TypeScript types from `src/lib/types.ts`
- **Server-to-Server Design**: This is a backend microservice API for Cawpile.org, not user-facing
- **Health Checks**: Maintain `/health` endpoint for monitoring and orchestration
- **Progress Streaming**: Use SSE (Server-Sent Events) for long-running operations like video renders
- **Async Handlers**: Use async/await pattern; wrap handlers with error catching middleware

**Examples:**
```typescript
// Good: Clear validation, proper types, error handling
app.post('/render', async (req, res) => {
  try {
    const request: RenderRequest = req.body;
    if (!request.month || !request.year) {
      return res.status(400).json({ error: 'Missing month or year' });
    }
    const result = await renderVideo(request);
    res.json({ url: result.s3Url, duration: result.duration });
  } catch (error) {
    res.status(500).json({ error: 'Render failed', details: error.message });
  }
});

// Bad: No validation, unclear error handling
app.post('/render', (req, res) => {
  renderVideo(req.body).then(r => res.json(r));
});
```
