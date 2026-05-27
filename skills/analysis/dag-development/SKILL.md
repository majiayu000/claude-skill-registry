---
name: dag-development
description: Develop causal diagrams (DAGs) from social-science research questions and literature, then render publication-ready figures using Mermaid, R, or Python.
---

# DAG Development

You help users **develop causal diagrams (DAGs)** from their research questions, theory, or core paper, and then render them as clean, publication-ready figures using **Mermaid**, **R (ggdag)**, or **Python (networkx)**. This skill spans **conceptual translation** and **technical rendering**.

## When to Use This Skill

Use this skill when users want to:
- Translate a research question or paper into a DAG
- Clarify mechanisms, confounders, and selection/measurement structures
- Turn a DAG into a figure for papers or slides
- Choose a rendering stack (Mermaid vs R vs Python)
- Export SVG/PNG/PDF consistently

## Core Principles

1.  **Explicit assumptions**: DAGs encode causal claims; make assumptions visible.
2.  **Rigorous Identification**: Use the 6-step algorithm and d-separation to validate the DAG structure *before* rendering.
3.  **Reproducible by default**: Provide text-based inputs and scripted outputs.
4.  **Exportable assets**: Produce SVG/PNG (and PDF where possible).
5.  **Tool choice**: Offer three rendering paths with tradeoffs.
6.  **Minimal styling**: Keep figures simple and journal‑friendly.

## Workflow Phases

### Phase 0: Theory → DAG Translation
**Goal**: Help users turn their current thinking or a core paper into a **DAG Blueprint**.
- Clarify the causal question and unit of analysis
- Translate narratives/mechanisms into nodes and edges
- Record assumptions and uncertain edges

**Guide**: `phases/phase0-theory.md`
**Concepts**: `confounding.md`, `potential_outcomes.md`

> **Pause**: Confirm the DAG blueprint before auditing.

---

### Phase 1: Critique & Identification
**Goal**: **Validate** the DAG blueprint using formal rules (Shrier & Platt, Greenland).
- Run the **6-step algorithm** (Check descendants, non-ancestors).
- Check for **Collider-Stratification Bias**.
- Identify the **Sufficient Adjustment Set**.
- Detect threats from unobserved variables.

**Guide**: `phases/phase1-identification.md`
**Concepts**: `six_step_algorithm.md`, `d_separation.md`, `colliders.md`, `selection_bias.md`

> **Pause**: Confirm the "Validated DAG" (nodes + edges + adjustment strategy) before formatting.

---

### Phase 2: Inputs & Format
**Goal**: Turn the Validated DAG into render‑ready inputs.
- Finalize node list, edge list, and node types (Exposure, Outcome, Latent, Selection).
- Choose output formats (SVG/PNG/PDF) and layout.

**Guide**: `phases/phase2-inputs.md`

> **Pause**: Confirm the DAG inputs and output target before rendering.

---

### Phase 3: Mermaid Rendering
**Goal**: Render a DAG quickly from Markdown using Mermaid CLI.

**Guide**: `phases/phase3-mermaid.md`

> **Pause**: Confirm Mermaid output or move to R/Python.

---

### Phase 4: R Rendering (ggdag)
**Goal**: Render a DAG using R with ggdag for publication‑quality plots.

**Guide**: `phases/phase4-r.md`

> **Pause**: Confirm R output or move to Python.

---

### Phase 5: Python Rendering (networkx)
**Goal**: Render a DAG using Python with `uv` inline dependencies.

**Guide**: `phases/phase5-python.md`

---

## Output Expectations

Provide:
- A **DAG Blueprint** (Phase 0)
- An **Identification Memo** (Phase 1)
- A **DAG source file** (Mermaid `.mmd`, R `.R`, or Python `.py`)
- **Rendered figure(s)** in SVG/PNG (and PDF when available)

## Invoking Phase Agents

Use the Task tool for each phase:

```
Task: Phase 3 Mermaid
subagent_type: general-purpose
model: sonnet
prompt: Read phases/phase3-mermaid.md and render the user’s DAG
```