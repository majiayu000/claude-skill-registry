---
name: bio-assembly-qc
description: Assemble genomes/metagenomes and produce assembly QC artifacts.
---

# Bio Assembly QC

## When to use
- Assemble genomes/metagenomes and produce assembly QC artifacts.

## Prerequisites
- Tools installed via pixi (see pixi.toml).
- Sufficient disk and RAM for chosen assembler.

## Inputs
- reads/*.fastq.gz (raw reads).
- assembler choice (spades | flye).

## Outputs
- results/bio-assembly-qc/contigs.fasta
- results/bio-assembly-qc/assembly_metrics.tsv
- results/bio-assembly-qc/qc_report.html
- results/bio-assembly-qc/logs/

## Steps
1. Select assembler based on read type and genome size.
2. Run assembly with resource-aware settings.
3. Run QUAST/MetaQUAST and summarize metrics.

## QC gates
- Assembly size range and N50 distribution meet project thresholds.
- On failure: retry with alternative parameters; if still failing, record in report and exit non-zero.

## Validation
- Verify reads are present and gzip-readable.
- Check available disk space before assembly.

## Tools
- spades v4.2.0
- flye v2.9.6
- quast v5.3.0

## Paper summaries (2023-2025)
- summaries/ (include example use cases and tool settings used)

## Tool documentation
- [SPAdes](docs/spades.md) - De novo genome/metagenome assembler
- [Flye](docs/flye.md) - Long-read assembly for PacBio and Nanopore
- [QUAST](docs/quast.html) - Assembly quality assessment and metrics

## References
- See ../bio-skills-references.md
