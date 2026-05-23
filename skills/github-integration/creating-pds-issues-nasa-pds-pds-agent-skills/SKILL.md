---
name: creating-pds-issues
description: Create GitHub issues in NASA-PDS repositories using organizational templates (bug reports, I&T bug reports, feature requests, tasks, vulnerabilities, release themes). Use when user requests to create, file, or submit PDS issues.
---

# Creating PDS Issues Skill

This skill creates GitHub issues in NASA-PDS repositories using the official organizational templates. It ensures consistent issue formatting while keeping content clear and concise.

## Prerequisites

- GitHub CLI (`gh`) must be installed and authenticated
- User must have write access to the target NASA-PDS repository

## Workflow

### 0. Detect Sub-Issue Request

**Before gathering other information, determine if this is a sub-issue request.**

Keywords that indicate a sub-issue relationship:
- "child task", "child issue", "sub-task", "sub-issue"
- "for theme", "for epic", "under issue", "part of"
- "attached to", "linked to parent", "belongs to"
- Explicit parent references: "for #123", "under NASA-PDS/repo#456"

If a sub-issue relationship is detected:
1. Identify the parent issue (theme, epic, or other issue)
2. Proceed with normal issue creation workflow
3. After creation, attach as sub-issue using GitHub GraphQL API (see Section 4)

**Parent Issue Identification:**

The parent can be specified as:
- Issue URL: `https://github.com/NASA-PDS/repo/issues/123`
- Short reference: `#123` (current repo) or `NASA-PDS/repo#123` (cross-repo)
- Search terms: "the registry theme" or "authentication epic"

If the parent is ambiguous, search for it:
```bash
# Search for potential parent issues by title
gh issue list --repo NASA-PDS/<repo> --search "theme OR epic" --label "theme,Epic" --limit 10
```

Then confirm with the user which parent issue to use.

### 1. Gather Information

**Detect Current Repository (if applicable):**

If the user is running this skill from within a cloned git repository, automatically detect the repository name:

```bash
# Check if in a git repo - try origin first, then upstream
git remote get-url origin 2>/dev/null || git remote get-url upstream 2>/dev/null
```

If the remote URL matches `NASA-PDS/<repo-name>`, use that as the default repository.

**Edge Cases:**
- **Multiple remotes:** Prefer `origin` first, then fall back to `upstream` or other NASA-PDS remotes
- **Forks:** If the detected repository is a fork (personal namespace), check for an `upstream` remote pointing to NASA-PDS
- **Non-NASA-PDS repos:** If no NASA-PDS remote is found, ask the user which repository to use
- **Ambiguous remotes:** If multiple NASA-PDS remotes exist, ask the user to clarify

**Determine Issue Type:**

Ask the user what type of issue to create using the AskUserQuestion tool with these options:

- **Bug Report** - Report defects or unexpected behavior
- **I&T Bug Report** - Internal Integration & Test bug report (requires test case references)
- **Feature Request** - Propose new features or enhancements
- **Task** - Internal development task (often sub-tasks of larger stories)
- **Vulnerability** - Security vulnerabilities or threats
- **Release Theme** - High-level epic for release planning

**Gather Template-Specific Information:**

Then gather the required information based on the template type:

**For Bug Reports:**
- Repository name (auto-detect from git remote, or ask if not in a repo or unclear)
- Brief title following format: `<system feature> <is not/does not> <expected behaviour>`
- Bug description (what happened)
- Expected behavior (what should have happened)
- Steps to reproduce (numbered list)
- Environment info (version, OS, etc.)

**For I&T Bug Reports:**
- Repository name (auto-detect from git remote, or ask if not in a repo or unclear)
- Brief title following format: `<system feature> <is not/does not> <expected behaviour>`
- Bug description (what happened)
- Expected behavior (what should have happened)
- **Related test cases** (TestRail or other test case references - REQUIRED)
- Steps to reproduce (numbered list)
- Environment info (version, OS, etc.)

**For Feature Requests:**
- Repository name (auto-detect from git remote, or ask if not in a repo or unclear)
- User story title: `As a <role>, I want to <accomplish>`
- User persona (e.g., "Data Engineer", "Node Operator")
- Motivation (why is this needed?)
- Additional context

**For Tasks:**
- Repository name (auto-detect from git remote, or ask if not in a repo or unclear)
- Task type (sub-task or theme)
- Description (clear but not excessive)

**For Vulnerabilities:**
- Repository name (auto-detect from git remote, or ask if not in a repo or unclear)
- Title: `<system feature> <is not/does not> <expected behaviour>`
- Vulnerability description
- Expected secure behavior
- Reproduction steps
- Environment info

**For Release Themes:**
- Repository name (auto-detect from git remote, or ask if not in a repo or unclear)
- Description of the release theme

### 2. Fill the Template

Use the cached templates in `resources/templates/` directory. If templates are not cached, run the caching script first:

```bash
cd creating-pds-issues
node scripts/cache-templates.mjs
```

Fill templates with these guidelines:

**Content Style:**
- Be clear and specific, but concise
- Avoid unnecessary elaboration or "novel-length" descriptions
- Use bullet points and numbered lists for clarity
- Include only essential technical details
- Skip optional fields unless user provides information

**Security and Privacy - CRITICAL:**
- **Remove or sanitize all sensitive information** before creating the issue
- Replace actual file paths with generic examples (e.g., `/Users/john/secrets/api-keys.txt` → `/path/to/file.txt`)
- Remove usernames, email addresses, and personal identifiers
- Replace IP addresses with dummy values (e.g., `192.168.1.100` → `10.0.0.1`)
- Strip API keys, tokens, passwords, and credentials
- Sanitize database connection strings and internal URLs
- Use placeholder hostnames (e.g., `prod-server-01.internal.nasa.gov` → `server.example.com`)
- Remove proprietary or confidential information
- If uncertain whether information is sensitive, ASK THE USER before including it

**Required Field Examples:**

*Bug description (good):*
```
When validating a PDS4 label with nested tables, the validator throws a NullPointerException
on line 342 of TableValidator.java. This occurs with labels containing 3+ nested table
definitions.
```

*Bug description (too verbose):*
```
I was working on my project late last night and I noticed that when I tried to validate
my carefully crafted PDS4 label that I had been working on for several days, the system
unexpectedly threw an error. I had been following all the documentation...
[continues for several paragraphs]
```

*Expected behavior (good):*
```
Validator should successfully validate labels with nested tables or provide a clear
error message about nesting limitations.
```

*Reproduction steps (good):*
```
1. Create PDS4 label with 3 nested <Table_Delimited> elements
2. Run: validate my-label.xml
3. Observe NullPointerException in output
```

*Feature motivation (good):*
```
...so that I can validate labels in CI/CD pipelines without manual intervention,
reducing deployment time from hours to minutes.
```

**Sanitization Examples:**

*Before (UNSAFE - contains sensitive info):*
```
When I run the validator on /Users/alice.johnson/Documents/NASA/mission-data/secret-project/labels/experiment-123.xml
using the API key sk-1234567890abcdef, it fails to connect to the database at
postgresql://admin:P@ssw0rd123@10.42.15.8:5432/pds_prod
```

*After (SAFE - sanitized):*
```
When running the validator on a PDS4 label file with the API configured, it fails to
connect to the PostgreSQL database with a connection timeout error.
```

*Before (UNSAFE - contains internal paths):*
```
The error log at /home/ops/pds-services/logs/validator-2024-11-13-prod.log shows:
ERROR: Connection refused by host pds-db-primary-01.jpl.nasa.gov
```

*After (SAFE - sanitized):*
```
The error log shows:
ERROR: Connection refused by database host
```

### 3. Create the Issue

Use GitHub CLI to create the issue with appropriate labels and metadata:

**Default Assignee:**
By default, issues requiring triage are assigned to `jordanpadams`. Users can override this by setting the `PDS_ISSUE_ASSIGNEE` environment variable or by using the `--assignee` flag.

**Bug Report:**
```bash
gh issue create \
  --repo NASA-PDS/<repo-name> \
  --title "<title>" \
  --body "<filled-template-body>" \
  --label "bug,needs:triage" \
  --assignee "${PDS_ISSUE_ASSIGNEE:-jordanpadams}"
```

**I&T Bug Report:**
```bash
gh issue create \
  --repo NASA-PDS/<repo-name> \
  --title "<title>" \
  --body "<filled-template-body>" \
  --label "B15.1,bug,needs:triage" \
  --assignee "${PDS_ISSUE_ASSIGNEE:-jordanpadams}"
```

**Feature Request:**
```bash
gh issue create \
  --repo NASA-PDS/<repo-name> \
  --title "<title>" \
  --body "<filled-template-body>" \
  --label "needs:triage,requirement" \
  --assignee "${PDS_ISSUE_ASSIGNEE:-jordanpadams}"
```

**Task:**
```bash
gh issue create \
  --repo NASA-PDS/<repo-name> \
  --title "<title>" \
  --body "<filled-template-body>" \
  --label "task,i&t.skip"
```

**Vulnerability:**
```bash
gh issue create \
  --repo NASA-PDS/<repo-name> \
  --title "<title>" \
  --body "<filled-template-body>" \
  --label "security,bug,needs:triage" \
  --assignee "${PDS_ISSUE_ASSIGNEE:-jordanpadams}"
```

**Release Theme:**
```bash
gh issue create \
  --repo NASA-PDS/<repo-name> \
  --title "<title>" \
  --body "<filled-template-body>" \
  --label "theme,Epic,i&t.skip"
```

**Template Body Format:**

The body should mirror the YAML template structure but in markdown. For example, a bug report body:

```markdown
## Checked for duplicates
Yes - I've already checked

## 🐛 Describe the bug
[Bug description here]

## 🕵️ Expected behavior
[Expected behavior here]

## 📜 To Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]

## 🖥 Environment Info
- Version of this software: vX.Y.Z
- Operating System: [OS details]

## 📚 Version of Software Used
[Version details]

## 🩺 Test Data / Additional context
[Context or N/A]

## 🦄 Related requirements
N/A

---
## For Internal Dev Team To Complete

## ⚙️ Engineering Details
[To be filled by engineering team]

## 🎉 Integration & Test
[To be filled by engineering team]
```

### 4. Attach Sub-Issue to Parent (If Applicable)

If this issue should be a sub-issue of a parent (theme, epic, or other issue), attach it using GitHub's GraphQL API.

**Step 1: Get the Parent Issue Node ID**

```bash
# Extract repo and issue number from parent reference
# For URL: https://github.com/NASA-PDS/repo/issues/123 → repo=repo, number=123
# For reference: NASA-PDS/repo#123 → repo=repo, number=123
# For local: #123 → use current repo, number=123

gh api graphql -f query='
  query {
    repository(owner: "NASA-PDS", name: "<parent-repo>") {
      issue(number: <parent-number>) {
        id
        title
      }
    }
  }
'
```

**Step 2: Get the Child Issue Node ID**

After creating the issue (from Section 3), extract the issue number from the returned URL and get its node ID:

```bash
# The gh issue create command returns: https://github.com/NASA-PDS/repo/issues/456
# Extract number 456 from the URL

gh api graphql -f query='
  query {
    repository(owner: "NASA-PDS", name: "<child-repo>") {
      issue(number: <child-number>) {
        id
      }
    }
  }
'
```

**Step 3: Add Sub-Issue Relationship**

```bash
gh api graphql -f query='
  mutation {
    addSubIssue(input: {
      issueId: "<PARENT_NODE_ID>",
      subIssueId: "<CHILD_NODE_ID>"
    }) {
      issue {
        id
        title
      }
      subIssue {
        id
        title
      }
    }
  }
'
```

**Combined Script Approach:**

For convenience, you can chain these operations:

```bash
# 1. Create the issue and capture the URL
ISSUE_URL=$(gh issue create \
  --repo NASA-PDS/<repo> \
  --title "<title>" \
  --body "<body>" \
  --label "<labels>" 2>&1)

# 2. Extract issue number from URL
CHILD_NUMBER=$(echo "$ISSUE_URL" | grep -oE '[0-9]+$')

# 3. Get parent node ID
PARENT_ID=$(gh api graphql -f query='
  query {
    repository(owner: "NASA-PDS", name: "<parent-repo>") {
      issue(number: <parent-number>) { id }
    }
  }
' --jq '.data.repository.issue.id')

# 4. Get child node ID
CHILD_ID=$(gh api graphql -f query="
  query {
    repository(owner: \"NASA-PDS\", name: \"<child-repo>\") {
      issue(number: $CHILD_NUMBER) { id }
    }
  }
" --jq '.data.repository.issue.id')

# 5. Attach sub-issue to parent
gh api graphql -f query="
  mutation {
    addSubIssue(input: {
      issueId: \"$PARENT_ID\",
      subIssueId: \"$CHILD_ID\"
    }) {
      issue { title }
      subIssue { title }
    }
  }
"
```

**Cross-Repository Sub-Issues:**

Sub-issues can span repositories. For example, a task in `pds-registry` can be a sub-issue of a theme in `pds-swg`. The parent and child repositories do not need to match.

**Error Handling:**

- If the parent issue doesn't exist: "Could not resolve to an Issue with the number..."
- If the GraphQL mutation fails: Check that both issues exist and you have write access
- If already a sub-issue: The API will return an error; check existing relationships first

### 5. Confirm Success

After creating the issue:
1. Display the issue URL to the user
2. Confirm the issue was created successfully
3. If a sub-issue relationship was created, confirm the parent-child link
4. Remind user that internal sections (Engineering Details, I&T) will be filled by the PDS engineering team

## Important Notes

- **All issues are added to project NASA-PDS/6** (PDS Engineering portfolio backlog)
- **Default assignee is jordanpadams** for triage (configurable via `PDS_ISSUE_ASSIGNEE` environment variable)
- **Leave internal sections blank** - "Engineering Details" and "Integration & Test" fields are filled by the PDS engineering team after triage
- **Skip optional fields** unless user explicitly provides information
- **Validate repository exists** before creating issue using `gh repo view NASA-PDS/<repo-name>`

## Template Caching

Templates are cached locally in `resources/templates/` to avoid repeated GitHub API calls. The caching script should:

1. Clone or fetch the latest templates from NASA-PDS/.github
2. Store them in `resources/templates/`
3. Update a timestamp file to track last cache update

Cache templates on first use or if cache is older than 7 days.

**Forcing Cache Refresh:**

If templates have been updated in NASA-PDS/.github and you need to refresh immediately:

```bash
# Option 1: Delete cache directory and re-run caching script
rm -rf creating-pds-issues/resources/templates/
cd creating-pds-issues
node scripts/cache-templates.mjs

# Option 2: Delete timestamp file to trigger automatic refresh
rm creating-pds-issues/resources/templates/.cache-timestamp
# Next skill invocation will automatically refresh templates

# Option 3: Set environment variable to force refresh
FORCE_TEMPLATE_REFRESH=true node scripts/cache-templates.mjs
```

## Error Handling

- If GitHub CLI is not authenticated, prompt: `gh auth login`
- If repository doesn't exist, list available repos: `gh repo list NASA-PDS --limit 100`
- If user lacks write access, display error and suggest contacting PDS Help Desk
- If required information is missing, ask user for specific details needed

## Example Invocations

User: "Create a bug report for pds-registry about validation errors"
→ Ask which template, gather bug details, create issue

User: "File a feature request for the API to support batch operations"
→ Ask which repo, gather user story details, create issue

User: "I need to create a security vulnerability issue for validate"
→ Use vulnerability template, gather security details, create issue

**Sub-Issue Examples:**

User: "Create a child task for theme #45 about implementing the new API endpoint"
→ Detect sub-issue request, gather task details, create issue, attach to #45 as sub-issue

User: "Add a sub-task under NASA-PDS/pds-swg#123 for updating the documentation"
→ Detect cross-repo sub-issue, gather task details, create issue, attach to parent in pds-swg

User: "Create a task for the registry modernization epic"
→ Search for "registry modernization" epic, confirm with user, gather task details, create and attach

User: "File a bug as part of the B17 theme issue"
→ Search for B17 theme, create bug report, attach as sub-issue to the theme
