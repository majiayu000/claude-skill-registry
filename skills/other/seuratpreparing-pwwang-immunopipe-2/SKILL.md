---
name: seuratpreparing
description: Load, prepare, and apply quality control (QC) to single-cell RNA-seq data using Seurat. Performs data loading, QC filtering, normalization, and multi-sample integration. This is a core preprocessing process that prepares Seurat objects for downstream clustering and analysis.
---

# SeuratPreparing Process Configuration

## Purpose
Load, prepare, and apply quality control (QC) to single-cell RNA-seq data using Seurat. Performs data loading, QC filtering, normalization, and multi-sample integration. This is a core preprocessing process that prepares Seurat objects for downstream clustering and analysis.

## When to Use
- **Essential process** for all RNA-based immunopipe analyses (TCR and non-TCR routes)
- Required unless loading from already-prepared Seurat objects (see `LoadingRNAFromSeurat` process)
- Multi-sample datasets requiring batch correction and integration
- Data requiring doublet detection and removal
- Raw scRNA-seq data needing QC, normalization, and integration

### Data Requirements
- Input data paths specified in `SampleInfo` metafile (`RNAData` column)
- Supported formats: 10x Genomics output (matrix.mtx, barcodes.tsv, features.tsv), h5 files, loom files, or pre-loaded Seurat objects (RDS/qs2)
- Each sample loaded individually and merged into one Seurat object

### Dependencies
- **Upstream**: `SampleInfo` (provides metadata) OR `LoadingRNAFromSeurat` (provides prepared Seurat object)
- **Downstream**: `SeuratClustering`, `SeuratClusteringOfAllCells`, `TOrBCellSelection`

## Configuration Structure

### Process Enablement
```toml
[SeuratPreparing]
cache = true  # Enable caching to speed up re-runs
```

### Input Specification
```toml
[SeuratPreparing.in]
# metafile is required unless LoadingRNAFromSeurat is used
metafile = ["path/to/sample_info.txt"]
```

**metafile format** (tab-delimited):
- `Sample`: Unique sample identifier (required)
- `RNAData`: Path to scRNA-seq data (required)
  - Directory containing matrix.mtx, barcodes.tsv, features.tsv (10x format)
  - Path to h5 file readable by `Seurat::Read10X_h5()`
  - Path to loom file readable by `SeuratDisk::LoadLoom()`
  - Path to RDS/qs2 file containing Seurat object
- Additional columns: Treated as sample metadata (optional)

### Environment Variables

```toml
[SeuratPreparing.envs]
# Core processing parameters
ncores = 1                           # Parallelization cores
mutaters = {}                          # Add custom metadata columns
min_cells = 0                           # Minimum cells per gene (CreateSeuratObject)
min_features = 0                         # Minimum features per cell (CreateSeuratObject)

# Quality control
cell_qc = ""                           # Cell filtering expression (R syntax)
gene_qc = { min_cells = 0 }            # Gene filtering options

# QC plots generation
qc_plots = {}                           # Visualization configuration

# Normalization method selection
use_sct = false                         # Use SCTransform instead of NormalizeData pipeline
no_integration = false                    # Skip sample integration

# Doublet detection
doublet_detector = "none"                # Options: none, DoubletFinder, scDblFinder

# Caching
cache = "/tmp"                          # Cache intermediate results
```

## External References

### Seurat Normalization Functions

**Standard Workflow** (`use_sct = false`):
1. **NormalizeData** - Log-normalization of UMI counts
   ```toml
   [SeuratPreparing.envs.NormalizeData]
   normalization-method = "LogNormalize"  # Options: LogNormalize, CLR, RC
   scale-factor = 10000                   # Normalization scaling factor
   margin = 1                             # Normalize across features (1) or cells (2)
   verbose = true
   ```
   - Reference: https://satijalab.org/seurat/reference/normalizedata
   - **LogNormalize**: Count / scale_factor * 10,000 (default)
   - **CLR**: Centered log-ratio transformation
   - **RC**: Relative count normalization

2. **FindVariableFeatures** - Identify highly variable genes
   ```toml
   [SeuratPreparing.envs.FindVariableFeatures]
   selection-method = "vst"             # Options: vst, mean.var.plot, disp
   nfeatures = 2000                      # Number of variable features to select
   verbose = true
   ```
   - Reference: https://satijalab.org/seurat/reference/findvariablefeatures
   - **vst**: Variance-stabilizing transformation (recommended)
   - **mean.var.plot**: Mean-variance relationship
   - **disp**: Dispersion-based selection

3. **ScaleData** - Center and scale gene expression
   ```toml
   [SeuratPreparing.envs.ScaleData]
   vars.to.regress = []                   # Variables to regress out (e.g., ["percent.mt"])
   model.use = "linear"                    # Regression model
   verbose = true
   ```
   - Reference: https://satijalab.org/seurat/reference/scaledata
   - Regresses unwanted variation (mitochondrial, ribosomal, cell cycle)
   - Centers data at mean = 0, SD = 1

4. **RunPCA** - Principal component analysis
   ```toml
   [SeuratPreparing.envs.RunPCA]
   npcs = 50                             # Number of principal components
   verbose = true
   rev.pca = false                        # Reverse PCA direction
   weight.by.var = true                     # Weight by variance
   ```
   - Reference: https://satijalab.org/seurat/reference/runpca
   - `npcs` limited by: number of columns - 1 per sample

**SCTransform Workflow** (`use_sct = true`):
5. **SCTransform** - Variance-stabilizing transformation (replaces standard pipeline)
   ```toml
   [SeuratPreparing.envs.SCTransform]
   assay = "RNA"                         # Input assay
   new.assay.name = "SCT"                # Output assay name
   return-only-var-genes = true            # Keep only variable genes
   min_cells = 3                           # Minimum cells per gene (hidden param)
   variable.features.n = 3000               # Number of variable features
   variable.features.rv.th = 1.3            # Residual variance threshold
   vars.to.regress = []                   # Variables to regress out
   do.correct.umi = true                   # Correct for UMI counts
   ncells = 5000                         # Subsample for model fitting
   do.scale = false                        # Scale after transformation
   do.center = true                         # Center after transformation
   clip.range = [-10, 10]                  # Clip residual values
   vst.flavor = "v2"                     # VST algorithm version
   conserve.memory = false                  # Memory-efficient mode
   seed.use = 1448145                     # Random seed
   verbose = true
   ```
   - Reference: https://satijalab.org/seurat/reference/sctransform
   - **Advantages**: Better normalization, handles technical noise, integrates well with Seurat v5
   - **Output**: New assay named "SCT" with corrected counts, log1p data, Pearson residuals
   - **To keep all genes**: Set `min_cells = 0` and `return-only-var-genes = false`
   - See: https://github.com/satijalab/seurat/issues/3598#issuecomment-715505537

### Integration Methods

**IntegrateLayers** - Multi-sample batch correction
```toml
[SeuratPreparing.envs.IntegrateLayers]
method = "harmony"                      # Integration method
orig.reduction = "pca"                  # Base reduction for correction
assay = null                             # Assay to integrate (auto-detected)
features = null                           # Features for integration
layers = null                             # Layers to integrate
scale.layer = "scale.data"                 # Scaled layer name
```
- Reference: https://satijalab.org/seurat/reference/integratelayers
- **Method options**:
  - **CCAIntegration / CCA / cca**: Canonical correlation analysis
    - Best for: Strong expression differences across conditions/species
    - Can overcorrect with non-overlapping cell types
    - Slower than RPCA
  - **RPCAIntegration / RPCA / rpca**: Reciprocal PCA
    - Best for: Same platform, large datasets, non-overlapping cells
    - Faster, more conservative
    - Recommended for multi-batch 10x data
    - Reference: https://satijalab.org/seurat/articles/integration_rpca
  - **HarmonyIntegration / Harmony / harmony**: Harmony algorithm
    - Fast, iterative integration
    - Good for complex batch structures
    - Default method in immunopipe
  - **FastMNNIntegration / FastMNN / fastmnn**: Fast mutual nearest neighbors
    - Good for large datasets
    - From batchelor package
  - **scVIIntegration / scVI / scvi**: Variational inference
    - Deep learning-based
    - Requires scVI package

### Doublet Detection

**DoubletFinder** - Simulation-based doublet detection
```toml
[SeuratPreparing.envs.DoubletFinder]
PCs = 10                                 # Number of PCs to use
doublets = 0.075                          # Expected doublet rate (7.5%)
pN = 0.25                                  # Doublet simulation proportion (25%)
ncores = 1                                  # Cores for paramSweep (null = use envs.ncores)
pK = 0.005                                 # Expected doublet rate parameter
reduction = "pca"                           # Reduction to use
```
- Reference: https://github.com/chris-mcginnis-ucsf/DoubletFinder
- Documentation: https://demultiplexing-doublet-detecting-docs.readthedocs.io
- **Workflow**: pK sweep → classify doublets → filter
- **Tip**: Set `ncores` smaller than `envs.ncores` if memory issues occur

**scDblFinder** - Machine learning-based doublet detection
```toml
[SeuratPreparing.envs.scDblFinder]
dbr = 0.075                               # Expected doublet rate (7.5%)
ncores = 1                                  # Cores for scDblFinder (null = use envs.ncores)
dbr.per1k = 0.8                            # Doublets per 1000 cells
verbose = true
```
- Reference: https://rdrr.io/bioc/scDblFinder/man/scDblFinder.html
- Documentation: https://www.bioconductor.org/packages/release/bioc/vignettes/scDblFinder/inst/doc/scDblFinder.html
- **Advantages**: Faster, more accurate, includes doublet origin predictions
- **Modes**: Cluster-based (clear structure) or random (complex datasets)
- **Default dbr**: Updated to 0.8% per 1000 cells in recent versions

## Configuration Examples

### Minimal Configuration (Single Sample, No Integration)
```toml
[SeuratPreparing]
[SeuratPreparing.in]
metafile = ["sample_info.txt"]

[SeuratPreparing.envs]
cell_qc = "nFeature_RNA > 200 & percent.mt < 5"
gene_qc = { min_cells = 3 }
```

### Standard SCTransform with Harmony Integration
```toml
[SeuratPreparing]
[SeuratPreparing.in]
metafile = ["sample_info.txt"]

[SeuratPreparing.envs]
ncores = 4
use_sct = true

# QC filtering
cell_qc = "nFeature_RNA > 200 & percent.mt < 5"
gene_qc = { min_cells = 3 }

# SCTransform parameters
[SeuratPreparing.envs.SCTransform]
vars.to.regress = ["percent.mt", "percent.ribo"]
variable.features.n = 3000

# Harmony integration
[SeuratPreparing.envs.IntegrateLayers]
method = "harmony"
```

### Multi-sample RPCA Integration
```toml
[SeuratPreparing]
[SeuratPreparing.in]
metafile = ["sample_info.txt"]

[SeuratPreparing.envs]
use_sct = false
ncores = 8

# Standard normalization workflow
[SeuratPreparing.envs.NormalizeData]
normalization-method = "LogNormalize"
scale-factor = 10000

[SeuratPreparing.envs.FindVariableFeatures]
selection-method = "vst"
nfeatures = 3000

[SeuratPreparing.envs.ScaleData]
vars.to.regress = ["percent.mt", "S.Score", "G2M.Score"]

# RPCA integration (faster, conservative)
[SeuratPreparing.envs.IntegrateLayers]
method = "rpca"
orig.reduction = "pca"
```

### With DoubletFinder
```toml
[SeuratPreparing]
[SeuratPreparing.in]
metafile = ["sample_info.txt"]

[SeuratPreparing.envs]
use_sct = true
doublet_detector = "DoubletFinder"

[SeuratPreparing.envs.DoubletFinder]
PCs = 30
doublets = 0.05
pN = 0.25
ncores = 4
```

### With scDblFinder
```toml
[SeuratPreparing]
[SeuratPreparing.in]
metafile = ["sample_info.txt"]

[SeuratPreparing.envs]
use_sct = true
doublet_detector = "scDblFinder"

[SeuratPreparing.envs.scDblFinder]
dbr = 0.05
ncores = 4
```

### Per-Sample Cell QC
```toml
[SeuratPreparing.envs]
cell_qc = { DEFAULT = "nFeature_RNA > 200 & percent.mt < 5",
              Sample1 = "nFeature_RNA > 300 & percent.mt < 10",
              Sample2 = "nFeature_RNA > 150 & percent.mt < 5" }
```

### Custom QC Plots
```toml
[SeuratPreparing.envs.qc_plots]
# Violin plots for QC metrics
[SeuratPreparing.envs.qc_plots."QC Violin Plots"]
kind = "cell"
plot_type = "violin"
devpars = { res = 100, height = 600, width = 1200 }

# Scatter plots
[SeuratPreparing.envs.qc_plots."QC Scatter Plots"]
kind = "cell"
plot_type = "scatter"
devpars = { res = 100, height = 800, width = 1200 }

# Gene expression distribution
[SeuratPreparing.envs.qc_plots."Gene Expression Distribution"]
kind = "gene"
plot_type = "histogram"
devpars = { res = 100, height = 1200, width = 1200 }
```

## Common Patterns

### Pattern 1: Single Sample (No Integration)
```toml
# Use when analyzing one sample or already batch-corrected data
[SeuratPreparing]
[SeuratPreparing.in]
metafile = ["single_sample_info.txt"]

[SeuratPreparing.envs]
no_integration = true  # Skip integration step
use_sct = true
cell_qc = "nFeature_RNA > 200 & percent.mt < 5"
gene_qc = { min_cells = 3 }
```

### Pattern 2: Multiple Samples with Harmony Integration
```toml
# Use for multi-batch data with complex batch structures
[SeuratPreparing]
[SeuratPreparing.in]
metafile = ["multi_sample_info.txt"]

[SeuratPreparing.envs]
use_sct = true
ncores = 8

# Cell QC
cell_qc = "nFeature_RNA > 200 & nCount_RNA > 500 & percent.mt < 10"
gene_qc = { min_cells = 3, excludes = ["MALAT1", "MT-ND3"] }

# SCTransform with regression
[SeuratPreparing.envs.SCTransform]
vars.to.regress = ["percent.mt", "percent.ribo", "S.Score", "G2M.Score"]
variable.features.n = 3000

# Harmony integration
[SeuratPreparing.envs.IntegrateLayers]
method = "harmony"
```

### Pattern 3: Batch Correction with RPCA (Large Datasets)
```toml
# Use for large datasets (>100k cells) or same-platform multi-batch
[SeuratPreparing]
[SeuratPreparing.in]
metafile = ["large_dataset_info.txt"]

[SeuratPreparing.envs]
use_sct = false  # RPCA works better with standard workflow
ncores = 16

# Standard workflow
[SeuratPreparing.envs.NormalizeData]
normalization-method = "LogNormalize"
scale-factor = 10000

[SeuratPreparing.envs.FindVariableFeatures]
selection-method = "vst"
nfeatures = 3000

[SeuratPreparing.envs.ScaleData]
vars.to.regress = ["percent.mt", "percent.ribo"]

[SeuratPreparing.envs.RunPCA]
npcs = 100

# RPCA integration (faster for large data)
[SeuratPreparing.envs.IntegrateLayers]
method = "rpca"
orig.reduction = "pca"
```

### Pattern 4: Doublet Detection + Integration
```toml
# Use for datasets with high doublet rates (>5%)
[SeuratPreparing]
[SeuratPreparing.in]
metafile = ["high_doublet_info.txt"]

[SeuratPreparing.envs]
use_sct = true
doublet_detector = "scDblFinder"  # or "DoubletFinder"

[SeuratPreparing.envs.scDblFinder]
dbr = 0.08  # Higher expected doublet rate
ncores = 4

[SeuratPreparing.envs.SCTransform]
vars.to.regress = ["percent.mt", "percent.ribo"]

[SeuratPreparing.envs.IntegrateLayers]
method = "harmony"
```

### Pattern 5: Keep All Genes (Not Just Variable Genes)
```toml
# Use when you need to analyze non-variable genes later
[SeuratPreparing]
[SeuratPreparing.in]
metafile = ["sample_info.txt"]

[SeuratPreparing.envs]
use_sct = true

[SeuratPreparing.envs.SCTransform]
min_cells = 0                    # Don't filter by expression
return-only-var-genes = false   # Keep all genes in RNA assay
```

## Dependencies

### Upstream Processes
- **SampleInfo**: Provides metadata and RNA data paths (required unless LoadingRNAFromSeurat used)
- **LoadingRNAFromSeurat**: Alternative input for pre-loaded Seurat objects

### Downstream Processes
- **SeuratClustering**: Clustering on selected cells (T/B or all)
- **SeuratClusteringOfAllCells**: Clustering on all cells before T/B selection
- **TOrBCellSelection**: T cell or B cell subset selection
- **SeuratClusterStats**: Cluster statistics and visualizations

### Assay Output
- **SCT assay**: Default assay when `use_sct = true`
- **RNA assay**: Default assay when `use_sct = false`
- **integrated assay**: Default assay when using CCA/RPCA integration

## Validation Rules

### Required Parameters
- `[SeuratPreparing.in.metafile]` is required unless `LoadingRNAFromSeurat` is in config
- Cell IDs in output are prefixed with sample names (metadata column: `Sample`)

### Normalization Method Constraints
- **SCTransform**: Sets default assay to "SCT"
  - Incompatible with: `NormalizeData`, `FindVariableFeatures`, `ScaleData`, `RunPCA` (when `use_sct = true`)
  - Compatible with: All integration methods
- **Standard workflow**: Sets default assay to "RNA"
  - Required when: `use_sct = false`
  - Sequence: NormalizeData → FindVariableFeatures → ScaleData → RunPCA

### Integration Method Constraints
- **SCTransform + Integration**: When `use_sct = true`, `IntegrateLayers.normalization-method` defaults to "SCT"
- **No integration**: Set `no_integration = true` for single sample or pre-integrated data
- **Integration required**: Automatic for multi-sample data unless `no_integration = true`

### Doublet Detection Constraints
- **DoubletFinder vs scDblFinder**: Choose one, not both
- **SCTransform compatibility**: Both detectors work with SCTransform
- **Memory**: DoubletFinder may require lower `ncores` than other processes

### Cache Configuration
- **cache = "/tmp"**: Default, uses system temp directory
- **cache = true**: Caches in job output directory (not cleaned on re-run)
- **cache = false**: Disables caching (re-runs entire process)
- **Force re-run**: Delete `<signature>.<kind>.RDS` files or set `cache = false`

## Troubleshooting

### Issue: Too many cells filtered by QC
**Symptoms**: Low cell count after `SeuratPreparing`
**Solutions**:
- Relax cell_qc thresholds: `"nFeature_RNA > 100 & percent.mt < 20"`
- Check `percent.mt` calculation: Ensure mitochondrial genes are prefixed correctly (human: `MT-`, mouse: `mt-`)
- Review `nFeature_RNA` and `nCount_RNA` distributions in QC plots
- Consider per-sample QC if batches differ significantly

### Issue: Integration overcorrects biological variation
**Symptoms**: Clusters mix distinct cell types after integration
**Solutions**:
- Switch from CCA to RPCA: `method = "rpca"`
- Switch from CCA/RPCA to Harmony: `method = "harmony"`
- Reduce integration strength: Adjust method-specific parameters
- Try no integration if batches are minimal: `no_integration = true`

### Issue: High doublet rate detected (>15%)
**Symptoms**: More doublets than expected
**Solutions**:
- Check `doublets` or `dbr` parameter matches actual loading
- Adjust expected doublet rate to match data loading
- Review cell loading: High UMI loading increases doublets
- Consider re-running cellranger with adjusted parameters

### Issue: SCTransform returns too few genes
**Symptoms**: Low number of genes in SCT assay
**Solutions**:
- Increase `min_cells`: `[SeuratPreparing.envs.SCTransform.min_cells = 0`
- Disable var-gene-only: `return-only-var-genes = false`
- Check `variable.features.n`: Increase to 5000 or higher
- Review `variable.features.rv.th`: Lower threshold (e.g., 1.2)

### Issue: Memory errors during processing
**Symptoms**: Process killed or out-of-memory errors
**Solutions**:
- Reduce `ncores`: Parallelization uses more memory
- Reduce `ncells` in SCTransform: Subsample for model fitting
- Use `conserve.memory = true` in SCTransform
- Switch to RPCA integration: Faster and less memory-intensive than CCA
- Reduce DoubletFinder `ncores`: Set to 1-2 cores

### Issue: Slow processing for large datasets
**Symptoms**: Process takes >24 hours
**Solutions**:
- Increase `ncores` (with sufficient memory)
- Use RPCA instead of CCA: `method = "rpca"`
- Use scDblFinder instead of DoubletFinder: Faster doublet detection
- Reduce `ncells` in SCTransform: Faster model fitting
- Enable caching: `cache = true` for faster re-runs

### Issue: Batch effects remain after integration
**Symptoms**: Cells cluster by sample rather than cell type
**Solutions**:
- Try different integration method: CCA for strong differences, RPCA/Harmony for subtle differences
- Regress batch variables: `vars.to.regress = ["batch_var"]`
- Check if biological differences are real: Batch vs condition effects
- Increase integration parameters: More PCs, longer Harmony iterations

### Issue: Seurat v5 compatibility errors
**Symptoms**: Assay layer errors, deprecated function warnings
**Solutions**:
- Ensure Seurat v5.0.0+ is installed: `install.packages("Seurat")`
- Update workflow: Use `IntegrateLayers` instead of `FindIntegrationAnchors`
- Check assay structure: `object[["RNA"]]` vs `object@assays$RNA`
- Review Seurat v5 migration guide: https://satijalab.org/seurat/articles/seurat5_integration

## Quick Reference

### Default Parameter Values
```toml
ncores = 1
min_cells = 0
min_features = 0
cell_qc = ""
gene_qc = { min_cells = 0 }
use_sct = false
no_integration = false
doublet_detector = "none"
cache = "/tmp"

# NormalizeData
normalization-method = "LogNormalize"
scale-factor = 10000

# FindVariableFeatures
selection-method = "vst"
nfeatures = 2000

# SCTransform
variable.features.n = 3000
variable.features.rv.th = 1.3
min_cells = 3
return-only-var-genes = true

# IntegrateLayers
method = "harmony"

# DoubletFinder
PCs = 10
doublets = 0.075
pN = 0.25

# scDblFinder
dbr = 0.075
```

### QC Metric Keys (Available in cell_qc expressions)
- `nFeature_RNA`: Number of genes detected per cell
- `nCount_RNA`: Total UMI counts per cell
- `percent.mt`: Percentage of mitochondrial gene expression
- `percent.ribo`: Percentage of ribosomal gene expression
- `percent.hb`: Percentage of hemoglobin gene expression
- `percent.plat`: Percentage of platelet gene expression

### Integration Method Selection Guide
| Situation | Recommended Method | Reason |
|-----------|-------------------|---------|
| Strong biological differences | CCA | Captures shared biology despite expression shifts |
| Same platform, large data | RPCA | Faster, conservative, less overcorrection |
| Complex batch structure | Harmony | Handles multiple batch variables |
| Very large datasets (>200k) | RPCA or scVI | Scales well computationally |
| Cross-modality integration | CCA or FastMNN | Designed for different data types |
| Preliminary analysis | Harmony | Fast, good default performance |

### Seurat Assay Information After Processing
- **use_sct = false**: Default assay = `RNA` (normalized, scaled)
- **use_sct = true**: Default assay = `SCT` (variance-stabilized)
- **CCA/RPCA integration**: Default assay = `integrated`
- **Harmony integration**: Default assay = `SCT` (if use_sct = true) or `RNA` (if use_sct = false)
