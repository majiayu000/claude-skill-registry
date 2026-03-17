---
name: architectural-forensics
description: Master protocol for deconstructing agent frameworks to inform derivative system architecture. Use when (1) analyzing an agent framework's codebase comprehensively, (2) comparing multiple frameworks to select best practices, (3) designing a new agent system based on prior art, (4) documenting architectural decisions with evidence, or (5) conducting technical due diligence on AI agent implementations. This skill orchestrates sub-skills for data substrate, execution engine, cognitive architecture, and synthesis phases.
---

# Architectural Forensics Protocol

Deconstruct agent frameworks to inform derivative system architecture.

## Mission

Distinguish between **software engineering decisions** (how it runs) and **cognitive architecture decisions** (how it thinks) to extract reusable patterns for new systems.

## Quick Start

```bash
# 1. Map the codebase (uses codebase-mapping skill's script)
python .claude/skills/codebase-mapping/scripts/map_codebase.py /path/to/framework --output codebase-map.json

# 2. Run analysis via the command
/analyze-frameworks
```

## Protocol Phases

### Phase 1: Engineering Chassis

Analyze the software substrate. See `references/phase1-engineering.md` for detailed guidance.

| Analysis | Focus Files | Output |
|----------|-------------|--------|
| Data Substrate | types.py, schema.py, state.py | Typing strategy, mutation patterns |
| Execution Engine | runner.py, executor.py, agent.py | Async model, control flow topology |
| Component Model | base_*.py, interfaces.py | Abstraction depth, DI patterns |
| Resilience | executor.py, try/except blocks | Error propagation, sandboxing |

### Phase 2: Cognitive Architecture

Extract agent "business logic". See `references/phase2-cognitive.md` for detailed guidance.

| Analysis | Focus Files | Output |
|----------|-------------|--------|
| Control Loop | agent.py, loop.py | Reasoning pattern, step function |
| Memory | memory.py, context.py | Context assembly, eviction policies |
| Tool Interface | tool.py, functions.py | Schema generation, error feedback |
| Harness-Model Protocol | llm.py, adapters/, stream.py | Wire format, tool call encoding, agentic primitives |
| Multi-Agent | orchestrator.py, router.py | Coordination model, state sharing |

### Phase 3: Synthesis

Generate actionable outputs:

1. **Best-of-Breed Matrix** → Framework comparison table
2. **Anti-Pattern Catalog** → "Do Not Repeat" list
3. **Reference Architecture** → New framework specification

## Execution Workflow

```
┌─────────────────────────────────────────────────────────┐
│                    For Each Framework                    │
├─────────────────────────────────────────────────────────┤
│  1. codebase-mapping                                    │
│       ↓                                                 │
│  2. Phase 1 Analysis (parallel)                         │
│     ├── data-substrate-analysis                         │
│     ├── execution-engine-analysis                       │
│     ├── component-model-analysis                        │
│     └── resilience-analysis                             │
│       ↓                                                 │
│  3. Phase 2 Analysis (parallel)                         │
│     ├── control-loop-extraction                         │
│     ├── memory-orchestration                            │
│     ├── tool-interface-analysis                         │
│     ├── harness-model-protocol                          │
│     └── multi-agent-analysis (if applicable)            │
└─────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────┐
│                      Synthesis                           │
├─────────────────────────────────────────────────────────┤
│  4. comparative-matrix                                   │
│  5. antipattern-catalog                                  │
│  6. architecture-synthesis                               │
└─────────────────────────────────────────────────────────┘
```

## Quick Analysis (Single Framework)

For rapid assessment, run the minimal path:

```
codebase-mapping → execution-engine-analysis → control-loop-extraction → tool-interface-analysis
```

## Output Directory Structure

```
forensics-output/                    # Working/intermediate files
├── .state/
│   ├── manifest.json
│   └── {framework}.state.json
└── frameworks/
    └── {framework}/
        ├── codebase-map.json
        ├── phase1/*.md
        └── phase2/*.md

reports/                             # Final deliverables
├── frameworks/
│   └── {framework}.md               # Framework summary
└── synthesis/
    ├── comparison-matrix.md
    ├── antipatterns.md
    ├── reference-architecture.md
    └── executive-summary.md
```

## State Management & Resumption

The protocol is designed to be stateful and resumable. 

- **Idempotency**: The Orchestrator tracks progress in `manifest.json` and will skip frameworks marked as `completed`.
- **Clean Slate Resumption**: If a run is interrupted, frameworks marked as `in_progress` are considered "stale". Use `python scripts/state_manager.py reset-running` to move them back to `pending` and delete their partial output directories, ensuring a clean restart for those items.

## Agent Orchestration

This skill uses a **4-tier hierarchy** of specialized agents for context efficiency:

```
Orchestrator
    │
    └── Framework Agents (parallel, one per framework)
            │
            └── Skill Agents (parallel, one per skill) [COORDINATORS]
                    │
                    └── Reader Agents (parallel, one per file cluster) [EXTRACTORS]
                            │
                            └── Synthesis Agent (cross-framework synthesis)
```

### Agent Roles

| Agent | Context Budget | Reads | Produces |
|-------|---------------|-------|----------|
| **Orchestrator** | ~10K | State files | Coordination decisions |
| **Framework Agent** | ~50K | Skill outputs | Framework summary report |
| **Skill Agent** | ~25K | Cluster extracts | Skill analysis report |
| **Reader Agent** | ~20K | 1-5 source files | JSON extract (~2K) |
| **Synthesis Agent** | ~40K | All framework reports | Comparison matrix, architecture spec |

### Key Innovation: Cluster-Based Reading

Reader Agents read **file clusters** (1-5 related files) rather than individual files:
- Clusters are grouped by relationship: hierarchy, module cohort, type+usage, interface+impl
- Cross-file patterns (inheritance, imports, shared state) are captured in the extract
- This enables understanding architectural patterns that span multiple files

See:
- `references/orchestrator-agent.md` — Top-level coordination
- `references/framework-agent.md` — Per-framework analysis coordination
- `references/skill-agent.md` — Skill coordination and cluster assignment
- `references/reader-agent.md` — File cluster extraction
- `references/synthesis-agent.md` — Cross-framework synthesis

## Sub-Skill Reference

| Skill | Purpose | Key Outputs |
|-------|---------|-------------|
| `codebase-mapping` | Repository structure | File tree, dependencies, entry points |
| `data-substrate-analysis` | Type system | Typing strategy, serialization |
| `execution-engine-analysis` | Control flow | Async model, event architecture |
| `component-model-analysis` | Extensibility | Abstraction patterns, DI |
| `resilience-analysis` | Error handling | Error propagation, sandboxing |
| `control-loop-extraction` | Reasoning loop | Pattern classification, step function |
| `memory-orchestration` | Context management | Assembly, eviction, tiers |
| `tool-interface-analysis` | Tool system | Schema gen, error feedback |
| `harness-model-protocol` | LLM interface layer | Wire format, encoding, agentic primitives |
| `multi-agent-analysis` | Coordination | Handoffs, state sharing |
| `comparative-matrix` | Comparison | Decision tables |
| `antipattern-catalog` | Tech debt | Do-not-repeat list |
| `architecture-synthesis` | New design | Reference spec |
