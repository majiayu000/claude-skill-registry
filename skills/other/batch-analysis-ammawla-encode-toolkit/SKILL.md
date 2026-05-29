---
name: batch-analysis
description: "Guide for multi-experiment batch operations: QC screening, batch download, comparison, and report generation across many ENCODE experiments simultaneously. Use when users need to process 5+ experiments together, create experiment comparison tables, perform batch quality checks, or generate summary reports. Trigger on: batch analysis, multiple experiments, bulk processing, experiment comparison, batch QC, multi-sample, batch download, experiment table, summary report, collection analysis."
---

# Batch Analysis of ENCODE Experiments

## When to Use

- User wants to process, compare, or QC multiple ENCODE experiments simultaneously
- User asks about "batch analysis", "bulk processing", "experiment comparison table", or "multi-sample QC"
- User needs to screen 5+ experiments for quality before analysis
- User wants a summary report or comparison table across many experiments
- Example queries: "QC all H3K27ac experiments in liver", "compare quality across 10 ChIP-seq datasets", "batch download and summarize my experiment collection"

Help the user perform systematic batch operations across multiple ENCODE experiments. When working with 5 or more experiments -- common in cross-tissue comparisons, multi-mark epigenomic profiling, or large-scale data collection -- individual experiment-by-experiment workflows become impractical and error-prone. This skill covers batch discovery, quality screening, download management, pairwise comparison, and report generation using the ENCODE MCP tools.

## Literature Foundation

| Reference | Journal | Key Contribution | DOI | Citations |
|-----------|---------|-----------------|-----|-----------|
| ENCODE Project Consortium (2020) | Nature | Expanded encyclopedia of 926,535 candidate cis-regulatory elements across 1,698 cell types; framework for large-scale integrative analysis | [10.1038/s41586-020-2493-4](https://doi.org/10.1038/s41586-020-2493-4) | ~2,000 |
| Hitz et al. (2023) | Nucleic Acids Research | The ENCODE Uniform Processing Pipelines: standardized processing enables large-scale batch comparisons | [10.1093/nar/gkac1067](https://doi.org/10.1093/nar/gkac1067) | ~50 |
| Landt et al. (2012) | Genome Research | ChIP-seq guidelines of ENCODE/modENCODE: QC metrics (FRiP, NSC, RSC, NRF) for batch quality assessment | [10.1101/gr.136184.111](https://doi.org/10.1101/gr.136184.111) | ~4,000 |
| Leek et al. (2010) | Nature Reviews Genetics | Tackling batch effects: detection via PCA, correction via ComBat/SVA; essential for multi-lab analyses | [10.1038/nrg2825](https://doi.org/10.1038/nrg2825) | ~1,200 |
| Amemiya et al. (2019) | Scientific Reports | ENCODE Blacklist: artifact regions to exclude across all experiments in batch analyses | [10.1038/s41598-019-45839-z](https://doi.org/10.1038/s41598-019-45839-z) | ~1,372 |

## Part 1: Batch Discovery and QC Screening

### 1a. Systematic Experiment Discovery

Start with `encode_get_facets` to understand the scope of available data before committing to a batch:

```
encode_get_facets(
    assay_title="Histone ChIP-seq",
    organ="pancreas"
)
```

This returns counts by target, biosample type, lab, and status. Use facets to estimate how many experiments match your criteria and identify potential batch variables (multiple labs, multiple biosample types).

Then search for all candidate experiments:

```
results = encode_search_experiments(
    assay_title="Histone ChIP-seq",
    target="H3K27ac",
    biosample_type="tissue",
    organism="Homo sapiens",
    limit=100
)
```

### 1b. Building the Experiment Table

Create a structured table of all candidate experiments for review:

```
For each experiment in search results:
    encode_get_experiment(accession="ENCSR...")

Collect into table:
| Accession | Target | Biosample | Lab | Replicates | Audit Status | Date Released |
```

Key fields to extract:
- Accession
- Assay title
- Target (for ChIP-seq)
- Biosample term name
- Biosample type (tissue, cell line, primary cell)
- Lab
- Number of biological replicates
- Audit level (ERROR, NOT_COMPLIANT, WARNING)
- Assembly
- Date released
- Pipeline version

### 1c. Quality Screening Criteria

Apply the ENCODE quality standards (Landt et al. 2012) to filter experiments:

**Mandatory exclusion** (remove from batch):

| Criterion | Threshold | Rationale |
|-----------|-----------|-----------|
| Audit level = ERROR | Exclude | Fundamental data quality failure |
| Assembly mismatch | Exclude if mixed | Cannot combine GRCh38 with hg19 |
| 0 replicates | Exclude | No biological replication |

**Quality flags** (include with notation):

| Criterion | Threshold | Action |
|-----------|-----------|--------|
| Audit level = NOT_COMPLIANT | Flag | Include but note in report |
| Single replicate | Flag | Reduced statistical power; note |
| FRiP < 1% (ChIP-seq) | Flag | Low enrichment; may lack signal |
| NRF < 0.8 | Flag | Low library complexity |
| NSC < 1.05 | Flag | Low signal-to-noise |
| RSC < 0.8 | Flag | Low relative strand correlation |

**Quality tiers for batch analysis**:

| Tier | Criteria | Use Case |
|------|----------|----------|
| Tier 1 | No audits, 2+ replicates, all QC pass | Gold standard; use for primary analysis |
| Tier 2 | WARNING audits only, 2+ replicates | Acceptable; include with documentation |
| Tier 3 | NOT_COMPLIANT audits or 1 replicate | Use only if Tier 1/2 insufficient; flag heavily |
| Exclude | ERROR audits or 0 replicates | Never include |

### 1d. Identifying Batch Variables

Before proceeding, identify potential confounders across the experiment collection:

```
Group experiments by:
    - Lab (different labs = potential batch effect)
    - Date released (>1 year gap = potential processing differences)
    - Pipeline version (different versions = different peak calls)
    - Sequencing platform (Illumina vs other)
    - Library prep method
```

If all experiments of one condition come from one lab and all experiments of another condition come from a different lab, the design is confounded. This cannot be corrected computationally (Leek et al. 2010). Document this limitation.

## Part 2: Batch Download

### 2a. Dry Run First

Always preview downloads before committing:

```
encode_batch_download(
    assay_title="Histone ChIP-seq",
    target="H3K27ac",
    organ="pancreas",
    file_format="bigWig",
    output_type="fold change over control",
    assembly="GRCh38",
    download_dir="/data/encode_batch/",
    preferred_default=True,
    dry_run=True,
    limit=100
)
```

The dry run returns:
- Number of files that would be downloaded
- Total estimated size
- File list with accessions and sizes

**Review before proceeding**: Check that the total size is manageable and that no unexpected files are included.

### 2b. Organizing Downloads

Choose an organization strategy based on your analysis plan:

| organize_by | Directory Structure | Best For |
|-------------|-------------------|----------|
| `flat` | All files in one directory | Small batches (<20 files) |
| `experiment` | `ENCSR.../filename` | Per-experiment analysis workflows |
| `format` | `bigWig/filename` | Downstream tools that expect format-grouped input |
| `experiment_format` | `ENCSR.../bigWig/filename` | Large multi-format batches |

```
encode_batch_download(
    assay_title="Histone ChIP-seq",
    target="H3K27ac",
    organ="pancreas",
    file_format="bigWig",
    output_type="fold change over control",
    assembly="GRCh38",
    download_dir="/data/encode_batch/",
    organize_by="experiment",
    preferred_default=True,
    verify_md5=True,
    dry_run=False,
    limit=100
)
```

### 2c. Downloading Multiple File Types

For comprehensive analysis, download multiple file types per experiment:

```
# Signal tracks for visualization and correlation
encode_batch_download(
    ...,
    file_format="bigWig",
    output_type="fold change over control",
    download_dir="/data/encode_batch/signal/",
    dry_run=False
)

# Peak calls for overlap and annotation
encode_batch_download(
    ...,
    file_format="bed",
    output_type="IDR thresholded peaks",
    download_dir="/data/encode_batch/peaks/",
    dry_run=False
)
```

### 2d. Handling Download Failures

For large batches, some downloads may fail due to network issues or temporary server errors. The download results report success/failure per file.

```
Strategy for failures:
1. Note failed file accessions from download results
2. Wait 5 minutes (transient server issues)
3. Retry failed files individually:
    encode_download_files(
        file_accessions=["ENCFF_failed_1", "ENCFF_failed_2"],
        download_dir="/data/encode_batch/",
        verify_md5=True
    )
4. If retry fails, check ENCODE portal status
```

### 2e. Storage Planning

Estimate storage needs before batch download:

| File Type | Typical Size | 50 Experiments |
|-----------|-------------|----------------|
| bigWig (signal) | 200MB-1GB | 10-50 GB |
| BED (peaks) | 1-50MB | 0.05-2.5 GB |
| BAM (alignments) | 2-20GB | 100-1000 GB |
| FASTQ (raw reads) | 5-50GB | 250-2500 GB |

**Recommendation**: Download bigWig signal and BED peaks first (compact, sufficient for most analyses). Only download BAM/FASTQ if you need to reprocess from reads.

## Part 3: Batch Comparison

### 3a. Track All Experiments

Track every experiment in the batch for local metadata management:

```
For each experiment accession:
    encode_track_experiment(
        accession="ENCSR...",
        fetch_publications=True,
        fetch_pipelines=True,
        notes="Part of pancreas H3K27ac batch analysis"
    )
```

This stores metadata, publications, and pipeline info locally for each experiment.

### 3b. Pairwise Compatibility Matrix

For N experiments, check pairwise compatibility to identify issues:

```
For each pair (i, j) where i < j:
    encode_compare_experiments(
        accession1="ENCSR_i",
        accession2="ENCSR_j"
    )

Build compatibility matrix:
| | ENCSR_1 | ENCSR_2 | ENCSR_3 | ... |
|---|---------|---------|---------|-----|
| ENCSR_1 | - | Compatible | Warning: different lab | ... |
| ENCSR_2 | Compatible | - | Compatible | ... |
| ENCSR_3 | Warning | Compatible | - | ... |
```

**Key compatibility dimensions**:
- **Assembly match**: Must be identical (no liftOver in batch workflows)
- **Target match**: Must be identical for same-mark comparisons
- **Biosample compatibility**: Expected to differ in cross-tissue designs; unexpected differences flagged
- **Lab concordance**: Different labs flagged for potential batch effects
- **Pipeline version**: Different versions flagged; consider re-processing

### 3c. Identifying and Documenting Batch Effects

After tracking all experiments, use the metadata to identify systematic differences:

```
encode_summarize_collection(
    assay_title="Histone ChIP-seq"
)
```

This returns experiments grouped by target, organ, biosample type, and lab. Look for:
- Conditions where all experiments come from one lab (potential confound)
- Experiments that are outliers in quality metrics
- Missing data: conditions without replicates

### 3d. Signal Correlation Across Batch

Use deepTools to assess whether experiments cluster by biology or by technical variables:

```bash
# Build signal matrix across all experiments
multiBigwigSummary bins \
    -b exp1_signal.bw exp2_signal.bw exp3_signal.bw ... \
    --labels Islet_Lab1 Islet_Lab2 Liver_Lab1 Liver_Lab2 ... \
    --binSize 10000 \
    -o batch_matrix.npz \
    -p 16

# Correlation heatmap (should cluster by tissue, not lab)
plotCorrelation -in batch_matrix.npz \
    --corMethod pearson \
    --whatToPlot heatmap \
    --plotFile batch_correlation.pdf

# PCA (PC1 should separate biology, not batch)
plotPCA -in batch_matrix.npz \
    --plotFile batch_pca.pdf
```

If samples cluster by lab rather than by condition, batch correction is needed before integrative analysis (see integrative-analysis skill).

## Part 4: Report Generation

### 4a. Export Experiment Table

Export the tracked collection as a structured table:

```
encode_export_data(
    format="csv",
    assay_title="Histone ChIP-seq"
)
```

This produces a CSV with columns: accession, assay, target, biosample, organ, organism, lab, replicates, audit, pipeline, publication count, derived file count, and PMIDs.

For R or pandas import:
```
encode_export_data(format="tsv")
```

### 4b. Collection Summary Statistics

Generate aggregate statistics:

```
encode_summarize_collection(
    assay_title="Histone ChIP-seq"
)
```

Returns:
- Total experiments tracked
- Breakdown by assay type, target, organ, biosample type, lab
- Publication count
- Derived file count
- External reference count

### 4c. Methods Section Generation

Use tracked metadata and citations to draft a reproducible methods section:

```
encode_get_citations(export_format="bibtex")
```

**Template methods paragraph**:

"We obtained [N] [assay] experiments from the ENCODE Project (ENCODE Consortium 2020; Hitz et al. 2023) targeting [marks/factors] in [biosamples]. All experiments were processed by the ENCODE Uniform Processing Pipeline v[X] and passed quality standards (Landt et al. 2012): [QC criteria]. Data were downloaded in [format] format aligned to [assembly]. [N] experiments were excluded due to [reasons]. Batch effects were assessed by PCA of genome-wide signal (Leek et al. 2010) and [correction applied/no correction needed]. ENCODE blacklist regions (Amemiya et al. 2019) were excluded from all analyses."

### 4d. Provenance Documentation

Log all batch-derived outputs:

```
encode_log_derived_file(
    file_path="/data/batch_analysis/correlation_matrix.pdf",
    source_accessions=["ENCSR001", "ENCSR002", "ENCSR003", ...],
    description="Pearson correlation heatmap of H3K27ac signal across 15 tissue types",
    file_type="visualization",
    tool_used="deepTools v3.5.4 multiBigwigSummary + plotCorrelation",
    parameters="--binSize 10000 --corMethod pearson"
)

encode_log_derived_file(
    file_path="/data/batch_analysis/experiment_summary.csv",
    source_accessions=["ENCSR001", "ENCSR002", "ENCSR003", ...],
    description="Summary table of 15 H3K27ac experiments with QC metrics and annotations",
    file_type="metadata_table",
    tool_used="encode_export_data",
    parameters="format=csv, assay_title=Histone ChIP-seq"
)
```

### 4e. Cross-Referencing with External Databases

Link experiments to external resources for comprehensive documentation:

```
# Link to PubMed publications
encode_link_reference(
    experiment_accession="ENCSR...",
    reference_type="pmid",
    reference_id="32728249",
    description="ENCODE Phase 3 paper describing this experiment"
)

# Link to GEO datasets
encode_link_reference(
    experiment_accession="ENCSR...",
    reference_type="geo_accession",
    reference_id="GSE118412",
    description="Companion GEO dataset with additional replicates"
)

# Link to bioRxiv preprints
encode_link_reference(
    experiment_accession="ENCSR...",
    reference_type="preprint_doi",
    reference_id="10.1101/2024.01.15.575000",
    description="Preprint using this data for pancreatic islet analysis"
)
```

## Full Workflow

```
Step 1: Discovery
    encode_get_facets(assay_title="...", organ="...")
    encode_search_experiments(..., limit=100)
    Build experiment candidate table

Step 2: QC Screening
    encode_get_experiment(accession="...") for each candidate
    Apply quality filters (audit, replicates, QC metrics)
    Categorize into Tier 1/2/3/Exclude
    Identify batch variables (lab, date, platform)

Step 3: Download
    encode_batch_download(..., dry_run=True) to preview
    Review total size and file list
    encode_batch_download(..., dry_run=False) to download
    Retry any failed downloads

Step 4: Track and Compare
    encode_track_experiment(...) for each included experiment
    encode_compare_experiments(...) for pairwise compatibility
    Build compatibility matrix
    Run deepTools correlation/PCA for batch assessment

Step 5: Report
    encode_export_data(format="csv") for experiment table
    encode_summarize_collection() for aggregate statistics
    encode_get_citations(export_format="bibtex") for references
    Draft methods section
    Log all derived files for provenance
```

## Common Pitfalls

1. **API rate limits**: The ENCODE API allows approximately 10 requests per second. When iterating over large experiment lists (50+), add 100-200ms delays between requests to avoid rate limiting. Batch tools like `encode_batch_download` handle rate limiting internally, but custom loops over `encode_get_experiment` or `encode_list_files` require manual throttling. If you receive HTTP 429 errors, pause for 30 seconds before retrying.

2. **Mixed assemblies in batch**: Before any batch operation, verify that ALL experiments use the same genome assembly. It is common for older ENCODE experiments to only have hg19 data while newer experiments have GRCh38. Mixing assemblies in a batch analysis produces meaningless results. Filter by `assembly="GRCh38"` when listing files, and verify at the experiment level. If you must include hg19-only experiments, perform liftOver before integration, but document the limitation.

3. **Lab batch effects in cross-tissue comparisons**: When comparing chromatin marks across tissues, the experiments often come from different labs. If all liver experiments are from Lab A and all pancreas experiments are from Lab B, then lab and tissue are confounded. Any differences you observe could be biological (tissue difference) or technical (lab difference). There is no computational solution for perfectly confounded designs (Leek et al. 2010). The only mitigation is to find experiments from shared labs across conditions, or to validate findings with independent datasets.

4. **Missing replicates degrade batch statistics**: Some ENCODE experiments have only one biological replicate. Including single-replicate experiments in a batch reduces statistical power for correlation analysis, differential binding, and batch effect detection. Document which experiments have single replicates and assess whether they behave as outliers relative to replicated experiments. Consider performing analyses with and without single-replicate experiments to assess sensitivity.

5. **Storage planning prevents interrupted workflows**: Batch downloads of bigWig files for 50+ experiments can easily exceed 50-100GB. BAM files are 10x larger. Always run `dry_run=True` first to estimate total download size, verify available disk space with `df -h`, and consider downloading only the file types needed for your specific analysis. Starting a 200GB download on a drive with 150GB free results in partial data and wasted time.

## Integration

| This skill produces... | Feed into... | Purpose |
|---|---|---|
| Batch-processed peak files | **histone-aggregation** | Aggregate peaks across batch-analyzed experiments |
| Batch QC reports | **quality-assessment** | Validate quality across batch of experiments |
| Batch experiment lists | **track-experiments** | Track all experiments in a batch |
| Batch-downloaded files | **download-encode** | Coordinate file downloads for batch |
| Multi-experiment comparisons | **compare-biosamples** | Systematic comparison across biosamples |
| Batch analysis metadata | **data-provenance** | Document batch processing parameters |
| Batch experiment citations | **cite-encode** | Generate citations for all experiments in batch |
| Batch peak sets | **peak-annotation** | Annotate peaks from multiple experiments |

## Presenting Results

When reporting batch analysis results:

- **Summary table**: Present a table of all experiments with columns: accession, assay, biosample, lab, replicate_count, QC_verdict (PASS/WARN/FAIL), and key metric (e.g., FRiP for ChIP-seq, TSS enrichment for ATAC-seq)
- **Highlight failures**: List any experiments that failed QC or download with the specific reason (audit ERROR, missing replicates, assembly mismatch)
- **Aggregated statistics**: Report total experiments processed, pass rate, total files downloaded, total size on disk, and any batch effect warnings (e.g., confounded lab-tissue combinations)
- **Always report**: Genome assembly used, ENCODE audit filter threshold applied, date of data retrieval, and whether `dry_run` was used before actual download
- **Context to provide**: Note if any experiments were excluded and why, and whether single-replicate experiments were included or removed
- **Next steps**: Suggest proceeding with `integrative-analysis` to combine the batch, or `quality-assessment` for deeper QC on flagged experiments

## Walkthrough: QC Screening 10 H3K27ac Experiments Before Multi-Tissue Analysis

**Goal**: Screen quality across 10 H3K27ac ChIP-seq experiments from different tissues.
**Context**: User plans a multi-tissue enhancer comparison and needs to exclude low-quality datasets.

### Step 1: Search for all H3K27ac experiments

```
encode_search_experiments(
  assay_title="Histone ChIP-seq",
  target="H3K27ac",
  limit=10
)
```

Expected output:
```json
{
  "total": 156,
  "experiments": [
    {"accession": "ENCSR001ABC", "biosample_summary": "liver tissue", "audit": {"ERROR": 0, "WARNING": 1}},
    {"accession": "ENCSR002DEF", "biosample_summary": "brain tissue", "audit": {"ERROR": 1, "WARNING": 0}}
  ]
}
```

### Step 2: Track all passing experiments

```
encode_track_experiment(
  accession="ENCSR001ABC",
  notes="Liver H3K27ac — passed QC (0 errors)"
)
```

### Step 3: Summarize the collection

```
encode_summarize_collection()
```

Expected output:
```json
{
  "total_experiments": 8,
  "assays": {"Histone ChIP-seq": 8},
  "organs": {"liver": 2, "brain": 2, "heart": 2, "kidney": 2}
}
```

**Interpretation**: 8 of 10 experiments passed QC. 2 excluded for audit errors. Collection has balanced tissue representation.

## Code Examples

### 1. Batch QC check across experiments

```
encode_get_experiment(accession="ENCSR001ABC")
```

Expected output:
```json
{
  "accession": "ENCSR001ABC",
  "assay_title": "Histone ChIP-seq",
  "target": "H3K27ac-human",
  "status": "released",
  "audit": {"ERROR": 0, "WARNING": 1, "NOT_COMPLIANT": 0},
  "replicates": 2
}
```

## Related Skills

- **search-encode** -- Foundation skill for discovering experiments; provides the search results that feed into batch analysis
- **download-encode** -- Individual file download with detailed control; use for retrying failed batch downloads or targeted file retrieval
- **track-experiments** -- Core experiment tracking functionality used throughout batch workflows
- **quality-assessment** -- Detailed QC assessment for individual experiments; use when batch screening identifies flagged experiments
- **compare-biosamples** -- Systematic biosample comparison; complements batch analysis when comparing across tissue types
- **data-provenance** -- Detailed provenance tracking and methods section writing; use after batch analysis to document the complete workflow
- **integrative-analysis** -- Next step after batch collection; use to combine the batch of experiments into a unified analysis
- **visualization-workflow** -- Create heatmaps, correlation plots, and track hubs from batch-downloaded data
- **publication-trust** -- Verify literature claims backing analytical decisions

## For the request: "$ARGUMENTS"
