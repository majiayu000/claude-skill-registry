# ATAC-seq Pipeline — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the pipeline-atacseq skill — papers defining ENCODE ATAC-seq processing standards, the original ATAC-seq method, and the tools used at each pipeline stage.

---

## ATAC-seq Method Development

These papers establish the ATAC-seq assay and its key methodological improvements.

---

### Buenrostro et al. 2013 — Transposition of native chromatin for ATAC-seq

- **Citation:** Buenrostro JD, Giresi PG, Zaba LC, Chang HY, Greenleaf WJ. Transposition of native chromatin for fast and sensitive epigenomic profiling of open chromatin, DNA-binding proteins and nucleosome position. Nature Methods, 10(12):1213-1218, 2013.
- **DOI:** [10.1038/nmeth.2688](https://doi.org/10.1038/nmeth.2688)
- **PMID:** 24097267 | **PMC:** PMC3959825
- **Citations:** ~5,600
- **Key findings:** Original ATAC-seq method paper. Described the use of the hyperactive Tn5 transposase to simultaneously fragment DNA and insert sequencing adapters into accessible chromatin regions in a single enzymatic step. The method requires only 500-50,000 cells and a simple two-step protocol (transposition + PCR amplification), making it substantially faster and simpler than DNase-seq or FAIRE-seq. Demonstrated that ATAC-seq captures open chromatin sites, DNA-binding protein footprints, individual nucleosome positions, and chromatin compaction at nucleotide resolution. Identified classes of DNA-binding factors that strictly avoided, could tolerate, or tended to overlap with nucleosomes. The characteristic nucleosomal ladder pattern in fragment size distribution (sub-nucleosomal < 150 bp, mono-nucleosome 150-300 bp, di-nucleosome 300-500 bp) serves as a key QC metric in this pipeline.

---

### Corces et al. 2017 — Omni-ATAC: Improved ATAC-seq protocol

- **Citation:** Corces MR, Trevino AE, Hamilton EG, Greenside PG, Sinnott-Armstrong NA, Vesuna S, Satpathy AT, Rubin AJ, Montine KS, Wu B, Kathiria A, Cho SW, Mumbach MR, Carter AC, Kasowski M, Orloff LA, Risca VI, Kundaje A, Khavari PA, Montine TJ, Greenleaf WJ, Chang HY. An improved ATAC-seq protocol reduces background and enables interrogation of frozen tissues. Nature Methods, 14(10):959-962, 2017.
- **DOI:** [10.1038/nmeth.4396](https://doi.org/10.1038/nmeth.4396)
- **PMID:** 28846090 | **PMC:** PMC5623106
- **Citations:** ~1,925
- **Key findings:** Introduced the Omni-ATAC protocol with three key improvements over the original method: (1) use of digitonin-based lysis with NP-40 and Tween-20 detergents to reduce mitochondrial DNA contamination, (2) ability to process archival frozen tissue samples including 50-micron sections, and (3) substantial improvement in signal-to-background ratio. The reduced mitochondrial contamination directly decreases sequencing cost by redirecting reads to informative nuclear DNA. Omni-ATAC enabled the first chromatin accessibility maps from distinct human brain structures, revealing activities of disease-associated DNA elements. This protocol is now the basis for most ENCODE ATAC-seq experiments and informs the aggressive mitochondrial filtering in this pipeline.

---

### Grandi et al. 2022 — Chromatin accessibility profiling by ATAC-seq (Nature Protocols)

- **Citation:** Grandi F, Modi H, Kampman L, Corces MR. Chromatin accessibility profiling by ATAC-seq. Nature Protocols, 17(6):1518-1552, 2022.
- **DOI:** [10.1038/s41596-022-00692-9](https://doi.org/10.1038/s41596-022-00692-9)
- **PMID:** 35478247
- **Citations:** ~287
- **Key findings:** Comprehensive step-by-step protocol for the Omni-ATAC workflow covering sample preparation, transposition, library preparation, sequencing, and data analysis. Documents that ATAC-seq libraries for 12 samples can be generated in approximately 10 hours, with downstream computational analysis implementable using benchmarked pipelines. Provides detailed recommendations for troubleshooting common issues including high mitochondrial fraction, low library complexity, and poor TSS enrichment. Serves as the current definitive experimental protocol reference for ATAC-seq.

---

## ENCODE Pipeline Standards

---

### ENCODE Project Consortium 2020 — Expanded encyclopaedias of DNA elements

- **Citation:** ENCODE Project Consortium et al. Expanded encyclopaedias of DNA elements in the human and mouse genomes. Nature, 583(7818):699-710, 2020.
- **DOI:** [10.1038/s41586-020-2493-4](https://doi.org/10.1038/s41586-020-2493-4)
- **PMID:** 32728249 | **PMC:** PMC7410828
- **Citations:** ~2,500
- **Key findings:** ENCODE Phase 3 paper establishing the uniform processing framework for all ENCODE assays including ATAC-seq. Defined the Registry of candidate cis-Regulatory Elements (cCREs) using integrated ATAC-seq and histone ChIP-seq data. ATAC-seq is a primary input for identifying open chromatin elements in the cCRE classification system, alongside DNase-seq and H3K4me3/H3K27ac ChIP-seq. Established assembly standards (GRCh38/mm10), IDR-based replicate consistency assessment, and preferred_default file selection criteria used in this pipeline.

---

### Hitz et al. 2023 — The ENCODE Uniform Analysis Pipelines

- **Citation:** Hitz BC, Lee JW, Jolanki O, et al. The ENCODE Uniform Analysis Pipelines. Research Square (preprint), 2023.
- **DOI:** [10.21203/rs.3.rs-311127/v1](https://doi.org/10.21203/rs.3.rs-311127/v1)
- **Citations:** ~84
- **Key findings:** Documents the official ENCODE ATAC-seq pipeline specification including Bowtie2 alignment (vs BWA-MEM for ChIP-seq), Tn5 offset correction (+4/-5 bp), mitochondrial read removal, nucleosome-free fragment selection (<150 bp), MACS2 peak calling without input control, and IDR-based replicate consistency. Specifies the pipeline infrastructure using Docker containers and WDL workflow language, enabling execution on local machines, HPC clusters, or cloud environments. This paper is the authoritative reference for the pipeline architecture implemented in this skill.

---

## ATAC-seq Analysis Best Practices

---

### Yan et al. 2020 — From reads to insight: a hitchhiker's guide to ATAC-seq data analysis

- **Citation:** Yan F, Powell DR, Curtis DJ, Wong NC. From reads to insight: a hitchhiker's guide to ATAC-seq data analysis. Genome Biology, 21(1):22, 2020.
- **DOI:** [10.1186/s13059-020-1929-3](https://doi.org/10.1186/s13059-020-1929-3)
- **PMID:** 32014034 | **PMC:** PMC6996192
- **Citations:** ~328
- **Key findings:** Comprehensive review of ATAC-seq computational analysis covering pre-analysis (quality check, alignment), core analysis (peak calling), and advanced analysis (differential accessibility, motif enrichment, footprinting, nucleosome positioning). Discussed the critical importance of the Tn5 offset correction for accurate TF footprinting and the distinction between nucleosome-free region (NFR) analysis and full-fragment analysis. Highlighted that MACS2 should be run with --nomodel --shift -100 --extsize 200 for ATAC-seq (or alternatively on NFR fragments only) and that peak calling should use the --keep-dup all flag to retain all unique fragments. Reviewed the reconstruction of transcriptional regulatory networks with multi-omics data integration.

---

### Orchard et al. 2020 — ataqv: quality control for ATAC-seq data

- **Citation:** Orchard P, Kyono Y, Hensley J, Kitzman JO, Parker SCJ. Quantification, Dynamic Visualization, and Validation of Bias in ATAC-Seq Data with ataqv. Cell Systems, 10(3):298-306.e4, 2020.
- **DOI:** [10.1016/j.cels.2020.02.009](https://doi.org/10.1016/j.cels.2020.02.009)
- **PMID:** 32213349 | **PMC:** PMC7138743
- **Citations:** ~62
- **Key findings:** Introduced ataqv, a computational toolkit for ATAC-seq quality control that computes, visualizes, and compares QC metrics across samples. Analyzed 2,009 public ATAC-seq datasets revealing a 10-fold range in QC metrics. Demonstrated through Tn5 dosage experiments that technical variation in the Tn5-to-nuclei ratio and sequencing flowcell density induces systematic bias by changing enrichment of reads across functional genomic annotations including promoters, enhancers, and TF-bound regions (with CTCF as a notable exception). Established TSS enrichment as a primary quality indicator and showed that the Tn5 dosage effect is the dominant source of technical bias in ATAC-seq. ataqv is used in this pipeline's QC stage alongside deepTools and MultiQC.

---

## Core Pipeline Tools

---

### Langmead & Salzberg 2012 — Bowtie 2

- **Citation:** Langmead B, Salzberg SL. Fast gapped-read alignment with Bowtie 2. Nature Methods, 9(4):357-359, 2012.
- **DOI:** [10.1038/nmeth.1923](https://doi.org/10.1038/nmeth.1923)
- **PMID:** 22388286 | **PMC:** PMC3322381
- **Citations:** ~47,300
- **Key findings:** Introduced Bowtie 2, which combines a full-text minute index with hardware-accelerated dynamic programming for fast, sensitive, and accurate gapped alignment. Unlike BWA-MEM (used for ChIP-seq), Bowtie 2 is particularly well-suited for ATAC-seq because of its superior handling of short fragments and the very short reads produced by nucleosome-free regions. The ENCODE ATAC-seq pipeline uses Bowtie 2 with --very-sensitive mode and maximum fragment length set to accommodate the nucleosomal ladder (typically --maxins 2000). Bowtie 2 is used in this pipeline's alignment stage.

---

### Zhang et al. 2008 — MACS peak caller

- **Citation:** Zhang Y, Liu T, Meyer CA, Eeckhoute J, Johnson DS, Bernstein BE, Nusbaum C, Myers RM, Brown M, Li W, Liu XS. Model-based Analysis of ChIP-Seq (MACS). Genome Biology, 9(9):R137, 2008.
- **DOI:** [10.1186/gb-2008-9-9-r137](https://doi.org/10.1186/gb-2008-9-9-r137)
- **PMID:** 18798982 | **PMC:** PMC2592715
- **Citations:** ~7,000
- **Key findings:** MACS2 is the ENCODE-standard peak caller for both ChIP-seq and ATAC-seq. For ATAC-seq, MACS2 is run differently than for ChIP-seq: no input control is used (peaks are called against the local background model), the --nomodel flag is set because the Tn5 insertion creates a distinct fragment distribution, and the --shift and --extsize parameters are adjusted for the Tn5 offset. Peak calling is performed only on nucleosome-free fragments (<150 bp) with --call-summits for precise accessible region identification. The narrow peak mode is always used for ATAC-seq (unlike ChIP-seq which uses broad mode for some histone marks).

---

### Li et al. 2011 — IDR (Irreproducible Discovery Rate)

- **Citation:** Li Q, Brown JB, Huang H, Bickel PJ. Measuring reproducibility of high-throughput experiments. Annals of Applied Statistics, 5(3):1752-1779, 2011.
- **DOI:** [10.1214/11-AOAS466](https://doi.org/10.1214/11-AOAS466)
- **Citations:** ~1,500
- **Key findings:** IDR framework for replicate consistency assessment. In ATAC-seq, IDR is applied to MACS2 peak calls from biological replicates to produce a consensus peak set at IDR threshold 0.05. The same methodology as ChIP-seq but particularly important for ATAC-seq because the open chromatin signal is typically broader and less punctate than TF ChIP-seq peaks, making replicate concordance assessment critical for distinguishing true accessible regions from noise.

---

## Supplementary Tools (Non-ATAC-Specific)

These tools are shared with the ChIP-seq pipeline and other genomics workflows. See pipeline-chipseq/references/literature.md for detailed descriptions.

---

### Li et al. 2009 — SAMtools

- **Citation:** Li H, et al. The Sequence Alignment/Map format and SAMtools. Bioinformatics, 25(16):2078-2079, 2009.
- **DOI:** [10.1093/bioinformatics/btp352](https://doi.org/10.1093/bioinformatics/btp352)
- **PMID:** 19505943 | **Citations:** ~53,700
- **ATAC-seq role:** Used for coordinate sorting, MAPQ filtering, mitochondrial read removal (samtools view filtering chrM), fragment size filtering for NFR selection, and BAM indexing. The mitochondrial filtering step is especially critical for ATAC-seq where mitochondrial reads can constitute 30-80% of total reads.

---

### Amemiya et al. 2019 — ENCODE Blacklist

- **Citation:** Amemiya HM, Kundaje A, Boyle AP. The ENCODE Blacklist: Identification of Problematic Regions of the Genome. Scientific Reports, 9:9354, 2019.
- **DOI:** [10.1038/s41598-019-45839-z](https://doi.org/10.1038/s41598-019-45839-z)
- **PMID:** 31249361 | **Citations:** ~1,372
- **ATAC-seq role:** Blacklist v2 filtering is applied after Tn5 offset correction and before peak calling. Essential for ATAC-seq because Tn5 can insert preferentially into certain repetitive regions, creating artifact peaks that overlap blacklisted regions.

---

### Ramírez et al. 2016 — deepTools2

- **Citation:** Ramírez F, et al. deepTools2: a next generation web server for deep-sequencing data analysis. Nucleic Acids Research, 44(W1):W160-W165, 2016.
- **DOI:** [10.1093/nar/gkw257](https://doi.org/10.1093/nar/gkw257)
- **PMID:** 27079975 | **Citations:** ~6,100
- **ATAC-seq role:** Generates normalized signal tracks (bigWig), fingerprint plots, and TSS enrichment heatmaps. The TSS enrichment score (computed via computeMatrix + plotProfile at RefSeq TSS annotations) is the primary ENCODE QC metric for ATAC-seq, with assembly-dependent thresholds: >= 5 GRCh38 / >= 6 hg19 / >= 10 mm10 (ENCODE data standards).

---

### Ewels et al. 2016 — MultiQC

- **Citation:** Ewels P, Magnusson M, Lundin S, Käller M. MultiQC: summarize analysis results for multiple tools and samples in a single report. Bioinformatics, 32(19):3047-3048, 2016.
- **DOI:** [10.1093/bioinformatics/btw354](https://doi.org/10.1093/bioinformatics/btw354)
- **PMID:** 27312411 | **Citations:** ~6,800
- **ATAC-seq role:** Aggregates QC metrics from FastQC, Bowtie2, Picard, ataqv, and MACS2 into a unified HTML report for batch-level quality assessment.

---

### Broad Institute — Picard MarkDuplicates

- **Citation:** Broad Institute. Picard toolkit. GitHub, 2019.
- **URL:** [https://broadinstitute.github.io/picard/](https://broadinstitute.github.io/picard/)
- **ATAC-seq role:** PCR duplicate marking and library complexity estimation. Particularly important for ATAC-seq where low-input protocols may have higher duplication rates. NRF, PBC1, PBC2 metrics are computed from Picard output.

---

### Quinlan & Hall 2010 — BEDTools

- **Citation:** Quinlan AR, Hall IM. BEDTools: a flexible suite of utilities for comparing genomic features. Bioinformatics, 26(6):841-842, 2010.
- **DOI:** [10.1093/bioinformatics/btq033](https://doi.org/10.1093/bioinformatics/btq033)
- **PMID:** 20110278 | **Citations:** ~12,000
- **ATAC-seq role:** Used for blacklist region removal, fragment size filtering, FRiP calculation, and peak annotation with gene models.

---

### Martin 2011 — Cutadapt (basis for Trim Galore)

- **Citation:** Martin M. Cutadapt removes adapter sequences from high-throughput sequencing reads. EMBnet.journal, 17(1):10-12, 2011.
- **DOI:** [10.14806/ej.17.1.200](https://doi.org/10.14806/ej.17.1.200)
- **Citations:** ~13,000
- **ATAC-seq role:** Trim Galore (Cutadapt wrapper) performs adapter trimming. ATAC-seq libraries frequently contain adapter sequences because nucleosome-free fragments are short (< 150 bp) and paired-end reads can read through the insert into the adapter on the other end.

---

### Andrews 2010 — FastQC

- **Citation:** Andrews S. FastQC: A quality control tool for high throughput sequence data. Babraham Bioinformatics, 2010.
- **URL:** [https://www.bioinformatics.babraham.ac.uk/projects/fastqc/](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
- **ATAC-seq role:** Raw read quality assessment. Note that ATAC-seq libraries often trigger FastQC warnings for per-sequence GC content (due to Tn5 insertion bias) and sequence duplication levels (expected for low-input libraries) — these warnings are typically not concerning for ATAC-seq.
