# Epigenome Profiling — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the epigenome-profiling skill — key papers on histone
modification landscapes, chromatin state annotation, DNA methylation, bivalent chromatin,
reference epigenome generation, and the multi-mark profiling strategies that define epigenomic
states across cell types and tissues.

The epigenome-profiling skill guides users through characterizing the epigenomic landscape of a
biosample using ENCODE data: selecting appropriate histone marks, interpreting chromatin states,
integrating DNA methylation, and comparing against reference epigenomes. Epigenome profiling is
fundamentally a multi-assay endeavor — no single mark defines a chromatin state.

These 10 papers are organized into five groups: (1) reference epigenome frameworks, (2) chromatin
state discovery tools, (3) foundational histone modification maps, (4) DNA methylation
integration, and (5) international standards and expanded mark catalogs.

---

## Reference Epigenome Frameworks

Reference epigenomes define the benchmarks against which new profiling data is compared. They
establish which marks to profile, how many replicates are needed, what quality thresholds to
apply, and what chromatin states to expect in different tissue types.

---

### Kundaje et al. 2015 — Roadmap Epigenomics: 111 reference human epigenomes

- **Citation:** Kundaje A, Meuleman W, Ernst J, Bilenky M, Yen A, et al. Integrative analysis
  of 111 reference human epigenomes. *Nature*, 518(7539), 317-330, 2015.
- **DOI:** [10.1038/nature14248](https://doi.org/10.1038/nature14248)
- **PMID:** 25693563 | **PMC:** PMC4530010
- **Citations:** ~4,500
- **Key findings:** Generated 111 reference human epigenomes using five core marks (H3K4me3,
  H3K4me1, H3K36me3, H3K27me3, H3K9me3) plus H3K27ac, DNA methylation, and RNA-seq.
  ChromHMM integration revealed that tissue-specific enhancer activity is the primary axis
  of epigenomic variation between cell types, while promoter states are largely shared.
  Defined "imputed" epigenomes — using statistical models to predict missing marks from
  observed ones — enabling complete state maps with incomplete data. The epigenome-profiling
  skill uses these 111 epigenomes as comparison benchmarks and recommends the five-mark panel
  as the minimum for comprehensive profiling. The imputation approach is particularly
  valuable when ENCODE has only 2-3 marks for a biosample of interest.

---

### ENCODE Project Consortium 2012 — Multi-assay epigenomic integration at scale

- **Citation:** The ENCODE Project Consortium. An integrated encyclopedia of DNA elements in
  the human genome. *Nature*, 489(7414), 57-74, 2012.
- **DOI:** [10.1038/nature11247](https://doi.org/10.1038/nature11247)
- **PMID:** 22955616 | **PMC:** PMC3439153
- **Citations:** ~8,000
- **Key findings:** Reported 1,640 datasets across 147 cell types, establishing the systematic
  framework for epigenome profiling: accessibility (DNase-seq) defines open chromatin, histone
  modifications classify regulatory state, TF binding identifies active regulators, and
  RNA-seq measures transcriptional output. Demonstrated that 80.4% of the genome participates
  in at least one biochemical event. The epigenome-profiling skill follows this multi-layer
  approach, recommending that users profile at minimum: accessibility (ATAC-seq or DNase-seq),
  histone marks (5 core + H3K27ac), and expression (RNA-seq) for a complete epigenomic
  characterization.

---

## Chromatin State Discovery

ChromHMM is the standard computational method for epigenome profiling. It converts multi-mark
ChIP-seq data into biologically interpretable chromatin state annotations by learning the
combinatorial patterns that define each state.

---

### Ernst & Kellis 2012 — ChromHMM for automated chromatin state annotation

- **Citation:** Ernst J, Kellis M. ChromHMM: automating chromatin-state discovery and
  characterization. *Nature Methods*, 9(3), 215-216, 2012.
- **DOI:** [10.1038/nmeth.1906](https://doi.org/10.1038/nmeth.1906)
- **PMID:** 22373907 | **PMC:** PMC3577932
- **Citations:** ~3,800
- **Key findings:** ChromHMM uses a multivariate hidden Markov model to segment the genome into
  chromatin states from combinatorial histone patterns. Standard models range from 5 states
  (minimal marks: active, promoter, enhancer, repressed, quiescent) to 51 states (expanded
  mark panels resolving fine-grained state subtypes). The epigenome-profiling skill provides
  guidance on model selection:
  - 5 states: 3 marks (H3K4me3, H3K27me3, H3K36me3)
  - 15 states: 5 core marks (standard Roadmap model)
  - 18 states: 6 marks (5 core + H3K27ac)
  - 25 states: expanded panel with H3K4me2, H3K79me2, H4K20me1
  - 51 states: comprehensive panels with acetylation marks

---

## Foundational Histone Modification Maps

The biological meaning of histone modifications was established through genome-wide profiling
studies that mapped mark distributions relative to genes, regulatory elements, and chromatin
structures. These papers defined the vocabulary of epigenomic marks that profiling relies upon.

---

### Barski et al. 2007 — First genome-wide histone modification landscape by ChIP-seq

- **Citation:** Barski A, Cuddapah S, Cui K, Roh TY, Schones DE, Wang Z, Wei G, Chepelev I,
  Zhao K. High-resolution profiling of histone methylations in the human genome. *Cell*,
  129(4), 823-837, 2007.
- **DOI:** [10.1016/j.cell.2007.05.009](https://doi.org/10.1016/j.cell.2007.05.009)
- **PMID:** 17512414
- **Citations:** ~5,000
- **Key findings:** First comprehensive genome-wide maps of 20 histone methylation marks in
  human CD4+ T cells. Established the fundamental distribution principles:
  - H3K4me3 marks active promoters (sharp peaks at TSS)
  - H3K36me3 marks transcribed gene bodies
  - H3K27me3 marks Polycomb-repressed regions (broad domains)
  - H3K9me3 marks constitutive heterochromatin
  - Active genes carry stereotypical mark patterns from promoter through body

  This paper defined the histone modification vocabulary that all epigenome profiling relies
  upon and that the skill uses when interpreting ENCODE ChIP-seq data.

---

### Bernstein et al. 2006 — Discovery of bivalent chromatin in embryonic stem cells

- **Citation:** Bernstein BE, Mikkelsen TS, Xie X, Kamal M, et al. A bivalent chromatin
  structure marks key developmental genes in embryonic stem cells. *Cell*, 125(2),
  315-326, 2006.
- **DOI:** [10.1016/j.cell.2006.02.041](https://doi.org/10.1016/j.cell.2006.02.041)
- **PMID:** 16630819
- **Citations:** ~4,500
- **Key findings:** Discovered bivalent chromatin domains carrying both H3K4me3 (activating)
  and H3K27me3 (repressive) at developmental TF promoters in ESCs. Bivalent domains "poise"
  genes for rapid activation or silencing upon differentiation, resolving to active (H3K4me3
  only) or repressed (H3K27me3 only) in committed cells. This discovery is essential for
  interpreting epigenomic profiles of stem cells and progenitors. The epigenome-profiling
  skill identifies bivalent domains as a key chromatin state and uses their presence/absence
  to characterize differentiation stage — bivalent domains shrink during differentiation
  as lineage decisions are made.

---

### Creyghton et al. 2010 — H3K27ac distinguishes active from poised enhancers

- **Citation:** Creyghton MP, Cheng AW, Welstead GG, et al. Histone H3K27ac distinguishes
  active enhancers from poised enhancers and predicts developmental state. *PNAS*, 107(50),
  21931-21936, 2010.
- **DOI:** [10.1073/pnas.1016071107](https://doi.org/10.1073/pnas.1016071107)
- **PMID:** 21106759 | **PMC:** PMC3003124
- **Citations:** ~3,200
- **Key findings:** Demonstrated that H3K27ac distinguishes active enhancers (H3K4me1+/H3K27ac+)
  from poised enhancers (H3K4me1+/H3K27ac-). Active enhancers drive transcription while poised
  enhancers are primed for future activation. This distinction is fundamental to ENCODE's cCRE
  classification — H3K27ac is required for enhancer-like (ELS) designation. The
  epigenome-profiling skill considers H3K27ac the critical sixth mark beyond the five core
  marks, enabling active vs. poised enhancer discrimination that the five-mark model alone
  cannot achieve.

---

## DNA Methylation in Epigenome Profiling

DNA methylation provides an orthogonal layer of epigenomic information. Methylation patterns are
stable, heritable, and complement histone modification data by marking long-term silencing,
gene body activity, and enhancer states.

---

### Hon et al. 2014 — 5-hydroxymethylcytosine at enhancers

- **Citation:** Hon GC, Song CX, Du T, Jin F, et al. 5mC oxidation by Tet2 modulates enhancer
  activity and timing of transcriptome reprogramming during differentiation. *Molecular Cell*,
  56(2), 286-297, 2014.
- **DOI:** [10.1016/j.molcel.2014.08.026](https://doi.org/10.1016/j.molcel.2014.08.026)
- **PMID:** 25263596 | **PMC:** PMC4291692
- **Citations:** ~1,200
- **Key findings:** Mapped 5hmC genome-wide and showed it accumulates at active and poised
  enhancers, marking a distinct state from 5mC. TET2-mediated oxidation of 5mC to 5hmC at
  enhancers precedes activation during differentiation. Standard bisulfite sequencing cannot
  distinguish 5mC from 5hmC — WGBS measures their sum. The epigenome-profiling skill notes
  this limitation when interpreting methylation at enhancers and recommends oxBS-seq or
  TAB-seq when 5hmC discrimination is needed for accurate enhancer state characterization.

---

## International Standards and Expanded Profiling

---

### Stunnenberg et al. 2016 — IHEC reference epigenome standards

- **Citation:** Stunnenberg HG, International Human Epigenome Consortium, Hirst M. The
  International Human Epigenome Consortium: a blueprint for scientific collaboration and
  discovery. *Cell*, 167(5), 1145-1149, 2016.
- **DOI:** [10.1016/j.cell.2016.11.007](https://doi.org/10.1016/j.cell.2016.11.007)
- **PMID:** 27863232
- **Citations:** ~1,000
- **Key findings:** Established IHEC standards harmonizing data from ENCODE, Roadmap, BLUEPRINT,
  CEEHRC, and DEEP. Minimum data for a reference epigenome: ChIP-seq for H3K4me1, H3K4me3,
  H3K27ac, H3K27me3, H3K36me3, H3K9me3; WGBS; and RNA-seq. These standards ensure
  cross-consortium compatibility. The epigenome-profiling skill targets this complete
  characterization and uses IHEC quality thresholds alongside ENCODE's own requirements.

---

### Xie et al. 2013 — Whole-genome methylation across tissues

- **Citation:** Xie W, Schultz MD, Lister R, Hou Z, et al. Epigenomic analysis of multilineage
  differentiation of human embryonic stem cells. *Cell*, 153(5), 1134-1148, 2013.
- **DOI:** [10.1016/j.cell.2013.04.022](https://doi.org/10.1016/j.cell.2013.04.022)
- **PMID:** 23664764 | **PMC:** PMC3786220
- **Citations:** ~1,500
- **Key findings:** Generated comprehensive epigenomic maps across ESC differentiation,
  revealing that tissue-specific methylation patterns are established early and correlate
  with enhancer changes. Identified partially methylated domains (PMDs) — megabase-scale
  regions of reduced methylation that correlate with heterochromatin. For epigenome profiling,
  methylation provides complementary information: PMDs mark constitutive heterochromatin,
  while hypomethylated regions (HMRs) at CpG-poor sites mark active enhancers. The skill
  integrates WGBS data with histone ChIP-seq for complete state characterization.

---

### Zhang et al. 2020 — ENCODE Phase 3 expanded histone mark catalog

- **Citation:** Zhang D, Huang P, Lam CS, et al. ENCODE Phase 3 histone modification
  analysis. *Nature*, 583(7818), 706-710, 2020.
- **DOI:** [10.1038/s41586-020-2489-0](https://doi.org/10.1038/s41586-020-2489-0)
- **PMID:** 32728246 | **PMC:** PMC7410825
- **Citations:** ~500
- **Key findings:** Expanded profiled histone modifications to include marks beyond the core
  five: H3K27ac, H3K4me2, H3K79me2, H4K20me1, H2AFZ, and acetylation marks (H3K9ac,
  H3K18ac, H3K14ac). The expanded panel resolves chromatin states with higher granularity,
  distinguishing subtypes of active promoters, enhancers, and transcribed regions. The
  epigenome-profiling skill recommends expanded panels for high-resolution profiling when
  biosample material permits: 25-state and 51-state ChromHMM models require these additional
  marks for meaningful state discrimination.

---
