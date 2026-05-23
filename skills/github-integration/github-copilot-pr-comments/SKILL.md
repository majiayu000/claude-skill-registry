---
name: github-copilot-pr-comments
description: Fetch GitHub Copilot code review comments from a pull request and generate a structured markdown report with all suggestions, inline comments, and review summaries using the `gh` CLI. Use when the user wants to: (1) see what Copilot said about a PR, (2) extract Copilot suggestions from a pull request, (3) generate a report of Copilot review feedback, (4) collect AI code review comments into a document. Triggers on mentions of "Copilot comments", "Copilot review", "Copilot suggestions", "PR review by Copilot", or any request to get/extract/summarize GitHub Copilot feedback on a pull request.
---

# GitHub Copilot PR Comments Skill

Extract GitHub Copilot review comments from a PR and produce a markdown report using `gh` CLI.

## Prerequisites

- **`gh`** CLI installed and authenticated (`gh auth login`)
- **`jq`** installed for JSON processing

## Usage

```bash
./scripts/fetch_copilot_comments.sh <owner/repo> <pr_number> [output_file]
```

### Parameters

| Param         | Required | Description                                    |
|---------------|----------|------------------------------------------------|
| `owner/repo`  | Yes      | Full repo identifier, e.g. `microsoft/vscode`  |
| `pr_number`   | Yes      | PR number                                      |
| `output_file` | No       | Output markdown path (default: `copilot_review.md`) |

## Workflow

1. Ask the user for repo and PR number if not provided.
2. Verify `gh` is authenticated (`gh auth status`). If not, instruct the user to run `gh auth login`.
3. Run: `bash scripts/fetch_copilot_comments.sh <owner/repo> <pr_number> /home/claude/copilot_review.md`
4. Copy output to `/mnt/user-data/outputs/copilot_review.md` and present to the user.

## Output Format

The generated markdown includes:

- **PR metadata** — title, author, link, creation date
- **Summary** — total Copilot comments by type, files reviewed, suggestion count
- **Review summaries** — top-level Copilot review bodies with approval state
- **Inline code comments** — grouped by file with diff context, line numbers, and `suggestion` blocks
- **General comments** — issue-level comments from Copilot

## Copilot Detection

Comments are attributed to Copilot if the author login matches: `copilot`, `copilot[bot]`, `github-copilot`, `github-copilot[bot]`, `github-advanced-security[bot]`, or any bot user with "copilot" in the login.