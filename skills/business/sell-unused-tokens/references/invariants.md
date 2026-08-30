# tokensto.cash invariants

Read only when the user asks how listing, pricing, or payouts work.

## House seller

tokensto.cash holds one Surplus seller identity. Users never SIWE with Surplus and never see a seller key. Every Surplus offer CRUD call goes through the app's `sellerFetch` key pool. Always `pricing_mode: "cost_multiplier"` with `cost_multiplier`.

## Keys

The provider key is sent once to Surplus. Surplus probes it, stores it encrypted per listing, and pays for every request. This app never persists the key.

Untrusted upstreams (Morpheus, Ollama Cloud, CheaperInference, Jatevo) only route to buyers who opted in. Trusted-only is Surplus's default for buyers.

## Pricing

The repricer keeps each listing just under the cheapest healthy, trusted competitor it can beat, floored at the user's cost basis. Dead offers at the top of the book do not count, and a quote at or below the floor is ignored rather than chased: the listing undercuts the next competitor above the floor. Text models use `cost_multiplier` (per-token pricing is retired on Surplus).

Client posts one model at a time. Server accepts 1–8. Always read the live book before create.

## Money

`payout_address` is always the signed-in Privy wallet. Earnings accrue per request; Surplus batches USDC payouts on Base at $5 or after 72 hours.

Accrued and in-flight earnings come from Surplus's per-recipient payout snapshot. Ready and received earnings come from inbound USDC sent by learned Surplus relayers. Do not count all inbound as earned.

Cash-out: Revolut, Monzo, Chime, Zelle direct. Venmo, Cash App, Wise, PayPal after a one-time in-app Verify registration (`useVerifyRegistration`, `@usdctofiat/offramp/extension`, extension 0.2.1+). Same handshake as usdctofiat.xyz. Mercado Pago stays out.

Deposits on Orders are one-off: full withdraw, never top-up. Send is Base USDC.

There is no tokensto.cash fee to list or cash out. A fee-bearing Send transfers the destination amount and 0.5% Galleon fee in one atomic wallet batch. The fee rounds down to USDC precision.

## Support

gm@galleonlabs.io
