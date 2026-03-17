---
name: hic-loop-calling
description: This skill performs chromatin loop detection from Hi-C .mcool files using cooltools.
---

# Hi-C Loop Calling

## Overview

This skill provides a minimal and efficient workflow for detecting chromatin loops from Hi-C data stored in .mcool format and preparing results for visualization in IGV. The key steps involved include:
- Refer to the **Inputs & Outputs** section to verify required files and output structure.
- **Always prompt user** for genome assembly used.
- **Always prompt user** for resolution used to call loops. ~2-50 kb is recommended. 5 kb is default.
- **Locate the genome FASTA file** from homer genome fasta file based on user input.
- **Rename chromosomes** in the .mcool or .cool file to satisfy the chromosome format with "chr".
- **Generate chromosome-arm view files** for compartment calling after changing the chromosome name.
- **Extract contact matrices** from .mcool files at the desired resolution.
- **Detect chromatin loops**.

---

## When to Use This Skill

Use this skill when:

- You need to identify (in other words, call, or detect) chromatin loops from Hi-C data in .mcool format.

---

## Inputs & Outputs

### Inputs

- **File format:** .mcool, .cool, or .hic (Hi-C data file).
- **Genome assembly:** Prompt the user for genome assembly used.
- **Resolution:** Choose the desired resolution for loop calling (e.g., 5 kb, 10 kb, etc.).

### Outputs

```bash
${sample}_loop_calling/
    loops/
        ${sample}_loops_${resolution}.bedpe  # Detected chromatin loops in BEDPE format.
    temp/
        view_${genome}.tsv
        expected_cis.${resolution}.tsv 
```
---

## Allowed Tools

When using this skill, you should restrict yourself to the following MCP tools from server `cooler-tools`, `cooltools-tools`, `project-init-tools`, `genome-locate-tools`:
- `mcp__project-init-tools__project_init`
- `mcp__genome-locate-tools__genome_locate_fasta`
- `mcp__HiCExplorer-tools__hic_to_mcool`
- `mcp__cooler-tools__list_mcool_resolutions`
- `mcp__cooler-tools__harmonize_chrom_names`
- `mcp__cooler-tools__make_view_chromarms`
- `mcp__cooltools-tools__run_expected_cis`
- `mcp__cooltools-tools__run_dots`

Do NOT fall back to:

- raw shell commands (`cooltools expected-cis`, `cooltools dots`, etc.)
- ad-hoc Python snippets (e.g. importing `cooler`, `bioframe`, `matplotlib` manually in the reply).

---


## Decision Tree

### Step 0 — Gather Required Information from the User

Before calling any tool, ask the user:

1. Sample name (`sample`): used as prefix and for the output directory `${sample}_loop_calling`.

2. Genome assembly (`genome`): e.g. `hg38`, `mm10`, `danRer11`.  
   - **Never** guess or auto-detect.

3. Hi-C matrix path/URI (`mcool_uri`):
   - `path/to/sample.mcool::/resolutions/5000` (.mcool file with resolution specified)
   - or `.cool` file path
   - or `.hic` file path

4. Resolution (`resolution`): default `5000` (5 kb).  
   - If user does not specify, use `5000` as default.
   - Must be the same as the resolution used for `${mcool_uri}`

---


### Step 1 — Initialize Project & Locate Genome FASTA

1. Make director for this project:

Call:

- `mcp__project-init-tools__project_init`

with:

- `sample`: the user-provided sample name
- `task`: loop_calling

The tool will:

- Create `${sample}_loop_calling` directory.
- Return the full path of the `${sample}_loop_calling` directory, which will be used as `${proj_dir}`.

---

2. If the user provides a `.hic` file, convert it to `.mcool` file using `mcp__HiCExplorer-tools__hic_to_mcool` tool:

Call:
- `mcp__HiCExplorer-tools__hic_to_mcool`

with:
- `input_hic`: the user-provided path (e.g. `input.hic`)
- `sample`: the user-provided sample name
- `proj_dir`: directory to save the view file. In this skill, it is the full path of the `${sample}_loop_calling` directory returned by `mcp__project-init-tools__project_init`.

The tool will:
- Convert the `.hic` file to `.mcool` file.
- Return the path of the `.mcool` file.

If the conversion is successful, update `${mcool_uri}` to the path of the `.mcool` file.

---

3. Locate genome fasta file:

Call:

- `mcp__genome-locate-tools__genome_locate_fasta`

with:

- `genome`: the user-provided genome assembly

The tool will:

- Locate genome FASTA.  
- Verify the FASTA exists.

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


### Step 3 — Create Chromosome-Arm View File

Use `bioframe` to define chromosome arms based on centromeres:

Call:

- `mcp__cooler-tools__make_view_chromarms`

with:

- `genome`: genome assembly
- `mcool_uri`: cooler URI with resolution specified, e.g. `input.mcool::/resolutions/${resolution}`
- `resolution`: `${resolution}` must be the same as the resolution used for `${mcool_uri}` and must be an integer
- `proj_dir`: directory to save the view file. In this skill, it is the full path of the `${sample}_loop_calling` directory returned by `mcp__project-init-tools__project_init`.

The tool will:

- Fetch chromsizes and centromeres via `bioframe`.
- Generate chromosomal arms and filter them to those present in the cooler.
- Return the path of the view file under `${proj_dir}/temp/` directory.

---


### Step 4: Detect Chromatin Loops

1. Calculate expected cis:

Call:
- `mcp__cooltools-tools__run_expected_cis`

with:
- `sample`: the user-provided sample name
- `proj_dir`: directory to save the view file. In this skill, it is the full path of the `${sample}_loop_calling` directory returned by `mcp__project-init-tools__project_init`.
- `mcool_uri`: cooler URI with resolution specified, e.g. `input.mcool::/resolutions/${resolution}`
- `resolution`: `${resolution}` must be the same as the resolution used for `${mcool_uri}` and must be an integer
- `view_path`: the path to the view file (e.g. `${proj_dir}/temp/view_${genome}.tsv`)
- `clr_weight_name`: the name of the weight column (default: `weight`)
- `ignore_diags`: the number of diagonals to ignore based on resolution

The tool will:
- Generate expected cis file.
- Return the path of the expected cis file under `${proj_dir}/temp/` directory.

---

2. Call loops:

Call:

- `mcp__cooltools-tools__run_dots`

with:

- `sample`: the user-provided sample name
- `proj_dir`: directory to save the view file. In this skill, it is the full path of the `${sample}_loop_calling` directory returned by `mcp__project-init-tools__project_init`.
- `mcool_uri`: cooler URI with resolution specified, e.g. `input.mcool::/resolutions/${resolution}`
- `resolution`: `${resolution}` must be the same as the resolution used for `${mcool_uri}` and must be an integer
- `view_path`: the path to the view file (e.g. `${proj_dir}/temp/view_${genome}.tsv`)
- `nproc`: the number of processes for cooltools (default 6)

The tool will:

- Generate loops bedpe.
- Return the path of the loops bedpe file under `${proj_dir}/loops/` directory.

---

