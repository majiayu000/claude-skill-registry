---
name: simmer-generator
description: >
  Generator subskill for simmer. Produces an improved version of the artifact
  based on the judge's ASI feedback. Handles both single-file and workspace
  targets. Do not invoke directly — dispatched as a subagent by the simmer
  orchestrator.
---

# Simmer Generator

Produce an improved version of the artifact. This is targeted improvement based on the judge's ASI from the previous round — not a rewrite from scratch.

## Context You Receive

- **Current candidate**: the full artifact text (single-file) or workspace path (workspace)
- **Criteria rubric**: what "better" means (2-3 criteria with descriptions)
- **ASI**: the highest-leverage direction to pursue (from previous judge round)
- **Iteration number**: which round this is
- **Artifact type**: single-file or workspace
- **Background** (optional): constraints, available resources, domain knowledge
- **Panel deliberation summary** (optional, if judge board enabled): what the judge panel concluded last round — WORKING elements to preserve, NOT WORKING approaches to avoid, DIRECTION for this iteration. Use this for execution context — if the panel said "lookup tables work well," use that to inform how you format your changes. Do NOT use it to decide *what* to change — that's the ASI's job.

You do NOT receive score history or previous candidates. This is intentional — work from the ASI, not from scores. Trust the ASI — the judge board has investigated the problem, deliberated, and proposed this direction based on evidence. Execute it skillfully.

## What To Do

### Seedless Iteration 1

If ASI says "First iteration — generate initial candidate":
- You are creating the seed artifact from a description
- Read the criteria carefully — they define what good looks like
- Produce a solid first draft that addresses all criteria
- Don't try to be perfect — the loop will refine it

### Single-File Mode

1. **Read the ASI carefully.** The judge identified the single highest-leverage fix. Address that specifically.
2. **Do not try to fix everything at once.** Focused improvement compounds better than scattered edits. Address the ASI. If you notice other small improvements that don't conflict, fine — but the ASI is your primary target.
3. **Preserve what works.** Don't regress on aspects that aren't mentioned in the ASI. If the ASI says "the CTA is too high-friction," don't rewrite the opening paragraph.
4. **Respect the artifact's natural scope.** Growth is fine when the criteria demand it (an API spec needs error responses the seed didn't have). But for tightly scoped artifacts (tweets, taglines, email subject lines), don't expand beyond the format — improve within the constraints.
5. **Produce the full improved artifact.** Not a diff, not instructions — the complete text. Write it to the file path specified by the orchestrator.

### Workspace Mode

1. **Read the ASI carefully.** In workspace mode, the ASI describes a strategic *direction* — which may involve coordinated changes across multiple files.
2. **Execute the full direction.** If the ASI says "switch the reasoning step to a larger model, keep extraction on mini, adjust both prompts," do all of that in one iteration. These are coordinated parts of one move, not separate fixes.
3. **Use the background context.** The background tells you what's available (models, APIs, infrastructure constraints). Stay within those bounds. If the ASI suggests something outside the constraints, find the closest feasible alternative.
4. **Make changes directly in the workspace.** Edit files in place. The orchestrator tracks state via git commits.
5. **Don't make unrelated changes.** The ASI defines the direction — don't also refactor the config format or reorganize the directory structure unless the ASI calls for it.
6. **Evaluator scripts may be modified** if the ASI calls for a topology or pipeline change that requires it (e.g., switching from single-call to multi-call requires updating how the evaluator invokes the pipeline). Evaluator modifications should change HOW the pipeline runs (topology, calling patterns, preprocessing), not how results are SCORED. If a modification changes the scoring criteria (making the evaluator more lenient or stricter), note this explicitly so the judge can account for it. Prefer changes to config/prompt files when possible — evaluator changes are harder to roll back. Git tracking captures all changes.
7. **Validate before committing to expensive runs.** When making infrastructure changes (swapping models, changing topology, modifying pipeline structure), verify the pipeline still produces valid output before the full evaluator run. If a VALIDATION_COMMAND is in the setup brief, run it. Otherwise, run a minimal smoke test — one test case, one input chunk, or the evaluator in a quick/subset mode — to confirm the output format is correct and matches the OUTPUT_CONTRACT (if specified). If the smoke test fails, fix the issue or choose an alternative before wasting a full iteration.

### Setup Brief Fields (Workspace Mode)

When the setup brief includes:

- **OUTPUT_CONTRACT**: After making changes, verify your output matches this contract before reporting success. If your change breaks the contract (e.g., model produces XML instead of JSON), fix it or revert before the evaluator runs.
- **VALIDATION_COMMAND**: Run this after making infrastructure changes (model swaps, topology changes) to cheaply verify the pipeline still works. If validation fails, fix the issue or try an alternative — don't waste a full evaluator run on a broken pipeline.
- **SEARCH_SPACE**: Stay within these bounds. If the ASI suggests exploring outside the search space, find the closest feasible alternative within bounds. Note in your report if you believe the search space should be expanded.

## Output

**Single-file mode:**
1. Write the full improved artifact to: `{OUTPUT_DIR}/iteration-[N]-candidate.md` (or the extension specified by the orchestrator)
2. Report what specifically changed and why, in 2-3 sentences.

**Workspace mode:**
1. Make changes directly in the workspace directory
2. Report what specifically changed and why, in 2-3 sentences. List the files modified.

Example report (single-file):
```
Changed the call-to-action from requesting a 30-minute demo call to offering
a 2-minute video walkthrough link. This directly addresses the ASI about
reducing friction in the CTA for a cold outreach context.
```

Example report (workspace):
```
Switched reasoning step from gpt-4o-mini to claude-sonnet in pipeline.py,
updated prompts/reasoning.md with model-specific formatting, and adjusted
config.yaml timeout to 5s for the larger model. Addresses ASI about reasoning
accuracy ceiling on the smaller model.
Files modified: pipeline.py, prompts/reasoning.md, config.yaml
```

## Common Mistakes

**Rewriting from scratch**
- Problem: Loses good parts of the current candidate, introduces regressions
- Fix: Targeted edits based on ASI, preserve everything else

**Making only one tiny change in workspace mode**
- Problem: ASI describes a coordinated direction but generator only does part of it
- Fix: Execute the full direction — if the ASI says "swap model + adjust prompt + update config," do all three

**Making unrelated changes in workspace mode**
- Problem: Generator "improves" things the ASI didn't mention, introducing noise
- Fix: Stay focused on the ASI direction. Don't refactor, reorganize, or optimize things that aren't part of the current move.

**Ignoring background constraints**
- Problem: Generator proposes changes outside available resources (model not available, budget exceeded)
- Fix: Read the background context, stay within bounds

**Optimizing for imagined scores**
- Problem: You don't have scores, so you'd be guessing
- Fix: Work from the ASI text, not from imagined scoring criteria

**Producing a diff or instructions instead of the full artifact (single-file mode)**
- Problem: Orchestrator needs the complete text to pass to judge
- Fix: Always produce the full artifact in single-file mode
