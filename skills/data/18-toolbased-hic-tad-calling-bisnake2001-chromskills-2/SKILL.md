---
name: hic-tad-calling
description: This skill should be used when users need to identify topologically associating domains (TADs) from Hi-C data in .mcools (or .cool) files or when users want to visualize the TAD in target genome loci. It provides workflows for TAD calling and visualization.
---

# TADs Calling with HiCExplorer and Cooltools

## Overview

This skill enables comprehensive identification and analysis of topologically associating domains (TADs) from Hi-C data stored in .mcool (or .cool) files. It integrates **HiCExplorer** for robust TAD calling and visualization capabilities.

Main steps include:

- Refer to the **Inputs & Outputs** section to verify required files and output structure.
- **Data Preparation**: Ensure .mcool files are formatted correctly and resolutions are verified.
- **Always prompt user** for resolution used to call TADs.
- **TAD Calling**: Use **HiCExplorer** to call TADs with customizable parameters.
- **Always prompt user** for target genomic loci for visualization.
- **Visualization**: Generate contact maps with TAD boundaries overlayed, for specific regions of the genome.

---

## When to use this skill

Use this skill when:

- You need to identify TADs in Hi-C data stored in .mcool (or .cool) files.
- You want to visualize TADs in a specific region of the genome.
- You need to perform automated TAD calling with HiCExplorer, including statistical corrections.

---

## Inputs & Outputs

### Inputs

- **File format:** .mcool, .cool, or .hic (Hi-C data file).
- **Resolution:** Provided by user. ~10-50 kb is recommended. Default is 50 kb. 25 kb is the best but memory-consuming.
- **Target region:** Genome region provided by user to visualize TADs (e.g., `"chr22:1000000-2000000"`).

### Outputs

```bash
${sample}_TAD_calling/
    TADs/
        ${sample}_TAD_boundaries.bed  # Called TADs in BED format
        ${sample}_TAD_boundaries.gff
        ${sample}_TAD_domains.bed
        ... # other files output by the hicFindTADs
    plots/
        ${sample}_TADs_${genome_loci}.pdf  # TADs visualization (contact map)
    temp/
        ${sample}_track.ini            # Configuration file for visualization
```
---

## Allowed Tools

When using this skill, you should restrict yourself to the following MCP tools from server `cooler-tools`, `cooltools-tools`, `project-init-tools`, `genome-locate-tools`:
- `mcp__project-init-tools__project_init`
- `mcp__genome-locate-tools__genome_locate_fasta`
- `mcp__HiCExplorer-tools__hic_to_mcool`
- `mcp__HiCExplorer-tools__check_mcool_file`
- `mcp__HiCExplorer-tools__run_hicFindTADs`
- `mcp__HiCExplorer-tools__generate_track_ini`
- `mcp__HiCExplorer-tools__plot_tads_region`

Do NOT fall back to:

- raw shell commands (`hicFindTADs`, `hicPlotTADs`, etc.)
- ad-hoc Python snippets (e.g. importing `cooler`, `bioframe`, `matplotlib` manually in the reply).

---

## Decision Tree

### Step 0 — Gather Required Information from the User

Before calling any tool, ask the user:

1. Sample name (`sample`): used as prefix and for the output directory `${sample}_TAD_calling`.
2. Genome assembly (`genome`): e.g. `hg38`, `mm10`, `danRer11`.  
   - **Never** guess or auto-detect.
3. Hi-C matrix path/URI (`mcool_uri`): e.g. `.mcool` file path or `.hic` file path.
   - `path/to/sample.mcool::/resolutions/50000` (.mcool file with resolution specified)
   - or `.cool` file path
   - or `.hic` file path
4. Resolution (`resolution`): default `50000` (50 kb).  
   - If user does not specify, use `50000` as default.
   - Must be the same as the resolution used for `${mcool_uri}`

---

### Step 1: Initialize Project

1. Make director for this project:

Call:
- `mcp__project-init-tools__project_init`

with:

- `sample`: the user-provided sample name
- `task`: TAD_calling

The tool will:

- Create `${sample}_TAD_calling` directory.
- Get the full path of the `${sample}_TAD_calling` directory, which will be used as `${proj_dir}`.

---

2. If the user provides a `.hic` file, convert it to `.mcool` file first using `mcp__HiCExplorer-tools__hic_to_mcool` tool:

Call:
- `mcp__HiCExplorer-tools__hic_to_mcool`

with:
- `input_hic`: the user-provided path (e.g. `input.hic`)
- `sample`: the user-provided sample name
- `proj_dir`: directory to save the view file. In this skill, it is the full path of the `${sample}_TAD_calling` directory returned by `mcp__project-init-tools__project_init`.
- `resolutions`: the user-provided resolutions (e.g. `[50000]`)

The tool will:
- Convert the `.hic` file to `.mcool` file.
- Return the path of the `.mcool` file.

If the conversion is successful, update `${mcool_uri}` to the path of the `.mcool` file.

---

3. Inspect the `.mcool` file to list available resolutions and confirm the analysis resolution with the user.

Call:

- `mcp__cooler-tools__list_mcool_resolutions`

with:

- `mcool_path`: the user-provided path (e.g. `input.mcool`) or the path of the `.mcool` file returned by `mcp__HiCExplorer-tools__hic_to_mcool`

The tool will:

- List all resolutions in the .mcool file.
- Return the resolutions as a list.

If the `${resolution}` is not found, ask the user to specify the resolution again.
Else, use `${resolution}`.

---


### Step 2: HiCExplorer TAD Calling

Use `mcp__HiCExplorer-tools__run_hicFindTADs` for comprehensive TAD identification. Customize parameters to suit the resolution and depth of your Hi-C data:
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
- `sample`: `${sample}`
- `proj_dir`: directory to save the view file. In this skill, it is the full path of the `${sample}_TAD_calling` directory returned by `mcp__project-init-tools__project_init`.
- `mcool_uri`: cooler URI with resolution specified, e.g. `input.mcool::/resolutions/${resolution}`
- `resolution`: `${resolution}` must be the same as the resolution used for `${mcool_uri}` and must be an integer
- `min_depth`: `${min_depth}`, must be at least 3 times larger than the resolution.
- `max_depth`: `${max_depth}`, must be at least 5 times larger than the resolution.
 `step`: `${step}`
- `multiple_testing`: `${multiple_testing}`
- `threshold_comparisons`: `${threshold_comparisons}`
- `delta`: `${delta}`
- `chromosomes`: chromosomes to call TADs, e.g. `chr22`, space-separated list.

The tool will:
- Call `mcp__HiCExplorer-tools__run_hicFindTADs` to identify TADs.
- Return the path of the TADs file under `${proj_dir}/TADs/` directory.

---

## Step 3: Visualization

1. generate the `<track.ini>` file first for visualization

Call:
- `mcp__HiCExplorer-tools__generate_track_ini`

with:
- `sample`: `${sample}`
- `proj_dir`: directory to save the view file. In this skill, it is the full path of the `${sample}_TAD_calling` directory returned by `mcp__project-init-tools__project_init`.
- `mcool_uri`: cooler URI with resolution specified, e.g. `input.mcool::/resolutions/${resolution}`
- `resolution`: `${resolution}` must be the same as the resolution used for `${mcool_uri}` and must be an integer
- `depth`: depth for the Hi-C matrix view, e.g. 1500000
- `min_value`: minimum value for the Hi-C matrix view, e.g. 0.0
- `max_value`: maximum value for the Hi-C matrix view, e.g. 80.0

The tool will:
- Generate the `<track.ini>` file under `${proj_dir}/temp/` directory.
- Return the path of the `<track.ini>` file.

---

2. Contact Maps with TAD Overlays
Before calling the tool, **ask the user** for the target region, like `"chr22:1000000-2000000"`.

Call:
- `mcp__HiCExplorer-tools__plot_tads_region`

with:
- `sample`: `${sample}`
- `proj_dir`: directory to save the view file. In this skill, it is the full path of the `${sample}_TAD_calling` directory returned by `mcp__project-init-tools__project_init`.
- `region`: user-provided target region, like `"chr22:1000000-2000000"`
- `dpi`: dpi for the contact map, default is 300

The tool will:
- Generate the contact map with TAD boundaries overlayed.
- Return the path of the contact map file under `${proj_dir}/plots/` directory.

---


# Best Practices

- It is suggested to call TADs on a certain chromosome because it is memory-consuming to call TADs on all chromosomes and this process would likely be killed by the system.
