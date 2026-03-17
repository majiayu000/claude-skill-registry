---
name: context-synchronization
description: Synchronize project documentation after track completion. Use when a track reaches completed status and product, tech-stack, or guidelines documents may need updates.
---

# Context Synchronization

This skill provides the protocol for synchronizing project-level documentation after completing a Conductor track.

## Execution Trigger

**Only execute this protocol when:**
- A track has reached `[x]` status in the tracks file
- The `/claude-conductor:implement` command has finished all tasks

**Do NOT execute for:**
- Status changes other than completion
- Partial task completion
- Track creation

## Protocol Overview

1. Load the completed track's specification
2. Analyze for documentation impacts
3. Propose updates with user confirmation
4. Apply approved changes
5. Commit documentation updates

## Step-by-Step Process

### 1. Announce Synchronization

Inform the user:
> "I am now synchronizing the project-level documentation with the completed track's specifications."

### 2. Load Track Specification

Read the completed track's `conductor/tracks/<track_id>/spec.md` into context.

### 3. Load Project Documents

Read the following files:
- `conductor/product.md`
- `conductor/product-guidelines.md`
- `conductor/tech-stack.md`

### 4. Analyze and Update

#### 4.1 Update `conductor/product.md`

**Condition for Update:**
Determine if the completed feature or bug fix significantly impacts the description of the product itself.

Examples that warrant updates:
- New major feature that changes product capabilities
- Fundamental change to how users interact with the product
- New integration that expands product scope

Examples that do NOT warrant updates:
- Bug fixes
- Internal refactoring
- Minor UI tweaks
- Performance improvements

**Propose and Confirm:**
If an update is needed:
> "Based on the completed track, I propose the following updates to `product.md`:"
> ```diff
> [Proposed changes in diff format]
> ```
> "Do you approve these changes? (yes/no)"

**Action:**
Only after explicit user confirmation, apply the edits. Record whether this file was changed.

#### 4.2 Update `conductor/tech-stack.md`

**Condition for Update:**
Determine if significant changes in the technology stack occurred.

Examples that warrant updates:
- New library or framework added
- Database technology changed
- New external service integration
- Significant architectural change

Examples that do NOT warrant updates:
- Version bumps of existing dependencies
- Development-only tool changes
- Configuration changes

**Propose and Confirm:**
If an update is needed:
> "Based on the completed track, I propose the following updates to `tech-stack.md`:"
> ```diff
> [Proposed changes in diff format]
> ```
> "Do you approve these changes? (yes/no)"

**Action:**
Only after explicit user confirmation, apply the edits. Record whether this file was changed.

#### 4.3 Update `conductor/product-guidelines.md` (Strictly Controlled)

**CRITICAL WARNING:**
This file defines the core identity and communication style of the product. It should be modified with **extreme caution** and ONLY in cases of significant strategic shifts.

**Valid reasons to update:**
- Product rebrand
- Fundamental change in user engagement philosophy
- Major shift in target audience
- Complete redesign of product voice/tone

**Invalid reasons (do NOT update):**
- Routine feature updates
- Bug fixes
- Minor UI changes
- Performance improvements
- New features that don't change brand identity

**Condition for Update:**
You may ONLY propose an update if the track's `spec.md` **explicitly describes** a change that directly impacts branding, voice, tone, or other core product guidelines.

**Propose and Confirm (with warning):**
If the strict conditions are met:
> "**WARNING:** The completed track suggests a change to the core product guidelines. This is an unusual step. Please review carefully:"
> ```diff
> [Proposed changes in diff format]
> ```
> "Do you approve these critical changes to `product-guidelines.md`? (yes/no)"

**Action:**
Only after explicit user confirmation, apply the edits. Record whether this file was changed.

### 5. Final Report

Announce completion and provide a summary based on which files were changed.

**Example (product.md changed):**
> "Documentation synchronization is complete.
> - **Changes made to `product.md`:** The user-facing description of the product was updated to include the new feature.
> - **No changes needed for `tech-stack.md`:** The technology stack was not affected.
> - **No changes needed for `product-guidelines.md`:** Core product guidelines remain unchanged."

**Example (no changes):**
> "Documentation synchronization is complete. No updates were necessary for `product.md`, `tech-stack.md`, or `product-guidelines.md` based on the completed track."

### 6. Commit Changes

If any files were changed:
- Stage: `product.md`, `tech-stack.md`, and/or `product-guidelines.md`
- Commit message: `docs(conductor): Synchronize docs for track '<track_description>'`

## Diff Format Guidelines

When proposing changes, use diff format for clarity:

```diff
# Product Overview

- Our product helps users manage tasks efficiently.
+ Our product helps users manage tasks efficiently with real-time collaboration features.

## Key Features

- Task management
- Due date tracking
+ - Real-time collaboration
+ - Team workspaces
```

## User Confirmation Patterns

Always wait for explicit user response:

**Approval patterns:**
- "yes"
- "y"
- "approve"
- "looks good"

**Rejection patterns:**
- "no"
- "n"
- "reject"
- Any request for changes

If unclear, ask for clarification before proceeding.
