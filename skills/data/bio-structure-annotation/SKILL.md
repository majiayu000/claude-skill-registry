---
name: bio-structure-annotation
description: Structure prediction and structure-based annotation.
---

# Bio Structure Annotation

## When to use
- Structure prediction and structure-based annotation.

## Prerequisites
- Tools installed via pixi (see pixi.toml).
- Reference DB root: /media/shared-expansion/db/ (wsu; override per machine branch).
- Protein FASTA inputs are available.

## Inputs
- proteins.faa (FASTA protein sequences)

## Outputs
- results/bio-structure-annotation/structures/
- results/bio-structure-annotation/structure_hits.tsv
- results/bio-structure-annotation/structure_report.md
- results/bio-structure-annotation/logs/

## Steps
1. Run fast embedding screen (tm-vec).
2. Predict structures (boltz or colabfold) as needed.
3. Search structures with Foldseek and annotate hits.

## QC gates
- Prediction success rate meets project thresholds.
- Search hit thresholds meet project thresholds.
- On failure: retry with alternative parameters; if still failing, record in report and exit non-zero.

## Validation
- Verify proteins.faa is non-empty and amino acid encoded.
- Verify Foldseek databases exist under the reference root.

## Tools
- tm-vec v1.0.3
- boltz v2.2.1
- colabfold v1.5.5
- foldseek v10-941cd33

## Paper summaries (2023-2025)
- summaries/ (include example use cases and tool settings used)

## Tool documentation
- [TM-Vec](docs/tm-vec.html) - Fast protein structure embedding and similarity search
- [Boltz](docs/boltz.html) - AI-based protein structure prediction
- [ColabFold](docs/colabfold.html) - Fast protein structure prediction using AlphaFold2
- [Foldseek](docs/foldseek.html) - Fast structure-based protein search

## References
- See ../bio-skills-references.md
