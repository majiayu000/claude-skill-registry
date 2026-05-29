---
name: simplify-docs
description: "Run a multi-agent review of code comments and markdown documentation for unnecessary content, then fix the issues. Covers what-restating comments, name-mirroring doc comments, status-update prose, and other documentation noise. Use when the user asks to \"simplify docs\", \"simplify documentation\", \"clean up comments\", \"clean up docs\", \"review documentation\", \"strip unnecessary comments\", \"reduce doc noise\", or \"run simplify-docs\"."
---

# Simplify Docs

Review code comments and markdown documentation for unnecessary content, then fix the issues.

## Step 1: Determine the Scope

Determine what to review:

- If a specific **diff command** was provided (e.g., `git diff --cached`), use that.
- If a **file list or directory** was provided, review those files directly (read the full files, not a diff).
- If **neither** was provided, determine the appropriate diff command (e.g., `git diff`, `git diff --cached`, `git diff HEAD`) based on the current git state. If there are no git changes, default to a full-tree sweep of source files plus top-level markdown.

## Step 2: Launch Two Review Agents in Parallel

Use the Agent tool to launch both agents below in a single assistant message so they run concurrently. Each Agent call uses `model: "opus"` and does not set `run_in_background`. Pass the scope from Step 1 to each agent.

### Agent 1: Code Comments Review

Review code files in scope. Flag a comment when it adds no information beyond what the code already says:

1. **Restates code, signature, or name** — paraphrases the immediately-following statement, a multi-statement block, a declaration's name, or the parameter/return shape. Includes doc blocks above a declaration whose prose elaborates the name and signature without adding rationale, and Parameters/Returns/Throws enumerations that only echo names and types. Flag only the redundant entries; non-obvious constraints (size, units, ranges, preconditions) stay. Drop the wrapping enumeration when no entries survive trimming.
2. **Narrates history or change** — references PRs, tickets, prior behavior, recent changes, "fixed by"/"previously did X"/"no longer Y" framing, or session-narrative voice ("turns out", "discovered", "we found that"). State the current invariant; past behavior belongs in git history, and session-derived lessons about tooling belong in auto memory or project instructions.
3. **Cross-references that decay** — names the caller ("used by X", "called from Y"), or task/flow/feature-flag context the code was added for ("added for the Y flow", "for the rollout"). Delete: caller relationships belong in the call graph, feature context in the PR description.
4. **Explains language or framework constructs** — describes what a stdlib feature, language keyword, or well-known framework call does. Assume a competent reader.
5. **Low-value section banners** — banners that don't section anything, or that restate what an access modifier or naming convention already conveys. Idiomatic structural markers around a real section stay.
6. **Overgrown rationale** — a comment that captures real WHY but in more lines or concerns than the rationale requires. Tighten to one sentence per concern, split bundled concerns to their decision points, or lift shared rationale to a design doc or commit message.
7. **Compensates for unclear code** — a comment that exists because the code is hard to read. Flag the underlying code as a refactor opportunity (rename, extract, restructure) rather than tightening the comment.

**Keep these:** comments that capture a load-bearing constraint the code itself cannot express — a hidden constraint or invariant, a workaround for a specific bug (ideally with a reference), a non-obvious performance characteristic, a pointer to a spec or RFC section, or behavior that would surprise a future reader and lead them to "fix" working code. Greenfield test: would you write this comment if the code had been greenfield from day one?

For each finding, propose: delete it, compress to the load-bearing WHY, or flag a refactor that would make the comment unnecessary.

### Agent 2: Markdown Documentation Review

Review markdown files in scope (READMEs, AGENTS.md, CLAUDE.md, docs/, contributor guides). Flag passages that add no information beyond what the reader can derive from current state:

1. **Status-update voice** — prose framed as recent updates or transitions. Rewrite as timeless current-state prose.
2. **Restates what the codebase already shows** — passages that duplicate the repo layout or re-summarize what the code makes obvious.
3. **WHAT without WHY** — explanations of what a feature does that the feature's own name and signature already convey. Keep the parts that explain motivation, constraints, or tradeoffs.
4. **Scaffolding leak** — auto-generated headings, boilerplate sections, or prescriptive bullets that read like spec output rather than reader-facing prose.
5. **Explanation rot** — passages that describe an old design or contradict the current code. Delete or update to match reality.
6. **Multi-paragraph essays where one line would do** — long-form passages that restate the same point multiple ways. Keep one tight version.

**Keep these:** passages that explain motivation, capture constraints or tradeoffs the code can't express, document interfaces meant for outside readers, or record decisions whose rationale would otherwise be lost.

For each flagged passage, propose: delete it, tighten it, or rewrite it as timeless current-state prose.

## Step 3: Fix Issues

Wait for both agents to complete. Aggregate their findings, then apply each fix directly, skipping false positives. When uncertain whether a comment captures a non-obvious WHY, keep it.

When done, briefly summarize what was removed or rewritten (or confirm the docs were already clean).

Then use the TaskList tool and proceed to any remaining task.
