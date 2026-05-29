---
name: taiga-api
description: Query the hosted Taiga API at taiga.ant.dev for job results, passrates, transcripts, and run evaluations. Use when user asks about Taiga jobs, problem scores, eval results, or needs to submit/check jobs.
---

# Taiga API

Query the hosted Taiga evaluation platform API for job results, transcripts, and problem runs.

## IMPORTANT: Use Python, Not Shell

**Always use Python for Taiga API requests.** Shell has env var + pipe bugs that strip cookie values.

Python helper to load cookie:
```python
def get_cookie():
    with open('/home/atondwal/dmodel/ant/taiga-worktree/.env') as f:
        for line in f:
            if line.startswith('TAIGA_IAP_COOKIE='):
                return line.split('=', 1)[1].strip().strip('"')
```

## IMPORTANT: Always Use Opus 4.5

**When submitting jobs, ALWAYS use `claude-opus-4-5-20251101` as the model. Never use Sonnet or other models unless explicitly requested.**

## Authentication

Cookie stored in `~/dmodel/ant/taiga-worktree/.env`. Uses `__Host-` prefix (session-only). If auth fails, ask user to refresh from browser DevTools → Network → copy Cookie header.

## Making Requests

```python
import urllib.request, json

def taiga_get(endpoint):
    cookie = get_cookie()  # see helper above
    req = urllib.request.Request(f"https://taiga.ant.dev/api{endpoint}")
    req.add_header('Cookie', cookie)
    return json.loads(urllib.request.urlopen(req).read())

# Example: get job problems
data = taiga_get(f"/jobs/{job_id}/problems")
```

## API Reference

Full docs at: `https://taiga.ant.dev/api/docs`

### Jobs (Most Common)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/jobs` | GET | List all jobs |
| `/jobs?environment_id={id}` | GET | List jobs for environment |
| `/jobs/{job_id}` | GET | Get job details |
| `/jobs/{job_id}/problems` | GET | **Get problem results (passrates, scores)** |
| `/jobs/{job_id}/problems/stream` | GET | Stream problem results |
| `/jobs/{job_id}/error-summary` | GET | Get error summary |
| `/jobs` | POST | Create job with problems |
| `/cancel-job/{job_id}` | POST | Cancel running job |
| `/resubmit-problem/{job_id}/{problem_id}` | POST | Resubmit specific problem |

### Transcripts

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/transcript/{problem_run_id}` | GET | Get full transcript |
| `/transcript/stream/{problem_run_id}` | GET | Stream transcript |

### Problem Runs

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/problem_runs/{problem_id}` | GET | List runs for problem |
| `/problem-runs/{id}/container-logs` | GET | Get container logs |
| `/problem-runs/{id}/mcp-server-logs` | GET | Get MCP server logs |
| `/problem-runs/{id}/download-output` | GET | Download output directory |

### Environments

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/environments` | GET | List environments |
| `/environments/{id}` | GET | Get environment details |
| `/environments?skip=0&limit=100` | GET | Paginated list |

### Problems

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/problems/{problem_id}/attempts` | GET | Get problem attempts |
| `/problems/versions/{version_id}` | GET | Get problem version |
| `/problems/versions/{version_id}/run` | POST | Run problem version |
| `/problem-crud` | GET | List all problems |
| `/problem-crud/stats/pass-rates` | POST | Get pass rate stats |

### Docker Images

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/docker-images` | GET | List docker images |
| `/docker-images/{id}/download` | GET | Download image source |

## Common Workflows

### Get Passrates for a Job

```python
job_id = "3c300cca-707a-4e92-ac71-5688165f9ae1"  # from URL ?id= param
data = taiga_get(f"/jobs/{job_id}/problems")
for r in data:
    print(f"{r['problem_id']}: {r['final_score']}")
```

### Aggregate Passrates

```python
from collections import defaultdict

job_id = "YOUR_JOB_ID"
data = taiga_get(f"/jobs/{job_id}/problems")

problems = defaultdict(list)
for r in data:
    problems[r['problem_id']].append(r['final_score'])

total_pass = total_runs = 0
for pid, scores in sorted(problems.items()):
    passed = sum(1 for s in scores if s == 1.0)
    total = len(scores)
    total_pass += passed
    total_runs += total
    print(f"{pid}: {passed}/{total} ({100*passed/total:.0f}%)")

print(f"\nOverall: {total_pass}/{total_runs} ({100*total_pass/total_runs:.1f}%)")
```

### Get Transcript

```python
problem_run_id = "118ed21a-9864-4c8c-b34b-d92428f1c22a"
transcript = taiga_get(f"/transcript/{problem_run_id}")
```

### List Jobs for Environment

```python
env_id = "8e646c11-1461-44a4-9e8d-e3800a02ba07"
jobs = taiga_get(f"/jobs?environment_id={env_id}")
for j in jobs:
    print(f"{j['id']}: {j['status']}")
```

### Check Job Status

```python
job = taiga_get(f"/jobs/{job_id}")
print(f"Status: {job['status']}, Completed: {job.get('completed_count')}")
```

### Create a Job

```python
import urllib.request, json

with open('problems-metadata.json') as f:
    problems = json.load(f)

payload = {
    "name": "my-job-name",
    "problems_metadata": problems,
    "n_attempts_per_problem": 10,
    "api_model_name": "claude-opus-4-5-20251101"  # ALWAYS use Opus 4.5
}

cookie = get_cookie()
req = urllib.request.Request(
    "https://taiga.ant.dev/api/jobs",
    data=json.dumps(payload).encode(),
    headers={"Cookie": cookie, "Content-Type": "application/json"}
)
resp = json.loads(urllib.request.urlopen(req).read())
print(f"Job ID: {resp.get('job_id')}")
```

## Response Schemas

### Problem Run
```json
{
  "id": "118ed21a-...",
  "problem_id": "sort-unique",
  "attempt_number": 1,
  "final_score": 1.0,
  "status": "completed",
  "subscores": {"matched_solution": 1.0},
  "weights": {"matched_solution": 1.0},
  "execution_time_ms": 467000,
  "total_tokens": 34205
}
```

### Job
```json
{
  "id": "3c300cca-...",
  "status": "completed",
  "environment_id": "8e646c11-...",
  "api_model_name": "claude-opus-4-5-20251101",
  "created_at": "2025-11-24T17:46:30Z"
}
```

## URL Patterns

From Taiga web UI URLs:
- Job page: `https://taiga.ant.dev/job?id={job_id}&environmentId={env_id}`
- Transcripts: `https://taiga.ant.dev/transcripts?id={job_id}&problemId={problem_id}&...`

The `id` parameter in URLs is the job_id.

## Tips

1. Use Python with `urllib.request` - avoid shell due to env var bugs
2. Cookie expires periodically - refresh from browser if auth fails
3. `/jobs/{id}/problems` is the main endpoint for checking pass rates
4. For streaming large responses, use the `/stream` variants
