# Hi-C Pipeline — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the pipeline-hic skill — papers defining ENCODE Hi-C processing standards, chromatin conformation capture methodology, contact matrix generation, loop calling, and 3D genome organization tools.

---

## Hi-C Method Development

---

### Lieberman-Aiden et al. 2009 — Comprehensive mapping of long-range interactions

- **Citation:** Lieberman-Aiden E, van Berkum NL, Williams L, Imakaev M, Raber T, Lajoie BR, Dekker J, Bhatt DM, Nussbaum MC, Anton IM, Ahmed K, Gnirke A, Lander ES. Comprehensive mapping of long-range interactions reveals folding principles of the human genome. Science, 326(5950):289-293, 2009.
- **DOI:** [10.1126/science.1181369](https://doi.org/10.1126/science.1181369)
- **PMID:** 19815776 | **PMC:** PMC2858594
- **Citations:** ~6,000
- **Key findings:** Introduced the Hi-C method, the first technique to map genome-wide chromatin interactions in an unbiased manner. Discovered that the human genome is organized into two spatial compartments: A compartments (open, gene-rich, active chromatin) and B compartments (closed, gene-poor, inactive chromatin), visible as a plaid/checkerboard pattern in contact matrices at megabase resolution. Demonstrated that chromatin conformation is consistent with a "fractal globule" model where the genome folds without knots, enabling maximum accessibility. This foundational paper established Hi-C as the standard method for studying 3D genome organization.

---

### Rao et al. 2014 — A 3D map of the human genome at kilobase resolution

- **Citation:** Rao SSP, Huntley MH, Durand NC, Stamenova EK, Bochkov ID, Robinson JT, Sanborn AL, Machol I, Omer AD, Lander ES, Aiden EL. A 3D map of the human genome at kilobase resolution reveals principles of chromatin looping. Cell, 159(7):1665-1680, 2014.
- **DOI:** [10.1016/j.cell.2014.11.021](https://doi.org/10.1016/j.cell.2014.11.021)
- **PMID:** 25497547 | **PMC:** PMC5635824
- **Citations:** ~5,000
- **Key findings:** Generated the highest-resolution Hi-C maps to date using the in situ Hi-C protocol, which performs ligation inside intact nuclei rather than in dilute solution. Identified ~10,000 chromatin loops in human cells, the majority of which are anchored by convergent CTCF/cohesin binding sites (the "convergent rule" of loop formation). Discovered six subcompartments (A1, A2, B1, B2, B3, B4) refining the original A/B compartment classification. Introduced HiCCUPS (Hi-C Computational Unbiased Peak Search) for systematic loop detection and Arrowhead for TAD/domain annotation. This paper established the in situ Hi-C protocol and loop calling methodology used in the ENCODE pipeline.

---

## ENCODE Pipeline Standards

---

### ENCODE Project Consortium 2020 — Expanded encyclopaedias of DNA elements

- **Citation:** ENCODE Project Consortium et al. Expanded encyclopaedias of DNA elements in the human and mouse genomes. Nature, 583(7818):699-710, 2020.
- **DOI:** [10.1038/s41586-020-2493-4](https://doi.org/10.1038/s41586-020-2493-4)
- **PMID:** 32728249 | **PMC:** PMC7410828
- **Citations:** ~2,500
- **Key findings:** ENCODE Phase 3 paper establishing Hi-C as a core 3D genome assay. Hi-C contact matrices are used to identify topologically associating domains (TADs), chromatin loops, and A/B compartments that organize gene regulation. Established quality standards: cis/trans ratio >1.5, long-range cis contacts (>20kb) >40%, and sufficient depth for the target resolution. Assembly standard: GRCh38/mm10.

---

### Hitz et al. 2023 — The ENCODE Uniform Analysis Pipelines

- **Citation:** Hitz BC, Lee JW, Jolanki O, et al. The ENCODE Uniform Analysis Pipelines. Research Square (preprint), 2023.
- **DOI:** [10.21203/rs.3.rs-311127/v1](https://doi.org/10.21203/rs.3.rs-311127/v1)
- **Citations:** ~84
- **Key findings:** Documents the official ENCODE Hi-C pipeline specification: BWA-MEM for per-mate alignment, pairtools for pair classification and deduplication, Juicer tools for .hic file generation with KR normalization, cooler for .mcool generation, and HiCCUPS for loop calling. Specifies MAPQ >= 30 filtering, restriction site-aware pair classification, and multi-resolution matrix generation. Pipeline infrastructure uses Docker containers and WDL for reproducible execution.

---

### Yardimci et al. 2019 — Measuring the reproducibility and quality of Hi-C data

- **Citation:** Yardimci GG, Ozadam H, Sauria MEG, Ursu O, Yan KK, Yang T, Chakraborty A, Kaul A, Lajoie BR, Song F, Zhan Y, Ay F, Gerstein M, Kundaje A, Li Q, Taylor J, Yue F, Dekker J, Noble WS. Measuring the reproducibility and quality of Hi-C data. Genome Biology, 20:57, 2019.
- **DOI:** [10.1186/s13059-019-1658-7](https://doi.org/10.1186/s13059-019-1658-7)
- **PMID:** 30890173 | **PMC:** PMC6425651
- **Citations:** ~250
- **Key findings:** Systematic evaluation of Hi-C data quality metrics and reproducibility. Established that cis/trans ratio, long-range cis fraction, and stratum-adjusted correlation coefficient (SCC) are the most informative quality metrics. Demonstrated that loop calling requires substantially deeper sequencing than compartment or TAD analysis. Recommended minimum depths for different analyses: 10M contacts for compartments, 50M for TADs, 500M+ for loops at 5-10kb resolution. These thresholds inform the QC standards in this pipeline.

---

## Core Pipeline Tools

---

### Durand et al. 2016 — Juicer: one-click Hi-C analysis

- **Citation:** Durand NC, Shamim MS, Machol I, Rao SSP, Huntley MH, Lander ES, Aiden EL. Juicer provides a one-click system for analyzing loop-resolution Hi-C experiments. Cell Systems, 3(1):95-98, 2016.
- **DOI:** [10.1016/j.cels.2016.07.002](https://doi.org/10.1016/j.cels.2016.07.002)
- **PMID:** 27467249 | **PMC:** PMC5846465
- **Citations:** ~2,000
- **Key findings:** Introduced the Juicer pipeline and juicer_tools for Hi-C data processing. The ENCODE pipeline uses juicer_tools pre for generating .hic files from sorted pairs, with Knight-Ruiz (KR) balanced normalization as the default. Juicer_tools also provides HiCCUPS for loop calling and Arrowhead for domain annotation. The .hic format stores multi-resolution contact matrices with embedded normalization vectors, enabling interactive exploration in Juicebox.

---

### Abdennur & Mirny 2020 — Cooler: scalable storage for Hi-C data

- **Citation:** Abdennur N, Mirny LA. Cooler: scalable storage for Hi-C data and other genomically labeled arrays. Bioinformatics, 36(1):311-316, 2020.
- **DOI:** [10.1093/bioinformatics/btz540](https://doi.org/10.1093/bioinformatics/btz540)
- **PMID:** 31290943
- **Citations:** ~300
- **Key findings:** Introduced the cooler format (.cool/.mcool), an HDF5-based storage format for Hi-C contact matrices that supports arbitrary genomic resolution and out-of-core operations on matrices too large for memory. The .mcool format stores multiple resolutions in a single file. Cooler integrates with cooltools for compartment analysis, insulation score calculation, and other downstream analyses. Used in this pipeline alongside Juicer to generate .mcool files as an alternative to .hic, with broader support in the Python scientific computing ecosystem.

---

### Open2C — pairtools: pair-level Hi-C data processing

- **Citation:** Open2C, Abdennur N, Abraham S, Fudenberg G, Flyamer IM, Galitsyna AA, Goloborodko A, Imakaev M, Oksuz BA, Venev SV. Pairtools: from sequencing data to chromosome-level 3D maps. PLoS Computational Biology, 20(5):e1012164, 2024.
- **DOI:** [10.1371/journal.pcbi.1012164](https://doi.org/10.1371/journal.pcbi.1012164)
- **PMID:** 38753885
- **Citations:** ~50
- **Key findings:** Pairtools provides a suite of command-line tools for processing Hi-C read pairs: parse (classify pairs from SAM), sort, dedup (remove PCR duplicates from pairs), select (filter by pair type), and stats (generate QC statistics). The ENCODE pipeline uses pairtools parse to classify read pairs into UU (both uniquely mapped), UR (one rescued), WW (walk/same-strand artifact), and other categories, followed by pairtools dedup to remove PCR duplicates. The .pairs format output is the standard intermediate format for Hi-C data before matrix generation.

---

### Imakaev et al. 2012 — Iterative correction of Hi-C data

- **Citation:** Imakaev M, Fudenberg G, McCord RP, Naumova N, Goloborodko A, Lajoie BR, Dekker J, Mirny LA. Iterative correction of Hi-C data reveals hallmarks of chromosome organization. Nature Methods, 9(10):999-1003, 2012.
- **DOI:** [10.1038/nmeth.2148](https://doi.org/10.1038/nmeth.2148)
- **PMID:** 22941365 | **PMC:** PMC3816492
- **Citations:** ~1,500
- **Key findings:** Introduced ICE (Iterative Correction and Eigenvector decomposition), a matrix balancing algorithm for removing systematic biases in Hi-C data including GC content, mappability, and restriction fragment length. ICE is the default normalization in the cooler/cooltools ecosystem (alternative to KR normalization in Juicer). Also introduced eigenvector decomposition of the normalized contact matrix for A/B compartment identification. The pipeline supports both KR (Juicer default) and ICE (cooler default) normalization methods.

---

## Supplementary Tools (Non-Hi-C-Specific)

See pipeline-chipseq/references/literature.md for detailed descriptions of shared tools.

---

### Li & Durbin 2009 — BWA: Burrows-Wheeler Aligner

- **DOI:** [10.1093/bioinformatics/btp324](https://doi.org/10.1093/bioinformatics/btp324) | **PMID:** 19451168 | **Citations:** ~25,000
- **Hi-C role:** Per-mate alignment of Hi-C reads. Unlike standard paired-end alignment, Hi-C reads are aligned independently because mates can map to distant genomic locations (chimeric ligation products). BWA-MEM is used with -SP flags to prevent rescue of discordant pairs. MAPQ >= 30 filtering removes ambiguously mapped reads.

---

### Li et al. 2009 — SAMtools

- **DOI:** [10.1093/bioinformatics/btp352](https://doi.org/10.1093/bioinformatics/btp352) | **PMID:** 19505943 | **Citations:** ~53,700
- **Hi-C role:** BAM operations including sorting, merging, and indexing of per-mate alignments. Used before pairtools parse to prepare aligned BAM files for pair classification.

---

### Ewels et al. 2016 — MultiQC

- **DOI:** [10.1093/bioinformatics/btw354](https://doi.org/10.1093/bioinformatics/btw354) | **PMID:** 27312411 | **Citations:** ~6,800
- **Hi-C role:** Aggregates QC metrics from FastQC, BWA alignment, pairtools stats, and contact statistics into a unified HTML report. Provides batch-level assessment of pair type distributions and library quality.

---

### Amemiya et al. 2019 — ENCODE Blacklist

- **DOI:** [10.1038/s41598-019-45839-z](https://doi.org/10.1038/s41598-019-45839-z) | **PMID:** 31249361 | **Citations:** ~1,372
- **Hi-C role:** Blacklist v2 filtering removes artifact-prone genomic regions from Hi-C contact matrices. Blacklisted regions can create spurious high-contact areas in matrices due to multi-mapping artifacts, affecting loop calling and compartment analysis.

---

### Andrews 2010 — FastQC

- **URL:** [https://www.bioinformatics.babraham.ac.uk/projects/fastqc/](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
- **Hi-C role:** Raw read quality assessment. Hi-C libraries typically show broader insert size distributions than standard WGS libraries and may have elevated adapter contamination rates from short ligation products.
