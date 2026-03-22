---
name: update-reqs
description: Add or update functional requirement documents in docs/requirements/
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo 'Updating project requirements...'"
          once: true
---

# Update Requirements

Add or update functional requirement documents that describe what the software must do. Requirements are implementation-agnostic. From these documents alone, a team could recreate the software in any language or framework without access to the current codebase.

## Scope

Requirement files live in `docs/requirements/`. Create files as needed based on the project's components.

| File | Coverage |
|------|----------|
| `project.md` | System-wide behavior, MCP tool contracts, subprocess management, data flow rules, cross-cutting constraints |

If the user specifies a component, only update that file. Otherwise update all applicable files.

## Core Rules

- **Append and update only.** NEVER remove a requirement. Requirements are a living record.
- **Mark, don't delete.** If a requirement no longer appears to match observed software behavior, set its status to `Warning` with a brief reason. Humans decide removal.
- **No implementation details.** No language, framework, library, file path, class name, function name, data structure, or internal architecture belongs in a requirement. Describe observable behavior and contracts between components.
- **No code, pseudocode, or structural examples.**
- **Each requirement is one testable statement.** If you cannot verify whether the software satisfies a requirement through its external behavior or documented contracts, it is too vague. If a requirement uses "and" to join two distinct behaviors, split it.
- **Be concise.** A requirement should rarely exceed two sentences. State the requirement directly.
- **Describe what, never how.** Say what outcome the system must produce, not what mechanism achieves it.

## Requirement File Format

```
# [Component] Requirements

## [Functional Area]

### REQ-[NNN]: [Short Title]
**Status**: Active | Warning
**Warning**: [reason this requirement may no longer apply - only present when status is Warning]

[Single requirement statement in plain prose. No bullets, sub-items, or conditional trees.]
```

Rules:
- Numbers are sequential per file starting at REQ-001
- Functional areas group related requirements under a shared heading
- New requirements append to the end of their functional area
- New functional areas append after existing ones
- A requirement's number never changes, even if requirements above it receive warnings

## Workflow

### 1. Explore Current Behavior

Launch parallel Explore subagents to understand what the software currently does. Focus on observable behavior and contracts, not implementation structure.

For **project.md**: What MCP tools are exposed, what each tool does, how subprocess management works, what safety guards exist, what timeouts and error handling guarantees exist, how the server behaves as an MCP endpoint.

### 2. Read Existing Requirements

Read all existing files in `docs/requirements/`. Note every current requirement number, status, and functional area. If a file does not exist, it will be created.

### 3. Compare Behavior to Requirements

For each existing requirement:
- Verify it still accurately describes the software. If not, set status to `Warning` with a reason.
- If accurate but the wording is incomplete or imprecise, update the requirement text.

For each observed behavior not yet covered by a requirement:
- Draft a new requirement with the next sequential number under the appropriate functional area.

### 4. Write Updates

- Create or update files in `docs/requirements/`.
- Preserve every existing requirement. Only modify status or requirement text, never delete entries.
- New requirements go at the end of their functional area.
- When creating a file for the first time, include all discovered requirements organized by functional area.

### 5. Validate All Requirements

After writing updates, launch one Explore subagent per requirement file. Each subagent independently validates every requirement in its assigned file against the actual codebase.

For each requirement the subagent must determine:
- Whether the described behavior exists in the software
- Whether the requirement accurately reflects that behavior as implemented

The subagent returns a list of requirement numbers with a verdict: **confirmed** (behavior matches), **warning** (behavior missing, changed, or ambiguous), or **unchanged** (status already correct).

### 6. Apply Validation Results

Using the subagent findings from step 5:
- Set any requirement marked **warning** to `Status: Warning` with the reason the subagent identified.
- Restore any previously warned requirement marked **confirmed** back to `Status: Active` and remove the Warning line.
- Leave **unchanged** requirements untouched.

This is the final write pass. No further exploration or requirement additions happen after validation.

## Constraints

- NEVER modify source code, tests, or any file outside `docs/requirements/`.
- NEVER write requirements about internal architecture, module layout, or code organization. Only specify behavior visible at component boundaries.
- ALWAYS explore the codebase before writing. Do not write requirements from memory or assumptions.
- ALWAYS read existing requirement files before making changes. Do not create duplicate requirements.
- ALWAYS use the sequential numbering scheme. Never skip or reuse numbers.
