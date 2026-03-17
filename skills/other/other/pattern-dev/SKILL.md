---
name: pattern-dev
description: Guide for developing CommonTools patterns (TypeScript modules that define reactive data transformations with UI). Use this skill when creating patterns, modifying existing patterns, or working with the pattern framework. Triggers include requests like "build a pattern", "fix this pattern error", "deploy this piece/patch", or questions about handlers and reactive patterns.
---

Use `Skill("ct")` for ct CLI documentation when running commands.

You and the user are a team finding the efficient path to their vision.

## Always Plan First

Use `EnterPlanMode` before building. **Scale the plan to the task:**

**Simple pattern** (todo list, counter):
- One file, types + handlers + UI together
- Minimal clarification needed
- Plan in 2-3 sentences

**Medium pattern** (form with validation, data viewer):
- Maybe split schemas if types get complex
- Clarify data shape and key actions
- Plan in a short list

**Complex pattern** (multi-entity system, integrations):
- Consider sub-patterns if genuinely distinct concepts
- Clarify entities, relationships, actions upfront
- Plan with structure, but don't over-specify

**Always start simple.** One file first. Split when it helps, not before.

## Pattern Structure

**Start simple:**
```
packages/patterns/[name]/
└── main.tsx           # Everything in one file to start
```

**Split when it helps** (not before):
```
packages/patterns/[name]/
├── schemas.tsx        # Types, if complex
├── main.tsx           # Main pattern
└── [other].tsx        # Extract when reuse is clear
```

Don't create separate files for every entity. A `Project` with `Task[]` can live in one file until complexity demands otherwise.

## Development Approach: Sketch → Run → Iterate

**Don't write finished code.** Write the minimum to see something work:

1. **Sketch** — Types, one handler, minimal UI. Just enough to render.
2. **Run it** — `deno task ct check main.tsx` and see what happens.
3. **Verify** — Does it render? Does the handler fire? Check console.
4. **Iterate** — Add the next piece, run again.

Each iteration should be deployable. If you can't run it, you've written too much.

## Verification

**Run the code, not just tests.** The primary verification is: does it work when you run it?

- `deno task ct check main.tsx` — See it render, click things, check console
- Tests for state logic that's hard to verify by clicking
- Don't write tests for obvious behavior or code that's still evolving

Pattern tests when needed: `deno task ct test [file].test.tsx`

## Delegate to Agents

### pattern-maker — Write Code

For implementing pattern code:
```
Task({
  prompt: "Implement [feature]. Keep it simple, one file.",
  subagent_type: "pattern-maker"
})
```

### pattern-user — Deploy & Debug

For deploying and testing with ct CLI:
```
Task({
  prompt: "Deploy and test [pattern].",
  subagent_type: "pattern-user"
})
```

### pattern-critic — Review (when needed)

For checking violations before release or when stuck:
```
Task({
  prompt: "Review [file] for violations.",
  subagent_type: "pattern-critic"
})
```

## Workflow

**Not phases, just common sense:**

1. **Build** — Use pattern-maker to sketch and iterate locally (`ct check`)
2. **Review** — Use pattern-critic before deploying to catch common mistakes
3. **Deploy** — Use pattern-user to deploy to toolshed
4. **Fix what's broken** — Iterate with maker, re-review, redeploy
5. **Commit** — At milestones, offer to commit

**Always run pattern-critic before first deploy.** It's fast (uses haiku) and catches mistakes that cause runtime errors. Skip only for tiny fixes where you're confident.

## Documentation

Start with `docs/common/patterns/`—especially `docs/common/patterns/meta/` which contains generalizable idioms that grow over time.

Prefer docs over existing patterns in `packages/patterns/`—docs contain validated snippets while existing patterns may be outdated. Use `packages/patterns/` as reference but don't copy blindly.

Phase skills consult as needed:
- Types: `docs/common/concepts/types-and-schemas/`
- Actions/handlers: `docs/common/concepts/action.md`, `docs/common/concepts/handler.md`
- Testing: `docs/common/workflows/pattern-testing.md`
- Components: `docs/common/components/COMPONENTS.md`
- Debugging: `docs/development/debugging/`
