---
name: component-gallery
description: "Encyclopedic access to UI component patterns and design system implementations from component.gallery (60 components, 95 design systems, 2,676+ real-world examples). This skill should be used when researching how specific UI components are implemented across production design systems, comparing component patterns before building, finding alternative component names, or grounding frontend decisions in real-world precedent. Pairs with minoan-frontend-design for research-then-build workflows."
allowed-tools: Bash(component-gallery:*), Read, Grep, Glob
---

# Component Gallery — Pattern Research via Local RAG

Research real component implementations before building. The gap between "I'll make a sidebar" and "here's how Atlassian, Shopify, and GitHub each solved sidebar navigation" is the gap between guessing and grounding. This skill bridges it.

## Philosophy

Every UI component has been built thousands of times. The best implementations share patterns that no single designer invented—they emerged from convergent problem-solving across design systems with different constraints. Studying these patterns before writing code prevents reinventing solved problems, surfaces accessibility requirements that are easy to miss, and reveals implementation trade-offs that only become visible when comparing multiple approaches side by side.

Pattern research is not copying. It is the equivalent of a literature review before writing a paper. Build with awareness of what exists, then make deliberate choices about what to keep, adapt, or reject.

## Quick Reference — Static Indexes

Read these files directly for fast lookup. No RAG query needed.

| File | Contents |
|------|----------|
| `references/component-index.md` | All 60 component types with alt names, example counts, descriptions |
| `references/design-system-index.md` | All 95 design systems with org, tech stack, features, links |
| `references/component-taxonomy.md` | Components grouped by functional category (Forms, Navigation, Feedback, Layout, Data Display, Actions) |

For a quick answer to "what is this component called?" or "which design systems use React?"—read the index files. Reserve RAG queries for deeper questions.

## RAG Query — Semantic Search

Query the `component-gallery` RLAMA collection for implementation details, cross-system comparisons, and pattern analysis.

```bash
# How do production design systems implement a specific component?
python3 ~/.claude/skills/component-gallery/scripts/query.py "how do design systems implement date picker accessibility"

# Compare implementations across systems
python3 ~/.claude/skills/component-gallery/scripts/query.py "compare sidebar navigation patterns"

# Find components that solve a specific UX problem
python3 ~/.claude/skills/component-gallery/scripts/query.py "components for progressive disclosure of complex forms"

# Search by alternative name (e.g., "flyout" → Drawer)
python3 ~/.claude/skills/component-gallery/scripts/query.py "flyout panel slide from edge"

# Broader queries benefit from more chunks
python3 ~/.claude/skills/component-gallery/scripts/query.py "responsive table patterns" -k 20
```

Default retrieve-only mode returns raw chunks for Claude to synthesize. This produces stronger analysis than local model generation.

## Workflow Protocol — Pairing with minoan-frontend-design

Component Gallery provides the *what* (pattern research, implementation precedent, accessibility requirements). Minoan Frontend Design provides the *how* (creative direction, typography, color, spatial composition, craft standards).

### Research-then-build sequence

1. **Identify components needed.** Read `references/component-index.md` to confirm the component type exists and find its canonical name.
2. **Query for implementation patterns.** Use RAG to retrieve how 3-5 design systems approach the component—focus on structure, states, accessibility, and responsive behavior.
3. **Synthesize findings.** Identify convergent patterns (things most systems agree on) and divergent choices (where systems differ based on context).
4. **Build with minoan-frontend-design.** Apply creative direction from the design skill. The component's *structure* is informed by research; its *aesthetic* is informed by the design skill.
5. **Verify accessibility.** Cross-reference research findings against the implementation. Confirm ARIA roles, keyboard navigation, focus management, and screen reader announcements.

### When to skip research

For trivial components (a single button, a text input) where the implementation is well-understood and creative direction is the primary concern, invoke minoan-frontend-design directly. Reserve component-gallery queries for components with meaningful structural complexity: data tables, date pickers, command palettes, multi-step forms, sidebar navigation, filterable lists.

## Maintenance

```bash
# Full re-crawl and rebuild (run when component.gallery updates)
python3 ~/.claude/skills/component-gallery/scripts/ingest.py --full

# Rebuild RLAMA collection only (from existing scraped files)
python3 ~/.claude/skills/component-gallery/scripts/ingest.py --rebuild-rag

# Rebuild static indexes only
python3 ~/.claude/skills/component-gallery/scripts/build_indexes.py
```

## Anti-Patterns

**Guessing component structure.** Never invent a component's ARIA pattern, keyboard behavior, or state machine from first principles when the collection contains documented patterns from production design systems. Query first.

**Skipping accessibility review.** Every component query should include or be followed by an accessibility check. The most common failure mode is building a visually correct component that is inaccessible to keyboard and screen reader users.

**Treating examples as templates.** Design system examples document *their* constraints (Shopify's Polaris serves commerce, Atlassian's ADS serves enterprise collaboration). Extract the structural pattern, not the specific aesthetic. The aesthetic comes from minoan-frontend-design.

**Over-querying for simple components.** A styled button does not need a five-system comparison. Match query depth to component complexity.

**Ignoring responsive behavior.** Desktop-only component research misses half the problem. Query explicitly for responsive patterns when the component will appear on mobile.
