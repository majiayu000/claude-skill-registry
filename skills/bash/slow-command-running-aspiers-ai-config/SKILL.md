---
name: slow-command-running
description: Pipe long running commands through tee(1) to allow watching output and repeated analyses without rerunning
---

# Command Output Logging

## When to use this skill

Use it whenever running commands that:

- are slow or long-running or expensive in any way
- are likely to need multiple analyses of their output
- involve API calls or other network operations
- are GitHub CLI commands (`gh`) or similar

## How it works

Always pipe these commands through `tee(1)` to capture output to a file while
still displaying it in real-time.

## Key Principles

- Never blindly pipe through `head(1)` unless you're sure premature
  termination via SIGPIPE won't cause problems.

- When tee-ing into a temporary logfile, prefer the `tmp/` subdirectory
  of the repository rather than `/tmp`, so that you don't have to ask
  permission for access to `/tmp`.

- Don't assume `tmp/` exists - you might need to create it first.

## Usage

1. Create `tmp/` directory if it doesn't exist: `mkdir -p tmp/`

2. Run the command with tee: `command | tee tmp/output.log`

3. The user can now choose to monitor that log file as it runs.

4. If you subsequently need to examine the output multiple times, reading from
   the log file prevents needing to re-run the slow command each time.

## Examples

```bash
# Run tests with logging
mkdir -p tmp/
npm test | tee tmp/test-output.log

# Check GitHub action run
mkdir -p tmp/
gh run view 12345 | tee tmp/action-run-12345.log

# Access some API
mkdir -p tmp/
some-API-call-command | tee tmp/logs.log
```
