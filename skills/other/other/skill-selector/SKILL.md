---
name: skill-selector
description: Analyze an implementation plan (defaults to .flow/specs/), discover relevant skills from the ecosystem, install them, and rewrite the plan to leverage installed skills. Use when user has a build plan, flow-next epic spec, or feature request and wants to equip the agent with the best available skills before building. Triggers on 'select skills for', 'equip for plan', 'find skills for this plan', 'skill up', or when reviewing a plan file before implementation.
---

# Skill Selector

Analyze a plan, discover skills that close expertise gaps, install them, and rewrite the plan to leverage what's now available.

## Thinking Framework

Before searching for anything, ask yourself:

1. **Where would a generalist fail?** Identify the plan steps where generic knowledge produces mediocre output. A CRUD API needs no skill. A SvelteKit app with runes reactivity, server-side data flow, and Tailwind v4 theming — that's three domains where expert skills prevent hours of debugging.

2. **What's the expertise surface area?** Count distinct technology/domain boundaries. Each boundary is a potential skill gap. A plan touching "SvelteKit + Tailwind + D3 + PostgreSQL" has 4 boundaries. Search for each.

3. **What would the expert do differently?** For each plan step, ask: "Would a domain expert approach this the same way a generalist would?" If yes, no skill needed. If no, that's where a skill earns its tokens.

## Workflow

### Phase 1: Extract Expertise Domains

Locate and read the plan:

1. **If `$ARGUMENTS` is a file path** — read that file directly
2. **If `$ARGUMENTS` is a flow ID** (e.g., `fn-1`, `fn-2`) — look for matching spec in `.flow/specs/`
3. **If `$ARGUMENTS` is empty or a description** — scan `.flow/specs/` for the most recent spec file and present it to the user for confirmation. If no specs exist, ask the user what they're building.

```bash
# Default: check .flow/specs/ for available plans
ls -lt .flow/specs/*.md 2>/dev/null
```

The `.flow/specs/` directory is where flow-next stores its epic and task specs. These specs contain architecture overviews, tech stacks, and implementation details — exactly what this skill needs to extract domains from.

Identify the **expertise boundaries** — the specific domains where specialized knowledge changes the outcome:

| Category | What to Extract | Why It Matters |
|---|---|---|
| **Frameworks** | SvelteKit, Next.js, Rails, etc. | Framework-specific skills encode idioms, gotchas, and patterns that differ from generic language knowledge |
| **Styling systems** | Tailwind v4, CSS-in-JS, design tokens | Version-specific configuration and conventions change rapidly |
| **Data patterns** | ORMs, query builders, data viz libraries | Schema design, query patterns, and visualization idioms are deep domains |
| **Quality dimensions** | Testing strategy, a11y, performance | These are most often skipped without explicit skill guidance |

**Present the domain map to the user before proceeding.** This catches misunderstandings early.

### Phase 2: Discover Skills

#### Check installed skills first

```bash
npx skills list
```

Map installed skills to plan domains. Already-installed skills don't need installation but DO need to inform the plan rewrite.

#### Search the ecosystem for gaps

For each uncovered domain, search using `npx skills find`:

```bash
npx skills find [specific-technology]
```

**Search heuristics that matter:**

- **Use the specific name first, then broaden.** `sveltekit` before `svelte` before `frontend`. The ecosystem uses inconsistent naming — `svelte5-best-practices` vs `svelte-code-writer` vs `sveltekit-structure` are all real skills with different scopes.
- **Search 3-8 times** depending on domain count. One search per expertise boundary, minimum.
- **Read the install counts.** Skills with >100 installs have community validation. Skills with <10 are untested. Weight recommendations accordingly.
- **Watch for skill families.** Some repos bundle multiple related skills (e.g., `spences10/svelte-skills-kit` has runes, data-flow, structure, and remote-functions). Installing the whole family is often better than cherry-picking.
- **NEVER search generic terms** like `code`, `web`, `app`, or `best practices`. These return noise. Be specific: `tailwind v4`, `playwright testing`, `d3 visualization`.

**When `npx skills find` returns 0 results**: Try alternate terminology. If `database schema` returns nothing, try `prisma` or `postgres` or `sql`. If still nothing, that domain has no ecosystem skill — note it as a gap and move on.

**When `npx skills find` errors or hangs**: The registry may be unreachable. Fall back to checking if the user has skills in `~/.agents/skills/` or `~/.claude/skills/` that match. Use `ls` to inspect.

### Phase 3: Evaluate, Recommend, and Install

This is where most agents get it wrong. Finding skills is easy. **Choosing the right ones is the expert move.**

#### Evaluating skill quality from search results

You can't read a skill's SKILL.md before installing it. So evaluate from signals:

| Signal | Good | Bad |
|---|---|---|
| **Install count** | >100 installs = community-tested | <10 installs = experimental |
| **Source repo** | Official org (`sveltejs/`, `vercel-labs/`) | Unknown single-user repo |
| **Skill name** | Specific (`svelte-runes`, `tailwind-v4-shadcn`) | Vague (`best-practices`, `helper`) |
| **Skill family** | Part of a curated collection | Standalone with no related skills |

#### The context budget rule

**NEVER recommend more than 5-7 skills for a single plan.** Each installed skill consumes context window when activated during implementation. Loading 12 skills simultaneously degrades agent performance — the agent starts ignoring some skills because context is saturated.

Prioritize: Which 5 skills would an expert consider non-negotiable for this tech stack?

#### Present the recommendation

```markdown
## Skill Recommendations for: [Plan Name]

### Already Installed (will leverage)
- `skill-name` → [which plan steps benefit]

### Recommended to Install
| Priority | Skill | Source | Why | Install Count |
|----------|-------|--------|-----|---------------|
| 1 | ... | owner/repo@skill | Covers [domain gap] | N installs |
| 2 | ... | ... | ... | ... |

### Considered but Skipped
- `skill-name` → [why: too generic / overlaps with X / low install count]
```

Use `AskUserQuestion` to confirm. After confirmation, install each:

```bash
npx skills add <owner/repo@skill> -y
```

**Install to project scope** (no `-g` flag). Project skills stay contained and won't pollute other projects. Mention the user can add `-g` if they want global availability.

If an install fails, report the error and continue with the rest. A failed install is not a blocker.

### Phase 4: Rewrite the Plan

**This is where the skill pays for itself.** A plan that doesn't reference its available skills is a plan that won't use them.

**MANDATORY**: Read each newly installed skill's SKILL.md before rewriting. You need to understand:
- What conventions does this skill prescribe?
- What anti-patterns does this skill warn about?
- What specific commands, patterns, or approaches does it recommend?

Then rewrite the plan:

1. **Annotate each step with relevant skills.** Format: `**Skills**: \`skill-a\`, \`skill-b\``
2. **Adopt skill conventions into the plan.** If `svelte-runes` says "use `$state` not `let`", the plan should specify that.
3. **Remove generic guidance now covered by skills.** "Set up Tailwind" becomes "Set up Tailwind (follow `tailwind-v4-shadcn` skill)" — the skill has the details, the plan doesn't need to repeat them.
4. **Add skill-triggered quality gates.** If a testing skill is installed, add a testing step that explicitly invokes it.
5. **Sequence skill activation.** Framework skills activate first (project setup), then domain skills (feature implementation), then quality skills (testing/review).

**The rewritten plan should be SHORTER than the original** — skills absorb detail that the plan previously had to spell out. If your rewrite is longer, you're duplicating what the skills already provide.

Present the rewritten plan. If the original was a file, offer to update it in place.

## NEVER Do

- **NEVER install without user confirmation** — always present the recommendation table first
- **NEVER install globally by default** — project scope prevents cross-project pollution
- **NEVER recommend >7 skills** — context budget overflow degrades implementation quality
- **NEVER trust skill names alone** — `best-practices` could be anything; evaluate the source repo and install count
- **NEVER skip reading installed skills before rewriting** — referencing a skill you haven't read produces wrong guidance
- **NEVER make the rewritten plan longer** — skills absorb detail; the plan should shrink
- **NEVER search generic terms** like `code`, `web`, `app` — they return unusable noise
- **NEVER rely on a single search query per domain** — skill naming is inconsistent; try alternate terms

## Edge Cases

**No relevant skills found for any domain**: The plan proceeds as-is. Note which domains lacked skills — the user may want to create custom skills after building, capturing the patterns they discover.

**Plan is too vague**: Don't guess. Check `.flow/specs/` first — there may be a detailed spec the user forgot to mention. If nothing there, ask: "What's the tech stack? What are the 3-4 main implementation steps?"

**Conflicting skills for the same domain**: Present both with their differences. Two React skills might differ in scope (one covers hooks patterns, another covers server components). They may complement rather than conflict. Let the user decide.

**Everything is already installed**: Skip directly to Phase 4. The plan rewrite is valuable even when no new skills are installed — the user may not realize which of their installed skills apply.

**`npx skills` not available**: Fall back to manually checking `~/.claude/skills/` and `~/.agents/skills/` for installed skills. Skip ecosystem search and focus on leveraging what's already there. Suggest the user install the skills CLI: `npm install -g skills`.
