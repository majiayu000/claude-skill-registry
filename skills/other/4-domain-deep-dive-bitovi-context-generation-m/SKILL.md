---
name: 4-domain-deep-dive
description: Fourth step in building instruction context for codebase
---


> This task may take some time — that is expected and acceptable.
>
> Do **not** skip files or produce partial results due to time or complexity. Accuracy and completeness are **mission-critical**.
>
> You are permitted to take as long as necessary to:
>
> - Review every relevant file
> - Extract actual patterns and conventions
> - Produce complete, high-fidelity output
>
> Do not optimize for speed or brevity. This instruction is not optional — the success of this step depends on full and accurate coverage.

For each of the domains listed in ./{output-folder}/3-architecture-domains.json, you're analyzing the codebase to understand how it implements the architectural domain: "{domain}".

The tech stack is summarized in ./{output-folder}/1-techstack.md.

Your Task:

- Examine relevant files for this domain.
- Identify consistent patterns, tools, conventions, and practices.
- Include real code examples that reflect actual usage in the codebase.
- Focus on what the project is doing — not what it should do.

Write your findings to: `./{output-folder}/4-domains/{domain}.md`

Requirements:

- If code snippets are included, use exact code examples from project files.
- Do not invent recommendations or include external best practices.
- Only describe what is actually used in this project.

Your goal is to document how the "{domain}" domain is implemented within this specific codebase in such a way that anyone could leverage or add features to it.

After writing each of the domain files, continue to skill 5-styleguide-generation and proceed accordingly with {output-folder} as the `output-folder`.