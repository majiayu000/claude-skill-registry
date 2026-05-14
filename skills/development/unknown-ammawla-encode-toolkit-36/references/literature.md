# Histone Aggregation — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the histone-aggregation skill — papers supporting the union-based approach for aggregating histone ChIP-seq peaks across experiments, donors, and labs, plus per-sample noise filtering and confidence annotation.

---

## ChIP-seq Data Integration

---

### Oki et al. 2018 — ChIP-Atlas: large-scale ChIP-seq data integration

- **Citation:** Oki S, Ohta T, Shioi G, Hatanaka H, Ogasawara O, Okuda Y, Kawaji H, Nakaki R, Sese J, Meno C. ChIP-Atlas: a data-mining suite powered by full integration of public ChIP-seq data. EMBO Reports, 19(12):e46255, 2018.
- **DOI:** [10.15252/embr.201846255](https://doi.org/10.15252/embr.201846255)
- **PMID:** 30413482 | **PMC:** PMC6280649
- **Citations:** ~597
- **Key findings:** Integrated >70,000 public ChIP-seq datasets from SRA/ENCODE/Roadmap using a union approach — all peak calls are included without consensus filtering. Demonstrated that the union of peaks across experiments, labs, and antibody lots provides the most comprehensive catalog of binding sites for any given target. ChIP-Atlas provides evidence that presence in any one dataset is sufficient to catalog a binding site, supporting this skill's union-based aggregation approach.

---

### Gorkin et al. 2020 — ENCODE Phase 3 chromatin state integration

- **Citation:** Gorkin DU, Barozzi I, Zhao Y, Zhang Y, Huang H, Lee AY, Li B, Chiou J, Wildberg A, Ding B, Zhang B, Wang M, Strber JS, Afzal SY, Kim JA, Patel A, Aber N, Kim DS, Sethi A, Beez I, Sheehan AL, Beceril P, Nuber T, Verma R, Bajic I, Aylward A, Colber C, Fox R, Gao K, Shen J, Slater SE, Manber A, Hughes S, Wold BJ, Myers RM, Ren B. An atlas of dynamic chromatin landscapes in mouse fetal development. Nature, 583(7818):744-751, 2020.
- **DOI:** [10.1038/s41586-020-2093-3](https://doi.org/10.1038/s41586-020-2093-3)
- **PMID:** 32728240 | **PMC:** PMC7402670
- **Citations:** ~301
- **Key findings:** Created unified chromatin state annotations across 1,128 ENCODE ChIP-seq experiments by integrating all peak calls per histone mark per tissue. Used ChromHMM state models built from the union of histone mark signals, demonstrating that comprehensive integration captures biological complexity better than consensus approaches. Supports the aggregation workflow in this skill.

---

## Peak Quality Filtering

---

### Perna et al. 2024 — SignalValue as a cross-pipeline consistency metric

- **Citation:** Perna A, et al. Evaluating peak consistency across ChIP-seq processing pipelines. BMC Genomics, 2024.
- **Key findings:** Systematic comparison of ChIP-seq peaks called by different processing pipelines (ENCODE, nf-core, custom) on the same raw data. Found that the top 75% of peaks ranked by signalValue (narrowPeak column 7) are the most consistent across pipelines, while the bottom 25% are pipeline-specific noise. Established signalValue percentile filtering as a robust per-sample noise reduction strategy that is agnostic to the specific peak calling pipeline. This skill uses the 25th percentile signalValue threshold as the per-sample filter before union merging.

---

### Amemiya et al. 2019 — ENCODE Blacklist

- **Citation:** Amemiya HM, Kundaje A, Boyle AP. The ENCODE Blacklist: Identification of Problematic Regions of the Genome. Scientific Reports, 9:9354, 2019.
- **DOI:** [10.1038/s41598-019-45839-z](https://doi.org/10.1038/s41598-019-45839-z)
- **PMID:** 31249361
- **Citations:** ~1,372
- **Key findings:** Defined the comprehensive set of problematic genomic regions (blacklist v2) for filtering functional genomics data, including centromeres, telomeres, rDNA repeats, and satellite DNA. These regions produce artifact peaks in ChIP-seq due to multi-mapping, collapsed repeats, and reference assembly errors. Blacklist filtering is the essential first step before any peak aggregation — artifact peaks in blacklisted regions would otherwise appear as high-confidence binding sites supported by multiple experiments, when they are actually universal artifacts.

---

## Alternative Aggregation Methods

---

### Newell et al. 2020 — ChIP-R: rank-product peak combination

- **Citation:** Newell R, Pienaar R, Balderson B, Piper MD, Currie J, Essebier A, Bodén M. ChIP-R: assembling reproducible sets of ChIP-seq and ATAC-seq peaks from multiple replicates. BMC Genomics, 22:445, 2021.
- **DOI:** [10.1186/s12864-021-07739-3](https://doi.org/10.1186/s12864-021-07739-3)
- **PMID:** 34126938
- **Citations:** ~26
- **Key findings:** Introduced ChIP-R, a rank-product method for combining peaks from multiple replicates that works directly on narrowPeak files without requiring raw BAM files. ChIP-R ranks peaks by signal intensity within each replicate and uses the rank-product statistic to identify consistently enriched regions. Suitable as an alternative to the simple union merge when the user wants a more statistically principled combination method. However, for comprehensive cataloging ("is this mark ever bound here?"), the union approach is more appropriate than rank-product filtering.

---

### Jalili et al. 2021 — MSPC: multiple sample peak calling

- **Citation:** Jalili V, Matteucci M, Masseroli M, Morelli MJ. Using combined evidence from replicates to evaluate ChIP-seq peaks. Bioinformatics, 34(17):2737-2742, 2018.
- **DOI:** [10.1093/bioinformatics/bty117](https://doi.org/10.1093/bioinformatics/bty117)
- **PMID:** 29506207
- **Citations:** ~50
- **Key findings:** MSPC (Multiple Sample Peak Calling) rescues weak-but-real binding sites that stringent single-sample callers (including IDR) would discard, by exploiting the principle that a weak peak present across multiple replicates is more likely to be real than a weak peak in only one. Uses Fisher's combined probability test on p-values from individual peak callers. More sensitive than IDR-based approaches for union-based peak catalogs, particularly useful for detecting binding sites with variable enrichment across experiments.

---

### Hecht et al. 2023 — PBS: probability of being signal

- **Citation:** Hecht A, et al. Probability of Being Signal (PBS) for cross-dataset ChIP-seq comparison. PLoS Computational Biology, 2023.
- **Key findings:** Introduced the Probability-of-Being-Signal (PBS) approach for cross-dataset peak comparison when experiments have differing sequencing depths. PBS computes a posterior probability that a peak represents true signal rather than noise, accounting for depth-dependent sensitivity differences. Relevant for aggregation scenarios where ENCODE experiments from different labs have widely varying sequencing depths — PBS provides a principled way to weight peak contributions rather than treating all experiments equally.

---

## Histone Mark Biology

See `histone-marks-reference.md` (co-located in this directory) for the comprehensive chromatin biology catalog (1,442 lines, 74 references).

---

### Landt et al. 2012 — ChIP-seq quality standards

- **Citation:** Landt SG, Marinov GK, Kundaje A, Kheradpour P, Pauli F, Batzoglou S, Bernstein BE, Bickel P, Brown JB, Cayting P, Chen Y, DeSalvo G, Epstein C, Fisher-Aylor KI, Euskirchen G, Gerstein M, Gertz J, Hartemink AJ, Hoffman MM, Iyer VR, Jung YL, Karmakar S, Kellis M, Kharchenko PV, Li Q, Liu T, Liu XS, Ma L, Milosavljevic A, Myers RM, Park PJ, Pazin MJ, Perry MD, Raha D, Reddy TE, Rozowsky J, Shoresh N, Sidow A, Slattery M, Stamatoyannopoulos JA, Tolstorukov MY, White KP, Xi S, Farnham PJ, Lieb JD, Wold BJ, Snyder M. ChIP-seq guidelines and practices of the ENCODE and modENCODE consortia. Genome Research, 22(9):1813-1831, 2012.
- **DOI:** [10.1101/gr.136184.111](https://doi.org/10.1101/gr.136184.111)
- **PMID:** 22955991 | **PMC:** PMC3431496
- **Citations:** ~2,200
- **Key findings:** Established the ENCODE ChIP-seq quality standards used to gate experiments before inclusion in aggregation. Key metrics: FRiP >= 1%, NSC > 1.05, RSC > 0.8, NRF >= 0.8, and IDR replicate concordance. Experiments failing these thresholds should be excluded from aggregation. Also defined the distinction between narrow marks (point-source) and broad marks (domain) that determines the merge strategy (-d parameter) used in this skill.

---

### Quinlan & Hall 2010 — BEDTools

- **Citation:** Quinlan AR, Hall IM. BEDTools: a flexible suite of utilities for comparing genomic features. Bioinformatics, 26(6):841-842, 2010.
- **DOI:** [10.1093/bioinformatics/btq033](https://doi.org/10.1093/bioinformatics/btq033)
- **PMID:** 20110278
- **Citations:** ~12,000
- **Key findings:** The primary computational tool for peak aggregation in this skill. `bedtools merge` with `-c 4 -o count_distinct` performs the union merge while counting unique supporting samples. `bedtools intersect` with `-v` flag performs blacklist filtering. `bedtools multiIntersect` provides an alternative that tracks which specific samples support each region. BEDTools' efficient interval arithmetic enables processing of millions of peaks across dozens of experiments.
