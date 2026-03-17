---
name: launchd-non-apple-jobs
description: List launchd jobs that are not from Apple and create user launchd jobs. Use when the user says "show me my jobs", "show my launchd jobs", asks for non-Apple launchd jobs, or wants to create a one-time or recurring launchd job.
---

# Launchd Non-Apple Jobs

## Overview
Show the current launchd job list filtered to non-Apple labels, and create user LaunchAgents (GUI domain) for one-time or recurring schedules.

## Quick Start
- List non-Apple jobs:

```bash
scripts/show_jobs.sh
```

- Create a one-time job:

```bash
scripts/create_job.sh --label "com.example.myjob" --command "echo hello" --once "2026-02-05 13:30"
```

- Create a recurring job:

```bash
scripts/create_job.sh --label "com.example.myjob" --command "echo hello" --daily "09:00"
```

- Remove a job:

```bash
scripts/delete_job.sh --label "com.example.myjob"
```

## Tasks

### Show non-Apple jobs
- Run `scripts/show_jobs.sh`.
- The output keeps the header and only non-Apple labels.

### Create a one-time job
- Use `--once "YYYY-MM-DD HH:MM"`.
- The job schedules via `StartCalendarInterval` and self-removes after the first run.

### Create a recurring job
- Use one of: `--daily`, `--weekly`, `--monthly`, or `--interval`.
- The job uses `StartCalendarInterval` (or `StartInterval`) and remains installed until removed.

### Remove a job
- Run `scripts/delete_job.sh --label "<label>"`.
- This unloads the job and moves the plist (and one-time wrapper, if present) to Trash.

### Customize the filter (optional)
- If the user wants to include additional Apple-like prefixes, update the regex in `scripts/show_jobs.sh`.

## Resources

### scripts/
- `show_jobs.sh`: Launches `launchctl list` and filters out Apple jobs.
- `create_job.sh`: Creates a user LaunchAgent for one-time or recurring schedules.
- `delete_job.sh`: Unloads and removes a user LaunchAgent by label.
