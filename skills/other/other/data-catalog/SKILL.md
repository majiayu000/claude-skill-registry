---
name: data-catalog
cluster: data-engineering
description: "Manages metadata for data assets to enable discovery, governance, and lineage tracking in data engineering."
tags: ["metadata","data-governance","data-discovery"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "data catalog metadata governance discovery engineering"
---

# data-catalog

## Purpose
This skill manages metadata for data assets, enabling discovery, governance, and lineage tracking in data engineering workflows. It catalogs datasets, schemas, and dependencies to support data-driven projects.

## When to Use
Use this skill when you need to track data assets in a project, such as during ETL processes, data governance audits, or when building data pipelines. Apply it in scenarios involving large-scale data repositories, compliance requirements, or collaborative data teams.

## Key Capabilities
- Register and update metadata for datasets using JSON structures, e.g., `{"name": "sales_data", "schema": {"columns": ["id", "date"]}}`.
- Search and query assets via full-text or tag-based filters, supporting lineage queries like tracing data origins.
- Enforce governance policies, such as access controls, by associating tags like "sensitive" to assets.
- Generate lineage graphs in JSON format, e.g., `{"source": "raw_logs", "target": "processed_reports"}`.
- Integrate with storage systems like S3 or databases, using connectors that require API keys via `$DATA_CATALOG_API_KEY`.

## Usage Patterns
To use this skill, first authenticate with an environment variable like `export DATA_CATALOG_API_KEY=your_key`. Then, follow a pattern: initialize the catalog, register assets, query as needed, and handle updates. For pipelines, embed it in scripts to auto-register outputs. Always validate metadata before operations to avoid conflicts.

## Common Commands/API
Use the `dcatalog` CLI or REST API for interactions. Authentication requires `$DATA_CATALOG_API_KEY` in requests.

- **CLI Commands:**
  - Register an asset: `dcatalog register --asset-name sales_data --type dataset --metadata '{"schema": ["id", "amount"]}' --api-key $DATA_CATALOG_API_KEY`
  - Query assets: `dcatalog search --query "sales" --tags metadata --limit 10`
  - Update lineage: `dcatalog update-lineage --source raw_data --target processed_data --relation depends_on`

- **API Endpoints:**
  - POST /api/v1/assets: Create a new asset. Example curl: `curl -H "Authorization: Bearer $DATA_CATALOG_API_KEY" -d '{"name": "sales_data", "tags": ["metadata"]}' -X POST https://api.opencclaw.com/api/v1/assets`
  - GET /api/v1/assets/search?query=sales: Search assets. Example: `curl -H "Authorization: Bearer $DATA_CATALOG_API_KEY" https://api.opencclaw.com/api/v1/assets/search?query=sales`
  - PUT /api/v1/lineage: Update lineage. Code snippet:  
    ```python
    import requests
    headers = {"Authorization": f"Bearer {os.environ['DATA_CATALOG_API_KEY']}"}
    response = requests.put('https://api.opencclaw.com/api/v1/lineage', headers=headers, json={"source": "raw_data", "target": "report"})
    ```

Config formats are JSON-based, e.g., for CLI config file (`~/.dcatalog/config.json`):  
`{"default_tags": ["data-governance"], "api_endpoint": "https://api.opencclaw.com"}`

## Integration Notes
Integrate this skill with data tools like Apache Airflow or AWS Glue by wrapping API calls in custom operators. For example, in a Python script, import the API client and pass `$DATA_CATALOG_API_KEY`. Ensure compatibility by matching schema versions; use JSON configs for mappings, e.g., link to S3 buckets via `{"bucket": "my-bucket", "prefix": "data/"}`. Test integrations in a sandbox environment before production.

## Error Handling
Handle errors by checking HTTP status codes in API responses; for example, if status is 401, prompt for `$DATA_CATALOG_API_KEY` revalidation. For CLI, use try-catch in scripts:  
```python
try:
    subprocess.run(["dcatalog", "register", "--asset-name", "test"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error: {e.returncode} - {e.output}")
```
Common issues include invalid JSON metadata (fix by validating with `json.loads()` before sending) or authentication failures (retry with refreshed keys). Log errors with timestamps for debugging.

## Graph Relationships
- Related Cluster: data-engineering
- Connected Tags: metadata, data-governance, data-discovery
- Dependencies: Often links to skills in storage or processing clusters, e.g., for data ingestion or transformation.
