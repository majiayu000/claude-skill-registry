---
name: longbridge-statement
description: |
  Account statements (daily / monthly) via Longbridge Securities — list available statements and export sections (equity holdings, cash transactions, fees, etc.) as CSV or markdown for accounting, tax filing, or audit. Also covers bank cards linked to the account, withdrawal history, and deposit history. Requires longbridge login with Trade scope. Read-only — no order placement here. Triggers: "对账单", "月结单", "日结单", "账单导出", "税务报表", "报税资料", "导出持仓", "导出交易记录", "银行卡", "出金记录", "入金记录", "充值记录", "對賬單", "月結單", "日結單", "賬單導出", "稅務報表", "報稅資料", "銀行卡", "出金記錄", "入金記錄", "account statement", "monthly statement", "daily statement", "export statement", "tax report", "bank cards", "withdrawal history", "deposit history", "1099", "year-end statement".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: account_read
  requires_login: true
  default_install: true
---

# longbridge-statement

Account statement listing and section export — for accounting, tax filing, and audit workflows.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.
>
> **Privacy**: statements contain account-level holdings, cash flow, and fees. Only return details in direct conversation.

## When to use

- *"我最近的对账单"*, *"上个月月结单"* → `statement` (default = list)
- *"日结单"*, *"daily statement"* → `statement --type daily`
- *"月结单"*, *"monthly statement"* → `statement --type monthly`
- *"导出某月对账单 CSV"*, *"export equity holdings"* → `statement export --file-key <KEY> --section <SECTION>`
- *"报税要交易明细"*, *"tax report data"* → list first, then export the relevant section.
- *"我绑定了哪些银行卡"*, *"bank cards"* → `bank-cards`
- *"我的出金记录"*, *"withdrawal history"* → `withdrawals`
- *"我的入金记录"*, *"deposit history"* → `deposits`

For trades / fills detail, prefer `longbridge-orders`. For live holdings / cash, prefer `longbridge-positions`.

## Subcommands

> Run `longbridge statement --help` and `longbridge statement export --help` if unsure of current flags / supported sections.

| CLI command | Returns |
|---|---|
| `longbridge statement --format json` | List of available statements (alias for `statement list`) |
| `longbridge statement --type daily --format json` | List of recent daily statements (default 30) |
| `longbridge statement --type monthly --format json` | List of recent monthly statements (default 12) |
| `longbridge statement list --format json` | Same as the bare command |
| `longbridge statement export --file-key <KEY> --section <SECTION> --format json` | Export one statement section as CSV / markdown |

Common flags on the parent command:

| Flag | Default | Notes |
|---|---|---|
| `--type` | `daily` | `daily` or `monthly` |
| `--start-date` | 30 days ago | `YYYY-MM-DD` |
| `--limit` | 30 (daily) / 12 (monthly) | Number of records |

## Workflow

1. **List** first: run `longbridge statement --type ... --format json` to see available statements; each row includes a `file-key` (or similar) identifier.
2. Pick the statement the user wants by date.
3. **Export** the desired section: `longbridge statement export --file-key <KEY> --section <SECTION>`. Confirm the filesystem location with the user before writing if the CLI streams to a path.
4. Surface the export path and section names; do not paraphrase or regenerate the contents — these are accounting source documents.

## OAuth scope

Account statements require **Trade scope**. If `unauthorized` shows up, tell the user to:

```bash
longbridge auth logout && longbridge auth login
```

and re-tick "Trade" during the OAuth flow.

## CLI examples

```bash
# List last 30 daily statements
longbridge statement                                                --format json

# List last 12 monthly statements
longbridge statement --type monthly                                 --format json

# Custom date window
longbridge statement --type daily --start-date 2026-01-01 --limit 90 --format json

# Export the equity-holdings section of one statement
longbridge statement export --file-key <KEY> --section equity_holdings --format json

# Bank cards linked to the account
longbridge bank-cards --format json

# Withdrawal history (paginated)
longbridge withdrawals --format json
longbridge withdrawals --page 2 --count 50 --format json

# Deposit history (with filters)
longbridge deposits --format json
longbridge deposits --states 1 --currencies HKD,USD --format json  # credited, HKD+USD only
```

> Available `--section` values vary by statement type and account. Run `longbridge statement export --help` for the canonical list before guessing.

## Output

- `list` mode: array of statement metadata rows (date, type, `file-key`, etc.).
- `export` mode: written-file path or inline CSV / markdown payload, depending on CLI version.

When summarising, give a small table of dates + keys; never re-format the section contents themselves.

## Error handling

| Situation | LLM response |
|---|---|
| Shell `command not found: longbridge` | Fall back to MCP if configured; otherwise tell the user to install longbridge-terminal. |
| stderr contains `not logged in` / `unauthorized` | Tell the user to run `longbridge auth logout && longbridge auth login` and tick "Trade" scope. |
| stderr `not_found` on export | Re-run the `list` step to confirm the `file-key`. |
| Empty list | "No statements available in the requested window — try widening `--start-date` or switching `--type`." |
| Other stderr | Surface verbatim — never silently retry. |

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

If the exact MCP names differ, the CLI is the canonical path.

## Related skills

| User asks | Route to |
|---|---|
| Live holdings / cash balance | `longbridge-positions` |
| Today / historical orders / fills | `longbridge-orders` |
| Account-level P&L analysis | `longbridge-portfolio` |
| Multi-currency conversion for the statement | `longbridge-fx` |

## File layout

```
longbridge-statement/
└── SKILL.md          # prompt-only, no scripts/
```
