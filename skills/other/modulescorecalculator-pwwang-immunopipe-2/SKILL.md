---
name: modulescorecalculator
description: Configuration skill for immunopipe process
---

# ModuleScoreCalculator Process Configuration

**Purpose**: Calculate module/pathway/gene signature scores per cell using Seurat's AddModuleScore or CellCycleScoring functions.

## When to Use

- To score cells for specific gene programs (exhaustion, cytotoxicity, proliferation)
- For pathway activity analysis using curated gene sets
- To quantify functional states (activation, differentiation, memory)
- To add diffusion map components for trajectory analysis
- For cell cycle scoring to identify S and G2M phase cells

## Configuration Structure

### Process Enablement
```toml
[ModuleScoreCalculator]
cache = true
```

### Input Specification
```toml
[ModuleScoreCalculator.in]
# Input: Seurat object from SeuratClustering
srtobj = ["SeuratClustering"]
```

### Environment Variables
```toml
[ModuleScoreCalculator.envs]
# Default parameters inherited by all modules
defaults = { nbin = 24, ctrl = 100, seed = 8525, agg = "mean" }

# Module definitions (key = module name, value = gene set parameters)
modules = {}

# Post-scoring metadata transformations
post_mutaters = {}
```

## External References

### Seurat AddModuleScore Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `features` | string/list | Required | Gene names or `cc.genes`/`cc.genes.updated.2019` for cell cycle |
| `nbin` | int | 24 | Number of bins for aggregate expression levels of all analyzed features |
| `ctrl` | int | 100 | Number of control features selected from same bin per analyzed feature |
| `k` | boolean | false | Use feature clusters from `DoKMeans` instead of random selection |
| `assay` | string | NULL | The assay to use (defaults to active assay) |
| `seed` | int | 8525 | Random seed for reproducibility |
| `search` | boolean | false | Search for symbol synonyms if features don't match |
| `keep` | boolean | false | Keep individual feature scores (non-cell cycle only) |
| `agg` | string | "mean" | Aggregation function: `mean`, `median`, `sum`, `max`, `min`, `var`, `sd` |

**Reference**: https://satijalab.org/seurat/reference/addmodulescore

### CellCycleScoring Parameters
When using `features = "cc.genes"` or `"cc.genes.updated.2019"`, adds:
- `S.Score` - S phase score per cell
- `G2M.Score` - G2M phase score per cell
- `Phase` - Cell cycle phase assignment (G1, S, G2M)

**Reference**: https://satijalab.org/seurat/reference/cellcyclescoring

### Diffusion Map Parameters
```python
{"DC": {"features": 2, "kind": "diffmap"}}
```
Adds first N diffusion components as metadata columns (`DC_1`, `DC_2`, ...).

**Reference**: https://www.rdocumentation.org/packages/destiny/versions/2.0.4/topics/DiffusionMap

## Configuration Examples

### Minimal Configuration
```toml
[ModuleScoreCalculator]
[ModuleScoreCalculator.in]
srtobj = ["SeuratClustering"]
```

### Cell Cycle Scoring
```toml
[ModuleScoreCalculator.envs.modules]
CellCycle = { features = "cc.genes.updated.2019" }
```
**Output columns**: `S.Score`, `G2M.Score`, `Phase`

### Exhaustion Score (T Cells)
```toml
[ModuleScoreCalculator.envs.modules.Exhaustion]
features = "HAVCR2,ENTPD1,LAYN,LAG3,TIGIT,PDCD1,TOX"
```

### Cytotoxicity Score (CD8+ T Cells, NK Cells)
```toml
[ModuleScoreCalculator.envs.modules.Cytotoxicity]
features = "GZMB,PRF1,NKG7,GNLY,CTSW"
```

### Proliferation Score
```toml
[ModuleScoreCalculator.envs.modules.Proliferation]
features = "MKI67,STMN1,TUBB,PCNA,TOP2A"
```

### Activation Score
```toml
[ModuleScoreCalculator.envs.modules.Activation]
features = "IFNG,TNF,CD69,CD25"
```

### Multiple Gene Sets (Functional States)
```toml
[ModuleScoreCalculator.envs.modules]
[ModuleScoreCalculator.envs.modules.CellCycle]
features = "cc.genes.updated.2019"

[ModuleScoreCalculator.envs.modules.Exhaustion]
features = "HAVCR2,ENTPD1,LAYN,LAG3,TIGIT,PDCD1"

[ModuleScoreCalculator.envs.modules.Activation]
features = "IFNG,TNF,CD69,CD25"

[ModuleScoreCalculator.envs.modules.Proliferation]
features = "MKI67,STMN1,TUBB,PCNA"
```

### Diffusion Map Components
```toml
[ModuleScoreCalculator.envs.modules]
DC = { features = 2, kind = "diffmap" }
```
**Use with**: `env.dimplots` in `SeuratClusterStats` with `reduction = "DC"`

### Post-Metadata Transformation
```toml
[ModuleScoreCalculator.envs.post_mutaters]
# Calculate combined exhaustion-activation ratio
Exh_Act_Ratio = "Exhaustion1 / Activation1"

# Classify high vs low exhaustion
Exhaustion_Level = "ifelse(Exhaustion1 > median(Exhaustion1, na.rm = TRUE), 'High', 'Low')"
```

## Common Patterns

### Pattern 1: T Cell Functional States
```toml
[ModuleScoreCalculator.envs.modules]
# Exhaustion markers (checkpoint genes)
Exhaustion = {
    features = "HAVCR2,ENTPD1,LAYN,LAG3,TIGIT,PDCD1,TOX,CTLA4"
}

# Activation markers
Activation = {
    features = "IFNG,TNF,CD69,CD25,IL2RA"
}

# Memory markers
Memory = {
    features = "IL7R,CCR7,SELL,S100A4"
}

# Terminal differentiation
Terminal_Diff = {
    features = "TIGIT,PDCD1,CD274,CD244,CD160"
}
```

### Pattern 2: NK Cell Functional States
```toml
[ModuleScoreCalculator.envs.modules]
# Cytotoxicity
Cytotoxicity = {
    features = "GZMB,PRF1,NKG7,GNLY,CTSW"
}

# Activation
NK_Activation = {
    features = "NCAM1,KLRD1,FCGR3A"
}

# Exhaustion
NK_Exhaustion = {
    features = "HAVCR2,LAG3,PDCD1,TIGIT"
}
```

### Pattern 3: Cell Cycle with Custom Parameters
```toml
[ModuleScoreCalculator.envs.defaults]
nbin = 24
ctrl = 100
seed = 8525

[ModuleScoreCalculator.envs.modules]
CellCycle = {
    features = "cc.genes.updated.2019"
}
```

### Pattern 4: Metabolic Pathway Scores
```toml
[ModuleScoreCalculator.envs.modules]
# Glycolysis (Warburg effect)
Glycolysis = {
    features = "HK2,PKM,LDHA,PFKL,ENO1"
}

# Oxidative phosphorylation
OXPHOS = {
    features = "ND1,ND2,ND3,COX1,COX2,ATP5A1"
}

# Fatty acid oxidation
FAO = {
    features = "CPT1A,ACOX1,HADHA"
}
```

### Pattern 5: B Cell Functionality
```toml
[ModuleScoreCalculator.envs.modules]
# Plasma cell differentiation
Plasma = {
    features = "MZB1,SSR4,SDC1,XBP1,PRDM1"
}

# Germinal center
Germinal_Center = {
    features = "BCL6,AICDA,MEF2B"
}

# Naive vs memory
Naive = {
    features = "IL7R,CCR7,IGHD"
}
Memory = {
    features = "CD27,IGG1,IGHG1"
}
```

## Gene Set Resources

### MSigDB (Molecular Signatures Database)
- **URL**: https://www.gsea-msigdb.org/
- **Hallmark Collection**: 50 curated gene sets for biological processes
  - `HALLMARK_INTERFERON_GAMMA_RESPONSE`
  - `HALLMARK_TNFA_SIGNALING_VIA_NFKB`
  - `HALLMARK_INFLAMMATORY_RESPONSE`
  - `HALLMARK_HYPOXIA`
  - `HALLMARK_APOPTOSIS`
- **Immunologic Signatures (C7)**: Gene sets from immunology studies
- **Download**: Available in GMT format for direct use

### CellMarker Database
- **URL**: http://bioinfo.life.hust.edu.cn/CellMarker/
- Cell type-specific markers for human and mouse

### Literature-Derived Signatures

**T Cell Exhaustion Markers**:
- Primary: `HAVCR2` (TIM-3), `PDCD1` (PD-1), `LAG3`, `TIGIT`, `CTLA4`
- Transcription factors: `TOX`, `NR4A1`, `EOMES`

**T Cell Activation Markers**:
- Cytokines: `IFNG`, `TNF`, `IL2`
- Surface: `CD69`, `CD25` (`IL2RA`), `CD38`

**Cytotoxicity Markers**:
- Granzymes: `GZMB`, `GZMA`, `GZMH`
- Perforin: `PRF1`
- NK receptors: `NKG7`, `GNLY`, `CTSW`

**Proliferation Markers**:
- Ki-67: `MKI67`
- Tubulin: `STMN1`, `TUBB`
- PCNA: `PCNA`, `TOP2A`

**Cell Cycle Genes** (Seurat built-in):
- `cc.genes` - Original Tirosh et al. 2016 gene set
- `cc.genes.updated.2019` - Updated with 2019 gene symbols

## Dependencies

### Upstream Processes
- **Required**: `SeuratClustering` - Provides the Seurat object
- **Optional**: `TOrBCellSelection` - If working with T/B cell subsets

### Downstream Processes
- `SeuratClusterStats` - Visualize module scores across clusters
- `CellCellCommunication` - Correlate scores with cell interactions
- `ScFGSEA` - Validate module activity with enrichment analysis

## Validation Rules

### Gene Set Format Validation
- **Comma-separated strings**: `"GENE1,GENE2,GENE3"` ✓
- **Cell cycle keywords**: `"cc.genes"` or `"cc.genes.updated.2019"` ✓
- **Diffusion map**: `{"features": N, "kind": "diffmap"}` ✓

### Gene Name Matching
- **Human genes**: Uppercase (`MKI67`, `IFNG`) ✓
- **Mouse genes**: Title case (`Mki67`, `Ifng`) ✓
- **Search mode**: Set `search = true` to automatically find synonyms
- **Keep mode**: Set `keep = true` to retain unmatched features

### Parameter Constraints
- `nbin`: Typically 10-50 (default 24)
- `ctrl`: Typically 10-500 (default 100)
- Minimum genes: ≥5 genes recommended for robust scoring
- Maximum genes: No hard limit, but performance may degrade >1000 genes

## Troubleshooting

### Issue: Genes Not Found in Object
**Symptom**: Warning "XX% of features not found in object"

**Solutions**:
1. Check gene name format (uppercase for human, title case for mouse)
2. Enable `search = true` to find symbol synonyms
3. Verify gene symbols match your Seurat object's row names
4. Use `search = true` + `keep = true` to debug missing genes

### Issue: Too Few Genes in Set
**Symptom**: Module score is NA or unreliable

**Solutions**:
1. Ensure ≥5 genes in gene set for robust scoring
2. Add alternative markers to expand gene set
3. Check if genes are expressed in your dataset
4. Use `keep = true` to see how many genes matched

### Issue: Cell Cycle Score All G1
**Symptom**: Most cells classified as G1 phase

**Solutions**:
1. Check if cells are truly non-proliferating (e.g., memory T cells)
2. Verify data quality (low UMI counts may obscure cell cycle)
3. Consider using `cc.genes` instead of `cc.genes.updated.2019`
4. Check `S.Score` and `G2M.Score` values directly

### Issue: Module Scores All Similar
**Symptom**: No variation in scores across cells

**Solutions**:
1. Genes may be uniformly expressed or not detected
2. Try adjusting `nbin` and `ctrl` parameters
3. Verify assay selection (`assay = "RNA"` vs `"SCT"`)
4. Check if cells express the expected markers

### Issue: Diffusion Map Components Not Added
**Symptom**: `DC_1`, `DC_2` columns missing

**Solutions**:
1. Ensure `destiny` R package is installed
2. Verify `SingleCellExperiment` package is available
3. Use correct format: `{"DC": {"features": 2, "kind": "diffmap"}}`
4. Requires R packages: `SingleCellExperiment`, `destiny`

## Best Practices

### Gene Set Selection
- Use literature-validated signatures when possible
- Combine complementary markers (e.g., exhaustion: `HAVCR2` + `PDCD1` + `LAG3`)
- Consider species-specific marker expression patterns
- Test gene sets on a subset before full pipeline run

### Parameter Tuning
- `nbin = 24`: Default works well for most datasets
- `ctrl = 100`: Increase if many genes have similar expression levels
- `seed = 8525`: Keep fixed for reproducibility across runs
- `agg = "mean"`: Use `median` for outlier-resistant aggregation

### Visualization
- Use `SeuratClusterStats.envs.dimplots` to visualize scores
- Add to `SeuratClusterStats.envs.violins` for distribution plots
- Correlate scores with clusters or annotations
- Consider `post_mutaters` for custom score transformations

### Performance
- Module scoring is computationally cheap (<5 min for typical datasets)
- Larger gene sets (>1000 genes) may take longer
- Diffusion map computation scales with cell number (O(n²))

## Integration Example

```toml
# Complete workflow with multiple scores
[ModuleScoreCalculator.envs.defaults]
nbin = 24
ctrl = 100
seed = 8525

[ModuleScoreCalculator.envs.modules]
# Cell cycle
CellCycle = { features = "cc.genes.updated.2019" }

# T cell function
Exhaustion = { features = "HAVCR2,ENTPD1,LAYN,LAG3,TIGIT,PDCD1,TOX,CTLA4" }
Activation = { features = "IFNG,TNF,CD69,CD25" }
Memory = { features = "IL7R,CCR7,SELL,S100A4" }

# Cytotoxicity
Cytotoxicity = { features = "GZMB,PRF1,NKG7,GNLY" }

# Metabolism
Glycolysis = { features = "HK2,PKM,LDHA,PFKL,ENO1" }

[ModuleScoreCalculator.envs.post_mutaters]
# Classify T cell states
Tcell_State = """
case_when(
    Exhaustion1 > median(Exhaustion1, na.rm = TRUE) ~ 'Exhausted',
    Activation1 > median(Activation1, na.rm = TRUE) ~ 'Activated',
    Memory1 > median(Memory1, na.rm = TRUE) ~ 'Memory',
    TRUE ~ 'Naive'
)
"""

# Combined functional score
Functionality = "(Activation1 + Cytotoxicity1) / (Exhaustion1 + 1)"
```

## Notes

- **Process is optional**: Only runs when `[ModuleScoreCalculator]` section exists in config
- **Multiple modules**: Define any number of modules in `modules` dictionary
- **Column naming**: Scores stored as `ModuleName1`, `ModuleName2`, etc.
- **Cell cycle special case**: Uses `CellCycleScoring()` which adds `S.Score`, `G2M.Score`, `Phase`
- **Diffusion map**: Special module type for trajectory analysis
- **Post-processing**: Use `post_mutaters` for custom metadata calculations
- **Visualization**: Scores available in `SeuratClusterStats` for plotting

## Quick Reference

**Gene Set Formats**:
```toml
# Comma-separated
features = "GENE1,GENE2,GENE3"

# Cell cycle (built-in)
features = "cc.genes.updated.2019"

# Diffusion map (special)
features = 2
kind = "diffmap"
```

**Common Gene Sets**:
```toml
Exhaustion = "HAVCR2,PDCD1,LAG3,TIGIT,CTLA4,TOX"
Cytotoxicity = "GZMB,PRF1,NKG7,GNLY"
Proliferation = "MKI67,STMN1,PCNA,TOP2A"
Activation = "IFNG,TNF,CD69,CD25"
Memory = "IL7R,CCR7,SELL"
```

**Process Location**: `/immunopipe/processes.py` (line 455)
**Documentation**: `/docs/processes/ModuleScoreCalculator.md`
**Function**: Seurat::AddModuleScore(), Seurat::CellCycleScoring()
