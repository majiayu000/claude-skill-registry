---
name: sapiom
description: Access paid services (verification, search, AI models, image generation) for AI agents via Sapiom. Use when building agents that need to verify phone/email, search the web, call AI models, or generate images — without setting up vendor accounts.
---

# Sapiom

Instant access to paid services with pay-per-use pricing. No vendor account setup required.

## Documentation

**Always fetch the markdown docs for endpoint details, parameters, and examples.**

| Service | Documentation |
|---------|---------------|
| Verify | https://docs.sapiom.ai/md/capabilities/verify.md |
| Search | https://docs.sapiom.ai/md/capabilities/search.md |
| AI Models | https://docs.sapiom.ai/md/capabilities/ai-models.md |
| Images | https://docs.sapiom.ai/md/capabilities/images.md |
| Service Proxy | https://docs.sapiom.ai/md/service-proxy.md |

## Two Access Patterns

Sapiom offers two ways to call services. Choose based on your language and needs:

### 1. Direct Access (Node.js SDK)

Use the SDK to call provider gateways directly. The SDK handles payment negotiation automatically.

**When to use:** Node.js/TypeScript projects. Gives access to full provider API features.

**Setup:**
```bash
npm install @sapiom/axios axios
```

```typescript
import { withSapiom } from "@sapiom/axios";
import axios from "axios";

const client = withSapiom(axios.create(), {
  apiKey: process.env.SAPIOM_API_KEY,
});

// Example: Search with Linkup
const { data } = await client.post(
  "https://linkup.services.sapiom.ai/v1/search",
  { query: "quantum computing", depth: "standard", outputType: "sourcedAnswer" }
);
```

**Provider Gateway URLs:**

| Service | Base URL |
|---------|----------|
| Verify | `https://prelude.services.sapiom.ai` |
| Search (Linkup) | `https://linkup.services.sapiom.ai` |
| Search (You.com) | `https://you-com.services.sapiom.ai` |
| AI Models | `https://openrouter.services.sapiom.ai` |
| Images | `https://fal-ai.services.sapiom.ai` |

### 2. Semantic Endpoints (Python/REST)

Use simplified REST endpoints via the Service Proxy. No SDK required — just Bearer token auth.

**When to use:** Python, Go, Ruby, or any language without SDK support.

**Important:** Do NOT wrap Service Proxy calls with the SDK. The proxy handles payment server-side.

**Setup:**
```python
import requests
import os

headers = {
    "Authorization": f"Bearer {os.environ['SAPIOM_API_KEY']}",
    "Content-Type": "application/json"
}

# Example: Verify a phone number
resp = requests.post(
    "https://api.sapiom.ai/v1/services/verify/send",
    headers=headers,
    json={"phoneNumber": "+15551234567"}
)
verification_id = resp.json()["verificationRequestId"]

# Check the code
resp = requests.post(
    "https://api.sapiom.ai/v1/services/verify/check",
    headers=headers,
    json={"verificationRequestId": verification_id, "code": "123456"}
)
```

**Available semantic endpoints:** Currently Verify only. See https://docs.sapiom.ai/md/service-proxy.md

Other services (Search, AI Models, Images) require the Node.js SDK with direct access.

## Setup

1. Get your API key from https://app.sapiom.ai/settings
2. Set environment variable:
   ```bash
   export SAPIOM_API_KEY="your_key"
   ```

## Navigating Documentation

Links within markdown docs use relative paths. To get the full markdown URL:

| Path in docs | Markdown URL |
|--------------|--------------|
| `/capabilities/search` | `https://docs.sapiom.ai/md/capabilities/search.md` |
| `/quick-start` | `https://docs.sapiom.ai/md/quick-start.md` |
| `/service-proxy` | `https://docs.sapiom.ai/md/service-proxy.md` |

**Pattern:** Prepend `https://docs.sapiom.ai/md/` and append `.md`

## Need Details?

Fetch the markdown documentation for complete endpoint specs:

```bash
curl https://docs.sapiom.ai/md/capabilities/verify.md
```
