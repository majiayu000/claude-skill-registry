---
name: fix_notebook
description: ノートブックのエラーを、そのノートブック自体の修正またはソースコードの修正により解決する
---

# Fix Notebook Errors

This skill handles fixing errors encountered during notebook execution.

## Instructions

1.  **Analyze the Failure**:
    *   Examine the traceback to determine if the error is in the notebook cell's logic or the underlying library.

2.  **Strategy A: Fix Notebook (Local)**:
    *   If the usage is wrong or imports are missing, edit the `.ipynb` cells.
    *   Modify the `"source"` field of the failing code cell in the notebook JSON.

3.  **Strategy B: Fix Source Code**:
    *   If the bug is in the `gwexpy/` package, trace it to the source file.
    *   Apply the fix to the Python source while ensuring no regressions.

4.  **Verification**:
    *   Re-run the notebook to confirm it passes.
