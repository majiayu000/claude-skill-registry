---
name: content-creator
description: Generate social content with brand voice - threads, posts, articles, announcements
---

# Content Creator Skill

Generate on-brand content for social media and marketing.

## Capabilities

- Twitter threads with preview
- Single posts/tweets
- Launch announcements
- Article drafts
- One-pagers and briefs
- Deck content
- Print-ready exports (PDF)

## Input Requirements

Requires:
- `knowledge/BRAND_BRIEF.md` - Brand identity
- `knowledge/VOICE_AND_TONE.md` - How to speak (optional)
- `knowledge/BRAND_DECISIONS.md` - Visual identity (for previews)

## Commands

```
/content thread [topic]       # Generate Twitter thread
/content post [topic]         # Generate single post
/content announce [what]      # Launch announcement
/content article [topic]      # Article draft
/content one-pager [topic]    # One-page summary
/content deck [topic]         # Presentation content
/content preview              # Preview in context
/content export pdf           # Export to PDF
```

## Workflows

### Twitter Thread

```
/content thread [topic]

Generating thread on: {topic}

THREAD DRAFT (6 tweets):

1/ {hook tweet - stops the scroll}

2/ {context/problem}

3/ {insight/solution}

4/ {proof/example}

5/ {implication/future}

6/ {CTA}
   {link}

---

Preview? (yes/no)
```

If yes, update `previews/content/twitter-thread.html` and open.

### Launch Announcement

```
/content announce [product/feature]

ANNOUNCEMENT DRAFT:

SHORT (Twitter):
"{short version - fits in one tweet}"

MEDIUM (Newsletter):
"{2-3 paragraph version}"

LONG (Blog):
"{full announcement with context}"

---

Which format to preview?
```

### One-Pager

```
/content one-pager [topic]

ONE-PAGER: {topic}

HEADLINE:
{main headline}

SUBHEAD:
{supporting line}

THE PROBLEM:
{1-2 sentences}

THE SOLUTION:
{1-2 sentences}

KEY BENEFITS:
• {benefit 1}
• {benefit 2}
• {benefit 3}

PROOF POINTS:
• {proof 1}
• {proof 2}

CTA:
{call to action}

---

Export to PDF? (yes/no)
```

### Article Draft

```
/content article [topic]

ARTICLE DRAFT: {topic}

HEADLINE OPTIONS:
1. {option 1}
2. {option 2}
3. {option 3}

SUBHEAD:
{supporting line}

INTRO (1 paragraph):
{hook + thesis}

SECTIONS:
1. {section title}
   {key points}

2. {section title}
   {key points}

3. {section title}
   {key points}

CONCLUSION:
{summary + CTA}

---

Expand which section?
```

## Preview System

### Twitter Thread Preview
`previews/content/twitter-thread.html`

Shows thread in Twitter UI context:
- Dark/light mode
- Engagement metrics (mock)
- Your profile info
- Reply chains

### Article Preview
`previews/content/article-preview.html`

Shows article in blog context:
- Your brand styling
- OG image preview
- Reading time
- Share buttons

### One-Pager Preview
`previews/content/one-pager.html`

Shows formatted one-pager:
- Print-ready layout
- Brand colors/typography
- Export to PDF button

## Voice Application

Read `knowledge/VOICE_AND_TONE.md` and apply:

### Before Writing, Check:
- Voice attributes (are we being {attribute}?)
- Words to use / avoid
- Formatting conventions
- Tone for this context

### During Writing:
- Match established patterns
- Use brand vocabulary
- Maintain consistent tone
- Follow punctuation rules

### After Writing, Verify:
- Does this sound like us?
- Would we say this out loud?
- Is it clear to our audience?

## PDF Export

For one-pagers and decks, generate print-ready PDF:

```
/content export pdf

Exporting to PDF...

Options:
├─ Size: Letter / A4
├─ Orientation: Portrait / Landscape
├─ Include: Header / Footer
└─ Brand: Apply brand colors

Output: outputs/pdf/{filename}.pdf
```

Uses browser print-to-PDF or headless Chrome.

## Output Files

```
outputs/
├── content/
│   ├── threads/
│   │   └── thread-{date}-{topic}.md
│   ├── posts/
│   │   └── post-{date}-{topic}.md
│   ├── articles/
│   │   └── article-{date}-{topic}.md
│   └── one-pagers/
│       └── one-pager-{topic}.md
└── pdf/
    └── one-pager-{topic}.pdf
```

## Content Patterns

### Thread Structures

**The Hook-Proof-CTA:**
1. Hook (stop scroll)
2. Problem
3. Solution
4. Proof
5. Implication
6. CTA

**The List Thread:**
1. "X things about Y:"
2-N. List items
Last. Summary + CTA

**The Story Thread:**
1. Opening scene
2-5. Story progression
6. Lesson/insight
7. CTA

### Post Formulas

**Problem-Solution:**
"{Problem statement}

{Solution in your words}

{CTA}"

**Contrarian:**
"Unpopular opinion: {take}

Here's why: {reasoning}

{CTA if relevant}"

**Announcement:**
"{What's new}

{Why it matters}

{Link/CTA}"
