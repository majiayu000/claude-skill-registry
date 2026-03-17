---
name: ask
description: Present a multiple-choice question to the user using AskUserQuestion tool
---

# Ask Skill

Quick invocation of the AskUserQuestion tool for single-select questions.

## Usage

```
/ask "Question" "Option 1" "Option 2" ["Option 3"] ["Option 4"]
```

## Instructions

When this skill is invoked:
1. First quoted argument = question text
2. Remaining arguments = options (2-4 required)
3. Invoke AskUserQuestion tool with parsed arguments
4. Set multiSelect: false

## Constraints

- Minimum 2 options, maximum 4 options
- If constraints violated, inform user of limits

## Examples

```
/ask "Which testing framework?" "pytest" "unittest" "nose2"
/ask "Deploy to which environment?" "staging" "production"
/ask "Database choice?" "PostgreSQL" "MySQL" "SQLite" "MongoDB"
```
