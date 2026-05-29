---
name: immunopipe-config
description: Master skill for generating immunopipe pipeline configurations. Determines pipeline architecture based on data type (scRNA-seq with or without scTCR/BCR-seq) and analysis requirements. Routes to individual process skills for detailed configuration. Use this skill when starting a new immunopipe configuration or modifying pipeline-level options.
---

# Immunopipe Configuration Generator (Main Skill)

**Purpose**: Master skill for generating immunopipe pipeline configurations. Routes to individual process skills and determines pipeline architecture based on analysis requirements.

## When to Use This Skill

- User wants to create/modify immunopipe configuration files
- Need to determine which processes to enable based on analysis goals
- Need to configure pipeline-level options (name, outdir, forks, scheduler)
- Need routing to specific process configuration skills

## Pipeline Architecture Decision Tree

### Step 1: Data Type Assessment

Ask the user about their data:

1. **Do you have scRNA-seq data?**
   - If YES → RNA analysis processes needed
   - If NO → Cannot proceed (RNA data required)

2. **Do you have scTCR-seq or scBCR-seq data?**
   - If YES → Enable TCR/BCR processes (TCR route)
   - If NO → RNA-only analysis (No-TCR route)

3. **Is your RNA data already processed in a Seurat object?**
   - If YES → Use `LoadingRNAFromSeurat` instead of `SampleInfo` + `SeuratPreparing`
   - If NO → Use standard input via `SampleInfo`

### Step 2: Analysis Goals

Ask what analyses they want to perform:

| Goal | Required Processes | Routing |
|------|-------------------|---------|
| Basic clustering & visualization | `SampleInfo`, `SeuratPreparing`, `SeuratClustering`, `SeuratClusterStats` | Use `sampleinfo`, `seuratpreparing`, `seuratclustering`, `seuratclusterstats` skills |
| T/B cell selection | Add `TOrBCellSelection` | Use `torbcellselection` skill |
| Cell type annotation | Add `CellTypeAnnotation` or `SeuratMap2Ref` | Use `celltypeannotation` or `seuratmap2ref` skills |
| Marker finding | Add `ClusterMarkers` or `MarkersFinder` | Use `clustermarkers` or `markersfinder` skills |
| TCR clonotype analysis | Add `CDR3Clustering`, `TESSA`, `ClonalStats` | Use `cdr3clustering`, `tessa`, `clonalstats` skills |
| Cell-cell communication | Add `CellCellCommunication` | Use `cellcellcommunication` skill |
| Pathway enrichment | Add `ScFGSEA` | Use `scfgsea` skill |
| Metabolic analysis | Add `ScrnaMetabolicLandscape` | Use `scrnametaboliclandscape` skill |
| Differential expression | Add `PseudoBulkDEG` | Use `pseudobulkdeg` skill |

### Step 3: Essential vs Optional Processes

**Essential Processes (always needed for TCR route)**:
- `SampleInfo` (or `LoadingRNAFromSeurat`)
- `ScRepLoading` (if TCR/BCR data present)
- `SeuratPreparing` (unless loading from prepared Seurat object)
- `SeuratClustering`
- `SeuratClusterStats`

**Essential Processes (RNA-only route)**:
- `SampleInfo` (or `LoadingRNAFromSeurat`)
- `SeuratPreparing`
- `SeuratClustering`
- `SeuratClusterStats`

**Optional Processes** (enable only if requested):
- `TOrBCellSelection` - T/B cell separation
- `SeuratClusteringOfAllCells` - Clustering before T/B selection
- `ClusterMarkersOfAllCells` - Markers before T/B selection
- `TopExpressingGenesOfAllCells` - Top genes before T/B selection
- `CellTypeAnnotation` - Automated cell type annotation
- `SeuratMap2Ref` - Reference-based annotation
- `SeuratSubClustering` - Sub-clustering analysis
- `ClusterMarkers` - Differential expression between clusters
- `TopExpressingGenes` - Top expressed genes per cluster
- `MarkersFinder` - Flexible marker finding
- `ModuleScoreCalculator` - Module/pathway scoring
- `ScRepCombiningExpression` - TCR + RNA integration
- `CDR3Clustering` - TCR CDR3 clustering
- `TESSA` - TCR-specific analysis
- `CDR3AAPhyschem` - CDR3 physicochemical properties
- `ClonalStats` - Clonality statistics
- `CellCellCommunication` - Ligand-receptor analysis
- `CellCellCommunicationPlots` - Communication plots
- `ScFGSEA` - Fast gene set enrichment
- `PseudoBulkDEG` - Pseudo-bulk differential expression
- `ScrnaMetabolicLandscape` - Comprehensive metabolic analysis

## Pipeline-Level Configuration

### Basic Pipeline Options

```toml
name = "my_pipeline"           # Pipeline name (affects workdir and outdir)
outdir = "./output"            # Output directory (default: ./<name>-output)
loglevel = "info"              # Logging level: debug, info, warning, error
forks = 4                      # Number of parallel jobs (adjust based on CPU cores)
cache = true                   # Enable caching (recommended)
error_strategy = "halt"        # halt, ignore, or retry
num_retries = 3                # Number of retries if error_strategy = "retry"
```

### Scheduler Configuration

**Local execution** (default):
```toml
scheduler = "local"
```

**SLURM cluster**:
```toml
scheduler = "slurm"

[scheduler_opts]
qsub_opts = "-p general -q general -N {job.name} -t {job.index}"
```

**SGE cluster**:
```toml
scheduler = "sge"

[scheduler_opts]
qsub_opts = "-V -cwd -j yes"
```

**Google Cloud Batch**:
```toml
# Use: immunopipe gbatch instead of immunopipe
# See gbatch skill for configuration
```

### Plugin Options

```toml
[plugin_opts.report]
filters = ["name:Filter"]  # Filter processes in report

[plugin_opts.runinfo]
# Runinfo plugin enabled by default
```

## Routing to Process Skills

When user needs specific process configuration, route to the appropriate skill:

### Core Input Processes
- **SampleInfo**: Use `sampleinfo` skill
- **LoadingRNAFromSeurat**: Use `loadingrnafromseurat` skill
- **ScRepLoading**: Use `screploading` skill

### Preprocessing Processes
- **SeuratPreparing**: Use `seuratpreparing` skill

### Clustering Processes
- **SeuratClustering**: Use `seuratclustering` skill
- **SeuratClusteringOfAllCells**: Use `seuratclusteringofallcells` skill
- **SeuratSubClustering**: Use `seuratsubclustering` skill

### Cell Selection
- **TOrBCellSelection**: Use `torbcellselection` skill

### Annotation Processes
- **CellTypeAnnotation**: Use `celltypeannotation` skill
- **SeuratMap2Ref**: Use `seuratmap2ref` skill

### Marker Analysis
- **ClusterMarkers**: Use `clustermarkers` skill
- **ClusterMarkersOfAllCells**: Use `clustermarkersofallcells` skill
- **MarkersFinder**: Use `markersfinder` skill
- **TopExpressingGenes**: Use `topexpressinggenes` skill
- **TopExpressingGenesOfAllCells**: Use `topexpressinggenesofallcells` skill

### TCR/BCR Analysis
- **ScRepCombiningExpression**: Use `screpcombiningexpression` skill
- **CDR3Clustering**: Use `cdr3clustering` skill
- **TESSA**: Use `tessa` skill
- **CDR3AAPhyschem**: Use `cdr3aaphyschem` skill
- **ClonalStats**: Use `clonalstats` skill

### Downstream Analysis
- **ModuleScoreCalculator**: Use `modulescorecalculator` skill
- **CellCellCommunication**: Use `cellcellcommunication` skill
- **CellCellCommunicationPlots**: Use `cellcellcommunicationplots` skill
- **SeuratClusterStats**: Use `seuratclusterstats` skill
- **ScFGSEA**: Use `scfgsea` skill
- **PseudoBulkDEG**: Use `pseudobulkdeg` skill

### Metabolic Analysis
- **ScrnaMetabolicLandscape**: Use `scrnametaboliclandscape` skill

## Configuration File Structure

A complete TOML configuration file has three sections:

```toml
# 1. PIPELINE-LEVEL OPTIONS
name = "my_pipeline"
outdir = "./output"
forks = 4

# 2. PROCESS-LEVEL OPTIONS
[ProcessName]
cache = true
forks = 2  # Override pipeline-level forks for this process

[ProcessName.in]
# Input files specification

[ProcessName.envs]
# Environment variables (process parameters)

# 3. GOOGLE BATCH OPTIONS (if using immunopipe gbatch)
[cli-gbatch]
project = "my-gcp-project"
region = "us-central1"
```

## Example Workflows

### Example 1: Basic TCR Analysis

**User request**: "I have scRNA-seq and scTCR-seq data. I want basic analysis with T cell selection."

**Response**:
1. Enable essential TCR processes: `SampleInfo`, `ScRepLoading`, `SeuratPreparing`, `SeuratClustering`, `SeuratClusterStats`
2. Enable T cell selection: `SeuratClusteringOfAllCells`, `TOrBCellSelection`
3. Route to `sampleinfo` skill to configure input files
4. Route to each process skill for configuration

**Minimal config**:
```toml
name = "tcr_analysis"
forks = 4

[SampleInfo.in]
infile = ["sample_info.txt"]

[SeuratClusteringOfAllCells]
[TOrBCellSelection]
```

### Example 2: Advanced RNA-only Analysis

**User request**: "RNA-only data. I need clustering, cell type annotation, marker finding, and pathway enrichment."

**Response**:
1. Enable essential RNA processes: `SampleInfo`, `SeuratPreparing`, `SeuratClustering`, `SeuratClusterStats`
2. Add requested analyses: `CellTypeAnnotation`, `ClusterMarkers`, `ScFGSEA`
3. Route to individual skills for configuration

### Example 3: Loading from Prepared Seurat Object

**User request**: "I already have a processed Seurat object. I want to run TCR analysis."

**Response**:
1. Use `LoadingRNAFromSeurat` instead of `SampleInfo` + `SeuratPreparing`
2. Enable TCR processes: `ScRepLoading`, `SeuratClustering`, etc.
3. Set `prepared = true` in `LoadingRNAFromSeurat` to skip preprocessing

## Important Notes

### Process Dependencies

Some processes have dependencies:
- `ScRepCombiningExpression` requires both `ScRepLoading` and RNA input
- `ClusterMarkers` requires `SeuratClustering`
- `TOrBCellSelection` usually follows `SeuratClusteringOfAllCells`
- `CellCellCommunication` requires clustering to be complete

### Mutually Exclusive Options

- Use EITHER `SampleInfo` OR `LoadingRNAFromSeurat` as entry point (not both)
- If using `TOrBCellSelection`, typically enable `SeuratClusteringOfAllCells` first
- `CellTypeAnnotation` and `SeuratMap2Ref` serve similar purposes (can use both, but one usually sufficient)

### Cache Strategy

- Set `cache = "force"` at pipeline level to reuse all previous results
- Set `cache = false` for specific process to force re-run
- Useful when tweaking visualization parameters without re-running analysis

### Configuration Validation

After generating configuration, validate with:
```bash
python -m immunopipe.validate_config config.toml
```

## External References

When process options reference external packages, expand them:

### Seurat Functions
- When seeing `Seurat::FunctionName`, check: https://satijalab.org/seurat/reference/
- Common functions: `FindMarkers()`, `FindClusters()`, `SCTransform()`, `RunUMAP()`

### Plotthis Functions  
- Plot types map to functions: `bar` → `BarPlot`, `box` → `BoxPlot`
- Full reference: https://pwwang.github.io/plotthis/reference/

### DESeq2 Design
- For `PseudoBulkDEG`, design formulas use DESeq2 syntax
- Reference: https://bioconductor.org/packages/release/bioc/html/DESeq2.html

### GSEA Databases
- For `ScFGSEA`, GMT files from MSigDB
- Reference: https://www.gsea-msigdb.org/gsea/msigdb/

### CellChat Database
- For `CellCellCommunication`, CellChat databases
- Reference: http://www.cellchat.org/

## Workflow Summary

1. **Assess data type** (RNA-only vs TCR/BCR)
2. **Determine analysis goals** (clustering, annotation, TCR analysis, etc.)
3. **Select essential processes** based on data type
4. **Add optional processes** based on goals
5. **Configure pipeline-level options** (name, forks, scheduler)
6. **Route to individual process skills** for detailed configuration
7. **Generate complete TOML file**
8. **Validate configuration** before running

## Quick Start Templates

For quick starts, use these templates:

- **Basic TCR**: `basic-tcr` template skill
- **Basic RNA-only**: `basic-rna` template skill
- **Advanced TCR**: `advanced-tcr` template skill
- **Metabolic analysis**: `metabolic` template skill
- **Cell communication**: `communication` template skill

## Error Prevention

Common configuration errors to avoid:

1. **Missing input specification**: Always set `[ProcessName.in]` for entry processes
2. **TCR data without ScRepLoading**: If TCRData/BCRData columns exist, enable `ScRepLoading`
3. **Contradictory process enablement**: Don't enable both "OfAllCells" and regular versions without `TOrBCellSelection`
4. **Invalid gene names**: Use human gene symbols (uppercase) or mouse (title case)
5. **Path issues**: Use absolute paths or paths relative to config file location
6. **Resource limits**: Set appropriate `forks` based on available CPU/memory

## Next Steps

After generating config:
1. Save to `.toml` file (e.g., `config.toml`)
2. Run: `immunopipe config.toml`
3. Or use web UI: `pipen board @config.toml`
4. Or use Google Batch: `immunopipe gbatch config.toml`

For modifications, route to specific process skills based on what needs to change.
