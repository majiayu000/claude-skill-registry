---
name: bip.scout
description: Check remote server CPU, memory, and GPU availability via SSH
---

# /bip.scout

Check remote server availability and resource usage. Runs `bip scout` to collect metrics, presents a human-readable summary, and answers follow-up questions by reasoning over the data.

## Usage

```
/bip.scout [question]
```

**Arguments:**
- `[question]` — Optional natural-language question (e.g., "which server has free GPUs?", "where should I run a training job?")

If no question is given, show a full summary of all servers.

## Workflow

### Step 1: Collect Server Metrics

Run `bip scout` from the nexus directory to get JSON output:

```bash
bip scout
```

**If the command fails**, check for common issues:
- Missing `servers.yml`: "No servers.yml found. Create one in your nexus directory — see `bip scout --help`."
- SSH authentication failure: Report the error and suggest checking SSH agent and `~/.ssh/config`.
- All servers offline: Report that all servers are unreachable and suggest checking network/VPN.

### Step 2: Parse JSON Output

The JSON output has this structure:

```json
{
  "servers": [
    {
      "name": "servername",
      "status": "online",
      "metrics": {
        "cpu_percent": 45.2,
        "memory_percent": 62.1,
        "load_avg_1min": 2.3,
        "load_avg_5min": 1.8,
        "load_avg_15min": 1.5,
        "gpus": [
          {
            "utilization_percent": 85,
            "memory_used_mb": 30720,
            "memory_total_mb": 49152
          }
        ],
        "top_users": [
          {"user": "alice", "cpu_percent": 45.2},
          {"user": "bob", "cpu_percent": 12.1}
        ]
      }
    },
    {
      "name": "deadserver",
      "status": "offline",
      "error": "connection timed out"
    }
  ]
}
```

### Step 3: Present Results

**If no question was asked**, present a summary table showing:
- All servers grouped by status (online first, offline last)
- For online servers: CPU%, Memory%, per-GPU utilization and memory
- For offline servers: note them as unreachable
- Highlight servers with low utilization (CPU < 20%, no busy GPUs) as good candidates

**If a question was asked**, reason over the JSON data to answer it. Common question types:

| Question Type | How to Answer |
|---------------|---------------|
| "Which server has free GPUs?" | Find online servers where GPU utilization < 50% and GPU memory has headroom |
| "Where should I run a training job?" | Find servers with lowest GPU utilization and most free GPU memory |
| "Is server X available?" | Check that specific server's status and metrics |
| "What's the GPU memory on Y?" | Report per-GPU memory used/total for that server |
| "Which servers are idle?" | Find servers with CPU < 20% and memory < 50% |
| "Who is using server X?" | Report top_users with their CPU percentages |

**Formatting guidelines:**
- Use a markdown table for multi-server summaries
- Convert GPU memory from MB to GB for readability (divide by 1024)
- Show percentages with one decimal place
- For GPU-focused questions, show per-GPU breakdown (not just averages)

### Step 4: Offer Follow-Up

After presenting results, briefly note that the user can ask follow-up questions like:
- "Which of these has the most free GPU memory?"
- "Run my job on the least-loaded GPU server"

## Error Handling

- **bip not found**: Report error, suggest building with `go build -o bip ./cmd/bip`
- **servers.yml missing**: Report error, suggest creating config file
- **SSH failures**: Report which servers failed and why
- **No GPU servers**: Note that no servers are configured with `has_gpu: true`
