---
name: bk
description: Use when checking Buildkite CI/CD builds, investigating failures, viewing job logs, or answering questions about pipeline status.
argument-hint: "[build URL | build number | 'latest' | pipeline question]"
allowed-tools:
  - Glob
  - Read
  - Grep
  - Bash(bk build view:*)
  - Bash(bk build list:*)
  - Bash(bk build watch:*)
  - Bash(bk build download:*)
  - Bash(bk job list:*)
  - Bash(bk job log:*)
  - Bash(bk pipeline list:*)
  - Bash(bk pipeline view:*)
  - Bash(bk pipeline validate:*)
  - Bash(bk artifacts list:*)
  - Bash(bk artifacts download:*)
  - Bash(bk whoami:*)
  - Bash(bk config list:*)
  - Bash(bk config get:*)
---

# Buildkite CI/CD

Investigate Buildkite builds, diagnose failures, and answer questions about pipeline status.

## Arguments

```
$ARGUMENTS
```

## Constraints

- **Never assume CLI subcommands or flags.** If unsure, run `bk <command> --help` first.
- The `bk` CLI uses `-p` for pipeline and `-b` for branch/build-number. Always check `--help` for the specific command.
- Use `--no-timestamps` with `bk job log` for cleaner output.
- Use `-o json` when you need structured data for analysis.

## Instructions

### 1. Parse Input

Determine what the user is asking about:

- **Build URL** (e.g., `https://buildkite.com/org/pipeline/builds/123`) → extract org, pipeline slug, build number
- **Build number** → use with current repo's pipeline
- **"latest"** or no number → use `bk build view` without a number (resolves to current branch)
- **General question** → use `bk build list` or `bk job list` with appropriate filters

### 2. Identify Pipeline

If not specified, infer from the current git repo. The `bk` CLI auto-detects pipeline when inside a repo.

If pipeline is ambiguous or `bk` can't detect it, use `-p <pipeline-slug>`.

### 3. Investigate

**For build failures:**

1. `bk build view <number> -o json` — get build state and job list
2. Find failed jobs (state: `failed`, non-zero `exit_status`)
3. `bk job log <job-id> -p <pipeline> -b <build-number> --no-timestamps` — get failure logs
4. Read from the end of logs — errors are usually at the bottom
5. For large logs, focus on lines near `exit_status`, `error`, `failed`, or `Error`

**For general status:**

- `bk build list -p <pipeline>` — recent builds
- `bk build view` — latest build on current branch
- `bk job list -p <pipeline> --state failed` — recent failures

### 4. Diagnose

When analyzing failures:

- **Exit status codes**: `-1` = agent lost, `255` = forced agent shutdown, `1` = command failure, `17` = docker-compose plugin failure
- **Docker build failures**: Look for `failed to solve:` messages
- **Plugin failures**: Look for `plugin <name> command hook exited with status`
- **Infrastructure**: Look for agent timeouts, OOM, disk space issues
- **Test failures**: Look for test framework output (go test, bats, jest, etc.)

### 5. Report

Provide a concise summary:
- Which step(s) failed
- Root cause (quote the key error lines)
- Suggested fix if apparent

## Examples

```
/bk 91                                    → investigate build 91
/bk https://buildkite.com/gusto/my-pipe/builds/42  → investigate from URL
/bk latest                                → check latest build on current branch
/bk why did this fail                     → latest build, find failures
/bk list failed builds                    → recent failures for current pipeline
```
