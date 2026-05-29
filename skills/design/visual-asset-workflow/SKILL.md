---
name: visual-asset-workflow
description: This skill should be used when creating visual assets for educational content. It provides professional creative brief methodology to activate reasoning mode for distinctive, pedagogically effective visuals.
version: "1.0.0"
---

# Visual Asset Workflow Skill

## Context & Problem

Educational visual generation converges toward generic infographics with technical specifications ("44pt Roboto Bold, 250px box") that activate prediction mode instead of reasoning mode. This produces bland, PowerPoint-default aesthetics instead of distinctive, pedagogically effective visuals.

This skill provides professional creative brief methodology to activate Gemini 3's reasoning capabilities.

---

## Core Principles

1. **Story activates reasoning** - Narrative intent produces distinctive visuals; technical specs produce generic ones
2. **Proficiency dictates complexity** - A2 students need <5 sec grasp; C2 professionals handle dense information
3. **Prerequisites gate content** - Visuals cannot assume knowledge students don't have yet
4. **Pedagogy drives hierarchy** - Visual weight teaches importance, not arbitrary aesthetics

---

## Dimensional Guidance

### Planning Before Execution

**Avoid:** Jumping into visual analysis without context
**Prefer:** Strategic planning phase (Q0)

Read FIRST:
- `robolearn-interface/docs/chapter-index.md` → Extract part, proficiency (A2/B1/C2), prerequisites
- `robolearn-interface/docs/[part]/[chapter]/README.md` → Understand lesson structure

Detect conflicts BEFORE work:
- Proficiency-complexity mismatch (complex visual for A2 beginners)
- Prerequisite violations (Python code when students haven't learned it)
- Pedagogical layer incoherence (Layer 1 content using Layer 4 approaches)

Output strategic plan, WAIT for approval before proceeding.

**Principle:** Plan prevents wasted work (Chapter 9 failure: 5 wrong lessons from skipping planning)

---

### Prompt Structure: Professional Creative Briefs

**Avoid:** Technical specifications
```
❌ "Title: 44pt Roboto Bold at (50, 20)"
❌ "Box: 250px × 90px, #aaaaaa, 8px corners"
❌ "Shadow: 4px offset, 8px blur"
```

**Prefer:** Story + Intent + Metaphor
```
✅ The Story: [1-2 sentence narrative of what's visualized]
✅ Emotional Intent: Should feel [exponential growth, surprising magnitude]
✅ Visual Metaphor: [Multiplication cascade - like compound interest]
✅ Key Insight: [ONE thing students must grasp]
✅ Color Semantics: Blue (#2563eb) = Authority (teaches governance concept)
✅ Typography Hierarchy: Largest = Key insight (not arbitrary sizing)
✅ Pedagogical Reasoning: Why these choices serve teaching
```

**Principle:** Creative briefs activate reasoning mode; specifications activate prediction mode

**Why it matters:** Gemini 3 reasons about HOW to achieve intent → Distinctive visuals instead of generic

---

### Token Conservation Strategy

**When:** Batch mode with >8 visuals OR continuation session

**Apply condensation while preserving reasoning activation:**

**ALWAYS KEEP:**
- Story (1-2 sentence narrative)
- Emotional Intent (what it should FEEL like)
- Visual Metaphor (universal concept)
- Key Insight (ONE thing students must grasp)
- Color semantics with hex codes (#2563eb)
- Pedagogical reasoning (why these choices)

**CONDENSE:**
- Long examples → Short labels
- Verbose descriptions → Bullet points
- Repeated patterns → Compact notation

**NEVER REMOVE:**
- Narrative elements
- Intent statements
- Reasoning explanations

**Example:**
```
FULL: "Top Layer shows the Coordinator at center top with label..."
CONDENSED: "Top Layer - Coordinator: Center top: 'Orchestrator'..."
```

**Target:** 60-70% token reduction, 100% reasoning activation preserved

**Principle:** Efficiency through compression, not through elimination of reasoning triggers

---

### Proficiency-Complexity Alignment

**Avoid:** One-size-fits-all complexity

**Prefer:** Proficiency-gated constraints

**A2 Beginner** (Non-negotiable limits):
- Max 5-7 elements
- <5 second grasp
- Static only (no interactive)
- Max 2×2 grids
- Clear hierarchy (largest = most important)

**B1 Intermediate**:
- Max 7-10 elements
- <10 second grasp
- Interactive Tier 1 OK (tap-to-reveal)
- Max 3×3 grids

**C2 Professional**:
- No artificial limits
- Dense infographics OK
- Full interactive architecture
- Production complexity

**Principle:** Overwhelming A2 students = learning failure; artificial simplicity for C2 = patronizing

---

### Prerequisite Validation Gate

**Avoid:** Assuming knowledge students don't have

**Prefer:** Validate against chapter prerequisites

**Detection:**
- Check Part number: Part 1-2 = no programming, Part 3 = markdown/prompts, Part 4+ = Python
- Check prerequisite list from chapter-index.md

**Example Violations:**
- ❌ Python code in Chapter 9 (Part 3 - students haven't learned it)
- ❌ Git commands in Part 2 (students haven't learned CLI)

**Exception:** Meta-level teaching OK
- ✅ Teaching "markdown code block syntax" by showing Python code block (teaches markdown, not Python)

**Principle:** Visual cannot require unknown knowledge

---

### Constitutional Alignment

**Avoid:** Decorative visuals without pedagogical purpose

**Prefer:** Every visual serves specific learning objective

**Principle 3 (Factual Accuracy):**
- Verify all statistics, dates, technical specs
- Enable Google Search grounding for factual claims
- Cite sources for data

**Principle 7 (Minimal Content):**
- Reject "let's add a visual for variety"
- Every element must teach something
- Remove non-teaching decoration

**Principle:** Visual decisions align with project constitution

---

### Pedagogical Layer Coherence

**Avoid:** Layer mismatch

**Prefer:** Visual approach matches chapter's pedagogical layer

**L1 (Manual Foundation):**
- Step-by-step diagrams
- Concrete examples
- Clear labeling (building vocabulary)

**L2 (AI Collaboration):**
- Before/after comparisons
- Iteration flows
- Three Roles Framework INVISIBLE (no role labels)

**L3 (Intelligence Design):**
- Architecture diagrams
- Reusable pattern illustrations

**L4 (Spec-Driven):**
- Specification → implementation flow
- Component composition diagrams

**Principle:** Visual design reinforces pedagogical approach

---

### Duplicate Prevention Protocol

**Avoid:** Generating different prompts that produce the same visual

**Prevent BEFORE generation:**

1. **Review existing visuals in chapter:**
   - List all `*.png` files in target chapter directory
   - Read corresponding `*.prompt.md` files
   - Identify visual patterns already used

2. **Validate prompt distinctiveness:**
   - Does this prompt's intent differ clearly from existing prompts?
   - Example conflicts to detect:
     - ❌ Timeline + Graph → Both might render as timeline
     - ❌ Architecture + Workflow → Both might render as hierarchy
     - ❌ Same metaphor, different names → Same visual result

3. **Differentiation strategy:**
   - Make visual type explicit in story ("GRAPH showing exponential growth" not just "showing growth")
   - Use distinct metaphors (cascade vs tree vs timeline vs curve)
   - Specify unique structural elements (2D axes vs linear flow vs hierarchical pyramid)

**Detect AFTER generation (in image-generator):**
- Visual comparison with existing chapter images
- Prompt alignment check (does output match brief intent?)

**Principle:** Prevention cheaper than rework

---

## Anti-Patterns

**Never:**
- Generate visuals without reading chapter-index.md first (skipping context)
- Use pixel specifications, font sizes, coordinates in prompts (kills reasoning)
- Assume knowledge not in prerequisites (prerequisite violation)
- Create decorative visuals without learning objective (Principle 7 violation)
- Apply same complexity to A2 and C2 students (proficiency mismatch)
- Create prompts without checking for duplicate visual patterns (causes rework)

**Even if it seems reasonable:**
- Don't use Python examples in Part 3 (students don't know Python yet)
- Don't create complex multi-step visuals for A2 (cognitive overload)
- Don't specify "44pt Roboto Bold" (removes Gemini's judgment)
- Don't skip distinctiveness validation "because they have different filenames" (names differ, visuals might not)

---

## Creative Variance

You tend to default to comparison diagrams even with story-driven prompts. Vary visual types:

- **Timeline progressions** (evolution over time)
- **Multiplication cascades** (compound growth visualization)
- **Hierarchical authority flows** (governance models)
- **Transformation sequences** (before → after → impact)
- **Conceptual metaphors** (abstract → concrete mapping)

Match visual type to story, not habit.

---

## Post-Generation Reflection

After batch completion, analyze systematically (Q8):

**Success patterns:**
- Quality gate performance (which caught most issues?)
- Average iterations (efficiency indicator)
- Time vs estimate (planning accuracy)

**Failure analysis:**
- Deferred visuals root causes (layout? spelling? concept mismatch?)
- Guardrail gaps (what principle would have prevented this?)
- Planning effectiveness (conflicts caught early vs missed?)

**Continuous improvement:**
- Pattern-based updates (not one-off fixes)
- New guardrails from learnings
- Prompt template refinements

Document in: `history/visual-assets/reflections/chapter-{NN}-reflection.md`

**Principle:** Systematic reflection → Improved future performance

---

## Success Indicators

You'll know this skill is working when:

- ✅ Zero pixel specifications in prompts (creative briefs only)
- ✅ Strategic plan created before visual analysis (Q0 complete)
- ✅ Proficiency conflicts detected early (A2 limits enforced)
- ✅ Prerequisite violations prevented (no unknown concepts)
- ✅ Story/Intent/Metaphor in every prompt (reasoning activated)
- ✅ Token conservation applied in batch mode (60-70% reduction)
- ✅ Duplicate prevention validation passed (zero duplicate visuals)
- ✅ Visuals feel distinctive and compelling (not generic PowerPoint)
- ✅ Reflection document created after batch (systematic learning)

**Result:** Professional-quality visuals that teach effectively, generated efficiently through planning, with zero duplicates requiring rework.
