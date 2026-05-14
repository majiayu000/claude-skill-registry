# WGBS Pipeline — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the pipeline-wgbs skill — papers defining ENCODE WGBS processing standards, bisulfite-aware alignment, methylation extraction, and quality assessment for whole-genome bisulfite sequencing.

---

## DNA Methylation Method & Standards

---

### Lister et al. 2009 — Human DNA methylomes at base resolution

- **Citation:** Lister R, Pelizzola M, Dowen RH, Hawkins RD, Hon G, Tonti-Filippini J, Nott JR, Lee L, Ye Z, Ngo QM, Edsall L, Antosiewicz-Bourget J, Stewart R, Ruotti V, Millar AH, Thomson JA, Ren B, Ecker JR. Human DNA methylomes at base resolution show widespread epigenomic differences. Nature, 462(7271):315-322, 2009.
- **DOI:** [10.1038/nature08514](https://doi.org/10.1038/nature08514)
- **PMID:** 19829295 | **PMC:** PMC2857523
- **Citations:** ~5,000
- **Key findings:** First base-resolution whole-genome DNA methylation maps for human (H1 ESCs and IMR90 fibroblasts). Demonstrated that ~25% of all methylated cytosines in embryonic stem cells are in non-CpG context (CHG, CHH), a phenomenon largely absent in differentiated cells. Identified widespread methylation differences between cell types, including large partially methylated domains (PMDs) covering ~40% of the genome in fibroblasts that correlate with gene repression and late-replicating chromatin. Established WGBS as the gold standard for comprehensive methylation profiling at single-nucleotide resolution, requiring ~30x genome coverage for reliable quantification.

---

### Schultz et al. 2015 — Human body epigenome maps

- **Citation:** Schultz MD, He Y, Whitaker JW, Hariharan M, Mukamel EA, Leung D, Rajagopal N, Nery JR, Urich MA, Chen H, Lin S, Lin Y, Jung I, Schmitt AD, Selvaraj S, Ren B, Sejnowski TJ, Wang W, Ecker JR. Human body epigenome maps reveal noncanonical DNA methylation variation. Nature, 523(7559):212-216, 2015.
- **DOI:** [10.1038/nature14248](https://doi.org/10.1038/nature14248)
- **PMID:** 26030523 | **PMC:** PMC4539777
- **Citations:** ~1,500
- **Key findings:** Generated WGBS methylomes for 18 human tissues as part of the Roadmap Epigenomics Project. Identified tissue-specific differentially methylated regions (DMRs) and described three classes of genomic methylation: highly methylated regions (HMRs, >80%), partially methylated domains (PMDs, 50-80%), and unmethylated regions (UMRs, <20%). PMDs are associated with late-replicating heterochromatin and expand during aging and in cancer. UMRs at CpG islands mark active promoters, while tissue-specific UMRs often mark active enhancers. Established the analytical framework for WGBS data interpretation used in this pipeline.

---

### ENCODE Project Consortium 2020 — Expanded encyclopaedias of DNA elements

- **Citation:** ENCODE Project Consortium et al. Expanded encyclopaedias of DNA elements in the human and mouse genomes. Nature, 583(7818):699-710, 2020.
- **DOI:** [10.1038/s41586-020-2493-4](https://doi.org/10.1038/s41586-020-2493-4)
- **PMID:** 32728249 | **PMC:** PMC7410828
- **Citations:** ~2,500
- **Key findings:** ENCODE Phase 3 paper establishing DNA methylation as a core epigenomic layer alongside histone modifications and chromatin accessibility. WGBS data is used to identify methylation valleys (large UMRs) at key developmental genes and to classify candidate cis-Regulatory Elements (cCREs) by their methylation status. Established the ENCODE WGBS pipeline standards: bisulfite conversion rate ≥98%, minimum 30x CpG coverage for reliable DMR calling, and GRCh38/mm10 as reference assemblies.

---

### Hitz et al. 2023 — The ENCODE Uniform Analysis Pipelines

- **Citation:** Hitz BC, Lee JW, Jolanki O, et al. The ENCODE Uniform Analysis Pipelines. Research Square (preprint), 2023.
- **DOI:** [10.21203/rs.3.rs-311127/v1](https://doi.org/10.21203/rs.3.rs-311127/v1)
- **Citations:** ~84
- **Key findings:** Documents the official ENCODE WGBS pipeline specification: Bismark for bisulfite-aware alignment, deduplication with Picard MarkDuplicates, MethylDackel for methylation extraction, and lambda phage spike-in for conversion rate quality control. Specifies bedMethyl as the standard output format and defines QC thresholds: bisulfite conversion ≥98%, mapping rate >70%, and sufficient CpG coverage depth for downstream DMR analysis. Pipeline infrastructure uses Docker containers and WDL for reproducible execution.

---

### Foox et al. 2021 — Performance assessment of DNA sequencing platforms

- **Citation:** Foox J, Nordlund J, Lalonde E, Lim S, Deschamps-Francoeur G, Trognitz F, Holmes M, Close MC, et al. Performance assessment of DNA sequencing platforms in the ABRF Next-Generation Sequencing Study. Nature Biotechnology, 39(9):1129-1140, 2021.
- **DOI:** [10.1038/s41587-021-01049-5](https://doi.org/10.1038/s41587-021-01049-5)
- **PMID:** 34504353
- **Citations:** ~200
- **Key findings:** Multi-site benchmarking of sequencing platforms for WGBS applications. Demonstrated that bisulfite conversion rate is the most critical QC parameter, with rates below 99% introducing thousands of false-positive methylation calls across the genome. Platform-specific biases in GC-rich regions affect CpG island coverage. Supports the ENCODE requirement for ≥98% conversion rate and provides the evidence base for this pipeline's QC thresholds.

---

## Core Pipeline Tools

---

### Krueger & Andrews 2011 — Bismark

- **Citation:** Krueger F, Andrews SR. Bismark: a flexible aligner and methylation caller for Bisulfite-Seq applications. Bioinformatics, 27(11):1571-1572, 2011.
- **DOI:** [10.1093/bioinformatics/btr167](https://doi.org/10.1093/bioinformatics/btr167)
- **PMID:** 21493656 | **PMC:** PMC3102221
- **Citations:** ~4,000
- **Key findings:** Introduced Bismark, the most widely used bisulfite-aware aligner. Bismark performs in silico C-to-T conversion of both the reference genome and sequencing reads, then aligns using Bowtie2 as the backend. After alignment, it determines the original methylation state of each cytosine by comparing the unconverted read to the reference. Handles all three cytosine contexts (CpG, CHG, CHH) and generates comprehensive methylation reports. The ENCODE pipeline uses Bismark as the default aligner for WGBS data, leveraging its --paired mode with --no_overlap to avoid double-counting methylation in overlapping paired-end reads.

---

### Pedersen et al. 2014 — bwa-meth

- **Citation:** Pedersen BS, Eyring K, De S, Yang IV, Schwartz DA. Fast and accurate alignment of long bisulfite-seq reads. arXiv:1401.1129, 2014.
- **DOI:** [10.48550/arXiv.1401.1129](https://doi.org/10.48550/arXiv.1401.1129)
- **Citations:** ~200
- **Key findings:** Introduced bwa-meth, an alternative bisulfite-aware aligner that wraps BWA-MEM for bisulfite-converted reads. Rather than creating four converted reference copies (like Bismark), bwa-meth converts only the C-to-T strand and the G-to-A strand, achieving faster alignment while maintaining accuracy. Particularly advantageous for longer reads (>100 bp) where BWA-MEM's local alignment outperforms Bowtie2's end-to-end mode. Included in this pipeline as an alternative aligner option (--aligner bwameth) for users who prefer faster processing or have long-read bisulfite data.

---

### MethylDackel — Methylation extraction from BAM files

- **Citation:** Ryan DP. MethylDackel: A (mostly) universal methylation extractor for BS-seq experiments. GitHub, 2023.
- **URL:** [https://github.com/dpryan79/MethylDackel](https://github.com/dpryan79/MethylDackel)
- **Key findings:** MethylDackel (formerly PileOMeth) extracts per-base methylation metrics from BAM files produced by any bisulfite-aware aligner. Key features used in this pipeline: --mergeContext flag to merge complementary CpG dinucleotide strands, --minDepth to filter low-coverage positions, M-bias plot generation for identifying end-repair artifacts, and --OT/--OB position-based trimming to remove biased read positions. MethylDackel outputs in bedMethyl format, the ENCODE standard for methylation data. Replaces Bismark's built-in methylation extractor with improved speed and flexibility.

---

## Quality Control

---

### Ewels et al. 2016 — MultiQC

- **Citation:** Ewels P, Magnusson M, Lundin S, Käller M. MultiQC: summarize analysis results for multiple tools and samples in a single report. Bioinformatics, 32(19):3047-3048, 2016.
- **DOI:** [10.1093/bioinformatics/btw354](https://doi.org/10.1093/bioinformatics/btw354)
- **PMID:** 27312411 | **Citations:** ~6,800
- **WGBS role:** Aggregates QC metrics from FastQC, Bismark alignment reports, Bismark deduplication reports, and MethylDackel M-bias plots into a unified HTML report. Provides batch-level assessment of bisulfite conversion rates, mapping rates, and duplication across all samples.

---

## Supplementary Tools (Non-WGBS-Specific)

See pipeline-chipseq/references/literature.md for detailed descriptions of shared tools.

---

### Li et al. 2009 — SAMtools

- **DOI:** [10.1093/bioinformatics/btp352](https://doi.org/10.1093/bioinformatics/btp352) | **PMID:** 19505943 | **Citations:** ~53,700
- **WGBS role:** BAM sorting, indexing, and filtering. Used for coordinate sorting after Bismark alignment and computing alignment statistics. Provides samtools flagstat for mapping rate assessment.

---

### Broad Institute — Picard MarkDuplicates

- **URL:** [https://broadinstitute.github.io/picard/](https://broadinstitute.github.io/picard/)
- **WGBS role:** PCR duplicate marking and removal. Critical for WGBS because PCR amplification of bisulfite-converted DNA is biased toward unmethylated molecules (which align better after conversion), making duplicates non-random. High duplication rates (>30%) indicate insufficient library complexity and can bias methylation estimates.

---

### Andrews 2010 — FastQC

- **URL:** [https://www.bioinformatics.babraham.ac.uk/projects/fastqc/](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
- **WGBS role:** Raw read quality assessment. Bisulfite-converted reads have characteristic quality profiles: reduced base diversity (most Cs converted to Ts), asymmetric per-base composition, and lower quality scores than standard WGS. These patterns are expected and not cause for concern in WGBS data.

---

### Martin 2011 — Cutadapt (basis for Trim Galore)

- **DOI:** [10.14806/ej.17.1.200](https://doi.org/10.14806/ej.17.1.200) | **Citations:** ~13,000
- **WGBS role:** Adapter trimming via Trim Galore wrapper. Particularly important for WGBS because bisulfite conversion reduces sequence complexity, making adapter contamination harder to detect. Trim Galore includes bisulfite-specific adapter detection and optional RRBS-aware trimming (--rrbs flag) for reduced representation data.

---

### Amemiya et al. 2019 — ENCODE Blacklist

- **DOI:** [10.1038/s41598-019-45839-z](https://doi.org/10.1038/s41598-019-45839-z) | **PMID:** 31249361 | **Citations:** ~1,372
- **WGBS role:** Blacklist v2 filtering removes artifact-prone regions before downstream analysis. In WGBS, blacklisted regions can show aberrant methylation estimates due to alignment artifacts in repetitive sequences. Applied after methylation calling to filter bedMethyl output.

---

## Additional Relevant Papers

---

### Hansen et al. 2012 — BSmooth: large-scale WGBS smoothing

- **Citation:** Hansen KD, Langmead B, Irizarry RA. BSmooth: from whole genome bisulfite sequencing reads to differentially methylated regions. Genome Biology, 13(10):R83, 2012.
- **DOI:** [10.1186/gb-2012-13-10-r83](https://doi.org/10.1186/gb-2012-13-10-r83)
- **PMID:** 23034175 | **PMC:** PMC3491411
- **Citations:** ~1,200
- **Key findings:** Introduced local-likelihood smoothing for WGBS data, demonstrating that single-CpG methylation estimates from WGBS are inherently noisy even at high coverage, and that smoothing across neighboring CpGs substantially improves differential methylation detection. Established the analytical framework for identifying differentially methylated regions (DMRs) from WGBS data, implemented in the bsseq R/Bioconductor package. Relevant for downstream analysis of pipeline output.

---

### Peters et al. 2015 — DMRcate: differentially methylated region analysis

- **Citation:** Peters TJ, Buckley MJ, Statham AL, Pidsley R, Samaras K, Lord RV, Clark SJ, Molloy PL. De novo identification of differentially methylated regions in the human genome. Epigenetics & Chromatin, 8:6, 2015.
- **DOI:** [10.1186/1756-8935-8-6](https://doi.org/10.1186/1756-8935-8-6)
- **PMID:** 25972926 | **PMC:** PMC4429357
- **Citations:** ~900
- **Key findings:** Introduced DMRcate, a method for de novo identification of differentially methylated regions using kernel smoothing and bump-hunting. Works with both array (450K/EPIC) and WGBS data, providing a unified framework for DMR detection. Relevant for downstream analysis of bedMethyl output from this pipeline, particularly when comparing methylation across conditions or tissues.
