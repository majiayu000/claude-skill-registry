---
name: podcast-production
description: Produce podcast episodes from Notion transcript to a single editor handoff document. Three phases with two human decision points.
---

# Podcast Production Skill (v2)

Transform a podcast transcript into a single **EDITOR_HANDOFF.md** - the one document your video editor needs. Three phases, two human checkpoints, converging on one deliverable.

**Previous version:** `SKILL_v1_archive.md` (4-checkpoint system, retired Feb 2026)

---

## The Pipeline

```
PHASE 1: SETUP (automated, no LLM needed for import)
  Step 0:   Import from Notion → SOURCE.md
  Step 0.5: Guest social research → GUEST_SOCIAL_RESEARCH.md
  Step 1:   SEO keyword research → SEO_Keywords.md

PHASE 2: AUDIT + HUMAN REVIEW
  Step 2:   Audit (angles, clips, cold opens, blog format assessment)
            → Checkpoint_1_Audit.md
  ────────── HUMAN CHECKPOINT: Select angle + approve clips ──────────
  Step 3:   Title + thumbnail variations (YouTube title + blog title)
            → Title_Options_By_Angle.md
  ────────── HUMAN CHECKPOINT: Select title + thumbnail ──────────

PHASE 3: HANDOFF ASSEMBLY (converges to one document)
  Step 4:   On-screen hook generation (3-4 per clip, * on recommended)
  Step 5:   Final clip markup (3 short + 2 long, edit-ready)
  Step 6:   Cold open assembly (2-3 options from selected clips)
  Step 7:   YouTube description + chapters (single code block, includes blog + transcript links)
  Step 8:   Narrative snippets extraction → blog post draft
  Step 9:   Social tagging strategy + platform post drafts
  Step 10:  Blog thumbnail + infographic generation (nano-banana-image-generator)
            → 3 Notion subpages + images in handoff folder
```

---

## Folder Structure

```
Studio/Podcast Studio/[Guest-Name]/
└── prep/
    ├── SOURCE.md                    # Raw transcript from Notion
    ├── GUEST_SOCIAL_RESEARCH.md     # Handles, platforms, reshare strategy
    ├── SEO_Keywords.md              # Keyword volumes + blog direction
    ├── Checkpoint_1_Audit.md        # Angles, clips, cold opens
    ├── Title_Options_By_Angle.md    # Framework-fit titles organized by angle
    ├── EDITOR_HANDOFF.md            # Combined reference (all sections)
    ├── POLISHED_TRANSCRIPT.md       # Cleaned transcript for publication
    └── notion-export/              # Files that map 1:1 to Notion subpages
        ├── editor-handoff.md        # → Notion subpage: "Editor Handoff"
        ├── youtube-and-transcript.md # → Notion subpage: "YouTube + Polished Transcript"
        └── blog-and-social.md       # → Notion subpage: "Blog Post + Social"
```

---

## Phase 1: Setup

### Step 0: Import from Notion

```bash
python3 /Users/charliedeist/Desktop/New\ Root\ Docs/.claude/scripts/notion_import.py <page_id> --title -o "Studio/Podcast Studio/[Guest-Name]/prep/SOURCE.md"
```

No LLM tokens. Direct Notion API to markdown. Creates the folder structure automatically.

To find page IDs for recorded episodes, query the Podcast Master Calendar Notion database (`d60323d3-8162-4cd0-9e1c-1fea5aad3801`) filtering for `Status = Recorded`.

### Step 0.5: Guest Social Research

Run a web search sub-agent to find:
- All personal + company handles (LinkedIn, X, IG, TikTok, YouTube)
- Which platform is their strongest (by engagement, not follower count)
- What kind of content they typically post/share
- Mutual connections with OpenEd
- Collaboration history (have they shared our content before?)

Output: `GUEST_SOCIAL_RESEARCH.md`

This informs clip selection (which platforms matter?) and social strategy (tagging, reshare potential).

### Step 1: SEO Keyword Research

Use DataForSEO to research 5-7 keywords related to the guest's topic. Focus on:
- Guest name + company (branded volume)
- Core topic terms (e.g., "microschool", "how to start a microschool")
- Related high-intent queries

Output: `SEO_Keywords.md` - consolidated summary, not individual briefs.

This informs title selection and blog post direction. YouTube title and blog title should be DIFFERENT:
- **YouTube title** = CTR optimized (curiosity, emotion, pattern interrupt)
- **Blog title** = SEO optimized (target keyword in title, search intent match)

---

## Phase 2: Audit + Human Review

### Step 2: Audit

Send to an Opus sub-agent with the full SOURCE.md. The audit produces:

1. **Angles** (3-5 distinct marketing angles, each with a 1-sentence pitch)
2. **Short clips** (5-8 candidates, 30-90 sec each)
   - Verbatim quotes with timestamps
   - Category: Counterintuitive / Memorable / Relatable / Practical / Emotional
3. **Long clips** (3-4 candidates, 2-5 min each)
   - Narrative arc summary
   - Opening hook verbatim
4. **Cold open candidates** (2-3 montage arrangements using [SWOOSH] transitions)
5. **Blog format assessment** - Is this a "day-in-the-life" candidate or standard blog?
6. **Timestamp index** - Full chapter-by-chapter breakdown

**CRITICAL RULES:**
- All quotes VERBATIM. Never paraphrase.
- Mine the ENTIRE transcript, not just the first half.
- Bold over safe. Surprising, contrarian moments beat obvious observations.
- Target 5-8 clips in the audit (mine broadly), user will whittle to 5 final.

Output: `Checkpoint_1_Audit.md`

**Sub-agent prompt template:**
```
You are auditing a podcast transcript for content production.

Episode: [Guest Name]
Working directory: [path to prep/]

Read SOURCE.md (the full transcript).

Produce Checkpoint_1_Audit.md with:
- 3-5 angles (1-sentence pitch each)
- 5-8 short clip candidates (30-90 sec, verbatim with timestamps)
- 3-4 long clip candidates (2-5 min, narrative arc + opening hook verbatim)
- 2-3 cold open montage arrangements
- Day-in-the-life assessment (yes/no with reasoning)
- Full timestamp index

Rules: ALL quotes verbatim. Mine the entire transcript. Bold over safe.
```

### HUMAN CHECKPOINT 1

Present the audit summary. User selects:
- **Primary angle** (which direction for the episode)
- **5 clips** (3 short + 2 long) from the candidates
- **Cold open preference** (or direction for assembly)
- **Blog format** (standard or day-in-the-life)

### Step 3: Title + Thumbnail Variations

After angle selection, generate titles using the `youtube-title-creator` skill:
- 5 titles per angle using the 119 Creator Hooks frameworks
- Each title includes: framework reference, psychological principles, thumbnail text suggestion
- Organize by angle so user can see which direction has the strongest title

**VERIFICATION RULE:** Any specific claim in a title (numbers, named concepts, frameworks) must cite the transcript moment that supports it. Never let a framework template inject a claim that isn't in the source.

**Retain 5+ title options per angle** to give the associate/editor room to weigh in. Don't over-filter.

After user narrows to 3-4 title finalists, produce 3 thumbnail concepts per title:
- Visual description (what the thumbnail image shows)
- On-screen text (2-4 words, complements title - never repeats it)
- Why this pairing works

Output: `Title_Options_By_Angle.md`

### HUMAN CHECKPOINT 2

User selects:
- **YouTube title** (CTR optimized)
- **Blog title** (SEO optimized, different from YouTube)
- **Thumbnail direction**

---

## Phase 3: Handoff Assembly

Everything converges into **3 Notion subpages** under the episode's master Notion page. Each subpage is generated from a local markdown file in `prep/notion-export/`.

### Output: 3 Notion Subpages

**Subpage 1: Editor Handoff** (`notion-export/editor-handoff.md`)
```markdown
# Editor Handoff: [Guest Name], [Company]

## Episode Info
- Guest, host, duration
- YouTube title (selected)
- Blog title (selected)
- Thumbnail text options (3, * on recommended)

## Cold Opens
- 2-3 options, each 25-35 seconds
- Verbatim with ~~strikethrough~~ for cuts, *italics* for smoothing
- [SWOOSH] between unrelated moments
- Source timestamps for each segment

## Short Clips (3 total)
For each clip:
- Timestamp range
- On-screen hook options (3-4, * next to recommended)
- Full verbatim transcript with edit markup
- Caption (universal for FB, TikTok, IG, LinkedIn)
- X variant

## Long Clips (2 total)
For each clip:
- Timestamp range
- Narrative arc (setup → tension → payoff)
- On-screen hook options (3, * next to recommended)
- Opening hook verbatim
- Caption + X variant

## Edit Markup Key
```

**Subpage 2: YouTube + Polished Transcript** (`notion-export/youtube-and-transcript.md`)
```markdown
# YouTube + Polished Transcript: [Guest Name]

## YouTube Title
[Selected title]

## Thumbnail Options
1. "[Text]" *
2. "[Text]"
3. "[Text]"

## YouTube Description
(Single code block - copy-paste ready. Includes:)
- Episode summary (2-3 sentences)
- Blog link: "Read the full blog post: opened.co/blog/[slug]" (ABOVE timestamps)
- Guest bio + social handles + resources
- OpenEd links
- Chapters (at the bottom)
- NO "In this episode you'll learn" bullet section
- NO transcript anchor link

## Blog Slug
[slug] → Full URL: https://opened.co/blog/[slug]

## Polished Transcript
(Generated from SOURCE.md. Section headers match chapter breakdown.
Appended to blog post under #transcript anchor.)
```

**Subpage 3: Blog Post + Social** (`notion-export/blog-and-social.md`)
```markdown
# Blog Post + Social: [Guest Name]

## SEO Metadata
- Blog title (SEO optimized), target keyword, search volume, blog slug

## Blog Post
- Full blog post draft (~1,200 words)
- Internal backlinks to relevant OpenEd content
- Guest handles + URLs in About section at bottom

## Social Tagging Strategy
- Guest handles per platform (table format)
- Platform priority ranking with reasoning

## Platform-Specific Post Drafts
For each platform, 1-2 ready-to-post drafts:
- **LinkedIn** (2 posts: episode announcement + mid-week angle)
- **X/Twitter** (2 posts: announcement + quote/stat hook)
- **Instagram** (2 posts: carousel concept + quote card)
- **Facebook** (1 post: full episode share)

## Distribution Timing
- Week 1: Launch day (all platforms) + staggered follow-ups
- Week 2: Evergreen angles (repurposed quotes, stats)
- Ongoing: Guest reshare coordination
```

### Step 8: Blog Post (Narrative Snippets Method)

Before writing the blog post, extract narrative beats from the transcript:

1. **Scan for story seeds** - transitions, contrast markers, failure admissions, turning points
2. **Extract 3-5 narrative arcs** using the 6-beat structure:
   - SETUP → DISASTER → FAILED APPROACH → INSIGHT → RESOLUTION → REFLECTION
3. **Pick one arc as the spine** of the blog post
4. **Weave other arcs** as supporting threads

The blog post should read like a great New Yorker profile at blog scale - observational, unhurried, letting scenes and quotes do the work. Voice: Ela (warm, curious, conversational) elevated by narrative craft.

**Blog post sub-agent reads:** SOURCE.md + GUEST_SOCIAL_RESEARCH.md + blog direction from subpage 3
**Blog post sub-agent uses:** `narrative-snippets` → `podcast-blog-post-creator` → `ghostwriter`
**Output:** ~1,200 word draft with SEO headers, 3-5 verbatim quotes, YouTube embed placeholder

**Integration requirements:**
- Include guest handles and URLs from GUEST_SOCIAL_RESEARCH.md (bio links, company URL)
- Scan published OpenEd content for internal backlinking opportunities (link to relevant articles, guides, and other podcast episodes)
- About section at bottom must include guest social handles with links

### Blog Slug Convention

Generate the slug during Phase 3 so it can be embedded in the YouTube description before publishing.

**Pattern:** `opened.co/blog/[seo-keyword-slug]`
**YouTube description must include:**
- `Read the full blog post: https://opened.co/blog/[slug]` (placed ABOVE timestamps)

### Step 10: Blog Thumbnail + Infographic

Generate visual assets using the `nano-banana-image-generator` skill. Save all images in the **handoff folder** alongside the markdown files.

**Required assets:**
1. **Blog thumbnail** (16:9, watercolor-line style) - conceptual illustration for the blog post header and Webflow CMS
2. **Infographic** (16:9, watercolor-line with Vox-style hierarchy) - data visualization or concept map for social sharing

**Optional assets (if the episode warrants them):**
- Quote card (1:1, opened-editorial style) - for Instagram/LinkedIn
- Instagram carousel intro slide (4:5, watercolor-line)

**Workflow:**
```bash
# Blog thumbnail
python3 ".claude/skills/nano-banana-image-generator/scripts/generate_image.py" \
  "prompt" --model pro --aspect 16:9 \
  --seo-name "[guest-slug]-podcast-thumbnail" \
  --context "[Blog title]" \
  --output "Studio/Podcast Studio/handoff-packages/[Guest-Name]/"

# Optimize for Webflow
python3 ".claude/skills/nano-banana-image-generator/scripts/image_optimizer.py" \
  "Studio/Podcast Studio/handoff-packages/[Guest-Name]/[file].jpg" \
  --use thumbnail
```

**Style selection guide:**
- **watercolor-line** (DEFAULT) - Warm, editorial, works for narrative/emotional episodes
- **opened-editorial** - Conceptual wit, better for data-driven or contrarian episodes
- **minimalist-ink** - High contrast, good for "bold statement" thumbnails

**Concept brainstorm:** Before generating, brainstorm 4-6 visual concepts with the user. Avoid generic education cliches (no lightbulbs, no raised hands, no stacks of books). Favor metaphor over literal depiction.

**Infographic principles:**
- Visual hierarchy does the work, not text
- Labels only, no explanatory paragraphs
- Icons should be hand-drawn style (not emoji)
- Clear left-to-right or top-to-bottom flow
- Pull key stats from the transcript (the guest's own data is most compelling)

### Notion Export

Push each subpage using:
```bash
python3 .claude/scripts/notion_markdown.py [file] --parent-id [episode-page-id] --title "[Subpage Title]"
```

Never use `--update` on the master episode page (it overwrites). Always create subpages.

### On-Screen Hook Standards

On-screen text is the #1 visual element. It does the PRIMARY work of stopping a scroll.

**Requirements per clip:**
- 3-4 hook options per clip
- Star (*) next to recommended pick
- No category labels, no rationale - just the options

**Hook categories:**
- **Polarizing** - Takes a side. "Schools trap families?"
- **Counter-Intuitive** - Surprises. "The school choice argument nobody makes"
- **Direct Challenge** - Confronts viewer. "Your kid's teacher hates their job"
- **Curiosity Gap** - Opens a loop. "55% want to quit"

**Complementarity principle:** On-screen text should ADD context that makes the audio land harder, not just label the clip. The gap between what you read and what you hear creates curiosity.

**"First 3 words" test:** The first 3 words someone reads do 80% of the work. Front-load the punch.

**Length variety (REQUIRED):** Every set of 3-4 hook options must span at least 2 length categories:
- **Punchy** (2-4 words): "Schools trap families?"
- **Statement** (5-8 words): "The school choice argument nobody makes"
- **Narrative** (9-15 words): "There's a cost every morning when a five-year-old walks in and knows"
- **Full quote** (15+ words): "If your strategy for keeping families is making sure they can't leave, you've lost"

If all hooks are the same length, redo them. The editor needs options that work at different scroll speeds.

### Edit Markup Convention

```
~~strikethrough~~ = cut this (editor removes)
*italics* = minor smoothing edit (change spoken word)
[SWOOSH] = visual transition between unrelated segments
[AMAR] = speaker label
```

---

## Key Principles

1. **Verbatim only.** All quoted transcript exactly as spoken. Cut and rearrange, never paraphrase.
2. **Three subpages.** Everything flows into 3 Notion subpages: Editor Handoff, YouTube + Transcript, Blog + Social.
3. **Mine the whole transcript.** The strongest moment might be at minute 48.
4. **Bold over safe.** Contrarian > obvious. Tension > comfort.
5. **5 clips total.** 3 short (30-90 sec) + 2 long (2-5 min). Quality over quantity.
6. **Same caption everywhere.** One caption per clip for FB/TikTok/IG/LinkedIn. Optional X variant.
7. **Title + thumbnail are a pair.** Design them together. Thumbnail complements, never repeats.
8. **YouTube title != blog title.** YouTube = CTR. Blog = SEO.
9. **On-screen hooks are the #1 priority.** 3-5 variations per clip, not afterthoughts.
10. **Guest research informs everything.** Know their platforms before selecting clips.

---

## Skill Dependencies

| Step | Skills Used |
|------|-------------|
| Step 0 | `notion_import.py` (script, not skill) |
| Step 1 | `seo-research` / DataForSEO |
| Step 3 | `youtube-title-creator` (119 frameworks) |
| Step 4 | `video-caption-creation` (hook categories, Triple Word Score) |
| Step 6 | `cold-open-creator` (optional reference) |
| Step 8 | `narrative-snippets` (extract beats) → `podcast-blog-post-creator` → `ghostwriter` (voice) |
| Step 8 alt | `day-in-the-life` (if applicable) |
| Step 10 | `nano-banana-image-generator` (thumbnail + infographic) |
| Quality | `quality-loop` (for blog post draft) |

---

## Common Mistakes

- Fabricating claims in titles (e.g., "6 Levels of Teaching" when transcript has no such framework)
- Single on-screen hook per clip instead of 3-5 options
- Generating platform-specific captions (same caption everywhere, X variant only)
- Thumbnail text that repeats the title
- Ignoring guest's social presence until the end
- SEO research after title selection instead of before
- Cold opens before clip selection (cold opens are assembled FROM clips)
- 25+ snippet inventory when 5-8 targeted clips is better

---

## Next Priorities (Skill Improvements Backlog)

- [ ] Build `youtube_autocomplete.py` using DataForSEO for YouTube search suggestions
- [ ] Research exemplar podcast YouTube/IG channels for on-screen hook reference library
- [ ] Improve `video-caption-creation` skill with complementarity principle + real education creator examples
- [ ] Build dedicated title+thumbnail sub-agent with better variation examples from Creator Hooks
- [x] Add internal linking step (integrated into Step 8 blog post sub-agent)

---

## References

- `references/checkpoint-1-template.md` - Detailed audit template
- `references/checkpoint-2-example.md` - Cold open + clip example (Claire Honeycutt)
- `references/checkpoint-3-example.md` - YouTube strategy example
- `references/checkpoint-4-example.md` - Polished transcript + blog example
- `references/day-in-the-life-format.md` - Day-in-the-life blog template
- `SKILL_v1_archive.md` - Previous 4-checkpoint system

---

*Rewritten Feb 6, 2026 after Amar Kumar session. See `Studio/Podcast Studio/Amar-Kumar/prep/SKILL_IMPROVEMENT_NOTES.md` for detailed rationale.*
