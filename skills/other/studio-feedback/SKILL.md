---
name: studio-feedback
description: Prepare a user-reviewed Architecture Studio bug report or feature request for GitHub. Use when the user runs /as:studio-feedback, says "report a bug", "this skill broke", "send feedback", or requests a feature. Do not use for Claude Code's native /feedback command.
allowed-tools:
  - Read
  - Bash
  - AskUserQuestion
---

# /as:studio-feedback — Prepare a GitHub report

Prepare a report locally, show exactly what would leave the machine, and open GitHub only after one informed confirmation. Never submit the issue, post a comment, call the GitHub API, or transmit diagnostics in the background.

## 1. Choose the report type

Infer `bug` or `feature` when the request is clear. Otherwise use one `AskUserQuestion` gate to choose the type; do not first ask the same question in prose.

Use these issue forms and labels:

- Bug: `bug-report.yml`, label `bug`; fields `version`, `os`, `skill`, `what-happened`, `expected`.
- Feature: `feature-request.yml`, label `enhancement`; fields `version`, `skill`, `problem`, `proposal`.

## 2. Prepare minimal fields locally

Read the installed version from `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`. Gather the operating-system name and version with local commands only. Infer the affected skill from the conversation when reliable; otherwise leave it blank or ask during editing.

Draft the report from the user's words, but do not automatically include raw conversation history, files, stack traces, environment variables, or command output. Before showing the draft, remove or visibly flag:

- client and project names;
- street and project addresses;
- home-directory paths and usernames;
- email addresses and phone numbers;
- likely secrets, tokens, keys, cookies, and credentials; and
- proprietary document contents.

When uncertain, omit the value and mark where the user can add a safe description. Never invent reproduction details.

## 3. Show the exact outbound values

Present every proposed query field verbatim in one fenced text block. Explain immediately before the gate:

> Opening GitHub sends the displayed fields immediately as URL query parameters, and the URL may remain in browser history. GitHub receives them before issue submission; closing the tab does not undo that transmission. Architecture Studio will not submit the issue.

Use a **single confirmation gate** with these outcomes:

1. Open the prefilled GitHub issue.
2. Edit the fields first.
3. Cancel without opening GitHub.

Do not ask for confirmation in prose and then repeat it with `AskUserQuestion`. Editing returns to the same preview and gate. Cancel ends with no browser action or network request.

## 4. Encode and open only after confirmation

Build the URL from `https://github.com/AlpacaLabsLLC/skills-for-architects/issues/new`, the selected `template`, title, label, and the form field IDs above. Percent-encode every value with `jq` `@uri`; use Python 3 `urllib.parse.quote` only when `jq` is unavailable. Never interpolate unencoded report text into a shell command.

Keep the final URL at or below **6,000 characters**. Reduce only the narrative fields, state visibly that they were shortened for the URL, and retain the complete draft locally in the conversation for optional manual pasting. Never shorten version, operating system, or affected skill.

After the confirmed URL is built:

- On macOS, safely pass it as one quoted argument to `open`.
- On other systems, print the URL rather than assuming a browser command.

Then say: "GitHub is open with the displayed fields. Review and edit the issue before choosing Submit on GitHub."

## Hard boundaries

- Never submit the issue or use `gh issue create`.
- Never open GitHub before the exact-value preview and informed gate.
- Never claim that closing an opened tab means nothing was transmitted.
- Never treat feedback as telemetry or send it to ALPA infrastructure.
- Never add project files, conversation transcripts, or attachments automatically.
