---
name: oiloil-ui-ux-guide
description: Modern, clean UI/UX guidance + review skill. Use when you need actionable UX/UI recommendations, design principles, or a design review checklist for new features or existing systems (web/app). Focus on CRAP (Contrast/Repetition/Alignment/Proximity) plus task-first UX, information architecture, feedback & system status, consistency, affordances, error prevention/recovery, and cognitive load. Enforce a modern minimal style (clean, spacious, typography-led), reduce unnecessary copy, forbid emoji as icons, and recommend intuitive refined icons from a consistent icon set.
---

# OilOil UI/UX Guide (Modern Minimal)

Use this skill in two modes:

- `guide`: Provide compact principles and concrete do/don't rules for modern clean UI/UX.
- `review`: Review an existing UI (screenshot / mock / HTML / PR) and output prioritized, actionable fixes.

Keep outputs concise. Prefer bullets, not long paragraphs.

## Workflow (pick one)

### 1) `guide` workflow
1. Identify the surface: marketing page / dashboard / settings / creation flow / list-detail / form.
2. Identify the primary user task and primary CTA.
3. Apply the system-level guiding principles first (mental model and interaction logic).
4. Then apply the core principles below (start from UX, then refine with CRAP).
5. If icons are involved: apply `references/icons.md`.

### 2) `review` workflow
1. State assumptions (platform, target user, primary task).
2. List findings as `P0/P1/P2` (blocker / important / polish) with short evidence.
3. For each major issue, label the diagnosis: execution vs evaluation gulf; slip vs mistake (see `references/design-psych.md`).
4. Propose fixes that are implementable (layout, hierarchy, components, copy, states).
5. End with a short checklist to verify changes.

Use `references/review-template.md` when you need a stable output format.

## Non-negotiables (hard rules)
- No emoji used as icons (or as UI decoration). If an emoji appears, replace it with a proper icon.
- Icons must be intuitive and refined. Use a single consistent icon set for the product (avoid mixing styles).
- Minimize copy by default. Add explanatory text only when it prevents errors, reduces ambiguity, or improves trust.

## System-Level Guiding Principles (cross-system, high-level)

Use these as first-order constraints before choosing specific components or page patterns.

- Concept constancy:
  - Definition: The same business concept keeps the same name, meaning, and interaction semantics across the system.
  - Review question: If a user learns this concept in one place, can they transfer that understanding everywhere else?
- Primary task focus:
  - Definition: Each screen has one dominant objective with the highest visual and interaction priority.
  - Review question: Can users identify the most important action within 3 seconds?
- UI copy source discipline (for product development):
  - Definition: visible UI copy should come from business content, not from implementation constraints or generation instructions.
  - Preferred copy sources:
    - User task: what the user is trying to do.
    - System state: what is happening now (loading, empty, error, success, permission).
    - Result + next step: what changed and what users can do next.
    - Risk/trust context: only when it prevents mistakes or improves confidence.
  - Internal-only sources (do not render directly in product UI by default):
    - Visual/style constraints (e.g., "minimal", "black-and-white", "modern").
    - Technical constraints and implementation notes.
    - Prompt instructions, review rubrics, and generation meta text.
  - User-facing copy framing heuristic (general, not title-specific):
    - Applies to any prominent UI copy: titles, section headers, callouts, badges, CTA labels, and empty states.
    - Prefer user-outcome framing: describe the user's goal and the result they get.
    - Avoid self-referential/process framing for end-user product UI (e.g., "to showcase", "this page demonstrates", "showing the skill's value").
    - Exception: if the surface is explicitly a demo/tutorial/spec page for builders, self-referential/process copy can be acceptable when it improves understanding.
  - State perceptibility (high-level, cross-system):
    - Problem: users make errors when an important internal state is not perceivable (mode, scope, selection, unsaved changes, environment, permission).
    - Principle: make state visible using the lowest-noise signal that reliably changes behavior.
    - Preferred signals (in order):
      - Structural change: the layout/components clearly switch (read -> edit; list -> selection; view -> compare).
      - Control state: the control that changes behavior shows its state (tabs, toggles, segmented controls).
      - Inline signifiers: local cues near the affected area (selection count, scope chip, disabled reason).
      - Post-action feedback: clear results + next step (reduces evaluation gulf).
      - Only if needed: persistent banners/labels for high-risk, sticky modes.
    - Avoid: redundant "status labels" that restate what the structure already makes obvious (they add noise but not clarity).
  - Practical workflow:
    - First build a content model (task/state/result/risk).
    - Then apply visual constraints through layout, hierarchy, and component styling.
    - Run a final copy pass: if a sentence does not help task completion, state understanding, or trust, move it to internal notes.
  - Review question: is each visible sentence useful for end users, or only useful for builders/reviewers?
- Help text layering (avoid "hint sprawl"):
  - Problem this prevents: dumping all tips onto the UI feels "safe", but it destroys hierarchy and increases scanning cost.
  - Placement heuristic:
    - L0 (Always visible): only information needed to complete the task correctly.
    - L1 (Nearby): short guidance for high-risk / high-ambiguity inputs.
    - L2 (On demand): examples, advanced details, "learn more".
    - L3 (After action): result, error, recovery, and next step.
  - Copy budget heuristic:
    - Prefer one clear helper line over multiple repetitive hints.
    - If a page needs many persistent hints, improve IA or defaults first.
- Feedback loop closure:
  - Definition: Every user action must complete a full loop: received, in progress, result, and clear next step.
  - Review question: At any moment, can users tell what the system is doing and what they should do next?
- Prevention first + recoverability:
  - Definition: Reduce error probability before submission, and provide recovery paths for high-risk outcomes.
  - Review question: Is the path designed to be easy to do right and safe to recover when wrong?
- Progressive complexity:
  - Definition: Show minimum-required controls by default; reveal advanced capability only when context requires it.
  - Review question: Can novices complete the core task quickly without limiting expert throughput?
- Action perceptibility (affordance + signifiers):
  - Definition: Interactive targets and likely outcomes are perceivable from structure and visual cues, without guesswork.
  - Review question: Without reading help text, can users predict what is actionable and what will happen?
- Cognitive load budget:
  - Definition: Limit new rules, terms, and interaction modes per screen; prioritize reuse over novelty.
  - Review question: As information grows, does comprehension cost stay stable?
- Evolution with semantic continuity:
  - Definition: Introduce new components/patterns only when existing ones cannot solve the problem, and keep semantic compatibility.
  - Review question: Is this necessary innovation or avoidable interaction drift?

## Core Principles (minimal set)

### A) Task-first UX
- Make the primary task obvious in <3 seconds.
- Allow exactly one primary CTA per screen/section.
- Optimize the happy path; hide advanced controls behind progressive disclosure.

### B) Information architecture (grouping & findability)
- Group by user mental model (goal/object/time/status), not by backend fields.
- Use clear section titles; keep navigation patterns stable across similar screens.
- When item count grows: add search/filter/sort early, not late.

### C) Feedback & system status
- Always show: loading, empty, error, success, and permission states.
- After any action, answer: "did it work?" + "what changed?" + "what can I do next?"
- Prefer inline, contextual feedback over global toasts (except for cross-page actions).

### D) Consistency & predictability
- Same interaction = same component + same wording + same placement.
- Use a small, stable set of component variants; avoid one-off styles.

### E) Affordance / 示能性 + Signifiers / 指示符 (make actions obvious)
- People should see **what can be done** and **how to do it** without guessing.
- Clickable things must look clickable (button/link styling + hover/focus + cursor); avoid “mystery meat” UI.
  - Web: if you implement clickability on non-native elements (e.g. `div` with `onClick`), ensure `cursor: pointer` and proper focus styles.
- Do not hide primary actions behind unlabeled icons. If an icon can be misunderstood, add a short label.
- Prefer **natural mapping**: control placement mirrors the thing it controls (layout, direction, grouping).
- Forms: show constraints before submit (format, units, examples, required), not only after errors.

### F) Error prevention & recovery
- Prevent errors with constraints, defaults, and inline validation.
- Make destructive actions reversible when possible; otherwise require deliberate confirmation.
- Error messages must be actionable (what happened + how to fix).

### G) Cognitive load control
- Reduce choices: sensible defaults, presets, and progressive disclosure.
- Break long tasks into steps only when it reduces thinking (not just to look "enterprise").
- Keep visual noise low: fewer borders, fewer colors, fewer competing highlights.

### H) CRAP (visual hierarchy & layout)
- Contrast: emphasize the few things that matter (CTA, current state, key numbers).
- Repetition: tokens/components/spacing follow a scale; avoid “almost the same” styles.
- Alignment: align to a clear grid; fix 2px drift; align baselines where text matters.
- Proximity: tight within a group, loose between groups; spacing is the primary grouping tool.

## Spacing & layout discipline (compact rule set)

Use this when implementing or reviewing layouts. Keep it short, but enforce it strictly.

- Rule 1 - One spacing scale:
  - Base unit: 4px.
  - Allowed spacing set (recommended): 4 / 8 / 12 / 16 / 24 / 32 / 40 / 48.
  - New gaps/padding should use this set; off-scale values need a clear reason.
- Rule 2 - Repetition first:
  - Same component type keeps the same internal spacing (cards, list rows, form groups, section blocks).
  - Components with the same visual role should not have different spacing patterns.
- Rule 3 - Alignment + grouping:
  - Align to one grid and fix 1-2px drift.
  - Tight spacing within a group, looser spacing between groups.
- Rule 4 - No decorative nesting:
  - Extra wrappers must add real function (grouping, state, scroll, affordance).
  - If a wrapper only adds border/background, remove it and group with spacing instead.
- Quick review pass:
  - Any off-scale spacing values?
  - Any baseline/edge misalignment?
  - Any wrapper layer removable without losing meaning?

## Modern minimal style guidance (taste with rules)
- Use whitespace + typography to create hierarchy; avoid decoration-first design.
- Prefer subtle surfaces (light elevation, low-contrast borders). Avoid heavy shadows.
- Keep color palette small; use one accent color for primary actions and key states.
- Copy: short, direct labels; add helper text only when it reduces mistakes or increases trust.

## Motion (animation) guidance (content/creator-friendly, not flashy)
- Motion explains **hierarchy** (what is a layer/panel) and **state change** (what just happened). Avoid motion as decoration.
- Default motion vocabulary: fade; then small translate+fade; allow tiny scale+fade for overlays. Avoid big bouncy motion.
- Keep the canvas/content area stable. Panels/overlays can move; the work surface should not “float.”
- Prefer consistency over variety: same component type uses the same motion pattern.
- Avoid layout jumps. Use placeholders/skeletons to keep layout stable while loading.

## References
- Icon rules and “intuitive refined” guidance: `references/icons.md`
- Review output template and scoring: `references/review-template.md`
- Expanded checklists (use when needed): `references/checklists.md`
- Design Psychology (示能性、指示符、映射、约束、错误类型、概念模型): `references/design-psych.md`
