---
name: social-content-creator
description: Generate social media posts for LinkedIn, Twitter/X, and Substack. Use this skill when the user wants to create content about their developer journey, build in public updates, project showcases, lessons learned, or curated content. Triggers include "post about", "linkedin post", "twitter thread", "content idea", "draft a post", "refine this post". Supports brainstorming, drafting, and refining posts for developer/agency audiences.
---

# Social Content Creator

Generate authentic social media content for a developer building in public, targeting agencies, recruiters, and fellow developers.

## Voice & Style Rules

**Always:**

- Conversational and authentic — like talking to a smart colleague
- Show vulnerability — share struggles, not just wins
- Specific over generic — "reduced CLS by 0.2s" not "improved performance"
- End with engagement hook — question or opinion prompt

**Never:**

- Em-dashes (—)
- Corporate buzzwords ("leverage", "synergy", "unlock")
- Humble bragging
- Generic CTAs ("follow for more")
- Oxford commas

## Platform Formats

### LinkedIn

- Hook in first 2 lines (before "see more")
- Short paragraphs (1-2 sentences)
- Line breaks for readability
- End with specific question to drive comments

```
[Hook - stop the scroll]

[Context - what you were doing]

[The insight/lesson/discovery]

[What you learned or changed]

[Engagement question - specific, not generic]
```

### Twitter/X — Single Tweet

- 280 characters max
- One idea, one punch
- Thread teaser if bigger topic

### Twitter/X — Thread

- First tweet = hook (must stand alone)
- 5-12 tweets ideal
- Each tweet = one complete thought
- Number tweets (1/, 2/, etc.)
- Last tweet = summary + soft CTA

```
1/ [Hook that creates curiosity]

2/ [Context/Setup]

3/ [Point 1]

4/ [Point 2]

5/ [Point 3]

6/ [The lesson/takeaway]

7/ [Question or invitation to discuss]
```

### Substack (Lower Priority)

- Newsletter format
- Deeper reflection than social
- Can expand on popular social posts
- 500-1,500 words

## Content Pillars

Identify which pillar the content belongs to:

1. **Build in Public** — Zone 2 progress, code decisions, project updates
2. **Tech & Tools** — Stack choices, git workflow, dev setup, Sanity/Shopify/Next.js
3. **Design → Code** — UI improvements, responsive design, component architecture
4. **Lessons Learned** — Mistakes, refactors, "what I'd do differently"
5. **Curated/Reacts** — Commenting on others' work, website teardowns, industry takes
6. **Career Journey** — Path to creative developer, agency goals, freelance vision

## Workflow Modes

### Mode 1: Brainstorm

User gives rough idea → Generate 3-5 angle options with hooks

**Input:** "post about my git workflow"

**Output:**

> Here are 5 angles for your git workflow post:
>
> 1. **The mistake angle:** "I pushed to production once. Here's the git workflow that makes that impossible now."
>
> 2. **The simplicity angle:** "My entire git workflow fits on a sticky note. main → staging → feature. That's it."
>
> 3. **The process angle:** "Every PR I ship follows the same 4 steps. Here's my checklist."
>
> 4. **The tool angle:** "I automated my PR descriptions with a Claude skill. Here's how it works."
>
> 5. **The comparison angle:** "I tried 3 git workflows. Only one stuck. Here's why."
>
> Which angle resonates? Or should I explore a different direction?

### Mode 2: Draft

User picks angle or provides rough draft → Generate full post for platform

### Mode 3: Refine

User pastes draft → Polish for tone, structure, engagement hook

## Visual Suggestions

Always suggest visuals when relevant:

**Code snippets:**

- "Use ray.so for the git commands — dark theme, highlight lines 3-5"
- "Screenshot your terminal showing the diff output"

**Architecture/Flow:**

- "Excalidraw diagram showing: Sanity → Next.js → Shopify flow"
- "Simple before/after folder structure comparison"

**UI/Design:**

- "Side-by-side screenshot: mobile vs desktop breakpoint"
- "Screen recording of the hover interaction (use Loom or CleanShot)"

**Progress/Journey:**

- "Screenshot of your Notion roadmap or project board"
- "Commit history showing consistency"

## Notion Database Fields

Output these fields with every post:

```
Platform: [LinkedIn / Twitter / Thread / Substack]
Content Pillar: [Build in Public / Tech & Tools / Design → Code / Lessons Learned / Curated / Career Journey]
Publish Date: [suggested or TBD]
Status: [Draft / Ready / Published]
Topic Tags: [e.g., git, workflow, automation]
Target Audience: [Developers / Agencies / Recruiters / All]
Hook/Opening Line: [First line of post]
Content Description: [1-sentence summary]
CTA Type: [Comment / Link / None]
Material Link: [Source repo, project, or page if applicable]
Visual Suggestion: [What image/screenshot/diagram to include]
```

## Examples

### Example 1: Brainstorm → Draft Flow

**User:** "I want to post about how I organize my Sanity schemas"

**Claude (Brainstorm):**

> Here are angles for your Sanity schema post:
>
> 1. **The structure angle:** "My Sanity folder structure after 6 months of headless ecommerce"
> 2. **The naming angle:** "I renamed all my Sanity schemas last week. Here's why naming matters."
> 3. **The mistake angle:** "My first Sanity schema was 400 lines. Now I keep them under 50. Here's what changed."

**User:** "I like #3"

**Claude (Draft):**

**LinkedIn Post:**

My first Sanity schema was 400 lines.

Everything in one file. Products, variants, images, SEO, settings. A monster.

Now my biggest schema is 47 lines.

What changed:

→ One schema = one content type
→ Shared fields become reusable objects
→ Preview config in every schema (editors thank you later)
→ Group by domain: /products, /content, /settings

The 400-line file still works. But I'd never ship it to a client.

What's your schema organization strategy? One big file or many small ones?

---

**Notion Fields:**

```
Platform: LinkedIn
Content Pillar: Tech & Tools
Publish Date: TBD
Status: Draft
Topic Tags: sanity, schemas, architecture, cms
Target Audience: Developers
Hook/Opening Line: "My first Sanity schema was 400 lines."
Content Description: How I refactored bloated Sanity schemas into clean, maintainable files
CTA Type: Comment
Material Link: Zone 2 project
Visual Suggestion: Side-by-side screenshot of old 400-line file vs new folder structure. Use VS Code with file tree visible.
```

### Example 2: Refine Mode

**User:** "refine this: been working on responsive design lately. learned a lot about breakpoints and tailwind. xl breakpoint is really useful for tablets."

**Claude:**

**LinkedIn Post:**

I kept breaking tablet layouts until I changed one thing.

I was treating lg (1024px) as "tablet." Wrong.

1024px is tablet landscape. Portrait is still squished.

The fix: xl (1280px) for split layouts.

Now my rule:

→ Mobile: stack everything
→ md/lg: minor adjustments
→ xl: side-by-side layouts activate

Tablets in portrait finally look intentional, not broken.

Small shift, big improvement.

What's your breakpoint strategy?

---

**Notion Fields:**

```
Platform: LinkedIn
Content Pillar: Design → Code
Publish Date: TBD
Status: Draft
Topic Tags: responsive, tailwind, breakpoints, css
Target Audience: Developers
Hook/Opening Line: "I kept breaking tablet layouts until I changed one thing."
Content Description: Why xl (1280px) is the right breakpoint for split layouts, not lg
CTA Type: Comment
Material Link: Zone 2 project
Visual Suggestion: Before/after screenshots showing tablet portrait at lg vs xl breakpoint. Annotate with breakpoint values.
```

### Example 3: Twitter Thread

**User:** "thread about my developer journey so far"

**Claude:**

**Twitter Thread:**

1/ One year ago I decided to become a creative developer.

Zero coding experience. Just a failed sneaker business and a dream to build beautiful ecommerce sites.

Here's what happened: 🧵

2/ I started by reverse-engineering sites I admired.

Grebban. Aino. Vaan Group.

I didn't understand the code. But I understood what made them feel premium.

3/ My first tech decision: Next.js + Sanity + Shopify.

Not because I understood it. Because every agency I wanted to work for used it.

Learn the tools your dream job uses.

4/ I built one project for 6 months straight.

Zone 2 — a headless running store.

No tutorials. Just docs, errors and figuring it out.

5/ The hardest part wasn't code.

It was staying consistent when nothing worked and no one was watching.

6/ Now I'm 6 months from my goal: work with a top Swedish agency or freelance for design-first brands.

Still learning. Still building. Still sharing.

What's your developer origin story?

---

**Notion Fields:**

```
Platform: Thread
Content Pillar: Career Journey
Publish Date: TBD
Status: Draft
Topic Tags: journey, career, build-in-public
Target Audience: All
Hook/Opening Line: "One year ago I decided to become a creative developer."
Content Description: My path from sneaker business to creative developer, building Zone 2
CTA Type: Comment
Material Link: N/A
Visual Suggestion: Tweet 1: Photo of workspace or coding setup. Tweet 4: Screenshot of Zone 2 homepage. Tweet 6: Notion roadmap or goals page.
```

### Example 4: Single Tweet

**User:** "quick tweet about finally fixing a bug"

**Claude:**

**Tweet:**

Spent 3 hours debugging a cart issue.

The fix: one missing await.

That's it. That's the tweet.

---

**Notion Fields:**

```
Platform: Twitter
Content Pillar: Build in Public
Status: Draft
Topic Tags: debugging, shopify, async
Target Audience: Developers
Hook/Opening Line: "Spent 3 hours debugging a cart issue."
Content Description: Relatable debugging moment - missing await
CTA Type: None
Material Link: N/A
Visual Suggestion: Optional: ray.so screenshot of the one-line fix
```

## Content Ideas Generator

If user asks for ideas, suggest based on recent work:

**Recurring themes:**

- Zone 2 build progress and milestones
- Headless ecommerce architecture decisions
- Sanity + Shopify integration patterns
- Git workflow and PR process (you have a skill for this!)
- Responsive design learnings
- Agency research and positioning
- Running/marathon parallels to coding discipline
- Tool setups (VS Code, terminal, Notion)

**Formats to try:**

- "What I learned this week" (weekly recap)
- Website teardown / "How I'd improve this"
- Tool comparison (what you use vs alternatives)
- Mistake → lesson posts
- Milestone celebrations (keep humble)

## Proactive Content Suggestions

**During development work, watch for post-worthy moments:**

When the user:

- Fixes a tricky bug → Suggest: "This bug fix could make a good post. Want me to draft something?"
- Makes an architecture decision → Suggest: "This decision has a clear before/after. Worth sharing?"
- Learns something new → Suggest: "This is a relatable learning moment. Post idea?"
- Refactors code → Suggest: "Refactors make great 'what I changed and why' posts."
- Hits a milestone → Suggest: "Milestone worth celebrating. Quick post?"
- Struggles then succeeds → Suggest: "The struggle-to-solution arc is perfect for LinkedIn."

**How to suggest:**

Keep it brief and non-intrusive:

> "Nice fix. This could be a quick post — the 3-hour debug for a one-line fix story resonates with devs. Want me to draft it?"

Or:

> "This breakpoint decision is a solid 'what I learned' post. Should I save it for your content queue?"

**Don't suggest for:**

- Routine tasks (basic commits, minor styling)
- Sensitive client work
- Incomplete thoughts (wait until resolved)

## Important Reminders

1. **Ask for context** if the topic is vague
2. **Suggest platform variations** — one idea can become LinkedIn post + Twitter thread
3. **Always include visual suggestion** — posts with images perform better
4. **Offer to refine** — first draft is never final
5. **Match energy to platform** — LinkedIn slightly more professional, Twitter more casual
6. **Proactively suggest posts** — when you spot post-worthy moments during dev work, mention it
