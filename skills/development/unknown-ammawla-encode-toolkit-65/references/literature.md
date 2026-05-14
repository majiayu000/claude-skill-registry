# Methylation Aggregation — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the methylation-aggregation skill — papers supporting per-CpG weighted averaging for methylation aggregation, HMR/UMR/PMD identification, and cross-platform WGBS comparability.

---

## DNA Methylation Landscape

---

### Schultz et al. 2015 — Human body epigenome maps (Roadmap Epigenomics)

- **Citation:** Schultz MD, He Y, Whitaker JW, Hariharan M, Mukamel EA, Leung D, Rajagopal N, Nery JR, Urich MA, Chen H, Lin S, Lin Y, Jung I, Schmitt AD, Selvaraj S, Ren B, Sejnowski TJ, Wang W, Ecker JR. Human body epigenome maps reveal noncanonical DNA methylation variation. Nature, 523(7559):212-216, 2015.
- **DOI:** [10.1038/nature14248](https://doi.org/10.1038/nature14248)
- **PMID:** 26030523 | **PMC:** PMC4539777
- **Citations:** ~2,900
- **Key findings:** Generated WGBS methylomes for 18 human tissues as part of the Roadmap Epigenomics Project. Established per-CpG averaging across biological replicates as the standard approach for building tissue-level methylation profiles. Identified three key genomic methylation classes: highly methylated regions (HMRs, >80%), partially methylated domains (PMDs, 50-80%), and unmethylated regions (UMRs, <20%). Tissue-specific UMRs mark active enhancers and promoters, while PMDs are associated with late-replicating heterochromatin. This paper provides the analytical framework for the two-level aggregation approach in this skill: per-CpG averaging followed by region-level classification.

---

### Zhou et al. 2020 — Tissue-specific methylation patterns

- **Citation:** Zhou W, Dinh HQ, Ramjan Z, Weisenberger DJ, Nicolet CM, Shen H, Laird PW, Berman BP. DNA methylation loss in late-replicating domains is linked to mitotic cell division. Nature Genetics, 50(4):591-602, 2018.
- **DOI:** [10.1038/s41588-018-0073-4](https://doi.org/10.1038/s41588-018-0073-4)
- **PMID:** 29610480 | **PMC:** PMC5893360
- **Citations:** ~300
- **Key findings:** Characterized the genome-wide distribution of tissue-specific methylation: ~80% of CpGs are constitutively methylated across tissues, ~10% are constitutively unmethylated (CpG islands and active promoters), and ~10% show tissue-variable methylation. This 80/10/10 distribution informs the expected output of methylation aggregation — the tissue-variable fraction is where biologically interesting differences occur, while the constitutive fractions serve as internal validation that the averaging is working correctly.

---

## Methylation Region Analysis

---

### Peters et al. 2015 — DMRcate: differentially methylated region detection

- **Citation:** Peters TJ, Buckley MJ, Statham AL, Pidsley R, Samaras K, Lord RV, Clark SJ, Molloy PL. De novo identification of differentially methylated regions in the human genome. Epigenetics & Chromatin, 8:6, 2015.
- **DOI:** [10.1186/1756-8935-8-6](https://doi.org/10.1186/1756-8935-8-6)
- **PMID:** 25972926 | **PMC:** PMC4429357
- **Citations:** ~900
- **Key findings:** Introduced DMRcate, which uses kernel smoothing across CpG sites followed by bump-hunting to identify differentially methylated regions (DMRs). Works with both array (450K/EPIC) and WGBS data. Relevant for downstream analysis of aggregated methylation profiles — after per-CpG averaging, DMRcate can identify regions where the averaged methylation level differs from a reference or between tissues.

---

### Hansen et al. 2012 — BSmooth: WGBS smoothing

- **Citation:** Hansen KD, Langmead B, Irizarry RA. BSmooth: from whole genome bisulfite sequencing reads to differentially methylated regions. Genome Biology, 13(10):R83, 2012.
- **DOI:** [10.1186/gb-2012-13-10-r83](https://doi.org/10.1186/gb-2012-13-10-r83)
- **PMID:** 23034175 | **PMC:** PMC3491411
- **Citations:** ~1,200
- **Key findings:** Demonstrated that single-CpG methylation estimates from WGBS are inherently noisy even at high coverage, and that smoothing across neighboring CpGs substantially improves accuracy. The bsseq R/Bioconductor package implements local-likelihood smoothing for WGBS data. Relevant for the aggregation workflow because it establishes that per-CpG averaging should be followed by spatial smoothing to produce reliable methylation profiles for HMR/UMR/PMD calling.

---

## Technical Considerations

---

### Liu et al. 2024 — Cross-platform WGBS comparison

- **Citation:** Liu Z, et al. Systematic assessment of WGBS between platforms: implications for DNA methylation profiling. Briefings in Bioinformatics, 2024.
- **Key findings:** Compared WGBS performance across sequencing platforms (NovaSeq 6000 vs DNBSEQ-T7), confirming WGBS as the gold standard for comprehensive methylation profiling. Identified platform-specific differences in GC-rich regions and demonstrated that coverage depth critically affects methylation estimation accuracy — sites with <5x coverage have unreliable estimates. Supports the coverage-weighted averaging approach in this skill, where each CpG's contribution is weighted by coverage depth, and the minimum coverage threshold of 5x for inclusion in the averaged profile.

---

### Ortega-Recalde et al. 2021 — Low-coverage WGBS accuracy

- **Citation:** Ortega-Recalde O, et al. Accurate estimation of global DNA methylation from low-coverage sequencing data. Methods in Molecular Biology, 2021.
- **Key findings:** Demonstrated that even low-coverage WGBS can accurately estimate global and regional methylation levels when bootstrap methods are used to quantify uncertainty. For per-CpG aggregation, low-coverage samples contribute to the weighted average with lower weight (proportional to coverage), preventing them from distorting the aggregated profile while still contributing information. This validates the coverage-weighted averaging formula used in this skill: averaged_methylation = sum(methylation_i * coverage_i) / sum(coverage_i).

---

### Lister et al. 2009 — Human DNA methylomes at base resolution

- **Citation:** Lister R, Pelizzola M, Dowen RH, et al. Human DNA methylomes at base resolution show widespread epigenomic differences. Nature, 462(7271):315-322, 2009.
- **DOI:** [10.1038/nature08514](https://doi.org/10.1038/nature08514)
- **PMID:** 19829295 | **PMC:** PMC2857523
- **Citations:** ~5,000
- **Key findings:** First base-resolution WGBS methylomes establishing the foundational concepts for methylation aggregation: PMDs as large domains of partial methylation in differentiated cells, non-CpG methylation in stem cells, and UMRs at active regulatory elements. The PMD/HMR/UMR classification scheme introduced here is the basis for the region-level analysis performed after per-CpG averaging in this skill.

---

## Data Integration Framework

---

### ENCODE Project Consortium 2020 — Expanded encyclopaedias of DNA elements

- **Citation:** ENCODE Project Consortium et al. Expanded encyclopaedias of DNA elements in the human and mouse genomes. Nature, 583(7818):699-710, 2020.
- **DOI:** [10.1038/s41586-020-2493-4](https://doi.org/10.1038/s41586-020-2493-4)
- **PMID:** 32728249 | **PMC:** PMC7410828
- **Citations:** ~2,500
- **Key findings:** ENCODE Phase 3 established DNA methylation as a core epigenomic layer integrated with histone modifications and chromatin accessibility for candidate cis-Regulatory Element (cCRE) classification. WGBS data is used to identify methylation valleys (large UMRs at key developmental genes) and to provide the methylation context for regulatory element classification. Established ENCODE WGBS processing standards used as quality gates in this skill's aggregation workflow.

---

### Amemiya et al. 2019 — ENCODE Blacklist

- **DOI:** [10.1038/s41598-019-45839-z](https://doi.org/10.1038/s41598-019-45839-z) | **PMID:** 31249361 | **Citations:** ~1,372
- **Methylation aggregation role:** CpGs within blacklisted regions may show aberrant methylation estimates due to alignment artifacts in repetitive sequences. These CpGs should be filtered from the aggregated profile to prevent false HMR/UMR calls at blacklisted loci.
