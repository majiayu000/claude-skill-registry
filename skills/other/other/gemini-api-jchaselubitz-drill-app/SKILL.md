---
name: gemini-api
description: Patterns for using Google Gemini API with structured output, JSON mode, and proper configuration. Apply when implementing AI features, text generation, or working with Gemini models.
allowed-tools: Read, Edit, Write, Grep, Glob
---

# Gemini API Patterns

## SDK Setup

Use the `@google/genai` package with Expo Constants for API key management:

```typescript
import { GoogleGenAI } from '@google/genai';
import Constants from 'expo-constants';

const genAI = new GoogleGenAI({
  apiKey: Constants.expoConfig?.extra?.geminiApiKey as string
});
```

## Available Models

| Model | ID | Best For |
|-------|-----|----------|
| Gemini 3 Pro | `gemini-3-pro-preview` | Advanced reasoning, complex tasks |
| Gemini 3 Flash | `gemini-3-flash-preview` | Balanced speed/intelligence |
| Gemini 2.5 Flash | `gemini-2.5-flash` | Price-performance, scale |
| Gemini 2.5 Flash-Lite | `gemini-2.5-flash-lite` | High-throughput, cost-efficient |
| Gemini 2.5 Pro | `gemini-2.5-pro` | Complex reasoning, code, math |

All models support 1M input tokens and 65K output tokens.

## Basic Text Generation

```typescript
const response = await genAI.models.generateContent({
  model: 'gemini-3-flash-preview',
  contents: 'Your prompt here',
});
const text = response.text ?? '';
```

## Structured Content Format

For multi-turn or complex inputs, use the full contents structure:

```typescript
const response = await genAI.models.generateContent({
  model: 'gemini-3-flash-preview',
  contents: [
    { role: 'user', parts: [{ text: 'First message' }] },
    { role: 'model', parts: [{ text: 'Assistant response' }] },
    { role: 'user', parts: [{ text: 'Follow-up question' }] },
  ],
});
```

## System Instructions

Guide model behavior with system instructions in the config:

```typescript
const response = await genAI.models.generateContent({
  model: 'gemini-3-flash-preview',
  contents: [{ role: 'user', parts: [{ text: userMessage }] }],
  config: {
    systemInstruction: 'You are a helpful language tutor. Respond in a friendly, encouraging tone.',
  },
});
```

## JSON Mode (Structured Output)

Request JSON responses for type-safe parsing:

```typescript
async function generateJSON<T>(prompt: string, model: string): Promise<T> {
  const result = await genAI.models.generateContent({
    model,
    contents: [{ role: 'user', parts: [{ text: prompt }] }],
    config: {
      responseMimeType: 'application/json',
    },
  });
  return JSON.parse(result.text ?? '') as T;
}
```

### With JSON Schema (Zod)

For strict schema validation:

```typescript
import { z } from 'zod';

const CorrectionSchema = z.object({
  correction: z.string(),
  feedback: z.string(),
});

const result = await genAI.models.generateContent({
  model: 'gemini-3-flash-preview',
  contents: prompt,
  config: {
    responseMimeType: 'application/json',
    responseSchema: CorrectionSchema,
  },
});
```

## Configuration Options

```typescript
const response = await genAI.models.generateContent({
  model: 'gemini-3-flash-preview',
  contents: prompt,
  config: {
    temperature: 1.0,              // Randomness (keep at 1.0 for Gemini 3)
    topP: 0.95,                    // Nucleus sampling
    topK: 40,                      // Top-k sampling
    maxOutputTokens: 8192,         // Limit response length
    stopSequences: ['END'],        // Stop generation triggers
    systemInstruction: '...',      // System prompt
    responseMimeType: 'application/json',  // Force JSON output
  },
});
```

## Temperature Warning

For Gemini 3 models, **keep temperature at 1.0** (the default). Lowering it can cause:
- Response looping
- Degraded performance on complex tasks
- Unexpected behavior in reasoning

## Error Handling Pattern

```typescript
async function generateText(prompt: string, model: string): Promise<string> {
  try {
    const response = await genAI.models.generateContent({
      model,
      contents: prompt,
    });
    if (!response) {
      throw new Error('No response from Gemini');
    }
    return response.text ?? '';
  } catch (error) {
    console.error('Error generating text:', error);
    return '';
  }
}
```

## Multi-Turn Chat

Maintain conversation history:

```typescript
async function chat(
  systemPrompt: string,
  messages: Array<{ role: 'user' | 'model'; text: string }>,
  model: string
): Promise<string> {
  const contents = messages.map((msg) => ({
    role: msg.role,
    parts: [{ text: msg.text }],
  }));

  const result = await genAI.models.generateContent({
    model,
    contents,
    config: {
      systemInstruction: systemPrompt,
    },
  });
  return result.text ?? '';
}
```

## Best Practices

1. **Always handle null/undefined**: Use `response.text ?? ''` for safe access
2. **Type your JSON responses**: Use generics with `JSON.parse()` result
3. **Use system instructions**: Define persona and behavior expectations
4. **Keep Gemini 3 temperature at 1.0**: Avoid performance degradation
5. **Validate JSON output**: Structured format doesn't guarantee semantic correctness
6. **Choose appropriate model**: Use Flash for speed, Pro for complex reasoning

## Common Mistakes to Avoid

- Don't lower temperature below 1.0 for Gemini 3 models
- Don't assume JSON responses are semantically valid - always validate
- Don't forget to handle the case where `response.text` is undefined
- Don't use raw string concatenation for multi-turn - use proper contents array
