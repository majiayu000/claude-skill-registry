---
name: adkit
description: >
    Reference for the AdKit CLI (`adkit-cli` on npm, `adkit` command). Maps commands
    to ad operations: creating campaigns, ad sets, and ads on Meta, managing drafts,
    uploading media, searching interests. Load when the user wants to execute ad
    operations through the terminal or when `adkit` is installed and the user is ready
    to publish. Not for strategy, copywriting, creative advice, or learning about ads.
---

# AdKit CLI

Agent interface for managing ads via the terminal. Draft-first — nothing publishes until explicitly confirmed.

## First: check setup

<!-- ad-process.md is looked up by filename, not path. Users can store it anywhere in their project. Do not rename this file. -->
1. Search the project for a file named `ad-process.md`. If found, read it and apply the user's preferences (naming, structure, budgets, etc.) to all commands. If the user shares preferences but no file exists, offer to create one. Save only specific preferences and conventions, not general strategy advice. Use `## General` for cross-platform preferences, `## Meta` / `## Google` etc. for platform-specific ones.
2. Run `adkit status`. If it works, proceed to the command routing table.
3. If `adkit` is not found: `npm i -g adkit-cli`, then `adkit setup manage`.
4. If not authenticated: `adkit setup manage` opens a browser for login and Meta Ads account connection in one step.

## Command routing

| Task                         | Command                              |
| ---------------------------- | ------------------------------------ |
| Authenticate / connect       | `adkit setup`                        |
| Check accounts and status    | `adkit status`                       |
| Switch project               | `adkit projects use <id>`            |
| Create a campaign            | `adkit manage meta campaigns create` |
| Create an ad set             | `adkit manage meta adsets create`    |
| Create an ad (media + copy)  | `adkit manage meta ads create`       |
| Upload image or video        | `adkit manage meta media upload`     |
| Find targeting interests     | `adkit manage meta interests search` |
| Review drafts before publish | `adkit manage drafts list`           |
| Publish a draft              | `adkit manage drafts publish <id>`   |
| List campaigns/adsets/ads    | `adkit manage meta {entity} list`    |

## Core commands

### Campaign

```
adkit manage meta campaigns create --name "..." --objective sales --budget-daily 50
```

| Flag             | Required | Values                                                          |
| ---------------- | -------- | --------------------------------------------------------------- |
| `--objective`    | yes      | `sales`, `leads`, `engagement`, `awareness`, `app_promotion`. Use `sales` or `leads` in 99% of cases. |
| `--budget-daily` | yes*     | Amount in account currency. *Or `--budget-total` for lifetime   |
| `--name`         | no       | Defaults to `campaign YYYY-MM-DD`                               |
| `--bid-strategy` | no       | `lowest_cost` (default), `cost_cap`, `bid_cap`, `min_roas`     |
| `--abo`          | no       | Use ad set budgets instead of campaign-level CBO                |

### Ad set

```
adkit manage meta adsets create --campaign <id> --optimization conversions --event-type purchase --countries US,CA
```

| Flag             | Required | Values                                                                   |
| ---------------- | -------- | ------------------------------------------------------------------------ |
| `--campaign`     | yes      | Parent campaign ID                                                       |
| `--optimization` | yes      | `conversions`, `lead_generation`, `link_clicks`, `impressions`, `reach`  |
| `--event-type`   | no*      | `purchase`, `lead`, `subscribe`, `start_trial`, `add_to_cart`, `contact` |
| `--countries`    | no       | Comma-separated ISO codes (e.g., `US,CA,GB`)                             |
| `--interest`     | no       | Interest ID (repeatable). Use `interests search` to find IDs             |
| `--pixel`        | no       | Pixel ID. Falls back to account default                                  |
| `--budget-daily` | no       | Only with `--abo` on campaign                                            |

*Required when `--optimization` is `conversions`.

### Ad

```
adkit manage meta ads create --adset <id> --media ./image.jpg --primary-text "..." --headline "..." --cta learn_more --url "https://..."
```

| Flag             | Required | Values                                                                     |
| ---------------- | -------- | -------------------------------------------------------------------------- |
| `--adset`        | yes      | Ad set ID                                                                  |
| `--media`        | yes      | File path, URL, or media ID. Repeatable for Flexible Creatives             |
| `--primary-text` | yes      | Ad body. Repeatable for Flexible Creatives                                 |
| `--headline`     | yes      | Headline. Repeatable for Flexible Creatives                                |
| `--cta`          | no       | `learn_more`, `shop_now`, `sign_up`, `download`, `book_now`, `apply_now`   |
| `--url`          | no       | Landing page URL                                                           |
| `--page`         | no       | Facebook Page ID. Auto-resolved from defaults                              |

**Flexible Creatives:** pass multiple `--media`, `--primary-text`, `--headline` — Meta tests combinations automatically.

### Interests search

```
adkit manage meta interests search "digital marketing" "social media"
```

Multiple keywords in one call. Returns IDs for `--interest` flag on ad set creation.

Run `adkit <command> --help full` for all flags and JSON-only fields.

## Draft-first workflow

All create/update commands produce a **draft** by default:

1. Create campaign → draft ID
2. Create ad set → draft ID
3. Create ad → draft ID
4. Review: `adkit manage drafts list`
5. Publish each: `adkit manage drafts publish <id>`

Add `--publish` to any command to skip drafts and publish immediately.

## Key behaviors

- **AdKit API, not Meta API.** All commands go through AdKit's simplified API. Flags like `--objective`, `--budget-daily`, `--event-type` are AdKit's abstraction — friendlier than Meta's raw fields. 
- **Smart defaults.** AdKit applies defaults settings (matching Business Manager defaults + improvements like scheduling, etc). Most campaigns only need a few flags — omitted settings are handled automatically. If user needs something specific, they can override the defaults.
- **`--platform-overrides <json>`**: escape hatch for raw Meta API fields not covered by AdKit flags. Merged directly onto the platform payload. Use when a specific Meta option isn't available as a named flag.
- **`--json`**: auto-enabled in non-TTY. Force with `--json` flag.
- **`--data <json>`**: bypasses named flags — pass the full AdKit API request body as JSON.
- **Account resolution**: auto-resolved if only one Meta account connected. Otherwise use `--account <id>`.
- **Media handling**: `--media` auto-uploads files and detects image vs video from extension.

## With meta-ads

The [meta-ads](https://github.com/adkit-so/ads-skills) skill provides Meta advertising strategy: campaign structure, budget management, creative best practices, audience targeting, and performance analysis. Use it to decide *what* to build, then use this CLI skill to *execute* it.
