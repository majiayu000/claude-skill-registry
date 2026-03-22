---
name: dk-compound
description: "Capture learnings from the current conversation as a clean, human-readable doc in docs/. Use after solving a non-trivial problem, discovering a design pattern, hitting a gotcha, or making an architectural decision worth remembering. Triggers on: 'document this', 'capture this learning', 'that was tricky', 'let's compound this', or /dk-compound."
argument-hint: "[optional: brief context about what to capture]"
allowed-tools: Bash, Read, Edit, Write, Task, Grep, Glob
---

# /dk-compound — Capture What You Learned

Write a single, clean markdown doc that captures what this conversation figured out — the principle, the gotcha, the pattern, or the fix. No slop, no filler. Every paragraph earns its place.

## What this captures

Two kinds of knowledge, often in the same doc:

1. **Meta-level**: Design principles, architectural decisions, philosophy — the "why" that applies beyond this specific instance
2. **Gotchas**: Concrete traps, error messages, things that broke and how to fix them — the "what" that saves 30 minutes next time

Good docs have both. A design pattern doc should include the concrete code. A bug fix doc should explain the principle it violated.

## When to use

- After solving a non-trivial problem
- After discovering a pattern worth reusing
- After making an architectural decision with trade-offs
- After hitting a gotcha that would bite someone else
- After a debugging session that revealed something non-obvious

Skip it for: typos, trivial config, obvious one-liners.

## Context hint

<context_hint> #$ARGUMENTS </context_hint>

If the context hint above is empty, scan the conversation for the most significant learning — usually the thing that took the most investigation or had the most non-obvious outcome.

## Process

### Step 1: Extract the learning

Spawn a haiku subagent to analyze the conversation and extract the raw material. The subagent returns text data only — it does NOT write any files.

```
Task(model: haiku, subagent_type: general-purpose)

Prompt: "You have access to the full conversation context. Extract the following:

1. TITLE: A clear, specific title (not generic — 'Flex Column Pinning for Modal Footers' not 'UI Fix')
2. CATEGORY: One of: design-patterns, gotchas, debugging, architecture, performance, integration, workflow, tooling
3. WHAT HAPPENED: 2-3 sentences. What was the problem or decision?
4. WHY IT MATTERS: 1-2 sentences. Why would someone care about this in the future?
5. THE INSIGHT: The core learning. Could be a principle, a pattern, a gotcha, or a fix. Be specific.
6. CODE EXAMPLES: If applicable, before/after code or key snippets. Include file paths.
7. PREVENTION/REUSE: How to apply this learning going forward. Concrete, not vague.
8. TAGS: 3-7 lowercase hyphenated keywords for searchability.
9. RELATED FILES: Key files that were involved.
10. COMPONENT: Which part of the system (odin-orchestrator, odin-harness, taskit-backend, taskit-frontend, taskit-models, cost-tracking, testing, tooling, cross-cutting)

Return these as clearly labeled sections. Be specific and concrete — exact error messages, exact file paths, exact code. No filler phrases like 'it's important to note that' or 'this ensures robustness'."
```

### Step 2: Check for existing related docs

Search `docs/` for similar topics:

```bash
Grep: pattern="<keywords from extracted tags>" path=docs/ output_mode=files_with_matches -i=true
```

If a closely related doc exists, decide:
- **Same topic, new angle**: Create new doc with cross-reference
- **Same topic, same angle**: Update existing doc instead of creating new one
- **Tangentially related**: Create new doc, add to Related section

### Step 3: Determine the file path

**Category directories** (mapped from the extracted category):

| Category | Directory |
|----------|-----------|
| design-patterns | `docs/solutions/design-patterns/` |
| gotchas | `docs/solutions/gotchas/` |
| debugging | `docs/solutions/debugging/` |
| architecture | `docs/solutions/architecture/` |
| performance | `docs/solutions/performance-issues/` |
| integration | `docs/solutions/integration-issues/` |
| workflow | `docs/solutions/workflow-issues/` |
| tooling | `docs/solutions/tooling/` |

**Filename**: `<slugified-title>-<YYYYMMDD>.md` if the title is unique enough, or `<slug>-<component>-<YYYYMMDD>.md` if disambiguation helps.

Examples:
- `flex-column-pinning-modal-footers-20260224.md`
- `cost-estimation-token-extraction-all-harnesses.md`
- `cascading-fetch-usecallback-searchparams-taskit-frontend-20260220.md`

### Step 4: Write the doc

Create a single markdown file using the template below. Populate it from the subagent's extracted material. The main conversation writes the file — no subagent writes files.

```bash
mkdir -p docs/solutions/<category>/
```

Then write the file.

## Document template

```markdown
---
title: "<specific descriptive title>"
date: <YYYY-MM-DD>
category: <category>
tags:
  - <tag1>
  - <tag2>
  - <tag3>
component: <component>
severity: <low|medium|high|critical OR design>
status: <implemented|documented|observed>
related:
  - <path/to/related/doc.md>
---

# <Title>

## Problem

[What happened. Concrete: error messages, symptoms, the situation that led here. 2-4 sentences max.]

## Insight

[The core learning. This is the section people will re-read. Could be:]
[- A design principle with rationale]
[- A pattern with when/why to use it]
[- A root cause explanation]
[- An architectural trade-off analysis]

[If there's a principle, state it as a single bold sentence first, then explain.]

## Solution

[What was done. Code examples with file paths. Before/after if applicable.]

```<language>
# file: path/to/file.ext
<code>
```

## Prevention / Reuse

[How to apply this going forward. Concrete checklist or rules, not vague advice.]

- [Specific thing to do or check]
- [Pattern to follow]
- [Signal that this problem is recurring]

## Related

- [Link to related doc or file]
```

### Adapting the template

Not every doc needs every section. Use judgment:

- **Design pattern docs**: Emphasize Insight + Solution with code. Problem can be brief.
- **Gotcha/debugging docs**: Emphasize Problem (exact errors) + Solution (exact fix). Insight explains why.
- **Architecture docs**: Emphasize Insight (trade-offs) + Prevention (decision criteria). Code may be minimal.
- **Performance docs**: Emphasize Problem (metrics) + Solution (before/after benchmarks).

If a section would be empty or forced, skip it. A 3-section doc that's all signal beats a 6-section doc with filler.

### Step 5: Present result

After writing the file, show the user:

```
Done — docs/solutions/<category>/<filename>.md

<2-sentence summary of what was captured>

Next:
1. View the doc
2. Cross-reference with another doc
3. Continue working
```

## Quality bar

Every doc should pass this test: **If someone reads only this doc 3 months from now, can they understand the problem, apply the solution, and know when it's relevant — without reading anything else?**

Signals of a good doc:
- Title tells you what it's about without opening it
- First paragraph of Problem gives you the "should I keep reading?" signal
- Insight section is quotable — you could paste it in a PR review
- Code examples are copy-pasteable
- Tags are searchable — someone grepping `docs/solutions/` for "n-plus-one" or "flex-column" finds it

Signals of a bad doc:
- Generic title ("Fixed a bug", "Updated the code")
- Insight is just "we fixed it by changing X" (that's a Solution, not an Insight)
- No code examples for a code-related learning
- Filler phrases ("It's worth noting that...", "This approach ensures...")
- Prevention section says "be careful" instead of giving concrete checks
