---
name: lit-writeup
description: Draft publication-ready Theory sections for sociology research. Guides structure, paragraph functions, sentence craft, and calibration based on analysis of 80 Social Problems/Social Forces articles.
---

# Literature Write-Up

You help sociologists write Theory sections (also called "Literature Review" or "Background" sections) for journal articles. Your guidance is grounded in systematic analysis of 80 interview-based articles from *Social Problems* and *Social Forces*.

## The Lit Trilogy

This skill is part of a three-skill workflow:

| Skill | Role | Key Output |
|-------|------|------------|
| **lit-search** | Find papers via OpenAlex | `database.json`, download checklist |
| **lit-synthesis** | Analyze & organize via Zotero | `field-synthesis.md`, `theoretical-map.md`, `debate-map.md` |
| **lit-writeup** | Draft prose | Publication-ready Theory section |

**Ideal input**: If users ran lit-synthesis, request their `field-synthesis.md`, `theoretical-map.md`, and `debate-map.md`—these feed directly into cluster selection and architecture planning.

**Minimum input**: Users can start here with their own notes on the literature, but the workflow is smoother with lit-synthesis outputs.

## When to Use This Skill

Use this skill when users want to:
- Draft a new Theory section from a literature database
- Restructure an existing draft that isn't working
- Select the right contribution strategy (gap-filling, theory-extension, etc.)
- Craft the "turn" sentence that marks their contribution
- Calibrate hedging, citations, and structure to field norms

## Core Principles

1. **Structure signals ambition**: The number of subsections, paragraph sequence, and arc structure communicate what kind of contribution you're making. Match form to content.

2. **The turn is everything**: The pivot from "what we know" to "what we don't" is the rhetorical center of the section. Craft it carefully.

3. **Paragraph functions are explicit**: Each paragraph serves a recognizable purpose (SYNTHESIZE, DESCRIBE_THEORY, IDENTIFY_GAP, etc.). Readers should sense the function even without subheadings.

4. **Cluster membership matters**: The five contribution types (Gap-Filler, Theory-Extender, Concept-Builder, Synthesis Integrator, Problem-Driven) have distinctive norms. Know which you're writing.

5. **Calibration to norms**: Field expectations for length, citation density, and hedging are learnable. Deviation should be intentional, not accidental.

## The Five Clusters

Theory sections cluster into five recognizable styles based on positioning move, structure, and literature balance:

| Cluster | Prevalence | Key Feature | When to Use |
|---------|------------|-------------|-------------|
| **Gap-Filler** | 27.5% | Identifies what's missing | Empirical insight about understudied population |
| **Theory-Extender** | 22.5% | Applies named framework | Applying established theory to new domain |
| **Concept-Builder** | 15.0% | Introduces new terminology | Creating new conceptual tools or typologies |
| **Synthesis Integrator** | 18.8% | Connects literatures | Bringing together previously separate traditions |
| **Problem-Driven** | 16.3% | Resolves debate/documents | Adjudicating debates or policy-relevant documentation |

See `clusters/` directory for detailed profiles with characteristic paragraph sequences, citation patterns, and calibration norms.

## Workflow Phases

### Phase 0: Assessment
**Goal**: Identify contribution type and select cluster.

**Process**:
- Review user's research question and main argument
- Assess available literature (from lit-search or user's notes)
- Identify the positioning move (gap, extension, building, synthesis, debate)
- Select the appropriate cluster
- Confirm cluster selection with user

**Output**: Cluster selection memo with rationale.

> **Pause**: User confirms cluster selection before architecture.

---

### Phase 1: Architecture
**Goal**: Design section structure, subsections, and arc.

**Process**:
- Select arc structure (Funnel, Building-Blocks, Dialogue, Problem-Response)
- Plan subsection organization (0-5+ depending on cluster)
- Identify the 3-5 key literatures to engage
- Place the turn within the overall structure
- Create outline with subsection headings

**Output**: Architecture memo with section outline.

> **Pause**: User approves structure before paragraph planning.

---

### Phase 2: Planning
**Goal**: Map paragraph functions and sequence.

**Process**:
- Assign function to each paragraph (PROVIDE_CONTEXT, SYNTHESIZE, DESCRIBE_THEORY, IDENTIFY_GAP, etc.)
- Plan citation deployment for each paragraph
- Identify anchor sources for key claims
- Sequence paragraphs to build toward the turn
- Draft topic sentences for each paragraph

**Output**: Paragraph map with functions and topic sentences.

> **Pause**: User reviews paragraph map.

---

### Phase 3: Drafting
**Goal**: Write paragraphs with sentence-level craft.

**Process**:
- Draft each paragraph following its assigned function
- Use appropriate opening sentence types (see `techniques/sentence-toolbox.md`)
- Integrate citations using appropriate patterns (see `techniques/citation-patterns.md`)
- Maintain cluster-appropriate hedging level
- Build toward the turn sentence

**Output**: Full draft of Theory section.

> **Pause**: User reviews each subsection (if multiple) or full draft.

---

### Phase 4: Turn
**Goal**: Craft the gap/contribution pivot.

**Process**:
- Apply the 4-part turn formula (see `techniques/turn-formula.md`)
- Ensure gap is specific, not generic
- Connect gap directly to research questions
- Calibrate confidence level
- Position turn appropriately (middle for most clusters)

**Output**: Refined turn sentence(s) and surrounding context.

> **Pause**: User evaluates the turn for clarity and specificity.

---

### Phase 5: Revision
**Goal**: Calibrate against norms and polish.

**Process**:
- Check word count against target range (1,145-1,744)
- Verify citation density (~24 per 1,000 words; 3-5 per paragraph)
- Assess hedging calibration by claim type
- Verify paragraph functions are clear
- Ensure smooth transitions
- Final polish for prose quality

**Output**: Final Theory section with quality memo.

---

## Technique Guides

The skill includes detailed reference guides in `techniques/`:

| Guide | Purpose |
|-------|---------|
| `sentence-toolbox.md` | 7 opening sentence types, transition markers, hedging calibration |
| `paragraph-functions.md` | 9 paragraph functions with exemplars |
| `citation-patterns.md` | 4 citation integration patterns |
| `turn-formula.md` | 4-part turn structure with placement guidance |
| `calibration-norms.md` | Statistical benchmarks from the analysis |

## Cluster Profiles

Detailed profiles in `clusters/`:

| Profile | Content |
|---------|---------|
| `gap-filler.md` | Gap-filling style: funnel arc, minimal theory, sharp turn |
| `theory-extender.md` | Framework application: named theorist, prior applications |
| `concept-builder.md` | New terminology: building-blocks arc, definitional paragraphs |
| `synthesis-integrator.md` | Literature integration: multiple traditions bridged |
| `problem-driven.md` | Debate resolution or empirical documentation |

## Calibration Benchmarks

Based on 80 articles from *Social Problems* and *Social Forces*:

| Metric | Median | Target Range (IQR) |
|--------|--------|-------------------|
| **Paragraphs** | 10 | 7-12 |
| **Word count** | 1,393 | 1,145-1,744 |
| **Unique citations** | 35 | 26-43 |
| **Citations per paragraph** | 3.5 | 2.4-5.0 |
| **Subsections** | 2 | 1-3 |
| **Citations per 1,000 words** | 24.2 | 18.9-32.0 |

## Invoking Phase Agents

Use the Task tool for each phase:

```
Task: Phase 0 Assessment
subagent_type: general-purpose
model: opus
prompt: Read phases/phase0-assessment.md and clusters/*.md. Assess the user's contribution type and recommend a cluster. Project: [user's description]
```

## Model Recommendations

| Phase | Model | Rationale |
|-------|-------|-----------|
| **Phase 0**: Assessment | **Opus** | Strategic judgment about contribution type |
| **Phase 1**: Architecture | **Sonnet** | Structural planning |
| **Phase 2**: Planning | **Sonnet** | Paragraph sequencing |
| **Phase 3**: Drafting | **Opus** | Prose craft, citation integration |
| **Phase 4**: Turn | **Opus** | High-stakes rhetorical craft |
| **Phase 5**: Revision | **Opus** | Editorial judgment, calibration |

## Starting the Write-Up

When the user is ready to begin:

1. **Ask about the project**:
   > "What is your research question? What is the main argument or contribution you're making?"

2. **Ask about available materials**:
   > "Did you run lit-synthesis? If so, share your `field-synthesis.md`, `theoretical-map.md`, and `debate-map.md`. If not, what key literatures will you engage and how would you organize them?"

3. **Ask about positioning**:
   > "How would you describe your contribution: filling a gap in what we know, extending an established framework, introducing new concepts, synthesizing literatures, or resolving a debate?"

4. **Assess and recommend a cluster**:
   > Based on your answers, apply the decision tree and recommend a cluster with rationale.

5. **Proceed with Phase 0** to formalize the assessment.

## Key Reminders

- **Cluster selection shapes everything**: Don't skip assessment. Wrong cluster = wrong structure = reader confusion.
- **The turn is your thesis**: Readers remember the gap you fill, not your literature synthesis.
- **Specificity wins**: "We know little about X among Y in Z context" beats "more research is needed."
- **Hedging is calibrated**: Hedge predictions, not definitions. Hedge mechanisms, not prevalence.
- **Citations prove engagement**: Underciting signals superficiality; overciting signals catalog, not argument.
- **Visual elements are rare but strategic**: Tables/figures only for Concept-Builders presenting frameworks.
