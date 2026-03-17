---
name: elevenlabs-agents
description: >
  Build conversational AI voice agents with ElevenLabs Platform.
  Workflow: configure agent, add tools and knowledge base, integrate SDK, test, deploy.
  Supports React, React Native, and Swift SDKs. Use when building voice agents,
  AI phone systems, or troubleshooting @11labs deprecated packages, webhook errors,
  CSP violations, localhost allowlist, or tool parsing errors.
---

# ElevenLabs Agent Builder

Build a production-ready conversational AI voice agent. Produces a configured agent with tools, knowledge base, and SDK integration.

## Packages

```bash
npm install @elevenlabs/react           # React SDK
npm install @elevenlabs/client          # JavaScript SDK (browser + server)
npm install @elevenlabs/react-native    # React Native SDK
npm install @elevenlabs/elevenlabs-js   # Full API (server only)
npm install -g @elevenlabs/agents-cli   # CLI ("Agents as Code")
```

**DEPRECATED:** `@11labs/react`, `@11labs/client` — uninstall if present.

**Server-only warning:** `@elevenlabs/elevenlabs-js` uses Node.js `child_process` and won't work in browsers. Use `@elevenlabs/client` for browser environments, or create a proxy server.

## Workflow

### Step 1: Create Agent via Dashboard or CLI

**Dashboard:** https://elevenlabs.io/app/conversational-ai → Create Agent

**CLI (Agents as Code):**
```bash
elevenlabs-cli init my-agent
# Edit agent.config.ts with agent settings
elevenlabs-cli deploy
```

Configure:
- **Voice** — Choose from 5000+ voices or clone
- **LLM** — GPT, Claude, Gemini, or custom
- **System prompt** — See `assets/system-prompt-template.md`
- **First message** — What the agent says when conversation starts

### Step 2: Add Tools

Tools let the agent take actions during conversation:

```typescript
// Client-side tools (run in browser)
const clientTools = {
  navigate: {
    description: "Navigate to a page",
    parameters: { type: "object", properties: { url: { type: "string" } } },
    handler: async ({ url }) => { window.location.href = url; return "Navigated"; }
  }
};

// Server-side tools (webhooks)
// Configure in dashboard: Settings → Tools → Add Webhook
```

See `references/tool-examples.md` for patterns.

### Step 3: Add Knowledge Base (RAG)

Upload documents for the agent to reference:
- PDFs, text files, web URLs
- Configure via dashboard or API
- Agent automatically searches knowledge base during conversation

### Step 4: Integrate SDK

**React** — copy and customise `assets/react-sdk-boilerplate.tsx`:

```typescript
import { useConversation } from '@elevenlabs/react';

const { startConversation, stopConversation, status } = useConversation({
  agentId: 'your-agent-id',
  signedUrl: '/api/elevenlabs/auth',
  clientTools,
  onEvent: (event) => { /* transcript, agent_response, tool_call */ },
});
```

**React Native** — see `assets/react-native-boilerplate.tsx`
**Widget embed** — see `assets/widget-embed-template.html`
**Swift** — see `assets/swift-sdk-boilerplate.swift`

### Step 5: Test and Deploy

```bash
# Test locally
elevenlabs-cli test my-agent

# Simulate conversation
elevenlabs-cli simulate my-agent --scenario "Book appointment for tomorrow"

# Deploy
elevenlabs-cli deploy my-agent
```

Use `scripts/test-agent.sh` and `scripts/simulate-conversation.sh` for automated testing.

---

## Critical Patterns

### Signed URLs (Security)

Never expose API keys in client code. Use a server endpoint:

```typescript
// Server endpoint
app.get('/api/elevenlabs/auth', async (req, res) => {
  const response = await fetch('https://api.elevenlabs.io/v1/convai/conversation/get-signed-url', {
    headers: { 'xi-api-key': process.env.ELEVENLABS_API_KEY },
    body: JSON.stringify({ agent_id: 'your-agent-id' }),
    method: 'POST'
  });
  const { signed_url } = await response.json();
  res.json({ signed_url });
});
```

### Agent Versioning (A/B Testing)

Create version branches for testing different configurations:
- Dashboard: Agent → Versions → Create Branch
- Compare metrics between versions
- Promote winning version to production

### Dynamic Variables

Pass user context to the agent's system prompt:

```typescript
const { startConversation } = useConversation({
  agentId: 'your-agent-id',
  dynamicVariables: {
    user_name: 'John',
    account_type: 'premium',
  }
});
```

System prompt references them as `{{user_name}}`.

---

## Asset Files

- `assets/react-sdk-boilerplate.tsx` — React integration template
- `assets/react-native-boilerplate.tsx` — React Native template
- `assets/swift-sdk-boilerplate.swift` — Swift/iOS template
- `assets/javascript-sdk-boilerplate.js` — Vanilla JS template
- `assets/widget-embed-template.html` — Embeddable widget
- `assets/system-prompt-template.md` — System prompt guide
- `assets/agent-config-schema.json` — Config schema reference
- `assets/ci-cd-example.yml` — CI/CD pipeline template

## Scripts

- `scripts/create-agent.sh` — Create agent via API
- `scripts/deploy-agent.sh` — Deploy agent
- `scripts/test-agent.sh` — Run agent tests
- `scripts/simulate-conversation.sh` — Simulate conversations

## Reference Files

- `references/api-reference.md` — Full API endpoints
- `references/tool-examples.md` — Client and server tool patterns
- `references/system-prompt-guide.md` — Prompt engineering for agents
- `references/cli-commands.md` — CLI reference
- `references/workflow-examples.md` — End-to-end workflow examples
- `references/testing-guide.md` — Testing and simulation
- `references/cost-optimization.md` — Pricing and optimisation
- `references/compliance-guide.md` — Data residency and compliance
