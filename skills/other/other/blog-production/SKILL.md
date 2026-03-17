---
name: blog-production
description: Produce a complete blog article for Clarido from topic selection through published, voice-analyzed markdown with illustration. Use when creating new blog content.
allowed-tools: Bash(pipenv *), Bash(cd * && pnpm *), Bash(pnpm *), Bash(ls *), Bash(mkdir *), Bash(cp *), Bash(open *), Bash(curl *), Bash(git *), mcp__claude-in-chrome__*, mcp__google-workspace__send_gmail_message
---

# Blog Production

End-to-end workflow for producing a published blog article on the Clarido blog. Takes a topic from ideation through research, writing, voice analysis, illustration, and verification.

Invoked by the user with `/blog-production` or when asked to write/create a new blog post.

## Repos

- **Landing page** (where blog lives): `~/dev/clarido-landing-page/`
  - Articles: `~/dev/clarido-landing-page/content/blog/{slug}.md`
  - Illustrations: `~/dev/clarido-landing-page/public/blog/{slug}.png`
  - Blog engine: `~/dev/clarido-landing-page/lib/blog.ts`
  - Blog post page: `~/dev/clarido-landing-page/app/blog/[slug]/page.tsx`
  - Blog index: `~/dev/clarido-landing-page/app/blog/page.tsx`
- **Marketing ops** (where tools live): `~/dev/clarido-marketing/`
  - Voice analyzer: `scripts/blog/ai_voice_analyzer.py`
  - Illustration generator (reuse pattern): `scripts/tiktok/illustrations.py`

## Workflow with Approval Gates

### Phase 1: Topic & Angle (user approves)

The user may invoke this skill in two ways:
- **With a topic:** User provides a specific concept, keyword, or idea.
- **Without a topic:** Claude proposes 2-3 options based on the target audience.

1. **Dedup check** -- Read all files in `~/dev/clarido-landing-page/content/blog/` to avoid repeating topics.
2. **Topic selection** -- Pick topics at the intersection of:
   - Psychology, neuroscience, or behavioral science (must have real research behind it)
   - Relevance to Clarido's audience: overthinkers, people in transition, people who carry too much in their heads
   - SEO opportunity: topics people actually search for (brain dump, overthinking, journaling, mental clarity, decision fatigue, cognitive load, etc.)
3. **Define the angle** -- Not just "what" but "why it's interesting." Every article needs a core insight that makes the reader think differently. Not a listicle, not a how-to guide. An essay that builds an argument.
4. **Present to user** -- Topic, angle, working title, 1-sentence thesis. Wait for approval.

### Phase 2: Research (automated)

5. **Find 4-6 real academic studies** that support the article's argument. Requirements:
   - Real authors, real journals, real years
   - Use WebSearch to verify each citation exists
   - Prefer landmark/foundational studies (they're more interesting to read about)
   - Include: author(s), year, paper title, journal name, volume/issue/pages if available
   - Mix of classic studies (establishes credibility) and recent ones (shows the field is active)

6. **Build a research brief** -- For each study, write 1-2 sentences summarizing the key finding that's relevant to the article. This becomes the raw material for weaving research into the prose.

### Phase 3: Writing (user approves)

7. **Write the article** following the style guide below. Target **1,500-2,200 words** (7-10 min read).

8. **Save to** `~/dev/clarido-landing-page/content/blog/{slug}.md` with proper frontmatter:
   ```yaml
   ---
   title: "Full Title Here"
   description: "1-2 sentence hook for SEO/social. Should make someone want to click."
   date: YYYY-MM-DD  # today's date
   author: Clarido Team
   tags: [primary-topic, secondary-topic, ...]  # 3-5 tags for SEO
   illustration: /blog/{slug}.png
   ---
   ```

9. **Present the draft** to the user and wait for approval before proceeding.

### Phase 4: Voice Analysis & Polish (automated)

10. **Run the voice analyzer:**
    ```bash
    pipenv run python3 scripts/blog/ai_voice_analyzer.py ~/dev/clarido-landing-page/content/blog/{slug}.md
    ```

11. **Fix flagged issues** -- Work through priority fixes. Target: **overall score 85+**, zero HIGH-severity flagged sentences.

12. **Em dash sweep** -- Search for any `---` (em dashes) and replace with periods, commas, colons, or parentheses. Em dashes are a strong AI tell.

13. **Re-run analyzer** to confirm score meets threshold.

### Phase 5: Illustration (automated)

14. **Generate a blog hero illustration** using OpenAI `gpt-image-1.5`. Use the Clarido brand illustration style:
    - Simple white character with black outlines, gray watercolor shading
    - Yellow (#FFD60A) as the only color accent
    - Clean, minimal, conceptual (not literal)
    - Soft gray wash texture, hand-drawn look
    - Reference images: `assets/illustrations/overwhelmed-filing-cabinet.png`, `floating-yellow-balloon.png`, `planting-yellow-seedling.png`

    Use the same approach as `scripts/tiktok/illustrations.py`: pass reference images via `images.edit()`, prepend the STYLE_PREFIX, use `quality="high"`.

    Save to: `~/dev/clarido-landing-page/public/blog/{slug}.png`
    Dimensions: `1536x1024` (3:2 landscape). Unlike TikTok (portrait 1024x1536), blog illustrations are landscape.

### Phase 6: Verify & Ship (automated)

15. **Build the landing page** to verify no errors:
    ```bash
    cd ~/dev/clarido-landing-page && pnpm build
    ```

16. **Start dev server:**
    ```bash
    cd ~/dev/clarido-landing-page && pnpm dev
    ```

17. **Visual audit with Chrome browser automation.** Use `mcp__claude-in-chrome__` tools to:
    - Navigate to `http://localhost:3000/blog/{slug}`
    - Read the page and verify:
      - Article renders with all HTML components (cards, callouts, pull quotes, etc.)
      - Illustration loads correctly
      - Email capture form appears above references section
      - No broken formatting, no raw HTML visible
      - Typography, spacing, and layout look correct
      - Internal links to other articles work
    - Navigate to `http://localhost:3000/blog` (index page) and verify:
      - New article appears in the list
      - Thumbnail/illustration shows
      - Title, description, tags, and date display correctly

18. **SEO & crawler audit.** Using Chrome tools, verify:
    - Check `http://localhost:3000/robots.txt` — blog pages must NOT be disallowed
    - Read the page source/meta tags on the article page:
      - `<title>` tag contains the article title
      - `<meta name="description">` is present and meaningful
      - No `<meta name="robots" content="noindex">` blocking crawlers
      - Open Graph tags (`og:title`, `og:description`, `og:image`) are present for social sharing
    - If any crawler-blocking issues are found, fix them in the landing page code and rebuild

19. **Push to production.** In the landing page repo (`~/dev/clarido-landing-page`):
    ```bash
    cd ~/dev/clarido-landing-page
    git add content/blog/{slug}.md public/blog/{slug}.png
    git commit -m "Publish blog: {article title}"
    git push origin main
    ```
    Include any other modified files (e.g., if SEO fixes were made to `app/` or `lib/` files).

20. **Send notification email.** Use `mcp__google-workspace__send_gmail_message` to email **abhinav@jabhi.ca** and **joieta@jabhi.ca** with:
    - **Subject:** `New blog published: {article title}`
    - **Body** (keep it concise):
      - 2-sentence brief summarizing the article and its angle
      - Link to the live article: `https://clarido.app/blog/{slug}`
      - **Target keywords:** list the 5-8 SEO keywords this article targets (from the tags + content strategy)
      - **Internal links:** list any other Clarido blog articles linked to from within this article (title + URL for each)

21. **Report to user** -- Share the live URL, final voice analyzer score, word count, and confirmation that the email was sent.

## Writing Style Guide

The voice is **Paul Graham meets quality journalism**. Intellectual rigor in conversational prose, with modern visual formatting for scanability.

### Prose Rules

| Rule | Do | Don't |
|------|-----|-------|
| **Tone** | Conversational, curious, direct | Academic, coaching, marketing |
| **Perspective** | "you" to engage, "I" for opinions | Impersonal third-person throughout |
| **Contractions** | "don't", "it's", "you're", "can't" | "do not", "it is", "you are" |
| **Sentences** | Wild variation: 4-word fragments mixed with 30-word explorations | Every sentence 15-20 words |
| **Paragraphs** | One-liners mixed with longer blocks | Uniform paragraph sizes |
| **Openers** | Questions, fragments, "But", "And", prepositional phrases | "The", "This", "It is" repeatedly |
| **Research** | Woven into narrative: "In the 1920s, a psychologist named Bluma Zeigarnik noticed..." | Announced: "Research shows that..." or "According to a study..." |
| **Analogies** | Concrete, visual: "Think of it as a desk with room for four things" | Abstract: "This can be compared to a multifaceted system" |
| **Em dashes** | Never. Use periods, commas, colons, parentheses instead. | "The answer is simple --- just write it down" |
| **Hedge phrases** | Never. See the analyzer's HEDGE_PHRASES list. | "It's important to note", "In today's world" |
| **Questions** | 5-10% of sentences. Rhetorical questions that make the reader feel seen. | Zero questions (pure declaration) |
| **Endings** | End with quiet resonance, not a CTA. The last paragraph should land. | "So what are you waiting for? Try it today!" |

### Structure Pattern

Don't follow a rigid template, but most good articles have this shape:

1. **Opening hook** -- Start with something specific and interesting. A feeling, a paradox, a question. Not "In today's fast-paced world." Not a definition. Drop the reader into the middle of something.
2. **The problem/phenomenon** -- What's actually going on? Build understanding through concrete details and analogies.
3. **The research** -- Weave in 3-4 studies naturally. Name the researchers, tell the story of the finding, make the reader care about the science.
4. **The mechanism** -- Why does this work? Go one level deeper than the surface explanation.
5. **The practical** -- What can the reader do? But frame it as insight, not instruction. "The people who benefit most are the ones who..." not "Step 1: Do this."
6. **The close** -- Tie back to the opening. Leave the reader thinking.

### HTML Components

Use these **sparingly** to aid comprehension. They should feel earned, not decorative. The article should read well as pure text; components enhance, they don't carry.

**Key Stat** -- For one striking number that anchors the argument:
```html
<div class="key-stat">
<span class="stat-number">4-7</span>
<span class="stat-label">items your working memory can hold at once. Recent research suggests the real number is closer to four.</span>
</div>
```

**Pull Quote** -- For a sentence that deserves emphasis. Use 1-2 per article max:
```html
<blockquote class="pull-quote">
Your brain evolved to think, analyze, and solve problems. Not to be a filing cabinet.
</blockquote>
```

**Card Grid** -- For parallel concepts (2-4 items). Use when items are genuinely parallel:
```html
<div class="card-grid">
<div class="card">
<h4>Title</h4>
<p>Description</p>
</div>
<!-- more cards -->
</div>
```
For 3 columns: add `cols-3` class to the card-grid div.
Cards can optionally include `<div class="card-example">` for italic examples.

**Callout** -- For a parenthetical tip or insight that doesn't fit the main flow:
```html
<div class="callout">
<strong>Label (optional)</strong>
Content here.
</div>
```
Add `insight` class for insight-style callouts: `<div class="callout insight">`.

**Comparison** -- For before/after or contrasting approaches:
```html
<div class="compare">
<div class="compare-bad">
<span class="compare-label">Label A</span>
"The bad example"
</div>
<div class="compare-good">
<span class="compare-label">Label B</span>
"The good example"
</div>
</div>
```

### References Section

Every article ends with a references section. Format:

```markdown
---

### References

- Author, A.B. (Year). "Paper Title." *Journal Name*, Volume(Issue), Pages.
- ...

---

*Clarido is a quiet log for a loud mind. Speak or type what's on your mind. Clarido holds it for you so you can return when you have space. [Join the beta](https://clarido.app)*
```

The references section gets automatically split from the main content by the blog engine. An email capture form appears between the article body and references.

## Quality Gates

| Gate | Threshold | Action if failed |
|------|-----------|-----------------|
| Voice analyzer overall score | 85+ | Fix flagged issues, re-run |
| HIGH-severity flagged sentences | 0 | Rewrite each flagged sentence |
| Em dashes | 0 | Replace with periods/commas/colons/parens |
| Hedge phrases detected | 0 | Delete every one |
| AI signal words detected | 0 | Replace or cut |
| Readability grade | 6-10 | Simplify vocabulary, shorten sentences |
| Questions asked | 5%+ of sentences | Add rhetorical questions |
| Word count | 1,500-2,200 | Expand thin sections or cut bloat |

## Reference Article

The brain-dumping article is the gold standard for style, structure, and quality:
`~/dev/clarido-landing-page/content/blog/brain-dumping-article.md`

Read it before writing any new article. It scores 95/100 on the voice analyzer.

## Topic Bank

Psychology and neuroscience concepts relevant to Clarido's audience. Each maps to search keywords people actually type:

| Concept | Search Keywords | Angle |
|---------|----------------|-------|
| Zeigarnik Effect | overthinking at night, can't stop thinking | Why unfinished tasks haunt you |
| Decision Fatigue | decision fatigue, too many choices | Why you can't decide anything by 8pm |
| Cognitive Offloading | brain dump, write things down | Your brain isn't meant to store things |
| Affect Labeling | name your emotions, journaling anxiety | Why naming the feeling makes it smaller |
| Implementation Intentions | how to follow through, procrastination | The planning trick that bypasses willpower |
| Attention Residue | can't focus, distracted, task switching | Why you're still thinking about the last thing |
| Peak-End Rule | bad days, why do I feel bad | You're judging your day by two moments |
| Expressive Writing | journaling benefits, writing therapy | Why writing about pain actually heals |
| Spotlight Effect | social anxiety, self-conscious, overthinking social | Nobody is thinking about you as much as you think |
| Ego Depletion (controversy) | willpower, self-control, mental energy | The willpower myth that won't die |
| Paradox of Choice | overwhelmed by options, too many choices | More options make you less happy |
| Bedtime Worry Journaling | can't sleep, racing thoughts at night | The 5-minute trick that fixes 3am anxiety |

Don't repeat topics already covered in existing blog posts.

## Files

| File | Repo | Purpose |
|------|------|---------|
| `content/blog/{slug}.md` | landing-page | Article markdown with frontmatter |
| `public/blog/{slug}.png` | landing-page | Hero illustration (1200x630) |
| `lib/blog.ts` | landing-page | Blog engine (splits references, calculates reading time) |
| `app/blog/[slug]/page.tsx` | landing-page | Blog post page template |
| `app/blog/[slug]/email-capture.tsx` | landing-page | Email capture component (auto-inserted above references) |
| `app/blog/page.tsx` | landing-page | Blog index page |
| `app/globals.css` | landing-page | Blog component CSS (callout, card-grid, key-stat, pull-quote, compare) |
| `scripts/blog/ai_voice_analyzer.py` | marketing | Voice analyzer script (19 dimensions) |
| `scripts/tiktok/illustrations.py` | marketing | OpenAI gpt-image-1.5 illustration generator (reuse the pattern) |
| `assets/illustrations/` | marketing | Brand illustration style references (passed to OpenAI as style refs) |
