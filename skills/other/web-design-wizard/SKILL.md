---
name: web-design-wizard
description: Use when user wants to explore, compare, or A/B test multiple design styles, visual directions, or mockups for a web page before implementation begins. Triggers on "show me design options", "style exploration", "design comparison", "visual options".
context: fork
allowed-tools: Task, Read, Write, Edit, Bash, AskUserQuestion, Skill, Glob
user-invocable: true
---

# Web Design Wizard

## Overview

Generate multiple distinct design styles for a web page in parallel worktrees, letting the user compare and refine before committing to a direction. Core principle: **explore divergently, then converge on the best option.**

## When to Use

- User wants to explore different design styles for a web page
- User asks for design options, visual direction, or style comparison
- User wants multiple implementations to choose from

**Do NOT use when:**
- User has a specific design already defined → use `saurun:react-tailwind-v4-components` or `frontend-design` directly
- User wants to modify an existing design, not create new ones

### Prerequisites

All skills below must be installed. **If any are missing, stop and inform the user.**

| Skill | Used In | Purpose |
|-------|---------|---------|
| `ui-ux-pro-max` | Phase 2 | Design system generation |
| `superpowers:using-git-worktrees` | Phase 6 | Parallel worktree setup |
| `frontend-design` | Phase 6 | Production-grade implementation |
| `vercel-react-best-practices` | Phase 6 | React optimization |
| `copywriting` | Phase 6 | Copy refinement |
| `nano-banana-pro` | Phase 6 | Image generation — install: `npx skills add intellectronica/agent-skills@nano-banana-pro -g -y` |

## Workflow

```dot
digraph design_wizard {
    "User request" [shape=doublecircle];
    "Discovery" [shape=box];
    "Style Generation" [shape=box];
    "User satisfied?" [shape=diamond];
    "Refinement" [shape=box];
    "Graphics Preference" [shape=box];
    "Project Setup" [shape=box];
    "Parallel Implementation" [shape=box];
    "Parallel Verification" [shape=box];
    "Complete" [shape=doublecircle];

    "User request" -> "Discovery";
    "Discovery" -> "Style Generation";
    "Style Generation" -> "User satisfied?";
    "User satisfied?" -> "Refinement" [label="no"];
    "Refinement" -> "User satisfied?";
    "User satisfied?" -> "Graphics Preference" [label="yes"];
    "Graphics Preference" -> "Project Setup";
    "Project Setup" -> "Parallel Implementation";
    "Parallel Implementation" -> "Parallel Verification";
    "Parallel Verification" -> "Complete";
}
```

## Phase 1: Discovery

Use AskUserQuestion to gather context. **Batch questions** — use up to 4 questions per call. **Infer obvious answers** from context (e.g., a coffee shop is consumer-facing, probably warm mood).

Gather:
1. **Project name** — detect from package.json or git repo name, confirm with user
2. **Page type** — Landing, Portfolio, Blog, E-commerce, SaaS, Documentation
3. **Target audience** — Professionals, Consumers, Developers, Creative industry
4. **Mood/feeling** — Professional, Playful, Luxury, Minimal, Bold, Warm, Futuristic
5. **Content language** — English, Danish, etc.
6. **Style preferences/anti-preferences** — only if not obvious from above

Skip questions where the answer is obvious from the user's request.

## Phase 2: Style Generation

Generate design styles using `ui-ux-pro-max`:

**Default:** 4 styles (user can request different count).

For each style:

1. **Craft diverse keywords** from discovery responses. Combine: page type + audience + mood + unique aesthetic. Ensure variety across all styles.

2. **Generate design system:** Invoke `ui-ux-pro-max` via the `Skill` tool with arguments:
   `"[keywords]" --design-system --persist -p "[ProjectName]" --page "[style-name]"`
   Saves to: `design-system/pages/[style-name].md` in current working directory.

3. **Present to user** with: style name, key colors, typography, mood adjectives, and best use case.

**Track generated styles** to avoid duplicate keywords in refinement rounds.

## Phase 3: Refinement (Iterative)

| User Says | Action |
|-----------|--------|
| "Give me N completely different styles" | Generate N NEW styles with different keywords |
| "Give me N more options" | Generate N NEW (avoid previous keywords) |
| "I like X and Y, give me more like X" | Keep X & Y, generate variations of X |
| "Combine styles X and Y" | Generate 1 new blending those aesthetics |
| "Implement X, Y, Z" or "Implement all" | Move to Phase 4 with selections |

## Phase 4: Graphics Preference

**Before implementation**, ask about graphics for all selected styles at once:

Use AskUserQuestion with options:
- "Lots of graphics for all (hero + accent graphics + illustrations)"
- "Minimal graphics for all (hero image only)"
- "Let the design style determine graphics" (Recommended)
- "I want to choose per style"

Only ask per-style if user picks the last option.

## Phase 5: Project Setup

### Confirm project location

**Suggested:** `designs/[project-name]/` in current working directory.

Ask user to confirm or override.

### Create project

1. `mkdir -p [location]`
2. Write `concept.md` — see [concept-template.md](concept-template.md) for template. Populate from discovery responses. **Only fill fields you have data for — omit sections with no info.**
3. **Do NOT run `git init`** — use the existing repo. Commit project docs to the current branch.

```bash
git add designs/[project-name]/concept.md
git commit -m "docs: initialize [project-name] design exploration"
```

### Project structure

```
[repo-root]/
├── designs/[project-name]/
│   └── concept.md
├── design-system/pages/
│   ├── [style-1].md
│   └── [style-2].md
└── .worktrees/
    ├── [style-1-branch]/    # React + Vite + TypeScript project
    └── [style-2-branch]/
```

## Phase 6: Parallel Implementation

**CRITICAL: Spawn ALL implementation agents in a SINGLE message with multiple Task tool calls.**

For each selected style, spawn one sub-agent. See [implementation-prompt.md](implementation-prompt.md) for the full prompt template. **Replace `[absolute-path-to-repo-root]`** with the actual repo root path so sub-agents can resolve cross-worktree references.

Key points for each sub-agent:
- Use `superpowers:using-git-worktrees` to create worktree at `.worktrees/[style-name]/`
- Create React + Vite + TypeScript project: `npm create vite@latest . -- --template react-ts`
- Read design spec from `design-system/pages/[style-name].md`
- Use `Skill` tool to invoke: `frontend-design`, `vercel-react-best-practices`, `copywriting`, `nano-banana-pro`
- Generate images per graphics preference
- Build with `npm run build` to verify
- Commit all changes

**Wait for ALL agents to complete before Phase 7.**

## Phase 7: Parallel Verification

**CRITICAL: Spawn ALL verification agents in a SINGLE message with multiple Task tool calls.**

For each implementation, spawn one verification sub-agent. See [verification-prompt.md](verification-prompt.md) for the full prompt template. **Assign ports sequentially** (5173, 5174, 5175, ...) and **replace `[absolute-path-to-repo-root]`** with the actual path.

Verification checks:
- Dev server starts without errors
- All URLs/links are valid
- Images exist and are properly referenced
- Design spec adherence (color, typography, layout, effects) — score 1-10
- Production build succeeds

**After all complete**, show comparison summary:

```
Style 1: [Name] — ✅ All passed — Design: 8.5/10
Style 2: [Name] — ⚠️ 2 broken URLs — Design: 9.0/10
Style 3: [Name] — ❌ Build failed — See report
```

Recommend best-performing style based on results.

## Quick Reference

| Phase | Action | Key Tool |
|-------|--------|----------|
| 1. Discovery | Gather context via AskUserQuestion (batch up to 4) | AskUserQuestion |
| 2. Style Generation | Generate 4 design systems via ui-ux-pro-max | Skill |
| 3. Refinement | Iterate until user selects styles | AskUserQuestion |
| 4. Graphics | Ask graphics preference for selected styles | AskUserQuestion |
| 5. Project Setup | Create concept.md, commit scaffolding | Write, Bash |
| 6. Implementation | Spawn parallel sub-agents per style | Task |
| 7. Verification | Spawn parallel verification agents, show comparison | Task |

## Common Mistakes

- **Regenerating design specs in sub-agents** — design specs are created in Phase 2. Sub-agents READ them, never re-invoke ui-ux-pro-max.
- **Sequential sub-agent spawning** — Phase 6 and 7 MUST spawn ALL agents in a single message with multiple Task calls. Never one-at-a-time.
- **Skipping Graphics Preference** — always ask before implementation. Don't assume.
- **Using `git add .` in worktrees** — stage specific paths only to avoid committing node_modules, .env, or OS files.
- **Identical keywords across styles** — track used keywords to ensure diversity. Duplicate keywords produce duplicate designs.

## Error Handling

| Error | Recovery |
|-------|----------|
| `ui-ux-pro-max` script fails | Retry with simpler keywords. If persistent, create design system manually from the style keywords. |
| All styles rejected | Ask user for specific direction: "What did you dislike? Colors? Layout? Overall feel?" |
| Sub-agent skill not found | The agent should use `Skill` tool to invoke. If skill genuinely missing, skip that enhancement step and note it. |
| Implementation build fails | Fix in worktree, re-run build. Report issue if unfixable. |
