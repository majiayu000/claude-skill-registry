---
name: seo-content-production
description: End-to-end workflow for creating SEO-optimized content from topic selection through publication. This skill should be used when writing comparison articles, curriculum guides, pillar content, or any article targeting search keywords. Orchestrates seomachine (data), quality-loop (QA), and webflow-publish (CMS).
---

# SEO Content Production

Complete workflow from keyword research to publication. This skill orchestrates other skills - it does not duplicate their functionality.

## Workflow Overview

```
RESEARCH → STRUCTURE → SOURCES → DRAFT → QUALITY → PUBLISH
    │           │          │        │        │         │
seomachine   outline   proprietary  write   quality   webflow
                       content              -loop     -publish
```

---

## Phase 1: Research

### Use `seomachine` for Data

All SEO data comes from the `seomachine` skill. DO NOT hardcode credentials.

**Credentials:** Stored in vault `.env` file:
- `DATAFORSEO_LOGIN`, `DATAFORSEO_PASSWORD` - Keyword research
- `GA4_PROPERTY_ID`, `GOOGLE_SERVICE_ACCOUNT_PATH` - Traffic data
- `GSC_SITE_URL` - Search Console data

**Common research tasks:**

```python
# Keyword research
import sys
sys.path.insert(0, ".claude/skills/seomachine/modules")
from dataforseo import DataForSEO

dfs = DataForSEO()
ideas = dfs.get_keyword_ideas("waldorf vs montessori", limit=50)
questions = dfs.get_questions("homeschool curriculum", limit=20)
serp = dfs.get_serp_data("best homeschool math curriculum")
```

```bash
# Generate content brief with competitor analysis
python3 .claude/skills/seomachine/scripts/content_brief_generator.py "keyword phrase"

# Find keyword gaps vs competitors
python3 .claude/skills/seomachine/scripts/competitor_gap_finder.py --batch --min-volume 200
```

### Validation Criteria

Before proceeding:
- [ ] Search volume > 500/month
- [ ] Keyword difficulty < 30 (winnable)
- [ ] Topic aligns with OpenEd expertise
- [ ] We have (or can create) proprietary perspective

---

## Phase 2: Structure

### Identify OpenEd's Unique Angle

Before outlining, answer:
1. What does OpenEd believe about this topic? (Check `opened-identity` skill)
2. What can we say that competitors can't? (Podcast quotes, staff expertise)
3. What do most articles get wrong or avoid?

### Content Type Templates

Templates are in `references/content-templates.md`. Common types:

| Type | Length | When to Use |
|------|--------|-------------|
| Comparison | 2000-3000 | X vs Y searches |
| Pillar Guide | 2500-3500 | "Complete guide to X" |
| How-To | 2000-2500 | "How to X" searches |
| Listicle | 1500-2500 | "Best X for Y" searches |

---

## Phase 3: Source Compilation

### Search Order (Priority)

1. **OpenEd Book** - `.claude/references/OpenEdBook/`
2. **Published Content** - Search Master Content Index
3. **Podcast Transcripts** - Grep `Published Content/Podcasts/`
4. **Staff Knowledge** - Tag relevant team members
5. **External Research** - Fill remaining gaps

### Source Search Commands

```bash
# Search published content
grep -rli "topic" "Published Content/" | head -20

# Check Master Content Index
grep -B5 "Tags:.*homeschool" ".claude/references/Master_Content_Index.md"
```

---

## Phase 4: Draft

### Before Writing

- [ ] Research brief complete (from seomachine)
- [ ] Unique angle identified
- [ ] Sources compiled
- [ ] Internal links planned (3+ minimum)

### Writing Constraints

Apply these skills automatically:
- `ai-tells` - Patterns to avoid
- `ghostwriter` - Authentic voice techniques

**Key rules:**
- Hook first (not definitions)
- Table early (for skimmers)
- 5+ internal links, 2-3 external
- Use spaced hyphens - not em dashes

### AI-isms to Eliminate

See `references/ai-tells-quick-reference.md` for full list.

**Kill words:** delve, comprehensive, crucial, leverage, landscape, navigate, foster, facilitate, realm, paradigm, journey, tapestry, myriad, seamless

**Kill patterns:**
- "It's not just X - it's Y" (correlative constructions)
- "In today's fast-paced world..."
- "Let's dive in..."
- "The best part? ..."

---

## Phase 5: Quality Control

### Use `quality-loop` Skill

Run every draft through 5 judges:

| Judge | Type | Checks |
|-------|------|--------|
| Human Detector | BLOCKING | AI tells, correlative constructions |
| Accuracy Checker | BLOCKING | Facts verified against sources |
| OpenEd Voice | BLOCKING | Brand alignment, not preachy |
| Reader Advocate | BLOCKING | Engaging, logical flow |
| SEO Advisor | ADVISORY | Keywords, links, meta elements |

### Quick Checks (Grep Patterns)

```bash
# Forbidden words
grep -inE "delve|comprehensive|crucial|leverage|landscape" DRAFT*.md

# Correlative constructions
grep -inE "isn't just|not just .* - it's" DRAFT*.md

# Em dashes (should be hyphens with spaces)
grep -n "—" DRAFT*.md

# Internal link count
grep -oE '\(https://opened\.co[^)]*\)|\(/[^)]*\)' DRAFT*.md | wc -l
```

---

## Phase 6: Visuals

### Use `nano-banana-image-generator` Skill

| Asset | Dimensions | Style |
|-------|------------|-------|
| Thumbnail | 16:9 | watercolor-line |
| Social card | 1:1, 4:5 | brand colors |

**Comparison article concepts:**
- Two hands offering different gifts
- Split path through two environments
- Same tree with different root systems

---

## Phase 7: Publish

### Use `webflow-publish` Skill

Pre-publish checklist:
- [ ] All blocking judges passed
- [ ] Thumbnail created
- [ ] Meta elements finalized
- [ ] Internal/external links verified

### Post-Publish

1. Update articles that should link TO this piece
2. Sync Master Content Index
3. Schedule social promotion via `newsletter-to-social`

---

## Skill Dependencies

| Phase | Primary Skill | Purpose |
|-------|---------------|---------|
| Research | `seomachine` | DataForSEO, GSC, GA4 data |
| Structure | `opened-identity` | Brand perspective |
| Draft | `ai-tells`, `ghostwriter` | Writing quality |
| Quality | `quality-loop` | 5-judge review |
| Visuals | `nano-banana-image-generator` | Thumbnails |
| Publish | `webflow-publish` | CMS upload |
| Social | `newsletter-to-social` | Derivative posts |

---

## Project Folder Structure

```
Studio/SEO Content Production/[Topic]/
├── SEO_RESEARCH_BRIEF.md   # From seomachine
├── SOURCES.md              # Compiled proprietary sources
├── OUTLINE.md              # Approved structure
├── DRAFT_v1.md             # First draft
├── DRAFT_v2.md             # Post-quality-loop
└── thumbnail-final.png     # Header image
```

---

## Quick Start

```
1. Validate topic with seomachine
   → Volume > 500, KD < 30, OpenEd has perspective

2. Create folder: Studio/SEO Content Production/[Topic]/

3. Run research: seomachine content brief + competitor gap

4. Compile sources: OpenEd book → Published → Podcasts → External

5. Get outline approved: Structure + unique angle

6. Draft with constraints: ai-tells + ghostwriter + internal links

7. Quality loop: 5 judges, fix blocking issues

8. Create thumbnail: nano-banana-image-generator

9. Publish: webflow-publish → newsletter-to-social
```

---

*Refactored: 2026-01-29 (consolidated from seo-content-writer, removed credential exposure)*
