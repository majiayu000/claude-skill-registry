# Accessibility Aggregation — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the accessibility-aggregation skill — papers supporting the union-based approach for aggregating ATAC-seq and DNase-seq chromatin accessibility peaks across experiments, and the comparability of these two accessibility assay platforms.

---

## ATAC-seq / DNase-seq Comparability

---

### Corces et al. 2017 — Omni-ATAC and DNase-seq comparison

- **Citation:** Corces MR, Trevino AE, Hamilton EG, Greenside PG, Sinnott-Armstrong NA, Vesuna S, Satpathy AT, Rubin AJ, Montine KS, Wu B, Kathiria A, Cho SW, Mumbach MR, Carter AC, Kasowski M, Orloff LA, Risca VI, Kundaje A, Khavari PA, Montine TJ, Greenleaf WJ, Chang HY. An improved ATAC-seq protocol reduces background and enables interrogation of frozen tissues. Nature Methods, 14(10):959-962, 2017.
- **DOI:** [10.1038/nmeth.4396](https://doi.org/10.1038/nmeth.4396)
- **PMID:** 28846090 | **PMC:** PMC5623106
- **Citations:** ~1,925
- **Key findings:** Established that ATAC-seq and DNase-seq identify largely overlapping sets of accessible chromatin regions, with ATAC-seq capturing ~75% of DNase-seq hypersensitive sites. The concordance supports combining ATAC-seq and DNase-seq peaks in union aggregation maps for comprehensive accessibility catalogs. Platform-specific differences (Tn5 insertion bias in ATAC-seq, requirement for higher cell input for DNase-seq) affect sensitivity at individual sites but not the validity of the union approach.

---

### Thurman et al. 2012 — The accessible chromatin landscape

- **Citation:** Thurman RE, Rynes E, Humbert R, et al. The accessible chromatin landscape of the human genome. Nature, 489(7414):75-82, 2012.
- **DOI:** [10.1038/nature11232](https://doi.org/10.1038/nature11232)
- **PMID:** 22955617 | **PMC:** PMC3721348
- **Citations:** ~3,000
- **Key findings:** Definitive DNase-seq accessibility atlas across 125 human cell and tissue types. Identified ~2.9 million unique DNase I hypersensitive sites covering ~40% of the genome, with individual cell types having 100,000-200,000 DHSs. Demonstrated that distal accessible sites (enhancers) are highly cell-type-specific while promoter-proximal sites are shared. This atlas provides the conceptual framework for the accessibility aggregation approach — combining sites across samples to build comprehensive tissue-level maps.

---

### Buenrostro et al. 2013 — ATAC-seq method

- **Citation:** Buenrostro JD, Giresi PG, Zaba LC, Chang HY, Greenleaf WJ. Transposition of native chromatin for fast and sensitive epigenomic profiling of open chromatin, DNA-binding proteins and nucleosome position. Nature Methods, 10(12):1213-1218, 2013.
- **DOI:** [10.1038/nmeth.2688](https://doi.org/10.1038/nmeth.2688)
- **PMID:** 24097267 | **PMC:** PMC3959825
- **Citations:** ~5,600
- **Key findings:** Original ATAC-seq method paper establishing Tn5 transposase-based chromatin accessibility profiling. ATAC-seq requires far fewer cells than DNase-seq (500-50,000 vs >100,000) and uses a simpler protocol, making it the dominant accessibility assay in modern experiments. The nucleosomal ladder pattern in ATAC-seq fragment sizes (sub-nucleosomal <150 bp, mono-nucleosome 150-300 bp) provides additional biological information not available from DNase-seq. Both assays fundamentally measure the same biology — open chromatin regions where regulatory factors bind.

---

## Peak Calling and Quality

---

### Zhao & Boyle 2021 — F-Seq2: improved peak calling for accessibility data

- **Citation:** Zhao Z, Boyle AP. F-Seq2: improving the feature density based peak caller with dynamic statistics. NAR Genomics and Bioinformatics, 3(1):lqab012, 2021.
- **DOI:** [10.1093/nargab/lqab012](https://doi.org/10.1093/nargab/lqab012)
- **PMID:** 33655203 | **PMC:** PMC7899645
- **Citations:** ~30
- **Key findings:** Introduced F-Seq2, an improved feature density peak caller for DNase-seq and ATAC-seq that provides proper test statistics (p-values) enabling IDR analysis across replicates. Unlike the original F-Seq which used kernel density estimation without statistical testing, F-Seq2 models background with a dynamic Poisson distribution and supports both narrow and broad peak modes. Provides an alternative to MACS2 (for ATAC-seq) and Hotspot2 (for DNase-seq) that works uniformly across both accessibility platforms, which is advantageous for mixed-platform aggregation.

---

### Amemiya et al. 2019 — ENCODE Blacklist

- **Citation:** Amemiya HM, Kundaje A, Boyle AP. The ENCODE Blacklist: Identification of Problematic Regions of the Genome. Scientific Reports, 9:9354, 2019.
- **DOI:** [10.1038/s41598-019-45839-z](https://doi.org/10.1038/s41598-019-45839-z)
- **PMID:** 31249361
- **Citations:** ~1,372
- **Key findings:** Blacklist v2 filtering is essential before accessibility peak aggregation. Both Tn5 (ATAC-seq) and DNase I preferentially access certain repetitive regions in the blacklist, creating artifact peaks. Without filtering, these artifacts would appear as high-confidence accessible regions in aggregated maps because they are consistently detected across experiments — but they represent technical artifacts, not genuine regulatory elements.

---

### Orchard et al. 2020 — ataqv: ATAC-seq quality control

- **Citation:** Orchard P, Kyono Y, Hensley J, Kitzman JO, Parker SCJ. Quantification, Dynamic Visualization, and Validation of Bias in ATAC-Seq Data with ataqv. Cell Systems, 10(3):298-306.e4, 2020.
- **DOI:** [10.1016/j.cels.2020.02.009](https://doi.org/10.1016/j.cels.2020.02.009)
- **PMID:** 32213349 | **PMC:** PMC7138743
- **Citations:** ~62
- **Key findings:** Identified TSS enrichment as the primary quality indicator for ATAC-seq experiments. Analysis of 2,009 public ATAC-seq datasets revealed a 10-fold range in quality metrics, establishing that quality-gating is essential before aggregation. ATAC-seq experiments with TSS enrichment <6 should be excluded from aggregation to prevent dilution of the accessibility signal with background noise.

---

## Data Integration Framework

---

### ENCODE Project Consortium 2020 — Expanded encyclopaedias of DNA elements

- **Citation:** ENCODE Project Consortium et al. Expanded encyclopaedias of DNA elements in the human and mouse genomes. Nature, 583(7818):699-710, 2020.
- **DOI:** [10.1038/s41586-020-2493-4](https://doi.org/10.1038/s41586-020-2493-4)
- **PMID:** 32728249 | **PMC:** PMC7410828
- **Citations:** ~2,500
- **Key findings:** ENCODE Phase 3 paper establishing the cCRE (candidate cis-Regulatory Element) classification system that uses integrated accessibility data. Both ATAC-seq and DNase-seq DHSs serve as core inputs for identifying cCREs, supporting the equivalence of these platforms for accessibility cataloging. The cCRE classification combines accessibility peaks with histone mark data to distinguish promoter-like, enhancer-like, and CTCF-only elements.

---

### Gorkin et al. 2020 — Atlas of chromatin landscapes in mouse development

- **Citation:** Gorkin DU, Barozzi I, Zhao Y, et al. An atlas of dynamic chromatin landscapes in mouse fetal development. Nature, 583(7818):744-751, 2020.
- **DOI:** [10.1038/s41586-020-2093-3](https://doi.org/10.1038/s41586-020-2093-3)
- **PMID:** 32728240 | **PMC:** PMC7402670
- **Citations:** ~301
- **Key findings:** Integrated accessibility data across tissues and developmental stages using union peak sets combined with histone marks for chromatin state annotation. Demonstrated that comprehensive accessibility catalogs from union merging enable discovery of tissue-specific enhancers and developmental regulatory switches. Supports the aggregation-then-annotate workflow used in this skill.

---

## Computational Tools

---

### Quinlan & Hall 2010 — BEDTools

- **Citation:** Quinlan AR, Hall IM. BEDTools: a flexible suite of utilities for comparing genomic features. Bioinformatics, 26(6):841-842, 2010.
- **DOI:** [10.1093/bioinformatics/btq033](https://doi.org/10.1093/bioinformatics/btq033)
- **PMID:** 20110278
- **Citations:** ~12,000
- **Key findings:** Core computational tool for accessibility peak aggregation. `bedtools merge` performs the union merge; `bedtools intersect -v` removes blacklisted regions; `bedtools multiIntersect` tracks which samples support each accessible region. The same BEDTools workflow is used for both ATAC-seq and DNase-seq peaks, enabling seamless cross-platform aggregation.
