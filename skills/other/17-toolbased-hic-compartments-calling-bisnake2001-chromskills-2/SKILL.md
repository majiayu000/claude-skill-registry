---
name: hic-compartments-calling
description: This skill performs PCA-based A/B compartments calling on Hi-C .mcool datasets using pre-defined MCP tools from the cooler-tools, cooltools-tools, and plot-hic-tools servers.
---
# Hi-C Compartments Calling (MCP-based)

## Overview
This skill provides an automated workflow for compartments calling on .mcool, .cool or .hic Hi-C data.

Main steps include:
- Refer to the **Inputs & Outputs** section to verify required files and output structure.
- **Always prompt user** for genome assembly used.
- **Always prompt user** for resolution used to call compartments. ~50-250 kb is recommended. 100 kb is default.
- **Locate the genome FASTA file** from homer genome fasta file based on user input.
- **Rename chromosomes** in the .mcool or .cool file to satisfy the chromosome format with "chr".
- **Generate chromosome-arm view files** for compartment calling after changing the chromosome name.
- Perform **PCA-based compartment analysis** and extract the first principal component (PC1).
- **Generate compartment interaction saddle plots** and BigWig outputs for visualization.

## When to Use This Skill

Use this skill when:

- You want to identify A/B compartments from Hi-C `.mcool` or `.cool` files.
- You need PC1 compartment scores and bigWig tracks for genome browser visualization.
- You want a reproducible, normalized, automated compartment-calling workflow.


## Inputs & Outputs

### Inputs

- **File format:** .mcool, .cool, or .hic (Hi-C data file) data.
- **Genome assembly:** Prompt the user for genome assembly used.
- **Resolution:** Prompt the user for resolution used to call compartments. The default resolution is 100 kb.

### Outputs

```bash
${sample}_Compartments_calling/
    compartments/
      eigs.${resolution}.cis.vecs.tsv    # PC1 compartment scores  
      eigs.${resolution}.bw
      eigs.${resolution}.cis.lam.txt
      saddle.cis.${resolution}.digitized.tsv
      saddle.cis.${resolution}.saddledump.npz
    plots/         # PC1 track for genome browser  
      saddle.cis.${resolution}.pdf      # Saddle plot visualization 
    temp/
      expected.${resolution}.cis.tsv
      view_${genome}.tsv # Chromosome-arm view definition
      bins.${res}.tsv
      gc.${res}.tsv
```
---

## Allowed Tools

When using this skill, you should restrict yourself to the following MCP tools from server `cooler-tools`, `cooltools-tools`, `plot-hic-tools`, `project-init-tools`, `genome-locate-tools`:
- `mcp__project-init-tools__project_init`
- `mcp__genome-locate-tools__genome_locate_fasta`
- `mcp__HiCExplorer-tools__hic_to_mcool`
- `mcp__cooler-tools__list_mcool_resolutions`
- `mcp__cooler-tools__harmonize_chrom_names`
- `mcp__cooler-tools__make_view_chromarms`
- `mcp__cooler-tools__dump_bins_for_gc`
- `mcp__cooltools-tools__run_genome_gc`
- `mcp__cooltools-tools__run_expected_cis`
- `mcp__cooltools-tools__run_eigs_cis`
- `mcp__cooltools-tools__run_saddle`
- `mcp__plot-hic-tools__plot_saddle_pdf`

Do NOT fall back to:

- raw shell commands (`cooler dump`, `cooltools eigs-cis`, `cooltools saddle`, etc.)
- ad-hoc Python snippets (e.g. importing `cooler`, `bioframe`, `matplotlib` manually in the reply).

---

## Decision Tree

### Step 0 — Gather Required Information from the User

Before calling any tool, ask the user:

1. Sample name (`sample`): used as prefix and for the output directory `${sample}_Compartments_calling`.

2. Genome assembly (`genome`): e.g. `hg38`, `mm10`, `danRer11`.  
   - **Never** guess or auto-detect.

3. Hi-C matrix path/URI (`mcool_uri`): e.g. `.mcool` file path or `.hic` file path.
   - `path/to/sample.mcool::/resolutions/100000` (.mcool file with resolution specified)
   - or `.cool` file path
   - or `.hic` file path

4. Resolution (`resolution`): default `100000` (100 kb).  
   - If user does not specify, use `100000` as default.
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

---


### Step 3 — Create Chromosome-Arm View File

Use `bioframe` to define chromosome arms based on centromeres:

Call:

- `mcp__cooler-tools__make_view_chromarms`

with:

- `proj_dir`: directory to save the expected-cis and eigs-cis files. In this skill, it is the full path of the `${sample}_Compartments_calling` directory returned by `mcp__project-init-tools__project_init`
- `mcool_uri`: cooler URI with resolution specified, e.g. `input.mcool::/resolutions/${resolution}`
- `resolution`: `${resolution}` must be the same as the resolution used for `${mcool_uri}` and must be an integer
- `genome`: genome assembly

The tool will:

- Fetch chromsizes and centromeres via `bioframe`.
- Generate chromosomal arms and filter them to those present in the cooler.
- Return the path of the view file under `${proj_dir}/temp/` directory.

---


### Step 4 — Compute GC Track for Bins

1. Dump bins for GC track:

Call:
- `mcp__cooler-tools__dump_bins_for_gc`
with:
- `sample`: the user-provided sample name
- `proj_dir`: directory to save the GC track file. In this skill, it is the full path of the `${sample}_Compartments_calling` directory returned by `mcp__project-init-tools__project_init`
- `mcool_uri`: cooler URI with resolution specified, e.g. `input.mcool::/resolutions/${resolution}`
- `resolution`: `${resolution}` must be the same as the resolution used for `${mcool_uri}` and must be an integer

The tool will:
- Dump bins at the specified resolution from the cooler.
- Return the path of the bins file under `${proj_dir}/temp/` directory.


2. Compute GC track:

Call:

- `mcp__cooltools-tools__run_genome_gc`

with:

- `sample`: the user-provided sample name
- `proj_dir`: directory to save the GC track file. In this skill, it is the full path of the `${sample}_Compartments_calling` directory returned by `mcp__project-init-tools__project_init`
- `mcool_uri`: cooler URI with resolution specified, e.g. `input.mcool::/resolutions/${resolution}`
- `resolution`: `${resolution}` must be the same as the resolution used for `${mcool_uri}` and must be an integer
- `genome`: genome assembly

The tool will:

- Compute GC content for each bin.
- Return the path of the GC track file under `${proj_dir}/temp/` directory.

---


### Step 5 — Run Expected-cis and Eigs-cis (PCA Compartment Calling)

1. Calculate expected cis:

Call:
- `mcp__cooltools-tools__run_expected_cis`

with:
- `sample`: the user-provided sample name
- `proj_dir`: directory to save the expected-cis and eigs-cis files. In this skill, it is the full path of the `${sample}_Compartments_calling` directory returned by `mcp__project-init-tools__project_init`
- `mcool_uri`: cooler URI with resolution specified, e.g. `input.mcool::/resolutions/${resolution}`
- `resolution`: `${resolution}` must be the same as the resolution used for `${mcool_uri}` and must be an integer
- `view_path`: the path to the view file (e.g. `${proj_dir}/temp/view_${genome}.tsv`)
- `clr_weight_name`: the name of the weight column (default: `weight`)
- `ignore_diags`: the number of diagonals to ignore based on resolution

The tool will:
- Generate expected cis file.
- Return the path of the expected cis file under `${proj_dir}/temp/` directory.


2. Calculate eigs cis:

Call:

- `mcp__cooltools-tools__run_eigs_cis`

with:

- `sample`: the user-provided sample name
- `proj_dir`: directory to save the expected-cis and eigs-cis files. In this skill, it is the full path of the `${sample}_Compartments_calling` directory returned by `mcp__project-init-tools__project_init`
- `mcool_uri`: cooler URI with resolution specified, e.g. `input.mcool::/resolutions/${resolution}`
- `resolution`: `${resolution}` must be the same as the resolution used for `${mcool_uri}` and must be an integer
- `view_path`: the view TSV from Step 3 (e.g. `view_${genome}.tsv`)
- `gc_tsv`: GC track TSV from Step 4
- `clr_weight_name`: balancing column name (default `"weight"`, but can be set based on `clr.bins().columns` if the user tells you the correct name)
- `n_eigs`: the number of principal components to compute (default 1)
- `make_bigwig`: whether to make bigwig file for PC1 track (default True)

This tool will:

- Run `cooltools expected-cis` to compute expected contact frequencies.
- Run `cooltools eigs-cis` to perform PCA and extract PC1.
- Return the path of the eigs-cis vecs file under `${proj_dir}/compartments/` directory.
- Return the path of the bigWig file under `${proj_dir}/compartments/` directory.

If the user reports an error about balancing weights:

- Ask the user which weight column should be used.
- Re-run `expected_and_eigs` with the correct `clr_weight_name`.

---

### Step 6 — Run Saddle Analysis

Call:

- `mcp__cooltools-tools__run_saddle`

with:

- `sample`: the user-provided sample name
- `proj_dir`: directory to save the saddle file. In this skill, it is the full path of the `${sample}_Compartments_calling` directory returned by `mcp__project-init-tools__project_init`
- `mcool_uri`: cooler URI with resolution specified, e.g. `input.mcool::/resolutions/${resolution}`
- `resolution`: `${resolution}` must be the same as the resolution used for `${mcool_uri}` and must be an integer
- `view_path`: the view TSV from Step 3 (e.g. `view_${genome}.tsv`)
- `eigs_vecs_tsv`: the eigs-cis vecs TSV from Step 5 (e.g. `compartments/eigs.${resolution}.cis.vecs.tsv`)
- `expected_cis_tsv`: the expected-cis TSV from Step 5 (e.g. `temp/expected_cis.${resolution}.tsv`)
- `clr_weight_name`: balancing column name (default `"weight"`, but can be set based on `clr.bins().columns` if the user tells you the correct name)
- `qrange_low` and `qrange_high`: default `0.02` and `0.98`

The tool will:

- Run `cooltools saddle`.
- Generate saddle dump and related outputs, typically:  
- Return the path of the saddle dump file under `${proj_dir}/compartments/` directory.
- Return the path of the other related outputs under `${proj_dir}/compartments/` directory.

---

### Step 7 — Plot Saddle as PDF

Call:

- `mcp__plot-hic-tools__plot_saddle_pdf`

with:

- `sample`: the user-provided sample name
- `proj_dir`: directory to save the saddle file. In this skill, it is the full path of the `${sample}_Compartments_calling` directory returned by `mcp__project-init-tools__project_init`
- `resolution`: `${resolution}` must be the same as the resolution used for `${mcool_uri}` and must be an integer
- `chr_name`: the user-provided chromosome name, e.g. `chr1`

This tool will:

- Load the corresponding `.saddledump.npz` file.
- Plot the saddle matrix with `LogNorm(1e-1, 1e1)` and `RdBu_r` colormap.
- Return the path of the compartment scores distribution PDF file under `${proj_dir}/plots/` directory.
- Return the path of the saddle plot PDF file under `${proj_dir}/plots/` directory.
- Return the path of the PC1 track PDF file under `${proj_dir}/plots/` directory.

If the saddledump file is missing, inform the user to run `run_saddle` first.

---

## Best Practices

- Always confirm the genome and resolution explicitly with the user.
- Always use the defined MCP tools instead of ad-hoc code.
- If the user asks “how to run this manually”, you may conceptually describe the steps but still **prefer** to recommend using the MCP pipeline for reproducibility.
- If multiple resolutions are required, re-run the MCP tools with different `resolution` values and keep outputs in the same `${proj_dir}` directory, using resolution in filenames for disambiguation.
```