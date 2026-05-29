---
name: Code Documentation Style
description: Minimal, evergreen code commenting focused on why over what. Use this when adding comments to complex logic, frame calculations, or non-obvious design decisions. Emphasizes self-documenting code through clear naming and structure over excessive comments.
---

# Code Documentation Style

This Skill provides Claude Code with specific guidance on how it should handle global commenting.

## When to use this skill:

- Documenting complex animation timing calculations
- Explaining non-obvious frame-based logic
- Adding context for architectural decisions
- Documenting tricky Remotion or S3 edge cases
- Clarifying business rules in validation logic
- Adding JSDoc for public function interfaces

## Instructions

- **Self-Documenting Code**: Write code that explains itself through clear structure and naming
- **Minimal, helpful comments**: Add concise, minimal comments to explain large sections of code logic.
- **Don't comment changes or fixes**: Do not leave code comments that speak to recent or temporary changes or fixes. Comments should be evergreen informational texts that are relevant far into the future.
