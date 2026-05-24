---
name: meta-protocol-writer
description: Generates a PROSPERO-compliant Meta-analysis protocol based on Title and PICOS. Use when the user wants to write a protocol for a systematic review or meta-analysis.
license: MIT
skill-author: AIPOCH
---
# Meta Protocol Writer

This skill helps users generate a standard protocol for PROSPERO registration (without the registration number) for a Meta-analysis or Systematic Review.

## When to Use

- Use this skill when you need generates a prospero-compliant meta-analysis protocol based on title and picos. use when the user wants to write a protocol for a systematic review or meta-analysis in a reproducible workflow.
- Use this skill when a protocol design task needs a packaged method instead of ad-hoc freeform output.
- Use this skill when the user expects a concrete deliverable, validation step, or file-based result.
- Use this skill when `scripts/utils.py` is the most direct path to complete the request.
- Use this skill when you need the `meta-protocol-writer` package behavior rather than a generic answer.

## Key Features

- Scope-focused workflow aligned to: Generates a PROSPERO-compliant Meta-analysis protocol based on Title and PICOS. Use when the user wants to write a protocol for a systematic review or meta-analysis.
- Packaged executable path(s): `scripts/utils.py`.
- Reference material available in `references/` for task-specific guidance.
- Structured execution path designed to keep outputs consistent and reviewable.

## Dependencies

- `Python`: `3.10+`. Repository baseline for current packaged skills.
- `Third-party packages`: `not explicitly version-pinned in this skill package`. Add pinned versions if this skill needs stricter environment control.

## Example Usage

```bash
cd "20260316/scientific-skills/Protocol Design/meta-protocol-writer"
python -m py_compile scripts/utils.py
python scripts/utils.py --help
```

Example run plan:
1. Confirm the user input, output path, and any required config values.
2. Edit the in-file `CONFIG` block or documented parameters if the script uses fixed settings.
3. Run `python scripts/utils.py` with the validated inputs.
4. Review the generated output and return the final artifact with any assumptions called out.

## Implementation Details

See `## Workflow` above for related details.

- Execution model: validate the request, choose the packaged workflow, and produce a bounded deliverable.
- Input controls: confirm the source files, scope limits, output format, and acceptance criteria before running any script.
- Primary implementation surface: `scripts/utils.py`.
- Reference guidance: `references/` contains supporting rules, prompts, or checklists.
- Parameters to clarify first: input path, output path, scope filters, thresholds, and any domain-specific constraints.
- Output discipline: keep results reproducible, identify assumptions explicitly, and avoid undocumented side effects.

## Workflow

Follow these steps to generate the protocol.

### 1. Validate Title

Check if the user provided a title.
- If **Title is missing**: Ask the user to provide a title or suggest one based on PICOS if provided.
- If **Title is present**: Validate it using the **Title Review Rules** (see below).

**Title Review Rules**:
- Must contain "Meta-analysis" or "Systematic review".
- Must cover PICOS elements (Population, Intervention, Comparison, Outcome).
- Must be concise (< 25 words).

If the title fails validation, explain why and ask for a revised title.

### 2. Gather Inputs

Ensure you have the following information (PICOS):
- **Participants** (P)
- **Interventions** (I)
- **Comparisons** (C)
- **Outcomes** (O)

If any are missing, ask the user.

### 3. Generate Protocol Sections

Use the prompts in `references/prompts.md` to generate the three main sections. You must follow the content requirements and word counts strictly.

#### Step 3.1: Administrative Information
- Use the **Administrative Information Prompt** in `references/prompts.md`.
- Inputs: Validated Title, Author information (if known, else use placeholders).

#### Step 3.2: Introduction
- Use the **Introduction Prompt** in `references/prompts.md`.
- Inputs: PICOS.
- Constraints: Rationale (5-150 words), Objectives (10-200 words).

#### Step 3.3: Methods
- Use the **Methods Prompt** in `references/prompts.md`.
- Inputs: PICOS.
- **Critical**: For the Search Strategy, use the **Current Date** as the end date.
  - You can run `python scripts/utils.py` to get the exact current date if needed, or just use today's date known to you.
  - Start date must be "inception". Do NOT set a specific start year (e.g., 2000) unless requested.

### 4. Final Output

Combine the sections into a single Markdown document.

Structure:
1.  **Administrative Information**
2.  **Introduction**
3.  **Methods**

Ensure all headings match the PROSPERO requirements.
