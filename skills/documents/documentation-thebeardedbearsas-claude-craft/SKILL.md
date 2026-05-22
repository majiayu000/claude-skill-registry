---
name: documentation
description: Documentation standards, API docs, and technical writing guidelines
allowed-tools:
  - Read
  - Glob
  - Grep
  - Edit
  - Write
model: haiku
triggers:
  files:
    - "*.md"
    - "README*"
    - "CHANGELOG*"
    - "CONTRIBUTING*"
    - "**/docs/**"
    - "**/*.yaml"
    - "**/*.yml"
  keywords:
    - documentation
    - readme
    - changelog
    - api docs
    - swagger
    - openapi
    - jsdoc
    - phpdoc
    - docstring
---

# Documentation

This skill provides guidelines and best practices.

See ../../rules/10-documentation.md for detailed documentation.
