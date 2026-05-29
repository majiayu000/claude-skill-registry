---
name: review-plan-shells
description: "Review plan shells against their source spec: launches an internal shell review and `/peer-review` in parallel and returns combined findings. Use when the user asks to \"review my plan shells\", \"review my shells\", \"check my plan shells\", \"critique my shells\", or wants shell feedback before implementation."
---

# Review Plan Shells

Run two AI shell reviews in parallel and return combined findings.

## Step 1: Identify the Plan Shells

Determine which shells to review using these rules in order:

1. **Shell text in conversation** — If full shell text is already in context, use it
2. **Explicit spec slug** — If a spec slug was provided, glob `.turbo/plans/<slug>-*.md` and filter to files whose YAML frontmatter has `type: shell`
3. **Explicit spec path** — If a spec path was provided, derive the slug from the filename and glob as above
4. **Single spec** — Glob `.turbo/specs/*.md`. If exactly one spec exists, derive its slug and glob for shells
5. **Most recent spec** — If multiple specs exist, use the most recently modified. Derive its slug and glob for shells
6. **Nothing found** — If no shells exist, say so and stop

Read each shell file and parse its YAML frontmatter (`type`, `status`, `spec`, `depends_on`). Read the source spec from the `spec` frontmatter field.

## Step 2: Run Two Reviews in Parallel

Launch two Agent tool calls in a single message so they run concurrently (`model: "opus"`, do not set `run_in_background`):

### Internal Shell Review

Spawn a subagent with every shell's full text and the source spec. Instruct it to:

1. Apply the shell review dimensions below
2. Return findings in the output format below

### Run `/peer-review` Skill

Spawn a subagent whose prompt includes every shell's full text, the source spec, and the following review prompt, and instructs it to invoke `/peer-review` via the Skill tool:

```
<task>
Review the following plan shells against their source spec. Each shell file has YAML frontmatter (type, status, spec, depends_on) and contains Context, Produces, Consumes, Covers Spec Requirements, high-level Implementation Steps, and Open Questions. Check for: spec requirements not appearing in any shell's Covers Spec Requirements field (gaps), dead ends where a shell's Produces is never consumed by a later shell or required by the final system, missing prerequisites where a shell's Consumes does not trace to a prior shell's Produces or to "from existing codebase", implicit dependencies where a shell's Consumes traces to a prior shell that is not listed in its depends_on frontmatter field, duplicated requirements across shells' Covers Spec Requirements fields, and incorrect dependency ordering.
</task>

<structured_output_contract>
For each issue, state: the problem, which shell(s) are affected, the impact, a suggested fix, and priority: P0 (spec requirement missing or system broken), P1 (significant gap), P2 (moderate issue), P3 (minor improvement).
Ignore stylistic preferences. If no issues are found, state that the shells look sound.
</structured_output_contract>
```

## Step 3: Aggregate Combined Findings

Wait for both agents to complete. Aggregate their findings with attribution (reviewer: "internal" or "peer").

Check your task list for remaining tasks and proceed.

## Shell Review Dimensions

### 1. Spec Coverage (No Gaps)

The union of every shell's `Covers Spec Requirements` field must equal the set of requirements in the source spec. For each spec requirement, verify it appears in at least one shell's `Covers Spec Requirements` list. Flag any requirement not covered.

### 2. Wiring (Consumes Trace to Produces)

Every entry in a shell's `Consumes` field must trace to either:

- A prior shell's `Produces` entry (check dependency ordering via the shell's `depends_on` frontmatter field), OR
- An explicit "from existing codebase" annotation

Flag:

- **Missing prerequisites** — Consumes entries with no matching source
- **Dead ends** — Produces entries that no later shell Consumes and that are not part of the final system's entry points (e.g., top-level APIs, main functions, UI routes)
- **Implicit dependencies** — Shells whose Consumes trace to a prior shell that is not listed in their `depends_on` frontmatter

### 3. Completeness (Chain Implements the Spec)

Walk through the shells in dependency order and accumulate their Produces into a running set. After the final shell, verify that every spec requirement (not just every Covers entry) is satisfied by a reachable component in the running set. No component should be orphaned.

### 4. No Duplication

The `Covers Spec Requirements` fields across shells must be disjoint. Flag any spec requirement that appears in more than one shell's `Covers Spec Requirements`. If two shells intentionally touch the same area (one creates, the other extends), the requirement should still map to exactly one of them.

### 5. Cross-Reference Accuracy

If shells reference external resources (other codebases, documentation, APIs, search terms) in their Context, Implementation Steps, or Open Questions, spot-check that referenced projects or docs actually exist and are relevant.

## Priority Levels

- **P0** — Spec requirement missing from all shells, or shell chain produces a broken system
- **P1** — Dead end, missing prerequisite, or implicit dependency that will cause implementation problems
- **P2** — Moderate issue: duplicated requirement, unclear shell boundary, or ordering improvement
- **P3** — Minor improvement

## Output Format

Return findings as a numbered list. For each finding:

```
### [P<N>] <title (imperative, ≤80 chars)>

**Shell(s):** <shell number(s) affected>
**Reviewer:** <internal | peer>

<one paragraph explaining the problem, what impact it has on implementation, and a suggested fix>
```

After all findings, add:

```
## Overall Verdict

**Readiness:** <ready | needs revision>

<1-3 sentence assessment>
```

If there are no qualifying findings, state that the shells look ready for implementation and explain briefly.

## Rules

- If any reviewer is unavailable or returns malformed output, proceed with findings from the remaining reviewer.
- Present findings grouped by priority, then by reviewer.
