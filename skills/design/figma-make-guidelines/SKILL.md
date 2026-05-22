---
name: figma-make-guidelines
description: Generate, rewrite, or repair exactly one copy-ready `guidelines/Guidelines.md` for Figma Make, with self-contained rules and explicit token values. Use when users ask to create/standardize/fix Figma Make guidelines, request one canonical guideline file, request tokenized design rules with direct values (color/type/spacing/states), or ask to replace repository-path references with inline values.
---

# Figma Make Guidelines

## Goal

Produce one deterministic output file that Figma Make can execute without repository inspection:
- `guidelines/Guidelines.md`

## Trigger Terms

Use this skill when requests include one or more of:
- "Figma Make guidelines"
- "one canonical guidelines file"
- "`guidelines/Guidelines.md`"
- "tokenized design rules"
- "direct token values"
- "rewrite or fix guideline rules"

Do not use this skill as primary workflow when the user asks for UI implementation, code refactors, or multi-file guideline architecture.

## Scope Gate (Run First)

1. If the user asks for a single-file guidelines workflow, use this skill.
2. If the user explicitly asks for multi-file guideline architecture (`guidelines/components/*`, `design-tokens/*`), do not force single-file output. State that this skill is single-file by design and ask whether to continue in single-file mode.
3. If the user asks for non-guideline deliverables (for example: direct component implementation or code refactor), do not use this skill as the primary workflow.

Decision outcomes:
- `single-file request` -> proceed
- `multi-file request` -> ask one confirmation to switch to single-file mode
- `non-guideline request` -> route to a better-matched skill

## Hard Constraints

- Create or update exactly one file: `guidelines/Guidelines.md`.
- Do not create `guidelines/components/*.md` or any additional guideline files.
- Do not instruct Figma Make to read repository files, code paths, or external docs.
- Do not use instructions such as "see `src/...`", "read tokens from ...", or "follow project config".
- Put all required values directly in `Guidelines.md`:
  - color tokens with concrete values
  - typography scale (size/line-height/weight)
  - spacing scale
  - radius/elevation/focus tokens
  - interaction states
  - component usage rules
- Keep language concise, imperative, and implementation-ready.

## Minimal Inputs to Collect

Ask only for missing essentials:
1. Product context + target surface (dashboard, marketing site, app shell, mobile web).
2. Visual direction (minimal, bold, enterprise, playful, etc.).
3. Theme mode (light, dark, both).
4. Existing token values (if already defined).
5. Component inventory + required states.
6. Optional stack constraints for handoff wording (Angular, React, Tailwind, CSS Modules, etc.).

If details are missing, proceed with defaults and list assumptions briefly.

Input discipline:
- Ask at most one compact clarification message that covers all missing essentials.
- If user is non-responsive or asks to proceed immediately, continue with defaults and explicit assumptions.

## Default Baseline (When User Values Are Missing)

Use this baseline only when the user did not provide values:
- Palette: neutral-first + one primary accent + one focus color.
- Spacing scale: `4, 8, 12, 16, 20, 24, 32, 40, 48`.
- Typography minimum:
  - Display `32/40 600`
  - H2 `24/32 600`
  - H3 `20/28 600`
  - Body `16/24 400`
  - Caption `12/16 400`
- Radius: `Sm 6`, `Md 10`, `Lg 14`, `Pill 999`.
- Elevation: `Level 0 none`, `Level 1 subtle`, `Level 2 stronger`.
- Focus style: visible `2px` ring + soft outer glow.

## Rules to Always Encode in `Guidelines.md`

### 1) Tokens are source of truth
- Define semantic token names and concrete values in the document.
- Include semantic names plus explicit values (hex/rgba and typography numbers).
- Use semantic tokens in component rules.
- Do not introduce off-scale spacing, colors, radii, or shadows.

### 2) Layout mapping is explicit
- Map Auto Layout to `flex`, `flex-col`, `items-*`, `justify-*`, `gap-*`.
- Keep spacing tokenized.
- Avoid absolute positioning except overlays/decorative layers.

### 3) Component reuse first
- Reuse existing components before introducing new patterns.
- If missing, use the closest existing pattern and request confirmation before adding a new component.

### 4) Variants and states are mandatory
- Required states: `default`, `hover`, `pressed`/`active`, `focus`, `disabled`.
- Preferred prop schema: `variant`, `size`, `tone`, `iconLeft`, `iconRight`, `loading`, `disabled`.
- Require visible `focus-visible` behavior.

### 5) Stack wording discipline
- If stack is specified, keep handoff stack-aware.
- If stack is unknown, keep guidance stack-neutral.
- Use one consistent icon family; no ad-hoc icon drawing.

## Generation Workflow (Deterministic)

1. Confirm scope gate and single-file requirement.
2. Collect only missing minimal inputs in one compact clarification step.
3. Resolve values using precedence:
   - user-provided values (highest)
   - existing canonical values already present in user text/context
   - default baseline values in this skill (lowest)
4. Write assumptions as a short bullet list.
5. Produce only `guidelines/Guidelines.md` using the required section order.
6. Run self-check and fix issues before returning.
7. Return only paste-ready file content; do not prepend planning notes.

Output contract:
- Default output is raw Markdown content, directly pasteable into `guidelines/Guidelines.md`.
- Use fenced code blocks only when user explicitly asks for fenced output.
- Do not emit JSON wrappers, metadata envelopes, or extra files.

## Self-Check (Required)

Fail output if any item is false:
- No contradictions across sections.
- All required values are present directly in the file.
- No references to local paths, folders, or "read from project" instructions.
- Rules are executable without extra repository context.
- Required footer line exists exactly once.

Required footer line:
- `_Open Code -> guidelines -> Guidelines.md in Figma Make._`

Uniqueness checks:
- Footer line appears exactly once.
- Section headers `## 1)` through `## 9)` each appear exactly once and in order.

## Output Structure (Required Order)

Use this exact order in `guidelines/Guidelines.md`:
1. Purpose & scope
2. General guidelines
3. Implementation rules
4. Design tokens (source of truth)
5. Layout & spacing
6. Component usage
7. Accessibility
8. Developer handoff
9. Extending guidelines

## Copy-Ready Template

```md
# Figma Make Guidelines

## 1) Purpose & scope
- Define what this guideline controls (UI structure, tokens, component behavior, handoff).
- State supported themes and platforms.

## 2) General guidelines
- Use Auto Layout and responsive constraints by default.
- Use the defined spacing scale consistently.
- Prefer components + variants over detached duplicates.
- Keep hierarchy clear and accents intentional.

## 3) Implementation rules
- If Angular + Tailwind is used:
  - Reuse existing components before writing new markup.
  - Prefer utility classes in templates.
  - Keep class pass-through on reusable components.
- If another stack is used:
  - Mirror these same principles with equivalent conventions.
- Icons:
  - Use one consistent icon family only.
  - Do not draw ad-hoc icons.

## 4) Design tokens (source of truth)
- Provide explicit token tables directly in this section.
- Include:
  - Base colors (neutral + brand)
  - Semantic background/text/border/accent/focus tokens
  - Typography tokens with size, line-height, and weight
  - Spacing scale values
  - Radius values
  - Elevation/focus effect values
- Example format:
  - `Semantic/Bg/Canvas: #0B0F14`
  - `Semantic/Text/Primary: #F8FAFC`
  - `Type/Body: 16px / 24px / 400`
  - `Radius/Md: 10`

## 5) Layout & spacing
- Auto Layout to Tailwind mapping:
  - `Horizontal` -> `flex items-center`
  - `Vertical` -> `flex flex-col`
  - `Gap` -> `gap-*`
  - `Align/Justify` -> `items-*` / `justify-*`
- Use spacing scale only.
- Avoid absolute positioning except overlays/decorative layers.

## 6) Component usage
- Reuse existing components first.
- Required states: `default`, `hover`, `pressed`, `focus`, `disabled`.
- Preferred prop schema: `variant`, `size`, `tone`, `iconLeft`, `iconRight`, `loading`, `disabled`.
- For each component, provide direct rules for:
  - Purpose
  - Variants
  - Visual tokens used
  - State behavior
  - Sizing and spacing
- Minimum components to define when not specified:
  - `Button`
  - `Input/Text field`
  - `Card/Panel`
  - `Navigation`
  - `Badge/Chip`
  - `Modal/Dialog`
- If no matching component exists, use the closest existing one and request approval before adding a new component.

## 7) Accessibility
- Require visible `focus-visible` states.
- Meet WCAG contrast requirements.
- Do not convey meaning with color alone.
- Ensure keyboard operability for interactive elements.

## 8) Developer handoff
- Map each Figma element to:
  1. Existing component
  2. Styling utilities or classes
  3. Semantic tokens used
- Include variant/state mapping in handoff notes.
- Do not reference repository paths as required context.

## 9) Extending guidelines
- Add new rules in this same `Guidelines.md` file.
- Keep rules concise, imperative, and non-duplicative.
- Add component-specific guidance as subsections under `## 6) Component usage`.

_Open Code -> guidelines -> Guidelines.md in Figma Make._
```

## Response Discipline

- Return content that is immediately pasteable.
- Keep output concise; avoid long theory sections.
- Enforce semantic tokens, component reuse, and variant-driven states.
- Prefer direct values over references to external sources.
- Keep `Guidelines.md` as the single canonical guidelines file.
- Do not emit additional files, JSON wrappers, or fenced-code-only placeholders unless user explicitly asks for fenced output.

## Failure Handling

- If required scope is ambiguous, ask exactly one compact clarification question.
- If user declines clarification or asks to proceed, continue with defaults and explicit assumptions.
- If user insists on multi-file output, state that this skill cannot satisfy that requirement as-is and propose switching to a multi-file-capable skill.
