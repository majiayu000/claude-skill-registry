---
name: sync_docs
description: ソースコードの実装に合わせてドキュメント (docstring, *.md) を更新する
---

# Sync Documentation

This skill ensures that the documentation is in sync with the actual code implementation.

## Instructions

1.  **Update Docstrings**:
    *   Read the target source code.
    *   Check if parameters, return types, and exceptions in the docstring match the signature and logic.
    *   Update the docstring using the standard format (NumPy or Google style, matching the project).

2.  **Update Documentation Files**:
    *   Check `docs/` or `README.md` for references to the changed code.
    *   **Crucial**: Check both English (`docs/reference/en/`) and Japanese (`docs/reference/ja/`) documentation directories.
    *   Update tutorials or API references if the usage has changed.
    *   If a new feature was added, ensure it is mentioned in the appropriate section in both languages.

3.  **Verify**:
    *   If possible, run the `build_docs` skill to ensure no syntax errors were introduced in ReStructuredText or Markdown.
