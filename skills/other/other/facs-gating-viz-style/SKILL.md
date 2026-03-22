---
name: facs-gating-viz-style
description: Beautify flow cytometry gating plots for publication. Applies contour, density, or dot plot styles to FCS data and produces publication-ready figures with consistent formatting.
license: MIT
skill-author: AIPOCH
status: beta
---
# FACS Gating Viz Style

Apply publication-ready styling to flow cytometry gating plots. Accepts FCS data files and produces contour, density, or dot plot visualizations formatted for journal submission.

> ✅ **IMPLEMENTED** — `scripts/main.py` is fully functional. fcsparser/flowio FCS parsing, scatter/density/contour plots, file validation, and `--demo` mode are all implemented.

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
python scripts/main.py --demo --output demo.png
```

## When to Use

- Reformatting flow cytometry gating plots for publication figures
- Applying consistent visual style across multiple FCS datasets
- Generating contour, density, or dot plot variants from the same data

## Workflow

1. Confirm the user objective, required inputs, and non-negotiable constraints before doing detailed work.
2. Validate that the request matches the documented scope and stop early if the task would require unsupported assumptions.
3. Use the packaged script path or the documented reasoning path with only the inputs that are actually available.
4. Return a structured result that separates assumptions, deliverables, risks, and unresolved items.
5. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

**Fallback template:** If `scripts/main.py` fails or the FCS file is unreadable, report: (a) the failure point, (b) which plot styles are still generatable from available data, (c) manual steps to export a plot using FlowJo or equivalent.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--input`, `-i` | string | Yes* | FCS file path |
| `--output`, `-o` | string | No | Output file path (default: `output.png`) |
| `--x-channel` | string | No | X axis channel name (default: `FSC-A`) |
| `--y-channel` | string | No | Y axis channel name (default: `SSC-A`) |
| `--style`, `-s` | string | No | Plot style: `scatter`, `density`, `contour` (default: `scatter`) |
| `--demo` | flag | No | Generate synthetic FSC/SSC data — no FCS file required |

*Required unless `--demo` is used.

## Usage

```text
python scripts/main.py --input sample.fcs --style contour
python scripts/main.py --input sample.fcs --style density --output figure1.png
python scripts/main.py --input sample.fcs --x-channel CD4 --y-channel CD8 --style scatter
python scripts/main.py --demo --style contour --output demo_plot.png
```

## Implementation Notes (for script developer)

The script must implement:

1. **File validation** — before processing, check `os.path.exists(data_path)`. If missing or empty string: print `Error: File not found: {data_path}` to stderr and exit with code 1.
2. **FCS parsing** — use `fcsparser` (supports FCS 2.0–3.1) or `flowio` (supports FCS 3.0+) to read FCS files and extract channel data. For FCS versions not supported by either library, instruct the user to export to CSV from FlowJo.
3. **Plot generation** — use `matplotlib`/`seaborn` to generate:
   - `contour`: 2D KDE contour plot of FSC vs SSC (or user-specified channels)
   - `density`: smooth kernel density estimate heatmap
   - `dot`: scatter plot with publication-appropriate point sizing and alpha
4. **Output file** — save to `--output` path (default `output.png`). Print the output path to stdout for agent consumption.
5. **`--demo` flag** — generate synthetic bivariate normal data mimicking FSC/SSC scatter and run the full visualization pipeline without requiring a real FCS file.

## Known Limitations

- `fcsparser` supports FCS 2.0–3.1; `flowio` supports FCS 3.0+. For older FCS 2.0 files not parsed by `flowio`, use `fcsparser` as the primary parser.
- For FCS files with non-standard channel names, the script defaults to the first two channels for FSC/SSC axes.

## Features

- Contour plots with configurable density levels
- Density visualization with smooth kernel estimation
- Dot plots with publication-appropriate point sizing
- Consistent axis labeling and font sizing for journal figures
- Demo mode for offline testing and CI validation (`--demo`)

## Output Requirements

Every response must make these explicit:

- Objective and deliverable
- Inputs used and assumptions introduced
- Workflow or decision path taken
- Core result: styled plot file path
- Constraints, risks, caveats (e.g., FCS version compatibility, channel naming)
- Unresolved items and next-step checks

## Input Validation

This skill accepts: FCS data files for flow cytometry gating plot styling.

If the request does not involve flow cytometry visualization — for example, asking to analyze gating strategy logic, perform statistical comparisons between populations, or process non-FCS file formats — do not proceed. Instead respond:

> "`facs-gating-viz-style` is designed to apply publication-ready styling to flow cytometry gating plots. Your request appears to be outside this scope. Please provide an FCS file and desired plot style, or use a more appropriate tool for your task."

## Error Handling

- If `--data` is missing (and `--demo` not set), state that the FCS file path is required.
- If the FCS file path is empty or does not exist, print `Error: File not found: {path}` to stderr and exit with code 1.
- If `--style` is not one of `contour`, `density`, `dot`, reject with a clear error listing valid options.
- If the task goes outside the documented scope, stop instead of guessing or silently widening the assignment.
- If `scripts/main.py` fails, report the failure point, summarize what still can be completed safely, and provide a manual fallback.
- Do not fabricate files, citations, data, search results, or execution outcomes.

## Response Template

1. Objective
2. Inputs Received
3. Assumptions
4. Workflow
5. Deliverable
6. Risks and Limits
7. Next Checks
