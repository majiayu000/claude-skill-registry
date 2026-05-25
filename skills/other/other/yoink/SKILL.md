---
name: yoink
description: "Curate tests then decompose dependencies"
argument-hint: "PROMPT [--url GITHUB_URL] [--package PACKAGE_NAME] [--skip-test-discoverer]"
---

# Yoink

> **Python only.** YOINK currently only supports Python packages. If the target is clearly not a Python package, inform the user and exit immediately.

Run the full yoink decomposition pipeline by invoking skills in sequence:

### 1. Setup

Invoke `/yoink:setup $ARGUMENTS` to scaffold the project (clone repo, install library).

**Wait for setup to complete before proceeding.**

### 2. Test Curation

Invoke `/yoink:curate-tests $ARGUMENTS` to discover and generate tests, validate against the real library, rewrite imports, and sanity check.

**Wait for test curation to complete before proceeding.**

### 3. Dependency Decomposition

Invoke `/yoink:decompose $ARGUMENTS` to run the decomposition loop.
