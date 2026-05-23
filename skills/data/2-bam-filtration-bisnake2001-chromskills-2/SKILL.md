---
name: BAM-filtration
description: Performs data cleaning and removal operations. This skill takes a raw BAM and creates a new, "clean" BAM file by actively removing artifacts: mitochondrial reads, blacklisted regions, PCR duplicates, and unmapped reads. Use this skill to "clean," "filter," or "remove bad reads" from a dataset. This is a prerequisite step before peak calling. Do NOT use this skill if you only want to view statistics without modifying the file.
---

# BAM Filtration for ChIP-seq / ATAC-seq

## Overview

Main steps include:

- Check the availability of blacklist file in current directory. **Always prompt user** whether to filter blacklist if blacklist files are missing. if the user need to filter blacklist file, then **prompt user** for the path of blacklist file.
- Initialize the project directory and create the required directory.
- Refer to the **Inputs & Outputs** section to check inputs and build the output architecture. All the output file should located in `${proj_dir}` in Step 0.
- Discover input BAMs in the current directory (or those matching a target token), and only select BAMs that are already coordinate-sorted and contain read group (RG) information.
- Perform the filtration task with tools.

---

## When to use this skill

- Use this skill to "clean," "filter," or "remove bad reads" from a dataset
- This is a prerequisite step before peak calling. 
- Do NOT use this skill if you only want to view statistics without modifying the file.

---

## Inputs & Outputs

### Inputs

```bash
${sample}.bam # BAMs that are already coordinate-sorted and contain read group (RG) information
```

### Outputs
```bash
all_bam_filtration/
  filtered_bam/
    ${sample}.filtered.bam
    ${sample}.filtered.bam.bai
  temp/
    ... # intermediate files
```

---

## Decision Tree

### Step 0: Initialize Project

Call:

- `mcp__project-init-tools__project_init`

with:

- `sample`: all
- `task`: bam_filtration

The tool will:

- Create `${sample}_bam_filtration` directory.
- Return the full path of the `${sample}_bam_filtration` directory, which will be used as `${proj_dir}`.

### Step 1: Filter BAM files

Call: 

- mcp__qc-tools__bam_artifacts

with:
- `bam_file`: BAMs that are already coordinate-sorted and contain read group (RG) information
- `output_bam`: ${proj_dir}/filtered_bam/${sample}.filtered.bam
- `temp_dir`: ${proj_dir}/temp/
- `blacklist_bed`: Path of the blacklist file
