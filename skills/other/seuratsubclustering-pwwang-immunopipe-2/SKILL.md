---
name: seuratsubclustering
description: Performs fine-grained re-clustering on specific subsets of cells (e.g., individual clusters, cell types, or custom subsets). Unlike `Seurat::FindSubCluster` which only finds subclusters within a single cluster, this process performs the complete clustering workflow (PCA, UMAP, FindNeighbors, FindClusters) on any subset of cells defined by metadata filters or cell barcode lists.
---

# SeuratSubClustering Process Configuration

## Purpose
Performs fine-grained re-clustering on specific subsets of cells (e.g., individual clusters, cell types, or custom subsets). Unlike `Seurat::FindSubCluster` which only finds subclusters within a single cluster, this process performs the complete clustering workflow (PCA, UMAP, FindNeighbors, FindClusters) on any subset of cells defined by metadata filters or cell barcode lists.

## When to Use
- **Cluster heterogeneity analysis**: When initial clustering identifies mixed cell populations within a cluster
- **Cell type sub-clustering**: To resolve heterogeneity within annotated cell types (e.g., T cell subsets: CD4+, CD8+, naive, memory, effector)
- **Lineage-specific analysis**: To examine substructure within major cell lineages
- **Differential sub-populations**: When a cluster contains multiple biologically distinct populations (e.g., NK cells + CD4 T cells)
- **Multi-resolution exploration**: To test different clustering granularities on specific cell subsets
- **Downstream marker discovery**: When you need markers for sub-populations within larger clusters

## Configuration Structure

### Process Enablement
```toml
[SeuratSubClustering]
cache = true  # Cache intermediate results for faster re-runs
```

### Input Specification
```toml
[SeuratSubClustering.in]
srtobj = ["SeuratClustering"]  # Path or reference to Seurat object
```

### Environment Variables

#### Core Parameters
```toml
[SeuratSubClustering.envs]
# Number of cores for parallelization
ncores = 1  # int; Higher values speed up computation

# Metadata mutaters to define subset cells
# Applied BEFORE subsetting to create temporary columns
mutaters = {}  # json; Dictionary of dplyr-like mutations

# Expression to subset cells (dplyr::filter syntax)
# Applied to metadata using tidyseurat::filter()
subset = "seurat_clusters == 'c3'"  # str; Filter expression

# Cache location for intermediate results
cache = "/tmp"  # Path; Set to false to disable caching
```

#### Sub-clustering Cases (Multiple Subsets)
```toml
[SeuratSubClustering.envs.cases]
# Keys are case names (prefixes for outputs)
# Values inherit envs parameters (except mutaters, cache)
# If empty, default case "subcluster" is created
```

**Case Naming Rules:**
- Case name becomes prefix for reductions: `<CASENAME>PC_`, `<CASENAME>UMAP_`
- Case name becomes prefix for cluster columns: `<CASENAME>.<resolution>`
- Case name becomes final cluster column: `<CASENAME>`
- Non-alphanumeric characters in case names are removed

**Metadata Output:**
- Each case adds new metadata columns to original Seurat object
- Reductions saved: `<CASENAME>.pc`, `<CASENAME>.umap`
- Clusters saved: `<CASENAME>.<resolution>` for each resolution
- Final clusters: `<CASENAME>` column

#### RunPCA Parameters
```toml
[SeuratSubClustering.envs.RunPCA]
# See https://satijalab.org/seurat/reference/runpca
# object specified internally as subset object
npcs = 30  # int; Number of PCs to compute
```

#### RunUMAP Parameters
```toml
[SeuratSubClustering.envs.RunUMAP]
# See https://satijalab.org/seurat/reference/runumap
# object specified internally as subset object
# dims=N expanded to dims=1:N (min(N, ncol-1))

dims = 30  # int; Number of PCs to use

# Use specific features instead of dimensions
# Can be list: {order = "desc(abs(avg_log2FC))", n = 30}
# Or numeric (treated as n with default order)
features = 30  # int or list; Top markers for UMAP

# Reduction to use for UMAP
reduction = "pca"  # str; Uses sobj@misc$integrated_new_reduction if omitted

n.neighbors = 30  # int; Neighborhood size
min.dist = 0.3  # float; Cluster tightness (0.001-0.5)
spread = 1  # float; Embedding scale
seed.use = 42  # int; Random seed
```

#### FindNeighbors Parameters
```toml
[SeuratSubClustering.envs.FindNeighbors]
# See https://satijalab.org/seurat/reference/findneighbors
# object specified internally

reduction = "pca"  # str; Uses sobj@misc$integrated_new_reduction if omitted
dims = 30  # int; Dimensions to use
k.param = 20  # int; K-nearest neighbors
prune.SNN = 0.067  # float; SNN pruning threshold (default: 1/15)
nn.method = "annoy"  # str; "annoy" or "rann"
```

#### FindClusters Parameters
```toml
[SeuratSubClustering.envs.FindClusters]
# See https://satijalab.org/seurat/reference/findclusters
# object specified internally

# Resolution: Higher = more clusters, Lower = fewer clusters
# Multiple resolutions supported: [0.4, 0.6, 0.8, 1.0]
# Range syntax: "0.1:0.5:0.1" -> [0.1, 0.2, 0.3, 0.4, 0.5]
resolution = 0.8  # float or list; Default: 0.8

# Cluster labels prefixed with "s" (s1, s2, ...) instead of (s0, s1, ...)
algorithm = 1  # int; 1=Louvain, 4=Leiden (recommended)
graph.name = "pca_snn"  # str; Must match FindNeighbors SNN graph
random.seed = 0  # int; Reproducibility
```

**Multi-resolution Output:**
- Multiple resolutions create columns: `<CASENAME>_0.4`, `<CASENAME>_0.6`, `<CASENAME>_0.8`, `<CASENAME>`
- Final resolution uses last value in list

## External References

### Seurat Functions
- **RunPCA()**: https://satijalab.org/seurat/reference/runpca
  - Principal component analysis on subset of cells
- **RunUMAP()**: https://satijalab.org/seurat/reference/runumap
  - Non-linear dimensionality reduction for visualization
- **FindNeighbors()**: https://satijalab.org/seurat/reference/findneighbors
  - K-nearest neighbor graph construction
- **FindClusters()**: https://satijalab.org/seurat/reference/findclusters
  - Community detection (Louvain/Leiden algorithms)

### tidyseurat::filter()
https://stemangiola.github.io/tidyseurat/reference/filter.html
- Subset Seurat objects using dplyr-like filter syntax
- Supports logical expressions: `seurat_clusters == 'c3'`, `celltype %in% c('CD4', 'CD8')`
- Can use any metadata column created by `mutaters`

## Configuration Examples

### Minimal Configuration (Default Case)
```toml
[SeuratSubClustering]
[SeuratSubClustering.in]
srtobj = ["SeuratClustering"]
```
**Result**: Creates default case "subcluster" with all cells

### Single Cluster Sub-clustering
```toml
[SeuratSubClustering]
[SeuratSubClustering.envs]
subset = "seurat_clusters == 'c3'"
```
**Result**: Re-clusters only cells in cluster c3

### Metadata-Based Sub-clustering (Cell Type)
```toml
[SeuratSubClustering]
[SeuratSubClustering.envs]
# First add cell type annotation via mutaters
mutaters = {is_cd4 = "if_else(celltype == 'CD4 T cell', TRUE, FALSE)"}

[SeuratSubClustering.envs.RunPCA]
npcs = 50

[SeuratSubClustering.envs.FindClusters]
resolution = 1.2
algorithm = 4  # Leiden
```
**Result**: Creates `subcluster` case for CD4+ cells only

### Multiple Sub-clustering Cases
```toml
[SeuratSubClustering]
[SeuratSubClustering.envs]
# Define multiple sub-clustering cases
[SeuratSubClustering.envs.cases.TEffector]
subset = "celltype == 'CD8 T cell' & state == 'Effector'"
resolution = 1.0

[SeuratSubClustering.envs.cases.TNaive]
subset = "celltype == 'CD8 T cell' & state == 'Naive'"
resolution = 0.8

[SeuratSubClustering.envs.cases.CD4Memory]
subset = "celltype == 'CD4 T cell' & state == 'Memory'"
resolution = 1.5
```
**Result**: Three sub-clustering analyses with different resolutions
- Metadata columns: `TEffector`, `TNaive`, `CD4Memory`
- Reductions: `TEFFECTORPC_`, `TNAIVEPC_`, `CD4MEMORYPC_`, etc.
- Clusters: `TEffector`, `TNaive`, `CD4Memory`

### Multi-resolution Sub-clustering
```toml
[SeuratSubClustering]
[SeuratSubClustering.envs.cases.Cluster3]
subset = "seurat_clusters == 'c3'"

[SeuratSubClustering.envs.cases.Cluster3.FindClusters]
# Test multiple resolutions
resolution = "0.4:1.2:0.2"  # [0.4, 0.6, 0.8, 1.0, 1.2]
algorithm = 4  # Leiden
```
**Result**: Cluster3 has columns `Cluster3_0.4`, `Cluster3_0.6`, `Cluster3_0.8`, `Cluster3_1.0`, `Cluster3`

### Using Top Markers for UMAP
```toml
[SeuratSubClustering]
[SeuratSubClustering.envs.cases.MixedCluster]
subset = "seurat_clusters == 'c5'"

[SeuratSubClustering.envs.cases.MixedCluster.RunUMAP]
# Use top 30 DEGs for UMAP instead of PCs
features = {order = "desc(abs(avg_log2FC))", n = 30}
```
**Result**: Sub-cluster based on top DEGs for better separation

### Leiden Algorithm with Custom Parameters
```toml
[SeuratSubClustering]
[SeuratSubClustering.envs]
ncores = 4

[SeuratSubClustering.envs.FindNeighbors]
k.param = 30
prune.SNN = 0.05

[SeuratSubClustering.envs.FindClusters]
algorithm = 4  # Leiden
resolution = 1.0
random.seed = 42
```

### Complex Subset with Multiple Conditions
```toml
[SeuratSubClustering]
[SeuratSubClustering.envs.cases.ActivatedT]
subset = "celltype %in% c('CD4 T cell', 'CD8 T cell') & activation == 'Activated'"

[SeuratSubClustering.envs.cases.ActivatedT.RunPCA]
npcs = 40

[SeuratSubClustering.envs.cases.ActivatedT.RunUMAP]
dims = 40
n.neighbors = 20
min.dist = 0.2
```

## Common Patterns

### Pattern 1: Single Cluster Deep Dive
```toml
[SeuratSubClustering]
[SeuratSubClustering.envs]
# Re-cluster cluster 3 to resolve heterogeneity
subset = "seurat_clusters == 'c3'"
```

### Pattern 2: Multiple Lineage Sub-clustering
```toml
[SeuratSubClustering]
[SeuratSubClustering.envs.cases.TCD4]
subset = "celltype == 'CD4 T cell'"

[SeuratSubClustering.envs.cases.TCD8]
subset = "celltype == 'CD8 T cell'"

[SeuratSubClustering.envs.cases.TGD]
subset = "celltype == 'Gamma delta T cell'"

[SeuratSubClustering.envs.cases.NK]
subset = "celltype == 'NK cell'"
```

### Pattern 3: Functional State Sub-clustering
```toml
[SeuratSubClustering]
[SeuratSubClustering.envs.cases.Effector]
subset = "state == 'Effector'"

[SeuratSubClustering.envs.cases.Effector.FindClusters]
resolution = 1.5  # Higher resolution for more sub-states

[SeuratSubClustering.envs.cases.Memory]
subset = "state == 'Memory'"

[SeuratSubClustering.envs.cases.Naive]
subset = "state == 'Naive'"
```

### Pattern 4: Re-clustering Based on Clonality (TCR+)
```toml
[SeuratSubClustering]
[SeuratSubClustering.envs]
# After ScRepCombiningExpression adds clonality metadata
[SeuratSubClustering.envs.cases.ExpandedClones]
subset = "clone_size >= 5"  # Large clones

[SeuratSubClustering.envs.cases.ExpandedClones.FindClusters]
resolution = 0.6  # Lower resolution for broader groups

[SeuratSubClustering.envs.cases.RareClones]
subset = "clone_size == 1"  # Unique clones

[SeuratSubClustering.envs.cases.RareClones.FindClusters]
resolution = 1.2  # Higher resolution to capture diversity
```

### Pattern 5: Multi-resolution Exploration
```toml
[SeuratSubClustering]
[SeuratSubClustering.envs.cases.TumorCluster]
subset = "seurat_clusters == 'c8'"

[SeuratSubClustering.envs.cases.TumorCluster.FindClusters]
resolution = "0.2:2.0:0.2"  # Sweep: [0.2, 0.4, ..., 2.0]
algorithm = 4  # Leiden
```

## Dependencies

### Upstream Processes
- **Required**: `SeuratClustering` (or `SeuratClusteringOfAllCells` if TOrBCellSelection used)
- **Optional**: `ScRepCombiningExpression` (if TCR/BCR data present, adds clonality metadata for subsetting)
- **Optional**: `CellTypeAnnotation` (if using annotated cell types for subsetting)

### Downstream Processes
- **SeuratClusterStats**: Statistics for sub-clusters
- **ClusterMarkers**: Differential expression between sub-clusters
- **MarkersFinder**: Flexible marker finding with enrichment analysis
- **ScFGSEA**: Pathway analysis on sub-cluster markers
- **ModuleScoreCalculator**: Module scoring within sub-clusters

## Validation Rules

### Subset Expression Validation
- Must be valid dplyr::filter() expression
- Can reference any metadata column in Seurat object
- Complex expressions supported: `&` (AND), `|` (OR), `%in%` (in operator)
- Example: `seurat_clusters == 'c3' & percent.mt < 5`
- Example: `celltype %in% c('CD4 T cell', 'CD8 T cell')`

### Case Name Validation
- Must contain only alphanumeric characters
- Non-alphanumeric characters automatically removed
- Used as prefix: reductions and cluster names
- Avoid spaces, special characters in case names

### Resolution Constraints
- Must be positive (resolution > 0)
- Single value, list, or range syntax allowed
- Range: `"start:end:step"` (step defaults to 0.1 if omitted)
- Multi-resolution creates multiple metadata columns

### Dimension Requirements
- `RunPCA.npcs` must not exceed cells in subset
- `RunUMAP.dims` automatically truncated to `min(dims, ncol(reduction) - 1)`
- Use fewer dimensions for small subsets (< 100 cells)

### Graph Name Consistency
- `FindClusters.graph.name` must match `FindNeighbors` output
- Default: `pca_snn` when not specified
- When using integrated reductions, ensure consistency

## Troubleshooting

### Issue: Subset Returns Zero Cells
**Symptoms**: Sub-clustering produces empty subset

**Solutions**:
1. Verify subset expression syntax
```toml
# Check if column exists and values are correct
[SeuratSubClustering.envs]
# Use single quotes for string comparison
subset = "seurat_clusters == 'c3'"  # Correct
subset = "seurat_clusters == c3"  # Wrong (treated as variable)
```

2. Verify column names exist in metadata
```toml
# Use existing columns only
subset = "seurat_clusters == 'c3'"  # seurat_clusters exists
subset = "cluster_id == 'c3'"  # cluster_id may not exist
```

3. Check for exact string matching
```toml
# Case-sensitive
subset = "celltype == 'CD4 T cell'"  # Exact match
subset = "celltype == 'CD4 T Cell'"  # Wrong case
```

### Issue: Too Many Small Sub-clusters
**Symptoms**: Hundreds of tiny sub-clusters, many singletons

**Solutions**:
```toml
[SeuratSubClustering.envs.FindClusters]
resolution = 0.4  # Lower resolution
algorithm = 4  # Leiden handles singletons better
```

### Issue: Sub-clusters Overlapping in UMAP
**Symptoms**: Poor separation in sub-cluster visualization

**Solutions**:
```toml
[SeuratSubClustering.envs.RunUMAP]
min.dist = 0.1  # Tighter clusters
n.neighbors = 15  # More local detail
spread = 1.2  # More separation
```

### Issue: Sub-clustering Uses Wrong Reduction
**Symptoms**: Clustering on raw RNA instead of integrated data

**Solutions**:
```toml
[SeuratSubClustering.envs.FindNeighbors]
reduction = "integrated.cca"  # Use integrated reduction

[SeuratSubClustering.envs.RunUMAP]
reduction = "integrated.cca"
```

### Issue: Multi-resolution Columns Not Created
**Symptoms**: Only final resolution column appears

**Solutions**:
```toml
[SeuratSubClustering.envs.FindClusters]
# Use list syntax (not single value with range)
resolution = [0.4, 0.6, 0.8, 1.0]  # Correct
resolution = "0.4:1.0:0.2"  # Also correct
```

### Issue: Case Names Too Similar
**Symptoms**: Confusion between multiple cases

**Solutions**:
```toml
# Use descriptive, unique case names
[SeuratSubClustering.envs.cases]
T_CD4_Effector = {subset = "..."}
T_CD4_Naive = {subset = "..."}
B_Memory = {subset = "..."}
```

### Issue: Sub-clustering on All Cells (Not Subset)
**Symptoms**: Default case runs on entire object

**Solutions**:
```toml
# Always specify subset or use cases
[SeuratSubClustering.envs]
subset = "seurat_clusters == 'c3'"  # Explicit subset

# Or define specific cases
[SeuratSubClustering.envs.cases.MyCase]
subset = "seurat_clusters == 'c3'"
```

### Issue: Reductions Not Saved
**Symptoms**: Cannot find `<CASENAME>PC_` or `<CASENAME>UMAP_`

**Solutions**:
```toml
# Ensure case name is alphanumeric only
[SeuratSubClustering.envs.cases]
MySubCluster1 = {subset = "..."}  # Correct
Sub-Cluster = {subset = "..."}  # Hyphen removed -> SubCluster

# Check metadata for actual reduction names
# Reductions are: <CASENAME>pc, <CASENAME>umap (lowercase)
```

## Best Practices

1. **Define explicit subsets**: Always specify `subset` or define `cases` to avoid default case on all cells
2. **Use descriptive case names**: Make case names clear and unique (e.g., `T_Effector`, not `case1`)
3. **Test multiple resolutions**: Sweep resolution range to find optimal granularity for each subset
4. **Use Leiden algorithm**: Prefer `algorithm = 4` for better community detection
5. **Leverage metadata columns**: Use CellTypeAnnotation results, TCR clonality, or custom mutaters for subsetting
6. **Set random seeds**: Ensure reproducible sub-clustering results with `random.seed`
7. **Parallelize large subsets**: Use `ncores > 1` for subsets > 10k cells
8. **Adjust UMAP parameters**: Smaller subsets may need different `n.neighbors` and `min.dist`
9. **Document sub-clustering strategy**: Comment on biological rationale for each case in config
10. **Use multi-resolution**: Test `[0.4, 0.6, 0.8, 1.0]` to capture different granularities

## Related Processes

- **SeuratClustering**: Initial clustering before sub-clustering
- **SeuratClusteringOfAllCells**: Clustering before T/B cell selection
- **CellTypeAnnotation**: Annotate clusters before sub-clustering by cell type
- **ClusterMarkers**: Find markers for sub-clusters
- **MarkersFinder**: Flexible marker finding with multiple comparison groups
