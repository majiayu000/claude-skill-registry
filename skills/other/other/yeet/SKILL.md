---
argument-hint: <create-pr|update-pr|create-issue|create-discussion> [options]
disable-model-invocation: false
name: yeet
user-invocable: true
description: This skill should be used when the user asks to "create a pull request", "create PR", "open PR", "update a pull request", "update PR", "create an issue", "file an issue", "create a GitHub issue", "create a Claude Code issue", "report a bug in Claude Code", "create a Codex issue", "report a bug in Codex CLI", "create a Sablier issue", "file an issue in sablier-labs", "create a discussion", "start a GitHub discussion", "yeet a PR", "yeet an issue", "yeet a discussion", or mentions GitHub contribution workflows.
---

# GitHub Contribution Workflows

## Overview

Facilitate GitHub-based open source contribution workflows including pull requests, issues, and discussions. This skill provides structured automation for common OSS contribution tasks, ensuring consistent formatting, proper metadata application, and adherence to repository conventions. Use this skill when contributing to open source projects or managing GitHub repositories through the command line.

The skill emphasizes semantic analysis over mechanical operations—understand the intent and context of changes before generating titles, descriptions, or selecting templates. All generated content should be conversational and informal rather than robotic or overly formal.

## Prerequisites

Before using any OSS contribution workflow, verify GitHub CLI authentication status:

```bash
gh auth status
```

Ensure the output shows you are logged in to github.com with appropriate scopes (repo, read:org, etc.). If not authenticated, run:

```bash
gh auth login
```

For pull request workflows, also verify:

- Working tree is clean or changes are committed
- Current branch has commits ahead of the base branch
- Remote tracking is configured for the current branch

## Related Skills

For detailed GitHub CLI command syntax, flags, and patterns, activate the `cli-gh` skill. That skill covers the full gh command surface including issue management, PR operations, repository queries, workflow triggers, and API interactions.

## Pull Requests

Create GitHub pull requests with semantic change analysis and structured formatting. The workflow generates meaningful titles and descriptions by reading actual code changes rather than relying solely on commit messages or filenames.

### Workflow Steps

**Validate Prerequisites**

Confirm git state before proceeding:

- Check `git status` for uncommitted changes
- Verify branch has commits ahead of base branch via `git log`
- Confirm remote tracking is configured
- Ensure gh CLI is authenticated

**Parse Arguments**

Support the following arguments:

- `base-branch`: Target branch for the PR (default: main/master)
- `reviewers`: Comma-separated list of GitHub usernames
- `--draft`: Create as draft PR
- `--test-plan`: Include test plan section in body

**Semantic Change Analysis**

Read the actual diff to understand what changed:

```bash
git diff base-branch...HEAD
```

Analyze:

- Nature of changes (feature, fix, refactor, docs, test, chore)
- Scope of impact (which components/modules affected)
- Intent and purpose (why the change was made)
- Dependencies or related changes

**Generate Title and Body**

Craft a concise title summarizing the change. Generate a body with:

- **Summary** section (1-3 bullet points explaining what and why)
- **Test Plan** section if `--test-plan` flag provided (bulleted checklist)
- GitHub admonitions (NOTE, TIP, IMPORTANT, WARNING, CAUTION) where appropriate

Pass the body using HEREDOC syntax:

```bash
gh pr create --title "the pr title" --body "$(cat <<'EOF'
## Summary
- First bullet point
- Second bullet point

## Test Plan
- [ ] Test item one
- [ ] Test item two
EOF
)"
```

**Create Pull Request**

Execute the gh command with all parsed flags and generated content. Include:

- `--base` for target branch
- `--reviewer` for each reviewer
- `--draft` if draft mode requested
- Return the PR URL to the user

For the complete pull request workflow with detailed steps, examples, and edge cases, refer to `references/create-pr.md`.

## Update Pull Requests

Update existing GitHub pull requests with semantic change analysis. The workflow regenerates titles and descriptions by reading actual code changes rather than relying solely on commit messages.

### Workflow Steps

**Validate Prerequisites**

Same as Pull Requests: confirm gh CLI auth, verify git repo state.

**Check for Existing PR**

Verify a PR exists for the current branch:

```bash
gh pr view --json number,url,title,baseRefName 2>/dev/null
```

If no PR found, error and direct user to `/create-pr`.

**Parse Arguments**

Interpret arguments as natural language instructions:

- References to "title" → update title
- References to "description" or "body" → regenerate description
- Quoted text → use as new title or append to description
- Everything else → additional context for description

**Semantic Change Analysis**

Same process as Pull Requests: read the diff, analyze intent, generate content.

**Execute Update**

```bash
gh pr edit --title "$title" --body "$body"
```

Push any local commits after updating.

For the complete update workflow with detailed steps and examples, refer to `references/update-pr.md`.

## Issues

Create GitHub issues with automatic template selection and label application. The workflow intelligently chooses the appropriate issue template based on the description content and applies relevant labels for repositories where you have write access.

### Workflow Steps

**Check for Issue Templates**

Search the repository for issue templates:

```bash
ls -la .github/ISSUE_TEMPLATE/
```

Templates may be in YAML or Markdown format. Parse YAML frontmatter to extract:

- Template name
- Description
- Labels to auto-apply

**Auto-Select Template**

Analyze the issue description to determine the most appropriate template:

- Bug reports: errors, crashes, unexpected behavior
- Feature requests: enhancements, new functionality
- Documentation: docs improvements, clarifications
- Questions: how-to, usage inquiries

If no template matches or templates don't exist, proceed without one.

**Apply Labels**

For repositories where you have write access, apply labels using the `--label` flag:

```bash
gh issue create --label "bug" --label "needs-triage"
```

Extract labels from:

- Selected template metadata
- Issue description content (infer appropriate labels)

**Support Similar Issue Search**

When `--check` flag is provided, search for similar existing issues before creating:

```bash
gh issue list --search "search terms" --state all
```

Display results and ask user if they want to proceed with creation.

**Create Issue**

Execute the gh command with generated title, body, and metadata. Pass multi-line bodies using HEREDOC syntax. Return the issue URL to the user.

For the complete issue creation workflow with template examples, label strategies, and search patterns, refer to `references/create-issue.md`.

## Claude Code Issues

Create issues specifically in the anthropics/claude-code repository with environment information gathering and specialized templates. This workflow is optimized for reporting bugs, requesting features, or improving documentation for Claude Code itself.

### Workflow Steps

**Identify Issue Type**

Determine which template to use based on user intent:

- `bug_report`: Errors, crashes, unexpected behavior
- `feature_request`: New functionality or enhancements
- `documentation`: Docs improvements or clarifications
- `model_behavior`: Issues related to Claude's responses or reasoning

**Gather Environment Information**

Collect relevant environment details:

```bash
# Claude Code version
claude --version

# Operating system (macOS format: "macOS Tahoe v26.2")
scripts/get-macos-version.sh

# Terminal emulator (macOS)
echo $TERM_PROGRAM

# Shell
echo $SHELL
```

**Generate Issue Body**

Create structured content following the selected template format:

- Clear description of the issue or request
- Steps to reproduce (for bugs)
- Expected vs actual behavior (for bugs)
- Environment information section
- Additional context or screenshots

Use GitHub admonitions for important callouts:

```markdown
> [!IMPORTANT]
> This issue affects all macOS users on Apple Silicon
```

**Create in anthropics/claude-code**

Execute the gh command targeting the correct repository:

```bash
gh issue create \
  --repo anthropics/claude-code \
  --title "Issue title" \
  --body "$(cat <<'EOF'
Issue content here
EOF
)"
```

Return the issue URL to the user.

For the complete Claude Code issue workflow with template examples and environment gathering scripts, refer to `references/issue-claude-code.md`.

## Codex CLI Issues

Create issues specifically in the openai/codex repository with environment information gathering and specialized templates. This workflow is optimized for reporting bugs, requesting features, improving documentation, or reporting VS Code extension issues for Codex CLI.

### Workflow Steps

**Identify Issue Type**

Determine which template to use based on user intent:

- `2-bug-report`: Errors, crashes, unexpected behavior in CLI
- `4-feature-request`: New functionality or enhancements
- `3-docs-issue`: Docs improvements or clarifications
- `5-vs-code-extension`: Issues with the VS Code/Cursor/Windsurf extension

**Gather Environment Information**

Collect relevant environment details:

```bash
# Codex CLI version
codex --version

# Platform (macOS format: "macOS Tahoe v26.2")
scripts/get-macos-version.sh

# For VS Code extension issues
code --version
```

**Generate Issue Body**

Create structured content following the selected template format:

- Clear description of the issue or request
- Steps to reproduce (for bugs)
- Expected vs actual behavior (for bugs)
- Environment information section (version, platform, model, subscription)
- Additional context

**Create in openai/codex**

Execute the gh command targeting the correct repository:

```bash
gh issue create \
  --repo openai/codex \
  --title "Issue title" \
  --body "$(cat <<'EOF'
Issue content here
EOF
)"
```

Return the issue URL to the user.

For the complete Codex CLI issue workflow with template examples and environment gathering scripts, refer to `references/issue-codex-cli.md`.

## Sablier Issues

Create issues in `sablier-labs/*` repositories with automatic label application. Since the user is the org owner, labels are always applied across four dimensions: Type, Work (Cynefin), Priority, and Effort. The `sablier-labs/command-center` repository additionally supports Scope labels for domain categorization.

### Workflow Steps

**Parse Repository**

The first argument token is the repo name (without org prefix). It maps to `sablier-labs/{repo_name}`.

**Apply Labels**

Always applied (org owner). Analyze issue content to determine:

- Type (bug, feature, docs, etc.)
- Work complexity (clear, complicated, complex, chaotic)
- Priority (0-3)
- Effort (low, medium, high, epic)
- Scope (frontend, backend, evm, solana, etc. — command-center only)

**Generate Issue Body**

Uses a default template with Problem, Solution, and Files Affected sections. No YAML/Markdown template detection—Sablier repos don't use GitHub issue templates.

**Create in sablier-labs/{repo_name}**

```bash
gh issue create \
  --repo "sablier-labs/{repo_name}" \
  --title "$title" \
  --body "$body" \
  --label "type: feature,work: clear,priority: 2,effort: medium"
```

Return the issue URL to the user.

For the complete Sablier issue workflow with label reference tables, scope labels, and examples, refer to `references/issue-sablier.md`.

## Discussions

Create GitHub discussions using the GraphQL API with automatic category selection. Discussions are ideal for Q&A, ideas, announcements, and general community conversations that don't fit the issue format.

### Workflow Steps

**Fetch Repository Information**

Query the repository to get its node ID:

```bash
gh api graphql -f query='
  query($owner: String!, $repo: String!) {
    repository(owner: $owner, name: $repo) {
      id
    }
  }
' -f owner="OWNER" -f repo="REPO"
```

**Fetch Discussion Categories**

Query available categories for the repository:

```bash
gh api graphql -f query='
  query($owner: String!, $repo: String!) {
    repository(owner: $owner, name: $repo) {
      discussionCategories(first: 10) {
        nodes {
          id
          name
          description
        }
      }
    }
  }
' -f owner="OWNER" -f repo="REPO"
```

**Auto-Select Category**

Analyze the discussion title and body to choose the most appropriate category:

- **Ideas**: Feature suggestions, proposals, brainstorming
- **Q&A**: Questions seeking answers, how-to inquiries
- **General**: Broad discussions, community topics
- **Announcements**: Important updates (if you have permissions)
- **Show and Tell**: Demos, showcases, sharing work

If uncertain, default to "General" or ask the user to select.

**Support Similar Discussion Search**

When `--check` flag is provided, search for similar existing discussions:

```bash
gh api graphql -f query='
  query($owner: String!, $repo: String!, $search: String!) {
    repository(owner: $owner, name: $repo) {
      discussions(first: 5, orderBy: {field: CREATED_AT, direction: DESC}, filterBy: {query: $search}) {
        nodes {
          title
          url
        }
      }
    }
  }
' -f owner="OWNER" -f repo="REPO" -f search="search terms"
```

Display results and confirm before proceeding.

**Create Discussion**

Execute the GraphQL mutation to create the discussion:

```bash
gh api graphql -f query='
  mutation($repositoryId: ID!, $categoryId: ID!, $title: String!, $body: String!) {
    createDiscussion(input: {
      repositoryId: $repositoryId
      categoryId: $categoryId
      title: $title
      body: $body
    }) {
      discussion {
        url
      }
    }
  }
' -f repositoryId="REPO_ID" -f categoryId="CATEGORY_ID" -f title="Title" -f body="Body"
```

Return the discussion URL to the user.

For the complete discussion workflow with GraphQL examples, category selection logic, and search patterns, refer to `references/create-discussion.md`.

## Common Patterns

Shared conventions and patterns used across all OSS contribution workflows.

### HEREDOC for Multi-line Content

Always use HEREDOC syntax when passing multi-line bodies to gh commands:

```bash
gh pr create --title "Title" --body "$(cat <<'EOF'
First paragraph

Second paragraph
EOF
)"
```

The single quotes around `'EOF'` prevent variable expansion, ensuring literal content is passed.

### GitHub Admonitions

Use GitHub-flavored markdown admonitions to highlight important information:

```markdown
> [!NOTE]
> Useful information that users should know

> [!TIP]
> Helpful advice for doing things better

> [!IMPORTANT]
> Key information users need to know

> [!WARNING]
> Urgent info that needs immediate attention

> [!CAUTION]
> Advises about risks or negative outcomes
```

Apply these judiciously—overuse reduces their impact.

### Semantic Analysis Over Mechanical Operations

Never generate content based solely on filenames or commit messages. Always read the actual changes:

```bash
# Read the diff
git diff base-branch...HEAD

# Or for specific files
git diff base-branch...HEAD -- path/to/file
```

Understand:

- What changed (the mechanics)
- Why it changed (the intent)
- How it fits into the broader system (the context)

Use this understanding to craft meaningful titles and descriptions that communicate value, not just mechanics.

### Informal Tone

Generated content should be conversational and approachable:

**Good:**

> This PR adds support for parsing YAML frontmatter in issue templates. Previously, we only supported markdown format, which meant users couldn't take advantage of GitHub's newer template features.

**Bad:**

> This pull request implements functionality for YAML frontmatter parsing in the issue template processing subsystem. The implementation enhances the system's capabilities regarding template format support.

Write like a human talking to another human, not like a technical specification.

### Error Handling

When operations fail, provide clear context:

- What was being attempted
- What went wrong
- What the user should do to fix it

Example:

```
Failed to create PR: current branch has no commits ahead of main.

Make sure you've committed your changes and that your branch differs from the base branch.
```

### Confirmation and Feedback

For destructive or significant operations:

- Show what will happen before executing
- Ask for confirmation when appropriate
- Provide clear feedback after completion

For search operations with `--check`:

- Display found items clearly
- Let the user decide whether to proceed
- Don't automatically skip creation if duplicates exist

## Additional Resources

For detailed workflows, examples, and edge case handling, refer to these reference documents:

- **`references/create-pr.md`** - Complete pull request workflow including git state validation, semantic analysis strategies, template examples, and reviewer management
- **`references/update-pr.md`** - Complete update PR workflow including argument parsing, semantic analysis, and title/description regeneration
- **`references/create-issue.md`** - Complete issue creation workflow including template parsing, label application strategies, and duplicate detection
- **`references/issue-claude-code.md`** - Claude Code-specific issue creation including all template formats, environment gathering scripts, and submission guidelines
- **`references/issue-codex-cli.md`** - Codex CLI-specific issue creation including bug reports, feature requests, docs issues, and VS Code extension templates
- **`references/issue-sablier.md`** - Sablier-specific issue creation for `sablier-labs/*` repos including label taxonomy, scope labels for command-center, and default template
- **`references/issue-biome.md`** - Biome-specific issue creation including playground reproduction links, formatter/linter bug templates, and environment detection
- **`references/create-discussion.md`** - GitHub discussions workflow including GraphQL queries, category selection logic, and search strategies

These references provide implementation details, code examples, and troubleshooting guidance for each workflow type.
