---
name: elevenlabs-agents
description: |
  Build conversational AI voice agents with ElevenLabs Platform. Configure agents, tools, RAG knowledge bases, multi-voice, and Scribe STT across React, React Native, or Swift. Prevents 34 documented errors.

  Use when: building voice agents, AI phone systems, or troubleshooting @11labs deprecated, webhook errors, CSP violations, localhost allowlist, tool parsing errors.
user-invocable: true
---

# ElevenLabs Agents Platform

## Overview

ElevenLabs Agents Platform is a comprehensive solution for building production-ready conversational AI voice agents. The platform coordinates four core components:

1. **ASR (Automatic Speech Recognition)** - Converts speech to text (32+ languages, sub-second latency)
2. **LLM (Large Language Model)** - Reasoning and response generation (GPT, Claude, Gemini, custom models)
3. **TTS (Text-to-Speech)** - Converts text to speech (5000+ voices, 31 languages, low latency)
4. **Turn-Taking Model** - Proprietary model that handles conversation timing and interruptions

### 🚨 Package Updates (January 2026)

ElevenLabs migrated to new scoped packages in August 2025. **Current packages:**

```bash
npm install @elevenlabs/react@0.12.3           # React SDK (Dec 2025: localization, Scribe fixes)
npm install @elevenlabs/client@0.12.2          # JavaScript SDK (Dec 2025: localization)
npm install @elevenlabs/react-native@0.5.7     # React Native SDK (Dec 2025: mic fixes, speed param)
npm install @elevenlabs/elevenlabs-js@2.30.0   # Base SDK (Jan 2026: latest)
npm install -g @elevenlabs/agents-cli@0.6.1    # CLI
```

**DEPRECATED:** `@11labs/react`, `@11labs/client` (uninstall if present)

**⚠️ CRITICAL:** v1 TTS models were removed on 2025-12-15. Use Turbo v2/v2.5 only.

### December 2025 Updates

**Widget Improvements (v0.5.5)**:
- Microphone permission handling improvements (better UX for permission requests)
- Text-only mode (`chat_mode: true`) no longer requires microphone access
- `end_call` system tool fix (no longer omits last message)

**SDK Fixes**:
- Scribe audio format parameter now correctly transmitted (v2.32.0, Jan 2026)
- React Native infinite loop fix in useEffect dependencies (v0.5.6)
- Speed parameter support in TTS overrides (v0.5.7)
- Localization support for chat UI terms (v0.12.3)

---

## Package Selection Guide

**Which ElevenLabs package should I use?**

| Package | Environment | Use Case |
|---------|-------------|----------|
| `@elevenlabs/elevenlabs-js` | **Server only** (Node.js) | Full API access, TTS, voices, models |
| `@elevenlabs/client` | **Browser + Server** | Agents SDK, WebSocket, lightweight |
| `@elevenlabs/react` | **React apps** | Conversational AI hooks |
| `@elevenlabs/react-native` | **Mobile** | iOS/Android agents |

**⚠️ Why elevenlabs-js doesn't work in browser:**
- Depends on Node.js `child_process` module (by design)
- **Error**: `Module not found: Can't resolve 'child_process'`
- **Workaround for browser API access**: Create proxy server endpoint using `elevenlabs-js`, call proxy from browser

**Affected Frameworks:**
- Next.js client components
- Vite browser builds
- Electron renderer process
- Tauri webview

**Source**: [GitHub Issue #293](https://github.com/elevenlabs/elevenlabs-js/issues/293)

---

## 1. Quick Start

### React SDK
```bash
npm install @elevenlabs/react zod
```

```typescript
import { useConversation } from '@elevenlabs/react';

const { startConversation, stopConversation, status } = useConversation({
  agentId: 'your-agent-id',
  signedUrl: '/api/elevenlabs/auth', // Recommended (secure)
  // OR apiKey: process.env.NEXT_PUBLIC_ELEVENLABS_API_KEY,

  clientTools: { /* browser-side tools */ },
  onEvent: (event) => { /* transcript, agent_response, tool_call */ },
  serverLocation: 'us' // 'eu-residency' | 'in-residency' | 'global'
});
```

### CLI ("Agents as Code")
```bash
npm install -g @elevenlabs/agents-cli
elevenlabs auth login
elevenlabs agents init                              # Creates agents.json, tools.json, tests.json
elevenlabs agents add "Bot" --template customer-service
elevenlabs agents push --env dev                    # Deploy
elevenlabs agents test "Bot"                        # Test
```

### API (Programmatic)
```typescript
import { ElevenLabsClient } from 'elevenlabs';
const client = new ElevenLabsClient({ apiKey: process.env.ELEVENLABS_API_KEY });

const agent = await client.agents.create({
  name: 'Support Bot',
  conversation_config: {
    agent: { prompt: { prompt: "...", llm: "gpt-4o" }, language: "en" },
    tts: { model_id: "eleven_turbo_v2_5", voice_id: "your-voice-id" }
  }
});
```

---

## 2. SDK Parameter Naming (camelCase vs snake_case)

**CRITICAL**: The JS SDK uses **camelCase** for parameters while the Python SDK and API use **snake_case**. Using snake_case in JS causes silent failures where parameters are ignored.

**Common Parameters:**

| API/Python (snake_case) | JS SDK (camelCase) |
|-------------------------|-------------------|
| `model_id` | `modelId` |
| `voice_id` | `voiceId` |
| `output_format` | `outputFormat` |
| `voice_settings` | `voiceSettings` |

**Example:**
```typescript
// ❌ WRONG - parameter ignored (snake_case):
const stream = await elevenlabs.textToSpeech.convert(voiceId, {
  model_id: "eleven_v3",  // Silently ignored!
  text: "Hello"
});

// ✅ CORRECT - use camelCase:
const stream = await elevenlabs.textToSpeech.convert(voiceId, {
  modelId: "eleven_v3",   // Works!
  text: "Hello"
});
```

**Tip**: Always check TypeScript types for correct parameter names. This is the most common error when migrating from Python SDK.

**Source**: [GitHub Issue #300](https://github.com/elevenlabs/elevenlabs-js/issues/300)

---

## 3. Agent Configuration

### System Prompt Architecture (6 Components)

**1. Personality** - Identity, role, character traits
**2. Environment** - Communication context (phone, web, video)
**3. Tone** - Formality, speech patterns, verbosity
**4. Goal** - Objectives and success criteria
**5. Guardrails** - Boundaries, prohibited topics, ethical constraints
**6. Tools** - Available capabilities and when to use them

**Template:**
```json
{
  "agent": {
    "prompt": {
      "prompt": "Personality:\n[Agent identity and role]\n\nEnvironment:\n[Communication context]\n\nTone:\n[Speech style]\n\nGoal:\n[Primary objectives]\n\nGuardrails:\n[Boundaries and constraints]\n\nTools:\n[Available tools and usage]",
      "llm": "gpt-4o", // gpt-5.1, claude-sonnet-4-5, gemini-3-pro-preview
      "temperature": 0.7
    }
  }
}
```

**2025 LLM Models:**
- `gpt-5.1`, `gpt-5.1-2025-11-13` (Oct 2025)
- `claude-sonnet-4-5`, `claude-sonnet-4-5@20250929` (Oct 2025)
- `gemini-3-pro-preview` (2025)
- `gemini-2.5-flash-preview-09-2025` (Oct 2025)

### Turn-Taking Modes

| Mode | Behavior | Best For |
|------|----------|----------|
| **Eager** | Responds quickly | Fast-paced support, quick orders |
| **Normal** | Balanced (default) | General customer service |
| **Patient** | Waits longer | Information collection, therapy |

```json
{ "conversation_config": { "turn": { "mode": "patient" } } }
```

### Workflows & Agent Management (2025)

**Workflow Features:**
- **Subagent Nodes** - Override prompt, voice, turn-taking per node
- **Tool Nodes** - Guarantee tool execution
- **Edges** - Conditional routing with `edge_order` (determinism, Oct 2025)

```json
{
  "workflow": {
    "nodes": [
      { "id": "node_1", "type": "subagent", "config": { "system_prompt": "...", "turn_eagerness": "patient" } },
      { "id": "node_2", "type": "tool", "tool_name": "transfer_to_human" }
    ],
    "edges": [{ "from": "node_1", "to": "node_2", "condition": "escalation", "edge_order": 1 }]
  }
}
```

**Agent Management (2025):**
- **Agent Archiving** - `archived: true` field (Oct 2025)
- **Agent Duplication** - Clone existing agents
- **Service Account API Keys** - Management endpoints (Jul 2025)

### Dynamic Variables

Use `{{var_name}}` syntax in prompts, messages, and tool parameters.

**System Variables:**
- `{{system__agent_id}}`, `{{system__conversation_id}}`
- `{{system__caller_id}}`, `{{system__called_number}}` (telephony)
- `{{system__call_duration_secs}}`, `{{system__time_utc}}`
- `{{system__call_sid}}` (Twilio only)

**Custom Variables:**
```typescript
await client.conversations.create({
  agent_id: "agent_123",
  dynamic_variables: { user_name: "John", account_tier: "premium" }
});
```

**Secret Variables:** `{{secret__api_key}}` (headers only, never sent to LLM)

**⚠️ Error:** Missing variables cause "Missing required dynamic variables" - always provide all referenced variables.

---

## 3. Voice & Language Features

### Multi-Voice, Pronunciation & Speed

**Multi-Voice** - Switch voices dynamically (adds ~200ms latency per switch):
```json
{ "prompt": "When speaking as customer, use voice_id 'voice_abc'. As agent, use 'voice_def'." }
```

**Pronunciation Dictionary** - IPA, CMU, word substitutions (Turbo v2/v2.5 only):
```json
{
  "pronunciation_dictionary": [
    { "word": "API", "pronunciation": "ey-pee-ay", "format": "cmu" },
    { "word": "AI", "substitution": "artificial intelligence" }
  ]
}
```

**PATCH Support (Aug 2025)** - Update dictionaries without replacement

**Speed Control** - 0.7x-1.2x (use 0.9x-1.1x for natural sound):
```json
{ "voice_settings": { "speed": 1.0 } }
```

**Voice Cloning Best Practices:**
- Clean audio (no noise, music, pops)
- Consistent microphone distance
- 1-2 minutes of audio
- Use language-matched voices (English voices fail on non-English)

### Language Configuration

**32+ Languages** with automatic detection and in-conversation switching.

**Multi-Language Presets:**
```json
{
  "language_presets": [
    { "language": "en", "voice_id": "en_voice", "first_message": "Hello!" },
    { "language": "es", "voice_id": "es_voice", "first_message": "¡Hola!" }
  ]
}
```

---

## 4. Knowledge Base & RAG

Enable agents to access large knowledge bases without loading entire documents into context.

**Workflow:**
1. Upload documents (PDF, TXT, DOCX)
2. Compute RAG index (vector embeddings)
3. Agent retrieves relevant chunks during conversation

**Configuration:**
```json
{
  "agent": { "prompt": { "knowledge_base": ["doc_id_1", "doc_id_2"] } },
  "knowledge_base_config": {
    "max_chunks": 5,
    "vector_distance_threshold": 0.8
  }
}
```

**API Upload:**
```typescript
const doc = await client.knowledgeBase.upload({ file: fs.createReadStream('docs.pdf'), name: 'Docs' });
await client.knowledgeBase.computeRagIndex({ document_id: doc.id, embedding_model: 'e5_mistral_7b' });
```

**⚠️ Gotchas:** RAG adds ~500ms latency. Check index status before use - indexing can take minutes.

---

## 5. Tools (4 Types)

### ⚠️ BREAKING CHANGE: prompt.tools Deprecated (July 2025)

The legacy `prompt.tools` array was **removed on July 23, 2025**. All agent configurations must use the new format.

**Migration Timeline:**
- July 14, 2025: Legacy format still accepted
- July 15, 2025: GET responses stop including `tools` field
- **July 23, 2025**: POST/PATCH reject `prompt.tools` (active now)

**Old Format** (no longer works):
```typescript
{
  agent: {
    prompt: {
      tools: [{ name: "get_weather", url: "...", method: "GET" }]
    }
  }
}
```

**New Format** (required):
```typescript
{
  agent: {
    prompt: {
      tool_ids: ["tool_abc123"],         // Client/server tools
      built_in_tools: ["end_call"]       // System tools (new field)
    }
  }
}
```

**Error if both used**: "A request must include either prompt.tool_ids or the legacy prompt.tools array — never both"

**Note**: All tools from legacy format were auto-migrated to standalone tool records.

**Source**: [Official Migration Guide](https://elevenlabs.io/docs/agents-platform/customization/tools/agent-tools-deprecation)

---

### A. Client Tools (Browser/Mobile)

Execute in browser or mobile app. **Tool names case-sensitive.**

```typescript
clientTools: {
  updateCart: {
    description: "Update shopping cart",
    parameters: z.object({ item: z.string(), quantity: z.number() }),
    handler: async ({ item, quantity }) => {
      // Client-side logic
      return { success: true };
    }
  }
}
```

### B. Server Tools (Webhooks)

HTTP requests to external APIs. **PUT support added Apr 2025.**

```json
{
  "name": "get_weather",
  "url": "https://api.weather.com/{{user_id}}",
  "method": "GET",
  "headers": { "Authorization": "Bearer {{secret__api_key}}" },
  "parameters": { "type": "object", "properties": { "city": { "type": "string" } } }
}
```

**⚠️ Secret variables** only in headers (not URL/body)

**2025 Features:**
- **transfer-to-human** system tool (Apr 2025)
- **tool_latency_secs** tracking (Apr 2025)

**⚠️ Historical Issue (Fixed Feb 2025):**
Tool calling was broken with `gpt-4o-mini` due to an OpenAI API change. This was fixed in SDK v2.25.0+ (Feb 17, 2025). If using older SDK versions, upgrade to avoid silent tool execution failures on that model.

**Source**: [Changelog Feb 17, 2025](https://elevenlabs.io/docs/changelog/2025/2/17)

### C. MCP Tools (Model Context Protocol)

Connect to MCP servers for databases, IDEs, data sources.

**Configuration:** Dashboard → Add Custom MCP Server → Configure SSE/HTTP endpoint

**Approval Modes:** Always Ask | Fine-Grained | No Approval

**2025 Updates:**
- **disable_interruptions** flag (Oct 2025) - Prevents interruption during tool execution
- **Tools Management Interface** (Jun 2025)

**⚠️ Limitations:** SSE/HTTP only. Not available for Zero Retention or HIPAA.

### D. System Tools

Built-in conversation control (no external APIs):
- `end_call`, `detect_language`, `transfer_agent`
- `transfer_to_number` (telephony)
- `dtmf_playpad`, `voicemail_detection` (telephony)

**2025:** `use_out_of_band_dtmf` flag for telephony integration

---

## 6. SDK Integration

### useConversation Hook (React/React Native)

```typescript
const { startConversation, stopConversation, status, isSpeaking } = useConversation({
  agentId: 'your-agent-id',
  signedUrl: '/api/auth', // OR apiKey: process.env.NEXT_PUBLIC_ELEVENLABS_API_KEY
  clientTools: { /* ... */ },
  onEvent: (event) => { /* transcript, agent_response, tool_call, agent_tool_request (Oct 2025) */ },
  onConnect/onDisconnect/onError,
  serverLocation: 'us' // 'eu-residency' | 'in-residency' | 'global'
});
```

**2025 Events:**
- `agent_chat_response_part` - Streaming responses (Oct 2025)
- `agent_tool_request` - Tool interaction tracking (Oct 2025)

### Connection Types: WebRTC vs WebSocket

| Feature | WebSocket | WebRTC (Jul 2025 rollout) |
|---------|-----------|---------------------------|
| **Auth** | `signedUrl` | `conversationToken` |
| **Audio** | Configurable (16k/24k/48k) | PCM_48000 (hardcoded) |
| **Latency** | Standard | Lower |
| **Best For** | Flexibility | Low-latency |

**⚠️ WebRTC:** Hardcoded PCM_48000, limited device switching

### Platforms

- **React**: `@elevenlabs/react@0.12.3`
- **JavaScript**: `@elevenlabs/client@0.12.2` - `new Conversation({...})`
- **React Native**: `@elevenlabs/react-native@0.5.7` - Expo SDK 47+, iOS/macOS (custom build required, no Expo Go)
- **Swift**: iOS 14.0+, macOS 11.0+, Swift 5.9+
- **Embeddable Widget**: `<script src="https://elevenlabs.io/convai-widget/index.js"></script>`
- **Widget Packages** (Dec 2025):
  - `@elevenlabs/convai-widget-embed@0.5.5` - For embedding in existing apps
  - `@elevenlabs/convai-widget-core@0.5.5` - Core widget functionality

### Scribe (Real-Time Speech-to-Text - Beta 2025)

Real-time transcription with word-level timestamps. **Single-use tokens**, not API keys.

```typescript
const { connect, startRecording, stopRecording, transcript, partialTranscript } = useScribe({
  token: async () => (await fetch('/api/scribe/token')).json().then(d => d.token),
  commitStrategy: 'vad', // 'vad' (auto on silence) | 'manual' (explicit .commit())
  sampleRate: 16000, // 16000 or 24000
  onPartialTranscript/onFinalTranscript/onError
});
```

**Events:** PARTIAL_TRANSCRIPT, FINAL_TRANSCRIPT_WITH_TIMESTAMPS, SESSION_STARTED, ERROR

**⚠️ Closed Beta** - requires sales contact. For agents, use Agents Platform instead (LLM + TTS + two-way interaction).

**⚠️ Webhook Mode Issue:**
Using `speechToText.convert()` with `webhook: true` causes SDK parsing errors. The API returns only `{ request_id }` for webhook mode, but the SDK expects the full transcription schema.

**Error Message:**
```
ParseError: response: Missing required key "language_code"; Missing required key "text"; ...
```

**Workaround** - Use direct fetch API instead of SDK:
```typescript
const formData = new FormData();
formData.append('file', audioFile);
formData.append('model_id', 'scribe_v1');
formData.append('webhook', 'true');
formData.append('webhook_id', webhookId);

const response = await fetch('https://api.elevenlabs.io/v1/speech-to-text', {
  method: 'POST',
  headers: { 'xi-api-key': apiKey },
  body: formData,
});

const result = await response.json(); // { request_id: 'xxx' }
// Actual transcription delivered to webhook endpoint
```

**Source**: [GitHub Issue #232](https://github.com/elevenlabs/elevenlabs-js/issues/232) (confirmed by maintainer)

---

## 7. Testing & Evaluation

### 🆕 Agent Testing Framework (Aug 2025)

Comprehensive automated testing with **9 new API endpoints** for creating, managing, and executing tests.

**Test Types:**
- **Scenario Testing** - LLM-based evaluation against success criteria
- **Tool Call Testing** - Verify correct tool usage and parameters
- **Load Testing** - High-concurrency capacity testing

**CLI Workflow:**
```bash
# Create test
elevenlabs tests add "Refund Test" --template basic-llm

# Configure in test_configs/refund-test.json
{
  "name": "Refund Test",
  "scenario": "Customer requests refund",
  "success_criteria": ["Agent acknowledges empathetically", "Verifies order details"],
  "expected_tool_call": { "tool_name": "lookup_order", "parameters": { "order_id": "..." } }
}

# Deploy and execute
elevenlabs tests push
elevenlabs agents test "Support Agent"
```

**9 New API Endpoints (Aug 2025):**
1. `POST /v1/convai/tests` - Create test
2. `GET /v1/convai/tests/:id` - Retrieve test
3. `PATCH /v1/convai/tests/:id` - Update test
4. `DELETE /v1/convai/tests/:id` - Delete test
5. `POST /v1/convai/tests/:id/execute` - Execute test
6. `GET /v1/convai/test-invocations` - List invocations (pagination, agent filtering)
7. `POST /v1/convai/test-invocations/:id/resubmit` - Resubmit failed test
8. `GET /v1/convai/test-results/:id` - Get results
9. `GET /v1/convai/test-results/:id/debug` - Detailed debugging info

**Test Invocation Listing (Oct 2025):**
```typescript
const invocations = await client.convai.testInvocations.list({
  agent_id: 'agent_123',      // Filter by agent
  page_size: 30,              // Default 30, max 100
  cursor: 'next_page_cursor'  // Pagination
});
// Returns: test run counts, pass/fail stats, titles
```

**Programmatic Testing:**
```typescript
const simulation = await client.agents.simulate({
  agent_id: 'agent_123',
  scenario: 'Refund request',
  user_messages: ["I want a refund", "Order #12345"],
  success_criteria: ["Acknowledges request", "Verifies order"]
});
console.log('Passed:', simulation.passed);
```

**Agent Tracking (Oct 2025):** Tests now include `agent_id` association for better organization

---

## 8. Analytics & Monitoring

**2025 Features:**
- **Custom Dashboard Charts** (Apr 2025) - Display evaluation criteria metrics over time
- **Call History Filtering** (Apr 2025) - `call_start_before_unix` parameter
- **Multi-Voice History** - Separate conversation history by voice
- **LLM Cost Tracking** - Per agent/conversation costs with `aggregation_interval` (hour/day/week/month)
- **Tool Latency** (Apr 2025) - `tool_latency_secs` tracking
- **Usage Metrics** - minutes_used, request_count, ttfb_avg, ttfb_p95

**Conversation Analysis:** Success evaluation (LLM-based), data collection fields, post-call webhooks

**Access:** Dashboard → Analytics | Post-call Webhooks | API

---

## 9. Privacy & Compliance

**Data Retention:** 2 years default (GDPR). Configure: `{ "transcripts": { "retention_days": 730 }, "audio": { "retention_days": 2190 } }`

**Encryption:** TLS 1.3 (transit), AES-256 (rest)

**Regional:** `serverLocation: 'eu-residency' | 'us' | 'global' | 'in-residency'`

**Zero Retention Mode:** Immediate deletion (no history, analytics, webhooks, or MCP)

**Compliance:** GDPR (1-2 years), HIPAA (6 years), SOC 2 (automatic encryption)

---

## 10. Cost Optimization

**LLM Caching:** Up to 90% savings on repeated inputs. `{ "caching": { "enabled": true, "ttl_seconds": 3600 } }`

**Model Swapping:** GPT-5.1, GPT-4o/mini, Claude Sonnet 4.5, Gemini 3 Pro/2.5 Flash (2025 models)

**Burst Pricing:** 3x concurrency limit at 2x cost. `{ "burst_pricing_enabled": true }`

---

## 11. Advanced Features

**2025 Platform Updates:**
- **Azure OpenAI** (Jul 2025) - Custom LLM with Azure-hosted models (requires API version field)
- **Genesys Output Variables** (Jul 2025) - Enhanced call analytics
- **LLMReasoningEffort "none"** (Oct 2025) - Control model reasoning behavior
- **Streaming Voice Previews** (Jul 2025) - Real-time voice generation
- **pcm_48000** audio format (Apr 2025) - New output format support

**Events:** `audio`, `transcript`, `agent_response`, `tool_call`, `agent_chat_response_part` (streaming, Oct 2025), `agent_tool_request` (Oct 2025), `conversation_state`

**Custom Models:** Bring your own LLM (OpenAI-compatible endpoints). `{ "llm_config": { "custom": { "endpoint": "...", "api_key": "{{secret__key}}" } } }`

**Post-Call Webhooks:** HMAC verification required. Return 200 or auto-disable after 10 failures. Payload includes conversation_id, transcript, analysis.

**Chat Mode:** Text-only (no ASR/TTS). `{ "chat_mode": true }`. Saves ~200ms + costs.

**Telephony:** SIP (sip-static.rtc.elevenlabs.io), Twilio native, Vonage, RingCentral. **2025:** Twilio keypad fix (Jul), SIP TLS remote_domains validation (Oct)

---

## 12. CLI & DevOps ("Agents as Code")

**Installation & Auth:**
```bash
npm install -g @elevenlabs/agents-cli@0.6.1
elevenlabs auth login
elevenlabs auth residency eu-residency  # 'in-residency' | 'global'
export ELEVENLABS_API_KEY=your-api-key  # For CI/CD
```

**Project Structure:** `agents.json`, `tools.json`, `tests.json` + `agent_configs/`, `tool_configs/`, `test_configs/`

**Key Commands:**
```bash
elevenlabs agents init
elevenlabs agents add "Bot" --template customer-service
elevenlabs agents push --env prod --dry-run  # Preview
elevenlabs agents push --env prod            # Deploy
elevenlabs agents pull                       # Import existing
elevenlabs agents test "Bot"                 # 2025: Enhanced testing

elevenlabs tools add-webhook "Weather" --config-path tool_configs/weather.json
elevenlabs tools push

elevenlabs tests add "Test" --template basic-llm
elevenlabs tests push
```

**Multi-Environment:** Create `agent.dev.json`, `agent.staging.json`, `agent.prod.json` for overrides

**CI/CD:** GitHub Actions with `--dry-run` validation before deploy

**.gitignore:** `.env`, `.elevenlabs/`, `*.secret.json`

---

## 13. Common Errors & Solutions (27 Documented)

### Error 1: Missing Required Dynamic Variables
**Cause:** Variables referenced in prompts not provided at conversation start
**Solution:** Provide all variables in `dynamic_variables: { user_name: "John", ... }`

### Error 2: Case-Sensitive Tool Names
**Cause:** Tool name mismatch (case-sensitive)
**Solution:** Ensure `tool_ids: ["orderLookup"]` matches `name: "orderLookup"` exactly

### Error 3: Webhook Authentication Failures
**Cause:** Incorrect HMAC signature, not returning 200, or 10+ failures
**Solution:** Verify `hmac = crypto.createHmac('sha256', SECRET).update(payload).digest('hex')` and return 200
**⚠️ Header Name:** Use `ElevenLabs-Signature` (NOT `X-ElevenLabs-Signature` - no X- prefix!)

### Error 4: Voice Consistency Issues
**Cause:** Background noise, inconsistent mic distance, extreme volumes in training
**Solution:** Use clean audio, consistent distance, avoid extremes

### Error 5: Wrong Language Voice
**Cause:** English-trained voice for non-English language
**Solution:** Use language-matched voices: `{ "language": "es", "voice_id": "spanish_voice" }`

### Error 6: Restricted API Keys Not Supported (CLI)
**Cause:** CLI doesn't support restricted API keys
**Solution:** Use unrestricted API key for CLI

### Error 7: Agent Configuration Push Conflicts
**Cause:** Hash-based change detection missed modification
**Solution:** `elevenlabs agents init --override` + `elevenlabs agents pull` + push

### Error 8: Tool Parameter Schema Mismatch
**Cause:** Schema doesn't match usage
**Solution:** Add clear descriptions: `"description": "Order ID (format: ORD-12345)"`

### Error 9: RAG Index Not Ready
**Cause:** Index still computing (takes minutes)
**Solution:** Check `index.status === 'ready'` before using

### Error 10: WebSocket Protocol Error (1002)
**Cause:** Network instability, incompatible browser, or firewall issues
**Symptoms:**
```
Error receiving message: received 1002 (protocol error)
Error sending user audio chunk: received 1002 (protocol error)
WebSocket is already in CLOSING or CLOSED state
```
Connection cycles: Disconnected → Connected → Disconnected rapidly

**Solution:**
1. **Use WebRTC instead of WebSocket** for better stability: `connectionType: 'webrtc'`
2. **Implement reconnection logic** with exponential backoff
3. **Check network stability** and firewall rules (port restrictions)
4. **Test on different networks/browsers** to isolate the issue

**Source**: [GitHub Issue #134](https://github.com/elevenlabs/elevenlabs-examples/issues/134)

### Error 11: 401 Unauthorized in Production
**Cause:** Agent visibility or API key config
**Solution:** Check visibility (public/private), verify API key in prod, check allowlist

### Error 12: Allowlist Connection Errors
**Cause:** Allowlist enabled but using shared link, OR localhost validation bug
**Symptoms:**
```
Host is not supported
Host is not valid or supported
Host is not in insights whitelist
WebSocket is already in CLOSING or CLOSED state
```

**Solution:**
1. Configure allowlist domains in dashboard or disable for testing
2. **Localhost workaround**: Use `127.0.0.1:3000` instead of `localhost:3000`

**⚠️ Localhost Validation Bug:**
The dashboard has inconsistent validation for localhost URLs:
- ❌ `localhost:3000` → Rejected (should be valid)
- ❌ `http://localhost:3000` → Rejected (protocol not allowed)
- ❌ `localhost:3000/voice-chat` → Rejected (paths not allowed)
- ✅ `www.localhost:3000` → Accepted (invalid but accepted!)
- ✅ `127.0.0.1:3000` → Accepted (use this for local dev)

**Source**: [GitHub Issue #320](https://github.com/elevenlabs/elevenlabs-js/issues/320)

### Error 13: Workflow Infinite Loops
**Cause:** Edge conditions creating loops
**Solution:** Add max iteration limits, test all paths, explicit exit conditions

### Error 14: Burst Pricing Not Enabled
**Cause:** Burst not enabled in settings
**Solution:** `{ "call_limits": { "burst_pricing_enabled": true } }`

### Error 15: MCP Server Timeout
**Cause:** MCP server slow/unreachable
**Solution:** Check URL accessible, verify transport (SSE/HTTP), check auth, monitor logs

### Error 16: First Message Cutoff on Android
**Cause:** Android needs time to switch audio mode
**Solution:** `connectionDelay: { android: 3_000, ios: 0 }` (3s for audio routing)

### Error 17: CSP (Content Security Policy) Violations
**Cause:** Strict CSP blocks `blob:` URLs. SDK uses Audio Worklets loaded as blobs
**Solution:** Self-host worklets:
1. `cp node_modules/@elevenlabs/client/dist/worklets/*.js public/elevenlabs/`
2. Configure: `workletPaths: { 'rawAudioProcessor': '/elevenlabs/rawAudioProcessor.worklet.js', 'audioConcatProcessor': '/elevenlabs/audioConcatProcessor.worklet.js' }`
3. Update CSP: `script-src 'self' https://elevenlabs.io; worker-src 'self';`
**Gotcha:** Update worklets when upgrading `@elevenlabs/client`

### Error 18: Webhook Payload - Null Message on Tool Calls
**Cause:** Schema expects `message: string` but ElevenLabs sends `null` when agent makes tool calls
**Solution:** Use `z.string().nullable()` for message field in Zod schemas
```typescript
// ❌ Fails on tool call turns:
message: z.string()

// ✅ Correct:
message: z.string().nullable()
```
**Real payload example:**
```json
{ "role": "agent", "message": null, "tool_calls": [{ "tool_name": "my_tool", ... }] }
```

### Error 19: Webhook Payload - call_successful is String, Not Boolean
**Cause:** Schema expects `call_successful: boolean` but ElevenLabs sends `"success"` or `"failure"` strings
**Solution:** Accept both types and convert for database storage
```typescript
// Schema:
call_successful: z.union([z.boolean(), z.string()]).optional()

// Conversion helper:
function parseCallSuccessful(value: unknown): boolean | undefined {
  if (value === undefined || value === null) return undefined
  if (typeof value === 'boolean') return value
  if (typeof value === 'string') return value.toLowerCase() === 'success'
  return undefined
}
```

### Error 20: Webhook Schema Validation Fails Silently
**Cause:** Real ElevenLabs payloads have many undocumented fields that strict schemas reject
**Undocumented fields in transcript turns:**
- `agent_metadata`, `multivoice_message`, `llm_override`, `rag_retrieval_info`
- `llm_usage`, `interrupted`, `original_message`, `source_medium`
**Solution:** Add all as `.optional()` with `z.any()` for fields you don't process
**Debugging tip:** Use https://webhook.site to capture real payloads, then test schema locally

### Error 21: Webhook Cost Field is Credits, NOT USD
**Cause:** `metadata.cost` contains **ElevenLabs credits**, not USD dollars. Displaying this directly shows wildly wrong values (e.g., "$78.0000" when actual cost is ~$0.003)
**Solution:** Extract actual USD from `metadata.charging.llm_price` instead
```typescript
// ❌ Wrong - displays credits as dollars:
cost: metadata?.cost  // Returns 78 (credits)

// ✅ Correct - actual USD cost:
const charging = metadata?.charging as any
cost: charging?.llm_price ?? null  // Returns 0.0036 (USD)
```
**Real payload structure:**
```json
{
  "metadata": {
    "cost": 78,  // ← CREDITS, not dollars!
    "charging": {
      "llm_price": 0.0036188999999999995,  // ← Actual USD cost
      "llm_charge": 18,   // LLM credits
      "call_charge": 60,  // Audio credits
      "tier": "pro"
    }
  }
}
```
**Note:** `llm_price` only covers LLM costs. Audio costs may require separate calculation based on your plan.

### Error 22: User Context Available But Not Extracted
**Cause:** Webhook contains authenticated user info from widget but code doesn't extract it
**Solution:** Extract `dynamic_variables` from `conversation_initiation_client_data`
```typescript
const dynamicVars = data.conversation_initiation_client_data?.dynamic_variables
const callerName = dynamicVars?.user_name || null
const callerEmail = dynamicVars?.user_email || null
const currentPage = dynamicVars?.current_page || null
```
**Payload example:**
```json
{
  "conversation_initiation_client_data": {
    "dynamic_variables": {
      "user_name": "Jeremy Dawes",
      "user_email": "jeremy@jezweb.net",
      "current_page": "/dashboard/calls"
    }
  }
}
```

### Error 23: Data Collection Results Available But Not Displayed
**Cause:** ElevenLabs agents can collect structured data during calls (configured in agent settings). This data is stored in `analysis.data_collection_results` but often not parsed/displayed in UI.
**Solution:** Parse the JSON and display collected fields with their values and rationales
```typescript
const dataCollectionResults = analysis?.dataCollectionResults
  ? JSON.parse(analysis.dataCollectionResults)
  : null

// Display each collected field:
Object.entries(dataCollectionResults).forEach(([key, data]) => {
  console.log(`${key}: ${data.value} (${data.rationale})`)
})
```
**Payload example:**
```json
{
  "data_collection_results": {
    "customer_name": { "value": "John Smith", "rationale": "Customer stated their name" },
    "intent": { "value": "billing_inquiry", "rationale": "Asking about invoice" },
    "callback_number": { "value": "+61400123456", "rationale": "Provided for callback" }
  }
}
```

### Error 24: Evaluation Criteria Results Available But Not Displayed
**Cause:** Custom success criteria (configured in agent) produce results in `analysis.evaluation_criteria_results` but often not parsed/displayed
**Solution:** Parse and show pass/fail status with rationales
```typescript
const evaluationResults = analysis?.evaluationCriteriaResults
  ? JSON.parse(analysis.evaluationCriteriaResults)
  : null

Object.entries(evaluationResults).forEach(([key, data]) => {
  const passed = data.result === 'success' || data.result === true
  console.log(`${key}: ${passed ? 'PASS' : 'FAIL'} - ${data.rationale}`)
})
```
**Payload example:**
```json
{
  "evaluation_criteria_results": {
    "verified_identity": { "result": "success", "rationale": "Customer verified DOB" },
    "resolved_issue": { "result": "failure", "rationale": "Escalated to human" }
  }
}
```

### Error 25: Feedback Rating Available But Not Extracted
**Cause:** User can provide thumbs up/down feedback. Stored in `metadata.feedback.thumb_rating` but not extracted
**Solution:** Extract and store the rating (1 = thumbs up, -1 = thumbs down)
```typescript
const feedback = metadata?.feedback as any
const feedbackRating = feedback?.thumb_rating ?? null  // 1, -1, or null

// Also available:
const likes = feedback?.likes    // Array of things user liked
const dislikes = feedback?.dislikes  // Array of things user disliked
```
**Payload example:**
```json
{
  "metadata": {
    "feedback": {
      "thumb_rating": 1,
      "likes": ["helpful", "natural"],
      "dislikes": []
    }
  }
}
```

### Error 26: Per-Turn Metadata Not Extracted (interrupted, source_medium, rag_retrieval_info)
**Cause:** Each transcript turn has valuable metadata that's often ignored
**Solution:** Store these fields per message for analytics and debugging
```typescript
const turnAny = turn as any
const messageData = {
  // ... existing fields
  interrupted: turnAny.interrupted ?? null,          // Was turn cut off by user?
  sourceMedium: turnAny.source_medium ?? null,       // Channel: web, phone, etc.
  originalMessage: turnAny.original_message ?? null, // Pre-processed message
  ragRetrievalInfo: turnAny.rag_retrieval_info       // What knowledge was retrieved
    ? JSON.stringify(turnAny.rag_retrieval_info)
    : null,
}
```
**Use cases:**
- `interrupted: true` → User spoke over agent (UX insight)
- `source_medium` → Analytics by channel
- `rag_retrieval_info` → Debug/improve knowledge base retrieval

### Error 27: Upcoming Audio Flags (August 2025)
**Cause:** Three new boolean fields coming in August 2025 webhooks that may break schemas
**Solution:** Add these fields to schemas now (as optional) to be ready
```typescript
// In webhook payload (coming August 15, 2025):
has_audio: boolean        // Was full audio recorded?
has_user_audio: boolean   // Was user audio captured?
has_response_audio: boolean // Was agent audio captured?

// Schema (future-proof):
const schema = z.object({
  // ... existing fields
  has_audio: z.boolean().optional(),
  has_user_audio: z.boolean().optional(),
  has_response_audio: z.boolean().optional(),
})
```
**Note:** These match the existing fields in the GET Conversation API response

### Error 28: Tool Parsing Fails When Tool Not Found
**Cause:** Calling `conversations.get(id)` when conversation contains tool_results where the tool was deleted/not found
**Error Message:**
```
Error: response -> transcript -> [11] -> tool_results -> [0] -> type:
Expected string. Received null.;
response -> transcript -> [11] -> tool_results -> [0] -> type:
[Variant 1] Expected "system". Received null.;
response -> transcript -> [11] -> tool_results -> [0] -> type:
[Variant 2] Expected "workflow". Received null.
```

**Solution:**
1. **SDK fix needed** - SDK should handle null tool_results.type gracefully
2. **Workaround for users:**
   - Ensure all referenced tools exist before deleting them
   - Wrap `conversation.get()` in try-catch until SDK is fixed
   ```typescript
   try {
     const conversation = await client.conversationalAi.conversations.get(id);
   } catch (error) {
     console.error('Tool parsing error - conversation may reference deleted tools');
   }
   ```

**Source**: [GitHub Issue #268](https://github.com/elevenlabs/elevenlabs-js/issues/268)

### Error 29: SDK Parameter Naming Confusion (snake_case vs camelCase)
**Cause:** Using snake_case parameters (from API/Python SDK docs) in JS SDK, which expects camelCase
**Symptoms:** Parameters silently ignored, wrong model/voice used, no error messages

**Common Mistakes:**
```typescript
// ❌ WRONG - parameter ignored:
convert(voiceId, { model_id: "eleven_v3" })

// ✅ CORRECT:
convert(voiceId, { modelId: "eleven_v3" })
```

**Solution:** Always use camelCase for JS SDK parameters. Check TypeScript types if unsure.

**Affected Parameters:** `model_id`, `voice_id`, `output_format`, `voice_settings`, and all API parameters

**Source**: [GitHub Issue #300](https://github.com/elevenlabs/elevenlabs-js/issues/300)

### Error 30: Webhook Mode ParseError with speechToText.convert()
**Cause:** SDK expects full transcription response but webhook mode returns only `{ request_id }`
**Error Message:**
```
ParseError: Missing required key "language_code"; Missing required key "text"; ...
```

**Solution:** Use direct fetch API instead of SDK for webhook mode:
```typescript
const formData = new FormData();
formData.append('file', audioFile);
formData.append('model_id', 'scribe_v1');
formData.append('webhook', 'true');
formData.append('webhook_id', webhookId);

const response = await fetch('https://api.elevenlabs.io/v1/speech-to-text', {
  method: 'POST',
  headers: { 'xi-api-key': apiKey },
  body: formData,
});

const result = await response.json(); // { request_id: 'xxx' }
```

**Source**: [GitHub Issue #232](https://github.com/elevenlabs/elevenlabs-js/issues/232)

### Error 31: Package Not Compatible with Browser/Web
**Cause:** Using `@elevenlabs/elevenlabs-js` in browser/client environments (depends on Node.js `child_process`)
**Error Message:**
```
Module not found: Can't resolve 'child_process'
```

**Affected Frameworks:**
- Next.js client components
- Vite browser builds
- Electron renderer process
- Tauri webview

**Solution:**
1. **For browser/web**: Use `@elevenlabs/client` or `@elevenlabs/react` instead
2. **For full API access in browser**: Create proxy server endpoint using `elevenlabs-js`, call from browser
3. **For Electron/Tauri**: Use `elevenlabs-js` in main process only, not renderer

**Note:** This is by design - `elevenlabs-js` is server-only

**Source**: [GitHub Issue #293](https://github.com/elevenlabs/elevenlabs-js/issues/293)

### Error 32: prompt.tools Deprecated - POST/PATCH Rejected
**Cause:** Using legacy `prompt.tools` array field after July 23, 2025 cutoff
**Error Message:**
```
A request must include either prompt.tool_ids or the legacy prompt.tools array — never both
```

**Solution:** Migrate to new format:
```typescript
// ❌ Old (rejected):
{ agent: { prompt: { tools: [...] } } }

// ✅ New (required):
{
  agent: {
    prompt: {
      tool_ids: ["tool_abc123"],         // Client/server tools
      built_in_tools: ["end_call"]       // System tools
    }
  }
}
```

**Note:** All legacy tools were auto-migrated to standalone records. Just update your configuration references.

**Source**: [Official Migration Guide](https://elevenlabs.io/docs/agents-platform/customization/tools/agent-tools-deprecation)

### Error 33: GPT-4o Mini Tool Calling Broken (Fixed Feb 2025)
**Cause:** OpenAI API breaking change affected `gpt-4o-mini` tool execution (historical issue)
**Symptoms:** Tools silently fail to execute, no error messages
**Solution:** Upgrade to SDK v2.25.0+ (released Feb 17, 2025). If using older SDK versions, upgrade or avoid `gpt-4o-mini` for tool-based workflows.

**Source**: [Changelog Feb 17, 2025](https://elevenlabs.io/docs/changelog/2025/2/17)

### Error 34: Scribe Audio Format Parameter Not Transmitted (Fixed v2.32.0)
**Cause:** WebSocket URI wasn't including `audio_format` parameter even when specified (historical issue)
**Solution:** Upgrade to `@elevenlabs/elevenlabs-js@2.32.0` or later (released Jan 19, 2026)

**Source**: [GitHub PR #319](https://github.com/elevenlabs/elevenlabs-js/pull/319)

---

## Integration with Existing Skills

This skill composes well with:

- **cloudflare-worker-base** → Deploy agents on Cloudflare Workers edge network
- **cloudflare-workers-ai** → Use Cloudflare LLMs as custom models in agents
- **cloudflare-durable-objects** → Persistent conversation state and session management
- **cloudflare-kv** → Cache agent configurations and user preferences
- **nextjs** → React SDK integration in Next.js applications
- **ai-sdk-core** → Vercel AI SDK provider for unified AI interface
- **clerk-auth** → Authenticated voice sessions with user identity
- **hono-routing** → API routes for webhooks and server tools

---

## Additional Resources

**Official Documentation**:
- Platform Overview: https://elevenlabs.io/docs/agents-platform/overview
- API Reference: https://elevenlabs.io/docs/api-reference
- CLI GitHub: https://github.com/elevenlabs/cli

**Examples**:
- Official Examples: https://github.com/elevenlabs/elevenlabs-examples
- MCP Server: https://github.com/elevenlabs/elevenlabs-mcp

**Community**:
- Discord: https://discord.com/invite/elevenlabs
- Twitter: @elevenlabsio

---

**Production Tested**: WordPress Auditor, Customer Support Agents, AgentFlow (webhook integration)
**Last Updated**: 2026-01-21
**Package Versions**: elevenlabs@1.59.0, @elevenlabs/elevenlabs-js@2.32.0, @elevenlabs/agents-cli@0.6.1, @elevenlabs/react@0.12.3, @elevenlabs/client@0.12.2, @elevenlabs/react-native@0.5.7
**Changes**: Added 7 new errors (tool parsing, parameter naming, webhook mode, prompt.tools deprecation, localhost allowlist bug, package compatibility, historical fixes). Expanded WebSocket 1002 and allowlist errors with troubleshooting. Added package selection guide and SDK parameter naming guide. Updated Scribe audio format fix to v2.32.0.
