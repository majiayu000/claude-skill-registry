---
name: bio-binning-qc
description: Perform metagenomic binning, refinement, and QC with completeness/contamination checks.
---

# Bio Binning QC

## When to use
- Perform metagenomic binning, refinement, and QC with completeness/contamination checks.

## Prerequisites
- Tools installed via pixi (see pixi.toml).
- Reference DB root: /media/shared-expansion/db/ (wsu; override per machine branch).
- Coverage/depth tables or reads available to compute coverage.

## Inputs
- contigs.fasta
- coverage.tsv (per-sample depth table)

## Outputs
- results/bio-binning-qc/bins/
- results/bio-binning-qc/bin_metrics.tsv
- results/bio-binning-qc/bin_qc_report.html
- results/bio-binning-qc/logs/

## Steps
1. Compute depth/coverage per sample.
2. Run multiple binners (MetaBAT2, SemiBin2, QuickBin).
3. Classify bins by domain (bacteria/archaea vs eukaryotes).
4. Run domain-specific QC:
   - CheckM2 for bacterial and archaeal bins
   - EukCC for eukaryotic bins
   - GUNC for contamination detection (all domains).

## QC gates
- Completeness and contamination meet project thresholds.
- Chimera and contamination flags are below thresholds.
- On failure: retry with alternative parameters; if still failing, record in report and exit non-zero.

## Validation
- Verify contigs.fasta and coverage.tsv are non-empty.
- Verify reference DBs for QC tools exist under the reference root.

## Tools
- coverm v0.7.0 (coverage computation)
- metabat2 v2.18 (binning)
- semibin2 v2.2.1 (binning)
- bbtools (quickbin) v39.52 (binning)
- checkm2 v1.0.2 (QC for bacteria/archaea)
- eukcc v2.x (QC for eukaryotes)
- gunc v1.0.6 (contamination detection)

## Paper summaries (2023-2025)
- summaries/ (include example use cases and tool settings used)

## Tool documentation
- [CoverM](docs/coverm.html) - Coverage and depth calculation
- [MetaBAT2](docs/metabat2.html) - Metagenomic binning
- [SemiBin2](docs/semibin2.html) - Deep learning-based metagenomic binning
- [QuickBin](docs/quickbin.html) - Fast binning with BBTools
- [CheckM2](docs/checkm2.html) - Quality assessment for bacterial and archaeal genomes
- [EukCC](docs/eukcc.html) - Quality assessment for eukaryotic genomes
- [GUNC](docs/gunc.html) - Detection of chimerism and contamination

## References
- See ../bio-skills-references.md
