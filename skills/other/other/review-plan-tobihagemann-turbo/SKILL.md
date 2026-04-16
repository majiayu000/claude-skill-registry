---
name: review-plan
description: "Review a planning artifact (plan, shells, or spec) by running internal and peer reviews in parallel and returning combined findings. Use when the user asks to \"review my plan\", \"review my shells\", \"review my spec\", \"check my plan\", \"check my shells\", \"check my spec\", \"critique my plan\", \"critique my shells\", \"critique my spec\", or wants feedback on a planning artifact."
---

# Review Plan

Review a planning artifact against type-specific criteria. Runs internal review and `/peer-review` in parallel by default. Returns combined structured findings.

## Step 1: Determine Artifact Type and Resolve

### Determine Artifact Type

1. **Explicit argument** — If the user specified a type (e.g., "review shells", "review spec"), use it. No argument defaults to **plan**.
2. **Conversation context** — If artifact text or a path is already in context, infer the type.
3. **Auto-detect** — Check `.turbo/` for existing artifacts. If multiple types exist, pick the one with the most recently modified file.

### Resolve the Artifact

#### Plan (default)

1. **Plan text in conversation** — use it
2. **Explicit path** — read it
3. **Explicit slug** — resolve to `.turbo/plans/<slug>.md`
4. **Single file** — Glob `.turbo/plans/*.md`. If exactly one file exists, use it
5. **Most recent** — most recently modified file
6. **Legacy fallback** — `.turbo/plan.md` if `.turbo/plans/` does not exist
7. **Nothing found** — stop and state that no artifact was found to review

#### Shells

1. **Shell text in conversation** — use it
2. **Explicit spec slug** — Glob `.turbo/shells/<slug>-*.md`
3. **Explicit spec path** — derive slug from filename, glob as above
4. **Single spec** — Glob `.turbo/specs/*.md`. If exactly one, derive slug and glob for shells
5. **Most recent spec** — most recently modified spec, derive slug and glob
6. **Nothing found** — stop and state that no artifact was found to review

For shells, read each shell file and parse its YAML frontmatter (`spec`, `depends_on`). Read the source spec from the `spec` field.

#### Spec

1. **Spec text in conversation** — use it
2. **Explicit path** — read it
3. **Explicit slug** — resolve to `.turbo/specs/<slug>.md`
4. **Single file** — Glob `.turbo/specs/*.md`. If exactly one, use it
5. **Most recent** — most recently modified
6. **Legacy fallback** — `.turbo/spec.md` if `.turbo/specs/` does not exist
7. **Nothing found** — stop and state that no artifact was found to review

If multiple candidates exist, pick the most recently modified.

## Step 2: Run Reviews in Parallel

Read the reference file for the resolved type:

- **Plan** — [references/plan-review.md](references/plan-review.md)
- **Shells** — [references/shells-review.md](references/shells-review.md)
- **Spec** — [references/spec-review.md](references/spec-review.md)

Skip peer review when the caller asked (e.g., "without peer review", "no peer", "internal only"). For shells, the internal review focuses on structural wiring and skips the project context read.

Use the Agent tool to launch all agents below in a single message (`model: "opus"`, do not set `run_in_background`) so they run concurrently:

- **Internal Agent:** Pass the artifact text and the reference file's content; the subagent reads project context (CLAUDE.md, relevant codebase files) before applying criteria, then returns findings in the output format below.
- **Peer review Agent (unless skipping):** Instruct the subagent to invoke `/peer-review` via the Skill tool with a request describing: (a) the artifact under review; (b) the criteria live in `~/.claude/skills/review-plan/references/<type>-review.md` for the resolved type from Step 1 — the reviewer should read that file directly and use its priority scale; (c) the Overall Verdict should use the `Readiness: <ready | needs revision>` label.

Aggregate findings with attribution (reviewer: "internal" or "peer"). Present them in the output format below.

Check your task list for remaining tasks and proceed.

## Output Format

Return findings as a numbered list. For each finding:

```
### [P<N>] <title (imperative, ≤80 chars)>

**Section:** <plan section, shell number(s), or spec section>
**Reviewer:** <internal | peer>

<one paragraph explaining the issue and its impact>
```

After all findings, add:

```
## Overall Verdict

**Readiness:** <ready | needs revision>

<1-3 sentence assessment>
```

If there are no qualifying findings, state so and explain briefly.

## Rules

- Present findings grouped by priority.
