---
name: executing-plans
description: "Controlled batch execution of implementation plans with review checkpoints between phases. Loads plan, critically reviews for issues, executes tasks in batches, then pauses for architect feedback before continuing. Use when you have a complete implementation plan from brainstorming/writing-plans and want structured execution with quality gates. Do NOT use for ad-hoc implementation, exploratory coding, or when you don't have a formal plan - just implement directly with code review at the end."
inputs:
  - from: pop-writing-plans
    field: plan_path
    required: true
  - from: any
    field: batch_size
    required: false
outputs:
  - field: tasks_completed
    type: number
  - field: verification_status
    type: string
  - field: github_issue
    type: issue_number
next_skills:
  - pop-finishing-a-development-branch
  - pop-session-capture
workflow:
  id: executing-plans
  name: Plan Execution Workflow
  version: 1
  description: Batch execution with review checkpoints
  steps:
    - id: load_plan
      description: Load and parse implementation plan
      type: agent
      agent: code-explorer
      next: review_plan
    - id: review_plan
      description: Critically review plan for issues
      type: agent
      agent: code-architect
      next: concerns_decision
    - id: concerns_decision
      description: Address any plan concerns
      type: user_decision
      question: "Found concerns with the plan. How should we proceed?"
      header: "Concerns"
      options:
        - id: no_concerns
          label: "No concerns"
          description: "Plan looks good, proceed"
          next: execute_batch
        - id: clarify
          label: "Need clarification"
          description: "Have questions before starting"
          next: clarify_plan
        - id: revise
          label: "Revise plan"
          description: "Plan needs updates first"
          next: revise_plan
      next_map:
        no_concerns: execute_batch
        clarify: clarify_plan
        revise: revise_plan
    - id: clarify_plan
      description: Get clarification on plan questions
      type: skill
      skill: pop-brainstorming
      next: execute_batch
    - id: revise_plan
      description: Revise the implementation plan
      type: skill
      skill: pop-writing-plans
      next: load_plan
    - id: execute_batch
      description: Execute current batch of tasks
      type: spawn_agents
      agents:
        - type: code-architect
          task: "Implement tasks in current batch"
        - type: test-writer-fixer
          task: "Run verification steps"
      wait_for: all
      next: batch_feedback
    - id: batch_feedback
      description: Report batch results and get feedback
      type: user_decision
      question: "Batch complete. How should I proceed?"
      header: "Feedback"
      options:
        - id: continue
          label: "Continue"
          description: "Looks good, proceed to next batch"
          next: check_remaining
        - id: revise
          label: "Revise"
          description: "I have feedback on this batch"
          next: apply_revisions
        - id: pause
          label: "Pause"
          description: "Stop here, I'll review more"
          next: pause_execution
      next_map:
        continue: check_remaining
        revise: apply_revisions
        pause: pause_execution
    - id: apply_revisions
      description: Apply feedback to current batch
      type: agent
      agent: code-architect
      next: execute_batch
    - id: pause_execution
      description: Pause and save progress
      type: skill
      skill: pop-session-capture
      next: complete
    - id: check_remaining
      description: Check if more tasks remain
      type: user_decision
      question: "Are there more tasks to execute?"
      header: "Remaining"
      options:
        - id: more
          label: "More tasks"
          description: "Continue with next batch"
          next: execute_batch
        - id: done
          label: "All done"
          description: "All tasks complete"
          next: final_verification
      next_map:
        more: execute_batch
        done: final_verification
    - id: final_verification
      description: Run final verification and tests
      type: skill
      skill: pop-finishing-a-development-branch
      next: next_action
    - id: next_action
      description: Decide next action after completion
      type: user_decision
      question: "What would you like to do next?"
      header: "Next Action"
      options:
        - id: another_issue
          label: "Another issue"
          description: "Work on another GitHub issue"
          next: fetch_issues
        - id: run_checks
          label: "Run checks"
          description: "Run tests or quality checks"
          next: run_checks
        - id: exit
          label: "Exit"
          description: "Save state and exit"
          next: save_and_exit
      next_map:
        another_issue: fetch_issues
        run_checks: run_checks
        exit: save_and_exit
    - id: fetch_issues
      description: Fetch prioritized open issues
      type: skill
      skill: pop-knowledge-lookup
      next: complete
    - id: run_checks
      description: Run test suite and quality checks
      type: agent
      agent: test-writer-fixer
      next: next_action
    - id: save_and_exit
      description: Save session state for later
      type: skill
      skill: pop-session-capture
      next: complete
    - id: complete
      description: Plan execution workflow complete
      type: terminal
---

# Executing Plans

## Overview

Load plan, review critically, execute tasks in batches, report for review between batches.

**Core principle:** Batch execution with checkpoints for architect review.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

## The Process

### Step 1: Load and Review Plan

1. Read plan file
2. Review critically - identify any questions or concerns about the plan
3. If concerns: Raise them with your human partner before starting
4. If no concerns: Create TodoWrite and proceed

### Step 2: Execute Batch

**Default: First 3 tasks**

For each task:

1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. Mark as completed

### Step 3: Report

When batch complete:

- Show what was implemented
- Show verification output
- Use AskUserQuestion for feedback:

```
Use AskUserQuestion tool with:
- question: "Batch complete. How should I proceed?"
- header: "Feedback"
- options:
  - label: "Continue"
    description: "Looks good, proceed to next batch"
  - label: "Revise"
    description: "I have feedback on this batch first"
  - label: "Pause"
    description: "Stop here, I'll review more carefully"
- multiSelect: false
```

### Step 4: Continue

Based on selection:

- **Continue**: Execute next batch
- **Revise**: Wait for feedback, apply changes, then continue
- **Pause**: Stop execution, preserve progress

### Step 5: Complete Development

After all tasks complete and verified:

- Announce: "I'm using the finishing-a-development-branch skill to complete this work."
- Use finishing-a-development-branch skill
- Follow that skill to verify tests, present options, execute choice

### Step 6: Next Action Loop (CRITICAL - Issue #118)

**After completion, ALWAYS present next actions:**

```
Use AskUserQuestion tool with:
- question: "What would you like to do next?"
- header: "Next Action"
- options:
  - label: "Work on another issue"
    description: "Continue with another GitHub issue"
  - label: "Run tests/checks"
    description: "Run test suite or quality checks"
  - label: "Session capture and exit"
    description: "Save state for later continuation"
- multiSelect: false
```

**NEVER end execution without presenting next step options.**

If user selects "Work on another issue", fetch prioritized open issues:

```bash
gh issue list --state open --milestone v1.0.0 --json number,title,labels --limit 5
```

Then present specific issue options via AskUserQuestion.

## When to Stop and Ask for Help

**STOP executing immediately when:**

- Hit a blocker mid-batch (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

## PDF Input Support

Plans can be provided as PDF files:

```
User: Execute this plan: /path/to/implementation-plan.pdf
```

**Process PDF plans:**

1. Use Read tool to analyze the PDF content
2. Extract tasks, steps, and verification criteria
3. Convert to internal task list format
4. Proceed with standard execution process

**When reading plan PDFs:**

- Look for: numbered tasks, code blocks, file paths
- Extract: exact commands, expected outputs
- Note: dependencies between tasks
- Identify: verification steps for each phase

PRD PDFs can also be processed to understand requirements context before execution.

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**

- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking

**Don't force through blockers** - stop and ask.

## Remember

- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Between batches: just report and wait
- Stop when blocked, don't guess
