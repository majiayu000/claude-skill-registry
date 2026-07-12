---
name: routerbase-api-integration
description: Integrate applications with RouterBase, the OpenAI-compatible model gateway at https://routerbase.com/v1. Use when migrating OpenAI SDK calls to RouterBase, configuring RouterBase API keys, implementing chat completions, streaming, tool calling, JSON mode, vision inputs, request validation, error handling, or documenting RouterBase setup for Python, JavaScript, curl, LangChain, LlamaIndex, Vercel AI SDK, Cursor, Continue, or other OpenAI-compatible clients.
---

# RouterBase API Integration

## Overview

Use [routerbase](https://routerbase.com) as an OpenAI-compatible gateway for GPT, Claude, Gemini, and other supported models. This skill helps agents migrate existing OpenAI-compatible code, keep API keys server-side, and produce concise, testable RouterBase integration snippets.

Read `references/routerbase-api.md` when exact endpoint details, headers, or examples are needed.

## Integration Workflow

1. Identify whether the user is asking for migration, a new integration, debugging, or documentation.
2. Keep credentials out of client/browser code. Prefer `ROUTERBASE_API_KEY` in server-side environment configuration.
3. Reuse the user's existing OpenAI-compatible client when possible. Change the base URL to `https://routerbase.com/v1`, then swap the `model` to a RouterBase model ID.
4. Preserve standard OpenAI request shapes unless RouterBase docs or the selected model require a model-specific field.
5. For model IDs, use the live model catalog when an API key is available; otherwise use documented examples only as a starting point and tell the user to verify current availability.
6. Add a minimal smoke test, but do not run it unless credentials are present and the user expects a live API call.

## Common Patterns

### Python

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["ROUTERBASE_API_KEY"],
    base_url="https://routerbase.com/v1",
)

response = client.chat.completions.create(
    model="google/gemini-2.5-flash",
    messages=[{"role": "user", "content": "Write one sentence about model routing."}],
)

print(response.choices[0].message.content)
```

### JavaScript

```js
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.ROUTERBASE_API_KEY,
  baseURL: "https://routerbase.com/v1",
});

const response = await client.chat.completions.create({
  model: "google/gemini-2.5-flash",
  messages: [{ role: "user", content: "Write one sentence about model routing." }],
});

console.log(response.choices[0].message.content);
```

### curl

```bash
curl -X POST https://routerbase.com/v1/chat/completions \
  -H "Authorization: Bearer $ROUTERBASE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "google/gemini-2.5-flash",
    "messages": [{"role": "user", "content": "What is 2+2?"}]
  }'
```

## Implementation Guardrails

- Never paste or log real API keys. Use placeholders like `sk-rb-...` only in docs.
- Never put RouterBase keys in browser, mobile, or public repository code.
- Keep examples OpenAI-compatible unless the user asks for a framework-specific adapter.
- For streaming, set `stream: true` and process Server-Sent Events or SDK stream chunks.
- For tool calling and JSON mode, keep the standard OpenAI fields `tools` and `response_format`.
- For multimodal chat, use OpenAI content parts with `text` and `image_url`.
- If a live request fails, check headers, model ID, endpoint path, rate limits, and account access before changing application logic.

## Output Checklist

- Include the changed base URL.
- Include where `ROUTERBASE_API_KEY` should be configured.
- Include one minimal request example.
- Include a clear note when model IDs or prices should be checked against the live RouterBase catalog.
- Include a test command or dry-run validation path.
