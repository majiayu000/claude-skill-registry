---
name: orchestrating-parallel-tasks
description: Decomposes complex or large-scale requirements into discrete, mutually exclusive sub-tasks that can be executed in parallel by multiple agents. Use when a task is described as an "epic", spans multiple architectural layers, or would benefit from concurrent development to reduce time-to-completion.
---

# SOP: Orchestrating Parallel Tasks

## Purpose

Provides a systematic workflow for breaking down "epic-level" requirements into independent sub-tasks. This approach maximizes agent efficiency, enables parallel execution, and minimizes merge conflicts by ensuring clear functional and file-level boundaries.

## Workflow Checklist

- [ ] **Step 1: Contextual Analysis**
  - [ ] Identify high-level architectural layers involved (UI, API, Data, Auth, etc.).
  - [ ] List existing files likely to be impacted.
  - [ ] Identify external dependencies (Third-party APIs, DB schemas).
- [ ] **Step 2: Boundary Identification & Slicing**
  - [ ] Apply **Vertical Slicing** to group features by user value.
  - [ ] Apply **Interface-First** slicing for shared components.
  - [ ] Identify "Shared Core" vs. "Independent Leaves".
- [ ] **Step 3: Mutual Exclusivity Enforcement**
  - [ ] Verify that no two sub-tasks target the same set of files for modification.
  - [ ] Decouple shared utilities into their own prerequisite task.
  - [ ] Define mock interfaces for cross-task dependencies.
- [ ] **Step 4: Sub-Task Specification**
  - [ ] Draft a clear "Acceptance Criteria" for each sub-task.
  - [ ] Define the "MVP Slice" for each task.
  - [ ] Map out the dependency graph (which tasks must finish before others start).
- [ ] **Step 5: User Validation**
  - [ ] Present the phased plan and task list to the user for approval.

## Detailed Instructions

### 1. Vertical Slicing vs. Horizontal Slicing

When decomposing, prefer **Vertical Slicing**. Instead of "Frontend Task" and "Backend Task" (Horizontal), aim for "User Login Flow" (Vertical) which includes UI, API, and DB changes. This allows an agent to deliver end-to-end value independently.

### 2. The Mutual Exclusivity Rule

To enable parallel execution:

- **File Isolation**: If Task A and Task B both need to edit `src/utils.ts`, they are NOT mutually exclusive. Extract the shared changes into a `Task 0: Preparation` or sequence them.
- **State Isolation**: Ensure sub-tasks don't depend on shared global state that is being modified concurrently without a locking mechanism or interface.

### 3. Interface-First Development

If Task B depends on the output of Task A, define the interface (API contract, Typescript interface, or DB schema) as the first step. Once the interface is defined and committed, Task A and Task B can proceed in parallel using mocks or stubs.

## Success Criteria

- All sub-tasks have non-overlapping primary file sets.
- Each sub-task has its own test plan and acceptance criteria.
- The dependency graph is acyclic and minimizes sequential bottlenecks.
- The breakdown is presented in a way that an agent can pick up any "Ready" task and execute it without further clarification.
