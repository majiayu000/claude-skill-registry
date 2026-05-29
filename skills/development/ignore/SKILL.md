---
name: ignore
description: 不要なファイル・ディレクトリを .gitignore に追加・管理する
---

# Update Gitignore

This skill adds specific files or patterns to `.gitignore` to prevent them from being tracked by git.

## Instructions

1.  **Check Status**:
    *   Check if the file/directory is already in `.gitignore`.
    *   Check if the file is currently tracked by git using `git ls-files <path>`.

2.  **Update .gitignore**:
    *   Append the path or pattern to the `.gitignore` file in the root directory.
    *   Add a comment if necessary to explain why it's ignored.

3.  **Untrack (if needed)**:
    *   If the file was already tracked, run `git rm --cached <path>` to stop tracking it while keeping the local copy.
