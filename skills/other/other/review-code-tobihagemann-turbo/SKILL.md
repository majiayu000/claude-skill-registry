---
name: review-code
description: "Review code for bugs, security vulnerabilities, API misuse, consistency issues, simplicity problems, or test coverage gaps by running internal reviews and a peer review in parallel and returning combined findings. Single-concern with a type argument, or full review with no argument. Use when the user asks to \"review my code\", \"full code review\", \"review my changes\", \"check for bugs\", \"scan for bugs\", \"review correctness\", \"security audit\", \"find vulnerabilities\", \"review security\", \"check API usage\", \"verify against docs\", \"check for cross-file duplication\", \"review consistency\", \"check for code reuse\", \"review simplicity\", \"find untested code\", or \"review test coverage\"."
---

# Review Code

Review code against type-specific criteria. Runs internal reviews and `$peer-review` in parallel by default. Returns combined structured findings.

**Types:** `correctness`, `security`, `api-usage`, `consistency`, `simplicity`, `coverage`

With a type argument, runs a single-concern internal review plus the peer review. With no type argument, runs all six internal reviews plus the peer review.

## Step 1: Determine the Scope

Determine what to review:

- If a specific **diff command** was provided (e.g., `git diff --cached`, `git diff main...HEAD`), use that.
- If a **file list or directory** was provided, review those files directly (read the full files, not a diff).
- If **neither** was provided, default to diffing against the repository's default branch (detect via `gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'`). If there are no changes against the default branch, stop and state that there is nothing to review.

## Step 2: Run Reviews in Parallel

Read the reference file(s) for the active type(s):

- **Correctness** — [references/correctness-review.md](references/correctness-review.md)
- **Security** — [references/security-review.md](references/security-review.md)
- **API usage** — [references/api-usage-review.md](references/api-usage-review.md)
- **Consistency** — [references/consistency-review.md](references/consistency-review.md)
- **Simplicity** — [references/simplicity-review.md](references/simplicity-review.md)
- **Coverage** — [references/coverage-review.md](references/coverage-review.md)

Full review activates all six types; a single-concern argument activates one. Skip peer review when instructed (e.g., "without peer review", "no peer", "internal only").

Run the review branches independently. Launch them with `spawn_agent` / `wait_agent` using inherited model defaults. For full review that is six internal branches plus one peer branch; for single-concern it is one internal branch plus one peer branch.

- **Internal branch (one per active type):** Apply the type's criteria to the scope and return findings in the output format below.
- **Peer review branch (unless skipping):** Run the `$peer-review` skill with a request describing: (a) the scope to review; (b) each active type as a separate review dimension so they are reviewed independently; (c) for each dimension, the criteria live in `~/.agents/skills/review-code/references/<type>-review.md` — Claude should read that file directly, use its priority scale and verdict label, and include any extra metadata fields it specifies (e.g., `**Category:**`, `**Library:**`, `**Docs:**`) between the `**Reviewer:**` line and the paragraph. The branch prompt must also state explicitly that the sub-agent's final message must contain the verbatim findings text `$peer-review` produced.

Aggregate findings with attribution (reviewer: "internal" or "peer"; type; file path). Present them in the output format below.

Then update or check the active plan and proceed to any remaining task.

## Output Format

Return findings as a numbered list. For each finding:

```
### [P<N>] <title (imperative, ≤80 chars)>

**File:** `<file path>` (lines <start>-<end>)
**Reviewer:** <internal | peer> (<type>)

<one paragraph explaining the issue and its impact>
```

The reference file may specify additional metadata fields (e.g., `**Category:**`, `**Library:**`, `**Docs:**`). Include them between the `**Reviewer:**` line and the paragraph.

After all findings, add an overall verdict per active type using the label from each reference file. For single-concern, that is one verdict block; for full review, six. After the per-type verdicts, add a single combined `## Peer Review Verdict` block summarizing what the peer review returned.

```
## Overall Verdict — <type>

**<Verdict Label>:** <status>

<1-3 sentence assessment>
```

If there are no qualifying findings for a type, state so under that type's verdict block and explain briefly.

## Rules

- Present findings grouped by priority.
- In full code review mode, present findings in file order to minimize context switching.
