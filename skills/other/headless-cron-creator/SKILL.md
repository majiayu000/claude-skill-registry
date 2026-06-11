---
name: headless-cron-creator
description: "Generate headless Claude Code cron jobs with safety."
user-invocable: false
argument-hint: "<name> <schedule> <prompt>"
agent: python-general-engineer
allowed-tools:
  - Read
  - Write
  - Bash
  - Edit
  - Glob
  - Grep
routing:
  triggers:
    - "create cron job"
    - "scheduled task"
    - "headless agent"
    - "background automation"
    - "recurring agent"
  category: process
  pairs_with:
    - cron-job-auditor
    - shell-process-patterns
---

# Headless Cron Creator Skill

Generate headless Claude Code cron jobs from a task description and schedule. Creates a wrapper script with safety mechanisms (lockfile, budget cap, dry-run default, logging) and installs crontab entries. All crontab mutations go through `scripts/crontab-manager.py`, which writes to temp files and creates timestamped backups in `~/.claude/crontab-backups/` before every change -- never pipe directly to `crontab -` because a mid-stream pipe failure wipes the entire crontab.

## Instructions

### Phase 1: PARSE

Extract job parameters from the user's request.

**Required parameters**:
- **name** -- short kebab-case identifier (e.g., `reddit-automod`, `feed-health-check`)
- **prompt** -- what Claude should do each run (natural language)
- **schedule** -- cron expression or human-readable interval

**Optional parameters** (with defaults):
- **workdir** -- where to `cd` before running (default: current repo root)
- **budget** -- max USD per run (default: `2.00`; user may override)
- **allowed-tools** -- which tools the headless session can use (default: `Bash Read`; user may override)
- **logdir** -- where to store logs (default: `{workdir}/cron-logs/{name}`)

**Human-readable schedule conversion** -- use off-minutes (7, 23, 47) instead of `:00`/`:30` because every cron job on the system fires at round minutes, creating load spikes:

| Human Input | Cron Expression |
|-------------|----------------|
| every 12 hours | `7 */12 * * *` |
| twice daily | `7 8,20 * * *` |
| hourly | `23 * * * *` |
| daily at 6am | `7 6 * * *` |
| weekly on sunday | `7 9 * * 0` |
| every 30 minutes | `*/30 * * * *` |

**Gate**: All required parameters extracted. Proceed to Phase 2.

### Phase 2: GENERATE

Create the wrapper script using `crontab-manager.py generate-wrapper`. Embed the prompt via bash heredoc to avoid escaping issues.

```bash
python3 ~/.claude/scripts/crontab-manager.py generate-wrapper \
  --name "{name}" \
  --prompt "{prompt}" \
  --schedule "{schedule}" \
  --workdir "{workdir}" \
  --budget "{budget}" \
  --allowed-tools "{allowed_tools}"
```

Review the generated script. Verify it contains:
- [ ] `set -euo pipefail`
- [ ] `flock` lockfile -- prevents concurrent runs of the same job
- [ ] `--permission-mode auto` -- never use `--dangerously-skip-permissions` (auto is sufficient) or `--bare` (breaks OAuth/keychain auth)
- [ ] `--max-budget-usd` -- caps spend per run (default $2.00)
- [ ] `--no-session-persistence`
- [ ] `--allowedTools`
- [ ] `tee` to per-run timestamped log file
- [ ] Dry-run/execute toggle -- scripts do nothing destructive without `--execute`
- [ ] Exit code propagation via `PIPESTATUS[0]`

Do not use the `CronCreate` tool -- it is session-scoped (dies when the session ends, auto-expires after 7 days). Use system `crontab` via `crontab-manager.py` instead.

**Gate**: Script generated and reviewed. Proceed to Phase 3.

### Phase 3: VALIDATE

Verify the generated script meets cron best practices.

1. Run the script in dry-run mode:
   ```bash
   bash -n scripts/{name}-cron.sh  # syntax check
   ```

2. Run `cron-job-auditor` checks:
   - [ ] Error handling (`set -e`)
   - [ ] Lock file (`flock`)
   - [ ] Logging (`tee`, `LOG_DIR`)
   - [ ] Working directory (absolute `cd`)
   - [ ] PATH awareness (absolute path to `claude` -- cron has minimal PATH, so all commands must use absolute paths)
   - [ ] Cleanup on exit (lock release)

**Gate**: All checks pass. Proceed to Phase 4.

### Phase 4: INSTALL

Install the crontab entry. Every entry gets a `# claude-cron: <tag>` marker so `crontab-manager.py` can identify and manage only its own entries without touching non-Claude crontab lines. All paths in the crontab entry must be absolute because cron has minimal PATH.

1. Show the proposed entry:
   ```bash
   python3 ~/.claude/scripts/crontab-manager.py add \
     --tag "{name}" \
     --schedule "{schedule}" \
     --command "{absolute_script_path} --execute >> {logdir}/cron.log 2>&1" \
     --dry-run
   ```

2. **Ask the user for confirmation** before installing. Never install without explicit approval.

3. If confirmed:
   ```bash
   python3 ~/.claude/scripts/crontab-manager.py add \
     --tag "{name}" \
     --schedule "{schedule}" \
     --command "{absolute_script_path} --execute >> {logdir}/cron.log 2>&1"
   ```

4. Verify:
   ```bash
   python3 ~/.claude/scripts/crontab-manager.py verify --tag "{name}"
   ```

**Gate**: Entry installed and verified. Proceed to Phase 5.

### Phase 5: REPORT

Summarize the created cron job and print the exact commands to test and manage it.

Output:
- Script path
- Cron schedule (human-readable + expression)
- Log directory
- Budget per run
- Tag for management
- Commands for future management:
  ```
  python3 ~/.claude/scripts/crontab-manager.py list          # see all claude cron jobs
  python3 ~/.claude/scripts/crontab-manager.py verify --tag {name}  # health check
  python3 ~/.claude/scripts/crontab-manager.py remove --tag {name}   # uninstall
  ```

To modify an existing wrapper script, regenerate it with `--force` rather than editing in place.

## Error Handling

### Error: "tag already exists"
Cause: A cron entry with this tag is already installed.
Solution: Either `remove --tag {name}` first, or choose a different name.

### Error: "claude: command not found" in cron
Cause: Cron has minimal PATH; `claude` isn't in it.
Solution: `generate-wrapper` resolves the absolute path to `claude` at generation time.
If the path changes, regenerate the wrapper with `--force`.

### Error: "crontab install failed"
Cause: System crontab service issue.
Solution: Check `crontab -l` manually. Restore from `~/.claude/crontab-backups/`.

## References

- `scripts/crontab-manager.py` -- all crontab mutations (add, remove, list, verify, generate-wrapper)
- `skills/infrastructure/cron-job-auditor/SKILL.md` -- validation checks for generated scripts
