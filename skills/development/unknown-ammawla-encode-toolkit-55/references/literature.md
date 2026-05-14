# RNA-seq Pipeline — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the pipeline-rnaseq skill — papers defining ENCODE RNA-seq processing standards, splice-aware alignment, transcript quantification, and quality assessment tools.

---

## ENCODE Pipeline Standards

---

### ENCODE Project Consortium 2020 — Expanded encyclopaedias of DNA elements

- **Citation:** ENCODE Project Consortium et al. Expanded encyclopaedias of DNA elements in the human and mouse genomes. Nature, 583(7818):699-710, 2020.
- **DOI:** [10.1038/s41586-020-2493-4](https://doi.org/10.1038/s41586-020-2493-4)
- **PMID:** 32728249 | **PMC:** PMC7410828
- **Citations:** ~2,500
- **Key findings:** ENCODE Phase 3 paper establishing RNA-seq as a core assay for the encyclopedia. RNA-seq quantification provides the expression data used to classify candidate cis-Regulatory Elements (cCREs) and annotate gene activity across cell types. Established uniform processing standards: stranded library protocol (dUTP), STAR 2-pass alignment, RSEM quantification, minimum 30M uniquely mapped reads per replicate, and GENCODE annotation as the reference gene model. Assembly standards: GRCh38/mm10.

---

### Hitz et al. 2023 — The ENCODE Uniform Analysis Pipelines

- **Citation:** Hitz BC, Lee JW, Jolanki O, et al. The ENCODE Uniform Analysis Pipelines. Research Square (preprint), 2023.
- **DOI:** [10.21203/rs.3.rs-311127/v1](https://doi.org/10.21203/rs.3.rs-311127/v1)
- **Citations:** ~84
- **Key findings:** Documents the official ENCODE RNA-seq pipeline specification: STAR 2-pass mode for splice-aware alignment, RSEM for gene/transcript quantification, strand-specific signal track generation, and comprehensive QC with RSeQC. Pipeline infrastructure uses Docker containers and WDL for reproducible execution on local machines, HPC clusters, or cloud environments.

---

### Conesa et al. 2016 — A survey of best practices for RNA-seq data analysis

- **Citation:** Conesa A, Madrigal P, Tarazona S, Gomez-Cabrero D, Cervera A, McPherson A, Szczesniak MW, Gaffney DJ, Elo LL, Zhang X, Mortazavi A. A survey of best practices for RNA-seq data analysis. Genome Biology, 17:13, 2016.
- **DOI:** [10.1186/s13059-016-0881-8](https://doi.org/10.1186/s13059-016-0881-8)
- **PMID:** 26813401 | **PMC:** PMC4728800
- **Citations:** ~4,500
- **Key findings:** Comprehensive best-practices review covering experimental design, quality control, alignment, quantification, normalization, differential expression, alternative splicing, functional analysis, and visualization. Recommended minimum sequencing depth of 10-30M reads for differential expression and >60M for transcript discovery. Established that RSEM with STAR alignment provides the most accurate quantification for multi-mapped reads through expectation-maximization. Defined key QC metrics: mapping rate >80%, rRNA contamination <10%, replicate Pearson correlation >= 0.9, and 3'/5' coverage bias assessment. This paper provides the scientific basis for many parameter choices in the ENCODE RNA-seq pipeline.

---

## Core Pipeline Tools

---

### Dobin et al. 2013 — STAR: ultrafast universal RNA-seq aligner

- **Citation:** Dobin A, Davis CA, Schlesinger F, Drenkow J, Zaleski C, Jha S, Batut P, Chaisson M, Gingeras TR. STAR: ultrafast universal RNA-seq aligner. Bioinformatics, 29(1):15-21, 2013.
- **DOI:** [10.1093/bioinformatics/bts635](https://doi.org/10.1093/bioinformatics/bts635)
- **PMID:** 23104886 | **PMC:** PMC3530905
- **Citations:** ~12,700
- **Key findings:** Introduced the STAR (Spliced Transcripts Alignment to a Reference) aligner, developed specifically for the ENCODE Transcriptome project to align >80 billion reads. STAR uses sequential maximum mappable seed search in uncompressed suffix arrays followed by seed clustering and stitching. Outperforms other aligners by >50x in mapping speed (550M 2x76bp paired-end reads per hour on 12 cores) while improving alignment sensitivity and precision. Supports de novo detection of canonical and non-canonical splice junctions, chimeric transcripts, and full-length RNA sequences. The ENCODE pipeline uses STAR in 2-pass mode: first pass discovers novel splice junctions, second pass uses the full junction database for improved alignment. Experimentally validated 1,960 novel intergenic splice junctions with 80-90% success rate.

---

### Li & Dewey 2011 — RSEM: accurate transcript quantification

- **Citation:** Li B, Dewey CN. RSEM: accurate transcript quantification from RNA-Seq data with or without a reference genome. BMC Bioinformatics, 12:323, 2011.
- **DOI:** [10.1186/1471-2105-12-323](https://doi.org/10.1186/1471-2105-12-323)
- **PMID:** 21816040 | **PMC:** PMC3163565
- **Citations:** ~18,600
- **Key findings:** Introduced RSEM (RNA-Seq by Expectation-Maximization), which uses a generative model and EM algorithm to handle multi-mapped reads for accurate gene and isoform quantification. RSEM outputs expected counts, TPM (Transcripts Per Million), and FPKM (Fragments Per Kilobase of transcript per Million mapped reads) along with 95% credibility intervals. Unlike simple counting methods (e.g., featureCounts), RSEM probabilistically assigns ambiguously mapped reads to their most likely transcripts of origin based on the overall expression landscape. Benchmarks showed RSEM slightly outperforms other quantification pipelines (Teng et al. 2016). The ENCODE pipeline uses RSEM with STAR's transcriptome BAM output for gene and transcript quantification.

---

### Bray et al. 2016 — Kallisto: near-optimal RNA-seq quantification

- **Citation:** Bray NL, Pimentel H, Melsted P, Pachter L. Near-optimal probabilistic RNA-seq quantification. Nature Biotechnology, 34(5):525-527, 2016.
- **DOI:** [10.1038/nbt.3519](https://doi.org/10.1038/nbt.3519)
- **PMID:** 27043002
- **Citations:** ~4,000
- **Key findings:** Introduced Kallisto, which uses pseudoalignment to a de Bruijn graph built from a transcriptome reference to quantify transcript abundances without full read alignment. Kallisto processes 30M reads in minutes (vs hours for alignment-based methods) while maintaining accuracy comparable to or better than alignment-based quantification. The ENCODE pipeline includes Kallisto as an optional fast pseudoalignment step that operates directly on FASTQ files without requiring genome alignment, providing an independent quantification for cross-validation with RSEM results.

---

## Quality Control

---

### Wang et al. 2012 — RSeQC: quality control of RNA-seq experiments

- **Citation:** Wang L, Wang S, Li W. RSeQC: quality control of RNA-seq experiments. Bioinformatics, 28(16):2184-2185, 2012.
- **DOI:** [10.1093/bioinformatics/bts356](https://doi.org/10.1093/bioinformatics/bts356)
- **PMID:** 22743226
- **Citations:** ~2,300
- **Key findings:** Comprehensive RNA-seq QC package evaluating sequence quality, GC bias, PCR bias, nucleotide composition bias, sequencing depth saturation, strand specificity, coverage uniformity, and read distribution over genome structure (exonic, intronic, intergenic). Key modules used in this pipeline: infer_experiment.py (strand specificity detection), read_distribution.py (exonic/intronic/intergenic classification), geneBody_coverage.py (3'/5' bias assessment), junction_saturation.py (splice junction discovery saturation), and inner_distance.py (fragment size estimation). RSeQC is the primary RNA-seq-specific QC tool in the ENCODE pipeline.

---

### Ewels et al. 2016 — MultiQC

- **Citation:** Ewels P, Magnusson M, Lundin S, Käller M. MultiQC: summarize analysis results for multiple tools and samples in a single report. Bioinformatics, 32(19):3047-3048, 2016.
- **DOI:** [10.1093/bioinformatics/btw354](https://doi.org/10.1093/bioinformatics/btw354)
- **PMID:** 27312411 | **Citations:** ~6,800
- **RNA-seq role:** Aggregates QC metrics from FastQC, STAR, RSEM, RSeQC, and Picard into a unified HTML report for batch-level assessment of RNA-seq experiments.

---

## Gene Annotation

---

### Frankish et al. 2021 — GENCODE 2021

- **Citation:** Frankish A, Diekhans M, Jungreis I, Lagarde J, Loveland JE, Mudge JM, Sisu C, Wright JC, Armstrong J, Barnes I, Berry A, Bignell A, Boix C, Carbonell Sala S, Cunningham F, Di Domenico T, Donaldson S, Fiddes IT, Garcia Giron C, Gonzalez JM, Grego T, Hardy M, Hourlier T, Howe KL, Hunt T, Izuogu OG, Johnson R, Martin FJ, Martinez L, Mohanan S, Muir P, Navarro FCP, Parker A, Pei B, Pozo F, Riera FC, Ruffier M, Schmitt BM, Stapleton E, Suner MM, Sycheva I, Uszczynska-Ratajczak B, Wolf MY, Xu J, Yang YT, Yates A, Zerbino D, Zhang Y, Choudhary JS, Gerstein M, Guigo R, Hubbard TJP, Kellis M, Paten B, Tress ML, Flicek P. GENCODE 2021. Nucleic Acids Research, 49(D1):D916-D923, 2021.
- **DOI:** [10.1093/nar/gkaa1087](https://doi.org/10.1093/nar/gkaa1087)
- **PMID:** 33270111 | **PMC:** PMC7778937
- **Citations:** ~2,500
- **Key findings:** GENCODE provides the comprehensive gene annotation used as the reference for RNA-seq quantification in ENCODE pipelines. Version 41 (GRCh38.p13) annotates 62,764 genes (20,090 protein-coding) and 248,396 transcripts. GENCODE annotations are distinguished from RefSeq by their inclusion of more alternative transcripts, non-coding RNA species, and pseudogenes. The ENCODE pipeline requires GENCODE GTF files for both STAR genome index generation and RSEM reference preparation, ensuring consistent annotation across all quantification steps.

---

## Supplementary Tools (Non-RNA-seq-Specific)

See pipeline-chipseq/references/literature.md for detailed descriptions of shared tools.

---

### Li et al. 2009 — SAMtools

- **DOI:** [10.1093/bioinformatics/btp352](https://doi.org/10.1093/bioinformatics/btp352) | **PMID:** 19505943 | **Citations:** ~53,700
- **RNA-seq role:** BAM sorting, indexing, and alignment statistics. Used for computing mapping rate and rRNA fraction.

---

### Broad Institute — Picard MarkDuplicates

- **URL:** [https://broadinstitute.github.io/picard/](https://broadinstitute.github.io/picard/)
- **RNA-seq role:** PCR duplicate marking. Note: duplicate removal is less critical for RNA-seq than for ChIP-seq because PCR duplicates in expression data do not create false peaks. ENCODE retains duplicates for quantification but marks them for QC statistics.

---

### Andrews 2010 — FastQC

- **URL:** [https://www.bioinformatics.babraham.ac.uk/projects/fastqc/](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
- **RNA-seq role:** Raw read quality assessment. RNA-seq libraries may show characteristic GC bias from highly expressed transcripts and sequence duplication from abundant mRNAs — these are expected and not concerning.

---

### Martin 2011 — Cutadapt (basis for Trim Galore)

- **DOI:** [10.14806/ej.17.1.200](https://doi.org/10.14806/ej.17.1.200) | **Citations:** ~13,000
- **RNA-seq role:** Adapter trimming with Phred quality cutoff of 20. Less critical for RNA-seq than for ATAC-seq since RNA-seq fragments are typically longer than read length, but still recommended for best alignment quality.

---

### Teng et al. 2016 — A benchmark for RNA-seq quantification pipelines

- **Citation:** Teng M, Love MI, Davis CA, Djebali S, Dobin A, Graveley BR, Li S, Mason CE, Olson S, Pervouchine D, Sloan CA, Wei X, Zhan L, Irizarry RA. A benchmark for RNA-seq quantification pipelines. Genome Biology, 17:74, 2016.
- **DOI:** [10.1186/s13059-016-0940-1](https://doi.org/10.1186/s13059-016-0940-1)
- **PMID:** 27107712 | **PMC:** PMC4842274
- **Citations:** ~162
- **Key findings:** Benchmark of seven RNA-seq quantification pipelines using two independent datasets. Found that performance was generally poor across methods, with RSEM slightly outperforming the rest. Established metrics for evaluating quantification accuracy including specificity (proportion of truly non-expressed genes called as non-expressed) and sensitivity (correlation between estimated and true expression). Supports the ENCODE choice of RSEM as the primary quantification tool.
