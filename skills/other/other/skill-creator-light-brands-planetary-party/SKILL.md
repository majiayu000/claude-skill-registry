---
name: skill-creator
description: "Use when creating or editing skills for ai-coding-config repo"
version: 1.2.0
---

<objective>
Skills are reusable reference guides for proven techniques, patterns, and tools. Write them as intelligent companions would read them - focused on goals and outcomes, not rigid procedures.

Core principle: Trust the LLM's intelligence. Describe what needs to happen and why, not
step-by-step how. </objective>

<when-to-create>
Create skills for techniques that weren't intuitively obvious to you, patterns you'd reference across projects, or broadly applicable approaches (not project-specific).

Skip skills for one-off solutions, well-documented standard practices, or
project-specific conventions (use CLAUDE.md instead). </when-to-create>

<skill-structure>
Every skill has YAML frontmatter and markdown content:

```markdown
---
name: skill-name-with-hyphens
description: Use when [triggering conditions] - [what it does and how it helps]
---

# Skill Name

## Overview

What is this? Core principle in 1-2 sentences.

## When to Use

Clear triggers and symptoms. When NOT to use.

## Core Pattern

Show desired approach with examples. Describe alternatives in prose.

## Common Pitfalls

What goes wrong and how to avoid it.
```

Frontmatter requirements:

name: Letters, numbers, hyphens only. Use verb-first active voice (e.g., creating-skills
not skill-creation).

description: Third-person, under 500 characters. Start with "Use when..." to describe
triggering conditions, then explain what it does. Include concrete symptoms and
situations, not just abstract concepts.

Good: "Use when tests have race conditions or pass/fail inconsistently - replaces
arbitrary timeouts with condition polling for reliable async tests" </skill-structure>

<writing-principles>
Show, don't tell (pattern reinforcement): LLMs encode patterns from what you show them. Demonstrate desired approaches with 5+ examples. Describe undesired alternatives in prose without code.

Good pattern:

```typescript
// Use condition-based waiting for reliable async tests
await waitFor(() => element.textContent === "loaded");
await waitFor(() => user.isAuthenticated === true);
await waitFor(() => data.length > 0);
```

Then in prose: "Avoid arbitrary timeouts like setTimeout() which make tests brittle and
slow."

Focus on goals, not process: Describe outcomes and constraints. Let the LLM figure out
how to achieve them.

Good: "Ensure each test has a clear failure mode that identifies what's wrong. Tests
should verify behavior, not implementation details."

Positive framing: Frame as "do this" not "avoid that." Focus on what success looks like.

Good: "Write minimal code to pass the test. Add features only when tests require them."

Trust intelligence: Assume the LLM can handle edge cases and variations. Specify
boundaries, not decision trees.

Good: "Check if files exist before copying. If they differ, show changes and ask the
user what to do." </writing-principles>

<file-organization>
Self-contained (preferred):
```
skill-name/
  SKILL.md    # Everything inline
```

With supporting files (when needed):

```
skill-name/
  SKILL.md           # Overview + patterns
  reference.md       # Heavy API docs (100+ lines)
  tool-example.ts    # Reusable code to adapt
```

Only separate files for heavy reference material (comprehensive API docs) or reusable
tools (actual code to copy/adapt).

Keep inline: Principles and concepts, code patterns under 50 lines, everything else.
</file-organization>

<optimize-for-discovery>
Future Claude needs to find your skill. Use rich keywords: error messages ("ENOTEMPTY", "race condition", "timeout"), symptoms ("flaky", "inconsistent", "unreliable"), tools (actual command names, library names), and synonyms (different terms for same concept).

Put searchable terms in the description and throughout the content.
</optimize-for-discovery>

<token-efficiency>
Every skill loaded costs tokens. Be concise:
- Frequently-loaded skills: under 200 words
- Other skills: under 500 words
- Reference external docs rather than duplicating them
- Use cross-references to other skills instead of repeating
</token-efficiency>

<quality-checklist>
Structure:
- Frontmatter with name and description (third-person, "Use when...")
- Clear overview with core principle
- Concrete "when to use" triggers
- Examples showing desired patterns (5+ for main approach)

Content:

- Goals and outcomes, not rigid procedures
- Positive framing (show what to do)
- Trust LLM intelligence (avoid over-prescription)
- Keywords for search throughout
- Common pitfalls addressed

Organization:

- Self-contained in SKILL.md when possible
- Supporting files only when truly needed
- Under 500 words unless it's reference material </quality-checklist>

<common-mistakes>
Over-prescription: Writing detailed step-by-step procedures for things the LLM can figure out. Describe the goal, not the algorithm.

Showing anti-patterns: Demonstrating "wrong" code teaches that pattern. Describe
alternatives in prose instead.

Vague triggers: "Use when debugging" is too broad. "Use when encountering test failures
with unclear root causes" is specific.

First person: Skills inject into system prompts. Write "Use when..." not "I can help
when..."

Missing keywords: Future Claude searches for skills by symptoms and errors. Include the
terms someone would actually search for. </common-mistakes>
