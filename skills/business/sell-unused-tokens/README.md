# sell-unused-tokens

Agent skill for [tokensto.cash](https://tokensto.cash): list leftover LLM API credits, earn USDC per request, receive batched payouts on Base, cash out to fiat.

[tokensto.cash](https://tokensto.cash) · [Skill page](https://tokensto.cash/skills/sell-unused-tokens) · [skills.sh](https://www.skills.sh/galleonlabs/sell-unused-tokens) · [agentskill.sh](https://agentskill.sh/@adwilkinson/sell-unused-tokens) · [Spec](https://agentskills.io/specification)

![tokensto.cash — sell spare AI tokens for cash](https://tokensto.cash/og.png)

Prepaid and included LLM allowances expire unused. This skill walks Claude, Codex, Cursor, or any [Agent Skills](https://agentskills.io) client through listing that capacity on [Surplus Intelligence](https://www.surplusintelligence.ai) through tokensto.cash.

tokensto.cash is the seller front door. Users never SIWE with Surplus. One house seller. Payouts go to the signed-in Privy wallet.

## Install

Pin the installer. This workflow handles provider API keys and cash-out rails.

```bash
npm exec --package=skills@1.5.23 -- skills add galleonlabs/sell-unused-tokens -g -y
```

This repo is the skill folder. Copy it to:

```text
~/.claude/skills/sell-unused-tokens
~/.codex/skills/sell-unused-tokens
~/.cursor/skills/sell-unused-tokens
```

Do not resolve `npx skills` unpinned.

The `validate` GitHub Actions workflow gates this repo: installability, link health, payload disclosure, installer pin freshness. It runs on every pull request and every push to `main`. Run it locally with `bash scripts/validate.sh`. A passing merge to `main` is the release.

## What the agent does

1. Opens https://tokensto.cash/start and signs in (Privy).
2. Stops if the user has not confirmed their provider terms allow monetizing unused capacity.
3. Pastes the key into `/start` only — never echoes, logs, or stores it.
4. Lists recommended text models, one per request, floored at the cost basis.
5. Points at `/sell` for live listings and `/cash-out` for Create / Orders / Send.

Worked loop: leftover OpenRouter credits → `/start` → one text model at Leftover 0.05× → listing live on `/sell` → cash out via Revolut or, after Verify, Venmo.

Raw instructions: [`SKILL.md`](./SKILL.md). Probe and rail failures: [`references/troubleshooting.md`](./references/troubleshooting.md). Pricing and payout mechanics: [`references/invariants.md`](./references/invariants.md).

## Security

The skill runs nothing on your machine. The one executable this package ships is `scripts/validate.sh`, the maintainer's CI check, which the skill never invokes. The agent must never echo, log, commit, or transmit a provider key except into the tokensto.cash `/start` field after the user says to paste it. Surplus stores the key encrypted per listing. tokensto.cash does not persist it.

Read [SECURITY.md](./SECURITY.md).

## Cash out

- Direct: Revolut, Monzo, Chime, Zelle.
- After a one-time USDCtoFiat Verify registration (desktop Chrome, extension 0.2.1+): Venmo, Cash App, Wise, PayPal.
- Mercado Pago stays out.
- Orders close with a full withdraw. No top-up.
- Send is Base USDC. Sell and cash out have no tokensto.cash fee; Send costs 0.5% of the amount entered.

Listing is free. Earnings accrue per request; Surplus batches USDC to the signed-in wallet at $5 or after 72 hours. Cash-out, tax, and provider-account risk stay with the user.

## Compatibility

Works in Claude Code, Codex, Cursor, and any client that loads [Agent Skills](https://agentskills.io/specification). Needs network access to tokensto.cash and a browser for the user to sign in. Not an MCP server.

## License

[MIT](./LICENSE). Operator: [Galleon Labs](https://galleonlabs.io). Support: gm@galleonlabs.io.
