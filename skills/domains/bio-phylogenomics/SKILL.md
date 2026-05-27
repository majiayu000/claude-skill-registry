---
name: bio-phylogenomics
description: Build marker gene alignments and phylogenetic trees.
---

# Bio Phylogenomics

## When to use
- Build marker gene alignments and phylogenetic trees.

## Prerequisites
- Tools installed via pixi (see pixi.toml).
- Marker gene set or alignments available.

## Inputs
- markers.faa (marker genes) or alignments.fasta

## Outputs
- results/bio-phylogenomics/alignments/
- results/bio-phylogenomics/trees/
- results/bio-phylogenomics/phylo_report.md
- results/bio-phylogenomics/logs/

## Steps
1. Extract marker genes or SSU rRNA sequences.
2. Align and trim sequences using project-standard workflows.
3. Build ML trees with bootstraps:
   - Standard accuracy: Use IQ-TREE (comprehensive model selection, publication-quality)
   - Fast mode: Use IQ-TREE -fast (exploratory analysis, large datasets >10K sequences)
   - Very large datasets: Use VeryFastTree (>100K sequences, ultra-fast)
4. Post-process trees with ETE Toolkit:
   - Calculate tree statistics (branch lengths, distances, topology metrics)
   - Root, prune, or collapse nodes as needed
   - Filter by bootstrap support values
   - Add taxonomic or trait annotations
   - Generate publication-quality visualizations

## QC gates
- Alignment length and missingness meet project thresholds.
- Bootstrap support summary meets project thresholds.
- On failure: retry with alternative parameters; if still failing, record in report and exit non-zero.

## Validation
- Verify markers.faa is non-empty and aligned sequences are consistent.

## Tools
- iqtree v3.0.1 (standard mode and -fast mode for rapid inference)
- veryfasttree v4.0+ (ultra-fast tree inference for massive datasets)
- ete3/ete4 (ETE Toolkit for tree processing, statistics, and visualization)

## Tool Selection Workflow

### Tree Inference
Choose tree inference tool based on dataset size and accuracy requirements:

| Dataset Size | Accuracy Required | Recommended Tool |
|-------------|-------------------|------------------|
| <1K sequences | High (publication) | IQ-TREE standard |
| <1K sequences | Medium (exploratory) | IQ-TREE -fast |
| 1K-10K sequences | High (publication) | IQ-TREE standard |
| 1K-10K sequences | Medium (exploratory) | IQ-TREE -fast |
| 10K-100K sequences | High | IQ-TREE standard |
| 10K-100K sequences | Medium/Fast | IQ-TREE -fast |
| >100K sequences | Any | VeryFastTree |

### Post-Tree Processing
Use ETE Toolkit for all tree post-processing tasks:
- Tree statistics and metrics
- Tree manipulation (rooting, pruning, filtering)
- Taxonomic annotation
- Visualization and figure generation

## Paper summaries (2023-2025)
- summaries/ (include example use cases and tool settings used)

## Tool documentation
- [IQ-TREE](docs/iqtree.html) - Maximum likelihood phylogenetic inference with model selection
- [VeryFastTree](docs/veryfasttree.html) - Ultra-fast approximate maximum likelihood trees
- [ETE Toolkit](docs/ete-toolkit.html) - Tree manipulation, statistics, and visualization

## References
- See ../bio-skills-references.md
