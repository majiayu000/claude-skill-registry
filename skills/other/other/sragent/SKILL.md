---
name: sragent
description: |
  Query the Sequence Read Archive (SRA), retrieve scientific publications, and analyze 
  genomics metadata using the SRAgent toolkit. Supports accession conversion (GSE→SRX→SRR), 
  BigQuery metadata queries, manuscript downloads from multiple sources, and scRNA-seq 
  technology identification. Use when working with SRA/GEO datasets, finding publications, 
  or analyzing single-cell sequencing experiments.
---

# SRAgent: Sequence Read Archive Data and Publication Retrieval

## Overview

SRAgent is an agentic workflow system for working with the NCBI Sequence Read Archive (SRA) and Gene Expression Omnibus (GEO) databases.
It automates literature discovery, metadata extraction, and manuscript retrieval for genomics datasets.

## Setup Instructions

### 1. Install SRAgent

SRAgent requires Python ≥3.11. Check to see if SRAgent is already installed:
```bash
which SRAgent
```

If SRAgent is not installed, follow the instructions below.

Install using `uv`:

```bash
# Clone the repository
git clone https://github.com/ArcInstitute/SRAgent.git
cd SRAgent

# Create and activate virtual environment with uv
uv venv
source .venv/bin/activate

# Install the package
uv pip install .
```

Verify installation:
```bash
SRAgent --help
```

### 2. Configure environment variables

The following environment variables are required:
- `OPENAI_API_KEY=sk-openai-...`
  - Needed to use OpenAI models
- `ANTHROPIC_API_KEY=sk-ant-...`
  - Needed to use Claude models
- `DYNACONF`
  - Needed to switch between Claude and OpenAI models
- `EMAIL=user@example.com`
  - Needed for using the Entrez API
- `NCBI_API_KEY=your-ncbi-key`
  - Optional for increased rate limits when using the Entrez API
- `CORE_API_KEY=your-core-key`
  - Optional for paper downloads from the CORE API
- `GCP_PROJECT_ID=your-project-id`
  - Needed for using Google BigQuery
- `GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json`
  - Needed for using Google BigQuery

Prompt the user to provide the environment variables if they are not already set as environment variables: `export MY_SECRET_VAR=my-secret-value`.

### 3. Configure Settings

SRAgent uses a settings file (`settings.yml`) to configure models and behavior.
The default configuration works for most users, but you can customize it.

#### Option A: Use Default Settings
No action needed - SRAgent ships with sensible defaults.

#### Option B: Custom Settings File

See `./references/example-settings.yml` for an example settings file that you can modify as needed.

### 4. Verify Setup

Test your configuration:

```bash
# Check which model is being used
python -c "from SRAgent.agents.utils import load_settings; s = load_settings(); print(s['models']['default'])"

# Test basic functionality
SRAgent entrez "Convert GSE121737 to SRX accessions"
```

## Core Capabilities

### 1. Accession Conversion
Convert between different genomics database accession formats:
- **GEO Series:** GSE* → SRA Study (SRP*)
- **SRA Study:** SRP*/PRJNA* → SRA Experiments (SRX*)
- **SRA Experiment:** SRX*/ERX* → SRA Runs (SRR*/ERR*)

### 2. Metadata Extraction
Query comprehensive metadata from SRA/GEO:
- Sequencing platform (Illumina, PacBio, Oxford Nanopore)
- Library preparation technology (10X Genomics, Smart-seq, etc.)
- Organism, tissue, cell type
- Study design and experimental details
- Single-cell vs bulk RNA-seq identification

### 3. BigQuery Analysis
Leverage NCBI's BigQuery dataset for large-scale queries:
- Batch accession conversions
- Technology identification across studies
- Filtering by platform, assay type, organism
- Study/experiment/run relationship mapping

### 4. Publication Retrieval
Automatically find and download manuscripts:
- Link SRA accessions to PubMed publications
- Extract DOIs from PubMed records
- Download full-text PDFs from multiple sources:
  - Preprint servers (arXiv, bioRxiv, medRxiv)
  - CORE API
  - Europe PMC
  - Unpaywall
- Batch processing with CSV input

## When to Use This Skill

Use SRAgent when the user:
- Mentions SRA, GEO, or genomics accessions (GSE, SRP, SRX, SRR)
- Needs to convert between accession formats
- Wants metadata about sequencing experiments
- Needs to find or download papers associated with datasets
- References the Sequence Read Archive (SRA), European Nucleotide Archive (ENA), or Gene Expression Omnibus (GEO)

## Available Commands

### Command 1: `SRAgent entrez`
**Purpose:** Low-level NCBI Entrez database queries

**Best for:**
- Simple accession conversions
- Quick dataset summaries
- Cross-database linking
- When you know exactly what Entrez tool to use (esearch, efetch, elink)

**Examples:**
```bash
# Convert GEO to SRX
SRAgent --no-progress --no-summaries entrez "Convert GSE121737 to SRX accessions"

# Summarize a dataset
SRAgent --no-progress --no-summaries entrez "Summarize SRX4967527"

# Link to publications
SRAgent --no-progress --no-summaries entrez "Find publications for GSE196830"
```

### Command 2: `SRAgent sragent`
**Purpose:** Comprehensive metadata extraction with multiple tools

**Best for:**
- Complex metadata queries
- Technology identification
- When simple Entrez queries aren't enough
- Determining if data is single-cell

**Tools available:**
- Entrez agent (all databases)
- BigQuery (large-scale queries)
- NCBI web scraping
- sra-stat (direct sequence file analysis)

**Examples:**
```bash
# Check sequencing technology
SRAgent --no-progress --no-summaries sragent "Which 10X Genomics technology was used for ERX11887200?"

# Comprehensive summary
SRAgent --no-progress --no-summaries sragent "Summarize SRX4967527"

# Verify data type
SRAgent --no-progress --no-summaries sragent "Is SRX4967527 single-cell RNA-seq data?"

# Get organism info
SRAgent --no-progress --no-summaries sragent "What organism was sequenced in study PRJNA498286?"
```

### Command 3: `SRAgent papers`
**Purpose:** Find and download manuscripts associated with SRA accessions

**Best for:**
- Downloading papers for datasets
- Batch retrieval of publications
- Enriching CSV files with DOIs and download paths

**Input formats:**
- Single accession: `SRX4967527`
- Study accession: `SRP167700` or `PRJNA498286`
- CSV file with `accession` column

**Examples:**
```bash
# Single experiment
SRAgent --no-progress --no-summaries papers SRX4967527

# Entire study
SRAgent --no-progress --no-summaries papers PRJNA498286

# Batch from CSV
SRAgent --no-progress --no-summaries papers accessions.csv --output-dir papers/

# Custom accession column name
SRAgent --no-progress --no-summaries papers my-data.csv --accession-column "experiment_id"

# Control concurrency
SRAgent --no-progress --no-summaries papers accessions.csv --max-concurrency 3
```

**Output:**
- PDFs saved to `--output-dir/<accession>/`
- Console summary showing:
  - PubMed IDs found
  - DOIs extracted
  - Download success/failure status
- Updated CSV (when input is CSV) with columns:
  - `pubmed_id`
  - `doi`
  - `download_path`

## Usage Patterns

### Pattern 1: Dataset Investigation Workflow
```bash
# Step 1: Convert GEO accession to SRX
SRAgent --no-progress --no-summaries entrez "Convert GSE121737 to SRX accessions"

# Step 2: Get detailed metadata
SRAgent --no-progress --no-summaries sragent "For each SRX from GSE121737, determine: Is it single-cell? What library prep?"

# Step 3: Find associated publications
SRAgent --no-progress --no-summaries papers GSE121737 --output-dir manuscripts/
```

### Pattern 2: Technology Verification
```bash
# Check if dataset meets specific criteria
SRAgent --no-progress --no-summaries sragent "Is SRX4967527 Illumina paired-end single-cell RNA-seq data?"

# Get specific technology details
SRAgent --no-progress --no-summaries sragent "Which 10X Genomics chemistry was used: SRX4967527?"

# Verify organism
SRAgent --no-progress --no-summaries sragent "What organism is SRX4967527?"
```

### Pattern 3: Batch Processing
```bash
# Create CSV with accessions
cat > accessions.csv << EOF
accession
SRX4967527
SRX4967528
SRX4967529
EOF

# Download all papers
SRAgent --no-progress --no-summaries \
  papers accessions.csv \
    --output-dir papers/ \
    --max-concurrency 5

# Result: CSV enriched with DOIs and download paths
```

### Pattern 4: Study-Level Analysis
```bash
# Get all experiments in a study
SRAgent --no-progress --no-summaries entrez "List all SRX accessions for study SRP167700"

# Or use a BioProject accession
SRAgent --no-progress --no-summaries entrez "Convert PRJNA498286 to SRX accessions"

# Then analyze the study
SRAgent --no-progress --no-summaries sragent "Summarize the library prep technologies used in PRJNA498286"
```

## Implementation Guide for Claude

### Running SRAgent Commands

When the user needs SRAgent functionality, use the bash tool:

```python
# Example: Convert accessions
result = bash_tool(
    command="SRAgent --no-progress --no-summaries entrez 'Convert GSE121737 to SRX accessions'",
    description="Converting GEO accession to SRX format"
)

# Example: Get metadata
result = bash_tool(
    command="SRAgent --no-progress --no-summaries sragent 'Which 10X technology was used for SRX4967527?'",
    description="Determining library preparation technology"
)

# Example: Download papers
result = bash_tool(
    command="SRAgent --no-progress --no-summaries papers SRX4967527 --output-dir /home/claude/papers",
    description="Downloading manuscripts for dataset"
)
```

### Working with CSV Files

When processing batch data:

```python
import pandas as pd

# User provides accessions - create CSV
accessions = ["SRX4967527", "SRX4967528", "SRX4967529"]
df = pd.DataFrame({"accession": accessions})
df.to_csv("/home/claude/accessions.csv", index=False)

# Run SRAgent papers command
result = bash_tool(
    command="SRAgent --no-progress --no-summaries papers /home/claude/accessions.csv --output-dir /home/claude/papers",
    description="Batch downloading papers for multiple accessions"
)

# Read enriched CSV
enriched_df = pd.read_csv("/home/claude/accessions.csv")
# Now has: accession, pubmed_id, doi, download_path columns
```

## Accession Format Reference

### GEO (Gene Expression Omnibus)
- **Series:** `GSE` + 5-7 digits (e.g., `GSE121737`)
- **Sample:** `GSM` + 6-7 digits (e.g., `GSM3457845`)

### SRA (Sequence Read Archive)
- **Study:** `SRP` + 6 digits (e.g., `SRP167700`)
  - Or BioProject: `PRJNA` + 6 digits (e.g., `PRJNA498286`)
- **Experiment:** `SRX` + 7-8 digits (e.g., `SRX4967527`)
- **Run:** `SRR` + 7-8 digits (e.g., `SRR8124405`)

### ENA (European Nucleotide Archive)
- **Study:** `ERP` + 6 digits or `PRJEB` + 6 digits
- **Experiment:** `ERX` + 7-8 digits (e.g., `ERX11887200`)
- **Run:** `ERR` + 7-8 digits

### Hierarchical Relationships
```
GEO Series (GSE)
    ↓
SRA Study (SRP) = BioProject (PRJNA)
    ↓
SRA Experiment (SRX) ← Links to → Publications (PubMed ID, DOI)
    ↓
SRA Run (SRR) [actual sequence files]
```

## Common Single-Cell Technologies

SRAgent can identify these scRNA-seq technologies:

### 10X Genomics
- **Chromium Single Cell 3'** (v1, v2, v3)
- **Chromium Single Cell 5'**
- **Chromium Single Cell ATAC**
- **Chromium Single Cell Multiome**
- **Visium Spatial**

### Other Platforms
- **Smart-seq2** / **Smart-seq3**
- **Drop-seq**
- **inDrop**
- **Seq-Well**
- **CEL-Seq2**
- **MARS-seq**
- **Quartz-Seq**

### Detection Strategy
SRAgent uses multiple signals:
1. Library prep metadata fields
2. Study descriptions and titles
3. PubMed abstracts
4. Sequence file characteristics (when using sra-stat)


### Working Without BigQuery

If you don't have Google Cloud credentials:

```bash
# SRAgent gracefully falls back to Entrez-only queries
# BigQuery features will be skipped with a warning

# These still work without BigQuery:
SRAgent --no-progress --no-summaries entrez "Convert GSE121737 to SRX accessions"
SRAgent --no-progress --no-summaries papers SRX4967527

# This will warn but proceed:
SRAgent --no-progress --no-summaries sragent "Which 10X technology for SRX4967527?"
# (Uses Entrez + web scraping instead of BigQuery)
```

### Performance Optimization

```bash
# For large batch operations, adjust concurrency
SRAgent --no-progress --no-summaries papers large-dataset.csv \
  --max-concurrency 10 \
  --recursion-limit 150

# For paper downloads specifically
SRAgent --no-progress --no-summaries papers accessions.csv \
  --core-api-key "$CORE_API_KEY" \
  --email "$EMAIL" \
  --max-concurrency 5
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'SRAgent'"
```bash
# Ensure package is installed
cd SRAgent
uv pip install .

# Verify installation
python -c "import SRAgent; print(SRAgent.__file__)"
```

### "Rate limit exceeded" (NCBI)
```bash
# Get NCBI API key: https://www.ncbi.nlm.nih.gov/account/settings/
export NCBI_API_KEY="your-ncbi-api-key"

# Reduces concurrent requests
SRAgent papers accessions.csv --max-concurrency 3
```

### Paper downloads fail

- Check: Is DOI found?
  - Some datasets may not have linked publications
  - Check PubMed link manually first

- Check: Multiple sources attempted?
  - SRAgent tries: preprints → CORE → Europe PMC → Unpaywall
  - Some papers are paywalled (no open access)

- Check: Network/authentication
  - CORE requires API key: export CORE_API_KEY="..."
  - Some sources may be blocked by institution firewall
  - Cloudflare may block automated access to some preprint servers


## Resources

### SRAgent Documentation

- `./references/metadata-fields.md`
  - All metadata fields that SRAgent can extract from SRA/GEO databases
- `./references/quick-reference.md`
 - Quick reference for SRAgent commands
- `./references/usage-examples.md`
 - Usage examples for SRAgent
- `./references/example-settings.yml`
  - Example settings file for SRAgent

### External Resources

- **GitHub:** https://github.com/ArcInstitute/SRAgent
- **Paper:** bioRxiv 2025.02.27.640494 (scBaseCount manuscript)
- **NCBI Entrez:** https://www.ncbi.nlm.nih.gov/books/NBK25500/
- **SRA Database:** https://www.ncbi.nlm.nih.gov/sra
- **GEO Database:** https://www.ncbi.nlm.nih.gov/geo/

