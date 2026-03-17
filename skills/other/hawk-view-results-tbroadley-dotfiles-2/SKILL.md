---
name: view-results
description: View and analyze Hawk evaluation results. Use when the user wants to see eval-set results, check evaluation status, list samples, view transcripts, or analyze agent behavior from a completed evaluation run.
---

# View Hawk Eval Results

When the user wants to analyze evaluation results, use these hawk CLI commands:

## 1. List Eval Sets

You can list all eval sets if the user do not know the eval set ID:

```bash
hawk list eval-sets
```

Shows: eval set ID, creation date, creator.

You can increase the limit of results returned by `--limit N`.

```bash
hawk list eval-sets --limit 50
```

Or you can search for a specific eval set by using `--search QUERY`.

```bash
hawk list eval-sets --search pico
```

## 2. List Evaluations

With an eval set ID, you can list all evaluations in the eval-set:

```bash
hawk list evals [EVAL_SET_ID]
```

Shows: task name, model, status (success/error/cancelled), and sample counts.

## 3. List Samples

Or you can list individual samples and their scores:

```bash
hawk list samples [EVAL_SET_ID] [--eval FILE] [--limit N]
```

## 4. Download Transcript

To get the full conversation for a specific sample:

```bash
hawk transcript <UUID>
```

The transcript includes full conversation with tool calls, scores, and metadata.

To get even more details, you can get the raw data by using `--raw`:

```bash
hawk transcript <UUID> --raw
```

### Batch Transcript Download

You can also download all transcripts for an entire eval set:

```bash
# Fetch all samples in an eval set
hawk transcripts <EVAL_SET_ID>

# Write to individual files in a directory
hawk transcripts <EVAL_SET_ID> --output-dir ./transcripts

# Limit number of samples
hawk transcripts <EVAL_SET_ID> --limit 10

# Raw JSON output (one JSON per line to stdout, or .json files with --output-dir)
hawk transcripts <EVAL_SET_ID> --raw
```

## Known Limitations

- `hawk list samples` has a max `--limit` of 500 (API returns 422 for higher values)
- `hawk transcript` and `hawk transcripts` time out on large eval files (100MB+), common with side-task evals that have thousands of samples × multiple epochs
- `hawk list samples` does not index score values — the `score_value` field is often `None`

## Prefer the Data Warehouse for Bulk Analysis

For querying sample-level data across eval sets (scores, limits, errors, token counts), use the `warehouse-query` skill instead of downloading eval files from S3 via `inspect_ai.log.read_eval_log()`. The warehouse has `eval`, `sample`, `score`, and `message` tables. A SQL query takes seconds vs minutes/hours for large eval files.

Example — find all samples that hit the working limit:
```sql
SELECT s.id AS sample_id, s.epoch, e.eval_set_id, e.model, e.task_args
FROM sample s
JOIN eval e ON s.eval_pk = e.pk
WHERE e.eval_set_id = 'eval-set-xxx'
  AND s."limit" = 'working';
```

Use `hawk transcript <uuid>` only when you need the full conversation transcript for a specific sample.

## Workflow

1. Run `hawk list eval-sets` to see available eval sets
2a. Run `hawk list evals <EVAL_SET_ID>` to see available evaluations
2b. or run `hawk list samples <EVAL_SET_ID>` to find samples of interest (max 500 per request)
3. For bulk sample-level analysis (scores, limits, errors), use `warehouse-query` skill with SQL
4. Run `hawk transcript <uuid>` only for full conversation details on individual samples

## API Environments

Production (`https://api.inspect-ai.internal.metr.org`) is used by default. Set `HAWK_API_URL` only when targeting non-production environments:

| Environment | URL |
|-------------|-----|
| Staging | `https://api.inspect-ai.staging.metr-dev.org` |
| Dev1 | `https://api.inspect-ai.dev1.staging.metr-dev.org` |
| Dev2 | `https://api.inspect-ai.dev2.staging.metr-dev.org` |
| Dev3 | `https://api.inspect-ai.dev3.staging.metr-dev.org` |
| Dev4 | `https://api.inspect-ai.dev4.staging.metr-dev.org` |

Example:
```bash
HAWK_API_URL=https://api.inspect-ai.staging.metr-dev.org hawk list eval_sets
```
