---
name: bioinformatician
description: Use when implementing data analysis pipelines, statistical tests, or bioinformatics workflows in code (Python/R), particularly for genomics, transcriptomics, proteomics, or other -omics data.
success_criteria:
  - Notebook runs end-to-end without errors
  - All visualizations properly labeled with units and legends
  - Session info documented for reproducibility
  - Biological sanity checks completed and documented
  - Code reviewed by copilot with no critical issues
  - Results match expectations from analysis plan
metadata:
    skill-author: David Angeles Albores
    category: bioinformatics-workflow
    workflow: notebook-analysis
    integrates-with: [principal-investigator, copilot, scanpy, pydeseq2, biopython]
allowed-tools: [Read, Write, Edit, Bash, Skill, NotebookEdit]
---

# Bioinformatician Skill

## Purpose

Implement computational analyses of biological data, including:
- Data loading and quality control
- Statistical analysis
- Bioinformatics pipelines
- Visualization
- Integration with domain-specific tools

## When to Use This Skill

Use this skill when you need to:
- Implement an analysis plan in code (from PI)
- Process genomics/transcriptomics/proteomics data
- Perform statistical tests on biological data
- Create publication-quality visualizations
- Build reproducible analysis pipelines
- Integrate multiple bioinformatics tools

## Workflow Integration

**Primary Pattern: Receive Plan → Implement → Deliver Notebook**
```
Receive analysis_plan.md from PI
    ↓
Implement in Jupyter notebook
    ↓  (copilot reviews continuously)
Deliver completed notebook to PI for interpretation
```

**Integration Points**:
- RECEIVES: Analysis plan from `principal-investigator`
- WORKS WITH: `copilot` (adversarial code review during implementation)
- CALLS: Domain-specific skills (`scanpy`, `pydeseq2`, `biopython`, etc.)
- OUTPUTS: Jupyter notebooks with analysis code + results

## Core Capabilities

### 1. Data Loading and Validation
- Read common formats (CSV, TSV, HDF5, Parquet, FASTQ, BAM, VCF)
- Validate data integrity and format
- Handle compressed files
- Memory-efficient loading for large datasets

### 2. Quality Control
- Sample quality metrics
- Outlier detection
- Batch effect assessment
- Positive/negative control validation

### 3. Statistical Analysis
- Differential expression/abundance
- Enrichment analysis
- Clustering and dimensionality reduction
- Correlation and regression
- Multiple testing correction

### 4. Visualization
- Publication-quality plots (matplotlib, seaborn, plotly)
- Interactive visualizations
- Consistent styling
- Proper labeling and legends

### 5. Pipeline Development
- Modular, reusable code
- Parameter documentation
- Progress logging
- Error handling

## Standard Notebook Structure

Use the template in `assets/notebook_structure_template.ipynb`:

```
1. Title and Description
   - Research question
   - Date, author
   - Reference to analysis plan

2. Setup
   - Imports
   - Configuration parameters
   - Random seeds for reproducibility

3. Data Loading
   - Read data files
   - Initial inspection
   - Data structure validation

4. Quality Control
   - Sample metrics
   - Filtering criteria
   - QC visualizations

5. Analysis
   - Statistical tests
   - Transformations
   - Model fitting

6. Visualization
   - Main figures
   - Supplementary plots

7. Export Results
   - Save processed data
   - Export figures
   - Summary statistics

8. Session Info
   - Package versions
   - Execution time
```

## Biological Literacy Framework

### Writing Style for Biological Context

All biological context in notebooks should follow **concise scientific prose**:

**Principles**:
- ✅ **Brief**: 1-3 sentences per section, not paragraphs
- ✅ **Clear**: Use precise biological terminology
- ✅ **Factual**: State what/why without excessive detail
- ✅ **Publication-ready**: Like Methods/Results sections in papers

**Example - Good (Concise)**:
```markdown
## Biological Context
Differential expression analysis comparing wild-type and mutant neurons identifies genes affected by loss of transcription factor X. Expected upregulation of target genes based on ChIP-seq data (Smith et al. 2020).
```

**Example - Avoid (Too Verbose)**:
```markdown
## Biological Context
In this analysis, we will perform differential expression analysis to compare gene expression between wild-type neurons and neurons with a mutation in transcription factor X. Previous research has shown that transcription factor X plays a critical role in neuronal development by binding to the promoters of many developmentally important genes...
```

### When to Provide Interpretation vs Handoff

**Bioinformatician Handles** (routine interpretation):
- Standard results following known biology
- Positive/negative controls behaving as expected
- Results matching literature precedents
- Technical QC assessments with biological implications
- Magnitude/direction sanity checks

**Handoff to Biologist-Commentator** (expert needed):
- Novel or unexpected findings
- Results contradicting established biology
- Unclear biological mechanisms
- Publication-critical interpretations
- Proposing new hypotheses or models

## Enhanced Notebook Structure

Use this structure for biologically-literate notebooks:

```
1. Title and Scientific Context
   - Research question (biological, not just technical)
   - Biological hypothesis
   - Expected outcome and why it matters
   - Relevant background (1-2 sentences)

2. Setup (code)
   - Imports, parameters, seeds

3. Data Loading
   - Code: Load data
   - Biological description of dataset (markdown):
     * What organism/tissue/condition
     * What genes/features measured
     * What biological question dataset addresses

4. Quality Control
   - Code: QC metrics, filtering
   - Biological interpretation of QC (markdown):
     * Are pass rates expected for this data type?
     * Do failed samples have biological meaning?
     * Red flags from biological perspective?

5. Analysis
   - Code: Statistical tests, transformations
   - Biological reasoning for each step (markdown):
     * Why this method for this question?
     * What biological assumption being tested?
     * Positive/negative controls?

6. Results
   - Code: Generate results
   - Biological sanity checks (markdown):
     * Do magnitudes make sense?
     * Do directions align with biology?
     * Any known biology violated?

7. Visualization
   - Code: Plots
   - Biological interpretation scaffolding (markdown):
     * What biological pattern does this show?
     * Is this expected or surprising?
     * What follow-up questions does this raise?

8. Preliminary Interpretation
   - Bioinformatician's biological assessment (markdown):
     * Main findings in biological terms
     * Caveats and limitations
     * Questions for biologist-commentator

9. Handoff to Expert (if needed)
   - Structured questions for biologist-commentator (markdown):
     * Specific results needing interpretation
     * Unexpected findings to validate
     * Biological mechanisms to explore

10. Export (code)
    - Save data, figures, session info
```

## Biological Sanity Check Framework

Run these checks before accepting results:

### Expression/Abundance Checks
- [ ] Order of magnitude reasonable? (log2FC > 10 is suspicious)
- [ ] Direction matches known biology? (check a few known genes)
- [ ] Positive controls behave as expected?
- [ ] Negative controls show no signal?

### Statistical Checks with Biological Lens
- [ ] Top hits include known biology? (literature validation)
- [ ] Results robust to threshold changes?
- [ ] Batch effects vs real biology separated?
- [ ] Multiple testing appropriate for biology? (discovery vs validation)

### Genomics-Specific
- [ ] Chromosome names consistent? (chr1 vs 1)
- [ ] Coordinates sensible? (within chromosome bounds)
- [ ] Strand orientation correct for gene features?
- [ ] Genome build consistent throughout?

### Experimental Design
- [ ] Sample size adequate for this effect size?
- [ ] Replicates biological or technical?
- [ ] Confounders identified and addressed?
- [ ] Controls appropriate for this experiment type?

**If any check fails**: Document in notebook, flag for biologist-commentator review

## Biological Context Templates

### Template: Differential Expression Analysis

```markdown
## Biological Context
Comparing [condition A] vs [condition B] to identify genes involved in [biological process]. Expected upregulation of [pathway X] genes based on [mechanism/literature]. Positive controls: [gene1, gene2]. Expected log2FC range: [X-Y] based on [citation].

## Biological Sanity Checks
- [ ] Known pathway genes show expected direction (e.g., gene1 ↑, gene2 ↓)
- [ ] Housekeepers unchanged (actb, gapdh)
- [ ] Magnitudes reasonable (log2FC < 10 for transcriptional regulation)

## Preliminary Interpretation
Top hits include [gene X, Y, Z] involved in [biological process], consistent with [hypothesis/literature]. [Gene W] unexpected - requires expert validation.

**Handoff**: Unexpected downregulation of [gene W] contradicts known role in [process]. Biologist-commentator needed for mechanism assessment.
```

### Template: Single-Cell Clustering

```markdown
## Biological Context
Clustering [tissue] cells to identify cell types. Expected populations: [celltype1 (markers: a,b,c), celltype2 (markers: d,e,f)]. Reference atlas: [citation if available].

## Cluster Validation
- Cluster 1: [celltype] - markers: [genes] ✓
- Cluster 2: [celltype] - markers: [genes] ✓
- Cluster 3: Novel population - markers: [genes] - needs expert review

**Handoff**: Cluster 3 shows unexpected marker combination [X+Y+Z-]. Biologist-commentator needed for cell type identification and biological significance.
```

### Template: Expert Handoff Format

Use this concise format when escalating to biologist-commentator:

```markdown
## Expert Interpretation Needed

**Finding**: [Specific result with statistics]
**Context**: [1-2 sentence background]
**Issue**: [What's unexpected/unclear and why]
**Question**: [Specific question for expert]

**Validation Done**: [Positive controls: ✓/✗, Literature: consistent/contradicts]
```

**Example**:
```markdown
## Expert Interpretation Needed

**Finding**: Gene X shows 8-fold upregulation (padj<0.001) in mutant vs WT
**Context**: Gene X is transcriptional repressor, expected downregulation of targets
**Issue**: Target genes also upregulated (contradicts repressor function)
**Question**: Alternative mechanism? Post-transcriptional regulation? Data artifact?

**Validation Done**: Positive controls ✓, replicates consistent ✓, literature shows conflicting results
```

## Biologist-Commentator Integration Pattern

### When to Invoke Biologist-Commentator

**Pre-Analysis** (Method Validation):
```python
Skill(skill="biologist-commentator", args="Validate that DESeq2 appropriate for [specific experiment design]. Confirm controls adequate and confounders addressed.")
```

**During Analysis** (Quick Check):
- Use biological sanity check framework (above)
- Document any red flags
- Continue if checks pass, escalate if fail

**Post-Analysis** (Expert Interpretation):
```python
Skill(skill="biologist-commentator", args="Interpret biological significance of [specific finding]. Results show [X], which is [expected/unexpected]. Known biology suggests [Y]. Please validate interpretation and suggest mechanisms.")
```

### Handoff Workflow

1. **Bioinformatician**: Run analysis, perform sanity checks, document findings
2. **Handoff**: Create structured handoff section in notebook (see template above)
3. **Biologist-Commentator**: Provides expert interpretation, mechanism insights, validation
4. **Bioinformatician**: Incorporate interpretation into notebook, flag needed validations

## Pre-Flight Checklist

Before starting implementation, verify:
- [ ] Analysis plan clearly defines objectives
- [ ] Data files exist and paths are correct
- [ ] Required packages installed
- [ ] Expected output format understood
- [ ] Random seeds set for reproducibility

Use `assets/analysis_checklist.md` for complete list.

## Reproducibility Standards

**Critical**: Every bioinformatics analysis must be fully reproducible. Another researcher should be able to recreate your computational environment and obtain identical results.

### Environment Documentation (Mandatory)

**Start every notebook with environment documentation:**

```python
# %%
# Computational Environment
import sys
import numpy as np
import pandas as pd
import scanpy as sc  # or relevant packages

print("=" * 60)
print("COMPUTATIONAL ENVIRONMENT")
print("=" * 60)
print(f"Python: {sys.version}")
print(f"NumPy: {np.__version__}")
print(f"Pandas: {pd.__version__}")
print(f"Scanpy: {sc.__version__}")  # Replace with your key packages
print("=" * 60)
print("\nFor full environment, see requirements.txt")
```

**Create environment files before starting analysis:**

```bash
# For conda users (recommended for bioinformatics):
conda env export > environment.yml

# For pip users:
pip freeze > requirements.txt

# Document which file to use in notebook
```

**In notebook markdown cell:**
```markdown
## Computational Environment

- **Kernel**: Python 3.11 (bio-analysis-env)
- **Environment file**: `environment.yml` (recreate with `conda env create -f environment.yml`)
- **Key packages**: scanpy==1.10.0, numpy==1.26.3, pandas==2.2.0, scipy==1.12.0
- **Execution date**: 2026-01-29
```

### Random Seed Setting (Mandatory for Stochastic Processes)

**Set seeds in setup cell:**

```python
# %%
# Random seeds for reproducibility
import numpy as np
import random

RANDOM_SEED = 42  # Document choice (convention, replicating published analysis, etc.)

# Core Python/NumPy
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

# Scanpy (single-cell analysis)
import scanpy as sc
sc.settings.seed = RANDOM_SEED

# PyTorch (if using deep learning)
import torch
torch.manual_seed(RANDOM_SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(RANDOM_SEED)

# TensorFlow (if using)
import tensorflow as tf
tf.random.set_seed(RANDOM_SEED)

print(f"Random seed set to {RANDOM_SEED} for reproducibility")
```

**Bioinformatics operations requiring seeds:**
- **Dimensionality reduction**: UMAP, t-SNE, PCA with randomized SVD
- **Clustering**: Leiden, Louvain (graph-based)
- **Sampling**: Random subsampling, bootstrap, cross-validation
- **Imputation**: Stochastic imputation methods
- **Simulation**: Monte Carlo, permutation tests
- **Machine learning**: Random forests, neural networks, k-means initialization

**Document in notebook:**
```markdown
## Stochastic Operations
This analysis uses:
- UMAP (random initialization, seed=42)
- Leiden clustering (random walk, seed=42)
- 1000-iteration permutation test (seed=42)

All seeds set to 42 for reproducibility.
```

### Session Info Output (Mandatory)

**End every notebook with comprehensive session info:**

```python
# %%
# Session Information for Reproducibility
import session_info

session_info.show(
    dependencies=True,
    html=False
)

# Alternative for single-cell workflows:
# import scanpy as sc
# sc.logging.print_versions()

# Alternative for base Python:
# import sys
# import pkg_resources
# print(f"Python: {sys.version}")
# for pkg in ['numpy', 'pandas', 'scipy', 'matplotlib', 'seaborn']:
#     print(f"{pkg}: {pkg_resources.get_distribution(pkg).version}")
```

**What this captures:**
- Python version
- Operating system
- All package versions (including dependencies)
- Execution timestamp

**Why this matters:**
- API changes between package versions
- Statistical method implementations evolve
- Bugs get fixed (results may change)
- Reviewers need to verify methods

### File Path Best Practices

**Use relative paths and variables:**

```python
# %%
from pathlib import Path

# Define all paths at top of notebook
DATA_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
RESULTS_DIR = Path("results/analysis_2026-01-29")
FIGURES_DIR = RESULTS_DIR / "figures"

# Create output directories
for directory in [PROCESSED_DIR, RESULTS_DIR, FIGURES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Use variables throughout
counts_file = DATA_DIR / "counts_matrix.h5ad"
metadata_file = DATA_DIR / "sample_metadata.csv"
output_file = PROCESSED_DIR / "normalized_counts.h5ad"
figure_file = FIGURES_DIR / "umap_clusters.pdf"

print(f"Data directory: {DATA_DIR.resolve()}")
print(f"Results directory: {RESULTS_DIR.resolve()}")
```

**Never use hardcoded absolute paths:**
```python
# ❌ BAD (non-reproducible):
adata = sc.read_h5ad("/Users/yourname/project/data/counts.h5ad")
plt.savefig("/Users/yourname/Desktop/figure.pdf")

# ✅ GOOD (reproducible):
adata = sc.read_h5ad(DATA_DIR / "counts.h5ad")
plt.savefig(FIGURES_DIR / "umap_clusters.pdf")
```

### Data Provenance Documentation

**Document data sources in notebook:**

```markdown
## Data Sources

### Input Data
- **File**: `data/raw/GSE123456_counts.h5ad`
- **Source**: GEO accession GSE123456
- **Download date**: 2026-01-15
- **Download command**: `wget https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE123456`
- **Original publication**: Smith et al. (2025) Nature 600:123-130
- **Organism**: Homo sapiens
- **Tissue**: Primary cortical neurons
- **n samples**: 50 (25 control, 25 treatment)
- **n features**: 20,000 genes

### Reference Data
- **Genome build**: GRCh38 (hg38)
- **Gene annotations**: GENCODE v42
- **Downloaded**: 2026-01-10 from https://www.gencodegenes.org/
```

**Why this matters:**
- Data can be updated or removed from repositories
- Genome builds affect coordinate-based analyses
- Sample metadata clarifies experimental design
- Enables others to download identical data

### Reproducibility Pre-Flight Checklist

**Before starting analysis, verify:**
- [ ] Environment documented (`environment.yml` or `requirements.txt` exists)
- [ ] Environment creation documented in notebook
- [ ] Random seeds will be set for all stochastic operations
- [ ] File paths use variables (no hardcoded absolute paths)
- [ ] Data sources documented (where to download, version, date)
- [ ] Genome build / reference database versions specified
- [ ] Session info cell will be added at end

**Before handoff to PI, verify:**
- [ ] Notebook runs end-to-end without errors (Restart Kernel & Run All)
- [ ] Results reproducible (run twice, identical outputs)
- [ ] All figures saved to `FIGURES_DIR` with descriptive names
- [ ] All processed data saved to `PROCESSED_DIR`
- [ ] Session info cell executed and output visible
- [ ] Execution time reasonable (< 2 hours for routine analyses)

### Integration with notebook-writer Skill

When creating notebooks programmatically, use `notebook-writer` skill with reproducibility standards:

```python
from pathlib import Path

# Use notebook-writer to create template
cells = [
    {'type': 'markdown', 'content': '## Computational Environment\n...'},
    {'type': 'code', 'content': 'import sys\nprint(f"Python: {sys.version}")'},
    {'type': 'markdown', 'content': '## Data Loading\n...'},
    # ... analysis cells ...
    {'type': 'markdown', 'content': '## Session Info'},
    {'type': 'code', 'content': 'import session_info\nsession_info.show()'}
]

# Create reproducible notebook
notebook_path = create_notebook_markdown(
    title="Reproducible RNA-seq Analysis",
    cells=cells,
    output_path=Path("analysis/rnaseq_analysis.md")
)
```

### Common Reproducibility Failures and Fixes

| Issue | Problem | Fix |
|-------|---------|-----|
| **Different results on rerun** | No random seed set | Set seeds for numpy, random, scanpy, torch |
| **Import errors** | Missing package versions | Create `requirements.txt` or `environment.yml` |
| **File not found** | Hardcoded paths | Use Path variables defined at top |
| **Old package behavior** | Package version mismatch | Document versions with `session_info.show()` |
| **Data source vanished** | URL changed or removed | Document download date, accession, mirror sites |
| **Genome coordinate mismatch** | Different genome build | Specify build (GRCh38 vs GRCh37) in notebook |

### Bioinformatics-Specific Reproducibility Considerations

**Organism and Reference Versions:**
```python
# Document in code cell
ORGANISM = "Homo sapiens"
GENOME_BUILD = "GRCh38"  # or "mm39" for mouse, "dm6" for fly, etc.
ANNOTATION_VERSION = "GENCODE v42"  # or "Ensembl 110"
ANNOTATION_DATE = "2026-01-10"

print(f"Analysis configuration:")
print(f"  Organism: {ORGANISM}")
print(f"  Genome: {GENOME_BUILD}")
print(f"  Annotations: {ANNOTATION_VERSION} ({ANNOTATION_DATE})")
```

**Bioinformatics Tools (if used):**
```markdown
## External Tools
- **STAR aligner**: v2.7.11a (for read mapping)
- **MACS2**: v2.2.9.1 (for peak calling)
- **bedtools**: v2.31.0 (for interval operations)

All tools available in conda environment (see environment.yml).
```

**Data Processing Parameters:**
```python
# Document all filtering/QC thresholds
QC_PARAMS = {
    'min_genes_per_cell': 200,
    'min_cells_per_gene': 3,
    'max_pct_mt': 15,  # percent mitochondrial reads
    'min_counts': 1000,
    'highly_variable_genes': 2000,
    'n_pcs': 50,  # principal components
    'umap_neighbors': 15,
    'leiden_resolution': 0.8
}

print("Quality control parameters:")
for param, value in QC_PARAMS.items():
    print(f"  {param}: {value}")
```

## Code Quality Standards

### During Implementation
- **Copilot reviews continuously** - expect adversarial feedback
- Write clear comments explaining biological context
- Use descriptive variable names
- Modularize repeated operations into functions
- Log progress for long-running analyses

### Testing
- Validate on small test data first
- Check edge cases (empty data, single sample, all zeros)
- Compare to expected results (positive controls)
- Verify reproducibility (run twice, same results)

## Common Analysis Patterns

### Pattern 1: Differential Expression (RNA-seq)
```python
# 1. Load counts
# 2. Filter low-abundance genes
# 3. Normalize (DESeq2, TMM, or library size)
# 4. Statistical test (DESeq2, edgeR, limma)
# 5. Multiple testing correction
# 6. Volcano plot + heatmap
```
→ Use `pydeseq2` skill for implementation details

### Pattern 2: Single-Cell Analysis
```python
# 1. Load AnnData object
# 2. QC filtering (cells and genes)
# 3. Normalization and log-transform
# 4. Feature selection (highly variable genes)
# 5. Dimensionality reduction (PCA, UMAP)
# 6. Clustering
# 7. Marker gene identification
# 8. Visualization
```
→ Use `scanpy` skill for implementation details

### Pattern 3: Sequence Analysis
```python
# 1. Read FASTA/FASTQ
# 2. Quality filtering
# 3. Alignment or motif search
# 4. Feature extraction
# 5. Statistical summary
```
→ Use `biopython` skill for implementation details

## References

For detailed guidance:
- `references/analysis_workflows.md` - Step-by-step workflows for common analyses
- `references/data_structures.md` - When to use pandas/anndata/Bioconductor
- `references/statistical_methods.md` - Which test for which data
- `references/visualization_best_practices.md` - Plot selection and styling

## Helper Scripts

Available in `scripts/`:
- `qc_pipeline.py` - Automated QC for RNA-seq data
- `differential_expression_template.py` - Complete DESeq2 pipeline
- `data_loader_helpers.py` - Functions for common file formats

**Usage**: Read these scripts as reference implementations, copy/adapt for your specific analysis, or call directly via Bash if appropriate.

## Integration with Domain Skills

When analysis requires specialized knowledge:

| Data Type | Primary Skill | When to Use |
|-----------|---------------|-------------|
| Single-cell RNA-seq | `scanpy` | Cell type identification, clustering, trajectory |
| Bulk RNA-seq | `pydeseq2` | Differential gene expression |
| Sequences | `biopython` | Alignment, motif search, format conversion |
| Statistical modeling | `statsmodels` | Regression, time series, GLMs |
| Pathway analysis | `gseapy` or manual | Gene set enrichment |

**Pattern**:
1. Use `bioinformatician` for overall workflow
2. Invoke specialized skill for domain-specific steps
3. Integrate results back into main analysis

## Copilot Review Integration

During implementation, `copilot` skill reviews your code:
- Expect critical feedback (adversarial but constructive)
- Fix issues immediately before proceeding
- Iterate until code is robust
- Don't take criticism personally - it catches bugs early

## Deliverables

Complete notebook should include:

**Technical Components** (existing):
1. **Code cells**: Well-commented, modular analysis
2. **Visualizations**: Publication-ready figures
3. **Statistics**: Complete reporting (test, p-value, effect size, n)
4. **Exports**: Processed data files, figure files
5. **Session info**: Package versions for reproducibility

**Biological Components** (new):
6. **Biological Context Cells** (markdown):
   - Research question in biological terms
   - Hypothesis and expected outcomes
   - Biological description of each analysis step
   - Relevance to biological question

7. **Sanity Check Documentation** (markdown):
   - Results of biological plausibility checks
   - Positive/negative control validation
   - Known biology comparison
   - Red flags or concerns

8. **Preliminary Interpretation** (markdown):
   - Main findings in biological language
   - Consistency with expectations
   - Novel or surprising results
   - Biological implications

9. **Expert Handoff Section** (markdown, if needed):
   - Structured questions for biologist-commentator
   - Specific findings needing interpretation
   - Recommended follow-up analyses
   - Caveats and limitations

**Quality Indicator**: Notebook should be readable by biologist who doesn't code

## Quality Indicators

Your notebook is ready when:

**Technical Quality**:
- [ ] All code executes without errors
- [ ] Random seed set, results reproducible
- [ ] QC checks passed (positive controls work)
- [ ] Visualizations properly labeled
- [ ] Statistics completely reported
- [ ] Copilot approved code (no outstanding critical issues)

**Biological Quality**:
- [ ] Biological context provided for all major sections (concise, 1-3 sentences)
- [ ] Biological sanity checks completed and documented
- [ ] Positive/negative controls validated against biological expectations
- [ ] Preliminary interpretation written in biological terms
- [ ] Handoff to biologist-commentator structured (if unexpected findings)
- [ ] Notebook readable by non-coding biologist

**Integration Ready**:
- [ ] Ready for PI to expand interpretations for publication
- [ ] Clear which findings are routine vs need expert review
