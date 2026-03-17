---
name: 2-categorize-files
description: Second step in building instruction context for codebase
---

You are a senior developer responsible for categorizing every file in the codebase. You’ve been informed that the project is defined as: ./{output-folder}/1-techstack.md (read this file first)

Your task:

- Visit every file in the codebase. You may ignore dependency files, for example if it is a js file, you may ignore node_modules
- Categorize each file based on its role, such as: react-components, utility-functions, hooks, types, etc.

Output the file-categorization as a JSON file at:
./{output-folder}/2-file-categorization.json

```json
{
  "react-components": ["./src/components/Button.tsx"],
  "hooks": ["./src/hooks/useUser.ts"]
}
```

A single file can appear in multiple categories if appropriate.

> This task may take some time — that is expected and acceptable.
> Do **not** skip files or produce partial results due to time or complexity. Accuracy and completeness are **mission-critical**.
> If a file is listed in ./{output-folder}/2-file-categorization.json or is part of a relevant domain, it **must** be included in your analysis.
> Do not optimize for speed or brevity. This instruction is not optional — the success of this step depends on full and accurate coverage.

You are permitted to take as long as necessary to:

- Review every relevant file
- Extract actual patterns and conventions
- Produce complete, high-fidelity output

After writing ./{output-folder}/2-file-categorization.json, continue to skill 3-identify-architecture and proceed accordingly with {output-folder} as the `output-folder`.