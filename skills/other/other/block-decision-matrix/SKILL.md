---
name: block-decision-matrix
description: |
  Decision framework for determining new block vs variant vs existing.
  Covers decision criteria, edge cases, and anti-patterns.
  Use this skill when planning block conversion from mocks.
allowed-tools: Read, Glob, Grep
version: 1.0.0
---

# Block Decision Matrix Skill

Framework for deciding whether a mock section should use an existing block,
create a variant, or require a completely new block.

## Decision Flowchart

```
                    Mock Section Analysis
                            │
                            ▼
            ┌───────────────────────────────┐
            │  Find semantically similar    │
            │  existing block               │
            └───────────────┬───────────────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
        FOUND MATCH                  NO MATCH
              │                           │
              ▼                           ▼
    ┌─────────────────────┐      ┌─────────────────┐
    │ Structure match     │      │  NEW_BLOCK      │
    │ >= 80%?             │      │  (definitely)   │
    └──────────┬──────────┘      └─────────────────┘
               │
     ┌─────────┴─────────┐
     │                   │
     ▼                   ▼
   YES                  NO
     │                   │
     ▼                   ▼
┌─────────────┐   ┌─────────────────────┐
│ How many    │   │ Can existing block  │
│ new props   │   │ be extended?        │
│ needed?     │   └──────────┬──────────┘
└──────┬──────┘              │
       │              ┌──────┴──────┐
       │              │             │
       ▼              ▼             ▼
  ┌────────┐       YES            NO
  │ 0-1    │        │             │
  │ props  │        ▼             ▼
  └───┬────┘   ┌─────────┐   ┌─────────┐
      │        │ 2-3     │   │NEW_BLOCK│
      ▼        │ props?  │   └─────────┘
┌───────────┐  └────┬────┘
│USE_EXISTING│      │
└───────────┘  ┌────┴────┐
               │         │
               ▼         ▼
            YES         NO (4+)
               │         │
               ▼         ▼
         ┌─────────┐ ┌─────────┐
         │ VARIANT │ │NEW_BLOCK│
         └─────────┘ └─────────┘
```

## Decision Criteria

### USE_EXISTING - When to Reuse

Use existing block when:

| Criterion | Required |
|-----------|----------|
| Same semantic purpose | Yes |
| Same HTML structure | Yes (>80%) |
| Differences only in styling | Yes |
| No new fields needed | 0-1 max |
| No new interaction patterns | Yes |

**Example scenarios:**
- Hero with different background color → Use `hero`, change `backgroundColor`
- Features grid with 4 columns instead of 3 → Use `features-grid`, change `columns`
- CTA with different button text → Use `cta-section`, change content props

### NEW_VARIANT - When to Extend

Create variant when:

| Criterion | Required |
|-----------|----------|
| Same semantic purpose | Yes |
| Similar structure (60-80%) | Yes |
| 2-3 new fields needed | Yes |
| No structural changes | Yes |
| Enhancement, not transformation | Yes |

**Example scenarios:**
- Hero with badge → Variant with `badge` field
- Features grid with animations → Variant with `animateOnScroll` field
- CTA with countdown → Variant with `countdown` field

### NEW_BLOCK - When to Create New

Create new block when:

| Criterion | Trigger |
|-----------|---------|
| Different semantic purpose | Automatic |
| 4+ new custom fields | Strong indicator |
| Different HTML structure | Strong indicator |
| Unique interaction patterns | Strong indicator |
| Would require >3 conditionals | Strong indicator |

**Example scenarios:**
- Hero with terminal animation → `hero-terminal` (unique component)
- Features as comparison table → `features-comparison` (different structure)
- CTA with lead form → `cta-with-form` (different interaction)

## Complexity Thresholds

### By Custom Props Count

| Custom Props | Decision | Confidence |
|--------------|----------|------------|
| 0 | USE_EXISTING | 100% |
| 1 | USE_EXISTING | 95% |
| 2 | Consider VARIANT | 70% |
| 3 | VARIANT likely | 60% |
| 4 | NEW_BLOCK likely | 70% |
| 5+ | NEW_BLOCK | 90% |

### By Conditionals Required

| Conditionals | Decision | Rationale |
|--------------|----------|-----------|
| 0-1 | Acceptable | Normal branching |
| 2 | Review | May be overloading |
| 3 | Concern | Likely should split |
| 4+ | Split required | Anti-pattern territory |

## Edge Case Examples

### Edge Case 1: Hero with Terminal Animation

**Initial assessment:** Variant of hero
**Final decision:** NEW_BLOCK → `hero-terminal`

**Analysis:**
```
Existing hero structure:
- title (string)
- content (string)
- cta (object)
- backgroundImage (string)
- textColor (enum)

Terminal requires:
- terminalLines (array of {command, output, delay})
- typingSpeed (number)
- cursorStyle (enum)
- promptSymbol (string)
- showLineNumbers (boolean)
```

**Why NEW_BLOCK:**
- 5 new custom fields
- Completely different HTML structure (animated `<pre>` blocks)
- JavaScript animation state management
- Would require 50+ lines of conditional code

### Edge Case 2: Features Grid with Comparison Table

**Initial assessment:** Variant of features-grid
**Final decision:** NEW_BLOCK → `features-comparison`

**Analysis:**
```
Existing features-grid:
- Grid of cards
- Each card: icon, title, description

Comparison table needs:
- Table headers (feature names)
- Row groups (categories)
- Check/X marks per plan
- Sticky header on scroll
```

**Why NEW_BLOCK:**
- Fundamentally different structure (table vs grid)
- Different semantic meaning (comparison vs showcase)
- Would corrupt features-grid's simplicity

### Edge Case 3: Stats with Animated Counters

**Initial assessment:** NEW_BLOCK
**Final decision:** VARIANT → `stats-counter` with `animateOnScroll`

**Analysis:**
```
Existing stats-counter:
- Array of {value, label, prefix, suffix}
- Grid layout options

Animation needs:
- animateOnScroll (boolean)
- animationDuration (number)
```

**Why VARIANT:**
- Same semantic purpose (show statistics)
- Same structure (grid of stat items)
- Only 2 new props
- Animation is enhancement, not transformation

### Edge Case 4: CTA with Email Form

**Initial assessment:** Variant of cta-section
**Final decision:** NEW_BLOCK → `cta-with-form`

**Analysis:**
```
Existing cta-section:
- title, content
- primary button
- secondary button (optional)

Form needs:
- Form fields configuration
- Validation rules
- Success/error states
- Integration settings (API endpoint)
```

**Why NEW_BLOCK:**
- Different interaction pattern (form submission vs navigation)
- State management requirements
- 5+ new props (formFields, submitEndpoint, successMessage, etc.)
- Server action integration

## Anti-Patterns

### The Frankenstein Block

When conditionals accumulate:

```tsx
// BAD - Over-engineered block
function HeroBlock(props) {
  return (
    <section>
      {props.variant === 'terminal' && <TerminalAnimation {...} />}
      {props.variant === 'video' && <VideoPlayer {...} />}
      {props.variant === 'form' && <LeadForm {...} />}
      {props.variant === 'slider' && <ImageSlider {...} />}
      {props.variant === 'basic' && <BasicHero {...} />}
    </section>
  )
}
```

**Problems:**
- Massive bundle size (all variants loaded)
- Testing nightmare
- Props explosion
- Maintenance burden

**Solution:** Split into focused blocks:
- `hero` (basic)
- `hero-terminal`
- `hero-video`
- `hero-with-form`
- `hero-slider`

### The Kitchen Sink

Adding fields "just in case":

```tsx
// BAD - Too many optional fields
interface HeroProps {
  title?: string
  subtitle?: string
  subtitle2?: string
  subtitle3?: string
  badge?: string
  badgeColor?: string
  badgeIcon?: string
  badgePosition?: string
  video?: string
  videoAutoplay?: boolean
  videoMuted?: boolean
  videoLoop?: boolean
  // ... 30 more optional fields
}
```

**Problems:**
- Confusing admin UI (too many fields)
- Most fields never used
- Performance impact
- Documentation burden

**Solution:** Create specific variants for specific needs.

### The God Component

One block trying to do everything:

```tsx
// BAD - One block for all content sections
function ContentBlock(props) {
  switch (props.layout) {
    case 'hero': return <HeroLayout {...} />
    case 'features': return <FeaturesLayout {...} />
    case 'cta': return <CTALayout {...} />
    case 'testimonials': return <TestimonialsLayout {...} />
    // ... 20 more layouts
  }
}
```

**Problems:**
- Breaks block categorization
- Impossible to validate properly
- Schema becomes meaningless
- Registry bloat

**Solution:** Separate blocks per semantic purpose.

## Decision Checklist

Before finalizing decision:

- [ ] Have I identified the semantic purpose?
- [ ] Have I counted required custom fields?
- [ ] Have I checked existing blocks in theme?
- [ ] Have I considered future variants?
- [ ] Would new fields benefit existing block users?
- [ ] Would conditionals be manageable (<3)?
- [ ] Is the HTML structure similar (>80%)?

## Quick Reference Card

```
REUSE: Same purpose + Same structure + 0-1 props
VARIANT: Same purpose + Similar structure + 2-3 props
NEW: Different purpose OR 4+ props OR Different structure
```

## Related Skills

- `page-builder-blocks` - Block structure and patterns
- `mock-analysis` - For understanding mock requirements
