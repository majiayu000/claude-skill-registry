---
name: context-engineering
description: Context engineering knowledge base for designing context stacks, memory, retrieval, orchestration, and AI system reliability in a Windsurf-compatible way.
---

# Context Engineering

Use this skill when designing or reviewing how context is assembled for AI systems.

## Use Cases

- Context stack design
- Retrieval and RAG planning
- Memory design
- Multi-step orchestration
- AI system reliability reviews

## Core Principle

Deliver the smallest high-signal context that makes the task solvable and safe.

## Layers

Think in layers:

1. System policy
2. Developer instructions
3. Tool contracts
4. Runtime state
5. Retrieved knowledge
6. Memory
7. Examples
8. Output contract

## Repository Mapping

- Root and scoped `AGENTS.md` -> developer instructions and runtime context
- `.windsurf/skills/*` -> reusable task workflows and knowledge
- Project files and retrieved docs -> knowledge context
- Structured outputs or explicit response formats -> output contract

## Companion Resources

- `context-stack-model.md`
- `memory-engineering.md`
- `agent-harness-patterns.md`
- `rag-engineering.md`
- `multi-agent-patterns.md`
- `production-checklists.md`
- `reference-templates.md`
- `privacy-compliance-ai.md`