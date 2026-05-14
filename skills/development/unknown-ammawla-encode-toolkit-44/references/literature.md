# Hi-C Aggregation — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the hic-aggregation skill — papers supporting the union-based approach for aggregating Hi-C chromatin loop calls across experiments, resolution-aware anchor matching, and the critical finding that loop callers produce highly discordant results.

---

## Hi-C Loop Catalogs

---

### Reyna et al. 2025 — Loop Catalog: comprehensive chromatin loop resource

- **Citation:** Reyna J, et al. Loop Catalog: a comprehensive, cell type-specific resource of chromatin loops. Nucleic Acids Research, 2025.
- **Citations:** ~20
- **Key findings:** Created the largest union catalog of chromatin loops, containing 4.19 million unique loops across 1,089 Hi-C datasets from human cell types and tissues. Used resolution-aware merging at 5kb, 10kb, and 25kb bins, matching loop anchors within one bin-width tolerance to account for resolution-dependent positional uncertainty. Demonstrated that the union approach captures both constitutive loops (shared across >50% of cell types) and cell-type-specific loops, providing the most comprehensive 3D genome map available. This catalog validates the union-based aggregation strategy used in this skill.

---

### Wolff et al. 2022 — Loop caller benchmarking

- **Citation:** Wolff J, Bhardwaj V, Nothjunge S, Richard G, Renschler G, Gilsbach R, Manke T, Backofen R, Ramírez F, Grüning BA. Galaxy HiCExplorer 3: a web server for reproducible Hi-C, capture Hi-C and single-cell Hi-C data analysis, quality control and visualization. Nucleic Acids Research, 50(W1):W697-W705, 2022.
- **DOI:** [10.1093/nar/gkac407](https://doi.org/10.1093/nar/gkac407)
- **PMID:** 35639517
- **Citations:** ~100
- **Key findings:** Benchmark showing that different Hi-C loop callers (HiCCUPS, HICCUPS2, Mustache, HiCExplorer, Fit-Hi-C2, chromosight) intersect by approximately 50% at most when applied to the same dataset. This ~50% concordance rate is the critical context for why union-based aggregation is necessary: no single caller captures all real loops, and combining calls from multiple callers and experiments provides the most complete contact map. This finding parallels the principle from histone ChIP-seq that absence of a peak does not mean absence of a binding site.

---

### Roayaei Ardakany et al. 2020 — Mustache: multi-scale loop detection

- **Citation:** Roayaei Ardakany A, Gezer HT, Lonardi S, Ay F. Mustache: multi-scale detection of chromatin loops from Hi-C and Micro-C maps using scale-space representation. Genome Biology, 21:256, 2020.
- **DOI:** [10.1186/s13059-020-02167-0](https://doi.org/10.1186/s13059-020-02167-0)
- **PMID:** 33023656 | **PMC:** PMC7537270
- **Citations:** ~165
- **Key findings:** Introduced Mustache, a multi-scale loop caller that uses scale-space theory to detect loops at multiple resolutions simultaneously. Recovers more experimentally validated loops than HiCCUPS, particularly at lower sequencing depths, because multi-scale analysis captures both sharp and diffuse contact enrichments. Relevant to aggregation because combining Mustache and HiCCUPS calls from the same dataset substantially increases the loop catalog — further supporting the union approach.

---

## Hi-C Data Processing

---

### Rao et al. 2014 — 3D map of the human genome

- **Citation:** Rao SSP, Huntley MH, Durand NC, Stamenova EK, et al. A 3D map of the human genome at kilobase resolution reveals principles of chromatin looping. Cell, 159(7):1665-1680, 2014.
- **DOI:** [10.1016/j.cell.2014.11.021](https://doi.org/10.1016/j.cell.2014.11.021)
- **PMID:** 25497547 | **PMC:** PMC5635824
- **Citations:** ~5,000
- **Key findings:** Introduced HiCCUPS (Hi-C Computational Unbiased Peak Search) for systematic loop detection, the primary loop caller used in ENCODE Hi-C experiments. Identified ~10,000 loops in GM12878 cells with convergent CTCF motifs at anchors. Loop calls from HiCCUPS are the primary input for aggregation in this skill, stored in BEDPE format.

---

### Durand et al. 2016 — Juicer tools

- **Citation:** Durand NC, Shamim MS, Machol I, et al. Juicer provides a one-click system for analyzing loop-resolution Hi-C experiments. Cell Systems, 3(1):95-98, 2016.
- **DOI:** [10.1016/j.cels.2016.07.002](https://doi.org/10.1016/j.cels.2016.07.002)
- **PMID:** 27467249 | **PMC:** PMC5846465
- **Citations:** ~2,000
- **Key findings:** Juicer pipeline and tools including HiCCUPS for loop calling and Arrowhead for TAD annotation. ENCODE Hi-C experiments are processed through Juicer, and HiCCUPS loop calls in BEDPE format are the primary input for aggregation. The .hic file format stores contact matrices at multiple resolutions enabling resolution-aware analysis.

---

## BEDPE Manipulation Tools

---

### Chakraborty et al. 2025 — AQuA Tools

- **Citation:** Chakraborty A, et al. AQuA Tools: toolkit for paired-region analysis of Hi-C and related data. 2025.
- **Key findings:** Computational toolkit for BEDPE intersection, union, and annotation, specifically designed for Hi-C loop analysis. Handles the paired-region arithmetic required for loop aggregation: two loops are considered "the same" only if both anchors overlap (not just one). Provides functions for resolution-aware anchor matching where anchor overlap is defined within one bin-width tolerance (e.g., anchors within 10kb of each other at 10kb resolution are considered matching).

---

### Flores et al. 2024 — mariner: R/Bioconductor for BEDPE operations

- **Citation:** Flores EK, et al. mariner: an R/Bioconductor package for exploring Hi-C data. Bioinformatics, 2024.
- **Key findings:** R/Bioconductor package for BEDPE manipulation including merging loops across experiments with configurable anchor tolerance. Provides functions for loop intersection, union, and annotation within the Bioconductor framework, integrating with InteractionSet and GenomicRanges. Useful for users who prefer R-based analysis of aggregated Hi-C loop catalogs.

---

## Quality Framework

---

### Yardimci et al. 2019 — Hi-C data quality and reproducibility

- **Citation:** Yardimci GG, Ozadam H, Sauria MEG, et al. Measuring the reproducibility and quality of Hi-C data. Genome Biology, 20:57, 2019.
- **DOI:** [10.1186/s13059-019-1658-7](https://doi.org/10.1186/s13059-019-1658-7)
- **PMID:** 30890173 | **PMC:** PMC6425651
- **Citations:** ~250
- **Key findings:** Established that cis/trans ratio and long-range cis fraction are the most informative quality metrics for Hi-C data. Experiments with poor quality metrics should be excluded from loop aggregation. Loop calling requires substantially deeper sequencing than compartment or TAD analysis — minimum 500M+ valid contacts for loops at 5-10kb resolution. These quality thresholds gate which experiments are included in the aggregation workflow.

---

### Amemiya et al. 2019 — ENCODE Blacklist

- **DOI:** [10.1038/s41598-019-45839-z](https://doi.org/10.1038/s41598-019-45839-z) | **PMID:** 31249361 | **Citations:** ~1,372
- **Hi-C aggregation role:** Loop anchors overlapping blacklisted regions should be filtered before aggregation because these regions produce artifactual high-contact signals due to multi-mapping reads, which can create false loops that would appear as high-confidence contacts in the aggregated catalog.
