---
name: w3rt-balance
description: Check Solana balance (SOL + optional SPL tokens) using w3rt runtime via a simple Node CLI wrapper.
homepage: https://github.com/DaviRain-Su/web3AIRuntime
metadata:
  openclaw:
    emoji: "💰"
    requires:
      bins: ["node"]
      config: ["~/.w3rt/config.yaml"]
---

# w3rt-balance

Use this skill when the user asks to check SOL balance or token balances.

## Preconditions

- `~/.w3rt/config.yaml` exists
- `wallet.keyPath` points to a valid Solana keypair JSON (64-byte array)

## Command

Run:

```bash
cd /home/davirain/clawd/web3AIRuntime
node scripts/w3rt_balance.mjs
```

Optional:

```bash
# Query a specific address
node scripts/w3rt_balance.mjs --address <SOLANA_PUBKEY>

# Include SPL tokens
node scripts/w3rt_balance.mjs --include-tokens

# Only one token mint
node scripts/w3rt_balance.mjs --include-tokens --token-mint <MINT>
```

## Output handling

- Parse JSON output.
- Provide a concise summary: SOL amount, and (if requested) a short list of SPL tokens.
- If the tool returns `ok:false` or throws, surface the error and suggest verifying `~/.w3rt/config.yaml` and `wallet.keyPath`.
