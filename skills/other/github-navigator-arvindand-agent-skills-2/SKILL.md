---
name: github-navigator
description: "GitHub operations via gh CLI. CRITICAL: Use instead of WebFetch for any `github.com` URL or GitHub repo path like `owner/repo`. Use when the user asks to inspect repositories, files, issues, pull requests, releases, Actions runs, or repository structure. Use when the user says 'show README', 'list issues', 'check PR', 'clone repo', or 'analyze this repo'."
compatibility: Designed for Claude Code-compatible agents. Uses Claude-specific context forking and hooks; other Agent Skills products may ignore these extensions. allowed-tools is optional and may be handled differently across clients.
allowed-tools: Bash(gh:*) Bash(git:clone) Read Glob Grep Task
context: fork
hooks:
  PostToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "python3 scripts/validate-gh-output.py"
---

# GitHub Navigator

Use `gh` for GitHub work. Prefer command discovery over memorizing flags.

This is an execution skill. Use `gh` instead of generic web fetching for GitHub tasks, inspect `gh --help` when syntax is uncertain, then execute with tight guardrails. Keep the main flow lean and load [REFERENCES.md](REFERENCES.md) only when you need concrete examples, installation steps, or GraphQL details.

## When to Use

Activate when:

- the user gives a `github.com` URL
- the user names a repo path like `facebook/react` or `owner/repo`
- the user asks about repository files, issues, PRs, releases, workflows, or metadata
- the user wants to understand the architecture or structure of a GitHub-hosted codebase

## Core Rules

- Always prefer `gh` over `WebFetch` for GitHub content and operations.
- Use `gh api` for raw file content, directory listings, and API-only endpoints.
- Use `gh` subcommands (`issue`, `pr`, `release`, `run`, `workflow`, `repo`) when a dedicated command exists.
- Use `gh <domain> --help` before guessing flags or subcommands.
- Limit each command pattern to 2 attempts; if it still fails, stop and report the error.

## Command Routing

| User Intent | Primary Command Path |
|-------------|----------------------|
| fetch file or list directory | `gh api repos/OWNER/REPO/contents/...` |
| inspect issues | `gh issue ...` |
| inspect pull requests | `gh pr ...` |
| inspect releases | `gh release ...` |
| inspect Actions runs or workflows | `gh run ...` or `gh workflow ...` |
| inspect repo metadata or clone/fork | `gh repo ...` |
| endpoints without a dedicated subcommand | `gh api ...` |

Use dedicated subcommands first. Fall back to `gh api` only when needed.

## Execution Pattern

1. Identify the command domain from the request.
2. Check the relevant help output if the exact syntax is not already obvious.
3. Substitute the user's repo, path, issue number, PR number, or other arguments.
4. Run the command.
5. If it fails, adjust once based on the error message.
6. If it fails again, stop and report the error instead of trying blind variations.

## Deep Analysis Mode

When the user wants to understand a codebase deeply, clone it locally for inspection instead of making many remote API calls.

Default flow:

1. Clone with depth 1 to `/tmp/github-navigator/OWNER-REPO/`

   ```bash
   git clone --depth 1 https://github.com/OWNER/REPO.git /tmp/github-navigator/OWNER-REPO
   ```

2. Inspect the repository for:
   - tech stack signals (`package.json`, `go.mod`, `Cargo.toml`, `pom.xml`, `requirements.txt`, etc.)
   - high-level directory structure
   - entry points and primary modules
   - README, docs, examples, and contribution files
   - architectural patterns worth calling out

3. Summarize the findings in plain language.
4. Keep the clone for follow-up questions unless cleanup is requested.

Use a full clone only if the user explicitly needs commit history or deeper git analysis.

## Safety

Always confirm before executing state-changing or destructive commands, including:

- creating, closing, or reopening issues
- creating, merging, or closing pull requests
- deleting, archiving, or transferring repositories
- setting secrets or triggering workflows
- any use of `--force`, `--yes`, or similar bypass flags

## Authentication and Recovery

- Check `gh auth status` when the task touches private repos or write operations.
- Use `gh auth login` if the client is not authenticated.
- If permissions are insufficient, use `gh auth refresh -s repo -s workflow -s read:org` as appropriate.
- If a command fails, read the error, check help, retry once, then stop.
- If `gh` is not installed, point the user to [REFERENCES.md](REFERENCES.md) for installation guidance.

## Reference Handoff

Use [REFERENCES.md](REFERENCES.md) when you need:

- concrete example commands for common tasks
- install and auth setup details
- troubleshooting reminders
- GraphQL examples or other lower-frequency patterns

---

> **License:** MIT
> **See also:** [REFERENCES.md](REFERENCES.md)
