---
name: get-docs-root
description: Retrieve the value of the DOCS_ROOT environment variable. Use this skill whenever you need to determine the documentation root directory for the current environment, or when a workflow requires knowledge of DOCS_ROOT.
---

# Get Docs Root

## Overview

## Usage

To retrieve the value of the DOCS_ROOT environment variable, execute the following script:

```bash
python3 scripts/get_docs_root.py
```

- If DOCS_ROOT is set, the script will print its value.
- If DOCS_ROOT is unset or empty, the script will print an empty line.

Use this skill whenever you need to programmatically determine the documentation root directory for the current environment, or when a workflow requires knowledge of DOCS_ROOT.
