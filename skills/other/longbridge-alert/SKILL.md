---
name: longbridge-alert
description: |
  Mutating operations on the user's Longbridge price alerts — list (read-only), add a new price alert, enable / disable an alert, delete an alert. Requires longbridge login. Every mutation (add / delete / enable / disable) requires a two-step preview + confirm protocol. Use only when the user gives a clear imperative ("set a price alert at 200 for NVDA", "delete alert 486469", "提醒我 NVDA 涨到 200"); ambiguous prompts ("整理我的提醒") must be rejected with a "please be more specific" reply rather than triggered. Triggers: "设置股价提醒", "添加股价提醒", "提醒我 X 涨到 Y", "提醒我 X 跌破 Y", "删除股价提醒", "关掉提醒", "暫停提醒", "設置股價提醒", "添加股價提醒", "提醒我 X 漲到 Y", "提醒我 X 跌破 Y", "刪除股價提醒", "關掉提醒", "set price alert", "add price alert", "alert me when X hits Y", "delete price alert", "enable alert", "disable alert", "price alert".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: mutating
  requires_login: true
  default_install: true
---

# longbridge-alert

⚠️ **Mutating skill**: changes the user's price-alert state on Longbridge. No money is involved, but the change is persistent and will affect future push notifications.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

Trigger only on **clear imperatives** to manage price alerts:

- *"提醒我 NVDA.US 涨到 200"* / *"在 200 美元提醒我"*
- *"删除提醒 486469"* / *"關掉那個提醒"*
- *"set an alert when TSLA hits 250"*

Vague prompts (*"整理一下我的提醒"*, *"看看我的提醒怎么样"*) must be **refused with a clarifying question** — ask which symbol, which direction, which price, which alert id — never guess.

For **read-only** listing of existing alerts, you may run `longbridge alert --format json` directly without the preview/confirm gate (listing changes nothing). Mutations always need the gate.

## Two-step protocol (mandatory)

Every mutation must run as **two distinct turns**:

1. **Preview** — describe exactly what you are about to do (symbol, target price, direction `rise`/`fall`, alert id for delete/enable/disable), in the user's language. **Do not run the CLI yet.**
2. **Wait for explicit confirmation** containing "确认 / yes / 是的 / confirm". If the user replies anything ambiguous, ask again — do **not** assume consent.
3. **Execute** — only after step 2, run the actual `longbridge alert <subcommand> ...` command.

> The Longbridge CLI's `delete` subcommand prints its own confirmation prompt — let it run; do not pipe `yes` or pass any flag that bypasses it. For `add` / `enable` / `disable`, this skill's preview-then-confirm protocol is the SKILL-layer gate.

## CLI subcommands

`longbridge alert` carries one read mode (no subcommand) and four write subcommands. **Always run `longbridge alert <subcommand> --help` first if you are not 100% sure of the current flag spelling, defaults, or argument order** — this protects against version drift.

| Action | CLI invocation (typical shape — verify with `--help` before use) |
|---|---|
| List all alerts | `longbridge alert --format json` |
| List alerts for one symbol | `longbridge alert <SYMBOL> --format json` |
| Add a price alert | `longbridge alert add <SYMBOL> --price <PRICE> --direction <rise\|fall> --format json` |
| Delete an alert by id | `longbridge alert delete <ALERT_ID> --format json` |
| Enable an alert | `longbridge alert enable <ALERT_ID> --format json` |
| Disable an alert | `longbridge alert disable <ALERT_ID> --format json` |

> The `delete` subcommand has a built-in confirmation prompt. Let it run interactively in your environment.

If the user gives a **symbol** but no alert id for delete/enable/disable, first run `longbridge alert <SYMBOL> --format json` to look up the id, then quote the id back in your preview before asking for confirmation.

## Preview templates (LLM)

> 即将{动作}:{plan 摘要}。是否确认执行?
>
> About to {action}: {plan summary}. Confirm?
>
> 即將{動作}:{plan 摘要}。是否確認執行?

Examples:

- *"即将设置 NVDA.US 在 200 美元时提醒,价格上穿触发。是否确认执行?"*
- *"About to add a price alert on TSLA.US at 250 USD, triggered when price falls below. Confirm?"*
- *"即將刪除提醒 486469(NVDA.US @ 200,上穿)。是否確認執行?"*
- *"即将停用提醒 486469。是否确认?"*

If the user did not specify a direction (rise vs fall), **ask** — do not default. If the user did not specify a price, ask. Never invent values.

## OAuth scope

Price alerts are tied to the user's Longbridge account but do not place trades, so the **basic login scope** is sufficient — `longbridge auth login` without trade scope works. If the call returns `unauthorized`, tell the user to re-run `longbridge auth login` and complete the OAuth flow.

## Error handling

| Situation | LLM response |
|---|---|
| Shell `command not found: longbridge` | Tell the user to install [longbridge-terminal](https://github.com/longportapp/longbridge-terminal); MCP fallback can apply (see below) but **only after user confirmation** — never use MCP to bypass the preview / confirm protocol. |
| stderr contains `not logged in` / `unauthorized` | Tell the user to run `longbridge auth login`. |
| Bad `<ALERT_ID>` (not found) | Re-run the list command (`longbridge alert --format json`) and re-check the id. |
| `direction` flag rejected | Run `longbridge alert add --help` to confirm the current accepted values (typically `rise` / `fall`); surface the help excerpt to the user. |
| Other stderr | Surface verbatim. **Do not silently retry** — if a mutating call failed, ask the user before any second attempt. |

## MCP fallback (only after confirmation)

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime.

> **Important**: the preview / confirm cycle still applies when going through MCP. MCP write tools have no built-in confirmation prompt; this SKILL is responsible for the gate.

## Related skills

- `longbridge-quote` — look up the current price of a symbol before suggesting an alert level.
- `longbridge-watchlist` / `longbridge-watchlist-admin` — manage the favourites list (alerts and watchlists are independent).
- `longbridge-subscriptions` — diagnose real-time stream health (separate from alert push notifications).

## File layout

```
longbridge-alert/
└── SKILL.md          # prompt-only, no scripts/
```

Prompt-only — no `scripts/`. Discover the latest CLI flags via `longbridge alert <subcommand> --help`.
