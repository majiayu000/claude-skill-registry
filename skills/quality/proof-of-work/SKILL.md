---
name: proof-of-work
description: |
  Enforces "prove before claim" discipline - validation, testing, and evidence requirements before declaring work complete.
  Triggers: validation, definition-of-done, proof, acceptance-criteria, testing, completion, finished, done, working, should work, configured, ready to use, implemented, fixed, improvement validated, workflow optimized, performance improved, issue resolved.
  Use when claiming work is complete, recommending solutions, or finishing implementations.
  Do not use when asking questions or for work clearly in-progress.
  MANDATORY: This skill is required before any completion claim.
category: workflow-methodology
tags: [validation, testing, proof, definition-of-done, acceptance-criteria]
dependencies:
  - imbue:evidence-logging
tools: []
usage_patterns:
  - completion-validation
  - acceptance-testing
  - proof-generation
complexity: intermediate
estimated_tokens: 3000
modules:
  - modules/validation-protocols.md
  - modules/acceptance-criteria.md
  - modules/red-flags.md
  - modules/iron-law-enforcement.md
version: 1.3.5
---
# Proof of Work

## Table of Contents

- [Overview](#overview)
- [The Iron Law](#the-iron-law)
- [Usage Standards](#usage-standards)
- [Validation Protocol](#validation-protocol)
- [Integration](#integration)
- [Validation Checklist](#validation-checklist-before-claiming-done)
- [Red Flag Self-Check](#red-flag-self-check)
- [Exit Criteria](#exit-criteria)

## Overview

The "Proof of Work" methodology prevents premature completion claims by requiring technical verification before stating that a task is finished. For example, instead of assuming an LSP configuration functions after a restart, we verify that the server starts and that tools respond to queries. This approach confirms the solution works before the user attempts validation.

Before claiming completion, provide reproducible evidence of the solution's performance and address edge cases. All claims must be backed by actual command output captured in the current environment.

## The Iron Law

**NO IMPLEMENTATION WITHOUT A FAILING TEST FIRST**
**NO COMPLETION CLAIM WITHOUT EVIDENCE FIRST**
**NO CODE WITHOUT UNDERSTANDING FIRST**

The Iron Law prevents testing from becoming a perfunctory exercise. If an implementation is planned before tests are written, the RED phase fails to drive the design. Understand the technical rationale for an approach and its limitations before declaring it done. Before writing code, document evidence of the failure being addressed and confirm that tests are driving the implementation.

### Verification and TDD Workflow

Verify the fundamentals of the implementation and the reasons for choosing it over alternatives. Identify where a solution might fail rather than stating it should always work. The TDD cycle follows these mandatory steps:

1. **RED**: Write a failing test before implementation.
2. **GREEN**: Create a minimal implementation that passes the test.
3. **REFACTOR**: Improve the code without changing its behavior.

### Iron Law Self-Check

| Self-Check Question | If Answer Is Wrong | Action |
|---------------------|-------------------|--------|
| Do I have documented evidence of failure/need? | No | STOP - document failure first |
| Am I testing pre-conceived implementation? | Yes | STOP - let test DRIVE design |
| Am I feeling design uncertainty? | No | STOP - uncertainty is GOOD |
| Did test drive implementation? | No | STOP - doing it backwards |

### Iron Law Progress Tracking

- `proof:iron-law-red`: Failing test written before implementation.
- `proof:iron-law-green`: Minimal implementation passes test.
- `proof:iron-law-refactor`: Code improved without behavior change.
- `proof:iron-law-coverage`: Coverage gates passed (line, branch, and mutation).

Confirm that work passes all line, branch, and mutation coverage gates. For detailed enforcement patterns, see [iron-law-enforcement.md](modules/iron-law-enforcement.md).

## Usage Standards

Apply this skill before stating that work is "done," "finished," or "ready." Use it before recommending solutions or stating that a configuration "should work." Stop if you find yourself assuming a configuration is correct without testing it or recommending a fix without first reproducing the problem. Red flags include thinking "this looks correct" without actual verification. If you cannot explain each line of a configuration or why a specific practice applies to the current context, the necessary validation steps have been skipped.

## Validation Protocol

### Step 1: Reproduce the Problem (`proof:problem-reproduced`)

Before proposing a solution, verify the current state. Use tools like `ps`, `echo`, and `cat` to check running processes, environment variables, and configuration files. Document the failure with command output and error logs.

### Step 2: Test the Solution (`proof:solution-tested`)

Before claiming a solution works, execute it in the current environment. Capture the actual output and confirm that it matches expected behavior. Do not rely on assumed output.

### Step 3: Check for Known Issues (`proof:edge-cases-checked`)

Research known bugs and limitations related to the approach. Check GitHub issues, version compatibility, and official documentation to identify potential blockers or common pitfalls.

### Step 4: Capture Evidence (`proof:evidence-captured`)

Use `imbue:evidence-logging` to document the commands executed, their output, timestamps, and the conclusions drawn from each step.

### Step 5: Prove Completion (`proof:completion-proven`)

Define acceptance criteria and validate each item. If a blocker is identified, document the diagnosis with evidence and provide workaround options instead of claiming completion.

## Integration

### With Improvement Workflows

Use proof-of-work to validate improvement opportunities identified by `/update-plugins` or `/fix-workflow`. Document the baseline metrics (step count, failure rate, duration), test the proposed changes, and capture the improved metrics to demonstrate quantitative impact.

## Validation Checklist (Before Claiming "Done")

Verify that the problem was reproduced with evidence and the solution was tested in the actual environment. Research known issues and consider edge cases. Capture evidence in a reproducible format and confirm that all acceptance criteria are met. The completion statement must detail the specific tests run and their results, citing evidence for each claim.

## Red Flag Self-Check

Before sending a completion message, confirm that you have run the recommended commands and captured their output. Verify that you have researched known issues and that the validation steps are reproducible by the user. Ensure you are proving rather than assuming.

## Exit Criteria

Complete all progress tracking items. Create an evidence log with reproducible proofs. Define and validate acceptance criteria, and document any identified blockers.
