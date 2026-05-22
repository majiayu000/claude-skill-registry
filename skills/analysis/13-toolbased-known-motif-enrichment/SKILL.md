---
name: known-motif-enrichment
description: This skill should be used when users need to perform known motif enrichment analysis on ChIP-seq, ATAC-seq, or other genomic peak files using HOMER (Hypergeometric Optimization of Motif EnRichment). It identifies enrichment of known transcription factor binding motifs from established databases in genomic regions.

---

# HOMER Known Motif Enrichment

## Overview

This skill enables comprehensive known motif enrichment analysis using HOMER tools for genomic peak files. It identifies enrichment of known transcription factor binding motifs from established databases in genomic regions.

---

## When to use this skill

Use this skill when you need to uncover the enrichment of a certain motif in the promoter regions of a set of genes, or directly from a set of genomic regions, such as peaks from ChIP-seq or ATAC-seq, with prior assumptions about which transcription factors are involved. Typical use cases include:

- Calculate the enrichment of a certain motif in the whole genome or in specific genomic regions, like promoters of a gene list or peaks from ChIP-seq or ATAC-seq.

---

## Inputs & Outputs

### Inputs

Input files should be in one of the following formats:
    - **BED files**: Standard genomic interval format
    - **narrowPeak**: narrow peak format
    - **broadPeak**: broad peak format
    - **gene list**: A list of genes provided by user or generated in previous analysis. May end with `.txt`, `.tsv`, `.csv`, etc.

### Outputs

```bash
${sample}_known_motif_enrichment/
    results/
        homerResults.html # De novo motif discovery results
        seq.autonorm.tsv # Sequence composition statistics
        motifFindingParameters.txt # Parameters used for analysis
        homerMotifs.all.motifs
        homerMotifs.motifs12
        homerMotifs.motifs10
        homerMotifs.motifs8
        nonRedundant.motifs

        homerResults/
            motif1.similar1.motif
            motif1.info.html
            motif1.logo.svg
            motif1.motif
            motif1.similar.html
            motif1.similar2.motif
            motif1.similar3.motif
            motif1.similar4.motif
            motif1RV.logo.svg
            motif1RV.motif
            # ...

    logs/ # analysis logs 
        motif.log
        # ...
```

---

## Decision Tree

### Step 0 — Gather Required Information from the User

Before calling any tool, **ask the user**:

1. Sample name (`sample`): used as prefix and for the output directory `${sample}_known_motif_enrichment`.
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
- Create `${sample}_known_motif_enrichment` directory.
- Get the full path of the `${sample}_known_motif_enrichment` directory, which will be used as `${proj_dir}`.


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


### Step 4: Locate motif file for a certain TF

If the user provides a TF name instead of a motif file, locate the motif file for the TF.

Call:
- `mcp__homer-tools__locate_motif_file`

With:
- `TF_name`: the user-provided TF name
- `motif_type`: Typically do not need to specify for model organisms. If the user provides data in "insects", "plants", "rna", "worms", "yeast", choose one as the appropriate motif type.

The tool will:
- Locate the motif file for the TF.
- Return the path of the motif file.


---


### Step 5: Calculate the enrichment of a certain motif in the genome or in specific genomic regions

Call:
- `mcp__homer-tools__find_motifs`

With:
- `sample`: the user-provided sample name
- `proj_dir`: directory to save the de novo motif discovery results. In this skill, it is the full path of the `${sample}_known_motif_enrichment` directory returned by `mcp__project-init-tools__project_init`
- `input_file`: the user-provided file containing genome regions or gene list. May end with `.bed`, `.narrowPeak`, `.broadPeak`, `.txt`, `.tsv`, `.csv`, etc.
- `genome`: the user-provided genome assembly, e.g. `hg38`, `mm10`, `danRer11`
- `size`: region size for motif finding for genome regions, typically 200-500bp for transcription factors (default: 200). If the input file is a gene list, set to None.
- `mask`: mask repeat regions for cleaner motif analysis (default: True)
- `threads`: number of processors to use (default: 4)
- `num_motifs`: number of motifs to find (default: 25)
- `lengths`: motif lengths to search (default: 8,10,12)
- `nomotif`: `True` to not use de novo motif finding
- `mknown`: motif file to use for enrichment analysis. May be the motif file returned by `mcp__homer-tools__locate_motif_file`.
- `mcheck`: motif file to check the enrichment of. May be the motif file returned by `mcp__homer-tools__locate_motif_file`.

The tool will:
- Calculate the enrichment of the motif in the genome regions in the bed file or the promoters of the genes in the gene list.
- Return the path of the known motif scan results under `${proj_dir}/results/` directory.


---


## Quality Control and Best Practices

### Important Metrics
- **p-value**: Statistical significance of motif enrichment
- **% of targets**: Percentage of input sequences containing motif
- **% of background**: Percentage of background sequences containing motif
- **Log P-value**: -log10(p-value) for visualization
- **Fold enrichment**: Ratio of target vs background motif occurrence

