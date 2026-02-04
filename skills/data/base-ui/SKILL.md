---
name: base-ui
description: Base UI reference and workflows for @base-ui/react (unstyled, accessible React components, composition utilities, and form helpers). Use when implementing Base UI components, portals, styling/state hooks, render-prop composition, eventDetails customization, animations, forms/validation, TypeScript typing, CSP/RTL utilities, or checking Base UI docs, issues, or releases.
---

# Base UI

## Overview
Use this skill as a navigation hub for Base UI. Load the specific reference files when needed.

## Start Here
- Read `references/overview.md` for install, portal isolation, iOS 26 Safari, and LLM docs access.
- Pick components from `references/components.md`.
- Choose guidance by need: styling, composition, customization, animation, forms, TypeScript, or utils.

## Reference Map
- `references/overview.md`: install, portals, iOS 26 Safari, LLM docs, project context.
- `references/components.md`: full component and utility index with .md doc links.
- `references/styling.md`: className/state, data attributes, CSS variables, style prop, Tailwind/CSS Modules/CSS-in-JS patterns.
- `references/composition.md`: render prop usage, ref forwarding, nesting render props.
- `references/customization.md`: Base UI events, eventDetails, cancel/allowPropagation, preventBaseUIHandler, controlled vs uncontrolled.
- `references/animation.md`: data attributes, transitions vs animations, Motion/AnimatePresence, keepMounted, getAnimations.
- `references/forms.md`: Form/Field patterns, constraint validation, server-side errors, RHF/TanStack integration.
- `references/typescript.md`: Props/State namespaces, ChangeEventDetails/Reason, actionsRef types, useRender types.
- `references/utils.md`: CSPProvider, DirectionProvider/useDirection, mergeProps/mergePropsN, useRender patterns.
- `references/edge-cases.md`: common pitfalls and fixes.
- `references/examples.md`: concise, runnable examples.
- `references/links.md`: issues and changelog entry points.

## Use Pattern
1. Identify the component or utility.
2. Read the component docs in `references/components.md`.
3. Pull in the relevant handbook or utility reference.
4. Confirm edge cases in `references/edge-cases.md`.
5. Use `references/links.md` for issues and release notes before shipping.
