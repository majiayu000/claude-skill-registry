---
name: doc-create-readme-for-gamma
description: "{{ ƔƔƔ }} Generate a README for a specific directory"
model: sonnet
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Write"]
argument-hint: [path/to/directory]
---

Generate a README.md for the following directory:

```
$ARGUMENTS
```

## Steps

1. Confirm the directory exists; if not, stop and report
2. Analyse the directory: purpose, contents, file structure, key modules, any existing docs
3. Look at surrounding context — parent README, sibling directories, project-level docs — to understand how this directory fits into the broader codebase
4. Determine appropriate README sections based on what the directory contains:
   - **Library/module:** overview, API, usage examples, exports
   - **Config/infra:** what it configures, how to modify, dependencies
   - **Commands/scripts:** what each does, arguments, examples
   - **General:** overview, structure, key files, usage notes
5. Generate README content:
   - Clear description of the directory's purpose
   - Code blocks for any commands or usage examples
   - Table of contents if more than 4 sections
   - Links to related docs where relevant
6. Show draft for approval before writing

## Notes

- Keep it proportional to the directory's complexity — don't over-document a simple folder
- Focus on what someone new to the directory needs to know
- Include actual paths and commands, not placeholders
- Match the style of any existing project READMEs
