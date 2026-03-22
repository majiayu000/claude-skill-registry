---
name: design-exploration
description: "Agent-mode pre-implementation design exploration. Invoked by other skills (brainstorm, nf) to gather codebase context and explore design approaches before implementation. Not user-invoked directly."
context: fork
agent: Explore
allowed-tools:
  - Read
  - Glob
  - Grep
  - Task
  - AskUserQuestion
---

# Brainstorming Ideas Into Designs

## Overview

Help turn ideas into fully formed designs and specs through natural collaborative dialogue.

Start by understanding the current project context using multiple Explore agents in parallel (with Sonnet model) to quickly gather relevant information from files, docs, and recent commits. Then ask questions to refine the idea. Once you understand what you're building, present the design in small sections (200-300 words), checking after each section whether it looks right so far.

## The Process

**Understanding the idea:**
- **Use multiple Explore agents in parallel** (Sonnet model) to quickly gather context from files, docs, and recent commits
- Ask questions to refine the idea - batch related questions when it makes sense
- Prefer multiple choice questions when possible, but open-ended is fine too
- Focus on understanding: purpose, constraints, success criteria

**Exploring approaches:**
- Propose 2-3 different approaches with trade-offs
- Present options conversationally with your recommendation and reasoning
- Lead with your recommended option and explain why

**Presenting the design:**
- Once you believe you understand what you're building, present the design
- Break it into sections of 200-300 words
- Ask after each section whether it looks right so far
- Cover: architecture, components, data flow, error handling, testing
- Be ready to go back and clarify if something doesn't make sense

## Key Principles

- **Parallel context gathering** - Use Explore agents to quickly understand the codebase
- **Multiple choice preferred** - Easier to answer than open-ended when possible
- **YAGNI ruthlessly** - Remove unnecessary features from all designs
- **Explore alternatives** - Always propose 2-3 approaches before settling
- **Incremental validation** - Present design in sections, validate each
- **Be flexible** - Go back and clarify when something doesn't make sense
