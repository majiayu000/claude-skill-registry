# CellxGene Context — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the cellxgene-context skill — key papers informing single-cell atlas resources, cell type annotation, and cross-tissue reference datasets for contextualizing ENCODE functional genomic data at cell-type resolution.

---

## Atlas Vision & Infrastructure

---

### Regev et al. 2017 — The Human Cell Atlas: a strategic overview

- **Citation:** Regev A, Teichmann SA, Lander ES, Amit I, Benoist C, Birney E,
  Bodenmiller B, Campbell P, Carninci P, Clatworthy M, et al. The Human Cell
  Atlas. eLife, 6:e27041, 2017.
- **DOI:** [10.7554/eLife.27041](https://doi.org/10.7554/eLife.27041)
- **PMID:** 29206104 | **PMC:** PMC5762154
- **Citations:** ~2,500
- **Key findings:** Outlined the vision and scientific strategy for the Human
  Cell Atlas (HCA), an international consortium to create comprehensive
  reference maps of all human cell types and states using single-cell and
  spatial genomics technologies. Formally defined a "cell type" as a stable
  transcriptional program reproducibly observed across individuals and
  experimental conditions, distinguishing it from transient "cell states"
  driven by activation signals, cell cycle position, or environmental stimuli.
  Proposed a hierarchical annotation framework from coarse lineages (immune,
  epithelial, stromal, endothelial, neural) through intermediate classes to
  fine-grained subtypes and states, establishing the ontological structure
  that CellxGene uses for organizing and querying atlas data. The HCA vision
  directly motivates the CellxGene platform as the primary portal for
  discovering reference cell type profiles and contextualizing bulk ENCODE
  chromatin data within the cellular composition of profiled tissues.

---

### Megill et al. 2021 — CellxGene: interactive exploration of single-cell datasets

- **Citation:** Megill C, Martin B, Weaver C, Bell S, Dedber L, Badajoz S,
  Heumos L, Pisco AO, et al. CellxGene: a performant, scalable exploration
  platform for high dimensional sparse matrices. bioRxiv, 2021.
- **DOI:** [10.1101/2021.04.05.438318](https://doi.org/10.1101/2021.04.05.438318)
- **PMID:** N/A | **PMC:** N/A
- **Citations:** ~300
- **Key findings:** Described the CellxGene platform architecture for
  interactive visualization and exploration of single-cell datasets supporting
  millions of cells with sub-second query response times through sparse matrix
  compression and server-side rendering. The platform enables real-time gene
  expression queries across cell types, on-the-fly differential expression
  between user-defined cell groups, and embedding visualization (UMAP/t-SNE)
  with multi-metadata overlays. CellxGene Census provides a programmatic
  Python/R API for querying across all hosted datasets simultaneously by cell
  type ontology, tissue, disease status, and gene expression — enabling cross-
  dataset meta-analyses without downloading individual h5ad files. As of 2025,
  the platform hosts >1,200 datasets with >80 million cells, making it the de
  facto portal for Human Cell Atlas data and the richest resource for cell-
  type-specific expression context.

---

## Reference Atlases

---

### Tabula Sapiens Consortium 2022 — Multi-organ human cell atlas

- **Citation:** The Tabula Sapiens Consortium. The Tabula Sapiens: a multiple-
  organ, single-cell transcriptomic atlas of humans. Science,
  376(6594):eabl4896, 2022.
- **DOI:** [10.1126/science.abl4896](https://doi.org/10.1126/science.abl4896)
- **PMID:** 35549404 | **PMC:** PMC9812015
- **Citations:** ~1,500
- **Key findings:** Profiled ~500,000 cells from 24 tissues of a small cohort
  of donors using standardized protocols, enabling direct cross-tissue cell
  type comparison without inter-individual batch confounds. Identified 475
  distinct cell types with tissue-shared and tissue-specific transcriptional
  programs, revealing that resident immune, endothelial, and fibroblast
  populations acquire tissue-adapted transcriptional signatures distinct from
  their circulating or generic counterparts — for example, liver sinusoidal
  endothelial cells express scavenger receptors absent from lung capillary
  endothelium, reflecting tissue-specific functional specialization. Discovered
  widespread alternative splicing differences between cell types, with ~40% of
  genes showing cell-type-specific isoform usage invisible in gene-level
  expression analysis — suggesting that ENCODE RNA-seq from heterogeneous
  tissues may mask important isoform dynamics. Tabula Sapiens is a key
  CellxGene reference atlas for label transfer: annotating cell types in user
  scRNA-seq datasets by projecting them onto the Tabula Sapiens reference
  embedding, and for deconvolving bulk ENCODE profiles into estimated cell
  type proportions to determine which cell populations contribute most to
  observed chromatin signals.

---

### Tabula Muris Consortium 2018 — Single-cell atlas of the mouse

- **Citation:** Tabula Muris Consortium. Single-cell transcriptomics of 20
  mouse organs creates a Tabula Muris. Nature, 562(7727):367-372, 2018.
- **DOI:** [10.1038/s41586-018-0590-4](https://doi.org/10.1038/s41586-018-0590-4)
- **PMID:** 30283141 | **PMC:** PMC6642641
- **Citations:** ~3,000
- **Key findings:** Generated single-cell transcriptomes from >100,000 cells
  across 20 mouse organs using dual protocols — FACS-sorted Smart-seq2 (full-
  length, deeper coverage per cell) and 10x Chromium (droplet-based, higher
  cell throughput). The dual-protocol design enabled rigorous assessment of
  platform-specific biases: Smart-seq2 detected ~4,000 genes per cell vs.
  ~1,500 for 10x, but cell type identification was consistent across both
  platforms when using appropriate integration methods, confirming that major
  cell populations are robustly identifiable regardless of technology choice.
  Established a standardized cell type ontology for mouse tissues that maps to
  ENCODE biosample terms (e.g., ENCODE's "pancreas" tissue corresponds to
  Tabula Muris acinar, ductal, alpha, beta, delta, epsilon, and stellate
  cells), enabling deconvolution of bulk ENCODE profiles into cell-type
  contributions. Tabula Muris serves as the primary reference for mouse cell
  type annotation in CellxGene, and its cross-species comparisons with human
  atlases reveal conserved and divergent cell type programs relevant for
  interpreting mouse ENCODE experiments in human disease context.

---

### Dominguez Conde et al. 2022 — Cross-tissue human immune cell atlas

- **Citation:** Dominguez Conde C, Xu C, Jarvis LB, Rainbow DB, Wells SB,
  Gomes T, Howlett SK, Sherber O, Gould J, Conde CD, et al. Cross-tissue
  immune cell analysis reveals tissue-specific features in humans. Science,
  376(6594):eabl5197, 2022.
- **DOI:** [10.1126/science.abl5197](https://doi.org/10.1126/science.abl5197)
- **PMID:** 35549406 | **PMC:** PMC7613554
- **Citations:** ~800
- **Key findings:** Profiled 330,000 immune cells from 16 tissues of 12
  donors, revealing that tissue-resident immune populations diverge
  substantially from circulating blood counterparts in gene expression,
  surface markers, and inferred transcription factor activity. Identified
  tissue-specific macrophage states (alveolar macrophages in lung, Kupffer
  cells in liver, microglia in brain, Langerhans cells in skin) with distinct
  regulatory programs driven by tissue-specific enhancer landscapes detectable
  by ENCODE ChIP-seq and ATAC-seq. Found that cross-tissue immune cell
  integration requires particularly careful batch correction because tissue
  processing artifacts (enzymatic digestion, mechanical dissociation) can be
  confounded with genuine tissue adaptation signatures. This atlas is
  essential for interpreting ENCODE immune cell profiling data in tissue
  context — a K562 or GM12878 ChIP-seq experiment captures only one state of
  one hematopoietic lineage, while the immune atlas reveals the full spectrum
  of immune cell diversity across tissues.

---

## Integration Methods

---

### Luecken et al. 2022 — Benchmarking atlas-level single-cell integration

- **Citation:** Luecken MD, Buttner M, Chaichoompu K, Danese A, Grote M,
  Herbst P, Erber W, Pineau J, Schulte-Schrepping J, Sikkema L, et al.
  Benchmarking atlas-level data integration in single-cell genomics. Nature
  Methods, 19(1):41-50, 2022.
- **DOI:** [10.1038/s41592-021-01336-8](https://doi.org/10.1038/s41592-021-01336-8)
- **PMID:** 34949812 | **PMC:** PMC8762698
- **Citations:** ~1,500
- **Key findings:** Systematically benchmarked 16 single-cell integration
  methods across 85 integration tasks spanning different biological and
  technical scenarios using the scIB (single-cell Integration Benchmarking)
  framework. Evaluated methods on two fundamentally competing objectives:
  batch correction quality (kBET statistic, batch-ASW, graph connectivity) and
  biological conservation (cell type ASW, NMI, ARI, isolated label score,
  trajectory conservation). ScVI, scANVI, and Harmony consistently ranked
  among the top methods for atlas-scale integration tasks, while BBKNN and
  Combat performed competitively for simpler within-tissue integration. The
  key insight was that batch correction and biological conservation are
  inherently in tension — methods that perfectly mix batches often merge
  biologically distinct but transcriptionally similar cell types, particularly
  rare populations. This benchmark directly informs method selection when
  building or querying CellxGene atlases and when deconvolving ENCODE bulk
  data using single-cell references.

---

### Chazarra-Gil et al. 2021 — Flexible comparison of batch correction methods

- **Citation:** Chazarra-Gil R, van Dongen S, Kiselev VY, Hemberger M.
  Flexible comparison of batch correction methods for single-cell RNA-seq
  using BatchBench. Genome Biology, 22(1):189, 2021.
- **DOI:** [10.1186/s13059-021-02393-y](https://doi.org/10.1186/s13059-021-02393-y)
- **PMID:** 34183031
- **Citations:** ~500
- **Key findings:** Introduced BatchBench, a modular Nextflow pipeline for
  standardized comparison of batch correction methods across diverse single-
  cell datasets with reproducible metrics. Evaluated 8 methods (Harmony,
  Scanorama, MNN, ComBat, limma, LIGER, Seurat v3 CCA, BBKNN) across 5 real-
  world datasets with varying batch complexity. Found that the optimal method
  depends critically on the nature of the batch effect: same-
  protocol/different-donor designs (simple batch effects) were correctable by
  most methods, while cross-platform batch effects (10x vs. Smart-seq2) or
  cross-species comparisons required embedding-based approaches. Critically
  demonstrated that integration quality should be assessed at the cell-type
  level rather than globally, because global metrics can mask complete failure
  to integrate rare cell populations — a particularly important concern for
  ENCODE cell type deconvolution where rare cell types like delta cells in
  islets or stellate cells in liver may be the populations of interest.

---
