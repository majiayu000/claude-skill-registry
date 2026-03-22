---
name: reactor-audit
description: Use when proposing or implementing any UI, rendering, shader, UX, motion, or DSP change in TRENCH — forces doctrine audit before code, kills generic output, requires structured review with dominant-read analysis and acceptance test
---

# Reactor Audit

**Purpose:** Stop generic, derivative, or doctrine-violating work before it enters the codebase. This is a mandatory review gate, not a style reference.

**Rule:** No UI, rendering, shader, UX, motion, or DSP implementation without completing the audit sequence first. Audit output goes in your response BEFORE any code.

**Doctrine reference:** All material rules, hierarchy, palette, and banned motifs live in the `containment-brutalism` skill. Read it before running this audit. Do not duplicate doctrine here.

## When to Invoke

- Any change to `trench-ui/`, `trench-plugin/src/ui.rs`, Canvas rendering, wgpu pipelines, WGSL shaders
- Any visual design proposal, mockup description, or layout change
- Any motion, animation, or interaction behavior change
- Any DSP logic change in `trench-core/` or audio path of `trench-plugin/`
- Any "make it look better" or "improve the UI" request
- Any new visual element, effect, or rendering technique
- When you catch yourself about to write generic rendering code

**If you skip the audit, the work is invalid. Delete it and start over.**

## Required Audit Sequence

Complete ALL steps. Output each heading in your response.

### 1. DOMINANT READ

What is this change actually about? Name the single dominant concept in ≤10 words. If you can't name it, the change is unfocused — stop and narrow scope.

### 2. STRUCTURAL WEAKNESS

What is generic, weak, derivative, or borrowed about the current state or proposal? Be specific. Name the cliché. Name what it looks like instead of TRENCH. Examples:
- "This looks like a synth plugin preset browser"
- "This glow treatment is terrain-shader-demo energy"
- "This layout reads as dashboard SaaS"

If nothing is weak, say so and why. Don't fabricate problems.

### 3. WHAT TO REMOVE

Before adding anything, what should be deleted or stripped? Restraint is the material. Addition without subtraction is bloat.

If nothing needs removal, state why the current density is correct.

### 4. DOCTRINE CHECK

Test the change against each applicable doctrine category (refer to `containment-brutalism` skill for specifics). Use ✅ PASS or ❌ FAIL with one-line justification.

- **Visual hierarchy** (hero object dominates → coordinate grammar → energy trace → readouts → background)
- **Material** (matte graphite, dead glass, aliased lines, sparse phosphor)
- **Motion** (mechanical, consequential, constrained, weighted)
- **Rendering** (orthographic/shallow iso, hard edges, no decorative effects)
- **DSP** (Rust-only, deterministic, testable, sample-rate-exact, narrow scope)

### 5. STRONGER DIRECTIONS (max 3)

If anything failed doctrine or reads as weak, propose up to 3 stronger directions. Each must:
- Name the specific improvement
- Explain why it is more TRENCH than the current approach
- Be implementable, not aspirational

If the proposal already passes, skip to step 6.

### 6. RECOMMENDED DIRECTION

Pick one. State it in one sentence. This is the direction you will implement.

### 7. ACCEPTANCE TEST

Write 3–5 concrete, falsifiable criteria the implementation must satisfy. Not vibes — checkable assertions.

Example:
- "Hero object occupies ≥60% of viewport area"
- "No element uses border-radius > 0"
- "Trace rendering uses putImageData, not strokeStyle with lineWidth > 1"
- "Motion completes in ≤150ms, no easing curve"

---

## Anti-Pattern Kill List

These trigger immediate rejection. If you catch yourself producing any, stop, delete, restart from step 1.

| Anti-Pattern | What It Looks Like | Why It Dies |
|---|---|---|
| **Shader sludge** | Perlin noise backgrounds, procedural fog, volumetric anything | Decorative computation. Zero information. |
| **Plugin chrome** | Brushed metal, knob skeuomorphism, LED arrays | Consumer audio product aesthetic. |
| **Dashboard drift** | Card layouts, sidebar nav, breadcrumbs, modals | SaaS UX leaked into instrument. |
| **Glow addiction** | bloom(50px), box-shadow spread, neon traces | Diffusion destroys precision. |
| **HUD cosplay** | Circular reticles, targeting brackets, scan lines as decoration | Sci-fi cliché. TRENCH is not a game. |
| **Prettification** | Smoothing rough edges, adding polish, "cleaning up" | Roughness is intentional. Crude = authority. |
| **Motion fluff** | Ease-in-out on everything, spring physics, parallax | Motion must be mechanical and consequential. |
| **Vague uplift** | "Modernize", "refresh", "elevate", "enhance" | Meaningless without doctrine-grounded direction. |
| **Architecture creep** | "While we're here, let's also refactor..." | Narrow scope. Do the thing asked. |
| **Rate confusion** | Mixing 39062.5 Hz and 44100 Hz contexts | Two domains. Know which one you're in. |

## Implementation Guardrails

After completing the audit, apply during implementation:

1. **Subtraction first.** Remove before adding. Every new element must justify displacement of emptiness.
2. **One material change at a time.** Don't combine structural + rendering + motion changes.
3. **Hero object test.** After every visual change: "Does the hero object still dominate?" If no, revert.
4. **Pixel-level specificity.** "Add a border" is not a spec. "2px solid #1A1A1A inset on left and bottom edges" is.
5. **No comfort defaults.** If your first instinct is border-radius, box-shadow, or gradient — delete it.
6. **Test the ugliness.** If it looks too polished, you've drifted. Crude is correct.
7. **DSP changes require numerical verification.** No "should work" — run the test, show the evidence.

## Review Language Rules

Blunt and high-signal. No motivational fluff.

Banned phrases: "Looks great", "Good foundation", "Consider...", "You might want to...", "To make it more...", "Adding some...", "A nice touch would be...", "For a more polished look..."

## Response Template

```
## REACTOR AUDIT

### 1. Dominant Read
[≤10 words naming the core concept]

### 2. Structural Weakness
[What is generic, weak, or derivative — be specific]

### 3. What to Remove
[What gets deleted before anything gets added]

### 4. Doctrine Check
- Visual hierarchy: ✅/❌ [one line]
- Material: ✅/❌ [one line]
- Motion: ✅/❌ [one line]
- Rendering: ✅/❌ [one line]
- DSP: ✅/❌ [one line] (if applicable)

### 5. Stronger Directions
[Up to 3, or "PASS — proposal already meets doctrine"]

### 6. Recommended Direction
[One sentence]

### 7. Acceptance Test
- [ ] [Falsifiable assertion 1]
- [ ] [Falsifiable assertion 2]
- [ ] [Falsifiable assertion 3]

---
[Implementation ONLY after audit is complete]
```
