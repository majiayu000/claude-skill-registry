---
name: Market Scout (Crypto Rotation)
description: Scan recent macro/crypto headlines and summarize ONLY market-moving items for BTC, ETH, SOL, ADA, PAXG. Use when the user asks for a market snapshot, catalysts, or rotation context in the last 4–24 hours.
allowed-tools: Read, Grep, Glob
---

# Market Scout (Crypto Rotation)

## Instructions
1) Search project data for files:
   - news/*.md
   - intel/*.md
   - events/*.json (if present)
   Use Glob to list files and Read to open them.
2) Extract items from the last 24h. Use Grep to highlight high-impact terms:
   ETF, liquidation, funding, basis, SEC, listing, outage, tariff, CPI, FOMC, whale, hack.
3) Output a table: Time(ET) | Headline | One-line Impact | Affected Assets | Risk Regime (+/-/neutral) | Confidence(0–1) | Source
4) End with 3 bullets: What changed? What’s next 24h? What could invalidate?
