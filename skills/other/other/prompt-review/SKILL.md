---
name: prompt-review
description: Reviews a prompt/instruction file against Anthropic prompt engineering best practices. Use when evaluating skill files, agent definitions, or instruction chunks for quality.
allowed-tools: Read, Glob, Grep, WebFetch
---

# Prompt Engineering Review

Review a prompt or instruction file against Anthropic's prompt engineering best practices and provide structured, actionable feedback.

## Arguments

`$ARGUMENTS` is the path to the file to review. If not provided, ask the user which file to review.

## Procedure

### Step 1: Fetch Current Best Practices

Fetch the latest Anthropic prompt engineering guidance to ground your review in current recommendations:

```
WebFetch https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
```

Use the fetched content as your primary reference for evaluation criteria. If the fetch fails, proceed using your built-in knowledge of Anthropic prompt engineering best practices.

### Step 2: Read the Target File

Read the file at the path specified in `$ARGUMENTS`. If the path is relative, resolve it from the current working directory.

If the file does not exist, inform the user and stop.

### Step 3: Determine the Prompt Context

Before evaluating, identify how this prompt will be used:

- **Standalone system prompt**: The file is the complete prompt given to Claude
- **Instruction chunk / skill file**: The file is injected into a larger prompt context (e.g., via `!command` dynamic context injection, Claude Code skill files, or agent core-knowledge files)
- **Template with variables**: The file contains placeholders or Jinja2 templates that are filled at runtime

This context affects how you evaluate the prompt. Instruction chunks, for example, must work well when composed with other instructions and should avoid conflicting with likely surrounding context.

### Step 4: Evaluate Against Best Practices

Evaluate the file against each of the following criteria. For each criterion, assess whether the prompt follows it well, partially, or poorly.

<criteria>

1. **Clarity and Specificity**
   - Are instructions unambiguous and precise?
   - Does the prompt say exactly what it wants rather than what it does not want?
   - Are success criteria clearly defined?
   - Would a reader understand exactly what to do without needing to guess intent?

2. **Structure and Formatting**
   - Does the prompt use headers, lists, and sections to organize content?
   - Are XML tags used appropriately to delineate sections (e.g., `<instructions>`, `<example>`, `<context>`)?
   - Is information ordered logically (context before task, general before specific)?
   - Is the structure scannable without being overly verbose?

3. **Role and Identity Prompting**
   - If applicable, does the prompt establish a clear role or expertise for Claude?
   - Is the role specific enough to guide behavior without being artificially constraining?
   - Does the identity framing match the actual task requirements?

4. **Examples and Demonstrations**
   - Are examples provided for complex or ambiguous tasks?
   - Do examples cover both typical cases and edge cases?
   - Are examples formatted consistently with the expected output format?
   - Do examples use realistic content rather than trivial placeholders?

5. **Handling Ambiguity and Edge Cases**
   - Does the prompt address what to do when inputs are incomplete or unexpected?
   - Are fallback behaviors specified?
   - Is there guidance for boundary conditions?

6. **Output Format Specification**
   - Is the expected output format clearly defined?
   - Are there constraints on length, structure, or style?
   - If structured output is needed, is the schema provided or described?

7. **Composability (for instruction chunks)**
   - Will this content work well when injected into a larger prompt?
   - Does it avoid assumptions about surrounding context that may not hold?
   - Does it avoid conflicting directives that might clash with other injected content?
   - Is it self-contained enough to be understood without the surrounding prompt?
   - Does it avoid redefining global behaviors (like persona) that the outer prompt may set?

8. **Conciseness and Signal-to-Noise Ratio**
   - Is every sentence earning its place in the prompt?
   - Is there redundancy or filler that could be removed?
   - Are instructions appropriately dense without sacrificing clarity?
   - Does the prompt avoid over-explaining obvious points?

9. **Variable and Placeholder Usage**
   - Are dynamic inputs clearly marked and documented?
   - Is it obvious what data will be substituted at runtime?
   - Are variable names descriptive and consistent?

10. **Task Decomposition**
    - For complex tasks, does the prompt break work into clear steps?
    - Is the sequence of operations logical?
    - Are dependencies between steps explicit?

</criteria>

### Step 5: Produce the Review

Output the review in the following format. Be direct and specific. Every recommendation must point to a concrete line or section in the file and explain exactly what to change.

<output_format>

## Prompt Review: `{filename}`

**Prompt type**: {standalone system prompt | instruction chunk | template}
**Overall grade**: {A | B | C | D | F}

> One-sentence summary of the prompt's overall quality.

### Strengths

- {Specific strength with brief explanation}
- {Specific strength with brief explanation}

### Issues Found

For each issue:

#### {Issue title}

- **Severity**: {Critical | High | Medium | Low}
- **Criterion**: {Which of the 10 criteria this relates to}
- **Location**: {Line number, section, or quote from the file}
- **Problem**: {What is wrong and why it matters}
- **Recommendation**: {Exact change to make, with a before/after example if helpful}

### Summary of Recommendations

| Priority | Recommendation | Effort |
|----------|---------------|--------|
| {1, 2, ...} | {Brief description} | {Small / Medium / Large} |

</output_format>

## Grading Rubric

- **A**: Follows nearly all best practices. Minor improvements only. Production-ready.
- **B**: Follows most best practices. A few notable gaps. Effective but could be stronger.
- **C**: Misses several important practices. Will work but likely produces inconsistent results.
- **D**: Significant issues. Missing structure, clarity, or key prompt engineering patterns.
- **F**: Fundamentally flawed. Needs a rewrite to be effective.
