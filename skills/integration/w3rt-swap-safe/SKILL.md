---
name: w3rt-swap-safe
description: Execute a safe two-step Solana swap (quote/simulate then explicit confirm/execute) using w3rt runtime.
homepage: https://github.com/DaviRain-Su/web3AIRuntime
metadata:
  openclaw:
    emoji: "🔁"
    requires:
      bins: ["node"]
      config: ["~/.w3rt/config.yaml"]
---

# w3rt-swap-safe

This skill performs a **two-step** swap to avoid accidental execution and to survive client retries.

## Safety rules (must follow)

1. Always run **quote** first.
2. Present a clear summary to the user (from/to/amount/slippage/route).
3. Only execute after the user explicitly confirms.
4. Start with small amounts when testing.

## Step 1 — Quote (build + simulate later)

```bash
cd /home/davirain/clawd/web3AIRuntime
node scripts/w3rt_swap_safe.mjs quote --from SOL --to USDC --amount 0.01 --slippage-bps 50
```

If Jupiter is flaky and you want to allow fallback to Meteora:

```bash
node scripts/w3rt_swap_safe.mjs quote --from SOL --to USDC --amount 0.01 --slippage-bps 50 --allow-fallback
```

This prints JSON with `quoteId`. Save it.

## Step 2 — Execute (requires explicit confirm phrase)

Only after the user confirms, run:

```bash
node scripts/w3rt_swap_safe.mjs exec --quote-id <QUOTE_ID> --confirm I_CONFIRM
```

## Output handling

- On success: show signature + Solscan link.
- On simulation failure: show the error + first ~30 logs and STOP.
- Never execute multiple times for the same `quoteId`.

## Policy

This tool honors `~/.w3rt/config.yaml` policy fields:

```yaml
policy:
  maxSlippageBps: 100
  maxSwapInputSol: 0.25
  maxSwapInputUsdc: 250
  requireConfirmPhrase: "I_CONFIRM"
```
