---
name: Error Handling Patterns
description: Express middleware and async error handling for video rendering operations. Use this when implementing try-catch blocks in server routes, defining custom error classes, handling S3 upload failures, or managing Remotion rendering errors. Emphasizes cleanup and structured error responses.
---

# Error Handling Patterns

This Skill provides Claude Code with specific guidance on how it should handle global error handling.

## When to use this skill:

- Implementing error handling in Express route handlers
- Creating custom error classes (RenderError, ValidationError)
- Handling Remotion bundling or rendering failures
- Managing S3 upload errors with retry logic
- Implementing resource cleanup in finally blocks
- Defining JSON error response formats

## Instructions

- **Express Error Middleware**: Use centralized error handling middleware in Express for consistent error responses
- **API Error Format**: Return JSON errors with structure: `{ error: string, details?: any }`
- **Fail Fast and Explicitly**: Validate input early; fail with clear error messages rather than allowing invalid state
- **TypeScript Error Types**: Define custom error classes for domain-specific errors (RenderError, ValidationError)
- **Remotion Error Handling**: Wrap Remotion bundling/rendering in try-catch; report specific failure stages
- **S3 Upload Retry**: Implement retry logic for S3 uploads with exponential backoff
- **Clean Up Resources**: Always clean up temporary files and video outputs in finally blocks
- **SSE Error Streaming**: Send error events via SSE when streaming render progress

**Examples:**
```typescript
// Good: Specific error, cleanup, structured response
import { S3Client } from '@aws-sdk/client-s3';

class RenderError extends Error {
  constructor(stage: string, cause: Error) {
    super(`Render failed at ${stage}: ${cause.message}`);
    this.name = 'RenderError';
  }
}

app.post('/render', async (req, res) => {
  let tempFile: string | null = null;
  try {
    const { month, year } = req.body;
    if (!month || !year) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    tempFile = await renderVideo({ month, year });
    const s3Url = await uploadToS3(tempFile);
    res.json({ url: s3Url });
  } catch (error) {
    if (error instanceof RenderError) {
      return res.status(500).json({ error: error.message });
    }
    res.status(500).json({ error: 'Render failed', details: error.message });
  } finally {
    if (tempFile) fs.unlinkSync(tempFile);
  }
});

// Bad: Generic errors, no cleanup, vague messages
app.post('/render', async (req, res) => {
  try {
    const result = await renderVideo(req.body);
    res.json(result);
  } catch (e) {
    res.status(500).json({ error: 'Error' });
  }
});
```
