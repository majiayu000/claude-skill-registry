---
name: wrap_up
description: 作業終了時の一連のフロー（検証、テスト、リント、ドキュメント更新、コミット）を一括実行する
---

# Wrap Up Work

This skill executes a standard sequence of tasks to verify, clean, and commit work.

## Instructions

1.  **Verify Physics**:
    *   Run the `verify_physics` skill to ensure physical correctness of any new implementation.

2.  **Quality Check**:
    *   Run the `run_tests` skill to verify functionality.
    *   Run the `lint_code` skill to ensure code style and types are correct.
    *   *Stop if significant errors are found.*

3.  **Documentation**:
    *   Run the `sync_docs` skill to update docstrings and documentation files.

4.  **Finalize**:
    *   Run the `update_gitignore` skill if new untracked files shouldn't be committed.
    *   Run the `commit_cleanup` skill to remove temporary files and commit the changes.
