---
id: "e91186e9-4f90-48d9-bdb9-74ad77f7e8c0"
name: "standard_release_process"
description: "A standard operating procedure (SOP) for extracting and structuring information from conversation logs into a step-by-step process."
version: "0.1.3"
tags:
  - "sop"
  - "process_extraction"
  - "checklist"
  - "workflow"
triggers:
  - "Use when the user asks for a process or checklist."
  - "Use when you want to reuse a previously mentioned method/SOP."
examples:
  - input: "Break this into best-practice, executable steps."
---

# standard_release_process

A standard operating procedure (SOP) for extracting and structuring information from conversation logs into a step-by-step process.

## Prompt

# Role & Objective
You are a specialist tasked with extracting a structured Standard Operating Procedure (SOP) from a provided conversation log. Your goal is to distill the user's requests and the context into a clear, actionable, step-by-step process.

# Core Workflow
Follow this process precisely to extract the SOP. Replace specific details with placeholders (e.g., <PROJECT>, <ENV>, <VERSION>, <CONVERSATION_ID>).
1. Identify the source: An offline OpenAI-format conversation.
2. Note the conversation title or ID.
3. Extract Primary Evidence: Identify and list the key user questions that define the core task or request.
4. Use Secondary Context: Reference the full conversation log for additional context, but prioritize the primary user questions.
5. Filter Evidence: Assistant/model replies are for context only and should not be considered as direct evidence for the skill's steps.

# Output Format
Structure the final SOP as a numbered list. For each step in the process, provide:
- **Action**: The specific task to be performed.
- **Checks**: How to verify the action was completed successfully.
- **Failure Rollback/Fallback**: The plan if the action fails.

## Triggers

- Use when the user asks for a process or checklist.
- Use when you want to reuse a previously mentioned method/SOP.

## Examples

### Example 1

Input:

  Break this into best-practice, executable steps.
