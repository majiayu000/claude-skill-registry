---
name: celltypeannotation
description: Annotates cell clusters with biological cell type labels using multiple methods: direct assignment, ScType, scCATCH, hitype, or CellTypist. This process is essential for interpreting clustering results by assigning meaningful biological identities to each cluster.
---

# CellTypeAnnotation Process Configuration

## Purpose
Annotates cell clusters with biological cell type labels using multiple methods: direct assignment, ScType, scCATCH, hitype, or CellTypist. This process is essential for interpreting clustering results by assigning meaningful biological identities to each cluster.

## When to Use
- **After clustering**: When you have cluster assignments but need biological cell type labels
- **Automated annotation**: When manual annotation is too time-consuming or subjective
- **Consistent nomenclature**: When you need standardized cell type names across multiple samples
- **Reference-based annotation**: When you have well-characterized reference datasets or marker databases
- **Cross-sample comparison**: When analyzing multiple samples with the same cell type definitions
- **Alternative to SeuratMap2Ref**: When you prefer database-based annotation over reference dataset mapping

## Configuration Structure

### Process Enablement
```toml
[CellTypeAnnotation]
cache = true  # Cache results for faster re-runs
```

### Input Specification
```toml
[CellTypeAnnotation.in]
sobjfile = ["SeuratClustering"]  # Path or reference to Seurat object
```

### Environment Variables

#### Core Parameters
```toml
[CellTypeAnnotation.envs]
# Annotation method selection
tool = "direct"  # Options: "direct", "sctype", "hitype", "sccatch", "celltypist"

# Cluster identity column (required for h5ad input, optional for Seurat objects)
ident = "seurat_clusters"  # Column name in metadata representing clusters

# Backup column name (stores original cluster labels)
backup_col = "seurat_clusters_id"  # Default: "seurat_clusters_id"

# New column name for annotated cell types
# If specified, original identity is kept; otherwise, it's replaced
newcol = ""  # Default: empty (overwrite identity)

# Merge clusters with same predicted cell types
merge = false  # Default: false; suffixes (.1, .2) added for duplicate labels

# Output file type
outtype = "input"  # Options: "input", "rds", "qs", "qs2", "h5ad"
```

#### Direct Annotation Parameters
```toml
[CellTypeAnnotation.envs]
tool = "direct"

# Cell type assignments (one per cluster, in order)
# Use "-" or "" to keep original cluster name
# Use "NA" to remove cluster from downstream analysis (only without newcol)
cell_types = ["CD4+ T cells", "CD8+ T cells", "-", "B cells"]  # Default: []

# Additional annotations (multiple cell type columns)
more_cell_types = {  # Dict: {new_column: [cell_types]}
    cell_type_broad = ["T cells", "T cells", "NK cells", "B cells"],
    cell_type_detailed = ["CD4+ naive", "CD8+ effector", "NK", "B naive"]
}
```

#### ScType Annotation Parameters
```toml
[CellTypeAnnotation.envs]
tool = "sctype"

# Tissue type (must match tissueType column in database)
sctype_tissue = "Immune system"  # Required for sctype

# Database file path (Excel format compatible with ScType)
sctype_db = "/path/to/ScTypeDB_full.xlsx"  # Optional: uses default if not specified
```

#### hitype Annotation Parameters
```toml
[CellTypeAnnotation.envs]
tool = "hitype"

# Tissue type (must match tissueType column in database)
hitype_tissue = "Immune system"  # Required for hitype

# Database file path or built-in database name
# Built-in options: "hitypedb_short", "hitypedb_full", "hitypedb_pbmc3k"
hitype_db = "hitypedb_full"  # Default: built-in database
```

#### scCATCH Annotation Parameters
```toml
[CellTypeAnnotation.envs]
tool = "sccatch"

[CellTypeAnnotation.envs.sccatch_args]
# Species (Human or Mouse)
species = "Human"  # Required

# Tissue origin
tissue = "Blood"  # Required

# Cancer type (if cancer tissue)
cancer = "Normal"  # Default: "Normal"

# Custom marker genes (RDS file or list)
marker = ""  # Optional

# Use custom marker instead of database
if_use_custom_marker = false  # Default: false

# Additional scCATCH::findmarkergene() arguments
# See: https://rdrr.io/cran/scCATCH/man/findmarkergene.html
```

#### CellTypist Annotation Parameters
```toml
[CellTypeAnnotation.envs]
tool = "celltypist"

[CellTypeAnnotation.envs.celltypist_args]
# Model file path (download from https://celltypist.cog.sanger.ac.uk/models/models.json)
model = "Immune_All_Low.pkl"  # Required

# Python interpreter where celltypist is installed
python = "python"  # Default: "python"

# Majority voting refinement for local subclusters
majority_voting = true  # Default: true

# Over-clustering column (for majority voting)
# Set to false to disable over-clustering
over_clustering = "seurat_clusters"  # Auto: identity for Seurat, false for h5ad

# Assay for Seurat-to-AnnData conversion
assay = ""  # Auto: RNA for h5seurat, default assay for Seurat
```

## Annotation Methods

### 1. Direct Annotation
Assigns cell types manually to each cluster. Best when you have well-defined marker genes or want complete control over annotations.

**Pros**:
- Full control over annotations
- Fast and deterministic
- Works with any clustering result

**Cons**:
- Requires domain knowledge
- Time-consuming for many clusters
- Subjective

**Use cases**:
- Small number of well-separated clusters
- Known marker genes
- Reproducible annotation needed

### 2. ScType
Uses pre-defined cell type markers from ScType database. Annotates based on enrichment of known marker genes in each cluster.

**Databases**:
- ScTypeDB_short.xlsx: Compact database (~70 cell types)
- ScTypeDB_full.xlsx: Full database (~200+ cell types)
- Custom database: Provide your own Excel file

**Pros**:
- Automated annotation
- Tissue-specific filtering available
- Well-curated marker database

**Cons**:
- Limited to predefined cell types
- Requires tissue specification
- May miss rare cell types

**Reference**: https://github.com/IanevskiAleksandr/sc-type

**Use cases**:
- Immune tissue datasets
- When tissue type is well-defined
- Need for comprehensive annotation

### 3. hitype
Flexible annotation tool compatible with ScType database format. Supports both file-based and built-in databases.

**Built-in databases**:
- `hitypedb_short`: Compact marker set
- `hitypedb_full`: Comprehensive marker set
- `hitypedb_pbmc3k`: PBMC-specific markers (from 10X PBMC3k dataset)

**Pros**:
- Faster than ScType (Python-based)
- Multiple built-in databases
- Tissue-specific filtering

**Cons**:
- Limited to database cell types
- Requires tissue specification

**Reference**: https://github.com/pwwang/hitype

**Use cases**:
- PBMC datasets (use `hitypedb_pbmc3k`)
- General immune annotation
- When speed matters

### 4. scCATCH
Identifies cell types by matching cluster marker genes to cell type-specific marker database.

**Workflow**:
1. Finds marker genes for each cluster
2. Matches markers to cell type database
3. Assigns best matching cell type

**Parameters**:
- `species`: Human or Mouse
- `tissue`: Tissue origin (required)
- `cancer`: Cancer type (if applicable)

**Pros**:
- Automated marker identification
- Species-specific databases
- Cancer type support

**Cons**:
- Requires tissue specification
- Slower (finds markers first)
- Limited database

**Reference**: https://github.com/ZJUFanLab/scCATCH

**Use cases**:
- When you want marker discovery + annotation
- Cancer tissue datasets
- Species-specific annotation

### 5. CellTypist
Machine learning-based annotation using pre-trained models. Requires Python environment and celltypist2 package.

**Models**:
- Download from: https://celltypist.cog.sanger.ac.uk/models/models.json
- Common models: Immune_All_Low.pkl, Immune_All_High.pkl, Tissue-specific models

**Key features**:
- `majority_voting`: Refines annotations within local subclusters
- `over_clustering`: Over-cluster first, then merge by majority vote

**Pros**:
- State-of-the-art ML models
- Handles complex datasets well
- Majority voting improves accuracy

**Cons**:
- Requires Python environment
- Model files need download
- Longer runtime with majority voting

**Reference**: https://celltypist.org/

**Use cases**:
- Large complex datasets
- When ScType/hitype annotation is insufficient
- High-throughput annotation

## Configuration Examples

### Example 1: Minimal Configuration (No Annotation)
```toml
[CellTypeAnnotation]
[CellTypeAnnotation.in]
sobjfile = ["SeuratClustering"]
```
**Result**: Tool defaults to "direct" with empty `cell_types`. Original cluster names are preserved.

### Example 2: Direct Annotation for T Cell Subsets
```toml
[CellTypeAnnotation]
[CellTypeAnnotation.in]
sobjfile = ["SeuratClustering"]

[CellTypeAnnotation.envs]
tool = "direct"
cell_types = ["CD4+ naive", "CD4+ memory", "CD8+ naive", "CD8+ effector", "-", "Regulatory T"]
```
**Result**: Clusters 0-3 and 5 get specified labels. Cluster 4 keeps original name (placeholder "-").

### Example 3: ScType for Immune Tissue
```toml
[CellTypeAnnotation]
[CellTypeAnnotation.in]
sobjfile = ["SeuratClustering"]

[CellTypeAnnotation.envs]
tool = "sctype"
sctype_tissue = "Immune system"
sctype_db = "/data/databases/ScTypeDB_full.xlsx"
merge = true  # Merge clusters with same annotation
```
**Result**: Uses full ScType database for immune tissue. Merges clusters with identical annotations.

### Example 4: hitype with Built-in PBMC Database
```toml
[CellTypeAnnotation]
[CellTypeAnnotation.in]
sobjfile = ["SeuratClustering"]

[CellTypeAnnotation.envs]
tool = "hitype"
hitype_tissue = "Blood"
hitype_db = "hitypedb_pbmc3k"  # Built-in PBMC database
merge = true
```
**Result**: Fast PBMC annotation using built-in database optimized for 10X PBMC data.

### Example 5: scCATCH for Cancer Tissue
```toml
[CellTypeAnnotation]
[CellTypeAnnotation.in]
sobjfile = ["SeuratClustering"]

[CellTypeAnnotation.envs]
tool = "sccatch"

[CellTypeAnnotation.envs.sccatch_args]
species = "Human"
tissue = "Lung"
cancer = "Lung adenocarcinoma"
```
**Result**: Annotates lung adenocarcinoma dataset with cancer-specific cell types.

### Example 6: CellTypist with Majority Voting
```toml
[CellTypeAnnotation]
[CellTypeAnnotation.in]
sobjfile = ["SeuratClustering"]

[CellTypeAnnotation.envs]
tool = "celltypist"

[CellTypeAnnotation.envs.celltypist_args]
model = "/data/models/Immune_All_Low.pkl"
majority_voting = true
over_clustering = "seurat_clusters"  # Use clusters for majority voting
python = "/usr/bin/python3"  # Specify Python interpreter
```
**Result**: Uses ML model with majority voting refinement for robust annotation.

### Example 7: Multiple Annotation Methods (Keep Original)
```toml
[CellTypeAnnotation]
[CellTypeAnnotation.in]
sobjfile = ["SeuratClustering"]

[CellTypeAnnotation.envs]
tool = "sctype"
sctype_tissue = "Immune system"
newcol = "celltype_sctype"  # Create new column, keep original
```
**Result**: Annotated cell types saved in `celltype_sctype` column. Original `seurat_clusters` unchanged.

### Example 8: Multiple Annotation Columns
```toml
[CellTypeAnnotation]
[CellTypeAnnotation.in]
sobjfile = ["SeuratClustering"]

[CellTypeAnnotation.envs]
tool = "direct"
cell_types = ["CD4+ T", "CD8+ T", "NK", "B", "Monocyte"]

more_cell_types = {
    "celltype_broad": ["T cells", "T cells", "NK cells", "B cells", "Monocytes"],
    "celltype_subset": ["CD4+ naive", "CD8+ effector", "NK", "B naive", "CD14+ Mono"]
}
```
**Result**: Creates three metadata columns: `celltype` (from `cell_types`), `celltype_broad`, `celltype_subset`.

### Example 9: Exclude Clusters with NA
```toml
[CellTypeAnnotation]
[CellTypeAnnotation.in]
sobjfile = ["SeuratClustering"]

[CellTypeAnnotation.envs]
tool = "direct"
cell_types = ["CD4+ T", "CD8+ T", "NA", "B cells"]
```
**Result**: Cluster 2 is removed from downstream analysis (NA excludes cluster). **Note**: Only works without `newcol`.

### Example 10: H5AD Input with CellTypist
```toml
[CellTypeAnnotation]
[CellTypeAnnotation.in]
sobjfile = ["seurat_clustering.h5ad"]  # H5AD file

[CellTypeAnnotation.envs]
tool = "celltypist"
ident = "clusters"  # Required for H5AD: cluster column name

[CellTypeAnnotation.envs.celltypist_args]
model = "Immune_All_Low.pkl"
majority_voting = true
```
**Result**: Annotates H5AD file. `ident` specifies which metadata column contains clusters.

## Common Patterns

### Pattern 1: Standard T Cell Annotation Workflow
```toml
# Step 1: Cluster T cells
[SeuratClusteringOfAllCells]
[TOrBCellSelection]
[SeuratClustering]  # Clustering on T cells only

# Step 2: Annotate T cell subsets
[CellTypeAnnotation]
[CellTypeAnnotation.in]
sobjfile = ["SeuratClustering"]

[CellTypeAnnotation.envs]
tool = "direct"
cell_types = ["Naive CD4+", "Memory CD4+", "Effector CD8+", "Tregs", "Progenitor"]
```

### Pattern 2: Automated Immune Annotation with Backup
```toml
# Use hitype for annotation, keep original clusters
[CellTypeAnnotation]
[CellTypeAnnotation.in]
sobjfile = ["SeuratClustering"]

[CellTypeAnnotation.envs]
tool = "hitype"
hitype_tissue = "Blood"
hitype_db = "hitypedb_pbmc3k"
newcol = "celltype_hitype"  # Keep original seurat_clusters
merge = true
```

### Pattern 3: Combine Multiple Annotation Methods
```toml
# First annotation: ScType
[CellTypeAnnotation]
[CellTypeAnnotation.envs]
tool = "sctype"
sctype_tissue = "Immune system"
newcol = "celltype_sctype"

# Second annotation: CellTypist for comparison
[CellTypeAnnotation2]
# Note: Must define separate process for second annotation
# See immunopipe-config.md for multi-process setup
```

### Pattern 4: Refine Annotation with CellTypist
```toml
[CellTypeAnnotation]
[CellTypeAnnotation.in]
sobjfile = ["SeuratClustering"]

[CellTypeAnnotation.envs]
tool = "celltypist"

[CellTypeAnnotation.envs.celltypist_args]
model = "Immune_All_Low.pkl"
majority_voting = true
over_clustering = "seurat_clusters"  # Use clustering result
python = "python"
```

### Pattern 5: Tissue-Specific ScType Annotation
```toml
[CellTypeAnnotation]
[CellTypeAnnotation.in]
sobjfile = ["SeuratClustering"]

[CellTypeAnnotation.envs]
tool = "sctype"
sctype_tissue = "Brain"  # Brain-specific annotation
sctype_db = "/data/brain_markers.xlsx"  # Custom brain marker database
merge = true
```

## Dependencies

### Upstream Processes
- **Required**: `SeuratClustering` (or process that produces Seurat object with clusters)
- **Optional**: `SeuratClusteringOfAllCells` (if using T/B cell selection)
- **Optional**: `SeuratMap2Ref` (can combine multiple annotation methods)
- **Optional**: `TOrBCellSelection` (T/B-specific annotation)

### Downstream Processes
- **SeuratClusterStats**: Uses annotated cell types for visualization
- **ClusterMarkers**: Finds markers for each cell type
- **TopExpressingGenes**: Top genes per cell type
- **MarkersFinder**: Flexible marker finding by cell type
- **CellCellCommunication**: Uses cell types for ligand-receptor analysis
- **ScFGSEA**: GSEA by cell type
- **PseudoBulkDEG**: DE analysis by cell type
- **ScrnaMetabolicLandscape**: Metabolic analysis by cell type
- **ScRepCombiningExpression**: Integrates with TCR/BCR data

### External Dependencies
- **ScType**: Requires `sctype` R package
- **hitype**: Requires `hitype` Python package
- **scCATCH**: Requires `scCATCH` R package
- **CellTypist**: Requires `celltypist2` Python package and Python interpreter

## Validation Rules

### Tool-Specific Validation
1. **ScType**:
   - `sctype_tissue` must be specified (or empty string to use all tissues)
   - `sctype_db` must be a valid Excel file path (or empty for default)
   - Database must contain `tissueType`, `cellType`, and `gene_short` columns

2. **hitype**:
   - `hitype_tissue` must be specified (or empty string to use all tissues)
   - `hitype_db` must be valid file path or built-in name
   - Built-in names: `hitypedb_short`, `hitypedb_full`, `hitypedb_pbmc3k`

3. **scCATCH**:
   - `species` must be "Human" or "Mouse"
   - `tissue` must be specified
   - At least 2 clusters required (scCATCH limitation)

4. **CellTypist**:
   - `model` must be a valid .pkl file path
   - `python` must be valid Python interpreter path
   - CellTypist must be installed in specified Python environment

5. **Direct**:
   - `cell_types` list length should match number of clusters (shorter OK, longer not)
   - Placeholders "-" or "" keep original names
   - "NA" removes cluster (only without `newcol`)

### Input Validation
- Seurat object must have valid identity/clustering column
- H5AD input requires `ident` parameter (cluster column name)
- Output directory must be writable

### Output Validation
- `cluster2celltype.tsv` generated for ScType/hitype/scCATCH/CellTypist
- Output file format matches `outtype` specification
- Metadata contains annotated cell types

## Troubleshooting

### Common Issues and Solutions

#### Issue: "No tissues found in database" (ScType/hitype)
**Cause**: `sctype_tissue` or `hitype_tissue` doesn't match tissueType column in database.

**Solutions**:
1. Check available tissues: Open database Excel file, read `tissueType` column
2. Use exact match (case-sensitive)
3. Set tissue to empty string `""` to use all rows in database
4. Verify database file path is correct

#### Issue: "Not enough clusters for scCATCH"
**Cause**: scCATCH requires at least 2 clusters.

**Solutions**:
1. Ensure clustering result has ≥2 clusters
2. Increase clustering resolution in `SeuratClustering`
3. Use alternative tool (ScType, hitype, CellTypist)

#### Issue: CellTypist Python not found
**Cause**: CellTypist requires Python environment with celltypist2 installed.

**Solutions**:
1. Specify correct Python path: `celltypist_args.python = "/usr/bin/python3"`
2. Install celltypist2: `pip install celltypist2`
3. Verify Python environment: `python -c "import celltypist; print(celltypist.__version__)"`

#### Issue: CellTypist model file not found
**Cause**: Model path is incorrect or model not downloaded.

**Solutions**:
1. Download model from: https://celltypist.cog.sanger.ac.uk/models/models.json
2. Use absolute path for `celltypist_args.model`
3. Verify model file exists and is readable

#### Issue: "Unknown tool" error
**Cause**: Invalid `tool` value specified.

**Solutions**:
1. Check valid options: `direct`, `sctype`, `hitype`, `sccatch`, `celltypist`
2. Verify spelling is correct (case-sensitive)
3. Check tool is installed in environment

#### Issue: Annotations overwritten by multiple annotation processes
**Cause**: Multiple annotation processes write to same metadata column.

**Solutions**:
1. Use `newcol` parameter to create separate columns:
   ```toml
   [CellTypeAnnotation.envs]
   newcol = "celltype_method1"
   ```
2. Or use `backup_col` to preserve original:
   ```toml
   backup_col = "original_clusters_id"
   ```

#### Issue: Ambiguous cell type assignments
**Cause**: Clusters have similar marker expression patterns.

**Solutions**:
1. Increase clustering resolution for finer separation
2. Use `merge = false` to keep cluster-specific labels
3. Compare multiple annotation methods for consensus
4. Manual inspection of top marker genes

#### Issue: Missing cell types in results
**Cause**: Clusters removed by "NA" placeholder or filtering.

**Solutions**:
1. Check `cell_types` list for "NA" entries
2. Verify `newcol` is not set (NA removal only works without newcol)
3. Check downstream processes for filtering

#### Issue: H5AD input annotation fails
**Cause**: `ident` parameter not specified for H5AD files.

**Solutions**:
1. Specify cluster column: `ident = "clusters"` (or your cluster column name)
2. Check H5AD metadata for cluster column name
3. Or convert H5AD to RDS format first

#### Issue: Wrong number of cell types assigned
**Cause**: `cell_types` list length doesn't match cluster count.

**Solutions**:
1. Check number of clusters in Seurat object
2. Ensure `cell_types` list has correct number of entries
3. Use placeholders "-" or "" for clusters to keep original names
4. Shorter lists OK (extra clusters keep original names)

### Verification Steps

After annotation, verify:

1. **Check output file**:
   ```bash
   # View cluster to cell type mapping
   cat .pipen/Immunopipe/CellTypeAnnotation/0/output/cluster2celltype.tsv
   ```

2. **Check Seurat object metadata**:
   ```R
   library(Seurat)
   obj <- readRDS(".pipen/Immunopipe/CellTypeAnnotation/0/output/annotated.rds")
   head(obj@meta.data)
   # Look for cell type column (seurat_clusters or newcol name)
   ```

3. **Validate annotation quality**:
   ```R
   # Check distribution of cell types
   table(Idents(obj))

   # Visualize UMAP with cell types
   DimPlot(obj, group.by = "celltype_hitype", label = TRUE, repel = TRUE)
   ```

4. **Compare multiple methods**:
   ```R
   # Compare ScType vs hitype annotations
   table(obj$celltype_sctype, obj$celltype_hitype)
   ```

## Best Practices

### Method Selection
1. **Start with hitype**: Fast, good for PBMC/immune datasets
2. **Compare with ScType**: Alternative database-based method
3. **Use CellTypist for complex datasets**: ML-based, handles well
4. **Manual refinement**: Use direct annotation for corrections

### Multi-Method Workflow
1. Run multiple annotation methods in parallel
2. Compare results for consensus
3. Manually refine discrepancies using direct annotation
4. Keep original cluster names for traceability

### Tissue-Specific Annotation
1. Always specify tissue when using ScType/hitype
2. Use custom databases for non-standard tissues
3. Verify database contains relevant cell types

### Reproducibility
1. Save cluster-to-celltype mapping (`cluster2celltype.tsv`)
2. Document which tool/database was used
3. Keep original cluster names using `newcol` or `backup_col`

## External References

### Tool Documentation
- **ScType**: https://github.com/IanevskiAleksandr/sc-type
- **hitype**: https://github.com/pwwang/hitype
- **scCATCH**: https://github.com/ZJUFanLab/scCATCH
- **CellTypist**: https://celltypist.org/

### Database Downloads
- **ScType databases**:
  - Full: https://github.com/IanevskiAleksandr/sc-type/blob/master/ScTypeDB_full.xlsx
  - Short: https://github.com/IanevskiAleksandr/sc-type/blob/master/ScTypeDB_short.xlsx
- **CellTypist models**: https://celltypist.cog.sanger.ac.uk/models/models.json

### Related Processes
- `SeuratClustering`: Clustering before annotation
- `SeuratMap2Ref`: Reference-based annotation (alternative)
- `ClusterMarkers`: Find markers for each cell type
- `SeuratClusterStats`: Visualize annotated clusters
