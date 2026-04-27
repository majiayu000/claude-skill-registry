---
name: research-mission-generator
description: "Package conversation research into a GSD-ready mission package. Produces a three-stage Vision → Research → Mission pipeline as a LaTeX PDF following GSD/NASA SE methodology, designed to be handed to gsd-skill-creator for execution. Use this skill when the user has been discussing, researching, or brainstorming a topic and then asks to turn it into a research mission, research pack, mission package, or says 'package this as a mission', 'make this a research pack', 'turn this into a mission for skill-creator', 'create a research mission from this', or 'use the research mission skill'. The skill harvests findings, sources, and structure from the current conversation and any prior research, then produces the complete pipeline document. Also trigger if the user asks to 'create a research mission on [topic]' cold — in that case, conduct web research first, then package."
---

# Research Mission Generator

Package conversation research into publication-quality GSD mission packages. Produces a three-stage pipeline (Vision → Research → Mission) as a LaTeX PDF, ready for handoff to gsd-skill-creator.

## Primary Workflow

The typical pattern is:

1. **User has a conversation** — discussion, brainstorming, web research, thinking time, or any exploration of a topic
2. **User says "turn this into a research mission"** — triggering this skill
3. **Skill harvests the conversation** — extracting findings, sources, structure, and insights already developed
4. **Skill fills gaps** — conducting additional web research only where the conversation left holes
5. **Skill produces the package** — three-stage LaTeX PDF + .tex source + index.html
6. **User hands package to gsd-skill-creator** — for execution via Claude Code

The skill is a *structuring and packaging* tool, not a from-scratch generator. The intellectual work has already happened in conversation. This skill gives it bones.

## When to Use

**Primary triggers (conversation already happened):**
- "Turn this into a research mission"
- "Package this as a mission for skill-creator"
- "Make this a research pack"
- "Use the research mission skill on what we've discussed"
- "Create a mission package from this conversation"
- "Structure this for GSD"

**Secondary trigger (cold start — research needed first):**
- "Create a research mission on [topic]"
- "I want a deep research study into [topic]"
- In this case, conduct 3–6 web searches first (see Step 2b below), then proceed with packaging.

## Workflow

### Step 1: Harvest the Conversation

Scan the current conversation (and any referenced past conversations) to extract:

| Element | Where to Find It | Fallback |
|---------|-------------------|----------|
| **Topic & scope** | User's original question or framing | Ask user |
| **Key findings** | Research results, web search outputs, discussion points | Conduct web research |
| **Sources cited** | URLs, papers, organizations mentioned in conversation | Validate via web search |
| **Structure** | Natural groupings that emerged in discussion | Infer modules from topic |
| **Quantitative data** | Numbers, percentages, measurements discussed | Source from research |
| **Sensitivity areas** | Cultural, safety, or ethical concerns raised | Detect from domain |
| **Insights & connections** | Cross-topic relationships the user identified | Preserve in synthesis module |
| **User's framing** | Metaphors, analogies, philosophical angles | Carry into vision narrative and through-line |

**Critical:** Preserve the user's own insights, framings, and connections. The conversation is the primary source material. Don't replace the user's thinking with generic content — amplify it with structure.

### Step 2a: Gap Analysis (Conversation-Based)

After harvesting, identify what's missing for a complete three-stage package:

- **Vision gaps:** Is there a clear problem statement? Are there enough concrete problems (need 3–5)?
- **Research gaps:** Are all claims sourced? Are there modules with thin evidence?
- **Mission gaps:** Can the topic decompose into 4–6 parallelizable modules?

Conduct targeted web searches ONLY to fill identified gaps. Don't re-research what the conversation already covered well.

### Step 2b: Cold-Start Research (Topic-Only)

If the user provides just a topic without prior conversation, conduct full research:

1. **Broad overview** — `[topic] overview`
2. **Authoritative sources** — `[topic]` + relevant agency names
3. **Peer-reviewed findings** — `[topic] research study findings`
4. **Subtopic deep-dives** — One search per identified module
5. **Threats/challenges** — `[topic] threats challenges risks`
6. **Unique/endemic features** — `[topic] unique rare endemic`

**Source quality rules (ABSOLUTE):**
- Government agencies (USGS, USFS, NPS, NOAA, NIH, NASA, EPA, etc.)
- Peer-reviewed journals
- University research programs
- Professional organizations
- NEVER entertainment media, blogs, or unsourced claims

### Step 3: Identify Research Modules

Decompose into 4–6 research modules. Prefer modules that emerged naturally from conversation structure. Each module must be:

- **Self-contained** — An agent can produce it from its spec alone
- **Parallelizable** — At least 2 modules can run simultaneously
- **Connected** — At least one cross-module relationship exists

Common module patterns by domain:

| Domain | Typical Modules |
|--------|----------------|
| Ecology/Biology | Flora, Fauna, Fungi/Microbiome, Aquatic, Ecological Networks |
| Technology | Architecture, Implementation, Security, Performance, Integration |
| History | Context, Key Events, People, Consequences, Legacy |
| Social Science | Demographics, Causes, Effects, Interventions, Outcomes |
| Physical Science | Theory, Measurement, Analysis, Modeling, Implications |
| Education | Foundations, Curriculum, Methods, Assessment, Integration |
| Engineering | Requirements, Design, Implementation, Testing, Deployment |

### Step 4: Determine Mission Parameters

**Activation profile** — based on module count and complexity:

| Modules | Profile | Crew Size | Parallel Tracks |
|---------|---------|-----------|-----------------|
| 2–3 | Patrol | 7 roles | 1 |
| 4–5 | Squadron | 12 roles | 2 |
| 6+ | Fleet | Full crew | 3+ |

See `references/crew-profiles.md` for complete role assignments per profile.

**Model assignment** — apply the 30/60/10 principle:
- **Opus (~30%)** — Synthesis, cross-module integration, judgment-heavy analysis, cultural sensitivity
- **Sonnet (~60%)** — Survey compilation, document assembly, verification, structured content
- **Haiku (~10%)** — Shared schemas, templates, scaffolding

**Wave structure** — always follows this pattern:
- **Wave 0:** Foundation (shared schemas, source index) — Sequential, Haiku
- **Wave 1:** Parallel survey/research tracks — Parallel, Sonnet+Opus mix
- **Wave 2:** Synthesis (cross-module integration) — Sequential, Opus
- **Wave 3:** Publication + Verification — Sequential, Sonnet

### Step 5: Generate the LaTeX PDF

Read `references/latex-template.md` for the complete document template, color scheme selection, and formatting patterns. **Read it before writing any LaTeX.**

The template includes:
- Domain-adaptive color schemes (ecology=green/blue/brown, tech=steel/electric/graphite, etc.)
- Title page, TOC, headers/footers with page counts
- Stage header banners (`\stageheader`)
- ASCII diagram boxes (`asciibox` environment)
- Alternating-row tables with colored headers
- Quote boxes for closing through-line
- Full document skeleton showing every section

**Three stages in one document:**

1. **Stage 1: Vision Guide** — Narrative vision (use the user's own framing and metaphors), problem statement (3–5 problems), core concept, study region/architecture (ASCII diagrams), module descriptions, chipset configuration, scope boundaries, 8–12 success criteria, relationship to other GSD vision docs, through-line connecting to ecosystem philosophy
2. **Stage 2: Research Reference** — Source organizations, detailed findings per module (harvested from conversation + gap-fill research), quantitative data with citations, safety/sensitivity considerations, complete source bibliography
3. **Stage 3: Mission Package** — Milestone spec, deliverables table, component breakdown with model assignments, wave execution plan with parallel tracks, cache optimization strategy, dependency graph (ASCII), test plan (safety-critical + core + integration + edge cases), verification matrix mapping criteria to tests, crew manifest, execution summary

**Compile with XeLaTeX** (three passes):
```bash
xelatex -interaction=nonstopmode mission.tex
xelatex -interaction=nonstopmode mission.tex
xelatex -interaction=nonstopmode mission.tex
```

Produce both the PDF and `.tex` source so the user can modify and recompile.

### Step 6: Create Index Page

Generate `index.html` with:
- Header reflecting the topic's color scheme
- File cards with slightly darker backgrounds, clickable as download links (`<a href="..." download>`)
- Contents breakdown listing all three stages
- Usage instructions (how to feed to GSD/skill-creator)
- LaTeX recompilation instructions

### Step 7: Deliver

Present all three files (PDF, .tex, index.html). Keep the summary brief — the user can read the document themselves.

## Conversation Harvesting Patterns

### Preserving User Voice

The vision narrative should echo the user's own language, metaphors, and philosophical framing. If the user described the topic with a particular analogy during conversation, that analogy should appear in the Vision section. The through-line should connect to the GSD ecosystem philosophy (Amiga Principle, spaces between, humane flow) in a way that feels natural to the domain.

### Thinking Time Sessions

If the conversation included "thinking time" sessions (user describing complex thought processes while Claude listens), the insights from those sessions are the highest-priority content for the vision and synthesis modules. These represent the user's original thinking and should be preserved with fidelity.

### Multi-Conversation Continuity

If the user references past conversations about the topic, use the conversation search tools to retrieve relevant context. The mission package should integrate findings across sessions, not just the current one.

### Research Already Done

If web searches were already conducted during the conversation, extract the findings and sources directly — don't re-search the same queries. Only search for gaps.

## Quality Checks

Before delivering, verify:

- [ ] Conversation insights are faithfully represented (not replaced with generic content)
- [ ] Vision narrative uses the user's own framing and metaphors where possible
- [ ] Problem statement has 3–5 concrete, recognizable problems
- [ ] Success criteria are testable (8–12 criteria, each observable and specific)
- [ ] All sources are professional organizations or peer-reviewed research
- [ ] Wave plan maximizes parallelism with correct dependency ordering
- [ ] Model assignments follow 30/60/10 Opus/Sonnet/Haiku split
- [ ] Test plan has 2–4 tests per success criterion
- [ ] Safety-critical tests are marked mandatory-pass / BLOCK
- [ ] Each component spec is self-contained
- [ ] LaTeX compiles without errors (three passes)
- [ ] Through-line connects to GSD ecosystem philosophy
- [ ] Sensitivity considerations addressed for the domain
- [ ] Package is ready for handoff to gsd-skill-creator with zero additional context

## Safety Boundaries

These apply to ALL research missions regardless of topic:

| Rule | Boundary Type |
|------|---------------|
| All sources must be professional organizations, peer-reviewed, or government agencies | ABSOLUTE |
| Never publish precise locations of endangered species | ABSOLUTE |
| Use nation-specific names for Indigenous peoples (never generic) | ABSOLUTE |
| Climate/health projections from published agency data only | GATE |
| All numerical claims attributed to specific sources | GATE |
| Present evidence without policy advocacy | ANNOTATE |

## Reference Files

- `references/latex-template.md` — Complete XeLaTeX document template with domain-adaptive color schemes, typography, table styles, tcolorbox environments, section formatting, and full document skeleton. **Read this before generating any LaTeX.**
- `references/crew-profiles.md` — Activation profiles (Patrol/Squadron/Fleet) with complete role assignments, CRAFT agent naming conventions, and communication loop architecture.
- `references/test-patterns.md` — Test plan templates, universal safety-critical tests, and domain-specific test patterns for core functionality, integration, and edge cases.

## Ecosystem Patterns

This skill implements these GSD ecosystem patterns:

- **Mission Control Pattern** — Each component spec is a complete flight plan
- **Safety Warden Pattern** — Safety-critical tests are mandatory-pass gates
- **Progressive Disclosure** — Three reading speeds (glance/scan/read) in all output
- **Amiga Principle** — Architectural leverage over brute-force research
- **Humane Flow** — Research supports understanding, never overwhelms

## Example Invocations

**After a conversation (primary use):**
- "OK, turn this into a research mission"
- "Package what we've discussed as a mission for skill-creator"
- "Make a research pack from this conversation"
- "Use the research mission generator on everything we've covered"
- "Structure this for GSD and give me the PDF"

**Cold start (secondary use):**
- "Create a research mission on coral reef bleaching in the Great Barrier Reef"
- "I want a deep research study into urban heat island effects"
- "Research mission: the neuroscience of musical perception"
