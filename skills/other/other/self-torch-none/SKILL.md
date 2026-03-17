---
id: "e4369d96-8fae-4bba-b733-e8f90897db62"
name: "self / torch / none"
description: "General SOP for common requests related to self, torch, none."
version: "0.1.1"
tags:
  - "self"
  - "torch"
  - "none"
triggers:
  - "Use when the user asks for a process or checklist."
  - "Use when you want to reuse a previously mentioned method/SOP."
examples:
  - input: "Break this into best-practice, executable steps."
---

# self / torch / none

General SOP for common requests related to self, torch, none.

## Prompt

# Role & Objective
Follow this Standard Operating Procedure (SOP) to process requests by breaking them down into actionable steps. Replace specific details with placeholders like <PROJECT>/<ENV>/<VERSION>.

# Core Workflow
1. **Source Identification**: Use the specified offline OpenAI-format conversation source.
2. **Contextual Anchoring**: Reference the provided title and conversation ID for context.
3. **Evidence Hierarchy**:
   - **Primary Evidence**: Use the user questions provided as the main source for extraction.
   - **Secondary Context**: Use the full conversation transcript for additional reference. Note that assistant/model replies in this section are for reference only and not considered skill evidence.
4. **Stepwise Execution**: For each step in the process, clearly define:
   - **Action**: The task to be performed.
   - **Checks**: Validation criteria to ensure the action was successful.
   - **Failure Rollback/Fallback Plan**: The procedure to follow if the action or checks fail.

# Output Format
For each step number, provide:
- **Status/Result**: The outcome of the step.
- **Next Action**: What to do next based on the result.

## Triggers

- Use when the user asks for a process or checklist.
- Use when you want to reuse a previously mentioned method/SOP.

## Examples

### Example 1

Input:

  Break this into best-practice, executable steps.
