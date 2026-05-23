---
name: 6-build-instructions
description: Final step in building instruction context for codebase
---

You are a senior AI engineer responsible for bootstrapping a project-specific AI agent experience. The goal is to generate a markdown instruction file at:

`{final_output_file}`

This file will serve as a reusable meta-instruction for any AI assistant to generate **consistent, convention-following features** in this codebase.

You must synthesize the following source materials:

- `./{output-folder}/1-techstack.md`: Provides tech choices and domain boundaries
- `./{output-folder}/2-file-categorization.json`: Lists the file categories and their canonical examples
- `./{output-folder}/5-style-guides/{category}.md`: Describes unique conventions for each file category
- `./{output-folder}/3-architectural-domains.json`: Defines how domains like `ui`, `routing`, `data-layer`, etc. are implemented, along with constraints and required patterns

---

## Your Output: `{final_output_file}`

This file must include:

---

### 1. **Overview Section**

Explain the purpose of this file:

- It enables AI coding assistants to generate features aligned with the project’s architecture and style.
- It is based only on actual, observed patterns from the codebase — not invented practices.

---

### 2. **File Category Reference**

For each category in `2-file-categorization.json`:

- Explain what it is
- List 1–2 representative file examples
- Summarize key conventions based on its corresponding `5-style-guides/{category}.md`

---

### 3. **Feature Scaffold Guide**

Define how to plan and implement a new feature. Include:

- How to determine which categories of files to create
- Where to place those files
- How to follow naming and structure conventions
- Example: what files to create for a new component, a hook, or an API integration

This section should refer to actual conventions in the project (e.g., if Storybook is used, include `*.stories.tsx`; if styles are colocated `.module.css`, mention that).

---

### 4. **Integration Rules**

From `3-architectural-domains.json`, summarize constraints like:

- "All canvas logic must use `useCanvas`"
- "Components must use shared tokens from the design-system"
- "API requests go through `apiClient.ts` pattern"

This prevents LLMs from generating non-compliant or inconsistent files.

---

### 5. **Example Prompt Usage**

Show how a user could prompt Copilot with a request like:

> "Create a searchable dropdown that lets users filter by category"

And have it respond with:

- `src/components/SearchableDropdown.tsx`
- `src/components/SearchableDropdown.module.css`
- `src/hooks/useSearchableDropdown.ts`
- `src/components/__tests__/SearchableDropdown.test.tsx`
- etc…

Only use categories and file types present in this project.

---

## ⚠️ Requirements

- **Do not** include invented best practices
- **Do not** list categories or conventions that aren’t supported by the codebase
- **Do not** omit any categories or domains defined in the analysis
- Maximum file lines: `{max_lines}`

If the file is more than `{max_lines}` lines, identify the most important information and distill it down to `${max_lines}` lines. It's important the file stays within the required limit.

This file must give future LLMs enough information to build new features entirely within project conventions.

To clarify further, if `{final_output_file}` already exists, overwrite it.
