---
name: doc-research-improvements
description: Research-driven critique and enhancement of Amelia architecture or ideas docs. Use with GPT-5.2 when given a design/architecture doc to analyze concepts, find sources, and propose improvements plus OSS candidates.
---

# Doc Research and Improvement (GPT-5.2)

Use this skill to analyze a single doc (architecture or idea), research its referenced concepts,
and propose improvements with external sources and implementation candidates.

## Input Parameters

| Parameter | Description | Required |
|---|---|---|
| `doc_path` | Path to the doc to analyze. | Required (unless `doc_text`) |
| `doc_text` | Raw doc content if not reading from file. | Optional |
| `focus_areas` | Comma list: architecture, data-model, orchestration, security, observability, testing, UX, scaling, cost. | Optional |
| `depth` | `quick` (top 3 items) or `standard` (top 5-8 items). | Optional |
| `constraints` | Explicit constraints to respect (ex: local-first, SQLite, no background jobs). | Optional |

## Repository Context (Align To)

These are core assumptions from `docs/site/architecture/*` and `docs/site/ideas/*`:

- Amelia is a local-first, agentic coding orchestrator with LangGraph, FastAPI, and SQLite.
- Primary workflow: Architect -> Developer -> Reviewer with human approval gates.
- Design principles: structured handoffs, verify before done, environment as truth.
- Drivers and trackers are pluggable abstractions.
- Ideas are exploratory; suggest improvements without assuming commitment.

Use these as guardrails when proposing changes.

## Required Workflow

1. **Ingest and summarize the doc**
   - Identify goals, scope, non-goals, and assumptions.
   - Note dependencies on current architecture or roadmap phases.

2. **Extract concepts, frameworks, and techniques**
   - List all explicit or implied frameworks (ex: LangGraph, RAG, SOX/ICFR, BDD).
   - Classify each as architecture, process, data, evaluation, or UI.

3. **Research and validate**
   - Use authoritative sources: specs, official docs, standards, reputable research.
   - Capture at least 1 source per key concept. If none, label as hypothesis.
   - Summarize evidence in 1-2 lines with citations.

4. **Propose improvements**
   - Prioritize items by impact and feasibility.
   - Provide rationale tied to evidence and Amelia constraints.
   - Include tradeoffs and risks.
   - Call out where changes touch existing modules (ex: `amelia/core/`, `amelia/server/`).

5. **Recommend OSS candidates**
   - Suggest open-source libraries or frameworks needed to implement changes.
   - Include license, maturity, and integration notes.
   - Prefer Python 3.12, FastAPI, React, SQLite compatible stacks.

## Output Format

**Doc Snapshot**
- Goal, scope, non-goals, assumptions

**Extracted Concepts**
| Concept | Category | Why it matters | Sources |

**Evidence and Research Notes**
- Bullet list of sources with 1-line relevance

**Improvements (Ranked)**
1. Title
   - Rationale + evidence (cite)
   - Tradeoffs/risks
   - Implementation notes (files/modules)

**OSS and Framework Candidates**
| Need | Options | License | Why it fits |

**Open Questions**
- Any missing inputs or decisions required

## Guardrails

- Do not contradict architecture principles unless the doc explicitly proposes it.
- If the doc is exploratory, frame improvements as experiments or phased probes.
- Avoid proprietary SaaS recommendations unless the doc already assumes them.
- No hallucinated citations; if unsure, say so and suggest verification.
