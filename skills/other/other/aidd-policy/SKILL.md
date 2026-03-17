---
name: aidd-policy
description: Defines the shared policy contract for output format, read discipline, question format, and loop safety. Use when applying cross-stage policy rules.
lang: en
model: inherit
user-invocable: false
---

## Scope
- This skill is the single source of truth for reusable policy guidance.
- Stage/runtime ownership stays in `feature-dev-aidd:aidd-core` and stage skills.
- Preload matrix v2: this skill is required for every subagent role.

## Output contract (required)
- Status: ...
- Work item key: ...
- Artifacts updated: ...
- Tests: ...
- Blockers/Handoff: ...
- Next actions: ...
- AIDD:READ_LOG: ...
- AIDD:ACTIONS_LOG: ...

Include `Checkbox updated: ...` when the command/stage contract expects it.

## Question format
Use this exact format when asking the user:

```text
Question N (Blocker|Clarification): ...
Why: ...
Options: A) ... B) ...
Default: ...
```

## Read policy (pack-first)
- Read packs/excerpts before full documents.
- Prefer `rlm_slice.py` and section slices for focused evidence.
- Full-file reads are allowed only when slices are insufficient.
- Keep `AIDD:READ_LOG` compact and point to `aidd/reports/**`.

## Loop safety
- Loop stages run through canonical stage-chain (`preflight -> run -> postflight -> stage_result`).
- Manual stage-result writes remain forbidden operator paths.
- Missing preflight/readmap/writemap/actions/log artifacts is a contract violation.

## Runtime path safety
- Never guess runtime filenames/paths.
- Execute only runtime entrypoints explicitly listed in the current stage skill `Command contracts`.
- Use only canonical active-state runtime commands from the current stage contract; do not use deprecated aliases.
- For loop stages, internal preflight runtime remains a stage-chain orchestration detail, not a user-facing command contract.
- If command output contains `can't open file .../skills/.../runtime/...`, stop and report BLOCKED (`runtime_path_missing_or_drift`) with evidence path.

## Retry safety
- Do not repeat the same failing shell command in a loop.
- For cwd/build-tool mismatch (`./gradlew` missing, or `does not contain a Gradle build`), allow at most one corrected attempt after explicit cwd resolution.
- If corrected attempt still fails, stop with blocker (`tests_cwd_mismatch`) and handoff instead of further retries.

## Subagent guard
- Subagents must not edit `aidd/docs/.active.json`.

## Command contracts
### `Policy output contract application`
- When to run: before final response for every stage/subagent output.
- Inputs: current stage result plus artifacts/tests/blockers evidence.
- Outputs: deterministic response skeleton with required contract fields.
- Failure mode: missing required fields, ambiguous status, or inconsistent blocker/handoff reporting.
- Next action: normalize output structure and rerun final response composition.

### `Policy question protocol`
- When to run: only when blocker/clarification is unavoidable after artifact-first checks.
- Inputs: verified blocker context, user-facing options, and default path.
- Outputs: one compact policy-compliant question using `Question N/Why/Options/Default` format.
- Failure mode: free-form or multi-topic questions that lack options/default.
- Next action: rewrite the question into deterministic policy format before asking.

## Additional resources
- [references/output-contract.md](references/output-contract.md) (when: response structure is unclear; why: copy exact contract fields and stage notes).
- [references/read-policy.md](references/read-policy.md) (when: deciding between slice and full read; why: keep evidence gathering deterministic and minimal).
- [references/question-format.md](references/question-format.md) (when: blockers require user clarification; why: ask short, actionable questions with defaults).
- [references/loop-safety.md](references/loop-safety.md) (when: loop-stage safety flags or artifacts are in question; why: apply consistent blocked/warn policy).
