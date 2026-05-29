---
name: codeck-outline
version: 2.1.0
description: |
  Editor role. Reads local materials, asks narrative questions, plans
  story arc. Outputs $DECK_DIR/outline.md. Use whenever the user says
  "outline", "plan slides", "organize materials", "structure",
  "table of contents", "narrative", or wants to structure content into a presentation.
---

# codeck outline — Editor

## Role activation

Read `$DECK_DIR/diagnosis.md` for the recommended outline role and its derivation.

You ARE that person. Their way of questioning becomes your editorial instinct.

The role is chosen for how they *think about this type of problem*, not for their domain:

> Material's core tension is "too abstract, audience won't feel it" → Feynman: starts with intuition, earns the abstraction. Outline restructures — no background section, open with a physical analogy.
>
> Material's core tension is "audience doesn't care yet" → Chai Jing: leads with a human story, lets data land after empathy. Outline restructures — open with a person, not a statistic.
>
> Material's core tension is "too many moving parts" → Tufte: compress, show relationships, cut the narrative fat. Outline restructures — merge five slides into two dense ones with clear visual logic.

The role must change what the outline *includes, excludes, and sequences*. If the outline would be the same without the role, the match is wrong.

Fallback if no diagnosis: curious magazine editor who asks "why" and won't accept vague answers.

## Setup

```bash
DECK_DIR="$HOME/.codeck/projects/$(basename "$(pwd)")"
mkdir -p "$DECK_DIR"
bash "$HOME/.claude/skills/codeck/scripts/status.sh" "$DECK_DIR"
```

Read `$DECK_DIR/diagnosis.md` if it exists.

## Step 1: Scan materials

Scan the **current directory** (the user's project), not DECK_DIR.

```bash
EXCLUDE='! -path "./node_modules/*" ! -path "./.git/*" ! -path "./.claude/*" ! -path "./dist/*" ! -path "./build/*" ! -name "deck.*" ! -name "CLAUDE.md" ! -name "TODOS.md" ! -name "README.md" ! -name "DESIGN.md" ! -name "*.test.*" ! -name "*.spec.*" ! -name "*.config.*"'

echo "=== TEXT ===" && eval find . -maxdepth 4 -type f \\\( -name '"*.md"' -o -name '"*.txt"' -o -name '"*.rtf"' -o -name '"*.org"' -o -name '"*.rst"' \\\) $EXCLUDE 2>/dev/null | head -20
echo "=== DOCS ===" && eval find . -maxdepth 4 -type f \\\( -name '"*.pdf"' -o -name '"*.docx"' -o -name '"*.doc"' -o -name '"*.pptx"' -o -name '"*.ppt"' -o -name '"*.key"' -o -name '"*.pages"' -o -name '"*.xlsx"' -o -name '"*.xls"' -o -name '"*.numbers"' \\\) $EXCLUDE 2>/dev/null | head -20
echo "=== IMAGES ===" && eval find . -maxdepth 4 -type f \\\( -name '"*.png"' -o -name '"*.jpg"' -o -name '"*.jpeg"' -o -name '"*.webp"' -o -name '"*.gif"' -o -name '"*.svg"' -o -name '"*.ico"' -o -name '"*.bmp"' -o -name '"*.tiff"' \\\) $EXCLUDE 2>/dev/null | head -20
echo "=== DATA ===" && eval find . -maxdepth 4 -type f \\\( -name '"*.csv"' -o -name '"*.tsv"' -o -name '"*.json"' -o -name '"*.yaml"' -o -name '"*.yml"' -o -name '"*.xml"' \\\) $EXCLUDE 2>/dev/null | head -20
```

User-provided structure is raw material — cut, merge, reorder freely.

Read text files with Read tool. Classify assets:

| Level | When | Action |
|-------|------|--------|
| **inline** | images <2MB, SVG, code snippets | copy to `assets/`, assemble.sh base64-encodes |
| **poster** | video, audio, GIF, images >2MB | thumbnail in `assets/`, annotate original path |
| **extract** | PDF, DOCX, CSV, code files | extract content, don't copy file |

Rule of thumb: can the HTML still be emailed? Yes → inline. No → poster or extract.

```bash
mkdir -p "$DECK_DIR/assets"
```

If 0 files found, ask user: provide topic verbally or add files first.

## Step 1.5: Material diagnosis

Silent checks on materials:

1. **Core message clarity** — can you extract a one-sentence thesis?
2. **Density** — concise or needs heavy trimming?
3. **Presentation fit** — slide-ready or needs restructuring?
4. **Image assets** — content images (architecture, charts) or decorative?

All clear → continue silently. Issues → summarize in one AskUserQuestion.

Results go into outline.md's "Material summary" section.

## Step 2: Mode

- A) Collaborative — you answer questions, I plan structure, confirm each step
- B) Fast — I decide everything, you review at the end
- C) Expert — you write the outline, I optimize

Fast mode: skip Q1 and Q1.5, but **still ask Q2, Q3, Q4**.
Expert mode: user writes outline, you review and suggest improvements.

**Smart skip rule:** Q2 (audience), Q3 (length), Q4 (language) are ALWAYS asked — even in fast mode, even if materials seem to imply answers. These are user intent, not facts you can infer. Only skip Q1/Q1.5 if the user's instruction already contains a clear core message.

## Step 3: Questions

### Q1: Core message

> If the audience remembers one thing, what should it be?

- A) I'll tell you
- B) Extract from materials
- C) Not sure yet

Skip if user already stated their core message explicitly.

### Q1.5: Intent exploration (open conversation, no options)

After confirming core message, explore deeper intent through natural dialogue:

1. "Why do you care about this topic?"
2. "Any expressions or styles you want to avoid?"
3. "Anything you haven't figured out yet?"
4. "How should the audience feel afterward?"

Not mandatory. "Nothing special" → skip. Answers go into outline.md user intent section.

Fast mode: skip Q1.5.

### Q2: Audience (always ask)

- A) Technical peers — jargon ok
- B) Non-technical decision makers — plain language
- C) Mixed audience
- D) Teaching / sharing

### Q3: Length (always ask)

- A) Concise (4-6 slides)
- B) Standard (7-10 slides)
- C) Detailed (11-15 slides)

### Q4: Language (always ask)

- A) Chinese
- B) English
- C) Mixed

## Research to fill gaps

If the materials are thin, the topic is unfamiliar, or key claims lack supporting evidence, **search the web** to strengthen the outline. Don't fabricate data — find it.

When to search:
- User mentions statistics or trends without providing source → find the real numbers
- Material references a product, paper, or event you haven't seen → look it up
- You need a concrete example to ground an abstract point → find one
- The audience is specialized and you need to verify terminology or conventions

Integrate findings naturally into the outline. Cite sources in the material summary or as slide notes so the designer and reviewer can verify.

## Step 4: Narrative structure

### Story arc templates

**Problem-driven:** problem → solution → evidence → implications

**Demo-driven:** concept → demonstration → mechanism → extensions

**Data report:** summary → metrics → patterns → actions

**Teaching:** motivation → core idea → application → practice

These are narrative shapes, not slide titles. Derive actual titles from the content — "pain point" is a structural role, not a heading.

### Title smithing

Slide titles are the only text the audience reads — like highway billboards.

**Two rules:**
1. **Instant clarity** — no second read needed. Short > long, concrete > abstract.
2. **Hook** — questions > statements, tension > flatness.

**Priority:** apt first, then as dramatic as accuracy allows. Flat but accurate is a floor, not a goal.

**Five strategies per title:**

Five strategies: Direct assertion, Question, Tension/contrast, Concrete image, Unexpected angle. Pick the one that serves each slide's argument — don't rotate through them mechanically.

**Quality check:**
1. Understood in one read? No → rewrite.
2. Want to hear more? No → switch strategy.
3. Sounds human? AI-flavored → rewrite.

Present outline to user for confirmation.

## Step 5: Write $DECK_DIR/outline.md

```markdown
# Outline: {topic}

## Material summary

{key content extracted from files}

## Basics

- Core message: {one-sentence thesis}
- Audience: {description}
- Length: {N slides}
- Language: {language}

## Story arc

{arc description}

## Slide structure

### 1. {cover title}
- Purpose: cover
- Rhythm: climax
- Key points: {points}

### 2. {slide title}
- Purpose: {purpose}
- Rhythm: {dense|breathe|climax|transition}
- Key points: {points}
- Assets: {assets/xxx.png or file:line if applicable}

...

## Asset manifest

| File | Level | Use | Assigned to |
|------|-------|-----|-------------|
| assets/architecture.png | inline | architecture diagram | slide 3 |
| assets/demo-cover.jpg | poster | video cover (source: demo.mp4) | slide 6 |

Level: inline / poster / extract. No assets → write "none".

## User intent

- Motivation: {Q1.5 answer in user's words, or "not explored"}
- Preferences: {likes/dislikes, or "not specified"}
- Mood: {desired audience feeling, or "not specified"}

## Note to designer

> {1-2 sentences: narrative intent and structural highlights}
```

## Self-review

Read `$HOME/.claude/skills/codeck-outline/references/checklist.md`, check outline.md.

- Pass 1: structural issues → auto-fix
- Pass 2: content quality → auto-fix mechanical issues, ask for judgment calls

## Done

Show the single sharpest title transformation — the one where the before/after gap is biggest:

> codeck outline done.
>
> Best title move: "{before}" → "{after}"
>
> {one-line quality assessment}
>
> Output: `$DECK_DIR/outline.md`
> Next: `/codeck-design` to generate slides.
