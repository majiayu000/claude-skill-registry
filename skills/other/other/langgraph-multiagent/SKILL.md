---
name: langgraph-multiagent
description: Architect-level development, audit, and migration of multi-agent systems using LangGraph (v1+) and LangChain (v1+). Use when building or refactoring supervisor/subagent architectures, orchestrator-worker workflows, routing/hand-offs, agentic RAG, memory (short + long-term), state + context engineering, guardrails + human-in-the-loop, MCP tool integration, observability (LangSmith/OpenTelemetry), deployment, and performance/cost optimization — or when migrating off deprecated patterns like `langgraph.prebuilt.create_react_agent` and libraries like `langgraph-supervisor(-py)`, LlamaIndex agents, CrewAI, Agno, or OpenAI Agents.
---

# LangGraph Multi-Agent

## What this skill does

Build, review, and modernize production-grade multi-agent systems with LangGraph/LangChain while staying version-accurate by default: always resolve the *current* APIs from docs + installed versions, and fall back to `opensrc/` source snapshots for under-the-hood edge cases.

## Default operating rules (do these every time)

1. Treat all LangGraph/LangChain APIs as **versioned**; never “code from memory” for any API surface that might have changed.
2. Establish **ground truth** before coding:
   - Determine installed/pinned versions (repo lockfiles + `importlib.metadata`).
   - Query official docs via `langchain-docs.SearchDocsByLangChain`.
   - Use Context7 for canonical API references and examples.
3. When docs are ambiguous or behavior is subtle, inspect dependency internals via `opensrc/` (read-only):
   - Run `npx opensrc pypi:<package>@<version> --modify=false`
   - Check `opensrc/sources.json` and cite exact `opensrc/...` paths + versions in your writeup.

Use `references/research_playbook.md` when you need a rigorous doc-sweep, including `llms.txt`-driven crawling of LangGraph docs.

## Workflow decision tree

- **Build something new** → follow **Build workflow**.
- **Audit/deprecations/migration** → follow **Audit & migrate workflow**.
- **Latency/cost/scale issues** → follow **Performance & scale workflow**.

## Quick start (repo-aware)

1. Generate a deprecations + framework audit report:
   - Run `python scripts/audit_repo_agents.py --root .` (from the skill folder)
   - Optional: `python scripts/audit_repo_agents.py --root . --json agent_audit.json`
   - Optional: `python scripts/generate_migration_plan.py --audit-json agent_audit.json --out migration_plan.md`
2. If you need “latest docs” for a specific area, start with:
   - `langchain-docs.SearchDocsByLangChain` using queries from `references/docs_index.md`
3. If you hit a behavior edge case, snapshot internals:
   - Run `python scripts/opensrc_snapshot.py --packages langgraph langchain langchain-core` (from the skill folder)
4. If you need a doc sitemap for LangGraph (for agentic RAG or doc crawling):
   - Run `python scripts/fetch_llms_txt_urls.py --print --unique` (from the skill folder)
5. If you need to build an offline docs cache (bounded crawl):
   - Use seeds in `references/doc_crawl_targets.md`
   - Run `python scripts/crawl_docs.py --llms-txt https://langchain-ai.github.io/langgraph/llms.txt --allow-prefixes https://langchain-ai.github.io/langgraph/ --out-dir docs_cache_langgraph` (from the skill folder)

## Reference map (use these, don’t guess)

- `references/langchain_create_agent_middleware.md`: `create_agent` + middleware hooks + migration mappings.
- `references/langchain_multiagent_handoffs.md`: choosing between subagents vs handoffs vs multi-node subgraphs.
- `references/langgraph_graph_api_primitives.md`: reducers, Send API, subgraphs, and common error codes.
- `references/memory_and_context_engineering.md`: state vs store vs runtime context; memory design.
- `references/mcp_integration_patterns.md`: MCP client/interceptors and ToolRuntime-driven auth/DI.
- `references/testing_evaluation.md`: tests + eval strategy for safe migrations.
- `references/deployment_agent_server.md`: `langgraph.json` and Agent Server deployment basics.
- `references/security_threat_model.md`: threat model + mitigations for tool calling systems.
- `references/upgrades_and_versioning.md`: repeatable upgrade process.
- `references/audit_and_migration_methodology.md`: end-to-end audit→plan→execute methodology.
- `references/api_map_python.md`: import-path cheat sheet (verify for your version).
- `references/ui_nextjs_rsc.md`: Next.js App Router (RSC) + React UI integration (Agent Server + `useStream`).
- `references/ui_nextjs_ai_sdk.md`: Next.js App Router using AI SDK v6 (`useChat`) + Streamdown (alternative UI stack).
- `references/ui_fastapi_backend.md`: FastAPI backend patterns for in-process agents or Agent Server BFF/proxy.
- `references/ui_streaming_protocol.md`: simple SSE event protocol for custom UI backends.
- `references/ui_streamlit.md`: Streamlit UI integration patterns (streaming + HITL).

## Build workflow (LangChain v1 + LangGraph v1+)

1. Select the right multi-agent topology (start simple):
   - **Supervisor + subagents (tool-calling)**: a main “supervisor” calls subagents as tools for context isolation.
   - **Orchestrator-worker (fan-out)**: use LangGraph’s worker primitives (e.g., Send-style fanout) for parallelizable tasks; use reducers to avoid concurrent state-update errors.
   - **Deterministic workflow + agent nodes**: keep control-flow explicit; use agents only where needed.
2. Define strict tool schemas and failure behavior:
   - Make tools idempotent where possible; add timeouts and retries; “fail open” on non-critical model/rerank steps.
3. Do context engineering explicitly:
   - Use typed state for dynamic runtime context; keep “store” for long-term memory; use runtime context injection for user/org-scoped dependencies.
4. Add safety controls early:
   - Use middleware guardrails and human-in-the-loop for high-stakes tools (payments, outbound emails, destructive actions).
5. Add observability before scaling:
   - Enable tracing (LangSmith/OpenTelemetry), record tool latency/cost, and add regression evaluations.

Use `references/patterns.md` for design templates and “gotchas” per topology.

## Audit & migrate workflow (deprecated patterns → modern stack)

1. Inventory current architecture (dependencies + imports + runtime behavior):
   - Run `scripts/audit_repo_agents.py` and expand it with repo-specific patterns if needed.
2. Identify deprecated patterns and their replacements using official docs:
   - Prioritize the LangGraph v1 and LangChain v1 migration guides.
   - Verify whether `langgraph.prebuilt.create_react_agent` usage should move to `langchain.agents.create_agent`.
3. Plan the migration in slices (keep it shippable):
   - Preserve external behavior; migrate internals; then upgrade prompts/tools; finally tighten types and add tests.
4. Execute migration and harden:
   - Replace legacy agent frameworks (LlamaIndex agents, CrewAI, Agno, OpenAI Agents) with LangGraph/LangChain equivalents.
   - Add offline tests with fixtures/mocks, and add trace-based regression checks when possible.

Use `references/migration_supervisor.md` and `references/migration_other_frameworks.md` for playbooks.

## Performance & scale workflow

1. Add measurement first:
   - Capture per-node latency, token usage, tool call counts, cache hit rates, and error taxonomy.
2. Apply the “cheapest win” stack in order:
   - Reduce context size (summaries, retrieval, subagent isolation).
   - Cache tool results (deterministic and keyed); add request coalescing.
   - Parallelize only where state updates are safe (reducers, fanout collection keys).
   - Use smaller/faster models for routing/validation; reserve larger models for synthesis.
3. Constrain worst-case behavior:
   - Recursion limits, max steps, max tool calls, and circuit breakers for flaky dependencies.

Use `references/performance_cost.md` for checklists and tactics.

## Bundled resources in this skill

- `scripts/`: deterministic helpers (audits, `llms.txt` extraction, `opensrc` snapshot runner)
- `references/`: playbooks + templates for docs research, patterns, migrations, safety, observability, and performance
- `assets/`: copy/paste templates for Python + UI integrations (Next.js, FastAPI, Streamlit)

Start with `references/docs_index.md` and `references/research_playbook.md`.
