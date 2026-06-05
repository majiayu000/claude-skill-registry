---
name: kai-podcast
description: Launch a podcast or plan podcast guest strategy — format, content planning, episode production, guest outreach, and distribution. Use when "podcast", "start a podcast", "podcast marketing", "podcast guest", "podcast strategy", "be a podcast guest", "launch a show", or any request related to podcast creation or guest appearances.
---

# Kai Podcast Skill

Launch a podcast OR plan a podcast guest strategy. Two modes: Host (launch your own show) and Guest (get booked on other shows).

---

## Phase 0: Load Product Context

Check if `MARKETING.md` exists in the **project root** (same directory as CLAUDE.md, README.md, package.json).

**If it exists:** Read it — skip product discovery questions. It has the product name, ICP, value prop, monetization, brand voice, current channels, and competitive landscape.

**If it does NOT exist:** Auto-explore the codebase to create it in the **project root** (next to CLAUDE.md). Do NOT ask the user what the product is. Read CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, and any project files. Search for email/ad/analytics config. Then create `MARKETING.md` using the template from `/kai-email-system`. Present draft to user for confirmation.

---

## Phase 1: Discovery

Read from `MARKETING.md`. Only ask about things not covered there:

1. **Mode** — Are we launching a show (Host) or getting booked on shows (Guest)?
2. **Goal** — Brand awareness, thought leadership, lead gen, networking, SEO backlinks?
3. **Target audience** — Which persona(s)? Load from `E:\Dev2\kai-cmo-harness-work\knowledge\personas\_persona-index.md`
4. **Topic territory** — What subjects can we own? What's our unique angle?
5. **Existing assets** — Blog posts, talks, interviews that prove expertise?
6. **Commitment level** — Weekly, biweekly, monthly? (Host) / How many appearances per month? (Guest)
7. **Equipment/setup** — Current mic, recording, and editing capabilities

### Transcript and RSS Ingest

If the user provides an RSS feed, episode URL, transcript, raw audio, or show notes, ingest before planning derivatives.

Create `workspace/podcast/_ingest-log.md` with:
- **Source**: RSS URL, episode URL, transcript path, audio path, or show-notes path
- **Permission status**: owned, guest-approved, public citation, internal review, or unknown
- **Episode metadata**: title, guest, publish date, runtime, canonical URL
- **Transcript status**: provided, generated, partial, missing, or low confidence
- **Repurpose candidates**: quotes, stories, objections, frameworks, clip timestamps

Guardrails:
- Preserve source locations for every quote, claim, and clip candidate.
- Use public RSS metadata for planning only; do not imply endorsement by a host or guest.
- Ask for approval before publishing show notes, clips, outreach, or guest quotes.
- Do not create fake expert authority from a transcript. Attribute ideas to the right speaker or keep them as internal notes.

---

## Phase 2: Plan

### Host Mode — Launch a Podcast

1. **Load podcast channel guide**: `E:\Dev2\kai-cmo-harness-work\knowledge\channels\podcast.md`
2. **Load podcast marketing playbook**: `E:\Dev2\kai-cmo-harness-work\knowledge\playbooks\podcast-MARKETING.md`
3. **Show concept**:
   - Name (3-5 candidates, check availability)
   - Format (solo, interview, co-host, panel, hybrid)
   - Episode length (target: 20-45 min for interview, 10-20 min for solo)
   - Unique angle — Why listen to THIS show over 100 others in the category?
4. **First 10 episodes** — Map topics and guests for the launch batch
5. **Production workflow** — Record, edit, show notes, publish, promote
6. **Distribution plan** — Apple, Spotify, YouTube, RSS, website embed
7. **Promotion plan** — Social clips, email, cross-promotion, guest sharing

### Guest Mode — Get Booked on Shows

1. **Load podcast marketing playbook**: `E:\Dev2\kai-cmo-harness-work\knowledge\playbooks\podcast-MARKETING.md`
2. **Speaker positioning**:
   - 3 signature topics you can speak on
   - Unique stories/frameworks/data you bring
   - One-liner that makes a host say "I need this person on my show"
3. **Target show list** — 20-50 shows where your audience listens
4. **Pitch template** — Personalized outreach to podcast hosts
5. **Media kit** — Bio, headshot, topic list, past appearances, social proof

---

## Phase 3: Produce

### Host Mode Assets

1. **Show description** — For podcast directories (under 600 characters)
2. **Episode template** — Intro, segments, outro, CTA structure
3. **Episode outlines** — First 10 episodes with talking points
4. **Guest interview questions** — If interview format
5. **Show notes template** — Summary, timestamps, links, CTA
6. **Promotion templates** — Social posts, audiogram scripts, email announcements

### Guest Mode Assets

1. **Speaker one-sheet** — Bio, topics, audience value, past appearances
2. **Pitch emails** — 3 variants for different show sizes/types
3. **Talking points per topic** — So you're always prepared
4. **Follow-up template** — Post-appearance thank-you + content sharing plan
5. **Tracking spreadsheet structure** — Shows pitched, status, air dates, results

---

## Phase 4: Quality Gates

Validate written assets:

1. **Four U's Score**: `python E:\Dev2\kai-cmo-harness-work\scripts\quality_gates\four_us_score.py <file>`
   - Minimum: **12/16** for show descriptions and episode outlines
   - Minimum: **10/16** for emails and pitches
2. **Banned Word Check**: `python E:\Dev2\kai-cmo-harness-work\scripts\quality_gates\banned_word_check.py <file>`
3. **AI Slop Check** — No filler. Every sentence earns its place.
4. **Pitch specificity check** — Does the pitch reference the host's show specifically?

Max 2 auto-retry cycles on gate failures.

---

## Phase 5: Output

Deliver the podcast package:

### Host Mode
- **Show concept document** (name, format, angle, positioning)
- **First 10 episode outlines**
- **Production workflow checklist**
- **Distribution and promotion plan**
- **Show notes template**
- **Gate pass/fail summary**

### Guest Mode
- **Speaker one-sheet**
- **Target show list** (20-50 shows with rationale)
- **Pitch email templates** (3 variants)
- **Talking points per topic**
- **Tracking spreadsheet structure**
- **Gate pass/fail summary**

Write output to `E:\Dev2\kai-cmo-harness-work\workspace\` with filename pattern: `podcast-[host|guest]-YYYY-MM-DD.md`
