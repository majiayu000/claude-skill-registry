---
name: self-relay-hyperlane-message
description: Uses the Hyperlane CLI to manually deliver (self-relay) a message between chains that are Ethereum protocol type.
---

# Self-Relay Hyperlane Message

Manually deliver a Hyperlane message using the CLI's `status --relay` command.

## Input Parameters

| Parameter       | Required | Default                                                         | Description                                                     |
| --------------- | -------- | --------------------------------------------------------------- | --------------------------------------------------------------- |
| `origin_chain`  | No       | Derived from Explorer API                                       | Name of the origin chain (auto-derived if not provided)         |
| `dispatch_tx`   | No\*     | -                                                               | Transaction hash of the dispatch (when message was sent)        |
| `message_id`    | No\*     | -                                                               | The Hyperlane message ID (alternative to dispatch_tx)           |
| `registry_path` | No       | CLI default                                                     | Path to a local registry (overridden if `private_rpcs` is true) |
| `key`           | No       | `$(HYPERLANE_MONOREPO=$(git rev-parse --show-toplevel) hypkey)` | Private key for signing the relay transaction                   |
| `private_rpcs`  | No       | `true`                                                          | If true, use private RPCs via local http-registry               |

**\*** Either `dispatch_tx` OR `message_id` must be provided, but not both.

## Instructions

### Step 0: Find Monorepo Root

The working directory may not be the monorepo root. Find it by looking for `CLAUDE.md` or `package.json` with `"name": "hyperlane-monorepo"`:

```bash
git rev-parse --show-toplevel
```

Store this path as `MONOREPO_ROOT`. All subsequent commands must be prefixed with `cd $MONOREPO_ROOT &&` to ensure correct execution.

### Step 1: Validate Inputs

**Validate dispatch_tx / message_id:**

- If NEITHER `dispatch_tx` nor `message_id` is provided → **Error:** "Must provide either dispatch_tx or message_id"
- If BOTH `dispatch_tx` and `message_id` are provided → **Error:** "Provide only one of dispatch_tx or message_id, not both"

### Step 2: Start Private RPC Registry (if needed)

If `private_rpcs` is `true`:

1. **Force override** `registry_path` to `http://localhost:3333`
2. **Start the http-registry** with /start-http-registry

### Step 3: Query Explorer API for Missing Data

Query the Hyperlane Explorer GraphQL API to resolve any missing values (`dispatch_tx`, `origin_chain`).

**If `message_id` was provided:**

```graphql
query {
  message_view(
    where: { msg_id: { _eq: "\\x<message_id_without_0x>" } }
    limit: 1
  ) {
    origin_tx_hash
    origin_domain
    is_delivered
  }
}
```

**If `dispatch_tx` was provided but `origin_chain` is missing:**

```graphql
query {
  message_view(
    where: { origin_tx_hash: { _eq: "\\x<dispatch_tx_without_0x>" } }
    limit: 1
  ) {
    origin_domain
    is_delivered
  }
}
```

Use the `mcp__hyperlane-explorer__query-graphql` tool. Note: bytea fields use `\\x` prefix without `0x`.

**Extract values:**

- `origin_tx_hash` → convert `\\x...` to `0x...` format → set as `dispatch_tx`
- `origin_domain` → set as `origin_chain` (e.g., "ethereum", "citrea")
- `is_delivered` → if `true`, inform user message is already delivered (no relay needed)

**If no message found:** Error "Message not found in Hyperlane Explorer"

### Step 4: Determine the Key Value

- If `key` was provided, use that value directly
- If `key` was NOT provided, use the default: `$(HYPERLANE_MONOREPO=$(git rev-parse --show-toplevel) hypkey)`
- **Important:** The default key value is a command substitution. Do NOT execute `hypkey` directly. Only use it as an environment variable value when running the relay command.

### Step 5: Run the Self-Relay Command

Run the following command (append `--registry <registry_path>` if `registry_path` is set):

```bash
cd $MONOREPO_ROOT && \
LOG_FORMAT=pretty LOG_LEVEL=debug HYP_KEY="<key>" \
pnpm -C typescript/cli hyperlane status --relay --origin <origin_chain> --dispatchTx <dispatch_tx>
```

### Step 6: Cleanup

If `private_rpcs` was `true`:

1. **Kill the http-registry** using the saved shell/task ID from Step 2
2. Confirm cleanup was successful

### Step 7: Report Results

Surface the output to the user, including:

- Whether the relay was successful
- Any errors encountered
- The destination transaction hash if successful

## Examples

### Example 1: Using dispatch_tx

```bash
cd $MONOREPO_ROOT && \
LOG_FORMAT=pretty LOG_LEVEL=debug HYP_KEY="$(HYPERLANE_MONOREPO=$(git rev-parse --show-toplevel) hypkey)" \
pnpm -C typescript/cli hyperlane status --relay --origin ethereum --dispatchTx 0xabc123...
```

### Example 2: Using message_id only (origin_chain auto-derived)

1. Find monorepo root: `MONOREPO_ROOT=$(git rev-parse --show-toplevel)`
2. Start http-registry in background via /start-http-registry
3. Query GraphQL for message `0xdef456...` → get `origin_tx_hash` and `origin_domain`
4. Check `is_delivered` - if already delivered, inform user and skip relay
5. Run:
   ```bash
   cd $MONOREPO_ROOT && \
   LOG_FORMAT=pretty LOG_LEVEL=debug HYP_KEY="$(HYPERLANE_MONOREPO=$(git rev-parse --show-toplevel) hypkey)" \
   pnpm -C typescript/cli hyperlane status --relay --origin <origin_domain> --dispatchTx <origin_tx_hash> --registry http://localhost:3333
   ```
6. Kill http-registry process
