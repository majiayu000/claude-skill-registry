---
name: oss-explore-repo
description: |
  Guided codebase exploration for understanding a repo's architecture, patterns,
  and domain language before contributing. Not issue-specific. builds general
  understanding. Use when exploring a new repo, wanting to understand how a
  project works, or preparing to become a regular contributor.
---

# Explore Repo

Explore a codebase the way experienced contributors do. by understanding the architecture, the patterns, and the domain language before touching anything.

## Purpose

Different from `oss-prep-to-contribute` (which is issue-specific and focused on one code path). This skill is for building broad understanding of a repo. Useful when a contributor wants to become a regular contributor rather than make a single drive-by PR. Also useful for GSoC candidates who need to demonstrate deep project understanding in their proposals.

## Prerequisites

- A repo cloned locally
- `gh` CLI authenticated
- A reason to explore (casual learning, planning to contribute, GSoC proposal, evaluating the project)

## Process

### 1. Understand the contributor's goal

Before exploring anything, ask:

- "Why are you exploring this repo? (Casual learning / planning to contribute regularly / GSoC proposal / evaluating whether to use it)"
- "How much time do you want to spend? (Quick overview / deep dive)"

This shapes the depth. A GSoC candidate needs deep understanding. Someone evaluating a library needs a quick architecture scan.

### 2. Map the project from the outside in

Start with what the project DOES, not what the code looks like. Read:

```bash
# Project identity
cat README.md
cat docs/index.md 2>/dev/null || cat docs/README.md 2>/dev/null

# What problem does it solve?
gh api repos/{owner}/{repo} --jq '{description, homepage, topics, language, stargazers_count, open_issues_count}'
```

The user should be able to explain what the project does to a non-technical person before reading a single source file.

**Thinking gate:**

> "Explain what this project does in one sentence. Who uses it? What problem does it solve?
> Don't use the README's words. rephrase it as if you're explaining to a friend who doesn't code."

If the user can't do this clearly, they need to read more docs before touching code.

### 3. Understand the architecture

Use Explore agents to map:

```bash
# Directory layout
ls -la
ls src/ lib/ app/ 2>/dev/null
ls -la */

# Entry points
cat package.json 2>/dev/null | jq '.main, .bin, .scripts'
cat setup.py 2>/dev/null || cat pyproject.toml 2>/dev/null
cat Makefile 2>/dev/null | head -30
cat Cargo.toml 2>/dev/null | head -30

# Key abstractions
grep -rn "class \|interface \|trait \|type \|struct " src/ lib/ \
  --include="*.ts" --include="*.py" --include="*.go" --include="*.rs" --include="*.java" | head -40
```

Present a structured architecture summary:
- Entry points and their flow
- Module boundaries (what talks to what)
- Key abstractions (interfaces, base classes, core types)
- Data flow: how information moves through the system
- Build system and dependency structure

### 4. Learn the domain language

Every codebase has its own vocabulary. Find the terms that appear everywhere:

```bash
# Domain-specific terms in variable/function/class names
grep -rn "class \|def \|function \|fn \|func " src/ lib/ --include="*.ts" --include="*.py" --include="*.go" --include="*.rs" | \
  grep -oP '(class|def|function|fn|func)\s+\w+' | sort | uniq -c | sort -rn | head -20

# Comments that define domain concepts
grep -rn "// \|# \|/// \|/\*\*" src/ lib/ --include="*.ts" --include="*.py" --include="*.go" --include="*.rs" | grep -i "represents\|defines\|a .* is\|means" | head -15

# Glossary in docs (if it exists)
find docs/ -name "*glossary*" -o -name "*terminology*" -o -name "*concepts*" 2>/dev/null
```

Present terms the contributor must understand to read the code fluently. Group by importance. which terms appear in nearly every file vs which are module-specific.

**Thinking gate:**

> "Pick 3 domain terms from the list above. Define each in your own words. Then find one place in the codebase where each is used.
> (This checks whether you can read the code, not just the summary I gave you.)"

### 5. Identify patterns and conventions

What patterns does this codebase follow? Investigate:

```bash
# Error handling approach
grep -rn "try\|catch\|except\|Error\|Result\|unwrap\|panic" src/ lib/ --include="*.ts" --include="*.py" --include="*.go" --include="*.rs" | head -20

# Testing patterns
ls test/ tests/ __tests__/ spec/ 2>/dev/null
cat test/*.{ts,py,go,rs} 2>/dev/null | head -40

# How new features get added - look at recent PRs
gh pr list -R {owner}/{repo} --state merged --limit 5 \
  --json title,changedFiles,additions,deletions \
  --jq '.[] | {title, files: .changedFiles, adds: .additions, dels: .deletions}'
```

Identify:
- Error handling approach (exceptions? Result types? error codes?)
- Testing patterns (unit vs integration vs e2e, mocking strategy, test file naming)
- Dependency injection or service registration
- Configuration management
- Logging conventions
- How new features get added (is there a pattern to follow?)

**Thinking gate:**

> "If you were adding a new feature to this repo, describe the steps. which files would you create, what patterns would you follow, where would you add tests?
> Don't worry about getting it right. I'll tell you what you missed."

Review the user's answer. Point out conventions they missed without giving the full answer.

### 6. Read recent history

What's actively being worked on?

```bash
# Recent merged PRs - what areas are changing?
gh pr list -R {owner}/{repo} --state merged --limit 10 \
  --json title,mergedAt,changedFiles --jq '.[] | {title, merged: .mergedAt, files: .changedFiles}'

# Open issues with most activity
gh issue list -R {owner}/{repo} --state open --sort comments --limit 10 \
  --json number,title,comments --jq '.[] | {number, title, comments}'

# Recent releases
gh release list -R {owner}/{repo} --limit 5

# Changelog
cat CHANGELOG.md 2>/dev/null | head -50
```

Present:
- Areas actively being developed vs areas in maintenance mode
- Topics generating the most discussion
- Release cadence (weekly? monthly? sporadic?)
- Where a new contributor's effort would be most valued

### 7. Identify knowledge gaps

Based on the exploration, what does the contributor still not understand?

- List areas that were unclear during steps 3-6
- Point to specific files or modules that need deeper reading
- Suggest which area to explore next based on their goal (step 1)

If the repo uses technologies the user isn't familiar with, suggest → `oss-learn-stack`.

### 8. Create a personal map

The user writes their own architecture summary. Not a copy of the LLM's summary from step 3. Their own version in their own words.

**Thinking gate:**

> "Write a 5-10 line summary of this repo's architecture. Include:
> - What it does (one sentence)
> - How it's structured (main modules and their roles)
> - The main patterns (error handling, testing, config)
> - One thing that surprised you
>
> This is YOUR mental model. It doesn't need to be perfect. it needs to be yours."

Review their summary. Flag anything incorrect but don't rewrite it.

## Related Skills

- **Next step (found an issue)**: → `oss-find-issue`: find an issue that matches your new understanding
- **Next step (find your own)**: → `oss-find-real-issues`: use your understanding to find real code problems
- **If tech gaps surfaced**: → `oss-learn-stack`: learn unfamiliar technologies from the repo itself
- **Issue-specific prep**: → `oss-prep-to-contribute`: once you have an issue, prepare specifically for it

## Anti-patterns

- **DO NOT** dump the entire codebase structure. guide the user through it layer by layer
- **DO NOT** skip the domain language step. code fluency requires vocabulary
- **DO NOT** treat this as a replacement for reading code. the user must read actual files, not just summaries
- **DO NOT** confuse this with `oss-prep-to-contribute`. this is general exploration, not issue-specific preparation
- **DO NOT** rush through thinking gates. the user's ability to explain the architecture in their own words IS the outcome
