---
name: review_repo
description: リポジトリ全体を構造、コード品質、テスト、ドキュメントの観点から体系的にレビューし、優先度付きの改善レポートを生成する
---

# Review Repository

Evaluates the overall quality and structure of the repository and creates an improvement roadmap.

## Procedure

1.  **Understand Directory Structure**:
    *   Use `list_dir` to obtain an overview of the project (e.g., `gwexpy`, `tests`, `docs`, `examples`).
    *   Use `find_by_name` to check the distribution of major file formats (`.py`, `.ipynb`, `.md`, `.toml`).

2.  **Verify Design and Dependencies**:
    *   Read `README.md` to understand the project's purpose and key features.
    *   Check `pyproject.toml` or `setup.py` to grasp dependencies and build configurations.

3.  **Code Quality Screening**:
    *   Use `grep_search` to find anti-patterns or lingering items:
        *   `except Exception:` (Overly broad exception catching)
        *   `pass` (Empty blocks)
        *   `TODO`, `FIXME`, `XXX`
        *   Support code for older Python versions (`sys.version_info`)
    *   Use `view_file_outline` to check if methods in major classes have type hints and docstrings.

4.  **Verification of Testing and QA**:
    *   Assess the scale and status of tests using the `run_tests` skill or `run_command` (`pytest --collect-only`).
    *   Check CI configurations such as GitHub Actions (`.github/workflows`).

5.  **Report Generation and Task Creation**:
    *   Create a report including the following sections:
        *   **Overview**: Project scale and current state.
        *   **Strengths**: Points of good implementation and design.
        *   **Improvements (P1: High, P2: Med, P3: Low)**: Specific issues organized by priority.
    *   Based on the report, save a "Markdown-formatted improvement task prompt" under `docs/developers/plans/` so it is tracked alongside other developer plans.
