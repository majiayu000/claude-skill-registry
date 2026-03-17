---
name: Proteomics
description: Proteomics analysis toolkit for label-free quantitative proteomics. Invokes R scripts for normalization, visualization (volcano, heatmap, PCA, LOPIT), pathway analysis (KEGG, ConsensusPathDB), and protein list cross-referencing (MISEV2018, SASP, Matrisome). USE WHEN user says 'analyze proteomics', 'volcano plot', 'normalize protein data', 'pathway enrichment', 'check EV markers', 'SASP analysis', 'matrisome', OR mentions q-value, fold-change, or protein quantification.
---

# Proteomics

Quantitative proteomics analysis toolkit combining R script invocation with embedded methodology knowledge. Fully portable - all scripts and reference data included.

**Skill Directory:** `~/.claude/Skills/Proteomics/`

---

## Workflow Routing

**When executing a workflow, output this notification:**

```
Running the **WorkflowName** workflow from the **Proteomics** skill...
```

| Workflow | Trigger | File |
|----------|---------|------|
| **Normalize** | "normalize data", "apply normalization", "median/quantile/loess normalize" | `workflows/Normalize.md` |
| **VolcanoPlot** | "volcano plot", "create volcano", "visualize fold change" | `workflows/VolcanoPlot.md` |
| **Heatmap** | "heatmap", "PCA", "correlation plot", "sample clustering" | `workflows/Heatmap.md` |
| **PathwayAnalysis** | "pathway analysis", "KEGG enrichment", "ConsensusPathDB", "GO enrichment" | `workflows/PathwayAnalysis.md` |
| **ProteinListQuery** | "check EV markers", "MISEV proteins", "exosome markers", "blood contaminants" | `workflows/ProteinListQuery.md` |
| **ExcelWorkup** | "create Excel report", "filter by q-value", "generate data tables" | `workflows/ExcelWorkup.md` |
| **Matrisome** | "matrisome analysis", "ECM proteins", "extracellular matrix" | `workflows/Matrisome.md` |
| **SaspAnalysis** | "SASP analysis", "senescence factors", "core SASP" | `workflows/SaspAnalysis.md` |

---

## Examples

**Example 1: Generate Volcano Plot**
```
User: "Create a volcano plot for my proteomics comparison data"
-> Invokes VolcanoPlot workflow
-> Asks for data file location and parameters (q-value, fold-change threshold)
-> Either invokes Plot_Workup_V10.R or generates custom ggplot2 code
-> Outputs TIFF files to output/ directory
```

**Example 2: Check for EV Markers**
```
User: "Which MISEV2018 EV markers are in my dataset?"
-> Invokes ProteinListQuery workflow
-> Reads user's protein list
-> Cross-references against data/MISEV2018_EV_Markers.txt
-> Returns categorized matches (Category 1-5, tetraspanins, annexins, etc.)
```

**Example 3: Full Analysis Pipeline**
```
User: "Run a complete proteomics analysis on my kidney data"
-> Sequences multiple workflows:
  1. Normalize (median normalization)
  2. Heatmap (PCA, sample correlation)
  3. VolcanoPlot (for each comparison)
  4. Matrisome (ECM protein analysis)
  5. SaspAnalysis (if relevant)
  6. ExcelWorkup (generate report)
-> Creates organized output/ directory structure
```

**Example 4: Pathway Enrichment**
```
User: "Run KEGG pathway analysis on my significantly altered proteins"
-> Invokes PathwayAnalysis workflow
-> Filters to q < 0.01, |log2FC| > 0.58
-> Runs clusterProfiler or ConsensusPathDB
-> Generates dotplot visualization
```

---

## R Script Quick Reference

All scripts are in the skill's `rscripts/` directory.

| Script | Purpose | Key Parameters |
|--------|---------|----------------|
| `Plot_Workup_V10.R` | Full visualization pipeline | `organism`, `batch`, `myFC`, `myQval`, `mypattern` |
| `Excel_Workup_v05.R` | Excel report generation | `myoutput`, `batch`, `myFC`, q-value flags |
| `normalization/Step_1_Normalization.R` | Data normalization | Input matrix (iMat) |
| `ConsensusPathDB_23_0411_v03.R` | Pathway dotplots | `input_dir`, `output_dir`, `q.val`, `t.level` |
| `toolkit.R` | Library loading | Called at start of analysis |
| `barplots.R` | Bar plot utility | Various |

---

## Standard Parameters

| Parameter | Typical Values | Description |
|-----------|---------------|-------------|
| q-value | 0.05, 0.01, 0.001 | Statistical significance threshold |
| Fold Change | 0.58 (1.5x), 1.0 (2x) | Log2 fold change cutoff |
| Organism | "human", "mouse" | Species for reference lists |
| Pattern | `"JB\\d_\\d+"` | Regex for sample ID extraction |

---

## Reference Data Available

All protein lists are in the skill's `data/` directory.

| List | File | Contents |
|------|------|----------|
| MISEV2018 EV Markers | `MISEV2018_EV_Markers.txt` | 500+ proteins, Category 1-5 |
| EV Categories | `MISEV2018_EV_Categories.txt` | Category definitions |
| Exosome Markers | `Exosome_Protein_Markers.txt` | CD63, CD81, CD9, TSG101, etc. |
| Blood Contaminants | `Top_10_Blood_Proteins.txt` | Albumin, IgG, fibrinogen, etc. |
| Apolipoproteins | `Apolipoproteins.txt` | APOA1, APOB, etc. |
| Human Core SASP | `Human_Core_SASP.csv` | 175 SASP factors with IR/RAS/ATV scores |
| Mouse Core SASP | `Mouse_Core_SASP.csv` | Mouse SASP orthologs |
| Human Matrisome | `matrisome_hs_masterlist.csv` | ECM proteins by category |
| Mouse Matrisome | `matrisome_mm_masterlist.csv` | Mouse ECM proteins |

---

## Required Data Structure

For running the full analysis scripts, data should be organized as:

```
[PROJECT_DIR]/
├── data/
│   ├── [batch]_Protein_Report_2pep.csv    # Protein intensities
│   ├── [batch]_candidates_2pep.csv         # Comparison results
│   └── [batch]_ConditionSetup.csv          # Sample metadata
└── output/
    ├── Data_Tables/                        # Excel reports
    └── [plots will be saved here]
```

---

## Invocation Pattern

**To run R scripts from this skill:**
```bash
cd [PROJECT_WORKING_DIR]
Rscript ~/.claude/Skills/Proteomics/rscripts/[SCRIPT_NAME].R
```

**Important:** Scripts expect:
1. Working directory set to project folder
2. `data/` subdirectory with input files
3. `output/` subdirectory for results
4. Reference data paths point to skill's `data/` directory (may need adjustment)

---

## When NOT to Use This Skill

- General R coding questions -> Use standard Claude
- Non-proteomics data analysis -> Use appropriate tools
- Genomics/transcriptomics -> Different methodology
- Statistical consulting without data -> Explain methodology, don't run
