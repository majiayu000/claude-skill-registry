---
name: hic-matrix-qc
description: This skill performs standardized quality control (QC) on Hi-C contact matrices stored in .mcool or .cool format. It computes coverage and cis/trans ratios, distance-dependent contact decay (P(s) curves), coverage uniformity, and replicate correlation at a chosen resolution using cooler and cooltools. Use it to assess whether Hi-C data are of sufficient quality for downstream analyses such as TAD calling, loop detection, and compartment analysis.
---

# Hi-C Contact Matrix QC for .mcool Files

## Overview

This skill performs QC on Hi-C matrices stored in .cool or .mcool format files at a user-selected resolution.

Main steps include:

- Refer to the **Inputs & Outputs** section to check required inputs and set up the output directory structure.  
- **Always wait the user feedback** if required files are not available in the current working directory by asking  
  `"${files} not available, provide required files or skip and proceed ?"`
- **Inspect the `.mcool` file** to list available resolutions and confirm the analysis resolution with the user.
- **Compute coverage and cis/trans ratios**.
- **Assess coverage uniformity** across bins from coverage tables.
- **Compute cis expected contact frequency and distance-dependent contact decay (P(s) curves)**.
- **Visualize contact decay and P(s) scaling curves**.
- **If multiple Hi-C replicates are provided**, compute pairwise correlation of balanced matrices at the chosen resolution.
- **Summarize QC metrics and plots** into a structured output directory.

---

## When to use this skill

Use the hic-matrix-qc skill when you need to evaluate the quality of Hi-C contact matrices that are already stored in .cool, .mcool or .hic format.

---

## Inputs & Outputs


### Inputs

- **File format:** .mcool, .cool, or .hic (Hi-C data file).
- **Genome assembly:** Prompt the user for genome assembly used.
- **Resolution:** Choose the desired resolution for matrix QC. ~50-100 kb is recommended. Default is 100 kb.

Optional: Multiple Hi-C matrices for replicate QC
`rep1.mcool` `rep2.mcool` `rep3.mcool`

### Outputs

```bash
${sample}_hic_matrix_qc/
  logs/
    hic_qc.log               # Commands, parameters, and software versions
  metrics/
    coverage.${resolution}.tsv               # Per-bin cis/total coverage from cooltools coverage
    cis_trans_summary.${resolution}.txt      # Summarized cis, total, trans counts, and ratios
    ps_scaling_summary.${resolution}.txt     # Optional table with P(s) slope(s) in defined distance ranges
    replicate_correlation.${resolution}.tsv  # Pairwise correlation coefficients between replicates
  plots/
    coverage_histogram.${resolution}.pdf     # Coverage uniformity plot
    ps_curve.${resolution}.pdf               # P(s) curve (contact probability vs distance)
    decay_curve.${resolution}.pdf            # Contact decay curve (raw/normalized)
    replicate_correlation_heatmap.${resolution}.pdf  # Correlation matrix heatmap (if multiple replicates)
  comparison/
    replicate_vectors_${resolution}.npz      # (Optional) Stored vectors used for replicate correlations
  temp/
    expected_cis.${resolution}.tsv           # Expected cis contacts vs distance from expected-cis
```
---

## Allowed Tools

When using this skill, you should restrict yourself to the following MCP tools from server `cooler-tools`, `cooltools-tools`, `plot-hic-tools`, `project-init-tools`:
- `mcp__project-init-tools__project_init`
- `mcp__cooler-tools__compute_coverage_and_cis_trans`
- `mcp__plot-hic-tools__plot_coverage_histogram`
- `mcp__cooltools-tools__run_expected_cis`
- `mcp__plot-hic-tools__plot_ps_and_decay`
- `mcp__plot-hic-tools__replicate_correlation`

Do NOT fall back to:

- raw shell commands (`cooltools coverage`, `cooltools expected-cis`, `cooltools dots`, etc.)
- ad-hoc Python snippets (e.g. importing `cooler`, `bioframe`, `matplotlib` manually in the reply).

---

## Decision Tree

### Step 0 — Gather Required Information from the User

Before calling any tool, ask the user:

1. Sample name (`sample`): used as prefix and for the output directory `${sample}_hic_matrix_qc`.

2. Genome assembly (`genome`): e.g. `hg38`, `mm10`, `danRer11`.  
   - **Never** guess or auto-detect.

3. Hi-C matrix path/URI (`mcool_uri`):
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
- `task`: hic_matrix_qc

The tool will:

- Create `${sample}_hic_matrix_qc` directory.
- Return the full path of the `${sample}_hic_matrix_qc` directory, which will be used as `${proj_dir}`.

---

2. If the user provides a `.hic` file, convert it to `.mcool` file using `mcp__HiCExplorer-tools__hic_to_mcool` tool:

Call:
- `mcp__HiCExplorer-tools__hic_to_mcool`

with:
- `input_hic`: the user-provided path (e.g. `input.hic`)
- `sample`: the user-provided sample name
- `proj_dir`: directory to save the view file. In this skill, it is the full path of the `${sample}_hic_matrix_qc` directory returned by `mcp__project-init-tools__project_init`.

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


### Step 3: Compute coverage and cis/trans ratio

- Quantify cis and total coverage and derive cis/trans ratio at the chosen resolution.
- If the cooler is unbalanced or has a different weight column name, ask the user for the correct weight name or whether to use raw counts (empty --clr_weight_name).

Call:
`mcp__cooler-tools__compute_coverage_and_cis_trans`

with:
- `proj_dir`: directory to save the view file. In this skill, it is the full path of the `${sample}_hic_matrix_qc` directory returned by `mcp__project-init-tools__project_init`.
- `mcool_uri`: cooler URI with resolution specified, e.g. `input.mcool::/resolutions/${resolution}`
- `resolution`: `${resolution}` must be the same as the resolution used for `${mcool_uri}` and must be an integer
- `clr_weight_name`: name of the weight column (default: `weight`)
- `cis_column`: name of the cis column (default: `cov_cis_weight`)
- `total_column`: name of the total column (default: `cov_tot_weight`)

The tool will:
- Compute coverage and cis/trans ratio at the chosen resolution.
- Output: `coverage.${resolution}.tsv` `cis_trans_summary.${resolution}.txt`

---


### Step 4: Assess coverage uniformity

Assess coverage uniformity by plotting a histogram of per-bin coverage.

Call:
`mcp__plot-hic-tools__plot_coverage_histogram`
with:
- `sample`: the user-provided sample name
- `proj_dir`: directory to save the view file. In this skill, it is the full path of the `${sample}_hic_matrix_qc` directory returned by `mcp__project-init-tools__project_init`.
- `resolution`: `${resolution}`
- `column`: which column to histogram, e.g. `cis`, `total`, or `n_valid` (default: `cis`)
- `bins`: number of histogram bins (default: 50)

The tool will:
- Draw the histogram of per-bin coverage.
- Return the path of the coverage histogram plot.

After the tool runs, **inform user with this**:
- A reasonably broad distribution is expected; a long tail is common.
- Many zero-coverage bins may indicate insufficient depth at this resolution.
- A few bins with extremely high coverage may indicate local artifacts (e.g. centromeres, rDNA, mapping issues).

---


### Step 5: Compute cis expected and P(s) contact decay curve

1. Use `bioframe` to define chromosome arms based on centromeres:

Call:

- `mcp__cooler-tools__make_view_chromarms`

with:

- `sample`: the user-provided sample name
- `proj_dir`: directory to save the view file. In this skill, it is the full path of the `${sample}_hic_matrix_qc` directory returned by `mcp__project-init-tools__project_init`.
- `mcool_uri`: cooler URI with resolution specified, e.g. `input.mcool::/resolutions/${resolution}`
- `resolution`: `${resolution}` must be the same as the resolution used for `${mcool_uri}` and must be an integer
- `genome`: the user-provided genome assembly

The tool will:

- Fetch chromsizes and centromeres via `bioframe`.
- Generate chromosomal arms and filter them to those present in the cooler.
- Return the path of the view file under `${proj_dir}/temp/` directory.

---

2. Calculate expected cis:

Call:
- `mcp__cooltools-tools__run_expected_cis`

with:
- `sample`: the user-provided sample name
- `proj_dir`: directory to save the view file. In this skill, it is the full path of the `${sample}_hic_matrix_qc` directory returned by `mcp__project-init-tools__project_init`.
- `mcool_uri`: cooler URI with resolution specified, e.g. `input.mcool::/resolutions/${resolution}`
- `resolution`: `${resolution}` must be the same as the resolution used for `${mcool_uri}` and must be an integer
- `view_path`: the path to the view file (e.g. `${proj_dir}/temp/view_${genome}.tsv`)
- `expected_cis_tsv`: the path to the expected cis file (e.g. `${proj_dir}/temp/expected_cis.${resolution}.tsv`)
- `clr_weight_name`: the name of the weight column (default: `weight`)
- `ignore_diags`: the number of diagonals to ignore based on resolution

The tool will:
- Generate expected cis file.
- Return the path of the expected cis file.

---

3. Plot the P(s) curve (log–log distance vs expected contacts) and decay curve (raw counts vs balanced P(s))

Call:
- `mcp__plot-hic-tools__plot_ps_and_decay`

with:
- `sample`: the user-provided sample name
- `proj_dir`: directory to save the view file. In this skill, it is the full path of the `${sample}_hic_matrix_qc` directory returned by `mcp__project-init-tools__project_init`.
- `mcool_uri`: cooler URI with resolution specified, e.g. `input.mcool::/resolutions/${resolution}`
- `resolution`: `${resolution}` must be the same as the resolution used for `${mcool_uri}` and must be an integer

The tool will:
- Plot the P(s) curve (log–log distance vs expected contacts)
- Plot the decay curve (raw counts vs balanced P(s))
- Return the path of the P(s) curve plot and decay curve plot.

---


### Step 6: Replicate correlation of Hi-C matrices (optional)

- Quantify similarity between Hi-C replicates at matrix level.
- Assumes:
  - At least two .mcool files (e.g. rep1.mcool, rep2.mcool, etc.).
  - Same genome assembly and resolution.

Call:
- `mcp__plot-hic-tools__replicate_correlation`

with:
- `mcool_uris`: list of cooler URIs with resolution specified, one per replicate, e.g. `['rep1.mcool::/resolutions/${resolution}', 'rep2.mcool::/resolutions/${resolution}']`
- `output_prefix`: prefix for the output files, e.g. `hic_qc_replicates_${resolution}`
- `chroms`: list of chromosomes to use for correlation, e.g. `['chr1', 'chr2']`
- `use_balanced`: whether to use balanced matrices (default: `True`)

The tool will:
- Compute replicate correlation of Hi-C matrices.
- Return the path of the replicate correlation file.

After the tool runs, **inform user with this**:
- Very low correlations (<0.7) between supposed biological replicates may indicate experimental issues or mismatched samples.

---

## Notes & troubleshooting

- If balancing weights are missing or correlation is calculated on raw counts, explicitly record this in logs and interpret with caution.

