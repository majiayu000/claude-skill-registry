---
name: kai-write
description: Write a single piece of marketing content using Kai CMO Harness frameworks and quality gates. Supports blog posts, LinkedIn articles, emails, cold outreach, press releases, ad copy, and TikTok scripts. Automatically loads the right framework, skill contract, and persona. Use when "write a blog post", "draft an email", "LinkedIn article", "cold outreach", "write ad copy", "press release", "TikTok script", or any single content creation request. For building a complete email system, use /kai-email-system instead.
---

> **Kai root note:** `knowledge/`, `harness/`, and `scripts/` paths in this skill live in the Kai install, not the user's project. Resolve them against the first ancestor directory of this SKILL.md that contains a `knowledge/` folder (the Kai plugin root, `~/.claude/kai`, or the kai-cmo-harness repo). `MARKETING.md`, `memory/`, and any output files live in the current project. If a referenced `scripts/` command is not available in this install, say so, skip it, and continue with the file-based guidance — never fabricate its output.

## Objective

One piece of content in the requested format, written against the framework and contract that govern that format and clean through every gate that applies to it — copy a human can approve and publish, not a draft that needs a second author. Format is the load-bearing decision: it selects the framework, the contract, the gate thresholds, the policy reference, and the ECO floor.

## Done when

**The work type varies by format** — read it off the request, never default to one. Floors from `harness/eco-floors.yaml`.

| Format | Work type | Floor | Contract | Four U's | SEO lint |
|---|---|:--:|---|:--:|:--:|
| Blog post / SEO content | `blog-post` | E5/C3/O3 | `harness/skill-contracts/blog-post.yaml` | 12/16 | required |
| LinkedIn article | `social-post` | E5/C2/O3 | `harness/skill-contracts/linkedin-article.yaml` | 12/16 | skipped |
| TikTok script | `social-post` | E5/C2/O3 | `harness/skill-contracts/social-post.yaml` | 10/16 | skipped |
| Email (lifecycle) | `email-lifecycle` | E5/C3/O3 | `harness/skill-contracts/email-lifecycle.yaml` | 10/16 | skipped |
| Email (cold outreach) | `cold-email` | E5/C4/O3 | `harness/skill-contracts/cold-email.yaml` | 10/16 | skipped |
| Meta / Google ad copy | `paid-ad-campaign` | E5/C4/O4 | `harness/skill-contracts/meta-ads.yaml` · `harness/skill-contracts/google-ads.yaml` | 10/16 | skipped |
| Press release | `press-release` | E5/C3/O3 | `harness/skill-contracts/press-release.yaml` | 12/16 | skipped |

- **E** — a file in `workspace/` is E1. E3 is a named human approving the exact bytes; E5 is a non-actor reading the live artifact back and matching it to the approved copy.
- **C** — C2 is every gate above passing at its threshold; C3 adds a named non-producer reading it end to end; C4 (cold email, paid ads) adds the legal or platform standard verified before send.
- **O** — metric, source, baseline, threshold, window, and owner recorded *before* ship. A baseline written after ship is rejected. This skill produces the artifact and can reach C; it does not publish, and it never issues its own verdict.

## Constraints

- **Load the framework and contract before writing.** Never write from memory of the rules.
- **Ad copy loads the platform policy reference first.** Confirm the platform before drafting. Full per-platform table: `.claude/rules/architecture-and-memory.md`. Ads pass platform TOS on top of the quality gates.
- **Cold email carries legal weight.** `harness/references/cold-email-rules.md` + `harness/references/advertising-compliance.md` govern identity, opt-out, and consent basis. Hard requirements, not style notes.
- **Read `MARKETING.md` from the project root before asking anything.** If missing, build it from CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, and email/ad/analytics config using the template from `/kai-email-system`, then confirm the draft. Do not ask discovery questions the repo can answer.
- **Know three things before drafting:** the persona (one of the 8 in `knowledge/personas/_persona-index.md`), the angle (the frame, not the topic), and the single CTA. With no brief supplied, build one from `harness/brief-schema.md`.
- **Banned words — instant reject:** leverage, utilize, synergy, innovative, deep dive, circle back, touch base, moving forward, at the end of the day. **AI slop — never:** "In conclusion", "It's important to note", "In today's rapidly evolving", "This comprehensive guide", "Without further ado", "It's worth noting that".
- **X-not-Y binary clichés fail the gate in every form.** The pattern reads as LinkedIn slop and slips past subjective scoring. Failing patterns, outside HTML comments and code fences: `, not [a-z]` · `— not [a-z]` · `\bisn'?t [a-z][^.\n]+ — it'?s\b` · `\bIt'?s (a\|the\|an) [^.\n]+, not (a\|the\|an)\b` · `\bIf you [a-z][^,.]+, [a-z]` · `\bHere'?s the thing\b` · `\bLet that sink in\b` · `\bHot take\b` · `\bI'?ll be honest\b`. Fix by collapsing to a single load-bearing claim or by parallel-positive contrast where both halves are affirmative.
- **One primary CTA, word count from the contract.** SEO content also applies Algorithmic Authorship: conditions after the main clause ("Do X if Y"), instructions start with verbs, sentences under 20 words, bold the answer rather than query-matching terms.
- **Gate failures get named fixes, never rewrites.** Max 2 retry cycles, each naming the specific failing rule. After 2 failures, deliver with failures listed and log the repeated diagnosis to `memory/lessons.md`.
- **Publishing is out of scope.** Deliver with gate scores visible, saved to `workspace/` when asked; nothing goes live without human approval.

## Context

| Need | Load |
|---|---|
| Blog post / SEO content | `knowledge/frameworks/content-copywriting/algorithmic-authorship.md` + `knowledge/frameworks/aeo-ai-search/aeo-ai-search-playbook-2026.md` · `knowledge/checklists/content-checklist.md` · `knowledge/checklists/seo-checklist.md` |
| LinkedIn article | `knowledge/channels/linkedin-articles.md` |
| Email, lifecycle or cold | `knowledge/channels/email-lifecycle.md` (+ `harness/references/cold-email-rules.md` for cold) |
| Meta ads | `knowledge/channels/meta-advertising.md` + `harness/references/meta-ads-rules.md` · `knowledge/checklists/meta-advertising-checklist.md` |
| Google ads | `knowledge/channels/paid-acquisition.md` + `harness/references/google-ads-policy-reference.md` · `knowledge/checklists/paid-acquisition-checklist.md` |
| Press release · TikTok script | `knowledge/channels/press-releases.md` · `knowledge/checklists/pr-checklist.md` — `knowledge/channels/tiktok-algorithm.md` · `knowledge/checklists/tiktok-checklist.md` |
| Persona · brief · product context | `knowledge/personas/_persona-index.md` · `harness/brief-schema.md` · `MARKETING.md` (project root) |

**Gates:** `python scripts/quality_gates/four_us_score.py <file>` · `banned_word_check.py <file>` · `seo_lint.py <file>` (SEO only). If the project has `.claude/hooks/voice-gate.py`, it fires PostToolUse on Edit/Write and catches voice violations at draft time; the gate run still applies the patterns above.

## Escalate when

- The format is ambiguous and the wrong guess would change the contract, policy reference, or gate threshold.
- Ad copy is requested for a platform with no policy reference in `harness/references/`, or cold outreach where the consent basis or suppression list is unknown.
- A claim the copy depends on cannot be sourced — a quantitative claim with no source does not ship.
- The piece still fails a gate after two targeted fixes.
- The request is a full email system rather than one piece — that is `/kai-email-system`.
