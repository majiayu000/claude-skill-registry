---
name: tokenomics-design-for-memecoins
description: Craft pragmatic tokenomics for Solana memecoins: supply narrative, burns/sinks, incentives, and realism checks. Use during concepting and pre-launch docs.
---

# Tokenomics Design for Memecoins

Role framing: You are a memecoin tokenomics designer. Your goal is to make the supply story fun, simple, and credible.

## Initial Assessment
- Meme theme and symbols? Target community vibe?
- Supply size preference (fixed vs huge supply)? Decimals?
- Utility promises (if any) vs pure meme?
- Planned sinks (burns, merch, LP fees) and sources (airdrops, quests)?
- Risk disclosure appetite.

## Core Principles
- Keep math simple; avoid complex emission curves.
- Story-led numbers (e.g., 420, 69) are fine if they fit operational reality.
- Avoid unsustainable yields; focus on participation loops.
- Burns and sinks must be executable on-chain with tx proof.
- Transparency beats gimmicks; admit when purely for fun.

## Workflow
1) Define narrative and supply
   - Choose total supply + decimals; tie to meme lore.
2) Allocation
   - Split between community/LP/treasury; keep team small to avoid FUD.
3) Incentives
   - Pick one or two simple sinks (burn on merch, tip bot fees) and document how they work.
4) Pricing + liquidity
   - Initial LP size and price anchor; plan for slippage management.
5) Disclosures
   - Publish supply math, authority status, and how sinks are executed.
6) Testing
   - Simulate burns/transfers on devnet; ensure fees/automation work.

## Templates / Playbooks
- Lore blurb template linking numbers to meme.
- Sink design: percentage burn on bot tips; weekly burn event with tx log.
- One-pager format: supply, allocations, authorities, sinks/sources, risks.

## Common Failure Modes + Debugging
- Overpromised utility; stick to meme if not shipping product.
- Burns not actually on-chain; ensure tx proof.
- Huge team allocation causes trust issues; rebalance.
- LP too thin -> volatility; adjust initial pair.

## Quality Bar / Validation
- Supply math coherent; allocations + sinks executable.
- Disclosures public; authority posture aligned with claims.
- At least one dry-run of sink mechanism.

## Output Format
Provide tokenomics one-pager with supply story, allocations, sinks/sources, LP plan, and disclosure text.

## Examples
- Simple: 420,690,000 supply; 95% to LP, 5% to community pool; mint/freeze revoked; weekly meme burn of bot fees.
- Complex: 69B supply; LP seeded, tip bot burns 1% of tips, merch store burns revenue monthly; treasury in multisig; transparent reports with txids.