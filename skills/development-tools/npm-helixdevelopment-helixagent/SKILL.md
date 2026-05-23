---
name: npm
description: Handle npm package installation in non-interactive environments by piping confirmations. Use when installing Node.js packages that require user confirmation prompts.
triggers:
- npm
---

When using npm to install packages, you will not be able to use an interactive shell, and it may be hard to confirm your actions.
As an alternative, you can pipe in the output of the unix "yes" command to confirm your actions.