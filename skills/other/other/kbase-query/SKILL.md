---
name: kbase-query
description: Skills for querying the KBase/BERDL Datalake via the MCP REST API. Use this when users want to explore KBase databases, list tables, get schemas, sample data, or run SQL queries against the KBase data lake. Triggers on mentions of KBase, BERDL, or requests to query biological/microbiome data stored in KBase.
---

# KBase Query

Query the KBase/BERDL Datalake MCP Server via REST API.

## Setup

```bash
export KBASE_TOKEN="your_token_here"
export KBASE_MCP_URL="https://hub.berdl.kbase.us/apis/mcp"  # optional default
```

### Getting your token

1. Login to the KBase JupyterHub
2. In any notebook, run:
   ```python
   BERDLSettings().KBASE_AUTH_TOKEN
   ```
3. Copy the token value

**Note:** Tokens expire after ~1 week. If you get auth errors, refresh your token.

## Scripts

All scripts require `KBASE_TOKEN` env var and `jq` installed.

| Script | Usage |
|--------|-------|
| `kbase_health.sh` | Check API health |
| `kbase_list_databases.sh` | List all databases |
| `kbase_list_tables.sh <db>` | List tables in database |
| `kbase_table_schema.sh <db> <table>` | Get table columns |
| `kbase_db_structure.sh [with_schema]` | Full DB structure |
| `kbase_table_count.sh <db> <table>` | Row count |
| `kbase_table_sample.sh <db> <table> [limit]` | Sample rows (max 100) |
| `kbase_query.sh <sql> [limit]` | Execute SQL (max 1000) |
| `kbase_select.sh <db> <table> [limit]` | Structured select |

## Example Workflow

```bash
# List databases
kbase_list_databases.sh
# → {"databases": ["kbase_ke_pangenome", "nmdc_core", ...]}

# List tables in pangenome database
kbase_list_tables.sh kbase_ke_pangenome
# → {"tables": ["genome", "gene", "gene_cluster", ...]}

# Get columns for a table (returns names only, not types)
kbase_table_schema.sh kbase_ke_pangenome genome
# → {"columns": ["genome_id", "gtdb_species_clade_id", ...]}

# Sample rows
kbase_table_sample.sh kbase_ke_pangenome genome 5

# SQL query
kbase_query.sh "SELECT * FROM kbase_ke_pangenome.genome LIMIT 10"
```

## Useful jq Patterns

```bash
# Extract just database names
kbase_list_databases.sh | jq -r '.databases[]'

# Get columns as comma-separated list
kbase_table_schema.sh kbase_ke_pangenome genome | jq -r '.columns | join(", ")'

# Loop through all tables to get schemas
for t in $(kbase_list_tables.sh kbase_ke_pangenome | jq -r '.tables[]'); do
  echo "=== $t ==="
  kbase_table_schema.sh kbase_ke_pangenome "$t" | jq -r '.columns | join(", ")'
done
```

## Available Databases

Key databases include:
- `kbase_ke_pangenome` - Pangenomic data with GTDB taxonomy
- `nmdc_core` - NMDC microbiome data
- `kbase_genomes` - KBase genome collection
- `kbase_uniprot_*` - UniProt reference data

## API Reference

See [references/api_reference.md](references/api_reference.md) for complete endpoint documentation.
