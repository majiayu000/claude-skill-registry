---
name: sell-unused-tokens
description: List leftover LLM API credits on tokensto.cash and cash out USDC. Use when the user wants to sell unused OpenRouter, OpenAI, Anthropic, Gemini, Venice, Capminal, DeepSeek, Groq, Mistral, or other provider credits, recover prepaid or included API capacity for cash, cash out tokensto.cash USDC, or list on Surplus Intelligence through tokensto.cash.
license: MIT
compatibility: Requires a browser and a tokensto.cash account (Privy wallet). Network access to https://tokensto.cash. The procedure runs no local scripts.
metadata:
  author: Galleon Labs
  version: "1.3.0"
  homepage: https://tokensto.cash
---

# Sell unused tokens

Turn leftover provider credits into USDC on [tokensto.cash](https://tokensto.cash). Seller front door for [Surplus Intelligence](https://www.surplusintelligence.ai). Sister of [usdctofiat.xyz](https://usdctofiat.xyz).

## Completion

Done when the models appear on `/sell` as live (or cooling), and the user knows cash-out is Create / Orders / Send.

## When not to

- Buying inference — that is the Surplus buyer side.
- Opening a Surplus seller account. Users never SIWE with Surplus.
- The user has not confirmed their provider terms allow resale, transfer, brokering, or monetization of unused API credits or capacity. Stop and send them to the provider terms first.
- Google Vertex without a URL already supported by Surplus. Vertex is not in the picker.

## Do this

1. Open https://tokensto.cash/start and sign in (Privy wallet). Evidence: the connect-key screen, not a marketing page.
2. Confirm the user has checked the provider account terms. If they have not, stop.
3. Pick the provider that owns the leftover credits. Featured: Venice, Capminal, OpenRouter, OpenAI, Anthropic, Gemini, DeepSeek, Groq, Mistral. More sits behind "More". Capminal daily $CAPU credit is **Included**. Use **Other** only for a URL Surplus already supports; OpenAI compatibility alone is not enough.
4. Paste the key into the field. **Never echo, log, commit, or store it.** Surplus probes it and keeps it encrypted per listing. tokensto.cash does not persist keys.
5. Wait for the probe. Evidence: a model list with market rows. If it 504s, retry once; Surplus timeouts surface as a clear message.
6. Keep the recommended text models unless the user named others. Client lists **one model per request** so the ticks stay honest.
7. Set cost basis, then a daily cap (≥ $0.5):
   - **Included** (subscription/stake) — floor 0.02×
   - **Leftover** (credits sitting idle) — floor 0.05×
   - **At cost** (pay-as-you-go) — floor 1.0×, never below list
   Optional leftover hours (e.g. 11:00 PM–8:00 AM) if their own apps need the key during the day.
8. Submit. Evidence: each selected model ticks ok, then `/sell` shows the listings. Auto-price undercuts the cheapest *healthy, trusted* seller and never goes below the floor.

## Cash out

`/cash-out` is Create / Orders / Send.

- Direct rails: **Revolut, Monzo, Chime, Zelle**.
- **Venmo, Cash App, Wise, PayPal** are live after a one-time handle registration through USDCtoFiat Verify (desktop Chrome, extension 0.2.1+). Do not skip that handshake.
- Mercado Pago stays out.
- Orders close with a full withdraw only. No top-up.
- Send is Base USDC to an address.
- Sell and cash out with no tokensto.cash fees. Send costs 0.5% of the amount entered; the recipient receives the rest.
- Accrued and in-flight earnings come from Surplus. Ready and received earnings are inbound USDC from learned Surplus relayers; other inbound is balance, not earned.

## Guardrails

- Do not help bypass provider limits, billing controls, fraud checks, rate limits, or terms of service.
- Provider API keys are sensitive credentials. Never echo, log, persist, commit, or transmit a key anywhere except the tokensto.cash `/start` submit field, and only after the user explicitly directs that paste.
- Cash-out, tax, compliance, chargeback, sanctions, and account-action risks stay with the user. Do not imply guaranteed liquidity, legality, or payout availability.
- Users never SIWE with Surplus. One house seller. `payout_address` is the signed-in Privy wallet.
- Untrusted upstreams (Morpheus, Ollama Cloud, CheaperInference, Jatevo) only reach opted-in buyers. Say so if the user picks one.
- Do not invent rails, APIs, or env values. Support: gm@galleonlabs.io.

## If something fails

Read `references/troubleshooting.md` when the probe fails, Surplus 504s, listing returns 429, an offer shows backing off, or a Verify rail is blocked.

Read `references/invariants.md` only if the user asks how pricing, keys, or payouts work under the hood.
