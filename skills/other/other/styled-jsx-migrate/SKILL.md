---
name: styled-jsx-migrate
description: Migrate a component from plain CSS/CSS Modules/other CSS-in-JS to styled-jsx while preserving behavior, accessibility, and SSR compatibility.
argument-hint: "[path or ComponentName] [source styling approach]"
allowed-tools: Read, Grep, Glob
disable-model-invocation: true
---

# styled-jsx Migration Skill

Migrate styles safely to styled-jsx.

## Steps

1. Identify current selectors, states, and variants.
2. Map to styled-jsx:
   - scoped styles: <style jsx>
   - global escapes: <style jsx global> with narrow selectors
   - dynamic values: CSS vars or class toggling
3. Remove dead selectors and reduce specificity.
4. Ensure the component remains accessible (roles/labels/focus styles).
5. Update tests/stories accordingly.

## Output expectations

- Provide:
  - Proposed refactor plan
  - New file structure and minimal diff summary
  - Test plan and any risks
