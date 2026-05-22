---
name: gitlab-skill
description: GitLab integration for fetching issues/MRs, generating executive summaries, performing comprehensive code reviews, and automating issue resolution workflows. Use when working with GitLab issues, merge requests, or when asked to summarize, review, comment on, or resolve GitLab work items.
---

# GitLab Integration

## Purpose

This skill provides comprehensive GitLab integration capabilities, enabling automated workflows for issue management, code review, and project insights. It bridges GitLab data with intelligent analysis and action, supporting both read operations (summaries, reviews) and write operations (posting comments, creating merge requests).

## When to Use This Skill

Invoke this skill when:
- Fetching or analyzing GitLab issues or merge requests
- Generating executive summaries of issues
- Performing code reviews on merge requests
- Posting comments or updates to GitLab issues/MRs
- Automating issue resolution (fetch issue → implement fix → create MR)
- Aggregating project insights across multiple issues or MRs
- The user mentions GitLab issue numbers (e.g., "#123") or MR numbers (e.g., "!456")

## Prerequisites

### Configuration Setup

This skill supports multiple GitLab instances through a configuration file, making it easy to work with different GitLab servers (work, personal, clients, etc.).

**Option 1: Configuration File (Recommended for Multiple Instances)**

Create a `gitlab_config.json` file in one of these locations:
- `./gitlab_config.json` (current directory)
- `~/.gitlab/config.json` (user home directory)
- Next to the skill's scripts directory

Example configuration:

```json
{
  "default": "work",
  "instances": {
    "work": {
      "url": "https://gitlab.company.com",
      "token": "glpat-xxxxxxxxxxxxxxxxxxxx",
      "description": "Company GitLab instance"
    },
    "personal": {
      "url": "https://gitlab.com",
      "token": "glpat-yyyyyyyyyyyyyyyyyyyy",
      "description": "Personal GitLab projects"
    },
    "client": {
      "url": "https://gitlab.client.com",
      "token": "glpat-zzzzzzzzzzzzzzzzzzzz",
      "description": "Client project GitLab"
    }
  }
}
```

See `gitlab_config.json.template` in the skill directory for a complete example.

**Option 2: Environment Variables (Single Instance)**

For a single GitLab instance, set environment variables:

```bash
export GITLAB_URL="https://gitlab.com"
export GITLAB_TOKEN="glpat-xxxxxxxxxxxxxxxxxxxx"
```

**Generating a GitLab Personal Access Token:**
1. Navigate to GitLab → Settings → Access Tokens
2. Create a token with `api` scope
3. Copy the token and add it to your config file or environment

**Listing Configured Instances:**

To see all configured GitLab instances:
```bash
python scripts/gitlab_api.py list-instances
```

### Project Aliases

To avoid typing full project IDs repeatedly, configure project aliases in your `gitlab_config.json`:

```json
{
  "default": "work",
  "instances": { ... },
  "projects": {
    "webapp": {
      "project_id": "acme/webapp",
      "instance": "work",
      "description": "Main company web application"
    },
    "blog": {
      "project_id": "john/personal-blog",
      "instance": "personal",
      "description": "My personal blog"
    },
    "mobile": {
      "project_id": "123",
      "instance": "client",
      "description": "Client mobile app (numeric ID)"
    }
  }
}
```

**Benefits:**
- Type `webapp` instead of `acme/webapp`
- Automatically uses the correct GitLab instance for each project
- Self-documenting project list with descriptions

**Listing Configured Projects:**

To see all configured project aliases:
```bash
python scripts/gitlab_api.py list-projects
```

**Using Project Aliases:**

```bash
# Use project alias - automatically uses the configured instance
python scripts/gitlab_api.py get-issue webapp 123

# Use full project ID (still works)
python scripts/gitlab_api.py get-issue "acme/webapp" 123

# Override instance for a specific command
python scripts/gitlab_api.py --instance=personal get-issue webapp 123
```

## Working with Multiple GitLab Instances and Projects

### Instance Selection

When using the configuration file, specify which instance to use with the `--instance=<name>` flag:

```bash
# Use the default instance (specified in config)
python scripts/gitlab_api.py get-issue "acme/webapp" 123

# Use a specific instance
python scripts/gitlab_api.py --instance=personal get-issue "myproject" 456
python scripts/gitlab_api.py --instance=client list-issues "client/project"
```

If no `--instance` flag is provided, the skill uses the instance marked as "default" in the config file.

### Project Aliases

Configure project aliases to avoid typing full project IDs and to automatically use the correct instance:

```bash
# With project alias (automatically uses configured instance)
python scripts/gitlab_api.py get-issue webapp 123
python scripts/gitlab_api.py list-mrs api

# List all configured project aliases
python scripts/gitlab_api.py list-projects
```

**Instance Resolution Priority:**
1. Explicit `--instance=<name>` flag (highest priority)
2. Instance specified in project configuration
3. Default instance from config file (lowest priority)

**Examples:**

```bash
# Uses instance from project config (webapp → work instance)
python scripts/gitlab_api.py get-issue webapp 123

# Override with explicit instance flag
python scripts/gitlab_api.py --instance=personal get-issue webapp 123

# Full project ID with explicit instance
python scripts/gitlab_api.py --instance=client get-issue "client/project" 456
```

## Core Workflows

### Workflow 1: Fetch and Summarize an Issue

**Trigger Examples:**
- "Summarize issue #247"
- "What's the status of #123?"
- "Give me an executive summary of issue 456 in project acme/webapp"

**Steps:**

1. **Fetch the issue data:**
   ```bash
   python scripts/gitlab_api.py get-issue <project_id> <issue_iid>
   ```
   This returns JSON with issue details, description, labels, state, and all comments.

2. **Load the summary format reference:**
   Read `references/issue_summary_format.md` to understand the executive summary structure.

3. **Analyze the issue data:**
   - Extract key information: title, state, labels, description, comments
   - Identify the core problem and business impact
   - Determine current status and next steps
   - Note affected users/systems and severity

4. **Generate the executive summary:**
   Follow the format defined in `references/issue_summary_format.md`:
   - Start with a header showing status, priority, and last update
   - Write 2-3 sentence executive summary focusing on business impact
   - Include key details: Problem, Impact, Current Status, Next Steps
   - Add context only if necessary for understanding
   - Keep total length under 200 words

5. **Optional - Post summary as comment:**
   If requested, post the summary back to the issue:
   ```bash
   python scripts/gitlab_api.py post-issue-comment <project_id> <issue_iid> "<summary_markdown>"
   ```

**Examples:**

```
User: "Summarize issue #247 in acme/webapp"

1. Fetch: python scripts/gitlab_api.py get-issue "acme/webapp" 247
2. Read references/issue_summary_format.md
3. Analyze issue data focusing on business impact
4. Generate executive summary following the format
5. Present summary to user
```

```
User: "Summarize issue #123 in webapp"

1. Resolve project: "webapp" → "acme/webapp" (instance: work)
2. Fetch: python scripts/gitlab_api.py get-issue webapp 123
3. Read references/issue_summary_format.md
4. Analyze and generate summary
5. Present to user
```

```
User: "Summarize issue #456 in my blog project"

1. Determine project alias: "blog" from context
2. Resolve: "blog" → "john/personal-blog" (instance: personal)
3. Fetch: python scripts/gitlab_api.py get-issue blog 456
4. Read references/issue_summary_format.md
5. Analyze and generate summary
6. Present to user
```

### Workflow 2: Review a Merge Request

**Trigger Examples:**
- "Review MR !89"
- "Code review merge request 145 in acme/api"
- "Check the code in !234 for security issues"

**Steps:**

1. **Fetch the merge request data:**
   ```bash
   python scripts/gitlab_api.py get-mr <project_id> <mr_iid>
   ```
   This returns MR metadata, changes (diffs), and comments.

2. **Get the full diff:**
   ```bash
   python scripts/gitlab_api.py get-diff <project_id> <mr_iid>
   ```
   This returns the unified diff format for all file changes.

3. **Load the code review style guide:**
   Read `references/code_review_style.md` to understand the review structure and focus areas.

4. **Analyze the code changes:**
   Review across four dimensions:
   - **Security:** Check for vulnerabilities, authentication issues, data exposure, injection risks
   - **Logic & Correctness:** Look for bugs, edge cases, race conditions, error handling gaps
   - **Performance:** Identify N+1 queries, inefficient algorithms, scalability concerns
   - **Code Quality:** Assess readability, duplication, maintainability, documentation

5. **Structure the review:**
   Follow the format from `references/code_review_style.md`:
   - Overview section with summary and recommendation
   - 🚨 Critical Issues (blockers)
   - ⚠️ Significant Concerns (should address)
   - 💡 Minor Suggestions (nice to have)
   - ✅ Positive Highlights (optional)

6. **Post the review:**
   ```bash
   python scripts/gitlab_api.py post-mr-comment <project_id> <mr_iid> "<review_markdown>"
   ```

**Example:**
```
User: "Review MR !89 in acme/webapp"

1. Fetch: python scripts/gitlab_api.py get-mr "acme/webapp" 89
2. Get diff: python scripts/gitlab_api.py get-diff "acme/webapp" 89
3. Read references/code_review_style.md
4. Analyze code across security, logic, performance, quality dimensions
5. Structure comprehensive review with categorized issues
6. Post review comment
```

### Workflow 3: Automated Issue Resolution

**Trigger Examples:**
- "Fix issue #123"
- "Implement the feature described in issue #456"
- "Resolve issue 789 and create an MR"

**Steps:**

1. **Fetch the issue:**
   ```bash
   python scripts/gitlab_api.py get-issue <project_id> <issue_iid>
   ```

2. **Understand the requirements:**
   Analyze the issue description and comments to understand:
   - What needs to be implemented or fixed
   - Acceptance criteria
   - Technical constraints or preferences mentioned

3. **Create a feature branch:**
   ```bash
   python scripts/auto_resolve_issue.py create-branch <issue_iid> "<issue_title>"
   ```
   This creates a branch named `issue-{iid}-{sanitized-title}`.

4. **Implement the solution:**
   - Use standard development tools (Read, Write, Edit, Bash) to implement the fix
   - Follow the codebase's existing patterns and conventions
   - Write or update tests as appropriate
   - Ensure the solution addresses the issue requirements

5. **Commit the changes:**
   ```bash
   git add .
   git commit -m "Fix issue #<iid>: <brief description>

   <detailed explanation>

   Closes #<issue_iid>"
   ```

6. **Push the branch:**
   ```bash
   python scripts/auto_resolve_issue.py push-branch <branch_name>
   ```

7. **Create a merge request:**
   ```bash
   python scripts/auto_resolve_issue.py create-mr <project_id> <source_branch> <target_branch> "Fix #<iid>: <title>" "<description>" <issue_iid>
   ```
   This automatically links the MR to the issue with "Closes #<iid>".

8. **Post update to the issue:**
   ```bash
   python scripts/gitlab_api.py post-issue-comment <project_id> <issue_iid> "I've implemented a fix for this issue. Please review MR !<mr_iid>."
   ```

**Example:**
```
User: "Fix issue #123 in acme/webapp"

1. Fetch: python scripts/gitlab_api.py get-issue "acme/webapp" 123
2. Analyze issue requirements
3. Create branch: python scripts/auto_resolve_issue.py create-branch 123 "Fix checkout discount bug"
4. Implement the fix using Read, Write, Edit tools
5. Commit: git commit with reference to #123
6. Push: python scripts/auto_resolve_issue.py push-branch "issue-123-fix-checkout-discount-bug"
7. Create MR: python scripts/auto_resolve_issue.py create-mr "acme/webapp" "issue-123-..." "main" "Fix #123: Checkout discount bug" "..." 123
8. Post comment: python scripts/gitlab_api.py post-issue-comment "acme/webapp" 123 "Fix implemented in MR !<iid>"
```

### Workflow 4: Aggregate Project Insights

**Trigger Examples:**
- "What's the status of all open issues in acme/webapp?"
- "Give me a report on recent issues"
- "Show me issue statistics by label"

**Steps:**

1. **Fetch aggregate data:**
   ```bash
   python scripts/gitlab_api.py aggregate-issues <project_id> [days]
   ```
   This returns statistics including:
   - Total issue count
   - Opened vs closed counts
   - Issues grouped by label
   - 10 most recently updated issues

2. **Analyze the data:**
   - Identify trends (high number of bugs, feature requests piling up)
   - Note priority issues (critical, high labels)
   - Detect potential problems (many stale issues, unassigned critical bugs)

3. **Generate insights report:**
   Create a structured summary:
   - Overview statistics
   - Key trends and patterns
   - High-priority or concerning issues
   - Recommendations

4. **Optional - List specific issues:**
   If deeper analysis is needed:
   ```bash
   python scripts/gitlab_api.py list-issues <project_id> [state] [labels...]
   ```

**Example:**
```
User: "Status report for acme/webapp"

1. Fetch: python scripts/gitlab_api.py aggregate-issues "acme/webapp" 7
2. Analyze statistics and recent activity
3. Generate insights report highlighting:
   - 15 open issues (3 critical)
   - Bug reports increased 40% this week
   - 2 critical issues unassigned
   - Recommendation: Triage unassigned critical bugs
```

### Workflow 5: List and Filter Issues/MRs

**Trigger Examples:**
- "Show me all open bugs"
- "List closed issues from last sprint"
- "What MRs are waiting for review?"

**Steps:**

1. **For issues:**
   ```bash
   python scripts/gitlab_api.py list-issues <project_id> [state] [label1 label2 ...]
   ```
   Parameters:
   - `state`: "opened" (default), "closed", or "all"
   - `labels`: Optional filter by label(s)

2. **For merge requests:**
   ```bash
   python scripts/gitlab_api.py list-mrs <project_id> [state]
   ```
   Parameters:
   - `state`: "opened" (default), "closed", "merged", or "all"

3. **Process and present the results:**
   - Format as a readable list or table
   - Highlight key information (title, status, assignee, labels, last updated)
   - Group or sort as appropriate (by priority, date, etc.)

**Example:**
```
User: "Show me all open bugs in acme/api"

1. Fetch: python scripts/gitlab_api.py list-issues "acme/api" "opened" "bug"
2. Format results as table showing: IID, Title, Priority, Assignee, Updated
3. Present to user
```

## Script Reference

### scripts/gitlab_api.py

Primary script for GitLab API interactions.

**Usage:**
```bash
python scripts/gitlab_api.py [--instance=<name>] <command> [args...]
```

**Options:**
- `--instance=<name>` - Specify which GitLab instance to use (from config file)

**Commands:**
- `list-instances` - List all configured GitLab instances
- `list-projects` - List all configured project aliases
- `get-issue <project> <issue_iid>` - Fetch issue with comments
- `list-issues <project> [state] [labels...]` - List issues with optional filters
- `get-mr <project> <mr_iid>` - Fetch merge request with changes and comments
- `list-mrs <project> [state]` - List merge requests
- `post-issue-comment <project> <issue_iid> <comment>` - Post comment on issue
- `post-mr-comment <project> <mr_iid> <comment>` - Post comment on MR
- `get-diff <project> <mr_iid>` - Get unified diff for MR
- `aggregate-issues <project> [days]` - Get issue statistics

**Project Parameter:**
- Can be a project alias from config (e.g., "webapp")
- Or numeric project ID (e.g., "123")
- Or namespace/project-name format (e.g., "acme/webapp")
- All formats are automatically URL-encoded

**Examples:**
```bash
# List configured instances and projects
python scripts/gitlab_api.py list-instances
python scripts/gitlab_api.py list-projects

# Use project alias (automatically uses configured instance)
python scripts/gitlab_api.py get-issue webapp 123

# Use full project ID with default instance
python scripts/gitlab_api.py get-issue "acme/webapp" 123

# Use specific instance
python scripts/gitlab_api.py --instance=personal get-issue blog 456

# Override project's configured instance
python scripts/gitlab_api.py --instance=work get-issue blog 789
```

### scripts/auto_resolve_issue.py

Automation script for issue resolution workflow.

**Usage:**
```bash
python scripts/auto_resolve_issue.py [--instance=<name>] <command> [args...]
```

**Options:**
- `--instance=<name>` - Specify which GitLab instance to use (only needed for create-mr command)

**Commands:**
- `create-branch <issue_iid> <issue_title>` - Create feature branch from issue
- `push-branch <branch_name>` - Push branch to remote
- `create-mr <project> <source_branch> <target_branch> <title> <description> <issue_iid>` - Create MR with issue link

**Notes:**
- The `--instance` flag is only required for the `create-mr` command, which needs to authenticate with GitLab API
- `<project>` can be a project alias or full project ID
- Project aliases automatically use their configured instance (unless overridden with `--instance` flag)

**Examples:**
```bash
# Create MR using project alias
python scripts/auto_resolve_issue.py create-mr webapp "feature-branch" "main" "Add feature" "Description" 123

# Create MR using full project ID with specific instance
python scripts/auto_resolve_issue.py --instance=client create-mr "client/project" "fix-bug" "main" "Fix" "..." 456
```

## Reference Files

### references/issue_summary_format.md

Comprehensive guide for generating executive summaries of GitLab issues. Defines:
- Format structure (header, executive summary, key details, context)
- Length and tone guidelines
- Examples and anti-patterns
- Focus on business impact over technical details

**When to use:** Before generating any issue summary, read this file to ensure consistency and quality.

### references/code_review_style.md

Detailed guide for performing comprehensive code reviews on merge requests. Covers:
- Review structure (overview, critical issues, concerns, suggestions, highlights)
- Four review dimensions: Security, Logic, Performance, Code Quality
- Specific items to check in each dimension
- Tone and communication guidelines
- Example reviews and comments

**When to use:** Before reviewing any merge request, read this file to ensure thorough and consistent reviews.

## Best Practices

### Project Organization

**Configure Project Aliases for Frequently Used Projects:**
- Add all projects you regularly work with to the `projects` section
- Use short, memorable aliases (e.g., "api", "web", "mobile")
- Include descriptions to document what each project is
- Associate each project with its primary instance

**Example:**
```json
{
  "projects": {
    "api": {
      "project_id": "acme/backend-api",
      "instance": "work",
      "description": "Main backend API service"
    },
    "docs": {
      "project_id": "acme/documentation",
      "instance": "work",
      "description": "Technical documentation site"
    }
  }
}
```

**Benefits:**
- Faster command execution (less typing)
- Automatic instance selection (no need to remember which instance each project is on)
- Self-documenting configuration

### Error Handling

All scripts handle errors gracefully and output to stderr. If a script fails:
1. Check that your GitLab configuration is set up correctly:
   - Run `python scripts/gitlab_api.py list-instances` to verify config
   - Ensure the config file exists in one of the searched locations
   - Verify the instance name is correct if using `--instance` flag
2. Verify the project ID and issue/MR IID are correct
3. Ensure the token has `api` scope permissions
4. Check the error message for specific API issues

**Common configuration errors:**
- "GitLab configuration not found" - Create `gitlab_config.json` or set environment variables
- "Instance 'X' not found in config" - Check instance name and config file
- "No default instance specified" - Set a "default" field in your config file

### Project ID Determination

When the user doesn't specify a project ID:
1. Check if the current directory is a git repository
2. Look for GitLab remote URL: `git remote get-url origin`
3. Extract project namespace/name from the remote URL
4. Use this as the default project ID

### Working with Large Issues/MRs

For issues or MRs with extensive comments or large diffs:
1. Focus analysis on the most recent and relevant information
2. Summarize comment threads rather than repeating everything
3. For large diffs, identify the most critical files/changes first
4. Use the structured format to keep summaries/reviews concise

### Posting Comments

When posting comments back to GitLab:
1. Use markdown formatting for readability
2. Include links to related issues/MRs when relevant
3. Keep comments professional and constructive
4. For code reviews, use the structured format to organize feedback

### Security Considerations

1. **Never commit the GitLab token or config file** to version control
   - Add `gitlab_config.json` to your `.gitignore`
   - Use the template file (`gitlab_config.json.template`) for sharing
2. **Protect your config file** with appropriate file permissions
   - Run: `chmod 600 ~/.gitlab/config.json`
3. **Use environment variables** for CI/CD or temporary access
4. **Rotate tokens regularly** and update your config file
5. **Validate user input** before passing to API scripts
6. **Be cautious with automation** - confirm destructive actions with user first

## Troubleshooting

**Issue: "GitLab configuration not found"**
- Solution: Create a `gitlab_config.json` file in one of the searched locations
- Or set `GITLAB_URL` and `GITLAB_TOKEN` environment variables
- Run `python scripts/gitlab_api.py list-instances` to check configuration

**Issue: "Instance 'X' not found in config"**
- Solution: Check the instance name spelling
- Run `python scripts/gitlab_api.py list-instances` to see available instances
- Verify the config file has an "instances" object with your instance

**Issue: "No default instance specified in config"**
- Solution: Add a "default" field to your config file pointing to an instance name
- Or use the `--instance=<name>` flag explicitly
- Or configure projects with instance associations

**Issue: Project alias not found**
- Solution: Run `python scripts/gitlab_api.py list-projects` to see available aliases
- Check spelling of project alias
- Add the project to your config file's "projects" section if needed
- Or use the full project ID instead

**Issue: "HTTP 404 Not Found"**
- Solution: Verify project ID and issue/MR IID are correct
- Check project visibility and token permissions
- Ensure you're using the correct GitLab instance

**Issue: "HTTP 401 Unauthorized"**
- Solution: Regenerate GitLab token with `api` scope
- Verify token is correctly set in config file
- Check that the token hasn't expired

**Issue: "HTTP 403 Forbidden"**
- Solution: Check token has appropriate permissions for the action
- Verify you have access to the project on that GitLab instance

**Issue: Git commands fail in auto_resolve_issue.py**
- Solution: Ensure current directory is a git repository
- Check git configuration is properly set up
- Verify remote 'origin' is configured

## Examples

### Example 1: Quick Issue Summary
```
User: "What's issue #456 about in webapp?"

Response steps:
1. Identify project alias: "webapp"
2. Fetch: python scripts/gitlab_api.py get-issue webapp 456
3. Read references/issue_summary_format.md
4. Generate concise summary focusing on: what, impact, status
5. Present to user
```

### Example 2: Comprehensive MR Review with Comments
```
User: "Review !234 and post your feedback"

Response steps:
1. Fetch MR: python scripts/gitlab_api.py get-mr "acme/webapp" 234
2. Get diff: python scripts/gitlab_api.py get-diff "acme/webapp" 234
3. Read references/code_review_style.md
4. Analyze across all four dimensions
5. Structure review with critical issues, concerns, suggestions
6. Post: python scripts/gitlab_api.py post-mr-comment "acme/webapp" 234 "<review>"
7. Confirm to user that review was posted
```

### Example 3: End-to-End Issue Resolution
```
User: "Please fix issue #123 in the webapp project"

Response steps:
1. Identify project: "webapp" alias
2. Fetch: python scripts/gitlab_api.py get-issue webapp 123
3. Analyze requirements from issue description
4. Create branch: python scripts/auto_resolve_issue.py create-branch 123 "Fix login bug"
5. Implement fix using development tools
6. Test the fix
7. Commit changes with message referencing #123
8. Push: python scripts/auto_resolve_issue.py push-branch "issue-123-fix-login-bug"
9. Create MR: python scripts/auto_resolve_issue.py create-mr webapp "issue-123-fix-login-bug" "main" "Fix #123: Login bug" "Fixes the login authentication issue" 123
10. Post update: python scripts/gitlab_api.py post-issue-comment webapp 123 "Fix implemented in MR !<iid>"
11. Provide MR link to user
```

## Integration with Other Tools

This skill works seamlessly with:
- **Git workflows:** Branch creation, commits, pushes
- **Development tools:** Read, Write, Edit for implementing fixes
- **Testing tools:** Run tests before creating MRs
- **CI/CD pipelines:** MRs trigger automated builds and tests

## Extending the Skill

To add custom functionality:
1. **Add new scripts** in `scripts/` for new automation workflows
2. **Create reference files** in `references/` for new formats or standards
3. **Update SKILL.md** to document new workflows and usage patterns
