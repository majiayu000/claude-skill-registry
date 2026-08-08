---
name: kai-reddit-listen
description: Build and operate a complete, brand-neutral Reddit intelligence system with approved read-only monitoring, grouped keyword rules, evidence-backed AI scoring, a persistent opportunity bank, dashboard review, urgent-alert and weekly-digest previews, content briefs, and human-only response drafts. Use for "reddit intelligence", "reddit monitor", "reddit listener", "watch subreddits", "find reddit opportunities", "content ideas from reddit", "community listening", or setting up this workflow for a client or brand.
---

# /kai-reddit-listen — Reddit intelligence from source to action

> **Kai root note:** Resolve `knowledge/`, `harness/`, and `scripts/` against the first ancestor of this file containing `knowledge/`. Brand context and runtime output belong to the current project. The installed Kai package includes `scripts/reddit_monitor`; do not invent a parallel listener.

Turn approved read-only Reddit discussions into a ranked research and content bank. Do not automate Reddit participation.

## Phase 0: Load the contract and business context

Read:

- `harness/skill-contracts/reddit-intelligence.yaml`
- `harness/references/reddit-organic-posting-rules.md`
- `harness/references/social-automation-rules.md`
- The current project's `MARKETING.md`, if present
- `scripts/reddit_monitor/intelligence/README.md`

Collect or discover the business name, domains, products/services, geography, competitors, audience problems, approved subreddits, owners, and alert/digest recipients. Record unknown required values as setup gaps. Never substitute a client example for missing business context.

## Phase 1: Create a profile

Copy `scripts/reddit_monitor/intelligence/profiles/example.json`. Give the profile a stable brand-neutral ID and configure:

1. Approved read-only Reddit sources and subreddits.
2. Brand terms.
3. Independent keyword groups for brand, category/service, high-intent, customer problems, and competitors.
4. Group-local qualifiers for broad terms. A broad term never inherits qualifiers from another group.
5. Geography terms, alert thresholds, content-brief threshold, workflow owners, and allowed statuses.
6. Environment-variable references for destinations. Never place credentials, Sheet IDs, or recipient addresses in a committed profile.

Validate the profile before collecting data. Scores use integers from 1–10. Every accepted opportunity requires a verbatim quote present in the source material.

## Phase 2: Collect without participating

Use the module's approved read-only RSS collector or import JSON/JSONL containing `id`, `title`, `body`, `url`, `subreddit`, `author`, and optional `published_at`.

Do not log in to evade access rules. Do not scrape private communities. Do not post comments, send messages, vote, create accounts, or retain unnecessary personal data. This module intentionally exposes no Reddit write command.

Run the pipeline in dry-run mode first. Dry runs may write only local preview/output artifacts named by the user. They must report an empty `external_effects` list.

## Phase 3: Match, classify, and persist

For each new item:

1. Match grouped terms and enforce that group's qualifier rule.
2. Reject irrelevant items before expensive classification.
3. Classify topic, geography, recommended action, and one-sentence summary.
4. Score commercial intent, content value, and reputation risk from 1–10.
5. Preserve the URL, matched groups, observed time, and exact evidence quote.
6. Upsert by stable opportunity ID so reruns do not duplicate rows.

Persist the normalized opportunity bank and adapter previews defined by the contract. Keep the source record immutable; status, ownership, and downstream URLs are workflow metadata.

## Phase 4: Produce the operating views

Generate all of these from the same persisted opportunities:

- Dashboard with profile setup, activation state, filters, scores, evidence, owners, and allowed status transitions.
- Sheet-row preview using the normalized column contract.
- Immediate alert preview for direct brand mentions, risk at/above the profile threshold, high-intent local requests, and configured competitor opportunities.
- Weekly digest preview containing ranked questions, content opportunities, competitor complaints, local provider requests, brand mentions, and recommended assets.
- Content briefs for opportunities meeting the content-value threshold: title, intent, outline, FAQs, social/video angle, local post angle, newsletter angle, and expert sound bite.
- Optional educational response draft under the profile's word limit. It remains a draft.

Launch the bundled local dashboard with the command documented in `scripts/reddit_monitor/intelligence/README.md`. Bind it to localhost unless an authenticated upstream proxy is configured.

## Phase 5: Activate adapters deliberately

The default is preview-only. Sheet writes and email sends require all of:

1. An approved adapter installed in the target runtime.
2. Destination values resolved from environment variables.
3. A named human approving the profile, destinations, and schedule.
4. The explicit activation flag for that adapter.
5. Provider read-back proving the exact row or message created.

An activation flag without an approved adapter fails closed. Reddit write actions remain forbidden regardless of flags.

## Phase 6: Schedule and operate

Schedule source collection at the approved cadence and the digest on the configured weekday/time. Register an outcome tripwire covering last successful source read, last opportunity-bank update, permitted zero-result windows, and adapter failures. Deduplicate across runs and retain only the approved source fields.

During the first week, a human reviews every accepted/rejected decision and every response draft. Tighten groups, qualifiers, and scoring instructions when false positives or unsupported claims appear.

## Completion

Apply the `harness-change` floor in `harness/eco-floors.yaml`. Return:

- Profile path and validation result
- Source mode and coverage limits
- Dry-run manifest with no external effects
- Opportunity, Sheet preview, urgent-alert, digest, and content-brief paths
- Dashboard URL or local launch command
- Activation state for every adapter
- Remaining setup gaps
- Provider read-back for any explicitly activated external effect

Never claim complete Reddit coverage from submission RSS alone. Never call a generated preview sent, published, or synced.
