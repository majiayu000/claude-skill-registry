---
name: content-os
description: "Content OS orchestrator - the master skill that produces ALL content types from one seed idea (forward mode) or splits long-form content into short-form pieces (backward mode). Invokes research, writing, quality review, and visual generation skills in a coordinated pipeline. Long-form content goes through full quality gates; short-form gets quick accuracy pass."
---

# Content OS: Multi-Format Content Orchestrator

**The "produce everything" button.** Give one seed idea → get all content types. Or give long-form content → get it split into short-form pieces.

## Quick Start

### Forward Mode (Seed → All Content)
```
User: "Content OS: Statins myth-busting for Indians"

Output:
├── Long-form (quality-passed)
│   ├── YouTube script (Hinglish)
│   ├── Newsletter (B2C - patients)
│   ├── Newsletter (B2B - doctors)
│   ├── Editorial
│   └── Blog post
├── Short-form (accuracy-checked)
│   ├── 5-10 tweets
│   ├── 1 thread
│   └── Carousel content
└── Visual
    ├── Instagram carousel slides
    └── Infographic concepts
```

### Backward Mode (Long-form → Split)
```
User: "Content OS: [paste your blog/script/newsletter]"

Output:
├── 5-10 tweets (key points)
├── 1 thread (condensed narrative)
├── Carousel slides (visual summary)
└── Snippets (quotable sections)
```

## How It Works

### Mode Detection
- **Forward Mode**: Input is a topic/idea (short text, question, or concept)
- **Backward Mode**: Input is existing long-form content (>500 words)

### Forward Mode Pipeline

```
PHASE 1: RESEARCH
│
├── PubMed MCP
│   └── Search for relevant papers, trials, guidelines
│
├── knowledge-pipeline (RAG)
│   └── Query AstraDB for ACC/ESC/ADA guidelines, textbooks
│
├── social-media-trends-research (optional)
│   └── Check trending angles, audience questions
│
└── OUTPUT: research-brief.md
    └── Synthesized knowledge with citations

PHASE 2: LONG-FORM CONTENT (Full Quality Pipeline)
│
├── youtube-script-master
│   └── Hinglish script → Quality Review → Final
│
├── cardiology-newsletter-writer
│   └── B2C newsletter → Quality Review → Final
│
├── medical-newsletter-writer
│   └── B2B newsletter → Quality Review → Final
│
├── cardiology-editorial
│   └── Editorial → Quality Review → Final
│
└── cardiology-writer
    └── Blog post → Quality Review → Final

PHASE 3: SHORT-FORM CONTENT (Quick Accuracy Pass)
│
├── x-post-creator-skill
│   └── 5-10 tweets → Accuracy Check → Final
│
├── twitter-longform-medical
│   └── Thread → Accuracy Check → Final
│
└── Extract carousel content from long-form

PHASE 4: VISUAL CONTENT
│
├── carousel-generator
│   └── Generate Instagram slides from key points
│
└── cardiology-visual-system
    └── Infographic concepts (if data-heavy)

PHASE 5: OUTPUT
│
└── Organized folder structure with all content
```

### Backward Mode Pipeline

```
PHASE 1: ANALYZE
│
└── Parse long-form content
    ├── Extract key points
    ├── Identify data/statistics
    ├── Find quotable sections
    └── Determine topic/theme

PHASE 2: SPLIT (Quick Accuracy Pass)
│
├── Generate tweets (5-10)
│   └── One key point per tweet
│
├── Generate thread
│   └── Condensed narrative
│
├── Extract carousel content
│   └── Key points for slides
│
└── Create snippets
    └── Quotable sections

PHASE 3: VISUAL
│
└── carousel-generator
    └── Generate slides from extracted content

PHASE 4: OUTPUT
│
└── All short-form pieces organized
```

## Quality Gates

### Long-Form Quality Pipeline (FULL)

Each long-form piece goes through:

1. **scientific-critical-thinking**
   - Evidence rigor check
   - Citation verification
   - Claim accuracy
   - Statistical interpretation

2. **peer-review**
   - Methodology review
   - Logical consistency
   - Completeness check
   - Counter-argument consideration

3. **content-reflection**
   - Pre-publish QA
   - Audience appropriateness
   - Clarity check
   - Structure review

4. **authentic-voice**
   - Anti-AI pattern removal
   - Voice consistency
   - Natural language check

### Short-Form Accuracy Pass (QUICK)

Each short-form piece gets:

1. **Data Interpretation Check**
   - Are trial results stated correctly?
   - Are statistics accurately represented?
   - Is the study conclusion not misrepresented?
   - Are effect sizes/NNT/HR correctly stated?

This is a sanity check, not full review. User can iterate manually.

## Skills Invoked

### Research Skills
| Skill | Purpose |
|-------|---------|
| `knowledge-pipeline` | RAG + PubMed synthesis |
| PubMed MCP | Direct paper search |
| `social-media-trends-research` | Trending angles |

### Writing Skills
| Skill | Content Type | Quality Gate |
|-------|--------------|--------------|
| `youtube-script-master` | YouTube script (Hinglish) | Full |
| `cardiology-newsletter-writer` | Patient newsletter | Full |
| `medical-newsletter-writer` | Doctor newsletter | Full |
| `cardiology-editorial` | Editorial | Full |
| `cardiology-writer` | Blog post | Full |
| `x-post-creator-skill` | Tweets | Quick |
| `twitter-longform-medical` | Thread | Quick |

### Quality Skills
| Skill | Purpose | Used For |
|-------|---------|----------|
| `scientific-critical-thinking` | Evidence rigor | Long-form |
| `peer-review` | Methodology check | Long-form |
| `content-reflection` | Pre-publish QA | Long-form |
| `authentic-voice` | Anti-AI cleanup | Long-form |

### Visual Skills
| Skill | Purpose |
|-------|---------|
| `carousel-generator` | Instagram slides |
| `cardiology-visual-system` | Infographics |

### Repurposing Skills
| Skill | Purpose |
|-------|---------|
| `cardiology-content-repurposer` | Backward mode splitting |

## Output Structure

```
/output/content-os/[topic-slug]/
├── research/
│   └── research-brief.md           # Foundation for all content
│
├── long-form/                       # Full quality pipeline
│   ├── youtube-script.md           ✓ Quality passed
│   ├── newsletter-b2c.md           ✓ Quality passed
│   ├── newsletter-b2b.md           ✓ Quality passed
│   ├── editorial.md                ✓ Quality passed
│   └── blog.md                     ✓ Quality passed
│
├── short-form/                      # Quick accuracy pass
│   ├── tweets.md                   ✓ Accuracy checked
│   ├── thread.md                   ✓ Accuracy checked
│   └── snippets.md                 ✓ Accuracy checked
│
├── visual/
│   ├── carousel/
│   │   └── slide-01.png...
│   └── infographic-concepts.md
│
└── summary.md                       # What was produced
```

## Invocation Examples

### Forward Mode
```
"Content OS: GLP-1 agonists cardiovascular benefits"
"Content OS: Statin myths for Indian patients"
"Content OS: When to get a CAC score"
"Content OS: SGLT2 inhibitors in heart failure"
```

### Backward Mode
```
"Content OS: [paste your 2000-word blog post]"
"Content OS: [paste your YouTube script]"
"Content OS: [paste your newsletter]"
```

## Configuration

### What Gets Produced (Forward Mode)

| Content Type | Default | Can Skip |
|--------------|---------|----------|
| YouTube Script | Yes | Yes |
| Newsletter B2C | Yes | Yes |
| Newsletter B2B | Yes | Yes |
| Editorial | Yes | Yes |
| Blog | Yes | Yes |
| Tweets | Yes | Yes |
| Thread | Yes | Yes |
| Carousel | Yes | Yes |

### Customization
```
"Content OS: Statins - only YouTube and tweets"
"Content OS: Heart failure - skip editorial"
"Content OS: CAC scoring - long-form only"
```

## Integration with Existing System

Content OS orchestrates skills that already exist in your system. It doesn't replace them - it coordinates them.

You can still use individual skills directly:
- `youtube-script-master` for just a script
- `x-post-creator-skill` for just tweets
- `carousel-generator` for just slides

Content OS is for when you want **everything at once**.

## Notes

- Long-form content takes longer due to quality pipeline
- Short-form is faster (quick accuracy pass only)
- Research phase runs once, shared by all content
- Visual content generated from text output
- All content uses same research foundation for consistency

## Voice & Quality Standards

All content follows:
- **YouTube**: Peter Attia depth + Hinglish (70% Hindi / 30% English)
- **Twitter/Writing**: Eric Topol Ground Truths style
- **B2B (Doctors)**: JACC editorial voice
- **Anti-AI**: No "It's important to note", no excessive hedging
- **Citations**: Q1 journals, specific statistics, NNT/HR/CI when relevant
