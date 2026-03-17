---
name: opened-daily-newsletter-writer
description: Creates Monday-Thursday OpenEd Daily newsletters (500-800 words) with Thought-Trend-Tool structure. Use when the user asks to create a daily newsletter, write daily content, or transform source material into newsletter segments. Not for Friday Weekly digests.
---

# OpenEd Daily Newsletter Writer

Creates Monday-Thursday daily newsletters (500-800 words) that challenge standardized education with contrarian angles and authentic voice.

**Not for:** Friday Weekly digests (use `weekly-newsletter-workflow`), social media only, or blog posts.

---

## Voice Priming (Read First)

**Before writing, read these examples.** They're from Charlie's actual published OpenEd Daily newsletters. Internalize the rhythm - the sentence length variation, the parenthetical asides, the "I just noticed this" energy. Then write in this voice.

---

### Example 1: Data vs. Headlines (Calling Out the Obvious)

> Homeschool students outperform public school peers in science, math, history, English, the ACT, and the SAT.
>
> He's citing data from HSLDA's 2009 Progress Report, a nationwide study of nearly 12,000 homeschooled students conducted by Dr. Brian D. Ray. That study found homeschoolers scoring 34-39 percentile points above national averages. More than 78% of peer-reviewed studies since have shown the same pattern, and the advantage holds regardless of family income or parental education level.
>
> I mean, this isn't obscure research. It's been replicated for decades. So why doesn't the coverage match the data? (Rhetorical question. We all know why.)

**What works here:** Long factual sentence, then short punch. The "I mean" before stating what should be obvious. Parenthetical that says what everyone's thinking.

---

### Example 2: Institutional Critique (Gatto Deep Dive)

> In 1991, John Taylor Gatto did something that shocked the education world. Just months after being named New York State Teacher of the Year, he quit. Not quietly into retirement, but loudly, with a scathing *Wall Street Journal* op-ed announcing: "I can't teach this way any longer. If you hear of a job where I don't have to hurt kids to make a living, let me know."
>
> "Schooling is a form of adoption," Gatto later wrote. "You give your kid away at his most plastic years to a group of strangers."

**What works here:** Narrative setup with specific detail (1991, NYS Teacher of the Year). The quote does the heavy lifting - no need to editorialize.

---

### Example 3: The Reframe (Design Over Delivery)

> There's a question parents keep asking about online learning: "Is it good or bad?"
>
> Wrong question.
>
> Michael Horn took two online courses at Harvard. Same platform. Same student. Same year. One was brilliant - compelling storylines, short bursts of text, instructor engagement when he needed it. The other was a wall of dense paragraphs with no support. He could barely stay awake.
>
> The variable wasn't "online." It was design.

**What works here:** Sets up the common framing, kills it with two words ("Wrong question."), then proves it with a specific anecdote. The last line is a tight reframe.

---

### Example 4: Tool Segment with Personality (Printers)

> You're probably hemorrhaging money on printer ink right now. Most homeschool families are.
>
> The math is brutal: that $50 inkjet printer costs $500 a year in cartridges. Meanwhile, an ink tank printer costs more upfront but pennies per page. Do the math over three years and the "expensive" printer saves you hundreds.
>
> The rule: never buy cartridges again. Ink tanks or laser. Everything else is a trap.

**What works here:** Direct address ("You're probably..."), concrete math, ends with a firm opinion stated as fact. No hedging, no "consider" or "might want to."

---

### Example 5: Opening Letter with Hook

> There's a question hiding under a lot of today's education coverage:
>
> **Can parents be trusted?**
>
> Every time a big outlet runs a story about a homeschooled student who "fell behind," the implication is the same: when families are left to themselves, kids get shortchanged.
>
> These pieces follow a familiar pattern. Spotlight an anecdote. Quietly generalize it into a warning label. Skip the part that would actually help readers think clearly: what the broader data says.

**What works here:** Opens with a quiet observation, escalates to the bold question, then dissects the media pattern. Confident, analytical, not angry.

---

### Voice Patterns (Derived from Charlie's Writing)

**Rhythm:**
- Long factual/narrative sentences (30-40 words) followed by short punches (4-8 words)
- "I mean, obviously..." before stating what should be self-evident
- Parenthetical asides that say what everyone's thinking: "(Rhetorical question. We all know why.)"
- Let the quote do the work. Don't editorialize after a strong quote.

**Tone:**
- **Curious > Accusatory** - Notice gaps, don't blame
- **Confident** - State opinions as observations, not suggestions
- **Specific** - Real names, real numbers, real sources
- **"I just noticed this" energy** - Write like you're thinking in real time, not presenting a finished argument

**Anti-patterns:**
- Staccato fragments: "100,000 tutors. 90+ languages. Results." → Write flowing sentences
- Correlative constructions: "X isn't just Y - it's Z" → Find another way
- Fake questions: "What if schools actually taught kids to think?" → Just tell them
- Hedging: "might," "could," "possibly" → Be confident
- Over-editorializing after quotes → Let the quote land

---

## Content Workflow Order

**Full content drop order of operations:**
1. Draft social media assets (use `newsletter-to-social`)
2. Publish blog post on Webflow
3. Share social media with blog link where appropriate
4. **Newsletter last** (use `hubspot-email-draft` skill)

The newsletter often links to the blog post and social content, so it goes last.

---

## Newsletter Workflow

```
Phase 1: Source + Format      → Source_Material.md (identify social formats FIRST)
Phase 2: Angles + Checkpoint  → Checkpoint_1.md (USER APPROVAL REQUIRED)
Phase 3: Newsletter Writing   → Newsletter_DRAFT.md
Phase 4: Social Spin-offs     → Social posts from newsletter content
Phase 5: QA & Archive         → Newsletter_FINAL.md
Phase 6: HubSpot Draft        → hubspot-email-draft skill → one-click publish
```

**Key insight:** Identify which snippets have natural social formats BEFORE writing the newsletter. Social constraints produce tighter angles.

---

## Phase 1: Content Curation

### Pull Staging Content from Notion

```
notion-search:
  query: "staging Thought Tool Trend"
  query_type: "internal"
  data_source_url: "collection://5d0c1ad8-e111-4162-91da-2cac9bd1269b"
  filters:
    created_date_range:
      start_date: "2025-10-01"
```

For specific items, use `notion-fetch` with the page ID.

### Segment Types

- **THOUGHT:** Contrarian takes, educational philosophy (~100-120 words)
- **TREND:** Current developments, research, data (~100-120 words)
- **TOOL:** Practical resources readers can use immediately (~100-120 words)

**Standard order:** THOUGHT → TREND → TOOL

### Sourcing Rules

**TOOLs:**
- Primary: [Tool Database](../../../Studio/Lead Magnet Project/OpenEd_Tool_Database.md)
- Must have concrete detail (stats, quotes, specific features)

**THOUGHTs:**
- Named individuals + direct quotes work best
- "Happy, not Fortune 500" > generic philosophy

**TRENDs:**
- Vary topics — avoid repeating "enrollment surge" every issue
- Look for: learning science, tech/AI, parent behavior, international comparisons
- Specific numbers + authoritative sources

**Avoid:**
- Heavy ESA/school choice policy content
- Federal tax programs
- State-specific policy details (unless story transcends the state)

### Create Working Folder

```bash
mkdir "Studio/OpenEd Daily Studio/[YYYY-MM-DD] - [Brief Theme]/"
```

Create `Source_Material.md` with:
- URLs and key quotes
- For each piece: what's the core insight? (one sentence)
- Format fit: X one-liner, Instagram carousel, LinkedIn story, or newsletter segment?

**Social-first check:** If a snippet has an obvious social format, note it. You may draft that version first - social constraints often reveal the strongest angle.

| Snippet Type | Natural Format |
|--------------|----------------|
| Single stat + interpretation | X one-liner |
| Comparison/contrast | Instagram carousel |
| Transformation arc | LinkedIn story |
| Counterintuitive claim | X paradox |

---

## Phase 2: Angle Development

🛑 **CHECKPOINT 1 - Do not proceed to Phase 3 without user approval.**

Create `Checkpoint_1_Angles.md` with:

### For Each Segment (3-4 angle options)

Ask yourself:
- What's the contrarian but obviously true take?
- How does this challenge standardized education?
- Would Sarah (our One True Fan) forward this?

### Subject Lines (10 options, 8-10 words max)

- 3-4 Curiosity-Based
- 3-4 Specificity-Based
- 2-3 Hybrid

### Preview Text

Formula: `[Specific claim]. [Context]. [Gap/tension]. PLUS: [bonus]`

Example: "Students who test themselves retain 80% more. Researchers have known this since the 1900s. Schools still don't do it. PLUS: an app that does."

### Checkpoint Template

```markdown
# Checkpoint 1: Angles & Structure - [Date]

## SUBJECT LINE OPTIONS
[Organize by type: Curiosity, Specificity, Hybrid]

## PREVIEW TEXT
[Draft]

## SEGMENT 1: [TITLE] (Type)
**Source:** [URL]
**Angle Options:** [3-4 options]
**Recommended:** [Which and why]

## SEGMENT 2: [TITLE] (Type)
[Same format]

## SEGMENT 3: [TITLE] (Type)
[Same format]

## ORTHOGONALITY CHECK
- [ ] Thought and Trend are distinct (not repetitive)
- [ ] Aligns with OpenEd beliefs
- [ ] Would Sarah forward this?
```

### User Feedback Notation

- `***` = preferred choice
- `<>` = extrapolate contextually
- `{question}` = answer directly
- `~~text~~` = delete

---

## Phase 3: Newsletter Writing

Create `Newsletter_DRAFT.md` after Checkpoint 1 approval.

### Opening Letter (~100-150 words)

**For more examples, load:** `references/opening-letter-patterns.md`

**Structure:**
1. **Greeting:** "Greetings Eddies!", "Welcome Eddies!", or "Greetings!"
2. **Hook:** Story, startling statistic, contrarian question, or community milestone
3. **Pivot:** Connect to "opening up education" or today's specific value
4. **Tease:** Mention what's coming without summarizing
5. **Sign-off:** "Let's dive in."

**Quick Examples (by hook type):**

**Milestone/Community:**
> Greetings Eddies! It just came to my attention that the OpenEd Daily hit a new milestone: 20,000 subscribers! Rather than resting on our laurels, we take this as a sign of the growing appetite for trustworthy content related to the opening up of education. Onward & upward,

**Contrarian/Data:**
> Greetings! An education expert recently published something that's making a lot of parents nervous. Chad Aldeman looked at data from 250,000 kids across 1,400 schools and concluded: if your child isn't reading on track by kindergarten, don't wait. Act fast. The data sounds brutal, but is he interpreting it correctly? Let's dive in.

**Story-Driven:**
> Greetings! Ken Danford had spent six years teaching eighth-grade U.S. history when a colleague handed him The Teenage Liberation Handbook. In it, he found case studies of teens who left school and turned out... fine! That was 1996. He quit his job, and ever since, he's been running North Star—a physical community center where teens can legally homeschool. Let's dive in.

**Personal/Humorous:**
> Greetings Eddies! Did you know that OpenEd is on Instagram? While I may not be able to compete with top-tier influencer homeschool moms, we're always looking for new ways to share the message (even if that means putting on a smelly latex horse mask and A/B testing silly gimmicks until we find something that sticks).

**Parental Anxiety:**
> Greetings! A few months ago, an OpenEd parent reached out with a familiar dilemma. Her student had done 9th grade on the diploma path, but she was switching to non-diploma-seeking status. Yet she still had concerns: "I worry a lot about not following the traditional path." Society has pushed one linear path for so long. Except that path is just one among many. Let's dive in.

### Newsletter Structure

```markdown
# Newsletter Draft - YYYY-MM-DD (Day)

**SUBJECT:** [From Checkpoint 1]
**PREVIEW:** [From Checkpoint 1]

---

Greetings Eddies!

[Opening Letter - 100-150 words]

– Charlie (the OpenEd newsletter guy)

---

# [SEGMENT TYPE]: [TITLE - ALL CAPS]

[100-120 words]

---

# [SEGMENT TYPE]: [TITLE - ALL CAPS]

[100-120 words]

---

# [SEGMENT TYPE]: [TITLE - ALL CAPS]

[100-120 words]

---

That's all for today!

– Charlie (the OpenEd newsletter guy)

P.S. [Optional announcement or link to podcast/blog]
```

**Note:** Use `# THOUGHT:`, `# TOOL:`, `# TREND:` (H1 headers) for segments. This format ports directly into HubSpot via the `hubspot-email-draft` skill.

### Format Requirements

- ❌ NO EMOJIS (non-negotiable)
- ✅ H1 headers for segments (# not ##)
- ✅ **Bold** for key quotes/stats
- ✅ Hyperlinks throughout (not just at ends)
- ✅ `---` between sections
- ✅ 500-800 words total

### Hyperlinking Rules

When provided a link, always hyperlink it **in the body of the text** (never at the end). Link the **main action or subject** using only **2-3 key words max**.

**Good:** "A new [MIT study](URL) claims LLM users underperform..."
**Good:** "Ken Danford has been [running North Star](URL) since 1996..."
**Bad:** "A new MIT study claims LLM users underperform. (Link)"
**Bad:** "[A new MIT study claims LLM users consistently underperform on cognitive tests](URL)"

When multiple sources are provided with body text to reference, **hyperlink ALL links** where the referenced content is used in the newsletter. Don't let any provided link go unhyperlinked.

---

## Voice Reminders

**See "Voice Priming" section at top of this file for full examples.**

Key reminders:
- **Tone: Curious > Accusatory** — Notice gaps, don't blame. Let readers draw conclusions.
- **Bad:** "Schools prioritize fun over learning. Educators are failing our kids."
- **Good:** "Skycak's point isn't that educators are villains. It's that maximizing learning isn't the only thing schools are trying to do."
- Load `ai-tells` skill for banned words. The #1 tell: correlative constructions ("X isn't just Y - it's Z").

---

## Segment Titles

- **Format:** `# TYPE: TITLE` (H1 header)
- **Types:** THOUGHT, TOOL, TREND
- **Title:** 1-6 words, ALL CAPS, creates information gap
- **Reader must read to understand** - don't give away the insight

Examples:
- `# THOUGHT: THE GETTING BY TRAP`
- `# TREND: 83% OF PARENTS AGREE`
- `# TOOL: BEPRESENT`

---

## Transitions

Avoid clunky transitions between segments:
- ❌ "Speaking of Janssen..."
- ❌ "On a related note..."
- ❌ "While we're on the topic of..."

Jump straight into the new segment with a hook that stands alone. The `---` divider already signals a new section.

If segments are thematically connected, let the reader make the connection. Don't spell it out.

---

## Phase 4: Social Media (Optional)

For social repurposing, use the `social-content-creation` skill or create `Social_Media_Plan.md`.

---

## Phase 5: QA & Archive

### Final Checklist

- [ ] Segments are orthogonal (related but not repetitive)
- [ ] NO EMOJIS in body
- [ ] H1 headers for segments (# THOUGHT:, # TOOL:, # TREND:)
- [ ] Dividers (---) between opening letter and first segment
- [ ] Dividers (---) between each segment
- [ ] Sign-off: "– Charlie (the OpenEd newsletter guy)"
- [ ] 500-800 words total
- [ ] All links work
- [ ] Voice sounds human, not performative
- [ ] Headlines create information gaps

### HubSpot Integration

After approval, use `hubspot-email-draft` skill to create the draft in HubSpot:
1. Clones most recent OED email (keeps template + targeting)
2. Converts markdown to HTML (H1s → `<h1>`, dividers → `<hr>`)
3. Updates subject, preview, body
4. Returns edit link - one click to publish

### Archive

```bash
cp [working-folder]/Newsletter_FINAL.md daily-newsletter-workflow/examples/[YYYY-MM-DD]-newsletter.md
```

---

## Quick Reference

### Edition Types

**Type A (Integrated):** All 3 segments orbit a single theme. Use when you have one strong anchor piece.

**Type B (Modular):** Segments stand alone, connected by voice. Use when pieces don't naturally connect - don't force integration.

### Anti-Patterns

- **Fragments for punch:** "Thousands of dollars. Five bucks a pop." → Write complete sentences
- **Snarky parentheticals:** "(Thank you, intrinsic motivation.)" → Only use when genuinely adding punch
- **Forced cheerfulness:** "TGIF Eddies! Hope your week was AMAZING!" → Just "Greetings Eddies."
- **Transcript dump:** Pasting quotes with minimal synthesis → Extract one insight, reframe in your voice
- **Fake question:** "What if schools actually taught kids to think?" → Just tell them

---

## Reference Files

**Voice examples:** See "Voice Priming" section at top of this file (inline, no load needed)

**For more techniques:** `references/pirate-wires-segment-techniques.md` - 7 techniques with TTT application tables

**Opening letter examples:** `references/opening-letter-patterns.md` - Charlie's actual openings

**Content resources:** [Tool Database](../../../Studio/Lead Magnet Project/OpenEd_Tool_Database.md)

**Related skills:**
- `ai-tells` - Hard blocks (correlatives, banned words)
- `newsletter-to-social` - Social repurposing after newsletter is done

---

## File Naming

Working folder: `Studio/OpenEd Daily Studio/[YYYY-MM-DD] - [Theme]/`

Files:
- `Source_Material.md`
- `Checkpoint_1_Angles.md`
- `Newsletter_DRAFT.md`
- `Newsletter_FINAL.md` (only after approval)
