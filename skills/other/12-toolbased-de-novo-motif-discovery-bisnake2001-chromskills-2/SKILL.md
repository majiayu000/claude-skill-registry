---
name: De-novo-motif-discovery
description: This skill identifies novel transcription factor binding motifs in the promoter regions of genes, or directly from genomic regions of interest such as ChIP-seq peaks, ATAC-seq accessible sites, or differentially acessible regions. It employs HOMER (Hypergeometric Optimization of Motif Enrichment) to detect both known and previously uncharacterized sequence motifs enriched within the supplied genomic intervals. Use the skill when you need to uncover sequence motifs enriched or want to know which TFs might regulate the target regions.
---

# HOMER De Novo Motif Discovery

## Overview

This skill enables comprehensive de novo motif discovery using HOMER tools for genomic peak files. It discovers novel transcription factor binding motifs from genomic regions without requiring prior knowledge of motif patterns. To perform de novo motif discovery:

- Always refer to the **Inputs & Outputs** section to check inputs and build the output architecture.
- Genome assembly: Always returned from user feedback (hg38, mm10, hg19, mm9, etc), never determined by yourself.
- Check chromosome names: Standardize chromosome names to format with "chr" (1 -> chr1, MT -> chrM).
- Set analysis parameters: Region size, number of motifs, motif lengths
- Run HOMER de novo motif discovery command

---

## When to use this skill

Use this skill when you need to uncover sequence motifs enriched in the promoter regions of a set of genes, or directly from a set of genomic regions, such as peaks from ChIP-seq or ATAC-seq, without prior assumptions about which transcription factors are involved. Typical use cases include:

- Performing motif enrichment analysis in promoters of a gene list provided by user or generated in previous analysis to infer potential transcription factors that might regulate the target genes.
- Performing motif enrichment analysis in TF-binding sites or differential TF-binding regions provided by user or generated in previous analysis to infer potential transcription factors that might be co-factors of the target TFs.
- Performing motif enrichment analysis on ATAC-seq peaks or differential accessible regions provided by user or generated in previous analysis to infer potential transcriptional regulators of accessible chromatin regions.
- Exploring novel sequence patterns for the binding motif of a specific TF.

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
${sample}_de_novo_motif_discovery/
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
```

---

## Decision Tree

### Step 0 — Gather Required Information from the User

Before calling any tool, **ask the user**:

1. Sample name (`sample`): used as prefix and for the output directory `${sample}_de_novo_motif_discovery`.
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
- Create `${sample}_de_novo_motif_discovery` directory.
- Get the full path of the `${sample}_de_novo_motif_discovery` directory, which will be used as `${proj_dir}`.

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

### Step 4: De Novo Motif Discovery

Here are three options for different situations. Pick one of them based on the user's request.

1. De novo + known motifs
2. De novo + known motifs + background
3. De novo only

### Option 1: De novo + known motifs

Call:
- `mcp__homer-tools__find_motifs`

With:
- `sample`: the user-provided sample name
- `proj_dir`: directory to save the de novo motif discovery results. In this skill, it is the full path of the `${sample}_de_novo_motif_discovery` directory returned by `mcp__project-init-tools__project_init`
- `input_file`: the user-provided file containing genome regions or gene list. May end with `.bed`, `.narrowPeak`, `.broadPeak`, `.txt`, `.tsv`, `.csv`, etc.
- `genome`: the user-provided genome assembly, e.g. `hg38`, `mm10`, `danRer11`
- `size`: region size for motif finding for genome regions (default: 200). If the input file is a gene list, set to None.
- `mask`: mask repeat regions (default: True)
- `threads`: number of processors to use (default: 4)
- `num_motifs`: number of motifs to find (default: 25)
- `lengths`: motif lengths to search (default: 8,10,12)

The tool will:
- Discover motifs in the genome regions in the bed file or the promoters of the genes in the gene list. The motifs could be known motifs or de novo motifs.
- Return the path of the de novo motif discovery results under `${proj_dir}/results/` directory.

---

### Option 2: De novo + known motifs + background

Call:
- `mcp__homer-tools__find_motifs`

With:
- `sample`: the user-provided sample name
- `proj_dir`: directory to save the de novo motif discovery results. In this skill, it is the full path of the `${sample}_de_novo_motif_discovery` directory returned by `mcp__project-init-tools__project_init`
- `input_file`: the user-provided file containing genome regions or gene list. May end with `.bed`, `.narrowPeak`, `.broadPeak`, `.txt`, `.tsv`, `.csv`, etc.
- `genome`: the user-provided genome assembly, e.g. `hg38`, `mm10`, `danRer11`
- `background_file`: the user-provided file containing background genome regions or gene list. May end with `.bed`, `.narrowPeak`, `.broadPeak`, `.txt`, `.tsv`, `.csv`, etc.
- `size`: region size for motif finding for genome regions (default: 200). If the input file is a gene list, set to None.
- `mask`: mask repeat regions (default: True)
- `threads`: number of processors to use (default: 4)
- `num_motifs`: number of motifs to find (default: 25)
- `lengths`: motif lengths to search (default: 8,10,12)

The tool will:
- Discover motifs in the genome regions in the bed file or the promoters of the genes in the gene list with background genome regions or gene list provided. The motifs could be known motifs or de novo motifs.
- Return the path of the de novo motif discovery results under `${proj_dir}/results/` directory.

---

### Option 3: De novo only

Call:
- `mcp__homer-tools__find_motifs`

With:
- `sample`: the user-provided sample name
- `proj_dir`: directory to save the de novo motif discovery results. In this skill, it is the full path of the `${sample}_de_novo_motif_discovery` directory returned by `mcp__project-init-tools__project_init`
- `input_file`: the user-provided file containing genome regions or gene list. May end with `.bed`, `.narrowPeak`, `.broadPeak`, `.txt`, `.tsv`, `.csv`, etc.
- `genome`: the user-provided genome assembly, e.g. `hg38`, `mm10`, `danRer11`
- `size`: region size for motif finding for genome regions (default: 200). If the input file is a gene list, set to None.
- `mask`: mask repeat regions (default: True)
- `threads`: number of processors to use (default: 4)
- `num_motifs`: number of motifs to find (default: 25)
- `lengths`: motif lengths to search (default: 8,10,12)
- `noknown`: `True` to not use known motifs

The tool will:
- Discover motifs in the genome regions in the bed file or the promoters of the genes in the gene list without searching for known motif enrichment.
- Return the path of the de novo motif discovery results under `${proj_dir}/results/` directory.

---

Here are additional parameters for calling `mcp__homer-tools__find_motifs` tool, which are not commonly used. Add these parameters only when necessary:

- `cpg`: Enrich for CpG islands (default: False)
- `chopify`: Chop sequences into smaller fragments (default: False)
- `norevopp`: Don't search reverse complement (default: False)
- `rna`: For RNA motif finding (default: False)
- `bits`: Set information content threshold (default: None)

---

## Quality Control and Best Practices

### Pre-processing Steps
1. **Filter peaks**: Remove low-quality or artifact peaks
2. **Size selection**: Use appropriate region size (-size parameter)
3. **Background selection**: Choose appropriate background for enrichment analysis
4. **Repeat masking**: Use `-mask` for cleaner motif discovery

### Parameter Optimization
- **Region size**: Typically 200-500bp for transcription factors
- **Motif length**: 8-12bp for most transcription factors
- **Number of motifs**: 10-25 for initial discovery
- **Threads**: Use available CPU cores for faster processing

## Troubleshooting

### Common Issues
1. **Memory errors**: Reduce region size or number of motifs
2. **Slow performance**: Use `-p` option for parallel processing
3. **No motifs found**: Check input file format and region size
4. **Genome not found**: Verify genome assembly name and installation

### Error Handling
- Ensure HOMER is properly installed and configured
- Check that genome data is downloaded and accessible
- Verify input file formats and chromosome naming
- Ensure sufficient disk space for output files

