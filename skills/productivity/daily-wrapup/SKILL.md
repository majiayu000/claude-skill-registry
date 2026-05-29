---
name: daily-wrapup
description: Automate daily note wrapup workflow. Interview for next episode, extract learning ideas, create concept notes. Use when daily wrapup, end of day or wrapup is mentioned by user.
---

# Daily Wrapup

Automates end-of-day workflow for Obsidian daily notes.

## Workflow

1. Read today's daily note (`daily/YYYY-MM-DD.md`)
2. Interview user about tomorrow's plans for Next Episode section
3. Analyze completed Tasks for learning opportunities
4. Extract ideas for new/existing notes
5. Update daily note with Next Episode and Ideas for Notes
6. Create concept notes in `work/concepts/`
7. Link notes back to daily note

## Key Patterns

- Use user-interview skill for Next Episode questions
- Scan Tasks for patterns: "decided", "learned", "debugged", "discovered"
- Create notes matching existing `work/concepts/` structure
- Always link notes to daily note in Origin section

## See `references/interview-questions.md` for Next Episode interview prompts
