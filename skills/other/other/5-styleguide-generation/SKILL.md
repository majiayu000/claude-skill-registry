---
name: 5-styleguide-generation
description: Fifth step in building instruction context for codebase
---


> This task may take time — that is expected and required.

You are a senior software engineer responsible for generating style guides that explain what makes this codebase unique for each category listed in `./{output-folder}/2-file-categorization.json`. Given the best practices **and guidelines you create**, anyone should be able to create a file of that category that matches the existing conventions.

## Requirements

You must:

- Review **every individual file** listed under each category
- Identify only the **unique and distinctive patterns** that make this project stand out from standard conventions
- Focus on project-specific approaches, custom patterns, and non-standard implementations
- Create **one markdown file per category** highlighting only these unique conventions

⚠️ You must create a separate file for **each category**, with no omissions.

## Required Output Files

For example, if the categories are:

- `react-components`
- `api-clients`
- `hooks`

Then you must create:

- `./{output-folder}/5-style-guides/react-components.md`
- `./{output-folder}/5-style-guides/api-clients.md`
- `./{output-folder}/5-style-guides/hooks.md`

## Important Guidelines

- Do **not** skip a single category. Partial output is unacceptable.
- Do **not** include common industry patterns — only extract the conventions that are **unique to this specific codebase**.
- Do **not** invent patterns — only use what is observed in the codebase.

After writing each of the domain files, execute skill 6-build-instructions and proceed accordingly with {output-folder} as the `output-folder`.