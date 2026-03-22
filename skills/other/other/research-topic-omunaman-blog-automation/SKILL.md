---
name: research-topic
description: "Deep research on a technical topic for blog writing. Use when user says research, look into, explore, or provides a blog topic to investigate. Searches the web extensively and creates structured research notes with visual opportunity identification."
allowed-tools: Bash, Read, Grep, Glob, WebFetch
---

# Deep Research Skill

## Input
$ARGUMENTS = the topic to research

## Process

### Step 1: Broad Search (5 to 8 searches)
Search the web for high-quality sources on the topic:
- Original research papers (arXiv, conference proceedings)
- Official documentation and blog posts from the creators
- Well-written technical blog posts (Lilian Weng, Jay Alammar, etc.)
- Video transcripts or lecture notes if available
- GitHub implementations for reference

### Step 2: Deep Read
For each promising source, use WebFetch to read the full content.
Extract and organize:

**Core Concepts**
- What is this? (one-paragraph definition)
- Why does it exist? What problem does it solve?
- What did it replace or improve upon?

**How It Works (Technical Depth)**
- Step-by-step mechanism
- Key equations and their intuition
- Concrete numerical examples (shapes, dimensions, values)
- Implementation details

**Comparisons and Alternatives**
- How does this compare to previous approaches?
- What are the trade-offs?
- Quantitative comparisons (benchmarks, memory savings, speedups)

**Historical Context**
- When was it introduced? By whom?
- What papers are most relevant?
- How has it evolved since introduction?

### Step 3: Identify Visual Opportunities
This is critical. For EVERY concept, ask: "Would a diagram help here?"
List 6 to 10 concepts that NEED visual diagrams:
- Architecture overviews
- Data flow through components
- Step-by-step process walkthroughs
- Before/after comparisons
- Matrix operations with concrete shapes
- Mathematical derivation steps

For each, write:
- Diagram name (e.g., "fig_mla_architecture")
- What it should show
- Type: architecture / flowchart / comparison / step-by-step / matrix-operation

### Step 4: Save Research Notes
Save to: `research/<topic-slug>.md`

Structure:
```
# Research: <Topic Name>

## Quick Summary
(2-3 sentence overview)

## Core Concepts
(detailed notes)

## How It Works
(step-by-step technical breakdown)

## Mathematical Foundation
(key equations with explanations)

## Comparisons and Alternatives
(vs previous approaches, with numbers)

## Visual Opportunities
(list of 6-10 diagrams needed with descriptions)

## Running Example
(define the simple example we will use throughout:
 e.g., 4 tokens, specific dimensions, concrete values)

## Key Sources
- [Paper Name](url) - what we extracted from it
- [Blog Post](url) - what we extracted from it
```

## Output
Save to research/<topic-slug>.md and summarize key findings to user.
Tell the user how many diagram opportunities were identified.
