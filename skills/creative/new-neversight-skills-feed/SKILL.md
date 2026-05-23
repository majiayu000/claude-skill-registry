---
name: new
description: Start a new fiction project from scratch. Interactive wizard guides you through discovery, architecture, characters, world, and outline.
argument-hint: "[genre or idea]"
context: fork
agent: fiction:new-project
allowed-tools:
  - Read
  - Glob
  - Write
  - Edit
  - Task
  - AskUserQuestion
  - WebSearch
---

Start a new fiction project with guided, Socratic dialogue.

## What This Does

Walks you through creating a complete project foundation:

1. **Discovery** — Find the heart of your story
2. **Architecture** — Build the structure (premise, theme, arc, ending)
3. **Characters** — Develop who lives in this world
4. **World** — Create setting and systems (if needed)
5. **Outline** — Map the journey chapter by chapter

## How It Works

This is a conversation, not a form. The agent asks questions that help you discover what you already know about your story. It offers choices when you're stuck, research when you need context, and celebrates progress along the way.

Everything is saved as you go—architecture, characters, outline—so you never lose work.

## Usage

```
/fiction:new               # Start the wizard
/fiction:new thriller      # Start with a genre in mind
/fiction:new "a story about loss and redemption"  # Start with an idea
```

If arguments provided: $ARGUMENTS
