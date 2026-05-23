---
name: bip-extract-refs
description: Extract paper references and concepts from a LaTeX repository for the bipartite knowledge graph.
---

# Extract References from LaTeX Repository

Analyze a LaTeX repository to extract papers and concepts for the bipartite knowledge graph.

## Usage

```
/bip-extract-refs <path-to-tex-repo>
```

## What This Skill Does

1. **Reads** `main.bib` and `main.tex` from the specified repository
2. **Extracts** citation keys and their context from the manuscript
3. **Identifies** key concepts and potential relationships
4. **Filters out** software/tool citations (e.g., packages, libraries)
5. **Returns** a structured summary with:
   - Papers found (using BibTeX citation keys as bip IDs)
   - Suggested concepts to create
   - Potential edges to add

## Workflow

Given a path like `../dasm-tex-1`, perform this analysis:

### Step 1: Read the BibTeX file

```bash
cat <repo>/main.bib
```

Extract citation keys (the part after `@article{` or `@inproceedings{`, etc.).

### Step 2: Read the manuscript

```bash
cat <repo>/main.tex
```

Look for:
- `\cite{...}` commands and their surrounding context
- Section structure to understand paper focus
- Key methodological terms

### Step 3: Identify Concepts

Look for recurring themes that could become concept nodes:
- Methods mentioned repeatedly
- Domain-specific terms
- Mathematical frameworks
- Data types or experimental approaches

### Step 4: Generate Output

Produce a structured summary:

```json
{
  "papers": [
    {"id": "Smith2026-ab", "role": "foundational", "context": "Defines the X model"},
    {"id": "Jones2025-xy", "role": "applies", "context": "Uses X for Y analysis"}
  ],
  "suggested_concepts": [
    {"id": "x-model", "name": "X Model", "description": "Statistical framework for..."},
    {"id": "y-analysis", "name": "Y Analysis", "description": "Method for..."}
  ],
  "suggested_edges": [
    {"source": "Smith2026-ab", "target": "x-model", "type": "introduces", "summary": "Foundational paper"},
    {"source": "Jones2025-xy", "target": "x-model", "type": "applies", "summary": "Application to Y"}
  ]
}
```

## Filtering Rules

**Skip these citation types:**
- Software packages (R packages, Python libraries)
- Datasets without methodology
- Generic references (textbooks, review articles) unless central to the paper
- Self-citations to prior versions of the same work

**Prioritize these:**
- Papers that introduce methods used in the manuscript
- Papers being compared against
- Foundational papers for the domain
- Papers being extended or built upon

## Integration with bip

After running this skill, use the output to update the knowledge graph:

```bash
# Check which papers exist in bip
bip get Smith2026-ab

# Create suggested concepts
bip concept add x-model --name "X Model" --description "..."

# Add edges
bip edge add -s Smith2026-ab -t x-model -r introduces -m "Foundational paper"
```

## Example Session

```
User: /bip-extract-refs ../dasm-tex-1

Claude: I'll analyze the LaTeX repository to extract references and concepts.

[Reads main.bib and main.tex]

Found 45 citations in main.bib. Here's my analysis:

**Key Papers** (12 identified as significant):
1. Halpern1998-yc - introduces mutation-selection model
2. Yaari2013-dg - introduces S5F targeting model
...

**Suggested Concepts** (4):
1. `mutation-selection-model` - Framework for codon substitution
2. `shm-targeting` - Somatic hypermutation targeting patterns
...

**Suggested Edges** (8):
- Halpern1998-yc --[introduces]--> mutation-selection-model
- Yaari2013-dg --[introduces]--> shm-targeting
...

Would you like me to:
1. Check which papers are already in your bip library?
2. Create these concepts and edges?
```
