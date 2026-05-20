---
name: doc-create-readme-omega
description: "{{ 𝛀𝛀𝛀 }} Generate a comprehensive README.md from project analysis"
model: opus
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Write"]
---

Analyze project structure, code, and existing docs to generate an accurate README.md.

## Steps
1. Analyze project: name, purpose, tech stack, directory structure, build system, key features
2. Determine README sections: overview, features, prerequisites, installation, usage, configuration, structure, development, doc links
3. Generate README content:
    - Clear project description
    - Code blocks for commands
    - Table of contents if long
    - Link to docs/ for details
4. Show for approval; backup existing README if present

## Structure

```md
# Project Name
[One-line description]
## Overview / ## Features / ## Prerequisites / ## Installation / ## Usage
## Configuration / ## Project Structure / ## Development / ## Documentation / ## License
```

## Notes
- Keep brief - README is overview, not full docs
- Focus on "getting started" info
- Include actual commands, not placeholders
