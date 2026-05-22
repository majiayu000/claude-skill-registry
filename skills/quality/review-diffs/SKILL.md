---
name: review-diffs
description: Performs comprehensive code review on git diffs and generates review.md with quality scores, critical issues, performance concerns, and potential bugs. Use when user requests to review changes, check code quality, analyze diffs, or validate LLM-generated code
---

# Review diffs

## Instructions

- Read diffs with `git diff` commands, and review code after LLM changes code

## Todo

- Read diffs with `git diff` commands
- Review diffs
- Create/update docs/review.md in the current directory that you're working on

## What docs/review.md should contain

- Score (up to 100)
- Short summary
- Critical issue
- Potentially performance issue
- potential bug


## Examples

- Score (up to 100): 45
- Short summary: `format_all_attachment` is now wired into the token counter, but the prompt builder still falls back to the old helper that drops full-file attachments whenever a ranged snippet exists, so the shipped behavior hasn’t actually improved and the token math is now inconsistent with what the LLM sees.
- Critical issue:
  - `PromptBuilder.build_prompt` still chooses `format_ranged_attachment` for the whole batch whenever *any* attachment has `line_range`, and the helper only emits entries for those ranged files, so attachments without ranges vanish from the actual prompt even though the new formatter counts them. Users still lose files and won’t get their code reviewed. (src/usecase/message/prompt_builder.py:24, src/usecase/helper/helper.py:198)
- Potentially performance issue:
  - `GenerateMessageUseCase.execute` now counts tokens for every attachment via `format_all_attachment`, but the prompt builder sends fewer tokens when the mix contains both ranged and full files. Legitimate requests are rejected too early with EEAOAI40003 even though the downstream prompt would have fit, effectively shrinking usable context and wasting retries. (src/usecase/message/generate.py:140, src/usecase/message/prompt_builder.py:24)
- potential bug:
  - The same prompt-builder helper is used for each `HistoryItem`, so any historical message that combined ranged and non-ranged attachments will also drop the non-ranged ones. Past context can silently disappear between turns, leading the model to hallucinate or ignore previous uploads. (src/usecase/message/prompt_builder.py:33)

