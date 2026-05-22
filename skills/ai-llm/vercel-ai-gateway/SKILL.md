---
name: vercel-ai-gateway
description: Vercel AI Gateway provider fallback and host order configuration. Use when working with aiGateway, hostOrder, getGatewayOptions, provider fallback, gateway configuration, or multi-host model routing.
---

# Vercel AI Gateway Patterns

Vercel AI Gateway routes requests to multiple inference hosts with automatic fallback. Enables specifying host order per model (e.g., try Cerebras first, fall back to Groq).

## Core Concepts

**Host order**: Array of inference provider names to try in sequence. Only set for specific models needing fallback.

**Gateway options**: Object passed to Vercel AI SDK with `gateway` key (SDK requirement).

**User tracking**: Propagate `userId` and `tags` for analytics/debugging.

## Key Files

- `apps/web/src/lib/ai/gateway.ts` - Main gateway logic
- `apps/web/src/lib/ai/providers/gateway.ts` - Gateway instantiation
- `apps/web/src/lib/ai/models.ts` - Model configs with hostOrder
- `packages/backend/convex/generation.ts` - Usage in generation

## Host Order Configuration

### Model Config Pattern

Set `hostOrder` in model config only when fallback needed:

```typescript
// From models.ts - Llama 4 Nemotron 70B (multi-host)
"openai:llama-4-nemotron-70b": {
  id: "openai:llama-4-nemotron-70b",
  provider: "openai",
  name: "Llama 4 Nemotron 70B",
  contextWindow: 131000,
  pricing: { input: 0.15, output: 0.6 },
  capabilities: ["function-calling", "thinking"],
  hostOrder: ["cerebras", "groq", "fireworks"], // Try in this order
  // ...
}

// From models.ts - Qwen 2.5 Coder (single host)
"openai:qwen-2.5-coder-32b": {
  id: "openai:qwen-2.5-coder-32b",
  provider: "openai",
  name: "Qwen 2.5 Coder 32B",
  contextWindow: 205000,
  pricing: { input: 0.3, output: 1.2, cached: 0.03 },
  capabilities: ["function-calling"],
  hostOrder: ["deepinfra"], // Single host - no fallback
  // ...
}

// Most models - no hostOrder (let Gateway decide)
"openai:gpt-5": {
  id: "openai:gpt-5",
  provider: "openai",
  name: "GPT-5",
  // ... no hostOrder property
}
```

### Retrieving Host Order

Use `getHostOrder()` to safely get model's host order:

```typescript
// From gateway.ts
export const getHostOrder = (modelId: string) => {
  const config = getModelConfig(modelId);

  // Use hostOrder from config if defined
  if (config?.hostOrder) {
    return config.hostOrder;
  }

  // For all other models, let Vercel AI Gateway decide
  return undefined;
};
```

Returns `undefined` when not set - Gateway uses default routing.

## Gateway Options Structure

### Building Options

Use `getGatewayOptions()` to build SDK-compliant options:

```typescript
// From gateway.ts
export const getGatewayOptions = (
  modelId?: string,
  userId?: string,
  tags?: string[],
) => {
  const order = getHostOrder(modelId || "");
  const options: any = {
    ...(userId && { user: userId }),
    tags: tags || ["chat"],
  };

  // Only add order if it's defined (for models with host fallback)
  if (order) {
    options.order = order;
  }

  // Note: "gateway" key is SDK-required for Vercel AI Gateway
  return { gateway: options };
};
```

**CRITICAL**: Return shape MUST be `{ gateway: {...} }` - SDK requirement.

### Conditional Order Injection

**Never set `order: undefined`** - only add property when defined:

```typescript
// ✅ CORRECT - only add order when defined
if (order) {
  options.order = order;
}

// ❌ WRONG - undefined breaks Gateway routing
options.order = order; // Don't do this when order is undefined
```

Leaving `order` undefined lets Gateway use smart defaults.

## Usage in Generation

### Basic Pattern

Pass gateway options to `streamText` via `providerOptions`:

```typescript
// From generation.ts (line 578-583)
const options: any = {
  model: finalModel,
  messages: allMessages,
  stopWhen: hasFunctionCalling ? stepCountIs(MAX_TOOL_STEPS) : undefined,
  providerOptions: getGatewayOptions(modelId, args.userId, ["chat"]),
};
```

### Merging with Reasoning Options

When model has reasoning config, merge options:

```typescript
// From generation.ts (line 620-626)
// Apply provider options (merge with gateway options)
if (reasoningResult?.providerOptions) {
  options.providerOptions = {
    ...options.providerOptions,
    ...reasoningResult.providerOptions,
  };
}
```

Reasoning options take precedence but gateway structure preserved.

### Tag Customization

Use tags to identify request context:

```typescript
// Chat generation
providerOptions: getGatewayOptions(modelId, userId, ["chat"])

// Continuation (tool results → text)
providerOptions: getGatewayOptions(modelId, userId, ["chat-continuation"])

// Summarization
providerOptions: getGatewayOptions(modelId, undefined, ["summary"])
```

## Helper: generateWithGateway

Convenience function for non-streaming calls:

```typescript
// From gateway.ts
export const generateWithGateway = async (params: {
  model: string;
  messages: any[];
  userId?: string;
  tags?: string[];
  temperature?: number;
  maxTokens?: number;
  tools?: any;
  providerOptions?: any;
}) => {
  const {
    model,
    messages,
    userId,
    tags,
    temperature,
    maxTokens,
    tools,
    providerOptions,
  } = params;

  const options: any = {
    model,
    messages,
    ...(temperature && { temperature }),
    ...(maxTokens && { maxTokens }),
    ...(tools && { tools }),
    providerOptions: {
      ...getGatewayOptions(model, userId, tags),
      ...providerOptions,
    },
  };

  return options;
};
```

Returns options object ready for `generateText()`.

## Model-Specific Patterns

### Ultra-Fast Models (Multi-Host)

Cerebras → Groq fallback for speed:

```typescript
"openai:llama-4-8b": {
  hostOrder: ["cerebras", "groq"],
  // Cerebras for speed, Groq if unavailable
}
```

### Agentic Models (Multi-Host)

DeepInfra → Fireworks for tool use:

```typescript
"openai:deepseek-r1": {
  hostOrder: ["deepinfra", "fireworks"],
  // DeepInfra primary, Fireworks backup
}
```

### Single-Host Models

Explicit single host when only one provider supports:

```typescript
"openai:qwen-2.5-coder-32b": {
  hostOrder: ["deepinfra"],
  // Only DeepInfra has this model
}
```

### Gateway-Managed Models

No `hostOrder` - let Gateway decide:

```typescript
"openai:gpt-5": {
  // No hostOrder property
  // Gateway uses default routing
}
```

## Anti-Patterns

**❌ Setting order: undefined explicitly**
```typescript
// DON'T
options.order = getHostOrder(modelId); // Could be undefined
```

**✅ Conditional property**
```typescript
// DO
const order = getHostOrder(modelId);
if (order) options.order = order;
```

**❌ Wrong return shape**
```typescript
// DON'T
return options; // Missing gateway wrapper
```

**✅ SDK-compliant shape**
```typescript
// DO
return { gateway: options };
```

**❌ Hardcoding order in calls**
```typescript
// DON'T
providerOptions: { gateway: { order: ["cerebras", "groq"] } }
```

**✅ Use config-driven approach**
```typescript
// DO
providerOptions: getGatewayOptions(modelId, userId, tags)
```

## Debugging Tips

Check Gateway routing in logs:

```typescript
logger.debug("Gateway options", {
  modelId,
  userId,
  order: getHostOrder(modelId),
  tags,
});
```

Common issues:

- **"Model not found"**: Host doesn't support model, check hostOrder
- **Slow fallback**: First host down, add more hosts to order
- **Missing analytics**: userId/tags not propagated
- **Gateway error**: Wrong return shape, check `{ gateway: {...} }` wrapper
