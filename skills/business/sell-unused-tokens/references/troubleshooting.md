# Troubleshooting

Read when the probe fails, Surplus 504s, listing returns 429, an offer shows backing off, or a Verify rail is blocked.

## Probe

| What you see | What to do |
|---|---|
| 504 / "Surplus took too long to respond" | Retry the connect once. If it 504s again, stop and tell the user Surplus timed out. |
| Host rejected that key (401/403) | Stop. The key is inactive, truncated, or from the wrong account. Do not retry with a guessed key. |
| Surplus does not support that host yet | The key was not checked. Pick a listed provider, or ask Surplus to add the host. |
| Key works but Surplus could not route any models | Wait and retry once. If it repeats, use another provider. |
| Empty model list | Stop. Do not invent models. |

Never echo the key while debugging.

## Listing

| What you see | What to do |
|---|---|
| 429 / retryAfterSec | Wait that many seconds, then retry the same model once. |
| already_listed | That model is already on `/sell` for this user. Skip it, or delete the existing listing before relisting. |
| 502 / 503 | Retry that model once. If it fails again, leave the successful rows and report the rest. |
| Ticks stall mid-batch | Client posts one model per request. Leave completed rows; retry only the failed model. |

## /sell status

| Label | Meaning | Action |
|---|---|---|
| live | Healthy and on the book | None |
| cooling | Temporary quiet | None |
| winning | Currently cheapest healthy trusted | None |
| backing off | Surplus marked it unhealthy; no traffic until retry | Wait. Replace the key only if it was revoked, exhausted, or will keep failing. |
| retrying | Health retry in flight | Wait |
| paused | Daily cap ≈ 0, or leftover hours are off | Resume from the dashboard, or wait until the leftover start time |
| syncing | House book not settled yet | Refresh `/sell` |

DELETE only flips an offer to inactive. Relisting the same key and model can return the same offer. Delete before relisting a model the user still lists.

## Cash out

| What you see | What to do |
|---|---|
| Venmo / Cash App / Wise / PayPal blocked | Desktop Chrome with USDCtoFiat Verify extension 0.2.1+. Run the in-app handshake. Do not skip it. |
| Wise / PayPal attestation | Bound to the active Privy wallet. `callerAddress` is that wallet. |
| Mercado Pago | Out. Do not offer it. |
| Want to add funds to an existing order | No top-up. Close with a full withdraw, then create a new order. |
| Inbound USDC that is not earnings | Other inbound is balance. Received earnings are Surplus relayer transfers only. |
| "That address is not mine" / wants a different payout address | It is the user's own Privy wallet, made at sign-in. `payout_address` is always the signed-in wallet, so there is no field to change it. Money leaves through Cash out or Send. |

## Support

gm@galleonlabs.io. Do not invent rails, APIs, or env values.
