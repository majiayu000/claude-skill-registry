---
name: repo-maintenance
description: "Use when triaging or maintaining the eslint-custom-rules repository."
user-invocable: false
---

# ESLint Custom Rules Repository Maintenance Guide

## The "Staying on Top" Ethos

**Goal: 0 Outstanding Issues**

If we can get to the point where there are **0 ESLint Issues** in the codebase, it will become impossible for new ESLint bugs & requests to accidentally be ignored in the noise. Every new ESLint bug and request will be immediately noticed and quickly addressed.

As a result, our AI agents do a very good job of writing extensible, bug-free, performant code. We want to get to the point where every ESLint Issue that is opened is addressed right away.

## Workflow Overview

We have replaced manual processes with **Claude Code agents** and **Claude Code Hooks**. Most manual checking is now enforced automatically by code.

### 1. Triage & Labeling (The "Click-Ops" Workflow)

Manage the repo by applying GitHub Labels to trigger specialized agents.

**Step 1: Triage**
Ensure every new issue has the correct type label:
- `rule-request` (for new rules)
- `bug` (for fixing existing rules)

**Step 2: Research (Automated)**
- Add the label `claude-research` to any new rule request.
- **Action**: A research agent will search the web and post findings.
- **Your Job**:
  - **EXACT MATCH**: Close issue or ask a member of the team to import an existing rule into the main monorepo.
  - **NO MATCH**: System automatically adds `claude-implement` to start coding.
  - **PARTIAL MATCH**: Decide whether to import into the main monorepo and adapt an existing rule or build a new custom rule.

**Step 3: Implementation**
- **New Rules**: Ensure issue has `rule-request`, `research-complete`, and `claude-implement`. Triggers coding agent.
- **Bugs**: Ensure issue has `bug` and `claude-fix`. Triggers bug-fix agent.

### 2. Enforcing Implementation Standards (Stop Hooks & PR Checks)

Stop Hooks & PR Checks prevent the agent from finishing unless the following run successfully:

1. File Structure Verification: the agent has correctly created/updated ALL of the following:
    - `src/index.ts` (Import, Rules object, Recommended config)
    - `src/rules/new-rule.ts`
    - `src/tests/new-rule.test.ts`
    - `docs/rules/new-rule.md`
    - `README.md`
    If the agent forgets a file, the system blocks the agent and forces it to fix the mistake.

2. Quality Checks: the agent must meet minimum code standards
    Stop Hooks prevent the agent from finishing unless the following run successfully:
    - **Tests & Linting**: PRs cannot be opened until `npm test`, `npm run build`, and `npm run lint` pass.
    - **Comprehensive Tests**: The system automatically prompts the agent to "Expand Tests" with edge cases (false positives/negatives).

### 3. Reviewing PRs

- **Role**: Final sanity check.
- **Action**: If you see something wrong, leave a comment (e.g., "You missed this edge case...").
- **Automation**: A generic "Review Agent" will see the comment, wake up, fix the code, and push changes.
- **Merge**: Merge when all checks are green.

## Troubleshooting

### Fixing Build/Test Failures

If `.github/workflows/test-report.yml` fails:
1. `git checkout <pr-branch-name>`
2. Open a Claude Code agent conversation and run the `fix-build-test` agent.
   - The agent will run build/tests, diagnose errors, and loop until success.
3. Commit & push changes.

### Addressing Bot Reviews

If you need to address bot reviews (CodeRabbit, Cursor Bugbot) or if the automatic trigger didn't fire:
1. Add label `claude-address-bot-review` to the PR.
2. This triggers the Claude agent to triage and fix bot comments.

**Note**: If a Claude agent stops abruptly, open it up and send a message in its conversation: "It looks like you were interrupted. Please continue."
