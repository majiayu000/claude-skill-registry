---
name: ask-multi
description: Present a multi-select question allowing multiple choices
---

# Ask Multi Skill

Multi-select variant of the AskUserQuestion tool.

## Usage

```
/ask-multi "Question" "Option 1" "Option 2" ["Option 3"] ["Option 4"]
```

## Instructions

When this skill is invoked:
1. First quoted argument = question text
2. Remaining arguments = options (2-4 required)
3. Invoke AskUserQuestion tool with parsed arguments
4. Set multiSelect: true

## Constraints

- Minimum 2 options, maximum 4 options
- If constraints violated, inform user of limits

## Examples

```
/ask-multi "Which features to enable?" "Auth" "Logging" "Caching" "Metrics"
/ask-multi "Select environments to deploy:" "dev" "staging" "prod"
/ask-multi "Install which extras?" "test" "dev" "docs"
```
