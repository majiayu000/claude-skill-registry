---
name: cellxgene-context
description: "Guide for integrating CellxGene Census single-cell data with ENCODE bulk experiments. Use when users need cell-type-specific expression context for ENCODE regulatory data, want to deconvolve bulk ENCODE signals, or validate regulatory elements at single-cell resolution. Trigger on: CellxGene, single-cell atlas, cell type expression, Census, cell type specificity, single-cell context, scRNA-seq atlas."
---

# Integrating CellxGene Census Single-Cell Data with ENCODE Bulk Experiments

Bridge bulk ENCODE functional genomics data with cell-type-specific expression from the CellxGene Census, the largest unified single-cell RNA-seq atlas, to resolve cell-type contributions to regulatory element activity.

## Scientific Rationale

**The question**: "Which specific cell types within my tissue drive the regulatory signals I see in bulk ENCODE data?"

ENCODE provides deeply sequenced bulk functional genomics (ChIP-seq, ATAC-seq, Hi-C) across hundreds of biosamples. But bulk data from a tissue like "pancreas" is a mixture of acinar cells (~80%), duct cells (~10%), endocrine cells (~5%), and others. An H3K27ac peak in bulk pancreas could be driven by any of these cell types. CellxGene Census provides cell-type-resolved expression data from 50M+ single-cell observations across thousands of datasets, enabling deconvolution of bulk ENCODE signals.

### The Bulk-to-Single-Cell Bridge

| Bulk ENCODE Signal | Single-Cell Question | CellxGene Answer |
|-------------------|---------------------|-----------------|
| H3K27ac peak near INS gene in pancreas | Which cell type expresses INS? | Beta cells (>500 TPM), not acinar (<1 TPM) |
| ATAC-seq peak in liver near ALB | Is this hepatocyte-specific? | Yes — ALB expressed only in hepatocytes |
| Enhancer active in brain cortex | Neurons or glia? | CellxGene resolves excitatory neurons vs. astrocytes vs. oligodendrocytes |
| Broad H3K27ac domain in blood | Which immune cell type? | Can distinguish T cells, B cells, monocytes, NK cells |

### What CellxGene Census Provides

- **50M+ single-cell observations** from thousands of published datasets
- **Standardized cell ontology** (Cell Ontology terms) across all datasets
- **Unified gene expression** in a consistent format
- **Metadata**: tissue, disease status, sex, ethnicity, developmental stage
- **API access** via Python (`cellxgene-census`) or R (`cellxgene.census`)
- **No authentication required** for public data

## Key Literature

- **Megill et al. 2021** "cellxgene: a performant, scalable exploration platform for high dimensional sparse matrices" (bioRxiv preprint). Describes the CellxGene platform architecture and exploration capabilities. [DOI: 10.1101/2021.04.05.438318](https://doi.org/10.1101/2021.04.05.438318)
- **CZ CELLxGENE Discover** (Chan Zuckerberg Initiative, 2023). CellxGene Census provides programmatic access to the entire CellxGene data corpus as a single unified dataset. [https://cellxgene.cziscience.com/](https://cellxgene.cziscience.com/)
- **Regev et al. 2017** "The Human Cell Atlas" (eLife, ~1,500 citations). The vision paper for comprehensive single-cell reference maps of all human cells. CellxGene Census is the largest realization of this vision. [DOI: 10.7554/eLife.27041](https://doi.org/10.7554/eLife.27041)
- **Tabula Sapiens Consortium 2022** "The Tabula Sapiens: A multiple-organ, single-cell transcriptomic atlas of humans" (Science, ~800 citations). Multi-organ human cell atlas contributing to CellxGene Census. [DOI: 10.1126/science.abl4896](https://doi.org/10.1126/science.abl4896)
- **ENCODE Project Consortium 2020** (Nature, ~1,656 citations). The bulk regulatory element catalog that CellxGene single-cell data contextualizes. [DOI: 10.1038/s41586-020-2493-4](https://doi.org/10.1038/s41586-020-2493-4)

## When to Use This Skill

| Scenario | How CellxGene Helps |
|---------|-------------------|
| Bulk ENCODE peak near a gene — which cell type? | Query gene expression by cell type in matching tissue |
| ENCODE enhancer active in tissue X — cell-type-specific? | Check if enhancer target gene is restricted to one cell type |
| Choosing ENCODE cell line as proxy | Verify which primary cell type the cell line best represents |
| Interpreting differential peaks between tissues | Determine if difference is due to cell-type composition |
| Validating ENCODE scATAC-seq findings | Cross-reference with CellxGene scRNA-seq for same cell types |
| Designing follow-up experiments | Identify which cell types to isolate for validation |

## Python API Reference

### Installation

```bash
pip install cellxgene-census
```

Requires Python 3.8+. The package uses TileDB-SOMA for efficient data access.

### Core API Pattern

```python
import cellxgene_census

# Open the Census (reads metadata, does not download all data)
with cellxgene_census.open_soma() as census:
    # Access human data
    human = census["census_data"]["homo_sapiens"]

    # Query specific genes in specific tissues/cell types
    # This is where filtering happens — be specific to control memory
```

## Step 1: Identify the ENCODE Target Gene

Start from an ENCODE finding — a regulatory element near a gene of interest:

```
# Find enhancers in pancreas
encode_search_experiments(
    assay_title="Histone ChIP-seq",
    target="H3K27ac",
    organ="pancreas",
    biosample_type="tissue"
)

# Get peaks
encode_list_files(
    experiment_accession="ENCSR...",
    file_format="bed",
    output_type="IDR thresholded peaks",
    assembly="GRCh38"
)
```

From peaks, identify the nearest gene(s). You need the gene symbol or Ensembl ID.

## Step 2: Query CellxGene Census for Cell-Type Expression

### Basic Gene Expression Query

```python
import cellxgene_census
import pandas as pd

gene_symbol = "INS"  # Insulin — example for pancreas

with cellxgene_census.open_soma() as census:
    human = census["census_data"]["homo_sapiens"]

    # Get expression for INS in pancreas tissue
    # Use obs_value_filter to restrict to pancreas
    # Use var_value_filter to restrict to the gene
    adata = cellxgene_census.get_anndata(
        census,
        organism="Homo sapiens",
        var_value_filter=f"feature_name == '{gene_symbol}'",
        obs_value_filter="tissue_general == 'pancreas'",
        obs_column_names=["cell_type", "tissue", "disease", "dataset_id"]
    )

    # Summarize expression by cell type
    expr_by_celltype = adata.to_df().join(adata.obs["cell_type"])
    summary = expr_by_celltype.groupby("cell_type").agg(
        mean_expr=(gene_symbol, "mean"),
        pct_expressed=(gene_symbol, lambda x: (x > 0).mean() * 100),
        n_cells=(gene_symbol, "count")
    ).sort_values("mean_expr", ascending=False)

    print(summary.head(10))
```

### Multi-Gene Query

```python
genes_of_interest = ["INS", "GCG", "SST", "PPY"]  # Islet hormones

with cellxgene_census.open_soma() as census:
    gene_filter = " or ".join([f"feature_name == '{g}'" for g in genes_of_interest])

    adata = cellxgene_census.get_anndata(
        census,
        organism="Homo sapiens",
        var_value_filter=gene_filter,
        obs_value_filter="tissue_general == 'pancreas'",
        obs_column_names=["cell_type", "tissue", "disease"]
    )
```

### Query by Cell Ontology Term

```python
# More precise than tissue — query specific cell types
with cellxgene_census.open_soma() as census:
    adata = cellxgene_census.get_anndata(
        census,
        organism="Homo sapiens",
        var_value_filter="feature_name == 'INS'",
        obs_value_filter="cell_type == 'type B pancreatic cell'",  # Cell Ontology term for beta cells
        obs_column_names=["cell_type", "tissue", "disease", "sex"]
    )
```

## Step 3: Map CellxGene Cell Types to ENCODE Biosamples

CellxGene uses Cell Ontology (CL) terms. ENCODE uses its own biosample ontology. Key mappings:

| CellxGene Cell Type (CL term) | ENCODE Biosample | Notes |
|-------------------------------|-----------------|-------|
| type B pancreatic cell | pancreatic beta cell | Beta cells |
| hepatocyte | hepatocyte | Direct match |
| CD4-positive, alpha-beta T cell | CD4+ T cell | ENCODE may have more specific subtypes |
| monocyte | monocyte | Direct match |
| excitatory neuron | neuron | ENCODE may use broader category |
| oligodendrocyte | oligodendrocyte | Direct match |
| fibroblast | fibroblast | Direct match |
| endothelial cell | endothelial cell of umbilical vein (HUVEC) | ENCODE often uses HUVEC cell line |
| erythrocyte | K562 (CML, erythroid features) | K562 is a proxy, not primary |

### Getting Available Cell Types for a Tissue

```python
with cellxgene_census.open_soma() as census:
    # Get all cell types observed in pancreas
    obs_df = cellxgene_census.get_obs(
        census,
        organism="Homo sapiens",
        value_filter="tissue_general == 'pancreas'",
        column_names=["cell_type"]
    )
    cell_types = obs_df["cell_type"].value_counts()
    print(cell_types)
```

## Step 4: Interpret Cell-Type Expression in ENCODE Context

### Interpretation Framework

```
IF gene is expressed in only ONE cell type in the tissue:
    -> Bulk ENCODE peak near that gene likely reflects that cell type
    -> Example: INS expressed only in beta cells -> pancreas H3K27ac peak at INS is beta-cell-driven

IF gene is expressed in MULTIPLE cell types:
    -> Bulk ENCODE peak could be from any contributing cell type
    -> Need additional evidence (cell-type-specific TF, scATAC-seq) to resolve

IF gene is expressed at low levels in the dominant cell type:
    -> Bulk signal may be weak despite real expression
    -> Example: A gene at 100 TPM in beta cells (2% of pancreas) shows ~2 TPM in bulk

IF gene is NOT expressed in any cell type in the tissue:
    -> ENCODE peak near that gene likely regulates a DIFFERENT gene
    -> Check other nearby genes, or consider long-range regulation
```

### Estimating Bulk Signal Contribution

```python
# Simple deconvolution estimate
# If beta cells = 2% of pancreas, and INS = 500 TPM in beta cells:
# Expected bulk signal contribution = 0.02 * 500 = 10 TPM
# This matches GTEx pancreas INS ~400 TPM (higher due to actual beta cell fraction ~5-10%)

cell_fraction = 0.05  # estimated fraction of cell type in tissue
sc_expression = 500   # TPM in the specific cell type
estimated_bulk = cell_fraction * sc_expression
```

## Step 5: Cross-Reference with ENCODE scATAC-seq

ENCODE has single-cell ATAC-seq data for some tissues. These provide cell-type-resolved chromatin accessibility that directly complements CellxGene scRNA-seq.

```
# Find ENCODE single-cell data
encode_search_experiments(
    assay_title="snATAC-seq",
    organ="pancreas"
)

encode_search_experiments(
    assay_title="scRNA-seq",
    organ="pancreas"
)
```

When both ENCODE scATAC-seq and CellxGene scRNA-seq are available for the same tissue:
1. Use CellxGene to identify which cell types express the gene
2. Use ENCODE scATAC-seq to confirm chromatin accessibility at the regulatory element in those cell types
3. Convergent evidence (expression + accessibility in same cell type) is strongest

## Step 6: Present Results

### Cell-Type Expression Summary Table

| Cell Type | N Cells | Mean Expression | % Expressing | ENCODE Biosample Available | Bulk Contribution |
|-----------|---------|----------------|-------------|---------------------------|-------------------|
| type B pancreatic cell | 12,456 | 487.3 | 92% | pancreatic beta cell (limited) | ~24 TPM (5% fraction) |
| acinar cell | 45,678 | 0.1 | 2% | pancreas tissue (bulk) | ~0.08 TPM |
| ductal cell | 8,901 | 0.0 | 0% | — | 0 TPM |
| alpha cell | 9,234 | 0.0 | 0% | — | 0 TPM |

### Key Numbers to Report

- Gene queried and tissue
- Total cells analyzed and number of datasets
- Number of cell types with expression (> threshold)
- Dominant cell type and its expression level
- Estimated contribution to bulk ENCODE signal
- Whether ENCODE has cell-type-specific data for validation

## Pitfalls & Edge Cases

- **Cell type ontology inconsistency**: Different datasets in CellxGene use different cell type annotation schemes. "Macrophage" in one dataset may be labeled "M1 macrophage" or "tissue-resident macrophage" in another. Use Cell Ontology IDs for consistent matching.
- **Batch effects across studies**: CellxGene aggregates data from many labs. Direct comparison of expression values across datasets requires batch correction (Harmony, scVI). Raw counts are NOT comparable.
- **Sparse single-cell data**: scRNA-seq has high dropout rates. A gene showing 0 expression in a cell may still be expressed — zero does not mean absent. Use imputation cautiously.
- **Species mismatch with ENCODE**: CellxGene contains both human and mouse data. Ensure you match the species when cross-referencing with ENCODE experiments. Gene symbols may differ between species.
- **Dataset size affects resolution**: Large datasets (>100K cells) can resolve rare cell types that small datasets miss. Check dataset size before concluding a cell type is absent.

## Walkthrough: Single-Cell Resolution for ENCODE Bulk Epigenomic Data

**Goal**: Use CellxGene single-cell RNA-seq atlases to deconvolve which cell types within a tissue contribute to ENCODE bulk epigenomic signals.
**Context**: ENCODE bulk ChIP-seq/ATAC-seq captures signals from all cell types in a tissue. CellxGene reveals the cellular composition.

### Step 1: Find ENCODE bulk experiments for a tissue

```
encode_search_experiments(assay_title="ATAC-seq", organ="lung", organism="Homo sapiens")
```

Expected output:
```json
{
  "total": 14,
  "results": [
    {"accession": "ENCSR500LNG", "assay_title": "ATAC-seq", "biosample_summary": "lung", "status": "released"}
  ]
}
```

### Step 2: Query CellxGene for lung cell types

Using CellxGene Census API (via skill guidance):
```python
import cellxgene_census
census = cellxgene_census.open_soma()
lung_cells = census["census_data"]["homo_sapiens"].obs.read(
    value_filter="tissue_general == 'lung'",
    column_names=["cell_type", "tissue"]
).concat().to_pandas()
lung_cells["cell_type"].value_counts().head(10)
```

Expected output:
```
AT2 cell                 45,230
macrophage               32,100
endothelial cell         28,450
AT1 cell                 22,890
fibroblast               18,670
ciliated cell            15,320
basal cell                9,850
club cell                 7,200
NK cell                   6,100
dendritic cell            4,800
```

**Interpretation**: AT2 cells dominate (45K cells) — bulk ATAC-seq signal likely reflects AT2 accessibility primarily. Immune cells (macrophages, NK, dendritic) contribute ~25% of cells.

### Step 3: Identify cell-type markers for deconvolution

For each cell type, identify marker genes with high expression specificity. Use these to estimate which fraction of the ENCODE bulk signal comes from each cell type.

### Step 4: Cross-reference with ENCODE single-cell data

```
encode_search_experiments(assay_title="snATAC-seq", organ="lung", organism="Homo sapiens")
```

Expected output:
```json
{
  "total": 4,
  "results": [
    {"accession": "ENCSR600SCA", "assay_title": "scATAC-seq", "biosample_summary": "lung", "status": "released"}
  ]
}
```

**Interpretation**: 4 scATAC-seq experiments available in lung. Compare cell-type accessibility profiles from scATAC-seq with the bulk ATAC-seq to validate deconvolution estimates.

### Integration with downstream skills
- Cell-type composition informs **compare-biosamples** interpretation of tissue differences
- Cell-type markers feed into **gtex-expression** for bulk deconvolution validation
- Cell-type-specific peaks from scATAC-seq integrate with **regulatory-elements**
- Cell-type proportions inform **disease-research** for cell-type-specific disease mechanisms

## Code Examples

### 1. Find ENCODE single-cell experiments for CellxGene comparison
```
encode_search_experiments(assay_title="scRNA-seq", organ="brain", organism="Homo sapiens")
```

Expected output:
```json
{
  "total": 22,
  "results": [
    {"accession": "ENCSR700SCR", "assay_title": "scRNA-seq", "biosample_summary": "brain", "status": "released"}
  ]
}
```

### 2. Survey single-cell data availability
```
encode_get_facets(assay_title="scRNA-seq", facet_field="organ", organism="Homo sapiens")
```

Expected output:
```json
{
  "facets": {
    "organ": {"brain": 22, "blood": 15, "lung": 8, "heart": 6, "liver": 4}
  }
}
```

### 3. Compare bulk vs single-cell experiments
```
encode_compare_experiments(accession_1="ENCSR500LNG", accession_2="ENCSR600SCA")
```

Expected output:
```json
{
  "comparison": {
    "shared": {"organ": "lung", "organism": "Homo sapiens"},
    "differences": {
      "assay": ["ATAC-seq", "scATAC-seq"],
      "biosample": ["lung", "lung"]
    }
  }
}
```

## Integration

| This skill produces... | Feed into... | Purpose |
|---|---|---|
| Cell-type composition estimates | **compare-biosamples** | Explain tissue differences by cellular composition |
| Cell-type marker genes | **gtex-expression** | Validate markers against GTEx bulk expression |
| Cell-type-specific gene sets | **peak-annotation** | Assign peaks to cell-type-specific genes |
| Deconvolution proportions | **disease-research** | Identify disease-relevant cell types within tissues |
| Single-cell expression matrix | **scrna-meta-analysis** | Integrate CellxGene data with ENCODE scRNA-seq |
| Cell-type-resolved enhancers | **regulatory-elements** | Map cCREs to specific cell types |
| Cell-type abundance data | **visualization-workflow** | Generate UMAP/t-SNE plots alongside epigenomic data |

## Presenting Results

When reporting CellxGene expression context:

- **Expression table**: Present a table with columns: cell_type, mean_expression, pct_expressing, n_cells, and tissue_source for the queried gene(s)
- **Dataset metadata**: Report the CellxGene Census version/snapshot date, organism, tissue filter applied, and whether disease samples were included or excluded
- **Key fields to include**: Gene symbol, Ensembl ID, tissue of origin, number of datasets contributing, and total cells queried
- **Always report**: Whether expression values are raw counts or normalized (log1p), the `obs_value_filter` used, and any cell type ontology terms (CL IDs) for reproducibility
- **Context to provide**: Note that cross-dataset expression comparisons are affected by protocol differences (10x v2 vs v3 vs Smart-seq2) and that presence/absence is more robust than quantitative levels across studies
- **Next steps**: Suggest `single-cell-encode` for ENCODE-specific scRNA-seq data, or `gtex-expression` for complementary bulk tissue expression context

## Related Skills

- `single-cell-encode` — Working with ENCODE's own single-cell data (scATAC-seq, scRNA-seq)
- `regulatory-elements` — Characterizing the bulk ENCODE regulatory elements that CellxGene contextualizes
- `gtex-expression` — Bulk tissue expression from GTEx (complements CellxGene single-cell)
- `cross-reference` — Linking ENCODE experiments to external databases
- `compare-biosamples` — Comparing ENCODE data across biosamples informed by cell-type composition
- `epigenome-profiling` — Building tissue epigenomic profiles informed by cell-type context
- `publication-trust` — Verify literature claims backing analytical decisions

## For the request: "$ARGUMENTS"
