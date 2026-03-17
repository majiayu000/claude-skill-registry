---
name: jgi-lakehouse
description: Skills for querying the JGI Dremio Lakehouse containing GOLD and IMG genomics databases. Use this when users want to explore JGI databases, query GOLD (Genomes OnLine Database), IMG (Integrated Microbial Genomes), or run SQL queries against JGI genomics data. Triggers on mentions of JGI, GOLD database, IMG database, genome metadata, or JGI lakehouse queries.
---

# JGI Lakehouse Query

Query the JGI Dremio Lakehouse via CLI.

## Setup

```bash
pip install linkml-store[dremio]
export DREMIO_USER="your_username"
export DREMIO_PASSWORD="your_password"
export CF_AUTHORIZATION="your_token"
```

## Getting the CF_AUTHORIZATION token

The CF_AUTHORIZATION token is a Cloudflare Access cookie required for authentication:

* Open https://lakehouse.jgi.lbl.gov/ in your browser
* Open Developer Tools (F12) > Application > Cookies
* Copy the value of the CF_Authorization cookie

Note that unless you have computer control you will have to ask your human to do this

## Connection

```bash
# Base connection (no schema filter)
DB="dremio-rest://lakehouse.jgi.lbl.gov"

# GOLD database
GOLD="dremio-rest://lakehouse.jgi.lbl.gov?schema=gold-db-2 postgresql.gold"

# IMG Core database
IMG="dremio-rest://lakehouse.jgi.lbl.gov?schema=img-db-2 postgresql.img_core_v400"
```

## SQL Queries

Direct SQL via `--sql` flag:

```bash
# Query GOLD studies
linkml-store -d "$DB" query --sql 'SELECT * FROM "gold-db-2 postgresql".gold.study LIMIT 10'

# Count by ecosystem
linkml-store -d "$DB" query --sql 'SELECT ecosystem, COUNT(*) as cnt FROM "gold-db-2 postgresql".gold.study GROUP BY ecosystem ORDER BY cnt DESC'

# Join tables
linkml-store -d "$DB" query --sql 'SELECT s.study_name, p.project_name FROM "gold-db-2 postgresql".gold.study s JOIN "gold-db-2 postgresql".gold.project p ON s.study_id = p.study_id LIMIT 10'

# Output formats
linkml-store -d "$DB" query --sql '...' -O json
linkml-store -d "$DB" query --sql '...' -O csv
linkml-store -d "$DB" query --sql '...' -O yaml
```

## Collection Queries

When schema is set, use collection-based queries:

```bash
# List tables
linkml-store -d "$GOLD" list-collections

# Query collection
linkml-store -d "$GOLD" -c study query --limit 10

# With filter
linkml-store -d "$GOLD" -c study query -w "ecosystem=Host-associated" --limit 20

# Describe table
linkml-store -d "$GOLD" -c study describe
```

## Schema Export

```bash
# Export LinkML schema with FK relationships
linkml-store -d "$GOLD" schema -O yaml -o gold.linkml.yaml
```

## Key Databases

| Schema Path | Tables | Description |
|-------------|--------|-------------|
| `"gold-db-2 postgresql".gold` | 42 | GOLD - genome project metadata |
| `"img-db-2 postgresql".img_core_v400` | 244 | IMG Core - genes, taxa, annotations |
| `"img-db-2 postgresql".img_ext` | 84 | IMG Extended data |
| `"img-db-2 postgresql".img_sat_v450` | 141 | IMG Satellite/experimental |

See [references/databases.md](references/databases.md) for complete listing.

## Common SQL Patterns

```bash
# List schemas
linkml-store -d "$DB" query --sql 'SELECT TABLE_SCHEMA, COUNT(*) as tables FROM INFORMATION_SCHEMA."TABLES" GROUP BY TABLE_SCHEMA ORDER BY TABLE_SCHEMA'

# List tables in schema
linkml-store -d "$DB" query --sql 'SELECT TABLE_NAME FROM INFORMATION_SCHEMA."TABLES" WHERE TABLE_SCHEMA = '\''gold-db-2 postgresql.gold'\'' ORDER BY TABLE_NAME'

# Table columns
linkml-store -d "$DB" query --sql 'SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA."COLUMNS" WHERE TABLE_SCHEMA = '\''gold-db-2 postgresql.gold'\'' AND TABLE_NAME = '\''study'\'' ORDER BY ORDINAL_POSITION'

# Row count
linkml-store -d "$DB" query --sql 'SELECT COUNT(*) FROM "gold-db-2 postgresql".gold.study'
```

## Pre-generated Schemas

LinkML schemas with FK relationships: `/Users/cjm/repos/linkml-store/jgi-lakehouse-analysis/`
