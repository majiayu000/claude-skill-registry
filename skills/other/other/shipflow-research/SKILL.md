---
name: shipflow-research
description: Deep web research on any topic — multi-source investigation, structured markdown report saved to file
disable-model-invocation: true
argument-hint: <topic>
---

## Context

- Current directory: !`pwd`
- Project CLAUDE.md: !`head -40 CLAUDE.md 2>/dev/null || echo "no CLAUDE.md"`

## Mode detection

- **`$ARGUMENTS` is provided** → Research that topic.
- **`$ARGUMENTS` is empty** → Use AskUserQuestion to ask what to research.

---

## Flow

### Step 1: Parse topic

If `$ARGUMENTS` is empty, use **AskUserQuestion**:
- Question: "What topic should I research?"
- Options:
  - **Library comparison** — "Compare libraries/tools for a specific need"
  - **Best practices** — "Current best practices for a technology or pattern"
  - **Migration guide** — "How to upgrade or migrate a specific tool"
  - **Architecture** — "Architecture patterns for a specific use case"

Then ask for the specific topic via a second question.

### Step 2: Multi-source research

Use multiple tools to gather comprehensive information:

1. **WebSearch** — broad search for overview, recent articles, blog posts
2. **mcp__exa__web_search_exa** — technical depth, documentation
3. **mcp__exa__get_code_context_exa** — code examples, implementations, Stack Overflow answers
4. **mcp__context7__resolve-library-id** + **mcp__context7__query-docs** — official library documentation
5. **WebFetch** — specific URLs found in search results that need deeper reading

Run searches in parallel where possible (multiple WebSearch + Exa calls in one message).

### Step 3: Synthesize report

Structure the research into a comprehensive markdown report:

```markdown
# Research: [Topic]

> Generated [date] — Sources: [count]

## Executive Summary
[2-3 sentences: what was researched, key finding, recommendation]

## Background
[Why this matters, context for the decision]

## Current State ([year])
[What's the current landscape? Latest versions, trends, adoption]

## Options / Approaches

### Option 1: [Name]
- **Pros**: ...
- **Cons**: ...
- **Best for**: ...
- **Example**:
  ```[lang]
  [code example]
  ```

### Option 2: [Name]
...

## Best Practices
[Current consensus on how to do this well]

## Code Examples
[Practical, tested examples relevant to the project's stack]

## Recommendations
[Specific recommendation for this project, with reasoning]

## Sources
- [Title](URL) — [one-line summary]
- ...
```

### Step 4: Save report

Determine save location:
- If inside a project directory: save to `research/[topic-slug].md` (create `research/` dir if needed)
- If at workspace root (`~/`): save to `~/ShipFlow/research/[topic-slug].md`

Generate a URL-safe slug from the topic: lowercase, hyphens, no special chars.

### Step 5: Report

```
RESEARCH COMPLETE: [topic]
═══════════════════════════════
Sources consulted:  [count]
Report saved to:    [file path]
Key finding:        [one-line summary]
Recommendation:     [one-line recommendation]
═══════════════════════════════
```

---

## Important

- **Every claim must have a source.** No unsourced assertions.
- **Prefer recent sources** (2024-2026). Flag older sources as potentially outdated.
- **Verify code examples** against current API versions. Don't copy deprecated patterns.
- **Save reports** — don't just print them. Reports are reusable reference material.
- If researching a library: always check Context7 first for official docs.
- If the topic is project-specific (e.g., "best auth for Astro"), include the project's stack context.
- Be honest about uncertainty. If sources conflict, present both views.
- Keep code examples in the project's language/framework when possible.
