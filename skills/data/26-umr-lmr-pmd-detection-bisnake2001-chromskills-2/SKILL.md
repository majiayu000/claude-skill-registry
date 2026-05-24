---
name: UMR-LMR-PMD-detection
description: This pipeline performs genome-wide segmentation of CpG methylation profiles to identify Unmethylated Regions (UMRs), Low-Methylated Regions (LMRs), and Partially Methylated Domains (PMDs) using whole-genome bisulfite sequencing (WGBS) methylation calls. The pipeline provides high-resolution enhancer-like LMRs, promoter-associated UMRs, and large-scale PMDs characteristic of reprogramming, aging, or cancer methylomes, enabling integration with chromatin accessibility, TF binding, and genome architecture analyses.
---

# Unmethylated Regions (UMR) & Low-Methylated Region (LMR) & Partially Methylated Domain (PMD) Detection

## 1. Overview
This pipeline performs genome-wide segmentation of CpG methylation profiles to identify Unmethylated Regions (UMRs), Low-Methylated Regions (LMRs), and Partially Methylated Domains (PMDs) using whole-genome bisulfite sequencing (WGBS) methylation calls.

Main steps include:

- Refer to the **Inputs & Outputs** section to check available inputs and design the output structure.
- **Always prompt user** for genome assembly used.  
- **Always prompt user** for which columns are methylation fraction/percent and coverage and strand.
- Convert BED → GRanges with mC/nC counts.
- Perform CpG filtering (coverage threshold).
- Call UMRs/LMRs using MethylSeekR segmentation.
- Mask UMR/LMR and detect PMDs using a 2-state HMM (optional).
- Export annotations as BED files and summary tables.

---

## 2. When to Use This Skill

### Biological questions

Use this skill when your research aims to: 
- Identify enhancer-like hypomethylated domains (LMRs). 
- Detect large-scale methylation erosion (PMDs). 
- Quantify global methylation heterogeneity. 
- Explore regulatory element accessibility from WGBS alone. 
- Integrate methylome segmentation with ATAC-seq, ChIP-seq, or chromatin states.

---

## 3. Inputs & Outputs

### Inputs

`<sample>.bed`

### Outputs

```bash
LMR_PMD_calling/
    regions/
        UMRs.bed/
        LMRs.bed/
        PMDs.bed/
```

---

## 4. Decision Tree

### Step 1: Prepare the object for detecting UMR/LMR/PMD

```r
library(MethylSeekR)
library(GenomicRanges)
bed <- read.table("sample.bed")
bed <- bed[, c(1,2,3,6,10,11)] # column index provided by user
colnames(bed) <- c("chr","start","end","percentage","coverage","strand")
bed$mC <- round(bed$beta * bed$coverage) # beta = 0.01 * percentage
bed$nC <- bed$coverage - bed$mC

gr <- GRanges(seqnames=bed$chr,
              ranges=IRanges(bed$start, bed$end),
              strand=bed$strand,
              mC=bed$mC,
              nC=bed$nC)

```

### Step 2: UMR and LMR detection

```r
library("BSgenome.Hsapiens.UCSC.hg38") # provided by user
sLengths=seqlengths(Hsapiens)
lmr_cutoff = 0.5
res <- segmentUMRsLMRs(m = gr, meth.cutoff = lmr_cutoff, seqLengths = sLengths, myGenomeSeq=Hsapiens)
UMRs <- res$UMRs
LMRs <- res$LMRs
# save UMR and LMR to the BED format files if more than zero UMRs and LMRs detected
```             

### Step 3: PMD detection

```r
pmds <- segmentPMDs(m=gr, chr.sel=unique(seqnames(gr)), 
                    seqLengths=seqlengths(gr))
```

## Notes & troubleshooting

- Install the required genome sequence or derived information with `BSgenome` package if not available

```r
# check available genomes
library(BSgenome)
available.genomes()
# install
BiocManager::install("BSgenome.Hsapiens.UCSC.hg38") # e.g. hg38
```