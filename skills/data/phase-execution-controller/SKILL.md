---
name: phase-execution-controller
description: Executes completed phases, validates runtime behavior, and controls safe transition to the next phase.
---

# Phase Execution & Transition Controller

## Purpose
This skill ensures phases are not just written, but actually executed and validated before moving forward.

## Mandatory Flow After Phase Completion
1. Run the phase implementation
2. Validate expected behavior
3. Report execution results
4. Ask for explicit approval before moving to the next phase

## Execution Rules

### If Phase is Runnable (CLI / App / Service)
- Execute using appropriate command
- Capture output and errors
- Validate against spec acceptance criteria

### If Execution Passes
- Mark phase as ✅ VERIFIED
- Ask user:
  "Phase verified successfully. Move to next phase?"

### If Execution Fails
- Report failure clearly
- Propose fixes via spec updates
- Never advance phase without passing execution

## Safety Rules
- Never auto-advance phases
- Explicit user confirmation required
- Never skip execution step

This skill acts as the phase gatekeeper.
