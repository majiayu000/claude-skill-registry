---
name: test_notebooks
description: 全てのプロジェクトノートブックを順次実行し、エラーがないか確認する
---

# Run All Notebooks

This skill executes all `.ipynb` files in the project one by one.

## Instructions

1.  **Find Notebooks**:
    *   Search for all `.ipynb` files in the project/workspace.
    *   Exclude `.ipynb_checkpoints`.

2.  **Execute Sequentially**:
    *   Iterate through the list of notebooks.
    *   For each notebook, execute it using a command line tool that runs the kernel.
    *   **Recommended Tool**: `jupyter nbconvert --to notebook --execute --inplace <notebook.ipynb>` or `pytest --nbmake <notebook.ipynb>` (if installed).
    *   **CRITICAL**: Wait for one notebook to finish before starting the next to conserve memory.

3.  **Report**:
    *   Track pass/fail status for each.
    *   If a notebook fails, stop or log the error and continue (depending on user preference, default to continue).
    *   Provide a summary report at the end.
