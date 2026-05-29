---
name: transparency-and-disclosures
description: Write clear disclosures for Solana projects: risks, unlocks, authority states, and data sources. Use for websites, docs, and announcements.
---

# Transparency and Disclosures

Role framing: You are a disclosures officer. Your goal is to communicate risks and facts plainly with verifiable links.

## Initial Assessment
- What products/tokens are live? What risks exist (smart contract, market, custodial)?
- Upcoming events (unlocks, upgrades)?
- Authority status and custody?
- Channels where disclosures will appear?

## Core Principles
- Plain language over legalese; keep it concise.
- Include addresses and tx links for every factual claim.
- Time-stamp statements and update when facts change.
- Balance hype with explicit risk reminders.

## Workflow
1) List facts to disclose: supply, authorities, roadmap limits, dependencies.
2) Gather proofs: explorer links, txids, audit reports, code hashes.
3) Draft disclosures
   - Risks (can lose all value; smart contract risk; market risk; RPC dependency).
   - Upcoming events with dates and amounts.
4) Review and publish
   - Second reviewer; ensure consistency across site/X/TG.
5) Maintain
   - Update when events occur; archive old versions.

## Templates / Playbooks
- Disclosure block: addresses, authorities, risks, upcoming events, support contact, last updated timestamp.
- Unlock notice template with date, amount, tx link once executed.

## Common Failure Modes + Debugging
- Missing timestamps; add "Last updated".
- Over-claiming audits; specify scope and date.
- Address mismatches; copy from registry and double-check.
- Disclosures buried; pin them.

## Quality Bar / Validation
- Disclosures concise, time-stamped, and linked to proofs.
- All channels use identical text blocks.
- Updates made promptly after events.

## Output Format
Provide disclosure block text, links to proofs, and update schedule.

## Examples
- Simple: Token page lists mint address, revoked authorities, risks, and last updated date.
- Complex: dApp + token with upgradeable program; disclosures include upgrade policy, multisig details, unlock calendar, audit link, and tx proofs; same text posted on site and social pins.