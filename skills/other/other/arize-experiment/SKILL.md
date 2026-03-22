---
name: arize-experiment
description: "INVOKE THIS SKILL when creating, running, or analyzing Arize experiments. Covers experiment CRUD, exporting runs, comparing results, and evaluation workflows using the ax CLI."
---

# Arize Experiment Skill

## Concepts

- **Experiment** = a named evaluation run against a specific dataset version, containing one run per example
- **Experiment Run** = the result of processing one dataset example -- includes the model output, optional evaluations, and optional metadata
- **Dataset** = a versioned collection of examples; every experiment is tied to a dataset and a specific dataset version
- **Evaluation** = a named metric attached to a run (e.g., `correctness`, `relevance`), with optional label, score, and explanation

The typical flow: export a dataset → process each example → collect outputs and evaluations → create an experiment with the runs.

## Prerequisites

Three things are needed: `ax` CLI, an API key (env var or profile), and a space ID. A project name is also needed but usually comes from the user's message.

### Install ax

If `ax` is not installed, not on PATH, or below version `0.3.0`, see ax-setup.md.

### Verify environment

Run a quick check for credentials:

**macOS/Linux (bash):**
```bash
ax --version && echo "--- env ---" && if [ -n "$ARIZE_API_KEY" ]; then echo "ARIZE_API_KEY: (set)"; else echo "ARIZE_API_KEY: (not set)"; fi && echo "ARIZE_SPACE_ID: ${ARIZE_SPACE_ID:-(not set)}" && echo "--- profiles ---" && ax profiles show 2>&1
```

**Windows (PowerShell):**
```powershell
ax --version; Write-Host "--- env ---"; Write-Host "ARIZE_API_KEY: $(if ($env:ARIZE_API_KEY) { '(set)' } else { '(not set)' })"; Write-Host "ARIZE_SPACE_ID: $env:ARIZE_SPACE_ID"; Write-Host "--- profiles ---"; ax profiles show 2>&1
```

**Read the output and proceed immediately** if either the env var or the profile has an API key. Only ask the user if **both** are missing. Resolve failures:

- No API key in env **and** no profile → **AskQuestion**: "Arize API key (https://app.arize.com/admin > API Keys)"
- Space ID unknown → run `ax spaces list -o json` to list all accessible spaces and pick the right one, or **AskQuestion** if the user prefers to provide it directly
- Project unclear → ask, or run `ax projects list -o json --limit 100` and present as selectable options

### Space ID and Project

Both are needed for most commands. Resolve each:

1. User provides it in the conversation -- note that space ID and project are resolved via the API key profile, not CLI flags.
2. Env var is set (`ARIZE_SPACE_ID`, `ARIZE_DEFAULT_PROJECT`) -- use silently.
3. If missing, **AskQuestion** once. Tell the user:
   - Run `ax spaces list -o json` to discover your space ID, or find it in the Arize URL: `/spaces/{SPACE_ID}/...`
   - Project is the project name as shown in the Arize UI.
   - For convenience, recommend setting env vars so they don't get asked again:
     `export ARIZE_SPACE_ID="U3BhY2U6..."` and `export ARIZE_DEFAULT_PROJECT="my-project"`

Prefer asking the user over searching or iterating through projects and API keys.
If you get a `401 Unauthorized`, tell the user their API key may not have access to
that space and ask them to verify.

## List Experiments: `ax experiments list`

Browse experiments, optionally filtered by dataset. Output goes to stdout.

```bash
ax experiments list
ax experiments list --dataset-id DATASET_ID --limit 20
ax experiments list --cursor CURSOR_TOKEN
ax experiments list -o json
```

### Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--dataset-id` | string | none | Filter by dataset |
| `--limit, -l` | int | 15 | Max results (1-100) |
| `--cursor` | string | none | Pagination cursor from previous response |
| `-o, --output` | string | table | Output format: table, json, csv, parquet, or file path |
| `-p, --profile` | string | default | Configuration profile |

## Get Experiment: `ax experiments get`

Quick metadata lookup -- returns experiment name, linked dataset/version, and timestamps.

```bash
ax experiments get EXPERIMENT_ID
ax experiments get EXPERIMENT_ID -o json
```

### Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `EXPERIMENT_ID` | string | required | Positional argument |
| `-o, --output` | string | table | Output format |
| `-p, --profile` | string | default | Configuration profile |

### Response fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Experiment ID |
| `name` | string | Experiment name |
| `dataset_id` | string | Linked dataset ID |
| `dataset_version_id` | string | Specific dataset version used |
| `experiment_traces_project_id` | string | Project where experiment traces are stored |
| `created_at` | datetime | When the experiment was created |
| `updated_at` | datetime | Last modification time |

## Export Experiment: `ax experiments export`

Download all runs to a file. By default uses the REST API; pass `--all` to use Arrow Flight for bulk transfer.

```bash
ax experiments export EXPERIMENT_ID
# -> experiment_abc123_20260305_141500/runs.json

ax experiments export EXPERIMENT_ID --all
ax experiments export EXPERIMENT_ID --output-dir ./results
ax experiments export EXPERIMENT_ID --stdout
ax experiments export EXPERIMENT_ID --stdout | jq '.[0]'
```

### Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `EXPERIMENT_ID` | string | required | Positional argument |
| `--all` | bool | false | Use Arrow Flight for bulk export (see below) |
| `--output-dir` | string | `.` | Output directory |
| `--stdout` | bool | false | Print JSON to stdout instead of file |
| `-p, --profile` | string | default | Configuration profile |

### REST vs Flight (`--all`)

- **REST** (default): Lower friction -- no Arrow/Flight dependency, standard HTTPS ports, works through any corporate proxy or firewall. Limited to 500 runs per page.
- **Flight** (`--all`): Required for experiments with more than 500 runs. Uses gRPC+TLS on a separate host/port (`flight.arize.com:443`) which some corporate networks may block.

**Agent auto-escalation rule:** If a REST export returns exactly 500 runs, the result is likely truncated. Re-run with `--all` to get the full dataset.

Output is a JSON array of run objects:

```json
[
  {
    "id": "run_001",
    "example_id": "ex_001",
    "output": "The answer is 4.",
    "evaluations": {
      "correctness": { "label": "correct", "score": 1.0 },
      "relevance": { "score": 0.95, "explanation": "Directly answers the question" }
    },
    "metadata": { "model": "gpt-4o", "latency_ms": 1234 }
  }
]
```

## Create Experiment: `ax experiments create`

Create a new experiment with runs from a data file.

```bash
ax experiments create --name "gpt-4o-baseline" --dataset-id DATASET_ID --file runs.json
ax experiments create --name "claude-test" --dataset-id DATASET_ID --file runs.csv
```

### Flags

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--name, -n` | string | yes | Experiment name |
| `--dataset-id` | string | yes | Dataset to run the experiment against |
| `--file, -f` | path | yes | Data file with runs: CSV, JSON, JSONL, or Parquet |
| `-o, --output` | string | no | Output format |
| `-p, --profile` | string | no | Configuration profile |

### Required columns in the runs file

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| `example_id` | string | yes | ID of the dataset example this run corresponds to |
| `output` | string | yes | The model/system output for this example |

Additional columns are passed through as `additionalProperties` on the run.

## Delete Experiment: `ax experiments delete`

```bash
ax experiments delete EXPERIMENT_ID
ax experiments delete EXPERIMENT_ID --force   # skip confirmation prompt
```

### Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `EXPERIMENT_ID` | string | required | Positional argument |
| `--force, -f` | bool | false | Skip confirmation prompt |
| `-p, --profile` | string | default | Configuration profile |

## Experiment Run Schema

Each run corresponds to one dataset example:

```json
{
  "example_id": "required -- links to dataset example",
  "output": "required -- the model/system output for this example",
  "evaluations": {
    "metric_name": {
      "label": "optional string label (e.g., 'correct', 'incorrect')",
      "score": "optional numeric score (e.g., 0.95)",
      "explanation": "optional freeform text"
    }
  },
  "metadata": {
    "model": "gpt-4o",
    "temperature": 0.7,
    "latency_ms": 1234
  }
}
```

### Evaluation fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `label` | string | no | Categorical classification (e.g., `correct`, `incorrect`, `partial`) |
| `score` | number | no | Numeric quality score (e.g., 0.0 - 1.0) |
| `explanation` | string | no | Freeform reasoning for the evaluation |

At least one of `label`, `score`, or `explanation` should be present per evaluation.

## Workflows

### Run an experiment against a dataset

1. Find or create a dataset:
   ```bash
   ax datasets list
   ax datasets export DATASET_ID --stdout | jq 'length'
   ```
2. Export the dataset examples:
   ```bash
   ax datasets export DATASET_ID
   ```
3. Process each example through your system, collecting outputs and evaluations
4. Build a runs file (JSON array) with `example_id`, `output`, and optional `evaluations`:
   ```json
   [
     {"example_id": "ex_001", "output": "4", "evaluations": {"correctness": {"label": "correct", "score": 1.0}}},
     {"example_id": "ex_002", "output": "Paris", "evaluations": {"correctness": {"label": "correct", "score": 1.0}}}
   ]
   ```
5. Create the experiment:
   ```bash
   ax experiments create --name "gpt-4o-baseline" --dataset-id DATASET_ID --file runs.json
   ```
6. Verify: `ax experiments get EXPERIMENT_ID`

### Compare two experiments

1. Export both experiments:
   ```bash
   ax experiments export EXPERIMENT_ID_A --stdout > a.json
   ax experiments export EXPERIMENT_ID_B --stdout > b.json
   ```
2. Compare evaluation scores by `example_id`:
   ```bash
   # Average correctness score for experiment A
   jq '[.[] | .evaluations.correctness.score] | add / length' a.json

   # Same for experiment B
   jq '[.[] | .evaluations.correctness.score] | add / length' b.json
   ```
3. Find examples where results differ:
   ```bash
   jq -s '.[0] as $a | .[1][] | . as $run |
     {
       example_id: $run.example_id,
       b_score: $run.evaluations.correctness.score,
       a_score: ($a[] | select(.example_id == $run.example_id) | .evaluations.correctness.score)
     }' a.json b.json
   ```
4. Score distribution per evaluator (pass/fail/partial counts):
   ```bash
   # Count by label for experiment A
   jq '[.[] | .evaluations.correctness.label] | group_by(.) | map({label: .[0], count: length})' a.json
   ```
5. Find regressions (examples that passed in A but fail in B):
   ```bash
   jq -s '
     [.[0][] | select(.evaluations.correctness.label == "correct")] as $passed_a |
     [.[1][] | select(.evaluations.correctness.label != "correct") |
       select(.example_id as $id | $passed_a | any(.example_id == $id))
     ]
   ' a.json b.json
   ```

**Statistical significance note:** Score comparisons are most reliable with ≥ 30 examples per evaluator. With fewer examples, treat the delta as directional only — a 5% difference on n=10 may be noise. Report sample size alongside scores: `jq 'length' a.json`.

### Download experiment results for analysis

1. `ax experiments list --dataset-id DATASET_ID` -- find experiments
2. `ax experiments export EXPERIMENT_ID` -- download to file
3. Parse: `jq '.[] | {example_id, score: .evaluations.correctness.score}' experiment_*/runs.json`

### Pipe export to other tools

```bash
# Count runs
ax experiments export EXPERIMENT_ID --stdout | jq 'length'

# Extract all outputs
ax experiments export EXPERIMENT_ID --stdout | jq '.[].output'

# Get runs with low scores
ax experiments export EXPERIMENT_ID --stdout | jq '[.[] | select(.evaluations.correctness.score < 0.5)]'

# Convert to CSV
ax experiments export EXPERIMENT_ID --stdout | jq -r '.[] | [.example_id, .output, .evaluations.correctness.score] | @csv'
```

## Related Skills

- **arize-dataset**: Create or export the dataset this experiment runs against → use `arize-dataset` first
- **arize-prompt-optimization**: Use experiment results to improve prompts → next step is `arize-prompt-optimization`
- **arize-trace**: Inspect individual span traces for failing experiment runs → use `arize-trace`
- **arize-link**: Generate clickable UI links to traces from experiment runs → use `arize-link`

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ax: command not found` | See ax-setup.md |
| `401 Unauthorized` | API key may not have access to this space. Verify the key and space ID are correct. Keys are scoped per space -- get the right one from https://app.arize.com/admin > API Keys. |
| `No profile found` | Run `ax profiles show --expand` to check; set `ARIZE_API_KEY` env var or write `~/.arize/config.toml` |
| `Experiment not found` | Verify experiment ID with `ax experiments list` |
| `Invalid runs file` | Each run must have `example_id` and `output` fields |
| `example_id mismatch` | Ensure `example_id` values match IDs from the dataset (export dataset to verify) |
| `No runs found` | Export returned empty -- verify experiment has runs via `ax experiments get` |
| `Dataset not found` | The linked dataset may have been deleted; check with `ax datasets list` |

## Save Credentials for Future Use

At the **end of the session**, if the user manually provided any of the following during this conversation (via AskQuestion response, pasted text, or inline values) **and** those values were NOT already loaded from a saved profile or environment variable, offer to save them for future use.

| Credential | Where it gets saved |
|------------|---------------------|
| API key | `ax` profile at `~/.arize/config.toml` |
| Space ID | **macOS/Linux:** shell config (`~/.zshrc` or `~/.bashrc`) as `export ARIZE_SPACE_ID="..."`. **Windows:** user environment variable via `[System.Environment]::SetEnvironmentVariable('ARIZE_SPACE_ID', '...', 'User')` |

**Skip this entirely if:**
- The API key was already loaded from an existing profile or `ARIZE_API_KEY` env var
- The space ID was already set via `ARIZE_SPACE_ID` env var
- The user only used base64 project IDs (no space ID was needed)

**How to offer:** Use **AskQuestion**: *"Would you like to save your Arize credentials so you don't have to enter them next time?"* with options `"Yes, save them"` / `"No thanks"`.

**If the user says yes:**

1. **API key** — Check if `~/.arize/config.toml` exists. If it does, read it and update the `[auth]` section. If not, create it with this minimal content:

   ```toml
   [profile]
   name = "default"

   [auth]
   api_key = "THE_API_KEY"

   [output]
   format = "table"
   ```

   Verify with: `ax profiles show`

2. **Space ID** — Persist the space ID as an environment variable:

   **macOS/Linux** — Detect the user's shell config file (`~/.zshrc` for zsh, `~/.bashrc` for bash). Append:

   ```bash
   export ARIZE_SPACE_ID="THE_SPACE_ID"
   ```

   Tell the user to run `source ~/.zshrc` (or restart their terminal) for it to take effect.

   **Windows (PowerShell)** — Set a persistent user environment variable:

   ```powershell
   [System.Environment]::SetEnvironmentVariable('ARIZE_SPACE_ID', 'THE_SPACE_ID', 'User')
   ```

   Tell the user to restart their terminal for it to take effect.
