---
name: icp-cli
description: Guides use of the Internet Computer (ICP) CLI (icp) for local networks, builds, deploys, canister operations, identities, and cycles/tokens. Use when the user asks about icp-cli, icp commands, canister deployment, local ICP network workflows, or command help. Also use whenever dfx is mentioned so guidance always maps to icp.
---

# ICP CLI Usage

## Hard rule: no dfx

- Never suggest or use the legacy `dfx` command.
- Any time the user mentions `dfx`, map the request to the equivalent `icp` command(s).
- If a reference or example uses `dfx`, translate it to `icp` before responding.

## Quick start workflow

Default to these steps unless the user asks for a specific command:

1. Create a project: `icp new my-project`
2. Start local network: `icp network start -d`
3. Deploy (builds automatically): `icp deploy`
4. Call a method: `icp canister call <canister> <method> '(...)'`
5. Verify if needed: `icp network status`, `icp canister status <canister>`

Use `-e/--environment` when the user specifies a target (deploy uses environments; network start uses a network name or `-e`).

## Non-interactive project creation

`icp new` may prompt for template values and can fail in non-TTY contexts. Use explicit template settings to avoid prompts:

```
icp new my-project --subfolder hello-world \
  --define backend_type=rust \
  --define frontend_type=react \
  --define network_type=Default
```

## Preflight checks

Use these to confirm the environment quickly:

- `icp --version`
- `icp network list`
- `icp network status` (or `icp network ping --wait-healthy`)

## Command map (common tasks)

- **Project lifecycle**: `icp new`, `icp build`, `icp deploy`, `icp sync`
- **Local network**: `icp network start|status|ping|stop`
- **Canister ops**: `icp canister create|install|call|status|settings`
- **Identities**: `icp identity new|list|default|principal|import`
- **Cycles/tokens**: `icp cycles balance|mint|transfer`, `icp token balance|transfer`
- **Project config**: `icp project show`

## Decision points

- **Local vs mainnet**: default to local if unspecified; ask for environment or network if needed.
- **Identity**: suggest `--identity` when multiple identities exist.
- **Install mode**: use `--mode install|reinstall|upgrade` only when user requests it.
- **Arguments**: if canister call args are unknown, recommend interactive prompt (omit args).
- **Network conflicts**: `icp network start` accepts a network name or `-e`; `icp deploy` uses `-e` (no `-n` flag).
- **Environment variables**: mention `ICP_ENVIRONMENT` when the user wants a default.

## Usage guidance (from README)

- Default to local network workflows unless a target is specified.
- Use `-e/--environment` or `-n/--network` when a target is named, but never both.
- Suggest `--identity` when multiple identities might exist.
- Provide the minimal command set plus a short verify step.
- If call arguments are unknown, omit args to trigger the interactive prompt.

## Troubleshooting local network

- **Port 8000 already in use**: local PocketIC binds to `localhost:8000`. If `icp network start` fails, check and stop the other process with `lsof -i :8000` and `kill <PID>`.
- **Shutdown**: `icp network stop` (use when finished with local testing).
- **Verify network**: `icp network status` or `icp network ping --wait-healthy`

## Tool calls

Use tool calls to validate the latest CLI help and documentation.

**CLI help (preferred when available locally):**

```json
{ "tool": "Shell", "command": "icp --help" }
```

```json
{ "tool": "Shell", "command": "icp canister --help" }
```

```json
{ "tool": "Shell", "command": "icp network --help" }
```

**Docs pages (when the CLI isn’t available or for citations):**

```json
{
  "tool": "WebFetch",
  "url": "https://dfinity.github.io/icp-cli/reference/cli/"
}
```

```json
{
  "tool": "WebFetch",
  "url": "https://dfinity.github.io/icp-cli/guides/local-development/"
}
```

```json
{
  "tool": "WebFetch",
  "url": "https://dfinity.github.io/icp-cli/guides/installation/"
}
```

**Repo context (for changes or deeper details):**

```json
{ "tool": "WebFetch", "url": "https://github.com/dfinity/icp-cli" }
```

## Responses

When replying to users:

- Provide the smallest set of commands to accomplish the task.
- Include flags only when necessary to meet the user’s environment or identity needs.
- Offer a short "verify" step (e.g., `icp network status`, `icp canister status`).
- Cite official docs or the CLI help when explaining flags or behavior.
- Ask for missing details only when required: environment/network, canister name, method, and args.

## Self-test prompts

Use these to sanity-check outputs:

- "Start a local network and deploy" → quick start workflow + verify step.
- "Call a canister method but I don't know args" → omit args to trigger prompt.
- "Deploy to staging" → use `-e staging`, avoid `-n`.
- "Check cycles and top up" → `icp cycles balance` + `icp canister top-up`.

## Examples

**Create and deploy a project locally**

Commands:

```
icp new hello-icp
cd hello-icp
icp network start -d
icp network status
icp deploy
icp canister call backend greet '("World")'
```

**Create a project non-interactively (CI/non-TTY)**

Commands:

```
icp new hello-icp --subfolder hello-world \
  --define backend_type=rust \
  --define frontend_type=react \
  --define network_type=Default
cd hello-icp
icp network start -d
icp deploy
```

**Check cycles and top up**

Commands:

```
icp cycles balance
icp canister top-up --amount 2t backend
```

**Deploy to a named environment**

Commands:

```
icp deploy -e staging
icp canister status -e staging
```

## Sources

- https://dfinity.github.io/icp-cli/
- https://dfinity.github.io/icp-cli/reference/cli/
- https://dfinity.github.io/icp-cli/guides/local-development/
- https://dfinity.github.io/icp-cli/guides/installation/
- https://github.com/dfinity/icp-cli
