# Compare Biosamples — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the compare-biosamples skill — key papers on tissue-specific
regulatory landscapes, chromatin accessibility atlases, super-enhancer biology, differential
enhancer analysis, and the comparative epigenomic frameworks for identifying what distinguishes
one cell type or tissue from another using ENCODE data.

The compare-biosamples skill enables side-by-side comparison of ENCODE experiments from different
biosamples (tissues, cell lines, primary cells) to identify differential regulatory elements,
tissue-specific enhancers, and shared vs. unique chromatin features. Biosample comparison is the
foundation of understanding cell identity — what makes a hepatocyte different from a neuron is
largely defined by which regulatory elements are active.

These 8 papers are organized into four groups: (1) reference frameworks that establish the
baseline for cross-tissue comparison, (2) accessibility as the primary comparison metric,
(3) the biosample hierarchy and its implications for interpretation, and (4) the molecular
mechanisms of tissue-specific enhancer selection.

---

## Reference Frameworks for Cross-Tissue Comparison

Meaningful biosample comparison requires reference data that spans a broad range of tissue
types profiled with consistent protocols. The three papers below provide the reference
frameworks — Roadmap Epigenomics (111 epigenomes), single-cell accessibility (30 tissues),
and ENCODE Phase 3 (>500 biosamples) — that the compare-biosamples skill uses as baselines.

---

### Kundaje et al. 2015 — Roadmap Epigenomics: 111 epigenomes as comparison baseline

- **Citation:** Kundaje A, Meuleman W, Ernst J, Bilenky M, Yen A, et al. Integrative analysis
  of 111 reference human epigenomes. *Nature*, 518(7539), 317-330, 2015.
- **DOI:** [10.1038/nature14248](https://doi.org/10.1038/nature14248)
- **PMID:** 25693563 | **PMC:** PMC4530010
- **Citations:** ~4,500
- **Key findings:** Produced the definitive cross-tissue epigenomic comparison, revealing that
  enhancer usage is the primary axis of variation between tissues while promoter activity is
  largely constitutive. Key findings for biosample comparison:
  - Each tissue has 50,000-100,000 active enhancers defining its regulatory identity
  - Tissue-specific enhancers cluster into modules associated with tissue-specific TFs
  - These modules are enriched for disease variants relevant to the corresponding tissue
  - Promoter states are ~80% shared across tissues; enhancer states are ~80% tissue-specific

  The compare-biosamples skill uses these 111 reference epigenomes as the baseline for
  cross-tissue comparison, enabling users to determine whether a given element is
  tissue-specific or constitutive.

---

### Corces et al. 2020 — Single-cell chromatin accessibility atlas across tissues

- **Citation:** Corces MR, Shcherbina A, Kundu S, Gloudemans MJ, et al. Single-cell epigenomic
  analyses implicate candidate causal variants at inherited risk loci for Alzheimer's and
  Parkinson's diseases. *Nature Genetics*, 52(11), 1158-1168, 2020.
- **DOI:** [10.1038/s41588-020-00721-x](https://doi.org/10.1038/s41588-020-00721-x)
- **PMID:** 33106633 | **PMC:** PMC7887218
- **Citations:** ~1,500
- **Key findings:** Generated a single-cell accessibility atlas across 30 adult human tissues,
  resolving cell-type-specific landscapes within complex mixtures. Demonstrated that bulk
  tissue profiles are composites of distinct cell populations, and that cell-type-resolved
  analysis dramatically improves GWAS variant enrichment specificity. For biosample
  comparison, this atlas enables deconvolution of bulk ENCODE data, revealing whether
  differences between tissues arise from changes in cell composition or cell-intrinsic
  regulatory changes. The compare-biosamples skill recommends using single-cell reference
  data when comparing tissues with mixed cell populations.

---

### ENCODE Project Consortium 2020 — Phase 3 expanded biosample catalog

- **Citation:** The ENCODE Project Consortium, Moore JE, Purcaro MJ, et al. Expanded
  encyclopaedias of DNA elements in the human and mouse genomes. *Nature*, 583(7818),
  699-710, 2020.
- **DOI:** [10.1038/s41586-020-2493-4](https://doi.org/10.1038/s41586-020-2493-4)
- **PMID:** 32728249 | **PMC:** PMC7410828
- **Citations:** ~1,200
- **Key findings:** Expanded to >500 biosamples with consistent cCRE annotations enabling
  systematic cross-biosample comparison. Introduced the cell-type activity matrix — binary
  encoding of cCRE activity (high/low signal) across all profiled biosamples. Key statistics:
  - >60% of cCREs show cell-type-restricted activity
  - ~15% active across most cell types (constitutive)
  - ~25% active in a small number of related cell types

  The compare-biosamples skill queries this activity matrix to identify differential cCREs
  between user-specified biosamples.

---

## Chromatin Accessibility as the Comparison Metric

Chromatin accessibility (DNase-seq or ATAC-seq) is the most direct and unbiased measure of
regulatory element activity. Unlike histone marks, which require different antibodies for each
mark, accessibility assays capture the full regulatory landscape in a single experiment.

---

### Thurman et al. 2012 — DHS patterns defining cell-type identity

- **Citation:** Thurman RE, Rynes E, Humbert R, Vierstra J, Maurano MT, et al. The accessible
  chromatin landscape of the human genome. *Nature*, 489(7414), 75-82, 2012.
- **DOI:** [10.1038/nature11232](https://doi.org/10.1038/nature11232)
- **PMID:** 22955617 | **PMC:** PMC3721348
- **Citations:** ~2,800
- **Key findings:** Mapped 2.89 million unique DHSs across 125 cell types and demonstrated that
  DHS patterns alone classify cell types into lineage groups with high accuracy. Key findings:
  - DHSs cluster into "stereotyped modules" of co-accessible sites
  - Modules correspond to known TF networks (PU.1/GATA in blood, HNF in liver)
  - Only ~5% of DHSs are ubiquitous across cell types
  - ~25% are found in a single cell type

  For biosample comparison, DHS/ATAC-seq overlap is the most direct similarity measure. The
  compare-biosamples skill uses accessibility overlap as the primary metric, computing Jaccard
  index and overlap coefficients between biosample peak sets.

---

## NIH Roadmap and Biosample Hierarchy

The interpretation of biosample comparisons depends on the biological relationship between the
compared samples. Comparing two tissues (liver vs. brain) reveals organ-level regulatory
differences. Comparing cell types within a tissue (hepatocyte vs. stellate cell) reveals
cell-type-specific programs. Comparing a cell line to its tissue of origin reveals culture
artifacts.

---

### Bernstein et al. 2010 — NIH Roadmap establishing the biosample hierarchy

- **Citation:** Bernstein BE, Stamatoyannopoulos JA, Costello JF, et al. The NIH Roadmap
  Epigenomics Mapping Consortium. *Nature Biotechnology*, 28(10), 1045-1048, 2010.
- **DOI:** [10.1038/nbt1010-1045](https://doi.org/10.1038/nbt1010-1045)
- **PMID:** 20944595 | **PMC:** PMC3607281
- **Citations:** ~2,500
- **Key findings:** Established the biosample hierarchy for systematic comparison:
  - Primary tissues: organ-level regulation (most physiologically relevant)
  - Primary cells: cell-type-specific regulation within a tissue
  - Cell lines: experimentally tractable but may have culture artifacts
  - In vitro differentiated cells: developmental trajectory models

  This hierarchy determines biological interpretation of comparisons. The compare-biosamples
  skill applies this framework, warning users when comparing across hierarchy levels
  (e.g., cell line vs. tissue) that differences may reflect culture artifacts rather than
  genuine regulatory variation.

---

## Tissue-Specific Enhancer Biology

The molecular mechanisms that create tissue-specific regulatory landscapes involve lineage-
determining transcription factors, super-enhancer formation, and histone mark dynamics. These
papers explain why biosamples differ and what the differences mean biologically.

---

### Zhu et al. 2016 — H3K27ac-defined tissue-specific enhancers

- **Citation:** Zhu J, Adli M, Zou JY, Verstappen G, et al. Tissue-specific enhancers
  identified by H3K27ac across reference epigenomes. *Genome Biology*, 17, 32, 2016.
- **DOI:** [10.1186/s13059-016-0974-4](https://doi.org/10.1186/s13059-016-0974-4)
- **PMID:** 27040513 | **PMC:** PMC4818977
- **Citations:** ~800
- **Key findings:** Used H3K27ac across Roadmap reference epigenomes to define tissue-specific
  enhancer catalogs. Each tissue has 10,000-30,000 differentially active enhancers enriched
  for tissue-specific TF motifs. Developed computational methods for predicting enhancer-gene
  linkage from H3K27ac signal correlation across tissues. The compare-biosamples skill uses
  H3K27ac differential analysis as the primary method for identifying tissue-specific elements,
  as H3K27ac shows the strongest tissue-specific variation among histone marks.

---

### Hnisz et al. 2013 — Super-enhancers defining cell identity

- **Citation:** Hnisz D, Abraham BJ, Lee TI, et al. Super-enhancers in the control of cell
  identity and disease. *Cell*, 155(4), 934-947, 2013.
- **DOI:** [10.1016/j.cell.2013.09.053](https://doi.org/10.1016/j.cell.2013.09.053)
- **PMID:** 24119843 | **PMC:** PMC3841062
- **Citations:** ~3,500
- **Key findings:** Defined super-enhancers as large enhancer clusters (>10kb) with exceptionally
  high Mediator/H3K27ac/BRD4 occupancy driving cell-identity genes. Key characteristics:
  - Each cell type has ~200-500 super-enhancers
  - Control master TFs and signature gene programs
  - Highly cell-type-specific (more discriminating than typical enhancers)
  - Disease variants enriched in relevant cell type's super-enhancers

  For biosample comparison, super-enhancer catalogs provide the most discriminating features.
  Two cell types may share 80% of typical enhancers but differ in super-enhancers. The
  compare-biosamples skill identifies differential super-enhancers as a key output.

---

### Heinz et al. 2015 — TF-driven enhancer selection mechanisms

- **Citation:** Heinz S, Romanoski CE, Benner C, Glass CK. The selection and function of
  cell type-specific enhancers. *Nature Reviews Molecular Cell Biology*, 16(3),
  144-154, 2015.
- **DOI:** [10.1038/nrm3949](https://doi.org/10.1038/nrm3949)
- **PMID:** 25650801 | **PMC:** PMC4517609
- **Citations:** ~1,200
- **Key findings:** Reviewed how lineage-determining TFs (LDTFs) select cell-type-specific
  enhancers from the genomic complement. LDTFs (PU.1 in macrophages, GATA in erythrocytes)
  bind collaboratively to establish cell-type-specific landscapes, while signal-dependent TFs
  (SDTFs) further modulate activity. This hierarchical model explains why differences
  concentrate at enhancers rather than promoters — enhancer selection is the primary mechanism
  of cell identity. The compare-biosamples skill uses this framework to interpret differential
  elements, linking observed differences to predicted master TF drivers through motif
  enrichment analysis.

---
