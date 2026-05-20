---
name: arize-instrumentation
description: "INVOKE THIS SKILL when adding Arize AX tracing to an application. Follow the Agent-Assisted Tracing two-phase flow: analyze the codebase (read-only), then implement instrumentation after user confirmation. When the app uses LLM tool/function calling, add manual CHAIN + TOOL spans so traces show each tool's input and output. Leverages https://arize.com/docs/ax/alyx/tracing-assistant and https://arize.com/docs/PROMPT.md."
---

# Arize Instrumentation Skill

Use this skill when the user wants to **add Arize AX tracing** to their application. Follow the **two-phase, agent-assisted flow** from the [Agent-Assisted Tracing Setup](https://arize.com/docs/ax/alyx/tracing-assistant) and the [Arize AX Tracing — Agent Setup Prompt](https://arize.com/docs/PROMPT.md).

## Quick start (for the user)

If the user asks you to "set up tracing" or "instrument my app with Arize", you can start with:

> Follow the instructions from https://arize.com/docs/PROMPT.md and ask me questions as needed.

Then execute the two phases below.

## Core principles

- **Prefer inspection over mutation** — understand the codebase before changing it.
- **Do not change business logic** — tracing is purely additive.
- **Use auto-instrumentation where available** — add manual spans only for custom logic not covered by integrations.
- **Follow existing code style** and project conventions.
- **Keep output concise and production-focused** — do not generate extra documentation or summary files.

## Phase 1: Analysis (read-only)

**Do not write any code or create any files during this phase.**

### Steps

1. **Check dependency manifests** to detect stack:
   - Python: `pyproject.toml`, `requirements.txt`, `setup.py`, `Pipfile`
   - TypeScript/JavaScript: `package.json`
   - Java: `pom.xml`, `build.gradle`, `build.gradle.kts`

2. **Scan import statements** in source files to confirm what is actually used.

3. **Check for existing tracing/OTel** — look for `TracerProvider`, `register()`, `opentelemetry` imports, `ARIZE_*`, `OTEL_*`, `OTLP_*` env vars, or other observability config (Datadog, Honeycomb, etc.).

4. **Identify scope** — for monorepos or multi-service projects, ask which service(s) to instrument.

### What to identify

| Item | Examples |
|------|----------|
| Language | Python, TypeScript/JavaScript, Java |
| Package manager | pip/poetry/uv, npm/pnpm/yarn, maven/gradle |
| LLM providers | OpenAI, Anthropic, LiteLLM, Bedrock, etc. |
| Frameworks | LangChain, LangGraph, LlamaIndex, Vercel AI SDK, Mastra, etc. |
| Existing tracing | Any OTel or vendor setup |
| Tool/function use | LLM tool use, function calling, or custom tools the app executes (e.g. in an agent loop) |

**Key rule:** When a framework is detected alongside an LLM provider, **instrument both**. Provider/framework instrumentors do **not** create spans for **tool execution** — only for LLM API calls. If the app runs tools (e.g. `check_loan_eligibility`, `run_fraud_detection`), add manual TOOL spans so each invocation appears with input/output (see **Enriching traces** below). The framework instrumentor does not trace the underlying LLM calls — you need the provider instrumentor too.

### Phase 1 output

Return a concise summary:

- Detected language, package manager, providers, frameworks
- Proposed integration list (from the routing table in the docs)
- Any existing OTel/tracing that needs consideration
- If monorepo: which service(s) you propose to instrument
- **If the app uses LLM tool use / function calling:** note that you will add manual CHAIN + TOOL spans so each tool call appears in the trace with input/output (avoids sparse traces).

**STOP. Present your analysis and wait for user confirmation before proceeding to Phase 2.**

## Integration routing and docs

The **canonical list** of supported integrations and doc URLs is in the [Agent Setup Prompt](https://arize.com/docs/PROMPT.md). Use it to map detected signals to implementation docs.

- **LLM providers:** [OpenAI](https://arize.com/docs/ax/integrations/llm-providers/openai), [Anthropic](https://arize.com/docs/ax/integrations/llm-providers/anthropic), [LiteLLM](https://arize.com/docs/ax/integrations/llm-providers/litellm), [Google Gen AI](https://arize.com/docs/ax/integrations/llm-providers/google-gen-ai), [Bedrock](https://arize.com/docs/ax/integrations/llm-providers/amazon-bedrock), [Ollama](https://arize.com/docs/ax/integrations/llm-providers/llama), [Groq](https://arize.com/docs/ax/integrations/llm-providers/groq), [MistralAI](https://arize.com/docs/ax/integrations/llm-providers/mistralai), [OpenRouter](https://arize.com/docs/ax/integrations/llm-providers/openrouter), [VertexAI](https://arize.com/docs/ax/integrations/llm-providers/vertexai).
- **Python frameworks:** [LangChain](https://arize.com/docs/ax/integrations/python-agent-frameworks/langchain), [LangGraph](https://arize.com/docs/ax/integrations/python-agent-frameworks/langgraph), [LlamaIndex](https://arize.com/docs/ax/integrations/python-agent-frameworks/llamaindex), [CrewAI](https://arize.com/docs/ax/integrations/python-agent-frameworks/crewai), [DSPy](https://arize.com/docs/ax/integrations/python-agent-frameworks/dspy), [AutoGen](https://arize.com/docs/ax/integrations/python-agent-frameworks/autogen), [Semantic Kernel](https://arize.com/docs/ax/integrations/python-agent-frameworks/semantic-kernel), [Pydantic AI](https://arize.com/docs/ax/integrations/python-agent-frameworks/pydantic), [Haystack](https://arize.com/docs/ax/integrations/python-agent-frameworks/haystack), [Guardrails AI](https://arize.com/docs/ax/integrations/python-agent-frameworks/guardrails-ai), [Hugging Face Smolagents](https://arize.com/docs/ax/integrations/python-agent-frameworks/hugging-face-smolagents), [Instructor](https://arize.com/docs/ax/integrations/python-agent-frameworks/instructor), [Agno](https://arize.com/docs/ax/integrations/python-agent-frameworks/agno), [Google ADK](https://arize.com/docs/ax/integrations/python-agent-frameworks/google-adk), [MCP](https://arize.com/docs/ax/integrations/python-agent-frameworks/model-context-protocol), [Portkey](https://arize.com/docs/ax/integrations/python-agent-frameworks/portkey), [Together AI](https://arize.com/docs/ax/integrations/python-agent-frameworks/together-ai), [BeeAI](https://arize.com/docs/ax/integrations/python-agent-frameworks/beeai), [AWS Bedrock Agents](https://arize.com/docs/ax/integrations/python-agent-frameworks/aws).
- **TypeScript/JavaScript:** [LangChain JS](https://arize.com/docs/ax/integrations/ts-js-agent-frameworks/langchain), [Mastra](https://arize.com/docs/ax/integrations/ts-js-agent-frameworks/mastra), [Vercel AI SDK](https://arize.com/docs/ax/integrations/ts-js-agent-frameworks/vercel), [BeeAI JS](https://arize.com/docs/ax/integrations/ts-js-agent-frameworks/beeai).
- **Java:** [LangChain4j](https://arize.com/docs/ax/integrations/java/langchain4j), [Spring AI](https://arize.com/docs/ax/integrations/java/spring-ai), [Arconia](https://arize.com/docs/ax/integrations/java/arconia).
- **Platforms (UI-based):** [LangFlow](https://arize.com/docs/ax/integrations/platforms/langflow), [Flowise](https://arize.com/docs/ax/integrations/platforms/flowise), [Dify](https://arize.com/docs/ax/integrations/platforms/dify), [Prompt flow](https://arize.com/docs/ax/integrations/platforms/prompt-flow).
- **Fallback:** [Manual instrumentation](https://arize.com/docs/ax/observe/tracing/setup/manual-instrumentation), [All integrations](https://arize.com/docs/ax/integrations).

**Fetch the matched doc pages** from the [full routing table in PROMPT.md](https://arize.com/docs/PROMPT.md) for exact installation and code snippets. Use [llms.txt](https://arize.com/docs/llms.txt) as a fallback for doc discovery if needed.

## Phase 2: Implementation

Proceed **only after the user confirms** the Phase 1 analysis.

### Steps

1. **Fetch integration docs** — Read the matched doc URLs and follow their installation and instrumentation steps.
2. **Install packages** using the detected package manager **before** writing code:
   - Python: `pip install arize-otel` plus `openinference-instrumentation-{name}` (hyphens in package name; underscores in import, e.g. `openinference.instrumentation.llama_index`).
   - TypeScript/JavaScript: `@opentelemetry/sdk-trace-node` plus the relevant `@arizeai/openinference-*` package.
   - Java: OpenTelemetry SDK plus `openinference-instrumentation-*` in pom.xml or build.gradle.
3. **Credentials** — User needs **Arize Space ID** and **API Key** from [Space API Keys](https://app.arize.com/organizations/-/settings/space-api-keys). Set as `ARIZE_SPACE_ID` and `ARIZE_API_KEY`. If the space ID is unknown, run `ax spaces list -o json` to discover it.
4. **Centralized instrumentation** — Create a single module (e.g. `instrumentation.py`, `instrumentation.ts`) and initialize tracing **before** any LLM client is created.
5. **Existing OTel** — If there is already a TracerProvider, add Arize as an **additional** exporter (e.g. BatchSpanProcessor with Arize OTLP). Do not replace existing setup unless the user asks.

### Implementation rules

- Use **auto-instrumentation first**; manual spans only when needed.
- **Fail gracefully** if env vars are missing (warn, do not crash).
- **Import order:** register tracer → attach instrumentors → then create LLM clients.
- **Project name attribute (required):** Arize rejects spans with HTTP 500 if the project name is missing — `service.name` alone is not accepted. Set it as a **resource attribute** on the TracerProvider (recommended — one place, applies to all spans): Python: `register(project_name="my-app")` handles it automatically (sets `"openinference.project.name"` on the resource); TypeScript: Arize accepts both `"model_id"` (shown in the official TS quickstart) and `"openinference.project.name"` via `SEMRESATTRS_PROJECT_NAME` from `@arizeai/openinference-semantic-conventions` (shown in the manual instrumentation docs) — both work. For routing spans to different projects in Python, use `set_routing_context(space_id=..., project_name=...)` from `arize.otel`.
- **CLI/script apps — flush before exit:** `provider.shutdown()` (TS) / `provider.force_flush()` then `provider.shutdown()` (Python) must be called before the process exits, otherwise async OTLP exports are dropped and no traces appear.
- **When the app has tool/function execution:** add manual CHAIN + TOOL spans (see **Enriching traces** below) so the trace tree shows each tool call and its result — otherwise traces will look sparse (only LLM API spans, no tool input/output).

## Enriching traces: manual spans for tool use and agent loops

### Why doesn't the auto-instrumentor do this?

**Provider instrumentors (Anthropic, OpenAI, etc.) only wrap the LLM *client* — the code that sends HTTP requests and receives responses.** They see:

- One span per API call: request (messages, system prompt, tools) and response (text, tool_use blocks, etc.).

They **cannot** see what happens *inside your application* after the response:

- **Tool execution** — Your code parses the response, calls `run_tool("check_loan_eligibility", {...})`, and gets a result. That runs in your process; the instrumentor has no hook into your `run_tool()` or the actual tool output. The *next* API call (sending the tool result back) is just another `messages.create` span — the instrumentor doesn't know that the message content is a tool result or what the tool returned.
- **Agent/chain boundary** — The idea of "one user turn → multiple LLM calls + tool calls" is an *application-level* concept. The instrumentor only sees separate API calls; it doesn't know they belong to the same logical "run_agent" run.

So TOOL and CHAIN spans have to be added **manually** (or by a *framework* instrumentor like LangChain/LangGraph that knows about tools and chains). Once you add them, they appear in the same trace as the LLM spans because they use the same TracerProvider.

---

To avoid sparse traces where tool inputs/outputs are missing:

1. **Detect** agent/tool patterns: a loop that calls the LLM, then runs one or more tools (by name + arguments), then calls the LLM again with tool results.
2. **Add manual spans** using the same TracerProvider (e.g. `opentelemetry.trace.get_tracer(...)` after `register()`):
   - **CHAIN span** — Wrap the full agent run (e.g. `run_agent`): set `openinference.span.kind` = `"CHAIN"`, `input.value` = user message, `output.value` = final reply.
   - **TOOL span** — Wrap each tool invocation: set `openinference.span.kind` = `"TOOL"`, `input.value` = JSON of arguments, `output.value` = JSON of result. Use the tool name as the span name (e.g. `check_loan_eligibility`).

**OpenInference attributes (use these so Arize shows spans correctly):**

| Attribute | Use |
|-----------|-----|
| `openinference.span.kind` | `"CHAIN"` or `"TOOL"` |
| `input.value` | string (e.g. user message or JSON of tool args) |
| `output.value` | string (e.g. final reply or JSON of tool result) |

**Python pattern:** Get the global tracer (same provider as Arize), then use context managers so tool spans are children of the CHAIN span and appear in the same trace as the LLM spans:

```python
from opentelemetry.trace import get_tracer

tracer = get_tracer("my-app", "1.0.0")

# In your agent entrypoint:
with tracer.start_as_current_span("run_agent") as chain_span:
    chain_span.set_attribute("openinference.span.kind", "CHAIN")
    chain_span.set_attribute("input.value", user_message)
    # ... LLM call ...
    for tool_use in tool_uses:
        with tracer.start_as_current_span(tool_use["name"]) as tool_span:
            tool_span.set_attribute("openinference.span.kind", "TOOL")
            tool_span.set_attribute("input.value", json.dumps(tool_use["input"]))
            result = run_tool(tool_use["name"], tool_use["input"])
            tool_span.set_attribute("output.value", result)
        # ... append tool result to messages, call LLM again ...
    chain_span.set_attribute("output.value", final_reply)
```

See [Manual instrumentation](https://arize.com/docs/ax/observe/tracing/setup/manual-instrumentation) for more span kinds and attributes.

## Verification

After implementation:

1. Run the application and trigger at least one LLM call.
2. **Use the `arize-trace` skill** to confirm traces arrived. If empty, retry shortly. Verify spans have expected `openinference.span.kind`, `input.value`/`output.value`, and parent-child relationships.
3. If no traces: verify `ARIZE_SPACE_ID` and `ARIZE_API_KEY`, ensure tracer is initialized before instrumentors and clients, check connectivity to `otlp.arize.com:443`; for debug set `GRPC_VERBOSITY=debug` or pass `log_to_console=True` to `register()`. Common gotchas: (a) missing project name resource attribute causes HTTP 500 rejections — `service.name` alone is not enough; Python: pass `project_name` to `register()`; TypeScript: set `"model_id"` or `SEMRESATTRS_PROJECT_NAME` on the resource; (b) CLI/script processes exit before OTLP exports flush — call `provider.force_flush()` then `provider.shutdown()` before exit.
4. If the app uses tools: confirm CHAIN and TOOL spans appear with `input.value` / `output.value` so tool calls and results are visible.

## Leveraging the Tracing Assistant (MCP)

For deeper instrumentation guidance inside the IDE, the user can enable:

- **Arize AX Tracing Assistant MCP** — instrumentation guides, framework examples, and support. In Cursor: **Settings → MCP → Add** and use:
  ```json
  "arize-tracing-assistant": {
    "command": "uvx",
    "args": ["arize-tracing-assistant@latest"]
  }
  ```
- **Arize AX Docs MCP** — searchable docs. In Cursor:
  ```json
  "arize-ax-docs": {
    "url": "https://arize.com/docs/mcp"
  }
  ```

Then the user can ask things like: *"Instrument this app using Arize AX"*, *"Can you use manual instrumentation so I have more control over my traces?"*, *"How can I redact sensitive information from my spans?"*

See the full setup at [Agent-Assisted Tracing Setup](https://arize.com/docs/ax/alyx/tracing-assistant).

## Reference links

| Resource | URL |
|----------|-----|
| Agent-Assisted Tracing Setup | https://arize.com/docs/ax/alyx/tracing-assistant |
| Agent Setup Prompt (full routing + phases) | https://arize.com/docs/PROMPT.md |
| Arize AX Docs | https://arize.com/docs/ax |
| Full integration list | https://arize.com/docs/ax/integrations |
| Doc index (llms.txt) | https://arize.com/docs/llms.txt |
