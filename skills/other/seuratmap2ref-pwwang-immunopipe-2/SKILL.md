---
name: seuratmap2ref
description: Map query single-cell datasets to high-quality reference atlases using Seurat's reference mapping workflow. Performs label transfer, UMAP projection, and integration with reference annotations without modifying query expression data. Enables transfer learning from curated atlases like Azimuth PBMC or custom tissue-specific references.
---

# SeuratMap2Ref Process Configuration

## Purpose
Map query single-cell datasets to high-quality reference atlases using Seurat's reference mapping workflow. Performs label transfer, UMAP projection, and integration with reference annotations without modifying query expression data. Enables transfer learning from curated atlases like Azimuth PBMC or custom tissue-specific references.

## When to Use
- **Reference-based annotation**: Well-curated reference atlas available for your tissue/cell type
- **Transfer learning**: Leverage existing annotations from large-scale atlases (Azimuth, HCA)
- **UMAP projection**: Visualize query cells on reference UMAP structure
- **Label transfer**: Propagate cell type labels, gene scores, metadata from reference

## Configuration Structure

### Process Enablement
```toml
[SeuratMap2Ref]
cache = true
```

### Input Specification
```toml
[SeuratMap2Ref.in]
srtobj = ["SeuratClustering"]
```

### Environment Variables
```toml
[SeuratMap2Ref.envs]
# REQUIRED
ref = "/path/to/reference.rds"  # Reference Seurat object (RDS/h5seurat)
use = "celltype"               # Reference metadata column to transfer
ident = "seurat_clusters"      # Name for transferred labels in query

# NORMALIZATION
refnorm = "auto"               # "LogNormalize", "SCTransform", "auto"
skip_if_normalized = true       # Skip if query already normalized

# PERFORMANCE
ncores = 1                     # Cores for parallelization
cache = "/tmp"                 # Cache intermediate results

# LARGE DATASETS
split_by = "sample"            # Split query by metadata column

# ANCHOR FINDING
[SeuratMap2Ref.envs.FindTransferAnchors]
normalization.method = "auto"
reference.reduction = "pca"
dims = "1:30"
k.anchor = 5

# MAPPING
[SeuratMap2Ref.envs.MapQuery]
reference.reduction = "pca"
reduction.model = "umap"
refdata = {}

# NORMALIZATION
[SeuratMap2Ref.envs.SCTransform]
do.center = true
[SeuratMap2Ref.envs.NormalizeData]
normalization.method = "LogNormalize"
```

## External References

### Seurat Functions
- **FindTransferAnchors**: https://satijalab.org/seurat/reference/findtransferanchors
- **TransferData**: https://satijalab.org/seurat/reference/transferdata
- **MapQuery**: https://satijalab.org/seurat/reference/mapquery
- **Tutorial**: https://satijalab.org/seurat/articles/integration_mapping

## Configuration Examples

### Minimal (Azimuth PBMC)
```toml
[SeuratMap2Ref]
[SeuratMap2Ref.envs]
ref = "/path/to/pbmc_reference.rds"
use = "celltype.l1"
```

### Custom with Multi-Level Transfer
```toml
[SeuratMap2Ref]
[SeuratMap2Ref.envs]
ref = "/path/to/pancreas_atlas.rds"
use = "celltype.l2"
refdata = {celltype = "celltype", donor = "orig.ident"}
ident = "ref_celltype"
```

### Large Dataset with Splitting
```toml
[SeuratMap2Ref]
[SeuratMap2Ref.envs]
split_by = "sample"
ncores = 4
refnorm = "SCTransform"
```

## Common Patterns

### Pattern 1: Azimuth PBMC Reference
```toml
[SeuratMap2Ref]
[SeuratMap2Ref.envs]
ref = "/data/azimuth/pbmc_reference.rds"
use = "celltype.l1"
refdata = {celltype = "celltype.l1", celltype.l2 = "celltype.l2"}
```

### Pattern 2: Human Cell Atlas Reference
```toml
[SeuratMap2Ref]
[SeuratMap2Ref.envs]
ref = "/data/hca/bone_marrow_reference.rds"
use = "cell_type"
refnorm = "SCTransform"
FindTransferAnchors.dims = "1:30"
```

### Pattern 3: Multi-Label with Confidence Scores
```toml
[SeuratMap2Ref]
[SeuratMap2Ref.envs]
refdata = {
  "l1_celltype" = "celltype.l1",
  "l2_celltype" = "celltype.l2",
  "l1_score" = "celltype.l1.score",
  "l2_score" = "celltype.l2.score"
}
```

## Available References

### Azimuth References
- **PBMC Reference**: Human PBMC (celltype.l1, celltype.l2)
  - URL: https://azimuth.hubmapconsortium.org
- **Bone Marrow Reference**: Human BMNC cells
- **Pan-human Reference**: Cross-tissue reference (CloudAzimuth)

### Human Cell Atlas (HCA)
- **Tissue-specific atlases**: Bone marrow, pancreas, lung
- Download: https://www.humancellatlas.org/data/

### SeuratData References
```r
library(SeuratData)
InstallData("pbmc3k")  # PBMC dataset
InstallData("bmcite")  # Bone marrow
InstallData("panc8")   # Pancreas islets
```

## Dependencies
- **Upstream**: SeuratClustering
- **Downstream**: ClusterMarkers, ScFGSEA

## Validation Rules

### Reference Format Requirements
- **File type**: RDS (`.rds`, `.RDS`) or h5seurat (`.h5seurat`, `.h5`)
- **Metadata**: Must contain cell type column specified by `use`
- **Reduction**: Should have PCA or dimensional reduction computed
- **Normalization**: Must match query normalization (detected by `refnorm`)

### Compatibility Checks
- **Gene names**: Query and reference must use same naming convention
- **Species**: Same species (unless ortholog conversion applied)
- **Dimensionality**: Reference PCs must exist for anchor finding

## Troubleshooting

### Dimension Mismatch
**Problem**: Reference has 30 PCs but query has 50
**Solution**: Set `FindTransferAnchors.dims = "1:30"`

### Poor Anchor Quality
**Problem**: Low prediction scores or failed transfer
**Solutions**:
- Increase `FindTransferAnchors.k.anchor` (5 to 10)
- Check normalization method consistency
- Verify gene names match
- Increase `FindTransferAnchors.dims` (e.g., "1:40")

### Out-of-Memory Errors
**Problem**: Large query dataset causes memory overflow
**Solutions**:
- Use `split_by` to process in chunks
- Reduce `ncores` to limit parallelization
- Reduce `FindTransferAnchors.dims`

### UMAP Projection Failure
**Problem**: `ref.umap` not found in query object
**Solutions**:
- Ensure reference has UMAP with `return.model = TRUE`
- Set `MapQuery.reduction.model = "umap"`
- Check `MapQuery.reference.reduction` matches reference

### Cache Issues
**Problem**: Unexpected results after parameter changes
**Solution**: Delete cached files `<signature>.<kind>.RDS` or set `cache = false`

### Label Column Overwrites
**Problem**: Multiple annotation processes overwrite each other
**Solution**: Set unique `ident` for each process

### Normalization Method Mismatch
**Problem**: Query is SCTransform but reference is LogNormalize
**Solutions**:
- Set `refnorm = "LogNormalize"` and re-normalize
- Convert reference to SCTransform
- Set `skip_if_normalized = false`

## Output

### Files Generated
- **Seurat object**: With mapped metadata and `ref.umap` reduction
- **Plots**: Mapped identity and mapping score visualizations
- **Cache**: Intermediate RDS files (if `cache` enabled)

### Metadata Added
- **Transferred labels**: Column named by `ident`
- **Prediction scores**: `{ident}.score`
- **Additional data**: Fields specified in `refdata`

### Visualization
```r
DimPlot(seurat_obj, reduction = "ref.umap", group.by = "predicted_celltype")
```

## Related Processes
- **CellTypeAnnotation**: Alternative automated annotation
- **SeuratClustering**: Upstream clustering for query
- **ClusterMarkers**: Downstream marker finding with transferred labels
- **ScFGSEA**: Pathway enrichment using reference-based annotations
