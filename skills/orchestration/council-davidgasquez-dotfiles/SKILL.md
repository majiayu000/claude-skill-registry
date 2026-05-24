---
name: council
description: Get a help or a second opinion from other agents. Bundle a prompt and a curated file set, then ask other LLMs for advice (debug, refactor, design, ...).
---

# Council

Use this skill when you want a fast second brain pass from other agents or LLMs on a problem you are facing.

## Workflow

1. Pick the relevant files and build a concise and clear prompt describing the problem
2. Run `ask-council "PROMPT"` to dispatch the same prompt to multiple agents
3. Wait for the responses to come back and review them

## Tips

- Share file paths relative to the project root for best results
- If you need diffs reviewed, paste the diff into the prompt
- Make the prompt completely standalone: include error text, constraints, and the desired output format (plan vs patch vs pros or cons)
- Council can be slow while it reasons. Allow it several minutes to process

## Example

```
ask-council "Review src/foo/bar.js. Find 3 risks and 2 improvements. Return bullets only."
```
