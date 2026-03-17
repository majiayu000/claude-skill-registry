---
name: elevenlabs-agents
description: |
  Use this skill when building AI voice agents with the ElevenLabs Agents Platform. This skill covers the complete platform including agent configuration (system prompts, turn-taking, workflows), voice & language features (multi-voice, pronunciation, speed control), knowledge base (RAG), tools (client/server/MCP/system), SDKs (React, JavaScript, React Native, Swift, Widget), Scribe (real-time STT), WebRTC/WebSocket connections, testing & evaluation, analytics, privacy/compliance (GDPR/HIPAA/SOC 2), cost optimization, CLI workflows ("agents as code"), and DevOps integration. Prevents 17+ common errors including package deprecation, Android audio cutoff, CSP violations, missing dynamic variables, case-sensitive tool names, webhook authentication failures, and WebRTC configuration issues. Provides production-tested templates for React, Next.js, React Native, Swift, and Cloudflare Workers. Token savings: ~73% (22k → 6k tokens). Production tested.

  Keywords: ElevenLabs Agents, ElevenLabs voice agents, AI voice agents, conversational AI, @elevenlabs/react, @elevenlabs/client, @elevenlabs/react-native, @elevenlabs/elevenlabs-js, @elevenlabs/agents-cli, elevenlabs SDK, voice AI, TTS, text-to-speech, ASR, speech recognition, turn-taking model, WebRTC voice, WebSocket voice, ElevenLabs conversation, agent system prompt, agent tools, agent knowledge base, RAG voice agents, multi-voice agents, pronunciation dictionary, voice speed control, elevenlabs scribe, @11labs deprecated, Android audio cutoff, CSP violation elevenlabs, dynamic variables elevenlabs, case-sensitive tool names, webhook authentication
license: MIT
metadata:
  version: 1.1.0
  last_updated: 2025-11-03
  production_tested: true
  packages:
    - name: "@elevenlabs/elevenlabs-js"
      version: 2.21.0
    - name: "@elevenlabs/agents-cli"
      version: 0.2.0
    - name: "@elevenlabs/react"
      version: 0.9.1
    - name: "@elevenlabs/client"
      version: 0.9.1
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

### 🚨 Package Updates (November 2025)

ElevenLabs migrated to new scoped packages in August 2025:

**DEPRECATED (Do not use):**
- `@11labs/react` → **DEPRECATED**
- `@11labs/client` → **DEPRECATED**

**Current packages:**
```bash
npm install @elevenlabs/react@0.9.1        # React SDK
npm install @elevenlabs/client@0.9.1       # JavaScript SDK
npm install @elevenlabs/react-native@0.5.2 # React Native SDK
npm install @elevenlabs/elevenlabs-js@2.21.0 # Base SDK
npm install -g @elevenlabs/agents-cli@0.2.0  # CLI
```

If you have old packages installed, uninstall them first:
```bash
npm uninstall @11labs/react @11labs/client
```

### When to Use This Skill

Use this skill when:
- Building voice-enabled customer support agents
- Creating interactive voice response (IVR) systems
- Developing conversational AI applications
- Integrating telephony (Twilio, SIP trunking)
- Implementing voice chat in web/mobile apps
- Configuring agents via CLI ("agents as code")
- Setting up RAG/knowledge bases for agents
- Integrating MCP (Model Context Protocol) servers
- Building HIPAA/GDPR-compliant voice systems
- Optimizing LLM costs with caching strategies

### Platform Capabilities

**Design & Configure**:
- Multi-step workflows with visual builder
- System prompt engineering (6-component framework)
- 5000+ voices across 31 languages
- Pronunciation dictionaries (IPA/CMU formats)
- Speed control (0.7x-1.2x)
- RAG-powered knowledge bases
- Dynamic variables and personalization

**Connect & Deploy**:
- React SDK (`@elevenlabs/react`)
- JavaScript SDK (`@elevenlabs/client`)
- React Native SDK (`@elevenlabs/react-native`)
- Swift SDK (iOS/macOS)
- Embeddable widget
- Telephony integration (Twilio, SIP)
- Scribe (Real-Time Speech-to-Text) - Beta

**Operate & Optimize**:
- Automated testing (scenario, tool call, load)
- Conversation analysis and evaluation
- Analytics dashboard (resolution rates, sentiment, compliance)
- Privacy controls (GDPR, HIPAA, SOC 2)
- Cost optimization (LLM caching, model swapping, burst pricing)
- CLI for "agents as code" workflow

---

## 1. Quick Start (3 Integration Paths)

### Path A: React SDK (Embedded Voice Chat)

For building voice chat interfaces in React applications.

**Installation**:
```bash
npm install @elevenlabs/react zod
```

**Basic Example**:
```typescript
import { useConversation } from '@elevenlabs/react';
import { z } from 'zod';

export default function VoiceChat() {
  const { startConversation, stopConversation, status } = useConversation({
    // Public agent (no API key needed)
    agentId: 'your-agent-id',

    // OR private agent (requires API key)
    apiKey: process.env.NEXT_PUBLIC_ELEVENLABS_API_KEY,

    // OR signed URL (server-generated, most secure)
    signedUrl: '/api/elevenlabs/auth',

    // Client-side tools (browser functions)
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
    onConnect: () => console.log('Connected'),
    onDisconnect: () => console.log('Disconnected'),
    onEvent: (event) => {
      switch (event.type) {
        case 'transcript':
          console.log('User said:', event.data.text);
          break;
        case 'agent_response':
          console.log('Agent replied:', event.data.text);
          break;
      }
    },

    // Regional compliance (GDPR, data residency)
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

### Path B: CLI ("Agents as Code")

For managing agents via code with version control and CI/CD.

**Installation**:
```bash
npm install -g @elevenlabs/agents-cli
# or
pnpm install -g @elevenlabs/agents-cli
```

**Workflow**:
```bash
# 1. Authenticate
elevenlabs auth login

# 2. Initialize project (creates agents.json, tools.json, tests.json)
elevenlabs agents init

# 3. Create agent from template
elevenlabs agents add "Support Agent" --template customer-service

# 4. Configure in agent_configs/support-agent.json

# 5. Push to platform
elevenlabs agents push --env dev

# 6. Test
elevenlabs agents test "Support Agent"

# 7. Deploy to production
elevenlabs agents push --env prod
```

**Project Structure Created**:
```
your_project/
├── agents.json              # Agent registry
├── tools.json               # Tool configurations
├── tests.json               # Test configurations
├── agent_configs/           # Individual agent files
├── tool_configs/            # Tool configuration files
└── test_configs/            # Test configuration files
```

### Path C: API (Programmatic Agent Management)

For creating agents dynamically (multi-tenant, SaaS platforms).

**Installation**:
```bash
npm install elevenlabs
```

**Example**:
```typescript
import { ElevenLabsClient } from 'elevenlabs';

const client = new ElevenLabsClient({
  apiKey: process.env.ELEVENLABS_API_KEY
});

// Create agent
const agent = await client.agents.create({
  name: 'Support Bot',
  conversation_config: {
    agent: {
      prompt: {
        prompt: "You are a helpful customer support agent.",
        llm: "gpt-4o",
        temperature: 0.7
      },
      first_message: "Hello! How can I help you today?",
      language: "en"
    },
    tts: {
      model_id: "eleven_turbo_v2_5",
      voice_id: "your-voice-id"
    }
  }
});

console.log('Agent created:', agent.agent_id);
```

---

## 2. Agent Configuration

### System Prompt Architecture (6 Components)

ElevenLabs recommends structuring agent prompts using 6 components:

#### 1. Personality
Define the agent's identity, role, and character traits.

**Example**:
```
You are Alex, a friendly and knowledgeable customer support specialist at TechCorp.
You have 5 years of experience helping customers solve technical issues.
You're patient, empathetic, and always maintain a positive attitude.
```

#### 2. Environment
Describe the communication context (phone, web chat, video call).

**Example**:
```
You're speaking with customers over the phone. Communication is voice-only.
Customers may have background noise or poor connection quality.
Speak clearly and occasionally use thoughtful pauses for emphasis.
```

#### 3. Tone
Specify formality, speech patterns, humor, and verbosity.

**Example**:
```
Tone: Professional yet warm. Use contractions ("I'm" instead of "I am") to sound natural.
Avoid jargon unless the customer uses it first. Keep responses concise (2-3 sentences max).
Use encouraging phrases like "I'll be happy to help with that" and "Let's get this sorted for you."
```

#### 4. Goal
Define objectives and success criteria.

**Example**:
```
Primary Goal: Resolve customer technical issues on the first call.
Secondary Goals:
- Verify customer identity securely
- Document issue details accurately
- Offer proactive solutions
- End calls with confirmation that the issue is resolved

Success Criteria: Customer verbally confirms their issue is resolved.
```

#### 5. Guardrails
Set boundaries, prohibited topics, and ethical constraints.

**Example**:
```
Guardrails:
- Never provide medical, legal, or financial advice
- Do not share confidential company information
- If asked about competitors, politely redirect to TechCorp's offerings
- Escalate to a human supervisor if customer becomes abusive
- Never make promises about refunds or credits without verification
```

#### 6. Tools
Describe available external capabilities and when to use them.

**Example**:
```
Available Tools:
1. lookup_order(order_id) - Fetch order details from database. Use when customer mentions an order number.
2. transfer_to_supervisor() - Escalate to human agent. Use when issue requires manager approval.
3. send_password_reset(email) - Trigger password reset email. Use when customer can't access account.

Always explain to the customer what you're doing before calling a tool.
```

**Complete Template**:
```json
{
  "agent": {
    "prompt": {
      "prompt": "Personality:\nYou are Alex, a friendly customer support specialist.\n\nEnvironment:\nYou're speaking with customers over the phone.\n\nTone:\nProfessional yet warm. Keep responses concise.\n\nGoal:\nResolve technical issues on the first call.\n\nGuardrails:\n- Never provide medical/legal/financial advice\n- Escalate abusive customers\n\nTools:\n- lookup_order(order_id) - Fetch order details\n- transfer_to_supervisor() - Escalate to human",
      "llm": "gpt-4o",
      "temperature": 0.7,
      "max_tokens": 500
    }
  }
}
```

### Turn-Taking Modes

Controls when the agent interrupts or waits for the user to finish speaking.

**3 Modes**:

| Mode | Behavior | Best For |
|------|----------|----------|
| **Eager** | Responds quickly, jumps in at earliest opportunity | Fast-paced support, quick orders |
| **Normal** | Balanced, waits for natural conversation breaks | General customer service (default) |
| **Patient** | Waits longer, allows detailed user responses | Information collection, therapy, tutoring |

**Configuration**:
```json
{
  "conversation_config": {
    "turn": {
      "mode": "patient" // "eager" | "normal" | "patient"
    }
  }
}
```

**Use Cases**:
- **Eager**: Fast food ordering, quick FAQs, urgent notifications
- **Normal**: General support, product inquiries, appointment booking
- **Patient**: Detailed form filling, emotional support, educational tutoring

**Gotchas**:
- Eager mode can feel interruptive to some users
- Patient mode may feel slow in fast-paced contexts
- Can be dynamically adjusted in workflows for context-aware behavior

### Workflows (Visual Builder)

Create branching conversation flows with subagent nodes and conditional routing.

**Node Types**:
1. **Subagent Nodes** - Override base agent config (change prompt, voice, turn-taking)
2. **Tool Nodes** - Guarantee tool execution (unlike tools in subagents)

**Configuration**:
```json
{
  "workflow": {
    "nodes": [
      {
        "id": "node_1",
        "type": "subagent",
        "config": {
          "system_prompt": "You are now a technical support specialist. Ask detailed diagnostic questions.",
          "turn_eagerness": "patient",
          "voice_id": "tech_support_voice_id"
        }
      },
      {
        "id": "node_2",
        "type": "tool",
        "tool_name": "transfer_to_human"
      }
    ],
    "edges": [
      {
        "from": "node_1",
        "to": "node_2",
        "condition": "user_requests_escalation"
      }
    ]
  }
}
```

**Use Cases**:
- Multi-department routing (sales → support → billing)
- Decision trees ("press 1 for sales, 2 for support")
- Role-playing scenarios (customer vs agent voices)
- Escalation paths (bot → human transfer)

**Gotchas**:
- Workflows add ~100-200ms latency per node transition
- Tool nodes guarantee execution (subagents may skip tools)
- Edges can create infinite loops if not tested properly

### Dynamic Variables & Personalization

Inject runtime data into prompts, first messages, and tool parameters using `{{var_name}}` syntax.

**System Variables (Auto-Available)**:
```typescript
{{system__agent_id}}         // Current agent ID
{{system__conversation_id}}  // Conversation ID
{{system__caller_id}}        // Phone number (telephony only)
{{system__called_number}}    // Called number (telephony only)
{{system__call_duration_secs}} // Call duration
{{system__time_utc}}         // Current UTC time
{{system__call_sid}}         // Twilio call SID (Twilio only)
```

**Custom Variables**:
```typescript
// Provide when starting conversation
const conversation = await client.conversations.create({
  agent_id: "agent_123",
  dynamic_variables: {
    user_name: "John",
    account_tier: "premium",
    order_id: "ORD-12345"
  }
});
```

**Secret Variables** (For API Keys):
```
{{secret__stripe_api_key}}
{{secret__database_password}}
```

**Important**: Secret variables only used in headers, never sent to LLM providers.

**Usage in Prompts**:
```json
{
  "agent": {
    "prompt": {
      "prompt": "You are helping {{user_name}}, a {{account_tier}} customer."
    },
    "first_message": "Hello {{user_name}}! I see you're calling about order {{order_id}}."
  }
}
```

**Gotcha**: Missing variables cause "Missing required dynamic variables" error. Always provide all referenced variables when starting conversation.

### Authentication Patterns

**Option 1: Public Agents** (No API Key)
```typescript
const { startConversation } = useConversation({
  agentId: 'your-public-agent-id' // Anyone can use
});
```

**Option 2: Private Agents with API Key**
```typescript
const { startConversation } = useConversation({
  agentId: 'your-private-agent-id',
  apiKey: process.env.NEXT_PUBLIC_ELEVENLABS_API_KEY
});
```

**⚠️ Warning**: Never expose API keys in client-side code. Use signed URLs instead.

**Option 3: Signed URLs (Recommended for Production)**
```typescript
// Server-side (Next.js API route)
import { ElevenLabsClient } from 'elevenlabs';

export async function POST(req: Request) {
  const client = new ElevenLabsClient({
    apiKey: process.env.ELEVENLABS_API_KEY // Server-side only
  });

  const signedUrl = await client.convai.getSignedUrl({
    agent_id: 'your-agent-id'
  });

  return Response.json({ signedUrl });
}

// Client-side
const { startConversation } = useConversation({
  agentId: 'your-agent-id',
  signedUrl: await fetch('/api/elevenlabs/auth').then(r => r.json()).then(d => d.signedUrl)
});
```

---

## 3. Voice & Language Features

### Multi-Voice Support

Dynamically switch between different voices during a single conversation.

**Use Cases**:
- Multi-character storytelling (different voice per character)
- Language tutoring (native speaker voices for each language)
- Role-playing scenarios (customer vs agent)
- Emotional agents (different voices for different moods)

**Configuration**:
```json
{
  "agent": {
    "prompt": {
      "prompt": "When speaking as the customer, use voice_id 'customer_voice_abc123'. When speaking as the agent, use voice_id 'agent_voice_def456'."
    }
  }
}
```

**Gotchas**:
- Voice switching adds ~200ms latency per switch
- Requires careful prompt engineering to trigger switches correctly
- Not all voices work equally well for all characters

### Pronunciation Dictionary

Customize how the agent pronounces specific words or phrases.

**Supported Formats**:
- **IPA** (International Phonetic Alphabet)
- **CMU** (Carnegie Mellon University Pronouncing Dictionary)
- **Word Substitutions** (replace words before TTS)

**Configuration**:
```json
{
  "pronunciation_dictionary": [
    {
      "word": "ElevenLabs",
      "pronunciation": "ɪˈlɛvənlæbz",
      "format": "ipa"
    },
    {
      "word": "API",
      "pronunciation": "ey-pee-ay",
      "format": "cmu"
    },
    {
      "word": "AI",
      "substitution": "artificial intelligence"
    }
  ]
}
```

**Use Cases**:
- Brand names (e.g., "IKEA" → "ee-KAY-uh")
- Acronyms (e.g., "API" → "A-P-I" or "ay-pee-eye")
- Technical terms
- Character names in storytelling

**Gotcha**: Only Turbo v2/v2.5 models support phoneme-based pronunciation. Other models silently skip phoneme entries but still process word substitutions.

### Speed Control

Adjust speaking speed dynamically (0.7x - 1.2x).

**Configuration**:
```json
{
  "voice_settings": {
    "speed": 1.0 // 0.7 = slow, 1.0 = normal, 1.2 = fast
  }
}
```

**Use Cases**:
- **Slow (0.7x-0.9x)**: Accessibility, children, non-native speakers
- **Normal (1.0x)**: Default for most use cases
- **Fast (1.1x-1.2x)**: Urgent notifications, power users

**Best Practices**:
- Use 0.9x-1.1x for natural-sounding adjustments
- Extreme values (below 0.7 or above 1.2) degrade quality
- Speed can be adjusted per agent, not per utterance

### Voice Design

Create custom voices using ElevenLabs Voice Design tool.

**Workflow**:
1. Navigate to Voice Library → Create Voice
2. Use Voice Design (text-to-voice) or Voice Cloning (sample audio)
3. Test voice with sample text
4. Save voice to library
5. Use `voice_id` in agent configuration

**Voice Cloning Best Practices**:
- Use clean audio samples (no background noise, music, or pops)
- Maintain consistent microphone distance
- Avoid extreme volumes (whispering or shouting)
- 1-2 minutes of audio recommended

**Gotcha**: Using English-trained voices for non-English languages causes pronunciation issues. Always use language-matched voices.

### Language Configuration

Support for 32+ languages with automatic detection and in-conversation switching.

**Configuration**:
```json
{
  "agent": {
    "language": "en" // ISO 639-1 code
  }
}
```

**Multi-Language Presets** (Different Voice Per Language):
```json
{
  "conversation_config": {
    "language_presets": [
      {
        "language": "en",
        "voice_id": "en_voice_id",
        "first_message": "Hello! How can I help you today?"
      },
      {
        "language": "es",
        "voice_id": "es_voice_id",
        "first_message": "¡Hola! ¿Cómo puedo ayudarte hoy?"
      },
      {
        "language": "fr",
        "voice_id": "fr_voice_id",
        "first_message": "Bonjour! Comment puis-je vous aider aujourd'hui?"
      }
    ]
  }
}
```

**Automatic Language Detection**: Agent detects user's language and switches automatically.

**Supported Languages**: English, Spanish, French, German, Italian, Portuguese, Dutch, Polish, Arabic, Chinese, Japanese, Korean, Hindi, and 18+ more.

---

## 4. Knowledge Base & RAG

### RAG (Retrieval-Augmented Generation)

Enable agents to access large knowledge bases without loading entire documents into context.

**How It Works**:
1. Upload documents (PDF, TXT, DOCX) to knowledge base
2. ElevenLabs automatically computes vector embeddings
3. During conversation, relevant chunks retrieved based on semantic similarity
4. LLM uses retrieved context to generate responses

**Configuration**:
```json
{
  "agent": {
    "prompt": {
      "knowledge_base": ["doc_id_1", "doc_id_2"]
    }
  }
}
```

**Upload Documents via API**:
```typescript
import { ElevenLabsClient } from 'elevenlabs';

const client = new ElevenLabsClient({ apiKey: process.env.ELEVENLABS_API_KEY });

// Upload document
const doc = await client.knowledgeBase.upload({
  file: fs.createReadStream('support_docs.pdf'),
  name: 'Support Documentation'
});

// Compute RAG index
await client.knowledgeBase.computeRagIndex({
  document_id: doc.id,
  embedding_model: 'e5_mistral_7b' // or 'multilingual_e5_large'
});
```

**Retrieval Configuration**:
```json
{
  "knowledge_base_config": {
    "max_chunks": 5,              // Number of chunks to retrieve
    "vector_distance_threshold": 0.8  // Similarity threshold
  }
}
```

**Use Cases**:
- Product documentation agents
- Customer support (FAQ, help center)
- Educational tutors (textbooks, lecture notes)
- Healthcare assistants (medical guidelines)

**Gotchas**:
- RAG adds ~500ms latency per query
- More chunks = higher cost but better context
- Higher vector distance = more context but potentially less relevant
- Documents must be indexed before use (can take minutes for large docs)

---

## 5. Tools (4 Types)

ElevenLabs supports 4 distinct tool types, each with different execution patterns.

### A. Client Tools

Execute operations on the client side (browser or mobile app).

**Use Cases**:
- Update UI elements (shopping cart, notifications)
- Trigger navigation (redirect user to page)
- Access local storage
- Control media playback

**React Example**:
```typescript
import { useConversation } from '@elevenlabs/react';
import { z } from 'zod';

const { startConversation } = useConversation({
  clientTools: {
    updateCart: {
      description: "Update the shopping cart with new items",
      parameters: z.object({
        item: z.string().describe("The item name"),
        quantity: z.number().describe("Quantity to add")
      }),
      handler: async ({ item, quantity }) => {
        // Client-side logic
        const cart = getCart();
        cart.add(item, quantity);
        updateUI(cart);
        return { success: true, total: cart.total };
      }
    },
    navigate: {
      description: "Navigate to a different page",
      parameters: z.object({
        url: z.string().describe("The URL to navigate to")
      }),
      handler: async ({ url }) => {
        window.location.href = url;
        return { success: true };
      }
    }
  }
});
```

**Gotchas**:
- Tool names are **case-sensitive**
- Must return a value (agent reads the return value)
- Handler can be async

### B. Server Tools (Webhooks)

Make HTTP requests to external APIs from ElevenLabs servers.

**Use Cases**:
- Fetch real-time data (weather, stock prices)
- Update CRM systems (Salesforce, HubSpot)
- Process payments (Stripe, PayPal)
- Send emails/SMS (SendGrid, Twilio)

**Configuration via CLI**:
```bash
elevenlabs tools add-webhook "Get Weather" --config-path tool_configs/get-weather.json
```

**tool_configs/get-weather.json**:
```json
{
  "name": "get_weather",
  "description": "Fetch current weather for a city",
  "url": "https://api.weather.com/v1/current",
  "method": "GET",
  "parameters": {
    "type": "object",
    "properties": {
      "city": {
        "type": "string",
        "description": "The city name (e.g., 'London', 'New York')"
      }
    },
    "required": ["city"]
  },
  "headers": {
    "Authorization": "Bearer {{secret__weather_api_key}}"
  }
}
```

**Dynamic Variables in Tools**:
```json
{
  "url": "https://api.crm.com/customers/{{user_id}}",
  "headers": {
    "X-API-Key": "{{secret__crm_api_key}}"
  }
}
```

**Gotchas**:
- Secret variables only work in headers (not URL or body)
- Schema description guides LLM on when to use tool

### C. MCP Tools (Model Context Protocol)

Connect to external MCP servers for standardized tool access.

**Use Cases**:
- Access databases (PostgreSQL, MongoDB)
- Query knowledge bases (Pinecone, Weaviate)
- Integrate with IDEs (VS Code, Cursor)
- Connect to data sources (Google Drive, Notion)

**Configuration**:
1. Navigate to MCP server integrations in dashboard
2. Click "Add Custom MCP Server"
3. Configure:
   - **Name**: Server identifier
   - **Server URL**: SSE or HTTP endpoint
   - **Secret Token**: Optional auth header
4. Test connectivity and discover tools
5. Add to agents (public or private)

**Approval Modes**:
- **Always Ask**: Maximum security, requires permission per tool call
- **Fine-Grained**: Per-tool approval settings
- **No Approval**: Auto-execute all tools

**Gotchas**:
- Only SSE and HTTP streamable transport supported
- MCP servers must be publicly accessible or behind auth
- Not available for Zero Retention Mode
- Not compatible with HIPAA compliance

**Example: Using ElevenLabs MCP Server in Claude Desktop**:
```json
{
  "mcpServers": {
    "ElevenLabs": {
      "command": "uvx",
      "args": ["elevenlabs-mcp"],
      "env": {
        "ELEVENLABS_API_KEY": "<your-key>",
        "ELEVENLABS_MCP_OUTPUT_MODE": "files"
      }
    }
  }
}
```

### D. System Tools

Modify the internal state of the conversation without external calls.

**Use Cases**:
- Update conversation context
- Switch between workflow nodes
- Modify agent behavior mid-conversation
- Track conversation state

**Built-in System Tools**:
- `end_call` - End the conversation
- `detect_language` - Detect user's language
- `transfer_agent` - Switch to different agent/workflow node
- `transfer_to_number` - Transfer to external phone number (telephony only)
- `dtmf_playpad` - Display DTMF keypad (telephony only)
- `voicemail_detection` - Detect voicemail (telephony only)

**Configuration**:
```json
{
  "system_tools": [
    {
      "name": "update_conversation_state",
      "description": "Update the conversation context with new information",
      "parameters": {
        "key": { "type": "string" },
        "value": { "type": "string" }
      }
    }
  ]
}
```

**Gotchas**:
- System tools don't trigger external APIs
- Changes are ephemeral (lost after conversation ends)
- Useful for workflows and state management

---

## 6. SDK Integration

### React SDK (`@elevenlabs/react`)

**Installation**:
```bash
npm install @elevenlabs/react zod
```

**Complete Example**:
```typescript
import { useConversation } from '@elevenlabs/react';
import { z } from 'zod';
import { useState } from 'react';

export default function VoiceAgent() {
  const [transcript, setTranscript] = useState<string[]>([]);

  const {
    startConversation,
    stopConversation,
    status,
    isSpeaking
  } = useConversation({
    agentId: 'your-agent-id',

    // Authentication (choose one)
    apiKey: process.env.NEXT_PUBLIC_ELEVENLABS_API_KEY,

    // Client tools
    clientTools: {
      updateCart: {
        description: "Update shopping cart",
        parameters: z.object({
          item: z.string(),
          quantity: z.number()
        }),
        handler: async ({ item, quantity }) => {
          console.log('Cart updated:', item, quantity);
          return { success: true };
        }
      }
    },

    // Events
    onConnect: () => {
      console.log('Connected to agent');
      setTranscript([]);
    },
    onDisconnect: () => console.log('Disconnected'),
    onEvent: (event) => {
      if (event.type === 'transcript') {
        setTranscript(prev => [...prev, `User: ${event.data.text}`]);
      } else if (event.type === 'agent_response') {
        setTranscript(prev => [...prev, `Agent: ${event.data.text}`]);
      }
    },
    onError: (error) => console.error('Error:', error),

    // Regional compliance
    serverLocation: 'us'
  });

  return (
    <div>
      <div>
        <button onClick={startConversation} disabled={status === 'connected'}>
          Start Conversation
        </button>
        <button onClick={stopConversation} disabled={status !== 'connected'}>
          Stop
        </button>
      </div>

      <div>Status: {status}</div>
      <div>{isSpeaking && 'Agent is speaking...'}</div>

      <div>
        <h3>Transcript</h3>
        {transcript.map((line, i) => (
          <p key={i}>{line}</p>
        ))}
      </div>
    </div>
  );
}
```

### JavaScript SDK (`@elevenlabs/client`)

For vanilla JavaScript projects (no React).

**Installation**:
```bash
npm install @elevenlabs/client
```

**Example**:
```javascript
import { Conversation } from '@elevenlabs/client';

const conversation = new Conversation({
  agentId: 'your-agent-id',
  apiKey: process.env.ELEVENLABS_API_KEY,

  onConnect: () => console.log('Connected'),
  onDisconnect: () => console.log('Disconnected'),

  onEvent: (event) => {
    switch (event.type) {
      case 'transcript':
        document.getElementById('user-text').textContent = event.data.text;
        break;
      case 'agent_response':
        document.getElementById('agent-text').textContent = event.data.text;
        break;
    }
  }
});

// Start conversation
document.getElementById('start-btn').addEventListener('click', async () => {
  await conversation.start();
});

// Stop conversation
document.getElementById('stop-btn').addEventListener('click', async () => {
  await conversation.stop();
});
```

### Connection Types: WebRTC vs WebSocket

ElevenLabs SDKs support two connection types with different characteristics.

**Comparison Table**:

| Feature | WebSocket | WebRTC |
|---------|-----------|--------|
| **Authentication** | `signedUrl` | `conversationToken` |
| **Audio Format** | Configurable | PCM_48000 (hardcoded) |
| **Sample Rate** | Configurable (16k, 24k, 48k) | 48000 (hardcoded) |
| **Latency** | Standard | Lower |
| **Device Switching** | Flexible | Limited (format locked) |
| **Best For** | General use, flexibility | Low-latency requirements |

**WebSocket Configuration** (default):

```typescript
import { useConversation } from '@elevenlabs/react';

const { startConversation } = useConversation({
  agentId: 'your-agent-id',

  // WebSocket uses signed URL
  signedUrl: async () => {
    const response = await fetch('/api/elevenlabs/auth');
    const { signedUrl } = await response.json();
    return signedUrl;
  },

  // Connection type (optional, defaults to 'websocket')
  connectionType: 'websocket',

  // Audio config (flexible)
  audioConfig: {
    sampleRate: 24000, // 16000, 24000, or 48000
    format: 'PCM_24000'
  }
});
```

**WebRTC Configuration**:

```typescript
const { startConversation } = useConversation({
  agentId: 'your-agent-id',

  // WebRTC uses conversation token (different auth flow)
  conversationToken: async () => {
    const response = await fetch('/api/elevenlabs/token');
    const { token } = await response.json();
    return token;
  },

  // Connection type
  connectionType: 'webrtc',

  // Audio format is HARDCODED to PCM_48000 (not configurable)
  // audioConfig ignored for WebRTC
});
```

**Backend Token Endpoints**:

```typescript
// WebSocket signed URL (GET /v1/convai/conversation/get-signed-url)
app.get('/api/elevenlabs/auth', async (req, res) => {
  const response = await fetch(
    `https://api.elevenlabs.io/v1/convai/conversation/get-signed-url?agent_id=${AGENT_ID}`,
    { headers: { 'xi-api-key': ELEVENLABS_API_KEY } }
  );
  const { signed_url } = await response.json();
  res.json({ signedUrl: signed_url });
});

// WebRTC conversation token (GET /v1/convai/conversation/token)
app.get('/api/elevenlabs/token', async (req, res) => {
  const response = await fetch(
    `https://api.elevenlabs.io/v1/convai/conversation/token?agent_id=${AGENT_ID}`,
    { headers: { 'xi-api-key': ELEVENLABS_API_KEY } }
  );
  const { conversation_token } = await response.json();
  res.json({ token: conversation_token });
});
```

**When to Use Each**:

| Use WebSocket When | Use WebRTC When |
|--------------------|-----------------|
| Need flexible audio formats | Need lowest possible latency |
| Switching between audio devices frequently | Audio format can be locked to 48kHz |
| Standard latency is acceptable | Building real-time applications |
| Need maximum configuration control | Performance is critical |

**Gotchas**:
- WebRTC hardcodes PCM_48000 - no way to change format
- Device switching in WebRTC limited by fixed format
- Different authentication methods (signedUrl vs conversationToken)
- WebRTC may have better performance but less flexibility

### React Native SDK (Expo)

**Installation**:
```bash
npx expo install @elevenlabs/react-native @livekit/react-native @livekit/react-native-webrtc livekit-client
```

**Requirements**:
- Expo SDK 47+
- iOS 14.0+ / macOS 11.0+
- **Custom dev build required** (Expo Go not supported)

**Example**:
```typescript
import { useConversation } from '@elevenlabs/react-native';
import { View, Button, Text } from 'react-native';
import { z } from 'zod';

export default function App() {
  const { startConversation, stopConversation, status } = useConversation({
    agentId: 'your-agent-id',
    signedUrl: 'https://api.elevenlabs.io/v1/convai/auth/...',

    clientTools: {
      updateProfile: {
        description: "Update user profile",
        parameters: z.object({
          name: z.string()
        }),
        handler: async ({ name }) => {
          console.log('Updating profile:', name);
          return { success: true };
        }
      }
    }
  });

  return (
    <View style={{ padding: 20 }}>
      <Button title="Start" onPress={startConversation} />
      <Button title="Stop" onPress={stopConversation} />
      <Text>Status: {status}</Text>
    </View>
  );
}
```

**Gotchas**:
- Requires custom dev build (not Expo Go)
- iOS/macOS only (Android support via Kotlin SDK, not yet officially released)

### Swift SDK (iOS/macOS)

**Installation** (Swift Package Manager):
```swift
dependencies: [
  .package(url: "https://github.com/elevenlabs/elevenlabs-swift-sdk", from: "1.0.0")
]
```

**Requirements**:
- iOS 14.0+ / macOS 11.0+
- Swift 5.9+

**Use Cases**:
- Native iOS apps
- macOS applications
- watchOS (with limitations)

### Widget (Embeddable Web Component)

**Installation**:
Copy-paste embed code from dashboard or use this template:

```html
<script src="https://elevenlabs.io/convai-widget/index.js"></script>
<script>
  ElevenLabsWidget.init({
    agentId: 'your-agent-id',

    // Theming
    theme: {
      primaryColor: '#3B82F6',
      backgroundColor: '#1F2937',
      textColor: '#F9FAFB'
    },

    // Position
    position: 'bottom-right', // 'bottom-left' | 'bottom-right'

    // Custom branding
    branding: {
      logo: 'https://example.com/logo.png',
      name: 'Support Agent'
    }
  });
</script>
```

**Use Cases**:
- Customer support chat bubbles
- Website assistants
- Lead capture forms

### Scribe (Real-Time Speech-to-Text)

**Status**: Closed Beta (requires sales contact)
**Release**: 2025

Scribe is ElevenLabs' real-time speech-to-text service for low-latency transcription.

**Capabilities**:
- Microphone streaming (real-time transcription)
- Pre-recorded audio file transcription
- Partial (interim) and final transcripts
- Word-level timestamps
- Voice Activity Detection (VAD)
- Manual and automatic commit strategies
- Language detection
- PCM_16000 and PCM_24000 audio formats

**Authentication**:
Uses single-use tokens (not API keys):

```typescript
// Fetch token from backend
const response = await fetch('/api/scribe/token');
const { token } = await response.json();

// Backend endpoint
const token = await client.scribe.getToken();
return { token };
```

**React Hook (`useScribe`)**:

```typescript
import { useScribe } from '@elevenlabs/react';

export default function Transcription() {
  const {
    connect,
    disconnect,
    startRecording,
    stopRecording,
    status,
    transcript,
    partialTranscript
  } = useScribe({
    token: async () => {
      const response = await fetch('/api/scribe/token');
      const { token } = await response.json();
      return token;
    },

    // Commit strategy
    commitStrategy: 'vad', // 'vad' (automatic) or 'manual'

    // Audio format
    sampleRate: 16000, // 16000 or 24000

    // Events
    onConnect: () => console.log('Connected to Scribe'),
    onDisconnect: () => console.log('Disconnected'),

    onPartialTranscript: (text) => {
      console.log('Interim:', text);
    },

    onFinalTranscript: (text, timestamps) => {
      console.log('Final:', text);
      console.log('Timestamps:', timestamps); // Word-level timing
    },

    onError: (error) => console.error('Error:', error)
  });

  return (
    <div>
      <button onClick={connect}>Connect</button>
      <button onClick={startRecording}>Start Recording</button>
      <button onClick={stopRecording}>Stop Recording</button>
      <button onClick={disconnect}>Disconnect</button>

      <p>Status: {status}</p>
      <p>Partial: {partialTranscript}</p>
      <p>Final: {transcript}</p>
    </div>
  );
}
```

**JavaScript SDK (`Scribe.connect`)**:

```javascript
import { Scribe } from '@elevenlabs/client';

const connection = await Scribe.connect({
  token: 'your-single-use-token',

  sampleRate: 16000,
  commitStrategy: 'vad',

  onPartialTranscript: (text) => {
    document.getElementById('interim').textContent = text;
  },

  onFinalTranscript: (text, timestamps) => {
    const finalDiv = document.getElementById('final');
    finalDiv.textContent += text + ' ';

    // timestamps: [{ word: 'hello', start: 0.5, end: 0.8 }, ...]
  },

  onError: (error) => {
    console.error('Scribe error:', error);
  }
});

// Start recording from microphone
await connection.startRecording();

// Stop recording
await connection.stopRecording();

// Manual commit (if commitStrategy: 'manual')
await connection.commit();

// Disconnect
await connection.disconnect();
```

**Transcribing Pre-Recorded Files**:

```typescript
import { Scribe } from '@elevenlabs/client';

const connection = await Scribe.connect({ token });

// Send audio buffer
const audioBuffer = fs.readFileSync('recording.pcm');
await connection.sendAudioData(audioBuffer);

// Manually commit to get final transcript
await connection.commit();

// Wait for final transcript event
```

**Event Types**:
- `SESSION_STARTED`: Connection established
- `PARTIAL_TRANSCRIPT`: Interim transcription (unbuffered)
- `FINAL_TRANSCRIPT`: Complete sentence/phrase
- `FINAL_TRANSCRIPT_WITH_TIMESTAMPS`: Final + word timing
- `ERROR`: Transcription error
- `AUTH_ERROR`: Authentication failed
- `OPEN`: WebSocket opened
- `CLOSE`: WebSocket closed

**Commit Strategies**:

| Strategy | Description | Use When |
|----------|-------------|----------|
| `vad` (automatic) | Voice Activity Detection auto-commits on silence | Real-time transcription |
| `manual` | Call `connection.commit()` explicitly | Pre-recorded files, controlled commits |

**Audio Formats**:
- `PCM_16000` (16kHz, 16-bit PCM)
- `PCM_24000` (24kHz, 16-bit PCM)

**Gotchas**:
- Token is **single-use** (expires after one connection)
- Closed beta - requires sales contact
- Language detection automatic (no manual override)
- No speaker diarization yet

**When to Use Scribe**:
- Building custom transcription UI
- Real-time captions/subtitles
- Voice note apps
- Meeting transcription
- Accessibility features

**When NOT to Use**:
Use **Agents Platform** instead if you need:
- Conversational AI (LLM + TTS)
- Two-way voice interaction
- Agent responses

---

## 7. Testing & Evaluation

### Scenario Testing (LLM-Based Evaluation)

Simulate full conversations and evaluate against success criteria.

**Configuration via CLI**:
```bash
elevenlabs tests add "Refund Request Test" --template basic-llm
```

**test_configs/refund-request-test.json**:
```json
{
  "name": "Refund Request Test",
  "scenario": "Customer requests refund for defective product",
  "user_input": "I want a refund for order #12345. The product was broken when it arrived.",
  "success_criteria": [
    "Agent acknowledges the request empathetically",
    "Agent asks for order number (which was already provided)",
    "Agent verifies order details",
    "Agent provides refund timeline or next steps"
  ],
  "evaluation_type": "llm"
}
```

**Run Test**:
```bash
elevenlabs agents test "Support Agent"
```

### Tool Call Testing

Verify that agents correctly use tools with the right parameters.

**Configuration**:
```json
{
  "name": "Account Balance Test",
  "scenario": "Customer requests account balance",
  "expected_tool_call": {
    "tool_name": "get_account_balance",
    "parameters": {
      "account_id": "ACC-12345"
    }
  }
}
```

### Load Testing

Test agent capacity under high concurrency.

**Configuration**:
```bash
# Spawn 100 users, 1 per second, test for 10 minutes
elevenlabs test load \
  --users 100 \
  --spawn-rate 1 \
  --duration 600
```

**Gotchas**:
- Load testing consumes real API credits
- Use burst pricing for expected traffic spikes
- Requires careful planning to avoid hitting rate limits

### Simulation API (Programmatic Testing)

**API Endpoint**:
```bash
POST /v1/convai/agents/:agent_id/simulate
```

**Example**:
```typescript
const simulation = await client.agents.simulate({
  agent_id: 'agent_123',
  scenario: 'Customer requests refund',
  user_messages: [
    "I want a refund for order #12345",
    "I ordered it last week",
    "Yes, please process it"
  ],
  success_criteria: [
    "Agent acknowledges request",
    "Agent asks for order details",
    "Agent provides refund timeline"
  ]
});

console.log('Test passed:', simulation.passed);
console.log('Criteria met:', simulation.evaluation.criteria_met);
```

**Use Cases**:
- CI/CD integration (test before deploy)
- Regression testing
- Load testing preparation

---

## 8. Analytics & Monitoring

### Conversation Analysis

Extract structured data from conversation transcripts.

**Features**:

#### Success Evaluation (LLM-Based)
```json
{
  "evaluation_criteria": {
    "resolution": "Was the customer's issue resolved?",
    "sentiment": "Was the conversation tone positive?",
    "compliance": "Did the agent follow company policies?"
  }
}
```

#### Data Collection
```json
{
  "data_collection": {
    "fields": [
      { "name": "customer_name", "type": "string" },
      { "name": "issue_type", "type": "enum", "values": ["billing", "technical", "other"] },
      { "name": "satisfaction", "type": "number", "range": [1, 5] }
    ]
  }
}
```

**Access**:
- Via Post-call Webhooks (real-time)
- Via Analytics Dashboard (batch)
- Via API (on-demand)

### Analytics Dashboard

**Metrics**:
- **Resolution Rates**: % of issues resolved
- **CX Metrics**: Sentiment, satisfaction, CSAT
- **Compliance**: Policy adherence, guardrail violations
- **Performance**: Response time, call duration, concurrency
- **Tool Usage**: Tool call frequency, success rates
- **LLM Costs**: Track costs per agent/conversation

**Access**: Dashboard → Analytics tab

---

## 9. Privacy & Compliance

### Data Retention

**Default**: 2 years (GDPR-compliant)

**Configuration**:
```json
{
  "privacy": {
    "transcripts": {
      "retention_days": 730  // 2 years (GDPR)
    },
    "audio": {
      "retention_days": 2190  // 6 years (HIPAA)
    }
  }
}
```

**Compliance Recommendations**:
- **GDPR**: Align with data processing purposes (typically 1-2 years)
- **HIPAA**: Minimum 6 years for medical records
- **SOC 2**: Encryption in transit and at rest (automatic)

### Encryption

- **In Transit**: TLS 1.3
- **At Rest**: AES-256
- **Regional Compliance**: Data residency (US, EU, India)

**Regional Configuration**:
```typescript
const { startConversation } = useConversation({
  serverLocation: 'eu-residency' // 'us' | 'global' | 'eu-residency' | 'in-residency'
});
```

### Zero Retention Mode

For maximum privacy, enable zero retention to immediately delete all conversation data.

**Limitations**:
- No conversation history
- No analytics
- No post-call webhooks
- No MCP tool integrations

---

## 10. Cost Optimization

### LLM Caching

Reduce costs by caching repeated inputs.

**How It Works**:
- **First request**: Full cost (`input_cache_write`)
- **Subsequent requests**: Reduced cost (`input_cache_read`)
- **Automatic cache invalidation** after TTL

**Configuration**:
```json
{
  "llm_config": {
    "caching": {
      "enabled": true,
      "ttl_seconds": 3600  // 1 hour
    }
  }
}
```

**Use Cases**:
- Repeated system prompts
- Large knowledge bases
- Frequent tool definitions

**Savings**: Up to 90% on cached inputs

### Model Swapping

Switch between models based on cost/performance needs.

**Available Models**:
- **GPT-4o** (high cost, high quality)
- **GPT-4o-mini** (medium cost, good quality)
- **Claude Sonnet 4.5** (high cost, best reasoning)
- **Gemini 2.5 Flash** (low cost, fast)

**Configuration**:
```json
{
  "llm_config": {
    "model": "gpt-4o-mini"  // Swap anytime via dashboard or API
  }
}
```

### Burst Pricing

Temporarily exceed concurrency limits during high-demand periods.

**How It Works**:
- **Normal**: Your subscription concurrency limit (e.g., 10 simultaneous calls)
- **Burst**: Up to 3x your limit (e.g., 30 simultaneous calls)
- **Cost**: 2x the standard rate for burst calls

**Configuration**:
```json
{
  "call_limits": {
    "burst_pricing_enabled": true
  }
}
```

**Use Cases**:
- Black Friday traffic spikes
- Product launches
- Seasonal demand (holidays)

**Gotchas**:
- Burst calls cost 2x (plan accordingly)
- Not unlimited (3x cap)

---

## 11. Advanced Features

### Events (WebSocket/SSE)

Real-time event streaming for live transcription, agent responses, and tool calls.

**Event Types**:
- `audio` - Audio stream chunks
- `transcript` - Real-time transcription
- `agent_response` - Agent's text response
- `tool_call` - Tool execution status
- `conversation_state` - State updates

**Example**:
```typescript
const { startConversation } = useConversation({
  onEvent: (event) => {
    switch (event.type) {
      case 'transcript':
        console.log('User said:', event.data.text);
        break;
      case 'agent_response':
        console.log('Agent replied:', event.data.text);
        break;
      case 'tool_call':
        console.log('Tool called:', event.data.tool_name);
        break;
    }
  }
});
```

### Custom Models (Bring Your Own LLM)

Use your own OpenAI API key or custom LLM server.

**Configuration**:
```json
{
  "llm_config": {
    "custom": {
      "endpoint": "https://api.openai.com/v1/chat/completions",
      "api_key": "{{secret__openai_api_key}}",
      "model": "gpt-4"
    }
  }
}
```

**Use Cases**:
- Custom fine-tuned models
- Private LLM deployments (Ollama, LocalAI)
- Cost control (use your own credits)
- Compliance (on-premise models)

**Gotchas**:
- Endpoint must be OpenAI-compatible
- No official support for non-OpenAI-compatible models

### Post-Call Webhooks

Receive notifications when a call ends and analysis completes.

**Configuration**:
```json
{
  "webhooks": {
    "post_call": {
      "url": "https://api.example.com/webhook",
      "headers": {
        "Authorization": "Bearer {{secret__webhook_auth_token}}"
      }
    }
  }
}
```

**Payload**:
```json
{
  "conversation_id": "conv_123",
  "agent_id": "agent_456",
  "transcript": "...",
  "duration_seconds": 120,
  "analysis": {
    "sentiment": "positive",
    "resolution": true,
    "extracted_data": {
      "customer_name": "John Doe",
      "issue_type": "billing"
    }
  }
}
```

**Security (HMAC Verification)**:
```typescript
import crypto from 'crypto';

export async function POST(req: Request) {
  const signature = req.headers.get('elevenlabs-signature');
  const payload = await req.text();

  const hmac = crypto
    .createHmac('sha256', process.env.WEBHOOK_SECRET!)
    .update(payload)
    .digest('hex');

  if (signature !== hmac) {
    return new Response('Invalid signature', { status: 401 });
  }

  // Process webhook
  const data = JSON.parse(payload);
  console.log('Conversation ended:', data.conversation_id);

  // MUST return 200
  return new Response('OK', { status: 200 });
}
```

**Gotchas**:
- Must return 200 status code
- Auto-disabled after 10 consecutive failures (7+ days since last success)
- Retry logic: 3 attempts with exponential backoff

### Chat Mode (Text-Only)

Disable voice, use text-only conversations.

**Configuration**:
```json
{
  "conversation_config": {
    "chat_mode": true  // Disables audio input/output
  }
}
```

**Benefits**:
- Faster response times (~200ms saved)
- Lower costs (no ASR/TTS charges)
- Easier testing (no microphone required)

**Use Cases**:
- Testing agents without audio
- Building text chat interfaces
- Accessibility (text-only users)

### Telephony Integration

**SIP Trunking**:
```
SIP Endpoint: sip-static.rtc.elevenlabs.io
TLS Transport: Recommended for production
SRTP Encryption: Supported
```

**Supported Providers**: Twilio, Vonage, RingCentral, Sinch, Infobip, Telnyx, Exotel, Plivo, Bandwidth

**Native Twilio Integration**:
```json
{
  "telephony": {
    "provider": "twilio",
    "phone_number": "+1234567890",
    "account_sid": "{{secret__twilio_account_sid}}",
    "auth_token": "{{secret__twilio_auth_token}}"
  }
}
```

**Use Cases**:
- Customer support hotlines
- Appointment scheduling
- Order status inquiries
- IVR systems

---

## 12. CLI & DevOps ("Agents as Code")

### Installation & Authentication

```bash
# Install globally
npm install -g @elevenlabs/cli

# Authenticate
elevenlabs auth login

# Set residency (for GDPR compliance)
elevenlabs auth residency eu-residency  # or 'in-residency' | 'global'

# Check current user
elevenlabs auth whoami
```

**Environment Variables** (For CI/CD):
```bash
export ELEVENLABS_API_KEY=your-api-key
```

### Project Structure

**Initialize Project**:
```bash
elevenlabs agents init
```

**Directory Structure Created**:
```
your_project/
├── agents.json              # Agent registry
├── tools.json               # Tool configurations
├── tests.json               # Test configurations
├── agent_configs/           # Individual agent files (.json)
├── tool_configs/            # Tool configuration files
└── test_configs/            # Test configuration files
```

### Agent Management Commands

```bash
# Create agent
elevenlabs agents add "Support Agent" --template customer-service

# Deploy to platform
elevenlabs agents push
elevenlabs agents push --agent "Support Agent"
elevenlabs agents push --env prod
elevenlabs agents push --dry-run  # Preview changes

# Import existing agents
elevenlabs agents pull

# List agents
elevenlabs agents list

# Check sync status
elevenlabs agents status

# Delete agent
elevenlabs agents delete <agent_id>
```

### Tool Management Commands

```bash
# Create webhook tool
elevenlabs tools add-webhook "Get Weather" --config-path tool_configs/get-weather.json

# Create client tool
elevenlabs tools add-client "Update Cart" --config-path tool_configs/update-cart.json

# Deploy tools
elevenlabs tools push

# Import existing tools
elevenlabs tools pull

# Delete tools
elevenlabs tools delete <tool_id>
elevenlabs tools delete --all
```

### Testing Commands

```bash
# Create test
elevenlabs tests add "Refund Test" --template basic-llm

# Deploy tests
elevenlabs tests push

# Import tests
elevenlabs tests pull

# Run test
elevenlabs agents test "Support Agent"
```

### Multi-Environment Deployment

**Pattern**:
```bash
# Development
elevenlabs agents push --env dev

# Staging
elevenlabs agents push --env staging

# Production (with confirmation)
elevenlabs agents push --env prod --dry-run
# Review changes...
elevenlabs agents push --env prod
```

**Environment-Specific Configs**:
```
agent_configs/
├── support-bot.json          # Base config
├── support-bot.dev.json      # Dev overrides
├── support-bot.staging.json  # Staging overrides
└── support-bot.prod.json     # Prod overrides
```

### CI/CD Integration

**GitHub Actions Example**:
```yaml
name: Deploy Agent
on:
  push:
    branches: [main]
    paths:
      - 'agent_configs/**'
      - 'tool_configs/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install CLI
        run: npm install -g @elevenlabs/cli

      - name: Test Configs
        run: elevenlabs agents push --dry-run --env prod
        env:
          ELEVENLABS_API_KEY: ${{ secrets.ELEVENLABS_API_KEY_PROD }}

      - name: Deploy
        run: elevenlabs agents push --env prod
        env:
          ELEVENLABS_API_KEY: ${{ secrets.ELEVENLABS_API_KEY_PROD }}
```

### Version Control Best Practices

**Commit**:
- `agent_configs/*.json`
- `tool_configs/*.json`
- `test_configs/*.json`
- `agents.json`, `tools.json`, `tests.json`

**Ignore**:
```
# .gitignore
.env
.elevenlabs/
*.secret.json
```

---

## 13. Common Errors & Solutions

### Error 1: Missing Required Dynamic Variables

**Symptom**: "Missing required dynamic variables" error, no transcript generated

**Cause**: Dynamic variables referenced in prompts/messages but not provided at conversation start

**Solution**:
```typescript
const conversation = await client.conversations.create({
  agent_id: "agent_123",
  dynamic_variables: {
    user_name: "John",
    account_tier: "premium",
    // Provide ALL variables referenced in prompts
  }
});
```

### Error 2: Case-Sensitive Tool Names

**Symptom**: Tool not executing, agent says "tool not found"

**Cause**: Tool name in config doesn't match registered name (case-sensitive)

**Solution**:
```json
// agent_configs/bot.json
{
  "agent": {
    "prompt": {
      "tool_ids": ["orderLookup"]  // Must match exactly
    }
  }
}

// tool_configs/order-lookup.json
{
  "name": "orderLookup"  // Match case exactly
}
```

### Error 3: Webhook Authentication Failures

**Symptom**: Webhook auto-disabled after failures

**Cause**:
- Incorrect HMAC signature verification
- Not returning 200 status code
- 10+ consecutive failures

**Solution**:
```typescript
// Always verify HMAC signature
import crypto from 'crypto';

const signature = req.headers['elevenlabs-signature'];
const payload = JSON.stringify(req.body);

const hmac = crypto
  .createHmac('sha256', process.env.WEBHOOK_SECRET)
  .update(payload)
  .digest('hex');

if (signature !== hmac) {
  return res.status(401).json({ error: 'Invalid signature' });
}

// Process webhook
// ...

// MUST return 200
res.status(200).json({ success: true });
```

### Error 4: Voice Consistency Issues

**Symptom**: Generated audio varies in volume/tone

**Cause**:
- Background noise in voice clone training data
- Inconsistent microphone distance
- Whispering or shouting in samples

**Solution**:
- Use clean audio samples (no music, noise, pops)
- Maintain consistent microphone distance
- Avoid extreme volumes
- Test voice settings before deployment

### Error 5: Wrong Language Voice

**Symptom**: Unpredictable pronunciation, accent issues

**Cause**: Using English-trained voice for non-English language

**Solution**:
```json
{
  "language_presets": [
    {
      "language": "es",
      "voice_id": "spanish_trained_voice_id"  // Must be Spanish-trained
    }
  ]
}
```

### Error 6: Restricted API Keys Not Supported (CLI)

**Symptom**: CLI authentication fails

**Cause**: Using restricted API key (not currently supported)

**Solution**: Use unrestricted API key for CLI operations

### Error 7: Agent Configuration Push Conflicts

**Symptom**: Changes not reflected after push

**Cause**: Hash-based change detection missed modification

**Solution**:
```bash
# Force re-sync
elevenlabs agents init --override
elevenlabs agents pull  # Re-import from platform
# Make changes
elevenlabs agents push
```

### Error 8: Tool Parameter Schema Mismatch

**Symptom**: Tool called but parameters empty or incorrect

**Cause**: Schema definition doesn't match actual usage

**Solution**:
```json
// tool_configs/order-lookup.json
{
  "parameters": {
    "type": "object",
    "properties": {
      "order_id": {
        "type": "string",
        "description": "The order ID to look up (format: ORD-12345)"  // Clear description
      }
    },
    "required": ["order_id"]
  }
}
```

### Error 9: RAG Index Not Ready

**Symptom**: Agent doesn't use knowledge base

**Cause**: RAG index still computing (can take minutes for large documents)

**Solution**:
```typescript
// Check index status before using
const index = await client.knowledgeBase.getRagIndex({
  document_id: 'doc_123'
});

if (index.status !== 'ready') {
  console.log('Index still computing...');
}
```

### Error 10: WebSocket Protocol Error (1002)

**Symptom**: Intermittent "protocol error" when using WebSocket connections

**Cause**: Network instability or incompatible browser

**Solution**:
- Use WebRTC instead of WebSocket (more resilient)
- Implement reconnection logic
- Check browser compatibility

### Error 11: 401 Unauthorized in Production

**Symptom**: Works locally but fails in production

**Cause**: Agent visibility settings or API key configuration

**Solution**:
- Check agent visibility (public vs private)
- Verify API key is set in production environment
- Check allowlist configuration if enabled

### Error 12: Allowlist Connection Errors

**Symptom**: "Host elevenlabs.io is not allowed to connect to this agent"

**Cause**: Agent has allowlist enabled but using shared link

**Solution**:
- Configure agent allowlist with correct domains
- Or disable allowlist for testing

### Error 13: Workflow Infinite Loops

**Symptom**: Agent gets stuck in workflow, never completes

**Cause**: Edge conditions creating loops

**Solution**:
- Add max iteration limits
- Test all edge paths
- Add explicit exit conditions

### Error 14: Burst Pricing Not Enabled

**Symptom**: Calls rejected during traffic spikes

**Cause**: Burst pricing not enabled in agent settings

**Solution**:
```json
{
  "call_limits": {
    "burst_pricing_enabled": true
  }
}
```

### Error 15: MCP Server Timeout

**Symptom**: MCP tools not responding

**Cause**: MCP server slow or unreachable

**Solution**:
- Check MCP server URL is accessible
- Verify transport type (SSE vs HTTP)
- Check authentication token
- Monitor MCP server logs

### Error 16: First Message Cutoff on Android

**Symptom**: First message from agent gets cut off on Android devices (works fine on iOS/web)

**Cause**: Android devices need time to switch to correct audio mode after connection

**Solution**:
```typescript
import { useConversation } from '@elevenlabs/react';

const { startConversation } = useConversation({
  agentId: 'your-agent-id',

  // Add connection delay for Android
  connectionDelay: {
    android: 3_000,  // 3 seconds (default)
    ios: 0,          // No delay needed
    default: 0       // Other platforms
  },

  // Rest of config...
});
```

**Explanation**:
- Android needs 3 seconds to switch audio routing mode
- Without delay, first audio chunk is lost
- iOS and web don't have this issue
- Adjust delay if 3 seconds isn't sufficient

**Testing**:
```bash
# Test on Android device
npm run android

# First message should now be complete
```

### Error 17: CSP (Content Security Policy) Violations

**Symptom**: "Refused to load the script because it violates the following Content Security Policy directive" errors in browser console

**Cause**: Applications with strict Content Security Policy don't allow `data:` or `blob:` URLs in `script-src` directive. ElevenLabs SDK uses Audio Worklets that are loaded as blobs by default.

**Solution - Self-Host Worklet Files**:

**Step 1**: Copy worklet files to your public directory:
```bash
# Copy from node_modules
cp node_modules/@elevenlabs/client/dist/worklets/*.js public/elevenlabs/
```

**Step 2**: Configure SDK to use self-hosted worklets:
```typescript
import { useConversation } from '@elevenlabs/react';

const { startConversation } = useConversation({
  agentId: 'your-agent-id',

  // Point to self-hosted worklet files
  workletPaths: {
    'rawAudioProcessor': '/elevenlabs/rawAudioProcessor.worklet.js',
    'audioConcatProcessor': '/elevenlabs/audioConcatProcessor.worklet.js',
  },

  // Rest of config...
});
```

**Step 3**: Update CSP headers to allow self-hosted scripts:
```nginx
# nginx example
add_header Content-Security-Policy "
  default-src 'self';
  script-src 'self' https://elevenlabs.io;
  connect-src 'self' https://api.elevenlabs.io wss://api.elevenlabs.io;
  worker-src 'self';
" always;
```

**Worklet Files Location**:
```
node_modules/@elevenlabs/client/dist/worklets/
├── rawAudioProcessor.worklet.js
└── audioConcatProcessor.worklet.js
```

**Gotchas**:
- Worklet files must be served from same origin (CORS restriction)
- Update worklet files when upgrading `@elevenlabs/client`
- Paths must match exactly (case-sensitive)

**When You Need This**:
- Enterprise applications with strict CSP
- Government/financial apps
- Apps with security audits
- Any app blocking `blob:` URLs

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

**Production Tested**: WordPress Auditor, Customer Support Agents
**Last Updated**: 2025-11-03
**Package Versions**: elevenlabs@1.59.0, @elevenlabs/cli@0.2.0
