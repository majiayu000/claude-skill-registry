---
name: nested-TAD-detection
description: This skill detects hierarchical (nested) TAD structures from Hi-C contact maps (in .cool or mcool format) using OnTAD, starting from multi-resolution .mcool files. It extracts a user-specified chromosome and resolution, converts the data to a dense matrix, runs OnTAD, and organizes TAD calls and logs for downstream 3D genome analysis.
---

# Nested TAD Detection from .mcool Using OnTAD

## Overview

This skill performs nested TAD (hierarchical TAD/subTAD) detection from Hi-C data using **OnTAD**, starting from a .mcool, .cool or .hic file.

Main steps include:

- Refer to the **Inputs & Outputs** section to verify required files and output structure.
- Inspect the `.mcool` file to list available resolutions and alway remember to confirm the chromosome name and analysis resolution with the user.
- Extract a **balanced or raw dense Hi-C matrix** for a selected chromosome and resolution from the `.mcool` file.
- Ensure matrix quality (symmetry, no all-zero rows/columns, reasonable contact decay).
- Run **OnTAD** to call TADs and nested TAD structures.
- Parse and standardize OnTAD output into BED-like tables and hierarchical annotation files.

---

## When to use this skill

Use this skill when you want to **identify TADs and nested sub-TADs** from high- or mid-resolution Hi-C data, especially when your contact maps are stored as **Cooler multi-resolution files (.mcool)** and you need **chromosome- and resolution-specific** OnTAD calls.

Typical biological questions / use-cases:

- Comparing **TAD hierarchy** between cell types (e.g., GM12878 vs K562) or conditions (control vs treated).
- Investigating whether **inner subTADs** are enriched for active regulatory elements, specific histone marks, or gene expression.
- Studying **boundary usage**, **boundary sharing**, or **hierarchical TAD levels** around key loci (e.g., HOX clusters, oncogenes).
- Integrating nested TAD structure with **ChIP-seq**, **ATAC-seq**, or **WGBS** to understand spatial regulatory architecture.

Data quality & replication assumptions:

- Hi-C experiments should have **sufficient depth** for the target resolution (e.g., ≥5–10 kb typically requires deep sequencing).
- Preferably, use **biological replicates** per condition and call TADs on either:
  - individual replicate matrices (and then merge/consensus), or  
  - replicate-merged matrices (if justified).
- The `.mcool` should be **properly normalized or at least QC’d** (ICE/balanced weights available if using `--balanced`).

---

## Inputs & Outputs

### Inputs

Required core inputs:

- **Hi-C matrix file**
  - Multi-resolution Cooler file (`.mcool`), e.g.:
    - `sample.mcool`
  - Or one-resolution Cooler file (`.cool`), e.g.:
    - `sample.cool`
  - Or Hi-C file (`.hic`), e.g.:
    - `sample.hic`
- **User-supplied parameters (must come from user feedback)**
  - Chromosome name: e.g., `chr1`, `chr2`, `chrX`
  - Resolution of interest: e.g., `10000`, `25000`, `40000` (in bp)
  - Chromosome length: e.g., 133275309
- **Software and environment**
  - `cooler` command-line utilities (or Python `cooler` module) available in `$PATH` or environment.
  - `OnTAD` installed and callable (e.g., `OnTAD` or `OnTAD_linux` command).
  - `python` (3.x) and basic scientific Python stack if using Python-based extraction.

Optional entry point:

- **Precomputed dense Hi-C matrix (OnTAD-ready)**
  - Plain text dense square matrix (no header), e.g. `proj_dir/matrices/chr17_25kb_dense.matrix`.  
  - If this is already present, you may **skip the `.mcool` → dense matrix conversion** and jump directly to OnTAD.

Operational rules for missing inputs:

- If `.mcool` or `.cool` or `.hic` file is missing:  
  `"sample.mcool not available, provide required files or skip and proceed ?"`
- If chromosome list not specified:  
  Ask the user explicitly rather than assuming default.
- If OnTAD executable is not found:  
  Ask user to install/locate OnTAD before proceeding.

---

### Outputs

Default output directory structure:

```bash
${sample}_nested_TAD_detection/
    matrices/
        ${chromosome}_${resolution}_dense.txt
        ${chromosome}_${resolution}_dense.log
    nested_TADs/
        ${chromosome}_${resolution}_OnTAD.tad
        ${chromosome}_${resolution}_OnTAD.bed
        ${chromosome}_${resolution}_OnTAD.log
```

---


## Allowed Tools

When using this skill, you should restrict yourself to the following MCP tools from server `cooler-tools`, `cooltools-tools`, `plot-hic-tools`, `project-init-tools`:
- `mcp__project-init-tools__project_init`
- `mcp__cooler-tools__list_mcool_resolutions`
- `mcp__cooler-tools__harmonize_chrom_names`
- `mcp__cooler-tools__dump_chroms`
- `mcp__cooler-tools__dump_dense_matrix`
- `mcp__OnTAD-tools__run_ontad`


Do NOT fall back to:

- raw shell commands (`OnTAD`, etc.)
- ad-hoc Python snippets (e.g. importing `cooler`, `bioframe`, `matplotlib` manually in the reply).

---


## Decision Tree

### Step 0 — Gather Required Information from the User

Before calling any tool, ask the user:

1. Sample name (`sample`): used as prefix and for the output directory `${sample}_nested_TAD_detection`.

2. Genome assembly (`genome`): e.g. `hg38`, `mm10`, `danRer11`.  
   - **Never** guess or auto-detect.

3. Hi-C matrix path/URI (`mcool_uri`):
   - `path/to/sample.mcool::/resolutions/25000` (.mcool file with resolution specified)
   - or `.cool` file path
   - or `.hic` file path

4. Resolution (`resolution`): default `25000` (100 kb).  
   - If user does not specify, use `25000` as default.
   - Must be the same as the resolution used for `${mcool_uri}`

---


### Step 1 — Initialize Project

1. Make director for this project:

Call:

- `mcp__project-init-tools__project_init`

with:

- `sample`: the user-provided sample name
- `task`: hic_matrix_qc

The tool will:

- Create `${sample}_nested_TAD_detection` directory.
- Return the full path of the `${sample}_nested_TAD_detection` directory, which will be used as `${proj_dir}`.

---

2. If the user provides a `.hic` file, convert it to `.mcool` file using `mcp__HiCExplorer-tools__hic_to_mcool` tool:

Call:
- `mcp__HiCExplorer-tools__hic_to_mcool`

with:
- `input_hic`: the user-provided path (e.g. `input.hic`)
- `sample`: the user-provided sample name
- `proj_dir`: directory to save the view file. In this skill, it is the full path of the `${sample}_nested_TAD_detection` directory returned by `mcp__project-init-tools__project_init`.

The tool will:
- Convert the `.hic` file to `.mcool` file.
- Return the path of the `.mcool` file.

If the conversion is successful, update `${mcool_uri}` to the path of the `.mcool` file.

---


### Step 2: List Available Resolutions in the .mcool file & Modify the Chromosome Names if Necessary

1. Check the resolutions in `mcool_uri`:

Call:

- `mcp__cooler-tools__list_mcool_resolutions`

with:

- `mcool_path`: the user-provided path (e.g. `input.mcool`) without resolution specified.

The tool will:

- List all resolutions in the .mcool file.
- Return the resolutions as a list.

If the user defined or default `${resolution}` is not found in the list, ask the user to specify the resolution again.
Else, use `${resolution}` for the following steps.

---

2. Check if the chromosome names in the .mcool file are started with "chr", and if not, modify them to start with "chr":

Call:

- `mcp__cooler-tools__harmonize_chrom_names`

with:
- `sample`: the user-provided sample name
- `proj_dir`: directory to save the expected-cis and eigs-cis files. In this skill, it is the full path of the `${sample}_Compartments_calling` directory returned by `mcp__project-init-tools__project_init`
- `mcool_uri`: cooler URI with resolution specified, e.g. `input.mcool::/resolutions/${resolution}`
- `resolution`: `${resolution}` must be the same as the resolution used for `${mcool_uri}` and must be an integer

The tool will:
- Check if the chromosome names in the .mcool file.
- If not, harmonize the chromosome names in the .mcool file.
- If the chromosome names are modified, return the path of the modified .mcool file under `${proj_dir}/` directory

---


### Step 3: Check chromosome length

Call:

- `mcp__cooler-tools__dump_chroms`

with:

- `mcool_uri`: cooler URI with resolution specified, e.g. `input.mcool::/resolutions/${resolution}`
- `resolution`: `${resolution}` must be the same as the resolution used for `${mcool_uri}` and must be an integer

The tool will:

- Return the chromosome name and length as a table.

---


### Step 4: Extract dense matrix from `.mcool`

Call:

- `mcp__cooler-tools__dump_dense_matrix`

with:

- `sample`: the user-provided sample name
- `proj_dir`: directory to save the view file. In this skill, it is the full path of the `${sample}_nested_TAD_detection` directory returned by `mcp__project-init-tools__project_init`.
- `mcool_uri`: cooler URI with resolution specified, e.g. `input.mcool::/resolutions/${resolution}`
- `resolution`: `${resolution}` must be the same as the resolution used for `${mcool_uri}` and must be an integer
- `chrom`: the user-provided chromosome name (e.g. `chr17`)
- `balanced`: whether to use balanced matrix (default: True)

The tool will:

- Extract the dense matrix from the .mcool file.
- Return the path of the dense matrix file.

---

### Step 5: Run OnTAD

Call:

- `mcp__OnTAD-tools__run_ontad`

with:

- `sample`: the user-provided sample name
- `proj_dir`: directory to save the view file. In this skill, it is the full path of the `${sample}_nested_TAD_detection` directory returned by `mcp__project-init-tools__project_init`.
- `dense_matrix`: the path to the dense matrix file (e.g. `${proj_dir}/matrices/chr17_25kb_dense.matrix`)
- `chrom`: the user-provided chromosome name (e.g. `chr17`)
- `chrom_length`: the corresponding chromosome length (e.g. 83257441) returned by `mcp__cooler-tools__dump_chroms` tool.
- `resolution`: the user-provided resolution (e.g. 25000)
- `penalty`: the penalty parameter for OnTAD (e.g. 0.1)
- `maxsz`: the maximum TAD size (in bins) (e.g. 200)

The tool will:
- Run OnTAD to call TADs and nested TAD structures.
- Return the path of the OnTAD output file (.tad, .bed, .log).

