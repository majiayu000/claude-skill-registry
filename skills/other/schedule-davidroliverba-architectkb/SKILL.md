---
context: fork
model: sonnet
description: Schedule vault maintenance tasks using macOS launchd
---

# /schedule

Schedule recurring vault maintenance tasks using macOS launchd (or cron on Linux).

## Usage

```
/schedule list                          # List scheduled jobs
/schedule add <job> <schedule>          # Add a scheduled job
/schedule remove <job>                  # Remove a scheduled job
/schedule run <job>                     # Run job immediately
/schedule status                        # Show job status and last run times
```

## Examples

```
/schedule list
/schedule add health-check daily
/schedule add graph-rebuild hourly
/schedule add validate weekly
/schedule remove health-check
/schedule status
```

## Available Jobs

| Job             | Description                                                        | Default Schedule  |
| --------------- | ------------------------------------------------------------------ | ----------------- |
| `health-check`  | Run vault health check (scripts/health-check.js)                   | Daily at 6am      |
| `validate`      | Run frontmatter/link validation (scripts/validate.js)              | Weekly on Monday  |
| `graph-rebuild` | Rebuild knowledge graph index (scripts/generate-graph-enhanced.js) | Hourly            |
| `vault-index`   | Rebuild SQLite FTS5 search index (scripts/vault-to-sqlite.js)      | Daily at 5am      |
| `backup`        | Git commit and push vault changes                                  | Daily at midnight |
| `weblink-check` | Check for dead weblinks                                            | Weekly on Sunday  |
| `custom`        | User-defined command                                               | As specified      |

## Schedule Formats

| Format        | Description                | Example            |
| ------------- | -------------------------- | ------------------ |
| `hourly`      | Every hour at :00          | `hourly`           |
| `daily`       | Every day at 6:00 AM       | `daily`            |
| `daily@HH:MM` | Every day at specific time | `daily@09:30`      |
| `weekly`      | Every Monday at 6:00 AM    | `weekly`           |
| `weekly@DAY`  | Specific day at 6:00 AM    | `weekly@friday`    |
| `cron EXPR`   | Cron expression (5 fields) | `cron 0 */4 * * *` |

## Instructions

### 1. Parse Command

Identify the subcommand:

- `list` - Show all scheduled jobs
- `add` - Create new scheduled job
- `remove` - Delete scheduled job
- `run` - Execute job immediately
- `status` - Show job status

### 2. Handle Subcommands

#### For `list`:

Read launchd plist files from `~/Library/LaunchAgents/`:

```bash
ls -la ~/Library/LaunchAgents/com.vault.* 2>/dev/null
```

Display in table format:

```
Scheduled Vault Jobs
====================

| Job           | Schedule      | Status  | Last Run   |
|---------------|---------------|---------|------------|
| health-check  | Daily @ 06:00 | Active  | 2026-01-26 |
| graph-rebuild | Hourly        | Active  | 2026-01-26 |
| validate      | Weekly Mon    | Paused  | 2026-01-20 |
```

#### For `add`:

1. Parse job name and schedule
2. Generate launchd plist file
3. Write to `~/Library/LaunchAgents/com.vault.{{job}}.plist`
4. Load the job: `launchctl load ~/Library/LaunchAgents/com.vault.{{job}}.plist`

**Plist Template**:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.vault.{{job}}</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/node</string>
        <string>{{vault_path}}/scripts/{{script}}.js</string>
    </array>
    <key>WorkingDirectory</key>
    <string>{{vault_path}}</string>
    <key>StartCalendarInterval</key>
    {{schedule_dict}}
    <key>StandardOutPath</key>
    <string>{{vault_path}}/.claude/logs/{{job}}.log</string>
    <key>StandardErrorPath</key>
    <string>{{vault_path}}/.claude/logs/{{job}}.error.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin</string>
    </dict>
</dict>
</plist>
```

**Schedule Dict Examples**:

```xml
<!-- Daily at 6am -->
<dict>
    <key>Hour</key>
    <integer>6</integer>
    <key>Minute</key>
    <integer>0</integer>
</dict>

<!-- Hourly -->
<dict>
    <key>Minute</key>
    <integer>0</integer>
</dict>

<!-- Weekly on Monday -->
<dict>
    <key>Weekday</key>
    <integer>1</integer>
    <key>Hour</key>
    <integer>6</integer>
    <key>Minute</key>
    <integer>0</integer>
</dict>
```

#### For `remove`:

1. Unload the job: `launchctl unload ~/Library/LaunchAgents/com.vault.{{job}}.plist`
2. Delete the plist file
3. Confirm removal

#### For `run`:

Execute the job immediately:

```bash
launchctl start com.vault.{{job}}
```

Or run directly:

```bash
node scripts/{{script}}.js
```

#### For `status`:

Show status for all jobs:

```bash
launchctl list | grep com.vault
```

Display last run times from log files.

### 3. Job Definitions

Map job names to scripts:

```javascript
const JOBS = {
  "health-check": {
    script: "health-check.js",
    defaultSchedule: "daily",
    description: "Run vault health check",
  },
  validate: {
    script: "validate.js",
    defaultSchedule: "weekly",
    description: "Validate frontmatter and links",
  },
  "graph-rebuild": {
    script: "generate-graph-enhanced.js",
    defaultSchedule: "hourly",
    description: "Rebuild knowledge graph index",
  },
  "vault-index": {
    script: "vault-to-sqlite.js",
    defaultSchedule: "daily@05:00",
    description: "Rebuild SQLite FTS5 search index",
  },
  backup: {
    script: "backup.sh",
    defaultSchedule: "daily@00:00",
    description: "Git commit and push",
  },
  "weblink-check": {
    script: "check-weblinks.js",
    defaultSchedule: "weekly@sunday",
    description: "Check for dead weblinks",
  },
};
```

### 4. Create Supporting Files

Ensure log directory exists:

```bash
mkdir -p .claude/logs
```

Create backup script if not exists (`.claude/scripts/backup.sh`):

```bash
#!/bin/bash
cd "$(dirname "$0")/../.."
git add -A
git commit -m "Automated backup: $(date +%Y-%m-%d)"
git push origin main
```

### 5. Linux Support (Alternative)

For Linux systems, use crontab instead:

```bash
# Add to crontab
(crontab -l 2>/dev/null; echo "0 6 * * * cd {{vault_path}} && node scripts/health-check.js") | crontab -

# List crontab
crontab -l | grep vault

# Remove from crontab
crontab -l | grep -v "{{job}}" | crontab -
```

### 6. Output Results

After any operation, display:

```
Schedule Operation Complete
===========================

Action: {{action}}
Job: {{job}}
Status: {{success/failed}}

{{details}}

Next run: {{next_scheduled_time}}
Log file: .claude/logs/{{job}}.log
```

## Error Handling

- If launchctl fails, suggest running with admin privileges
- If plist syntax is invalid, show validation error
- If script doesn't exist, offer to create it
- If job already exists (for add), ask to overwrite

## Related Skills

- [[.claude/skills/vault-maintenance/SKILL.md|/vault-maintenance]] - Manual maintenance
- [[.claude/skills/quality-report/SKILL.md|/quality-report]] - Quality metrics
- [[.claude/skills/check-weblinks/SKILL.md|/check-weblinks]] - Weblink validation
