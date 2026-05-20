---
name: issue-extract
description: Extracts Issue ID from the current branch name. Use this skill when you need to determine the Issue number associated with the current work context.
---

# Issue Extract

現在のブランチ名から Issue 番号を抽出する。

## Goal

ブランチ名から Issue 番号を取得し、GitHub Issue との連携を可能にする。

## Instructions

1. **現在のブランチ名を取得**
   ```bash
   BRANCH=$(git branch --show-current)
   ```

2. **Issue 番号を抽出**
   ```bash
   ISSUE_ID=$(echo "$BRANCH" | grep -oE '[0-9]+' | head -1)
   ```

3. **エラーチェック**
   ```bash
   if [ -z "$ISSUE_ID" ]; then
       echo "Error: Could not extract Issue ID from branch name: $BRANCH"
       echo "Branch name must contain Issue number (e.g., feature/123-description)"
       exit 1
   fi
   ```

## Expected Branch Naming Patterns

| パターン | 例 |
|----------|-----|
| `feature/ISSUE_ID-description` | `feature/42-add-login` |
| `research/ISSUE_ID-description` | `research/15-explore-caching` |
| `fix/ISSUE_ID-description` | `fix/7-memory-leak` |
| `docs/ISSUE_ID-description` | `docs/3-update-readme` |

## Output

- `ISSUE_ID` 変数に Issue 番号が設定される
- Issue が見つからない場合はエラーメッセージを出力

## Usage in Workflows

このスキルは以下のワークフローで内部的に使用される:
- `/commit-merge`
- `/commit-push`
- `/report-progress`
- `/branch-task`
