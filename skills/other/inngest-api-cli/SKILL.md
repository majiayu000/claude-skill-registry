---
name: inngest-api-cli
description: >-
  Use when operating Inngest API resources from the terminal with
  `npx inngest-cli@latest api`: Cloud/local run debugging, event-run lookup,
  function traces, function invocation, app syncs, webhooks, environments,
  keys, account checks, and Insights queries. Provides prescriptive command
  routing for agents: which CLI command to run for a run ID, event ID, app ID,
  function ID, Cloud environment, API key, missing ID, or potentially mutating
  operation. Use `inngest-cli` for dev server setup/general CLI workflows and
  `inngest-api` only when raw REST API v2 docs or OpenAPI fallback are needed.
---

# Inngest API CLI

Use this skill when the task is operational: inspect, debug, sync, invoke, or
query Inngest API resources through the terminal. This skill is intentionally
prescriptive so agents can act without guessing.

For general CLI setup, `inngest dev`, Docker, local testing, MCP setup, or
self-hosted `inngest start`, use `inngest-cli`. For code changes, pair this
with the domain skill that owns the code pattern: `inngest-setup`,
`inngest-durable-functions`, `inngest-events`, `inngest-steps`,
`inngest-flow-control`, `inngest-realtime`, or `inngest-middleware`.

## First Move

Verify the current CLI surface before relying on memory:

```bash
npx inngest-cli@latest api --help
npx inngest-cli@latest api <command> --help
```

The active API command is `inngest api`. If prompt context or old docs mention
`inngest alpha api`, switch to `inngest api`.

Use `inngest-api` only when:

- The CLI does not expose the needed endpoint.
- The user explicitly asks for raw REST API v2.
- You need the OpenAPI spec or LLM API docs to resolve request shape.

For complete command flags, read
[references/cli-commands.md](references/cli-commands.md) after this skill
triggers.

## Target Rules

- Local is the default target for `inngest api`.
- Cloud Production requires `--prod`.
- Non-production Cloud environments require `INNGEST_ENV=<name>` or `--env`.
- Prefer `INNGEST_API_KEY` for Cloud API access.
- Do not pass API keys inline with `--api-key <secret>` unless the user
  explicitly accepts process-list and transcript exposure.
- Never write API keys, event keys, signing keys, webhook URLs, or decrypted
  secrets into source files, docs, fixtures, or final answers.

Common targets:

```bash
npx inngest-cli@latest api health
npx inngest-cli@latest api --prod get-account
INNGEST_ENV=staging npx inngest-cli@latest api --prod get-webhooks
npx inngest-cli@latest api --api-host http://127.0.0.1 --api-port 8288 health
```

## Local Development

For local app work:

1. Start the user's app with local dev mode when applicable, for example
   `INNGEST_DEV=1 npm run dev`.
2. Start the dev server:

   ```bash
   npx inngest-cli@latest dev
   ```

3. Prefer Dev Server MCP tools, when available, to list local functions, send
   test events, inspect runs, and watch status.
4. Use `npx inngest-cli@latest api ...` for API-compatible local checks,
   command-help verification, and workflows not exposed through MCP.

If the local API says the dev server is unavailable, start `inngest dev` or
switch to Cloud with `--prod` when the user is debugging deployed runs.

## Command Routing

Use this table before asking the human for more context.

| Situation | Command path |
| --- | --- |
| Check CLI/API reachability | `api health` |
| Confirm Cloud auth | `api --prod get-account` |
| List environments | `api --prod get-account-envs --limit 10` |
| List event keys | `api --prod get-account-event-keys --limit 10` |
| List signing keys | `api --prod get-account-signing-keys --limit 10` |
| List webhooks | `api --prod get-webhooks` |
| User gives a run ID | `api --prod get-function-run <run_id>` |
| Need step-level detail | `api --prod get-function-trace <run_id> --include-output` |
| User gives an event ID | `api --prod get-event-runs <event_id> --limit 5 --include-output` |
| Sync a known app ID | `api --prod sync-app --app-id <app_id> --url <serve_url>` |
| Invoke a known app/function ID | `api --prod invoke-function --app-id <app_id> --function-id <function_id> --data '<json>'` |
| Discover Insights tables | `api --prod get-insights-tables` |
| Discover event schemas for Insights | `api --prod get-insights-event-schemas --limit 25` |
| Draft an Insights query | `api --prod query-insights-prompt --prompt '<request>'` |
| Run an Insights query | `api --prod query-insights --query '<sql>'` |

If a command accepts positional IDs, prefer positional IDs in examples because
they are shorter and match current help. Flag forms such as `--run-id` are also
accepted by the current CLI for many path parameters.

## Debug a Run

When the user gives a run ID:

```bash
npx inngest-cli@latest api --prod get-function-run <run_id>
npx inngest-cli@latest api --prod get-function-trace <run_id> --include-output
```

Summarize status, failed spans, retry state, timing, error names/messages, and
the likely code boundary to inspect. Do not paste full traces unless asked.

When the user gives an event ID:

```bash
npx inngest-cli@latest api --prod get-event-runs <event_id> --limit 5 --include-output
```

Pick the relevant run from the response, then fetch the run and trace. If
multiple runs are plausible, explain the candidates and use timestamps,
function IDs, or failure status to choose.

## Missing IDs

Do not immediately ask the user for app IDs, function IDs, or run IDs.

Try, in order:

1. Dev Server MCP tools, if available.
2. The user's prompt, pasted dashboard URLs, logs, alert text, or stack traces.
3. Repository config and Inngest serve definitions.
4. Event ID lookup with `get-event-runs`.
5. Current CLI help to see if discovery commands such as `get-functions` or
   `get-app` have appeared.

Ask the user for the ID only after those sources cannot provide it.

## Mutating Operations

Read before write. List or fetch the relevant resource first, then mutate only
when target and intent are clear.

Confirm before running these against Cloud unless the user already specified
the account/environment and exact intent:

- `create-env`
- `patch-env`
- `create-webhook`
- `sync-app`
- `invoke-function`
- Broad or expensive `query-insights` calls

For repeatable invocation tests, use a stable idempotency key:

```bash
npx inngest-cli@latest api --prod invoke-function \
  --app-id <app_id> \
  --function-id <function_id> \
  --idempotency-key <stable_test_key> \
  --data '{"example":true}'
```

For complex JSON, use `--body-file` to avoid quoting mistakes.

## Insights

Use Insights when the question is analytic, when logs only give partial clues,
or when the user asks about trends, frequency, volume, failures over time, or
event/run data.

Start small:

```bash
npx inngest-cli@latest api --prod get-insights-tables
npx inngest-cli@latest api --prod get-insights-event-schemas --limit 25
npx inngest-cli@latest api --prod query-insights-prompt \
  --prompt "Show failed functions in the last 24 hours"
```

Inspect generated SQL before running broad queries. Add limits and time windows
when possible.

## Output Handling

- CLI output is JSON. Parse it structurally before making decisions.
- Use `--raw` only when a downstream command needs exact response bodies.
- If responses are paginated and `page.hasMore` is true, continue with
  `--cursor` when complete results are needed.
- Treat missing `data` on list responses as an empty list unless an error is
  present.
- Redact secrets, webhook URLs, token values, and sensitive payload fields in
  summaries.

## Drift Handling

The CLI is beta. If behavior differs from this skill:

1. Run top-level and command-specific help.
2. Check `https://api-docs.inngest.com/llms.txt`.
3. Check `https://api-docs.inngest.com/api-specs/v2.json`.
4. Use the `inngest-api` skill for raw REST API fallback.

Some launch material may mention aliases such as `get-run` or
`invoke-function-by-slug`. Use them only if current `api --help` exposes them.
If absent, use `get-function-run` and `invoke-function`.
