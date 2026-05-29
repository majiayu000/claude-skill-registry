---
name: read-inspect-eval
description: Read and analyze Inspect AI evaluation log files using the Python API. Extract samples, messages, events, and metrics from .eval files.
---

# Read Inspect AI Evaluation Files

This skill provides instructions for reading and analyzing Inspect AI evaluation log files using the Python API.

## When to Use

Use this skill when the user needs to:
- Read evaluation results from `.eval` log files
- Extract samples, messages, or events from evaluations
- Analyze model performance metrics and scores
- Convert eval data to dataframes for analysis
- Debug evaluation failures or errors
- Access specific samples by task or epoch

## Prerequisites

Requires the `inspect_ai` package:
```bash
pip install inspect-ai
```

## Core Functions

The `inspect_ai.log` module provides these primary functions:

| Function | Purpose |
|----------|---------|
| `list_eval_logs()` | List all eval logs at a location |
| `read_eval_log()` | Read an EvalLog from a file path |
| `read_eval_log_sample()` | Retrieve a single EvalSample |
| `read_eval_log_samples()` | Read all samples incrementally (generator) |
| `read_eval_log_sample_summaries()` | Access summary-level info for all samples |

## Reading Eval Logs

### Basic Usage

```python
from inspect_ai import log

# List available logs
logs = log.list_eval_logs("./logs")

# Read a specific log
eval_log = log.read_eval_log("path/to/file.eval")

# Check status
print(f"Status: {eval_log.status}")  # "success", "error", or "started"
print(f"Results: {eval_log.results}")
```

### Read Options

```python
# Read only header/metadata (fast, no sample data)
eval_log = log.read_eval_log("file.eval", header_only=True)

# Resolve de-duplicated attachments
eval_log = log.read_eval_log("file.eval", resolve_attachments=True)

# Require successful completion
eval_log = log.read_eval_log("file.eval", all_samples_required=True)
```

### Iterating Samples

For large files, iterate samples without loading all into memory:

```python
from inspect_ai import log

# Read samples as generator (memory efficient)
for sample in log.read_eval_log_samples("file.eval"):
    print(f"Sample {sample.id}: {sample.scores}")

# Or get summaries only (even faster)
for summary in log.read_eval_log_sample_summaries("file.eval"):
    print(f"Sample {summary.id}: score={summary.scores}")
```

## EvalLog Structure

The `EvalLog` object contains:

```python
eval_log.status      # "success", "error", "started"
eval_log.samples     # List[EvalSample] - individual evaluations
eval_log.results     # Aggregate metrics
eval_log.stats       # Token usage data
eval_log.error       # Exception details if failed
eval_log.eval        # Eval configuration (task, model, etc.)
```

### EvalSample Structure

Each sample contains:

```python
sample.id            # Sample identifier
sample.epoch         # Epoch number
sample.input         # Input to the model
sample.target        # Expected target
sample.output        # Model output
sample.scores        # Dict of scorer results
sample.messages      # List of conversation messages
sample.metadata      # Custom metadata
sample.error         # Error if sample failed
```

## Dataframe API

The `inspect_ai.analysis` module provides functions to extract dataframes:

### Evaluation-Level Data

```python
from inspect_ai import analysis

# One row per eval log
df = analysis.evals_df("./logs")

# Custom columns
df = analysis.evals_df("./logs", columns=analysis.EvalInfo + analysis.EvalResults)
```

### Sample-Level Data

```python
# One row per sample (summary info - fast)
df = analysis.samples_df("./logs")

# Full sample data (slower, use parallel)
df = analysis.samples_df("./logs", full=True, parallel=True)
```

### Message-Level Data

```python
# One row per message
df = analysis.messages_df("./logs", parallel=True)

# Filter by role
df = analysis.messages_df("./logs", filter=["assistant"], parallel=True)
```

### Event-Level Data

```python
# One row per event (model calls, tool use, etc.)
df = analysis.events_df(
    "logs",
    columns=analysis.EventTiming + analysis.ModelEventColumns,
    filter=lambda e: e.event == "model",
    parallel=True
)
```

### Column Groups

Pre-defined column groups for `evals_df`:
- `EvalInfo` - Metadata (created, tags, git commit)
- `EvalTask` - Task configuration
- `EvalModel` - Model details
- `EvalResults` - Status, errors, headline metrics
- `EvalScores` - All scores as separate columns

Pre-defined column groups for `samples_df`:
- `SampleSummary` - Default lightweight columns
- `SampleScores` - Score details (answer, metadata, explanation)
- `SampleMessages` - Message content as strings

## Common Workflows

### Analyze Evaluation Results

```python
from inspect_ai import log, analysis

# Load eval
eval_log = log.read_eval_log("results.eval")

if eval_log.status == "success":
    print(f"Total samples: {len(eval_log.samples)}")
    print(f"Results: {eval_log.results}")

    # Accuracy by task
    df = analysis.samples_df([eval_log])
    print(df.groupby("task")["score"].mean())
```

### Extract Conversation Messages

```python
from inspect_ai import log

for sample in log.read_eval_log_samples("results.eval"):
    print(f"\n=== Sample {sample.id} ===")
    for msg in sample.messages:
        role = msg.role
        content = msg.content if isinstance(msg.content, str) else str(msg.content)
        print(f"{role}: {content[:200]}...")
```

### Find Failed Samples

```python
from inspect_ai import log

for sample in log.read_eval_log_samples("results.eval"):
    if sample.error:
        print(f"Sample {sample.id} failed: {sample.error}")
```

### Compare Model Performance

```python
from inspect_ai import analysis

df = analysis.evals_df("./logs")
print(df.groupby("model")["accuracy"].mean().sort_values(ascending=False))
```

### Export to CSV

```python
from inspect_ai import analysis

samples = analysis.samples_df("./logs", parallel=True)
samples.to_csv("samples.csv", index=False)

evals = analysis.evals_df("./logs")
evals.to_csv("evals.csv", index=False)
```

## Working with Downloaded .eval Files

If you downloaded an `.eval` file using the `download-inspect-eval` skill, use the standard `inspect_ai` functions:

```python
from inspect_ai import log

# Read the downloaded file directly
eval_log = log.read_eval_log("2025-12-17T05-42-03+00-00_debug_xyz.eval")

# Iterate samples
for sample in log.read_eval_log_samples("file.eval"):
    print(sample.id, sample.scores)
```

As a last resort, you can manually extract the archive (`.eval` files are zip archives):

```python
import zipfile
with zipfile.ZipFile("file.eval", "r") as z:
    z.extractall("extracted")

# Read sample JSON directly
import json
with open("extracted/samples/task_epoch_1.json") as f:
    sample_data = json.load(f)
```

## Error Handling

```python
from inspect_ai import log, analysis

# Handle missing fields gracefully
df, errors = analysis.evals_df("./logs", strict=False)
if errors:
    print(f"Errors: {errors}")

# Check log status before processing
eval_log = log.read_eval_log("file.eval")
if eval_log.status == "error":
    print(f"Evaluation failed: {eval_log.error}")
elif eval_log.status == "started":
    print("Evaluation incomplete")
```

## Performance Tips

1. **Use `header_only=True`** when you only need metadata
2. **Use `read_eval_log_samples()`** generator for large files
3. **Use `SampleSummary`** columns (default) for fast `samples_df()`
4. **Use `parallel=True`** for full sample/message/event extraction
5. **Filter early** in `messages_df()` and `events_df()` to reduce data

## Reference

- [Eval Logs Documentation](https://inspect.aisi.org.uk/eval-logs.html)
- [Dataframe API Documentation](https://inspect.aisi.org.uk/dataframe.html)
