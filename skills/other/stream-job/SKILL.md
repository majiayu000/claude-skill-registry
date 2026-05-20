---
name: stream-job
description: "Stream agent logs for a GKE job. Accepts issue #, PR #, session ID, or job name — figures out which agent job to tail. Use when the user says 'stream job', 'show logs', 'tail agent', 'watch job', or provides a number/ID to monitor."
---

# stream-job — Smart Agent Log Streamer

Accepts any identifier and resolves it to a GKE agent job, then streams the parsed logs
in a tmux pane (right column, stacked).

## Usage

```
/stream-job 714              # Issue number — finds latest job for that issue
/stream-job #714             # Same, with hash
/stream-job PR:760           # PR number — finds the issue linked to the PR, then the job
/stream-job issue-714-step1-firemandecko-3a19c027   # Session ID — direct
/stream-job --all            # All active jobs
```

## Resolution Logic

The skill resolves the input to a GKE job name using this cascade:

### 1. Parse the input

Strip `#` prefix, `PR:` prefix, GitHub URLs. Determine what we have:

| Input pattern | Type |
|---------------|------|
| `issue-N-stepS-agent-uuid` | Session ID → direct job lookup |
| `agent-issue-N-...` | Job name → direct |
| `PR:N` or `pr:N` | PR number → resolve to issue |
| Bare number (`714`) | Could be issue or PR — try issue first |
| `--all` | All active jobs |

### 2. Resolve PR → Issue

If input is a PR number:
```bash
gh pr view N --json body --jq '.body' | grep -oP 'issue: #\K\d+'
```
Falls back to branch name parsing: `fix/issue-714-...` → issue 714.

### 3. Resolve Issue → Job

```bash
kubectl get jobs -n fenrir-agents --sort-by=.metadata.creationTimestamp \
  -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}' | grep "issue-N-"
```
Takes the most recent job for that issue.

### 4. Stream

Once we have the job name, delegate to `agent-logs.mjs`:

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
node "$REPO_ROOT/infrastructure/k8s/agents/agent-logs.mjs" "<SESSION_ID>" --tools --spawn-pane
```

This opens a tmux pane in the right column with the parsed log stream.

If the job is completed and the pod is reaped, show:
```
Job completed. Saved log: tmp/agent-logs/<session-id>.log
Brandify: /brandify-agent <session-id>
```

### 5. Report

After spawning the pane, report back:
```
Streaming #<ISSUE> — <JOB_NAME>
Pane: right column (stacked)
```

## Flags

| Flag | Effect |
|------|--------|
| `--all` | Stream all active jobs (delegates to `agent-logs.mjs --all --tmux`) |
| `--verbose` | Pass `--tools` to agent-logs (default: on) |
| `--thinking` | Include thinking blocks |
| `--no-follow` | Dump existing logs, don't stream |

## Error Handling

| Condition | Behavior |
|-----------|----------|
| No job found for issue | Error: "No agent jobs for issue #N" |
| PR has no linked issue | Error: "Can't find issue for PR #N" |
| Job pod reaped | Show saved log path + brandify hint |
| Invalid input | Error with usage hint |
