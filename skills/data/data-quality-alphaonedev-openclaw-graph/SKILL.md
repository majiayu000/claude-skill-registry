---
name: data-quality
cluster: data-engineering
description: "Ensures data accuracy, completeness, and consistency via validation, cleaning, and monitoring in data pipelines."
tags: ["data-validation","quality-assurance","data-monitoring"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "data quality validation cleaning monitoring engineering"
---

# data-quality

## Purpose
This skill ensures data accuracy, completeness, and consistency in pipelines by performing validation, cleaning, and monitoring. It integrates with data engineering workflows to catch issues early, using tools like rule-based checks and automated alerts.

## When to Use
Use this skill when building or maintaining data pipelines that handle large datasets, such as ETL processes, to prevent downstream errors. Apply it for compliance checks in regulated industries or when integrating new data sources that might introduce inconsistencies. Avoid it for simple data tasks without validation needs.

## Key Capabilities
- Validate data schemas and values using predefined rules (e.g., check for nulls, duplicates, or type mismatches).
- Clean datasets by applying transformations like trimming strings or imputing missing values.
- Monitor pipelines in real-time with metrics and alerts for anomalies.
- Support for various data formats (CSV, JSON, Parquet) and integration with storage systems like S3 or databases.
- Generate reports or logs for auditing, including summary statistics and error counts.

## Usage Patterns
Invoke this skill via CLI for quick checks or integrate it into Python scripts for automated pipelines. Always load configuration files first, then run validations. For monitoring, set up recurring jobs. Example pattern: Load data, apply validation, clean if needed, and monitor outputs.

## Common Commands/API
Use the OpenClaw CLI for direct execution or the REST API for programmatic access. Authentication requires setting the environment variable `$OPENCLAW_API_KEY` before running commands.

- CLI Command: Validate a file with rules  
  `openclaw data-quality validate --file data.csv --rules config.json --output report.txt`  
  This checks data against rules in config.json and saves results to report.txt.

- CLI Command: Clean and monitor data  
  `openclaw data-quality clean --input data.parquet --rules clean_rules.json --monitor`  
  Applies cleaning rules and enables monitoring for ongoing checks.

- API Endpoint: POST /api/data-quality/validate  
  Send a JSON body like:  
  `{ "file_url": "s3://bucket/data.csv", "rules": { "columns": ["id", "name"], "checks": ["no_nulls"] } }`  
  Response: JSON with status and errors, e.g., `{ "status": "success", "errors": [] }`.

- API Endpoint: GET /api/data-quality/monitor/{job_id}  
  Fetch monitoring status:  
  `curl -H "Authorization: Bearer $OPENCLAW_API_KEY" https://api.openclaw.ai/api/data-quality/monitor/12345`  
  Returns metrics like error rate.

Config format: Use JSON for rules, e.g.,  
`{ "checks": [ { "type": "null_check", "column": "age", "action": "alert" } ] }`

## Integration Notes
Integrate with Python using the OpenClaw SDK: Import and initialize with your API key. For example, in a data pipeline:  
`import openclaw`  
`client = openclaw.Client(api_key=os.environ['OPENCLAW_API_KEY'])`  
`result = client.validate_data(file_path='data.csv', rules={'checks': ['duplicates']})`  
Ensure data pipelines handle asynchronous API calls by checking response status codes. For cloud integration, configure webhooks for alerts, e.g., POST to your endpoint on validation failures. Always test integrations in a staging environment first.

## Error Handling
Handle errors by checking return codes from CLI or API responses. For CLI, if a command fails, it exits with a non-zero code; parse stderr for details. In code, catch exceptions like:  
`try:`  
`    result = client.validate_data(...)`  
`except openclaw.APIError as e:`  
`    log_error(e.message)  # e.message contains error details`  
Common errors include authentication failures (e.g., 401 Unauthorized) or invalid configs (e.g., 400 Bad Request). Use retry logic for transient issues, like network errors, with exponential backoff.

## Graph Relationships
- Related to: data-processing (for pipeline integration), data-monitoring (for shared alerting features)
- Depends on: data-storage (for accessing data sources)
- Complements: machine-learning (for data prep in ML workflows)
