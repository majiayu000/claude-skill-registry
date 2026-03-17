---
name: Apple-Search-Ads
description: Manage Apple Search Ads campaigns, ad groups, keywords, and reports via the asa-cli tool. Use when the user asks about Apple Search Ads management, campaign operations, keyword bidding, ASA reports, or ad performance.
---

# Apple Search Ads CLI

Use `asa-cli` to interact with the Apple Search Ads Campaign Management API v5. Always use `-o json` when you need to parse results programmatically.

## Organizations

Run `asa-cli whoami` to list available orgs. For multi-org accounts, pass `--org-id` with every command (except `whoami`). Single-org accounts auto-detect the org.

## Commands

### Auth & Config
```bash
asa-cli whoami                          # List all orgs (no --org-id needed)
asa-cli configure --client-id "..." --team-id "..." --key-id "..." --private-key-path "..."
asa-cli configure                       # Interactive mode
```

### Campaigns
```bash
asa-cli campaigns list [--org-id <orgid>] [--limit N] [--offset N]
asa-cli campaigns get <id> [--org-id <orgid>]
asa-cli campaigns find [--org-id <orgid>] [--filter "status=ENABLED"] [--sort "name:asc"] [--limit N] [--all]
asa-cli campaigns create [--org-id <orgid>] --name "..." --budget 1000 --daily-budget 50 --countries US,GB --app-id 123456
asa-cli campaigns update <id> [--org-id <orgid>] [--name ...] [--budget ...] [--daily-budget ...] [--status ENABLED|PAUSED]
asa-cli campaigns delete <id> [--org-id <orgid>]
```

### Ad Groups (require --campaign-id)
```bash
asa-cli adgroups list --campaign-id <id> [--org-id <orgid>]
asa-cli adgroups get <id> --campaign-id <id> [--org-id <orgid>]
asa-cli adgroups find --campaign-id <id> [--org-id <orgid>] [--filter "status=ENABLED"]
asa-cli adgroups create --campaign-id <id> [--org-id <orgid>] --name "..." --default-bid 1.50 --start-time "2026-01-01T00:00:00.000" [--cpa-goal 5.00] [--auto-keywords true|false]
asa-cli adgroups update <id> --campaign-id <id> [--org-id <orgid>] [--name ...] [--default-bid ...] [--status ...]
asa-cli adgroups delete <id> --campaign-id <id> [--org-id <orgid>]
```

### Keywords (require --campaign-id --adgroup-id)
```bash
asa-cli keywords list --campaign-id <id> --adgroup-id <id> [--org-id <orgid>]
asa-cli keywords get <kwid> --campaign-id <id> --adgroup-id <id> [--org-id <orgid>]
asa-cli keywords find --campaign-id <id> --adgroup-id <id> [--org-id <orgid>] [--filter "text~brand"]
asa-cli keywords create --campaign-id <id> --adgroup-id <id> [--org-id <orgid>] --text "keyword" [--text "another"] --match-type BROAD|EXACT [--bid 1.50]
asa-cli keywords update --campaign-id <id> --adgroup-id <id> [--org-id <orgid>] --id <kwid> [--status ACTIVE|PAUSED] [--bid 2.00]
asa-cli keywords delete <kwid,kwid2> --campaign-id <id> --adgroup-id <id> [--org-id <orgid>]
```

### Negative Keywords
```bash
# Campaign-level
asa-cli negative-keywords campaign-list --campaign-id <id> [--org-id <orgid>]
asa-cli negative-keywords campaign-find --campaign-id <id> [--org-id <orgid>] [--filter "text~free"]
asa-cli negative-keywords campaign-create --campaign-id <id> [--org-id <orgid>] --text "term" [--text "another"] --match-type EXACT|BROAD
asa-cli negative-keywords campaign-delete <kwid,...> --campaign-id <id> [--org-id <orgid>]

# Ad group-level
asa-cli negative-keywords adgroup-list --campaign-id <id> --adgroup-id <id> [--org-id <orgid>]
asa-cli negative-keywords adgroup-find --campaign-id <id> --adgroup-id <id> [--org-id <orgid>] [--filter "text~competitor"]
asa-cli negative-keywords adgroup-create --campaign-id <id> --adgroup-id <id> [--org-id <orgid>] --text "term" [--text "another"] --match-type EXACT|BROAD
asa-cli negative-keywords adgroup-delete <kwid,...> --campaign-id <id> --adgroup-id <id> [--org-id <orgid>]
```

### Reports
```bash
asa-cli reports campaigns [--org-id <orgid>] --start-date 2024-01-01 --end-date 2024-01-31 [--granularity DAILY|WEEKLY|MONTHLY] [--group-by countryOrRegion,deviceClass]
asa-cli reports adgroups --campaign-id <id> [--org-id <orgid>] --start-date ... --end-date ...
asa-cli reports keywords --campaign-id <id> [--org-id <orgid>] --start-date ... --end-date ...
asa-cli reports search-terms --campaign-id <id> [--org-id <orgid>] --start-date ... --end-date ...
```

### Utilities
```bash
asa-cli apps search --query "MyApp" [--owned]
asa-cli geo search --query "US" [--entity ...] [--country-code ...]
```

## Filter Syntax
Operators for `--filter`: `=` EQUALS, `~` CONTAINS, `@` IN (comma-sep), `>` GT, `<` LT, `>=` GTE, `<=` LTE, `!~` NOT_CONTAINS.

Example: `--filter "status=ENABLED" --filter "name~Brand"`

## Global Flags
| Flag | Short | Description |
|------|-------|-------------|
| `--output` | `-o` | `json` or `table` (default: `table`) |
| `--org-id` | | Organization ID — required for multi-org accounts, auto-detected for single-org |
| `--profile` | `-p` | Named config profile |
| `--verbose` | `-v` | Show HTTP request/response details |
| `--no-color` | | Disable colored output |

## Config
- Config stored at `~/.asa-cli/config.yaml`, token cache at `~/.asa-cli/token_cache.json`
- Profiles: `asa-cli configure -p production --client-id "..." ...`, then `asa-cli campaigns list -p production`
- Env var overrides: `ASA_CLIENT_ID`, `ASA_TEAM_ID`, `ASA_KEY_ID`, `ASA_ORG_ID`, `ASA_PRIVATE_KEY_PATH`

## Guidelines
- Always use `-o json` and pipe through `jq` when extracting specific fields
- For multi-org accounts, always include `--org-id` — run `asa-cli whoami -o json` to discover org IDs
- Fetch campaign/adgroup IDs first before operating on child resources
- Use `--all` on find commands to auto-paginate large result sets
- Reports require `--start-date` and `--end-date` in YYYY-MM-DD format
- Currency is auto-detected from the org — no need to specify it manually
- Ad group create requires `--start-time` (ISO 8601 format, e.g. `"$(date -u +%Y-%m-%dT%H:%M:%S.000)"` for now)
- `--auto-keywords` defaults to `false` (search match OFF). Only enable explicitly when creating discovery ad groups
- `keywords find` may return 404 on paused/deleted campaigns — use `keywords list` as a fallback
- Default pagination limit is 20. Use `--limit 50` (or higher) when expecting more results (e.g. negative keywords)
- Report metrics use v5 field names: `totalInstalls`, `tapInstalls`, `viewInstalls`, `totalNewDownloads`, `totalRedownloads`, `totalInstallRate`, `tapInstallRate`, `totalAvgCPI`, `tapInstallCPI`, `avgCPM` — not the old v4 names
- Use `--grand-totals` on campaign reports to get aggregated totals across all campaigns
