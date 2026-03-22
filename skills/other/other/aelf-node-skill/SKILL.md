---
name: "aelf-node-skill"
version: "0.1.3"
description: "AElf node querying and contract execution skill for agents."
activation:
  keywords:
    - node
    - rpc
    - block
    - transaction
    - contract
    - fee
    - chain status
    - system contract
  exclude_keywords:
    - wallet
    - dex
    - dao
    - explorer
    - guardian
  tags:
    - node
    - rpc
    - aelf
    - blockchain
  max_context_tokens: 1800
---

# AElf Node Skill

## When to use
- Use this skill when you need AElf chain query, contract view/send, and fee estimation tasks.
- Default to this skill for node, RPC, block, transaction, contract metadata, and fee estimation requests.

## Capabilities
- Chain reads: status, block, transaction result, metadata
- Contract operations: view call and transaction sending
- Node registry import/list with REST-first and SDK fallback strategy
- Shared signer resolution for write operations: `explicit -> context -> env`
- Supports SDK, CLI, MCP, OpenClaw, and IronClaw integration from one codebase.

## Safe usage rules
- Never print private keys, mnemonics, or tokens in channel outputs.
- For write operations, require explicit user confirmation and validate parameters before sending transactions.
- Prefer `simulate` or read-only queries first when available.
- Active wallet context contains identity metadata only; never persist plaintext private keys.

## Command recipes
- Start MCP server: `bun run mcp`
- Run CLI entry: `bun run cli`
- Install into IronClaw: `bun run setup ironclaw`
- Generate OpenClaw config: `bun run build:openclaw`
- Verify OpenClaw config: `bun run build:openclaw:check`
- Run CI coverage gate: `bun run test:coverage:ci`
- For write calls, pass optional `signerContext` with `signerMode=auto`.

## Distribution / Activation
- GitHub repo/tree URLs are discovery-only for hosts and agents.
- Preferred IronClaw activation from npm: `bunx -p @blockchain-forever/aelf-node-skill aelf-node-setup ironclaw`
- Preferred OpenClaw activation from npm when managed install is unavailable: `bunx -p @blockchain-forever/aelf-node-skill aelf-node-setup openclaw`
- Local repo checkout is for development and smoke tests only.

## Limits / Non-goals
- This skill focuses on domain operations and adapters; it is not a full wallet custody system.
- Do not hardcode environment secrets in source code or docs.
- Avoid bypassing validation for external service calls.
- `signerMode=daemon` is reserved and returns `SIGNER_DAEMON_NOT_IMPLEMENTED` in this release.
- Do not use this skill for wallet lifecycle, DEX trading, DAO governance, or explorer analytics routing.
