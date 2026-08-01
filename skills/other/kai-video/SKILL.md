---
name: kai-video
description: Produce video scripts and clipping plans for TikTok, YouTube Shorts, Instagram Reels, and long-form YouTube. Generates hook-first scripts optimized for each platform's algorithm, plus a clipping plan to extract short-form from long-form content. Use when "video script", "TikTok script", "YouTube script", "Reels script", "Shorts script", "video content", "clipping plan", "video ideas", or any request to create video content for social platforms.
---

# /kai-video — shootable scripts and a defensible clip list

> **Kai root note:** `knowledge/`, `harness/`, and `scripts/` paths in this skill live in the Kai install, not the user's project. Resolve them against the first ancestor directory of this SKILL.md that contains a `knowledge/` folder (the Kai plugin root, `~/.claude/kai`, or the kai-cmo-harness repo). `MARKETING.md`, `memory/`, and any output files live in the current project. If a referenced `scripts/` command is not available in this install, say so, skip it, and continue with the file-based guidance — never fabricate its output.

## Objective

Scripts someone can shoot without asking a follow-up question, and — where long-form source exists — a clipping plan naming which moments become short-form, at which timestamps, and why. Hook-first and platform-specific: the first three seconds decide whether the rest of the work matters.

## Done when

Work type `social-post` — floor **E5/C2/O3** (`harness/eco-floors.yaml`), contract `harness/skill-contracts/social-post.yaml`.

- **E5** — the video is live and a non-actor read the public permalink back against the approved script and cut. A script file in `workspace/` is E1; approval of the exact script is E3. This skill reaches the artifact; publishing is a separate, approved step.
- **C2** — `four_us_score` at 10/16 and `banned_word_check` clean on the script copy, plus the per-script bar below.
- **O3** — reach, engagement rate, profile clicks, and link clicks read from platform insights at 7 days, against a baseline recorded before publish.

**Per-script bar:** hook lands in the first 3 seconds (no intros, no "hey guys", no logo animation) · one idea per short-form video · zero banned words and zero AI slop · a CTA that closes naturally rather than being bolted on · visual direction included, not words alone · length appropriate to the platform.

## Constraints

- **Read `MARKETING.md` from the project root before asking the user anything.** If it does not exist, build it from the codebase — CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, email/ad/analytics config — using the template from `/kai-email-system`, and confirm the draft.
- **Know these before scripting:** topic, target platforms, format (talking head, screen recording, b-roll, animation), length band (15–60s short-form or 5–15min long-form), goal, and any existing content to adapt from.
- **Load the platform guide before writing for that platform** — the algorithms differ and the pacing rules are not transferable.
- **Every clip row carries a source timestamp or file locator.** If the source is a guest, customer, podcast, or third-party show, mark approval status before export and follow `harness/references/transcript-video-research-rules.md`.
- **Clip plans are dry runs.** Publishing or upload requires human approval.
- **Vary the hook formula across videos.** Repeating one formula across a slate trains the audience to skip.

## Context

| Need | Load |
|---|---|
| Video content mechanics | `knowledge/playbooks/video-content-creation.md` |
| TikTok | `knowledge/channels/tiktok-algorithm.md` |
| YouTube (Shorts and long-form) | `knowledge/channels/youtube.md` |
| Instagram Reels | `knowledge/channels/instagram.md` |
| Clipping long-form into short-form | `knowledge/playbooks/video-clipping-automation-workflow.md` |
| Any transcript, caption, podcast, webinar, or third-party source | `harness/references/transcript-video-research-rules.md` |
| Product, ICP, voice, channels | `MARKETING.md` (project root) |

**Short-form script (15–60s)** carries: platform, length, format, HOOK (0–3s, pattern interrupt — question, bold claim, or visual surprise), BODY (3–45s, one idea and one takeaway with bracketed visual direction), CTA (last 3–5s), timestamped on-screen text overlays, 3–5 platform-appropriate hashtags, and a trending-audio suggestion or "original audio".

**Long-form script (5–15min)** carries: HOOK (0–30s previewing the payoff), INTRO (30s–1min: context, credibility, structure promise), three content sections with visual direction, RECAP + CTA, chapter timestamps, and a thumbnail concept (3–5 words of title text, expression, key visual).

**Hook formulas** — rotate across a slate:

| Type | Formula | Example |
|---|---|---|
| Question | "Did you know [surprising fact]?" | "Did you know 73% of leads call after hours?" |
| Bold claim | "[Contrarian statement]" | "Cold email is dead. Here's what replaced it." |
| Problem | "If you're struggling with [X]..." | "If your landing page converts under 3%..." |
| Result | "We went from [bad] to [good] in [time]" | "We went from 2% to 11% conversion in 3 weeks" |
| List | "[Number] [things] that [outcome]" | "5 emails every SaaS needs on day one" |

**Clip scoring** — score every candidate before scripting it, 1–5 per factor:

| Factor | Question |
|---|---|
| Hook | Do the first 3 seconds create a clear reason to keep watching? |
| Standalone clarity | Can the viewer understand the moment without the full source? |
| Proof | Does it include a concrete example, result, quote, or demo moment? |
| Tension | Does it contain contrast, surprise, objection, stakes, or a reveal? |
| Source safety | Is the claim attributable and cleared for use? |

Clips scoring **18/25 or higher** are production candidates. Lower scores go to `workspace/video/clipping-plan/_kill-list.md` with the reason.

**Output** goes to `workspace/video/`: `_video-plan.md`, `short-form/` (per-platform scripts), `long-form/`, `clipping-plan/clips-from-[source].md`, `_quality-report.md`.

## Escalate when

- Source footage rights, guest approval, or customer permission for a clip is unconfirmed.
- A claim in the script needs a number that has no source.
- The requested length or format conflicts with the platform's current norms in the loaded channel guide.
- The user wants the video rendered rather than scripted — that is `/kai-video-production`.
- Anything would be uploaded or published before human approval.
