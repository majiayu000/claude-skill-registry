---
name: bio-gene-calling
description: Call genes and annotate basic features for prokaryotes, viruses, and eukaryotes.
---

# Bio Gene Calling

## When to use
- Call genes and annotate basic features for prokaryotes, viruses, and eukaryotes.

## Prerequisites
- Tools installed via pixi (see pixi.toml).
- Input contigs or bins are available.

## Inputs
- contigs.fasta or bins/*.fasta

## Outputs
- results/bio-gene-calling/genes.gff3
- results/bio-gene-calling/proteins.faa
- results/bio-gene-calling/cds.fna
- results/bio-gene-calling/gene_metrics.tsv
- results/bio-gene-calling/logs/

## Steps
1. Select gene caller by organism class.
2. Run gene calling and produce GFF/FAA/FNA.
3. Detect tRNAs/rRNAs if requested.

## QC gates
- Gene count sanity checks pass.
- Start/stop codon checks pass.
- On failure: retry with alternative parameters; if still failing, record in report and exit non-zero.

## Validation
- Verify contigs are non-empty and DNA alphabet.
- Verify outputs contain expected feature types.

## Tools
- pyrodigal v3.7.0
- prodigal-gv v2.11.0
- braker v3.0.8
- augustus v3.5.0
- trnascan-se v2.0.12

## Paper summaries (2023-2025)
- summaries/ (include example use cases and tool settings used)

## Tool documentation
- [Pyrodigal](docs/pyrodigal.html) - Fast prokaryotic gene prediction
- [Prodigal-gv](docs/prodigal-gv.html) - Gene prediction for giant viruses
- [BRAKER](docs/braker.html) - Eukaryotic gene prediction pipeline
- [AUGUSTUS](docs/augustus.html) - Eukaryotic gene prediction
- [tRNAscan-SE](docs/trnascan-se.html) - Transfer RNA gene detection

## References
- See ../bio-skills-references.md
