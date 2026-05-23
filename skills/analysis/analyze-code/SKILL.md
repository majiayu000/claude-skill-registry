---
name: analyze_code
description: 外部ライブラリや他言語で書かれたコードの実装を分析する
---

# Analyze External Code

This skill helps in understanding code outside of the main Python source tree.

## Instructions

1.  **Locate Source**:
    *   If analyzing an installed library: Find where it is installed (usually `.venv/lib/pythonX.X/site-packages/`).
    *   If analyzing non-Python code (e.g. C++, MEDM files): Find the files in the file tree.

2.  **Read and Analyze**:
    *   Use `view_file` to read the implementation.
    *   For binary files or unknown formats, try to find a parser or read as text if applicable (e.g. MEDM `.adl` files are text).
    *   Map the external logic to how it interacts with or should be implemented in `gwexpy`.

3.  **Report**:
    *   Explain the data structures, algorithms, or logic flow found.
    *   Highlight differences with the current `gwexpy` implementation.
