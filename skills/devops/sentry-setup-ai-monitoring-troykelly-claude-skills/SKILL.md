---
name: sentry-setup-ai-monitoring
description: Setup Sentry AI Agent Monitoring in any project. Use this when asked to add AI monitoring, track LLM calls, monitor AI agents, or instrument OpenAI/Anthropic/Vercel AI/LangChain/Google GenAI. Automatically detects installed AI SDKs and configures the appropriate Sentry integration.
allowed-tools: Read, Edit, Write, Bash, Grep, Glob, AskUserQuestion
---

# SOURCE: getsentry/sentry-for-claude
# PATH: skills/sentry-setup-ai-monitoring/SKILL.md
# DO NOT EDIT: This file is synced from external source


# Setup Sentry AI Agent Monitoring

This skill helps configure Sentry's AI Agent Monitoring to track LLM calls, agent executions, tool usage, and token consumption.

## When to Use This Skill

Invoke this skill when:
- User asks to "setup AI monitoring" or "add AI agent tracking"
- User wants to "monitor LLM calls" or "track OpenAI/Anthropic usage"
- User requests "AI observability" or "agent monitoring"
- User mentions tracking token usage, model latency, or AI costs
- User asks about instrumenting their AI/LLM code with Sentry

## CRITICAL: Detection-First Approach

**ALWAYS detect installed AI SDKs before suggesting configuration.** Do not assume which AI library the user is using.

---

## Step 1: Detect Platform and AI SDKs

### For JavaScript/TypeScript Projects

Run these commands to detect installed AI packages:

```bash
# Check package.json for AI SDKs
grep -E '"(openai|@anthropic-ai/sdk|ai|@langchain|@google/genai|@langchain/langgraph)"' package.json
```

**Supported JavaScript AI SDKs:**

| Package | Sentry Integration | Min SDK Version | Package Version |
|---------|-------------------|-----------------|-----------------|
| `openai` | `openAIIntegration` | 10.2.0 | >=4.0.0 <7 |
| `@anthropic-ai/sdk` | `anthropicAIIntegration` | 10.12.0 | >=0.19.2 <1 |
| `ai` (Vercel AI SDK) | `vercelAIIntegration` | 10.6.0 | >=3.0.0 <6 |
| `@langchain/*` | `langChainIntegration` | 10.22.0 | >=0.1.0 <1 |
| `@google/genai` | `googleGenAIIntegration` | 10.14.0 | >=0.10.0 <2 |
| `@langchain/langgraph` | `langGraphIntegration` | 10.25.0 | >=0.2.0 <1 |

### For Python Projects

```bash
# Check requirements.txt or pyproject.toml
grep -E '(openai|anthropic|langchain|huggingface)' requirements.txt pyproject.toml 2>/dev/null
```

**Supported Python AI SDKs:**

| Package | Sentry Extra | Min SDK Version | Package Version |
|---------|-------------|-----------------|-----------------|
| `openai` | `sentry-sdk[openai]` | 2.41.0 | >=1.0.0 |
| `anthropic` | `sentry-sdk[anthropic]` | 2.x | >=0.16.0 |
| `langchain` | `sentry-sdk[langchain]` | 2.x | >=0.1.11 |
| `huggingface_hub` | `sentry-sdk[huggingface_hub]` | 2.x | >=0.22.0 |

---

## Step 2: Verify Sentry SDK Version

### JavaScript
```bash
grep -E '"@sentry/(nextjs|react|node)"' package.json
```

Check version meets minimum for detected AI SDK (see table above).

**Upgrade if needed:**
```bash
npm install @sentry/nextjs@latest  # or appropriate package
```

### Python
```bash
pip show sentry-sdk | grep Version
```

**Upgrade if needed:**
```bash
pip install --upgrade "sentry-sdk[openai]"  # include detected extras
```

---

## Step 3: Verify Tracing is Enabled

AI Agent Monitoring requires tracing. Check that `tracesSampleRate` is set in `Sentry.init()`.

If not enabled, inform the user:
```
AI Agent Monitoring requires tracing to be enabled. I'll add tracesSampleRate to your Sentry configuration.
```

---

## Step 4: Configure Based on Detected SDK

### IMPORTANT: Present Detection Results First

Before configuring, tell the user what you found:

```
I detected the following AI SDK(s) in your project:
- [SDK NAME] (version X.X.X)

Sentry has automatic integration support for this SDK. I'll configure the appropriate integration.
```

If no supported SDK is detected:
```
I didn't detect any AI SDKs with automatic Sentry integration support in your project.

Your options:
1. Manual Instrumentation - I can help you set up custom spans for your AI calls
2. Install a supported SDK - If you're planning to add one of the supported SDKs

Would you like to proceed with manual instrumentation? If so, please describe where your AI/LLM calls are located.
```

---

## JavaScript Integration Configurations

### OpenAI Integration

**Automatic** - Enabled by default in SDK 10.2.0+

**Explicit configuration** (to enable input/output recording):

```javascript
import * as Sentry from "@sentry/nextjs"; // or @sentry/node, @sentry/react

Sentry.init({
  dsn: "YOUR_DSN_HERE",
  tracesSampleRate: 1.0,

  integrations: [
    Sentry.openAIIntegration({
      recordInputs: true,  // Capture prompts/messages
      recordOutputs: true, // Capture responses
    }),
  ],
});
```

**Supported methods (auto-instrumented):**
- `chat.completions.create()`
- `responses.create()`

**Example usage (no changes needed):**
```javascript
import OpenAI from "openai";

const openai = new OpenAI();
const response = await openai.chat.completions.create({
  model: "gpt-4o",
  messages: [{ role: "user", content: "Hello!" }],
});
// Automatically captured by Sentry
```

---

### Anthropic Integration

**Automatic** - Enabled by default in SDK 10.12.0+

**Explicit configuration:**

```javascript
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: "YOUR_DSN_HERE",
  tracesSampleRate: 1.0,

  integrations: [
    Sentry.anthropicAIIntegration({
      recordInputs: true,
      recordOutputs: true,
    }),
  ],
});
```

**Supported methods (auto-instrumented):**
- `messages.create()` / `messages.stream()`
- `messages.countTokens()`
- `completions.create()`
- `beta.messages.create()`

---

### Vercel AI SDK Integration

**Automatic in Node runtime** - Enabled by default in SDK 10.6.0+

**For Edge runtime (Next.js)** - Must be explicitly enabled in `sentry.edge.config.ts`:

```javascript
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: "YOUR_DSN_HERE",
  tracesSampleRate: 1.0,
  integrations: [Sentry.vercelAIIntegration()],
});
```

**IMPORTANT: Telemetry must be enabled per-call:**

```javascript
import { generateText } from "ai";
import { openai } from "@ai-sdk/openai";

const result = await generateText({
  model: openai("gpt-4o"),
  prompt: "Hello!",
  experimental_telemetry: {
    isEnabled: true,
    recordInputs: true,
    recordOutputs: true,
    functionId: "my-generation", // Optional but recommended
  },
});
```

**Configuration options:**
```javascript
Sentry.vercelAIIntegration({
  recordInputs: true,
  recordOutputs: true,
  force: false, // Force enable even if AI module not detected
})
```

---

### LangChain Integration

**Requires explicit integration** in SDK 10.22.0+

```javascript
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: "YOUR_DSN_HERE",
  tracesSampleRate: 1.0,

  integrations: [
    Sentry.langChainIntegration({
      recordInputs: true,
      recordOutputs: true,
    }),
  ],
});
```

**Auto-instrumented operations:**
- Chat model calls (`gen_ai.request`)
- LLM pipeline executions (`gen_ai.pipeline`)
- Chain invocations (`gen_ai.invoke_agent`)
- Tool calls (`gen_ai.execute_tool`)
- `invoke()`, `stream()`, `batch()` methods

---

### LangGraph Integration

**Requires explicit integration** in SDK 10.25.0+

```javascript
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: "YOUR_DSN_HERE",
  tracesSampleRate: 1.0,

  integrations: [
    Sentry.langGraphIntegration({
      recordInputs: true,
      recordOutputs: true,
    }),
  ],
});
```

**Auto-instrumented:**
- Agent creation (StateGraph compilation)
- Agent invocation (`invoke()` method)

---

### Google GenAI Integration

**Automatic** - Enabled by default in SDK 10.14.0+

**Explicit configuration:**

```javascript
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: "YOUR_DSN_HERE",
  tracesSampleRate: 1.0,

  integrations: [
    Sentry.googleGenAIIntegration({
      recordInputs: true,
      recordOutputs: true,
    }),
  ],
});
```

**Supported methods:**
- `models.generateContent()` / `models.generateContentStream()`
- `chats.create()`
- `sendMessage()` / `sendMessageStream()`

---

## Python Integration Configurations

### OpenAI Integration (Python)

**Install with extra:**
```bash
pip install "sentry-sdk[openai]"
```

**Configuration:**

```python
import sentry_sdk
from sentry_sdk.integrations.openai import OpenAIIntegration

sentry_sdk.init(
    dsn="YOUR_DSN_HERE",
    traces_sample_rate=1.0,
    send_default_pii=True,  # Required for input/output capture
    integrations=[
        OpenAIIntegration(
            include_prompts=True,  # Capture inputs/outputs
            tiktoken_encoding_name="cl100k_base",  # For streaming token count
        ),
    ],
)
```

**Usage (auto-instrumented):**
```python
from openai import OpenAI

client = OpenAI()

with sentry_sdk.start_transaction(name="AI inference"):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello!"}]
    )
```

---

### Anthropic Integration (Python)

**Install with extra:**
```bash
pip install "sentry-sdk[anthropic]"
```

**Configuration:**

```python
import sentry_sdk
from sentry_sdk.integrations.anthropic import AnthropicIntegration

sentry_sdk.init(
    dsn="YOUR_DSN_HERE",
    traces_sample_rate=1.0,
    send_default_pii=True,
    integrations=[
        AnthropicIntegration(
            include_prompts=True,
        ),
    ],
)
```

**Usage:**
```python
from anthropic import Anthropic

client = Anthropic()

with sentry_sdk.start_transaction(name="Claude inference"):
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello!"}]
    )
```

---

### LangChain Integration (Python)

**Install with extra:**
```bash
pip install "sentry-sdk[langchain]"
```

**Configuration:**

```python
import sentry_sdk
from sentry_sdk.integrations.langchain import LangchainIntegration

sentry_sdk.init(
    dsn="YOUR_DSN_HERE",
    traces_sample_rate=1.0,
    send_default_pii=True,  # Required for LLM input/output capture
    integrations=[
        LangchainIntegration(
            include_prompts=True,
        ),
    ],
)
```

**Usage:**
```python
with sentry_sdk.start_transaction(name="LangChain agent"):
    agent_executor = AgentExecutor(agent=agent, tools=tools)
    result = agent_executor.invoke({"input": "your prompt"})
```

---

### Hugging Face Hub Integration (Python)

**Install with extra:**
```bash
pip install "sentry-sdk[huggingface_hub]"
```

**Configuration:**

```python
import sentry_sdk
from sentry_sdk.integrations.huggingface_hub import HuggingfaceHubIntegration

sentry_sdk.init(
    dsn="YOUR_DSN_HERE",
    traces_sample_rate=1.0,
    send_default_pii=True,
    integrations=[
        HuggingfaceHubIntegration(
            include_prompts=True,
        ),
    ],
)
```

---

## Manual Instrumentation (Last Resort)

**IMPORTANT:** Only use manual instrumentation when:
1. No supported AI SDK is detected
2. User explicitly confirms they want manual instrumentation
3. User describes where their AI calls are located

### Ask User Before Proceeding

```
I'll help you set up manual AI instrumentation. To do this effectively, I need to know:

1. Where are your AI/LLM calls located? (file paths)
2. What AI provider/model are you using?
3. What operations do you want to track?
   - LLM requests (prompts, completions)
   - Agent executions
   - Tool calls
   - Agent handoffs
```

### Manual Span Types

Four span types are required for AI Agents Insights:

#### 1. AI Request Span (`gen_ai.request`)

Tracks individual LLM calls:

```javascript
import * as Sentry from "@sentry/nextjs";

async function callLLM(prompt, model = "custom-model") {
  return await Sentry.startSpan(
    {
      op: "gen_ai.request",
      name: `LLM request ${model}`,
      attributes: {
        "gen_ai.request.model": model,
        "gen_ai.request.temperature": 0.7,
        "gen_ai.request.max_tokens": 1000,
      },
    },
    async (span) => {
      // Record input messages
      span.setAttribute(
        "gen_ai.request.messages",
        JSON.stringify([{ role: "user", content: prompt }])
      );

      const startTime = performance.now();

      // Your actual LLM call here
      const result = await yourLLMClient.complete(prompt);

      // Record output and metrics
      span.setAttribute("gen_ai.response.text", result.text);
      span.setAttribute("gen_ai.usage.input_tokens", result.inputTokens || 0);
      span.setAttribute("gen_ai.usage.output_tokens", result.outputTokens || 0);

      return result;
    }
  );
}
```

#### 2. Invoke Agent Span (`gen_ai.invoke_agent`)

Tracks full agent execution lifecycle:

```javascript
async function runAgent(task) {
  return await Sentry.startSpan(
    {
      op: "gen_ai.invoke_agent",
      name: "Execute AI Agent",
      attributes: {
        "gen_ai.agent.name": "my-agent",
        "gen_ai.agent.available_tools": JSON.stringify(["search", "calculate"]),
      },
    },
    async (span) => {
      span.setAttribute("gen_ai.agent.input", task);

      // Agent execution logic (may include multiple LLM calls and tool uses)
      const result = await agent.execute(task);

      span.setAttribute("gen_ai.agent.output", JSON.stringify(result));
      span.setAttribute("gen_ai.usage.total_tokens", result.totalTokens || 0);

      return result;
    }
  );
}
```

#### 3. Execute Tool Span (`gen_ai.execute_tool`)

Tracks tool/function calls:

```javascript
async function executeTool(toolName, toolInput) {
  return await Sentry.startSpan(
    {
      op: "gen_ai.execute_tool",
      name: `Tool: ${toolName}`,
      attributes: {
        "gen_ai.tool.name": toolName,
        "gen_ai.tool.description": getToolDescription(toolName),
      },
    },
    async (span) => {
      span.setAttribute("gen_ai.tool.input", JSON.stringify(toolInput));

      const result = await tools[toolName](toolInput);

      span.setAttribute("gen_ai.tool.output", JSON.stringify(result));

      return result;
    }
  );
}
```

#### 4. Handoff Span (`gen_ai.handoff`)

Tracks agent-to-agent control transitions:

```javascript
async function handoffToAgent(fromAgent, toAgent, context) {
  return await Sentry.startSpan(
    {
      op: "gen_ai.handoff",
      name: `Handoff: ${fromAgent} -> ${toAgent}`,
      attributes: {
        "gen_ai.handoff.from_agent": fromAgent,
        "gen_ai.handoff.to_agent": toAgent,
      },
    },
    async (span) => {
      span.setAttribute("gen_ai.handoff.context", JSON.stringify(context));

      // Perform handoff
      const result = await agents[toAgent].receive(context);

      return result;
    }
  );
}
```

### Python Manual Instrumentation

```python
import sentry_sdk
import json

def call_llm(prompt, model="custom-model"):
    with sentry_sdk.start_span(
        op="gen_ai.request",
        name=f"LLM request {model}",
    ) as span:
        span.set_data("gen_ai.request.model", model)
        span.set_data("gen_ai.request.messages", json.dumps([
            {"role": "user", "content": prompt}
        ]))

        # Your actual LLM call
        result = your_llm_client.complete(prompt)

        span.set_data("gen_ai.response.text", result.text)
        span.set_data("gen_ai.usage.input_tokens", result.input_tokens)
        span.set_data("gen_ai.usage.output_tokens", result.output_tokens)

        return result
```

---

## Span Attributes Reference

### Required Attributes
| Attribute | Description |
|-----------|-------------|
| `gen_ai.request.model` | AI model identifier (e.g., "gpt-4o", "claude-3") |

### Token Usage Attributes
| Attribute | Description |
|-----------|-------------|
| `gen_ai.usage.input_tokens` | Tokens in prompt/input |
| `gen_ai.usage.output_tokens` | Tokens in response/output |
| `gen_ai.usage.total_tokens` | Total tokens used |

### Request Attributes
| Attribute | Description |
|-----------|-------------|
| `gen_ai.request.messages` | JSON string of input messages |
| `gen_ai.request.temperature` | Temperature setting |
| `gen_ai.request.max_tokens` | Max tokens limit |
| `gen_ai.request.top_p` | Top-p sampling value |

### Response Attributes
| Attribute | Description |
|-----------|-------------|
| `gen_ai.response.text` | Generated text response |
| `gen_ai.response.tool_calls` | JSON string of tool calls |

### Agent Attributes
| Attribute | Description |
|-----------|-------------|
| `gen_ai.agent.name` | Agent identifier |
| `gen_ai.agent.available_tools` | JSON array of tool names |
| `gen_ai.agent.input` | Agent input/task |
| `gen_ai.agent.output` | Agent output/result |

### Tool Attributes
| Attribute | Description |
|-----------|-------------|
| `gen_ai.tool.name` | Tool identifier |
| `gen_ai.tool.description` | Tool description |
| `gen_ai.tool.input` | JSON string of tool input |
| `gen_ai.tool.output` | JSON string of tool output |

**Note:** All complex data must be JSON stringified. Span attributes only allow primitive types.

---

## Framework-Specific Notes

### Next.js
- Configure in `instrumentation-client.ts`, `sentry.server.config.ts`, `sentry.edge.config.ts`
- Vercel AI SDK requires explicit edge runtime configuration
- Server-side LLM calls captured in server config
- Client-side calls (if any) in client config

### Node.js / Express
- Configure in entry point or dedicated sentry config
- All integrations work in Node runtime

### React (Client-Only)
- Limited usefulness - most LLM calls should be server-side
- Consider moving AI calls to API routes

### Python (Django/Flask/FastAPI)
- Configure in settings or app initialization
- Wrap LLM calls in transactions for proper span hierarchy

---

## Privacy and PII Considerations

**Prompts and outputs are considered PII.** To capture them:

### JavaScript
```javascript
Sentry.init({
  sendDefaultPii: true,
  // OR configure per-integration:
  integrations: [
    Sentry.openAIIntegration({
      recordInputs: true,
      recordOutputs: true,
    }),
  ],
});
```

### Python
```python
sentry_sdk.init(
    send_default_pii=True,
    # OR configure per-integration:
    integrations=[
        OpenAIIntegration(include_prompts=True),
    ],
)
```

**To exclude prompts/outputs:**
- Set `recordInputs: false` / `recordOutputs: false` (JS)
- Set `include_prompts=False` (Python)

---

## Verification Steps

After setup, verify AI monitoring is working:

### JavaScript
```javascript
// Trigger a test LLM call
const response = await openai.chat.completions.create({
  model: "gpt-4o-mini",
  messages: [{ role: "user", content: "Say 'Sentry test successful'" }],
});
console.log("Test complete:", response.choices[0].message.content);
```

### Python
```python
with sentry_sdk.start_transaction(name="AI Test"):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Say 'Sentry test'"}]
    )
    print("Test complete:", response.choices[0].message.content)
```

**Check in Sentry:**
1. Go to **Traces** > **AI Spans** tab
2. Look for spans with `gen_ai.*` operations
3. Verify token usage and latency are captured

---

## Common Issues and Solutions

### Issue: AI spans not appearing
**Solutions:**
1. Verify tracing is enabled (`tracesSampleRate > 0`)
2. Check SDK version meets minimum requirements
3. Ensure integration is properly configured
4. For Vercel AI: Check `experimental_telemetry.isEnabled: true`

### Issue: Token counts missing
**Solutions:**
1. Some providers don't return token counts for streaming
2. For Python OpenAI streaming, install `tiktoken`
3. Manual instrumentation: Ensure you're setting token attributes

### Issue: Prompts/outputs not captured
**Solutions:**
1. Enable `sendDefaultPii: true` or per-integration recording
2. Check `recordInputs`/`recordOutputs` or `include_prompts` settings

### Issue: Integration not detected
**Solutions:**
1. Verify AI package is installed and version is compatible
2. For Vercel AI edge runtime, explicitly add integration
3. Use `force: true` option if module detection fails

---

## Summary Checklist

```markdown
## Sentry AI Agent Monitoring Setup Complete

### Detection Results:
- [ ] AI SDK(s) detected: [LIST DETECTED SDKS]
- [ ] Sentry SDK version verified
- [ ] Tracing enabled

### Configuration Applied:
- [ ] Integration(s) added to Sentry.init()
- [ ] Input/output recording configured
- [ ] PII settings reviewed

### For Vercel AI SDK (if applicable):
- [ ] Edge runtime integration added
- [ ] experimental_telemetry enabled in function calls

### Next Steps:
1. Make an AI/LLM call to verify
2. Check Sentry > Traces > AI Spans
3. Review AI Agents Dashboard for metrics
```

---

## Quick Reference

| AI SDK | JS Integration | Python Extra |
|--------|----------------|--------------|
| OpenAI | `openAIIntegration()` | `sentry-sdk[openai]` |
| Anthropic | `anthropicAIIntegration()` | `sentry-sdk[anthropic]` |
| Vercel AI | `vercelAIIntegration()` | N/A |
| LangChain | `langChainIntegration()` | `sentry-sdk[langchain]` |
| LangGraph | `langGraphIntegration()` | N/A |
| Google GenAI | `googleGenAIIntegration()` | N/A |
| Hugging Face | N/A | `sentry-sdk[huggingface_hub]` |
