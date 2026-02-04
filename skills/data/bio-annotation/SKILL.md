---
name: bio-annotation
description: Functional annotation and taxonomy inference from sequence homology.
---

# Bio Annotation

## When to use
- Functional annotation and taxonomy inference from sequence homology.

## Prerequisites
- Tools installed via pixi (see pixi.toml).
- Reference DB root: /media/shared-expansion/db/ (wsu; override per machine branch).
- Input FASTA and reference DBs are readable.

## Inputs
- proteins.faa (FASTA protein sequences).
- reference_db/ (eggNOG, InterPro, DIAMOND databases + taxdump).

## Outputs
- results/bio-annotation/annotations.parquet
- results/bio-annotation/taxonomy.parquet
- results/bio-annotation/annotation_report.md
- results/bio-annotation/logs/

## Steps
1. Run InterProScan for domain/family annotation.
2. Run eggnog-mapper for orthology-based annotation.
3. Run DIAMOND and resolve taxonomy with TaxonKit.

## QC gates
- Annotation hit rate and taxonomy rank coverage meet project thresholds.
- On failure: retry with alternative parameters; if still failing, record in report and exit non-zero.

## Validation
- Verify proteins.faa is non-empty and amino acid encoded.
- Verify required reference DBs exist under the reference root.

## Tools
- interproscan v6.0.0
- eggnog-mapper v2.1.13
- diamond v2.1.16
- taxonkit v0.20.0

## Paper summaries (2023-2025)
- summaries/ (include example use cases and tool settings used)

## Tool documentation
- [InterProScan](docs/interproscan.html) - Domain and family annotation
- [eggNOG-mapper](docs/eggnog-mapper.html) - Orthology-based functional annotation
- [DIAMOND](docs/diamond-usage.md) - Fast sequence homology search
- [TaxonKit](docs/taxonkit.html) - Taxonomy resolution and manipulation

## References
- See ../bio-skills-references.md
