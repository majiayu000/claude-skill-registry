---
name: otta-cli
description: "Use `otta-cli` to automate `otta.fi` workflows from terminal. This tool is usually used for tracking working time, absences, and sick leaves: authenticate, inspect config/cache, check account status, manage worktimes (list/add/update/delete), browse absences, fetch holidays, and generate combined/detailed calendar reports. Trigger this skill when a request needs CLI-first Otta operations, `OTTA_CLI_*` environment setup, machine-readable `--format json` output, or diagnosis of auth/config/API validation errors."
---

# Otta CLI

Use this skill to execute Otta time-tracking tasks end-to-end with repeatable CLI commands.

Main repository: https://github.com/mekedron/otta-cli

## Quick Start

1. Use the `otta` binary directly.

2. Verify command surface and storage paths.

```bash
otta --help
otta config path
otta config cache-path
```

3. Authenticate and hydrate cache.

```bash
otta auth login --username "$OTTA_CLI_USERNAME" --password "$OTTA_CLI_PASSWORD" --format json
otta status --format json
```

- `status` updates cached user metadata (for `user` and `worktimegroup` fallbacks used by worktimes/holidays/calendar commands).
- For non-interactive automation, prefer `--password-stdin` or secret env handling to reduce shell history exposure.

## Command Recipes

Use explicit dates/times in `YYYY-MM-DD` and `HH:MM` formats.

List worktimes:

```bash
otta worktimes list --date 2026-02-20 --format json
```

Add worktime:

```bash
otta worktimes add \
  --date 2026-02-20 \
  --start 09:00 \
  --end 17:00 \
  --pause 30 \
  --project <project-id> \
  --worktype <worktype-id> \
  --description "Example task description" \
  --format json
```

- `--user` is optional if `OTTA_CLI_USER_ID` or cached user ID exists.

Update worktime:

```bash
otta worktimes update --id <worktime-id> --start 10:00 --end 18:00 --format json
```

- Send at least one changed field with `--id`.

Delete worktime:

```bash
otta worktimes delete --id <worktime-id> --format json
```

Fetch holidays/workday calendar:

```bash
otta holidays \
  --from 2026-02-20 \
  --to 2026-02-29 \
  --worktimegroup <worktimegroup-id> \
  --format json
```

- `--worktimegroup` is optional if `OTTA_CLI_WORKTIMEGROUP_ID` or cached value exists.

Browse absences:

```bash
otta absence browse \
  --from 2026-02-01 \
  --to 2026-02-28 \
  --format json
```

Fetch current cumulative saldo:

```bash
otta saldo --format json
```

Generate combined calendar overview:

```bash
otta calendar overview \
  --from 2026-02-01 \
  --to 2026-02-28 \
  --format json
```

Generate detailed calendar day-by-day report:

```bash
otta calendar detailed \
  --from 2026-02-01 \
  --to 2026-02-28 \
  --format json
```

Use alternate duration units when totals are minute-based:

```bash
otta calendar detailed --from 2026-02-01 --to 2026-02-28 --format json --duration-format hours
otta worktimes browse --from 2026-02-01 --to 2026-02-28 --format json --duration-format days
```

- `--duration-format` values: `minutes` (default), `hours`, `days`, `hhmm`
- day conversion is fixed at `1 day = 24h = 1440 minutes`

Generate absence comment text:

```bash
otta absence comment \
  --type sick \
  --from 2026-02-20 \
  --to 2026-02-20 \
  --details "Flu symptoms" \
  --format json
```

## Environment Variables

Use these variables when running in CI/non-interactive environments:

- `OTTA_CLI_CONFIG_PATH`
- `OTTA_CLI_CACHE_PATH`
- `OTTA_CLI_API_BASE_URL`
- `OTTA_CLI_CLIENT_ID`
- `OTTA_CLI_USERNAME`
- `OTTA_CLI_PASSWORD`
- `OTTA_CLI_ACCESS_TOKEN`
- `OTTA_CLI_TOKEN_TYPE`
- `OTTA_CLI_REFRESH_TOKEN`
- `OTTA_CLI_TOKEN_SCOPE`
- `OTTA_CLI_USER_ID`
- `OTTA_CLI_WORKTIMEGROUP_ID`

## Agent Operating Rules

1. Prefer `--format json` for all data-producing commands and parse response fields instead of scraping text output.
2. `worktimes list/browse/report` are worktime-only and never include absences; do not infer absences from empty worktime rows.
3. For user schedule checks/log interpretation, prefer `calendar detailed --format json` first; use `calendar overview` as lighter fallback.
4. Use `--duration-format` when users request non-minute output; keep raw minute values for auditability.
5. Run `status --format json` before operations that rely on cached user/worktimegroup metadata.
6. Validate dates/times before command execution (`YYYY-MM-DD`, `HH:MM`).
7. Run `worktimes list` before `update` or `delete` when IDs are not explicitly known.
8. Return exact command, exit code, and concise stderr message when failures happen.
9. Never print raw credentials or tokens in summaries.

## Failure Recovery

- `no access token configured (run \`otta auth login\`)`
  - Run `auth login`, then rerun `status`.
- `username is required (use --username)`
  - Pass `--username` or set `OTTA_CLI_USERNAME`.
- `--worktimegroup is required (...)`
  - Pass `--worktimegroup`, set `OTTA_CLI_WORKTIMEGROUP_ID`, or run `status` to refresh cache.
- `--date must be YYYY-MM-DD`, `--start must be HH:MM`, `--to must be greater than or equal to --from`
  - Correct input format/order, rerun command.
- `directory ... is contained in a module that is not one of the workspace modules listed in go.work`
  - Build/run with `GOWORK=off` in this repository context.
