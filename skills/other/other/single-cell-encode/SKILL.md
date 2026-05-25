---
name: single-cell-encode
description: Find and work with ENCODE single-cell genomics data including scRNA-seq and scATAC-seq. Use when the user asks about single-cell experiments, cell type resolution, clustering from ENCODE data, deconvolution of bulk signals using single-cell references, or comparing single-cell vs bulk profiles. Covers platform differences (10X Chromium, Smart-seq2, Drop-seq), quality limitations of single-cell data, multimodal integration (RNA+ATAC), and cross-study reproducibility concerns. Also use for cell type annotation, gene detection limits, dropout artifacts, and single-cell data structure in ENCODE.
---

# Single-Cell ENCODE Data

## When to Use

- User wants to find or analyze single-cell data (scRNA-seq, scATAC-seq, snRNA-seq) from ENCODE
- User asks about "single-cell", "scRNA-seq", "scATAC-seq", "cell type annotation", or "single-nucleus"
- User needs to integrate ENCODE single-cell data with bulk epigenomic profiles
- User wants to identify cell-type-specific regulatory elements from single-cell chromatin accessibility
- Example queries: "find scRNA-seq data in ENCODE for brain", "what snATAC-seq is available?", "integrate single-cell with bulk ChIP-seq"

Help the user find and work with ENCODE single-cell genomics data, understand quality limitations relative to bulk assays, and integrate single-cell with bulk ENCODE profiles for cell-type-resolved regulatory analysis.

## Literature Foundation

| # | Reference | Key Contribution |
|---|-----------|-----------------|
| 1 | Mawla & Huising 2019, Endocrinology, DOI:10.1210/en.2018-01037 (~200 cit) | Cross-study scRNA-seq meta-analysis revealing that only ~1-2% of heterogeneity-driving genes replicate across studies; TIN-based quality assessment; detection-limit awareness framework. PMC6609986. |
| 2 | Regev et al. 2017, eLife, DOI:10.7554/eLife.27041 (~1,200 cit) | Human Cell Atlas white paper defining the vision for comprehensive single-cell reference maps of all human cells. Establishes community standards for cell atlas construction. |
| 3 | Stuart et al. 2019, Cell, DOI:10.1016/j.cell.2019.05.031 (~7,000 cit) | Seurat v3 — CCA-based anchor identification for cross-dataset integration. The most widely used scRNA-seq integration framework. |
| 4 | Luecken & Theis 2019, Mol Syst Biol, DOI:10.15252/msb.20188746 (~1,500 cit) | Current best practices for scRNA-seq analysis: QC, normalization, batch correction, feature selection, dimensionality reduction, clustering, and differential expression. |
| 5 | Buenrostro et al. 2015, Nature, DOI:10.1038/nature14590 (~1,800 cit) | Single-cell ATAC-seq method. Established that individual cells yield the same nucleosomal fragment size ladder as bulk ATAC-seq, enabling chromatin accessibility profiling at single-cell resolution. |
| 6 | Granja et al. 2021, Nat Genet, DOI:10.1038/s41588-021-00790-6 (~1,000 cit) | ArchR — scalable framework for scATAC-seq analysis including peak calling, gene activity scoring, trajectory inference, and integration with scRNA-seq. |
| 7 | Luecken et al. 2022, Nat Methods, DOI:10.1038/s41592-021-01336-8 (~800 cit) | Benchmarking atlas-level integration methods across tasks, metrics, and scalability. Establishes evaluation framework (kBET, LISI, ARI, NMI) for comparing integration quality. |
| 8 | Hao et al. 2021, Cell, DOI:10.1016/j.cell.2021.04.048 (~5,000 cit) | Seurat v4 — weighted nearest neighbors (WNN) for multimodal integration of RNA + ATAC (or CITE-seq). Defines the standard for joint profiling analysis. |
| 9 | ENCODE Project Consortium 2020, Nature, DOI:10.1038/s41586-020-2493-4 (~1,656 cit) | ENCODE Phase 3; registry of candidate cis-regulatory elements (cCREs) providing the bulk reference against which single-cell data can be compared. |

## Available Single-Cell Assays in ENCODE

| Assay | What It Measures | Key Outputs | Typical Files in ENCODE |
|-------|-----------------|-------------|------------------------|
| scRNA-seq | Single-cell gene expression | Cell-type-specific transcriptomes | FASTQ, gene quantifications (TSV), filtered count matrices, h5ad |
| scATAC-seq | Single-cell chromatin accessibility | Cell-type-specific regulatory elements | FASTQ, fragments (TSV), aggregate peaks (BED), cell-barcode assignments |

## Step 1: Search for Single-Cell Data in ENCODE

Search for scRNA-seq and scATAC-seq experiments in the tissue of interest:

```
# Single-cell RNA-seq
encode_search_experiments(
    assay_title="scRNA-seq",
    organ="pancreas",           # user's tissue of interest
    biosample_type="tissue",
    limit=50
)

# Single-cell ATAC-seq
encode_search_experiments(
    assay_title="snATAC-seq",
    organ="pancreas",
    biosample_type="tissue",
    limit=50
)
```

If no results, try broader search terms:
```
encode_search_experiments(search_term="single cell RNA", organ="pancreas", limit=50)
encode_search_experiments(search_term="single cell ATAC", organ="pancreas", limit=50)
```

Check facets first to understand what organs have single-cell data:
```
encode_get_facets(assay_title="scRNA-seq")
encode_get_facets(assay_title="snATAC-seq")
```

Present a summary to the user showing:
- Number of scRNA-seq and scATAC-seq experiments found
- Organs/tissues represented
- Platforms used (10X Chromium, Smart-seq2, Drop-seq)
- Labs contributing data
- Number of unique donors/biosamples

## Step 2: Understand ENCODE Single-Cell Data Structure

### scRNA-seq Files

Use `encode_list_files` to see what is available per experiment:

```
encode_list_files(
    experiment_accession="ENCSR...",
    assembly="GRCh38",
    preferred_default=True
)
```

Typical file hierarchy:
- **FASTQ** (`output_type="reads"`): Raw sequencing reads with cell barcodes and UMIs
- **Gene quantifications** (`output_type="gene quantifications"`, format TSV): Count matrices (genes x cells) after ENCODE uniform pipeline processing
- **Filtered counts** (`output_type="filtered feature barcode matrix"`): Post-QC cell-filtered matrices ready for analysis
- **h5ad**: AnnData format when available (convenient for Scanpy workflows)

### scATAC-seq Files

```
encode_list_files(
    experiment_accession="ENCSR...",
    file_format="bed",
    assembly="GRCh38"
)
```

Typical file hierarchy:
- **FASTQ** (`output_type="reads"`): Raw reads with cell barcodes
- **Fragments** (TSV/BED): Fragment files with cell-barcode assignments — the primary input for ArchR/Signac
- **Peaks** (BED narrowPeak): Aggregate peak calls across all cells (pseudo-bulk)
- **Cell assignments**: Barcode-to-cluster or barcode-to-cell-type mapping files

**Key difference**: scATAC-seq data is extremely sparse at the single-cell level. Most analyses operate on the fragment file, not on per-cell peak calls.

**ENCODE Blacklist filtering (required for scATAC-seq)**: Before any downstream analysis of scATAC-seq peaks or fragments, remove reads/peaks overlapping ENCODE Blacklist regions (Amemiya et al. 2019, Scientific Reports, 1,372 citations). These regions produce artifactual signal in chromatin accessibility assays and inflate per-cell quality metrics (TSS enrichment, FRiP). Both ArchR and Signac apply blacklist filtering by default when provided, but verify it is active. Download blacklists from [Boyle-Lab/Blacklist](https://github.com/Boyle-Lab/Blacklist):
- Human GRCh38: `hg38-blacklist.v2.bed.gz`
- Mouse mm10: `mm10-blacklist.v2.bed.gz`

## Step 3: Assess Single-Cell Quality (ENCODE-Specific Considerations)

Check experiment-level quality:
```
encode_get_experiment(accession="ENCSR...")
```

### Quality Metrics for scRNA-seq

| Metric | 10X Chromium | Smart-seq2 | Red Flag |
|--------|-------------|------------|----------|
| Genes per cell (median) | 1,500-4,000 | 4,000-8,000 | <500 |
| UMIs per cell (median) | 3,000-15,000 | N/A (no UMIs) | <1,000 |
| Mitochondrial % | <10-15% | <10-15% | >25% |
| Doublet rate (estimated) | 2-8% (cell-count dependent) | <2% (plate-based) | >10% |
| Mapping rate | >80% | >80% | <60% |
| Saturation | >40% | N/A | <20% |

### Quality Metrics for scATAC-seq

| Metric | Acceptable | Red Flag |
|--------|-----------|----------|
| Unique fragments per cell | >3,000 | <1,000 |
| TSS enrichment per cell | >5 | <2 |
| Fraction in peaks | >20% | <10% |
| Nucleosomal banding | Clear mono/di/tri pattern | Absent or noisy |
| Doublet rate | <5% | >10% |

### ENCODE Audit Flags

Apply the same audit hierarchy as bulk data:
- **ERROR**: Avoid unless no alternative
- **NOT_COMPLIANT**: Usable with caveats
- **WARNING**: Generally safe; document
- **INTERNAL_ACTION**: DCC processing notes; usually not a concern

Track passing experiments:
```
encode_track_experiment(accession="ENCSR...", notes="scRNA-seq, [tissue], [platform]")
```

## Step 4: Evaluate Cross-Study Comparability

**This is the most critical section.** Cross-study scRNA-seq comparisons are fraught with technical confounders (Mawla & Huising 2019). Before combining datasets, understand these fundamental limitations:

### The Detection Limit Problem
- **Gene detection**: Only 2,000-6,000 genes detected per cell vs. ~15,000 in a typical bulk RNA-seq library
- **Universal detection**: On average, only ~86 genes are consistently detected across ALL cells in a study
- **Dropout is abundance-dependent**: The fraction of cells with detectable expression correlates strongly with transcript abundance — this is a sensitivity floor, not biological heterogeneity

### Cross-Study Reproducibility (Mawla & Huising 2019)
- **Study-related confounders outweigh biological heterogeneity** in most comparisons
- Only **~1-2% of heterogeneity-driving genes** replicate across independent studies of the same tissue
- **~50% of clustering genes may be unique to a single dataset** — driven by platform, library prep, or processing differences rather than biology
- Established heterogeneity markers (e.g., NPY, TH, UCN3, DKK3 in pancreatic beta cells) were **not independently identified** by unbiased scRNA-seq approaches

### Platform Differences

| Feature | 10X Chromium | Smart-seq2 | Drop-seq |
|---------|-------------|------------|----------|
| Genes per cell | 1,500-4,000 | 4,000-8,000 | 1,000-3,000 |
| Throughput (cells) | 500-10,000 | 96-384 per plate | 500-5,000 |
| Coverage | 3' biased (polyA capture) | Full-length | 3' biased |
| UMI support | Yes | No | Yes |
| Cost per cell | Low ($0.05-0.10) | High ($1-5) | Low ($0.05-0.15) |
| Transcript detection | Lower per cell, more cells | Higher per cell, fewer cells | Lower per cell |
| Splice variant detection | No (3' only) | Yes (full-length) | No (3' only) |

**Never treat 10X and Smart-seq2 cells as equivalent without batch correction.** Gene detection rates differ 2-3x and coverage patterns are fundamentally different.

## Step 5: Compare with Bulk ENCODE Data

Single-cell findings should always be validated against bulk ENCODE data from the same tissue. This is where ENCODE's bulk catalog becomes invaluable:

```
# Find bulk RNA-seq for same tissue
encode_search_experiments(
    assay_title="total RNA-seq",
    organ="pancreas",
    biosample_type="tissue",
    limit=50
)

# Find bulk ATAC-seq for same tissue
encode_search_experiments(
    assay_title="ATAC-seq",
    organ="pancreas",
    biosample_type="tissue",
    limit=50
)
```

### Validation Strategy
1. **Marker gene validation**: Confirm that scRNA-seq-derived cell type markers are expressed in expected bulk profiles
2. **Detection rate calibration**: Genes detected in bulk but absent in single-cell are likely dropout, not true absence
3. **Pseudo-bulk comparison**: Aggregate single-cell data into pseudo-bulk profiles and correlate with real bulk. Pearson r > 0.8 expected for well-matched samples
4. **Quantitative sanity check**: If a gene is highly expressed in bulk (top 10%) but detected in <10% of cells in the relevant cell type, suspect technical dropout

### When Bulk Outperforms Single-Cell (Mawla & Huising 2019)
- **Low-abundance transcripts**: Bulk detects ~15,000 genes vs. 2,000-6,000 per cell
- **Differential expression**: Pseudobulk DE on FACS-sorted populations outperforms single-cell-level tests for known cell types
- **Transcript integrity**: TIN scores are uniformly higher in bulk; over half of genes in scRNA-seq have TIN <20

## Step 6: Integration Approaches

### scRNA-seq Integration (Stuart et al. 2019; Luecken et al. 2022)

**CCA/RPCA (Seurat)**: Canonical correlation analysis finds shared correlation structure across datasets. Use RPCA (reciprocal PCA) for large datasets (>100k cells) — faster and more memory-efficient. Best when cell types are shared across datasets.

**Harmony**: Fast iterative soft clustering in PCA space. Recommended as first-line approach by Tran et al. 2020. Works well across platforms.

**Evaluation metrics**: After integration, assess quality using kBET (batch mixing), iLISI (integration LISI, higher = better mixing), cLISI (cell-type LISI, should remain separated), ARI and NMI (cluster agreement with known labels).

### scATAC-seq Integration (Granja et al. 2021)

**ArchR**: The standard framework for scATAC-seq analysis and integration:
1. Create Arrow files from fragment files
2. Compute gene activity scores (accessibility near gene bodies as proxy for expression)
3. Dimensionality reduction on TF-IDF-normalized peak matrix or iterative LSI
4. Integration across samples using Harmony within ArchR
5. Peak calling on pseudo-bulk aggregates per cluster

**Signac (Seurat ecosystem)**: Alternative for users in the Seurat workflow. Uses LSI dimensionality reduction and integrates with Seurat's anchor-based methods.

### Multimodal Integration: RNA + ATAC (Hao et al. 2021)

For 10X Multiome (joint RNA + ATAC profiling from same cell):

**Weighted Nearest Neighbors (WNN)**: Constructs a joint graph from both modalities, weighting each modality per cell based on its informativeness. A cell in a region with distinctive chromatin but generic expression will weight ATAC more heavily, and vice versa.

```
# Conceptual Seurat v4/v5 WNN workflow:
# 1. Process RNA: NormalizeData -> FindVariableFeatures -> ScaleData -> RunPCA
# 2. Process ATAC: RunTFIDF -> FindTopFeatures -> RunSVD (LSI)
# 3. Joint: FindMultiModalNeighbors(reduction.list = list("pca", "lsi"), dims.list = list(1:30, 2:30))
# 4. Cluster on WNN graph: FindClusters(graph.name = "wsnn")
# 5. UMAP: RunUMAP(nn.name = "weighted.nn")
```

For **unpaired** RNA and ATAC (from different cells/experiments):
- Use ArchR's `addGeneIntegrationMatrix` to transfer RNA labels to ATAC cells
- Or use Seurat's `FindTransferAnchors` between RNA reference and ATAC query (using gene activity scores)

## Step 7: Cell-Type Deconvolution of Bulk Signals

Use scRNA-seq references to deconvolve bulk ENCODE data — this assigns bulk signal to cell types without running single-cell experiments:

### RNA Deconvolution
- **MuSiC** (Wang et al. 2019): Uses scRNA-seq reference to estimate cell type proportions in bulk RNA-seq. Accounts for cross-subject variability.
- **CIBERSORTx** (Newman et al. 2019): Signature matrix from scRNA-seq applied to bulk expression. Also performs digital cytometry (cell-type-specific gene expression from bulk).

### Chromatin Deconvolution
- **scATAC-seq peak sets per cell type** can be used to partition bulk ChIP-seq or ATAC-seq signal
- Overlap bulk peaks with cell-type-specific accessible regions to infer which cell types contribute to bulk signal

## Step 8: Integrate with Bulk Epigenomic Profiles

The ultimate value of ENCODE single-cell data is connecting cell-type-resolved expression to the deep bulk epigenomic catalog:

1. **Assign bulk ChIP-seq peaks to cell types**: Overlap bulk histone mark peaks with scATAC-seq cell-type accessibility. A bulk H3K27ac peak that overlaps a beta-cell-specific scATAC peak is likely a beta-cell enhancer.

2. **Build cell-type regulatory networks**: Combine scRNA-seq (which genes) with scATAC-seq (which regulatory elements) and bulk TF ChIP-seq (which factors bind) to reconstruct cell-type-specific GRNs.

3. **Validate cell-type-specific regulomes**: Check that predicted enhancers (from scATAC) overlap expected histone marks in bulk (H3K4me1 + H3K27ac = active enhancer; H3K4me1 + H3K27me3 = poised enhancer).

4. **Chromatin state annotation per cell type**: Use ENCODE cCRE registry (ENCODE Phase 3) as the reference and assign each cCRE to contributing cell types based on scATAC-seq accessibility.

```
# Find ENCODE cCREs for comparison
encode_search_files(
    output_type="candidate Cis-Regulatory Elements",
    assembly="GRCh38",
    organ="pancreas"
)
```

## Step 9: Document and Track

Log all analyses for provenance:

```
encode_track_experiment(accession="ENCSR...", notes="scRNA-seq [tissue], included in single-cell analysis")

encode_log_derived_file(
    file_path="/path/to/sc_analysis/integrated_atlas.h5ad",
    source_accessions=["ENCSR...", "ENCSR..."],
    description="Integrated scRNA-seq atlas of [tissue], N donors, N cells, [platform(s)]",
    file_type="integrated_atlas",
    tool_used="Seurat v5 / ArchR / Scanpy",
    parameters="Integration method, HVGs, resolution, batch variables"
)
```

Link any relevant publications or external datasets:
```
encode_link_reference(
    experiment_accession="ENCSR...",
    reference_type="pmid",
    reference_id="31305906",
    description="Mawla & Huising 2019 - cross-study scRNA-seq reproducibility framework"
)
```

## scATAC-seq Specific Considerations

### Fragment Size Distribution
scATAC-seq produces the same nucleosomal fragment size ladder as bulk ATAC-seq (Buenrostro et al. 2015):
- **Sub-nucleosomal** (<147 bp): Open chromatin, TF-bound regions
- **Mono-nucleosomal** (~200 bp): Single nucleosome wrapping
- **Di-nucleosomal** (~400 bp): Two nucleosomes
- **Tri-nucleosomal** (~600 bp): Three nucleosomes

The presence of this banding pattern per cell is a key quality indicator. Cells without clear banding should be filtered.

### TSS Enrichment
Per-cell TSS enrichment measures signal pileup at transcription start sites. Minimum threshold of 4-5 is standard (ArchR default = 4). Low TSS enrichment indicates poor signal-to-noise in that cell.

### Sparsity
The peak-cell matrix is extremely sparse (~2-5% non-zero entries). This is fundamentally different from scRNA-seq sparsity:
- scRNA-seq zeros are a mix of dropout and true absence
- scATAC-seq zeros are overwhelmingly true absence (each cell has only 2 alleles per locus, and Tn5 sampling is stochastic)

This extreme sparsity motivates:
- Gene activity scoring (aggregating signal across gene body + promoter) rather than per-peak analysis
- Pseudo-bulk aggregation by cluster for peak calling
- Topic modeling (cisTopic) or LSI rather than PCA for dimensionality reduction

## Cross-Study Integration Checklist (Based on Mawla & Huising 2019)

Before combining any single-cell datasets, verify each item:

- [ ] **Same organism and assembly**: Never mix GRCh38 and hg19; never mix human and mouse without ortholog mapping
- [ ] **Platform documented**: Record platform for each experiment (10X Chromium v2/v3/v3.1, Smart-seq2, Drop-seq, 10X Multiome)
- [ ] **Clustering not platform-driven**: After integration, check that clusters correspond to cell types, not to platform/donor/batch. UMAP colored by study should be intermingled within clusters.
- [ ] **Gene detection rates compared**: Before combining, tabulate median genes/cell per study. If rates differ >2x, expect batch effects to dominate.
- [ ] **Key markers validated against bulk**: Confirm top cluster markers are expressed in bulk RNA-seq of the same tissue. Markers absent from bulk may be artifacts.
- [ ] **TIN scores assessed** (if BAMs available): Genes with TIN <20 should not be the sole basis for heterogeneity claims
- [ ] **Ambient RNA removed**: For droplet-based data, apply SoupX or CellBender before integration to remove cross-contamination artifacts (Macosko et al. 2015 showed 0.26-2.44% ambient RNA per cell)
- [ ] **Technical confounders documented**: Record all known differences between datasets (dissociation protocol, sequencing depth, library prep date, operator, sequencing platform)

## Common Pitfalls

1. **Over-interpreting clusters**: Not every cluster represents a biologically distinct cell type. Clusters can be driven by cell cycle, dissociation stress, or ambient RNA contamination. Validate against known markers and orthogonal methods (immunohistochemistry, FISH).

2. **Batch-driven clustering**: If UMAP clusters correspond to studies rather than cell types, integration has failed or is insufficient. Always color UMAP by both cell type AND study origin. Technical variables (platform, donor) should not predict cluster membership.

3. **Low gene detection masquerading as heterogeneity**: With only 2,000-6,000 genes per cell and TIN <20 for most genes, apparent "heterogeneous expression" may reflect operating at the detection limit. Validate by checking whether detection fraction correlates with average expression (Mawla & Huising 2019).

4. **3' bias in droplet platforms**: 10X Chromium and Drop-seq capture only the 3' end of transcripts. Genes with alternative 3' UTRs, short 3' UTRs, or non-polyadenylated transcripts (some lncRNAs, histone mRNAs) may be systematically underdetected or absent. Do not interpret their absence as biological.

5. **Platform-specific artifacts**: Smart-seq2 is susceptible to length bias (longer genes detected more readily). 10X is susceptible to ambient RNA contamination and barcode swapping. Drop-seq has higher multiplet rates at high cell loading. Know your platform's failure modes.

6. **Doublets corrupting cluster identity**: Doublets can create false intermediate populations or inflate rare cell type counts. Apply computational doublet detection (Scrublet, DoubletFinder) before integration. Expected doublet rates for 10X: ~0.8% per 1,000 cells loaded.

7. **Reference dataset quality propagates**: If using scRNA-seq as a reference for deconvolution or label transfer to scATAC-seq, errors in the reference annotations propagate to all downstream analyses. Use well-validated references with marker gene support, not just unsupervised clustering labels.

## Walkthrough: Analyzing ENCODE Single-Cell Data for Cell-Type-Resolved Regulation

**Goal**: Discover and analyze ENCODE single-cell experiments (scRNA-seq, scATAC-seq) to identify cell-type-specific regulatory programs within complex tissues.
**Context**: ENCODE's single-cell experiments decompose bulk tissue signals into cell-type-specific profiles, revealing regulatory heterogeneity masked in bulk assays.

### Step 1: Survey available single-cell ENCODE data

```
encode_get_facets(assay_title="scRNA-seq", facet_field="organ", organism="Homo sapiens")
```

Expected output:
```json
{
  "facets": {
    "organ": {"brain": 22, "blood": 15, "lung": 8, "heart": 6, "liver": 4, "kidney": 3}
  }
}
```

**Interpretation**: Brain has the most scRNA-seq data (22 experiments). Brain's cellular diversity makes it ideal for single-cell analysis.

### Step 2: Find scATAC-seq experiments for the same tissue

```
encode_search_experiments(assay_title="snATAC-seq", organ="brain", organism="Homo sapiens")
```

Expected output:
```json
{
  "total": 12,
  "results": [
    {"accession": "ENCSR700SCA", "assay_title": "scATAC-seq", "biosample_summary": "brain", "status": "released"},
    {"accession": "ENCSR701CTX", "assay_title": "scATAC-seq", "biosample_summary": "cerebral cortex", "status": "released"}
  ]
}
```

### Step 3: Download single-cell data files

```
encode_list_files(accession="ENCSR700SCA", file_format="h5ad", assembly="GRCh38")
```

Expected output:
```json
{
  "files": [
    {"accession": "ENCFF800H5A", "output_type": "gene quantifications", "file_format": "h5ad", "file_size_mb": 320}
  ]
}
```

### Step 4: Compare with bulk ENCODE experiments

```
encode_search_experiments(assay_title="ATAC-seq", organ="brain", organism="Homo sapiens")
```

Expected output:
```json
{
  "total": 32,
  "results": [
    {"accession": "ENCSR800BLK", "assay_title": "ATAC-seq", "biosample_summary": "brain", "status": "released"}
  ]
}
```

**Interpretation**: Compare scATAC-seq cell-type clusters with bulk ATAC-seq peaks. Cell types that dominate the tissue (e.g., neurons) will contribute most to the bulk signal. Rare cell types (e.g., microglia) may have unique regulatory elements invisible in bulk data.

### Step 5: Integrate with external single-cell atlases

Use → **cellxgene-context** to access the CellxGene Census for additional single-cell reference data. Use → **scrna-meta-analysis** for cross-study integration.

### Integration with downstream skills
- scATAC-seq cell-type peaks feed into → **regulatory-elements** for cell-type-specific cCRE classification
- Cell-type marker genes integrate with → **cellxgene-context** for atlas comparison
- Cell-type-specific peaks feed into → **peak-annotation** for cell-type gene regulatory networks
- Cross-study integration via → **scrna-meta-analysis** for meta-analysis
- Bulk vs. single-cell comparison via → **compare-biosamples**

## Code Examples

### 1. Survey single-cell experiment availability
```
encode_get_facets(assay_title="snATAC-seq", facet_field="organ", organism="Homo sapiens")
```

Expected output:
```json
{
  "facets": {
    "organ": {"brain": 12, "blood": 8, "lung": 5, "heart": 3}
  }
}
```

### 2. Compare single-cell and bulk experiments
```
encode_compare_experiments(accession_1="ENCSR700SCA", accession_2="ENCSR800BLK")
```

Expected output:
```json
{
  "comparison": {
    "shared": {"organ": "brain", "organism": "Homo sapiens"},
    "differences": {
      "assay": ["scATAC-seq", "ATAC-seq"],
      "resolution": ["single-cell", "bulk"]
    }
  }
}
```

### 3. Track single-cell experiments
```
encode_track_experiment(accession="ENCSR700SCA", notes="Brain scATAC-seq for cell-type-specific regulatory analysis")
```

Expected output:
```json
{
  "status": "tracked",
  "accession": "ENCSR700SCA",
  "notes": "Brain scATAC-seq for cell-type-specific regulatory analysis"
}
```

## Integration

| This skill produces... | Feed into... | Purpose |
|---|---|---|
| Cell-type-specific peaks | **regulatory-elements** | Classify cCREs by cell type |
| Cell-type marker genes | **cellxgene-context** | Cross-reference with CellxGene atlas data |
| Cell-type peak sets | **peak-annotation** | Assign cell-type-specific regulatory elements to genes |
| Cross-study cell annotations | **scrna-meta-analysis** | Integrate ENCODE scRNA-seq across studies |
| Bulk vs. single-cell comparison | **compare-biosamples** | Quantify cell-type contributions to bulk signal |
| Cell-type accessibility profiles | **motif-analysis** | Discover cell-type-specific TF motifs |
| scATAC-seq fragment files | **visualization-workflow** | Generate cell-type-resolved browser tracks |
| Single-cell QC metrics | **quality-assessment** | Validate single-cell data quality |

## Related Skills

- **scrna-meta-analysis**: Deep cross-study meta-analysis workflow following Mawla et al. 2019 framework with full batch correction, reproducibility assessment, and pseudobulk DE. Use when combining multiple scRNA-seq datasets.
- **quality-assessment**: Evaluate ENCODE experiment quality metrics (FRiP, NSC, RSC, audit flags). Apply to both single-cell and bulk experiments before analysis.
- **compare-biosamples**: Compare data availability across tissues and cell types. Use to find which organs have both single-cell and bulk data for integrated analysis.
- **integrative-analysis**: Plan multi-omic integration across ENCODE experiments. Use when combining single-cell data with bulk histone, TF ChIP-seq, or methylation data.
- **multi-omics-integration**: Deep multi-omic regulatory landscape (enhancers, ChromHMM, TF networks). Single-cell data provides the cell type resolution needed for cell type-specific multi-omics.
- **regulatory-elements**: Discover enhancers, promoters, and insulators from ENCODE data. Cell-type-specific elements identified here can be cross-referenced with scATAC-seq accessibility.
- **histone-aggregation**: Pseudo-bulk peaks from scATAC-seq/scCUT&Tag are inputs for histone aggregation.
- **accessibility-aggregation**: Pseudo-bulk ATAC peaks from scATAC-seq feed into accessibility aggregation.
- **variant-annotation**: Cell type-resolved scATAC-seq peaks are valuable for variant annotation in heterogeneous tissues.
- **disease-research**: Single-cell data is critical for resolving cell type-specific disease mechanisms.
- **data-provenance**: Document all single-cell processing parameters, tool versions, and results.
- **cellxgene-context**: CellxGene single-cell atlas context for cross-referencing cell type annotations and expression profiles.
- **publication-trust**: Verify literature claims backing analytical decisions

## Presenting Results

- Present single-cell results as: cell_type | cluster | marker_genes | cell_count. Show UMAP/tSNE coordinates if available. Suggest: "Would you like to compare with bulk ENCODE data for the same tissue?"

## For the request: "$ARGUMENTS"
