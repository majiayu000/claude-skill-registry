---
name: todo-skill
description: A skill to break large tasks into smaller actionable steps, optimize execution for each step, and dynamically adapt based on progress.
---

# To-Do Skill

This skill enables the assistant to break down a large task into smaller tasks, create an optimized execution plan, and dynamically adjust actions based on progress and new information.

## Features
- **Task Breakdown**: Automatically decompose a complex request into smaller, actionable sub-tasks.
- **Execution Optimization**: Analyze and plan how to execute each step better before proceeding.
- **Adaptive Progress**: Dynamically adjust to-do lists based on feedback or results from completed tasks.
- **Visual To-Do List**: Provide a clear and interactive to-do list for tracking and managing progress.
- **Priority Management**: Prioritize tasks based on importance, deadlines, or complexity.

## Workflow
1. **Input -** User specifies a high-level task or goal.
2. **Breakdown -** Skill breaks the task down into sub-tasks using logical order.
3. **Optimization -** Each task is optimized for execution, identifying dependencies, tools, and strategies.
4. **Execution and Update -** Execute tasks one by one while adjusting the plan dynamically based on progress.
5. **Output -** Provide status updates and final results with a review of completed sub-tasks.

## Usage
- **Add Task:**
  Say "Plan and execute [TASK] step by step."
- **Check Progress:**
  Say "What is the status of [TASK]?"
- **Update Task:**
  Say "Update step [STEP NUMBER] of [TASK]."

## Example Interaction
User: "Plan and execute a marketing campaign."

Assistant:
- Step 1: Define the target audience.
- Step 2: Create marketing materials.
- Step 3: Schedule and launch the campaign.
- Step 4: Collect and analyze feedback.

Shall we start with Step 1?

User: "Yes, continue with Step 1."

Assistant: "For Step 1, let us first research the ideal demographic profile for our product. I'll document my findings."

...