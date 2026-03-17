---
name: make_notebook
description: 機能やテーマについて解説付きのJupyter Notebook (.ipynb) を生成する
---

# Create Notebook

This skill generates a Jupyter Notebook to demonstrate a feature or explain a concept.

## Instructions

1.  **Plan the Notebook**:
    *   **Title & Introduction**: What is this notebook about?
    *   **Setup/Imports**: Necessary imports.
    *   **Data Generation/Loading**: Create synthetic data or load sample data.
    *   **Processing/Analysis**: Demonstrate the core feature.
    *   **Visualization**: Plot the results.

2.  **Create File**:
    *   Use the `write_to_file` tool to create the `.ipynb` file. (*Note: Since writing JSON manually for ipynb is error-prone, ensure you use a valid JSON structure or use a helper script if available. If writing raw JSON, keep it simple.*)
    *   Alternately, write a Python script `make_notebook.py` using `nbformat` and run it.

3.  **Content Requirements**:
    *   Use Markdown cells to explain *why* and *how*.
    *   Comment the code cells extensively.
    *   Ensure the code is runnable without external local files (or create them on the fly).
