---
name: genomic-feature-annotation
description: This skill is used to perform genomic feature annotation and visualization for any file containing genomic region information using Homer (Hypergeometric Optimization of Motif EnRichment). It annotates regions such as promoters, exons, introns, intergenic regions, and TSS proximity, and generates visual summaries of feature distributions.
---

# Genomic Feature Annotation and Visualization with Homer

## Overview

1. Prepare genomic region files in BED or other supported formats. Ensure that the input genomic regions are provided in a valid BED format (chromosome, start, end). If the file does not meet this format, extract the required columns to create a valid BED file.regions file.
2. Identify and specify the correct genome assembly for annotation.  
3. Annotate the genomic regions using Homer's `annotatePeaks.pl`.  
4. Generate annotation statistics and feature distribution summaries.  
5. Visualize annotation results (e.g., pie charts, barplots).  

---

## When to use this skill

- Find target genes of a certain TF. This skill will return an annotated peak file with the nearby genes of the TF. Genes whose promoter annotated to the TF peaks could be candidate target genes of the TF.
- Annotate the genomic regions like TF peaks, histone modification peaks, ATAC-seq peaks, etc.
- Generate annotation statistics and feature distribution summaries.
- Visualize annotation results (e.g., pie charts, barplots).


---

## Inputs & Outputs

### Inputs
Genomic region formats supported:
- **BED files**: Standard genomic interval format
- **narrowPeak**: narrow peak format
- **broadPeak**: broad peak format

### Outputs
```bash
${sample}_genomic_feature_annotation/
    results/
        ${sample}.anno_genomic_features.txt
        ${sample}.anno_genomic_features_stats.txt
    logs/
        ${sample}.anno_genomic_features.log
    plots/
        ${sample}.anno_genomic_features.pdf
```


## Decision Tree

### Step 0 — Gather Required Information from the User

Before calling any tool, **ask the user**:

1. Sample name (`sample`): used as prefix and for the output directory `${sample}_genomic_feature_annotation`.
2. Genome assembly (`genome`): e.g. `hg38`, `mm10`, `danRer11`.  
   - **Never** guess or auto-detect.

---

### Step 1: Initialize Project

1. Make director for this project:

Call:
- `mcp__project-init-tools__project_init`

with:
- `sample`: the user-provided sample name
- `task`: de_novo_motif_discovery

The tool will:
- Create `${sample}_genomic_feature_annotation` directory.
- Get the full path of the `${sample}_genomic_feature_annotation` directory, which will be used as `${proj_dir}`.

---


### Step 2: Prepare genome file for homer

Call:
- `mcp__homer-tools__check_genome_installation`

With:
- `genome`: the user-provided genome assembly, e.g. `hg38`, `mm10`, `danRer11`

The tool will:
- Check if the genome is installed in HOMER.
- If not, install the genome.


---


### Step 3 (Optional): Standardize chromosome names for BED files

This step is optional. Only perform this step if the input file is a BED file. If the input file is a gene list, skip this step.

From `1` format to `chr1` format
From `MT` format to `chrM` format

Call:
- `mcp__file-format-tools__standardize_bed_chrom_names`

with:
- `input_bed`: the user-provided BED file
- `output_bed`: the path to save the standardized BED file

The tool will:
- Standardize the chromosome names in the BED file.
- Return the path of the standardized BED file.


---


### Step 4: Genomic Feature Annotation

Call:
`mcp__homer-tools__annotate_genomic_features`

With:
- `sample`: the user-provided sample name
- `proj_dir`: directory to save the genomic feature annotation results. In this skill, it is the full path of the `${sample}_genomic_feature_annotation` directory returned by `mcp__project-init-tools__project_init`
- `regions_bed`: the user-provided regions file in BED format. May end with `.bed`, `.narrowPeak`, `.broadPeak`, etc.
- `genome`: the user-provided genome assembly, e.g. `hg38`, `mm10`, `danRer11`
- `ann`: "custom homer annotation file (created by assignGenomeAnnotation.pl), (default: None).
- `size_given`: keep original region sizes (default: True)
- `cpg`: include CpG information (default: False)

The tool will:
- Annotate the genomic regions using Homer's `annotatePeaks.pl`.
- Return the path of the annotated regions file under `${proj_dir}/results/` directory, and the path to the log file under `${proj_dir}/logs/` directory.
    - `${proj_dir}/results/${sample}.anno_genomic_features.txt`
    - `${proj_dir}/results/${sample}.anno_genomic_features_stats.txt`
    - `${proj_dir}/logs/${sample}.anno_genomic_features.log`


---


### Step 5: Visualize the annotation results

Call:
- `mcp__plot-anno-tools__visualize_annotation_results`

With:
- `sample`: the user-provided sample name
- `proj_dir`: directory to save the annotation results. In this skill, it is the full path of the `${sample}_genomic_feature_annotation` directory returned by `mcp__project-init-tools__project_init`
- `chart_type`: Type of plot: 'pie' for pie chart, 'bar' for barplot. Default: 'pie'.

The tool will:
- Visualize the annotation results.
- Return the path of the plot file under `${proj_dir}/plots/` directory, and ends with `.pdf`.

---

### Step 6. Interpretation of Results

Typical annotation categories:
- **Promoter**: -1 kb to +100 bp from TSS  
- **5' UTR**, **Exon**, **Intron**, **3' UTR**, **Intergenic**, **TTS**  

Quality indicators:
- **Annotation rate**: % of peaks successfully annotated.  
- **Promoter fraction**: Often high in TF ChIP-seq.  
- **Intergenic fraction**: Reflects enhancer-rich or noncoding regions.  


---

## Best Practices

- Use high-confidence regions (e.g., IDR-filtered peaks).  
- Ensure genome naming convention matches input files.  
- Use visualization to assess annotation patterns across datasets.  
- Save annotation parameters and plots for reproducibility.  

---

