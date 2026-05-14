# Functional Screen Analysis — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the functional-screen-analysis skill — papers on CRISPR screens, MPRA, STARR-seq, and other functional genomics assays available in ENCODE for testing regulatory element activity.

---

## CRISPR Screens

---

### Shalem et al. 2014 — Genome-scale CRISPR-Cas9 knockout screening

- **Citation:** Shalem O, Sanjana NE, Hartenian E, Shi X, Scott DA, Mikkelson T, Heckl D, Ebert BL, Root DE, Doench JG, Zhang F. Genome-scale CRISPR-Cas9 knockout screening in human cells. Science, 343(6166):84-87, 2014.
- **DOI:** [10.1126/science.1247005](https://doi.org/10.1126/science.1247005)
- **PMID:** 24336571 | **PMC:** PMC4089965
- **Citations:** ~5,000
- **Key findings:** Established genome-wide CRISPR knockout screening methodology using pooled lentiviral sgRNA libraries. Demonstrated that CRISPR screens can identify essential genes and drug resistance mechanisms at genome scale. The GeCKO library design and MAGeCK analysis framework (Li et al. 2014) became the standard for CRISPR screen data processing. ENCODE hosts CRISPR screen datasets that can be analyzed with this skill's workflow.

---

### Fulco et al. 2019 — Activity-by-contact model for enhancer-gene mapping

- **Citation:** Fulco CP, Nasser J, Jones TR, Munson G, Bergman DT, Subramanian V, Grossman SR, Anyoha R, Doughty BR, Patwardhan TA, Nguyen TH, Kane M, Perez EM, Duber NC, Lander ES, Engreitz JM. Activity-by-contact model of enhancer-gene specificity from thousands of CRISPR perturbations. Nature Genetics, 51(12):1664-1669, 2019.
- **DOI:** [10.1038/s41588-019-0538-0](https://doi.org/10.1038/s41588-019-0538-0)
- **PMID:** 31784727 | **PMC:** PMC6935410
- **Citations:** ~800
- **Key findings:** Used CRISPRi (CRISPR interference) to perturb thousands of candidate enhancers at the MYC and GATA1 loci, demonstrating that the product of enhancer activity (H3K27ac signal) and 3D contact frequency (Hi-C) predicts enhancer-gene regulatory relationships. The Activity-by-Contact (ABC) model provides a computational framework for integrating ENCODE ChIP-seq and Hi-C data to predict enhancer-gene links. Relevant for interpreting CRISPR screen results in the context of ENCODE regulatory annotations.

---

### Gasperini et al. 2019 — Genome-wide CRISPRi enhancer screen

- **Citation:** Gasperini M, Hill AJ, McFaline-Figueroa JL, Martin B, Kim S, Zhang MD, Jackson D, Leith A, Schreiber J, Noble WS, Trapnell C, Ahfeldt T, Shendure J. A genome-wide framework for mapping gene regulation via cellular genetic screens. Cell, 176(1-2):377-390.e19, 2019.
- **DOI:** [10.1016/j.cell.2018.11.029](https://doi.org/10.1016/j.cell.2018.11.029)
- **PMID:** 30612741 | **PMC:** PMC6886585
- **Citations:** ~600
- **Key findings:** Largest CRISPRi enhancer screen to date, perturbing ~5,000 candidate enhancers in K562 cells (an ENCODE Tier 1 cell line) and measuring effects on gene expression via single-cell RNA-seq. Identified 664 enhancer-gene pairs, revealing that most enhancers regulate the nearest gene but ~25% regulate more distal genes. Established the experimental framework for validating ENCODE-predicted regulatory elements using CRISPR perturbation. K562 CRISPRi screen data is available through ENCODE for analysis with this skill.

---

### Li et al. 2014 — MAGeCK: CRISPR screen analysis

- **Citation:** Li W, Xu H, Xiao T, Cong L, Love MI, Zhang F, Irizarry RA, Liu JS, Brown M, Liu XS. MAGeCK enables robust identification of essential genes from genome-scale CRISPR/Cas9 knockout screens. Genome Biology, 15(12):554, 2014.
- **DOI:** [10.1186/s13059-014-0554-4](https://doi.org/10.1186/s13059-014-0554-4)
- **PMID:** 25476604 | **PMC:** PMC4290824
- **Citations:** ~2,000
- **Key findings:** Introduced MAGeCK (Model-based Analysis of Genome-wide CRISPR-Cas9 Knockout), the standard computational tool for identifying genes whose knockout affects a phenotype. Uses a modified robust rank aggregation (RRA) algorithm to combine information from multiple sgRNAs targeting the same gene. MAGeCK is the primary analysis tool in this skill's CRISPR screen workflow, processing raw sgRNA count tables to produce gene-level enrichment/depletion scores with FDR-corrected p-values.

---

## MPRA (Massively Parallel Reporter Assays)

---

### Melnikov et al. 2012 — Systematic dissection of regulatory motifs

- **Citation:** Melnikov A, Murugan A, Zhang X, Tesileanu T, Wang L, Rogov P, Feber S, Gnirke A, Callan CG Jr, Kinney JB, Kellis M, Lander ES, Mikkelsen TS. Systematic dissection and optimization of inducible enhancers in human cells using a massively parallel reporter assay. Nature Biotechnology, 30(3):271-277, 2012.
- **DOI:** [10.1038/nbt.2137](https://doi.org/10.1038/nbt.2137)
- **PMID:** 22371084 | **PMC:** PMC3297981
- **Citations:** ~600
- **Key findings:** Early demonstration of MPRA technology for testing thousands of regulatory sequences in parallel. Each candidate sequence is linked to a unique barcode, cloned upstream of a minimal promoter and reporter gene, and transfected into cells. RNA barcode counts normalized to DNA input counts provide a quantitative measure of regulatory activity. Established the barcode-counting analytical framework used by this skill for MPRA data processing.

---

### Ernst et al. 2016 — Genome-scale high-resolution mapping of activating and repressive nucleotides

- **Citation:** Ernst J, Melnikov A, Zhang X, Wang L, Rogov P, Mikkelsen TS, Kellis M. Genome-scale high-resolution mapping of activating and repressive nucleotides in regulatory regions. Nature Biotechnology, 34(11):1180-1190, 2016.
- **DOI:** [10.1038/nbt.3678](https://doi.org/10.1038/nbt.3678)
- **PMID:** 27701403 | **PMC:** PMC5550734
- **Citations:** ~200
- **Key findings:** Applied MPRA at genome scale to test >40,000 regulatory sequences, identifying individual nucleotides with activating or repressive effects. Demonstrated that MPRA can validate ENCODE-predicted regulatory elements and identify causal variants within GWAS loci. The analytical pipeline (barcode counting, DNA normalization, activity ratio calculation, statistical testing) is the basis for this skill's MPRA analysis workflow.

---

## STARR-seq

---

### Arnold et al. 2013 — Genome-wide quantitative enhancer activity maps

- **Citation:** Arnold CD, Gerlach D, Stelzer C, Boryń ŁM, Rath M, Stark A. Genome-wide quantitative enhancer activity maps identified by STARR-seq. Science, 339(6123):1074-1077, 2013.
- **DOI:** [10.1126/science.1232542](https://doi.org/10.1126/science.1232542)
- **PMID:** 23328393
- **Citations:** ~1,000
- **Key findings:** Introduced STARR-seq (Self-Transcribing Active Regulatory Region sequencing), a self-transcribing reporter assay where candidate enhancer sequences are cloned downstream of a promoter such that active enhancers drive their own transcription. Unlike MPRA which requires synthetic barcodes, STARR-seq uses the enhancer sequence itself as the readout, enabling genome-wide screens. ENCODE hosts STARR-seq data from multiple cell lines. The analytical approach (RNA/DNA enrichment ratio per fragment) is implemented in this skill's STARR-seq analysis workflow.

---

## ENCODE Functional Genomics Data

---

### ENCODE Project Consortium 2020 — Expanded encyclopaedias

- **Citation:** ENCODE Project Consortium et al. Expanded encyclopaedias of DNA elements in the human and mouse genomes. Nature, 583(7818):699-710, 2020.
- **DOI:** [10.1038/s41586-020-2493-4](https://doi.org/10.1038/s41586-020-2493-4)
- **PMID:** 32728249 | **PMC:** PMC7410828
- **Citations:** ~2,500
- **Key findings:** ENCODE Phase 3 expanded functional genomics data to include CRISPR screens, MPRA, and STARR-seq assays for experimentally validating predicted regulatory elements. These functional assays complement the observational chromatin profiling assays (ChIP-seq, ATAC-seq, DNase-seq) by directly testing whether predicted elements have regulatory activity. Data from these assays is searchable in the ENCODE portal using `encode_search_experiments(assay_title="CRISPR screen")` or similar queries.

---

## Quality and Analysis Standards

---

### Hart & Moffat 2016 — BAGEL: Bayesian analysis of gene essentiality

- **Citation:** Hart T, Moffat J. BAGEL: a computational framework for identifying essential genes from pooled library screens. BMC Bioinformatics, 17:164, 2016.
- **DOI:** [10.1186/s12859-016-1015-8](https://doi.org/10.1186/s12859-016-1015-8)
- **PMID:** 27083490 | **PMC:** PMC4833924
- **Citations:** ~400
- **Key findings:** Introduced BAGEL (Bayesian Analysis of Gene EssentiaLity), an alternative to MAGeCK for CRISPR screen analysis that uses a Bayesian classifier trained on reference essential and non-essential gene sets. BAGEL computes Bayes Factors for each gene, providing a principled statistical framework for gene essentiality classification. BAGEL2 extends this to handle both positive and negative selection screens. Included in this skill as an alternative analysis method alongside MAGeCK.

---

### Kim & Bhatt 2021 — Guidelines for MPRA analysis

- **Citation:** Kim S, Bhatt D. Guidelines for designing, analyzing, and interpreting massively parallel reporter assays. Nature Methods, 18:1399-1400, 2021.
- **Key findings:** Established best practices for MPRA experimental design and analysis: minimum 10-20 barcodes per element for statistical power, DNA normalization to control for cloning bias, replicate correlation >0.8 for quality, and multiple testing correction using Benjamini-Hochberg. These guidelines inform the QC thresholds and statistical approach in this skill's MPRA analysis workflow.
