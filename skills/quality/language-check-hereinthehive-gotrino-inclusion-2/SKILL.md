---
name: language-check
description: Analyze code and documentation for non-inclusive language, understanding context and intent before flagging issues. Use when reviewing code for biased terms, gendered language, or problematic terminology.
allowed-tools: Read, Grep, Glob
user-invocable: true
---

# Language Check

Analyze files for non-inclusive language, with emphasis on understanding context before flagging issues.

## Philosophy

This is not a linter. A linter finds strings; this skill *understands code*.

The goal is to:
1. Understand what the code/content is doing
2. Consider who will read or use it
3. Identify language that could exclude or harm
4. Provide contextual, thoughtful suggestions

Pattern matching helps *find candidates*, but your job is to *analyze and reason*.

## Scope

The user may specify a file path, glob pattern, or directory. If not specified, ask what they'd like to check.

## Config Integration

Before starting, check for `.inclusion-config.md` in the project root.

If it exists:
1. **Read** scope decisions and acknowledged findings
2. **Skip** any acknowledged findings (note them in output)
3. **Respect** priority settings
4. **Note** at the top of output: "Config loaded: .inclusion-config.md"

If config says certain checks are out of scope, still run language checks (core dignity principles), but respect acknowledged individual findings.

## Process

### 1. Read and Understand

First, **read the files** to understand:
- What is this code/content for?
- Who is the audience? (developers? end users? both?)
- What's the tone and style?

### 2. Analyze Holistically

As you read, look for language issues in context:

**Gendered language** - Does this assume gender? Use "guys", "he/she", gendered job titles?
- Consider: Who reads this? How might non-male or non-binary people feel?

**Ableist language** - Does this use disability as metaphor? ("crazy", "blind to", "lame")
- Consider: How does this land for someone with that condition?

**Racially loaded terms** - Does this use terms with harmful history? ("whitelist", "master/slave")
- Consider: What's the impact of normalizing these metaphors?

**Dismissive language** - Does this assume things are "easy" or "obvious"?
- Consider: Easy for whom? What if someone struggles with this?

### 3. Apply Context

Not every match is a problem. Use judgment:

**Probably fine:**
- "master's degree" (academic term)
- "blind study" (scientific term)
- "Master" in a proper noun (MasterCard, Scrum Master as job title)
- Historical quotes or references
- Code interfacing with external systems that use these terms

**Probably worth flagging:**
- Variable names: `whitelist`, `masterDB`, `slaveNode`
- Comments addressing readers: "Hey guys", "obviously you'll want to..."
- Documentation: "simply click", "just run this command"
- Error messages users will see

### 4. Suggest Thoughtfully

Don't just say "change X to Y". Explain:
- Why this matters for this specific context
- What the impact might be
- A suggestion that fits the code's style

## Reference

For comprehensive term lists, see `references/language-terms.md`. Use this as a guide, not a checklist.

## Output Format

Keep it **compact**. This is a "fast" check—users want findings, not essays.

```markdown
## Language Analysis: [path]

[1-2 sentences: What is this? Who's the audience? What's the main issue pattern?]

---

### Racially Loaded Terms (4 issues)

Terms with slavery/racial connotations that normalize harmful metaphors.

| Location | Term | Suggestion |
|----------|------|------------|
| file.tsx:7 | `whitelist` | `allowlist` |
| file.tsx:8 | `master/slave` | `primary/replica` |

### Ableist Language (3 issues)

Uses disability as shorthand for "broken" or "bad."

| Location | Term | Suggestion |
|----------|------|------------|
| file.tsx:92 | `sanityCheck` | `validateData` |
| docs.md:57 | "crazy" | "unexpected" |

### Gendered Language (2 issues)

Assumes male as default.

| Location | Term | Suggestion |
|----------|------|------------|
| docs.md:3 | "Hey guys" | "Hello everyone" |
| docs.md:65 | "businessmen" | "professionals" |

### Dismissive Language (3 issues)

Minimizes difficulty, makes struggling users feel inadequate.

| Location | Term | Suggestion |
|----------|------|------------|
| docs.md:7 | "super simple" | (remove) |
| docs.md:11 | "Obviously" | "We recommend" |

---

### Exceptions

- `Mastercard` in docs.md:36 — brand name, fine

### Summary

**22 issues** across 2 files. Priority: user-facing docs (hostile tone in troubleshooting section), then racially loaded variable names.
```

## Output Guidelines

- **Use tables** for findings—one row per issue, not a paragraph
- **One-sentence category intros** max—explain why it matters, then list findings
- **Skip code blocks** unless context is truly ambiguous
- **No individual "Analysis" paragraphs**—the table columns say enough
- **Insights only when non-obvious**—skip the insight if it's just restating why the category matters
- **Summary is a TL;DR**—total count, priority, where to start

## What Makes This Different From a Linter

A linter would flag every instance of "master". You should:

1. **Understand intent** - Is this a database replica config or someone's job title?
2. **Consider audience** - Is this internal code comments or user-facing docs?
3. **Weigh impact** - Will changing this break external integrations?
4. **Suggest appropriately** - Match the codebase's style and conventions

Your value is **judgment**, not detection.
