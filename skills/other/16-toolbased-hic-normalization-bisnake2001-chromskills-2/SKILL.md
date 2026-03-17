---
name: hic-normalization
description: Automatically detect and normalize Hi-C data. Only .cool or .mcool file is supported. All .mcool files are then checked for existing normalization (supports bins/weight only) and balanced if none of the normalizations exist.
---

## Overview

This skill performs Hi-C data normalization on .mcool files.  
Main steps include:

- Refer to the **Inputs & Outputs** section to verify required files and output structure.
- **Check normalization status** per resolution (supports bins/weight columns only).
- If a resolution is not normalized, perform normalization with cooler balance (ICE) to create bins/weight.
- **Verify normalization** and emit a concise report on the file, resolution, and normalization status.

---

## When to use this skill

Use the hic-normalization pipeline when:

- You need to ensure that Hi-C data is normalized for downstream analysis.
- Your data comes in .cool or .mcool formats, and you want to check or refresh normalization status (ICE normalization).

This tool assumes the file already has correct genome assembly and chromosome names.

---

## Inputs & Outputs

### Inputs

- Accepted file format: .mcool

### Outputs

```bash
${sample}_hic_norm/
    ${sample}_norm.mcool
    normalization_report.txt  # A brief log/report indicating which resolutions were detected, normalized, or skipped.
```
---

## Decision Tree

### Step 0 — Gather Required Information from the User

Before calling any tool, ask the user:

1. Sample name (`sample`): used as prefix and for the output directory `${sample}_hic_norm`.
2. Genome assembly (`genome`): e.g. `hg38`, `mm10`, `danRer11`.  
   - **Never** guess or auto-detect.
3. Hi-C matrix path (`mcool_path`): e.g. `.mcool` file path or `.hic` file path.
   - `path/to/sample.mcool` (.mcool file without resolution specified)
   - or `.hic` file path

---

### Step 1: Initialize Project

1. Make director for this project:

Call:
- `mcp__project-init-tools__project_init`

with:
- `sample`: the user-provided sample name
- `task`: hic_norm

The tool will:
- Create `${sample}_hic_norm` directory.
- Get the full path of the `${sample}_hic_norm` directory, which will be used as `${proj_dir}`.

---

2. If the user provides a `.hic` file, convert it to `.mcool` file first using `mcp__HiCExplorer-tools__hic_to_mcool` tool:

Call:
- `mcp__HiCExplorer-tools__hic_to_mcool`

with:
- `input_hic`: the user-provided path (e.g. `input.hic`)
- `sample`: the user-provided sample name
- `proj_dir`: directory to save the view file. In this skill, it is the full path of the `${sample}_hic_norm` directory returned by `mcp__project-init-tools__project_init`.
- `resolutions`: the user-provided resolutions (e.g. `[50000]`)

The tool will:
- Convert the `.hic` file to `.mcool` file.
- Return the path of the `.mcool` file.

If the conversion is successful, update `${mcool_uri}` to the path of the `.mcool` file. The `${mcool_path}` should be updated to the path of the `.mcool` file without resolution specified.

---

3. Inspect the `.mcool` file to list available resolutions and confirm the analysis resolution with the user.

Call:
- `mcp__cooler-tools__list_mcool_resolutions`

with:
- `mcool_path`: the user-provided path (e.g. `input.mcool`) or the path of the `.mcool` file returned by `mcp__HiCExplorer-tools__hic_to_mcool`

The tool will:
- List all resolutions in the .mcool file.
- Return the resolutions as a list.

---


### Step 2: Check Normalization Status (per resolution) on .mcool and normlize if missing

Call:
- `mcp__cooler-tools__check_and_balance_mcool`

with:
- `sample`: the user-provided sample name
- `proj_dir`: the full path to the project directory
- `mcool_path`: the path to the .mcool file (e.g. input.mcool) without resolution specified.
- `balance_missing`: if true, run `cooler.balance_cooler` on resolutions missing /bins/weight
- `store_name`: the name of the weight column to write into bins (default: 'weight')
- `ignore_diags`: the number of diagonals to ignore (`ignore_diags` in cooler.balance_cooler)
- `mad_max`: the `mad_max` parameter for cooler.balance_cooler (default: cooler's own)
- `converge`: the convergence tolerance, maps to `tol` in cooler.balance_cooler
- `max_iters`: the `max_iters` parameter for cooler.balance_cooler
- `cis_only`: if true, balance cis contacts only (`cis_only=True`)

The tool will:
- Check the normalization status (per resolution) on the .mcool file.
- If the normalization is missing, balance the .mcool file.
- Return the path of the balanced .mcool file under `${proj_dir}/` directory.


## Notes & Troubleshooting

- **Normalization fails to converge**: Increase iterations or adjust the convergence criteria (--max-iters, --converge)
