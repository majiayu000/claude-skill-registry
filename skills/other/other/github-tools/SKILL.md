---
name: github-tools
type: complex
depth: base
user-invocable: false
description: >-
  Executes GitHub operations via gh CLI 2.62+ Python wrapper for issues, PRs, workflows, projects, releases, cache, labels, discussions, and search. Use when managing repository lifecycle, reviewing code, triggering CI/CD, or querying GitHub API.
---

# [H1][GITHUB-TOOLS]
>**Dictum:** *Standardized invocation reduces agent errors.*

<br>

Invokes gh CLI commands through Python wrapper.

[IMPORTANT] Zero-arg commands default to `state=open`, `limit=30`. All commands use positional args. gh CLI 2.62+ features: `pr revert`, `release verify`, `auth status --json`, Copilot CLI integration.

---
## [1][COMMANDS]

### [1.1][ISSUES]

| [CMD]         | [ARGS]                    | [PURPOSE]          |
| ------------- | ------------------------- | ------------------ |
| issue-list    | `[state] [limit]`         | List issues        |
| issue-view    | `<number>`                | View issue details |
| issue-create  | `<title> [body]`          | Create issue       |
| issue-comment | `<number> <body>`         | Comment on issue   |
| issue-close   | `<number>`                | Close issue        |
| issue-edit    | `<number> [title] [body]` | Edit issue         |
| issue-reopen  | `<number>`                | Reopen issue       |
| issue-pin     | `<number>`                | Pin issue          |

### [1.2][PULL_REQUESTS]

| [CMD]     | [ARGS]                    | [PURPOSE]         |
| --------- | ------------------------- | ----------------- |
| pr-list   | `[state] [limit]`         | List PRs          |
| pr-view   | `<number>`                | View PR details   |
| pr-create | `<title> [body] [base]`   | Create PR         |
| pr-diff   | `<number>`                | Get PR diff       |
| pr-files  | `<number>`                | List PR files     |
| pr-checks | `<number>`                | View PR checks    |
| pr-merge  | `<number>`                | Merge PR (squash) |
| pr-review | `<number> <event> [body]` | Review PR         |
| pr-edit   | `<number> [title] [body]` | Edit PR           |
| pr-close  | `<number>`                | Close PR          |
| pr-ready  | `<number>`                | Mark PR ready     |

### [1.3][WORKFLOWS]

| [CMD]         | [ARGS]              | [PURPOSE]          |
| ------------- | ------------------- | ------------------ |
| run-list      | `[limit]`           | List workflow runs |
| run-view      | `<run_id>`          | View run details   |
| run-logs      | `<run_id> [failed]` | Get run logs       |
| run-rerun     | `<run_id>`          | Rerun failed jobs  |
| run-cancel    | `<run_id>`          | Cancel run         |
| workflow-list | --                  | List workflows     |
| workflow-view | `<workflow>`        | View workflow YAML |
| workflow-run  | `<workflow> [ref]`  | Trigger workflow   |

### [1.4][SEARCH]

| [CMD]         | [ARGS]            | [PURPOSE]           |
| ------------- | ----------------- | ------------------- |
| search-repos  | `<query> [limit]` | Search repositories |
| search-code   | `<query> [limit]` | Search code         |
| search-issues | `<query> [limit]` | Search issues       |

### [1.5][PROJECTS]

| [CMD]              | [ARGS]                    | [PURPOSE]           |
| ------------------ | ------------------------- | ------------------- |
| project-list       | `[owner]`                 | List projects       |
| project-view       | `<project> [owner]`       | View project        |
| project-item-list  | `<project> [owner]`       | List project items  |
| project-create     | `<title> [owner]`         | Create project      |
| project-close      | `<project> [owner]`       | Close project       |
| project-delete     | `<project> [owner]`       | Delete project      |
| project-item-add   | `<project> <url> [owner]` | Add item to project |
| project-field-list | `<project> [owner]`       | List project fields |

### [1.6][RELEASES_AND_CACHE]

| [CMD]        | [ARGS]                | [PURPOSE]       |
| ------------ | --------------------- | --------------- |
| release-list | `[limit]`             | List releases   |
| release-view | `<tag>`               | View release    |
| cache-list   | `[limit]`             | List caches     |
| cache-delete | `<cache_key>`         | Delete cache    |
| label-list   | --                    | List labels     |
| repo-view    | `[repo]`              | View repository |
| api          | `<endpoint> [method]` | Raw API call    |

### [1.7][DISCUSSIONS]

| [CMD]                    | [ARGS]                         | [PURPOSE]                  |
| ------------------------ | ------------------------------ | -------------------------- |
| discussion-list          | `[category] [limit]`           | List discussions           |
| discussion-view          | `<number>`                     | View discussion            |
| discussion-category-list | --                             | List discussion categories |
| discussion-create        | `<category_id> <title> <body>` | Create discussion          |
| discussion-comment       | `<discussion_id> <body>`       | Comment on discussion      |
| discussion-close         | `<discussion_id>`              | Close discussion           |
| discussion-delete        | `<discussion_id>`              | Delete discussion          |

---
## [2][USAGE]

```bash
# Zero-arg commands
uv run .claude/skills/github-tools/scripts/gh.py issue-list
uv run .claude/skills/github-tools/scripts/gh.py pr-list
uv run .claude/skills/github-tools/scripts/gh.py run-list
uv run .claude/skills/github-tools/scripts/gh.py workflow-list
uv run .claude/skills/github-tools/scripts/gh.py label-list
uv run .claude/skills/github-tools/scripts/gh.py release-list
uv run .claude/skills/github-tools/scripts/gh.py repo-view
uv run .claude/skills/github-tools/scripts/gh.py discussion-category-list

# With positional args
uv run .claude/skills/github-tools/scripts/gh.py issue-list closed 50
uv run .claude/skills/github-tools/scripts/gh.py issue-view 42
uv run .claude/skills/github-tools/scripts/gh.py issue-create "Bug report" "Details here"
uv run .claude/skills/github-tools/scripts/gh.py issue-comment 42 "This is a comment"
uv run .claude/skills/github-tools/scripts/gh.py issue-close 42
uv run .claude/skills/github-tools/scripts/gh.py issue-pin 42

uv run .claude/skills/github-tools/scripts/gh.py pr-view 99
uv run .claude/skills/github-tools/scripts/gh.py pr-create "Feature" "Description" main
uv run .claude/skills/github-tools/scripts/gh.py pr-merge 99
uv run .claude/skills/github-tools/scripts/gh.py pr-review 99 APPROVE "LGTM"
uv run .claude/skills/github-tools/scripts/gh.py pr-edit 99 "New Title"

uv run .claude/skills/github-tools/scripts/gh.py run-list 10
uv run .claude/skills/github-tools/scripts/gh.py run-view 12345
uv run .claude/skills/github-tools/scripts/gh.py run-logs 12345 failed
uv run .claude/skills/github-tools/scripts/gh.py workflow-run ci.yml main

uv run .claude/skills/github-tools/scripts/gh.py search-repos "nx monorepo" 10
uv run .claude/skills/github-tools/scripts/gh.py search-code "dispatch table" 10

uv run .claude/skills/github-tools/scripts/gh.py project-view 1
uv run .claude/skills/github-tools/scripts/gh.py project-item-list 1

uv run .claude/skills/github-tools/scripts/gh.py discussion-list
uv run .claude/skills/github-tools/scripts/gh.py discussion-view 5

uv run .claude/skills/github-tools/scripts/gh.py api "/repos/{owner}/{repo}/issues" GET
```

---
## [3][OUTPUT]

Commands return: `{"status": "success|error", ...}`.

| [INDEX] | [PATTERN]         | [RESPONSE]                           |
| :-----: | ----------------- | ------------------------------------ |
|   [1]   | List commands     | `{items: object[]}`                  |
|   [2]   | View commands     | `{item: object}`                     |
|   [3]   | Mutation commands | `{number: int, action: bool}`        |
|   [4]   | Search commands   | `{query: string, results: object[]}` |
|   [5]   | Diff commands     | `{number: int, diff: string}`        |

---
## [4][ENVIRONMENT]

| [VAR]               | [REQUIRED] | [DESCRIPTION]                             |
| ------------------- | ---------- | ----------------------------------------- |
| `GH_TOKEN`          | Yes        | GitHub token (auto-configured by gh auth) |
| `GH_PROJECTS_TOKEN` | No         | Override token for project commands       |

---
## [5][ERROR_HANDLING]

- gh CLI errors print `[ERROR] <message>` and exit 1
- Rate limit (403): `[ERROR] API rate limit exceeded`; retry after `X-RateLimit-Reset`
- Not found (404): `[ERROR] Could not resolve` for missing issues/PRs
- Auth failure: `[ERROR] authentication required`; run `gh auth login`
- Project commands require `GH_PROJECTS_TOKEN` with `project` scope
