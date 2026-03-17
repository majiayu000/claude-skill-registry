---
name: status
description: >
  Display code-forge feature dashboard with task-level progress from state.json, or show
  detailed status for a specific feature. Use when checking progress, asking "what's left",
  viewing task completion, or wanting a bird's-eye view of the project.
---

# Code Forge — Status

Display a dashboard of all features or detailed progress for a specific feature.

## When to Use

- Want to see all features and their progress
- Want to check status of a specific feature
- Need to regenerate the project-level overview

## Examples

```bash
/code-forge:status                  # Show project dashboard
/code-forge:status user-auth        # Show detail for one feature
```

## Workflow

```
Load Config → Scan Features → Display Dashboard or Detail → Update Overview
```

## Detailed Steps

@../shared/configuration.md

---

### Step 1: Determine Mode

Based on arguments:
- **No argument** → Global Dashboard (Step 2)
- **Feature name provided** → Feature Detail (Step 3)

---

### Step 2: Global Dashboard

#### 2.1 Scan for Features

1. Resolve the output directory: `<base_dir>/<output_dir>/`
2. Search for all `state.json` files in **both** locations:
   - `<output_dir>/*/state.json` (standard plans)
   - `.code-forge/tmp/*/state.json` (temporary plans created with `--tmp`)
3. For each `state.json`, extract: `feature`, `status`, `progress.*`, `metadata.source_doc`, `updated`
4. Mark features from `.code-forge/tmp/` with `[tmp]` suffix in display

#### 2.2 Display Feature Dashboard

**Features found:** Show table with #, Feature, Progress, Status, Last Updated.

```
code-forge — Feature Dashboard

  #  | Feature        | Progress   | Status      | Last Updated
  1  | user-auth      | 3/5 (60%)  | in_progress | 2026-02-14
  2  | file-upload    | 0/3 (0%)   | pending     | 2026-02-13
  3  | notifications  | 4/4 (100%) | completed   | 2026-02-12

Commands:
  /code-forge:plan @doc.md          Create new plan from document
  /code-forge:plan "requirement"    Create new plan from prompt
  /code-forge:impl <feature>        Execute tasks for a feature
  /code-forge:status <feature>      View feature detail
  /code-forge:fixbug "description"  Debug a bug
  /code-forge:review <feature>      Review completed feature
```

Offer actions via `AskUserQuestion`:
- Enter a feature name to view its detail
- Start a new plan
- Exit

**No features found:** Show empty state with instructions:
- How to create a feature document at `{base_dir}/{input_dir}/{feature-name}.md`
- How to run `/code-forge:plan @path/to/feature.md` or `/code-forge:plan "requirement text"`

#### 2.3 Update Project-Level Overview

After scanning, regenerate `{output_dir}/overview.md` using Step 4 logic.

#### 2.4 Handle User Selection

- **Feature name selected** → show Feature Detail (Step 3)
- **"New plan"** → suggest `/code-forge:plan` command
- **"Exit"** → end

---

### Step 3: Feature Detail

#### 3.1 Locate Feature

1. Look for `{output_dir}/{feature_name}/state.json`
2. If not found, also check `.code-forge/tmp/{feature_name}/state.json`
3. If still not found: show error, list available features

#### 3.2 Display Feature Detail

Read `state.json` and display:

```
code-forge — Feature: user-auth

Status: in_progress
Source: docs/features/user-auth.md
Created: 2026-02-10
Updated: 2026-02-14

Tasks:
  #  | Task           | Status      | Started     | Completed
  1  | setup          | completed   | 2026-02-10  | 2026-02-10
  2  | models         | completed   | 2026-02-11  | 2026-02-11
  3  | auth-logic     | in_progress | 2026-02-14  | —
  4  | api-endpoints  | pending     | —           | —
  5  | integration    | pending     | —           | —

Progress: 2/5 (40%)

Commands:
  /code-forge:impl user-auth      Continue execution
  /code-forge:review user-auth    Review completed tasks
  /code-forge:fixbug "..."        Fix a bug in this feature
```

---

### Step 4: Generate/Update Project-Level Overview

@../shared/overview-generation.md

Display: `Project overview updated: {output_dir}/overview.md`
