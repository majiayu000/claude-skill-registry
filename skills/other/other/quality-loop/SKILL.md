---
name: quality-loop
description: Iterative drafting system with 5-judge quality gates. This skill should be used for any writing project requiring multiple drafts and systematic quality control - profiles, deep dives, guides, articles. Includes source compilation, hook-first drafting, and backpressure from judge personas.
---

# Quality Loop

Iterative drafting system with backpressure from judge personas. Creates high-quality content through systematic source gathering, hook-first drafting, and multi-pass quality gates.

## When to Use This Skill

**UNIVERSAL QUALITY GATES:** This skill triggers for ALL public-facing content.

### Trigger Points by Content Type

| Content Type | Trigger Point | Mode |
|--------------|---------------|------|
| **Newsletter** | After draft, before send | Full 5-judge |
| **Deep Dive/Article** | Before Webflow publish | Full 5-judge |
| **Podcast blog** | Before publish | Full 5-judge |
| **LinkedIn post** | After draft, before schedule | Lite 3-judge |
| **X post** | After draft, before schedule | Lite 3-judge |
| **Instagram** | After draft + visual | Lite 3-judge |
| **Facebook** | After draft, before schedule | Lite 3-judge |

### Full 5-Judge Mode

For long-form content (articles, newsletters, blog posts):
- Human Detector (BLOCKING)
- Accuracy Checker (BLOCKING)
- OpenEd Voice (BLOCKING)
- Reader Advocate (BLOCKING)
- SEO Advisor (ADVISORY)

### Lite 3-Judge Mode

For social posts (faster, focused on voice and AI tells):
- AI-Tell Judge (BLOCKING) - Hard blocks only
- Voice Judge (BLOCKING) - Brand alignment
- Platform Judge (ADVISORY) - Platform-specific optimization

See "Lite Quality Loop for Social" section below.

---

## The Quality Loop Process

```
SOURCES → HOOK → DRAFT → JUDGES → ITERATE
    ↑                         ↓
    └─────── (if blocked) ────┘
```

### Phase 1: Source Compilation

Before drafting, gather all relevant sources into a single compiled file.

**Source Search Order:**

1. **Proprietary content first** - Search OpenEd podcast transcripts, newsletters, Slack
2. **Content database** - Grep `Content/` for related themes (not just exact terms)
3. **External research** - Web search for biography, facts, external validation

**When no direct coverage exists:**
Expand the search to related themes. For example, if writing about "Daniel Greenberg":
- Search for "democratic education"
- Search for "self-directed"
- Search for "trust children"
- Search for related thinkers who discuss him (Peter Gray)

**Source File Format:**

```markdown
# Source: [Topic] Compiled

## Biographical Facts
- Key dates, roles, locations
- Verified from multiple sources

## OpenEd Proprietary Content
**From Podcast [Episode]:**
> "Direct quote..."

**From Newsletter:**
> "Direct quote..."

## Key Themes
- Theme 1 with supporting evidence
- Theme 2 with supporting evidence

## SEO Notes
- Primary keyword: [keyword] ([volume]/mo)
- Secondary keywords: [list]

## Sources for Verification
- [URL 1]
- [URL 2]
```

---

### Phase 2: Hook First

Never draft without user approval of the hook angle. Propose 4-6 hook options with clear differentiation.

**Hook Proposal Format:**

| # | Hook | Opening Line | Why It Works |
|---|------|--------------|--------------|
| 1 | [Name] | "[First sentence]" | [Reasoning] |
| 2 | [Name] | "[First sentence]" | [Reasoning] |
| ... | ... | ... | ... |

**Good hooks:**
- Start with a specific moment, fact, or tension
- Create curiosity without clickbait
- Connect to something the reader cares about
- Differentiate from what's already ranking

**Bad hooks:**
- Generic "In today's world..." openings
- Definition-first approaches ("X is defined as...")
- Vague statements that could apply to anyone

After user selects a hook, proceed to drafting.

**For series content:** When writing multiple pieces on similar topics (e.g., profiles of thinkers), ensure each piece has a structurally different approach to avoid sameness. Examples:
- Profile A: Personal drama narrative
- Profile B: Scientific/research angle
- Profile C: Evolution story (phases of career)
- Profile D: Institutional critique
- Profile E: Evidence/longevity angle

Track the structural approach used for each piece to ensure variety.

---

### Phase 3: Draft

Create the full draft following OpenEd style guidelines.

**Draft Structure:**

```markdown
# Draft v[N]: [Title]

**Date:** [YYYY-MM-DD]
**Type:** [New / Enhancement]
**Target:** ~[X] words

---

## META ELEMENTS

**Title Options:**
1. [Option 1] ([char count])
2. [Option 2] ([char count])
...

**Meta Description (155 chars):** [Description]

**URL:** /blog/[slug]

---

## ARTICLE

[Full article content]

---

## NOTES FOR JUDGES

**Word count:** ~[X] words
**Internal links:** [N]
**External links:** [N]
**Target keywords:** [list]
**OpenEd connection:** [what makes this ours]
**Unique angle:** [what differentiates from competitors]
```

---

### Phase 4: Five Judges

Run every draft through all five judges in order. If ANY blocking judge fails, fix and re-run that judge before proceeding.

**Full judge references:** See `references/` folder for expanded criteria.

#### Judge 1: Human Detector (BLOCKING)
*See: `references/human-detector.md`*

Scans for AI tells. Zero tolerance for:
- Correlative constructions ("X isn't just Y - it's Z")
- Dramatic contrast reveals ("Not X. Y.")
- AI vocabulary (delve, comprehensive, crucial, landscape, journey, tapestry, myriad)
- Staccato patterns ("No fluff. No filler. Just results.")
- Triple Threat Syndrome (forced three-adjective stacks)

**VERDICT:** PASS only if zero AI tells found.

---

#### Judge 2: Accuracy Checker (BLOCKING)
*See: `references/accuracy-checker.md`*

Verifies all factual claims against compiled sources:
- Dates, names, quotes must match sources exactly
- Statistics need citations
- Timeline events in correct order
- No unverifiable claims presented as fact

**VERDICT:** PASS only if all facts verified.

---

#### Judge 3: OpenEd Voice (BLOCKING)
*See: `references/opened-voice.md`*

Core stance: **Pro-child, not anti-school.**
- Describes, doesn't prescribe
- Practical takeaways present
- 3+ internal links
- Uses proprietary OpenEd content

**VERDICT:** PASS only if aligned with stance.

---

#### Judge 4: Reader Advocate (BLOCKING)
*See: `references/reader-advocate.md`*

Assesses engagement:
- Hook creates curiosity (not definitions)
- Logical section flow
- Scannable structure
- Appropriate length
- Strong ending

**VERDICT:** PASS only if engaging throughout.

---

#### Judge 5: SEO Advisor (ADVISORY)
*See: `references/seo-advisor.md`*

Evaluates search optimization. Does not block.
- Keyword in title, first 100 words, H2s
- Meta elements optimized
- 5+ internal links, 2-3 external
- Featured snippet opportunities

**VERDICT:** Advisory feedback only.

---

### Phase 5: Iterate

If any blocking judge fails:
1. Make the specific fixes identified
2. Re-run ONLY the failed judge
3. If pass, continue to next judge
4. If fail again, make additional fixes and repeat

After all judges pass:
- Update status in tracking document
- Move to next piece or finalize for publication

---

## Folder Structure

The folder structure depends on the project type. Organize sources and drafts logically.

**Example for profile series:**
```
project/
├── sources/
│   ├── person-a/compiled-sources.md
│   └── person-b/compiled-sources.md
├── drafts/
│   ├── person-a/v1.md
│   └── person-b/v1.md
└── TRACKING.md
```

**Example for guide project:**
```
project/
├── sources/compiled-sources.md
├── drafts/
│   ├── v1.md
│   ├── v2.md
│   └── final.md
└── TRACKING.md
```

---

## Tracking Progress

Maintain a tracking document showing status of each piece.

**Tracking Table Format:**

| Item | Sources | Hook | Draft | HD | AC | OV | RA | SEO | Status |
|------|---------|------|-------|----|----|----|----|-----|--------|
| [Name] | DONE | [Hook name] | v1 | PASS | PASS | PASS | PASS | PASS | COMPLETE |
| [Name] | DONE | pending | - | - | - | - | - | - | NEEDS HOOK |

**Legend:**
- HD = Human Detector
- AC = Accuracy Checker
- OV = OpenEd Voice
- RA = Reader Advocate
- SEO = SEO Advisor

---

## Lite Quality Loop for Social

Faster quality checks for social posts. Run after draft, before scheduling.

### Judge 1: AI-Tell Judge (BLOCKING)

**Hard blocks - auto-reject if ANY found:**

- [ ] Correlative constructions ("X isn't just Y - it's Z")
- [ ] Banned words: delve, comprehensive, crucial, leverage, landscape
- [ ] Setup phrases: "The best part?", "What if I told you", "Here's the thing"
- [ ] Staccato patterns: "No fluff. No filler. Just results."
- [ ] Em dashes without spaces (use " - " not "—")

**VERDICT:** PASS only if zero hard blocks found.

### Judge 2: Voice Judge (BLOCKING)

**Checks:**
- [ ] Sounds like OpenEd/brand account (not personal blog)
- [ ] Aligns with Open Education values (parent empowerment, learner agency)
- [ ] Appropriate tone for platform
- [ ] No preachy or prescriptive language

**VERDICT:** PASS only if brand-aligned.

### Judge 3: Platform Judge (ADVISORY)

**Platform-specific checks:**

| Platform | Checklist |
|----------|-----------|
| LinkedIn | 200-500 words, links in comments, 3-5 hashtags, hook in first 2 lines |
| X | 70-100 chars optimal, 1-2 hashtags, retweet-worthy |
| Instagram | Visual-first, caption supports, 5-10 hashtags, first 150 chars hook |
| Facebook | No external links, no hashtags, ends with question/engagement prompt |

**VERDICT:** Advisory feedback - does not block.

### Lite Loop Process

```
DRAFT → AI-Tell Judge → Voice Judge → Platform Judge → SCHEDULE
             ↓ (fail)        ↓ (fail)
           FIX & RETRY     FIX & RETRY
```

---

## Quick Reference: AI Patterns to Avoid

### Correlative Constructions (Most Common Tell)
- "X isn't just Y - it's Z"
- "X didn't Y. It Z."
- "The goal isn't X - it's Y"
- "It's not about X, it's about Y"

### Forbidden Words
delve, comprehensive, crucial, vital, leverage, landscape, navigate, foster, facilitate, realm, paradigm, embark, journey, tapestry, myriad, multifaceted, seamless, cutting-edge

### Forbidden Phrases
- "The best part? ..." / "The secret? ..."
- "What if I told you..." / "Here's the thing..."
- "In today's fast-paced..." / "In the ever-evolving..."
- "In conclusion" / "In summary"
- "Let that sink in" / "Now more than ever"

### Dramatic Contrast Reveals (Priority #2)
- "Not on lessons. On fear."
- "Not the curriculum. The structure."
- "He didn't teach. He observed."
- Any "Not X. Y." fragment pattern

### Forbidden Patterns
- Staccato: "No fluff. No filler. Just results."
- Triple adjectives: "Bold, beautiful, brilliant"
- Negation structure: "No X. No Y. Just Z."

### Formatting Rules
- Use hyphens with spaces - like this - not em dashes
- No emojis in body content
- No bold for emphasis in articles
