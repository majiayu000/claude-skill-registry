# RouterBase API Reference Notes

Use this reference for exact integration details. Prefer the live RouterBase documentation when making production claims.

## Product Facts

- RouterBase routes LLMs through one OpenAI-compatible API.
- The public docs describe the base URL as `https://routerbase.com/v1`.
- RouterBase positions itself as a drop-in replacement for the OpenAI SDK: change the client base URL and use a RouterBase API key.
- Publicly documented benefits include 200+ models, one API key, smart routing, automatic fallback, unified billing, and usage analytics.

Source pages:

- https://routerbase.com
- https://docs.routerbase.com
- https://docs.routerbase.com/api-reference/chat-completions

## Authentication

Every API request needs:

```http
Authorization: Bearer <YOUR_API_KEY>
Content-Type: application/json
```

Use `ROUTERBASE_API_KEY` in examples. Never place keys in frontend code.

## Core Endpoints

```text
POST https://routerbase.com/v1/chat/completions
POST https://routerbase.com/v1/images/generations
POST https://routerbase.com/v1/videos/generations
POST https://routerbase.com/v1/audio/speech
POST https://routerbase.com/v1/audio/generations
GET  https://routerbase.com/api/v1/models
GET  https://routerbase.com/api/v1/models/{model_id}
GET  https://routerbase.com/api/v1/models/{model_id}/pricing
GET  https://routerbase.com/api/v1/pricing
```

## Chat Completion Fields

Common OpenAI-compatible fields:

- `model`
- `messages`
- `temperature`
- `max_tokens`
- `top_p`
- `stream`
- `stop`
- `seed`
- `response_format`
- `presence_penalty`
- `frequency_penalty`
- `tools`
- `prompt_cache_key`

## Examples

Python:

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["ROUTERBASE_API_KEY"],
    base_url="https://routerbase.com/v1",
)

response = client.chat.completions.create(
    model="google/gemini-2.5-flash",
    messages=[{"role": "user", "content": "What is 2+2?"}],
)
```

JavaScript:

```js
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.ROUTERBASE_API_KEY,
  baseURL: "https://routerbase.com/v1",
});
```

Streaming:

```python
stream = client.chat.completions.create(
    model="google/gemini-2.5-flash",
    messages=[{"role": "user", "content": "Write a haiku"}],
    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")
```

Vision content parts:

```json
{
  "model": "google/gemini-2.5-flash",
  "messages": [
    {
      "role": "user",
      "content": [
        { "type": "text", "text": "What's in this image?" },
        { "type": "image_url", "image_url": { "url": "https://example.com/image.png" } }
      ]
    }
  ]
}
```

## Validation

When debugging:

1. Confirm `ROUTERBASE_API_KEY` is set server-side.
2. Confirm `base_url` or `baseURL` is exactly `https://routerbase.com/v1`.
3. Confirm headers include bearer auth and JSON content type.
4. Confirm model ID exists in the live catalog.
5. Confirm the selected endpoint matches the model modality.
6. Check for rate-limit responses before adding fallback logic.
