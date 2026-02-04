---
name: bio-viromics
description: Detect, classify, and QC viral contigs.
---

# Bio Viromics

## When to use
- Detect, classify, and QC viral contigs.

## Prerequisites
- Tools installed via pixi (see pixi.toml).
- Reference DB root: /media/shared-expansion/db/ (wsu; override per machine branch).
- Input contigs are available.

## Inputs
- contigs.fasta

## Outputs
- results/bio-viromics/viral_contigs.fasta
- results/bio-viromics/checkv_results/
- results/bio-viromics/vcontact3_results/
- results/bio-viromics/viral_taxonomy.tsv
- results/bio-viromics/genome_clusters.tsv
- results/bio-viromics/viromics_report.md
- results/bio-viromics/logs/

## Steps
1. Run virus detection (geNomad).
2. Run CheckV for completeness/contamination.
3. Assign taxonomy and cluster genomes (vConTACT3 for hierarchical classification and gene-sharing network analysis).

## QC gates
- CheckV quality thresholds meet project standards.
- Contamination flags are below thresholds.
- On failure: retry with alternative parameters; if still failing, record in report and exit non-zero.

## Validation
- Verify contigs.fasta is non-empty.
- Verify viral reference DBs exist under the reference root.

## Tools
- genomad v1.11.2
- checkv v1.0.3
- vcontact3 v3.0.1
- gvclass v1.2.0 (internal build tag)

## Paper summaries (2023-2025)
- summaries/ (include example use cases and tool settings used)

## Tool documentation
- [geNomad](docs/genomad.html) - Viral sequence identification and classification
- [CheckV](docs/checkv.html) - Viral genome quality assessment
- [vConTACT3](docs/vcontact3.html) - Viral taxonomy and clustering via gene-sharing networks
- [GVClass](docs/gvclass.html) - Giant virus classification

## References
- See ../bio-skills-references.md
