---
name: basic-research-design
description: A biomedical research topic designer that generates progressive experimental subtitles and detailed research outlines based on a given subject. Use when the user wants to design a research proposal, outline experiments for a topic, or structure a biomedical study.
license: MIT
skill-author: AIPOCH
---
# Basic Research Topic Design

This skill helps users design a biomedical research topic by generating progressive subtitles and a detailed experimental outline.

## When to Use

- Use this skill when the request matches its documented task boundary.
- Use it when the user can provide the required inputs and expects a structured deliverable.
- Prefer this skill for repeatable, checklist-driven execution rather than open-ended brainstorming.

## Key Features

- Scope-focused workflow aligned to: A biomedical research topic designer that generates progressive experimental subtitles and detailed research outlines based on a given subject. Use when the user wants to design a research proposal, outline experiments for a topic, or structure a biomedical study.
- Documentation-first workflow with no packaged script requirement.
- Reference material available in `references/` for task-specific guidance.
- Structured execution path designed to keep outputs consistent and reviewable.

## Dependencies

- `Python`: `3.10+`. Repository baseline for current packaged skills.
- `Third-party packages`: `not explicitly version-pinned in this skill package`. Add pinned versions if this skill needs stricter environment control.

## Example Usage

```text
Skill directory: 20260316/scientific-skills/Protocol Design/basic-research-design
No packaged executable script was detected.
Use the documented workflow in SKILL.md together with the references/assets in this folder.
```

Example run plan:
1. Read the skill instructions and collect the required inputs.
2. Follow the documented workflow exactly.
3. Use packaged references/assets from this folder when the task needs templates or rules.
4. Return a structured result tied to the requested deliverable.

## Implementation Details

See `## Workflow` above for related details.

- Execution model: validate the request, choose the packaged workflow, and produce a bounded deliverable.
- Input controls: confirm the source files, scope limits, output format, and acceptance criteria before running any script.
- Primary implementation surface: instruction-only workflow in `SKILL.md`.
- Reference guidance: `references/` contains supporting rules, prompts, or checklists.
- Parameters to clarify first: input path, output path, scope filters, thresholds, and any domain-specific constraints.
- Output discipline: keep results reproducible, identify assumptions explicitly, and avoid undocumented side effects.

## Workflow

Follow these steps to generate the research design.

### Step 1: Generate Subtitles

1.  Identify the **Subject** (keywords) from the user's request (e.g., "PD-1 in lung cancer").
2.  Use the **Subtitle Generation Prompt** (see `references/prompt_templates.md`) to generate 6 progressive subtitles.
3.  **Input for Prompt**:
    *   `<Subject>`: The user's subject.

### Step 2: Generate Research Outline

1.  Take the **Subject** and the **Subtitles** generated in Step 1.
2.  Use the **Research Outline Generation Prompt** (see `references/prompt_templates.md`) to generate the detailed outline.
3.  **Input for Prompt**:
    *   `<Subject>`: The original subject.
    *   `<Subtitles>`: The output from Step 1.

### Quality Rules

*   **Progressive Logic**: Ensure the subtitles and experiments show a clear logical progression (screening -> verification -> mechanism -> in vivo).
*   **Specific Methods**: The outline must include specific experimental method names.
*   **No Summary**: Do not output a summary at the end.
*   **Exact Count**: Ensure exactly 6 subtitles are generated in Step 1.

## Output Format

Present the final result in Markdown, following the format specified in the prompt templates.

## When Not to Use

- Do not use this skill when the required source data, identifiers, files, or credentials are missing.
- Do not use this skill when the user asks for fabricated results, unsupported claims, or out-of-scope conclusions.
- Do not use this skill when a simpler direct answer is more appropriate than the documented workflow.

## Required Inputs

- A clearly specified task goal aligned with the documented scope.
- All required files, identifiers, parameters, or environment variables before execution.
- Any domain constraints, formatting requirements, and expected output destination if applicable.

## Output Contract

- Return a structured deliverable that is directly usable without reformatting.
- If a file is produced, prefer a deterministic output name such as `basic_research_design_result.md` unless the skill documentation defines a better convention.
- Include a short validation summary describing what was checked, what assumptions were made, and any remaining limitations.

## Validation and Safety Rules

- Validate required inputs before execution and stop early when mandatory fields or files are missing.
- Do not fabricate measurements, references, findings, or conclusions that are not supported by the provided source material.
- Emit a clear warning when credentials, privacy constraints, safety boundaries, or unsupported requests affect the result.
- Keep the output safe, reproducible, and within the documented scope at all times.

## Failure Handling

- If validation fails, explain the exact missing field, file, or parameter and show the minimum fix required.
- If an external dependency or script fails, surface the command path, likely cause, and the next recovery step.
- If partial output is returned, label it clearly and identify which checks could not be completed.

## Quick Validation

Run this minimal verification path before full execution when possible:

```text
No local script validation step is required for this skill.
```

Expected output format:

```text
Result file: basic_research_design_result.md
Validation summary: PASS/FAIL with brief notes
Assumptions: explicit list if any
```
