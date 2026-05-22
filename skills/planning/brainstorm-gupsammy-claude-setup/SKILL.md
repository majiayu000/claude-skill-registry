---
name: brainstorm
description: >
  Use when user says "brainstorm", "let's design", "help me think through",
  "I have an idea", "before I start coding", "explore approaches", or wants
  to refine rough ideas into designs through collaborative questioning.
argument-hint: [topic]
---

# Brainstorm Ideas Into Designs

Help turn ideas into fully formed designs and specs through natural collaborative dialogue.

Start by understanding the current project context, then ask questions one at a time to refine the idea. Once you understand what you're building, present the design in small sections (200-300 words), checking after each section whether it looks right so far.

## Process

**1. Understand context**
- Check project state (files, docs, recent commits)
- If `$ARGUMENTS` provided, start with that topic
- Ask questions one at a time to refine the idea
- Prefer multiple choice when possible, but open-ended is fine too
- Only one question per message—if a topic needs more exploration, break it into multiple questions
- Focus on: purpose, constraints, success criteria

**2. Explore approaches**
- Propose 2-3 different approaches with trade-offs
- Present options conversationally with your recommendation and reasoning
- Lead with your recommended option and explain why

**3. Present design incrementally**
- Break into 200-300 word sections
- Ask after each section whether it looks right so far
- Cover: architecture, components, data flow, error handling, testing
- Be ready to go back and clarify if something doesn't make sense

## Principles

- **One question at a time** — Don't overwhelm with multiple questions
- **Multiple choice preferred** — Easier to answer than open-ended when possible
- **YAGNI ruthlessly** — Remove unnecessary features from all designs
- **Explore alternatives** — Always propose 2-3 approaches before settling
- **Incremental validation** — Present design in sections, validate each
- **Be flexible** — Go back and clarify when something doesn't make sense

## Output

When design is complete, offer to save:
- Technical designs → `./[topic]-design.md`
- Save only if user confirms
