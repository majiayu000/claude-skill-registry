---
name: paperconfig
description: Create and validate paperconfig.yaml files for integrating omics publication data (RNA-seq, proteomics, metabolomics, microarray) into the knowledge graph. Use when adding a new paper's differential expression data.
argument-hint: [paper-directory-name]
user-invocable: true
allowed-tools: Read, Grep, Glob, Write, Edit, Bash(uv *), Bash(python *)
---

# Paperconfig YAML Instructions

How to create a `paperconfig.yaml` file for integrating omics publication data into the knowledge graph.

## Overview

Each publication with differential expression or omics data gets its own `paperconfig.yaml` file under `data/Prochlorococcus/papers_and_supp/<AuthorName Year>/`. This config tells the OMICSAdapter how to parse supplementary data tables and create knowledge graph nodes and edges.

## Directory Setup

1. Create a folder: `data/Prochlorococcus/papers_and_supp/<AuthorName Year>/`
2. Place the publication PDF in this folder
3. Place the supplementary data CSV file(s) in this folder (or a subfolder)
4. Create `paperconfig.yaml` in the same folder

## YAML Structure

A paperconfig has three top-level sections under `publication:`:

```yaml
publication:
  papername: "<Author Year>"
  papermainpdf: "data/Prochlorococcus/papers_and_supp/<AuthorName Year>/<filename>.pdf"

  environmental_conditions:
    # ... (optional, see below)

  supplementary_materials:
    # ... (required)
```

### 1. Publication Metadata (Required)

```yaml
publication:
  papername: "Author Year"
  papermainpdf: "data/Prochlorococcus/papers_and_supp/<folder>/<pdf_filename>.pdf"
```

- `papername`: Short citation label (e.g., "Biller 2016"). Used for display only.
- `papermainpdf`: Relative path to the publication PDF. The adapter extracts metadata (title, DOI, authors, abstract) from this PDF automatically using an LLM-based extractor.

### 2. Environmental Conditions (Optional)

Define environmental conditions when the experiment varies an environmental factor (light, gas, salinity, nutrients, growth state) rather than a biological organism. Each condition becomes a node in the knowledge graph and can be used as the **source** of `affects_expression_of` edges (instead of an organism).

```yaml
  environmental_conditions:
    <unique_condition_id>:
      condition_type: "<type>"    # e.g., gas_shock, salt_stress, light_stress, growth_medium, growth_state, coculture
      name: "<human-readable name>"
      description: "<detailed description of the condition>"
      # Include any relevant parameters:
      medium: "<growth medium>"
      temperature: "<temp>"
      light_condition: "<light type>"
      light_intensity: "<intensity>"
      # Gas-specific:
      co2_level: "<level>"
      oxygen_level: "<level>"
      # Salinity-specific:
      salinity: "<level>"
```

Rules:
- The `<unique_condition_id>` is a local key used to link conditions to analyses (via `environmental_treatment_condition_id` and `environmental_control_condition_id`).
- Use a naming convention: `<authorlastname>_<year>_<short_description>` (e.g., `bagby_2015_low_co2`).
- All property keys are stored as-is on the environmental_condition node.
- If the experiment compares organisms (e.g., coculture vs axenic), you may still define environmental conditions but they are not strictly required -- you can use `treatment_organism`/`treatment_taxid` on the analysis instead.

### 3. Supplementary Materials (Required)

Each supplementary table is a keyed entry containing a filename and one or more statistical analyses.

```yaml
  supplementary_materials:
    <table_key>:
      type: csv
      filename: "data/Prochlorococcus/papers_and_supp/<folder>/<data_file>.csv"
      statistical_analyses:
        - <analysis_1>
        - <analysis_2>
        # ... multiple analyses can reference the same file
```

- `<table_key>`: A descriptive key for the table (e.g., `supp_table_1`, `supp_table_2_timepoint_A`).
- `type`: Always `csv`.
- `filename`: Relative path to the data CSV file.
- Multiple analyses can share the same file if different columns represent different comparisons (e.g., different timepoints or conditions in the same spreadsheet).

### 4. Statistical Analysis Fields

Each analysis entry describes one differential expression comparison.

#### Required Fields

| Field | Description | Examples |
|-------|-------------|----------|
| `type` | Omics data type | `RNASEQ`, `MICROARRAY`, `PROTEOMICS`, `METABOLOMICS` |
| `name` | Human-readable description of the analysis | `"DE Analysis of Prochlorococcus MED4 coculture vs axenic at 20h"` |
| `id` | Unique identifier for this analysis | `DE_coculture_vs_axenic_med4_20h` |
| `test_type` | Statistical method used | `DESeq2`, `edgeR`, `Rockhopper`, `Affymetrix microarray`, `DESeq` |
| `control_condition` | Baseline/reference condition | `"Axenic"`, `"Time 0 (pre-shock)"`, `"Normal seawater (3.8% salt)"` |
| `treatment_condition` | Experimental/test condition | `"Coculture with Alteromonas HOT1A3"`, `"Salt-acclimated (5% salt)"` |
| `organism` | Organism being profiled | `"Prochlorococcus MED4"`, `"Alteromonas macleodii MIT1002"` |
| `name_col` | Column name in CSV containing the gene/protein identifier | `"Gene"`, `"Locus tag2"`, `"Gene ID"`, `"Synonym"`, `"ID"` |
| `logfc_col` | Column name in CSV containing the log2 fold change value | `"log2FoldChange"`, `"logFC"`, `"0.036%_CO2_21%_O2 FC"` |

#### Optional Fields

| Field | Description | When to Use |
|-------|-------------|-------------|
| `adjusted_p_value_col` | Column name for adjusted p-value | When the CSV has a p-value column (e.g., `"padj"`, `"FDR"`, `"q Value"`) |
| `experimental_context` | Other factors held constant | Always helpful; describes medium, light, temperature, etc. |
| `timepoint` | Time point of measurement | For time-course experiments (e.g., `"20h"`, `"48h"`, `"-12h"`, `"24h vs 12h"`) |
| `skip_rows` | Number of header rows to skip when reading CSV | When the CSV has extra header rows before the data columns (e.g., `3`) |
| `pvalue_asterisk_in_logfc` | Boolean, `true` if significance is marked by `*` appended to fold-change values | When there is no separate p-value column and the fold-change column has asterisks (e.g., `"2.5*"`) |
| `prefiltered` | Boolean, `true` if the table only contains significant results | When authors pre-filtered the table to significant genes only |
| `pvalue_threshold` | Adjusted p-value threshold used/stated in the publication (e.g., `0.05`) | When the paper states a specific significance cutoff |
| `logfc_threshold` | Absolute log2 fold-change threshold used/stated in the publication (e.g., `0.8`, `1.0`) | When the paper states a specific fold-change cutoff |

**Note on tables where all values are significant:** Some supplementary tables only list genes that are already significantly differentially expressed (pre-filtered by the authors). In these cases, set `prefiltered: true` on the analysis. This tells the adapter that all rows are significant. You may also omit `adjusted_p_value_col` and `pvalue_asterisk_in_logfc` if not applicable.

**Note on significance thresholds:** If the paper or table legend states specific significance criteria (e.g., "adjusted p-value < 0.05 and |log2FC| >= 1"), record these as `pvalue_threshold` and `logfc_threshold`. The adapter uses these to mark edges as significant or not. If the paper does not state thresholds, omit these fields — the adapter can apply default thresholds from its constructor settings.

#### Edge Source Fields (One Set Required)

The adapter needs to determine what **causes** the expression change. You must provide one of these two sets:

**Option A -- Organism as cause** (e.g., coculture experiments):

| Field | Description | Example |
|-------|-------------|---------|
| `treatment_organism` | Name of the organism causing the effect | `"Alteromonas macleodii HOT1A3"` |
| `treatment_taxid` | NCBI Taxonomy ID of the treatment organism | `28108` |

**Option B -- Environmental condition as cause** (e.g., stress experiments):

| Field | Description | Example |
|-------|-------------|---------|
| `environmental_treatment_condition_id` | References a key from `environmental_conditions` | `bagby_2015_low_co2` |
| `environmental_control_condition_id` | (Optional) References the control condition key | `alhosani_2015_seawater_control` |

If `environmental_treatment_condition_id` is present, the adapter uses the environmental condition node as the edge source. Otherwise it falls back to the organism node from `treatment_taxid`.

## Choosing Between Organism and Environmental Condition Edges

Use **organism edges** (`treatment_organism` + `treatment_taxid`) when:
- The experiment adds or removes a biological organism (e.g., coculture with a heterotroph, viral infection)
- The "cause" of expression change is the presence of another organism

Use **environmental condition edges** (`environmental_treatment_condition_id`) when:
- The experiment varies a physical or chemical factor (light, gas, salinity, nutrients, temperature)
- The experiment compares growth states or phases (planktonic vs biofilm, exponential vs stationary)
- You want the condition details (CO2 level, salinity, etc.) stored as a node with rich properties

## CSV Data File Requirements

- Must be a valid CSV file readable by pandas
- Must contain at minimum:
  - A column with gene/protein identifiers (referenced by `name_col`)
  - A column with log2 fold-change values (referenced by `logfc_col`)
- Optionally: a column with adjusted p-values (referenced by `adjusted_p_value_col`)
- Gene identifiers should ideally be locus tags or gene IDs that can be matched to existing gene nodes in the knowledge graph
- Rows with empty/NA gene identifiers or non-numeric fold-change values are automatically skipped

## Complete Examples

### Example 1: Coculture Experiment (Organism as Cause)

```yaml
publication:
  papername: "Aharonovich 2016"
  papermainpdf: "data/Prochlorococcus/papers_and_supp/Aharonovich 2016/paper.pdf"

  supplementary_materials:
    supp_table_1:
      type: csv
      filename: "data/Prochlorococcus/papers_and_supp/Aharonovich 2016/de_genes_med4_t20h.csv"
      statistical_analyses:
        - type: RNASEQ
          name: "DE of Prochlorococcus MED4 in Coculture with Alteromonas HOT1A3 vs Axenic at 20h"
          id: DE_coculture_vs_axenic_med4_20h
          test_type: Rockhopper
          control_condition: Axenic
          treatment_condition: "Coculture with Alteromonas HOT1A3"
          experimental_context: "in Pro99 medium under continuous light"
          timepoint: 20h
          organism: "Prochlorococcus MED4"
          treatment_taxid: 28108
          treatment_organism: "Alteromonas macleodii HOT1A3"
          name_col: Synonym
          logfc_col: "log 2 fold change coculture/axenic"
          adjusted_p_value_col: "q Value"
```

### Example 2: Environmental Stress (Condition as Cause)

```yaml
publication:
  papername: "Al-Hosani 2015"
  papermainpdf: "data/Prochlorococcus/papers_and_supp/Al-Hosani 2015/paper.pdf"

  environmental_conditions:
    alhosani_2015_seawater_control:
      condition_type: growth_medium
      name: "Normal seawater control (3.8% salt)"
      medium: "PRO99 natural seawater medium"
      temperature: 22C
      light_condition: continuous_light
      light_intensity: "46 umol photons m-2 s-1"
      salinity: "3.8% w/v NaCl"
      description: "Axenic Prochlorococcus AS9601 in PRO99 medium, normal salinity"
    alhosani_2015_salt_acclimation:
      condition_type: salt_stress
      name: "Salt-acclimated (5% salt)"
      medium: "PRO99 natural seawater medium with added NaCl"
      temperature: 22C
      light_condition: continuous_light
      light_intensity: "46 umol photons m-2 s-1"
      salinity: "5% w/v NaCl"
      description: "Axenic Prochlorococcus AS9601 acclimated to 5% NaCl"

  supplementary_materials:
    supp_table_3:
      type: csv
      filename: "data/Prochlorococcus/papers_and_supp/Al-Hosani 2015/de_genes_salt.csv"
      statistical_analyses:
        - type: RNASEQ
          name: "DE of Prochlorococcus AS9601 under salt acclimation vs normal seawater"
          id: DE_salt_acclimated_vs_seawater_AS9601
          test_type: DESeq
          control_condition: "Normal seawater (3.8% salt)"
          treatment_condition: "Salt-acclimated (5% salt)"
          environmental_control_condition_id: alhosani_2015_seawater_control
          environmental_treatment_condition_id: alhosani_2015_salt_acclimation
          experimental_context: "Axenic cells in PRO99 medium at 22C under continuous light"
          organism: "Prochlorococcus AS9601"
          name_col: "Gene id"
          logfc_col: log2FoldChange
          adjusted_p_value_col: padj
```

### Example 3: Multiple Analyses from One File (Time Course)

When a single CSV contains columns for multiple timepoints:

```yaml
  supplementary_materials:
    supp_table_2:
      type: csv
      filename: "data/.../PRO_DE_genes.csv"
      statistical_analyses:
        - type: RNASEQ
          name: "DE Prochlorococcus NATL2A coculture vs axenic (2h)"
          id: DE_coculture_vs_axenic_NATL2A_2h
          test_type: DESeq2
          control_condition: Axenic
          treatment_condition: "Co-culture with Alteromonas macleodii MIT1002"
          timepoint: 2h
          organism: "Prochlorococcus NATL2A"
          treatment_taxid: 28108
          treatment_organism: "Alteromonas macleodii MIT1002"
          name_col: Original_NCBI_ID
          logfc_col: "2 hours"
          skip_rows: 3
          pvalue_asterisk_in_logfc: true
        - type: RNASEQ
          name: "DE Prochlorococcus NATL2A coculture vs axenic (12h)"
          id: DE_coculture_vs_axenic_NATL2A_12h
          test_type: DESeq2
          control_condition: Axenic
          treatment_condition: "Co-culture with Alteromonas macleodii MIT1002"
          timepoint: 12h
          organism: "Prochlorococcus NATL2A"
          treatment_taxid: 28108
          treatment_organism: "Alteromonas macleodii MIT1002"
          name_col: Original_NCBI_ID
          logfc_col: "12 hours"
          skip_rows: 3
          pvalue_asterisk_in_logfc: true
```

### Example 4: Multiple Tables from Same Paper

When a paper has separate CSV files for different organisms or experiments:

```yaml
  supplementary_materials:
    supp_table_pro:
      type: csv
      filename: "data/.../pro_de_genes.csv"
      statistical_analyses:
        - type: RNASEQ
          # ... Prochlorococcus analysis
    supp_table_alt:
      type: csv
      filename: "data/.../alt_de_genes.csv"
      statistical_analyses:
        - type: RNASEQ
          # ... Alteromonas analysis
```

### Example 5: Environmental Stress with Multiple Biological Contexts in One File

When a single CSV has columns for different biological contexts (e.g., axenic and coculture) at multiple timepoints, all comparing the same environmental treatment vs control:

```yaml
publication:
  papername: "Biller 2018"
  papermainpdf: "data/Prochlorococcus/papers_and_supp/Biller 2018/paper.pdf"

  environmental_conditions:
    biller_2018_diel_ld_control:
      condition_type: growth_medium
      name: "13:11 diel light:dark cycle control"
      medium: Pro99 natural seawater medium
      temperature: 24C
      light_condition: "13:11 light:dark cycle with simulated dawn and dusk"
      light_intensity: "55 umol photons m-2 s-1"
      description: "Prochlorococcus NATL2A maintained under a 13:11 light:dark diel cycle"
    biller_2018_extended_darkness:
      condition_type: light_stress
      name: "Extended darkness"
      medium: Pro99 natural seawater medium
      temperature: 24C
      light_condition: continuous_darkness
      light_intensity: "0 umol photons m-2 s-1"
      description: "Cultures shifted to continuous darkness at expected sunrise"

  supplementary_materials:
    supp_table_s3:
      type: csv
      filename: "data/.../de_genes.csv"
      statistical_analyses:
        # Axenic condition at 1h
        - type: RNASEQ
          name: "DE Prochlorococcus NATL2A axenic in extended darkness vs diel (1h)"
          id: DE_extended_darkness_vs_diel_axenic_NATL2A_1h
          test_type: DESeq2
          control_condition: "13:11 diel light:dark cycle"
          treatment_condition: "Extended darkness"
          environmental_control_condition_id: biller_2018_diel_ld_control
          environmental_treatment_condition_id: biller_2018_extended_darkness
          experimental_context: "Axenic Prochlorococcus NATL2A in Pro99 at 24C"
          timepoint: "1h extended darkness"
          organism: Prochlorococcus NATL2A
          name_col: "NCBI ID"
          logfc_col: "Axenic, 36 hours"
          pvalue_asterisk_in_logfc: true
        # Coculture condition at 1h (same file, different logfc_col)
        - type: RNASEQ
          name: "DE Prochlorococcus NATL2A coculture in extended darkness vs diel (1h)"
          id: DE_extended_darkness_vs_diel_coculture_NATL2A_1h
          test_type: DESeq2
          control_condition: "13:11 diel light:dark cycle"
          treatment_condition: "Extended darkness"
          environmental_control_condition_id: biller_2018_diel_ld_control
          environmental_treatment_condition_id: biller_2018_extended_darkness
          experimental_context: "Prochlorococcus NATL2A co-cultured with Alteromonas macleodii MIT1002 in Pro99 at 24C"
          timepoint: "1h extended darkness"
          organism: Prochlorococcus NATL2A
          name_col: "NCBI ID"
          logfc_col: "Co-culture, 36 hours"
          pvalue_asterisk_in_logfc: true
        # ... repeat for additional timepoints
```

## Registration

After creating the paperconfig, register it in the pipeline:

1. Add the path to `data/Prochlorococcus/papers_and_supp/paperconfig_files.txt` (one path per line)
2. Or instantiate it directly in `create_knowledge_graph.py`:

```python
omics = OMICSAdapter(config_file="data/Prochlorococcus/papers_and_supp/<AuthorName Year>/paperconfig.yaml")
omics.download_data(cache=True)
bc.write_nodes(omics.get_nodes())
bc.write_edges(omics.get_edges())
```

## Validation Checklist

Before submitting a paperconfig:

- [ ] `papermainpdf` path points to an existing PDF file
- [ ] All `filename` paths point to existing CSV files
- [ ] `name_col` matches an actual column name in the CSV
- [ ] `logfc_col` matches an actual column name in the CSV
- [ ] `adjusted_p_value_col` (if specified) matches an actual column name in the CSV
- [ ] Each analysis has either (`treatment_organism` + `treatment_taxid`) or `environmental_treatment_condition_id`
- [ ] If using `environmental_treatment_condition_id`, the referenced key exists under `environmental_conditions`
- [ ] Each analysis `id` is unique within the file
- [ ] `skip_rows` is set correctly if the CSV has extra header rows
- [ ] Gene/protein identifiers in `name_col` use locus tags or IDs that can match existing gene nodes
- [ ] `prefiltered` is set to `true` if the table only contains significant results
- [ ] `pvalue_threshold` and `logfc_threshold` are set if the paper states specific significance criteria

## Workflow

When the user invokes this skill with a paper directory name (e.g., `/paperconfig "Author Year"`):

1. Look for the paper directory under `data/Prochlorococcus/papers_and_supp/$ARGUMENTS/`
2. List all files in that directory (PDF, CSV, XLSX, TXT, DOCX, etc.)
3. Read any legend/description text files first -- these explain what the supplementary tables contain (column meanings, significance criteria, experimental details)
4. Read the CSV file headers and a few sample rows to identify available columns and data format (check for asterisks in fold-change values, presence of p-value columns, skip rows, etc.)
5. Read the PDF to understand the experiment (organisms, conditions, methods, statistical approach)
6. Draft the `paperconfig.yaml` following the schema above
7. Run the validation script (see below) to check all paths, columns, references, and ID uniqueness
8. Register the config in `paperconfig_files.txt`

### Validation Script

After creating the paperconfig, always run the validation script:

```bash
uv run python .claude/skills/paperconfig/validate_paperconfig.py "data/Prochlorococcus/papers_and_supp/<Author Year>/paperconfig.yaml"
```

This script checks:
- YAML is parseable and has required top-level structure
- PDF file exists
- All CSV files exist and are readable
- Column names (`name_col`, `logfc_col`, `adjusted_p_value_col`) match actual CSV headers
- `skip_rows` is applied correctly when reading CSV headers
- Each analysis has all required fields (`type`, `name`, `id`, `test_type`, `control_condition`, `treatment_condition`, `organism`, `name_col`, `logfc_col`)
- Each analysis has either (`treatment_organism` + `treatment_taxid`) or `environmental_treatment_condition_id`
- Environmental condition ID references resolve to keys in `environmental_conditions`
- All analysis IDs are unique
- `logfc_col` values look numeric (warns on non-numeric values)
- `type` is one of: RNASEQ, MICROARRAY, PROTEOMICS, METABOLOMICS

The script exits with code 0 on success, 1 on validation failure.
