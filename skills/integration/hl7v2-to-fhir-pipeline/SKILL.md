---
name: hl7v2-to-fhir-pipeline
description: Comprehensive pipeline for creating a new message converter or add/edit a field mapping for an existing converter.
---

# HL7v2->fhir Module Extension

Your job is to extend the conversion module according to user's request.

If the user request is not related to creating a new message converter, a new field mapping, or adapting the existing conversion to new message examples - return an error.

## Rules

- You are the orchestrator agent. You perform work by creating sub-agents for each step in the pipeline.
- Only you can interact with the user. If a sub-agent needs user-input, it can stop and return questions. You must resume the sub-agent with provided user feedback if it didn't finish its step.
  - IMPORTANT: if user starts to discuss a question that is related to the work a sub-agent is doing, you act like a proxy and let the sub-agent answer user's questions or concerns. Don't pollute your context by thinking about a specific task the sub-agent is doing.
- If user points you to specific directory in `ai/tickets/converter-skill-tickets/`, you work there, resuming the last step or starting with the Step 1 if no work has been done.
- Between steps, your only job is to commit and move to the next step. Do NOT present, summarize, or ask the user about content from the ticket document when it's not explicitly required by a sub-agent (when it returns `NEED_USER_INPUT`).
- **CRITICAL**: NEVER USE PROVIDED EXAMPLE MESSAGES UNCHANGED. ALWAYS DE-IDENTIFY THEM BY CHANGING NAMES, DATES AND NUMERIC IDS.

## Pipeline

### Step 1

- Create a folder in `ai/tickets/converter-skill-tickets/` that stands for the name of the change user needs (unless user instructed you to work in a specific directory).
- Create a ticket file that will contain all the collected work by the sub-agents: `ai/tickets/converter-skill-tickets/<the-ticket-name>/ticket.md`
- Fill the ticket with the high-level description of the goal ("# Goal" section)
- Create a sub-folder `/examples` in the ticket directory. 
- Ask user to put example messages in the examples directory.
- If user explicitly said they don't have real examples, run a sub-agent to generate the examples.
The sub-agent prompt:
```
Generate 5 examples of <related-hl7v2-message> messages in `ai/tickets/converter-skill-tickets/<the-ticket-name>/examples/`
Use skill hl7v2-info to read the hl7v2 spec and generate examples, conforming to the spec:
- 3 messages conforming to 2.5
- 2 messages configming to 2.8.2
Each examples must have its own file.
```
- Specify the path to example messages in the ticket
- Commit the files.

### Step 2

Run a sub-agent to explore the hl7v2 spec and mappings and make a requirements document. The prompt is located in file named `requirements-prompt.md` in the skill directory.

Commit the changed files once the sub-agent finished.

### Step 3

Run a sub-agent to explore the codebase, existing conversion logic, note what's already done, what's missing, and what patterns/structures can be helpful to re-use for the implementation. The prompt is located in file named `explore-prompt.md` in the skill directory.

Commit the changed files once the sub-agent finished.

### Step 4

Spawn a sub-agent to write the design to satisfy the requirements given the existing codebase. If the sub-agent returns `NEED_USER_INPUT` marker, you must ask the user this question and then **resume** the sub-agent that asked this question to continue its work. The prompt is located in file named `design-prompt.md` in the skill directory.

Commit the changed files once the sub-agent finished.

### Step 5 

Run a sub-agent with `ai-review` skill to review the design.

Prompt:
```
/ai-review <path-to-ticket-file>
```

After the review agent finished, **resume** the design agent to address findings and remove the AI Review Notes section. You only do this once. Do not run subsequent reviews after one was completed.

Commit the changes.

###  Step 6

Run a sub-agent to make the plan. The prompt is located in file named `planning-prompt.md` in the skill directory.

Commit the changes.

### Step 7

Iteratively run 1 sub-agent to implement 1 task using prompt from `implementation-prompt.md` file in the skill directory.

After each task is completed, commit the changes and run the next sub-agent until all tasks are done.

When all tasks are completed, move to the next step.

### Step 8

Run a sub-agent to review the implementation.

Prompt:
```
/ai-review implementation of <path-to-ticket-file>. Think hard. Return your review output as your response, do not change any files. 
```

If the review agent returned any issues, spawn a sub-agent to fix them.

Prompt:
```
Get familiar with <path-to-ticket-file>. A review of this implementation revealed issues you need to address:

<review-agent-output>
```

When the review and the fixes are done, your job is done. Report to the user the implementation is complete, they can test the functionality in the ui.
