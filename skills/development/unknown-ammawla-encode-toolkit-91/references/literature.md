# Visualization Workflow — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the visualization-workflow skill — key papers on genome
browsers, track visualization tools, heatmap and signal profile generation, 3D genome
visualization, normalization methods, and annotation retrieval systems for creating
publication-quality figures from ENCODE data.

The visualization-workflow skill guides users through visualizing ENCODE data at multiple scales:
individual loci (genome browsers), genome-wide patterns (heatmaps, metaplots), 3D chromatin
architecture (contact maps), and comparative displays (multi-sample overlays). Effective
visualization requires appropriate normalization, color scales, and annotation layers.

These 8 papers cover four aspects of genomic visualization: (1) genome browsers for locus-level
exploration, (2) signal processing tools for genome-wide heatmaps and profiles, (3) 3D genome
visualization, and (4) normalization and annotation retrieval for accurate cross-sample displays.

---

## Genome Browsers

Genome browsers are the primary tools for locus-level visualization of ENCODE data. They display
multiple data types as horizontal tracks aligned to genomic coordinates, enabling visual
integration of ChIP-seq signal, accessibility peaks, gene models, and conservation scores at
specific regulatory regions. The UCSC Genome Browser is web-based (data rendered server-side),
while IGV is a desktop application (data rendered locally).

---

### Kent et al. 2002 — UCSC Genome Browser: foundational genomic visualization

- **Citation:** Kent WJ, Sugnet CW, Furey TS, Roskin KM, Pringle TH, Zahler AM, Haussler D.
  The human genome browser at UCSC. *Genome Research*, 12(6), 996-1006, 2002.
- **DOI:** [10.1101/gr.229102](https://doi.org/10.1101/gr.229102)
- **PMID:** 12045153 | **PMC:** PMC186604
- **Citations:** ~5,000
- **Key findings:** Introduced the UCSC Genome Browser, establishing the multi-track paradigm
  for genomic data visualization with synchronized coordinate systems. The browser displays
  diverse data types (gene models, conservation, repeats, regulatory annotations, custom user
  data) as horizontal tracks aligned to genomic coordinates. ENCODE data is directly available
  as public track hubs with pre-configured display settings for signal tracks (bigWig), peak
  calls (BED/bigBed), and interaction data (interact format). The visualization-workflow skill
  uses UCSC as the primary locus-level visualization tool and can generate track hub
  configurations (hub.txt, genomes.txt, trackDb.txt) for custom ENCODE data displays.
  UCSC also hosts the ENCODE cCRE tracks and regulation tracks that overlay element annotations
  on any genomic region.

---

### Robinson et al. 2011 — IGV: interactive local genomic data exploration

- **Citation:** Robinson JT, Thorvaldsdottir H, Winckler W, Guttman M, Lander ES, Getz G,
  Mesirov JP. Integrative genomics viewer. *Nature Biotechnology*, 29(1), 24-26, 2011.
- **DOI:** [10.1038/nbt.1754](https://doi.org/10.1038/nbt.1754)
- **PMID:** 21221095 | **PMC:** PMC3346182
- **Citations:** ~10,000
- **Key findings:** Introduced IGV, a high-performance desktop application for interactive
  exploration of large genomic datasets. IGV renders data locally, enabling rapid navigation
  through BAM alignments, VCF variants, BED peaks, and bigWig signal tracks without uploading
  to a remote server. This is critical for unpublished or in-progress analyses. Key features:
  - Split-panel views for multi-sample comparison
  - Read-level visualization for inspecting individual alignments
  - Sashimi plots for splice junction visualization in RNA-seq
  - Session files (XML) for reproducible visualization configurations

  The visualization-workflow skill recommends IGV for exploratory analysis of downloaded ENCODE
  files, particularly for inspecting read-level evidence at specific loci.

---

### Thorvaldsdottir et al. 2013 — IGV best practices for publication-quality figures

- **Citation:** Thorvaldsdottir H, Robinson JT, Mesirov JP. Integrative Genomics Viewer (IGV):
  high-performance genomics data visualization and exploration. *Briefings in Bioinformatics*,
  14(2), 178-192, 2013.
- **DOI:** [10.1093/bib/bbs017](https://doi.org/10.1093/bib/bbs017)
- **PMID:** 22517427 | **PMC:** PMC3603213
- **Citations:** ~2,000
- **Key findings:** Comprehensive guidance on IGV for publication figures:
  - Track height optimization (taller for signal, shorter for peaks)
  - Color scheme selection (blue for ChIP, green for accessibility, red for expression)
  - Consistent y-axis scales when comparing samples
  - Input/control tracks alongside ChIP-seq signal
  - Gene model annotations for genomic context
  - Batch screenshot generation via IGV command-line for multi-locus panels

  The paper also describes IGV session files for reproducible views and the IGV batch script
  interface for automated figure generation across hundreds of loci. The visualization-workflow
  skill encodes these best practices into its figure generation recommendations.

---

## Signal Processing and Heatmap Visualization

Genome-wide visualization requires transforming raw sequencing data into interpretable signal
profiles, heatmaps, and metaplots. deepTools is the standard toolkit for these transformations,
providing normalization, matrix computation, and publication-ready plotting.

---

### Ramirez et al. 2016 — deepTools: genome-wide signal visualization

- **Citation:** Ramirez F, Ryan DP, Gruning B, Bhatt V, Kilpert F, Richter AS, Heyne S,
  Dundar F, Manke T. deepTools2: a next generation web server for deep-sequencing data
  analysis. *Nucleic Acids Research*, 44(W1), W160-W165, 2016.
- **DOI:** [10.1093/nar/gkw257](https://doi.org/10.1093/nar/gkw257)
- **PMID:** 27079975 | **PMC:** PMC4987876
- **Citations:** ~3,800
- **Key findings:** deepTools provides the standard toolkit for genome-wide signal visualization:
  - **computeMatrix**: Extract signal around genomic features (TSS, peaks, gene bodies)
  - **plotHeatmap**: Clustered heatmaps of signal at thousands of sites
  - **plotProfile**: Average signal metaplots (e.g., H3K27ac at enhancers)
  - **bamCoverage**: Generate normalized bigWig from BAM files
  - **bamCompare**: Log2 ratio of ChIP vs. input signal
  - **plotCorrelation**: Sample similarity matrices

  Supports normalization methods: RPKM, CPM, BPM, RPGC (reads per genomic content). The
  visualization-workflow skill recommends deepTools as the primary tool for genome-wide
  patterns — heatmaps of histone marks at enhancers, metaplots of accessibility at TSS,
  and ChIP/input ratio tracks for signal-to-noise assessment.

---

## 3D Genome Visualization

Hi-C contact maps require specialized visualization tools that handle the two-dimensional matrix
format and provide synchronized views of linear tracks alongside contact frequency data.

---

### Kerpedjiev et al. 2018 — HiGlass: interactive Hi-C contact maps

- **Citation:** Kerpedjiev P, Abdennur N, Lekschas F, McCallum C, Dinkla K, Strobelt H,
  Luber JM, Ouellette SB, Azhir A, Kumar N, Hwang J, Lee S, Alber BH, Pfister H,
  Mirny LA, Park PJ, Gehlenborg N. HiGlass: web-based visual exploration and analysis of
  genome interaction maps. *Genome Biology*, 19(1), 125, 2018.
- **DOI:** [10.1186/s13059-018-1486-1](https://doi.org/10.1186/s13059-018-1486-1)
- **PMID:** 30143029 | **PMC:** PMC6109259
- **Citations:** ~600
- **Key findings:** HiGlass provides interactive, multi-resolution Hi-C visualization with:
  - Synchronized 1D track views alongside 2D contact matrices
  - Multi-resolution tiling for smooth zoom (chromosome to kilobase)
  - Side-by-side contact map comparison between biosamples
  - CTCF/cohesin ChIP-seq track overlay to annotate loop anchors
  - Integration with 4D Nucleome and ENCODE Hi-C data

  The visualization-workflow skill recommends HiGlass for Hi-C visualization, particularly
  when linking 3D contacts to 1D ENCODE annotations (ChIP-seq peaks at loop anchors,
  accessibility at TAD boundaries, expression at loop-connected promoters).

---

## Heatmap and Statistical Visualization

For multi-dimensional ENCODE data displays that go beyond genome browser views, ComplexHeatmap
provides the flexibility to create publication-ready multi-panel figures with synchronized
annotations, clustering, and color scales.

---

### Gu et al. 2016 — ComplexHeatmap: multi-panel publication figures

- **Citation:** Gu Z, Eils R, Schlesner M. Complex heatmaps reveal patterns and correlations
  in multidimensional genomic data. *Bioinformatics*, 32(18), 2847-2849, 2016.
- **DOI:** [10.1093/bioinformatics/btw313](https://doi.org/10.1093/bioinformatics/btw313)
- **PMID:** 27207943
- **Citations:** ~3,500
- **Key findings:** ComplexHeatmap (R/Bioconductor) creates customizable multi-panel heatmaps
  with synchronized annotations, dendrograms, and color scales. For ENCODE visualization:
  - Multi-mark views: rows = regions, columns = histone marks, color = signal intensity
  - Cross-biosample panels: rows = cCREs, columns = biosamples, color = activity state
  - Correlation matrices between experiments
  - ChromHMM state annotations alongside quantitative signal

  The visualization-workflow skill recommends ComplexHeatmap for all multi-dimensional
  ENCODE displays requiring statistical annotation and hierarchical clustering.

---

## Normalization for Cross-Sample Visualization

Visualizing multiple ENCODE experiments on the same scale requires appropriate normalization.
Naive normalization (RPKM, CPM) can produce biased comparisons when the underlying signal
distributions differ between samples.

---

### Robinson & Oshlack 2010 — TMM normalization for accurate cross-sample display

- **Citation:** Robinson MD, Oshlack A. A scaling normalization method for differential
  expression analysis of RNA-seq data. *Genome Biology*, 11(3), R25, 2010.
- **DOI:** [10.1186/gb-2010-11-3-r25](https://doi.org/10.1186/gb-2010-11-3-r25)
- **PMID:** 20196867 | **PMC:** PMC2864565
- **Citations:** ~8,000
- **Key findings:** Introduced TMM (Trimmed Mean of M-values) normalization, demonstrating that
  naive read-count normalization produces biased cross-sample comparisons when underlying
  distributions differ (composition bias). TMM computes normalization factors from trimmed
  mean of log-fold-changes. While developed for RNA-seq, TMM-style normalization is equally
  critical for ChIP-seq and ATAC-seq cross-sample comparison — if one sample has globally
  stronger signal, CPM normalization underestimates differences at individual peaks.

  The visualization-workflow skill warns users about normalization artifacts and recommends:
  - TMM for expression data (RNA-seq, gene quantifications)
  - RPGC for ChIP-seq signal track comparison (normalizes by genome content)
  - Spike-in normalization for comparing ChIP-seq between conditions
  - Quantile normalization only within matched sample groups

---

## Annotation Retrieval for Visualization

Genomic visualizations require annotation layers — gene names, functional categories, ontology
terms — that provide biological context for the underlying signal data. biomaRt enables
programmatic retrieval of these annotations.

---

### Durinck et al. 2009 — biomaRt: programmatic annotation for visualizations

- **Citation:** Durinck S, Spellman PT, Birney E, Huber W. Mapping identifiers for the
  integration of genomic datasets with the R/Bioconductor package biomaRt. *Nature
  Protocols*, 4(8), 1184-1191, 2009.
- **DOI:** [10.1038/nprot.2009.97](https://doi.org/10.1038/nprot.2009.97)
- **PMID:** 19617889 | **PMC:** PMC3159387
- **Citations:** ~2,500
- **Key findings:** biomaRt provides an R interface to BioMart databases (Ensembl, UCSC,
  Wormbase), enabling programmatic retrieval of:
  - Gene identifier conversion (Ensembl ID, symbol, Entrez)
  - TSS coordinates for metaplot anchor points
  - GO annotations for functional grouping in heatmaps
  - Cross-species orthologs for comparative visualization
  - Chromosome band annotations for karyotype views

  The visualization-workflow skill uses biomaRt for automated annotation retrieval when
  building visualizations — labeling peaks with gene names, grouping regions by functional
  category, and annotating heatmap rows with genomic metadata. biomaRt connects to
  Ensembl's REST API, enabling annotation without local database installation.

---
