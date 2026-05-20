---
name: figma-make-always-check
description: Always check the OMS Figma Make project before executing user work, then route to the best matching global .agents skills and complete the requested task. Use when a request should stay aligned with the canonical OMS design intent while still handling any concrete implementation, refactor, review, or content task the user asks.
---

# Figma Make Always Check

## Goal

Enforce one orchestration rule: verify the OMS Figma Make source first, then execute the user request using the minimal set of relevant global `.agents` skills.

## Mandatory First Action

1. Open `references/oms-figma-make.md`.
2. Check this exact URL first: `https://www.figma.com/make/VQeYDTGteluPfiNKq1ZaQC/OMS?t=j4sIRnOerI7uoUG0-1`.
3. Treat the linked Make project as baseline design intent for OMS decisions.
4. If the URL is unavailable, continue with local context and explicitly note that the Figma Make check could not be completed.

## Routing and Execution

1. Parse the user request into one concrete objective.
2. Select the smallest set of global `.agents` skills needed to execute that objective.
3. Apply selected skills in deterministic order:
   - Architecture/setup skills first.
   - Design translation skills second.
   - Validation/enforcement skills last.
4. Reuse existing app components before creating new ones.
5. Complete the requested work end-to-end, including code updates and validation when possible.

## Selection Heuristics

Use these mappings to pick helper skills quickly:

- Figma-to-code build/refactor: prefer `implement-design` and relevant Angular enforcement skills.
- Atomic decomposition requests: add `figma-atomic-design-implementation`.
- Figma Make pipeline requests: add `figma-make-angular20-tailwind4-implementation`.
- Folder architecture requests: add `angular-folder-structure`.
- Component companion-file enforcement: add `angular-component-rule`.
- Theme/token work: add `angular-tailwind-theme-design`.

If multiple skills overlap, keep only the minimum set that fully covers the request.

## Output Contract

Return:

1. Whether the OMS Figma Make URL check succeeded.
2. Which additional global skills were used and why.
3. Files changed and validation outcomes.
4. Any gap between user request and available design context.

## Guardrails

1. Never skip the Figma Make check when accessible.
2. Never let orchestration block delivery of the user request.
3. Prefer minimal changes that satisfy the request and existing repository conventions.
4. Keep assumptions explicit when design details are missing.
