---
name: ck:ck-help
description: "ClaudeKit usage guide — discover commands, skills, workflows naturally."
argument-hint: "[category|command|task description]"
---

# ClaudeKit Help

All-in-one ClaudeKit guide. Run the script and present output based on type markers.

## Intent Validation

The script uses keyword matching with smart weighting. After getting results, **validate** against these heuristics:

| Sentence Pattern | Primary Intent | Example |
|------------------|----------------|---------|
| `[action verb] my [object]` | The action verb | "commit my changes" → git |
| `[context] [subject noun]` | The subject noun | "setup notifications" → notifications |
| `[noun] [noun]` | Last noun (topic) | "discord webhook" → notifications |

**Action verbs** (high intent when first): fix, test, commit, push, build, create, review, deploy, run, check, find, plan, refactor

**Context words** (low intent, modify subject): setup, add, start, new, my, the, configure

**Override script only if:** result clearly mismatches the sentence pattern above. Otherwise trust the algorithm.

## Translation

**IMPORTANT: Always translate `$ARGUMENTS` to English before passing to script.**

The Python script only understands English keywords. If `$ARGUMENTS` is in another language:
1. Translate `$ARGUMENTS` to English
2. Pass the translated English string to the script

## Execution

```bash
python .claude/skills/ck-help/scripts/ck-help.py "$ARGUMENTS"
```

## Output Type Detection

The script outputs a type marker on the first line: `@CK_OUTPUT_TYPE:<type>`

**Read this marker and adjust your presentation accordingly:**

### `@CK_OUTPUT_TYPE:comprehensive-docs`

Full documentation (config, schema, setup guides).

**Presentation:**
1. Show the **COMPLETE** script output verbatim
2. **THEN ADD** helpful context: real-world examples, common gotchas, practical scenarios
3. End with a specific follow-up question

### `@CK_OUTPUT_TYPE:category-guide`

Workflow guides for skill categories.

**Presentation:**
1. Show the complete workflow and command list
2. **ADD** practical context: when to use vs alternatives, real examples, transition tips
3. Offer to help with a specific task

### `@CK_OUTPUT_TYPE:command-details`

Single skill/subcommand documentation.

**Presentation:**
1. Show full skill info from script
2. **ADD**: concrete usage example, when this skill shines vs alternatives, common flags
3. Offer to run the skill flow for them

### `@CK_OUTPUT_TYPE:search-results`

Search matches for a keyword.

**Presentation:**
1. Show all matches from script
2. **HELP** user navigate: group by relevance, suggest most likely match, offer to explain
3. Ask what they're trying to accomplish

### `@CK_OUTPUT_TYPE:task-recommendations`

Task-based skill suggestions.

**Presentation:**
1. Show recommended skills from script
2. **EXPLAIN** the reasoning: why these skills fit, suggested order, what each step accomplishes
3. Offer to start with the first recommended command

## Key Principle

**Script output = foundation. Your additions = value-add.**

Never replace or summarize the script output. Always show it fully, then enhance with your knowledge and context.

## Important: Correct Workflows

- **`/ck:plan` → `/ck:cook`**: Best for high-risk or complex changes
- **`/ck:cook`**: Standalone for straightforward implementation
- **NEVER** claim `/ck:plan` is mandatory before `/ck:cook`
