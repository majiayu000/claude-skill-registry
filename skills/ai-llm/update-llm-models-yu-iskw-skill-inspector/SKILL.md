---
name: update-llm-models
description: Autonomously research and update the default lightweight LLM models in `src/core/llm.ts` using web search to ensure the most current versions are used.
---

# Update LLM Models

## Purpose

This skill maintains the `src/core/llm.ts` file by ensuring that the default model identifiers for each provider are the latest available "lightweight" versions (e.g., Flash, Haiku, Mini).

## Workflow

### 1. Research Latest Models

Use `web_search` to identify the most recent lightweight model identifiers for the following providers:

- **OpenAI**: Look for "mini" or "nano" variants of the latest GPT model (e.g., GPT-5.2).
- **Anthropic**: Look for "haiku" variants (e.g., Claude 4.5 Haiku).
- **Google**: Look for "flash" variants (e.g., Gemini 3 Flash).
- **Mistral**: Look for "small" or "mini" variants (e.g., Mistral Small 3.1).
- **Groq**: Look for the most efficient models available on Groq (usually Llama 8B or 70B variants).

### 2. Identify Target Function

Locate the `getDefaultModel` function in `[src/core/llm.ts](src/core/llm.ts)`.

### 3. Apply Updates

Update the return values in the `switch` statement for each provider. Ensure the model identifiers match the exact strings found during research.

### 4. Verification

- Run `pnpm lint` to ensure no syntax errors or linting violations.
- Run `pnpm build` to confirm the project still compiles.

## Guidelines

- **Prefer Efficiency**: Always choose the "lighter" or "faster" version if multiple variants exist (e.g., prefer `gemini-2.5-flash` over `gemini-2.5-pro`).
- **Exact Identifiers**: Use the precise model identifier string required by the provider's API.
- **Provider Coverage**: Ensure all providers in the `LLMProvider` type are addressed if they have a known lightweight default.

## Examples

### Before

```typescript
case "google":
  return "gemini-2.5-flash";
```

### After (Hypothetical Jan 2026)

```typescript
case "google":
  return "gemini-3-flash";
```

## Resources

- **OpenAI**: [Models Overview](https://platform.openai.com/docs/models) <!-- trunk-ignore(markdown-link-check/403) -->
- **Anthropic**: [Claude Models](https://docs.anthropic.com/en/docs/about-claude/models/all-models)
- **Google Gemini**: [Gemini Models](https://ai.google.dev/gemini-api/docs/models)
- **Vertex AI**: [Model Garden](https://cloud.google.com/vertex-ai/generative-ai/docs/model-garden/available-models)
- **Mistral**: [Models Overview](https://docs.mistral.ai/getting-started/models)
- **Groq**: [Supported Models](https://console.groq.com/docs/models)
