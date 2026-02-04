---
name: ai-agent-implementation
description: Step-by-step checklist and best practices for implementing new AI agent tools in the omer-akben portfolio. Use when creating new agent tools, API routes, or extending agent capabilities.
---

# AI Agent Implementation Skill

## Implementation Checklist

Use this checklist for every new AI agent tool:

### Planning Phase

- [ ] Define clear tool purpose and triggers
- [ ] Design Zod schemas for input/output validation
- [ ] Consider rate-limiting requirements
- [ ] Plan security measures (validation, sanitization, PII)
- [ ] Document environment variables needed

### Implementation Phase

- [ ] Create API route handler (`src/app/api/tools/[name]/route.ts`)
- [ ] Implement tool schema in `lib/agent-tools/schemas.ts`
- [ ] Add Mastra tool in `lib/mastra/tools.ts` (if needed)
- [ ] Update AI knowledge base (`lib/agent-knowledge-base.ts`)
- [ ] Configure rate-limiting in `lib/rate-limit.ts`

### Testing Phase

- [ ] Write unit tests for API route
- [ ] Test Zod schema validation (valid + invalid inputs)
- [ ] Manual testing via Playwright for AI behavior
- [ ] Verify rate-limiting works correctly
- [ ] Test all 6 quality gates pass

### Documentation Phase

- [ ] Update AGENTS.md with tool details
- [ ] Update CLAUDE.md with implementation notes
- [ ] Document environment variables in `.env.example`
- [ ] Add lessons learned section
- [ ] Update README.md if needed

### Deployment Phase

- [ ] Configure environment variables in Vercel
- [ ] Configure secrets in GitHub Actions
- [ ] Create PR with comprehensive description
- [ ] Verify CI/CD passes all gates
- [ ] Monitor production deployment

## Tool Implementation Pattern

### 1. Create API Route Handler

**Location:** `src/app/api/tools/[tool-name]/route.ts`

```typescript
import { NextRequest } from "next/server";
import { z } from "zod";
import { ratelimit } from "@/lib/rate-limit";

// Define input schema
const inputSchema = z.object({
  param1: z.string().min(1).max(100),
  param2: z.number().optional(),
});

export async function POST(request: NextRequest) {
  try {
    // Rate limiting (if needed)
    const ip = request.headers.get("x-forwarded-for") ?? "anonymous";
    const result = await ratelimit.limit(ip);
    if (!result.success) {
      return Response.json(
        { error: "Rate limit exceeded" },
        { status: 429 }
      );
    }

    // Parse and validate input
    const body = await request.json();
    const input = inputSchema.parse(body);

    // Implement tool logic
    const result = await performToolAction(input);

    // Return response
    return Response.json(result);
  } catch (error) {
    console.error("Tool error:", error);

    if (error instanceof z.ZodError) {
      return Response.json(
        { error: "Invalid input", details: error.errors },
        { status: 400 }
      );
    }

    return Response.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}
```typescript

### 2. Define Tool Schema

**Location:** `src/lib/agent-tools/schemas.ts`

```typescript
import { z } from "zod";

export const toolNameSchema = z.object({
  param1: z.string()
    .min(1, "Parameter cannot be empty")
    .max(100, "Parameter too long"),
  param2: z.number().optional(),
});

export type ToolNameInput = z.infer<typeof toolNameSchema>;

export const toolNameResponseSchema = z.object({
  success: z.boolean(),
  data: z.unknown(),
  message: z.string().optional(),
});
```typescript

### 3. Add to Mastra Tools (if needed)

**Location:** `src/lib/mastra/tools.ts`

```typescript
import { createTool } from "@mastra/core";
import { z } from "zod";

export const toolName = createTool({
  id: "tool_name",
  description: "Clear description of what this tool does and when to use it",
  inputSchema: z.object({
    param1: z.string().describe("Description of param1"),
    param2: z.number().optional().describe("Optional param2"),
  }),
  outputSchema: z.object({
    success: z.boolean(),
    data: z.unknown(),
  }),
  execute: async ({ context, input }) => {
    // Call API route
    const response = await fetch("/api/tools/tool-name", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(input),
    });

    if (!response.ok) {
      throw new Error(`Tool failed: ${response.statusText}`);
    }

    return await response.json();
  },
});
```typescript

### 4. Update Knowledge Base

**Location:** `src/lib/agent-knowledge-base.ts`

```typescript
export const AGENT_KNOWLEDGE_BASE = `
...existing knowledge...

## Tool Name

**Purpose:** Clear description of what the tool does

### When to use
- Trigger condition 1
- Trigger condition 2
- Trigger condition 3

### Parameters
- param1 (required): Description
- param2 (optional): Description

### Example usage
"Can you [action]?" → Use tool_name

**Rate limits:** X requests per Y timeframe (if applicable)
`;
```typescript

### 5. Configure Rate Limiting (if needed)

**Location:** `src/lib/rate-limit.ts`

```typescript
export const rateLimits = {
  // Existing limits...

  toolName: {
    limit: 10,          // 10 requests
    window: 3600,       // per hour
  },
};

// Create rate limiter
export const toolNameRateLimit = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(
    rateLimits.toolName.limit,
    `${rateLimits.toolName.window}s`
  ),
  prefix: "ratelimit:tool_name",
});
```typescript

## Testing Pattern

### Unit Tests

**Location:** `src/app/api/tools/[tool-name]/__tests__/route.test.ts`

```typescript
import { describe, it, expect, beforeEach, vi } from "vitest";
import { POST } from "../route";

describe("Tool API Route", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe("Input Validation", () => {
    it("should reject invalid input", async () => {
      const request = new Request("http://localhost", {
        method: "POST",
        body: JSON.stringify({ invalid: "data" }),
      });

      const response = await POST(request);
      expect(response.status).toBe(400);
    });

    it("should accept valid input", async () => {
      const request = new Request("http://localhost", {
        method: "POST",
        body: JSON.stringify({
          param1: "valid",
          param2: 42,
        }),
      });

      const response = await POST(request);
      expect(response.status).toBe(200);
    });
  });

  describe("Rate Limiting", () => {
    it("should enforce rate limits", async () => {
      // Test rate limit logic
    });
  });

  describe("Tool Logic", () => {
    it("should perform expected action", async () => {
      // Test tool functionality
    });
  });
});
```typescript

### E2E Tests

**Location:** `e2e/tools/tool-name.spec.ts`

```typescript
import { test, expect } from "@playwright/test";

test.describe("Tool Name Integration", () => {
  test("should trigger tool from chat", async ({ page }) => {
    await page.goto("/");

    // Open chat
    await page.getByRole("button", { name: "Chat" }).click();

    // Send message that triggers tool
    await page.getByRole("textbox").fill("Trigger phrase");
    await page.getByRole("button", { name: "Send" }).click();

    // Wait for tool response
    await page.waitForSelector('[data-tool="tool_name"]');

    // Assert result
    await expect(page.getByText("Expected result")).toBeVisible();
  });
});
```typescript

## Security Best Practices

### Input Validation

1. **Always use Zod schemas** - Never trust user input
2. **Sanitize strings** - Remove/escape dangerous characters
3. **Validate lengths** - Prevent DoS via large inputs
4. **Check types** - Ensure correct data types

### API Key Protection

1. **Server-side only** - Never expose keys in client
2. **Environment variables** - Use `.env` files
3. **Validate in middleware** - Check keys before processing
4. **Rotate regularly** - Update keys periodically

### Rate Limiting

1. **Apply to all tools** - Prevent abuse
2. **Use IP-based limits** - Track by requester
3. **Sliding window** - More accurate than fixed window
4. **Graceful degradation** - Inform user of limits

### PII Handling

1. **Minimize collection** - Only collect necessary data
2. **Validate before storing** - Ensure data integrity
3. **Encrypt in transit** - Use HTTPS
4. **Log carefully** - Never log sensitive data

## Common Patterns

### Email Sending Tool

```typescript
import { Resend } from "resend";

const resend = new Resend(process.env.RESEND_API_KEY);

await resend.emails.send({
  from: process.env.RESEND_FROM_EMAIL!,
  to: validatedEmail,
  subject: "Subject",
  html: templateContent,
});
```typescript

### Database Query Tool

```typescript
import { vectorClient } from "@/lib/vector-client";

const results = await vectorClient.query({
  vector: embedding,
  topK: 5,
  includeMetadata: true,
});
```typescript

### External API Tool

```typescript
const response = await fetch("https://api.example.com/endpoint", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${process.env.API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify(data),
});

if (!response.ok) {
  throw new Error(`API failed: ${response.statusText}`);
}

const result = await response.json();
```typescript

## Error Handling

### Graceful Degradation

```typescript
try {
  const result = await performAction();
  return Response.json(result);
} catch (error) {
  console.error("Tool error:", error);

  // Return helpful error message
  return Response.json({
    error: "Operation failed",
    message: "Please try again or contact support",
  }, { status: 500 });
}
```typescript

### Error Categories

1. **Validation errors (400)** - Invalid input
2. **Authentication errors (401)** - Missing/invalid API key
3. **Authorization errors (403)** - Insufficient permissions
4. **Rate limit errors (429)** - Too many requests
5. **Server errors (500)** - Internal failures

## Documentation Requirements

### In-Code Documentation

```typescript
/**
 * Tool Name API Route
 *
 * Purpose: What the tool does
 *
 * @param param1 - Description of param1
 * @param param2 - Description of param2
 * @returns Success/error response
 *
 * @example
 * POST /api/tools/tool-name
 * {
 *   "param1": "value",
 *   "param2": 42
 * }
 */
```typescript

### AGENTS.md Documentation

```markdown
## Tool Name

**Purpose:** Clear description

### Triggers
- User asks to [action]
- User mentions [keyword]

### Implementation
- API Route: `/api/tools/tool-name`
- Schema: `toolNameSchema` in `lib/agent-tools/schemas.ts`
- Rate Limit: X requests per Y timeframe

### Example conversation
User: "Can you [action]?"
Ozzy: [Uses tool_name to perform action] "Done! [Result description]"
```typescript

## Deployment Considerations

### Environment Variables

1. Add to `.env.example` with description
2. Configure in Vercel project settings
3. Update deployment checklist in CLAUDE.md

### Monitoring

1. Add PostHog tracking events
2. Configure Sentry error tracking
3. Monitor rate limit hit rates
4. Track tool usage metrics

### Performance

1. Use caching where appropriate
2. Implement timeouts for external APIs
3. Consider async processing for slow operations
4. Monitor API response times

## Common Pitfalls

### ❌ Don't Do This

```typescript
// Exposing API keys
const apiKey = process.env.API_KEY; // Client-side!

// No validation
const data = await request.json(); // Unsafe!

// Hardcoded values
const limit = 100; // Use config file

// No error handling
const result = await action(); // What if it fails?
```typescript

### ✅ Do This Instead

```typescript
// Server-side only
export async function POST(request: NextRequest) {
  const apiKey = process.env.API_KEY; // Secure

  // Validate input
  const data = inputSchema.parse(await request.json());

  // Use config
  const limit = rateLimits.toolName.limit;

  // Handle errors
  try {
    const result = await action();
    return Response.json(result);
  } catch (error) {
    return handleError(error);
  }
}
```typescript

## Success Metrics

### After implementing a new tool

- [ ] Tool successfully triggered by AI agent
- [ ] All edge cases handled gracefully
- [ ] Rate limiting prevents abuse
- [ ] Tests cover success and failure scenarios
- [ ] Documentation complete and accurate
- [ ] No security vulnerabilities
- [ ] Performance meets requirements
- [ ] Monitoring and logging in place
