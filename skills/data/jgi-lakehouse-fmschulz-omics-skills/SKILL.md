---
name: jgi-lakehouse
description: Queries JGI Lakehouse (Dremio) for genomics metadata from GOLD, IMG, Mycocosm, Phytozome. Downloads genome files from JGI filesystem using IMG taxon OIDs. Use when working with JGI data, GOLD projects, IMG annotations, or downloading microbial genomes.
---

# JGI Lakehouse Skill

## Quick Start

**What is it?** JGI's unified data warehouse (651 tables) + filesystem access to genome files.

**Two data access methods:**
1. **Lakehouse (Dremio)** → Metadata, annotations, taxonomy (no sequences)
2. **JGI Filesystem** → Actual genome files (FNA, FAA, GFF) via taxon OID

**SQL Dialect:** ANSI SQL (not PostgreSQL)
- Use `CAST(x AS type)` not `::`
- Use `REGEXP_LIKE()` not `~`
- Identifiers with dashes need double quotes: `"gold-db-2 postgresql"`

```sql
-- Quick test
SELECT gold_id, project_name FROM "gold-db-2 postgresql".gold.project
WHERE is_public = 'Yes' LIMIT 5;
```

---

## When to Use

- Query JGI genomics metadata (GOLD, IMG, Mycocosm, Phytozome)
- Find genomes by taxonomy, ecosystem, or phenotype
- Download microbial genomes with IMG taxon OIDs
- Cross-reference GOLD projects with IMG annotations

---

## Data Access: Lakehouse vs Filesystem

| Need | Source | Access Method |
|------|--------|---------------|
| Metadata (taxonomy, projects) | Lakehouse | SQL via REST API |
| Gene annotations (COG, Pfam, KO) | Lakehouse | SQL via REST API |
| **Genome sequences (FNA)** | **JGI Filesystem** | Copy from `/clusterfs/jgi/img_merfs-ro/` |
| **Protein sequences (FAA)** | **JGI Filesystem** | Copy from `/clusterfs/jgi/img_merfs-ro/` |
| Metagenome proteins only | Lakehouse | `numg-iceberg.faa` table |

**Critical insight:** The Lakehouse is a METADATA warehouse. Genome sequences must be accessed from the JGI filesystem or downloaded from NCBI.

---

## Key Data Sources

| Source | Path | Contents |
|--------|------|----------|
| GOLD | `"gold-db-2 postgresql".gold.*` | Projects, studies, samples, taxonomy |
| IMG | `"img-db-2 postgresql".img_core_v400.*` | Taxons, genes, annotations (244 tables) |
| Portal | `"portal-db-1".portal.*` | Download tracking, file paths |
| Mycocosm | `"myco-db-1 mysql".<organism>.*` | Fungal genomes (2,711 schemas) |
| Phytozome | `"plant-db-7 postgresql".*` | Plant genomics |
| NUMG | `"numg-iceberg"."numg-iceberg".*` | Metagenome proteins, Pfam hits |

**Full table catalog:** See [docs/data-catalog.md](docs/data-catalog.md)

---

## Downloading Genomes with IMG Taxon OIDs

### Option 1: JGI Filesystem (Fastest)

```bash
# Genome packages are at:
/clusterfs/jgi/img_merfs-ro/img_web/img_web_data/download/{taxon_oid}.tar.gz

# Example: Copy and extract
cp /clusterfs/jgi/img_merfs-ro/img_web/img_web_data/download/8136918376.tar.gz .
tar -xzf 8136918376.tar.gz
```

**Package contents:**
- `{taxon_oid}.fna` - Genome assembly
- `{taxon_oid}.genes.faa` - Protein sequences
- `{taxon_oid}.genes.fna` - Gene nucleotide sequences
- `{taxon_oid}.gff` - GFF annotations
- `{taxon_oid}.cog.tab.txt` - COG annotations
- `{taxon_oid}.pfam.tab.txt` - Pfam annotations
- `{taxon_oid}.ko.tab.txt` - KEGG KO annotations

### Option 2: Query Lakehouse + Download from NCBI

```sql
-- Get NCBI accessions for download
SELECT assembly_accession, organism_name, assembly_level, genome_size
FROM "gold-db-2 postgresql".gold.ncbi_assembly
WHERE assembly_level = 'Complete Genome' AND group_ = 'bacteria'
LIMIT 10;
```

```bash
# Download via NCBI datasets CLI
datasets download genome accession GCA_000219355.1 \
    --include genome,gff3,protein --filename genome.zip
```

**Detailed workflow:** See [examples/04-download-img-genomes.md](examples/04-download-img-genomes.md)

---

## Common Queries

### Find Bacterial Isolate Genomes
```sql
SELECT taxon_oid, taxon_display_name, phylum, genus, species
FROM "img-db-2 postgresql".img_core_v400.taxon
WHERE domain = 'Bacteria'
  AND genome_type = 'isolate'
  AND is_public = 'Yes'
  AND seq_status = 'Finished'
LIMIT 100;
```

### Link GOLD Project to IMG Taxon
```sql
SELECT t.taxon_oid, t.taxon_display_name, t.sequencing_gold_id
FROM "img-db-2 postgresql".img_core_v400.taxon t
WHERE t.sequencing_gold_id IS NOT NULL
LIMIT 50;
```

### Find Genomes with File Paths (Portal)
```sql
SELECT taxonOid, filePath
FROM "portal-db-1".portal.downloadRequestFiles
WHERE taxonOid IS NOT NULL
  AND filePath LIKE '%.tar.gz'
LIMIT 20;
```

---

## Critical Pitfalls

| Wrong | Correct |
|-------|---------|
| Join `ncbi_assembly` on `project_id` | `ncbi_assembly` has no `project_id`; use `bioproject` or `biosample` |
| `project.ecosystem` | Join `study` via `master_study_id` |
| `SHOW SCHEMAS IN "source"` | Works, but some syntax errors in older Dremio |
| Get sequences from Lakehouse | Download from filesystem or NCBI |
| `sra_experiment_v2.platform` | Use `library_instrument` |

---

## Authentication

```bash
export DREMIO_PAT=$(cat ~/.secrets/dremio_pat)
```

Token setup: See [docs/authentication.md](docs/authentication.md)

---

## API Access

**REST API Base:** `http://lakehouse-1.jgi.lbl.gov:9047/api/v3`

```python
# Use scripts/rest_client.py
from rest_client import query
results = query("SELECT * FROM ... LIMIT 10")
```

---

## Documentation

- [docs/data-catalog.md](docs/data-catalog.md) - Complete table inventory (651 tables)
- [docs/sql-quick-reference.md](docs/sql-quick-reference.md) - Dremio SQL syntax
- [examples/04-download-img-genomes.md](examples/04-download-img-genomes.md) - Download with taxon OIDs
- [scripts/download_img_genomes.py](scripts/download_img_genomes.py) - Automated download script
