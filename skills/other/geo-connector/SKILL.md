---
name: geo-connector
description: Search, query, and cross-reference NCBI GEO (Gene Expression Omnibus) datasets with ENCODE experiments. Use when the user wants to find GEO accessions for ENCODE experiments, search GEO for complementary datasets, download GEO metadata or series matrices, cross-reference ENCODE and GEO data, find supplementary files from GEO, or link GEO series to ENCODE experiments for provenance tracking. Also use when the user mentions GEO, GSE, GSM, GPL, GDS, series matrix, SOFT format, or needs to find expression data in GEO that complements their ENCODE analysis.
---

# Search and Cross-Reference NCBI GEO with ENCODE

## When to Use

- User wants to find complementary datasets in NCBI GEO to supplement ENCODE data
- User asks about "GEO", "Gene Expression Omnibus", "supplementary data", or "find related datasets"
- User needs to cross-reference ENCODE experiments with GEO series for additional replicates or conditions
- User wants to link ENCODE accessions to GEO/SRA identifiers for data sharing or citation
- Example queries: "find GEO datasets for pancreatic islet RNA-seq", "link this ENCODE experiment to GEO", "search GEO for complementary ATAC-seq data"

Query the Gene Expression Omnibus programmatically to find complementary datasets, cross-reference ENCODE experiments, and download metadata.

## Scientific Rationale

**The question**: "What additional expression or epigenomic datasets exist in GEO that complement my ENCODE analysis?"

GEO hosts >200,000 series across all organisms and assay types. Many ENCODE experiments are deposited in GEO as secondary archives (ENCODE Portal is primary). GEO also contains vast amounts of non-ENCODE data — disease cohorts, perturbation experiments, time courses — that complement ENCODE's reference epigenomes.

### GEO ↔ ENCODE Relationship

- ENCODE processed data is deposited at GEO as standard GSE submissions
- Raw sequencing data goes to SRA (linked from both GEO and ENCODE)
- The ENCODE Portal is canonical; GEO is secondary archive
- GEO accessions are stored in ENCODE's `dbxrefs` field as `GEO:GSExxxxx`
- NCBI maintains a dedicated ENCODE listing: https://www.ncbi.nlm.nih.gov/geo/encode/

## GEO Entity Hierarchy

```
Series (GSE) — An experiment/study
  ├── Sample (GSM) — Individual measurements
  │     ├── references → Platform (GPL)
  │     ├── has → Supplementary files (raw data)
  │     └── has → Data table (normalized values)
  │
  └── curated into → DataSet (GDS) [not all GSE get curated]
        └── generates → Profiles (gene-level summaries)
```

## Step 1: Find GEO Accessions for ENCODE Experiments

### From ENCODE → GEO

ENCODE experiments may have GEO cross-references in their metadata. After tracking an experiment:

```
encode_track_experiment(accession="ENCSR...")
```

Check the experiment's `dbxrefs` field for `GEO:GSExxxxx` entries. If found, link it:

```
encode_link_reference(
    experiment_accession="ENCSR...",
    reference_type="geo_accession",
    reference_id="GSE12345"
)
```

### From GEO → ENCODE

Search GEO for ENCODE-deposited data:

```bash
# Via NCBI E-utilities
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&term=ENCODE[KEYWORD]+AND+gse[ETYP]&retmax=100&usehistory=y&tool=encode_mcp&email=YOUR_EMAIL"
```

## Step 2: Search GEO for Complementary Datasets

### E-utilities Search Syntax

**Base URL**: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi`

**Required parameters**: `db=gds`, `term=QUERY`, `tool=encode_mcp`, `email=YOUR_EMAIL`

**Rate limit**: 3 req/sec without API key, 10 req/sec with key. Get a key at https://www.ncbi.nlm.nih.gov/account/

### Search Field Qualifiers

| Qualifier | Purpose | Example |
|-----------|---------|---------|
| `[ETYP]` | Entry type | `gse[ETYP]`, `gds[ETYP]` |
| `[ORGN]` | Organism | `"Homo sapiens"[ORGN]` |
| `[PDAT]` | Publication date | `2024[PDAT]` |
| `[ACCN]` | Accession | `GPL96[ACCN]` |
| `[suppFile]` | Supplementary file type | `bed[suppFile]`, `bw[suppFile]` |

### Example Searches

```bash
# Human pancreas ATAC-seq datasets with BED files
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&term=pancreas+AND+ATAC-seq+AND+%22Homo+sapiens%22[ORGN]+AND+gse[ETYP]+AND+bed[suppFile]&retmax=50&tool=encode_mcp&email=YOUR_EMAIL"

# ChIP-seq datasets from a specific year
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&term=ChIP-seq+AND+H3K27ac+AND+gse[ETYP]+AND+2024[PDAT]&retmax=50&tool=encode_mcp&email=YOUR_EMAIL"

# Datasets associated with a PubMed ID
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&db=gds&id=PMID&tool=encode_mcp&email=YOUR_EMAIL"
```

## Step 3: Retrieve GEO Metadata

### Get Summary for GEO Records

```bash
# Step 1: Search (returns UIDs, NOT accessions)
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&term=GSE12345[ACCN]&tool=encode_mcp&email=YOUR_EMAIL"

# Step 2: Get summary (use UID from step 1)
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gds&id=UID&version=2.0&tool=encode_mcp&email=YOUR_EMAIL"
```

### Direct Record Access (acc.cgi)

```bash
# Get full SOFT-format record
curl "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE12345&targ=self&view=full&form=text"

# Get XML (MINiML) format
curl "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE12345&targ=self&view=full&form=xml"

# Get all sample metadata for a series
curl "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE12345&targ=gsm&view=brief&form=text"
```

## Step 4: Download GEO Data Files

### FTP Directory Convention

GEO uses a "nnn" directory pattern: replace last 3 digits with "nnn".

| Accession | FTP Path |
|-----------|----------|
| GSE12345 | `ftp://ftp.ncbi.nlm.nih.gov/geo/series/GSE12nnn/GSE12345/` |
| GSM575 | `ftp://ftp.ncbi.nlm.nih.gov/geo/samples/GSMnnn/GSM575/` |

### Key Download Paths

| Content | Path Under Series Directory |
|---------|----------------------------|
| Series matrix (expression table) | `matrix/GSE12345_series_matrix.txt.gz` |
| SOFT metadata | `soft/GSE12345_family.soft.gz` |
| MINiML (XML) | `miniml/GSE12345_family.xml.tgz` |
| All supplementary files | `suppl/GSE12345_RAW.tar` |
| Individual supplementary | `suppl/FILENAME.gz` |

### Download Commands

```bash
# Download series matrix (fastest for expression data)
wget "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE12nnn/GSE12345/matrix/GSE12345_series_matrix.txt.gz"

# Download all supplementary files
wget "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE12nnn/GSE12345/suppl/GSE12345_RAW.tar"
```

### Format Selection Guide

| Use Case | Format | Speed |
|----------|--------|-------|
| Expression matrix analysis | Series matrix | Fastest (10-100x vs SOFT) |
| Full metadata extraction | SOFT | Complete but slow |
| XML processing | MINiML | Good for programmatic parsing |
| Peak/BED files | Supplementary | Direct download |
| Raw sequencing reads | SRA (not GEO) | Use SRA Toolkit |

## Step 5: Cross-Reference Workflow

### ENCODE + GEO Integration Pattern

```
1. Find ENCODE experiments of interest:
   encode_search_experiments(assay_title="total RNA-seq", organ="pancreas")

2. For each experiment, check for GEO accession:
   encode_get_experiment(accession="ENCSR...")
   → Look in dbxrefs for "GEO:GSExxxxx"

3. If GEO accession found, link it:
   encode_link_reference(
       experiment_accession="ENCSR...",
       reference_type="geo_accession",
       reference_id="GSE12345"
   )

4. Search GEO for complementary non-ENCODE datasets:
   E-utils search for same tissue + different assay or condition

5. Download GEO metadata for comparison:
   acc.cgi or E-utils esummary

6. Log the cross-reference:
   encode_log_derived_file(
       file_path="/path/to/comparison.tsv",
       source_accessions=["ENCSR...", "GSE12345"],
       description="ENCODE-GEO cross-tissue comparison"
   )
```

### Finding SRA Accessions from GEO

For sequencing data, raw reads are in SRA, not GEO:

```bash
# Link GEO to SRA
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=gds&db=sra&id=GDS_UID&tool=encode_mcp&email=YOUR_EMAIL"
```

Python alternative using pysradb:
```python
from pysradb.search import SraSearch
# Convert GSE to SRP
pysradb gse-to-srp GSE12345
# Get all SRR run accessions
pysradb gsm-to-srr GSM12345
```

## Pitfalls and Caveats

1. **E-utils return UIDs, not accessions**: GEO search returns numeric UIDs. You must call ESummary to get the actual GSE/GDS accession numbers.
2. **Not all ENCODE experiments have GEO accessions**: The `dbxrefs` field may be empty. ENCODE Portal is always the canonical source.
3. **GEO search max is 10,000 per call**: Use `usehistory=y` and paginate with `retstart` for large result sets.
4. **Series matrix may be split**: Large studies can produce multiple matrix files (`*_series_matrix-1.txt.gz`, `*_series_matrix-2.txt.gz`).
5. **SOFT format discontinued for new submissions** (early 2024): Existing records are still downloadable, but new submissions use different formats.
6. **Rate limits are strict**: Without API key, max 3 requests/second. Include `tool=` and `email=` parameters on every request.
7. **GEO metadata quality varies**: User-submitted metadata may be inconsistent. Always verify organism, platform, and sample characteristics.

## Walkthrough: Finding Complementary GEO Datasets for ENCODE Experiments

**Goal**: Identify Gene Expression Omnibus (GEO) datasets that complement ENCODE epigenomic experiments, enabling integrative analysis of gene expression with regulatory elements.
**Context**: ENCODE provides epigenomic maps (ChIP-seq, ATAC-seq), while GEO hosts vast RNA-seq expression datasets. Combining them links regulatory elements to transcriptional output.

### Step 1: Identify the ENCODE experiment to complement

```
encode_get_experiment(accession="ENCSR123HEP")
```

Expected output:
```json
{
  "accession": "ENCSR123HEP",
  "assay_title": "Histone ChIP-seq",
  "target": "H3K27ac",
  "biosample_summary": "HepG2",
  "organism": "Homo sapiens",
  "status": "released"
}
```

**Interpretation**: This is H3K27ac ChIP-seq in HepG2 (liver cancer cell line). We need matching RNA-seq data from the same cell line.

### Step 2: Search GEO for complementary RNA-seq

Using NCBI E-utilities (via skill guidance):
```
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&term=HepG2[cell+line]+AND+RNA-seq[strategy]+AND+Homo+sapiens[organism]&retmax=10
```

Expected response:
```json
{
  "esearchresult": {
    "count": "142",
    "idlist": ["200156789", "200145678", "200134567"]
  }
}
```

### Step 3: Link ENCODE experiment to GEO dataset

```
encode_link_reference(accession="ENCSR123HEP", reference_type="geo", reference_id="GSE156789", notes="HepG2 RNA-seq for enhancer-expression integration")
```

Expected output:
```json
{
  "status": "linked",
  "accession": "ENCSR123HEP",
  "reference_type": "geo",
  "reference_id": "GSE156789"
}
```

### Step 4: Check for ENCODE RNA-seq in same biosample

```
encode_search_experiments(assay_title="total RNA-seq", biosample_term_name="HepG2", organism="Homo sapiens")
```

Expected output:
```json
{
  "total": 15,
  "results": [
    {"accession": "ENCSR456RNA", "assay_title": "RNA-seq", "biosample_summary": "HepG2", "status": "released"}
  ]
}
```

**Interpretation**: ENCODE already has 15 HepG2 RNA-seq experiments! Always check ENCODE first before going to GEO. GEO becomes essential when ENCODE lacks expression data for your specific biosample or experimental condition (e.g., drug treatment, knockdown).

### Integration with downstream skills
- GEO expression data feeds into → **peak-annotation** for enhancer target gene validation
- GEO dataset accessions integrate with → **cite-encode** for proper data attribution
- GEO RNA-seq complements → **gtex-expression** for cell-line-specific expression
- GEO metadata links to → **data-provenance** for full analysis audit trail

## Code Examples

### 1. Link an ENCODE experiment to GEO

```
encode_link_reference(
  accession="ENCSR000AKA",
  reference_type="geo_accession",
  reference_id="GSE76079",
  notes="Complementary RNA-seq from same lab"
)
```

Expected output:
```json
{
  "status": "linked",
  "accession": "ENCSR000AKA",
  "reference_type": "geo_accession",
  "reference_id": "GSE76079"
}
```

### 2. View all references for a tracked experiment

```
encode_get_references(accession="ENCSR000AKA")
```

Expected output:
```json
{
  "accession": "ENCSR000AKA",
  "references": [
    {"type": "geo_accession", "id": "GSE76079", "notes": "Complementary RNA-seq"},
    {"type": "pmid", "id": "27429435", "notes": "Primary publication"}
  ]
}
```

## Integration

| This skill produces... | Feed into... | Using tool/skill |
|---|---|---|
| GEO accession (GSE/GSM) | Cross-reference link | encode_link_reference(reference_type="geo_accession") |
| Supplementary expression data | Differential expression | integrative-analysis skill |
| Complementary replicates from GEO | Expanded sample size | download-encode + batch-analysis |
| SRA run accessions | Raw data download | bioinformatics-installer (sra-tools) |
| GEO metadata | Publication cross-reference | cite-encode skill |

## Related Skills

| Skill | When to Use Instead/Additionally |
|-------|--------------------------------|
| `cross-reference` | General external reference linking (PubMed, DOI, GEO, NCT) |
| `data-provenance` | Logging derived files from ENCODE+GEO combined analyses |
| `search-encode` | Finding ENCODE experiments (primary source) |
| `download-encode` | Downloading ENCODE files (preferred over GEO for ENCODE data) |
| `track-experiments` | Local experiment tracking with GEO cross-references |
| `cite-encode` | Getting citations for ENCODE experiments found via GEO |
| `ucsc-browser` | Querying aggregated ENCODE tracks at UCSC |
| `publication-trust` | Verify literature claims backing analytical decisions |

## Presenting Results

- Present GEO links as: ENCODE_accession | GEO_accession | title | organism | samples. Suggest: "Would you like to link these GEO accessions to the tracked experiments?"

## For the request: "$ARGUMENTS"
