---
name: track-generation
description: This skill generates normalized BigWig (.bw) tracks (and/or fold-change tracks) from BAM files for ATAC-seq and ChIP-seq visualization. It handles normalization (RPM or fold-change) and Tn5 offset correction automatically. Use this skill when you have filtered and generated the clean BAM file (e.g. `*.filtered.bam`).
---

## Overview

This skill converts filtered BAM files into normalized signal tracks (BigWig) for genome browser visualization.  
It supports both ATAC-seq and ChIP-seq datasets, automatically detecting genome assembly and chromosome size files.

Main steps include:
- Refer to the **Inputs & Outputs** section to check inputs and build the output architecture. All the output file should located in `${proj_dir}` in Step 0.
- Always use filtered BAM file (`*.filtered.bam`) if available.
- **Normalize all tracks** to 1 million mapped reads (RPM normalization).
- Generate the chrom.size file.  
- **For ATAC-seq**, apply Tn5 offset correction (+4/−5) and generate normalized BigWig (RPM).  
- **For ChIP-seq**, generat RPM-normalized track without applying Tn5 offset correction

---

## Decision Tree

### Step 0: Initialize Project

Call:

- `mcp__project-init-tools__project_init`

with:

- `sample`: all
- `task`: track_generation

The tool will:

- Create `${sample}_track_generation` directory.
- Return the full path of the `${sample}_track_generation` directory, which will be used as `${proj_dir}`.


### Step 1: Generate Chromosome size file

Call:
- `mcp__bw-tools__generate_chrom_sizes`
with:
- `bam_file`: Path for the BAM file for generating bigWig Tracks
- `output_path`: ${proj_dir}/temp/${sample}.chrom.sizes

### Step 2: Calculate Scaling Factor

Call:

- `mcp__bw_tools__calculate_scaling_factor`
with:
`bam_file`: Path for the BAM file for generating bigWig Tracks

This step will store result as variable ${scale_factor}

### Step 3:  Create RPM-normalized BigWig scaled to 1M mapped reads.

- (Option 1) For ATAC-seq data: Apply the standard Tn5 shift (+4/-5bp)

Call:
- `mcp__bw_tools__bam_to_bigwig`
with:
`bam_file`: ${bam_file}
`chrom_sizes`: ${proj_dir}/temp/${sample}.chrom.sizes (from Step 2)
`output_bw`: ${proj_dir}/tracks/${sample_name}.RPM.bw
`scale_factor`: ${scale_factor}
`shift_tn5`: True
`temp_dir`: ${proj_dir}/temp

- (Option 2) For ChIP-seq data: 
**Do Not Apply the standard Tn5 shift by setting `shift_tn5` as False**
