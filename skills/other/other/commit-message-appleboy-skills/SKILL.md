---
name: commit-message
description: "Generate a conventional commit message by analyzing staged git changes. Use when the user wants to create, write, or generate a git commit message from their current staged diff. Trigger on phrases like \"commit\", \"commit message\", \"commit msg\", \"寫 commit\", \"提交訊息\", \"generate commit\", or when the user has just finished making code changes and wants to commit them. Also trigger when the user runs /commit."
---

# Generate Commit Message

Generate a conventional commit message from staged git changes following a structured prompt pipeline.

## Steps

### 1. Stage changes and get the diff

Only stage files that were modified as part of the current session's work. Do not blindly run `git add -A` or `git add .` — pick specific files relevant to the task. If unsure which files to stage, show the user `git status` and let them decide.

Then get both an overview and the full diff:

```bash
git diff --staged --stat
git diff --staged
```

If the diff is empty after this, inform the user that there are no staged changes and stop.

If the diff is very large (e.g., more than 2000 lines), focus on the `--stat` output and the most important hunks. For files where changes are too extensive, note that those diffs were omitted and base the summary on the stat overview and available context.

If the staged changes span many unrelated modules or more than 10 files across different concerns, suggest splitting into multiple focused commits before proceeding.

### 2. Check existing commit style

Run a quick scan of recent commits to match the repo's conventions:

```bash
git log --oneline -20
```

If the repo already follows a consistent style (e.g., specific scope naming, prefix preferences, or language), adapt the generated message to match. The conventions in this skill are defaults — defer to the repo's existing patterns when they differ.

### 3. Analyze the diff

Produce a bullet-point summary of the changes. Follow these rules:

- A line starting with `+` means it was added, `-` means deleted. Lines with neither are context.
- Write every summary comment as a bullet point starting with `-`.
- Do not include file names as part of the comment.
- Do not use `[` or `]` characters in the summary.
- Do not include comments copied from the code.
- Write only the most important comments. When in doubt, write fewer comments.
- Readability is top priority.

Example summary comments for reference (do not copy verbatim):

```
- Increase the number of returned recordings from 10 to 100
- Correct a typo in the GitHub Action name
- Relocate the octokit initialization to a separate file
- Implement an OpenAI API endpoint for completions
```

### 4. Generate the commit title

From the summary, write a single-line commit title:

- Use imperative tense following the kernel git commit style guide.
- Write a high-level title that captures a single specific theme.
- Do not repeat the file summaries or list individual changes.
- Keep the title concise — aim for under 50 characters (the full header including prefix and scope should stay under 72 characters).
- Lowercase the first character.
- Remove any trailing period.

### 5. Determine the prefix and scope

**Prefix** — choose exactly one label based on the summary:

- `build`: Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)
- `chore`: Updating libraries, copyrights, or other repo settings, includes updating dependencies
- `ci`: Changes to CI configuration files and scripts (example scopes: Travis, Circle, GitHub Actions)
- `docs`: Non-code changes, such as fixing typos or adding new documentation
- `feat`: Introduces a new feature to the codebase
- `fix`: Patches a bug in the codebase
- `perf`: A code change that improves performance
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, etc.)
- `test`: Adding missing tests or correcting existing tests

**Breaking changes** — if the diff removes or renames a public API, changes a function signature in a breaking way, or makes any other backward-incompatible change, append `!` after the prefix (or after the scope if present). For example: `feat!:` or `feat(api)!:`. Additionally, include a `BREAKING CHANGE:` line in the commit body describing what changed and how to migrate.

**Scope** — identify the module or package scope from the changed files:

- Look at the file paths in the diff to determine which module, package, or component is affected.
- If all changes are within a single module/package/directory, use that as the scope (e.g., `model`, `git`, `prompt`, `cmd`, `provider`).
- Use the most specific common directory or package name. For example, changes only in `provider/openai/` should use `openai`, not `provider`.
- If changes span multiple modules, pick the one most central to the change's purpose.
- Keep the scope short — a single lowercase word.
- Scope is **recommended but optional** — if no clear scope can be determined (e.g., changes touch many unrelated areas), omit it and use the format `<prefix>: <title>` instead.

### 6. Create the commit

Format the commit message as:

```
<prefix>(<scope>): <title>

<summary>
```

Or without scope:

```
<prefix>: <title>

<summary>
```

If there is a breaking change, include the footer:

```
<prefix>(<scope>)!: <title>

<summary>

BREAKING CHANGE: <description of what broke and migration path>
```

Use a HEREDOC to pass the multi-line message to `git commit`:

```bash
git commit -m "$(cat <<'EOF'
<prefix>(<scope>): <title>

<summary>
EOF
)"
```

Run `git commit` directly — do not ask for confirmation.

### 7. Handle additional user requests

If the user's request includes extra actions beyond committing (e.g., "commit and push", "commit 然後推上去", "commit and create PR"), execute those after the commit succeeds. Common patterns:

- **push**: run `git push` after commit
- **push and PR**: push, then create a pull request
- **tag**: create a git tag after commit

Only perform actions the user explicitly requested.
