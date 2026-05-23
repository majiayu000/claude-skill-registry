---
name: sapiom
description: Access paid services (verification, search, AI models, image generation) for AI agents via Sapiom. Use when building agents that need to verify phone/email, search the web, call AI models, or generate images — without setting up vendor accounts.
---

# Sapiom

Instant access to paid services with pay-per-use pricing. No vendor account setup required.

## Documentation

For detailed, up-to-date endpoint documentation, fetch the markdown docs:

| Topic | Markdown URL |
|-------|--------------|
| Quick Start | https://docs.sapiom.ai/md/quick-start.md |
| Verify Users | https://docs.sapiom.ai/md/capabilities/verify.md |
| Web Search | https://docs.sapiom.ai/md/capabilities/search.md |
| AI Models | https://docs.sapiom.ai/md/capabilities/ai-models.md |
| Images | https://docs.sapiom.ai/md/capabilities/images.md |
| Service Proxy (Python) | https://docs.sapiom.ai/md/service-proxy.md |

## Setup

1. Get your API key from https://app.sapiom.ai/settings
2. Set environment variable:
   ```bash
   export SAPIOM_API_KEY="your_key"
   ```

### Node.js

```bash
npm install @sapiom/axios axios
```

```typescript
import { withSapiom } from "@sapiom/axios";
import axios from "axios";

const client = withSapiom(axios.create(), {
  apiKey: process.env.SAPIOM_API_KEY,
});
```

### Python (Service Proxy)

No SDK required. Use REST API with Bearer token authentication.

```python
import requests
import os

headers = {
    "Authorization": f"Bearer {os.environ['SAPIOM_API_KEY']}",
    "Content-Type": "application/json"
}
```

**Note:** Service Proxy currently supports Verify only. See https://docs.sapiom.ai/md/service-proxy.md

## Services

| Service | Base URL | Docs |
|---------|----------|------|
| Verify | `https://prelude.services.sapiom.ai` | [verify.md](https://docs.sapiom.ai/md/capabilities/verify.md) |
| Search (Linkup) | `https://linkup.services.sapiom.ai` | [search.md](https://docs.sapiom.ai/md/capabilities/search.md) |
| Search (You.com) | `https://you-com.services.sapiom.ai` | [search.md](https://docs.sapiom.ai/md/capabilities/search.md) |
| AI Models | `https://openrouter.services.sapiom.ai` | [ai-models.md](https://docs.sapiom.ai/md/capabilities/ai-models.md) |
| Images | `https://fal-ai.services.sapiom.ai` | [images.md](https://docs.sapiom.ai/md/capabilities/images.md) |

## Quick Examples

### Search with AI Answer (Node.js)

```typescript
const { data } = await client.post(
  "https://linkup.services.sapiom.ai/v1/search",
  { query: "quantum computing", depth: "standard", outputType: "sourcedAnswer" }
);
console.log(data.answer);
```

### Verify Phone (Node.js)

```typescript
// Step 1: Send code
const { data: send } = await client.post(
  "https://prelude.services.sapiom.ai/verifications",
  { target: { type: "phone_number", value: "+15551234567" } }
);

// Step 2: Check code
const { data: check } = await client.post(
  "https://prelude.services.sapiom.ai/verifications/check",
  { verificationRequestId: send.id, code: "123456" }
);
```

### Verify Phone (Python)

```python
# Step 1: Send code
resp = requests.post(
    "https://api.sapiom.ai/v1/services/verify/send",
    headers=headers,
    json={"phoneNumber": "+15551234567"}
)
request_id = resp.json()["verificationRequestId"]

# Step 2: Check code
resp = requests.post(
    "https://api.sapiom.ai/v1/services/verify/check",
    headers=headers,
    json={"verificationRequestId": request_id, "code": "123456"}
)
```

### AI Models (Node.js)

```typescript
const { data } = await client.post(
  "https://openrouter.services.sapiom.ai/v1/chat/completions",
  {
    model: "openai/gpt-4o-mini",
    messages: [{ role: "user", content: "Hello!" }],
    max_tokens: 100,
  }
);
```

## Pricing

| Service | Price |
|---------|-------|
| Verify | $0.015/verification |
| Search (Linkup) | $0.01-$0.08/search |
| Search (You.com) | $0.006/search |
| AI Models | Per-token (see [OpenRouter](https://openrouter.ai/docs#models)) |
| Images | $0.004-$0.04/megapixel |

## Navigating Documentation

Links within markdown docs use relative paths (e.g., `/capabilities/search`). To get the markdown version:

| HTML Path | Markdown Path |
|-----------|---------------|
| `/capabilities/search` | `/md/capabilities/search.md` |
| `/quick-start` | `/md/quick-start.md` |
| `/governance` | `/md/governance.md` |

**Pattern:** Prepend `/md/` and append `.md` to any doc path.

**Alternative:** Use `Accept: text/markdown` header with the regular URL:
```bash
curl -H "Accept: text/markdown" https://docs.sapiom.ai/capabilities/search
```

## Need More Details?

Fetch the markdown documentation for complete endpoint specs, parameters, and examples:

```bash
curl https://docs.sapiom.ai/md/capabilities/verify.md
```
