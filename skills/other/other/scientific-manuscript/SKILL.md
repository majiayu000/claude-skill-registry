---
name: scientific-manuscript
description: |
  High-impact scientific manuscript development for top-tier journals such as Nature, Science,
  and Cell. Use when the user mentions: high-impact paper, top-tier journal, Nature, Science,
  Cell, Current Biology, eLife, or similar prestigious venues. Provides feedback on narrative
  structure, prose style, paragraph flow, sentence-level craft, and rhetorical impact.

  NOT for: routine papers, lower-tier journals, review articles, or grant writing (separate
  skills may handle those). This skill is specifically for crafting papers aimed at the most
  competitive journals where narrative arc, concise prose, and strategic rhetoric matter most.
---

# Scientific Manuscript Skill

Craft and refine manuscripts for high-impact journals through structured feedback, comparative analysis with exemplar papers, and sentence-level prose craft.

## Core Focus Areas

This skill emphasizes four dimensions of high-impact writing:

1. **Narrative arc** — how the story builds across sections and paragraphs
2. **Paragraph architecture** — how individual paragraphs create momentum and impact
3. **Sentence-level craft** — concise, punchy prose with word economy
4. **Strategic rhetoric** — calculated use of adjectives and flourishes

## Reference Files

### Section-Specific Guides
| Section | Reference File |
|---------|---------------|
| Abstract | `references/abstract.md` |
| Introduction | `references/introduction.md` |
| Results | `references/results.md` |
| Discussion | `references/discussion.md` |
| Methods | `references/methods.md` |
| Figures | `references/figures.md` |

### Craft-Level Guides (Load for any section)
| Focus | Reference File | When to Load |
|-------|---------------|--------------|
| Narrative structure | `references/narrative-structure.md` | Story arc, section flow, momentum |
| Prose craft | `references/prose-craft.md` | Sentence-level style, word economy, rhetoric |
| Evaluation | `references/rubrics.md` | Systematic scoring |

### Annotated Examples
| Paper | File | Best for |
|-------|------|----------|
| Musser 2021 Science | `references/examples/musser_2021_science.md` | Paradox hooks, cell type papers |
| Ruperti 2024 Curr Biol | `references/examples/ruperti_2024_curbio.md` | Challenging paradigms, quantitative prose |
| Tarashansky 2021 eLife | `references/examples/tarashansky_2021_elife.md` | Methods papers, comparative analysis |
| Vergara 2021 Cell | `references/examples/vergara_2021_cell.md` | Resource papers, multimodal data |

## Feedback Modes

### Mode 1: Narrative Analysis
Analyze story arc and momentum. Use when:
- Draft feels flat or disjointed
- User asks about "flow" or "structure"
- Sections don't build toward a conclusion

Load: `references/narrative-structure.md`

Format:
```
**Arc diagnosis**: [Where tension is established, where it resolves, what's missing]
**Momentum check**: [Which paragraphs build vs. stall]
**Pivot analysis**: [How you transition from known → unknown → your contribution]
**Suggested restructuring**: [Concrete reordering or additions]
```

### Mode 2: Prose Craft Review
Sentence-level style analysis. Use when:
- User asks about "style" or "writing quality"
- Prose feels bloated or academic
- User wants text to be "punchier" or "more concise"

Load: `references/prose-craft.md`

Format:
```
**Bloat patterns**: [Specific phrases to cut with rewrites]
**Verb weakness**: [Weak verbs → strong verb suggestions]
**Sentence rhythm**: [Where variation is needed]
**Adjective audit**: [Which add meaning vs. clutter]
**Power positions**: [Sentences where key info is buried]
```

### Mode 3: Comparative Critique
Compare to exemplar papers. Use when:
- User wants to see "how good papers do it"
- Draft has rhetorical issues best shown by contrast

Load: Relevant example file from `references/examples/`

Format:
```
**Your draft**: [quote passage]
**Exemplar**: [quote from example paper]
**Key difference**: [What the exemplar does that yours doesn't]
**Principle**: [The generalizable technique]
**Suggested revision**: [Concrete rewrite applying the principle]
```

### Mode 4: Rubric Evaluation
Systematic scoring. Use when:
- User asks "Is this ready for submission?"
- Comprehensive assessment needed

Load: `references/rubrics.md`

### Mode 5: Iterative Dialogue
Socratic questioning. Use when:
- Logic or argument needs development
- User refining specific claims

## Quick Diagnostics

### The Arc Check
For any section, ask:
1. Where is the tension established?
2. Where does it resolve?
3. Does each paragraph advance toward resolution?

### The First/Last Test
- **First sentence of each paragraph**: Does it state the main point?
- **Last sentence of the paper**: Is it memorable and quotable?
- **Last sentence of each section**: Does it transition or conclude powerfully?

### The Economy Test
Flag these bloat patterns:
- "It is important to note that" → [delete]
- "plays a role in" → "regulates" / "drives"
- "is involved in" → [specific verb]
- "in order to" → "to"
- Stacked adjectives → choose one

### The Flourish Audit
Flourishes should appear at:
- Paper opening (hook)
- Key conceptual pivot
- Paper closing (take-home)

NOT in: routine findings, methods, figure descriptions

## Handling Requests

**"Review my introduction"**
→ Load `introduction.md` + `narrative-structure.md`, analyze arc and pivot, check prose craft

**"Make this punchier"**
→ Load `prose-craft.md`, do sentence-level audit, provide rewrites

**"How does this compare to good examples?"**
→ Load relevant example file, do comparative critique

**"Is the narrative working?"**
→ Load `narrative-structure.md`, analyze tension-resolution arc, check paragraph momentum

**"Help me cut this down"**
→ Load `prose-craft.md`, identify bloat patterns, suggest cuts with preserved meaning

**"Is this ready for submission?"**
→ Load `rubrics.md` + all relevant references, comprehensive evaluation

## Output Principles

1. **Quote exactly**: Reference specific passages from the draft
2. **Rewrite concretely**: Don't just diagnose—show the fix
3. **Be honest**: User wants critical feedback, not encouragement
4. **Prioritize**: Identify 2-3 highest-impact changes
5. **Model excellence**: Pull from exemplar papers to show what good looks like
