---
name: elevenlabs-agents
description: ElevenLabs Agents Platform for AI voice agents (React/JS/Native/Swift). Use for voice AI, RAG, tools, or encountering package deprecation, audio cutoff, CSP violations, webhook auth failures.

  Keywords: ElevenLabs Agents, ElevenLabs voice agents, AI voice agents, conversational AI, @elevenlabs/react, @elevenlabs/client, @elevenlabs/react-native, @elevenlabs/elevenlabs-js, @elevenlabs/agents-cli, elevenlabs SDK, voice AI, TTS, text-to-speech, ASR, speech recognition, turn-taking model, WebRTC voice, WebSocket voice, ElevenLabs conversation, agent system prompt, agent tools, agent knowledge base, RAG voice agents, multi-voice agents, pronunciation dictionary, voice speed control, elevenlabs scribe, @11labs deprecated, Android audio cutoff, CSP violation elevenlabs, dynamic variables elevenlabs, case-sensitive tool names, webhook authentication
license: MIT
metadata:
  version: 1.1.0
  last_updated: 2025-11-21
  production_tested: true
  packages:
    - name: "@elevenlabs/elevenlabs-js"
      version: 2.25.0
    - name: "@elevenlabs/agents-cli"
      version: 0.2.0
    - name: "@elevenlabs/react"
      version: 0.11.0
    - name: "@elevenlabs/client"
      version: 0.11.0
    - name: "@elevenlabs/react-native"
      version: 0.5.2
  documentation:
    - https://elevenlabs.io/docs/agents-platform/overview
    - https://elevenlabs.io/docs/api-reference
    - https://github.com/elevenlabs/elevenlabs-examples
  errors_prevented: 17+
  token_savings: ~73%
---

# ElevenLabs Agents Platform

## Overview

ElevenLabs Agents Platform is a comprehensive solution for building production-ready conversational AI voice agents. The platform coordinates four core components:

1. **ASR (Automatic Speech Recognition)** - Converts speech to text (32+ languages, sub-second latency)
2. **LLM (Large Language Model)** - Reasoning and response generation (GPT, Claude, Gemini, custom models)
3. **TTS (Text-to-Speech)** - Converts text to speech (5000+ voices, 31 languages, low latency)
4. **Turn-Taking Model** - Proprietary model that handles conversation timing and interruptions

### 🚨 Package Migration (August 2025)

**DEPRECATED (Do not use):** `@11labs/react` and `@11labs/client`

**Current packages:**
```bash
bun add @elevenlabs/react@0.11.0        # React SDK
bun add @elevenlabs/client@0.11.0       # JavaScript SDK
bun add @elevenlabs/react-native@0.5.2  # React Native SDK
bun add @elevenlabs/elevenlabs-js@2.25.0 # Base SDK
bun add -g @elevenlabs/agents-cli@0.2.0  # CLI
```

If migrating, uninstall old packages first: `npm uninstall @11labs/react @11labs/client`

---

## Quick Start

### Path A: React SDK (Embedded Voice Chat)

For building voice chat interfaces in React applications.

**Installation:**
```bash
bun add @elevenlabs/react zod
```

**Basic Example:**
```typescript
import { useConversation } from '@elevenlabs/react';
import { z } from 'zod';

export default function VoiceChat() {
  const { startConversation, stopConversation, status } = useConversation({
    // Authentication (choose one)
    agentId: 'your-agent-id',  // Public agent (no key needed)
    // apiKey: process.env.NEXT_PUBLIC_ELEVENLABS_API_KEY,  // Private (dev only)
    // signedUrl: '/api/elevenlabs/auth',  // Signed URL (production)

    // Client-side tools
    clientTools: {
      updateCart: {
        description: "Update the shopping cart",
        parameters: z.object({
          item: z.string(),
          quantity: z.number()
        }),
        handler: async ({ item, quantity }) => {
          console.log('Updating cart:', item, quantity);
          return { success: true };
        }
      }
    },

    // Event handlers
    onEvent: (event) => {
      if (event.type === 'transcript') console.log('User:', event.data.text);
      if (event.type === 'agent_response') console.log('Agent:', event.data.text);
    },

    // Regional compliance
    serverLocation: 'us' // 'us' | 'global' | 'eu-residency' | 'in-residency'
  });

  return (
    <div>
      <button onClick={startConversation}>Start Conversation</button>
      <button onClick={stopConversation}>Stop</button>
      <p>Status: {status}</p>
    </div>
  );
}
```

**Complete template:** See `templates/basic-react-agent.tsx`

### Path B: CLI ("Agents as Code")

For managing agents via code with version control and CI/CD. Load `references/cli-commands.md` when using CLI workflows.

**Quick workflow:**
```bash
bun add -g @elevenlabs/agents-cli
elevenlabs auth login
elevenlabs agents init
elevenlabs agents add "Support Agent" --template customer-service
# Edit agent_configs/support-agent.json
elevenlabs agents push --env dev
elevenlabs agents test "Support Agent"
```

**See:** `references/cli-commands.md` for complete CLI reference and workflows.

### Path C: API (Programmatic Agent Management)

For creating agents dynamically (multi-tenant, SaaS platforms). Load `references/api-reference.md` when using the API directly.

**Quick example:**
```typescript
import { ElevenLabsClient } from 'elevenlabs';

const client = new ElevenLabsClient({
  apiKey: process.env.ELEVENLABS_API_KEY
});

const agent = await client.agents.create({
  name: 'Support Bot',
  conversation_config: {
    agent: {
      prompt: { prompt: "You are a helpful support agent.", llm: "gpt-4o" },
      first_message: "Hello! How can I help you today?"
    },
    tts: { model_id: "eleven_turbo_v2_5", voice_id: "your-voice-id" }
  }
});
```

**See:** `references/api-reference.md` for complete API reference.

---

## Agent Configuration

### System Prompt Framework

ElevenLabs recommends a 6-component prompt structure: **Personality** (identity/role), **Environment** (communication context), **Tone** (formality/speech patterns), **Goal** (objectives/success criteria), **Guardrails** (boundaries/ethics), and **Tools** (available functions).

**Example structure:**
```
Personality: You are Alex, a friendly customer support specialist at TechCorp.
Environment: Phone communication, voice-only, potential background noise.
Tone: Professional yet warm. Use contractions. Keep responses to 2-3 sentences.
Goal: Resolve issues on first call. Success = customer confirms resolution.
Guardrails: Never give medical/legal advice. Escalate if customer becomes abusive.
Tools: lookup_order(id), transfer_to_supervisor(), send_password_reset(email)
```

**Complete guide:** Load `references/system-prompt-guide.md` when configuring agent prompts or improving conversation quality.

### Turn-Taking Modes

| Mode | Behavior | Best For |
|------|----------|----------|
| **Eager** | Responds quickly, jumps in early | Fast-paced support, quick orders |
| **Normal** | Balanced, waits for natural breaks | General customer service (default) |
| **Patient** | Waits longer for detailed responses | Information collection, tutoring |

Configuration: `"turn": { "mode": "patient" }` in `conversation_config`

---

## Core Features Summary

### Voice & Language
- **Multi-Voice:** Dynamic voice switching (adds ~200ms latency per switch)
- **Pronunciation Dictionary:** IPA, CMU, or word substitutions for custom pronunciation
- **Speed Control:** 0.7x - 1.2x (1.0x = normal)
- **Languages:** 32+ languages with auto-detection and multi-language presets

### Knowledge Base (RAG)
Upload documents (PDF/TXT/DOCX) for semantic search during conversations. Agent retrieves relevant chunks automatically. Adds ~500ms latency per query. Documents must be indexed before use.

**See:** `references/api-reference.md` for knowledge base API and configuration.

### Tools (4 Types)
1. **Client Tools** - Execute in browser (UI updates, navigation, local storage)
2. **Server Tools (Webhooks)** - Execute on your backend (database, payments, CRM)
3. **MCP Tools** - Connect to Model Context Protocol servers (enterprise APIs)
4. **System Tools** - Built-in platform tools (end_conversation, transfer_call, mute_microphone, press_digit)

**See:** `references/tool-examples.md` when implementing tools. Load `references/api-reference.md` for webhook tool creation API.

---

## Top 3 Critical Errors

### Error 1: Package Deprecation (@11labs/*)

**Symptom:** Import errors, "module not found"

**Solution:**
```bash
npm uninstall @11labs/react @11labs/client
bun add @elevenlabs/react@0.11.0 @elevenlabs/client@0.11.0

# Update imports:
import { useConversation } from '@elevenlabs/react';  // Not @11labs/react
```

### Error 2: Android Audio Cutoff (First Message)

**Symptom:** First agent message cuts off on Android only (iOS/web work fine)

**Solution:**
```typescript
const { startConversation } = useConversation({
  agentId: 'your-agent-id',
  connectionDelay: {
    android: 3_000,  // 3 seconds for Android audio mode switch
    ios: 0,
    default: 0
  }
});
```

### Error 3: CSP (Content Security Policy) Violations

**Symptom:** "Refused to load the script..." errors, CSP blocks blob URLs

**Solution - Self-host worklet files:**
```bash
cp node_modules/@elevenlabs/client/dist/worklets/*.js public/elevenlabs/
```

```typescript
const { startConversation } = useConversation({
  agentId: 'your-agent-id',
  workletPaths: {
    'rawAudioProcessor': '/elevenlabs/rawAudioProcessor.worklet.js',
    'audioConcatProcessor': '/elevenlabs/audioConcatProcessor.worklet.js',
  }
});
```

**See all 17 errors:** Load `references/error-catalog.md` when troubleshooting errors, debugging webhook failures, RAG issues, or platform-specific problems.

---

## When to Load References

Load specific reference files based on your current task:

### `references/api-reference.md`
Load when: Creating agents via API, managing agents programmatically, building multi-tenant systems, implementing knowledge base, creating webhook tools, handling API errors, or understanding API rate limits.

### `references/cli-commands.md`
Load when: Using CLI for agent management, setting up CI/CD pipelines, managing multi-environment deployments (dev/staging/prod), version controlling agent configs, or troubleshooting CLI issues.

### `references/compliance-guide.md`
Load when: Implementing GDPR compliance, handling HIPAA requirements (healthcare), configuring SOC 2 controls, setting data retention policies, implementing regional data residency (EU/IN), or handling PCI DSS (payments).

### `references/cost-optimization.md`
Load when: Optimizing LLM costs, implementing caching strategies, choosing between models (GPT/Claude/Gemini), handling traffic spikes (burst pricing), reducing token usage, or setting budget limits.

### `references/error-catalog.md`
Load when: Troubleshooting errors, debugging webhook failures, fixing voice consistency issues, resolving authentication problems, handling RAG index issues, or diagnosing platform-specific bugs.

### `references/system-prompt-guide.md`
Load when: Writing agent system prompts, improving conversation quality, implementing 6-component framework, iterating on prompts, testing prompt effectiveness, or defining agent personality/goals/guardrails.

### `references/testing-guide.md`
Load when: Setting up automated tests, implementing scenario testing, load testing agents, converting real conversations to tests, integrating with CI/CD, or debugging failed tests.

### `references/tool-examples.md`
Load when: Implementing client tools (browser functions), creating server tools (webhooks), connecting MCP servers, using system tools, or debugging tool execution issues.

### `references/workflow-examples.md`
Load when: Building multi-agent workflows, implementing call routing, creating escalation flows, designing multi-language support, or debugging workflow transitions.

---

## SDK Integrations

### React SDK (`@elevenlabs/react`)
Primary hook: `useConversation()`. Features: client tools, event streaming, connection management, regional compliance. See Quick Start Path A above.

### Other SDKs
- **JavaScript SDK** (`@elevenlabs/client`) - Vanilla JS/Node.js
- **React Native SDK** (`@elevenlabs/react-native`) - Mobile apps (Expo)
- **Swift SDK** - iOS/macOS native apps
- **Widget** - Embeddable web component (no code)

**Template:** See `templates/basic-react-agent.tsx` for complete React implementation.

---

## Additional Platform Features

**Testing & Evaluation:** Scenario testing (LLM-based), tool call testing, load testing, simulation API. See `references/testing-guide.md`.

**Analytics:** Conversation analysis, success evaluation, data collection, analytics dashboard.

**Privacy & Compliance:** Data retention, encryption, zero retention mode, GDPR/HIPAA/SOC 2. See `references/compliance-guide.md`.

**Cost Optimization:** LLM caching (90% savings), model swapping, burst pricing. See `references/cost-optimization.md`.

**Advanced:** Custom models (bring your own LLM), post-call webhooks, chat mode (text-only), telephony (Twilio/SIP), workflows (multi-agent routing).

---

## Integration with Other Skills

Composes with:
- **cloudflare-worker-base** → Deploy agents on edge network
- **cloudflare-workers-ai** → Use Cloudflare LLMs as custom models
- **cloudflare-durable-objects** → Persistent conversation state
- **nextjs** → React SDK integration in Next.js
- **ai-sdk-core** → Vercel AI SDK provider
- **clerk-auth** → Authenticated voice sessions
- **hono-routing** → API routes for webhooks

---

## Resources

**Templates** (`templates/`):
- `basic-react-agent.tsx` - React SDK with client tools and events
- `basic-cli-agent.json` - CLI agent with 6-component prompt

**References** (`references/`):
- `api-reference.md` - Complete API reference
- `cli-commands.md` - CLI commands and workflows
- `compliance-guide.md` - GDPR/HIPAA/SOC 2 compliance
- `cost-optimization.md` - LLM caching and cost reduction
- `error-catalog.md` - All 17 errors with solutions
- `system-prompt-guide.md` - 6-component framework guide
- `testing-guide.md` - Testing and evaluation
- `tool-examples.md` - Client/server/MCP tool examples
- `workflow-examples.md` - Multi-agent workflow patterns

**Official Documentation:**
- Platform: https://elevenlabs.io/docs/agents-platform/overview
- API: https://elevenlabs.io/docs/api-reference
- Examples: https://github.com/elevenlabs/elevenlabs-examples
- Discord: https://discord.com/invite/elevenlabs

---

**Production Tested:** WordPress Auditor, Customer Support Agents
**Last Updated:** 2025-11-21
**Package Versions:** Verified current (see metadata)
