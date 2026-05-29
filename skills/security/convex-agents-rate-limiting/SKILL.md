---
name: "Convex Agents Rate Limiting"
description: "Controls message frequency and token usage to prevent abuse and manage API budgets. Use this to implement per-user limits, global caps, burst capacity, and token quota management."
---

## Purpose

Rate limiting protects against abuse, manages LLM costs, and ensures fair resource allocation. Covers message frequency limits and token usage quotas.

## When to Use This Skill

- Preventing rapid-fire message spam
- Limiting total tokens per user
- Implementing burst capacity
- Global API limits to stay under provider quotas
- Fair resource allocation in multi-user systems
- Billing based on token usage

## Configure Rate Limiter

```typescript
import { RateLimiter, MINUTE, SECOND } from "@convex-dev/rate-limiter";

export const rateLimiter = new RateLimiter(components.rateLimiter, {
  sendMessage: {
    kind: "fixed window",
    period: 5 * SECOND,
    rate: 1,
    capacity: 2,
  },
  globalSendMessage: {
    kind: "token bucket",
    period: MINUTE,
    rate: 1_000,
  },
  tokenUsagePerUser: {
    kind: "token bucket",
    period: MINUTE,
    rate: 2000,
    capacity: 10000,
  },
  globalTokenUsage: {
    kind: "token bucket",
    period: MINUTE,
    rate: 100_000,
  },
});
```

## Check Message Rate Limit

```typescript
export const sendMessage = mutation({
  args: { threadId: v.string(), message: v.string(), userId: v.string() },
  handler: async (ctx, { threadId, message, userId }) => {
    try {
      await rateLimiter.limit(ctx, "sendMessage", {
        key: userId,
        throws: true,
      });

      await rateLimiter.limit(ctx, "globalSendMessage", { throws: true });

      const { messageId } = await saveMessage(ctx, components.agent, {
        threadId,
        prompt: message,
      });

      return { success: true, messageId };
    } catch (error) {
      if (isRateLimitError(error)) {
        return {
          success: false,
          error: "Rate limit exceeded",
          retryAfter: error.data.retryAfter,
        };
      }
      throw error;
    }
  },
});
```

## Check Token Usage

```typescript
export const checkTokenUsage = action({
  args: { threadId: v.string(), question: v.string(), userId: v.string() },
  handler: async (ctx, { threadId, question, userId }) => {
    const estimatedTokens = await estimateTokens(ctx, threadId, question);

    try {
      await rateLimiter.check(ctx, "tokenUsagePerUser", {
        key: userId,
        count: estimatedTokens,
        throws: true,
      });

      // Proceed with generation
      const { thread } = await myAgent.continueThread(ctx, { threadId });
      const result = await thread.generateText({ prompt: question });

      return { success: true, response: result.text };
    } catch (error) {
      if (isRateLimitError(error)) {
        return {
          success: false,
          error: "Token limit exceeded",
          retryAfter: error.data.retryAfter,
        };
      }
      throw error;
    }
  },
});

async function estimateTokens(
  ctx: QueryCtx,
  threadId: string,
  question: string
): Promise<number> {
  const questionTokens = Math.ceil(question.length / 4);
  const responseTokens = Math.ceil(questionTokens * 3);
  return questionTokens + responseTokens;
}
```

## Track Actual Usage

```typescript
const myAgent = new Agent(components.agent, {
  name: "My Agent",
  languageModel: openai.chat("gpt-4o-mini"),
  usageHandler: async (ctx, { usage, userId }) => {
    if (!userId) return;

    await rateLimiter.limit(ctx, "tokenUsagePerUser", {
      key: userId,
      count: usage.totalTokens,
      reserve: true,
    });
  },
});
```

## Client-Side Rate Limit Checking

```typescript
import { useRateLimit } from "@convex-dev/rate-limiter/react";
import { isRateLimitError } from "@convex-dev/rate-limiter";

function ChatInput() {
  const { status } = useRateLimit(api.rateLimiting.getRateLimit);

  if (status && !status.ok) {
    return (
      <div className="text-red-500">
        Rate limit exceeded. Retry after{" "}
        {new Date(status.retryAt).toLocaleTimeString()}
      </div>
    );
  }

  return <input type="text" placeholder="Send a message..." />;
}
```

## Key Principles

- **Fixed window for frequency**: Use for simple X per period
- **Token bucket for capacity**: Use for burst-friendly limits
- **Estimate before, track after**: Prevent early, record actual usage
- **Global + per-user limits**: Balance fair access with resource caps
- **Retryable errors**: Clients can retry with backoff

## Next Steps

- See **usage-tracking** for billing based on token usage
- See **fundamentals** for agent setup
- See **debugging** for troubleshooting
