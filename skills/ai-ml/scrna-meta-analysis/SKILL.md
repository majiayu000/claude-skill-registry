---
name: scrna-meta-analysis
description: Conduct rigorous cross-study meta-analysis of scRNA-seq data from ENCODE, integrating multiple single-cell transcriptomic datasets for a tissue/cell type. Use when the user wants to answer "what cell types exist in my tissue and what genes define them?" by combining scRNA-seq data across donors, labs, and platforms. Follows the Mawla et al. 2019 framework for assessing cross-study reproducibility, TIN-based quality filtering, and detection-limit-aware interpretation. Handles batch correction (Harmony/Seurat), dropout awareness, cross-contamination artifacts, and platform-specific biases. Use this skill for ANY scRNA-seq integration task, cross-dataset comparison, cell atlas construction, or reproducibility assessment involving ENCODE single-cell data.
---

# Cross-Study Meta-Analysis of scRNA-seq Data

## When to Use

- User wants to perform meta-analysis across multiple single-cell RNA-seq datasets
- User asks about "scRNA-seq meta-analysis", "dataset integration", "batch correction", or "cross-study comparison"
- User needs to harmonize cell type annotations across studies from different labs
- User wants to build reference atlases or identify conserved cell populations across datasets
- Example queries: "integrate 5 scRNA-seq datasets from different labs", "harmonize cell type labels across studies", "meta-analyze single-cell data for pancreas"

Integrate multiple ENCODE scRNA-seq datasets for a tissue/cell type into a unified cell atlas with reproducibility-aware quality assessment.

## Scientific Rationale

**The question**: "What cell types and transcriptional programs are present in my tissue, and which findings are reproducible across studies?"

Unlike bulk genomic assays (ChIP-seq, ATAC-seq) where signal detection is largely binary, single-cell transcriptomics operates at or below the limit of detection for most genes. This means that **heterogeneous detection is the norm, not the exception** — and distinguishing true biological heterogeneity from technical dropout is the central challenge of any scRNA-seq meta-analysis.

### The Core Problem (Mawla et al. 2019)

Mawla, van der Meulen & Huising (2019, Diabetes) conducted a landmark meta-analysis of five independent human pancreatic islet scRNA-seq studies and revealed:

1. **Sparse overlap in reported heterogeneity**: Not a single gene was highlighted as heterogeneously expressed across all five studies. Only 24 genes (1.2% of the top 2,000 variable genes per study) emerged as common drivers of beta-cell clustering across all five datasets.

2. **Detection is abundance-dependent**: Only 0.005–0.83% of genes are detected in ALL single cells in any study. The fraction of cells with detectable expression strongly correlates with transcript abundance — more abundant genes are detected in more cells.

3. **Quality gap with bulk RNA-seq**: TIN (Transcript Integrity Number) scores reveal that even highly abundant transcripts in scRNA-seq have lower coverage quality than bulk RNA-seq. Over half of genes in single-cell libraries have TIN scores <20, compared to uniformly high TIN scores in bulk.

4. **Cross-contamination from ambient RNA**: Species-mixing experiments (Macosko et al. 2015) showed 0.26–2.44% of reads in each single cell map to the wrong species. For highly abundant transcripts (INS, GCG), this ambient contamination alone can explain cross-detection between cell types.

5. **Known heterogeneity markers underdetected**: Established beta-cell heterogeneity markers (NPY, TH, UCN3, DKK3) were not independently identified by any "unbiased" scRNA-seq approach.

**Therefore: a meta-analysis of scRNA-seq data must prioritize reproducibility across studies and explicitly account for detection limits, rather than treating all zero values as biological absence.**

### Literature Support

- **Mawla, van der Meulen & Huising 2019** (Diabetes): Foundational cross-study meta-analysis framework. Introduced TIN-based quality assessment for scRNA-seq, demonstrated detection-limit artifacts, and proposed guidance for when to use single-cell vs bulk approaches. [DOI](https://doi.org/10.2337/dbi18-0019)
- **Tran et al. 2020** (Genome Biology, 854 citations): Benchmarked 14 batch-correction methods across 5 scenarios. Recommends Harmony first (fastest), then LIGER and Seurat 3 as alternatives. Evaluated using kBET, LISI, ASW, and ARI metrics. [DOI](https://doi.org/10.1186/s13059-019-1850-9)
- **Luecken & Theis 2019** (Molecular Systems Biology, 1,631 citations): Current best practices for scRNA-seq analysis — QC, normalization, batch correction, feature selection, dimensionality reduction, clustering, and differential expression. The standard reference for any scRNA-seq workflow. [DOI](https://doi.org/10.15252/msb.20188746)
- **Andreatta et al. 2023** (Nature Communications): STACAS — semi-supervised integration that leverages prior cell type knowledge. Outperforms unsupervised methods when partial cell type labels are available. Particularly relevant when integrating across studies where some cell types are shared but not all. [DOI](https://doi.org/10.1038/s41467-024-45062-7)
- **Zappia et al. 2025** (Nature Methods): Benchmarked feature selection methods for integration. Confirms highly variable gene selection is effective; provides guidance on number of features, batch-aware selection, and interaction with integration models. [DOI](https://doi.org/10.1038/s41592-025-02625-w)
- **Stuart et al. 2019** (Cell, 8,400+ citations): Seurat v3 — CCA-based anchor identification for cross-dataset integration. The most widely used integration framework. [DOI](https://doi.org/10.1016/j.cell.2019.05.031)
- **Korsunsky et al. 2019** (Nature Methods, 3,200+ citations): Harmony — fast, scalable iterative soft clustering for batch correction. Works in PCA space, preserving biological variance while removing batch effects. [DOI](https://doi.org/10.1038/s41592-019-0619-0)
- **Macosko et al. 2015** (Cell): Drop-seq — original species-mixing experiment quantifying ambient RNA contamination at 0.26–2.44% of reads per cell. Critical control for interpreting cross-cell-type transcript detection. [DOI](https://doi.org/10.1016/j.cell.2015.05.002)
- **Squair et al. 2021** (Nature Communications, 700+ citations): Demonstrated that pseudobulk differential expression dramatically outperforms single-cell-level tests (Wilcoxon, MAST, etc.) for multi-sample comparisons. Now the recommended standard. [DOI](https://doi.org/10.1038/s41467-021-25960-2)
- **Young & Beber 2020** (Genome Biology, SoupX): Ambient RNA removal from droplet-based scRNA-seq. Essential preprocessing step to remove contaminating transcripts from lysed cells before integration.
- **Lopez et al. 2018** (Nature Methods, 2,700+ citations): scVI — deep generative model for single-cell transcriptomics. Provides a probabilistic framework for batch correction, visualization, clustering, and differential expression, accounting for both biological and technical noise. [DOI](https://doi.org/10.1038/s41592-018-0229-2)
- **Xu et al. 2021** (Molecular Systems Biology): scANVI — semi-supervised variant of scVI for cell type annotation during integration. Leverages existing cell state annotations to improve both integration quality and automatic annotation transfer across datasets. [DOI](https://doi.org/10.15252/msb.20209620)
- **Luecken et al. 2022** (Nature Methods, 700+ citations): Benchmarked 68 method+preprocessing combinations across 85 batches (>1.2 million cells) in 13 atlas-level integration tasks. Found scANVI, Scanorama, scVI, and scGen perform best on complex tasks. HVG selection improves performance; scaling hurts biology preservation. Provides the scIB benchmarking framework (14 metrics). [DOI](https://doi.org/10.1038/s41592-021-01336-8)
- **Xu et al. 2023** (Cell, CellHint): Automatic cell-type harmonization across datasets. Uses predictive clustering trees to resolve differences in annotation resolution and technical biases. Applied to 12 tissues from 38 datasets (~3.7M cells). Essential when integrating datasets that use different cell type ontologies. [DOI](https://doi.org/10.1016/j.cell.2023.11.026)
- **Domínguez Conde et al. 2022** (Science, CellTypist): Automated cross-tissue cell type annotation using machine learning. Surveyed 16 tissues from 12 donors (~360,000 cells). CellTypist provides pre-trained models for rapid, reproducible cell type annotation that reduces subjectivity. [DOI](https://doi.org/10.1126/science.abl5197)

## Step 1: Find All Available scRNA-seq Experiments

Search for all single-cell RNA-seq data for the target tissue:

```
encode_search_experiments(
    assay_title="scRNA-seq",
    organ="pancreas",            # user's tissue of interest
    limit=100
)
```

If no results for "scRNA-seq", broaden the search:
```
encode_search_experiments(
    search_term="single cell RNA",
    organ="pancreas",
    limit=100
)
```

Also check for 10x Chromium, Smart-seq2, Drop-seq, or other specific platforms:
```
encode_get_facets(
    assay_title="scRNA-seq",
    organ="pancreas"
)
```

Present a summary table showing:
- Number of experiments and total cells estimated
- Platforms used (10x Chromium v2/v3, Smart-seq2, Drop-seq, etc.)
- Labs represented
- Number of unique donors/biosamples
- Organism (never mix human and mouse in integration)

**Platform matters**: Smart-seq2 captures full-length transcripts with higher gene detection per cell but lower throughput. Droplet-based methods (10x, Drop-seq) provide higher cell counts but with 3' bias and lower genes/cell. Integration across platforms requires explicit batch correction (see Step 4).

## Step 2: Quality-Gate Each Experiment

For each experiment, assess quality:

```
encode_get_experiment(accession="ENCSR...")
```

### Include if:
- Released status with no ERROR audit flags
- Has gene quantification files (TSV format)
- Reported cell counts >500 (very small datasets add noise disproportionate to information)
- Library complexity reported (unique genes/cell)

### Exclude if:
- ERROR audit flags
- Extremely low cell counts (<200) unless rare cell type study
- Known quality issues in audit details (e.g., low mapping rate, high mitochondrial fraction)
- No gene-level quantification available

### Key QC Metrics to Record Per Study:
| Metric | Acceptable Range | Red Flag |
|--------|-----------------|----------|
| Genes/cell (median) | 1,000–6,000 (droplet) / 3,000–10,000 (plate) | <500 |
| UMI/cell (median) | 2,000–20,000 (droplet) | <1,000 |
| Mitochondrial % | <10–20% | >25% |
| Doublet rate | <5% estimated | >10% |
| Mapping rate | >80% | <60% |

Track all included experiments:
```
encode_track_experiment(accession="ENCSR...", notes="scRNA-seq meta-analysis")
```

## Step 3: Download Gene Quantification Files

For each passing experiment:

```
encode_list_files(
    experiment_accession="ENCSR...",
    file_format="tsv",
    output_type="gene quantifications",
    assembly="GRCh38",     # human; mm10 for mouse
    preferred_default=True
)
```

If gene quantifications aren't available, check for:
```
encode_list_files(
    experiment_accession="ENCSR...",
    file_format="h5ad",     # AnnData format
    preferred_default=True
)
```

Or raw data:
```
encode_list_files(
    experiment_accession="ENCSR...",
    file_format="fastq",
    output_type="reads"
)
```

Download selected files:
```
encode_download_files(
    file_accessions=["ENCFF..."],
    download_dir="/path/to/scrna_meta/",
    organize_by="experiment"
)
```

## Step 4: Integration Strategy

The choice of integration method should follow the Tran et al. 2020 benchmark hierarchy:

### Decision Tree

```
Are datasets from the SAME platform?
├── YES: Seurat v5 IntegrateLayers() or Harmony
│         └── Batch variable = donor/sample
└── NO: Different platforms (e.g., 10x + Smart-seq2)
    ├── Harmony (recommended first — fast, robust)
    ├── scVI/scANVI (deep generative — best for atlas-level tasks per Luecken 2022)
    │   └── scANVI if partial cell type labels available (semi-supervised)
    ├── Seurat v5 with rpca or cca reduction
    └── STACAS if partial cell type labels available (semi-supervised)

Do cell type ontologies DIFFER across datasets?
├── YES: Use CellHint (Xu 2023) to harmonize cell type labels first
│         └── Builds a predictive clustering tree resolving resolution differences
└── NO: Proceed directly to integration
```

### Method Selection Guide (Luecken et al. 2022 Benchmark)

For atlas-level integration (>1M cells, many batches), the scIB benchmark found:
- **scANVI** — best overall when partial labels available (semi-supervised)
- **scVI** — best overall unsupervised (probabilistic, scalable)
- **Scanorama** — strong performance, deterministic
- **Harmony** — fast, good for simple batch structures
- **Seurat CCA/rPCA** — well-established, good for moderate complexity

HVG selection improves all methods. Scaling (z-score per gene) biases methods toward batch removal at the expense of biological conservation — avoid unless specifically needed.

### Integration Workflow (Scanpy/Seurat)

**Pre-integration QC (per dataset)**:
1. Filter cells: nGene > 200, nGene < [98th percentile], mito% < 20%
2. Filter genes: expressed in >= 3 cells
3. Remove ambient RNA — directly addresses the cross-contamination artifact described by Macosko et al. 2015:
   - **CellBender** (recommended, best-in-class): Probabilistic deep generative model that distinguishes cell-containing from empty droplets and removes ambient RNA. Works on raw (unfiltered) count matrices.
   - **SoupX**: Requires a cluster assignment to estimate contamination profile. Simpler but less accurate for complex experiments.
   - **DecontX** (celda package): Alternative for Bioconductor workflows.
4. Remove doublets (Scrublet or DoubletFinder)
5. Normalize: LogNormalize (Seurat) or scran pooling (Scanpy)
6. Identify highly variable genes: 2,000–3,000 HVGs per dataset

**Integration**:
1. Find shared HVGs across all datasets (union or intersection depending on method)
2. Run integration using chosen method:
   - **Harmony**: Run on PCA space, fast, deterministic
   - **Seurat v5**: CCA or rPCA anchors with IntegrateLayers()
   - **scVI**: Train on raw counts with batch covariate, produces latent space
   - **scANVI**: Like scVI but incorporate known cell type labels (semi-supervised)
3. Validate integration with scIB metrics (Luecken et al. 2022):
   - **Batch mixing**: kBET, iLISI, graph connectivity (higher = better mixing)
   - **Biology preservation**: cLISI, ARI, NMI, isolated label score (should retain cell type separation)
   - **Overall score**: Weighted combination of batch + bio metrics (default: 40% batch, 60% bio)
   - **Silhouette scores**: Per cell type before and after integration

**Post-integration**:
1. UMAP/tSNE on corrected embedding
2. Leiden/Louvain clustering at multiple resolutions
3. Marker gene identification per cluster

### Cell Type Annotation (Post-Clustering)

After clustering, annotate cell types using complementary approaches:

1. **Manual annotation**: Canonical marker genes per cluster (most reliable, slowest)
2. **CellTypist** (Domínguez Conde et al. 2022): Pre-trained ML models for automated annotation. Available models span multiple tissues. Fast, reproducible, reduces annotator subjectivity.
3. **scANVI** (Xu et al. 2021): If used for integration, simultaneously provides cell type probability scores per cell. Natural companion to scVI-based workflows.
4. **Reference mapping**: Project query cells onto a reference atlas (e.g., Azimuth for well-characterized tissues)

### Cell Type Harmonization (Cross-Study)

When combining datasets from different groups, cell type annotations often differ:
- "T cell" vs. "CD4+ T cell" vs. "CD4+ naïve T cell" — different granularity
- "Macrophage" vs. "Monocyte-derived macrophage" — overlapping definitions

Use **CellHint** (Xu et al. 2023) to resolve these differences:
1. Build a predictive clustering tree that relates cell types hierarchically
2. Identify when two datasets use different names for the same population
3. Reveal when one dataset's annotation is a sub-type of another's
4. Create a harmonized cell type ontology for the integrated atlas

## Step 5: Reproducibility Assessment (Following Mawla et al. 2019)

This is the critical step that distinguishes a meta-analysis from simple dataset merging. After integration, assess what is reproducible:

### 5a. Cross-Study Marker Overlap

For each cell type cluster, identify marker genes per original study independently:
- Perform differential expression within each study's cells separately
- Compare the top N marker genes across studies
- Report the **intersection** of markers found in ALL studies vs. study-specific markers

**Interpretation framework** (from Mawla et al. 2019):
- Genes in the intersection across all studies = **high-confidence markers**
- Genes found in only 1 study = likely technical artifacts, dropout patterns, or study-specific confounders
- Use a Venn diagram or UpSet plot to visualize overlap

### 5b. TIN-Based Quality Assessment

For datasets where BAM files are available, compute TIN scores to assess transcript coverage quality:

- Genes with TIN > 50: high-quality detection, reliable for heterogeneity claims
- Genes with TIN 20–50: moderate quality, interpret with caution
- Genes with TIN < 20: poor coverage, 3' bias dominates — dropout is likely technical

**Over half of genes in single-cell libraries have TIN < 20** (Mawla et al. 2019). This means claims about heterogeneous expression for low-TIN genes should be tempered.

### 5c. Detection Rate vs. Abundance Correlation

For key genes of interest, plot:
- X-axis: Average expression level (log CPM)
- Y-axis: Fraction of cells with detectable expression

This reveals whether "heterogeneous expression" is actually heterogeneous detection driven by operating at the detection limit. Genes with high expression but low detection rates warrant investigation for technical artifacts.

### 5d. Cross-Contamination Check

For cell types with highly abundant, type-specific transcripts (e.g., INS in beta-cells, GCG in alpha-cells):
- Check if the "other type's" marker is detected at levels below the 0.26–2.44% ambient RNA threshold (Macosko et al. 2015)
- If cross-detection is below this threshold, it cannot be taken as proof of true co-expression
- Report this explicitly in any findings about multi-hormone cells

## Step 6: Downstream Analysis

After establishing the reproducible cell atlas:

### Differential Expression
- Use **pseudobulk** approaches (aggregate cells per donor/sample, then use DESeq2/edgeR) — this is now the recommended standard over single-cell-level tests
- Pseudobulk avoids inflated p-values from treating individual cells as independent observations
- Require minimum cell counts per pseudobulk sample (>10 cells per cell type per donor)

### Cell Proportion Analysis
- Estimate cell type proportions per donor
- Use compositional analysis (e.g., scCODA, propeller) for condition comparisons
- Proportions are confounded by dissociation protocol efficiency across cell types

### Trajectory Analysis
- Only meaningful if developmental or differentiation continuum is expected
- Use established methods (Monocle3, PAGA, Slingshot)
- Validate trajectories by checking known temporal markers

## Step 7: Log Provenance

Log the integrated dataset:
```
encode_log_derived_file(
    file_path="/path/to/integrated_atlas.h5ad",
    source_accessions=["ENCSR...", "ENCSR...", ...],
    description="Integrated scRNA-seq atlas of [tissue], N donors, N cells",
    file_type="integrated_atlas",
    tool_used="Seurat v5 / Harmony / Scanpy",
    parameters="HVGs=3000, resolution=0.5, batch_key=donor"
)
```

## Pitfalls and Edge Cases

### Platform Mixing Caveats
- **Never treat Smart-seq2 and 10x cells as equivalent** without batch correction — gene detection rates differ 2-3x
- Smart-seq2 captures full-length transcripts; 10x is 3'-biased. Gene body coverage patterns differ fundamentally
- If mixing platforms, always verify that known cell types cluster by biology, not by platform

### Overcorrection
- Integration can merge biologically distinct populations if correction is too aggressive
- Always compare integrated vs. unintegrated results
- If two known cell types merge after integration, reduce the correction strength
- STACAS with prior labels helps prevent overcorrection

### Small Cell Populations
- Rare cell types (<1% of total) may be lost during integration
- Consider analyzing rare populations separately from the main integration
- Use targeted subclustering after initial broad classification

### Donor Effects vs. Batch Effects
- Multiple donors from the same study share batch effects
- Multiple studies may share donors (check!)
- When possible, separate donor effects from platform/lab effects in the integration model

### scRNA-seq vs. Bulk: When to Use What (Mawla et al. 2019 Guidance)
| Experimental Goal | Recommended Approach |
|---|---|
| Identify cell types | scRNA-seq |
| Resolve rare populations | scRNA-seq (high cell count) |
| Differential expression in known cell types | Bulk RNA-seq of FACS-sorted populations |
| Detect low-abundance transcripts | Bulk RNA-seq |
| Validate heterogeneity claims | Orthogonal validation (IF, FISH) |
| Developmental trajectories | scRNA-seq (with pseudotime) |

### Assembly Mismatch
- NEVER integrate human (GRCh38) and mouse (mm10) data without explicit ortholog mapping
- Even within species, ensure all datasets use the same genome annotation version (GENCODE)

### Cross-Species Integration
- If comparing human and mouse scRNA-seq (e.g., for conserved cell types), use one-to-one ortholog genes only
- Gene name conversion is not trivial — many genes have species-specific paralogs
- Use established ortholog mapping resources (ENSEMBL BioMart, HGNC)
- Expect species-specific cell populations and gene expression differences even for conserved cell types
- Validate cross-species findings with independent approaches (e.g., ISH, IHC)

### Foundation Models (Emerging, Not Yet Standard)
- **scGPT** (Cui et al. 2024, Nature Methods) and similar foundation models show promise for zero-shot cell annotation and integration
- These models are pre-trained on large corpora of scRNA-seq data and can transfer knowledge to new datasets
- **Caveat**: Foundation models are rapidly evolving and not yet established as the standard approach. They may outperform traditional methods in some contexts but underperform in others (especially rare cell types and non-standard tissues)
- **Recommendation**: Use as a complementary check, not as the sole integration/annotation strategy. Always validate against marker-gene-based approaches

## Summary Statistics to Report

For the final integrated atlas, report:
- Total cells after QC (per study and total)
- Number of studies, donors, platforms
- Ambient RNA removal method used and estimated contamination rate
- Integration method and parameters
- scIB benchmark metrics if computed (batch mixing + bio conservation scores)
- Number of clusters and cell type annotations
- Cell type annotation method (manual, CellTypist, scANVI, reference mapping)
- Cell type harmonization approach if cross-study labels differed (CellHint)
- Cross-study marker overlap statistics
- Known marker detection rates per cell type
- Any TIN-based quality assessments performed

## Walkthrough: Cross-Study scRNA-seq Meta-Analysis for ENCODE Brain Data

**Goal**: Integrate single-cell RNA-seq datasets from multiple ENCODE experiments and external sources to build a unified cell-type reference atlas for brain regulatory analysis.
**Context**: Individual scRNA-seq experiments capture limited cell diversity. Meta-analysis across studies increases statistical power and cell-type coverage.

### Step 1: Find ENCODE scRNA-seq experiments

```
encode_search_experiments(assay_title="scRNA-seq", organ="brain", organism="Homo sapiens")
```

Expected output:
```json
{
  "total": 22,
  "results": [
    {"accession": "ENCSR700SCR", "assay_title": "scRNA-seq", "biosample_summary": "brain", "status": "released"},
    {"accession": "ENCSR701FRC", "assay_title": "scRNA-seq", "biosample_summary": "frontal cortex", "status": "released"},
    {"accession": "ENCSR702CRB", "assay_title": "scRNA-seq", "biosample_summary": "cerebellum", "status": "released"}
  ]
}
```

**Interpretation**: 22 brain scRNA-seq experiments across multiple brain regions. Select experiments with compatible protocols (10x Chromium v3) for integration.

### Step 2: Download count matrices

```
encode_list_files(accession="ENCSR700SCR", file_format="h5ad", assembly="GRCh38")
```

Expected output:
```json
{
  "files": [
    {"accession": "ENCFF800H5A", "output_type": "gene quantifications", "file_format": "h5ad", "file_size_mb": 320}
  ]
}
```

### Step 3: Integrate datasets

Meta-analysis pipeline:
1. **Quality filter** each dataset independently (genes in ≥3 cells, cells with ≥200 genes, <20% mitochondrial)
2. **Normalize** with scran or Seurat SCTransform
3. **Integrate** using Harmony, scVI, or Seurat CCA to remove batch effects while preserving biology
4. **Cluster** with Leiden algorithm at multiple resolutions
5. **Annotate** clusters using known marker genes and CellxGene reference

### Step 4: Validate cell-type annotations

Cross-reference with → **cellxgene-context** for consensus cell-type labels:
- Neurons (excitatory, inhibitory subtypes)
- Astrocytes, oligodendrocytes, OPCs
- Microglia, endothelial cells

### Step 5: Track all integrated experiments

```
encode_track_experiment(accession="ENCSR700SCR", notes="Brain scRNA-seq for cross-study meta-analysis - 10x Chromium v3")
```

Expected output:
```json
{
  "status": "tracked",
  "accession": "ENCSR700SCR",
  "notes": "Brain scRNA-seq for cross-study meta-analysis - 10x Chromium v3"
}
```

### Integration with downstream skills
- Cell-type annotations feed into → **cellxgene-context** for atlas cross-reference
- Cell-type marker genes inform → **peak-annotation** for cell-type-specific peak assignment
- Meta-analysis results connect to → **single-cell-encode** for ENCODE-specific analysis
- Cell-type proportions feed into → **compare-biosamples** for tissue composition comparison
- Marker gene lists integrate with → **gtex-expression** for bulk expression validation

## Code Examples

### 1. Survey scRNA-seq data availability
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

### 2. Compare experiments for batch effect awareness
```
encode_compare_experiments(accession_1="ENCSR700SCR", accession_2="ENCSR701FRC")
```

Expected output:
```json
{
  "comparison": {
    "shared": {"assay": "scRNA-seq", "organism": "Homo sapiens"},
    "differences": {
      "biosample": ["brain", "frontal cortex"],
      "lab": ["/labs/bing-ren/", "/labs/joe-ecker/"]
    }
  }
}
```

### 3. Get collection summary of integrated datasets
```
encode_summarize_collection()
```

Expected output:
```json
{
  "total_tracked": 8,
  "by_assay": {"scRNA-seq": 5, "scATAC-seq": 3},
  "by_organ": {"brain": 8}
}
```

## Integration

| This skill produces... | Feed into... | Purpose |
|---|---|---|
| Unified cell-type annotations | **cellxgene-context** | Cross-reference with CellxGene atlas |
| Cell-type marker genes | **peak-annotation** | Assign regulatory peaks to cell-type-specific genes |
| Integrated expression matrix | **single-cell-encode** | Cell-type-resolved ENCODE analysis |
| Cell-type proportions | **compare-biosamples** | Quantify tissue composition differences |
| Cell-type-specific gene sets | **gtex-expression** | Validate markers against bulk expression |
| Batch-corrected embeddings | **visualization-workflow** | Generate UMAP/t-SNE plots |
| Cell-type DEGs | **disease-research** | Connect cell types to disease mechanisms |
| Meta-analysis QC metrics | **quality-assessment** | Validate cross-study integration quality |

## Presenting Results

When reporting scRNA-seq meta-analysis results:

- **Dataset table**: Present a table with columns: study (first author + year), GEO/ENCODE accession, total_cells, technology (10x v2/v3, Smart-seq2), species, tissue, and whether the dataset passed QC
- **Integration summary**: Report integration method (Harmony, scVI, scANVI, BBKNN), key parameters (n_latent, batch_key), number of cells before and after QC filtering, and scIB benchmark metrics if computed (batch mixing score, biological conservation score)
- **Marker gene table**: Present top markers per cell type with columns: cell_type, gene, log2FC, pct_in (% expressing in cluster), pct_out (% in other clusters), adjusted_p-value, and cross-study reproducibility (detected in N/M datasets)
- **Always report**: Cell type annotation method (manual, CellTypist, reference mapping), total clusters identified, cell type harmonization approach if cross-study labels differed, and scanpy/Seurat version used
- **Context to provide**: Note which datasets dominate each cluster (composition bias), whether rare cell types were only detected in specific studies, and any TIN-based quality concerns
- **Next steps**: Suggest `multi-omics-integration` to combine the meta-analysis with ENCODE epigenomic layers, or `cellxgene-context` for validation against CellxGene Census expression data

## Related Skills

- `single-cell-encode` — Finding and downloading ENCODE single-cell datasets
- `quality-assessment` — Evaluating ENCODE experiment quality metrics
- `histone-aggregation` — Aggregating histone ChIP-seq peaks (complementary epigenomic layer)
- `accessibility-aggregation` — Aggregating ATAC-seq peaks (complementary chromatin layer)
- `multi-omics-integration` — Combining scRNA-seq with ATAC-seq, histone, and TF data
- `publication-trust` — Verify literature claims backing analytical decisions

## For the request: "$ARGUMENTS"
