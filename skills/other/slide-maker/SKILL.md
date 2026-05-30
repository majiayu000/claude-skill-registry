---
name: slide-maker
description: >-
  Create slide presentations from topics, URLs, PDFs, git repos, or vault notes.
  Use this skill when the user asks to make slides, create a presentation, build
  a deck, or says "slides about X". Handles research, synthesis, outline, and
  creation. Default output is reveal.js HTML; pptx available on request. Also
  handles editing existing slide decks (HTML or pptx). Triggers on /slides,
  /slide-maker, or any request involving presentation creation.
allowed-tools: Bash, Read, Write, Edit, Agent, Grep, Glob, WebFetch, WebSearch
argument-hint: "<topic, URLs, file paths, or vault notes>"
---

<Purpose>
End-to-end slide creation: from raw sources or a topic to a polished
presentation. Handles research, synthesis, outlining, and slide generation.
Produces self-contained reveal.js HTML by default (easy to edit, preview in any
browser). Can delegate to pptx skill when PowerPoint output is requested.
</Purpose>

<Use_When>
- User asks to create slides or a presentation about a topic
- User provides sources (URLs, PDFs, repos, vault notes) and wants slides
- User wants to edit an existing HTML or pptx slide deck
- User uses /slides or /slide-maker
</Use_When>

<Do_Not_Use_When>
- User wants a research note, not slides (use /research)
- User just wants to read/extract text from a pptx (use pptx skill directly)
</Do_Not_Use_When>

<Workspace>
All intermediate files go in `temp/slides/` (gitignored). Structure:
```
temp/slides/
├── research/          # Source research files (one per source)
├── images/            # Downloaded images (diagrams, charts, screenshots)
├── outline.md         # Approved outline
└── output.html        # Draft before copying to notes/slides/
```

Create workspace + output directories at the start of every session:
```bash
mkdir -p temp/slides/research temp/slides/images notes/slides
```

**Final output** always goes to `notes/slides/<presentation-name>.html` (or
`.pptx`). Images used by the presentation are copied to
`notes/slides/images/`. The `temp/slides/` workspace is for intermediate files
only.
</Workspace>

<Steps>

## Stage 1: PARSE — Classify Inputs

Parse $ARGUMENTS and any user context. Classify each input:

| Input type | Detection | Strategy |
|------------|-----------|----------|
| URL | starts with http(s):// | WebFetch + download images |
| Git repo | github.com or git URL | clone to temp, read key files |
| PDF | .pdf extension | Read tool (for local) or download |
| Vault note | `(Type) Name` or [[wikilink]] | Read via MCP or Read tool |
| Existing slides (.html) | .html extension | Editing mode |
| Existing slides (.pptx) | .pptx extension | Delegate to pptx skill |
| Raw topic | none of the above | WebSearch + WebFetch |

**Auto-detect research depth:**
- **Quick mode**: 1-2 simple sources or a short topic → inline research, no subagents
- **Thorough mode**: 3+ sources, complex topic, or broad request → parallel research agents

Present what was detected:
```
Detected sources:
1. [URL] blog post — will fetch + extract
2. [URL] paper PDF — will download and read
3. "transformer architecture" — will web search

Mode: thorough (3 sources → parallel research)
Proceeding to research...
```

Don't wait for confirmation unless something is ambiguous.

## Stage 2: DISCOVER — Understand the Goal

Before researching, understand what the user actually needs. Ask **up to 5
focused questions** in a single message. Adapt questions to what's already known
— skip anything the user already specified.

**Questions to consider** (pick the ones that aren't already answered):

1. **Goal & context** — What's this presentation for? (class lecture, team
   meeting, conference talk, pitch, self-study, sharing with a friend?)
2. **Audience** — Who's watching? (technical experts, general audience, exec
   stakeholders, students?) What do they already know?
3. **Language** — What language should the slides be in? (Don't assume English —
   the user may want slides in their native language or a mix)
4. **Angle & emphasis** — What's the ONE thing the audience should walk away
   with? Any specific aspects to emphasize or skip?
5. **Vibe & format** — Formal or casual? Dense/technical or visual/storytelling?
   Any color or style preferences? Dark or light theme?

**How to ask** — be conversational, not interrogation-style:

```
Before I start researching, a few quick questions so I build the right deck:

1. What's this for — conference talk, team meeting, class?
2. Who's the audience? What do they already know about [topic]?
3. What language should the slides be in?
4. Any specific angle — what should the audience walk away remembering?
5. Style preference — formal/minimal, bold/visual, dark/light theme?

(Skip any that don't apply — I'll use sensible defaults)
```

**After the user responds**, synthesize their answers into a **creative brief**
that guides all downstream stages. Save it to `temp/slides/brief.md`:

```markdown
# Creative Brief

**Topic**: [topic]
**Goal**: [what this presentation accomplishes]
**Audience**: [who, what they know, what they care about]
**Language**: [language for slide content]
**Key takeaway**: [the ONE thing the audience should remember]
**Tone**: [formal / casual / technical / storytelling / provocative]
**Style direction**: [dark/light, color mood, density level]
**Emphasis**: [specific aspects to highlight]
**Skip**: [anything the user explicitly wants to avoid]
**Format**: [reveal.js HTML / pptx]
**Duration**: [if mentioned — affects slide count]
```

**Palette selection**: Based on the brief, choose a palette from the Design
Principles table (or craft a custom one). The palette should feel designed for
THIS topic and THIS audience — not generic. Include your palette choice and
reasoning in the brief.

**Skip this stage when**:
- Editing an existing deck (the design decisions are already made)
- The user explicitly says "just do it" or provides all context upfront

Then proceed to research with the brief guiding what to look for.

## Stage 3: RESEARCH — Gather Information

### Thorough mode (3+ sources or complex topic)

Read the agent definition:
```
Read("${CLAUDE_SKILL_DIR}/agents/source-researcher.md")
```

Spawn one `source-researcher` agent per source, **all in parallel in a single
message**. Each agent:
- Receives: one source, its output file path, images directory
- Writes structured research to `temp/slides/research/source-NN-slug.md`
- Downloads relevant images to `temp/slides/images/`
- Returns a 3-5 sentence summary (keeps orchestrator context small)
- Uses **sonnet** model

```
Agent(
  model="sonnet",
  prompt="You are Source Researcher. Follow these instructions:

  [INSERT FULL CONTENT OF agents/source-researcher.md]

  SOURCE: [url/path/topic]
  SOURCE_NUMBER: [NN]
  OUTPUT_FILE: temp/slides/research/source-NN-slug.md
  IMAGES_DIR: temp/slides/images/

  Research this source and write findings to the output file.
  Return only a 3-5 sentence summary."
)
```

If a source fails, continue with what succeeded — note the failure.

For raw topics with no other sources, spawn one agent that does WebSearch
(2-3 queries) + WebFetch (top 3 results).

### Quick mode (1-2 simple sources)

Skip agents. Do inline research:
1. WebFetch each URL (or Read each file)
2. For raw topics: WebSearch + WebFetch top 2-3 results
3. Download key images to `temp/slides/images/`
4. Write a single research file to `temp/slides/research/source-01-topic.md`

### Image handling

During research (both modes), download diagrams, charts, and screenshots that
could enhance slides. Skip decorative/stock images. Save to
`temp/slides/images/` with descriptive names.

```bash
curl -sL "IMAGE_URL" -o temp/slides/images/descriptive-name.png
```

## Stage 4: OUTLINE — Synthesize + User Approval (MANDATORY)

Read all research files from disk:
```
Glob(pattern="temp/slides/research/*.md")
# Then Read each file
```

Read the creative brief from `temp/slides/brief.md` — use it to guide content
selection, ordering, emphasis, language, and tone.

Build a slide outline. Present it to the user:

```markdown
## Slide Outline

**Title**: [Presentation Title — in the brief's language]
**Audience**: [from brief]
**Language**: [from brief]
**Tone**: [from brief]
**Palette**: [from brief — name + hex values]
**Key takeaway**: [the ONE thing from the brief]
**Slides**: ~[N] slides

---

1. **Title Slide** — [title + subtitle]
2. **[Insight headline, not label]** — [2-3 key points] | Layout: [type]
3. **[Insight headline]** — [key points] | Image: [image-name.png]
4. ...
N. **Closing / Key Takeaways** — [summary points]
```

**Headline rule**: every slide headline should be an insight ("Attention is
$O(n^2)$ — that's the bottleneck"), not a label ("Attention Mechanism").

**ALWAYS wait for user approval before proceeding to Stage 4.**

The user may:
- Approve as-is → proceed
- Request changes → revise and re-present
- Add/remove slides → adjust

Save the approved outline to `temp/slides/outline.md`.

## Stage 5: CREATE or EDIT

### Path A: New reveal.js HTML deck (default)

Read the agent definition and template:
```
Read("${CLAUDE_SKILL_DIR}/agents/slide-writer.md")
Read("${CLAUDE_SKILL_DIR}/references/reveal-template.html")
```

Launch the slide-writer agent:
```
Agent(
  model="sonnet",
  prompt="You are Slide Writer. Follow these instructions:

  [INSERT FULL CONTENT OF agents/slide-writer.md]

  CREATIVE BRIEF:
  [content of temp/slides/brief.md]

  OUTLINE:
  [approved outline from temp/slides/outline.md]

  RESEARCH FILES (read each for detailed content):
  [list of temp/slides/research/*.md paths]

  IMAGE FILES AVAILABLE:
  [list of temp/slides/images/* paths]

  TEMPLATE:
  [reveal-template.html content]

  OUTPUT_FILE: temp/slides/output.html

  Build the presentation following the brief's language, tone, palette,
  and audience direction. Write the HTML to the output file."
)
```

### Path B: New pptx deck (when user explicitly requests PowerPoint)

**Option 1 — Convert from HTML (preferred, faster):**
First create the reveal.js HTML (Path A), then convert to pptx:
```bash
npx --yes -p pptxgenjs node "${CLAUDE_SKILL_DIR}/scripts/html2pptx.js" notes/slides/name.html notes/slides/name.pptx
```
This preserves palette, layouts, and content from the HTML. Review the
output and fix any issues.

**Option 2 — Direct pptx creation (for complex cases):**
Delegate to the pptx skill at `.agents/skills/pptx/`. Pass:
- Approved outline
- Research file paths
- Image paths
- Design choices from outline (palette, tone)

### Path C: Edit existing HTML slides

1. Read the existing HTML file
2. Apply requested changes using the Edit tool (HTML is plain text — trivial)
3. For structural changes (add/remove slides): read, modify section, write back

### Path D: Edit existing pptx

Delegate to pptx skill's unpack/edit/pack workflow.

## Stage 6: PREVIEW + ITERATE

After the slide-writer agent finishes:

1. Copy the HTML + images to their final location:
```bash
# Generate a slug from the presentation title
SLUG="presentation-name"  # kebab-case from title
cp temp/slides/output.html "notes/slides/${SLUG}.html"
# Copy any images referenced by the presentation
cp -r temp/slides/images/ "notes/slides/images/" 2>/dev/null || true
```

2. Tell the user:
```
Presentation created: notes/slides/[name].html

Open in your browser to preview (File → Open or drag into browser).
Let me know if you'd like any changes — I can edit individual slides,
adjust colors, reorder, add/remove content.

Need PowerPoint? I can export to .pptx too.
```

For iteration:
- HTML edits use the Edit tool directly on `notes/slides/[name].html`
- Fast — no rebuild needed, HTML is plain text
- Track which slides the user wants changed
- Apply targeted edits, not full regeneration

</Steps>

<Design_Principles>
Borrowed from the pptx skill — apply to ALL slide formats.

### Color Palettes
Pick a palette that matches the topic. Don't default to generic blue.

| Theme | Primary | Secondary | Accent |
|-------|---------|-----------|--------|
| **Midnight Executive** | `#1E2761` (navy) | `#CADCFC` (ice blue) | `#FFFFFF` (white) |
| **Forest & Moss** | `#2C5F2D` (forest) | `#97BC62` (moss) | `#F5F5F5` (cream) |
| **Coral Energy** | `#F96167` (coral) | `#F9E795` (gold) | `#2F3C7E` (navy) |
| **Warm Terracotta** | `#B85042` (terracotta) | `#E7E8D1` (sand) | `#A7BEAE` (sage) |
| **Ocean Gradient** | `#065A82` (deep blue) | `#1C7293` (teal) | `#21295C` (midnight) |
| **Charcoal Minimal** | `#36454F` (charcoal) | `#F2F2F2` (off-white) | `#212121` (black) |
| **Teal Trust** | `#028090` (teal) | `#00A896` (seafoam) | `#02C39A` (mint) |
| **Berry & Cream** | `#6D2E46` (berry) | `#A26769` (dusty rose) | `#ECE2D0` (cream) |
| **Cherry Bold** | `#990011` (cherry) | `#FCF6F5` (off-white) | `#2F3C7E` (navy) |

### Layout Rules
- **Every slide needs a visual element** — image, chart, diagram, large number, or shape
- **Vary layouts** — don't repeat the same structure across slides
- **Dominance over equality** — one color dominates (60-70%), others support
- **Dark/light contrast** — dark backgrounds for title + closing, light for content
- Layout options: two-column, icon+text rows, grids, half-bleed images, stat callouts, timelines

### Typography (for reveal.js)
- Use Google Fonts for variety (loaded via CDN in template)
- Title slides: 2.5-3em bold
- Slide headlines: 1.5-2em
- Body text: 0.9-1.1em
- Size contrast matters — headlines must visually dominate body text

### Avoid (Common Mistakes)
- Don't repeat the same layout across slides
- Don't center body text — left-align; center only titles
- Don't use low-contrast text
- Don't create text-only slides — add visual elements
- Don't default to blue — match the topic
- NEVER use accent lines under titles — hallmark of AI slides
- Don't cram too much on one slide — fewer points, more slides
</Design_Principles>

<Tool_Usage>
- **WebSearch**: Find sources for raw topics
- **WebFetch**: Fetch URL content, extract insights
- **Read/Glob**: Read local files, vault notes, research files
- **Agent**: Parallel source-researcher agents (sonnet), slide-writer agent (sonnet)
- **Write**: Create output HTML file, research files
- **Edit**: Iterate on existing HTML slides
- **Bash**: mkdir, curl (image downloads), file operations
</Tool_Usage>

<Examples>
<Good>
User: /slides about transformer architecture
1. Parse → raw topic, quick mode
2. Discover → asks: who's the audience? language? what angle? → user says "ML
   study group, English, focus on why attention replaced RNNs, dark theme"
3. Brief → audience: ML practitioners, key takeaway: attention enables parallelism,
   palette: Ocean Gradient (matches deep learning vibe), tone: technical but visual
4. Research → WebSearch 3 queries, fetch top results, download architecture diagram
5. Outline → 10 slides ordered around the "why attention wins" narrative
6. User approves with minor reorder
7. Create → reveal.js HTML, dark Ocean Gradient, diagrams embedded, speaker notes
8. Preview → user asks to add flash attention slide → Edit tool, done

User: ทำสไลด์จาก [url1] [url2] [url3] กับ (Paper) Scaling Laws
1. Parse → 3 URLs + 1 vault note, thorough mode
2. Discover → asks: ภาษาอะไร? กลุ่มเป้าหมาย? → user says "Thai slides, for team
   meeting, casual tone, bright colors"
3. Brief → language: Thai, audience: engineering team, palette: Coral Energy,
   tone: casual/visual
4. Research → 4 parallel agents, each writes research file
5. Outline → 12 Thai-language slides synthesizing across all sources
6. User approves
7. Create → slide-writer produces Thai HTML with Coral Energy palette
</Good>

<Bad>
- Skipping DISCOVER and assuming English, formal, blue theme
- Skipping the outline checkpoint and going straight to slides
- Putting all research content in agent prompts instead of writing to disk
- Creating text-only slides with no visual elements
- Using the same two-column layout for every slide
- Not downloading available images during research phase
- Ignoring user's language preference in the final slides
</Bad>
</Examples>

<Escalation_And_Stop_Conditions>
- **Too many sources (>8)**: Ask user to prioritize top 5-6
- **Source fetch fails**: Note failure, continue with remaining sources
- **User wants pptx**: Delegate to pptx skill after outline approval
- **Ambiguous topic**: Ask one clarifying question about audience/angle
- **Existing deck format unclear**: Ask user to confirm format
</Escalation_And_Stop_Conditions>

$ARGUMENTS
