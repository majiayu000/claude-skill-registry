---
name: modern-accessible-html-jsx
description: Write clean, modern, and highly accessible HTML & JSX code, using semantically correct elements and attributes
---

# Clean & Accessible HTML

We write **semantic, accessible, standards-compliant HTML** by default.
Accessibility is a baseline requirement, not an enhancement.

## Semantics First

- **PREFER** semantic elements (`header`, `nav`, `main`, `section`, `article`, `footer`)
- **AVOID** generic `div`/`span` usage when a semantic element exists
- Use correct heading hierarchy (`h1` → `h6`) without skipping levels

## Accessibility

- **ALWAYS** ensure interactive elements are keyboard accessible
- **PREFER** native HTML elements over ARIA whenever possible
- **DO NOT** use ARIA to fix bad HTML semantics
- Provide accessible names for all interactive controls
  - Labels for inputs
  - `aria-label` or visible text where required

## Forms & Inputs

- **ALWAYS** associate labels with form controls
- **PREFER** native validation and input types (`email`, `url`, `number`, etc.)
- Ensure error messages are accessible and announced properly

## Images & Media

- **ALWAYS** provide meaningful `alt` text for images
- Use empty `alt=""` only for purely decorative images
- Provide captions (`figcaption`) where context matters

## Landmarks & Structure

- Use landmark roles implicitly via semantic elements
- Ensure a single, clear `main` region
- Structure content for screen readers, not just visual layout

## General Principles

- HTML is the foundation — do not fight it
- Accessibility is non-negotiable
- If it works without CSS or JS, it’s probably correct
