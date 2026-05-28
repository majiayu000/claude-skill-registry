---
name: task-test
description: Test skill that exercises the Task tool system to create and manage tasks
allowed-tools: TaskCreate TaskUpdate TaskList Glob Bash
model: sonnet
---

# Task System Test Skill

This skill exercises the Task tool system. You _MUST_ use TaskCreate, TaskUpdate, and TaskList to manage tasks. Set awn owner for the tasks to "haiku".

## Instructions

**Step 1: Create tasks IN PARALLEL** (all three TaskCreate calls in one response):

- TaskCreate: subject="List Go files", description="Count the number of \*.go files", activeForm="Listing Go files"
- TaskCreate: subject="Check formatting", description="Run go fmt on all the files", activeForm="Checking formatting"
- TaskCreate: subject="Count lines", description="Count # of lines in \*.go files", activeForm="Counting lines"

**Step 2: List tasks** to see what was created.

**Step 3: Complete each task**

Summarize results.
