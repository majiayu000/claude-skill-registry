---
name: screpcombiningexpression
description: Combine scTCR/BCR repertoire data with scRNA-seq expression data using `scRepertoire::combineExpression()`. This process integrates immune receptor information (CDR3 sequences, V(D)J genes, clonotypes) into a Seurat object's metadata, enabling clonotype-aware gene expression analysis.
---

# ScRepCombiningExpression Process Configuration

## Purpose
Combine scTCR/BCR repertoire data with scRNA-seq expression data using `scRepertoire::combineExpression()`. This process integrates immune receptor information (CDR3 sequences, V(D)J genes, clonotypes) into a Seurat object's metadata, enabling clonotype-aware gene expression analysis.

## When to Use
- When analyzing paired scTCR-seq + scRNA-seq data or paired scBCR-seq + scRNA-seq data
- Required for all downstream TCR/BCR analyses (CDR3Clustering, TESSA, ClonalStats)
- After ScRepLoading and SeuratClustering (or TOrBCellSelection)
- When you need to visualize or analyze clonotype distribution across RNA clusters

## Configuration Structure

### Process Enablement
```toml
[ScRepCombiningExpression]
cache = true
```

### Input Specification
```toml
[ScRepCombiningExpression.in]
# Required inputs
screpfile = ["ScRepLoading"]      # scRepertoire object from ScRepLoading
srtobj = ["SeuratClustering"]     # Seurat object with RNA data
```

**Note**: Barcodes in `srtobj` must match barcodes in `screpfile`. Ensure both datasets were generated from the same cell calling run.

### Environment Variables
```toml
[ScRepCombiningExpression.envs]
# Clonotype definition
cloneCall = "aa"  # How to define a clonotype (default: aa)

# Chain selection
chain = "both"    # Which TCR/BCR chains to use (default: both)

# Frequency calculation
group_by = "Sample"  # Group for frequency/proportion calculation (default: Sample)
proportion = true    # Use proportion (true) or total frequency (false) (default: true)

# Filtering options
filterNA = false   # Remove cells without TCR/BCR data (default: false)

# Clone size bins
cloneSize = {Rare = 0.0001, Small = 0.001, Medium = 0.01, Large = 0.1, Hyperexpanded = 1}

# Label customization
addLabel = false   # Add label to frequency header (default: false)
```

#### Environment Variables Explained

**cloneCall**: Defines clonotype grouping strategy
- `gene`: Group by V(D)JC gene usage (e.g., TRBV12-3*01, TRBJ2-7*01)
- `nt`: Group by CDR3 nucleotide sequence
- `aa`: Group by CDR3 amino acid sequence (default)
- `strict`: Group by V(D)JC gene + CDR3 nucleotide (most specific)
- Custom: Use a custom column from the data

**chain**: Which receptor chains to include
- `both`: Include both chains (e.g., TRA + TRB for TCR, IGH + IGL/IGK for BCR)
- `TRA`: T cell receptor alpha chain only
- `TRB`: T cell receptor beta chain only
- `TRG`: T cell receptor gamma chain only
- `TRD`: T cell receptor delta chain only
- `IGH`: B cell immunoglobulin heavy chain only
- `IGL`: B cell immunoglobulin light chain (lambda/kappa) only

**group_by**: Column for frequency calculation
- `"Sample"`: Calculate clonotype frequency per sample (default)
- `"seurat_clusters"`: Calculate per RNA cluster
- `NULL` or `"none"`: Keep input format without grouping
- Custom: Use any metadata column name

**proportion**:
- `true`: Calculate as proportion (0-1 scale) within group
- `false`: Calculate as absolute frequency (counts)

**filterNA**:
- `true`: Remove cells without V(D)J data from Seurat object
- `false`: Keep all cells, add `VDJ_Presence = FALSE` for non-productive cells

**cloneSize**: Bins for categorizing clone sizes
- Values are thresholds for proportion or frequency
- Keys become new metadata column with categories
- If `proportion = false`, upper limit may auto-adjust based on data

**addLabel**: Useful when running multiple configurations with different `group_by` or `cloneCall` settings.

## Configuration Examples

### Minimal Configuration
```toml
[ScRepCombiningExpression]
[ScRepCombiningExpression.in]
screpfile = ["ScRepLoading"]
srtobj = ["SeuratClustering"]
```
**Use when**: Default CDR3aa clonotype definition is sufficient.

### Standard TCR Integration
```toml
[ScRepCombiningExpression]
[ScRepCombiningExpression.in]
screpfile = ["ScRepLoading"]
srtobj = ["SeuratClustering"]
[ScRepCombiningExpression.envs]
# Use CDR3 amino acid for clonotype definition
cloneCall = "aa"
# Include both TRA and TRB chains
chain = "both"
# Calculate frequency per sample
group_by = "Sample"
# Use proportional frequency
proportion = true
```
**Use when**: Analyzing TCR data with standard parameters.

### BCR Heavy+Light Chain Integration
```toml
[ScRepCombiningExpression]
[ScRepCombiningExpression.in]
screpfile = ["ScRepLoading"]
srtobj = ["SeuratClustering"]
[ScRepCombiningExpression.envs]
# BCR data - analyze both heavy and light chains
chain = "both"
# Use V gene + CDR3aa for specific clonotype definition
cloneCall = "aa"
# Calculate frequency per sample
group_by = "Sample"
```
**Use when**: Analyzing paired IGH + IGL/IGK BCR data.

### Clonotype by RNA Cluster
```toml
[ScRepCombiningExpression]
[ScRepCombiningExpression.in]
screpfile = ["ScRepLoading"]
srtobj = ["SeuratClustering"]
[ScRepCombiningExpression.envs]
# Calculate clonotype frequency within each RNA cluster
group_by = "seurat_clusters"
# Use absolute counts instead of proportions
proportion = false
```
**Use when**: Need to track which RNA clusters contain expanded clones.

### Remove Non-Productive Cells
```toml
[ScRepCombiningExpression]
[ScRepCombiningExpression.in]
screpfile = ["ScRepLoading"]
srtobj = ["SeuratClustering"]
[ScRepCombiningExpression.envs]
# Remove cells without productive V(D)J rearrangements
filterNA = true
```
**Use when**: Analysis should only include cells with receptor data.

### Gene-Based Clonotype Definition
```toml
[ScRepCombiningExpression]
[ScRepCombiningExpression.in]
screpfile = ["ScRepLoading"]
srtobj = ["SeuratClustering"]
[ScRepCombiningExpression.envs]
# Group by V(D)JC gene usage only
cloneCall = "gene"
```
**Use when**: Interested in V gene bias rather than CDR3 specificity.

## Common Patterns

### Pattern 1: Simple TCR Addition (Default)
```toml
[ScRepCombiningExpression]
[ScRepCombiningExpression.in]
screpfile = ["ScRepLoading"]
srtobj = ["SeuratClustering"]
```
**Best for**: Initial exploratory analysis with default CDR3aa clonotypes.

### Pattern 2: TCR Beta Chain Only
```toml
[ScRepCombiningExpression.envs]
# Analyze only TRB chain
chain = "TRB"
```
**Best for**: TRB-focused analyses when TRA data is noisy or unavailable.

### Pattern 3: BCR with Custom Clone Bins
```toml
[ScRepCombiningExpression.envs]
chain = "both"
cloneCall = "aa"
# Custom bins for BCR clonal expansion
cloneSize = {Single = 1, Small = 3, Medium = 10, Large = 50, Hyperexpanded = 500}
```
**Best for**: BCR analysis where expansion patterns differ from TCR.

### Pattern 4: Frequency by Condition
```toml
[ScRepCombiningExpression.envs]
# Calculate frequency per experimental condition
group_by = "Diagnosis"
# Use absolute counts
proportion = false
```
**Best for**: Comparing clonal expansion across treatment groups.

### Pattern 5: Strict Clonotype Definition
```toml
[ScRepCombiningExpression.envs]
# Most specific: V(D)JC gene + CDR3 nucleotide
cloneCall = "strict"
```
**Best for**: High-resolution clonotype analysis where gene + CDR3 matter.

## Metadata Added to Seurat Object

After running `ScRepCombiningExpression`, the Seurat object's metadata will include:

### Core Columns (from scRepertoire)
- **`CTgene`**: V(D)JC gene names (e.g., "TRBV12-3*01_TRBJ2-7*01" for paired chains)
- **`CTnt`**: CDR3 nucleotide sequences
- **`CTaa`**: CDR3 amino acid sequences (separated by `_` for paired chains)
- **`CTcount`**: Count of cells in each clonotype
- **`CTfrequency`**: Frequency of clonotype within group (if `group_by` set)
- **`CTproportion`**: Proportion of clonotype within group (if `group_by` set)
- **`cloneSize`**: Category from `cloneSize` bins (Rare, Small, Medium, Large, Hyperexpanded)

### Custom Column (immunopipe-specific)
- **`VDJ_Presence`**: Boolean indicating if cell has TCR/BCR sequence
  - `TRUE`: Productive V(D)J rearrangement detected
  - `FALSE`: No productive V(D)J data

### Chain-Specific Columns (when applicable)
- **`TRA_1`, `TRA_2`**: Individual CDR3aa sequences for TRA chains
- **`TRB_1`, `TRB_2`**: Individual CDR3aa sequences for TRB chains
- **`IGH_1`, `IGH_2`**: Individual CDR3aa sequences for IGH chains
- **`IGL_1`, `IGL_2`**: Individual CDR3aa sequences for IGL/IGK chains

## Dependencies

### Upstream Processes
- **ScRepLoading** (required): Loads TCR/BCR data from raw files
- **SeuratClustering** or **TOrBCellSelection** (required): Provides RNA data with clustering

### Downstream Processes
- **CDR3Clustering**: Clusters TCR/BCR clones by CDR3 similarity
- **TESSA**: TCR-specific analysis using clonotype information
- **ClonalStats**: Visualizes clonal statistics and diversity
- **CDR3AAPhyschem**: Analyzes CDR3 physicochemical properties
- **SeuratClusterStats**: Uses combined metadata for cluster statistics

### Data Flow
```
ScRepLoading (TCR/BCR data)
         ↓
SeuratClustering (RNA clusters)
         ↓
ScRepCombiningExpression (integrate)
         ↓
CDR3Clustering / TESSA / ClonalStats
```

## Validation Rules

### Barcode Matching
- **Critical**: Cell barcodes in `screpfile` must exactly match barcodes in `srtobj`
- **Common cause**: Different cell calling algorithms or filtering thresholds
- **Solution**: Re-run cell calling with same parameters or manually filter to common barcodes

### Clonotype Definition Constraints
- `cloneCall = "strict"` requires both V(D)J genes AND CDR3 nt to match
- `cloneCall = "gene"` only uses gene usage (may over-group clones)
- `cloneCall = "aa"` is recommended for most analyses (balance specificity and grouping)

### Chain Selection Rules
- `chain = "both"` requires paired data (TRA+TRB for TCR, IGH+IGL/IGK for BCR)
- If single-chain data, specify which chain: `chain = "TRB"` or `chain = "IGH"`
- Unpaired chains will result in NA values in CTaa column

## Troubleshooting

### Issue: No metadata columns added
**Possible causes**:
1. Barcode mismatch between RNA and TCR/BCR data
2. All cells filtered out (low QC or missing V(D)J data)
3. Empty TCR/BCR input file

**Diagnosis**:
```r
# Check barcode overlap
length(intersect(Cells(srtobj), rownames(screpfile)))
```

**Solution**: Ensure both datasets come from same cell calling run, or manually filter to common barcodes.

### Issue: Many cells with `VDJ_Presence = FALSE`
**Possible causes**:
1. Low sequencing depth for V(D)J library
2. Stringent V(D)J calling filters
3. Non-T/B cells in dataset (e.g., myeloid cells)

**Solution**:
- Check V(D)J library quality metrics
- Verify cell type composition
- Consider `filterNA = true` to remove non-productive cells

### Issue: Empty `CTaa` column
**Possible causes**:
1. Wrong chain selected (e.g., `chain = "TRB"` for alpha-only T cells)
2. Paired chain data but single-chain selection
3. Non-productive rearrangements filtered out

**Solution**:
- Use `chain = "both"` if paired data available
- Verify which chains are present in raw contig file
- Check `ScRepLoading` output for chain distribution

### Issue: Clonotype frequency doesn't sum to 1
**Possible causes**:
1. `group_by` includes cells without V(D)J data
2. `proportion = false` (using counts, not proportions)
3. Multiple samples with different cell counts

**Solution**:
- Check if `filterNA = true` should be enabled
- Verify `group_by` column is appropriate
- Use `proportion = true` for normalized frequencies

### Issue: All clones in "Rare" category
**Possible causes**:
1. `cloneSize` thresholds too high for data
2. Low clonal expansion in dataset
3. `proportion = false` with absolute counts

**Solution**:
- Adjust `cloneSize` bins to match data distribution
- Check if dataset truly has expanded clones
- Use `proportion = true` for relative clone sizes

## Best Practices

### Data Preparation
1. Run same cell calling for RNA and V(D)J libraries
2. Apply consistent QC filters before integration
3. Verify sample matching between RNA and TCR/BCR metadata

### Parameter Selection
1. Use `cloneCall = "aa"` for most analyses (default)
2. Use `chain = "both"` for paired receptor data
3. Set `group_by = "Sample"` for frequency calculations (default)
4. Keep `filterNA = false` to distinguish productive vs non-productive cells

### Validation
1. Check barcode overlap before running: `sum(rownames(srtobj) %in% rownames(screpfile))`
2. Verify VDJ_Presence distribution: `table(srtobj$VDJ_Presence)`
3. Inspect clone size distribution: `table(srtobj$cloneSize)`
4. Check clonotype counts: `length(unique(srtobj$CTaa))`

## External References

### scRepertoire Documentation
- **combineExpression**: https://www.borch.dev/uploads/screpertoire/reference/combineexpression
- **combineTCR/combineBCR**: https://www.borch.dev/uploads/screpertoire/articles/combining_contigs
- **Working with Single-Cell Objects**: https://www.borch.dev/uploads/screpertoire/articles/attaching_sc

### Clonotype Definition
- CDR3aa: Most common - uses amino acid sequence of CDR3 region
- CDR3nt: More specific - uses nucleotide sequence (higher resolution)
- V(D)JC gene: Broader - groups by gene usage only
- Strict: Most specific - requires both gene usage and CDR3nt match

### Chain Pairing
- TCR: Typically TRA (alpha) + TRB (beta) paired
- BCR: IGH (heavy) + IGL/IGK (light) paired
- Gamma-delta T cells: TRG + TRD chains
