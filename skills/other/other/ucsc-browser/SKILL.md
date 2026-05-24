---
name: ucsc-browser
description: Query the UCSC Genome Browser REST API to retrieve regulatory tracks, DNA sequences, cCRE annotations, TF binding clusters, and track schemas for any genomic region. Use when the user wants to look up what regulatory elements exist at a genomic locus, retrieve DNA sequence under peaks, query ENCODE cCREs or TF rPeak clusters from UCSC, check what tracks are available for a genome assembly, get chromatin accessibility across cell types, or cross-reference ENCODE data with UCSC-hosted annotations. Also use when the user mentions UCSC, genome browser, cCRE lookup, SCREEN, TF binding clusters, DNA sequence retrieval, or track data extraction.
---

# Query the UCSC Genome Browser REST API

## When to Use

- User wants to query the UCSC Genome Browser REST API for tracks, sequences, or cCRE annotations
- User asks about "UCSC", "genome browser", "cCREs", "track hub", or "sequence retrieval"
- User needs to retrieve DNA sequences for peak regions or regulatory elements
- User wants to intersect ENCODE peaks with UCSC-hosted annotations (cCREs, conservation, repeat masker)
- Example queries: "get cCRE annotations for my region", "fetch DNA sequence under my peaks", "query UCSC for conservation scores at my enhancers"

Retrieve regulatory annotations, DNA sequences, TF binding data, and ENCODE-hosted tracks from the UCSC Genome Browser programmatic interface.

## Scientific Rationale

**The question**: "What regulatory annotations exist at this genomic locus, and what is the underlying sequence?"

The UCSC Genome Browser hosts the most comprehensive collection of genome annotations, including ENCODE cCREs (926,535 human), TF rPeak clusters (21.8M from 912 factors across 1,152 biosamples), DNase clusters, conservation scores, and gene models. The REST API at `api.genome.ucsc.edu` enables programmatic access without authentication.

### Why UCSC Complements the ENCODE Portal

The ENCODE Portal (`encodeproject.org`) provides experiment-level data — individual ChIP-seq peaks, BAM files, quality metrics. UCSC provides **aggregated, cross-experiment annotations**: which cCREs overlap your region, which TFs bind there across all ENCODE biosamples, and what the underlying DNA sequence is. Together they answer: "What did ENCODE find at this locus?" (UCSC) and "What are the specific experiments behind it?" (ENCODE Portal).

### Literature Support

- **ENCODE Project Consortium 2020** (Nature, ~1,656 citations): Registry of 926,535 human cCREs hosted on UCSC as `encodeCcreCombined` track. [DOI](https://doi.org/10.1038/s41586-020-2493-4)
- **Nassar et al. 2023** (Nucleic Acids Research): The UCSC Genome Browser database: 2023 update. [DOI](https://doi.org/10.1093/nar/gkac1072)
- **ENCODE4 TF Atlas**: 21.8M TF rPeak clusters from 912 factors in 1,152 biosamples, hosted as `TFrPeakClusters` track on UCSC.

## API Reference

**Base URL**: `https://api.genome.ucsc.edu`

**No authentication required.** Rate limit: ~1 request/second recommended. Use semicolons (`;`) to separate parameters.

**Coordinate system**: Half-open, 0-based start (matches BED format). `start=1000000;end=1000100` returns 100 bases starting at position 1,000,000.

## Step 1: Discover Available Tracks

Before querying data, check what tracks exist for your assembly:

```bash
# List all tracks for hg38
curl "https://api.genome.ucsc.edu/list/tracks?genome=hg38"

# Search for ENCODE-specific tracks
curl "https://api.genome.ucsc.edu/search?search=encode+regulation&genome=hg38&categories=trackDb"

# Get schema (field definitions) for a track
curl "https://api.genome.ucsc.edu/list/schema?genome=hg38;track=encodeCcreCombined"
```

### Key ENCODE Tracks on UCSC (hg38)

| Track ID | Description | Data Type | Source |
|----------|-------------|-----------|--------|
| `encodeCcreCombined` | 926,535 candidate cis-regulatory elements (V3) | bigBed 9+ | ENCODE Phase 3 |
| `TFrPeakClusters` | 21.8M TF rPeak clusters, 912 factors, 1,152 biosamples | bigBed 12+ | ENCODE 4 |
| `wgEncodeRegDnaseClustered` | 2.1M+ DNase clusters across 95 cell types | MySQL table | ENCODE 2/3 |
| `wgEncodeRegTfbsClustered` | TF binding site clusters (legacy) | MySQL table | ENCODE 2/3 |

### Key Non-ENCODE Regulatory Tracks

| Track ID | Description | Use Case |
|----------|-------------|----------|
| `cpgIslandExt` | CpG islands | Promoter identification |
| `rmsk` | RepeatMasker | Filter repetitive elements |
| `snp155` | dbSNP 155 with ClinVar | Variant annotation |
| `phastCons100way` | Conservation scores (100 vertebrates) | Evolutionary constraint |
| `phyloP100way` | Per-base conservation (100 vertebrates) | Variant impact |

## Step 2: Query ENCODE cCREs at a Locus

The most common use case — what regulatory elements does ENCODE predict at this region?

```bash
# Get all cCREs in a 100kb window
curl "https://api.genome.ucsc.edu/getData/track?genome=hg38;track=encodeCcreCombined;chrom=chr1;start=1000000;end=1100000"

# Use jsonOutputArrays for named fields (recommended)
curl "https://api.genome.ucsc.edu/getData/track?genome=hg38;track=encodeCcreCombined;chrom=chr1;start=1000000;end=1100000;jsonOutputArrays=1"
```

### Response Fields (encodeCcreCombined)

| Field | Description | Example |
|-------|-------------|---------|
| `chrom` | Chromosome | chr1 |
| `chromStart` | Start (0-based) | 999856 |
| `chromEnd` | End | 1000009 |
| `name` | ENCODE accession | EH38E1310344 |
| `score` | Signal strength (0-1000) | 312 |
| `encodeLabel` | cCRE class | PLS, pELS, dELS, CTCF-only |
| `zScore` | Max DNase Z-score | 3.1283 |
| `ccre` | Full classification | PLS,CTCF-bound |

### cCRE Classification Key

| Class | Full Name | Biochemical Signature |
|-------|-----------|----------------------|
| PLS | Promoter-like signature | DNase+ H3K4me3+ near TSS |
| pELS | Proximal enhancer-like | DNase+ H3K27ac+ within 2kb of TSS |
| dELS | Distal enhancer-like | DNase+ H3K27ac+ >2kb from TSS |
| CTCF-only | CTCF-only | DNase+ CTCF+ (no H3K4me3/H3K27ac) |
| DNase-H3K4me3 | DNase-H3K4me3 | DNase+ H3K4me3+ >200bp from TSS |

## Step 3: Query TF Binding at a Locus

Which transcription factors bind at your region across all ENCODE biosamples?

```bash
# Get TF rPeak clusters in a region
curl "https://api.genome.ucsc.edu/getData/track?genome=hg38;track=TFrPeakClusters;chrom=chr1;start=1000000;end=1100000;jsonOutputArrays=1"
```

### Response Fields (TFrPeakClusters)

| Field | Description |
|-------|-------------|
| `factor` | Transcription factor name (e.g., CTCF, POLR2A) |
| `ubiquity` | Fraction of experiments showing binding (0-1) |
| `cCRE` | Overlapping cCRE accession |
| `exp` | ENCODE experiment accessions (links to Portal) |

**Cross-reference with ENCODE Portal**: The `exp` field contains ENCODE experiment accessions. Use `encode_get_experiment` to get full metadata:
```
encode_get_experiment(accession="ENCSR...")
```

## Step 4: Retrieve DNA Sequence

Get the underlying DNA sequence for regulatory elements:

```bash
# Get sequence for a region
curl "https://api.genome.ucsc.edu/getData/sequence?genome=hg38;chrom=chr1;start=1000000;end=1000500"

# Get reverse complement
curl "https://api.genome.ucsc.edu/getData/sequence?genome=hg38;chrom=chr1;start=1000000;end=1000500;revComp=1"
```

Response includes a `dna` field with the nucleotide sequence.

**Use cases for sequence retrieval**:
- Extract sequence under ENCODE peaks for motif analysis (HOMER, MEME)
- Get sequence for CRISPR guide design at regulatory elements
- Check for known TF binding motifs at variants of interest
- Verify sequence context around GWAS variants

## Step 5: Query DNase Accessibility Across Cell Types

```bash
# DNase clusters (95 cell types)
curl "https://api.genome.ucsc.edu/getData/track?genome=hg38;track=wgEncodeRegDnaseClustered;chrom=chr1;start=1000000;end=1100000;jsonOutputArrays=1"
```

The `sourceCount` field tells you how many of the 95 cell types show accessibility at each site — a measure of how constitutive vs tissue-specific the element is.

## Step 6: Bulk Data Access with Command-Line Tools

For genome-wide queries, use UCSC command-line utilities instead of the REST API (which caps at 1M items):

```bash
# Download UCSC tools (macOS example)
# Available at: https://hgdownload.gi.ucsc.edu/admin/exe/

# Extract ENCODE cCREs for a region from hosted bigBed
bigBedToBed https://hgdownload.gi.ucsc.edu/gbdb/hg38/encode3/encodeCcreCombined.bb \
  -chrom=chr1 -start=1000000 -end=2000000 stdout

# Extract TF rPeak clusters
bigBedToBed https://hgdownload.gi.ucsc.edu/gbdb/hg38/bbi/ENCODE4/TFrPeakClusters.bb \
  -chrom=chr1 -start=1000000 -end=2000000 stdout

# Summarize bigWig signal over regions
bigWigSummary http://path/to/signal.bw chr1 1000000 1100000 10
```

### MySQL Direct Access (for legacy tables)

```bash
mysql --user=genome --host=genome-mysql.gi.ucsc.edu -A -P 3306 -D hg38 \
  -e "SELECT * FROM wgEncodeRegDnaseClustered WHERE chrom='chr1' AND chromStart >= 1000000 AND chromEnd <= 1100000;"
```

## Practical Workflow: ENCODE Portal + UCSC Integration

A typical regulatory analysis workflow combining both:

```
1. Search ENCODE for tissue-specific experiments:
   encode_search_experiments(assay_title="Histone ChIP-seq", target="H3K27ac", organ="pancreas")

2. Get experiment details and download peaks:
   encode_list_files(experiment_accession="ENCSR...", output_type="IDR thresholded peaks", assembly="GRCh38")

3. For each peak region, query UCSC for regulatory context:
   curl "https://api.genome.ucsc.edu/getData/track?genome=hg38;track=encodeCcreCombined;chrom=CHR;start=START;end=END;jsonOutputArrays=1"

4. Check which TFs bind at each peak:
   curl "https://api.genome.ucsc.edu/getData/track?genome=hg38;track=TFrPeakClusters;chrom=CHR;start=START;end=END;jsonOutputArrays=1"

5. Get DNA sequence for motif analysis:
   curl "https://api.genome.ucsc.edu/getData/sequence?genome=hg38;chrom=CHR;start=START;end=END"

6. Track and log provenance:
   encode_track_experiment(accession="ENCSR...", notes="Pancreas H3K27ac - UCSC cCRE overlap analysis")
```

## Pitfalls and Caveats

1. **1M item cap**: REST API returns maximum 1,000,000 items per query. For genome-wide analyses, iterate by chromosome or use command-line tools.
2. **No keyword filtering**: The API returns raw track data. Filtering (e.g., only PLS elements, only zScore > 5) must be done client-side after retrieval.
3. **Coordinate system mismatch**: UCSC uses 0-based half-open (BED format). VCF and GFF use 1-based. Always verify coordinate systems when cross-referencing.
4. **Legacy vs current tracks**: Tracks with `wgEncode` prefix are from ENCODE 2/3 and stored in MySQL tables. ENCODE 4 data uses bigBed files accessed via the REST API. Access methods differ.
5. **cCRE version**: The `encodeCcreCombined` track contains V3 cCREs (926,535). The expanded V4 registry (2.35M cCREs, Moore et al. 2024) may not yet be reflected on UCSC — check the SCREEN portal for the latest.
6. **Mirror availability**: Use `api.genome.ucsc.edu` (US), `genome-euro.ucsc.edu` (EU), or `genome-asia.ucsc.edu` (Asia) based on your location.

## Walkthrough: Visualizing ENCODE Data in the UCSC Genome Browser

**Goal**: Use UCSC Genome Browser REST API to retrieve candidate cis-regulatory elements (cCREs) and custom track data that complement ENCODE experiments, enabling genome-wide regulatory visualization.
**Context**: UCSC Genome Browser hosts ENCODE-derived cCRE tracks and provides REST API access to sequence, annotations, and track data.

### Step 1: Find ENCODE experiments to visualize

```
encode_search_experiments(assay_title="ATAC-seq", organ="heart", organism="Homo sapiens", limit=5)
```

Expected output:
```json
{
  "total": 18,
  "results": [
    {"accession": "ENCSR100HRT", "assay_title": "ATAC-seq", "biosample_summary": "heart left ventricle", "status": "released"}
  ]
}
```

### Step 2: Get ENCODE file URLs for UCSC track hub

```
encode_get_file_info(accession="ENCFF200BW")
```

Expected output:
```json
{
  "accession": "ENCFF200BW",
  "file_format": "bigWig",
  "output_type": "fold change over control",
  "href": "https://www.encodeproject.org/files/ENCFF200BW/@@download/ENCFF200BW.bigWig",
  "assembly": "GRCh38",
  "file_size_mb": 45.2
}
```

**Interpretation**: Use the bigWig download URL directly in a UCSC custom track or track hub for visualization.

### Step 3: Query UCSC cCRE track for the region of interest

Using UCSC REST API (via skill guidance):
```
GET https://api.genome.ucsc.edu/getData/track?genome=hg38&track=encodeCcreCombined&chrom=chr1&start=1000000&end=1100000
```

Expected response (key fields):
```json
{
  "encodeCcreCombined": [
    {"chrom": "chr1", "chromStart": 1020500, "chromEnd": 1021200, "name": "EH38E1234567", "ucscLabel": "pELS"},
    {"chrom": "chr1", "chromStart": 1050800, "chromEnd": 1051500, "name": "EH38E1234568", "ucscLabel": "dELS"}
  ]
}
```

**Interpretation**: pELS = proximal enhancer-like signature, dELS = distal enhancer-like signature. These cCRE classifications are derived from ENCODE data and provide standardized regulatory element annotations.

### Step 4: Retrieve sequence for motif analysis

```
GET https://api.genome.ucsc.edu/getData/sequence?genome=hg38&chrom=chr1&start=1020500&end=1021200
```

Use the retrieved sequence for downstream motif scanning with → **jaspar-motifs**.

### Step 5: Cross-reference with liftOver for assembly conversion

If you have hg19 coordinates that need conversion:
```
# Use liftover-coordinates skill for assembly conversion
# Then query UCSC API with GRCh38 coordinates
```

### Integration with downstream skills
- UCSC cCRE annotations complement → **regulatory-elements** ENCODE-based classification
- Sequence retrieval feeds into → **jaspar-motifs** for TF motif scanning
- UCSC track hub URLs support → **visualization-workflow** genome browser sessions
- cCRE coordinates integrate with → **peak-annotation** for regulatory element assignment
- Assembly conversion via → **liftover-coordinates** ensures correct UCSC API queries

## Code Examples

### 1. Search ENCODE for data to visualize on UCSC

```
encode_search_experiments(
  assay_title="ATAC-seq",
  organ="brain"
)
```

Expected output:
```json
{
  "total": 24,
  "experiments": [
    {
      "accession": "ENCSR789XYZ",
      "assay_title": "ATAC-seq",
      "biosample_summary": "brain tissue female adult (53 years)"
    }
  ]
}
```

### 2. Get file details for UCSC track hub setup

```
encode_list_files(
  accession="ENCSR789XYZ",
  file_format="bigWig",
  assembly="GRCh38"
)
```

Expected output:
```json
{
  "total": 4,
  "files": [
    {
      "accession": "ENCFF456DEF",
      "file_format": "bigWig",
      "output_type": "fold change over control",
      "assembly": "GRCh38",
      "file_size_mb": 125.3,
      "href": "/files/ENCFF456DEF/@@download/ENCFF456DEF.bigWig"
    }
  ]
}
```

## Integration

| This skill produces... | Feed into... | Using tool/skill |
|---|---|---|
| cCRE annotations | Regulatory element classification | regulatory-elements skill |
| DNA sequences from peak regions | Motif analysis | motif-analysis → HOMER/MEME |
| Conservation scores | Variant prioritization | variant-annotation skill |
| Track hub configuration | Visualization | visualization-workflow skill |
| Repeat masker annotations | Peak filtering | peak-annotation skill |

## Related Skills

| Skill | When to Use Instead/Additionally |
|-------|--------------------------------|
| `regulatory-elements` | Comprehensive cCRE classification and chromatin state analysis |
| `variant-annotation` | Annotating GWAS/eQTL variants with ENCODE functional data |
| `search-encode` | Finding specific ENCODE experiments by assay, tissue, target |
| `integrative-analysis` | Multi-mark integration for regulatory element characterization |
| `epigenome-profiling` | Full histone mark profiling workflow |
| `data-provenance` | Logging derived files from UCSC+ENCODE combined analyses |
| `geo-connector` | Cross-referencing ENCODE experiments with GEO accessions |
| `gnomad-variants` | Population frequency and constraint data for variants in UCSC regions |
| `ensembl-annotation` | VEP annotation and Regulatory Build overlap for UCSC-retrieved regions |
| `publication-trust` | Verify literature claims backing analytical decisions |

## Presenting Results

- Present UCSC links as clickable URLs with region, tracks, and assembly specified. Include direct session links when possible. Suggest: "Would you like to create a UCSC track hub for these experiments?"

## For the request: "$ARGUMENTS"
