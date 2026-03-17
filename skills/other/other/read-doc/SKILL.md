---
name: read-doc
description: "Leverage the llmdoc documentation system to quickly understand the project architecture, code details, and key concepts without reading source code directly."
disable-model-invocation: true
context: fork
allowed-tools: Read, Glob, Grep
---

# /read-doc

This skill reads the project's `llmdoc` documentation and provides a comprehensive summary to help understand the project quickly.

## Pre-fetched Context

- **Doc index:** !`cat llmdoc/index.md 2>/dev/null || echo "No llmdoc found"`
- **Doc structure:** !`find llmdoc -name "*.md" 2>/dev/null | head -200 || echo "No llmdoc directory"`

## Actions

1. **Step 1: Check Documentation Exists**
   - If `llmdoc/` directory doesn't exist, inform the user and suggest running `/tr:initDoc` first.

2. **Step 2: Read Index**
   - Read `llmdoc/index.md` to understand the documentation structure.

3. **Step 3: Read Overview Documents**
   - Read all documents in `llmdoc/overview/` to understand the project's purpose and context.

4. **Step 4: Scan Architecture & Guides**
   - Scan `llmdoc/architecture/` for system design information.
   - Scan `llmdoc/guides/` for available workflows.

5. **Step 5: Generate Summary**
   - Provide a concise summary including:
     - Project purpose and main features
     - Key architectural components
     - Available guides and workflows
     - Important references

Output the summary directly to the user in a well-structured format.
