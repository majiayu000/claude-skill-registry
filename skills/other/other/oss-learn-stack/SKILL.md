---
name: oss-learn-stack
description: |
  Learn unfamiliar technologies used in a repo by studying how the repo actually uses
  them. Finds patterns, explains concepts in context, and points to examples in the
  codebase. Use when a repo uses frameworks, languages, or patterns you haven't
  worked with before.
---

# Learn Stack

Don't learn a framework from docs alone - learn it from how THIS repo uses it. This skill finds the patterns, explains the concepts, and points to real examples in the codebase you're about to contribute to.

## Purpose

`oss-prep-to-contribute` does a knowledge check for one issue. This skill is broader: when a repo uses tech you don't know (unfamiliar language, framework, testing tool, build system, architecture pattern), this skill teaches those concepts using the repo itself as the textbook. Faster than reading generic docs because every example is from the actual codebase you'll contribute to.

## Prerequisites

- A repo cloned locally
- At least a basic understanding of the project (from `oss-explore-repo` or your own exploration)
- An honest assessment of what you don't know

## Process

### 1. Identify the stack

Inventory the technologies used:

```bash
# Dependencies
cat package.json 2>/dev/null | jq '.dependencies, .devDependencies' 2>/dev/null
(cat requirements.txt 2>/dev/null || cat pyproject.toml 2>/dev/null) | head -40
cat go.mod 2>/dev/null | head -20
cat Cargo.toml 2>/dev/null | head -30

# Build and CI tools
ls .github/workflows/ 2>/dev/null
cat Makefile 2>/dev/null | head -20

# Testing
ls test/ tests/ __tests__/ spec/ 2>/dev/null
grep -l "jest\|pytest\|mocha\|vitest\|cargo test\|go test" * .* 2>/dev/null

# Linting and formatting
cat .eslintrc* .prettierrc* pyproject.toml tox.ini setup.cfg 2>/dev/null | head -30
```

Present the full stack categorized:

```
## Stack: {repo}

| Category | Technology |
|----------|-----------|
| Language | {e.g., TypeScript 5.x} |
| Framework | {e.g., Express.js} |
| Testing | {e.g., Vitest + Testing Library} |
| Build | {e.g., Vite} |
| CI | {e.g., GitHub Actions} |
| Linting | {e.g., ESLint + Prettier} |
| Database | {e.g., PostgreSQL via Prisma} |
| Other | {anything else notable} |
```

### 2. Find the user's gaps

Ask targeted questions:

> "Here's the stack this repo uses. For each technology, tell me your comfort level:
> - **Comfortable** - used it in a project
> - **Familiar** - read about it, haven't used it
> - **Unknown** - never used it or only vaguely know what it is
>
> Be honest - I'll focus teaching on the gaps. No judgment."

Process one gap at a time, starting with the most critical for the contribution they plan to make.

### 3. Teach from the codebase

For each identified gap, find real examples in this repo. Do NOT teach from generic docs.

```bash
# Find usage of the technology in the codebase
grep -rn "{framework_import_or_pattern}" src/ lib/ \
  --include="*.ts" --include="*.py" --include="*.go" --include="*.rs" | head -20

# Find the simplest, clearest example
# (pick files that are short, well-named, and demonstrate the concept cleanly)
```

For each concept, present:

```
## {Technology}: {Concept Name}

**What it is**: {2-3 sentence explanation - just enough to read the code}

**How this repo uses it**:
- `src/handlers/auth.ts:15-30` - {what this example demonstrates}
- `src/middleware/validate.ts:8-22` - {what this example demonstrates}

**Walk-through** of `src/handlers/auth.ts:15-30`:
{line-by-line explanation of the key lines - not every line, just the ones that matter}

**Learn more**: {one link to official docs for this specific concept - not the homepage, the specific page}
```

Rules:
- Every example comes from THIS repo, not generic tutorials
- Explain in 2-3 sentences, not paragraphs
- One external link per concept (the specific doc page, not the homepage)
- Walk through the clearest example, skip the complex ones

### 4. Thinking gate - user reads the code

After explaining a concept:

> "Now find one MORE example of {concept} in the codebase that I didn't show you.
> Read it and tell me what it does.
>
> (This checks whether you can recognize the pattern on your own, not just understand my explanation.
> Hint: search for `{relevant import or keyword}` in the codebase.)"

If the user can find and explain an example, they understand the concept. Move to the next gap.

If the user can't find one or explains it wrong:
- Show one more example with a different angle
- Repeat the thinking gate

Don't move on until the user can recognize the pattern independently.

### 5. Connect to the contribution

Once gaps are filled, tie the learning to what the user needs to do:

> "The issue you're working on touches `{area}` which uses `{concept you just learned}`.
> Specifically, look at `{file}:{line}` - that's where your change will interact with {concept}.
> Based on what you just learned, what do you think needs to change there?"

If the user doesn't have a specific issue yet, point to areas where the newly learned technology is most visible and suggest they explore those files on their own.

### 6. Build a reference sheet

The user creates their own quick-reference for while they code.

**Thinking gate:**

> "Write a cheat sheet for yourself - 3-5 bullet points covering the key concepts you just learned, with file references for each.
> This is your reference while you code. Write it in YOUR words, not mine.
>
> Example format:
> - {Concept}: {what it does} - see `{file}:{line}` for an example"

Review their cheat sheet. Flag anything incorrect but don't rewrite it.

### 7. Verify readiness

Quick comprehension check:

> "Without looking at your notes:
> 1. What does `{key concept}` do in this repo?
> 2. If you saw `{pattern}` in a file you haven't read yet, what would you expect it to do?
> 3. Where would you look in the codebase for more examples of `{concept}`?"

If the user can answer all three, they're ready to contribute. If not, revisit the relevant concept.

## Related Skills

- **Triggered from**: ← `oss-prep-to-contribute` - when knowledge check reveals unfamiliar technology
- **Triggered from**: ← `oss-explore-repo` - when exploration reveals the user doesn't understand the stack
- **Next step**: → `oss-contribute` - ready to work on the issue
- **Pairs with**: `oss-explore-repo` (architecture understanding) + this skill (technology understanding) = full preparation

## Anti-patterns

- **DO NOT** teach from generic docs - every example must come from THIS repo's codebase
- **DO NOT** dump all concepts at once - teach one gap at a time, verify understanding, then move on
- **DO NOT** skip the "find another example" gate - recognition matters more than explanation
- **DO NOT** teach more than what's needed for the contribution - the goal is sufficiency, not mastery
- **DO NOT** replace official documentation - point to it for depth, don't reproduce it
- **DO NOT** assume the user knows prerequisite concepts - if they're unknown on React, don't assume they know JSX
