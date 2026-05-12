<!-- SOURCE-OF-TRUTH: shared/references/git_scope_detection.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# Git Scope Detection

Algorithm for building `changed_files[]` — the set of files to analyze for code quality.

## Base Branch Detection (run once, first match wins)

```
1. git reflog --format="%gs" | grep "moving from" | head -1  → extract source branch name
2. git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||'
3. Check local branches: develop → main → master (first that exists locally)
4. Fallback: "main"
```

## Committed Changes

- **If on `feature/*` branch:**
  ```
  git diff --name-only {base_branch}...HEAD
  ```
  (three-dot uses merge-base automatically)
  → if fails: `git diff --name-only origin/{base_branch}...HEAD`
  → if both fail: `[]`

- **Else (main/master/develop/detached HEAD):** committed = `[]`

## Uncommitted Changes

```
git diff --name-only          # unstaged
git diff --name-only --cached # staged
```

## Build `changed_files[]`

```
changed_files[] = union(committed, uncommitted)  # deduplicated
```

## Enrich from Task Metadata

Add file paths from task Affected Components / Existing Code Impact not already in `changed_files[]`.

> Metadata **expands** scope only — never restricts. All files in `changed_files[]` are analyzed.

## Error Handling

If all git commands fail → WARN "git scope unavailable", fall back to task metadata only.


## Compact Output Flags

Default to machine-readable / truncated forms to keep context budget tight. Escalate to full output only when the compact form is insufficient.

| Verbose | Compact default | When to escalate |
|---------|-----------------|------------------|
| `git status` | `git status --porcelain` | Human-facing report only |
| `git log` | `git log --oneline -N` (N = budget, typically 10–20) | Need full commit bodies |
| `git diff` | `git diff --stat` first | Decide based on `--stat` whether to load full diff |
| `git diff --cached` | `git diff --cached --stat` first | Same as above |
| `git show` | `git show --stat {rev}` first | Same as above |

Rules:

- Never read a full diff solely to count files — `--stat` is sufficient.
- When piping (`| head`, `| tail`), preserve exit code via `set -o pipefail` or `${PIPESTATUS[0]}`.
- `git reflog --format="%gs"` (already used in Base Branch Detection) is the canonical compact reflog form; do not switch to full `git reflog`.
