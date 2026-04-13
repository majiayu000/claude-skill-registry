---
name: baoyu-diagram
description: Generates publication-ready SVG diagrams — flowcharts, sequence/protocol diagrams, structural/architecture diagrams, and illustrative intuition diagrams — by writing real SVG code directly following a cohesive design system. Supports both single-diagram mode (topic-based) and multi-diagram mode (analyze article content and generate multiple diagrams at identified positions). Use whenever the user asks to "draw a flowchart", "draw a sequence diagram", "show the OAuth / TCP / auth protocol", "make an architecture diagram", "explain how X works visually", "illustrate this article with diagrams", "为文章画图解", "画流程图", "画时序图", "画架构图", "画示意图", "画图解", or wants clean, embeddable vector diagrams for articles, WeChat posts, slides, or docs. Output is one or more self-contained .svg files that render correctly in light and dark mode anywhere they are embedded.
version: 1.1.0
metadata:
  openclaw:
    homepage: https://github.com/JimLiu/baoyu-skills#baoyu-diagram
---

# Diagram Generator

Write **real SVG code** directly, following a consistent design system, the output is self-contained `.svg` files (embedded styles, auto dark-mode), editable by humans, scales to any size without quality loss, and embeds cleanly into articles, WeChat posts, slide decks, Notion, and markdown.

When given article or document content, the skill analyzes structure, identifies concepts that benefit from diagramming, and generates multiple diagrams — each with its own type, layout plan, and SVG. When given a single topic, it generates one diagram.

This is not an image-generation skill — it does not call any LLM image model. Claude writes the SVG node-by-node, doing the layout math by hand so every diagram honors the rules in `references/`.

## Usage

### Single-diagram mode

```bash
# Prompt for the topic if no argument given
/baoyu-diagram

# Plain-text description
/baoyu-diagram "how JWT authentication works"

# Path to a markdown file as source content (single diagram about one topic)
/baoyu-diagram path/to/content.md --mode single

# Force a specific diagram type
/baoyu-diagram "transformer attention"    --type illustrative
/baoyu-diagram "Kubernetes architecture"  --type structural
/baoyu-diagram "CI/CD pipeline"           --type flowchart
/baoyu-diagram "OAuth 2.0 flow"           --type sequence
/baoyu-diagram "Shape hierarchy"          --type class

# Language and output path
/baoyu-diagram "微服务架构"              --lang zh
/baoyu-diagram "build pipeline" --out docs/build-pipeline.svg
```

### Multi-diagram mode

```bash
# Analyze article and generate diagrams at identified positions
/baoyu-diagram path/to/article.md

# With density control
/baoyu-diagram path/to/article.md --density balanced
/baoyu-diagram path/to/article.md --density per-section --lang zh

# Force multi mode on pasted content
/baoyu-diagram --mode multi
```

### Mode detection

| Signal | Mode |
|--------|------|
| File path to `.md` / `.txt` (unless `--mode single`) | **Multi** |
| Multi-paragraph pasted content (unless `--mode single`) | **Multi** |
| Short quoted topic string (under ~100 chars, no markdown structure) | **Single** |
| `--type` given | **Single** (forces) |
| `--out` given | **Single** (forces) |
| `--mode single` or `--mode multi` | Forced by flag |
| Ambiguous | Ask with AskUserQuestion |

## Options

| Option | Values |
|--------|--------|
| `--type` | `flowchart`, `sequence`, `structural`, `illustrative`, `class`, `auto` (default — route on verb). Forces single-diagram mode. |
| `--lang` | `en`, `zh`, `ja`, `ko`, ... (default: match the user's language) |
| `--out` | Output file path (default: `diagram/{slug}/diagram.svg`). Forces single-diagram mode. |
| `--density` | `minimal` (1-2), `balanced` (3-5, default), `per-section`, `rich` (6+). Multi-diagram mode only. |
| `--mode` | `single`, `multi`, `auto` (default). Override automatic mode detection. |

## Diagram types

Pick the type by what the reader needs, not by the noun in the prompt.

**The primary test**: is the reader trying to *document* this, or *understand* it? Documentation wants precision — flowchart, sequence, or structural. Understanding wants the right mental model — illustrative.

| Type | Reader need | Route on verbs like | Reference |
|------|-------------|---------------------|-----------|
| **Flowchart** | Walk me through the steps, in order | "walk through", "steps", "process", "lifecycle", "workflow", "state machine", "gate", "router", "parallelization", "orchestrator", "evaluator" | `references/flowchart.md` |
| **Flowchart (phase band)** | Walk me through each phase; show the tools at each stage | "phase 1/2/3", "multi-phase operation", "each phase has tools", "attack phases", "phased workflow", "security operation phases", "penetration test stages", "phase N feeds phase N+1" | `references/flowchart-phase-bands.md` |
| **Sequence** | Who talks to whom, in what order | "protocol", "handshake", "auth flow", "OAuth", "TCP", "TLS", "gRPC", "request/response", "who calls what", "exchange between", "round trip", "webhook" | `references/sequence.md` |
| **Structural** | Show me what's inside what, how it's organized | "architecture", "organised", "components", "layout", "what's inside", "topology", "subsystem", "two systems", "side by side", "foreground + background" | `references/structural.md` |
| **Illustrative** | Give me the intuition — draw the mechanism | "how does X work", "explain X", "I don't get X", "intuition for", "why does X do Y", "LLM with tools", "agent and environment", "central + attachments" | `references/illustrative.md` |
| **Class** | What are the types and how are they related | "class diagram", "UML", "inheritance", "interface", "schema", "types and subtypes", "data model" | `references/class.md` |

**Routing heuristic**: "how does X work" is the default ambiguous case. Prefer **illustrative** unless the user specifically asks for steps or components. A diagram that makes the reader feel "oh, *that's* what it's doing" is illustrative — even if the subject is software.

**Multi-actor test for sequence**: if the prompt names ≥2 distinct actors/participants/services (User + Server, Client + Auth + Resource, Browser + CDN + Origin), prefer **sequence** even when the verb is "flow" or "process". Single-actor "X flow" (build pipeline, request lifecycle, GC) stays flowchart. When you pick sequence for a multi-actor reason, announce it: *"Picked sequence because the prompt names N actors (…). Rerun with `--type flowchart` to force the step-list version."*

**Worked examples of verb-based routing**: same subject, different diagram depending on what was asked. Use these as a sanity check after picking a type.

| User says                                 | Type         | What to draw                                                                     |
|-------------------------------------------|--------------|----------------------------------------------------------------------------------|
| "how do LLMs work"                        | Illustrative | Token row, stacked layer slabs, attention threads across layers.                 |
| "transformer architecture / components"   | Structural   | Labeled boxes: embedding, attention heads, FFN, layer norm.                      |
| "how does attention work"                 | Illustrative | One query token, fan of lines to every key, line thickness = weight.             |
| "how does gradient descent work"          | Illustrative | Contour surface, a ball rolling down, a trail of discrete steps.                 |
| "what are the training steps"             | Flowchart    | Forward → loss → backward → update.                                              |
| "how does TCP work"                       | Illustrative | Two endpoints, numbered packets in flight, an ACK returning.                     |
| "TCP handshake sequence"                  | Sequence     | SYN → SYN-ACK → ACK between client and server lifelines.                         |
| "how does a hash map work"                | Illustrative | Key falling through a hash function into one of N buckets.                       |
| "LLM with retrieval, tools, memory"       | Illustrative | Central LLM subject with dashed radial spokes to three labeled attachments.      |
| "gate pattern with pass/fail exit"        | Flowchart    | Pill In → LLM → Gate → LLM → LLM → pill Out, with a dashed Fail branch to Exit.  |
| "LLM router / parallelization"            | Flowchart    | Simple fan-out: pill In → hub → 3 branches → aggregator → pill Out.              |
| "Pi session + background analyzer"        | Structural (subsystem) | Two dashed sibling containers side by side, each with a short internal flow, labeled cross-system arrows. |
| "prompt engineering vs. context engineering" | Structural (subsystem) | Two sibling containers, each showing its internal mechanism with cross-links.           |
| "agent + environment loop"                | Illustrative | Human pill ↔ LLM rect ↔ Environment pill, Action/Feedback labels on the edges.   |
| "Claude Code workflow with sub-loops"     | Sequence     | 4 actors with 1–2 dashed message frames labeled "Until tests pass" / "Until tasks clear". |
| "generator-verifier loop"                 | Flowchart    | Outer loop container; two boxes with green ✓ / coral ✗ status circles on the return edge. See `flowchart.md` → "Loop container" + "Status-circle junctions". |
| "from TODOs to tasks"                     | Structural (subsystem) | Two siblings: left = checklist (checkbox glyphs); right = DAG of task nodes with one dashed future-state node. See `structural.md` → "Rich interior" + "Dashed future-state node". |
| "finding the sweet spot"                  | Illustrative | Horizontal spectrum axis between two opposing labels; option boxes under tick points with the middle one highlighted. See `illustrative.md` → "Spectrum / continuum". |
| "agent teams with task queue"             | Flowchart    | Queue glyph inside the lead box, then vertical fan-out to workers. See `flowchart.md` → "Queue glyph inside box" + "Vertical fan-out". |
| "message bus architecture"                | Structural   | Central horizontal bar + agents above/below, each linked by a publish/subscribe arrow pair. See `structural.md` → "Bus topology". |
| "shared state store"                      | Structural   | Central hub with a doc icon + 4 corner satellites, bidirectional arrow pairs. See `structural.md` → "Radial star topology". |
| "orchestrator vs. agent teams"            | Structural (subsystem) | Two siblings; left = hub + fan-out; right = queue + vertical fan-out. See `structural.md` → "Rich interior for subsystem containers". |
| "orchestrator vs. message bus"            | Structural (subsystem) | Two siblings; left = hub + fan-out; right = mini bus topology. See `structural.md` → "Rich interior". |
| "advisor strategy"                        | Structural   | Single container, multi-line box bodies (title/role/meta), mixed solid+dashed+bidirectional arrows with a legend strip. See `structural.md` → "Mixed arrow semantics" + "Multi-line box body". |
| "tool calling vs. programmatic"           | Sequence     | Parallel independent rounds — left = stacked rounds; right = stacked rounds wrapped in a tall script box. See `sequence.md` → "Parallel independent rounds". |
| "Claude + environment + skill"            | Illustrative | Two subject boxes with a bidirectional arrow; annotation circle at the midpoint labels the skill. See `illustrative.md` → "Annotation circle on connector". |
| "code execution vs. dedicated tool"       | Structural (subsystem) | Two siblings; left = Computer box with nested Terminal; right = Claude with an attached gadget box for Tools. See `structural.md` → "Rich interior" + "Attached gadget box". |
| "Shape inheritance / class hierarchy"     | Class        | 3-compartment rects (name / attrs / methods) with hollow-triangle inheritance arrows. See `class.md`.                                               |
| "order lifecycle / status transitions"    | Flowchart (state machine) | State rects + initial/final markers + `event [guard] / action` transition labels. See `flowchart.md` → "State machine".                           |
| "network topology (3-tier)"               | Structural (network) | Dashed zone containers (Internet / DMZ / Internal) + labeled device rects. See `structural.md` → "Network topology".                               |
| "database comparison matrix"              | Structural (matrix) | Header row + zebra-striped body rows with ✓/✗ glyphs in cells. See `structural.md` → "Comparison matrix".                                           |
| "multi-phase attack / each phase has tools" | Flowchart (phase band) | Stacked dashed phase bands; compact tool cards with icons in each band; colored cross-band arrows (normal / exploit / findings); operator icons on left. See `flowchart-phase-bands.md`. |
| "phased workflow / phase 1 recon phase 2 exploit" | Flowchart (phase band) | Phase labels as eyebrow text; tool card rows centered in each band; side annotations; legend strip. See `flowchart-phase-bands.md`. |

**Most common routing failure**: picking a flowchart because it feels safer when an illustrative diagram would give the reader more insight. Illustrative is the more ambitious choice, and almost always the right one when the reader needs understanding rather than documentation.

Cycles, ERDs, and gantt charts are **out of scope for v1**. For cycles, draw the stages linearly with a small `↻ returns to start` return glyph (see `flowchart.md`). For ERDs, suggest a dedicated tool (mermaid, plantuml) — do not attempt to fake them in pure SVG.

## Workflow

### Step 1: Detect mode and capture input

Read the user's prompt, content file, or pasted content. Determine the mode:

| Signal | Mode |
|--------|------|
| Short topic string, `--type` given, or `--out` given | **Single** |
| File path to `.md` / `.txt`, or multi-paragraph pasted content | **Multi** |
| `--mode single` or `--mode multi` | Forced by flag |
| Ambiguous (medium-length text, unclear if topic or content) | Ask with AskUserQuestion |

**Single mode** → jump to Step 5.

**Multi mode** → continue to Step 2.

If input is a file path, read the file. If input is pasted content, note it for saving later. If no input at all, ask for it with AskUserQuestion.

### Step 2: Analyze content (multi-diagram mode)

Analyze the article or document for diagramming opportunities. For each section or concept cluster, determine:

| Analysis | Output |
|----------|--------|
| Content structure | Sections, subsections, key transitions |
| Core concepts | 2-8 concepts that benefit from visual explanation |
| Diagram positions | Where in the article each diagram belongs (anchored to specific paragraphs or headings) |
| Per-position type signal | What verb/need drives each diagram (→ routing table in "Diagram types") |
| Per-position complexity | Simple (3-4 nodes) vs. complex (poster/subsystem) |

**What to diagram:**
- Core mechanisms the reader needs to *understand* (→ illustrative)
- Multi-step processes described in prose (→ flowchart)
- Multi-actor interactions (→ sequence)
- Architectural descriptions with containment or hierarchy (→ structural)
- Type hierarchies or data models (→ class)
- Comparisons between two approaches or systems (→ structural subsystem)

**What NOT to diagram:**
- Simple lists — a bullet list is already visual enough
- Concepts already shown in an existing image or figure in the article
- Purely emotional or narrative passages with no underlying mechanism
- Content that is a single sentence or trivially simple
- Decorative filler — every diagram must earn its place with a concrete reader need

**Output**: A list of N candidate diagram positions, each with: section anchor, tentative type, named elements, and the "After seeing this diagram, the reader understands ___" sentence.

### Step 3: Confirm settings (multi-diagram mode)

**ONE AskUserQuestion, max 3 questions. Q1 required. Q2 required unless `--density` given.**

| Q | When to ask | Options |
|---|-------------|---------|
| **Q1: Diagram positions** | Always | Show the N candidate positions with tentative types. "I identified N positions for diagrams: [numbered list with section anchor + type + one-line purpose]. Adjust, add, or remove?" |
| **Q2: Density** | No `--density` flag | minimal (1-2 core concepts only), balanced (3-5 major concepts, Recommended), per-section (one per section/chapter), rich (6+ comprehensive) |
| **Q3: Language** | Article language ≠ user's language or `--lang` | Which language for diagram labels? |

After confirmation, finalize the list of diagrams to generate. If the user adjusts positions or types, update accordingly.

### Step 4: Generate outline (multi-diagram mode)

Save `outline.md` with YAML frontmatter and per-diagram entries:

```yaml
---
article: path/to/article.md    # or "pasted content"
slug: article-topic-slug
density: balanced
diagram_count: 4
language: en
---
```

Per-diagram entry format:

```markdown
## Diagram 1
**Position**: [section name / paragraph anchor, e.g. "Section 2, after 'Authentication is the first step...'"]
**Purpose**: [why this diagram helps the reader]
**Type**: [flowchart | sequence | structural | illustrative | class]
**Named elements**: [list of actors, components, states, or concepts]
**Reader need**: "After seeing this diagram, the reader understands ___"
**Slug**: [2-4 kebab-case words]
**Filename**: 01-{type}-{slug}/diagram.svg
```

**Requirements**:
- Each position justified by a concrete reader need (the "After seeing this..." sentence)
- Type chosen per the routing table, not arbitrarily
- Count matches the confirmed density
- If input was pasted content, also save it as `source-{slug}.md` in the output directory

Save to `diagram/{article-slug}/outline.md`.

### Step 5: Load shared references

**Always read**:
- `references/design-system.md` — philosophy, typography, color palette, hard rules
- `references/svg-template.md` — the `<style>` + `<defs>` boilerplate to copy verbatim
- `references/layout-math.md` — text-width estimation, viewBox sizing, arrow routing
- `references/pitfalls.md` — the pre-save checklist

Per-type reference files are loaded inside the generation loop (Step 6b) since each diagram may have a different type.

### Step 6: Per-diagram generation loop

For each diagram (single iteration in single mode, N iterations in multi mode):

#### 6a: Capture intent

**Single mode**: Read the user's prompt. Extract these five things from the source:

1. **Named elements** — list every distinct actor, component, service, state, or phase explicitly named. Count them. If the count is 6+, plan multiple diagrams rather than cramming everything into one (see `flowchart.md` → "Planning before you write SVG").

2. **Relationship type** — for each interaction between elements, classify it:
   - Sequential steps / order of operations → flowchart signal
   - Containment ("X is inside Y", zones, hierarchies) → structural signal
   - Multi-actor message exchange (A sends to B, B replies to C) → sequence signal
   - Mechanism ("how does X produce Y") → illustrative signal
   More than one type present? Pick the dominant one, or plan two diagrams.

3. **What the reader needs** — complete this sentence before routing: *"After seeing this diagram, the reader understands ___."* If you can't finish it, the topic is underspecified — ask.

4. **Label preview** — for each element name, count the characters. Latin titles >30 chars (CJK >16) will overflow a 180-wide box and need shortening. Draft the abbreviated form now, before layout math, so Step 6d uses real labels.

5. **Language** — CJK vs. Latin. Affects text-width multipliers in Step 6d (15 px/char vs. 8 px/char for titles). Mixed content (CJK labels with some Latin terms) counts as CJK.

**Multi mode**: Most of this was already done in Steps 2/4. Read the current diagram's outline entry. Refine the named elements and label preview now, for this specific diagram.

#### 6b: Route type and load type reference

**Single mode**: Match the user's phrasing to the routing table in "Diagram types". If `--type` is given, use it. Otherwise route on the verb. When genuinely ambiguous between flowchart and illustrative, default to **illustrative**. Tell the user which type you picked and why, in one sentence.

**Multi mode**: The type was already determined in the outline. Load the matching reference file now.

**Read the one that matches the type**:
- `references/flowchart.md`
- `references/sequence.md`
- `references/structural.md`
- `references/illustrative.md`
- `references/class.md`

**Read on demand** when the plan calls for a small pictorial element (status circle on a decision branch, checkbox inside a list, queue slot inside a box, doc/terminal/script icon inside a subject, annotation circle on a connector, paired pub/sub arrows, dashed future-state node) **or** when drawing a phase-band diagram (compact tool card icons, operator icons):
- `references/glyphs.md` — the shared glyph library, tool card icon set, operator icons, and dark-mode rules

**Read on demand for diagram type extensions:**
- `references/flowchart-poster.md` — when ≥3 poster-mode triggers fire in Step 6d (topic has a short name, named phases, parallel candidates, a loop termination mechanic, overflow annotations, or a footer quote)
- `references/flowchart-phase-bands.md` — when the prompt describes a multi-phase sequential operation where each phase contains parallel tools or steps and outcomes propagate between phases
- `references/structural-network.md` — when drawing network topology: zone containers, wired/wireless device connectivity, security zones
- `references/structural-matrix.md` — when drawing a comparison matrix: feature table, ✓/✗ cells, side-by-side grid

#### 6c: Check patterns library

If the topic matches a known AI-system pattern, there is a pre-cooked starter plan in `references/patterns/`. Scan `references/patterns/README.md` for a pattern name that matches. If one matches, load that pattern file and use its mermaid reference + baoyu SVG plan as the starting point for Step 6d.

If nothing matches, skip and plan from scratch in Step 6d. Do not force a near-miss.

#### 6d: Plan on paper

Before writing any SVG, draft a short layout plan. Do the math once, correctly, so the SVG comes out right on the first pass.

**6d-i. Extract structure from the source** — don't just transcribe bullets into boxes. Read the source looking for these elements. Not every element will be present, but every present element should land in the diagram:

- **Mechanism name** — does the topic have a short, nameable identity (Autoreason, AutoResearch, OAuth, JWT auth, Reflexion loop)? If yes, that's a candidate `.title`.
- **Framing question** — does the source contain a "why does this exist" sentence? That's a candidate subtitle.
- **Phases** — do the stages naturally cluster into 2–4 named groups? Each cluster is a candidate `.eyebrow` section.
- **Anchor inputs** — is there a constant input (the task prompt, a dataset, a knowledge base) that every stage references? That's a candidate anchor box above the main flow.
- **Parallel candidates** — at some point, does the process generate N alternatives that are then compared? **Watch for the implicit "keep unchanged" candidate.**
- **Loop scope + termination** — which boxes are inside a loop that repeats? What is the *specific* termination rule? That's a candidate left-rail loop bracket + a dedicated termination box.
- **Per-box context that won't fit in a subtitle** — those are candidate right-column `.anno` annotations.
- **Quotable hook** — does the source end with a test result, a quote, or a memorable framing? That's a candidate footer `.caption`.
- **Role categories** — how many *distinct kinds* of operation does the process have? This determines the color budget. Identity is a category, not a sequence.

Write the answers to these in the plan file. If ≥3 of them land, you're building a **poster flowchart** — load `references/flowchart-poster.md` and follow its coordinate budget. Otherwise, it's a simple flowchart and the linear-top-down pattern applies.

**6d-ii. Draft the layout:**

1. **List the nodes / regions / shapes** with their full label text (title + optional subtitle).
   - Simple flowchart: ≤5 nodes.
   - Poster flowchart: ≤12 nodes grouped into ≤4 eyebrow-divided phases.
   - Structural: ≤3 inner regions.
   - Illustrative: 1 subject.
   - Sequence: list actors (2–4, max 4) in left-to-right order, each with a short title (≤12 chars) and optional role subtitle; then list messages as ordered `(sender, receiver, short label)` tuples (6–10 total, 10 is the sweet spot); mark any self-messages; draft a side-note title for the protocol.
2. **For every rect, compute the width** using the formula in `layout-math.md`:
   - `width = max(title_chars × 8, subtitle_chars × 7) + 24` (Latin)
   - Replace 8 with 15 and 7 with 13 for CJK
   - Round up to the nearest 10
3. **Pick colors by category**, not sequence. ≤2 accent ramps per diagram. Gray for neutral/start/end. Reserve blue/green/amber/red for semantic meanings.
   - **Sequence exception**: assign one ramp per actor (default `[gray, teal, purple, blue]`), up to 4 ramps total — arrows inherit the sender's ramp.
   - **Poster-flowchart exception**: up to 4 ramps, one per distinct agent/role (drafter=purple, critic=coral, synthesizer=teal, judge=amber). Baseline/anchor/convergence stay gray.
4. **Check tier packing**: `N × box_width + (N-1) × gap ≤ 600`. For sequence, use the lane table in `layout-math.md` (N=4 → centers 100/260/420/580) and verify every message label fits its lane span with `label_chars × 7 ≤ |sender_x − receiver_x| − 8`. For poster fan-out rows (3 candidates), see the coordinate sketch in `flowchart.md`.
5. **Map arrows** and verify none cross an unrelated box. Use L-bends where a straight line would collide. (Sequence messages are always straight horizontal lines — no L-bends. Fan-out candidates converge to a common `ymid` channel just above the judge box.)
6. **Compute viewBox height**: `H = max_y + 20` where `max_y` is the bottom of the lowest element. Poster flowcharts routinely reach H=800–950 — don't force them to be compact.

Save this plan:
- **Single mode**: `diagram/{slug}/plan.md`
- **Multi mode**: `diagram/{article-slug}/NN-{type}-{slug}/plan.md`

#### 6e: Write the SVG

Emit a single `<svg width="100%" viewBox="0 0 680 H">` element. Copy the `<style>` + `<defs>` block from `svg-template.md` **verbatim** — don't abbreviate or edit the color ramp definitions. Then add visual elements in z-order:

1. Background decorations (rare)
2. Containers (outer `<rect>` for structural diagrams)
3. Connectors and arrows (drawn first so nodes paint on top)
4. Nodes (rects with text)
5. Labels outside boxes (leader callouts, legends, external I/O labels)

Typography rules:
- Two sizes only: 14px (`t`, `th`) and 12px (`ts`)
- Two weights only: 400 and 500
- Sentence case everywhere — "User login" not "User Login"
- Every `<text>` element gets a class (`t`, `ts`, or `th`) — never hardcode fill colors on text

#### 6f: Run the pre-save checklist

Walk through every item in `references/pitfalls.md`. The top failures to catch every time:

1. viewBox height covers every element with a 20px buffer
2. No rect extends past x=640
3. Every labeled rect is wide enough for its text (char-width check)
4. No arrow crosses an unrelated box
5. Every `<path>` connector has `fill="none"` (or uses `class="arr"`)
6. Every `<text>` has a class — no hardcoded `fill="black"`
7. No `text-anchor="end"` at low x values (label would clip past x=0)
8. ≤2 accent ramps, colors encode category not sequence
9. No `<!-- comments -->` in the final output

If any item fails, fix the SVG before saving. Don't rationalize past a failure — the checklist exists because these bugs are silent: the SVG is valid but looks wrong when rendered.

#### 6g: Save and report progress

Save the SVG and plan:
- **Single mode**: `diagram/{slug}/plan.md` + `diagram.svg`
- **Multi mode**: `diagram/{article-slug}/NN-{type}-{slug}/plan.md` + `diagram.svg`

**Backup rule**: if `diagram.svg` already exists at the target path, rename the existing one to `diagram-backup-YYYYMMDD-HHMMSS.svg` before writing the new file — never overwrite prior work silently.

**Multi mode progress**: after each diagram, report progress: "Generated 2/4: 02-illustrative-jwt-token-structure".

### Step 7: Finalize (multi-diagram mode)

If input was a file path, insert `![description](relative-path/NN-{type}-{slug}/diagram.svg)` at each identified position in the article. Compute the relative path based on the article location vs. the diagram output directory.

If input was pasted content, skip insertion — the diagrams are generated and the outline records positions, but there's no source file to modify.

### Step 8: Report

**Single mode** — tell the user in 4-6 lines:
- Diagram type picked (and one-sentence why)
- Node count / complexity
- viewBox dimensions
- Language
- Output file path
- One suggestion for how to preview it (e.g., "Open in Chrome for light/dark check")

**Multi mode**:

```
Article Diagram Generation Complete!

Article: [path or "pasted content"]
Density: [level] | Language: [lang]
Diagrams: X/N generated

Positions:
- 01-sequence-jwt-auth-flow → After "Authentication is the first step..."
- 02-illustrative-jwt-token-structure → After "The token structure..."
- 03-flowchart-token-refresh → After "When the token expires..."
- 04-structural-microservice-auth → After "In a microservices architecture..."

Output: diagram/{article-slug}/
Preview: Open any .svg in Chrome for light/dark check
```

## Output structure

### Single-diagram mode

```
diagram/{topic-slug}/
├── source-{slug}.md          # optional: user's input content if provided
├── plan.md                   # layout sketch from Step 6d
└── diagram.svg               # final output
```

### Multi-diagram mode

```
diagram/{article-slug}/
├── source-{slug}.md          # saved input content (file copy or pasted content)
├── outline.md                # frontmatter + all diagram entries from Step 4
├── 01-{type}-{slug}/
│   ├── plan.md               # layout sketch for this diagram
│   └── diagram.svg           # final SVG
├── 02-{type}-{slug}/
│   ├── plan.md
│   └── diagram.svg
└── 03-{type}-{slug}/
    ├── plan.md
    └── diagram.svg
```

- **Slug**: 2–4 kebab-case words derived from the topic or concept.
- **Backup rule**: if `diagram.svg` already exists at the target path, rename the existing one to `diagram-backup-YYYYMMDD-HHMMSS.svg` before writing the new file.
- **Plan**: always save `plan.md` beside the SVG so the next iteration can re-read it.
- **Source**: if the user pasted source content, save it as `source-{slug}.md` in the output directory.
- **Numbering**: NN prefix (01, 02, ...) matches the outline order, which matches article position order.
- **Outline**: in multi mode, always save `outline.md` from Step 4 so the generation can be resumed or individual diagrams can be regenerated.

## Modification

| Action | Steps |
|--------|-------|
| **Regenerate one diagram** (multi mode) | Re-read `outline.md` → find the entry → re-run Step 6 for that diagram only → update the SVG |
| **Add a diagram** (multi mode) | Identify position → add entry to `outline.md` → run Step 6 for the new entry → insert into article |
| **Remove a diagram** (multi mode) | Delete the `NN-{type}-{slug}/` directory → remove entry from `outline.md` → remove `![...]` from article |
| **Change type** (single or multi) | Update the outline entry or re-run with `--type` → regenerate |

## Core principles

- **Draw the mechanism, not a diagram about the mechanism** (illustrative). **Draw the sequence, not the architecture** (flowchart). **Draw the containment, not the flow** (structural). **Draw the conversation, not the steps** (sequence). Picking the wrong type is the single biggest failure mode — more harmful than any layout bug.
- **One design system, always.** No `--style` flag, no alternate themes, no per-topic visual variants. The cohesive look across every diagram is the product — if a reader sees two baoyu diagrams in different articles, they should feel they came from the same hand. Any request to "use a different style" is a request to break this principle; push back and ask what the underlying need is instead. In multi-diagram mode, all diagrams in a run share the same design system — no per-diagram style overrides.
- **Self-contained output.** Every SVG carries its own styles and dark-mode rules. The reader should never need to edit anything after pasting it into their article.
- **Math before markup.** SVG has no auto-layout. Every coordinate is hand-computed. A diagram that "almost fits" has a bug — fix the math, don't nudge pixels.
- **Color encodes meaning, not position.** Five steps in a flowchart are not five colors. All five are gray unless one specific step deserves emphasis — in which case it gets the accent color.
- **The reader has 3 seconds.** If the diagram needs prose explanation to parse, it's failing. Simplify until it can stand alone with only its labels.

## References

- `references/design-system.md` — palette, typography, hard rules
- `references/svg-template.md` — the `<style>` + `<defs>` boilerplate (copy verbatim)
- `references/layout-math.md` — coordinates, text widths, viewBox math, arrow routing
- `references/pitfalls.md` — the pre-save checklist
- `references/flowchart.md` — flowchart-specific rules and worked examples (includes state-machine sub-pattern)
- `references/flowchart-poster.md` — poster flowchart dialect (load on demand when ≥3 poster triggers fire)
- `references/flowchart-phase-bands.md` — phase-band flowchart (horizontal dashed phase containers, compact tool card rows, cross-band semantic arrows, operator icons, legend strip)
- `references/sequence.md` — sequence-diagram rules (actors, lifelines, messages, self-messages)
- `references/structural.md` — structural-specific rules and worked examples (subsystem, bus, radial star, rich interior, mixed arrows)
- `references/structural-network.md` — network topology sub-pattern (zone containers, wired/wireless, tiered layout)
- `references/structural-matrix.md` — comparison matrix sub-pattern (feature table, ✓/✗ cells, zebra rows)
- `references/illustrative.md` — illustrative-specific rules and worked examples
- `references/class.md` — UML class diagram rules (3-compartment rects, relationships, stereotypes)
- `references/glyphs.md` — shared glyph library (status circles, checkboxes, queue slots, icons, annotation circles) and concept-to-shape conventions
- `references/patterns/` — pre-planned starters for common AI-system topologies (RAG, agents, memory tiers, verifier loops, …)
