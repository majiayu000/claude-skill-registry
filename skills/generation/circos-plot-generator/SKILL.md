---
name: circos-plot-generator
description: Generate Circos configuration files for circular genomics data visualization. Supports genomic variations (SNPs, CNVs, structural variants), cell-cell communication networks, and custom track configurations for publication-ready circular plots. Generates configuration files only — rendering requires Circos installed separately.
license: MIT
skill-author: AIPOCH
status: beta
---

# Circos Plot Generator

Generate configuration files for Circos circular visualization plots, enabling genomics data visualization including genomic variations, chromosome ideograms, cell-cell communication networks, and custom track annotations.

**Key Capabilities:**
- **Genomic Variation Visualization**: SNPs, CNVs, structural variants (translocations, inversions)
- **Cell-Cell Communication Networks**: Intercellular interactions and signaling pathways
- **Chromosome Ideograms**: Chromosome structure with bands and annotations
- **Multiple Track Types**: Histograms, scatter plots, links, heatmaps, text tracks
- **Custom Tracks**: Histogram and link track types via `tracks` configuration key
- **Publication-Ready Output**: High-quality PNG/SVG figures

---

## Input Validation

This skill accepts: genomic variation data (TSV/CSV with chrom, start, end, type, value columns) or cell communication data (TSV with source, target, weight columns), plus optional configuration parameters.

**Rendering constraint:** This skill generates Circos configuration files only. Rendering requires Circos installed separately (`conda install -c bioconda circos`). This constraint applies to every invocation.

If the request does not involve generating a Circos configuration for genomic or cell communication data — for example, asking to perform variant calling, run statistical analysis, or create non-circular plots — do not proceed. Instead respond:
> "Circos Plot Generator is designed to generate Circos configuration files for circular genomics visualization. Please provide a data file (TSV/CSV) with genomic coordinates or cell communication data. For other visualization tasks, use a more appropriate tool."

---

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
```

## Workflow

1. Confirm the input data file, plot type (variation or cell-comm), and output parameters.
2. **Data size check:** If input data has >5,000 rows, proactively warn: "Large dataset detected (>5,000 rows) — rendering performance may degrade. Consider filtering for significance or increasing bin size before generating the config."
3. Validate that the request matches the documented scope; stop if the task requires unsupported assumptions.
4. Run the script or apply the documented configuration path with only the inputs available.
5. Return a structured result separating assumptions, deliverables, risks, and unresolved items.
6. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

**Fallback:** If `--data` is missing, respond: "Required parameter `--data` not provided. Please supply an input data file (TSV/CSV). Cannot generate Circos configuration without input data."

---

## Core Capabilities

### 1. Genomic Variation Track

```python
from scripts.main import CircosConfig
config = {
    "type": "variation",
    "title": "Sample Genomic Variations",
    "data": "variations.csv",
    "width": 1200, "height": 1200,
    "color_scheme": "nature",
    "output": "./circos_output"
}
generator = CircosConfig(config)
config_path = generator.generate()
```

**Input Data Format:**

| Column | Description | Example |
|--------|-------------|---------|
| `chrom` | Chromosome name | chr1, chrX |
| `start` | Start position | 1000000 |
| `end` | End position | 2000000 |
| `type` | Variation type | SNP, CNV, TRANSLOCATION |
| `value` | Score or magnitude | 0.5, -0.8 |

### 2. Cell-Cell Communication

```python
config = {
    "type": "cell-comm",
    "title": "Tumor Microenvironment Interactions",
    "data": "cell_communication.csv",
    "color_scheme": "cell",
    "output": "./cell_comm_plots"
}
```

**Input Format:**

| Column | Description | Example |
|--------|-------------|---------|
| `source` | Source cell type | T_Cell |
| `target` | Target cell type | Macrophage |
| `weight` | Interaction strength (0–1) | 0.8 |

### 3. Custom Tracks

The `custom` track type supports histogram and link tracks via the `tracks` configuration key:

```python
config = {
    "type": "custom",
    "tracks": [
        {"type": "histogram", "data": "expression.txt", "r0": "0.6r", "r1": "0.8r"},
        {"type": "link", "data": "links.txt", "color": "red"}
    ]
}
```

### 4. Color Schemes

| Scheme | Best For |
|--------|----------|
| **default** | Quick visualization, drafts |
| **nature** | Nature publications |
| **lancet** | Medical/clinical papers |
| **cell** | Cell biology papers |

---

## CLI Usage

```text
# Generate genomic variation Circos plot
python scripts/main.py --data variations.tsv --output genome.svg

# Cell communication plot with custom colors
python scripts/main.py --data cell_comm.tsv --type cell-communication --colors nature

# Custom radius
python scripts/main.py --data data.tsv --radius 500 --output large.svg
```

---

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--data` | string | **Yes** | Input data file (TSV/CSV) |
| `--output`, `-o` | string | No | Output SVG file path |
| `--type` | string | No | Plot type (variation, cell-communication, custom) |
| `--colors` | string | No | Color scheme (default, nature, lancet, cell) |
| `--radius` | float | No | Plot radius in pixels |

---

## Output Files

| File | Description |
|------|-------------|
| `circos.conf` | Main configuration |
| `data/karyotype.txt` | Chromosome definitions |
| `data/*.txt` | Track data files |
| `circos.png` | Raster image (if rendered) |
| `circos.svg` | Vector image (if rendered) |

> **Constraint:** This skill generates configuration files only. Rendering requires Circos installed separately (`conda install -c bioconda circos`). Always include this constraint in every response.

---

## Output Requirements

Every final response must make these explicit:

- Objective or requested deliverable
- Inputs used (data file, plot type, color scheme) and assumptions introduced
- Configuration generated and track layout
- Core result: config file path and rendering instructions
- **Constraints:** Rendering requires Circos installed separately (`conda install -c bioconda circos`). This skill generates configuration files only.
- Unresolved items and next-step checks

---

## Error Handling

- If `--data` is missing, state the missing parameter and request it. Do not proceed.
- If chromosome naming is inconsistent (chr1 vs 1), flag and request standardization.
- If input data has >5,000 rows, warn about rendering performance and suggest filtering.
- If `scripts/main.py` fails, report the failure point and provide manual configuration fallback.
- Do not fabricate configuration files or rendering outputs.

---

## Common Pitfalls

- **Inconsistent chromosome names**: Use consistent "chr" prefix (chr1, not 1)
- **Coordinates out of bounds**: Verify all positions ≤ chromosome size
- **Too many data points**: Filter for significance (>5,000 rows degrades rendering); increase bin size
- **Tracks overlap**: Adjust radius ranges; use transparency
- **Image too small**: Use minimum 1200×1200 for publications

---

## References

- Circos Official Documentation: http://circos.ca/documentation
- Circos Tutorials: http://circos.ca/documentation/tutorials
- Bioconda Circos: https://bioconda.github.io/recipes/circos/README.html
