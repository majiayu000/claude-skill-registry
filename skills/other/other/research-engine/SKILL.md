---
name: research-engine
description: Autonomous research pipeline — topic to structured documents with HTML/PDF output. Proven at HEL (28 docs, 91K words) and OOPS (9 docs, 20K words) scale.
version: 1.0.0
---

# Research Engine

Activates when user requests deep research, investigation, or analysis of a topic that will produce multiple structured documents.

## Pipeline

```
TOPIC → DECOMPOSE → PARALLEL RESEARCH → AGGREGATE → STRUCTURE → BUILD → PUBLISH
```

### Stage 1: Decompose
Break the research topic into 4-12 investigation tracks. Each track becomes one document.

### Stage 2: Parallel Research
Launch research agents (2-6 in parallel) with specific investigation briefs. Use `run_in_background: true` for independence.

### Stage 3: Aggregate
Collect findings. Check for contradictions. Identify cross-references.

### Stage 4: Structure
Organize into a numbered document series with:
- Index page (index.html)
- Individual research documents (research/NN-slug.md)
- Knowledge graph (knowledge-nodes.json)
- Retrospective (retrospective.md)

### Stage 5: Build
Convert markdown to HTML and PDF using pandoc + xelatex:
```bash
bash build.sh  # Uses template.tex and html-template.html
```

### Stage 6: Publish
Commit, tag, merge to main, push, create GitHub release, FTP sync to tibsfox.com.

## Quality Standards

- Minimum 1,500 words per document
- Every claim needs evidence or explicit reasoning
- Cross-references between documents
- Fact-check pass before final publish
- Three output formats: markdown (source), HTML (reading), PDF (sharing)

## Project Codes

Each research project gets a 3-4 letter code added to series.js:
- HEL (Helium Supply Chain)
- OOPS (Ecosystem Alignment)
- OPEN (Unsolved Problems)

## Build Infrastructure

Templates at the project level:
- `template.tex` — LaTeX template for branded PDFs
- `html-template.html` — Standalone HTML template
- `build.sh` — Automated pandoc build script
