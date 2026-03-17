---
name: differential-tad-analysis
description: This skill performs differential topologically associating domain (TAD) analysis using HiCExplorer's hicDifferentialTAD tool. It compares Hi-C contact matrices between two conditions based on existing TAD definitions to identify significantly altered chromatin domains.
---

# Differential TAD Analysis with HiCExplorer

## Overview

This skill identifies differentially interacting TADs between two experimental conditions using HiCExplorer.  
It assumes that TADs have already been called for the target condition.

Steps:
1. Normalize Hi-C matrices between conditions. Modify the chromosome name in the .mcool file if not started with "chr".
2. Prepare TAD domains (BED file) of the target sample. Make sure the consistence of the chromosame names between .mcool files and BED files. Modify the chromosome name in the BED file if not consistent with the .mcool file.
3. Perform differential TAD analysis.
4. Visualize the Hi-C contact maps for the target and control conditions.
5. Visualize and interpret significant TAD changes.


## When to Use This Skill

Use this skill when:
- You have already called TADs for one condition.
- You want to detect TADs that show significant interaction changes between two Hi-C matrices.
- You are comparing chromatin architecture between experimental conditions (e.g., treated vs. control, different cell types).

---

## Inputs & Outputs

### Inputs

- **File format:** Two files in .mcool, .cool, or .hic format for the target and control conditions.
- **Genome assembly:** Prompt the user for genome assembly used.
- **Resolution:** Provided by user. ~10-50 kb is recommended. Default is 50 kb. 25 kb is the best but memory-consuming.

### Outputs

```bash
${target}_${control}_differential_tad_analysis/
    normalize/
        ${target}_norm.cool
        ${control}_norm.cool
    TADs/
        ${target}_TAD_boundaries.bed  # Called TADs in BED format
        ${target}_TAD_boundaries.gff
        ${target}_TAD_domains.bed
        ${target}_TAD_score.bedgraph
        ${target}_TAD_tad_score.bm
    diff_TADs/
        ${target}_${control}_accepted.diff_tad
        ${target}_${control}_rejected.diff_tad
    plots/
        ${target}_${control}_contactmap_chrN.png
```

---


## Allowed Tools

When using this skill, you should restrict yourself to the following MCP tools from server `project-init-tools`, `genome-locate-tools`, `HiCExplorer-tools`:
- `mcp__project-init-tools__project_init`
- `mcp__HiCExplorer-tools__hic_to_mcool`
- `mcp__HiCExplorer-tools__run_hicFindTADs`
- `mcp__HiCExplorer-tools__hic_normalize`
- `mcp__HiCExplorer-tools__hic_differential_tad`
- `mcp__HiCExplorer-tools__generate_track_ini`
- `mcp__HiCExplorer-tools__plot_hic_contact_maps`
- `mcp__HiCExplorer-tools__plot_tads_region`

Do NOT fall back to:

- raw shell commands (`hicFindTADs`, `hicPlotTADs`, etc.)
- ad-hoc Python snippets (e.g. importing `cooler`, `bioframe`, `matplotlib` manually in the reply).

---


## Decision Tree

### Step 0 — Gather Required Information from the User

Before calling any tool, ask the user:

1. Target sample name (`target`): used as prefix and for the output directory `${target}_${control}_differential_tad_analysis`.
2. Control sample name (`control`): used as prefix and for the output directory `${target}_${control}_differential_tad_analysis`.
3. Genome assembly (`genome`): e.g. `hg38`, `mm10`, `danRer11`.  
   - **Never** guess or auto-detect.
4. Hi-C matrix path/URI (`mcool_uri_target`, `mcool_uri_control`): .
   - `path/to/target.mcool::/resolutions/50000`, `path/to/control.mcool::/resolutions/50000` (.mcool files with resolution specified)
   - or `.cool` file path
   - or `.hic` file path
5. Resolution (`resolution`): default `50000` (50 kb).  
   - If user does not specify, use `50000` as default.
   - Must be the same as the resolution used for `${mcool_uri_target}` and `${mcool_uri_control}`

---

### Step 1: Initialize Project

1. Make director for this project:

Call:
- `mcp__project-init-tools__project_init`

with:

- `sample`: `${target}_${control}`
- `task`: differential_tad_analysis

The tool will:

- Create `${target}_${control}_differential_tad_analysis` directory.
- Get the full path of the `${target}_${control}_differential_tad_analysis` directory, which will be used as `${proj_dir}`.

---

2. If the user provides `.hic` files for the target and control conditions, convert it to `.mcool` file first using `mcp__HiCExplorer-tools__hic_to_mcool` tool for the target and control conditions separately:

Call:
- `mcp__HiCExplorer-tools__hic_to_mcool`

with:
- `input_hic`: the user-provided path (e.g. `input.hic`)
- `sample`: `${target}`
- `proj_dir`: directory to save the view file. In this skill, it is the full path of the `${target}_${control}_differential_tad_analysis` directory returned by `mcp__project-init-tools__project_init`.
- `resolutions`: the user-provided resolutions (e.g. `[50000]`)

The tool will:
- Convert the `.hic` file to `.mcool` file for the target condition.
- Return the path of the `.mcool` file for the target condition.

---

Call:
- `mcp__HiCExplorer-tools__hic_to_mcool`

with:
- `input_hic`: the user-provided path (e.g. `input.hic`)
- `sample`: `${control}`
- `proj_dir`: directory to save the view file. In this skill, it is the full path of the `${target}_${control}_differential_tad_analysis` directory returned by `mcp__project-init-tools__project_init`.
- `resolutions`: the user-provided resolutions (e.g. `[50000]`)

The tool will:
- Convert the `.hic` file to `.mcool` file for the control condition.
- Return the path of the `.mcool` file for the control condition.

If the conversion is successful, update `${mcool_uri_target}` and `${mcool_uri_control}` to the path of the `.mcool` files.

---

3. Inspect the `.mcool` files for the target and control conditions respectively to list available resolutions and confirm the analysis resolution with the user.

Call:

- `mcp__cooler-tools__list_mcool_resolutions`

with:

- `mcool_path`: the path of the `.mcool` file for the target condition. If the user provides the path of the `.hic` file, these are the `.mcool` files returned by `mcp__HiCExplorer-tools__hic_to_mcool` tool.

The tool will:

- List all resolutions in the .mcool file for the target condition.
- Return the resolutions as a list.

---

Call:

- `mcp__cooler-tools__list_mcool_resolutions`

with:

- `mcool_path`: the path of the `.mcool` file for the control condition. If the user provides the path of the `.hic` file, these are the `.mcool` files returned by `mcp__HiCExplorer-tools__hic_to_mcool` tool.

The tool will:

- List all resolutions in the .mcool file for the control condition.
- Return the resolutions as a list.


If the `${resolution}` for the target condition or the control condition is not found, ask the user to specify the resolution again.
Else, use `${resolution}` for the target condition and `${resolution}` for the control condition.

---


### Step 2. Normalize Hi-C matrices

To ensure both matrices have comparable sequencing depth and coverage, perform normalization before analysis.

Call:

- `mcp__HiCExplorer-tools__hic_normalize`

with:

- `sample_target`: `${target}`
- `sample_control`: `${control}`
- `proj_dir`: Full path to project directory. In this skill, it is the full path of the `${target}_${control}_differential_tad_analysis` directory returned by `mcp__project-init-tools__project_init`.
- `mcool_uri_target`: `${mcool_uri_target}` with the resolution `${resolution}` specified.
- `mcool_uri_control`: `${mcool_uri_control}` with the resolution `${resolution}` specified.
- `resolution`: `${resolution}`, must be the same as the resolution used in previous steps and must be an integer.
- `method`: Normalization method: smallest, largest, or sum.

The tool will:
- Normalize the Hi-C matrices for the target and control conditions.
- Return the path of the normalized Hi-C matrices for the target and control conditions, which will be used as `${cool_target_norm}` and `${cool_control_norm}`.

---


### Step 3. Prepare TAD domains for the target condition

Use `mcp__HiCExplorer-tools__run_hicFindTADs` for comprehensive TAD identification for the target condition. Customize parameters to suit the resolution and depth of your Hi-C data:
Before calling the tool, **ask the user** for the following parameters:
- `${min_depth}`: Minimum window size (e.g. 3x resolution, default 150000, must be at least 3 times larger than the resolution)
- `${max_depth}`: Maximum window size (e.g. 6-10x resolution, default 300000, must be at least 5 times larger than the resolution)
- `${step}`: Step size for sliding window (default 50000, 25000 is the best but memory-consuming)
- `${multiple_testing}`: Multiple testing correction method (e.g. 'fdr')
- `${threshold_comparisons}`: FDR threshold for significant TADs (default 0.05)
- `${delta}`: Delta parameter for TAD boundary detection (default 0.01)
- `${chromosomes}`: Chromosomes to call TADs (default `chr22`). It is suggested to call TADs on a certain chromosome because it is memory-consuming to call TADs on all chromosomes and this process would likely be killed by the system.

Call:
- `mcp__HiCExplorer-tools__run_hicFindTADs`

with:
- `sample`: `${target}`
- `proj_dir`: directory to save the view file. In this skill, it is the full path of the `${sample}_TAD_calling` directory returned by `mcp__project-init-tools__project_init`.
- `mcool_uri`: cooler URI with resolution specified, e.g. `input.mcool::/resolutions/${resolution}`
- `resolution`: `${resolution}` must be the same as the resolution used for `${mcool_uri}` and must be an integer
- `min_depth`: `${min_depth}`, must be at least 3 times larger than the resolution.
- `max_depth`: `${max_depth}`, must be at least 5 times larger than the resolution.
- `step`: `${step}`
- `multiple_testing`: `${multiple_testing}`
- `threshold_comparisons`: `${threshold_comparisons}`
- `delta`: `${delta}`
- `chromosomes`: chromosomes to call TADs, e.g. `chr22`, space-separated list.

The tool will:
- Call `mcp__HiCExplorer-tools__run_hicFindTADs` to identify TADs.
- Return the path of the TADs file under `${proj_dir}/TADs/` directory.

---


### Step 4. Run differential TAD analysis

Detect TADs with statistically different intra- and inter-TAD interactions between the normalized matrices.

Call:
- `mcp__HiCExplorer-tools__hic_differential_tad`

with:
- `target`: `${target}`
- `control`: `${control}`
- `cool_target_norm`: `${cool_target_norm}` returned by `mcp__HiCExplorer-tools__hic_normalize` tool.
- `cool_control_norm`: `${cool_control_norm}` returned by `mcp__HiCExplorer-tools__hic_normalize` tool.
- `proj_dir`: directory to save the view file. In this skill, it is the full path of the `${target}_${control}_differential_tad_analysis` directory returned by `mcp__project-init-tools__project_init`.
- `target_tads`: `${target}_TADs_domains.bed` under `${proj_dir}/TADs/` directory returned by `mcp__HiCExplorer-tools__run_hicFindTADs` tool.
- `p_value`: Significance cutoff for differential TADs (default 0.05)
- `region_mode`: Region types used for testing: 'intra-TAD', 'left-inter-TAD', 'right-inter-TAD', or 'all' (default)
- `reject_rule`: Multiple region reject rule: 'one' (default) or 'all' for stricter criteria
- `threads`: Number of threads for chromosome-level parallelization (default 4)

The tool will:
- Run differential TAD analysis.
- Return the path of the differential TADs file under `${proj_dir}/diff_TADs/` directory.

---


### Step 5. Visualize the Hi-C matrices

Before calling the tool, **ask the user** for the target region, like `"chr22:1000000-2000000"`.

1. Visualize the Hi-C contact map for the target condition

Call :

- `mcp__HiCExplorer-tools__plot_hic_contact_maps`

with:
- `sample`: `${target}`
- `proj_dir`: directory to save the view file. In this skill, it is the full path of the `${target}_${control}_differential_tad_analysis` directory returned by `mcp__project-init-tools__project_init`.
- `cool_norm`: `${cool_target_norm}` returned by `mcp__HiCExplorer-tools__hic_normalize` tool.
- `region`: region to plot, e.g. `chr1:1000000-5000000`
- `dpi`: DPI for the plot (default 300)
- `log1p`: Apply log1p transform to contact values (default True)
- `per_chr`: Use --perChr option of hicPlotMatrix (default True)

The tool will:
- Visualize the Hi-C contact map for the target condition.
- Return the path of the Hi-C contact map file under `${proj_dir}/plots/` directory.

---

2. Visualize the Hi-C contact map for the control condition

Call:
- `mcp__HiCExplorer-tools__plot_hic_contact_maps`

with:
- `sample`: `${control}`
- `proj_dir`: directory to save the view file. In this skill, it is the full path of the `${target}_${control}_differential_tad_analysis` directory returned by `mcp__project-init-tools__project_init`.
- `cool_norm`: `${cool_control_norm}` returned by `mcp__HiCExplorer-tools__hic_normalize` tool.
- `region`: region to plot, e.g. `chr1:1000000-5000000`
- `dpi`: DPI for the plot (default 300)
- `log1p`: Apply log1p transform to contact values (default True)
- `per_chr`: Use --perChr option of hicPlotMatrix (default True)

The tool will:
- Visualize the Hi-C contact map for the control condition.
- Return the path of the Hi-C contact map file under `${proj_dir}/plots/` directory.

---


### Step 6. Overlay differential TADs

1. generate the `<track.ini>` file first for visualization

Call:
- `mcp__HiCExplorer-tools__generate_track_ini`

with:
- `sample`: `${target}_${control}`
- `proj_dir`: directory to save the view file. In this skill, it is the full path of the `${target}_${control}_differential_tad_analysis` directory returned by `mcp__project-init-tools__project_init`.
- `mcool_uri`: cooler URI with resolution specified, e.g. `input.mcool::/resolutions/${resolution}`
- `resolution`: `${resolution}` must be the same as the resolution used for `${mcool_uri}` and must be an integer
- `depth`: depth for the Hi-C matrix view, e.g. 1500000
- `min_value`: minimum value for the Hi-C matrix view, e.g. 0.0
- `max_value`: maximum value for the Hi-C matrix view, e.g. 80.0
- `if_diff_TADs`: True
- `target`: `${target}`, target sample name.
- `control`: `${control}`, control sample name.

The tool will:
- Generate the `<track.ini>` file under `${proj_dir}/temp/` directory.
- Return the path of the `<track.ini>` file.

---

2. Contact Maps with TAD Overlays
Before calling the tool, **ask the user** for the target region, like `"chr22:1000000-2000000"`.

Call:
- `mcp__HiCExplorer-tools__plot_tads_region`

with:
- `sample`: `${target}_${control}`
- `proj_dir`: directory to save the view file. In this skill, it is the full path of the `${sample}_TAD_calling` directory returned by `mcp__project-init-tools__project_init`.
- `region`: user-provided target region, like `"chr22:1000000-2000000"`
- `dpi`: dpi for the contact map, default is 300

The tool will:
- Generate the contact map with TAD boundaries overlayed.
- Return the path of the contact map file under `${proj_dir}/plots/` directory.

---


## Best Practices

- Ensure both Hi-C matrices are balanced and have identical resolutions.
- Confirm that the TAD BED file is derived from the target condition at the same resolution.
- Verify consistent normalization methods across all samples.
- Inspect the resulting visualizations to confirm biological plausibility.

