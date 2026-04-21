---
name: idea-explorer
description: Collaborative exploration to refine ideas into clear requirements before spec writing. Explores user intent, requirements and design through iterative dialogue.
argument-hint: [topic] [--depth=<quick|normal|thorough>] [--output=<path>]
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(git diff:*)
  - Bash(git status:*)
  - Bash(git log:*)
  - Bash(ls *)
  - Bash(mkdir:*)
  - Write
---

# Idea Explorer

Explore, understand and refine ideas ready to be turned into designs and specs.

## Overview

Through collaboration, help turn ideas into better understood initiatives and goals that can be used by the spec-orchestrator or spec-writer skill to create detailed specifications and implementation plans.

Start by understanding the current project context, then ask questions one at a time to refine the idea. Once you understand what you're building, present the approach and understanding as a succinct summary (200-500 words), checking after each section whether it looks right so far.

## Arguments

- `topic` (positional): The idea or topic to explore
- `--depth=<quick|normal|thorough>`: How deep to explore (default: normal)
  - `quick`: Minimal questions, faster to refined idea
  - `normal`: Balanced exploration
  - `thorough`: Deep dive with more alternatives explored
- `--output=<path>`: Write the refined idea to a file

## Configuration

Check for `.claude/spec-workflow/config.yaml` in the project. If present, use configured paths:

```yaml
paths:
  specs: "./specs" # Where to save output if --output not specified
```

If no config exists, default to `./specs/`.

### Project DNA

If `.claude/spec-workflow/PROJECT.md` exists, read it **before asking any questions**.
This file contains permanent project context: stack, architecture rules, code conventions,
known constraints, and what "done" means for this project.

When PROJECT.md is present:

- Inject Architecture Rules into your exploration questions
- Reference known constraints when evaluating feasibility
- Use "Out of Scope" section to apply YAGNI ruthlessly
- Frame questions in terms of the actual stack (e.g., "This project uses Firestore — should the new entity follow the soft-delete pattern already in use?")

If PROJECT.md does **not** exist, offer to generate it:

```
⚠️ No PROJECT.md found at .claude/spec-workflow/PROJECT.md
   This file enriches all spec phases with permanent project context.
   Generate one now? [Yes — analyze codebase and ask a few questions] [Skip for now] [I'll create it manually]
```

If user says yes: analyze `package.json` / `Cargo.toml` / `Package.swift` / `go.mod`, read `CLAUDE.md` if present, then ask 4-6 targeted questions to populate the template. Save to `.claude/spec-workflow/PROJECT.md`.

### Philosophy Injection

If `.claude/spec-workflow/philosophy/exploration.md` exists, read it and incorporate its guidance into your exploration process. This file contains the user's philosophy about what makes exploration complete, what questions to always ask, and what red flags to surface.

## The Process

**0. Context Gathering (automatic, before any questions):**

Before asking the user anything, gather codebase context:

**Derive `{slug}`** from the feature topic using the same rule as `context-gatherer`:
lowercase → strip punctuation → drop stop words (`a an the to for of in with from and or but is are was`) → first 6 significant words → join with hyphens → max 60 chars.

1. Parse the feature topic/prompt for key terms (entities, actions, domain words)
2. Use the **Grep tool** (not bash grep) per term — `output_mode: "files_with_matches"`, `-i`, glob `*.{ts,tsx,js,swift,rs,py,go}` — find the **5–10 most relevant files**
3. Read project context files: `CLAUDE.md`, `.claude/spec-workflow/PROJECT.md`, `README.md`, stack config
4. Identify existing patterns, similar features, and related entities already in the codebase
5. If `.claude/feature-state/{slug}/context.md` already exists, **load it** (skip re-scan); otherwise run `mkdir -p .claude/feature-state/{slug}` then write it with the Write tool
6. Show a brief summary before the first question:
   ```
   📂 Context gathered — 7 related files found.
      Existing: Student entity (src/types/student.ts), Trainer entity, checkout Cloud Function.
      Patterns: MVVM + Firebase Auth + Firestore (soft delete).
      Injecting codebase context into exploration...
   ```

Context gathering is best-effort — partial results are fine. Never block on it.

**0.2. Prompt Enrichment (automatic, after context gathering):**

After saving `context.md`, run the **prompt-enricher** phase to ground the raw prompt in discovered constraints:

1. Read `context.md` from the state directory
2. Detect architectural, data, infrastructure, and dependency constraints relevant to the feature
3. Identify ambiguities (decisions with multiple valid interpretations)
4. Auto-suggest edge cases based on feature type keywords detected in the prompt:
   - connect/link/assign → connection/relationship edge cases
   - login/auth/token → auth/permissions edge cases
   - list/search/filter → list/query edge cases
   - create/add/submit → form/input edge cases
   - stripe/payment/checkout → payment edge cases
   - delete/remove/archive → delete/remove edge cases
   - notify/push/email → notification edge cases
   - webhook/API/external → external integration edge cases
5. Suggest scope boundaries (In Scope / Likely Out of Scope YAGNI / Deferred)
6. If `.claude/feature-state/{slug}/enriched-prompt.md` already exists, **load it** (skip re-enrichment); otherwise write it with the Write tool (directory already created in step 0.5 above)

Use the enriched prompt as the **starting brief** for the first question:

```
Based on what I found in the codebase, here's what we're working with:

**Constraints discovered:**
- [Key constraint from context.md]
- [Key constraint from context.md]

**Ambiguities to resolve:**
- [First ambiguity]

**Suggested scope:**
- In scope: [inferred from prompt + context]
- Likely out of scope (YAGNI): [things not essential for v1]

My first question: [first question anchored in the ambiguities above]
```

Prompt enrichment is best-effort — skip silently if context.md is empty or prompt is too vague.

**1. Understand the context:**

Check out the current project state first by reading the repository contents, docs, recent commits.
Use the context.md from step 0 as the primary source — avoid re-reading files already scanned.

**2. Understanding the idea and develop the intention, problem space and opportunity:**

This purpose of this step is to narrow down and clarify the idea, its purpose, constraints and success criteria.

- Ask questions one at a time to refine the idea
- **Anchor questions in the actual codebase**: reference real files, entities, and patterns found in context.md
  - ❌ Generic: "How should the student connect to the trainer?"
  - ✅ Grounded: "I found `handleCheckoutComplete` which already creates a trainer-student link via Stripe. Should this new feature use that existing mechanism or create a separate direct-connect flow?"
- Prefer multiple choice questions when possible, but open-ended is fine too
- Only one question per message - if a topic needs more exploration, break it into multiple questions
- Where possible, provide 2-4 options to choose from
- Evaluate the options yourself before presenting them and provide a recommendation with reasoning
- Focus on understanding: problem to be solved, constraints, success criteria and the minimum viable solution
- Avoid feature creep - ruthlessly apply YAGNI (You Ain't Gonna Need It) to remove unnecessary features

Adjust depth based on `--depth` argument:

- `quick`: 2-3 key questions only
- `normal`: 4-6 questions covering core aspects
- `thorough`: 8+ questions, explore more alternatives

**3. High level solutionizing:**

Think deeply about the discussion that's been had so far and propose a high level approach to solving the problem.

- Propose 2-4 different approaches with trade-offs
- Present options conversationally with your recommendation and reasoning
- Lead with your recommended option and explain why

**4. Presenting the refined idea:**

Now that you understand the idea, problem, success criteria and what we're building, present the agreed design.

- Break it into sections of 100-200 words
- Ask after each section whether it looks right so far
- Key areas to cover are: architecture, components, data flow, error handling, testing
- Be ready to go back and clarify if something doesn't make sense

## After the Design

**Saving the output:**

If `--output` was specified, write the refined idea to that path.

**Handing over to the next stage:**

Ask the user if they'd like to hand this idea discovery to the spec-orchestrator skill to formalize as a spec. If they prefer to skip the review cycle, they can use spec-writer directly.

## Key Principles

- **One question at a time** - Don't overwhelm with multiple questions
- **Multiple choice preferred** - Easier to answer than open-ended when possible
- **YAGNI ruthlessly** - Remove unnecessary features from all designs
- **Explore alternatives** - Always propose 2-4 approaches before settling
- **Incremental validation** - Present design in sections, validate each
- **Be flexible** - Go back and clarify when something doesn't make sense
