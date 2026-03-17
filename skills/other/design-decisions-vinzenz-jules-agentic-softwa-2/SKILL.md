---
name: design-decisions
description: Forces documentation of the reasoning behind every significant design decision. Creates a decision log that explains WHY choices were made, alternatives considered, and trade-offs accepted. Prevents unjustified "default" choices.
---

# Design Decision Logger Skill

You are operating with design decision logging capabilities. This skill ensures that every significant design choice has documented reasoning — transforming unconscious defaults into conscious decisions.

## Core Philosophy

> "Great design isn't about creating features; it's about intentionality."

AI design fails not because it picks the "wrong" options, but because it picks options without reasons. A design where every choice has documented justification will always be better than one with "good defaults."

## Why Log Decisions?

**For the current design:**
- Forces examination of unconscious defaults
- Reveals unjustified choices that need reconsideration
- Creates accountability for design quality

**For future iteration:**
- Explains WHY something is the way it is
- Enables informed changes (not breaking things accidentally)
- Teaches newcomers the design rationale

**For collaboration:**
- Makes critique more productive ("I understand why, but...")
- Enables delegation without loss of context
- Creates institutional memory

## What Counts as a "Significant Decision"?

<decision_threshold>
Log decisions that:
- Affect multiple components or screens
- Establish a pattern that will be repeated
- Required choosing between viable alternatives
- Override a common convention or expectation
- Will be questioned by someone reviewing the design

Don't log:
- Individual pixel values within an established system
- Obvious choices with no real alternatives
- Temporary implementations meant to be revisited
</decision_threshold>

## Decision Categories

### 1. Typography Decisions

<typography_decisions>
**Font Family:**
```xml
<decision category="typography" element="font-family">
  <choice>Geist Sans</choice>
  <reason>
    Our users are developers. Geist is designed specifically for
    developer tools, embodying "simplicity, minimalism, and speed"
    which aligns with our principle of "professional precision."
  </reason>
  <alternatives>
    <alternative name="Inter">
      Rejected: Overused in our competitive space (Linear, Vercel,
      Notion all use it). We need differentiation.
    </alternative>
    <alternative name="SF Pro">
      Rejected: Platform-specific. We need cross-platform consistency.
    </alternative>
    <alternative name="IBM Plex">
      Considered: Good option, but Geist's mono variant is better
      integrated. Would reconsider if Geist unavailable.
    </alternative>
  </alternatives>
  <trade_offs>
    - Less personality than a distinctive display font
    - Requires hosting (not a system font)
    + Excellent readability at all sizes
    + Consistent with developer tool expectations
  </trade_offs>
  <reversibility>Medium — would require full rebrand to change</reversibility>
</decision>
```

**Type Scale:**
```xml
<decision category="typography" element="type-scale">
  <choice>1.25 ratio (Major Third): 12, 15, 19, 24, 30, 37</choice>
  <reason>
    Moderate ratio provides clear hierarchy without dramatic jumps.
    Appropriate for information-dense interfaces where many levels
    of hierarchy are needed.
  </reason>
  <alternatives>
    <alternative name="1.5 ratio (Perfect Fifth)">
      Rejected: Too dramatic for our dense UI. Would require
      too much scrolling to accommodate large headings.
    </alternative>
    <alternative name="1.125 ratio (Major Second)">
      Rejected: Too subtle. Hierarchy becomes unclear, especially
      when combined with weight variations.
    </alternative>
  </alternatives>
</decision>
```
</typography_decisions>

### 2. Color Decisions

<color_decisions>
**Primary Color:**
```xml
<decision category="color" element="primary">
  <choice>#0066FF (Vibrant blue)</choice>
  <reason>
    Blue conveys trust and professionalism (aligned with "professional
    precision" principle). This specific shade is:
    - Distinct from competitor blues (Stripe's is lighter, Linear's is different hue)
    - Accessible against both white and dark backgrounds
    - Energetic enough to serve as CTA color
  </reason>
  <alternatives>
    <alternative name="#6366F1 (Indigo/Purple)">
      Rejected: Too associated with AI/generic SaaS. Would blend
      in rather than differentiate.
    </alternative>
    <alternative name="#10B981 (Green)">
      Rejected: Green implies success/completion. Wrong semantic
      for primary actions.
    </alternative>
  </alternatives>
  <accessibility>
    - White text on this blue: 4.8:1 (AA pass)
    - This blue on white: 4.8:1 (AA pass)
    - Tested with Coblis for color blindness visibility
  </accessibility>
</decision>
```

**Color Palette Philosophy:**
```xml
<decision category="color" element="palette-philosophy">
  <choice>Monochromatic base + single accent</choice>
  <reason>
    Our UI is information-dense. Multiple colors would create
    visual chaos. Single accent creates clear affordances
    (blue = interactive). Grayscale hierarchy for content.
  </reason>
  <principles_served>
    - "Professional precision" — not playful multicolor
    - "Focus on content" — color doesn't distract
  </principles_served>
</decision>
```
</color_decisions>

### 3. Spacing Decisions

<spacing_decisions>
**Base Unit:**
```xml
<decision category="spacing" element="base-unit">
  <choice>4px base unit</choice>
  <reason>
    4px allows fine-grained control while maintaining consistency.
    8px would be too coarse for our dense UI. Scale: 4, 8, 12, 16,
    24, 32, 48, 64.
  </reason>
  <alternatives>
    <alternative name="8px base">
      Rejected: Jumps between 8 and 16 too large for subtle
      adjustments in dense layouts.
    </alternative>
  </alternatives>
  <implementation>
    CSS custom properties: --space-1 through --space-8
    Tailwind: Extended spacing scale
  </implementation>
</decision>
```

**Component Density:**
```xml
<decision category="spacing" element="density">
  <choice>Compact density (less padding than typical)</choice>
  <reason>
    Power users (our target) prefer information density. They're
    scanning, not reading. Reference: Linear, GitHub, VS Code
    all use compact density for professional tools.
  </reason>
  <trade_offs>
    - Harder for beginners
    - Requires careful touch target sizing
    + More visible at once
    + Feels professional/powerful
  </trade_offs>
</decision>
```
</spacing_decisions>

### 4. Layout Decisions

<layout_decisions>
**Page Structure:**
```xml
<decision category="layout" element="page-structure">
  <choice>Fixed sidebar + fluid content area</choice>
  <reason>
    Sidebar provides consistent navigation anchor. Fluid content
    allows adaptation to data needs. Reference: Linear, Notion,
    VS Code all use this pattern for tool-based products.
  </reason>
  <alternatives>
    <alternative name="Top navigation">
      Rejected: Loses vertical space. Our users have wide screens;
      horizontal space is abundant.
    </alternative>
    <alternative name="Collapsible sidebar">
      Accepted as option: Sidebar can collapse for full-focus mode.
    </alternative>
  </alternatives>
</decision>
```

**Grid System:**
```xml
<decision category="layout" element="grid">
  <choice>12-column grid with 24px gutters</choice>
  <reason>
    12 divides evenly by 2, 3, 4, 6 — maximum flexibility.
    24px gutters balance density with breathing room.
  </reason>
  <responsive_behavior>
    - Desktop: 12 columns
    - Tablet: 8 columns
    - Mobile: 4 columns
  </responsive_behavior>
</decision>
```
</layout_decisions>

### 5. Component Decisions

<component_decisions>
**Button Styles:**
```xml
<decision category="components" element="buttons">
  <choice>
    Primary: Filled blue, white text
    Secondary: Outlined, blue border, blue text
    Tertiary: Text only, blue text
    Destructive: Filled red for dangerous actions
  </choice>
  <reason>
    Visual hierarchy matches importance hierarchy. Fill = most
    important, outline = alternative option, text = least prominent.
    Color coding (blue vs red) adds semantic meaning.
  </reason>
  <size_rationale>
    Default: 36px height (comfortable click target)
    Small: 28px (for dense contexts)
    Large: 44px (for primary page actions)
  </size_rationale>
</decision>
```

**Form Inputs:**
```xml
<decision category="components" element="inputs">
  <choice>Bottom border only (not full border)</choice>
  <reason>
    Reduces visual noise in forms with many fields. Lighter
    appearance aligns with "professional precision" — not
    chunky or heavy.
  </reason>
  <alternatives>
    <alternative name="Full border">
      Available as variant: For isolated inputs or emphasis.
    </alternative>
  </alternatives>
  <accessibility>
    Border color meets 3:1 contrast for UI components.
    Focus state adds left border + background shift.
  </accessibility>
</decision>
```
</component_decisions>

### 6. Motion Decisions

<motion_decisions>
**Animation Philosophy:**
```xml
<decision category="motion" element="philosophy">
  <choice>Functional motion only — no decorative animation</choice>
  <reason>
    Our users are power users doing focused work. Animation
    should communicate state changes, not entertain. Every
    animation must answer: "What information does this convey?"
  </reason>
  <where_animation_used>
    - Page transitions (context: what changed)
    - Loading states (progress: something is happening)
    - Feedback (confirmation: action succeeded/failed)
    - Reveals (hierarchy: new content appearing)
  </where_animation_used>
  <where_animation_not_used>
    - Hover effects (too noisy at high interaction rates)
    - Idle states (distracting)
    - "Personality" animations (off-brand)
  </where_animation_not_used>
</decision>
```

**Timing:**
```xml
<decision category="motion" element="timing">
  <choice>
    Micro-interactions: 150ms
    Component transitions: 200ms
    Page transitions: 300ms
    Easing: cubic-bezier(0.4, 0, 0.2, 1) (Material "standard")
  </choice>
  <reason>
    Fast enough to feel instant, slow enough to be perceived.
    Consistent easing creates unified feel. Material easing
    is well-tested and feels natural.
  </reason>
</decision>
```
</motion_decisions>

## Decision Log Template

<decision_template>
```xml
<design_decision_log>
  <metadata>
    <project>Project name</project>
    <created>Date</created>
    <last_updated>Date</last_updated>
    <authors>Who made/documented these decisions</authors>
  </metadata>

  <principles_reference>
    <!-- Link back to design brief -->
    <principle id="1">Principle name</principle>
    <principle id="2">Principle name</principle>
  </principles_reference>

  <decisions>
    <decision id="DES-001" category="typography" date="YYYY-MM-DD">
      <element>What was decided</element>
      <choice>The decision made</choice>
      <reason>Why this choice serves our users/principles</reason>
      <alternatives>
        <alternative name="Option name" rejected_because="Reason"/>
      </alternatives>
      <trade_offs>
        <accepted>What we gave up</accepted>
        <gained>What we gained</gained>
      </trade_offs>
      <principles_served>1, 2</principles_served>
      <reversibility>easy/medium/hard</reversibility>
      <depends_on>DES-000 (if dependent on another decision)</depends_on>
    </decision>

    <!-- More decisions... -->
  </decisions>

  <unresolved>
    <question id="Q-001">
      <topic>What needs to be decided</topic>
      <options>Possible choices</options>
      <blocking>What this blocks</blocking>
    </question>
  </unresolved>
</design_decision_log>
```
</decision_template>

## Validation Questions

For each logged decision, verify:

<validation>
1. **"Why this?"** — Can you explain the choice without saying "it looks good"?
2. **"Why not that?"** — Can you explain why alternatives were rejected?
3. **"For whom?"** — Does this serve the specific users defined in the brief?
4. **"According to what?"** — Which design principle does this support?
5. **"What if wrong?"** — How hard is this to change later?
</validation>

## Red Flags

Decisions that need reconsideration:

<red_flags>
- **"It's the default"** — Not a reason. Why is the default right for us?
- **"Everyone does it"** — Not a reason. Why is convention right here?
- **"It looks good"** — Not a reason. Good for whom? In what context?
- **"I like it"** — Not a reason. User preference trumps designer preference.
- **No alternatives listed** — Did you actually consider options?
- **Principle not referenced** — How does this serve the design goals?
</red_flags>

## Output Summary

<summary_format>
```xml
<decision_log_summary>
  <statistics>
    <total_decisions>N</total_decisions>
    <fully_justified>N with complete reasoning</fully_justified>
    <needs_revision>N missing justification</needs_revision>
    <unresolved_questions>N</unresolved_questions>
  </statistics>

  <coverage>
    <typography_decisions>N</typography_decisions>
    <color_decisions>N</color_decisions>
    <spacing_decisions>N</spacing_decisions>
    <layout_decisions>N</layout_decisions>
    <component_decisions>N</component_decisions>
    <motion_decisions>N</motion_decisions>
  </coverage>

  <red_flags_found>
    <flag decision_id="DES-XXX">
      <issue>What's problematic</issue>
      <recommendation>How to fix</recommendation>
    </flag>
  </red_flags_found>

  <overall_intentionality>
    Score 1-10 with explanation of how well decisions are justified
  </overall_intentionality>
</decision_log_summary>
```
</summary_format>

## Key Principle

> "It feels like a person looked at it and said, 'This is it.'" — On Linear's design

Every decision in a great design system should feel like someone cared about it specifically. The decision log is proof of that care.
