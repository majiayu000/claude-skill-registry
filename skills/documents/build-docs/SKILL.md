---
name: build_docs
description: Sphinxドキュメントをビルドする
---

# Build Code

This skill builds the project documentation.

## Usage

To build the HTML documentation:
```bash
sphinx-build -b html docs docs/_build/html
```

To clean the build directory first:
```bash
rm -rf docs/_build
sphinx-build -b html docs docs/_build/html
```

## View Docs

After building, the index file is located at:
`docs/_build/html/index.html`
