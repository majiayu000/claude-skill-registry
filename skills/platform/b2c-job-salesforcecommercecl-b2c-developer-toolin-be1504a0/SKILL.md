---
name: b2c-job
description: Using the b2c CLI to run and monitor existing jobs, import/export site archives (IMPEX). Use this for executing jobs, not creating new job step code.
keywords: [run job, execute job, import data, export data, site archive, IMPEX, job status, job log]
---

# B2C Job Skill

Use the `b2c` CLI plugin to **run existing jobs** and import/export site archives on Salesforce B2C Commerce instances.

> **Creating a new job?** If you need to write custom job step code (batch processing, scheduled tasks, data sync), use the `b2c:b2c-custom-job-steps` skill instead.

## Examples

### Run a Job

```bash
# run a job and return immediately
b2c job run my-custom-job

# run a job and wait for completion
b2c job run my-custom-job --wait

# run a job with a timeout (in seconds)
b2c job run my-custom-job --wait --timeout 600

# run a job with parameters (standard jobs)
b2c job run my-custom-job -P "SiteScope={\"all_storefront_sites\":true}" -P OtherParam=value

# show job log if the job fails
b2c job run my-custom-job --wait --show-log
```

### Run System Jobs with Custom Request Bodies

Some system jobs (like search indexing) use non-standard request schemas. Use `--body` to provide a raw JSON request body:

```bash
# run search index job for specific sites
b2c job run sfcc-search-index-product-full-update --wait --body '{"site_scope":["RefArch","SiteGenesis"]}'

# run search index job for a single site
b2c job run sfcc-search-index-product-full-update --wait --body '{"site_scope":["RefArch"]}'
```

Note: `--body` and `-P` are mutually exclusive.

### Import Site Archives

The `job import` command automatically waits for the import job to complete before returning. It does not use the `--wait` option.

```bash
# import a local directory as a site archive
b2c job import ./my-site-data

# import a local zip file
b2c job import ./export.zip

# keep the archive on the instance after import
b2c job import ./my-site-data --keep-archive

# import an archive that already exists on the instance (in Impex/src/instance/)
b2c job import existing-archive.zip --remote

# show job log on failure
b2c job import ./my-site-data --show-log
```

### Export Site Archives

```bash
# export site data using the job export command
b2c job export
```

### Search Job Executions

```bash
# search for job executions
b2c job search

# search with JSON output
b2c job search --json
```

### Wait for Job Completion

```bash
# wait for a specific job execution to complete
b2c job wait <execution-id>
```

### More Commands

See `b2c job --help` for a full list of available commands and options in the `job` topic.

## Related Skills

- `b2c:b2c-custom-job-steps` - For **creating** new custom job steps (batch processing scripts, scheduled tasks, data sync jobs)
- `b2c-cli:b2c-site-import-export` - For site archive structure and metadata XML patterns
