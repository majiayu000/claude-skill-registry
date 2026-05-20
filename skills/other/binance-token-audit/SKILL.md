---
name: binance-token-audit
description: Binance Web3 official skill — security audit for token contracts, detecting honeypots, rug pulls, and malicious functions across BSC, Base, Solana, and Ethereum. Sourced from github.com/binance/binance-skills-hub.
metadata: { "cryptoclaw": { "emoji": "🛡️", "always": false } }
---

# Binance Token Security Audit

Official Binance Web3 skill for detecting scams, honeypots, and malicious contracts before trading.

> Source: [binance/binance-skills-hub](https://github.com/binance/binance-skills-hub/tree/main/skills/binance-web3/query-token-audit)

## Supported Chains

| Chain    | binanceChainId |
| -------- | -------------- |
| BSC      | 56             |
| Base     | 8453           |
| Solana   | CT_501         |
| Ethereum | 1              |

## API — Token Audit

```
POST https://web3.binance.com/bapi/defi/v1/public/wallet-direct/security/token/audit
Content-Type: application/json

{
  "binanceChainId": "56",
  "contractAddress": "0x...",
  "requestId": "<uuid-v4>"
}
```

`requestId` must be a valid UUID v4 (generate a new one per request).

## Risk Levels

| Level | Severity | Meaning                                    |
| ----- | -------- | ------------------------------------------ |
| 0–1   | LOW      | Lower risk detected — NOT guaranteed safe  |
| 2–3   | MEDIUM   | Moderate risks — review carefully          |
| 4     | HIGH     | Critical risks — avoid trading             |
| 5     | HIGH     | Severe confirmed risks — block transaction |

## Response Fields

- `hasResult`: whether audit data exists for this contract
- `isSupported`: whether this chain/contract is supported
- `riskLevel`: 0–5 numeric risk score
- `riskItems`: list of detected risk factors (honeypot, rug pull, malicious functions, etc.)
- `auditTime`: timestamp of audit

**Results are only valid when both `hasResult: true` AND `isSupported: true`.**

## Critical Limitations

⚠️ LOW risk does NOT mean "safe". Audit results are point-in-time snapshots only. Contract owners can modify contracts or restrict liquidity after your purchase. Always conduct your own research (DYOR).

This audit is for reference only and does not constitute investment or financial advice.

## Usage Examples

```
User: Is this contract safe to buy? 0xabc...
→ POST Token Audit, binanceChainId:56, contractAddress:0xabc...
→ Report risk level and detected risk items

User: Check this Solana token for honeypot
→ POST Token Audit, binanceChainId:CT_501, contractAddress:<address>

User: Run security check before swapping
→ Automatically call Token Audit before any swap operation
```

## Best Practice

Always run a token audit before:

- Swapping or buying an unknown token
- Adding liquidity to a new pool
- Interacting with an unfamiliar contract
