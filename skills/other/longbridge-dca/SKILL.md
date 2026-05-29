---
name: longbridge-dca
description: |
  Mutating operations on the user's Longbridge recurring-investment (DCA) plans — list (read-only), create a plan, update / pause / resume / stop a plan, view trade history, check eligibility. Requires longbridge login WITH TRADE SCOPE because every plan automatically commits real money on a schedule. Every mutation requires a two-step preview + confirm protocol, and `create` requires the user to read back amount / frequency / symbol / start date / end date before confirming. Use only when the user gives a clear imperative ("create a monthly DCA on AAPL for 500 USD", "停止定投 700.HK"); ambiguous prompts ("帮我看看定投") must be rejected with a "please be specific" reply rather than triggered. Triggers: "创建定投", "新建定投计划", "设置定投", "暂停定投", "停止定投", "恢复定投", "修改定投", "建立定投", "建立定投計劃", "設置定投", "暫停定投", "停止定投", "恢復定投", "修改定投", "create DCA", "create recurring investment", "set up DCA plan", "pause DCA", "stop DCA plan", "resume DCA", "monthly DCA on X", "weekly recurring buy".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: mutating
  requires_login: true
  default_install: true
---

# longbridge-dca

⚠️ **EXTRA-HIGH-RISK mutating skill**: a recurring-investment plan **commits real money on a schedule** — every active plan will automatically place buy orders against the user's brokerage account on the chosen frequency, until paused or stopped. Mistakes here cost real money. Treat creation and modification with extreme caution.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## Extra risk note (read this before every `create` / `update`)

DCA commits real money on a recurring schedule. **Read the plan back including amount / frequency / symbol / start date / end date or duration / day-of-week or day-of-month before asking for confirmation.** If the user is not 100% sure of any parameter, **ask before executing — never paper over uncertainty**. Specifically:

- If the user did not specify the **amount**, ask. Do not default.
- If the user did not specify the **frequency** (`daily` / `weekly` / `fortnightly` / `monthly`), ask.
- If the user said "weekly" without naming a `day-of-week`, ask.
- If the user said "monthly" without naming a `day-of-month`, ask.
- If the user did not specify when to **stop** (or that the plan is open-ended), confirm explicitly.
- If the user gave an amount in an ambiguous currency, ask which currency (USD vs HKD vs CNY).

If anything is unclear after one round of clarification, **do not proceed** — escalate back to the user instead of guessing.

## When to use

Trigger only on **clear imperatives** about recurring investment plans:

- *"给 AAPL 每月 500 美元定投,每月 15 号"*
- *"create a weekly DCA on TSLA.US for 200 USD every Monday"*
- *"暂停定投 plan 12345"* / *"停止 700.HK 的定投"*

Vague prompts (*"帮我看看定投怎么样"*, *"我应不应该定投"*) must be **refused with a clarifying question** — never trigger automated execution from advice-style prompts.

For **read-only** listing (`longbridge dca`, `longbridge dca --status Active`, `longbridge dca history <PLAN_ID>`, `longbridge dca stats`, `longbridge dca check <SYMBOL>...`, `longbridge dca calc-date ...`) you may run the CLI directly without the preview/confirm gate. Mutations always need the gate.

## Two-step protocol (mandatory)

Every mutation must run as **two distinct turns**:

1. **Preview** — describe exactly what you are about to do (symbol, amount + currency, frequency, day-of-week / day-of-month, plan id for pause/resume/stop/update), in the user's language. **Do not run the CLI yet.** For `create`, list every parameter on a separate line and explicitly note that this will execute real buy orders going forward.
2. **Wait for explicit confirmation** containing "确认 / yes / 是的 / confirm". If the user replies anything ambiguous, ask again — do **not** assume consent. Casual acknowledgements like "好" / "ok" / "嗯" alone are NOT confirmation for a `create` — require an explicit "确认" / "confirm" / "是的".
3. **Execute** — only after step 2, run the actual `longbridge dca <subcommand> ...` command.

## CLI subcommands

`longbridge dca` carries read modes (no subcommand, plus `history` / `stats` / `calc-date` / `check`) and several mutating subcommands. **Always run `longbridge dca <subcommand> --help` first if you are not 100% sure of the current flag spelling, defaults, or argument order** — this protects against version drift, especially because monetary parameters are involved.

| Action | CLI invocation (typical shape — verify with `--help` before use) |
|---|---|
| List all plans | `longbridge dca --format json` |
| Filter by status | `longbridge dca --status <Active\|Suspended\|Finished> --format json` |
| Filter by symbol | `longbridge dca --symbol <SYMBOL> --format json` |
| Plan trade history (read) | `longbridge dca history <PLAN_ID> --format json` |
| Stats summary (read) | `longbridge dca stats --format json` |
| Calculate next trade date (read) | `longbridge dca calc-date ... --format json` |
| Check symbol eligibility (read) | `longbridge dca check <SYMBOL>... --format json` |
| Create monthly plan (mutating) | `longbridge dca create <SYMBOL> --amount <N> --frequency monthly --day-of-month <D> --format json` |
| Create weekly plan (mutating) | `longbridge dca create <SYMBOL> --amount <N> --frequency weekly --day-of-week <mon\|tue\|...> --format json` |
| Update an existing plan (mutating) | `longbridge dca update <PLAN_ID> [...flags] --format json` |
| Pause a plan (mutating) | `longbridge dca pause <PLAN_ID> --format json` |
| Resume a paused plan (mutating) | `longbridge dca resume <PLAN_ID> --format json` |
| Stop a plan permanently (mutating) | `longbridge dca stop <PLAN_ID> --format json` |
| Set pre-trade reminder hours | `longbridge dca set-reminder ... --format json` |

> Other flags exist (start date, end date, daily / fortnightly frequency, etc.). The exact spelling can drift between CLI versions — **always verify with `longbridge dca create --help` before issuing the command, and quote the exact command back to the user in the preview.**

If the user gives a **symbol** but no plan id for pause/resume/stop/update, first run `longbridge dca --symbol <SYMBOL> --format json` to look up the plan id and current status, then quote the id back in your preview before asking for confirmation.

## Preview templates (LLM)

For `create` (the highest-risk action):

> ⚠️ 即将创建定投计划:
> - 标的:{SYMBOL}
> - 金额:{AMOUNT} {CURRENCY}
> - 频率:{frequency}({day-of-week / day-of-month})
> - 起始日:{start date}
> - 结束:{end date 或 "无结束日,持续运行"}
>
> 此计划生效后,系统会按计划自动从你的账户下单买入。是否确认执行?(请回复"确认"/"confirm"/"是的")

> ⚠️ About to create a recurring investment plan:
> - Symbol: {SYMBOL}
> - Amount: {AMOUNT} {CURRENCY}
> - Frequency: {frequency} ({day-of-week / day-of-month})
> - Start date: {start date}
> - End: {end date or "open-ended, runs until paused/stopped"}
>
> Once active, the system will automatically place buy orders from your brokerage account on every scheduled date. Confirm? (Reply "confirm" / "yes" / "确认" to proceed.)

> ⚠️ 即將建立定投計劃:
> - 標的:{SYMBOL}
> - 金額:{AMOUNT} {CURRENCY}
> - 頻率:{frequency}({day-of-week / day-of-month})
> - 起始日:{start date}
> - 結束:{end date 或 "無結束日,持續運行"}
>
> 此計劃生效後,系統會按計劃自動從你的賬戶下單買入。是否確認執行?(請回覆「確認」/「confirm」/「是的」)

For pause / resume / stop / update — list plan id + symbol + amount + frequency + new state, then ask:

- *"即将暂停定投计划 12345 (AAPL.US,每月 500 USD,每月 15 号)。是否确认执行?"*
- *"About to permanently stop DCA plan 12345 (AAPL.US, 500 USD monthly). Confirm?"*
- *"即將恢復定投 12345。是否確認?"*

## OAuth scope

DCA mutations require the **trade scope**. Without it, both CLI and MCP fail with `unauthorized` / `not in authorized scope`. Tell the user to `longbridge auth logout && longbridge auth login` and tick "Trade" in the browser. Read-only DCA listing also requires trade scope to view account-bound plan data.

## Error handling

| Situation | LLM response |
|---|---|
| Shell `command not found: longbridge` | Tell the user to install [longbridge-terminal](https://github.com/longportapp/longbridge-terminal); MCP fallback may apply (see below) but **only after user confirmation** — never use MCP to bypass the preview / confirm protocol. |
| stderr contains `not logged in` / `unauthorized` / `not in authorized scope` | Tell the user to run `longbridge auth logout && longbridge auth login` and tick "Trade". |
| Symbol not eligible for DCA | Run `longbridge dca check <SYMBOL> --format json` and surface the reason verbatim. Do not retry. |
| Insufficient buying power on the scheduled date | This typically surfaces as a downstream order failure, not at create-time. Surface the message verbatim and ask the user how to proceed (top-up cash / pause / lower amount). |
| Bad `<PLAN_ID>` (not found) | Re-run `longbridge dca --format json` and re-check the id. |
| Other stderr | Surface verbatim. **Do not silently retry** — if a mutating call failed, ask the user before any second attempt. Money is involved; a silent retry could double-execute. |

## MCP fallback (only after confirmation)

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime.

> **Important**: the preview / confirm cycle still applies when going through MCP. MCP write tools have no built-in confirmation prompt; this SKILL is responsible for the gate. The extra read-back-of-parameters rule applies in full to MCP calls.

## Related skills

- `longbridge-positions` — check cash balance and buying power before sizing a DCA plan.
- `longbridge-portfolio` — review existing exposure before adding a new recurring buy.
- `longbridge-orders` — review the actual fills produced by an active DCA plan.
- `longbridge-quote` — sanity-check current price vs. plan amount.

## File layout

```
longbridge-dca/
└── SKILL.md          # prompt-only, no scripts/
```

Prompt-only — no `scripts/`. Discover the latest CLI flags via `longbridge dca <subcommand> --help`. Because money is at stake, **always** run `--help` before issuing a `create` or `update` you have not run in this session.
