# Integrative Analysis — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the integrative-analysis skill — key papers on chromatin state
modeling, functional enrichment analysis, peak annotation, 3D genome architecture, single-cell
multi-omics integration, and the reference epigenome frameworks that enable cross-assay synthesis
of ENCODE data.

The integrative-analysis skill guides users through combining multiple ENCODE data types
(histone ChIP-seq, accessibility, expression, methylation, 3D genome) into coherent biological
models. Integration requires chromatin state annotation (ChromHMM), functional enrichment testing
(LOLA, GREAT), peak-to-gene assignment (ChIPseeker), and increasingly single-cell approaches for
cell-type deconvolution.

These 10 papers are organized into five thematic groups: (1) reference epigenomes and chromatin
state modeling, (2) functional enrichment and annotation, (3) 3D genome architecture,
(4) single-cell chromatin accessibility, and (5) multi-modal integration methods.

---

## Chromatin State Modeling

Chromatin state models are the primary integration framework for multi-mark ENCODE data. By
learning the combinatorial patterns of histone modifications, accessibility, and other signals,
these models partition the genome into biologically interpretable categories — active promoters,
enhancers, Polycomb-repressed domains, heterochromatin, and more.

---

### Kundaje et al. 2015 — Roadmap Epigenomics: 111 reference epigenomes

- **Citation:** Kundaje A, Meuleman W, Ernst J, Bilenky M, Yen A, et al. Integrative analysis
  of 111 reference human epigenomes. *Nature*, 518(7539), 317-330, 2015.
- **DOI:** [10.1038/nature14248](https://doi.org/10.1038/nature14248)
- **PMID:** 25693563 | **PMC:** PMC4530010
- **Citations:** ~4,500
- **Key findings:** Produced 111 reference human epigenomes using a standardized five-mark assay
  panel (H3K4me3, H3K4me1, H3K36me3, H3K27me3, H3K9me3), generating ChromHMM state maps, DNA
  methylation profiles, and expression data across diverse tissues and cell types. Demonstrated
  that integrating histone modifications with DNA accessibility and methylation reveals enhancer
  usage patterns, bivalent chromatin domains, and tissue-specific regulatory programs not
  visible from any single assay alone. This paper defines the reference framework for all
  integrative analysis: the five core marks, 15-state ChromHMM model, and tissue-by-state
  enrichment matrices. The integrative-analysis skill uses these 111 reference epigenomes as
  comparison benchmarks when users perform ChromHMM on ENCODE data from new biosamples.

---

### Ernst & Kellis 2012 — ChromHMM: automated chromatin state discovery

- **Citation:** Ernst J, Kellis M. ChromHMM: automating chromatin-state discovery and
  characterization. *Nature Methods*, 9(3), 215-216, 2012.
- **DOI:** [10.1038/nmeth.1906](https://doi.org/10.1038/nmeth.1906)
- **PMID:** 22373907 | **PMC:** PMC3577932
- **Citations:** ~3,800
- **Key findings:** Introduced ChromHMM, a multivariate hidden Markov model that segments the
  genome into chromatin states based on combinatorial patterns of histone modifications.
  ChromHMM takes binarized ChIP-seq signal across marks and learns state emission probabilities
  and transition parameters in an unsupervised manner. Standard models use 15 states (active
  TSS, flanking TSS, enhancer, weak enhancer, bivalent, repressed Polycomb, heterochromatin,
  quiescent, etc.), though models from 5 to 51 states have been applied depending on the
  number of available marks. The integrative-analysis skill recommends ChromHMM as the
  primary integration method for multi-mark ChIP-seq experiments and provides guidance on
  selecting the number of states based on mark combinations: 5 states for 3 marks, 15 states
  for 5 marks, 18 states for 6 marks with H3K27ac, and 25+ states for expanded panels.

---

## Functional Enrichment Analysis

After defining chromatin states or identifying differential peaks, the next integration step is
functional interpretation — asking what biological processes, pathways, and regulatory programs
are enriched in a set of genomic regions.

---

### Sheffield & Bock 2016 — LOLA: genomic region set enrichment analysis

- **Citation:** Sheffield NC, Bock C. LOLA: enrichment analysis for genomic region sets and
  regulatory elements in R and Bioconductor. *Bioinformatics*, 32(4), 587-589, 2016.
- **DOI:** [10.1093/bioinformatics/btv612](https://doi.org/10.1093/bioinformatics/btv612)
- **PMID:** 26508757 | **PMC:** PMC4743626
- **Citations:** ~600
- **Key findings:** LOLA (Locus Overlap Analysis) performs Fisher's exact test enrichment
  analysis of genomic region sets against curated databases of regulatory annotations including
  ENCODE ChIP-seq peaks, Roadmap chromatin states, CODEX, and CpG islands. Unlike GREAT
  (which maps regions to genes first), LOLA tests direct genomic overlap between query regions
  and annotation databases, making it the preferred tool for testing regulatory context
  enrichment. The integrative-analysis skill recommends LOLA for hypothesis-free enrichment
  testing when users have a set of genomic regions (differential peaks, DMRs, GWAS loci) and
  want to identify which ENCODE annotations they overlap. LOLA is particularly powerful when
  testing against the full ENCODE ChIP-seq peak database, revealing which TFs and histone marks
  are enriched at a set of differentially accessible regions.

---

## Peak Annotation and Gene Assignment

Connecting regulatory elements to their target genes is one of the most challenging aspects of
integrative analysis. Two complementary approaches address this: nearest-gene assignment
(ChIPseeker) and regulatory-domain-based association (GREAT). Neither is perfect — Hi-C data
provides the ground truth for enhancer-gene linkage.

---

### Yu et al. 2015 — ChIPseeker: peak annotation with genomic features

- **Citation:** Yu G, Wang LG, He QY. ChIPseeker: an R/Bioconductor package for ChIP peak
  annotation, comparison and visualization. *Bioinformatics*, 31(14), 2382-2383, 2015.
- **DOI:** [10.1093/bioinformatics/btv145](https://doi.org/10.1093/bioinformatics/btv145)
- **PMID:** 25765347
- **Citations:** ~3,200
- **Key findings:** ChIPseeker annotates genomic peaks with their nearest gene, distance to TSS,
  and genomic feature category (promoter, 5'UTR, 3'UTR, exon, intron, downstream, intergenic).
  Provides publication-ready visualizations including TSS enrichment profiles, peak distribution
  pie charts, and Venn diagram comparisons between datasets. The integrative-analysis skill uses
  ChIPseeker for the critical step of assigning regulatory elements to putative target genes,
  noting that nearest-gene assignment is a useful heuristic but should be complemented with
  GREAT or 3D contact data for distal enhancers that may regulate genes >100kb away.

---

### McLean et al. 2010 — GREAT: regulatory domain-based gene association

- **Citation:** McLean CY, Bristor D, Hiller M, Clarke SL, Schaar BT, Lowe CB, Wenger AM,
  Bejerano G. GREAT improves functional interpretation of cis-regulatory regions.
  *Nature Biotechnology*, 28(5), 495-501, 2010.
- **DOI:** [10.1038/nbt.1630](https://doi.org/10.1038/nbt.1630)
- **PMID:** 20436461 | **PMC:** PMC4840234
- **Citations:** ~2,800
- **Key findings:** GREAT assigns biological meaning to non-coding regions using a "regulatory
  domain" model: each gene has a basal domain (5kb upstream, 1kb downstream) extended up to
  1Mb until reaching another gene's domain. This approach outperforms nearest-gene assignment
  for enhancers, which can regulate genes over hundreds of kilobases. GREAT performs ontology
  enrichment analysis (GO, MSigDB, disease ontology) on the associated gene set. The
  integrative-analysis skill recommends GREAT as the primary tool for functional interpretation
  of distal regulatory elements from ENCODE enhancer annotations. GREAT's web interface at
  great.stanford.edu accepts BED files directly, making it accessible without R/Bioconductor.

---

## 3D Genome Architecture

One-dimensional regulatory element annotations must be interpreted within three-dimensional
chromatin context. Enhancers and promoters that appear far apart on the linear genome may be
in close physical proximity through chromatin looping.

---

### Rao et al. 2014 — Hi-C chromatin architecture: TADs and loops

- **Citation:** Rao SSP, Huntley MH, Durand NC, Stamenova EK, Bochkov ID, Robinson JT,
  Sanborn AL, Machol I, Omer AD, Lander ES, Aiden EL. A 3D map of the human genome at
  kilobase resolution reveals principles of chromatin looping. *Cell*, 159(7),
  1665-1680, 2014.
- **DOI:** [10.1016/j.cell.2014.11.021](https://doi.org/10.1016/j.cell.2014.11.021)
- **PMID:** 25497547 | **PMC:** PMC5635824
- **Citations:** ~5,500
- **Key findings:** Produced the first kilobase-resolution Hi-C maps identifying ~10,000
  CTCF-mediated chromatin loops, TADs, and six chromatin subcompartments (A1, A2, B1, B2, B3,
  B4). Established that enhancer-promoter interactions are constrained within TADs and that
  CTCF loop anchors follow the convergent orientation rule. For integrative analysis, this
  demonstrates that 1D regulatory annotations must be interpreted within 3D context — an
  enhancer and its target gene should share a TAD or chromatin loop. The integrative-analysis
  skill uses ENCODE Hi-C data to validate enhancer-gene assignments and identify regulatory
  interactions that cross large linear distances but are physically proximal.

---

## Single-Cell Multi-Omics

Bulk ENCODE data represents the average signal across millions of cells, potentially mixing
distinct cell populations. Single-cell methods enable cell-type deconvolution of bulk signals and
direct linking of regulatory elements to gene expression at cellular resolution.

---

### Corces et al. 2018 — Single-cell chromatin accessibility across cancers

- **Citation:** Corces MR, Granja JM, Shams S, Louber BH, Banber CE, et al. The chromatin
  accessibility landscape of primary human cancers. *Science*, 362(6413), eaav1898, 2018.
- **DOI:** [10.1126/science.aav1898](https://doi.org/10.1126/science.aav1898)
- **PMID:** 30361341 | **PMC:** PMC6408149
- **Citations:** ~2,000
- **Key findings:** Applied scATAC-seq across 23 cancer types creating cell-type-resolved
  accessibility profiles. Developed chromVAR for TF motif deviation scoring in single-cell
  data and showed that regulatory heterogeneity predicts clinical outcomes. For integrative
  analysis of ENCODE bulk data, this demonstrates the importance of cell-type deconvolution
  — the skill recommends using scATAC-seq reference data to decompose bulk ENCODE profiles
  when the biosample contains mixed cell populations.

---

### Regev et al. 2017 — Human Cell Atlas framework for cell-type references

- **Citation:** Regev A, Teichmann SA, Lander ES, Amit I, et al. The Human Cell Atlas.
  *eLife*, 6, e27041, 2017.
- **DOI:** [10.7554/eLife.27041](https://doi.org/10.7554/eLife.27041)
- **PMID:** 29206104 | **PMC:** PMC5762154
- **Citations:** ~2,500
- **Key findings:** Proposed the Human Cell Atlas initiative to create comprehensive reference
  maps of all human cell types using single-cell technologies. The HCA framework defines cell
  types by transcriptomic signatures, spatial position, and functional assays, providing a
  taxonomy for interpreting bulk ENCODE data. HCA reference datasets enable cell-type
  deconvolution of bulk ENCODE profiles and provide cell-type labels needed to connect
  regulatory elements to specific cellular contexts.

---

### Cusanovich et al. 2018 — Large-scale scATAC-seq atlas for cell-type resolution

- **Citation:** Cusanovich DA, Hill AJ, Aghamirzaie D, Daza RM, Pliner HA, et al. A
  single-cell atlas of in vivo mammalian chromatin accessibility. *Cell*, 174(5),
  1309-1324, 2018.
- **DOI:** [10.1016/j.cell.2018.06.052](https://doi.org/10.1016/j.cell.2018.06.052)
- **PMID:** 30078704 | **PMC:** PMC6104449
- **Citations:** ~1,800
- **Key findings:** Generated scATAC-seq profiles from >100,000 cells across 13 mouse tissues,
  creating the first comprehensive single-cell accessibility atlas. Demonstrated that
  cell-type-specific accessibility peaks cluster into regulatory modules corresponding to
  known cell identities and developmental lineages. Developed the topic model approach for
  dimensionality reduction. For integrative analysis, this atlas provides single-cell
  resolution needed to decompose ENCODE bulk tissue accessibility profiles into cell-type
  contributions, enabling more precise regulatory element annotation.

---

### Stuart et al. 2019 — Multi-modal single-cell integration methods

- **Citation:** Stuart T, Butler A, Hoffman P, Hafemeister C, Papalexi E, et al.
  Comprehensive integration of single-cell data. *Cell*, 177(7), 1888-1902, 2019.
- **DOI:** [10.1016/j.cell.2019.05.031](https://doi.org/10.1016/j.cell.2019.05.031)
- **PMID:** 31178118 | **PMC:** PMC6687398
- **Citations:** ~3,000
- **Key findings:** Introduced methods for integrating single-cell datasets across modalities
  (RNA + ATAC, RNA + protein), technologies (10x vs. Smart-seq2), and conditions. The
  transfer learning approach uses "anchor" correspondences between datasets to project
  information across modalities. For integrative analysis of ENCODE data, this framework
  enables combining single-cell expression and accessibility to link regulatory elements to
  target genes at cell-type resolution, overcoming the limitation of bulk-level correlations.
  The Seurat v3 implementation (>100,000 installations) is the standard tool for this workflow.

---
