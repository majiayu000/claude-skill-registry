---
name: kai-podcast
description: Launch a podcast or plan podcast guest strategy — format, content planning, episode production, guest outreach, and distribution. Use when "podcast", "start a podcast", "podcast marketing", "podcast guest", "podcast strategy", "be a podcast guest", "launch a show", or any request related to podcast creation or guest appearances.
---

> **Kai root note:** `knowledge/`, `harness/`, and `scripts/` paths in this skill live in the Kai install, not the user's project. Resolve them against the first ancestor directory of this SKILL.md that contains a `knowledge/` folder (the Kai plugin root, `~/.claude/kai`, or the kai-cmo-harness repo). `MARKETING.md`, `memory/`, and any output files live in the current project. If a referenced `scripts/` command is not available in this install, say so, skip it, and continue with the file-based guidance — never fabricate its output.

## Objective

A podcast operation the user can start next week — either their own show (Host mode) or a booked-guest pipeline (Guest mode). Host mode ends with a show concept, ten mapped episodes, a production and distribution workflow, and the templates that keep every episode consistent. Guest mode ends with a speaker one-sheet, a real target-show list, and pitches specific enough that a host replies.

Pick the mode before anything else. Host and Guest share almost no assets.

## Done when

Work type `strategy-plan` — floor **E3/C3/O1** (`harness/eco-floors.yaml`). The package is a plan, not a live channel, so E tops out at approval of the exact bytes.

- **E3** — a named human approved the delivered package at `workspace/podcast-[host|guest]-YYYY-MM-DD.md`.
- **C3** — `banned_word_check` clean, zero AI slop (every sentence earns its place), Four U's at **12/16** for show descriptions and episode outlines and **10/16** for pitch emails, and a non-author read the package end to end. Max 2 retry cycles, each naming the specific failing dimension.
- **O1** — the plan names its metric with a baseline, a threshold, a window, and an owner: episodes published and downloads per episode (Host), or pitches sent, booking rate, and appearances aired (Guest).

Two floors this skill does not own: an episode actually published is `blog-post`-class published content, and a pitch email actually sent is `cold-email` (E5/C4/O3). Neither is SHIPPED by this skill.

## Constraints

- **Read `MARKETING.md` from the project root first.** If it does not exist, build it from the codebase — CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, email/ad/analytics config — using the template from `/kai-email-system`, and confirm the draft. Do not ask the user what the product is.
- **Know these seven things before planning:** mode (Host or Guest); goal (awareness, thought leadership, lead gen, networking, backlinks); target persona; topic territory and unique angle; existing assets that prove expertise; commitment level (cadence for Host, appearances per month for Guest); equipment and editing capability.
- **Ingest before deriving.** Given an RSS feed, episode URL, transcript, raw audio, or show notes, record it in `workspace/podcast/_ingest-log.md` first: source locator, permission status (owned / guest-approved / public citation / internal review / unknown), episode metadata (title, guest, publish date, runtime, canonical URL), transcript status (provided / generated / partial / missing / low confidence), and repurpose candidates (quotes, stories, objections, frameworks, clip timestamps).
- **Source locations are preserved for every quote, claim, and clip candidate.** Public RSS metadata is for planning only — it never implies a host or guest endorses anything.
- **No fabricated authority.** Ideas from a transcript are attributed to the speaker who said them or kept as internal notes. Never present transcript material as the user's own expertise.
- **Approval before anything leaves the workspace** — show notes, clips, outreach, and guest quotes all require human sign-off. This skill drafts.
- **Pitch specificity is a hard rule.** A pitch that does not reference the specific show — an episode, a recurring theme, the host's stated interest — fails regardless of its Four U's score. Generic pitches are the reason guest outreach dies.
- **Guest pitches are cold outreach.** Sender identity, opt-out, and consent basis follow `harness/references/cold-email-rules.md` before any send.
- **Format targets:** show description under 600 characters for directories; 20–45 min interview episodes, 10–20 min solo; 3–5 candidate show names with availability checked; 20–50 target shows for Guest mode.

## Context

| Need | Load |
|---|---|
| Show format, production, distribution mechanics | `knowledge/channels/podcast.md` |
| Launch strategy, guest booking, promotion | `knowledge/playbooks/podcast-marketing.md` |
| Which persona the show is for | `knowledge/personas/_persona-index.md` |
| Rules for mining third-party audio, video, or transcripts | `harness/references/transcript-video-research-rules.md` |
| Cold outreach compliance for host pitches | `harness/references/cold-email-rules.md` |
| Product, ICP, voice, current channels | `MARKETING.md` (project root) |
| Turning one episode into channel assets | `/kai-repurpose` |

**Host package:** show concept (name, format, length, angle), first ten episode outlines, production workflow, distribution plan (Apple, Spotify, YouTube, RSS, website embed), promotion plan (social clips, email, cross-promotion, guest sharing), episode template, show notes template, interview question set.

**Guest package:** speaker one-sheet (bio, three signature topics, audience value, past appearances), target show list with rationale, three pitch variants sized to different shows, talking points per topic, post-appearance follow-up, and a tracking structure covering shows pitched, status, air dates, and results.

**Output** goes to `workspace/` as `podcast-[host|guest]-YYYY-MM-DD.md`. Ingest notes go to `workspace/podcast/_ingest-log.md`. Same paths as v1.

## Escalate when

- Permission status for a transcript, clip, or guest quote is unknown and the asset is needed.
- The user wants a guest quote or host endorsement published without written approval.
- The claimed expertise behind a signature topic is not supported by any existing asset.
- Cadence commitment does not match available production capacity — a show that dies at episode four is worse than no show.
- A pitch would require claiming an experience or result the user does not have.
