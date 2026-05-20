---
name: create-ticket
argument-hint: "[feature|bug|refactor] \"<description>\" | update <issue-number-or-url>"
allowed-tools: Bash(gh *)
description: Create or update a GitHub issue for easy-zeebe using the `gh` CLI. Use when the user asks to "file a bug", "create a feature request", "open a GitHub issue", or "update an existing one". Supports feature, bug, and refactor issue types with structured templates; shows a draft for confirmation before creating or editing; looks up existing issues by number or URL for updates.
---

# Skill: create-ticket

Create or update a GitHub issue for this repository
(feature request, bug report, or refactor task).

## IMPORTANT

- Always use gh-cli to create or update tickets.
- Never call the api directly.
- If gh-cli not available, abort the execution and ask the user to install it. The user must restart the skill then
- When any gh call fails, ask the user what to do (repeat, stop, do something else)

## Instructions

### Step 1 – Determine mode

Inspect `$ARGUMENTS`:

- If context contains `update` and/or an issue number or GitHub issue URl, use update-mode
- Otherwise use create-mode
- If create mode, does not make sense based on your context, as well, use AskUserQuestion to ask the user, to add more
  context, about what to do.

### Step 2 – Gather information

For a new issue:

- Extract the issue type (`feature`, `bug`, `refactor`) from `$ARGUMENTS`; if missing, ask the user
- For `feature`: understand the desired behaviour and why it is needed
- For `bug`: understand the current vs. expected behaviour and reproduction steps
- For `refactor`: understand the scope, motivation, and target state

For an issue that needs to be updated

- Fetch the issue using `gh issue view <number-or-url>`

### Step 3 – Research (optional)

If the issue involves a specific library, framework version, API, or configuration that you are not
fully certain about, ask the user:
*"Should I search online for [topic] to get accurate details (e.g. exact property names,
migration guides) before drafting?"*
If yes, use `WebSearch` / `WebFetch` to collect relevant facts, then incorporate them into the
draft. Skip this step if you already have sufficient knowledge.

### Step 4 – Draft

Draft the issue using the matching template from the Templates section below.

### Step 5 – Show and confirm

Present the full draft (create) or the current state + proposed changes (update) and ask:
*"Proceed? (yes / edit / cancel)"*. Apply edits and show again if requested.

### Step 6 – Create or update

Using the GitHub CLI:

- **Create**: `gh issue create --title "<title>" --body "<body>" --label "<label>"`
- **Update** (use whichever commands apply):
  ```bash
  gh issue edit <number> --title "<title>" --body "<body>"
  gh issue edit <number> --add-label "<label>" --remove-label "<label>"
  gh issue comment <number> --body "<comment>"
  gh issue close <number>
  gh issue reopen <number>
  ```

### Step 7 – Report

Run `gh issue view <number>` and show the final issue state with its URL.

---

## Templates

### Feature Request

```
**Title**: [Feature]: <short imperative title>
**Label**: enhancement

**Body**:
## Summary
<One sentence describing the desired feature>

## Motivation
<Why is this feature needed? What problem does it solve?>

## Proposed Solution
<How should the feature work? Include Zeebe/process details where relevant>

## Acceptance Criteria
- [ ] <criterion 1>
- [ ] <criterion 2>
```

### Bug Report

```
**Title**: [Bug]: <short description of the broken behaviour>
**Label**: bug

**Body**:
## Description
<What is going wrong?>

## Steps to Reproduce
1. <step 1>
2. <step 2>

## Expected Behaviour
<What should happen>

## Actual Behaviour
<What actually happens>

## Environment
- Java version:
- Zeebe / Camunda version:
- Module affected:
```

### Refactor

```
**Title**: [Refactor]: <short description of the change>
**Label**: refactor

**Body**:
## Summary
<What will be refactored and why?>

## Current State
<Describe the current implementation and its shortcomings>

## Target State
<Describe what the code should look like after the refactor>

## Out of Scope
<What will NOT be changed>
```
