---
name: automated-review-addressing
description: "Use when PR review batches need automated addressing. Human reviews auto-launch; bot reviews use pr-review-ai-bots."
user-invocable: false
---

# Automated Review Addressing System

## Introduction

### Purpose

The Automated Review Addressing System streamlines pull request reviews by automatically launching a Claude Code agent after feedback lands and pushing fixes directly to the PR's head branch. Human reviews trigger on submission; bot reviews trigger after CodeRabbit and Cursor Bugbot checks succeed or when maintainers add the `claude-address-bot-review` label to force a run. Agents iterate on feedback in small batches and resolve review threads via repository-provided scripts, so developers do not have to merge mini PRs.

### Definitions

- **Agent**: A Claude Code agent launched automatically for human reviews and for bot reviews after required checks succeed; it edits the PR head branch directly.
- **Review Batch**: A single GitHub review submission (human or AI bot) that may contain multiple inline comments.
- **Direct Branch Update**: The agent pushes commits to the PR head branch; no mini PR is opened.
- **Human Review Flow**: Automatically triggered for human review submissions; processes about seven comments per pass to keep context focused.
- **AI Bot Review Flow**: Automatically triggered after CodeRabbit and Cursor Bugbot checks succeed or when the `claude-address-bot-review` label is applied; processes about five comments per pass and triages validity before applying updates.
- **Review Batch ID**: The numeric GitHub review identifier; used for context building and, when present, scoping human review fetches.
- **Manual Bot Trigger Label**: `claude-address-bot-review` on a PR signals an intentional bot run even if required checks have not completed.

## Why Automated Review Addressing Exists

Manual triage of dense review batches slows down delivery and burdens reviewers with repetitive coordination. Automatically launching an agent keeps PRs progressing: unresolved items are fetched and addressed in tight loops, small groups of comments are processed per pass, and the resulting commits land on the PR branch without extra merge steps. Bot reviews wait for CodeRabbit and Cursor Bugbot checks so all automated feedback is available before launching.

## How does this system make developers' lives easier?

- **Faster review turnaround**: For human reviews, an agent begins addressing comments immediately upon review submission.
- **Reduced toil**: Repetitive fetch/triage/resolve steps are automated using in-repo scripts and skills.
- **Direct branch updates**: Agents push fixes to the PR head branch; no mini PR needs to be merged.
- **Bot coverage without manual steps**: Bot reviews auto-launch after CodeRabbit and Cursor Bugbot checks finish so automated feedback is handled in one pass. Manual `pr-review-ai-bots` agent and the `claude-address-bot-review` label remain available when explicit instructions or overrides are needed.

## Directory Structure

```text
.github/
├── workflows/
│   ├── claude-pr-review-agent.yml        # Launches agent on pull_request_review: submitted (human reviews)
│   └── claude-bot-pr-review-agent.yml    # Launches agent after CodeRabbit + Cursor Bugbot checks succeed
└── scripts/
    ├── address-review.ts                  # Local CLI to replicate cloud agent setup
    ├── build-pr-review-context.py        # Gathers structured context for agent prompts
    ├── build-pr-review-prompt.ts         # Constructs agent prompt with dynamic task sizing
    └── merge-review.ts                   # Merges review branches back into base with optional commit message

scripts/
├── claude-hooks/
│   ├── pr-review-check.ts                # Detects PR review branches, checks for unresolved comments
│   └── agent-check.ts                    # Orchestrates all stop-time checks including PR review
├── cli/
│   └── git-utils.ts                      # Git CLI utilities for branch/PR operations
├── pr-check-comments.sh                  # Fetch unresolved human comments via GitHub GraphQL API
├── pr-check-bot-comments.sh              # Fetch unresolved bot comments
├── pr-apply-comment-decisions.sh         # Apply reactions and resolve threads for bot comments
└── pr-resolve-comments.sh                # Resolve review threads directly

.claude/agents/
├── pr-review.md                          # Agent playbook for human reviews
└── pr-review-ai-bots.md                  # Agent playbook for AI bot reviews
```

## Core Components

- **Workflows**: `claude-pr-review-agent.yml` launches on `pull_request_review: submitted` for human reviews; `claude-bot-pr-review-agent.yml` launches after CodeRabbit and Cursor Bugbot check runs succeed or when the `claude-address-bot-review` label is applied to a PR.
- **Context Builders**: `build-pr-review-context.py` and `build-pr-review-prompt.ts` assemble PR metadata, review/bot context, and unresolved comments into the agent prompt.
- **Fetch Scripts**: `pr-check-comments.sh` and `pr-check-bot-comments.sh` pull unresolved threads (human vs bot) with batching and bot filtering controls.
- **Claude Code Hooks**: `scripts/claude-hooks/pr-review-check.ts` plus `agent-check.ts` enforce unresolved-comment gating, then run build/lint/test/structure checks before agents can stop.
- **CLI**: `scripts/address-review.ts` mirrors the cloud flow locally: infers PR, fetches comments, builds prompt, and sets up the working branch.
- **Merge helper**: `.github/scripts/merge-review.ts` parses review branch names, stages pending changes with an optional or default commit message, checks out the base branch (local or inferred from the PR), and merges the review branch without opening a new PR.
- **Agents**: `.claude/agents/pr-review.md` and `.claude/agents/pr-review-ai-bots.md` provide manual playbooks when automation is skipped or extra guidance is needed.

## How It Works

### 1) Launch on Review Submission

When a review is submitted on a PR, `.github/workflows/claude-pr-review-agent.yml` executes:

- Runs Python context builder (`.github/scripts/build-pr-review-context.py`) to gather PR metadata, review metadata, determine bot status, and fetch CodeRabbit summary.
- **For human reviews**: Automatically launches an agent to address comments on the PR head branch (no mini PR).
- **For bot reviews**: Skips automatic launch here; the bot workflow below handles automation. Manual `pr-review-ai-bots` agent remains available for explicit instructions.
- Builds a structured prompt file embedding the JSON context and inline instructions.
- Posts a PR review comment with a link to the agent run for visibility.

### 1b) Launch on Bot Checks

When CodeRabbit and Cursor Bugbot checks both succeed for a PR head SHA, `.github/workflows/claude-bot-pr-review-agent.yml` executes. The same workflow also runs when a maintainer applies the `claude-address-bot-review` label to a PR, which serves as a manual override and skips the required-check gate:

- Confirms both check runs (by app slug/name) have `conclusion: success` on the PR head SHA unless the manual override label is present.
- Fetches unresolved bot comments (limit 5) and builds a synthetic bot review context plus prompt.
- Launches a Claude Code agent on the PR head branch.
- Posts a PR comment with the agent link.

### 2) Agent Iteration Loop

Inside the agent session, the agent follows inline instructions embedded in the prompt:

- **Human review flow** (automatic): The agent receives ~7 unresolved comments in the initial prompt and, on each stop attempt, receives additional unresolved comments via Claude Code stop-hook followups. It processes comments, implements edits, and resolves completed threads with `npm run resolve-comments -- <comment_url_1> <comment_url_2> ...`.
- **AI bot review flow** (automatic or manual): The bot workflow auto-launches after CodeRabbit and Cursor Bugbot checks succeed (or you can invoke the `pr-review-ai-bots` agent). The agent receives ~5 unresolved bot comments, triages validity, generates `decisions.json`, and runs `npm run apply-comment-decisions -- .claude/tmp/decisions.json` to react and resolve threads.
- Agents commit directly to the PR head branch; no mini PR is created.
- **Note**: The agent does not need to fetch comments manually; the stop hook automatically fetches and presents unresolved comments when the agent attempts to stop.

### 3) Stop Hook Integration

When the agent attempts to stop, the stop hook (`scripts/claude-hooks/agent-check.ts`) executes:

- Calls `performPrReviewCheck()` from `pr-review-check.ts` BEFORE running build/lint/test checks (priority 1).
- `performPrReviewCheck()` extracts PR number and review batch from branch patterns when present, otherwise falls back to the open PR for the current branch to keep direct-branch agents in the loop.
- Determines bot vs human review (by review batch when available, otherwise by checking unresolved bot comments first).
- Runs the appropriate fetch script (`fetch-unresolved-comments` or `fetch-unresolved-bot-comments`) to check for remaining comments.
- If comments remain, returns a block message with:
  - The full markdown checklist of unresolved comments
  - Resolution instructions specific to review type
  - The agent cannot stop until all comments are resolved.
- If no comments remain, allows the agent to proceed to build/lint/test checks.

**Execution Order**: merge conflicts → PR review comment check → build → linting → tests → rule structure validation → check-your-work. Merge conflicts run first because they block compilation entirely; review feedback runs before quality checks to keep the agent focused on reviewer intent.

## How to Use the System

### Human Review Batches

1. Submit a standard GitHub review with inline comments.
2. Wait for the PR comment confirming that an agent was launched. Follow the link to monitor it.
3. The agent processes ~7 comments per pass and pushes commits directly to the PR branch.
4. If needed, run locally:
   - Fetch unresolved: `npm run fetch-unresolved-comments -- --pr=<PR_NUMBER> [--review-batch=<REVIEW_ID>]`
   - Resolve threads: `npm run resolve-comments -- <comment_url_1> <comment_url_2> ...`

### AI Bot Review Batches (CodeRabbit, Graphite, Cursor BugBot, etc.)

1. Submit or trigger CodeRabbit and Cursor Bugbot checks.
2. After both checks succeed, an agent launches automatically. Follow the PR comment to monitor it. Use the `pr-review-ai-bots` agent manually if you want to provide explicit instructions or skip automation.
3. The agent triages validity, processes ~5 comments at a time, and resolves valid items with `apply-comment-decisions`, pushing fixes directly to the PR branch.
4. If needed, run locally:
   - Fetch unresolved: `npm run fetch-unresolved-bot-comments -- --pr=<PR_NUMBER> [--review-batch=<REVIEW_ID>]`
   - Apply decisions: `npm run apply-comment-decisions -- .claude/tmp/decisions.json [--pr=<PR_NUMBER>]`

**Note**: Automatic mini-PRs are disabled for bot reviews to prevent clutter and reduce costs.

### Merging review branches

Use the merge helper when finishing a review branch that follows the `(<base>)-review-pr-(<pr>)[-(<reviewBatch>)][-(human|bot)]` pattern:

- Run on the review branch: `npm run merge-review -- --message "<optional_commit_message>"`
- The helper stages all changes, commits with the provided message or `chore: merge review branch for PR #<pr> [(review <reviewBatch>)]`, checks out the base branch (local match or inferred from the PR), and merges the review branch.
- Ensure the branch name matches the pattern so the base branch candidate and PR number resolve correctly.

### Tips

- **For bot reviews**: Before using the `pr-review-ai-bots` agent, mark invalid comments with a 👎 reaction and resolve them. This prevents the agent from fetching them.
- Bot automation runs after CodeRabbit and Cursor Bugbot checks succeed; the `claude-address-bot-review` label can force a launch when those checks are not yet green.
- Agents push directly to the PR branch; watch the PR commits tab for updates.
- You can still use `.claude/agents/pr-review.md` or `.claude/agents/pr-review-ai-bots.md` manually in Claude Code Chat for follow-ups.

## Local Development Workflow

Developers can replicate the cloud agent setup locally using the `address-review` npm script:

```bash
# Auto-detect PR from current branch, process all unresolved comments
npm run address-review

# Specify PR explicitly
npm run address-review -- --pr=123

# Process specific review batch (PR inferred from current branch)
npm run address-review -- --review-batch=456789

# Process specific review batch with explicit PR
npm run address-review -- --pr=123 --review-batch=456789

# Force bot review workflow (overrides auto-detection)
npm run address-review -- --pr=123 --review-batch=456789 --force-bot

# Force human review workflow (overrides auto-detection)
npm run address-review -- --pr=123 --review-batch=456789 --force-human
```

### What the Script Does

1. **Validates Prerequisites**: Checks that `gh`, `jq`, and `git` are installed and working directory is clean
2. **Infers Context**: Auto-detects PR number from current branch if not provided
3. **Builds Review Context**: Gathers PR metadata, review metadata, determines bot vs. human review
4. **Fetches Unresolved Comments**: Runs the appropriate bash script to get the checklist
5. **Builds Agent Prompt**: Uses the same prompt builder as the cloud workflow
6. **Creates Review Branch**: Checks out a new branch following the naming pattern
7. **Writes Prompt File**: Saves the complete prompt to `.claude/tmp/pr-review-prompt.md`
8. **Provides Instructions**: Displays next steps for opening Claude Code Chat

### After Running the Script

1. Open the prompt file at `.claude/tmp/pr-review-prompt.md`
2. Copy its entire contents
3. Open a new Claude Code conversation
4. Paste the prompt and start the agent

The agent follows the same workflow as a cloud agent—the stop hook automatically presents new unresolved comments when the agent attempts to finish.

### Prerequisites

- **GitHub CLI (`gh`)**: Authenticated with appropriate repository permissions
- **jq**: JSON parsing utility for processing GitHub API responses
- **git**: Clean working directory (no uncommitted changes)

## Configuration

### GitHub Action Secrets

| Secret | Purpose |
|--------|---------|
| `CURSOR_API_KEY` | API authentication for background agents |
| `GITHUB_TOKEN` | Auto-provided, used for PR/issue operations |

### npm Scripts

| Script | Purpose |
|--------|---------|
| `npm run address-review` | Local CLI to set up PR review workflow |
| `npm run fetch-unresolved-comments` | Fetch unresolved human review comments |
| `npm run fetch-unresolved-bot-comments` | Fetch unresolved bot review comments |
| `npm run resolve-comments` | Resolve review threads by URL |
| `npm run apply-comment-decisions` | Apply reactions and resolve bot comment threads |
| `npm run merge-review` | Commit staged changes on a review branch and merge into the inferred base branch |

## Critical Insights for Maintainers

- **Bot gating is deliberate**: Bot agents launch only after both CodeRabbit and Cursor Bugbot checks succeed to ensure all automated feedback is present and avoid redundant runs; the `pr-review-ai-bots` agent and the `claude-address-bot-review` label are available when a manual launch is intentional.
- **Batch sizing balances load**: ~7 items for human reviews maximizes throughput with manageable context; ~5 items for bot reviews limits triage overhead because bot feedback often mixes valid and invalid findings.
- **Direct branch commits reduce friction**: Agents push to the PR head branch (no mini PR) to avoid merge overhead and keep review threads resolvable on the original branch.
- **Branch detection fallback**: When no `-review-pr-*` suffix exists (direct-branch automation), `pr-review-check.ts` falls back to the open PR for the current branch and still blocks completion until unresolved comments are cleared.
- **Merge helper expectations**: `merge-review.ts` requires the review branch naming pattern to extract the PR number and base candidate; if the base branch is missing locally it falls back to the PR head name. It stages all working tree changes before merging and uses a generated commit message when none is provided.
- **Future improvements**: Consider sourcing the required bot check names from repo settings instead of hard-coding CodeRabbit/Cursor, and expose a config flag to change bot batch size when feedback volume is higher.

## Common Pitfalls

- Bot automation waits for both CodeRabbit and Cursor Bugbot checks to finish successfully; if one is missing, the bot agent will not launch.
- The manual override label bypasses required-check gating; apply it only when a forced bot pass is desired and when unresolved bot feedback is present.
- The CLI review scripts require both `gh` and `jq` in the execution environment.
- The agent does not need to fetch comments manually; the stop hook handles this automatically.
- For manual runs, you can still use `.claude/agents/pr-review.md` or `.claude/agents/pr-review-ai-bots.md` in Claude Code Chat.

## Relationship to Other Systems

This system integrates with the **Claude Code Hooks and Workflows System** documented in `.claude/skills/claude-hooks/SKILL.md`. The PR review check runs as the first priority in the stop hook execution order, before build/lint/test checks. This ensures all reviewer feedback is addressed before code quality enforcement.
