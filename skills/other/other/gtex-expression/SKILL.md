---
name: gtex-expression
description: "Guide for integrating GTEx tissue expression data with ENCODE regulatory elements. Use when users need to check if a gene is expressed in a tissue, correlate regulatory elements with expression, or validate ENCODE findings against GTEx. Trigger on: GTEx, tissue expression, gene expression levels, expression atlas, eQTL, tissue-specific expression, TPM values."
---

# Integrating GTEx Tissue Expression with ENCODE Regulatory Data

Use GTEx gene expression across 54 human tissues to validate ENCODE regulatory element activity, establish enhancer-gene links, and provide tissue-specific expression context for functional genomics findings.

## Scientific Rationale

**The question**: "Is the gene near my ENCODE regulatory element actually expressed in the tissue where the element is active?"

ENCODE catalogs where regulatory elements exist (enhancers, promoters, insulators) but does not directly measure gene expression across a broad tissue panel. GTEx (Genotype-Tissue Expression) fills this gap by providing RNA-seq-based gene expression measurements across 54 human tissues from ~1,000 post-mortem donors. Integrating the two answers a fundamental question: does the regulatory landscape match the transcriptional output?

An active enhancer (H3K27ac+, ATAC-seq+) near a gene in pancreas tissue is much more meaningful if GTEx confirms the gene is highly expressed in pancreas. Conversely, an ENCODE enhancer near a gene with zero expression in the relevant tissue suggests the enhancer regulates a different gene, or acts in a cell-type subpopulation not captured by bulk GTEx.

### What GTEx Provides

- **Median gene expression (TPM)** across 54 human tissues from ~1,000 donors
- **Transcript-level expression** for isoform analysis
- **eQTLs** — variants associated with gene expression in specific tissues (cis and trans)
- **sQTLs** — variants associated with alternative splicing
- **Single-nucleus RNA-seq** for selected tissues (GTEx v8+)
- **Allele-specific expression** data

### Why Integrate with ENCODE

| ENCODE provides | GTEx provides | Together |
|----------------|--------------|---------|
| Where regulatory elements are | Where genes are expressed | Regulatory element-expression correlation |
| Tissue-specific enhancers | Tissue-specific expression | Enhancer-gene validation |
| TF binding sites | eQTLs in those sites | Functional variant identification |
| Chromatin accessibility | Expression levels | Accessibility-expression concordance |

## Key Literature

- **GTEx Consortium 2020** "The GTEx Consortium atlas of genetic regulatory effects across human tissues" (Science, ~4,000 citations). The flagship publication describing the v8 release with 17,382 samples across 54 tissues from 948 donors. Identified cis-eQTLs for 95% of genes, tissue-sharing patterns, and cell-type interaction eQTLs. [DOI: 10.1126/science.aaz1776](https://doi.org/10.1126/science.aaz1776)
- **Aguet et al. 2017** "Genetic effects on gene expression across human tissues" (Nature, ~3,000 citations). The v6p analysis establishing the multi-tissue eQTL framework, demonstrating widespread tissue-specific genetic regulation. [DOI: 10.1038/nature24277](https://doi.org/10.1038/nature24277)
- **ENCODE Project Consortium 2020** (Nature, ~1,656 citations). Registry of 926,535 human cCREs. Provides the regulatory element catalog to cross-reference with GTEx expression. [DOI: 10.1038/s41586-020-2493-4](https://doi.org/10.1038/s41586-020-2493-4)
- **Nasser et al. 2021** (Nature, ~468 citations). ABC model linking enhancers to genes using ENCODE data. GTEx expression validates ABC-predicted enhancer-gene pairs. [DOI: 10.1038/s41586-021-03446-x](https://doi.org/10.1038/s41586-021-03446-x)

## When to Use This Skill

| Scenario | How GTEx helps |
|---------|---------------|
| Found enhancer near gene X in ENCODE | Check if gene X is expressed in the matching tissue |
| GWAS variant in ENCODE peak | Query GTEx eQTLs to identify regulated gene |
| Comparing regulatory landscapes across tissues | Validate that differential enhancers correspond to differential expression |
| Designing functional validation | Confirm gene is expressed before investing in CRISPR/reporter assays |
| Interpreting TF ChIP-seq | Check if TF target genes show expected expression patterns |
| Choosing relevant ENCODE biosamples | Use GTEx to identify which tissues express your gene of interest |

## GTEx REST API Reference

**Base URL**: `https://gtexportal.org/api/v2`

No authentication required. Responses are JSON.

### Key Endpoints

| Endpoint | Purpose | Key Parameters |
|---------|---------|---------------|
| `/expression/geneExpression` | Median TPM by tissue for a gene | `geneId`, `datasetId` |
| `/expression/medianTranscriptExpression` | Transcript-level TPM by tissue | `geneId`, `datasetId` |
| `/eqtl/singleTissueEqtl` | eQTLs for a gene in a tissue | `geneId`, `tissueSiteDetailId`, `datasetId` |
| `/expression/topExpressedGene` | Most expressed genes in a tissue | `tissueSiteDetailId`, `datasetId` |
| `/dataset/tissueSiteDetail` | List all GTEx tissues with IDs | — |
| `/reference/gene` | Gene metadata lookup | `geneId` or `geneName` |

### Dataset IDs

- `gtex_v8` — Current release (54 tissues, 948 donors, 17,382 samples)

## Step 1: Identify the Gene of Interest from ENCODE Data

The starting point is typically an ENCODE finding — an active regulatory element near a gene:

```
# Find enhancers in pancreas
encode_search_experiments(assay_title="Histone ChIP-seq", target="H3K27ac", organ="pancreas")

# Get peak files
encode_list_files(
    experiment_accession="ENCSR...",
    file_format="bed",
    output_type="IDR thresholded peaks",
    assembly="GRCh38"
)
```

From the peak file, identify the nearest gene(s) to the enhancer. You will need the Ensembl gene ID (ENSG...) for GTEx queries.

## Step 2: Query GTEx for Gene Expression

### Get median expression across all tissues

```python
import requests

gene_id = "ENSG00000254647"  # INS (insulin)
url = f"https://gtexportal.org/api/v2/expression/geneExpression"
params = {
    "geneId": gene_id,
    "datasetId": "gtex_v8"
}

response = requests.get(url, params=params)
data = response.json()

# Each entry has: tissueSiteDetailId, median, geneSymbol, etc.
for entry in sorted(data["data"], key=lambda x: x["median"], reverse=True)[:10]:
    print(f"{entry['tissueSiteDetailId']}: {entry['median']:.1f} TPM")
```

### Get transcript-level expression

```python
url = "https://gtexportal.org/api/v2/expression/medianTranscriptExpression"
params = {
    "geneId": gene_id,
    "datasetId": "gtex_v8"
}
response = requests.get(url, params=params)
```

## Step 3: Map GTEx Tissues to ENCODE Biosamples

GTEx and ENCODE use different tissue nomenclature. Key mappings:

| GTEx tissueSiteDetailId | ENCODE organ/biosample | Notes |
|------------------------|----------------------|-------|
| `Pancreas` | pancreas | Direct match |
| `Liver` | liver | Direct match |
| `Brain_Cortex` | brain | GTEx has 13 brain sub-regions |
| `Brain_Hippocampus` | brain | Map to specific brain region |
| `Heart_Left_Ventricle` | heart | GTEx separates ventricle/atrial |
| `Heart_Atrial_Appendage` | heart | — |
| `Lung` | lung | Direct match |
| `Kidney_Cortex` | kidney | GTEx has cortex only |
| `Whole_Blood` | blood | ENCODE uses specific blood cell types |
| `Skin_Sun_Exposed_Lower_leg` | skin of body | GTEx has sun-exposed/not-exposed |
| `Adipose_Subcutaneous` | adipose tissue | GTEx has subcutaneous/visceral |
| `Muscle_Skeletal` | muscle | Direct match |
| `Stomach` | stomach | Direct match |
| `Small_Intestine_Terminal_Ileum` | intestine | Partial match |
| `Colon_Sigmoid` | large intestine | GTEx has sigmoid/transverse |

To get the full list of GTEx tissue IDs:

```python
url = "https://gtexportal.org/api/v2/dataset/tissueSiteDetail"
response = requests.get(url)
tissues = response.json()["data"]
for t in tissues:
    print(f"{t['tissueSiteDetailId']}: {t['tissueSiteDetail']}")
```

## Step 4: Interpret TPM Values

### Expression Thresholds

| TPM Range | Interpretation | ENCODE Implication |
|-----------|---------------|-------------------|
| 0 | Not detected | Regulatory elements likely inactive or regulating a different gene |
| 0.1 - 1 | Low / noise threshold | May reflect rare cell-type expression in bulk tissue |
| 1 - 10 | Expressed | Regulatory elements expected to show moderate activity |
| 10 - 100 | Moderately expressed | Strong expectation of active promoter + enhancers |
| 100 - 1,000 | Highly expressed | Expect broad H3K27ac, multiple enhancers |
| >1,000 | Very highly expressed | Tissue-defining genes (e.g., INS in pancreas at ~400 TPM) |

**The 1 TPM threshold**: Widely used as a minimum for "expressed" status. Below this, signal is difficult to distinguish from noise in bulk RNA-seq. However, genes expressed in rare cell types within a tissue (e.g., beta cells in pancreas) may show low bulk TPM but high single-cell expression.

### Tissue Specificity Metric

Calculate the tau specificity index (Yanai et al. 2005):

```python
import numpy as np

def tau_specificity(tpm_values):
    """Calculate tissue specificity (0 = ubiquitous, 1 = tissue-specific)."""
    if max(tpm_values) == 0:
        return 0
    x = np.array(tpm_values) / max(tpm_values)
    n = len(x)
    return sum(1 - x) / (n - 1)
```

- tau > 0.8: Highly tissue-specific (e.g., INS in pancreas, ALB in liver)
- tau 0.4 - 0.8: Moderately specific
- tau < 0.4: Broadly expressed (housekeeping genes)

## Step 5: Cross-Reference ENCODE Regulatory Elements with GTEx Expression

### Validation Logic

```
IF ENCODE shows active enhancer (H3K27ac+) near gene X in tissue T
AND GTEx shows gene X expressed (TPM > 1) in tissue T
THEN: Consistent — regulatory element likely drives expression

IF ENCODE shows active enhancer near gene X in tissue T
AND GTEx shows gene X NOT expressed (TPM < 1) in tissue T
THEN: Discordant — enhancer may regulate a different gene, or
      expression is cell-type-specific (below bulk detection)

IF GTEx shows gene X highly expressed in tissue T
AND ENCODE shows NO active enhancer near gene X in tissue T
THEN: Regulatory data may be incomplete for this tissue,
      or regulation is promoter-driven (check H3K4me3)
```

### Using ENCODE Tools for Cross-Referencing

```
# Check what ENCODE regulatory data exists for the GTEx tissue
encode_get_facets(organ="pancreas")

# Get H3K27ac (enhancer) data
encode_search_experiments(
    assay_title="Histone ChIP-seq",
    target="H3K27ac",
    organ="pancreas",
    biosample_type="tissue"
)

# Get ATAC-seq (accessibility) data
encode_search_experiments(
    assay_title="ATAC-seq",
    organ="pancreas",
    biosample_type="tissue"
)
```

## Step 6: eQTL Integration

GTEx eQTLs identify variants that regulate gene expression. These can be cross-referenced with ENCODE peaks.

### Query eQTLs for a Gene

```python
url = "https://gtexportal.org/api/v2/eqtl/singleTissueEqtl"
params = {
    "geneId": "ENSG00000254647",
    "tissueSiteDetailId": "Pancreas",
    "datasetId": "gtex_v8"
}
response = requests.get(url, params=params)
eqtls = response.json()["data"]

# Each eQTL has: variantId, pValue, nes (effect size), tissueSiteDetailId
for eqtl in eqtls[:5]:
    print(f"{eqtl['variantId']}: p={eqtl['pValue']:.2e}, NES={eqtl['nes']:.3f}")
```

### GTEx-ENCODE eQTL Workflow

1. Get eQTLs for gene of interest in relevant tissue
2. Convert GTEx variant IDs to genomic coordinates (format: `chr1_12345_A_G_b38`)
3. Intersect eQTL positions with ENCODE peak files (H3K27ac, ATAC-seq, TF ChIP-seq)
4. eQTLs falling in active regulatory elements are high-confidence regulatory variants
5. Check the `variant-annotation` skill for full variant prioritization

## Step 7: R Workflow Example

```r
library(httr)
library(jsonlite)

# Query GTEx API
gene_id <- "ENSG00000254647"
url <- paste0("https://gtexportal.org/api/v2/expression/geneExpression",
              "?geneId=", gene_id, "&datasetId=gtex_v8")
response <- GET(url)
data <- fromJSON(content(response, "text", encoding = "UTF-8"))

# Create expression table
expr_df <- data.frame(
  tissue = data$data$tissueSiteDetailId,
  median_tpm = data$data$median,
  stringsAsFactors = FALSE
)
expr_df <- expr_df[order(-expr_df$median_tpm), ]

# Filter to tissues matching ENCODE organs
encode_tissues <- c("Pancreas", "Liver", "Lung", "Heart_Left_Ventricle",
                    "Brain_Cortex", "Kidney_Cortex")
matched <- expr_df[expr_df$tissue %in% encode_tissues, ]
print(matched)
```

## Walkthrough: Tissue-Specific Expression Context for ENCODE Enhancer Targets

**Goal**: Use GTEx expression data to validate that genes near ENCODE enhancers are expressed in the expected tissue, providing functional context for epigenomic findings.
**Context**: ENCODE identifies enhancers by chromatin marks, but expression data confirms the target gene is active in the same tissue.

### Step 1: Identify enhancer target genes from ENCODE

Start with H3K27ac ChIP-seq peaks near gene promoters:
```
encode_search_experiments(assay_title="Histone ChIP-seq", organ="liver", target="H3K27ac", organism="Homo sapiens")
```

Expected output:
```json
{
  "total": 8,
  "results": [
    {"accession": "ENCSR123LIV", "assay_title": "Histone ChIP-seq", "biosample_summary": "liver", "target": "H3K27ac"}
  ]
}
```

### Step 2: Query GTEx for tissue-specific expression

Using the GTEx REST API (via skill guidance):
```
GET https://gtexportal.org/api/v2/expression/medianGeneExpression?gencodeId=ENSG00000134243&tissueSiteDetailId=Liver
```

Expected response:
```json
{
  "medianGeneExpression": [
    {"geneSymbol": "SORT1", "tissueSiteDetailId": "Liver", "median": 45.2, "unit": "TPM"},
    {"geneSymbol": "SORT1", "tissueSiteDetailId": "Brain_Cortex", "median": 12.8, "unit": "TPM"},
    {"geneSymbol": "SORT1", "tissueSiteDetailId": "Heart_Left_Ventricle", "median": 2.1, "unit": "TPM"}
  ]
}
```

**Interpretation**: SORT1 is highly expressed in liver (45.2 TPM) — consistent with the H3K27ac enhancer mark in liver tissue. The 22x enrichment over heart confirms tissue-specific regulation.

### Step 3: Validate multi-gene enhancer targets

For each gene near an ENCODE enhancer peak, check GTEx expression:
- Tissue-matched expression (TPM > 5) = **concordant** (enhancer is near an active gene)
- No expression in tissue (TPM < 1) = **discordant** (enhancer may regulate a different gene, or the gene is active in a rare cell subtype)

### Step 4: Track validated experiments

```
encode_track_experiment(accession="ENCSR123LIV", notes="Liver H3K27ac - validated with GTEx expression for SORT1, PCSK9")
```

### Integration with downstream skills
- Enhancer targets from **peak-annotation** provide gene lists to query in GTEx
- GTEx tissue specificity informs **disease-research** for tissue-relevant disease genes
- Compare GTEx bulk expression with **cellxgene-context** single-cell data for cell-type resolution
- GTEx eQTL data connects to **gwas-catalog** trait-associated variants

## Code Examples

### 1. Find ENCODE experiments matching a GTEx tissue
```
encode_search_experiments(assay_title="Histone ChIP-seq", organ="brain", target="H3K27ac", organism="Homo sapiens")
```

Expected output:
```json
{
  "total": 24,
  "results": [
    {"accession": "ENCSR456BRN", "assay_title": "Histone ChIP-seq", "biosample_summary": "brain", "target": "H3K27ac"}
  ]
}
```

### 2. Explore available ENCODE data for GTEx tissues
```
encode_get_facets(facet_field="organ", assay_title="Histone ChIP-seq", organism="Homo sapiens")
```

Expected output:
```json
{
  "facets": {
    "organ": {"brain": 45, "liver": 18, "heart": 15, "lung": 12, "kidney": 8}
  }
}
```

### 3. Get file details for expression comparison
```
encode_list_files(accession="ENCSR456BRN", file_format="bed", output_type="IDR thresholded peaks", assembly="GRCh38")
```

Expected output:
```json
{
  "files": [
    {"accession": "ENCFF789IDR", "output_type": "IDR thresholded peaks", "file_format": "bed narrowPeak", "file_size_mb": 1.2}
  ]
}
```

## Integration

| This skill produces... | Feed into... | Purpose |
|---|---|---|
| Tissue-specific gene expression (TPM) | **peak-annotation** | Validate enhancer target gene assignments with expression evidence |
| GTEx eQTL associations | **gwas-catalog** | Connect GWAS variants to expression-altering mechanisms |
| Tissue expression profiles | **disease-research** | Identify disease-relevant tissues for ENCODE data selection |
| Multi-tissue expression matrix | **visualization-workflow** | Generate tissue expression heatmaps alongside epigenomic data |
| Expression-validated gene lists | **regulatory-elements** | Prioritize cCREs near expressed genes |
| GTEx tissue matches | **cellxgene-context** | Compare bulk (GTEx) vs single-cell expression resolution |
| Tissue-specific genes | **compare-biosamples** | Identify genes differentially expressed between ENCODE biosamples |

## Presenting Results

### Expression Summary Table

| Tissue | GTEx Median TPM | Rank (of 54) | ENCODE Data Available | Concordance |
|--------|----------------|-------------|----------------------|-------------|
| Pancreas | 387.2 | 1 | H3K27ac, ATAC-seq, RNA-seq | Active enhancer confirmed |
| Liver | 0.3 | 48 | H3K27ac, ATAC-seq | No active enhancer (expected) |
| Brain_Cortex | 0.0 | 54 | H3K27ac, ATAC-seq, Hi-C | No signal (expected) |

### Key Numbers to Report

- Gene symbol and Ensembl ID
- TPM in target tissue and rank across all 54 tissues
- Tissue specificity (tau index)
- Number of tissues where gene is expressed (TPM > 1)
- Whether ENCODE regulatory data is concordant
- eQTL count in target tissue (if queried)

## Pitfalls & Edge Cases

- **GTEx tissue names ≠ ENCODE organ names**: GTEx uses specific tissue subregions (e.g., "Brain - Cortex", "Brain - Cerebellum") while ENCODE uses broader organ terms ("brain"). Map carefully using the GTEx tissue-to-ENCODE organ mapping table.
- **GTEx v8 vs v10 coordinate differences**: GTEx v8 uses GRCh38 but gene models differ from v10. Ensure you match the GTEx version to your GENCODE annotation version.
- **Bulk tissue heterogeneity**: GTEx expression represents a mixture of cell types. A gene with "low" GTEx expression may be highly expressed in a rare cell type. Use single-cell deconvolution for cell-type resolution.
- **eQTL effect sizes are tissue-specific**: A variant that is an eQTL in liver may not be one in pancreas. Never assume eQTL effects generalize across tissues — always check the specific tissue of interest.
- **TPM normalization caveats**: GTEx TPM values cannot be directly compared across tissues with very different transcriptome compositions. Use the GTEx-provided median TPM or normalized values for cross-tissue comparisons.

## Related Skills

- `variant-annotation` — Full variant interpretation workflow using ENCODE functional data
- `disease-research` — Disease-focused ENCODE analysis workflows
- `regulatory-elements` — Characterizing ENCODE regulatory elements near expressed genes
- `cellxgene-context` — Single-cell expression context when GTEx bulk is insufficient
- `cross-reference` — Linking ENCODE experiments to GTEx and other external databases
- `ensembl-annotation` — Gene annotation, VEP, and coordinate conversion
- `publication-trust` — Verify literature claims backing analytical decisions

## For the request: "$ARGUMENTS"
