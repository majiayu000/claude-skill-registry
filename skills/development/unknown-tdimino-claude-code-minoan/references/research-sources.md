# Research Sources

Sources synthesized into the dag-typesafe skill architecture.

## Academic Papers

- **GraphSentry** — Li, Cao, Liu, Duprey, Ge (Feb 2026). "Contract-Checked Graph Surgery for Budgeted LLM Reasoning DAGs." Research Square rs-8912156. Certificate-driven topology search; grammar-generated typed DAGs; (artifact, certificate) pairs; contract-checked graph surgery; +5.3–10.8pts accuracy, 29–45% token reduction.

- **ChopChop** — Nagy, Zhou, Polikarpova, D'Antoni (POPL 2026). "A Programmable Framework for Semantically Constraining the Output of Language Models." arxiv 2509.00360. First framework for semantic constrained decoding; enforces type safety and program equivalence during generation via coinductive realizability analysis.

- **Agint** — Chivukula, Somasundaram, Somasundaram (Nov 2025). "Agentic Graph Compilation for Software Engineering Agents." arxiv 2511.19635. Typed, effect-aware code DAGs; type floors (text→data→spec→code); Unix toolchain (dagify, dagent, schemagin, datagin).

- **CRANE** (Feb 2025, ICML 2025). Alternating constrained/unconstrained decoding windows; recovers up to 10pts on symbolic reasoning benchmarks.

## Tools & Frameworks

- **PlanCompiler** — prnvh (Feb 2026). github.com/prnvh/plancompiler. Constraint-guided program synthesis over typed node libraries. LLM confined to node selection + parameterization; deterministic compilation to executable Python.

- **PlanAI** — Provos (Mar 2026). starlog.is/articles/llm-engineering/provos-planai. Type-safe workflow orchestration with Pydantic-typed DAG nodes. Automatic type-aware routing.

- **ChainWeaver** — dgenio (Mar 2026). github.com/dgenio/ChainWeaver. Deterministic MCP tool flows compiled into LLM-free executable flows.

- **ax-llm/ax** (Mar 2026). deepwiki.com/ax-llm/ax/5.4-type-system-and-compile-time-safety. TypeScript compile-time type safety for LLM pipelines via signatures and field constraints.

- **XGrammar** (CMU, 2024–2025). <40µs token mask generation for constrained decoding.

- **llguidance** (Microsoft). Rust grammar engine for SGLang constrained decoding.

## Architecture & Analysis

- **Zylos Research** (Apr 2026). "Structured Output and Constrained Decoding for Production AI Agents (2026)." State of the art survey.

- **Axiom Logica** (Mar 2026). "Deterministic Routing in Probabilistic DAGs: Handling Multi-Agent Reasoning."

- **A11** — Gormenz (Feb 2026). "A Deterministic Reasoning Architecture for Autonomous Systems and LLM-Based Agents." Verifiable decision paths, rollback, bounded recursion.

- **Engram** — Jelínek (Apr 2026). "A Deterministic Operations Layer for LLM Agent Workflows." Evolving directed graph of confirmed resolution patterns; confidence-weighted edges.

- **Brenndoerfer** (Jul 2025). "Constrained Decoding: Grammar-Guided Generation for Structured LLM Output." Interactive guide.
