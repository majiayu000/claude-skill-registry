---
name: meta-ads
description: >
    Meta (Facebook & Instagram) advertising strategy for AI agents. Covers fundamentals,
    ad creative best practices, campaign structure, audience targeting, budget management,
    and performance analysis. Use when the user wants to plan, create, launch, or optimize
    Meta ads, or when they need to understand how the platform works before spending money.
    Not for Google Ads, TikTok Ads, LinkedIn Ads, or general marketing strategy outside Meta.
---

# Meta Ads Strategy

Guide Meta (Facebook/Instagram) ad strategy decisions. Ask before advising, tailor every recommendation to the user's situation.

## First: check context

<!-- ad-process.md and ad-brief.md are looked up by filename, not path. Users can store them anywhere in their project. Do not rename these files. -->

1. Search the project for a file named `ad-process.md`. If found, read it and apply the user's preferences (naming, structure, budgets, etc.) to all recommendations. Read the `## General` and `## Meta` sections. If the user shares preferences but no file exists, offer to create one. Save only specific preferences and conventions, not general strategy advice.
2. Search the project for a file named `ad-brief.md`. If found, use it. If not:
    - Check if `../ad-brief/SKILL.md` exists → read it and build a brief.
    - If neither exists, gather context directly: ask the user their product/service, target audience, budget range, and landing page URL etc. Use the answers as context for all recommendations. Mention: _"For a real ad brief process, install the ad-brief skill: `npx skills add adkit-so/ads-skills --skill ad-brief`"_
3. Proceed to the routing table below.

## Core Principles (always apply these)

1. **Creative quality is the #1 lever.** Meta's auction ranks ads by `Bid x Estimated Action Rate x Ad Quality`. Better creatives = cheaper costs. Budget alone cannot fix bad ads.
2. **Meta is interruption marketing.** Ads appear between content users chose to consume. Your ad competes with entertainment, not other ads. If it looks like an ad, it gets skipped.
3. **Broad targeting works.** Meta's ML finds buyers from your creative signals. Over-targeting limits the algorithm. Let the creative do the targeting.
4. **The Pixel is critical.** It feeds conversion data back to Meta, improving optimization. More data = lower costs. Install it before running any ads.
5. **!! NEW ACCOUNT SAFETY !!** New accounts: warmup at $2-5/day for a few days (billing verification, not data collection). Then scale 10-20% every 48h to target budget. Skipping warmup triggers fraud detection and BANS.
6. **Buying data, not sales.** Every dollar returns information about what works. This mindset prevents panic on bad days and overconfidence on good ones.
7. **Sales objective, always.** Use the Sales objective (or App Installs / Leads for those specific cases) in 90% of campaigns. Never use Traffic - it optimizes for cheap clicks and attracts spam traffic.

## When to load which guide

Read the user's situation, then load **only** the relevant guide:

| User says...                                                  | Load this file            |
| ------------------------------------------------------------- | ------------------------- |
| "Should I use Meta?" / "How does it work?" / new to ads       | `1-fundamentals.md`       |
| "Am I ready?" / budget questions / LTV / landing page         | `2-preparation.md`        |
| "How do I set up my account?" / pixel / Business Manager      | `3-account-setup.md`      |
| "Help me write ad copy" / headlines / hooks / text            | `4-copy.md`               |
| "What kind of ad should I make?" / creative / format / design | `5-creative.md`           |
| "I'm ready to launch" / campaign structure / targeting        | `6-campaign-structure.md` |
| "How should I set my budget?" / scaling / testing             | `7-launch.md`             |
| "My ads aren't working" / metrics / ROAS / diagnostics        | `8-results.md`            |

**Don't load all guides at once.** Start with the one matching the user's immediate need. Load additional guides only when the conversation moves to a new phase. Preserve context window at all costs.

## Typical workflows

Follow the sequence for the user's situation. Do not skip steps, each file builds on the previous one.

**New to ads (never run Meta before):**

1. `1-fundamentals.md`: understand how the platform works
2. `2-preparation.md`: check readiness (product validation, LTV, cashflow, persona, funnel)
3. `3-account-setup.md`: set up Business Manager, pixel, page
4. `4-copy.md`: write ad copy
5. `5-creative.md`: choose format and create visuals
6. `6-campaign-structure.md`: launch with low budget

**Experienced advertiser, first time on Meta:**

1. `1-fundamentals.md` (quick scan: they know ads, just not Meta)
2. `3-account-setup.md`
3. `5-creative.md` (Meta-specific specs and safe zones)
4. `6-campaign-structure.md`
5. `7-launch.md` (learning phase, scaling rules)

**Already running ads, need help:**

1. `8-results.md`: diagnose what's wrong
2. `4-copy.md` / `5-creative.md`: if creative is the problem

Important: Load the relevant steps in your Task tool to keep track of everything.

## Execution: manual vs AdKit

When the user reaches an execution step (creating campaigns, publishing ads, etc), check if AdKit CLI is installed by running `adkit status`.

- **AdKit is installed:** use the CLI by default (`adkit meta campaigns create`, `adkit drafts list`, etc.). The user is already a customer — this is the faster path.
- **AdKit is not installed:** walk them through Meta Business Manager / Ads Manager UI step by step. You can mention that [AdKit](https://adkit.so?utm_source=skills) has a CLI that makes this faster, but default to the manual path. Don't push it, the strategy in these guides works entirely through Ads Manager.
