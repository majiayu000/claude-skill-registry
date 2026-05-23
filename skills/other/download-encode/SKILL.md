---
name: download-encode
description: Download ENCODE genomics files (BED, FASTQ, BAM, bigWig, etc.) to the user's machine. Use when the user wants to download data files from ENCODE experiments.
---

# Download ENCODE Files

## When to Use

- User wants to download ENCODE data files to their local machine
- User asks to "download", "get", or "fetch" ENCODE files
- User needs specific file formats (BED, FASTQ, BAM, bigWig) from experiments
- User wants to batch download files matching search criteria
- User needs to verify file integrity after download (MD5 checksums)
- User asks about organizing downloaded files by experiment or format

Help the user download ENCODE data files to their local machine.

## Download Strategy

1. **Specific files by accession**: Use `encode_download_files` with file accession IDs (e.g., "ENCFF635JIA").

2. **Batch download by criteria**: Use `encode_batch_download` to search and download in one step.
   - Always start with `dry_run=True` (default) to preview what will be downloaded
   - Show the user the file count, total size, and file list
   - Only proceed with `dry_run=False` after user confirms

3. **Download organization options**:
   - `"flat"`: All files in one directory
   - `"experiment"`: Organized by experiment accession (recommended)
   - `"format"`: Organized by file format
   - `"experiment_format"`: Organized by experiment, then format

## Important Notes

- All downloads include MD5 verification by default (`verify_md5=True`)
- Ask the user for a download directory if not specified
- Warn about large downloads (>1GB total or >50 files)
- Files already downloaded will be skipped (idempotent)
- For restricted files, credentials must be configured first via `encode_manage_credentials`

## Pitfalls & Edge Cases

1. **Disk space**: BAM files can be 5-50GB each; FASTQ files 1-20GB. Before any batch download, warn the user about estimated total size from the dry_run preview. A single ChIP-seq experiment can produce 10-30GB of raw data files.
2. **MD5 verification failures**: If MD5 verification fails, the file may be corrupted or incompletely downloaded. Always re-download rather than skipping verification. Never set `verify_md5=False` unless the user explicitly requests it and understands the risk.
3. **Downloading too much data**: Users often request BAM files when they only need peak calls or signal tracks. Suggest `preferred_default=True` to get ENCODE's recommended files, or filter by `output_type` (e.g., "IDR thresholded peaks", "fold change over control") to avoid downloading raw data unnecessarily.
4. **Restricted/unreleased data**: Files with status other than "released" may require ENCODE credentials. Use `encode_manage_credentials(action="check")` to verify credentials are configured before attempting to download restricted data.
5. **Mixed assemblies in batch download**: Always specify the `assembly` filter (e.g., "GRCh38") in batch downloads. Without it, you may download files aligned to different genome assemblies (hg19, GRCh38, mm10), making downstream analysis impossible.
6. **Timeout on large files**: For downloading many files or very large files, `encode_batch_download` handles retries and concurrent downloads better than individual `encode_download_files` calls. The default limit of 100 files provides a safety cap.

## File Type Guide

When users request "files" without specifying a type, use this priority to suggest the right output_type:
- **Peak analysis**: `output_type="IDR thresholded peaks"` (most stringent, recommended for ChIP-seq/ATAC-seq)
- **Signal visualization**: `file_format="bigWig"`, `output_type="fold change over control"` (for genome browser tracks)
- **Gene expression**: `output_type="gene quantifications"` (for RNA-seq TPM/FPKM tables)
- **Raw data reprocessing**: `file_format="fastq"` (only when user needs to run their own pipeline)
- **Quick defaults**: `preferred_default=True` (ENCODE's recommended files for any experiment)

### What to Download for Each Analysis

| Analysis Goal | File Format | Output Type | Why This File |
|---|---|---|---|
| Peak locations (ChIP/ATAC) | bed narrowPeak | IDR thresholded peaks | Gold-standard replicated peaks passing irreproducibility threshold |
| Broad domain marks (H3K27me3) | bed broadPeak | replicated peaks | Broad marks need broadPeak format, not narrowPeak |
| Signal visualization | bigWig | fold change over control | Normalized signal track for genome browser display |
| Signal statistics | bigWig | signal p-value | Statistical significance of signal over background |
| Raw data reprocessing | fastq | reads | Starting from scratch with your own pipeline |
| Alignment inspection | bam | alignments | Check read mapping quality, fragment sizes, duplicates |
| Browser-compatible peaks | bigBed | peaks | UCSC/IGV-compatible binary peak format |
| Gene expression levels | tsv | gene quantifications | TPM/FPKM tables for RNA-seq differential expression |
| Transcript isoforms | tsv | transcript quantifications | Isoform-level expression for splicing analysis |
| 3D genome contacts | hic | contact matrix | Hi-C interaction matrices for loop/TAD calling |
| Methylation levels | bed | methylation state at CpG | Per-CpG methylation fractions for WGBS |

### Assay-Specific Recommendations

| Assay | Primary Download | Secondary Download |
|---|---|---|
| Histone ChIP-seq | IDR thresholded peaks (bed) | fold change over control (bigWig) |
| TF ChIP-seq | IDR thresholded peaks (bed) | fold change over control (bigWig) |
| ATAC-seq | IDR thresholded peaks (bed) | fold change over control (bigWig) |
| DNase-seq | peaks (bed) | signal of unique reads (bigWig) |
| RNA-seq | gene quantifications (tsv) | signal of unique reads (bigWig) |
| WGBS | methylation state at CpG (bed) | signal (bigWig) |
| Hi-C | contact matrix (hic) | contact domains (bed) |
| CUT&RUN | peaks (bed) | fold change over control (bigWig) |
| CUT&Tag | peaks (bed) | fold change over control (bigWig) |
| eCLIP | peaks (bed) | signal of unique reads (bigWig) |

## File Selection Priority

When multiple files exist for the same experiment, choose files in this priority order:

1. **preferred_default=True**: ENCODE curators mark recommended files. Always prefer these when available. Use `encode_list_files(experiment_accession="ENCSR...", preferred_default=True)` to find them.

2. **Peak file hierarchy** (most to least stringent):
   - IDR thresholded peaks — replicated, irreproducibility-filtered (gold standard)
   - Optimal IDR thresholded peaks — union of replicate-level peaks
   - Conservative IDR thresholded peaks — intersection of replicate-level peaks
   - Pseudoreplicated peaks — peaks from pooled pseudoreplicates
   - Replicated peaks — peaks found in both replicates (broad marks)

3. **Signal track hierarchy**:
   - fold change over control — normalized signal, best for comparing across experiments
   - signal p-value — statistical significance of enrichment
   - signal of unique reads — uniquely mapped read signal
   - signal of all reads — includes multi-mapped reads (noisier)

4. **Assembly preference**:
   - GRCh38 for human (current standard) — always use this
   - hg19 for human (legacy) — only if collaborators require it
   - mm10 for mouse (current standard)
   - Never mix assemblies within an analysis

5. **Replicate preference**:
   - Replicated files (combined replicates) over single-replicate files
   - Biological replicates over technical replicates
   - Isogenic replication over anisogenic

6. **Status preference**:
   - released — fully validated, use these
   - archived — older versions, avoid unless specifically needed
   - revoked — quality issues found, never use

## Storage Estimates

Plan disk space before downloading. Use `dry_run=True` to get exact sizes for your query.

| File Type | Typical Size per File | 10 Experiments | 50 Experiments |
|---|---|---|---|
| BED peaks (narrowPeak) | 1-10 MB | 10-100 MB | 50-500 MB |
| BED peaks (broadPeak) | 5-50 MB | 50-500 MB | 250 MB - 2.5 GB |
| bigWig signal tracks | 200 MB - 2 GB | 2-20 GB | 10-100 GB |
| bigBed peaks | 1-20 MB | 10-200 MB | 50 MB - 1 GB |
| TSV quantifications | 5-50 MB | 50-500 MB | 250 MB - 2.5 GB |
| BAM alignments | 2-50 GB | 20-500 GB | 100 GB - 2.5 TB |
| FASTQ reads | 5-100 GB | 50 GB - 1 TB | 250 GB - 5 TB |
| HiC contact matrices | 500 MB - 5 GB | 5-50 GB | 25-250 GB |

**Rule of thumb**: Peak files and quantifications are small (MB). Signal tracks are medium (hundreds of MB). Alignments and raw reads are large (GB to tens of GB). Always preview with `dry_run=True` before committing to a large download.

## Walkthrough: Downloading a Complete ChIP-seq Dataset

This walkthrough shows the full process for downloading H3K27ac ChIP-seq data from human pancreas tissue.

### Step 1: Find the experiment

```
encode_search_experiments(
  assay_title="Histone ChIP-seq",
  target="H3K27ac",
  organ="pancreas",
  biosample_type="tissue",
  assembly="GRCh38"
)
  -> Returns experiments, e.g., ENCSR831JOY
```

### Step 2: List available files

```
encode_list_files(
  experiment_accession="ENCSR831JOY",
  assembly="GRCh38"
)
  -> Returns all files: FASTQs, BAMs, peaks, signals
  -> Note the file accessions for the files you need
```

### Step 3: Identify the right files

Filter to what you actually need — usually peaks + signal tracks:

```
encode_list_files(
  experiment_accession="ENCSR831JOY",
  assembly="GRCh38",
  preferred_default=True
)
  -> Returns ENCODE-recommended files only
  -> Typically: IDR peaks (bed) + fold change signal (bigWig)
```

Or be specific about output types:

```
encode_list_files(
  experiment_accession="ENCSR831JOY",
  output_type="IDR thresholded peaks",
  assembly="GRCh38"
)
  -> Returns only IDR peak files, e.g., ENCFF635JIA
```

### Step 4: Download with MD5 verification

```
encode_download_files(
  file_accessions=["ENCFF635JIA", "ENCFF388RZD"],
  download_dir="/Users/you/data/encode/h3k27ac_pancreas",
  organize_by="experiment",
  verify_md5=True
)
  -> Downloads files with integrity verification
  -> Creates: download_dir/ENCSR831JOY/ENCFF635JIA.bed.gz
              download_dir/ENCSR831JOY/ENCFF388RZD.bigWig
```

### Step 5: Verify the download results

Check the returned JSON for:
- `summary.successful` — number of files downloaded
- `summary.failed` — should be 0
- `summary.total_size_human` — total bytes downloaded
- Each file's `md5_verified` — should be True for all files

If any file fails MD5 verification, re-download that specific file. Do not proceed with a corrupted file.

### Step 6: Log provenance

Track the experiment and log where the data came from:

```
encode_track_experiment(
  accession="ENCSR831JOY",
  notes="H3K27ac ChIP-seq, pancreas tissue, downloaded for enhancer analysis"
)
  -> Stores experiment metadata, publications, and pipeline info locally
```

If you create derived files later (e.g., filtered peaks), log them too:

```
encode_log_derived_file(
  file_path="/Users/you/data/encode/h3k27ac_pancreas/filtered_peaks.bed",
  source_accessions=["ENCSR831JOY", "ENCFF635JIA"],
  description="H3K27ac peaks filtered against ENCODE Blacklist v2",
  file_type="filtered_peaks",
  tool_used="bedtools intersect v2.31.0",
  parameters="bedtools intersect -v -a ENCFF635JIA.bed.gz -b hg38-blacklist.v2.bed"
)
```

## Walkthrough: Batch Download for Multi-Experiment Analysis

Use `encode_batch_download` when downloading data across multiple experiments, such as collecting all H3K4me3 peaks across many tissues.

### Step 1: Preview with dry run

Always start with `dry_run=True` to see what will be downloaded:

```
encode_batch_download(
  download_dir="/Users/you/data/encode/h3k4me3_multi_tissue",
  output_type="IDR thresholded peaks",
  target="H3K4me3",
  assembly="GRCh38",
  assay_title="Histone ChIP-seq",
  biosample_type="tissue",
  organize_by="experiment",
  dry_run=True
)
  -> Preview: 42 files, 180MB total, from 42 experiments
  -> Shows file list with accessions, sizes, and experiment info
```

### Step 2: Review and confirm

Present the dry run results to the user:
- Total file count and size
- Breakdown by experiment or tissue
- Any unexpected files (wrong assembly, archived status)

If the count is too large, narrow with additional filters (e.g., add `organ="pancreas"`).

### Step 3: Execute the download

```
encode_batch_download(
  download_dir="/Users/you/data/encode/h3k4me3_multi_tissue",
  output_type="IDR thresholded peaks",
  target="H3K4me3",
  assembly="GRCh38",
  assay_title="Histone ChIP-seq",
  biosample_type="tissue",
  organize_by="experiment",
  dry_run=False
)
  -> Downloads all 42 files with MD5 verification
  -> Creates: download_dir/ENCSR.../ENCFF....bed.gz (one per experiment)
```

### Step 4: Handle failed downloads

If some files fail:
- Check the `errors` array in the response for specific failure reasons
- Network timeouts: retry the failed accessions with `encode_download_files`
- MD5 mismatches: re-download the specific files
- 403/404 errors: the file may be restricted or withdrawn from ENCODE

```
encode_download_files(
  file_accessions=["ENCFF_FAILED_1", "ENCFF_FAILED_2"],
  download_dir="/Users/you/data/encode/h3k4me3_multi_tissue",
  organize_by="experiment",
  verify_md5=True
)
```

### Organization strategies

Choose `organize_by` based on your analysis plan:

| Strategy | Directory Structure | Best For |
|---|---|---|
| `"experiment"` | `download_dir/ENCSR.../files` | Comparing files within experiments |
| `"format"` | `download_dir/bed/files`, `download_dir/bigWig/files` | Running format-specific pipelines |
| `"experiment_format"` | `download_dir/ENCSR.../bed/files` | Large multi-format downloads |
| `"flat"` | `download_dir/files` | Small downloads, quick access |

## Gotchas

1. **Assembly mismatch**: Always specify `assembly="GRCh38"` for human or `assembly="mm10"` for mouse. Omitting this in batch downloads can produce a mix of GRCh38 and hg19 files that cannot be compared. There is no automated liftover in the download tools — you must use the `liftover-coordinates` skill separately if you need to convert between assemblies.

2. **File status matters**: Only `status="released"` files are fully validated by ENCODE. Archived files may have been superseded by newer processing. Revoked files had quality issues discovered after release. Always check file status before using data in analysis.

3. **MD5 verification is not optional**: Corrupted files produce silent errors in downstream analysis — wrong peak counts, shifted signal tracks, truncated alignments. The few extra seconds for MD5 verification prevents hours of debugging. Only disable with `verify_md5=False` if you are re-downloading a file you already verified.

4. **Streaming for large files**: BAM and FASTQ files are downloaded with streaming to avoid loading entire files into memory. The `encode_batch_download` tool handles this automatically. If a download is interrupted, re-running the same command will skip already-completed files (idempotent).

5. **The 100-file safety limit**: `encode_batch_download` defaults to `limit=100` to prevent accidentally downloading thousands of files. If your query returns more than 100 files, narrow your filters or run multiple targeted batches. You can increase the limit explicitly if you have confirmed the download is intentional.

6. **preferred_default may return nothing**: Not all experiments have files marked as `preferred_default=True`. If this filter returns empty results, fall back to filtering by specific `output_type` and `assembly` instead.

7. **Credential requirements**: Files with status "in progress" or "submitted" require ENCODE DCC credentials. Use `encode_manage_credentials(action="check")` before attempting restricted downloads. Contact the ENCODE DCC for access to unreleased data.

8. **Duplicate files across experiments**: When downloading the same file type across many experiments, some control files (e.g., input ChIP-seq) may be shared between experiments. The download tool skips already-existing files, so shared controls will not be downloaded twice.

## Code Examples

### 1. Smart download: "Download IDR thresholded peaks for H3K4me3 ChIP-seq in GRCh38"

```
Step 1: Preview with dry run
  encode_batch_download(
    download_dir="/Users/you/data/encode",
    output_type="IDR thresholded peaks",
    target="H3K4me3",
    assembly="GRCh38",
    assay_title="Histone ChIP-seq",
    dry_run=True
  )
  -> Shows: 18 files, 45MB total (peak files are small)
  -> Present file list to user for confirmation

Step 2: Confirm and download
  encode_batch_download(
    download_dir="/Users/you/data/encode",
    output_type="IDR thresholded peaks",
    target="H3K4me3",
    assembly="GRCh38",
    assay_title="Histone ChIP-seq",
    dry_run=False
  )
  -> Downloads with MD5 verification, skips already-downloaded files
```

### 2. Batch download with preview: "Download all ATAC-seq bigWig signal tracks for pancreas"

```
Step 1: Dry run to see what's available
  encode_batch_download(
    download_dir="/Users/you/data/encode/atac_pancreas",
    file_format="bigWig",
    assay_title="ATAC-seq",
    organ="pancreas",
    assembly="GRCh38",
    organize_by="experiment",
    dry_run=True
  )
  -> Review: 24 files, 8.3GB total, from 6 experiments

Step 2: Download after user confirms
  (same call with dry_run=False)
```

### 3. Organized download: "Download files organized by experiment and format"

```
Step 1: Download specific files with organization
  encode_download_files(
    file_accessions=["ENCFF635JIA", "ENCFF388RZD", "ENCFF901ABC"],
    download_dir="/Users/you/data/encode",
    organize_by="experiment_format"
  )
  -> Creates: download_dir/ENCSR.../bed/file.bed.gz
             download_dir/ENCSR.../bigWig/file.bigWig
```

### 4. ENCODE-recommended defaults: "Just get the recommended files for this experiment"

```
encode_batch_download(
  download_dir="/Users/you/data/encode/defaults",
  preferred_default=True,
  assembly="GRCh38",
  assay_title="Histone ChIP-seq",
  target="H3K27me3",
  organ="liver",
  organize_by="experiment",
  dry_run=True
)
  -> Returns only ENCODE-curated default files
  -> Typically the most useful subset for standard analyses
```

### 5. RNA-seq expression data: "Download gene quantification tables"

```
encode_batch_download(
  download_dir="/Users/you/data/encode/rnaseq_brain",
  output_type="gene quantifications",
  assay_title="total RNA-seq",
  organ="brain",
  assembly="GRCh38",
  organize_by="experiment",
  dry_run=True
)
  -> Preview: TSV files with TPM/FPKM values, typically 5-20MB each
```

## Integration

| This skill produces... | Feed into... | Purpose |
|---|---|---|
| Downloaded FASTQ files | **pipeline-chipseq** through **pipeline-cutandrun** | Raw data for pipeline processing |
| Downloaded BED peak files | **peak-annotation** | Peak files for gene assignment |
| Downloaded bigWig signals | **visualization-workflow** | Signal tracks for genome browser |
| MD5-verified files | **data-provenance** | Verified file acquisition for audit trail |
| Downloaded BED files | **histone-aggregation** | Peak files for cross-experiment merge |
| Downloaded methylation files | **methylation-aggregation** | CpG methylation data for aggregation |
| File download metadata | **track-experiments** | Record which files were downloaded |
| Downloaded reference data | **bioinformatics-installer** | Reference genomes and annotations |

## Presenting Results

When presenting download results to the user:
- Show a download summary table: **filename** | **size** | **format** | **MD5 status** | **path**
- For `dry_run=True`, present what WOULD be downloaded with total size estimate and file count
- Report any failures separately with error messages
- After successful downloads, suggest next steps:
  - "Would you like to log these as tracked experiments?" (use `encode_track_experiment`)
  - "Would you like to log any derived files for provenance?" (use `encode_log_derived_file`)
- For large batch downloads, summarize by experiment and format rather than listing every file

## Key Literature

- **ENCODE Phase 3**: ENCODE Project Consortium 2020 (Nature, ~2,000 citations) DOI: 10.1038/s41586-020-2493-4 — Source catalog for all downloadable genomic data.
- **FAIR Principles**: Wilkinson et al. 2016 (Scientific Data, ~5,000 citations) DOI: 10.1038/sdata.2016.18 — Findable, Accessible, Interoperable, Reusable data principles that ENCODE's download infrastructure supports.
- **IDR Framework**: Li et al. 2011 (Annals of Applied Statistics) DOI: 10.1214/11-AOAS466 — Irreproducible Discovery Rate method used for peak thresholding in ENCODE.
- **ENCODE Blacklist**: Amemiya et al. 2019 (Scientific Reports, ~1,400 citations) DOI: 10.1038/s41598-019-45839-z — Regions to exclude from downloaded peak files before analysis.

## Related Skills

| Skill | When to Use Instead/Additionally |
|-------|--------------------------------|
| `search-encode` | Finding experiments and files before downloading |
| `track-experiments` | Tracking downloaded experiments locally |
| `data-provenance` | Logging derived files created from downloaded data |
| `quality-assessment` | Evaluating experiment quality before downloading |
| `publication-trust` | Evaluating the provenance and trustworthiness of linked publications |
| `liftover-coordinates` | Converting between genome assemblies if you downloaded hg19 data |
| `batch-analysis` | Running analyses across multiple downloaded experiments |

## For the request: "$ARGUMENTS"
