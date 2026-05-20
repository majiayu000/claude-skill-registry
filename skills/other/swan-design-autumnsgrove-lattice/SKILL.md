---
name: swan-design
description: Craft elegant technical specifications with ASCII artistry, flow diagrams, and the Grove voice. The swan glides with purpose—vision first, then form, then perfection. Use when creating specs, reviewing documents, or transforming technical plans into storybook entries.
---

# Swan Design 🦢

The swan doesn't rush. It glides across still water with purpose and grace. Each movement is deliberate. Every feather is in place. When the swan creates, it weaves technical precision with poetic vision — specs that feel like opening a beautifully illustrated field guide to the forest.

## When to Activate

- User asks to "write a spec" or "create a specification"
- User says "document this feature" or "design this system"
- User calls `/swan-design` or mentions swan/designing specs
- Creating technical specifications for Grove systems
- Adding ASCII art and diagrams to text-heavy documents
- Validating existing specs against Grove standards
- Transforming technical plans into storybook entries

**Pair with:** `owl-archive` for Grove voice and text refinement

---

## The Design

```
VISION → SKETCH → REFINE → POLISH → LAUNCH
   ↓        ↲        ↓         ↲         ↓
See      Create   Write    Perfect   Release
Clearly  Form     Content  Voice     Spec
```

### Phase 1: VISION

*The swan sees the whole lake before moving a single feather...*

Before touching code blocks or ASCII characters, understand what you're creating.

- What problem does this system solve? What would you tell a Wanderer about it?
- Choose the nature metaphor — Heartwood (auth), Wisp (help), Patina (backups), etc.
- Define scope: what's in/out of bounds for this spec?
- Identify the audience: developers implementing, or Wanderers exploring?

**Output:** Nature metaphor chosen, scope defined, target audience identified

---

### Phase 2: SKETCH

*The swan traces patterns on the water, creating the form...*

Build the spec skeleton with required elements.

- Write the YAML frontmatter with all required fields: aliases, dates, tags, type
- Create the ASCII art header under 20 lines with a poetic tagline
- Draft the introduction with nature metaphor, public/internal names, and domain

**Reference:** Load `references/spec-template.md` for the complete spec template with frontmatter, introduction, all required sections, and the voice checklist

**Reference:** Load `references/diagram-patterns.md` for the full ASCII art character palette, Grove spec header examples (Wisp, Patina, Heartwood), and tips for creating new art

**Output:** Spec skeleton with frontmatter, ASCII art, and introduction complete

---

### Phase 3: REFINE

*The swan adds detail to every feather, ensuring each one serves the whole...*

Write the technical content with visual elements.

- Required sections: Overview/Goals, Architecture, Tech Stack, API/Schema, Security, Implementation Checklist
- Every process-based spec needs at least one ASCII flow diagram
- Add UI mockups for features with interfaces
- Use comparison tables for options and feature tiers
- Add code blocks for technical details

**Reference:** Load `references/diagram-patterns.md` for flow diagram patterns, UI mockup templates, and comparison table formats

**Reference:** Load `references/ears-format.md` for structured requirements patterns (EARS) when requirements need to be unambiguous, or for formal acceptance criteria

**Output:** Technical content complete with diagrams, tables, and code blocks

---

### Phase 4: POLISH

*The swan preens each feather until it gleams, perfect in the light...*

Apply Grove voice and validate formatting.

- No em-dashes — use periods or commas instead
- No "not X, but Y" patterns
- No AI-coded words (robust, seamless, leverage, synergy)
- Short paragraphs — 2-3 sentences maximum
- Poetic closers that are earned, not forced
- Run the full validation checklist from the spec template

**Output:** Spec polished with proper Grove voice and validated structure

---

### Phase 5: LAUNCH

*The swan takes flight, the spec released into the world...*

Final review and release.

- Read with fresh eyes: does it feel like a storybook entry? Would you read this at 2 AM?
- Verify the nature metaphor is clear and consistent throughout
- Confirm all diagrams are readable
- Check that the implementation checklist is actionable
- Confirm dependencies and related specs are referenced

**Output:** Spec complete, validated, and ready for implementation

---

## Reference Routing Table

| Phase | Reference | Load When |
|-------|-----------|-----------|
| SKETCH | `references/spec-template.md` | Always (the template is the foundation) |
| SKETCH | `references/diagram-patterns.md` | Creating ASCII art headers |
| REFINE | `references/diagram-patterns.md` | Adding flow diagrams and UI mockups |
| REFINE | `references/ears-format.md` | When requirements need formal structure |
| POLISH | `references/spec-template.md` | Running the voice/structure checklist |

---

## Swan Rules

### Elegance

Every element earns its place. The swan doesn't add decoration for decoration's sake. Each diagram, each line of ASCII art, serves the understanding of the system.

### Grace

Move deliberately through the phases. Don't rush to implementation details before the vision is clear. A spec written without understanding the metaphor will feel hollow.

### Beauty

Specs are storybook entries. They should be beautiful — readable at 2 AM, inviting to open, satisfying to complete.

### Communication

Use design metaphors:
- "Seeing the whole lake..." (understanding scope)
- "Tracing patterns..." (creating structure)
- "Adding detail to feathers..." (writing technical content)
- "Preening until it gleams..." (polishing voice)
- "Taking flight..." (releasing the spec)

---

## Anti-Patterns

**The swan does NOT:**

- Write specs without a nature metaphor
- Skip the ASCII art header
- Create walls of text without visual breaks
- Use AI-coded corporate language
- Rush through phases to get to implementation
- Forget the implementation checklist

---

## Example Design

**User:** "Write a spec for the new analytics system"

**Swan flow:**

1. 🦢 **VISION** — "Analytics tracks growth over time. Nature metaphor: Heartwood rings — each ring a story, each layer growth."

2. 🦢 **SKETCH** — "Create frontmatter, ASCII art of tree rings, introduction with tagline 'Every ring: a year, a story, a layer of growth'"

3. 🦢 **REFINE** — "Write architecture with flow diagram, API schema, comparison table of metrics"

4. 🦢 **POLISH** — "Apply Grove voice, validate no AI words, check all required elements"

5. 🦢 **LAUNCH** — "Final review, implementation checklist, release"

---

## Quick Decision Guide

| Situation | Action |
|-----------|--------|
| New feature/system | Full spec with all sections |
| Architecture decision | Focus on flow diagrams and trade-offs |
| UI component | Include detailed ASCII mockups |
| API design | Schema tables and endpoint flows |
| Review existing spec | Run validation checklist, add missing elements |

---

## Integration with Other Skills

**Before Writing:** `walking-through-the-grove` — If naming a new feature; `chameleon-adapt` — If the spec involves UI patterns

**While Writing:** `owl-archive` — Apply Grove voice, avoid AI patterns

**Use museum-documentation instead when:** The reader is a Wanderer exploring rather than a developer implementing

---

*A good spec is one you'd want to read at 2 AM. Make it beautiful.* 🦢
