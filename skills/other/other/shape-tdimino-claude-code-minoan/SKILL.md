---
name: shape
description: "Plan the UX and UI for a feature before writing code. Run a structured discovery interview, then produce a design brief (.design-context.md) that guides implementation. Establishes design direction, constraints, and strategy before any code is written. Triggers on plan the design, design brief, shape the UX, before we build, design discovery."
argument-hint: "[feature to shape]"
---

Shape the UX and UI for a feature before any code is written. This skill produces a **design brief** — a structured artifact that guides implementation through discovery, not guesswork.

**Scope**: Design planning only. This skill produces design briefs, not code.

## Preparation

Read `~/.claude/skills/minoan-frontend-design/SKILL.md` for aesthetic principles and anti-pattern guidance. These inform the design direction but should not constrain the discovery interview.

Check for existing design context: `.design-context.md` in the project root, or a `## Design Context` section in CLAUDE.md. If either exists, use it as a starting point — don't re-ask questions it already answers.

## Phase 1: Discovery Interview

Do NOT make any design decisions during this phase. Understand the feature deeply enough to make excellent decisions later.

### Interview cadence

Ask **2-3 questions per round**, then wait for answers. One round is the default. Add a second only if the first answers leave material gaps — don't run a second round just to feel thorough.

**Assert-then-confirm, not menu-with-escape.** When the user's prompt and existing context make one option obvious, name it and ask the user to confirm or override. "This reads as Restrained, confirm?" beats a four-option menu when the answer is already clear.

Ask these questions conversationally — adapt based on answers, don't dump them all at once:

### Purpose & Context
- What is this feature for? What problem does it solve?
- Who specifically will use it? (Role, context, frequency — not just "users")
- What does success look like? How will you know this feature is working?
- What's the user's state of mind when they reach this? (Rushed? Exploring? Anxious?)

### Content & Data
- What content or data does this feature display or collect?
- What are the realistic ranges? (Minimum, typical, maximum — e.g., 0 items, 5 items, 500 items)
- What are the edge cases? (Empty state, error state, first-time use, power user)

### Design Direction

Force a visual decision on three fronts. Skip anything existing context already answers; ask only what's missing.

- **Color strategy for this surface.** Pick one: Restrained / Committed / Full palette / Drenched. Can override the project default if the surface earns it (e.g. a drenched hero inside an otherwise Restrained product).
- **Theme via scene sentence.** Write one sentence of physical context for this surface: who uses it, where, under what ambient light, in what mood. The sentence forces dark vs light. If it doesn't, add detail until it does.
- **Two or three named anchor references.** Specific products, brands, objects. Not adjectives like "modern" or "clean."
- What's the single most important thing a user should do or understand here?
- Are there existing patterns in the product this should be consistent with?

### Scope

Always ask. Sketch quality and shipped quality are different outputs — don't guess between them.

- **Fidelity.** Sketch / mid-fi / high-fi / production-ready?
- **Breadth.** One screen / a flow / a whole surface?
- **Interactivity.** Static visual / interactive prototype / shipped-quality component?
- **Time intent.** Quick exploration, or polish until it ships?

### Constraints
- Technical constraints? (Framework, performance budget, browser support)
- Content constraints? (Localization, dynamic text length, user-generated content)
- Mobile/responsive requirements?
- Accessibility requirements beyond WCAG AA?

### Anti-Goals
- What should this NOT be? What would be a wrong direction?
- What's the biggest risk of getting this wrong?

## Phase 1.5: Visual Direction Probe (Capability-Gated)

After the interview, generate 2-4 visual direction probes **before** writing the final brief when all of these are true:
- The work is **net-new** or directionally ambiguous enough that visual exploration will clarify the brief.
- The requested fidelity is **mid-fi, high-fi, or production-ready**.
- The current harness gives you native image generation (e.g. `image_gen`, an MCP tool, or similar).

When those conditions are met, this step is mandatory. If image generation isn't natively available, state in one line that the step is skipped and proceed.

The probes should differ in **primary visual direction** (hierarchy, topology, density, typographic voice, color strategy), not just palette tweaks. Treat them as direction tests — ask the user which feels closest, what's off, and what should carry forward. If probes reveal a mismatch, revise the brief inputs before finalizing.

## Phase 2: Design Brief

After the interview (and any probes), synthesize into a structured design brief. Present it and **stop** — the user must confirm before considering this skill complete.

**Choose the brief shape based on clarity:**
- **Compact form (3-5 bullets)** when discovery was crisp and existing context already pins scope, content, and direction. End with one or two specific questions or "confirm or override?"
- **Full structured form** when the task is genuinely ambiguous, multi-screen, or the user asked for shape as a standalone step.

Don't pad a clear brief into a long one to look thorough.

**1. Feature Summary** (2-3 sentences)
What this is, who it's for, what it needs to accomplish.

**2. Primary User Action**
The single most important thing a user should do or understand here.

**3. Design Direction**
Color strategy (Restrained / Committed / Full palette / Drenched) + theme scene sentence + 2-3 named anchor references. Reference the project's design context if available. Set DESIGN_VARIANCE, MOTION_INTENSITY, and VISUAL_DENSITY (1-10 each) based on discovery answers. Consult `~/.claude/skills/minoan-frontend-design/references/design-dials.md`. If Visual Direction Probes were run, name which direction won and what changed.

**4. Layout Strategy**
High-level spatial approach: what gets emphasis, what's secondary, how information flows. Describe the visual hierarchy and rhythm, not specific CSS.

**5. Key States**
List every state the feature needs: default, empty, loading, error, success, edge cases. For each, note what the user needs to see and feel.

**6. Interaction Model**
How users interact with this feature. What happens on click, hover, scroll? What feedback do they get? What's the flow from entry to completion?

**7. Content Requirements**
What copy, labels, empty state messages, error messages, and microcopy are needed. Note any dynamic content and its realistic ranges.

**8. Open Questions**
Anything unresolved that the implementer should resolve during build.

**9. Implementation Skills**
Consult `references/design-media-catalog.md`. Based on discovery answers, recommend which skills the implementer should invoke beyond `/minoan-frontend-design`. Only list skills that match actual needs discovered — don't enumerate the full catalog.

---

Get explicit confirmation of the brief before finishing. If the user disagrees with any part, revisit the relevant discovery questions.

Once confirmed, write the brief to `.design-context.md` in the project root (or update the existing file). The user can then hand it to `/minoan-frontend-design` or use it to guide any other implementation approach.
