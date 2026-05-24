---
name: atac-footprinting
description: This skill performs transcription factor (TF) footprint analysis using TOBIAS on ATAC-seq data. It corrects Tn5 sequence bias, quantifies TF occupancy at motif sites, generates footprint scores, and optionally compares differential TF binding across conditions.
---

# ATAC-seq Footprint Analysis using TOBIAS

## 1. Overview
This skill performs TF footprint detection and optional differential TF binding analysis using TOBIAS. It identifies true TF occupancy by modeling depletion of Tn5 insertions at motif cores.

Main steps include:
- Refer to the **Inputs & Outputs** section to check required inputs and set up the output directory structure. 
- **Always prompt user** for genome assembly used.
- **Always prompt user** if other required files are missing.
- Tn5 bias correction with ATACorrect.
- Motif scanning.
- Footprint scoring.
- Binding detection with BINDetect.
- Aggregate footprint visualization.

---

## 2. When to use this skill

Use this skill when you need to identify transcription factor occupancy using ATAC-seq data. It is suitable for:

- Mapping TF binding events without ChIP-seq.
- Comparing TF footprint strength between conditions or cell types.
- Identifying which TFs gain or lose binding activity during differentiation or perturbation.
- Supporting integrative regulatory analyses with RNA-seq, ChIP-seq, or chromatin conformation data.

Recommended data requirements:

- Biological replicates are preferred (≥2 per condition).
- ≥30M paired-end ATAC-seq reads per sample.
- Properly aligned, duplicate-removed BAM files.
- High-quality peak calls for constraining motif scanning.

---

## 3. Inputs & Outputs

### Inputs
Required:
- ATAC-seq BAM + BAI
- Peak files (BED / narrowPeak)
- Genome FASTA + FAI
- Motif PWMs (*.jaspar)

Optional:
- Motif site BED
  - If not provided, TOBIAS will scan motifs.
- Metadata sheet
  - Only required for differential footprinting.

### Outputs
```bash
ATAC_footprint_analysis/
    01_ATACorrect/
      <sample>_corrected.bw       # bias-corrected insertion signal
      <sample>_bias_model.txt     # Tn5 bias report
      <sample>_correction.log     # logs
    02_TFBScan/
      motifs.bed                  # motif genomic coordinates
      scan.log
    03_ScoreBigwig/
      <sample>_ftprints.bw          # footprint score bigWig
      score.log
    04_BINDetect/
        <TF>_sites.bed          # bound/unbound calls per TF
        motif_activity.txt          # differential TF activity (if applicable)
        bindetect.log
    05_PlotAggregate/
        <TF>_aggregate.pdf          # aggregate footprint plots
        aggregate.log
    logs/ # all logs
    temp/ # intermediate files
```

## 4. Decision Tree

### Step 1: Validate inputs
User must confirm missing files.

### Step 2: Tn5 Bias correction

Call:
- mcp__tobias-tools__run_atacorrect

with:

- `bam`: Path to input ATAC-seq BAM file
- `peaks`: Path to peak BED / narrowPeak file restricting insertion sites
- `genome`: HOMER genome identifier, e.g. 'hg38', 'mm10'
- `outdir`: Output directory for ATACorrect results (e.g. 01_ATACorrect)
- `prefix`: Prefix / sample name used for output files

### Step 3: Motif scanning

Call:
- mcp__tobias-tools__run_tfbscan

with:

- `motifs`: Path to motif PWM file or directory (e.g. JASPAR *.jaspar)
- `genome`: HOMER genome identifier, e.g. 'hg38', 'mm10'
- `regions_bed`: BED file defining regions to scan (typically ATAC peaks)
- `outdir`: Output directory for TFBScan results (e.g. 02_TFBScan)
- `prefix`: Prefix / sample name used for output files

### Step 4: Footprint scoring

Call:
- mcp__tobias-tools__run_scorebigwig

with:

- `signal_bw`: Bias-corrected signal bigWig (e.g. from Step 2)
- `regions_bed`: Motif regions BED file (e.g. from Step 3)
- `output_bw`: Output bigWig path for footprint scores
- `cores`: Number of CPU cores to use

### Step 5: Binding detection

Call:
- mcp__tobias-tools__run_bindetect

with:

- `signals`: List of footprint bigWig files
- `peaks_bed`: BED file of peaks (or merged peaks for multi-condition analysis)
- `motifs`: Path to motif PWM file or directory (e.g. JASPAR *.jaspar)
- `genome`: HOMER genome identifier, e.g. 'hg38', 'mm10'
- `outdir`: Output directory for BINDetect results (e.g. 04_BINDetect)
- `conditions`: Optional list of condition labels matching the order of `signals`


### Step 6: Aggregate plots

Call:
- mcp__tobias-tools__run_plotaggregate

with:

- `signals`: List of bigWig signal files to plot (e.g. corrected ATAC signal)
- `tfbs_bed`: BED file of TF binding sites (e.g. from BINDetect, <TF>_sites.bed)
- `motifs`: Path to motif PWM file or directory (e.g. JASPAR *.jaspar)
- `flank`: Number of bp flanking the motif to include in the aggregate plot
- `output_pdf`: Output PDF file path for the aggregate footprint plot

## Advanced Usage

- Merged peaks for condition-wide scanning
- Flank window can be adjusted for large or small motifs.
- Draw footprints plot for each motif if multiple motifs are provided.