---
name: phx-intro
description: Walk through the Elixir/Phoenix plugin commands, workflow, and features
  in 6 interactive sections. Use when a new user wants to learn what the plugin offers
  or needs a refresher on available commands.
---

# Plugin Introduction Tutorial

Interactive walkthrough of the Elixir/Phoenix plugin in 6 sections (~5 min).

## Arguments

- `$ARGUMENTS` may contain `--section N` to jump to a specific section (1-6)
- No arguments = start from Section 1

## Execution Flow

1. Read `references/tutorial-content.md` for all section content
2. Parse `$ARGUMENTS` for `--section N` flag (1-6)
3. If `--section N` specified, jump directly to that section
4. Otherwise start from Section 1

### Section Presentation Loop

For each section:

1. Present the section content **completely** — do NOT abbreviate or summarize. Every paragraph, table, and code block in the reference file must appear in output
   — as **visible response text emitted BEFORE the `AskUserQuestion` call**; content composed only in thinking is invisible to the user
2. After presenting, use `AskUserQuestion` with options:
   - If sections remain: "Next: [next section title]", "Skip to Cheat Sheet", "Stop here"
   - If on final section (6): no question needed, end with closing message

### Section Titles

| N | Title |
|---|-------|
| 1 | Welcome |
| 2 | Core Workflow Commands |
| 3 | Knowledge & Safety Net |
| 4 | Hooks & Behavioral Rules |
| 5 | Init, Review & Gaps |
| 6 | Cheat Sheet & Next Steps |

## Iron Laws

1. **ONE section at a time** — never dump all content at once
2. **User controls pace** — always offer to stop between sections
3. **Clean formatting** — use tables and code blocks, not walls of text
4. **NEVER skip the user's questions** — tutorial is interactive, not a monologue; if the user asks a question mid-section, answer it before continuing

## Closing Message

After Section 6 (or when user stops):

```
You're all set! Try `/phx-plan` with your next feature to see the workflow in action.
Run `/phx-intro --section N` anytime to revisit a specific section.
```

## Notes

- This runs in main conversation context (not a subagent)
- Reference file is readable since skill runs in user's session
- Keep tone welcoming but concise — developers don't want fluff
