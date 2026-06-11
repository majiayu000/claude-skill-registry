---
name: cron-job-auditor
description: "Audit cron scripts for reliability and safety."
user-invocable: false
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
routing:
  triggers:
    - "audit cron jobs"
    - "review scheduled scripts"
    - "cron safety"
    - "cron reliability"
    - "scheduled task safety"
  category: infrastructure
  pairs_with:
    - shell-process-patterns
    - headless-cron-creator
---

# Cron Job Auditor Skill

Static analysis of cron and scheduled job scripts against a 9-point reliability checklist. Produces structured PASS/FAIL/WARN results with severity classification (CRITICAL, HIGH, MEDIUM, LOW) and paste-ready code fixes for every finding. Audits are read-only and pattern-based -- scripts are never executed, because cron scripts may delete data, send emails, or modify production state.

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| Checking error handling, `set -e`, `pipefail`, `trap`, exit codes | `shell-error-handling.md` | Routes to the matching deep reference |
| Checking lock files, flock, PID files, concurrent execution | `concurrency-and-locks.md` | Routes to the matching deep reference |
| Checking logging, timestamps, log rotation, stderr routing | `logging-and-rotation.md` | Routes to the matching deep reference |

## Instructions

### Phase 1: DISCOVER

**Goal**: Locate all cron/scheduled scripts to audit.

**Step 1: Read repository CLAUDE.md** (if present) to understand project conventions before auditing.

**Step 2: Identify target scripts**

If the user provides specific paths, use those. Otherwise search these directories recursively:
```
scripts/*.sh, cron/*.sh, jobs/*.sh, bin/*.sh
```

Also check for scripts referenced in crontab files, Makefiles, or CI configs.

**Step 3: Validate targets**

For each discovered file:
- Confirm it exists and is readable
- Check it has a shell shebang (`#!/bin/bash`, `#!/bin/sh`, `#!/usr/bin/env bash`)
- Skip non-shell files (Python cron jobs, etc.) with a note -- this skill audits shell scripts only; it cannot replace shellcheck for syntax issues or analyze complex control flow beyond pattern matching

**Step 4: Log discovery results**

```markdown
## Scripts Found
1. scripts/daily_backup.sh (bash, 45 lines)
2. cron/cleanup.sh (bash, 22 lines)
3. jobs/sync_data.sh (SKIPPED: Python script)
```

**Gate**: At least one auditable shell script identified. Proceed only when gate passes.

### Phase 2: AUDIT

**Goal**: Run every check against every script. Run all 9 checks regardless of script size or apparent simplicity -- small scripts grow, and missing basics cause production incidents.

**Step 1: Read each script fully**

Read the entire file content. Do not sample or skip sections. If the script sources a common library file (`source ...` or `. ...`), read the sourced file too -- patterns provided by sourced libraries count as PASS (with a note indicating the source).

**Step 2: Run the 9-point checklist**

Use regex pattern matching for reliable, reproducible detection. Verify matches are not inside comments (`# ...`) before counting them -- when a match appears in a comment or string, note reduced confidence rather than silently accepting it.

| # | Check | Patterns | Severity |
|---|-------|----------|----------|
| 1 | Error handling | `set -e`, `set -o errexit`, `\|\| exit` | CRITICAL |
| 2 | Exit code checking | `$?`, `if [ $? -eq`, `&& ... \|\|` | HIGH |
| 3 | Logging with timestamps | `>> *.log`, `$(date)`, `date +` | HIGH |
| 4 | Log rotation | `find -mtime -delete`, `logrotate`, `tail -n` | MEDIUM |
| 5 | Working directory | `cd "$(dirname"`, `SCRIPT_DIR=`, absolute paths | HIGH |
| 6 | PATH environment | `PATH=`, `export PATH`, `source *env` | MEDIUM |
| 7 | Lock file / concurrency | `.lock`, `flock`, `.pid`, lock file check | HIGH |
| 8 | Cleanup on exit | `trap ... EXIT`, `trap ... cleanup`, `rm -rf *tmp` | MEDIUM |
| 9 | Failure notification | `mail -s`, `curl *webhook`, `notify`, `alert` | LOW |

For each check, record:
- PASS with line number where pattern found, OR
- FAIL/WARN with specific recommendation including a paste-ready code snippet (findings without fixes create work without guidance)

**Step 3: Calculate score**

```
Score = passed / total_checks * 100
```

Classify scripts: 90-100% Excellent, 70-89% Good, 50-69% Needs Work, <50% Critical.

**Gate**: All 9 checks run against every script. No checks skipped. Proceed only when gate passes.

### Phase 3: REPORT

**Goal**: Produce structured, actionable audit output. Do not modify any scripts -- report problems with recommendations only.

**Step 1: Format per-script results**

```
CRON JOB AUDIT: scripts/daily_backup.sh
==================================================
  [PASS] Error handling (line 3)
  [PASS] Logging with timestamps (line 12)
  [FAIL] Lock file: No concurrent run prevention
  [WARN] PATH environment: PATH not explicitly set

SCORE: 7/9 (78%) - Good
```

**Step 2: Provide recommendations**

Every FAIL and WARN must include a specific code snippet the user can paste. Keep recommendations proportional to the script's scope -- suggest lock files, not monitoring frameworks.

```bash
# Recommendation: Add lock file
LOCK_FILE="/tmp/daily_backup.lock"
exec 200>"$LOCK_FILE"
flock -n 200 || { echo "Already running"; exit 0; }
trap "rm -f $LOCK_FILE" EXIT
```

**Step 3: Produce aggregate summary**

If auditing multiple scripts:

```
AGGREGATE SUMMARY
=================
Scripts audited: 4
Average score: 72%
Critical issues: 2 (missing error handling)
Most common gap: Lock files (3/4 scripts missing)
```

**Gate**: Every finding has a recommendation. Report is complete. Audit is done.

## Error Handling

### Error: "No Shell Scripts Found"
Cause: Scripts in unexpected locations, or cron jobs written in Python/Ruby
Solution:
1. Ask user for explicit paths
2. Search broader: `**/*.sh` across the entire repository
3. Check crontab entries for referenced file paths

### Error: "Script Has No Shebang"
Cause: Script relies on default shell interpreter
Solution:
1. Still audit the script (treat as bash)
2. Add finding: "Missing shebang line" as MEDIUM severity
3. Recommend adding `#!/bin/bash` or `#!/usr/bin/env bash`

### Error: "Regex Produces False Positive"
Cause: Pattern matches in comments, strings, or unrelated context
Solution:
1. Verify match by reading surrounding lines for context
2. Check if match is inside a comment (`# ...`) and exclude
3. Report the finding but note reduced confidence

### Error: "Script Uses Non-Standard Patterns"
Cause: Custom error handling, logging frameworks, or wrapper functions
Solution:
1. Check if script sources a common library file
2. Read the sourced file for the missing patterns
3. If patterns exist in sourced libraries, mark as PASS with note

## Reference Loading

| Task type / signal | Load this reference |
|--------------------|---------------------|
| Checking error handling, `set -e`, `pipefail`, `trap`, exit codes | `references/shell-error-handling.md` |
| Checking lock files, flock, PID files, concurrent execution | `references/concurrency-and-locks.md` |
| Checking logging, timestamps, log rotation, stderr routing | `references/logging-and-rotation.md` |

## References

### Best Practices Reference

```bash
#!/bin/bash
set -euo pipefail                              # Error handling
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"                                # Working directory
PATH=/usr/local/bin:/usr/bin:/bin               # Explicit PATH
LOCK="/tmp/$(basename "$0").lock"               # Lock file
exec 200>"$LOCK"
flock -n 200 || { echo "Already running"; exit 0; }
LOG="logs/$(basename "$0" .sh)_$(date +%Y%m%d).log"
exec > >(tee -a "$LOG") 2>&1                   # Logging
echo "$(date): Starting"
trap 'rm -f "$LOCK" /tmp/mytmp_*' EXIT         # Cleanup
find logs -name "*.log" -mtime +30 -delete      # Log rotation

# ... actual work ...

if [ $? -ne 0 ]; then                          # Failure notification
    echo "FAILED" | mail -s "Cron Alert" admin@example.com
fi
```
