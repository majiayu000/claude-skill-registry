---
name: screploading
description: Load single-cell TCR-seq or scBCR-seq data from various formats into a scRepertoire-compatible object. This process reads VDJ (variable, diversity, joining) receptor contig data from multiple single-cell sequencing platforms and prepares it for integration with scRNA-seq data.
---

# ScRepLoading Process Configuration

## Purpose
Load single-cell TCR-seq or scBCR-seq data from various formats into a scRepertoire-compatible object. This process reads VDJ (variable, diversity, joining) receptor contig data from multiple single-cell sequencing platforms and prepares it for integration with scRNA-seq data.

## When to Use
- **When analyzing scTCR-seq or scBCR-seq data** alongside scRNA-seq
- **Required for TCR/BCR clonotype analysis** (CDR3 clustering, clone expansion, TESSA analysis)
- **Enables integration** of immune receptor information with single-cell expression data
- **Supports multiple sequencing platforms**: 10x Genomics, AIRR, BD, Dandelion, Immcantation, MiXCR, ParseBio, TRUST4, WAT3R, Omniscope

**Important**: This process is automatically enabled when your sample info file contains `TCRData` or `BCRData` columns.

## Configuration Structure

### Process Enablement
```toml
[ScRepLoading]
cache = true  # Enable caching (default: true)
```

### Input Specification
```toml
[ScRepLoading.in]
# Type: file
# Required: yes
# Description: Sample metadata file (tab-delimited) with TCR/BCR data paths
metafile = "path/to/sample_info.txt"
```

**Required input file columns:**
- `Sample`: Unique identifier for each sample (required)
- `TCRData` (for TCR analysis): Directory path to scTCR-seq data
- `BCRData` (for BCR analysis): Directory path to scBCR-seq data
- Additional columns: Treated as sample metadata (optional)

**Data format requirements:**
- **10x Genomics**: Directory containing `filtered_contig_annotations.csv` or `all_contig_annotations.csv`
- **AIRR format**: Directory containing `airr_rearrangement.tsv`
- **BD platform**: Directory containing `Contigs_AIRR.tsv`
- **Dandelion**: Directory containing `all_contig_dandelion.tsv`
- **Immcantation**: Directory containing `_data.tsv` or similar
- **JSON**: File with `.json` extension
- **MiXCR**: Directory containing `clones.tsv`
- **ParseBio**: Directory containing `barcode_report.tsv`
- **TRUST4**: Directory containing `barcode_report.tsv`
- **WAT3R**: Directory containing `barcode_results.csv`
- **Omniscope**: Directory containing `.csv` files

**Path handling:**
- If `TCRData`/`BCRData` specifies a **directory**: Process uses `scRepertoire::loadContigs()` directly
- If `TCRData`/`BCRData` specifies a **file**: Creates symbolic link to temp directory for processing
- When filename is not recognized by scRepertoire: Set `envs.format` explicitly

### Environment Variables

```toml
[ScRepLoading.envs]
# type: choice - Data type to load (default: "auto")
# Options:
#   "TCR" - T cell receptor data
#   "BCR" - B cell receptor data
#   "auto" - Auto-detect from column names in sample info
# Note: If both TCRData and BCRData present, TCR selected by default
type = "auto"

# format: choice - Format of TCR/BCR data files (optional)
# Options: auto, 10X, AIRR, BD, Dandelion, Immcantation,
#          JSON, MiXCR, Omniscope, ParseBio, TRUST4, WAT3R
# If not provided, scRepertoire guesses from filename
format = "auto"

# combineTCR: json - Extra arguments for scRepertoire::combineTCR()
# See: https://rdrr.io/github/ncborcherding/scRepertoire/man/combinetcr
combineTCR = {"samples": true}

# combineBCR: json - Extra arguments for scRepertoire::combineBCR()
# See: https://rdrr.io/github/ncborcherding/scRepertoire/man/combinebcr
combineBCR = {"samples": true}

# exclude: auto or list - Columns to exclude from metadata (default: auto)
# auto = ["BCRData", "TCRData", "RNAData"]
# Can also be comma-separated string: "BCRData,TCRData,RNAData"
exclude = "auto"

# tmpdir: str - Temporary directory for symbolic links (default: "/tmp")
tmpdir = "/tmp"
```

#### Detailed combineTCR Parameters

```toml
[ScRepLoading.envs.combineTCR]
# samples: bool or list - Sample labels (default: true)
# true = use Sample column from metadata
# false = no sample grouping
# list = explicit sample labels
samples = true

# ID: str or null - Additional sample labeling (optional)
# Adds prefix to barcodes to prevent duplicate issues
ID = null

# removeNA: bool - Remove cells with missing chain values (default: false)
# true = filter out cells with NA in any chain
# false = include cells with 1 NA value (default)
removeNA = false

# removeMulti: bool - Remove cells with >2 chains (default: false)
# true = filter out multi-chain cells (>2 chains)
# false = include multi-chain cells (default)
removeMulti = false

# filterMulti: bool - Select highest-expression chain for multi-chain (TCR default: false)
# true = keep highest UMI count chain if multiple chains present
# false = keep all chains (default)
filterMulti = false

# filterNonproductive: bool - Remove non-productive rearrangements (default: true)
# true = filter out non-functional receptors
# false = include all rearrangements
filterNonproductive = true
```

#### Detailed combineBCR Parameters

```toml
[ScRepLoading.envs.combineBCR]
# samples: bool or list - Sample labels (default: true)
samples = true

# ID: str or null - Additional sample labeling (optional)
ID = null

# call.related.clones: bool - Cluster related BCR clones (default: true)
# Uses nucleotide sequence + V gene with Levenshtein distance
# false = uses V gene + amino acid sequence for CTstrict
call.related.clones = true

# threshold: num - Normalized edit distance for clustering (default: 0.85)
# Higher = more permissive clustering (more sequences grouped)
# Range: 0.0 - 1.0
threshold = 0.85

# removeNA: bool - Remove cells with missing chain values (default: false)
removeNA = false

# removeMulti: bool - Remove cells with >2 chains (default: false)
removeMulti = false

# filterMulti: bool - Select highest-expression chain (default: true)
# true = keep highest UMI count chain
# false = keep all chains
filterMulti = true

# filterNonproductive: bool - Remove non-productive rearrangements (default: true)
filterNonproductive = true
```

## Configuration Examples

### Minimal Configuration (10x TCR Data)

```toml
[SampleInfo.in]
infile = "sample_info.txt"

# Sample info file contents:
# Sample  Age  Sex  Diagnosis  RNAData            TCRData
# C1      62   F    Colitis    /data/C1/rna      /data/C1/tcr
# C2      71   F    Colitis    /data/C2/rna      /data/C2/tcr

# ScRepLoading auto-enables when TCRData column present
# No explicit ScRepLoading section needed
```

### Single Sample with Format Specification

```toml
[ScRepLoading]
cache = true

[ScRepLoading.in]
metafile = "metadata/single_sample.txt"

[ScRepLoading.envs]
type = "TCR"
format = "10X"

[ScRepLoading.envs.combineTCR]
removeNA = true
filterNonproductive = true
```

### Multi-Sample BCR Analysis with Clustering

```toml
[ScRepLoading]
cache = true

[ScRepLoading.in]
metafile = "metadata/bcr_samples.txt"

[ScRepLoading.envs]
type = "BCR"

[ScRepLoading.envs.combineBCR]
call.related.clones = true
threshold = 0.85  # Higher threshold for more permissive clustering
filterMulti = true
removeMulti = false
```

### Non-10x Format (AIRR)

```toml
[ScRepLoading]

[ScRepLoading.in]
metafile = "metadata/airr_samples.txt"

[ScRepLoading.envs]
format = "AIRR"
type = "auto"

[ScRepLoading.envs.combineTCR]
removeNA = false
removeMulti = false
```

### TRUST4 Format

```toml
[ScRepLoading]

[ScRepLoading.in]
metafile = "metadata/trust4_samples.txt"

[ScRepLoading.envs]
format = "TRUST4"

[ScRepLoading.envs.combineTCR]
removeNA = true
filterNonproductive = true
```

## Common Patterns

### Pattern 1: 10x Genomics TCR Data (Most Common)

```toml
# sample_info.txt
# Sample    RNAData              TCRData
# Sample1   /data/Sample1/rna   /data/Sample1/vdj
# Sample2   /data/Sample2/rna   /data/Sample2/vdj

[SampleInfo.in]
infile = "sample_info.txt"

# TCR directories must contain filtered_contig_annotations.csv
# No ScRepLoading configuration needed - auto-detected
```

### Pattern 2: Both TCR and BCR Data (Auto-Detect TCR)

```toml
# sample_info.txt
# Sample    RNAData              TCRData              BCRData
# Sample1   /data/Sample1/rna   /data/Sample1/tcr   /data/Sample1/bcr

[SampleInfo.in]
infile = "sample_info.txt"

# TCR selected by default when both columns present
# To explicitly analyze BCR instead:
[ScRepLoading.envs]
type = "BCR"
```

### Pattern 3: Filtered TCR Data (Remove NA and Multi-Chain)

```toml
[ScRepLoading]

[ScRepLoading.in]
metafile = "metadata/tcr_filtered.txt"

[ScRepLoading.envs.combineTCR]
removeNA = true      # Remove cells with missing chains
removeMulti = true   # Remove cells with >2 chains
filterNonproductive = true  # Remove non-functional receptors
```

### Pattern 4: Relaxed Filtering for Exploratory Analysis

```toml
[ScRepLoading]

[ScRepLoading.in]
metafile = "metadata/tcr_exploratory.txt"

[ScRepLoading.envs.combineTCR]
removeNA = false     # Keep cells with single chain
removeMulti = false  # Include multi-chain cells for inspection
filterNonproductive = false  # Include non-productive rearrangements
```

### Pattern 5: BCR Clone Clustering with Custom Threshold

```toml
[ScRepLoading]

[ScRepLoading.in]
metafile = "metadata/bcr_clustering.txt"

[ScRepLoading.envs.combineBCR]
call.related.clones = true
threshold = 0.90  # More stringent clustering (lower = more permissive)
```

### Pattern 6: Sample-Specific Labeling

```toml
[ScRepLoading]

[ScRepLoading.in]
metafile = "metadata/longitudinal.txt"

[ScRepLoading.envs.combineTCR]
samples = true  # Use Sample column from metadata
ID = "Timepoint"  # Add Timepoint as additional label prefix

# Creates barcodes like: "Sample1_Timepoint1_AAACCC..."
# Prevents duplicate barcode issues across timepoints
```

### Pattern 7: Custom Metadata Exclusion

```toml
[ScRepLoading]

[ScRepLoading.in]
metafile = "metadata/custom_columns.txt"

[ScRepLoading.envs]
exclude = ["RNAData", "TCRData", "BCRData", "ExperimentID", "Batch"]

# These columns excluded from scRepertoire object metadata
# Helps reduce metadata clutter in downstream analysis
```

### Pattern 8: Paired Chain Analysis (TRA+TRB for TCR)

```toml
# Default behavior - ScRepLoading automatically pairs chains
# at cell barcode level when both TRA and TRB present

[ScRepLoading]

[ScRepLoading.in]
metafile = "metadata/tcr_paired.txt"

[ScRepLoading.envs.combineTCR]
removeNA = false  # Keep single-chain cells for inspection
filterMulti = false  # Don't filter multi-chain cells

# Later analysis can filter for true paired chains
# Using downstream processes like CDR3Clustering
```

## Dependencies

### Upstream Processes
- **SampleInfo** (required): Provides sample metadata with `TCRData`/`BCRData` columns
- **LoadingRNAFromSeurat** (alternative): When loading RNA from Seurat instead of SampleInfo

### Downstream Processes
- **ScRepCombiningExpression**: Integrates TCR/BCR data with scRNA-seq expression
- **CDR3Clustering**: Clones cells by CDR3 sequence similarity
- **TESSA**: TCR-specific analysis (epitope specificity prediction)
- **CDR3AAPhyschem**: Physicochemical properties of CDR3 sequences
- **ClonalStats**: Clonality statistics and diversity metrics

## Validation Rules

### Common Configuration Errors

1. **Missing TCRData/BCRData column**:
   - **Error**: Process not enabled, no TCR/BCR analysis
   - **Fix**: Add `TCRData` or `BCRData` column to sample info file

2. **Invalid format specified**:
   - **Error**: scRepertoire fails to recognize file format
   - **Fix**: Set `envs.format` to one of: `10X`, `AIRR`, `BD`, `Dandelion`, `Immcantation`, `JSON`, `MiXCR`, `ParseBio`, `TRUST4`, `WAT3R`, `Omniscope`

3. **Directory path not found**:
   - **Error**: Cannot access TCR/BCR data directory
   - **Fix**: Verify paths in `TCRData`/`BCRData` columns exist and are readable

4. **Missing required files in directory**:
   - **Error**: Expected contig file not found (e.g., `filtered_contig_annotations.csv`)
   - **Fix**: Ensure directory contains appropriate file for specified format

5. **Both TCR and BCR specified without type selection**:
   - **Warning**: TCR selected by default
   - **Fix**: Set `envs.type = "BCR"` if BCR analysis intended

### File Format Requirements

- **10x Genomics**: Must have `filtered_contig_annotations.csv` in directory
- **AIRR**: Must have `airr_rearrangement.tsv` in directory
- **BD**: Must have `Contigs_AIRR.tsv` in directory
- **Dandelion**: Must have `all_contig_dandelion.tsv` in directory
- **MiXCR**: Must have `clones.tsv` in directory
- **TRUST4**: Must have `barcode_report.tsv` in directory
- **ParseBio**: Must have `barcode_report.tsv` in directory
- **WAT3R**: Must have `barcode_results.csv` in directory

### Chain Compatibility

- **TCR chains**: Supports TRA, TRB, TRG, TRD (auto-detected from data)
- **BCR chains**: Supports IGH, IGL, IGK (auto-detected from data)
- **Paired analysis**: Automatically pairs TRA+TRB or IGH+IGL/IGK when both present
- **Single-chain**: Keeps single-chain cells when `removeNA = false`

## Troubleshooting

### Issue: ScRepLoading not running
**Cause**: No `TCRData` or `BCRData` column in sample info file
**Solution**:
1. Add `TCRData` or `BCRData` column to sample info
2. Verify column name exactly matches (case-sensitive)
3. Check that `SampleInfo.in.infile` is correctly specified

### Issue: "File format not recognized"
**Cause**: Filename doesn't match expected pattern for auto-detection
**Solution**:
1. Set `envs.format` explicitly to your format type
2. Example: `format = "TRUST4"` for TRUST4 output
3. Verify directory contains expected file for that format

### Issue: "No cells loaded" or empty output
**Cause**: Too aggressive filtering or mismatched barcodes
**Solution**:
1. Set `removeNA = false` and `removeMulti = false` temporarily
2. Check that TCR/BCR barcodes match RNA barcodes
3. Verify filterMulti is appropriate for your data type

### Issue: Duplicate barcode errors
**Cause**: Multiple samples have identical cell barcodes
**Solution**:
1. Set `ID = "Sample"` or use explicit sample labels
2. This adds sample prefix to barcodes: `Sample1_AAACCC...`
3. Required when merging samples from same run

### Issue: BCR clustering too strict/too permissive
**Cause**: Default threshold (0.85) not optimal for data
**Solution**:
1. Adjust `envs.combineBCR.threshold`
2. Higher (0.90+): More stringent, fewer clusters
3. Lower (0.80-): More permissive, more sequences clustered together

### Issue: Single-chain cells lost
**Cause**: `filterNonproductive = true` or `removeNA = true`
**Solution**:
1. For exploratory analysis, set `removeNA = false`
2. For developmental studies, consider `filterNonproductive = false`
3. Use `filterMulti = true` only when confident in data quality

### Issue: Metadata columns missing from output
**Cause**: Excluded by default (`exclude = "auto"`)
**Solution**:
1. Set `exclude = []` to keep all metadata columns
2. Or specify custom list: `exclude = ["RNAData"]`
3. Default excludes: `RNAData`, `TCRData`, `BCRData`

### Issue: Cannot load from specific directory path
**Cause**: Path not accessible or permission issues
**Solution**:
1. Verify directory exists and is readable
2. Check file permissions: `ls -la path/to/tcr/`
3. Use absolute paths if relative paths fail

### Issue: Combining TCR and BCR data separately
**Cause**: Need to analyze both receptor types
**Solution**:
1. Run pipeline twice with different `type` settings
2. First run: `[ScRepLoading.envs] type = "TCR"`
3. Second run: `[ScRepLoading.envs] type = "BCR"`
4. Use different output directories to avoid conflicts

### Issue: Integration with ScRepCombiningExpression fails
**Cause**: Barcodes don't match between RNA and VDJ data
**Solution**:
1. Ensure same samples used in both RNA and VDJ data
2. Check that SampleInfo has correct paths for both data types
3. Verify barcode prefixes match (if using `ID` parameter)
