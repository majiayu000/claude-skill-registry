# Batch Analysis — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the batch-analysis skill — key papers informing batch effect detection, correction, and multi-experiment integration strategies for genomic data.

---

## Foundational Reviews

---

### Leek et al. 2010 — Tackling the widespread and critical impact of batch effects

- **Citation:** Leek JT, Scharpf RB, Bravo HC, Simcha D, Langmead B, Johnson
  WE, Geman D, Baggerly K, Irizarry RA. Tackling the widespread and critical
  impact of batch effects in high-throughput data. Nature Reviews Genetics,
  11(10):733-739, 2010.
- **DOI:** [10.1038/nrg2825](https://doi.org/10.1038/nrg2825)
- **PMID:** 20838408 | **PMC:** PMC3880143
- **Citations:** ~3,000
- **Key findings:** Landmark review establishing batch effects as a pervasive
  confound in high-throughput genomic studies affecting microarrays, RNA-seq,
  ChIP-seq, proteomics, and metabolomics. Demonstrated through re-analysis of
  published datasets that batch effects can account for more variance than
  biological signal — in one striking example, samples clustered by processing
  date rather than disease status. Classified batch effects into known batches
  (processing date, lab, reagent lot, operator) and unknown/hidden batches
  detectable only through surrogate variable analysis (SVA). Established the
  fundamental principle that experimental design (balanced randomization of
  conditions across batches) is always preferable to computational correction,
  and that confounded designs where all cases were processed in batch 1 and
  all controls in batch 2 cannot be rescued by any statistical method.

---

### Goh et al. 2017 — Why batch effects matter for genomic analysis

- **Citation:** Goh WWB, Wang W, Wong L. Why batch effects matter in omics
  data, and how to avoid them. Trends in Biotechnology, 35(6):498-507, 2017.
- **DOI:** [10.1016/j.tibtech.2017.02.012](https://doi.org/10.1016/j.tibtech.2
  017.02.012)
- **PMID:** 28351613
- **Citations:** ~400
- **Key findings:** Comprehensive review categorizing batch effects by source
  across the entire experimental pipeline: sample handling (collection time,
  storage temperature, freeze-thaw cycles), library preparation (reagent lots,
  operator skill, protocol version, PCR cycles), sequencing (instrument model,
  flow cell, lane, run date), and computational processing (reference genome
  version, aligner, peak caller, normalization method). Demonstrated through
  case studies that batch effects can create entirely artifactual biological
  signals — including false disease subtypes in cancer expression data,
  spurious biomarkers that fail replication, and misleading pathway
  enrichments driven by technical rather than biological variation.
  Recommended a structured batch assessment approach: (1) visualize batch
  structure with PCA/t-SNE colored by batch variables before any biological
  analysis, (2) formally test for batch-phenotype confounding using ANOVA or
  chi-squared tests, (3) apply correction only when batches are not perfectly
  confounded with biology, and (4) validate findings in independent cohorts
  processed separately.

---

### Lazar et al. 2012 — Batch effect removal in genomic data: a survey

- **Citation:** Lazar C, Meganck S, Taminau J, Steenhoff D, Coletta A, Molter
  C, Weiss-Solis DY, Duque R, Bersini H, Nowe A. Batch effect removal methods
  for microarray gene expression data integration: a survey. Briefings in
  Bioinformatics, 14(4):469-490, 2013.
- **DOI:** [10.1093/bib/bbs037](https://doi.org/10.1093/bib/bbs037)
- **PMID:** 22851511
- **Citations:** ~500
- **Key findings:** Surveyed 10 batch correction methods across four
  algorithmic categories: ratio-based (dividing by batch-specific means),
  standardization-based (z-score normalization per batch), regression-based
  (ComBat, limma removeBatchEffect), and matrix factorization-based (SVA,
  RUV). Evaluated methods on both synthetic datasets with known ground truth
  and real datasets with independent validation, using differential expression
  recovery as the primary performance metric. Found that empirical Bayes
  methods (ComBat) consistently outperformed simpler ratio and standardization
  approaches, particularly when batch sizes were small (<5 samples) and
  imbalanced across conditions. Critically demonstrated that aggressive batch
  correction can remove genuine biological signal when batch and biological
  variables are partially confounded — establishing the principle that
  correction methods must always be validated by checking that known positive-
  control biological differences are preserved post-correction.

---

## Bulk Correction Methods

---

### Johnson et al. 2007 — ComBat: empirical Bayes batch adjustment

- **Citation:** Johnson WE, Li C, Rabinovic A. Adjusting batch effects in
  microarray expression data using empirical Bayes methods. Biostatistics,
  8(1):118-127, 2007.
- **DOI:** [10.1093/biostatistics/kxj037](https://doi.org/10.1093/biostatistic
  s/kxj037)
- **PMID:** 16632515
- **Citations:** ~5,000
- **Key findings:** Introduced ComBat (Combating Batch effects), which uses an
  empirical Bayes framework to estimate and remove batch-specific location
  (mean shift) and scale (variance inflation/deflation) parameters for each
  gene. By pooling information across all genes within each batch, ComBat
  produces robust batch parameter estimates even with very small sample sizes
  (n=2-3 per batch) — a critical advantage over gene-by-gene regression
  approaches that require larger samples. The parametric empirical Bayes
  priors shrink noisy per-gene estimates toward batch-wide means, preventing
  overcorrection of features with limited data while still correcting features
  with clear batch effects. ComBat became the most cited batch correction
  method (>5,000 citations) because it preserves biological variation while
  removing technical batch effects, works reliably with small samples common
  in genomics, and can include biological covariates of interest in the model
  to protect them from removal.

---

## Single-Cell Correction Methods

---

### Haghverdi et al. 2018 — Mutual nearest neighbors for batch correction in scRNA-seq

- **Citation:** Haghverdi L, Lun ATL, Morgan MD, Marioni JC. Batch effects in
  single-cell RNA-sequencing data are corrected by matching mutual nearest
  neighbors. Nature Biotechnology, 36(5):421-427, 2018.
- **DOI:** [10.1038/nbt.4091](https://doi.org/10.1038/nbt.4091)
- **PMID:** 29608177 | **PMC:** PMC6152897
- **Citations:** ~2,000
- **Key findings:** Introduced the mutual nearest neighbors (MNN) approach for
  single-cell batch correction, which identifies pairs of cells from different
  batches that are each other's nearest neighbors in high-dimensional
  expression space. These MNN pairs represent the same biological cell
  type/state in both batches, and the expression vector connecting them
  defines the batch correction to apply locally. Unlike global methods like
  ComBat or limma that apply a uniform correction across all cells, MNN
  performs local corrections that adapt to different regions of expression
  space — critical for single-cell data where different cell types may
  experience different magnitudes of technical variation (e.g., dropout rates
  vary by expression level). The method requires no pre-defined cell type
  labels, no balanced cell type composition across batches, and makes minimal
  assumptions about the batch effect structure, making it broadly applicable
  to atlas-scale integration projects.

---

### Zhang et al. 2020 — Harmony: fast and flexible batch correction for scRNA-seq

- **Citation:** Korsunsky I, Millard N, Fan J, Slowikowski K, Zhang F, Wei K,
  Baglaenko Y, Brenner M, Loh PR, Raychaudhuri S. Fast, sensitive and accurate
  integration of single-cell data with Harmony. Nature Methods,
  16(12):1289-1296, 2019.
- **DOI:** [10.1038/s41592-019-0619-0](https://doi.org/10.1038/s41592-019-0619-0)
- **PMID:** 31740819 | **PMC:** PMC6884693
- **Citations:** ~1,200
- **Key findings:** Harmony performs iterative soft clustering in PCA space
  followed by within-cluster linear correction, alternating between two steps:
  maximum-diversity clustering (forcing each cluster to contain cells from all
  batches via a diversity penalty) and linear regression correction within
  each cluster to remove batch-specific shifts. The algorithm converges in
  10-20 iterations and is 10-100x faster than Seurat CCA and Scanorama,
  enabling integration of millions of cells on a standard laptop. Harmony
  operates directly on PCA embeddings rather than full expression matrices,
  preserving computational efficiency and memory. Validated on immune cell
  datasets where it correctly aligned shared cell types across platforms (10x
  Chromium, Smart-seq2, Drop-seq) while maintaining separation of biologically
  distinct populations, demonstrating that speed and accuracy are not mutually
  exclusive.

---

## Benchmarking

---

### Tran et al. 2020 — Benchmarking batch correction methods for scRNA-seq

- **Citation:** Tran HTN, Ang KS, Chevrier M, Zhang X, Lee NYS, Goh M, Chen J.
  A benchmark of batch-effect correction methods for single-cell RNA
  sequencing data. Genome Biology, 21(1):12, 2020.
- **DOI:** [10.1186/s13059-019-1850-9](https://doi.org/10.1186/s13059-019-1850-9)
- **PMID:** 31948481 | **PMC:** PMC6965632
- **Citations:** ~800
- **Key findings:** Systematically benchmarked 14 batch correction methods
  across 10 scRNA-seq datasets using complementary metrics for batch mixing
  (kBET, ASW batch) and biological conservation (ARI, NMI, cell type ASW).
  Harmony, LIGER, and Seurat v3 CCA consistently performed well on both batch
  integration and biological conservation metrics, while BBKNN and MNN offered
  competitive performance with lower computational requirements. ComBat and
  limma (bulk methods naively applied to single-cell data) performed poorly on
  complex multi-cell-type datasets because they assume a uniform batch effect
  across all cell types — an assumption violated in single-cell data where
  different populations exhibit different technical biases. The key practical
  conclusion was that no single method dominates across all scenarios: simpler
  methods suffice for same-platform/same-protocol data from different donors,
  while more sophisticated embedding-based approaches are necessary for cross-
  platform, cross-protocol, or cross-species integration tasks.

---
