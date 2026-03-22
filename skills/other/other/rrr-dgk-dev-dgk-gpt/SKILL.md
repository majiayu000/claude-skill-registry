---
name: rrr
description: GLM-5 코드 리뷰. /rr의 상위 버전으로 더 강한 모델로 변경사항을 검토하고, Codex가 결과를 다시 검증해 유효한 이슈만 정리한다.
---

# /rrr

Use `glm-review --model glm-5` as the deeper paid review pass, then validate the results against the code before you trust them.

## Default Flow

1. Determine the exact review scope first.
- commit hash known -> commit mode
- `staged` -> staged mode
- `pr` -> PR mode
- mixed unrelated local changes -> focused diff file
2. Run a health check only when auth or connectivity looks questionable:

```bash
glm-review --model glm-5 --health
```

3. Run the review with the smallest correct input:

```bash
glm-review --model glm-5
glm-review --model glm-5 --mode staged
glm-review --model glm-5 --mode pr
glm-review --model glm-5 --mode commit --ref <COMMIT_HASH>
glm-review --model glm-5 --diff-file /tmp/glm-review-diff.patch
```

4. Verify every reported issue in the actual code and diff.
5. Keep only confirmed issues.
6. If fixes are requested or clearly in scope, apply them and rerun the closest verification.

## Choosing Review Input

- committed single change:

```bash
glm-review --model glm-5 --mode commit --ref <COMMIT_HASH>
```

- committed subset of files:

```bash
glm-review --model glm-5 --mode commit --ref <COMMIT_HASH> --files src/a.ts src/b.ts
```

- custom focused diff:

```bash
GIT_ROOT=$(git rev-parse --show-toplevel)
cd "$GIT_ROOT" && git diff HEAD -- <file1> <file2> ... > /tmp/glm-review-diff.patch
glm-review --model glm-5 --diff-file /tmp/glm-review-diff.patch
```

If the diff is empty, stop and say there is nothing to review.

## Validation Rules

- `glm-review` is a reviewer, not an oracle.
- Re-check referenced code paths before reporting a bug.
- Separate confirmed defects from debatable style feedback.
- If a finding depends on broader context, inspect the relevant surrounding code before accepting it.

## Error Handling

- `command not found: glm-review`
  Install it with `npm install -g glm-review`
- `ZAI_API_KEY not set`
  Export `ZAI_API_KEY` in the shell or your normal secret-loading path
- auth or API failure
  Re-run `glm-review --model glm-5 --health` after refreshing credentials

## Finish

Return:

- review scope used
- confirmed findings only
- notable false positives filtered out
- what verification ran after fixes, if any
