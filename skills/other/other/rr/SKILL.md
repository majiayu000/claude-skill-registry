---
name: rr
description: 코드 리뷰. 작업 후 변경사항을 Z.AI 모델로 검토하고, Codex가 결과를 다시 검증해 유효한 이슈만 정리한다. /rr 또는 'GLM 리뷰' 요청 시 사용.
---

# /rr

Use `glm-review` as a second reviewer for the current change set, then validate the reported issues against the actual code before you trust or repeat them.

## Default Flow

1. Determine the exact change scope first.
- If the user points to a commit, prefer commit mode.
- If the user says `staged`, use staged mode.
- If the user says `pr`, use PR mode.
- If the workspace has mixed unrelated changes, build a focused diff file for only the intended files.
2. Run a quick connectivity check only when the environment looks suspect:

```bash
glm-review --health
```

3. Run the review with the narrowest correct input:

```bash
glm-review
glm-review --mode staged
glm-review --mode pr
glm-review --mode commit --ref <COMMIT_HASH>
glm-review --diff-file /tmp/glm-review-diff.patch
```

4. Treat the output as a candidate issue list, not ground truth.
5. Re-open the referenced code and verify each claim.
6. Report only valid issues, ordered by severity.
7. If fixing issues is in scope, fix them and rerun the closest relevant verification.

## Choosing Review Input

Prefer the most specific path that isolates the current task:

- committed single change:

```bash
glm-review --mode commit --ref <COMMIT_HASH>
```

- committed subset of files:

```bash
glm-review --mode commit --ref <COMMIT_HASH> --files src/a.ts src/b.ts
```

- custom focused diff for multi-session or mixed worktrees:

```bash
GIT_ROOT=$(git rev-parse --show-toplevel)
cd "$GIT_ROOT" && git diff HEAD -- <file1> <file2> ... > /tmp/glm-review-diff.patch
glm-review --diff-file /tmp/glm-review-diff.patch
```

If the diff is empty, stop and say there is nothing to review.

## Validation Rules

- Do not parrot `glm-review` output without checking the code.
- Drop false positives explicitly instead of forwarding them.
- Distinguish between confirmed bugs, arguable style comments, and already-fixed issues.
- If the review claims a regression, inspect the relevant file and the actual diff before accepting it.

## Error Handling

Common fixes:

- `command not found: glm-review`
  Install it with `npm install -g glm-review`
- `ZAI_API_KEY not set`
  Export `ZAI_API_KEY` in the shell or your normal secret-loading path before rerunning
- `401` or auth failure
  Re-run `glm-review --health` after refreshing credentials

## Finish

Return:

- review scope used
- confirmed findings only
- what was rejected as false positive, if anything material
- what verification ran after fixes, if any
