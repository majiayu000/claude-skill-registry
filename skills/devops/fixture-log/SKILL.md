---
name: fixture-log
description: Retrieves agent log files from GKE and saves them as fixtures for the monitor UI. Use when the user says "save fixture", "fixture-log", "download agent log", "save agent log to fixtures", or "grab the logs".
allowed-tools: Bash
argument-hint: <session-id | #issue-number> [--all]
---

# fixture-log

## Purpose

You retrieve agent log files from GKE jobs in the `fenrir-agents` namespace and save them as JSONL fixtures for the monitor UI development environment.

## Arguments

You will receive one of the following via `$ARGUMENTS`:

| Arg | Description |
|-----|-------------|
| `<session-id>` | Full session ID, e.g. `issue-783-step1-firemandecko-4d31c13c` |
| `#N` | Issue number -- looks up the latest job(s) for that issue |
| `--all` | Save logs for ALL running/completed agent jobs |

## Workflow

When invoked, follow these steps exactly:

### 1. Determine the repo root

```bash
REPO_ROOT=$(git -C /Users/declanshanaghy/src/github.com/declanshanaghy/fenrir-ledger rev-parse --show-toplevel)
```

Ensure the fixtures directory exists:

```bash
mkdir -p "$REPO_ROOT/development/odins-throne/fixtures"
```

### 2. Resolve session IDs

**If given a direct session ID** (e.g. `issue-783-step1-firemandecko-4d31c13c`):
- Use it directly. The k8s job name is `agent-<SESSION_ID>`.

**If given `#N`** (issue number):
- Find matching jobs by label first:
  ```bash
  kubectl get jobs -n fenrir-agents -l fenrir.dev/issue=N -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}'
  ```
- If that returns nothing, fall back to name matching:
  ```bash
  kubectl get jobs -n fenrir-agents -o name | grep "issue-N-"
  ```
- Process ALL matching jobs (there may be multiple steps for one issue).

**If given `--all`**:
- List all agent jobs:
  ```bash
  kubectl get jobs -n fenrir-agents -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}'
  ```
- Process each one using the download flow below.

### 3. Download each job's logs (temp-then-verify-then-copy)

For each job name (e.g. `agent-issue-783-step1-firemandecko-4d31c13c`):

Extract the session ID by stripping the `agent-` prefix from the job name.

```bash
SESSION_ID="<extracted-session-id>"
JOB_NAME="agent-${SESSION_ID}"
TEMP_FILE="/tmp/agent-${SESSION_ID}.jsonl"
DEST_FILE="$REPO_ROOT/development/odins-throne/fixtures/agent-${SESSION_ID}.jsonl"

# Step A: Download to temp
kubectl logs "job/${JOB_NAME}" -n fenrir-agents > "$TEMP_FILE" 2>&1

# Step B: Check for server errors in the output
if grep -q "Error from server" "$TEMP_FILE"; then
  echo "FAIL: ${JOB_NAME} -- kubectl returned a server error"
  cat "$TEMP_FILE"
  rm -f "$TEMP_FILE"
  # Continue to next job if processing multiple, otherwise stop
  continue 2>/dev/null || exit 1
fi

# Step C: Verify content exists (at least 1 line of real content)
LINES=$(wc -l < "$TEMP_FILE" | tr -d ' ')
if [ "$LINES" -lt 1 ]; then
  echo "FAIL: ${JOB_NAME} -- downloaded log is empty (pod may have been cleaned up)"
  rm -f "$TEMP_FILE"
  continue 2>/dev/null || exit 1
fi

# Step D: Copy to fixtures (overwrites existing -- fresher logs are always better)
cp "$TEMP_FILE" "$DEST_FILE"
SIZE=$(wc -c < "$DEST_FILE" | tr -d ' ')

echo "OK: ${LINES} lines, ${SIZE} bytes -> development/odins-throne/fixtures/agent-${SESSION_ID}.jsonl"
```

### 4. Clean up temp files

Remove any temp files that were successfully copied:

```bash
rm -f /tmp/agent-*.jsonl
```

## Error Handling Rules

Follow these rules strictly:

1. **NEVER write an empty or error file to fixtures.** Always download to `/tmp` first and verify.
2. If `kubectl logs` fails (pod not found, logs evicted), report the error clearly and skip that job.
3. If the temp file is empty (0 lines), delete it and report failure.
4. If the temp file contains "Error from server", treat it as failure -- do NOT copy to fixtures.
5. If processing multiple jobs (`#N` or `--all`), continue to the next job on failure rather than stopping entirely.
6. Always report the final tally: how many succeeded, how many failed.

## Report

After processing all jobs, report a summary:

```
=== fixture-log results ===
Saved:  N fixture(s)
Failed: M job(s)

Fixtures written:
  - development/odins-throne/fixtures/agent-<id1>.jsonl (123 lines, 45.2 KB)
  - development/odins-throne/fixtures/agent-<id2>.jsonl (456 lines, 128.7 KB)

Failures:
  - agent-<id3>: pod not found (logs evicted)
```

If all jobs succeeded, omit the Failures section. If all failed, omit the Fixtures section.
