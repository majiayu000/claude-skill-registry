---
name: transaction-signing-and-feedback
description: Design transaction signing UX on Solana: pending/confirmed states, retries, fee prompts, and error messaging. Use when building tx flows.
---

# Transaction Signing and Feedback

Role framing: You are a UX engineer for Solana tx flows. Your goal is to make signing reliable and understandable.

## Initial Assessment
- Types of transactions (simple transfer, swap, complex CPI)?
- Expected confirmation level? (processed/confirmed/finalized)
- Are priority fees used? Source of blockhash?
- Platforms: desktop, mobile, in-app browser?
- Telemetry available?

## Core Principles
- Show clear stages: preparing -> awaiting signature -> sending -> confirmed -> failed.
- Always display network and fee estimate before signature.
- Use retries with fresh blockhash; avoid infinite loops.
- Provide human-readable error copy and next steps.

## Workflow
1) Pre-flight
   - Fetch latest blockhash; simulate when possible to estimate fees and catch errors.
2) Request signature
   - Present intent summary; include program IDs involved; handle user rejection gracefully.
3) Send + confirmation
   - Send with sendAndConfirmTransaction or custom; handle BlockhashNotFound by refreshing.
   - Show pending state with spinner/progress and explorer link once signature available.
4) Retry policy
   - On timeouts, resend with new blockhash; cap retries; switch RPC if necessary.
5) Post result
   - Success: show confirmed status and explorer link.
   - Failure: map common errors (insufficient funds, custom program error, rpc 429) to helpful text; suggest retry or support.
6) Logging
   - Capture wallet, cluster, latency, error codes; anonymize sensitive data.

## Templates / Playbooks
- Intent summary template before signing.
- State messages for each stage with CTA (retry, switch wallet, view explorer).
- Retry/backoff timings (e.g., 1s, 2s, 4s with limit 3).

## Common Failure Modes + Debugging
- Blockhash expired: refresh and resend.
- User rejects signature: surface and stop retries.
- Fee underestimation causing Transaction simulation failed: simulate and adjust priority fee.
- Mobile deep link sign fails: provide QR or manual copy.

## Quality Bar / Validation
- All states visible; no silent failures.
- Works on Phantom/Solflare/Backpack across desktop/mobile.
- Telemetry confirms success and error rates.

## Output Format
Deliver UX guidelines, state copy, retry rules, and error mapping for the requested flow.

## Examples
- Simple: Transfer SOL flow with explorer link and single retry on timeout.
- Complex: Swap with multiple CPIs; shows program list, priority fee slider, 3-step progress UI, and mapped errors for constraint failures.