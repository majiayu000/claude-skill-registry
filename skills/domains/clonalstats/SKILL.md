---
name: clonalstats
description: Generate comprehensive clonality statistics and diversity visualizations for TCR/BCR repertoire analysis. Quantifies clonal expansion, measures diversity metrics (Shannon, Simpson, Gini), and creates publication-ready plots.
---

# ClonalStats Process Configuration

## Purpose
Generate comprehensive clonality statistics and diversity visualizations for TCR/BCR repertoire analysis. Quantifies clonal expansion, measures diversity metrics (Shannon, Simpson, Gini), and creates publication-ready plots.

## When to Use
- To quantify clonal expansion patterns in TCR/BCR data
- For diversity analysis comparing multiple samples or conditions
- To identify hyperexpanded clones and their distribution
- For rarefaction analysis to assess sampling depth
- After `ScRepCombiningExpression` to analyze integrated TCR+RNA data

## Configuration Structure

### Process Enablement
```toml
[ClonalStats]
cache = true
```

### Input Specification
```toml
[ClonalStats.in]
screpfile = ["ScRepCombiningExpression"]
```

### Core Environment Variables
```toml
[ClonalStats.envs]
# Clone definition: "gene" (VDJC), "aa" (CDR3 amino acid), "nt" (CDR3 nucleotide)
clone_call = "aa"
# Chain analysis: "both", "TRA", "TRB", "TRG", "IGH", "IGL"
chain = "both"
# Data transformations (dplyr::mutate syntax)
mutaters = {}
# Data filtering (dplyr::filter syntax)
subset = null
# Output device parameters
devpars = {width = 800, height = 600, res = 100}
# Save code and data (large files - use with caution)
save_code = false
save_data = false
```

### Case-Based Plot Generation
```toml
[ClonalStats.envs.cases."Case Name"]
viz_type = "volume"  # volume, abundance, length, residency, stat,
                    # composition, overlap, diversity, geneusage,
                    # positional, kmer, rarefaction
```

## Diversity Metrics

| Metric | Range | Interpretation | Best For |
|--------|-------|----------------|----------|
| **shannon** | 0 - ∞ | Higher = more diversity | General comparison |
| **inv.simpson** | 1 - ∞ | Higher = more diversity | Common clones |
| **gini.coeff** | 0 - 1 | 0 = equality, 1 = inequality | Clonality dominance |
| **norm.entropy** | 0 - 1 | Higher = more diversity | Evenness-focused |
| **chao1** | ≥ richness | Estimates total richness | Small samples |
| **d50** | Count | Clones making up 50% | Practical dominance |

**Interpretation:**
- High diversity = Many unique clones, even distribution (healthy repertoire)
- Low diversity = Few dominant clones (antigen-specific response, infection, cancer)
- Gini ≈ 1 = Very skewed, few clones dominate
- Gini ≈ 0 = Even distribution

## Visualization Types

**viz_type options:**
- `volume` - Number of clones per sample/group
- `abundance` - Clone abundance distribution (trend/histogram/density)
- `length` - CDR3 sequence length distribution
- `residency` - Clones present across groups (venn/upset)
- `stat` - Expanded clone analysis (pies/sankey)
- `diversity` - Diversity metrics (bar/box/violin)
- `geneusage` - V/D/J gene usage frequency
- `rarefaction` - Sampling depth assessment

## Configuration Examples

### Minimal Configuration
```toml
[ClonalStats.in]
screpfile = ["ScRepCombiningExpression"]
```

### Standard Diversity Analysis
```toml
[ClonalStats.in]
screpfile = ["ScRepCombiningExpression"]

[ClonalStats.envs.cases."Diversity"]
viz_type = "diversity"
method = "shannon"
plot_type = "box"
group_by = "Diagnosis"
comparisons = true

[ClonalStats.envs.cases."Gini Coeff"]
viz_type = "diversity"
method = "gini.coeff"
plot_type = "violin"
group_by = "Diagnosis"
add_box = true
```

### Expanded Clone Analysis
```toml
[ClonalStats.in]
screpfile = ["ScRepCombiningExpression"]

[ClonalStats.envs.cases."Expanded Clones"]
viz_type = "stat"
plot_type = "pies"
group_by = "Diagnosis"
subgroup_by = "seurat_clusters"
clones = {"Expanded (>2)" = "sel(Colitis > 2)"}
```

### Rarefaction Analysis
```toml
[ClonalStats.in]
screpfile = ["ScRepCombiningExpression"]

[ClonalStats.envs.cases."Rarefaction"]
viz_type = "rarefaction"
group_by = "Patient"
q = 1  # 0=richness, 1=shannon, 2=simpson
n_boots = 20
```

### Complete Analysis Suite
```toml
[ClonalStats.in]
screpfile = ["ScRepCombiningExpression"]

[ClonalStats.envs.cases."Volume"]
viz_type = "volume"

[ClonalStats.envs.cases."Abundance"]
viz_type = "abundance"
plot_type = "density"

[ClonalStats.envs.cases."Diversity"]
viz_type = "diversity"
method = "shannon"

[ClonalStats.envs.cases."Rarefaction"]
viz_type = "rarefaction"
```

## Common Patterns

### Disease vs Healthy
```toml
[ClonalStats.envs.cases."Comparison"]
viz_type = "diversity"
method = "gini.coeff"
plot_type = "box"
group_by = "Condition"
comparisons = true
```

### Time Course
```toml
[ClonalStats.envs.cases."Timepoint"]
viz_type = "volume"
x = "Timepoint"

[ClonalStats.envs.cases."Diversity"]
viz_type = "diversity"
method = "shannon"
group_by = "Timepoint"
```

### Treatment Response
```toml
[ClonalStats.envs.cases."Response"]
viz_type = "diversity"
method = "gini.coeff"
group_by = "Response"
plot_type = "box"
comparisons = true
```

## Dependencies
- **Upstream**: `ScRepCombiningExpression` (required)
- **Related**: `ScRepLoading`, `CDR3Clustering`, `TESSA` (optional)

## Validation Rules
- Input must be valid scRepertoire object
- For `viz_type = "diversity"`, method must be supported
- For rarefaction, `n_boots` should be ≥ 10
- Use `sel()` syntax in `clones` parameter for filtering

## Troubleshooting

**Sample column not found**: Input must have `Sample` column or specify `x` parameter.

**Strange diversity values**: Small repertoire sizes cause bias. Use `plot_type = "box"`.

**Rarefaction curves noisy**: Increase `n_boots` (try 50-100).

**Too many clones in stat plots**: Use `subset` or stricter `clones` thresholds.

**Plot generation slow**: Use `clone_call = "gene"` for speed, apply `subset`.

**Missing comparisons**: Set `comparisons = true` to add significance tests.

## Best Practices
1. Start with default cases to see standard visualizations
2. Use multiple diversity metrics: Shannon + Gini
3. Check rarefaction curves to ensure sufficient sampling
4. Document clone thresholds when defining expanded clones
5. Use `clone_call = "gene"` for speed, "aa" for granularity
6. Set `save_data = true` for debugging (watch disk space)
7. Validate findings with complementary diversity indices
8. Consider sample size: small samples underestimate richness
