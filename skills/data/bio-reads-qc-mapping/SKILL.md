---
name: bio-reads-qc-mapping
description: Ingest, QC, and map reads with reproducible outputs. Use for raw read processing and coverage stats.
---

# Bio Reads QC Mapping

## When to use
- Ingest, QC, and map reads with reproducible outputs. Use for raw read processing and coverage stats.

## Prerequisites
- Tools installed via pixi (see pixi.toml).
- Sample sheet and reads are available.

## Inputs
- sample_sheet.tsv
- reads/*.fastq.gz
- reference.fasta (optional)

## Outputs
- results/bio-reads-qc-mapping/trimmed_reads/
- results/bio-reads-qc-mapping/qc_reports/
- results/bio-reads-qc-mapping/mapping_stats.tsv
- results/bio-reads-qc-mapping/coverage.tsv
- results/bio-reads-qc-mapping/logs/

## Steps
1. Parse sample sheet and validate inputs.
2. For short reads: Run QC/trimming (bbduk).
3. For long reads: Trim adapters (Porechop) and filter by quality/length (Filtlong).
4. Map reads (bbmap or minimap2) and generate coverage tables.

## QC gates
- Post-QC read count sanity checks pass.
- Mapping rate meets project thresholds.
- On failure: retry with alternative parameters; if still failing, record in report and exit non-zero.

## Validation
- Validate sample sheet schema and FASTQ integrity.

## Tools
- bbtools (bbduk, bbmap) v39.52
- minimap2 v2.30
- Filtlong (long read quality filtering)
- Porechop (Nanopore adapter trimming)

## Paper summaries (2023-2025)
- summaries/ (include example use cases and tool settings used)

## Tool documentation
- [BBDuk](docs/bbduk.html) - Quality trimming and adapter removal for short reads
- [BBMap](docs/bbmap.html) - Short read aligner and coverage calculator
- [Minimap2](docs/minimap2.html) - Long read aligner
- [Filtlong](docs/filtlong.html) - Long read quality filtering
- [Porechop](docs/porechop.html) - Nanopore adapter trimming

## References
- See ../bio-skills-references.md
