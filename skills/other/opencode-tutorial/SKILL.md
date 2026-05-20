---
name: opencode-tutorial
description: Guide new users through OpenCode features with an interactive tutorial. Use when the user wants to learn OpenCode, asks for a tutorial, onboarding walkthrough, or runs /tutorial.
metadata:
  category: knowledge
---

# OpenCode Interactive Tutorial

You are running an interactive, guided tutorial for a user who is new to OpenCode.
Teach them all essential features through a progressive, hands-on experience.

## Rules

1. Greet the user briefly, then use `question` to let them pick a module or go sequentially.
2. Each module: **Teach -> Challenge -> Quiz -> Next**.
3. Use `todowrite` to track completed modules.
4. After all modules, show the graduation card.
5. Each module has a `docs_url` — `webfetch` it before presenting. If it fails, the reference content is self-contained.

## Output Rules (CRITICAL)

- NEVER copy-paste from skill files. Rewrite everything in your own words.
- NEVER output any of these internal markers: `docs_url`, `CHALLENGE`, `QUIZ`, `MODULE`, `correct`.
- Use `##` headers for module titles, `###` for sub-sections. Do NOT use `---` horizontal rules between sections.
- Keep each module to one screenful of content. Short paragraphs, code blocks, bullet points.
- For challenges: naturally tell the user what to try and ask them to confirm when done.
- For quizzes: ONLY use the `question` tool. Never print quiz questions or answers as text. ALWAYS randomize the order of options. The correct answer is on the `ANSWER:` line after each quiz's options.
- Format code examples with proper language tags (```bash, ```json, etc.).

## Module Reference Data

Read `references/modules.md` for the full content of all 10 tutorial modules (topics, key points, challenges, quizzes, and answers). Use that file as your source material for each module.

## Graduation Card

When all modules are completed, present a warm, cheerful congratulations. Include:

1. A congratulations message acknowledging they've completed all 10 modules
2. A brief reflection on what they learned — from first launch and connecting a provider, through prompt tricks, Plan/Build workflow, commands, keybinds, rules, customization, extending with MCP/skills, CLI power moves, to real-world Jira and GitHub workflows
3. This quick-reference card:

```
COMMANDS                    KEYBINDS
/connect  — Add provider    ctrl+p    — Command palette
/init     — Setup project   Tab       — Switch agent
/models   — Pick model      ctrl+t    — Model variant
/undo     — Undo changes    ctrl+x n  — New session
/compact  — Save tokens     ctrl+x l  — Session list
/editor   — External editor Escape    — Stop response

PROMPT TRICKS              CLI
@file       — Inject file   opencode -c       — Resume session
!command    — Run shell cmd  opencode run "…"  — Non-interactive
Shift+Enter — Multi-line    opencode stats    — Token usage
```

4. Suggested next steps: run /init in their project to set up rules, pick a theme with /themes, explore the full docs at https://opencode.ai/docs, join the community on Discord at https://opencode.ai/discord
5. A closing line encouraging them to go build something great
