---
name: motif-scanning
description: This skill identifies the locations of known transcription factor (TF) binding motifs within genomic regions such as ChIP-seq or ATAC-seq peaks. It utilizes HOMER to search for specific sequence motifs defined by position-specific scoring matrices (PSSMs) from known motif databases. Use this skill when you need to detect the presence and precise genomic coordinates of known TF binding motifs within experimentally defined regions such as ChIP-seq or ATAC-seq peaks.
---

# Motif Scanning

## Overview

This skill enables comprehensive motif scanning using HOMER tools for genomic peak files. It scans genomic regions for specific transcription factor binding motifs using position-specific scoring matrices and identifies exact motif locations. To perform motif scanning:

- Always refer to the **Inputs & Outputs** section to check inputs and build the output architecture.
- Genome assembly: Always returned from user feedback (hg38, mm10, hg19, mm9, etc), never determined by yourself.
- Check chromosome names: Standardize chromosome names to format with "chr" (1 -> chr1, MT -> chrM).
- Prepare motif files: Position-specific scoring matrices (PSSM) in HOMER format, saved in ${HOMER_data}/knownTFs/motifs/${tf}.motif, and "tf" should be in lower case.
- Set scanning parameters: Region size, score thresholds, output format
- Run HOMER motif scanning command

---

## When to use this skill

- Scan for potential binding sites for a certain TF in the whole genome or in specific genomic regions, like promoters of a gene list or peaks from ChIP-seq or ATAC-seq.
- Scanning ChIP-seq or ATAC-seq peaks for known motifs to validate TF binding specificity.
- Testing whether co-factor motifs (e.g., TAL1, KLF1, SPI1) co-occur within TF-bound or accessible regions to infer cooperative binding.
- Evaluating motif distribution patterns relative to genomic landmarks such as transcription start sites (TSS) or enhancers.
- Generating motif-annotated BED files for visualization in genome browsers or subsequent feature analysis.

---

## Inputs & Outputs

### Inputs
(1) Peak formats supported
- **BED files**: Standard genomic interval format
- **narrowPeak**: ENCODE narrow peak format
- **broadPeak**: ENCODE broad peak format
- **HOMER peak files**: Output from HOMER peak calling
(2) Motif formats supported
- **HOMER motif format**: Position-specific scoring matrices
- **MEME motif format**: MEME suite motif format
- **TRANSFAC format**: TRANSFAC database format


### Outputs
```bash
${sample}_known_motif_scan/
    results/
      combined_motifs.txt # combined motif hits from all TFs

      ### Option 1: Scan motif in the specific genomic regions
      ${sample}_motif_find.txt
      ${sample}_motif_find.bed

      ### Option 2: Scan motif in the genome
      ${sample}.genomewide.txt
      ${sample}.genomewide.bed

      ### Option 3: Annotate peaks with motif hits
      ${sample}.anno_motif.txt
      ${sample}.motif_pos.bed (if `mbed` is True)

    logs/ # analysis logs 
        motif_scan.log
```
---

## Decision Tree

### Step 0 — Gather Required Information from the User

Before calling any tool, **ask the user**:

1. Sample name (`sample`): used as prefix and for the output directory `${sample}_known_motif_scan`.
2. Genome assembly (`genome`): e.g. `hg38`, `mm10`, `danRer11`.  
   - **Never** guess or auto-detect.

---

### Step 1: Initialize Project

1. Make director for this project:

Call:
- `mcp__project-init-tools__project_init`

with:
- `sample`: the user-provided sample name
- `task`: known_motif_scan

The tool will:
- Create `${sample}_known_motif_scan` directory.
- Get the full path of the `${sample}_known_motif_scan` directory, which will be used as `${proj_dir}`.

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

### Step 4: Prepare motif file for a certain TF

Here are two options depending on the user's request. Pick one of them based on the user's request.
1. Locate motif file for a certain TF
2. Use a custom motif file

#### Option 1: Locate motif file for a certain TF or a set of TFs

If the user provides a TF name or a set of TF names instead of a motif file, locate the motif file for the TF.

Call:
- `mcp__homer-tools__locate_motif_file`

With:
- `proj_dir`: directory to save the known motif scan results. In this skill, it is the full path of the `${sample}_known_motif_scan` directory returned by `mcp__project-init-tools__project_init`
- `TF_name`: the user-provided TF name or a set of TF names separated by comma, e.g. `TF1,TF2,TF3`
- `motif_type`: Typically do not need to specify for model organisms. If the user provides data in "insects", "plants", "rna", "worms", "yeast", choose one as the appropriate motif type.

The tool will:
- Locate the motif file for the TF.
- Return the path of the motif file.

#### Option 2: Use a custom motif file

If the user provides a custom motif file, use the custom motif file. If the custom motif file is in MEME format, convert it to HOMER format:

Call:
- `mcp__file-format-tools__meme_to_homer`

With:
- `proj_dir`: directory to save the known motif scan results. In this skill, it is the full path of the `${sample}_known_motif_scan` directory returned by `mcp__project-init-tools__project_init`
- `meme_file`: the user-provided MEME motif file

The tool will:
- Convert the MEME motif file to HOMER motif file.
- Return the path of the HOMER motif file.

---

### Step 5: Scan motif

Here are 3 options depending on the user's request. Pick one of them based on the user's request.
1. Scan motif in the specific genomic regions
2. Scan motif in the genome
3. Annotate peaks with motif hits

#### Option 1: Scan motif in the specific genomic regions

1. If the user provides a specific genomic regions file, scan the motif in the specific genomic regions:

Call:
- `mcp__homer-tools__find_motifs`

With:
- `sample`: the user-provided sample name
- `proj_dir`: directory to save the known motif scan results. In this skill, it is the full path of the `${sample}_known_motif_scan` directory returned by `mcp__project-init-tools__project_init`
- `input_file`: the user-provided file containing genome regions. May end with `.bed`, `.narrowPeak`, `.broadPeak`, etc.
- `genome`: the user-provided genome assembly, e.g. `hg38`, `mm10`, `danRer11`
- `size`: region size for motif finding for genome regions, typically 200-500bp for transcription factors (default: 200). If the input file is a gene list, set to None.
- `mask`: mask repeat regions for cleaner motif analysis (default: True)
- `threads`: number of processors to use (default: 4)
- `num_motifs`: number of motifs to find (default: 25)
- `lengths`: motif lengths to search (default: 8,10,12)
- `find`: the path to the motif file. May be the motif file returned by `mcp__homer-tools__locate_motif_file`. This parameter must be set for this step.
- `nomotif`: `True` to not use de novo motif finding

The tool will:
- Scan for potential binding sites for a certain TF in the genome regions in the bed file or the promoters of the genes in the gene list.
- Return the path of the known motif scan results under `${proj_dir}/results/` directory:
  - `"{sample}_motif_find.txt"` (To get this, `find` parameter must be set)

2. Convert the results to BED format:

Call:
- `mcp__homer-tools__homer_pos2bed`

With:
- `pos_file`: the path to the known motif scan results. It will be under `${proj_dir}/results/` directory, and ends with `.motif.txt`.

The tool will:
- Convert the known motif scan results to BED format.
- Return the path of the converted BED file under `${proj_dir}/results/` directory:
  - `"{sample}_motif_find.bed"`


#### Option 2: Scan motif in the genome

Call:
`mcp__homer-tools__scan_motif_genome_wide`

With:
- `sample`: the user-provided sample name
- `proj_dir`: directory to save the known motif scan results. In this skill, it is the full path of the `${sample}_known_motif_scan` directory returned by `mcp__project-init-tools__project_init`
- `motif_file`: the path to the motif file. May be the motif file returned by `mcp__homer-tools__locate_motif_file`.
- `genome`: the user-provided genome assembly, e.g. `hg38`, `mm10`, `danRer11`
- `mask`: mask repeat regions for cleaner motif analysis (default: True)
- `threads`: number of processors to use (default: 4)

The tool will:
- Scan for potential binding sites for a certain TF in the genome.
- Return the path of the known motif scan results under `${proj_dir}/results/` directory:
  - `${sample}.genomewide.txt`


2. Convert the results to BED format:

Call:
- `mcp__homer-tools__homer_pos2bed`

With:
- `pos_file`: the path to the known motif scan results. It will be under `${proj_dir}/results/` directory, and ends with `.genomewide.txt`.

The tool will:
- Convert the known motif scan results to BED format.
- Return the path of the converted BED file under `${proj_dir}/results/` directory:
  - `${sample}.genomewide.bed`


#### Option 3: Annotate peaks with motif hits

1. Annotate peaks with motif hits:

Call:
`mcp__homer-tools__annotate_peaks_motif_scan`

With:
- `sample`: the user-provided sample name
- `proj_dir`: directory to save the known motif scan results. In this skill, it is the full path of the `${sample}_known_motif_scan` directory returned by `mcp__project-init-tools__project_init`
- `peakfile`: the user-provided peak file in BED format. May end with `.bed`, `.narrowPeak`, `.broadPeak`, etc.
- `genome`: the user-provided genome assembly, e.g. `hg38`, `mm10`, `danRer11`
- `motif_file`: the path to the motif file. May be the motif file returned by `mcp__homer-tools__locate_motif_file`.
- `size`: region size around peak centers (default: 200)
- `nmotifs`: number of motifs to report per peak (default: None)
- `mbed`: output motif hits in BED format (default: True). If True, a `.motif_pos.bed` file will be created under `${proj_dir}/results/` directory.
- `mscore`: include motif scores in the output (default: False)
- `cpu`: number of processors for parallel processing (default: 1)
- `bedgraph`: output in bedGraph format (default: False)
- `hist`: include histogram output with given number of bins (default: None)

The tool will:
- Annotate peaks with motif hits.
- Return the path of the known motif scan results under `${proj_dir}/results/` directory:
  - `${sample}.anno_motif.txt`
  - `${sample}.motif_pos.bed` (if `mbed` is True)




## Quality Control and Best Practices

### Pre-processing Steps
1. **Filter peaks**: Remove low-quality or artifact peaks
2. **Size selection**: Use appropriate region size (-size parameter)
3. **Motif quality**: Use high-quality position-specific scoring matrices
4. **Score thresholds**: Set appropriate motif score cutoffs

### Parameter Optimization
- **Region size**: Typically 200-500bp for transcription factors
- **Number of motifs**: Report top 1-5 motifs per peak
- **Score thresholds**: Use default or optimize based on motif quality
- **Threads**: Use available CPU cores for faster processing

### Important Metrics
- **Motif score**: Position-specific scoring matrix match score
- **Position**: Exact genomic location of motif match
- **Strand**: DNA strand where motif was found
- **Sequence**: Actual DNA sequence at motif location


## Troubleshooting

### Common Issues
1. **No motif hits found**: Check motif file format and region size
2. **Memory errors**: Reduce region size or use fewer threads
3. **Slow performance**: Use `-cpu` option for parallel processing
4. **Genome not found**: Verify genome assembly name and installation

### Error Handling
- Ensure HOMER is properly installed and configured
- Check that genome data is downloaded and accessible
- Verify input file formats and chromosome naming
- Ensure motif files are in correct format
- Check sufficient disk space for output files

