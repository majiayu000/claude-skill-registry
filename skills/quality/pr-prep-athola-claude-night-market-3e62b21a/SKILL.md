---
name: pr-prep
description: |

Triggers: pr, quality-gates, prep, git, testing
  Prepare a pull request by validating the workspace, running quality gates,
  summarizing changes, and drafting the PR template.

  Triggers: PR preparation, pull request, quality gates, PR template, PR summary,
  branch preparation, merge request

  Use when: preparing PRs for submission, running quality gates, drafting
  PR descriptions and templates

  DO NOT use when: reviewing existing PRs - use pr-review instead.
  DO NOT use when: just generating commit messages - use commit-messages.

  Use this skill for PR preparation.
category: artifact-generation
tags: [git, pr, pull-request, quality-gates, testing]
tools: [Bash, Write, TodoWrite]
complexity: medium
estimated_tokens: 1000
progressive_loading: true
modules:
  - quality-gates.md
  - pr-template.md
dependencies:
  - sanctum:shared
  - sanctum:git-workspace-review
  - imbue:evidence-logging
  - imbue:structured-output
  - scribe:slop-detector
  - scribe:doc-generator

# Claude Code 2.1.0+ lifecycle hooks
hooks:
  PreToolUse:
    - matcher: "Bash"
      command: |
        # Log quality gate execution
        if echo "$CLAUDE_TOOL_INPUT" | grep -qE "(make|npm|cargo|pytest|ruff|eslint|clippy) (test|lint|fmt|build|check)"; then
          cmd=$(echo "$CLAUDE_TOOL_INPUT" | jq -r '.command // empty' 2>/dev/null || echo 'N/A')
          echo "[skill:pr-prep] Quality gate: $cmd at $(date)" >> ${CLAUDE_CODE_TMPDIR:-/tmp}/skill-audit.log
        fi
      once: false
  PostToolUse:
    - matcher: "Write"
      command: |
        # Track PR template generation
        file=$(echo "$CLAUDE_TOOL_INPUT" | jq -r '.file_path // empty' 2>/dev/null)
        if echo "$file" | grep -qE "(pr[-_]description|PR[-_]TEMPLATE|pull[-_]request)"; then
          echo "[skill:pr-prep] PR template written: $file at $(date)" >> ${CLAUDE_CODE_TMPDIR:-/tmp}/skill-audit.log
        fi
  Stop:
    - command: |
        echo "[skill:pr-prep] === Workflow completed at $(date) ===" >> ${CLAUDE_CODE_TMPDIR:-/tmp}/skill-audit.log
version: 1.3.5
---
# Pull Request Preparation Workflow

## Usage

Use this skill to stage changes and generate a PR summary. Run `Skill(sanctum:git-workspace-review)` first to capture the repository state and diffs.

## Required Progress Tracking

Create `TodoWrite` items for these steps before starting:
1. `pr-prep:workspace-reviewed`
2. `pr-prep:quality-gates`
3. `pr-prep:changes-summarized`
4. `pr-prep:testing-documented`
5. `pr-prep:pr-drafted`
6. `pr-prep:content-verified`

Mark each item as complete as the section is finished.

## Step 1: Review Workspace (`workspace-reviewed`)

Confirm that `Skill(sanctum:git-workspace-review)` is complete. If changes were staged after the initial review, re-execute the skill to refresh the context.

## Step 2: Run Quality Gates (`quality-gates`)

Execute formatting, linting, and tests using project-specific commands (e.g., `make fmt`, `make lint`, `make test`). Resolve all failures before proceeding. If a task cannot be executed locally, document the reason and the alternative validation performed. Language-specific commands and failure handling are detailed in `modules/quality-gates.md`.

## Step 3: Summarize Changes (`changes-summarized`)

Use the notes from the workspace review and the output of `git diff --stat origin/main...HEAD` to understand the scope. Identify key points in the diffs and group them into 2-4 paragraphs highlighting the technical changes and their rationale. Note breaking changes, migrations, or documentation updates.

## Step 4: Document Testing (`testing-documented`)

List each test command executed and its result. Include manual verification steps where relevant. If tests were skipped, document the reason and the mitigation plan.

## Step 5: Draft the PR (`pr-drafted`)

Populate the standard template with Summary, Changes, Testing, and Checklist sections. Include issue references, screenshots, or follow-up TODO items. Template structure and examples are available in `modules/pr-template.md`.

## Step 6: Verify Content Quality (`content-verified`)

Apply `Skill(scribe:slop-detector)` principles to the draft. Verify that the PR description avoids tier-1 slop words (delve, comprehensive, leverage, utilize, robust, seamless) and formulaic phrases like "I'd be happy to" or "It should be noted." Ensure there is no AI attribution in the text and that all claims are grounded with evidence such as commands, numbers, or filenames. Use active voice and maintain a balanced structure with prose for context.

### Vocabulary Substitutions

- Replace **leverage** or **utilize** with **use**.
- Replace **comprehensive** with **thorough** or **complete**.
- Replace **robust** with **solid** or **reliable**.
- Replace **facilitate** with **help** or **enable**.
- Replace **streamline** with **simplify**.

### Remediation

If the description contains slop, apply `Skill(scribe:doc-generator)` principles to ground claims with specifics, remove marketing language, and use direct statements.

## Output Instructions

Write the final PR description to the specified path, then display the file path and its contents for confirmation.

## Notes

Do not include tool or AI attribution in the PR text. If changes are required mid-process, re-run quality gates. This skill covers preparation; pushing changes and opening the PR occurs outside this workflow.

## Troubleshooting

If project-specific commands like `make` or `npm` are unavailable, verify the environment setup against the `README`. For permission errors, check write access to build directories. If a step fails without clear output, retry the command with verbose flags to inspect the logs.
