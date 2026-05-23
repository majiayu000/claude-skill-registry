---
name: tool-calling
description: Define and run tool-calling patterns for LLMs (schema design, call loops, validation, parallel calls). Use when building function/tool calling workflows or debugging tool selection and arguments; triggers: tool-calling, function-calling, tool schema, tool declaration, parallel function calling.
---

# Tool Calling

## Overview
Define tools as structured interfaces the model can call, then implement a loop that executes those calls and returns results. Treat tool calls as suggestions that must be validated before execution.

## When to Use
- Use this skill when the frontmatter triggers apply; otherwise start with a simple prompt or deterministic workflow.

## Decision Tree
1. Does the model need access to external data or actions?
   - Yes: define tools and a call loop.
2. Are calls independent and can be executed in parallel?
   - Yes: allow parallel calls and aggregate results.
3. Do arguments frequently fail validation?
   - Yes: tighten schemas and add a validation gate.

## Workflows

### 1. Tool Schema Definition
1. Choose a single, concrete action per tool (fetch, mutate, or transform).
2. Write a JSON schema with `name`, `description`, and `parameters`.
3. Use `type: object`, `properties`, and `required` for arguments.
4. Add enums or patterns where arguments are restricted.
5. Register the tool list in the model request.

### 2. Tool Call Execution Loop
1. Send the prompt with tool definitions.
2. If a tool call is returned, validate the arguments against the schema.
3. Execute the tool and capture the result.
4. Send the tool result back to the model for a final response.

### 3. Validation Gate for Arguments
1. Validate required keys and type compatibility.
2. Reject unknown keys or invalid enum values.
3. If validation fails, return a structured error to the model and request a corrected call.

## Non-Obvious Insights
- Tool calls are model decisions; treat them as requests and gate with validation.
- Tool schemas are the only interface the model sees, so the schema quality directly shapes behavior.
- Schemas specify how to call functions; ambiguous or incomplete schemas yield ambiguous arguments.
- Parallel calls should only be used when calls do not depend on each other.

## Evidence
- "the model determines when to call specific functions and provides the necessary parameters to execute real-world actions." - [Google AI](https://ai.google.dev/gemini-api/docs/function-calling)
- "schema specifying how to call one or more of the declared functions in order to respond to the user's question." - [Google AI](https://ai.google.dev/gemini-api/docs/function-calling)
- "A function or tool refers in the abstract to a piece of functionality that we tell the model it has access to." - [OpenAI](https://platform.openai.com/docs/guides/function-calling)
- "As a model generates a response to a prompt, it may decide that it needs data or functionality provided by a tool to follow the prompt's instructions." - [OpenAI](https://platform.openai.com/docs/guides/function-calling)

## Scripts
- `scripts/tool-calling_tool.py`: CLI for linting tool schemas and validating tool calls.
- `scripts/tool-calling_tool.js`: Node.js CLI for the same checks.

## Dependencies
- Python 3.11+ or Node 18+.

## References
- [references/README.md](references/README.md)
