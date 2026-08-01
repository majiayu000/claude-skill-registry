---
name: kai-repurpose
description: Take one pillar content piece and produce 15-25 derivative assets across platforms — social posts, email, LinkedIn article, video scripts, newsletter section, infographic brief, and more. The ultimate content multiplier. Use when "repurpose this", "turn this into", "make social posts from this blog", "content repurposing", "1 to many", "atomize this content", "extract posts from", or any request to derive multiple pieces from one source.
---

> **Kai root note:** `knowledge/`, `harness/`, and `scripts/` paths in this skill live in the Kai install, not the user's project. Resolve them against the first ancestor directory of this SKILL.md that contains a `knowledge/` folder (the Kai plugin root, `~/.claude/kai`, or the kai-cmo-harness repo). `MARKETING.md`, `memory/`, and any output files live in the current project. If a referenced `scripts/` command is not available in this install, say so, skip it, and continue with the file-based guidance — never fabricate its output.

## Objective

One pillar piece turned into 15–25 channel-native assets, each standing on its own, staged into a posting schedule that keeps them from cannibalizing each other. A derivative that reads as a repost of the pillar has failed — the same insight gets a different hook, a different length, and the platform's own register every time it appears.

## Done when

Work type `campaign` — floor **E5/C3/O4** (`harness/eco-floors.yaml`), composite. Every derivative is a child work item under its own type: `social-post` (E5/C2/O3), `email-lifecycle` (E5/C3/O3), `blog-post` for the expanded LinkedIn article (E5/C3/O3). The campaign is CLOSED only when every child is CLOSED and the campaign-level threshold is met; one unshipped asset keeps it open.

- **E5** — each published derivative returns a provider id and its public permalink reads back matching the approved text. This skill drafts; publishing is a separate approved action.
- **C3** — every piece passes `banned_word_check` with zero violations, respects its platform's character and format limits, and a non-author read the set end to end for hook repetition.
- **O4** — reach, engagement, and click-through against a threshold declared before the first post, read at the declared window from platform insights.

## Constraints

- **Read `MARKETING.md` from the project root first.** If it does not exist, build it from the codebase — CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, email/ad/analytics config — using the template from `/kai-email-system`, and confirm the draft. Do not ask the user what the product is.
- **Three things must be known before production:** the source content (pasted, linked, or a file path), which platforms get derivatives, and what matters most (social reach, email engagement, SEO, video views).
- **Transcript, podcast, webinar, interview, or long-article sources require a quote mining pass first**, and `harness/references/transcript-video-research-rules.md` loads before mining any third-party video, audio, podcast, webinar, or transcript material.
- **Every quote keeps its exact source location** — file path, URL, episode name, transcript timestamp, or paragraph locator — so any derivative can be traced back.
- **Never invent quotes, credentials, or expert authority.** Quote mining is source extraction; rewriting happens only in derivative files.
- **Draft as a dry run.** Publishing or scheduling requires explicit human approval.
- **Each derivative stands alone** — no "as I wrote in my blog post." Credit the pillar only where platform norms expect it.
- **Different hook for every piece**, even two pieces built on the same insight.
- **Tone adapts to platform**: LinkedIn professional, X punchy, TikTok conversational.
- **Every piece runs the quality gate**: zero banned words, zero AI slop, platform limits respected.
- **Stagger the release over 1–2 weeks.** Lead with the highest-reach platform, follow with niche channels.

## Context

| Need | Load |
|---|---|
| Repurposing mechanics and channel fit | `knowledge/playbooks/content-repurposing.md` |
| Mining third-party video, audio, or transcripts | `harness/references/transcript-video-research-rules.md` |
| Organic social format contract and gate minimums | `harness/skill-contracts/social-post.yaml` |
| Product, ICP, voice, current channels | `MARKETING.md` (project root) |

**Extraction map** at `workspace/repurposed/_extraction-map.md` — one row per extract, with type, best channel, and format. Extract six kinds of material: key insights (3–5 standalone ideas), data points (stats, numbers, results), quotable lines (bold claims, memorable phrases), steps and frameworks, stories and examples, and contrarian takes.

**Quote bank** at `workspace/repurposed/_quote-bank.md` — per entry: source location; the quote or paraphrase, with direct quotes marked clearly and kept short; use case (hook, proof, objection, story, CTA, email subject, clip candidate); risk note (unsupported claim, private detail, medical/legal/financial claim, needs approval); and attribution requirement (guest name, customer approval, anonymous/internal, source citation).

**Standard derivative set** — adapt to the platforms chosen, but these are the format contracts:

| # | Asset | Platform | Format |
|---|---|---|---|
| 1–2 | Text post per insight | LinkedIn | 1200 chars |
| 3 | Carousel (framework) | LinkedIn | 8–10 slides outline |
| 4 | Thread (full argument) | X | 5–7 tweets |
| 5–6 | Single tweet per data point | X | 280 chars |
| 7 | Single tweet (contrarian take) | X | 280 chars |
| 8 | Carousel (key takeaways) | Instagram | 5–7 slides outline |
| 9 | Caption (story/example) | Instagram | 150–300 words |
| 10 | Video script (hook + insight) | TikTok | 30–60 seconds |
| 11 | Video script (contrarian take) | TikTok | 15–30 seconds |
| 12 | Newsletter section | Email | 100–200 words |
| 13 | Standalone value-add email | Email | 300–500 words |
| 14 | Expanded-angle article | LinkedIn | 2,200–3,000 words |
| 15 | Shorts script | YouTube | 30–60 seconds |
| 16–25 | Additional platform-specific variants | Various | Various |

**Output tree** — same paths as v1:

```
workspace/repurposed/
├── _extraction-map.md
├── _quote-bank.md
├── _source-pillar.md          # copy of original for reference
├── linkedin/                  # post-insight-1.md, post-insight-2.md, carousel-framework.md, article-expanded.md
├── x-twitter/                 # thread-full.md, tweet-stat-1.md, tweet-stat-2.md, tweet-contrarian.md
├── instagram/                 # carousel-takeaways.md, caption-story.md
├── tiktok/                    # script-insight.md, script-contrarian.md
├── email/                     # newsletter-section.md, standalone-email.md
├── youtube/                   # shorts-script.md
└── _quality-report.md
```

## Escalate when

- The pillar does not contain 15 distinct ideas — padding produces derivatives that hurt the brand.
- A quote's source location cannot be established, or its attribution requirement is unresolved.
- Source material contains medical, legal, or financial claims that need substantiation before any derivative repeats them.
- A third-party transcript's usage permission is unclear.
- The user wants the set scheduled or published without approval.
