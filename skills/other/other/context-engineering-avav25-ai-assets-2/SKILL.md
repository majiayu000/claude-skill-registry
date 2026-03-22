---
name: context-engineering
description: Context engineering knowledge base — context stack architecture (8-layer model), memory engineering (taxonomy, CRUD, conflict resolution, compression), agent harness patterns (init/continuation, state blobs, token budgeting, caching, failure modes), RAG pipeline design (chunking, packing, degradation signals), multi-agent orchestration (boundaries, payload schemas, fan-out patterns), production AI checklists (8 checklists), reference implementation templates (grounding envelope, untrusted wrapper, tool error envelope), privacy and compliance for AI systems. Use when designing AI agent systems, reviewing context quality, building RAG pipelines, implementing memory, planning multi-agent architectures, or preparing AI systems for production.
user-invocable: true
---

# Context Engineering

Context engineering is the discipline of **systematically selecting, structuring, and delivering the smallest possible set of high-signal tokens** that make a task plausibly solvable for an LLM — reliably, safely, and cost-effectively.

This skill provides actionable patterns, checklists, and templates for the full context pipeline — from first principles through production readiness.

## When to Use

- Designing context pipelines for AI agents (what enters the LLM context window, in what order)
- Reviewing context quality and token efficiency of existing systems
- Building RAG systems (retrieval pipeline, chunking, packing, grounding)
- Implementing memory (session, working, long-term, organizational, tool-output)
- Designing agent harness (init/continuation prompts, state management, token budgets, caching)
- Multi-agent orchestration (context boundaries, payload schemas, fan-out merge)
- Production readiness assessment for AI systems (8-checklist gate)
- Privacy and compliance for AI features (multi-tenant isolation, consent, data residency)

## When NOT to Use

- Prompt technique selection and template patterns → use `prompt-engineering` skill
- Security audit of individual prompts → use `prompt-engineering` skill → `security-checklist.md`
- Non-AI software engineering tasks → use `Agent(software-engineer)` + stack-specific role
- Infrastructure and deployment → use `Agent(devops-engineer)`

## Context Engineering vs Prompt Engineering

These are **complementary** disciplines:

- **Prompt engineering** = designing the instruction text (technique selection, template patterns, formatting, few-shot)
- **Context engineering** = designing the full context PIPELINE (what enters the window, in what order, how it's managed across turns, how it degrades gracefully)

Context engineering is the **system**; prompt engineering is one **layer** within it.

## Key Concepts

### First Principles

1. **Attention is finite** — curate, don't stuff. "More context" is not monotonically better
2. **Position effects** — critical info at beginning and end ("lost-in-the-middle"). Models use tokens near the start and end more effectively than those buried in the middle
3. **High-signal tokens > high-volume tokens** — compact, discriminative context beats verbose dumps
4. **Separation of concerns** — policy, knowledge, examples, output contract in distinct layers. Enables independent swap, A/B testing, failure analysis
5. **Context is a pipeline** — produced by a system (retrieval, ranking, summarization, memory, policy filters, schema enforcement), not concatenated strings

### The Context Stack (8-Layer Architecture)

Ordered layers, top = highest priority. Higher layers override lower on conflict.

| Layer | What Goes Here | Design Notes |
|---|---|---|
| 1. System policy & safety | Non-negotiable constraints, content policies, refusal rules | First in window — highest attention. Cacheable |
| 2. Developer instructions | Role definitions, hard rules, reasoning protocols, conventions | Maps to: Claude Code rules ((auto-loaded), (agent)) |
| 3. Tool contracts | Schemas, descriptions, permissions, failure modes, retry policies | Tool descriptions ARE prompts — optimize them |
| 4. Runtime state | Current project context, CLAUDE.md, active file, task state, structured state blob | Maps to: Claude Code CLAUDE.md files |
| 5. Knowledge context (RAG) | Retrieved documents, search results, file contents | Must be wrapped as untrusted data with grounding envelopes |
| 6. Memory | Session, working, long-term, organizational, tool-output | Must be scoped, filtered, and conflict-resolved |
| 7. Examples (few-shot) | Minimal, high-leverage exemplars aligned to output contract | Dynamic selection preferred; skip if schema suffices |
| 8. Output contract | JSON Schema, format instructions, constraints, error handling | End of context — recency bias helps compliance |

**Rule**: keep **policy/instructions** (Layers 1-2) separate from **knowledge** (Layer 5). Mixing them is a root cause of prompt injection and "obedience confusion."

→ Full reference: `context-stack-model.md`

### Cacheable Prefix Design

Layers 1-3 rarely change → group all static content at the beginning of the prompt to enable KV cache reuse. Append dynamic content (Layer 4-8) at the end. Never interleave static and dynamic blocks.

Track `cache_prefix_ratio = cached_tokens / total_input_tokens` (target > 0.3).

### Token Budget Allocation

Treat context window as a finite resource with explicit budget per layer:

| Allocation | Suggested % | Notes |
|---|---|---|
| System + rules + tools (L1-3) | 15-25% | Stable, cacheable prefix |
| Runtime state (L4) | 5-10% | Structured state blob |
| Knowledge / RAG (L5) | 30-40% | Dynamic, highest signal variance |
| Memory (L6) | 10-15% | Filtered, relevance-ranked |
| Examples (L7) | 0-10% | Only when needed |
| Output contract (L8) | 5-10% | Schema + error handling |

Overflow strategy: truncate lowest-priority layers first (L7 → L6 → L5).

## Resource Files

| File | Contents | Guide §§ |
|---|---|---|
| `context-stack-model.md` | 8-layer architecture, layer design patterns, position effects, mapping to Claude Code assets | §3 |
| `memory-engineering.md` | Memory taxonomy, CRUD lifecycle, conflict handling, compression strategies | §6 |
| `agent-harness-patterns.md` | Init/continuation, state blobs, token budgets, caching, failure modes, streaming | §7 |
| `rag-engineering.md` | Pipeline blueprint (7 stages), chunking, packing, degradation signals | §5 |
| `multi-agent-patterns.md` | Context boundaries, payload schemas, return contracts, fan-out, contamination | §7.6, §14 |
| `production-checklists.md` | All 8 production readiness checklists | §11 |
| `reference-templates.md` | Grounding envelope, untrusted wrapper, structured output, tool error envelope | §12 |
| `privacy-compliance-ai.md` | Multi-tenant isolation, data controls, consent, regional compliance | §9 |

## Integration

- **Follows rules**: `Agent(prompt-engineer)` (prompt-level techniques, security, eval-first quality)
- **Used by workflows**: `/ai-assets` (context engineering validation), `/feature-dev` (AI features), `/feature-plan` (AI work packages), `/code-review` (context quality review)
- **Companion skill**: `prompt-engineering` skill (technique selection, template patterns, eval, security checklist)
- **Collaborates with roles**: `Agent(solution-architect)` (AI system design), `Agent(product-manager)` (agent contracts), `Agent(sre-engineer)` (context observability), `Agent(software-engineer)` (implementation)
- **Primary source**: `guides/context_engineering_guide.md`
