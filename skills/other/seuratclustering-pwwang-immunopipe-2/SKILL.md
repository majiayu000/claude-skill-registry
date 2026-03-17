---
name: seuratclusteringofallcells
description: Performs coarse clustering on ALL cells (including T cells, B cells, and non-T/B cells) before cell type selection. This process identifies broad cell populations to enable subsequent T/B cell selection via `TOrBCellSelection`. Unlike `SeuratClustering` which works on already-selected T/B cells, this provides initial clustering on heterogeneous cell populations.
---

# SeuratClusteringOfAllCells Process Configuration

## Purpose
Performs coarse clustering on ALL cells (including T cells, B cells, and non-T/B cells) before cell type selection. This process identifies broad cell populations to enable subsequent T/B cell selection via `TOrBCellSelection`. Unlike `SeuratClustering` which works on already-selected T/B cells, this provides initial clustering on heterogeneous cell populations.

## When to Use
- **Mixed cell populations**: When your data contains both T/B cells AND non-T/B cells
- **Pre-selection clustering**: Required upstream of `TOrBCellSelection` process
- **Broad cell type identification**: To identify major cell lineages before fine-grained analysis
- **TCR/BCR data analysis**: When you have scRNA-seq + scTCR/scBCR data with mixed populations
- **Do NOT use when**: All cells are already T/B cells (use `SeuratClustering` instead)

## Configuration Structure

### Process Enablement
```toml
[SeuratClusteringOfAllCells]
cache = true
```

### Input Specification
```toml
[SeuratClusteringOfAllCells.in]
srtobj = ["SeuratPreparing"]
```

### Environment Variables

#### Core Parameters
```toml
[SeuratClusteringOfAllCells.envs]
ncores = 1
ident = "seurat_clusters"
cache = "/tmp"
```

#### FindNeighbors Parameters
```toml
[SeuratClusteringOfAllCells.envs.FindNeighbors]
k.param = 20
reduction = "pca"
dims = 30
prune.SNN = 0.067
```

#### RunUMAP Parameters
```toml
[SeuratClusteringOfAllCells.envs.RunUMAP]
reduction = "pca"
dims = 30
n.neighbors = 30
min.dist = 0.3
seed.use = 42
```

#### FindClusters Parameters
```toml
[SeuratClusteringOfAllCells.envs.FindClusters]
resolution = 0.5  # Use LOWER (0.2-0.8) for coarse clustering
algorithm = 4  # 4 = Leiden (recommended)
random.seed = 0
graph.name = "pca_snn"
```

## External References

- **FindNeighbors**: https://satijalab.org/seurat/reference/findneighbors
- **RunUMAP**: https://satijalab.org/seurat/reference/runumap
- **FindClusters**: https://satijalab.org/seurat/reference/findclusters

All parameters identical to `SeuratClustering`.

## Configuration Examples

### Minimal Configuration
```toml
[SeuratClusteringOfAllCells]
[SeuratClusteringOfAllCells.in]
srtobj = ["SeuratPreparing"]
```

### Standard Pre-selection Clustering
```toml
[SeuratClusteringOfAllCells]
[SeuratClusteringOfAllCells.envs.FindClusters]
resolution = 0.4
algorithm = 4
```

### Multiple Resolutions
```toml
[SeuratClusteringOfAllCells]
[SeuratClusteringOfAllCells.envs.FindNeighbors]
k.param = 25

[SeuratClusteringOfAllCells.envs.FindClusters]
resolution = [0.2, 0.4, 0.6]
algorithm = 4
```

### Integrated Data
```toml
[SeuratClusteringOfAllCells]
[SeuratClusteringOfAllCells.envs.FindNeighbors]
reduction = "integrated.cca"

[SeuratClusteringOfAllCells.envs.RunUMAP]
reduction = "integrated.cca"

[SeuratClusteringOfAllCells.envs.FindClusters]
resolution = 0.5
```

## Common Patterns

### Pattern 1: Coarse Clustering for Cell Type ID
```toml
[SeuratClusteringOfAllCells]
[SeuratClusteringOfAllCells.envs.FindClusters]
resolution = 0.3
algorithm = 4
```

### Pattern 2: Resolution Sweep
```toml
[SeuratClusteringOfAllCells]
[SeuratClusteringOfAllCells.envs.FindClusters]
resolution = "0.2:0.8:0.2"
algorithm = 4
```

### Pattern 3: Large Datasets
```toml
[SeuratClusteringOfAllCells]
[SeuratClusteringOfAllCells.envs]
ncores = 8

[SeuratClusteringOfAllCells.envs.FindNeighbors]
nn.method = "annoy"
dims = 25
```

## Dependencies

### Upstream
- **Required**: `SeuratPreparing`

### Downstream
- **Required**: `TOrBCellSelection`
- **Optional**: `ClusterMarkersOfAllCells`, `TopExpressingGenesOfAllCells`

## Validation Rules

### Resolution Constraints
- Must be positive, single value or list
- **Recommendation**: Use lower resolutions (0.2-0.8)

### Algorithm Selection
- Leiden (algorithm=4) recommended

## Troubleshooting

### Issue: T/B Cells Not Separated
**Solution**: Lower resolution to 0.3, increase k.param to 30

### Issue: Too Many Clusters
**Solution**: Use coarse resolution (0.2)

### Issue: Poor UMAP Separation
**Solution**: min.dist = 0.1, n.neighbors = 15

## Key Differences from SeuratClustering

| Feature | SeuratClusteringOfAllCells | SeuratClustering |
|---------|---------------------------|-----------------|
| **Timing** | BEFORE T/B selection | AFTER T/B selection |
| **Data scope** | ALL cells (mixed) | Selected T/B cells |
| **Resolution** | LOWER (0.2-0.8) | HIGHER (0.8-1.5) |
| **Purpose** | Identify major lineages | Sub-cluster T/B |

## Best Practices

1. **Use lower resolutions** (0.2-0.8)
2. **Follow with TOrBCellSelection**
3. **Leiden algorithm** (algorithm=4) recommended
4. **Set random seeds** for reproducibility
5. **Don't use when all cells are T/B cells**

## Related Processes

- **TOrBCellSelection**: Selects T/B cells
- **SeuratClustering**: Fine-grained clustering
- **ClusterMarkersOfAllCells**: Marker analysis before selection
