---
name: documenting-project
description: Generates comprehensive technical documentation including READMEs, setup guides, and API specs. Ensures every project has a clear "Instruction Manual" for future developers.
---

# Technical Writer & Documentarian

## When to use this skill
- When the user says "write the readme" or "how do I run this?".
- After finishing a major feature to document how it works.
- When the codebase is complex and needs identifying comments.

## Workflow
1.  **Scan Context**: Read `package.json`, `docker-compose.yml`, and main entry points to understand the stack.
2.  **Select Artifact**:
    - **README.md**: The landing page (Title, Install, Features).
    - **CONTRIBUTING.md**: For open source (Code formatting, PR rules).
    - **Inline Docs**: JSDoc/Docstrings for confusing code blocks.
3.  **Draft**: Write clear, step-by-step markdown.
4.  **Polish**: Add emojis, code blocks, and badges to make it readable.

## Instructions
### The Perfect README Structure
1.  **Title & Banner**: Project name and 1-sentence pitch.
2.  **Tech Stack**: Icons or list of frameworks used.
3.  **Quick Start**: The *shortest* path to running the app (e.g., `npm install && npm run dev`).
4.  **Env Variables**: A table of required `.env` keys (do not reveal secrets!).
5.  **Features**: Bullet points of what the app does.
6.  **Architecture**: Brief mention of the folder structure (referencing `architecting-structure` skill).

## Self-Correction Checklist
- "Did I include the `.env` example?" -> Critical for setup.
- "Is the Quick Start copy-pasteable?" -> Users hate typing long commands.
