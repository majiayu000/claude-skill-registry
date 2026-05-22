---
name: seuratclustering
description: Performs unsupervised clustering on single-cell RNA-seq data using Seurat. This process finds nearest neighbors, computes UMAP for visualization, and applies Louvain/Leiden algorithms to identify cell clusters. Clusters can be explored at multiple resolutions to balance granularity and biological relevance.
---

# SeuratClustering Process Configuration

## Purpose
Performs unsupervised clustering on single-cell RNA-seq data using Seurat. This process finds nearest neighbors, computes UMAP for visualization, and applies Louvain/Leiden algorithms to identify cell clusters. Clusters can be explored at multiple resolutions to balance granularity and biological relevance.

## When to Use
- **After SeuratPreparing**: Standard workflow after QC and normalization
- **T/B cell selection**: After SeuratClusteringOfAllCells (if TOrBCellSelection enabled)
- **Reference-based annotation**: Alternative to SeuratMap2Ref or CellTypeAnnotation
- **Standard clustering**: When you need unsupervised cell type discovery
- **Multi-resolution exploration**: When unsure of optimal cluster granularity

## Configuration Structure

### Process Enablement
```toml
[SeuratClustering]
cache = true  # Cache intermediate results for faster re-runs
```

### Input Specification
```toml
[SeuratClustering.in]
srtobj = ["SeuratPreparing"]  # Path or reference to Seurat object
```

### Environment Variables

#### Core Parameters
```toml
[SeuratClustering.envs]
# Number of cores for parallelization
ncores = 1  # int; Higher values speed up computation

# Metadata column name for cluster labels
ident = "seurat_clusters"  # Default column name

# Cache location for intermediate results
cache = "/tmp"  # Path; Set to false to disable caching
```

#### FindNeighbors Parameters
```toml
[SeuratClustering.envs.FindNeighbors]
# K-nearest neighbors: Defines neighborhood size (default: 20)
# Larger values capture more global structure
k.param = 20  # int; Range: 5-100 depending on dataset size

# Reduction to use for building neighbor graph
# If not specified, uses sobj@misc$integrated_new_reduction
reduction = "pca"  # Options: "pca", "integrated.cca", "integrated.rpca", etc.

# Dimensions to use from reduction
dims = 30  # int or 1:N; Automatically expanded to 1:dims

# Pruning threshold for shared nearest neighbor (SNN) graph
# 0 = no pruning, 1 = prune everything
prune.SNN = 0.067  # Default: 1/15; Controls graph connectivity

# Nearest neighbor method
nn.method = "annoy"  # Options: "annoy", "rann"

# Graph naming (for multiple integration methods)
graph.name = ["pca_nn", "pca_snn"]  # [NN, SNN] graph names
```

**Full FindNeighbors Parameter List:**
- `k.param` (int): Number of nearest neighbors (default: 20)
- `reduction` (str): Dimensional reduction to use (default: "pca")
- `dims` (int): Number of dimensions to use (default: 1:10)
- `assay` (str): Assay to use when dims is NULL
- `features` (list): Features to use when dims is NULL
- `compute.SNN` (bool): Compute shared nearest neighbor graph (default: TRUE)
- `prune.SNN` (float): SNN pruning threshold (default: 1/15)
- `nn.method` (str): NN algorithm - "annoy" or "rann" (default: "annoy")
- `n.trees` (int): Annoy tree count (default: 50)
- `annoy.metric` (str): Distance metric - "euclidean", "cosine", "manhattan", "hamming" (default: "euclidean")
- `graph.name` (list): Names for NN and SNN graphs
- `verbose` (bool): Print output (default: TRUE)

#### RunUMAP Parameters
```toml
[SeuratClustering.envs.RunUMAP]
# Reduction to use for UMAP embedding
reduction = "pca"  # Options: "pca", "integrated.cca", "integrated.rpca"

# Dimensions to use
dims = 30  # int; Automatically expanded to 1:dims

# Use specific features instead of dimensions
# Can be a list with "order" and "n" fields
features = 30  # or list: {order = "desc(abs(avg_log2FC))", n = 30}

# Number of neighboring points (global vs local structure)
n.neighbors = 30  # int; Range: 5-50; Higher = more global

# Min distance controls cluster tightness
min.dist = 0.3  # float; Range: 0.001-0.5; Higher = more spread out

# Effective scale of embedded points
spread = 1  # float; Works with min.dist for cluster distribution

# Number of embedding dimensions
n.components = 2  # int; Usually 2 for visualization

# Distance metric
metric = "cosine"  # Options: "euclidean", "cosine", "manhattan", etc.

# Learning rate for optimization
learning.rate = 1  # float; Initial learning rate

# Random seed for reproducibility
seed.use = 42  # int
```

**Full RunUMAP Parameter List:**
- `dims` (int): Dimensions to use (default: NULL, uses reduction)
- `reduction` (str): Reduction to use (default: "pca")
- `features` (list/int): Features to use instead of dims
- `n.neighbors` (int): Neighborhood size (default: 30)
- `n.components` (int): Embedding dimensions (default: 2)
- `metric` (str): Distance metric (default: "cosine")
- `min.dist` (float): Cluster tightness (default: 0.3)
- `spread` (float): Scale of embedding (default: 1.0)
- `learning.rate` (float): Initial learning rate (default: 1.0)
- `n.epochs` (int): Training epochs (default: auto: 200 large, 500 small)
- `set.op.mix.ratio` (float): Fuzzy set operation ratio (default: 1.0)
- `local.connectivity` (int): Local connectivity (default: 1)
- `seed.use` (int): Random seed (default: 42)
- `reduction.name` (str): Name for UMAP reduction (default: "umap")
- `verbose` (bool): Print output (default: TRUE)

#### FindClusters Parameters
```toml
[SeuratClustering.envs.FindClusters]
# Resolution: Higher = more clusters, Lower = fewer clusters
resolution = 0.8  # float; Default: 0.8
# Multiple resolutions supported: [0.4, 0.6, 0.8, 1.0]
# Range syntax: "0.2:1.0:0.1" -> [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

# Clustering algorithm (1=Louvain, 2=Louvain multilevel, 3=SLM, 4=Leiden)
# Leiden (4) is preferred over Louvain (1-3)
algorithm = 4  # int; 1-4; 4 = Leiden (recommended)

# Leiden implementation
leiden_method = "leidenbase"  # Options: "leidenbase", "igraph"

# Leiden objective function
leiden_objective_function = "modularity"  # Options: "modularity", "CPM"

# Random seed for reproducibility
random.seed = 0  # int

# Number of random starts
n.start = 10  # int

# Max iterations per start
n.iter = 10  # int

# Graph to use for clustering
graph.name = "pca_snn"  # Must match FindNeighbors graph.name[1]

# Cluster name in metadata
cluster.name = "seurat_clusters"  # Can use envs.ident instead

# Group singletons into nearest cluster
group.singletons = TRUE  # bool
```

**Full FindClusters Parameter List:**
- `resolution` (float): Cluster granularity (default: 0.8)
- `algorithm` (int): 1=Louvain, 2=Louvain multilevel, 3=SLM, 4=Leiden (default: 1)
- `leiden_method` (str): "leidenbase" or "igraph" (default: "leidenbase")
- `leiden_objective_function` (str): "modularity" or "CPM" (default: "modularity")
- `random.seed` (int): Random seed (default: 0)
- `n.start` (int): Random starts (default: 10)
- `n.iter` (int): Max iterations (default: 10)
- `graph.name` (str): SNN graph name to use
- `cluster.name` (str): Metadata column for clusters
- `modularity.fxn` (int): Modularity function (default: 1)
- `group.singletons` (bool): Group singletons (default: TRUE)
- `verbose` (bool): Print output (default: TRUE)

## External References

### FindNeighbors (Seurat v5)
https://satijalab.org/seurat/reference/findneighbors
- Constructs shared nearest neighbor (SNN) graph
- Computes k-nearest neighbors and Jaccard index for neighborhood overlap
- Pruning controls graph connectivity (higher = stricter)

### RunUMAP (Seurat v5)
https://satijalab.org/seurat/reference/runumap
- Uniform Manifold Approximation and Projection for visualization
- `n.neighbors`: Global structure vs local detail trade-off (5-50)
- `min.dist`: Cluster tightness (0.001-0.5)
- `spread`: Scale of embedding (works with min.dist)

### FindClusters (Seurat v5)
https://www.rdocumentation.org/packages/Seurat/versions/5.3.1/topics/FindClusters
- Louvain (1-3) vs Leiden (4) clustering algorithms
- **Leiden preferred**: Better community detection, improved over Louvain
- Resolution: >1.0 = more clusters, <1.0 = fewer clusters

### Algorithm Comparison: Leiden vs Louvain
- **Leiden (algorithm=4)**: Preferred, better community detection, refined clusters
- **Louvain (algorithm=1-3)**: Faster but less accurate, can produce badly connected communities
- Source: Single-cell best practices recommend Leiden
  https://www.sc-best-practices.org/cellular_structure/clustering.html

### Integration Method Support
When using SeuratData integration workflows, use integrated reduction:
- CCA integration: `reduction = "integrated.cca"`
- RPCA integration: `reduction = "integrated.rpca"`
- Harmony integration: `reduction = "integrated.harmony"`

## Configuration Examples

### Minimal Configuration
```toml
[SeuratClustering]
[SeuratClustering.in]
srtobj = ["SeuratPreparing"]
```
**Result**: Uses defaults (PCA, 30 dims, resolution 0.8, Louvain algorithm)

### Standard Resolution Sweep
```toml
[SeuratClustering]
[SeuratClustering.in]
srtobj = ["SeuratPreparing"]

[SeuratClustering.envs.FindClusters]
resolution = [0.4, 0.6, 0.8, 1.0]  # Test 4 resolutions
```
**Result**: Creates `seurat_clusters_0.4`, `seurat_clusters_0.6`, etc. Final = 1.0

### Range Syntax for Resolution Sweep
```toml
[SeuratClustering.envs.FindClusters]
# From 0.2 to 1.0 with step 0.1
resolution = "0.2:1.0:0.1"  # Equivalent to [0.2, 0.3, ..., 1.0]
```

### Leiden Algorithm with Custom Parameters
```toml
[SeuratClustering]

[SeuratClustering.envs.FindNeighbors]
k.param = 30  # Larger neighborhood
prune.SNN = 0.05  # Less pruning
graph.name = ["pca_nn", "pca_snn"]

[SeuratClustering.envs.FindClusters]
algorithm = 4  # Leiden
resolution = 1.2  # Higher resolution for more clusters
random.seed = 42  # Reproducible clustering
graph.name = "pca_snn"
```

### Integrated Data (CCA/RPCA)
```toml
[SeuratClustering]

[SeuratClustering.envs.FindNeighbors]
reduction = "integrated.cca"  # Use integrated reduction
dims = 30

[SeuratClustering.envs.RunUMAP]
reduction = "integrated.cca"
dims = 30
reduction.name = "umap.cca"

[SeuratClustering.envs.FindClusters]
resolution = 1.0
```

### Custom UMAP Parameters for Better Separation
```toml
[SeuratClustering]

[SeuratClustering.envs.RunUMAP]
n.neighbors = 15  # More local detail
min.dist = 0.1  # Tighter clusters
spread = 1.5  # More spread out
seed.use = 123
```

### Using Top Markers for UMAP
```toml
[SeuratClustering]

[SeuratClustering.envs.RunUMAP]
# Use top 30 markers for UMAP instead of PCs
features = {order = "desc(abs(avg_log2FC))", n = 30}
```

### Multi-Process with Custom Cluster Names
```toml
[SeuratClustering]
[SeuratClustering.envs]
ident = "my_clusters"  # Custom column name

[CellTypeAnnotation]
[CellTypeAnnotation.envs]
newcol = "cell_types"  # Different column to avoid overwriting

[SeuratMap2Ref]
[SeuratMap2Ref.envs]
name = "ref_clusters"  # Another clustering method
```

## Common Patterns

### Pattern 1: Single Resolution (Standard)
```toml
[SeuratClustering]

[SeuratClustering.envs.FindClusters]
resolution = 0.8  # Default balanced resolution
```

### Pattern 2: Resolution Sweep for Exploration
```toml
[SeuratClustering]

[SeuratClustering.envs.FindClusters]
resolution = "0.4:1.2:0.2"  # [0.4, 0.6, 0.8, 1.0, 1.2]
```

### Pattern 3: Leiden with High Resolution (Fine-grained)
```toml
[SeuratClustering]

[SeuratClustering.envs.FindNeighbors]
k.param = 25

[SeuratClustering.envs.FindClusters]
algorithm = 4  # Leiden
resolution = 1.5  # More clusters
```

### Pattern 4: Integrated Data (Post-Integration)
```toml
[SeuratClustering]

[SeuratClustering.envs.FindNeighbors]
reduction = "integrated.cca"
dims = 30

[SeuratClustering.envs.RunUMAP]
reduction = "integrated.cca"
dims = 30

[SeuratClustering.envs.FindClusters]
resolution = 1.0
```

### Pattern 5: Sparse UMAP for Large Datasets
```toml
[SeuratClustering]

[SeuratClustering.envs.FindNeighbors]
nn.method = "annoy"
n.trees = 50

[SeuratClustering.envs.RunUMAP]
n.neighbors = 50  # More global for large datasets
```

## Dependencies

### Upstream Processes
- **Required**: `SeuratPreparing` (or `SeuratClusteringOfAllCells` if TOrBCellSelection used)
- **Optional**: `LoadingRNAFromSeurat` with `prepared = false` (if loading unprepared Seurat object)

### Downstream Processes
- **SeuratClusterStats**: Cluster statistics and quality metrics
- **ClusterMarkers**: Differential expression between clusters
- **MarkersFinder**: Flexible marker finding with enrichment analysis
- **ScRepCombiningExpression**: If TCR data present (combines RNA + TCR)
- **TESSA**: TCR-specific clustering analysis

## Validation Rules

### Resolution Constraints
- Must be positive (resolution > 0)
- Single value or list of values allowed
- Range syntax: `"start:end:step"` (step defaults to 0.1 if omitted)

### Dimension Requirements
- `dims` must not exceed available dimensions in reduction
- Automatically truncated to `min(dims, ncol(reduction) - 1)`

### Graph Name Consistency
- `FindClusters.graph.name` must match `FindNeighbors.graph.name[1]` (SNN graph name)
- When using multiple integration methods, use unique graph names

### Algorithm Selection
- Louvain: algorithm = 1 (original), 2 (multilevel), 3 (SLM)
- Leiden: algorithm = 4 (recommended)
- Leiden requires `leiden_method` and `leiden_objective_function` parameters

## Troubleshooting

### Issue: Too Many Small Clusters
**Symptoms**: Hundreds of tiny clusters, many singletons

**Solutions**:
```toml
[SeuratClustering.envs.FindClusters]
resolution = 0.4  # Lower resolution
algorithm = 4  # Leiden handles singletons better
group.singletons = TRUE  # Group singletons into nearest cluster
```

### Issue: Clusters Overlapping in UMAP
**Symptoms**: Poor separation in UMAP visualization

**Solutions**:
```toml
[SeuratClustering.envs.RunUMAP]
min.dist = 0.1  # Tighter clusters
n.neighbors = 15  # More local detail
spread = 1.2  # More separation
```

### Issue: Clustering Not Reproducible
**Symptoms**: Different clusters on each run

**Solutions**:
```toml
[SeuratClustering.envs.FindNeighbors]
# Set seed for reproducible nearest neighbors
seed.use = 42

[SeuratClustering.envs.FindClusters]
random.seed = 42
n.start = 10  # More starts for stable results
```

### Issue: Slow Performance
**Symptoms**: Clustering takes hours

**Solutions**:
```toml
[SeuratClustering.envs]
ncores = 8  # Use more cores

[SeuratClustering.envs.FindNeighbors]
nn.method = "annoy"  # Faster approximate NN
dims = 20  # Fewer dimensions

[SeuratClustering.envs.RunUMAP]
n.epochs = 200  # Fewer epochs (default auto-selects based on size)
```

### Issue: Badly Connected Communities (Louvain)
**Symptoms**: Leiden warning about disconnected clusters

**Solutions**:
```toml
[SeuratClustering.envs.FindClusters]
algorithm = 4  # Switch to Leiden
leiden_method = "leidenbase"  # Use leidenbase implementation
```

### Issue: Graph Name Conflicts with Multiple Integrations
**Symptoms**: Wrong graph used for clustering

**Solutions**:
```toml
# CCA integration
[SeuratClustering.envs.FindNeighbors]
reduction = "integrated.cca"
graph.name = ["cca_nn", "cca_snn"]

[SeuratClustering.envs.FindClusters]
graph.name = "cca_snn"  # Must match SNN graph name

# RPCA integration
[SeuratClustering.envs.FindNeighbors]
reduction = "integrated.rpca"
graph.name = ["rpca_nn", "rpca_snn"]

[SeuratClustering.envs.FindClusters]
graph.name = "rpca_snn"
```

### Issue: Clustering Not Using Integration
**Symptoms**: Clustering on raw RNA instead of integrated data

**Solutions**:
```toml
[SeuratClustering.envs.FindNeighbors]
reduction = "integrated.cca"  # Specify integrated reduction
dims = 30

# If using SCTransform + integration:
[SeuratPreparing.envs]
integration_method = "CCA"  # Ensure integration is performed
```

## Best Practices

1. **Use Leiden algorithm** (algorithm = 4) for better community detection
2. **Test multiple resolutions** to find optimal granularity
3. **Set random seeds** for reproducible results
4. **Match reduction to integration** if using CCA/RPCA/Harmony
5. **Custom cluster names** when running multiple annotation methods to avoid overwriting
6. **Cache intermediate results** for faster re-runs with different parameters
7. **Parallelize with ncores** for large datasets (>50k cells)
8. **Use resolution sweeps** when unsure of optimal granularity

## Related Processes

- **SeuratClusteringOfAllCells**: Clustering before T/B cell selection
- **SeuratSubClustering**: Re-clustering within specific clusters
- **SeuratMap2Ref**: Reference-based supervised clustering
- **CellTypeAnnotation**: Automated cell type annotation
