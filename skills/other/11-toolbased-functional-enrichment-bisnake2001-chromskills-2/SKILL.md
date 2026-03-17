---
name: functional-enrichment
description: Perform GO and KEGG functional enrichment using HOMER from genomic regions (BED/narrowPeak/broadPeak) or gene lists, and produce R-based barplot/dotplot visualizations. Use this skill when you want to perform GO and KEGG functional enrichment using HOMER from genomic regions or just want to link genomic region to genes.

---

# Functional Enrichment (HOMER + R)

## Overview

- **Validate input**: Accept BED/peak files with genomic coordinates or gene lists; check format and genome assembly.
- **Map regions to genes**: Convert regions to a unique gene set using HOMER `annotatePeaks.pl`.
- **Run GO enrichment**: Use HOMER `findGO.pl` (or `annotatePeaks.pl -go`) for BP/MF/CC.
- **Run KEGG enrichment**: Use HOMER `findGO.pl -kegg` (or `annotatePeaks.pl -kegg`).
- **Collect outputs**: Save tidy tables for downstream plotting and a compact summary of top terms.
- **Visualize in R**: Create barplots and dotplots (GO/KEGG) with `ggplot2` from standardized outputs.
- **QC & troubleshooting**: Provide checks for genome mismatch, chromosome naming, and low-signal inputs.

## Inputs & Outputs

### Inputs (choose one):
#### Option 1: Input is a genomic region file (BED/narrowPeak/broadPeak)
Genomic region formats supported:
- **BED files**: Standard genomic interval format
- **narrowPeak**: narrow peak format
- **broadPeak**: broad peak format

#### Option 2: Input is a gene list (txt)
- `gene_list.txt` with one official gene symbol per line (no header). And an optional `gene_list_background.txt` with one official gene symbol per line (no header).

### Outputs (directory layout):
```bash
${sample}_functional_enrichment/
    results/
      ${sample}.anno_genomic_features.txt
      ${sample}.anno_genomic_features_stats.txt
      biological_process.txt
      cellular_component.txt  
      molecular_function.txt  

      kegg.txt                
      biocyc.txt              
      chromosome.txt  
      cosmic.txt
      interactions.txt  
      interpro.txt
      gene3d.txt
      pathwayInteractionDB.txt
      pfam.txt
      prints.txt    
      prosite.txt   
      reactome.txt
      smpdb.txt
      wikipathways.txt

      gwas.txt          
      lipidmaps.txt           
      msigdb.txt                
      smart.txt

    tables/
      ${sample}.gene_list.txt
      go_bp.tsv
      go_mf.tsv
      go_cc.tsv
      kegg.tsv
    logs/
      ${sample}.anno_genomic_features.log # if genome region file is provided
      findGO.log
```


## Decision Tree


### Step 0 — Gather Required Information from the User

Before calling any tool, **ask the user**:

1. Sample name (`sample`): used as prefix and for the output directory `${sample}_functional_enrichment`.
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
- Create `${sample}_functional_enrichment` directory.
- Get the full path of the `${sample}_functional_enrichment` directory, which will be used as `${proj_dir}`.

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

### Step 4 (Optional): Convert gene ID to gene symbol

This step is optional. Only perform this step if the input file is a gene list file. If the input file is a BED file, skip this step.

Call:
- `mcp__mygene-tools__convert_gene_ids_mygene`

With:
- `input_ids_file`: the user-provided gene list file. May end with `.txt`.
- `scopes`: the source ID type for mygene (e.g., 'ensembl.gene', 'symbol', 'entrezgene', 'uniprot', or a comma-separated list).
- `fields`: the comma-separated target fields to retrieve from mygene (e.g., 'symbol,ensembl.gene,uniprot,entrezgene').
- `species`: the species for mygene (e.g., 'human', 'mouse', 'zebrafish', or NCBI taxon ID like '9606').
- `out_file`: the path to save the converted gene list file. In this skill, it is the full path of the `${sample}_functional_enrichment` directory returned by `mcp__project-init-tools__project_init`
- `batch_size`: the batch size for mygene.querymany (default 1000).

The tool will:
- Convert the gene ID to gene symbol.
- Return the path of the converted gene list file.

---


### Step 5: GO enrichment analysis

#### Option 1: from genomic regions file

Only if the input file is a BED file. If the input file is a gene list, call tools in Option 2.

1. annotate the genomic regions using Homer's `annotatePeaks.pl` with `-go` option. If user also provides a background genome region file, like a control peak file, also call this tool for the background genome region file. Use a different `${sample}` as the sample name for the background sample.

Call:
`mcp__homer-tools__annotate_genomic_features`

With:
- `sample`: the user-provided sample name
- `proj_dir`: directory to save the genomic feature annotation results. In this skill, it is the full path of the `${sample}_functional_enrichment` directory returned by `mcp__project-init-tools__project_init`
- `regions_bed`: the user-provided regions file in BED format. May end with `.bed`, `.narrowPeak`, `.broadPeak`, etc.
- `genome`: the user-provided genome assembly, e.g. `hg38`, `mm10`, `danRer11`
- `ann`: "custom homer annotation file (created by assignGenomeAnnotation.pl), (default: None).
- `size_given`: keep original region sizes (default: True)
- `cpg`: include CpG information (default: False)
- `go`: `True` to perform GO enrichment analysis.

The tool will:
- Annotate the genomic regions using Homer's `annotatePeaks.pl`.
- Return the path of the annotated regions file under `${proj_dir}/results/` directory, and the path to the log file under `${proj_dir}/logs/` directory.
    - `${proj_dir}/results/${sample}.anno_genomic_features.txt`
    - `${proj_dir}/results/${sample}.anno_genomic_features_stats.txt`
    - `${proj_dir}/logs/${sample}.anno_genomic_features.log`

---

2. (optional) extract the genes from the annotated regions file if neccessary for future analysis or the target gene list is requested by user. If not requested, skip this step.

Call:
`mcp__file-format-tools__extract_gene_list`

With:
- `sample`: the user-provided sample name
- `proj_dir`: directory to save the genomic feature annotation results. In this skill, it is the full path of the `${sample}_functional_enrichment` directory returned by `mcp__project-init-tools__project_init`

The tool will:
- Extract the genes from the annotated regions file.
- Return the path of the gene list file under `${proj_dir}/tables/` directory.
    - `${proj_dir}/tables/${sample}.gene_list.txt`


---

#### Option 2: from gene list file

Only if the input file is a gene list file. If the input file is a BED file, call tools in Option 1.

Call:
`mcp__homer-tools__gene_function_enrichment`

With:
- `sample`: the user-provided sample name
- `proj_dir`: directory to save the GO & KEGG enrichment results. In this skill, it is the full path of the `${sample}_functional_enrichment` directory returned by `mcp__project-init-tools__project_init`
- `gene_list_file`: the user-provided gene list file. May end with `.txt`.
- `organism`: the user-provided organism name, e.g. `human`, `mouse`, `zebrafish`, etc.
- `background_gene_list_file`: the user-provided background gene list file. May end with `.txt`. If not provided, set this parameter to `None`.

The tool will:
- Find the GO enrichment for the gene list.
- Return the path of the GO & KEGG enrichment results under `${proj_dir}/results/` directory.
    - `${proj_dir}/results/biological_process.txt`
    - `${proj_dir}/results/kegg.txt`
    - ... other GO and KEGG enrichment results files.
- Return the path of the log file under `${proj_dir}/logs/` directory.
    - `${proj_dir}/logs/${sample}.find_go_and_kegg_enrichment.log`


---




> **Alternative direct from BED**  
> `annotatePeaks.pl peaks.bed hg38 -go results/{run}/tables/go_dir -genomeOntology`  
> `annotatePeaks.pl peaks.bed hg38 -kegg results/{run}/tables/kegg_dir`


## Notes & Best Practices

- **Genome & naming**: Ensure the HOMER genome key matches the species; chromosome naming must be consistent (`chr1` vs `1`).
- **BED format**: Tab-delimited, ≥3 columns, 0-based coordinates, no header.
- **Multiple testing**: Prefer FDR (BH) if provided; otherwise fallback to P-value.
- **Background set**: `-bg` helps reduce bias; choose a reasonable universe (e.g., all expressed or all accessible regions → genes).
- **Direct-from-BED**: `annotatePeaks.pl -go/-kegg` is convenient; the gene-list route yields uniform TSVs for plotting.

## Troubleshooting

- **Many NAs after annotation**: Check genome version, chromosome naming, BED formatting, and headers.
- **Empty/weak enrichment**: Ensure sufficient genes (suggest ≥50), verify species of symbols, tune thresholds or background.
- **Column name drift**: HOMER versions may differ; adjust R column mappings if needed.