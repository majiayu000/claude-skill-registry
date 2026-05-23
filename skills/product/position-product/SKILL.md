---
name: position-product
description: Define product positioning and brand strategy
argument-hint: <product-name>
---

# position-product

**Category**: Product & Strategy

## Usage

```bash
position-product
```

## Interactive Mode

This command runs an interactive discovery session. Claude Code will:
1. Read the source file
2. Extract discovery questions
3. Guide you through the questions
4. Save results for future reference

## Execution Instructions for Claude Code

When this command is run, Claude Code should:

1. Read the source file at `claude_settings/python/processes/product-positioning.md`
2. Extract all discovery questions from the markdown
3. Run an interactive Q&A session with the user
4. Save the answers to `discovery-results/{command}-{timestamp}.json`
5. Use the answers to guide the implementation

## Source Content Location

The full process documentation can be found at:
`claude_settings/python/processes/product-positioning.md`

Claude Code should read this file and follow the documented process exactly.
