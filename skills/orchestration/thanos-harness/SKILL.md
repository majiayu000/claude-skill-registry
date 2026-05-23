---
name: thanos-harness
description: Route all OpenClaw user messages through Thanos orchestration.
metadata: {"openclaw":{"always":true}}
---

You are running inside OpenClaw, but Thanos is the canonical architecture.

Rules:
- For every user message, call the `thanos_route` tool with the full message.
- Do not answer directly; return the tool's response content.
- If `thanos_route` fails, return the error and stop.
 - Never propose OAuth or ask for Drive folder IDs. Thanos handles Drive sync via `gog` + OpenAI RAG.
 - Do not run ad-hoc ingestor scripts; always delegate to `thanos_route`.
