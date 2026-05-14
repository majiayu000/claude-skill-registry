# GTEx Expression — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the gtex-expression skill — key papers informing tissue-specific gene expression analysis, eQTL mapping, and transcriptome-wide association studies using the Genotype-Tissue Expression project.

---

## Core GTEx Releases

---

### GTEx Consortium 2020 — GTEx v8: the definitive multi-tissue expression resource

- **Citation:** GTEx Consortium. The GTEx Consortium atlas of genetic
  regulatory effects across human tissues. Science, 369(6509):1318-1330, 2020.
- **DOI:** [10.1126/science.aaz1776](https://doi.org/10.1126/science.aaz1776)
- **PMID:** 32913098 | **PMC:** PMC7737656
- **Citations:** ~4,000
- **Key findings:** GTEx v8 profiled gene expression via RNA-seq across 54
  tissue types from 838 postmortem donors, generating the largest multi-tissue
  eQTL map with 4.1 million significant cis-eQTLs across 49 tissues.
  Demonstrated that 95% of protein-coding genes have at least one eQTL in at
  least one tissue, with approximately 30% of eQTLs showing tissue-specific or
  tissue-enriched effects — meaning that genetic regulation of gene expression
  is pervasive but often constrained to particular biological contexts.
  Introduced MASH (Multivariate Adaptive Shrinkage) for Bayesian multi-tissue
  eQTL sharing analysis, revealing that most eQTL effect sizes are shared
  across tissues but with quantitative magnitude differences reflecting
  tissue-specific regulatory activity. The v8 release also expanded splicing
  QTL (sQTL) analysis, identifying 32,663 sQTL associations affecting
  alternative splicing in a tissue-dependent manner, often at loci distinct
  from eQTLs — demonstrating that genetic variants regulate gene output at
  both the expression level and the isoform level. This dataset is the
  foundational resource for interpreting GWAS variants in regulatory context —
  by overlapping GWAS hits with GTEx eQTLs and sQTLs, researchers can identify
  which gene is affected, in which tissue, and through which regulatory
  mechanism (expression vs. splicing), connecting non-coding variants to
  specific molecular mechanisms.

---

### Aguet et al. 2017 — Multi-tissue eQTL mapping reveals regulatory mechanisms

- **Citation:** Aguet F, Brown AA, Castel SE, Davis JR, He Y, Jo B, Mohammadi
  P, Park Y, Parsana P, Segre AV, et al. Genetic effects on gene expression
  across human tissues. Nature, 550(7675):204-213, 2017.
- **DOI:** [10.1038/nature24277](https://doi.org/10.1038/nature24277)
- **PMID:** 29022597 | **PMC:** PMC5776756
- **Citations:** ~2,500
- **Key findings:** GTEx v6p analysis of 44 tissues identified cis-eQTLs for
  19,725 protein-coding and 3,692 lncRNA genes, establishing these as "eGenes"
  with genetically controlled expression levels. Demonstrated that cis-eQTLs
  map predominantly within 1 Mb of the TSS with strong enrichment in promoters
  and enhancers annotated by ENCODE and Roadmap Epigenomics, directly linking
  histone modification patterns to functional genetic variation. Tissue-
  sharing analysis revealed distinct regulatory clusters: immune tissues share
  eQTLs with each other, brain regions form a separate regulatory cluster, and
  reproductive tissues (testis, ovary) show unique effects rarely shared with
  other tissues. The multi-tissue framework enabled identification of "master
  regulatory variants" affecting gene expression across dozens of tissues,
  distinguishing these from tissue-restricted regulatory effects.

---

### GTEx Consortium 2015 — GTEx pilot: establishing the genotype-tissue expression resource

- **Citation:** GTEx Consortium. Human genomics. The Genotype-Tissue
  Expression (GTEx) pilot analysis: multitissue gene regulation in humans.
  Science, 348(6235):648-660, 2015.
- **DOI:** [10.1126/science.1262110](https://doi.org/10.1126/science.1262110)
- **PMID:** 25954001 | **PMC:** PMC4547484
- **Citations:** ~3,500
- **Key findings:** Pilot phase analyzing 1,641 samples across 43 tissues from
  175 donors, establishing the feasibility and scientific value of systematic
  multi-tissue eQTL mapping from postmortem samples. Showed that tissue-
  specific eQTLs are significantly enriched in tissue-specific enhancers
  defined by histone modifications (H3K27ac, H3K4me1 from Roadmap
  Epigenomics), providing the first genome-wide evidence that chromatin-
  defined regulatory elements harbor functional genetic variants. Demonstrated
  that allelic expression (ASE) analysis within individuals provides
  independent validation of population-level eQTL effects and can detect
  regulatory variants with smaller sample sizes. Established the analytical
  framework — including correction for hidden confounders using PEER factors
  and permutation-based significance thresholds — that all subsequent GTEx
  analyses built upon, and which became the de facto standard for eQTL
  studies.

---

## TWAS / Gene-Level Methods

---

### Gamazon et al. 2015 — PrediXcan: gene-level association testing from genotypes

- **Citation:** Gamazon ER, Wheeler HE, Shah KP, Mozaffari SV, Aquino-Michaels
  K, Carroll RJ, Eyler AE, Denny JC, GTEx Consortium, Nicolae DL, Cox NJ, Im
  HK. A gene-based association method for mapping traits using reference
  transcriptome data. Nature Genetics, 47(9):1091-1098, 2015.
- **DOI:** [10.1038/ng.3367](https://doi.org/10.1038/ng.3367)
- **PMID:** 26258848 | **PMC:** PMC4552594
- **Citations:** ~2,500
- **Key findings:** Introduced PrediXcan, which imputes tissue-specific gene
  expression from genotype data using elastic net models trained on GTEx
  reference panels, then tests the association between imputed expression and
  phenotype. By aggregating the effects of multiple regulatory variants into a
  single gene-level test statistic, PrediXcan increases statistical power over
  single-variant GWAS and provides directional interpretation — whether higher
  or lower expression of a specific gene in a specific tissue associates with
  disease. Demonstrated that gene-level associations replicate across
  independent cohorts at substantially higher rates than single-SNP
  associations, suggesting they capture more biologically meaningful signals.
  PrediXcan launched the transcriptome-wide association study (TWAS) field,
  creating a direct bridge between ENCODE regulatory annotations (which define
  which variants are regulatory) and disease genetics (which identifies which
  variants matter for phenotypes).

---

### Barbeira et al. 2018 — MetaXcan: multi-tissue TWAS framework

- **Citation:** Barbeira AN, Dickinson SP, Bonazzola R, Zheng J, Wheeler HE,
  Torres JM, Tober ES, Shah KP, Edwards TL, Stahl EA, et al. Exploring the
  phenotypic consequences of tissue specific gene expression variation
  inferred from GWAS summary statistics. Nature Communications, 9(1):1825,
  2018.
- **DOI:** [10.1038/s41467-018-03621-1](https://doi.org/10.1038/s41467-018-03621-1)
- **PMID:** 29739930 | **PMC:** PMC5940825
- **Citations:** ~1,200
- **Key findings:** Extended PrediXcan to work with GWAS summary statistics
  (S-PrediXcan) rather than requiring individual-level genotype data, vastly
  expanding applicability to the thousands of published GWAS results with
  publicly available summary statistics. The MetaXcan framework integrates
  TWAS results across multiple tissues, using multi-tissue meta-analysis to
  identify 247 novel gene-trait associations across 108 phenotypes from GWAS
  Catalog studies. Showed that multi-tissue analysis increases power by
  leveraging regulatory effects shared across related tissues (e.g., combining
  all 13 brain regions for neuropsychiatric traits, or combining adipose
  subcutaneous and visceral for metabolic traits) while maintaining the ability
  to identify tissue-specific effects through conditional analysis. Revealed
  that many GWAS loci contain multiple independent gene-trait associations
  operating in different tissues, suggesting more complex regulatory
  architectures than the "one locus, one gene" model implies. The summary
  statistics-based approach also enables colocalization analysis with ENCODE
  regulatory annotations, testing whether the same causal variant drives both
  the GWAS signal and the eQTL signal within a specific chromatin context.

---

## Cell-Type Resolution

---

### Kim-Hellmuth et al. 2020 — Cell-type-specific eQTLs from GTEx bulk tissue

- **Citation:** Kim-Hellmuth S, Aguet F, Oliva M, Munoz-Aguirre M, Kasela S,
  Wucher V, Castel SE, Hamel AR, Vinuela A, Roberts AL, et al. Cell type-
  specific genetic regulation of gene expression across human tissues.
  Science, 369(6509):eaaz8528, 2020.
- **DOI:** [10.1126/science.aaz8528](https://doi.org/10.1126/science.aaz8528)
- **PMID:** 32913075 | **PMC:** PMC7668455
- **Citations:** ~800
- **Key findings:** Used computational deconvolution of GTEx v8 bulk RNA-seq
  to estimate cell type proportions per sample, then identified cell-type-
  interaction eQTLs (ct-eQTLs) whose regulatory effects depend on the
  abundance of specific cell types. Found 3,347 ct-eQTLs across 8 tissues,
  with ~20% representing effects entirely missed by standard bulk eQTL
  analysis because they average out across cell types. Many ct-eQTLs
  colocalize with cell-type-specific ATAC-seq peaks from ENCODE and with GWAS
  loci, suggesting that disease-associated variants frequently act through
  specific cell populations within heterogeneous tissues. This work
  established that bulk tissue eQTL studies — including GTEx — systematically
  underestimate the complexity of gene regulation and miss cell-type-specific
  disease mechanisms that single-cell or deconvolution approaches can reveal.

---

### Eraslan et al. 2022 — Single-cell GTEx: cell-type resolution across human tissues

- **Citation:** Eraslan G, Drokhlyansky E, Anber S, Regev A, et al. Single-
  nucleus cross-tissue molecular reference maps toward understanding disease
  gene function. Science, 376(6594):eabl4290, 2022.
- **DOI:** [10.1126/science.abl4290](https://doi.org/10.1126/science.abl4290)
- **PMID:** 35549429 | **PMC:** PMC9744718
- **Citations:** ~600
- **Key findings:** Generated single-nucleus RNA-seq profiles from ~200,000
  nuclei across 8 tissue types from GTEx donors with matched genotype data,
  creating the first cell-type-resolution expression atlas linked to
  individual genomes. Identified 6,600 cell-type-level eQTLs, of which 43%
  showed significant cell-type specificity invisible in bulk tissue analysis.
  Disease-associated GWAS variants were enriched in cell-type-specific eQTLs
  corresponding to pathogenically relevant cell types — hepatocytes for liver
  disease, podocytes for kidney disease, glutamatergic neurons for
  neuropsychiatric conditions. This single-cell GTEx pilot proved that cell-
  type-resolved eQTL mapping is essential for mechanistic interpretation of
  GWAS results, for identifying causal cell types, and for understanding why
  the same genetic variant can have different effects in different tissues —
  namely because it operates in cell types present at varying proportions
  across tissues.

---
