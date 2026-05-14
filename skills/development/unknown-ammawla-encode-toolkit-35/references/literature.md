# ChIP-seq Pipeline — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the pipeline-chipseq skill — papers defining ENCODE ChIP-seq processing standards and the tools used at each pipeline stage.

---

## ENCODE Pipeline Standards

These papers define the official ENCODE consortium standards that this pipeline implements.

---

### Landt et al. 2012 — ChIP-seq guidelines and practices of the ENCODE and modENCODE consortia

- **Citation:** Landt SG, Marinov GK, Kundaje A, Kheradpour P, Pauli F, Batzoglou S, Bernstein BE, Bickel P, Brown JB, Cayting P, Chen Y, DeSalvo G, Epstein C, Fisher-Aylor KI, Euskirchen G, Gerstein M, Gertz J, Hartemink AJ, Hoffman MM, Iyer VR, Jung YL, Karmakar S, Kellis M, Kharchenko PV, Li Q, Liu T, Liu XS, Ma L, Milosavljevic A, Myers RM, Park PJ, Pazin MJ, Perry MD, Raha D, Reddy TE, Rozowsky J, Shoresh N, Sidow A, Slattery M, Stamatoyannopoulos JA, Tolstorukov MY, White KP, Xi S, Farnham PJ, Lieb JD, Wold BJ, Snyder M. ChIP-seq guidelines and practices of the ENCODE and modENCODE consortia. Genome Research, 22(9):1813-1831, 2012.
- **DOI:** [10.1101/gr.136184.111](https://doi.org/10.1101/gr.136184.111)
- **PMID:** 22955991 | **PMC:** PMC3431496
- **Citations:** ~4,000
- **Key findings:** Foundational ENCODE standards paper establishing quality metrics and experimental guidelines for ChIP-seq. Defined minimum sequencing depth requirements (20M uniquely mapped reads for TF, 45M for histone modifications), antibody validation criteria (immunoprecipitation followed by western blot, mass spectrometry, or immunofluorescence), and replicate concordance requirements (at least 2 biological replicates). Introduced the FRiP (Fraction of Reads in Peaks) metric with a minimum threshold of 1% and the cross-correlation analysis framework (NSC > 1.05, RSC > 0.8) for assessing enrichment quality. Established the traffic-light QC system where no single metric is sufficient — quality must be interpreted collectively. These standards remain the basis for all ENCODE ChIP-seq data production and are implemented directly in this pipeline's QC stage.

---

### ENCODE Project Consortium 2020 — Expanded encyclopaedias of DNA elements

- **Citation:** ENCODE Project Consortium, Moore JE, Purcaro MJ, Pratt HE, Epstein CB, Shoresh N, Adrian J, Kawli T, Davis CA, Dobin A, Kaul R, Halow J, Van Nostrand EL, Freese P, Gorkin DU, Shen Y, He Y, Mackiewicz M, Pauli-Behn F, Williams BA, Mortazavi A, Keller CA, Zhang XO, Amin SI, Hardy M, Mber F, Sandstrom R, Bernstein BE, Wold BJ, Kundaje A, Stam M, Partridge EC, Bristow CA, Gerstein M, Gingeras TR, Stamatoyannopoulos JA, Weng Z, Snyder M, Birney E, Myers RM, Hardison RC, Ren B, Cherry JM, Bernstein BE. Expanded encyclopaedias of DNA elements in the human and mouse genomes. Nature, 583(7818):699-710, 2020.
- **DOI:** [10.1038/s41586-020-2493-4](https://doi.org/10.1038/s41586-020-2493-4)
- **PMID:** 32728249 | **PMC:** PMC7410828
- **Citations:** ~2,500
- **Key findings:** Phase 3 ENCODE paper describing the expanded encyclopedia of regulatory elements. Introduced the Registry of candidate cis-Regulatory Elements (cCREs), which classified 926,535 human and 339,815 mouse cCREs into promoter-like, enhancer-like, and CTCF-only categories using integrated ChIP-seq and chromatin accessibility data. Established the uniform processing pipeline framework where all ENCODE data are processed through standardized pipelines to ensure cross-experiment comparability. Defined updated quality standards including the use of IDR (Irreproducible Discovery Rate) for replicate consistency assessment, preferred_default file selection criteria, and assembly standards (GRCh38 for human, mm10 for mouse). This paper provides the scientific basis for the pipeline's parameter choices and output format standards.

---

### Hitz et al. 2023 — The ENCODE Uniform Analysis Pipelines

- **Citation:** Hitz BC, Lee JW, Jolanki O, Kagda MS, Graham K, Sud P, Gabdank I, Strattan JS, Sloan CA, Dreszer T, Rowe LD, Podduturi NR, Malladi V, Chan ET, Davidson JM, Ho M, Miyasato S, Simison M, Tanaka F, Luo Y, Whaling I, Hong EL, Lee BT, Sandstrom R, Rynes E, Nelson J, Nishida A, Ingersoll A, Buckley M, Frerker M, Kim DS, Boley N, Trout D, Dobin A, Rahmanian S, Wyman D, Balderrama-Gutierrez G, Reese F, Durand NC, Dudchenko O, Weisz D, Rao SSP, Blackburn A, Gkountaroulis D, Sadr M, Olshansky M, Eliaz Y, Nguyen D, Bochkov ID, Shamim M, Mahajan R, Lieberman Aiden E, Gingeras TR, Heath S, Hirst M, Kent WJ, Kundaje A, Mortazavi A, Wold BJ, Cherry JM. The ENCODE Uniform Analysis Pipelines. Research Square (preprint), 2023.
- **DOI:** [10.21203/rs.3.rs-311127/v1](https://doi.org/10.21203/rs.3.rs-311127/v1)
- **Citations:** ~84
- **Key findings:** Comprehensive description of all ENCODE uniform analysis pipelines including ChIP-seq, ATAC-seq, RNA-seq, WGBS, Hi-C, and others. Documents the infrastructure for pipeline distribution using Docker containers and Workflow Description Language (WDL), enabling execution on local machines, HPC clusters, or cloud environments via Cromwell. Details the quality control metrics and thresholds applied uniformly across all ENCODE data, including library complexity metrics (NRF, PBC1, PBC2), enrichment metrics (NSC, RSC, FRiP), and reproducibility metrics (IDR). Establishes the principle that standardized computational methodologies are prerequisites for successful integrative analyses across different ENCODE collections. This paper serves as the authoritative reference for the pipeline architecture and parameter choices implemented in this skill.

---

## Core Pipeline Tools

Papers for the primary algorithms used at each pipeline stage. These tools are selected to match ENCODE uniform pipeline specifications.

---

### Zhang et al. 2008 — Model-based Analysis of ChIP-Seq (MACS)

- **Citation:** Zhang Y, Liu T, Meyer CA, Eeckhoute J, Johnson DS, Bernstein BE, Nusbaum C, Myers RM, Brown M, Li W, Liu XS. Model-based Analysis of ChIP-Seq (MACS). Genome Biology, 9(9):R137, 2008.
- **DOI:** [10.1186/gb-2008-9-9-r137](https://doi.org/10.1186/gb-2008-9-9-r137)
- **PMID:** 18798982 | **PMC:** PMC2592715
- **Citations:** ~7,000
- **Key findings:** Introduced the MACS peak-calling algorithm, which models the shift size of ChIP-seq tags empirically from the data and uses a dynamic local Poisson model to capture local biases in the genome. MACS accounts for both the DNA fragment size and the local background to improve peak detection sensitivity and specificity. The algorithm operates in two modes: narrow peak calling (default, suitable for TF and sharp histone marks like H3K4me3) with q-value cutoff of 0.05, and broad peak calling (for diffuse histone marks like H3K27me3 and H3K36me3) using --broad with a relaxed cutoff of 0.1. MACS2 remains the ENCODE-standard peak caller for ChIP-seq and is the primary peak caller in this pipeline.

---

### Li et al. 2011 — Measuring reproducibility of high-throughput experiments (IDR)

- **Citation:** Li Q, Brown JB, Huang H, Bickel PJ. Measuring reproducibility of high-throughput experiments. Annals of Applied Statistics, 5(3):1752-1779, 2011.
- **DOI:** [10.1214/11-AOAS466](https://doi.org/10.1214/11-AOAS466)
- **Citations:** ~1,500
- **Key findings:** Developed the Irreproducible Discovery Rate (IDR) framework for assessing the reproducibility of high-throughput experiments, specifically designed for peak-based genomic assays like ChIP-seq. IDR uses a copula mixture model to distinguish signal from noise by comparing ranked peak lists from biological replicates, classifying each peak as either belonging to the reproducible signal component or the irreproducible noise component. The IDR threshold of 0.05 is used by ENCODE to define the final peak set from replicated experiments. IDR is preferred over simple overlap-based approaches because it uses the quantitative ranking information (e.g., peak signal or p-value) rather than just peak presence/absence. This pipeline applies IDR analysis as the final stage before generating the consensus peak set.

---

### Li 2013 — BWA-MEM alignment algorithm

- **Citation:** Li H. Aligning sequence reads, clone sequences and assembly contigs with BWA-MEM. arXiv:1303.3997, 2013.
- **DOI:** [10.48550/arXiv.1303.3997](https://doi.org/10.48550/arXiv.1303.3997)
- **Citations:** ~11,600
- **Key findings:** Introduced BWA-MEM, an alignment algorithm for mapping sequence reads against large reference genomes. BWA-MEM automatically chooses between local and end-to-end alignments, supports paired-end reads, and performs chimeric alignment. The algorithm is robust to sequencing errors and applicable to a wide range of sequence lengths from 70bp to several megabases. For mapping 100bp sequences typical of ChIP-seq, BWA-MEM outperforms other contemporary aligners in both speed and accuracy. BWA-MEM is the ENCODE-standard aligner for ChIP-seq data and is used in this pipeline's alignment stage with default parameters plus MAPQ filtering at Q30.

---

### Li et al. 2009 — The Sequence Alignment/Map format and SAMtools

- **Citation:** Li H, Handsaker B, Wysoker A, Fennell T, Ruan J, Homer N, Marth G, Abecasis G, Durbin R; 1000 Genome Project Data Processing Subgroup. The Sequence Alignment/Map format and SAMtools. Bioinformatics, 25(16):2078-2079, 2009.
- **DOI:** [10.1093/bioinformatics/btp352](https://doi.org/10.1093/bioinformatics/btp352)
- **PMID:** 19505943 | **PMC:** PMC2723002
- **Citations:** ~53,700
- **Key findings:** Defined the SAM/BAM format specification, now the universal standard for storing read alignments against reference sequences. SAMtools provides utilities for post-processing alignments: indexing, sorting, merging, filtering by mapping quality, and extracting statistics. In the ChIP-seq pipeline, samtools is used for coordinate sorting, MAPQ-based filtering (removing reads with MAPQ < 30), removal of unmapped reads, mitochondrial read filtering, and BAM indexing. The SAM/BAM format enables interoperability between all downstream tools in the pipeline.

---

## Quality Control & Visualization

---

### Ramírez et al. 2016 — deepTools2

- **Citation:** Ramírez F, Ryan DP, Grüning B, Bhardwaj V, Kilpert F, Richter AS, Heyne S, Dündar F, Manke T. deepTools2: a next generation web server for deep-sequencing data analysis. Nucleic Acids Research, 44(W1):W160-W165, 2016.
- **DOI:** [10.1093/nar/gkw257](https://doi.org/10.1093/nar/gkw257)
- **PMID:** 27079975 | **PMC:** PMC4987876
- **Citations:** ~6,100
- **Key findings:** Comprehensive suite for processing and visualizing deep-sequencing data. Provides tools for generating normalized coverage tracks (bamCoverage for RPKM/CPM bigWig files), computing enrichment heatmaps (computeMatrix + plotHeatmap), fingerprint plots for assessing IP enrichment (plotFingerprint), and correlation analyses between replicates (multiBamSummary + plotCorrelation). In this pipeline, deepTools generates the signal tracks (bigWig files) using RPGC normalization and produces QC visualizations including fingerprint plots that distinguish well-enriched from failed ChIP experiments.

---

### Ewels et al. 2016 — MultiQC

- **Citation:** Ewels P, Magnusson M, Lundin S, Käller M. MultiQC: summarize analysis results for multiple tools and samples in a single report. Bioinformatics, 32(19):3047-3048, 2016.
- **DOI:** [10.1093/bioinformatics/btw354](https://doi.org/10.1093/bioinformatics/btw354)
- **PMID:** 27312411 | **PMC:** PMC5039924
- **Citations:** ~6,800
- **Key findings:** Tool for aggregating QC results from multiple bioinformatics tools into a single interactive HTML report. Parses output from FastQC, Picard, Samtools, MACS2, deepTools, and many other tools. Enables rapid identification of batch effects, outlier samples, and systematic quality issues across an entire project. In this pipeline, MultiQC is the final QC step that aggregates metrics from all preceding stages into a comprehensive report, providing the overview needed for the traffic-light QC assessment.

---

### Ramachandran et al. 2013 — phantompeakqualtools

- **Citation:** Kharchenko PV, Tolstorukov MY, Park PJ. Design and analysis of ChIP-seq experiments for DNA-binding proteins. Nature Biotechnology, 26(12):1351-1359, 2008. (Algorithm basis); Landt et al. 2012 (ENCODE implementation); phantompeakqualtools software by Anshul Kundaje.
- **DOI:** [10.1038/nbt.1508](https://doi.org/10.1038/nbt.1508) (Kharchenko et al.)
- **PMID:** 19029915
- **Citations:** ~2,500 (Kharchenko et al.)
- **Key findings:** phantompeakqualtools computes strand cross-correlation metrics that quantify ChIP enrichment independent of peak calling. The Normalized Strand Coefficient (NSC) measures the ratio of the cross-correlation peak to the background minimum — values > 1.05 indicate acceptable enrichment. The Relative Strand Correlation (RSC) measures the ratio of the fragment-length cross-correlation to the read-length peak — values > 0.8 indicate the ChIP signal exceeds the phantom peak artifact. These metrics were adopted by ENCODE as mandatory QC measures (Landt et al. 2012) and are computed in this pipeline's QC stage for every ChIP-seq sample.

---

## Supplementary Tools (Non-ENCODE-Specific)

These tools are widely used in genomics pipelines and are incorporated here but are not specific to the ENCODE ChIP-seq standard.

---

### Andrews 2010 — FastQC

- **Citation:** Andrews S. FastQC: A quality control tool for high throughput sequence data. Babraham Bioinformatics, 2010.
- **URL:** [https://www.bioinformatics.babraham.ac.uk/projects/fastqc/](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
- **Citations:** Widely cited (no formal publication; referenced via URL)
- **Key findings:** De facto standard tool for raw sequencing data quality assessment. Generates per-base and per-sequence quality scores, GC content distribution, sequence length distribution, adapter content detection, sequence duplication levels, and overrepresented sequence identification. FastQC's modular report format integrates directly with MultiQC for batch-level quality assessment. Used in this pipeline's first stage to assess raw FASTQ quality before trimming.

---

### Martin 2011 — Cutadapt (basis for Trim Galore)

- **Citation:** Martin M. Cutadapt removes adapter sequences from high-throughput sequencing reads. EMBnet.journal, 17(1):10-12, 2011.
- **DOI:** [10.14806/ej.17.1.200](https://doi.org/10.14806/ej.17.1.200)
- **Citations:** ~13,000
- **Key findings:** Introduced Cutadapt, an adapter trimming tool that finds and removes adapter sequences, primers, poly-A tails, and other unwanted sequences from high-throughput sequencing reads. Supports color-space data, allows multiple adapter types per read, and handles partial adapter matches. Trim Galore, used in this pipeline, is a wrapper around Cutadapt that adds automatic adapter detection and integrates quality trimming with a default Phred score cutoff of 20. Trim Galore also runs FastQC on trimmed output for post-trimming quality verification.

---

### Broad Institute — Picard MarkDuplicates

- **Citation:** Broad Institute. Picard toolkit. GitHub, 2019.
- **URL:** [https://broadinstitute.github.io/picard/](https://broadinstitute.github.io/picard/)
- **Citations:** Widely cited (no formal publication; referenced via URL)
- **Key findings:** Picard MarkDuplicates identifies and flags PCR and optical duplicate reads in aligned BAM files. Duplicates arise from PCR amplification during library preparation where multiple copies of the same template molecule are sequenced. In ChIP-seq, duplicate removal is essential because PCR duplicates inflate peak signal intensity and can create false positive peaks. Picard uses read alignment coordinates (and optionally molecular barcodes) to identify duplicates, keeping the read with the highest base quality sum. Library complexity metrics (NRF, PBC1, PBC2) are derived from Picard's duplication statistics. ENCODE recommends NRF >= 0.8, PBC1 >= 0.8, PBC2 >= 3 for acceptable library complexity.

---

### Quinlan & Hall 2010 — BEDTools

- **Citation:** Quinlan AR, Hall IM. BEDTools: a flexible suite of utilities for comparing genomic features. Bioinformatics, 26(6):841-842, 2010.
- **DOI:** [10.1093/bioinformatics/btq033](https://doi.org/10.1093/bioinformatics/btq033)
- **PMID:** 20110278 | **PMC:** PMC2832824
- **Citations:** ~12,000
- **Key findings:** Suite of utilities for genomic interval arithmetic: intersection, union, subtraction, merging, and complement operations on BED, BAM, VCF, and GFF files. In the ChIP-seq pipeline, bedtools is used for blacklist region removal (bedtools intersect -v), peak annotation (bedtools intersect with gene models), and computing the Fraction of Reads in Peaks (FRiP) metric. The tool's efficiency with large genomic datasets and streaming I/O support make it suitable for integration into automated pipeline workflows.

---

### Amemiya et al. 2019 — The ENCODE Blacklist

- **Citation:** Amemiya HM, Kundaje A, Boyle AP. The ENCODE Blacklist: Identification of Problematic Regions of the Genome. Scientific Reports, 9:9354, 2019.
- **DOI:** [10.1038/s41598-019-45839-z](https://doi.org/10.1038/s41598-019-45839-z)
- **PMID:** 31249361 | **PMC:** PMC6597582
- **Citations:** ~1,372
- **Key findings:** Defined comprehensive blacklists for human (hg19/GRCh38), mouse (mm9/mm10), worm, and fly genomes containing regions that produce anomalous, unstructured, or high signal in next-generation sequencing experiments regardless of cell type or experiment. These regions include collapsed repeats, satellite sequences, and other assembly artifacts. Removing blacklisted regions is described as an essential quality measure for all functional genomics analyses. The ENCODE blacklist v2 for GRCh38 contains 910 regions (totaling ~36 Mb). In this pipeline, blacklist filtering is applied immediately after duplicate marking and before peak calling, ensuring that artifact peaks are excluded from all downstream analyses.

---

## Additional Relevant Papers

---

### Bailey et al. 2013 — Practical Guidelines for Comprehensive ChIP-seq Analysis

- **Citation:** Bailey T, Krajewski P, Ladunga I, Lefebvre C, Li Q, Liu T, Madrigal P, Taslim C, Zhang J. Practical Guidelines for the Comprehensive Analysis of ChIP-seq Data. PLoS Computational Biology, 9(11):e1003326, 2013.
- **DOI:** [10.1371/journal.pcbi.1003326](https://doi.org/10.1371/journal.pcbi.1003326)
- **PMID:** 24244136 | **PMC:** PMC3828144
- **Citations:** ~274
- **Key findings:** Step-by-step computational guidelines complementing the ENCODE standards, covering sequencing depth selection, quality checking, mapping, data normalization, reproducibility assessment, peak calling, differential binding analysis, FDR control, peak annotation, visualization, and motif analysis. Provides a decision tree for selecting appropriate peak callers based on the type of ChIP-seq experiment (TF vs. histone) and discusses the impact of control sample selection on peak calling accuracy. Particularly useful for understanding the rationale behind the parameter choices in this pipeline.

---

### Danecek et al. 2021 — Twelve years of SAMtools and BCFtools

- **Citation:** Danecek P, Bonfield JK, Liddle J, Marshall J, Ohan V, Pollard MO, Whitwham A, Keane T, McCarthy SA, Davies RM, Li H. Twelve years of SAMtools and BCFtools. GigaScience, 10(2):giab008, 2021.
- **DOI:** [10.1093/gigascience/giab008](https://doi.org/10.1093/gigascience/giab008)
- **PMID:** 33590861 | **PMC:** PMC7931819
- **Citations:** ~9,400
- **Key findings:** Retrospective on 12 years of SAMtools development documenting major improvements including multi-threaded I/O, CRAM format support, improved variant calling, and the modular HTSlib library. Both SAMtools and BCFtools have been installed over 1 million times via Bioconda. Documents the samtools flagstat, samtools idxstats, and samtools stats utilities used in this pipeline for alignment QC metrics including mapping rate, properly paired percentage, and mitochondrial fraction calculation.
