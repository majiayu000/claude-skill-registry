---
name: create-task
description: "Create a GitHub issue, add it to a project, and set all metadata (status, priority, labels, milestone, type). Use when user wants to create a new task/issue."
argument-hint: "[task description or requirements]"
allowed-tools: "Bash, AskUserQuestion"
---

Create a new GitHub issue with full project board integration.

## Workflow

Follow these steps **in order**. Use `AskUserQuestion` (the `mcp_question` tool) to gather all required info before creating anything.

### Step 1: Detect the GitHub owner

Try to infer the GitHub owner/org from the current repository:

```bash
gh repo view --json owner --jq '.owner.login'
```

- If this succeeds, use the detected owner and confirm with the user.
- If this fails (e.g., not in a git repo), ask the user for the GitHub owner/org name.

Store this as `<owner>` for all subsequent commands.

### Step 2: Ask which project

Fetch the list of projects dynamically:

```bash
gh project list --owner <owner> --format json --jq '.projects[] | "\(.number) \(.title)"'
```

Then ask the user to select a project. Include a "None (no project)" option.

### Step 3: Ask for repo, title, assignee, description, and content style

Ask these in a single question block if possible:

1. **Repository** - List repos from the owner. Run:
   ```bash
   gh repo list <owner> --json name --jq '.[].name' --limit 50
   ```
   Let user select one.

2. **Title** - Ask for the issue title (free text).

3. **Assignee** - Fetch collaborators/members dynamically:
   ```bash
   gh api repos/<owner>/<repo>/collaborators --jq '.[].login'
   ```
   Let user select from the list. Allow multiple selections. Include an "Unassigned" option.

4. **Description/Body** - Ask for the issue body content (free text). If user provides `$ARGUMENTS`, pre-fill from that. This is the **raw/brief** content that will be enhanced in the next step.

5. **Content Style Instructions** - Ask the user for custom guidelines on how to rewrite/enhance the description (free text). Examples:
   - "use checkboxes for action items"
   - "use simple english"
   - "no emojis"
   - "add acceptance criteria section"
   - "keep it concise"
   - "use bullet points"

   This is a single free-text field where the user writes their style preferences.

### Step 4: Enhance the description

The raw description from Step 3 is just a brief/rough input. Before creating the issue, **rewrite and enhance** the description following the user's content style instructions.

- Use the raw description as the source material
- Apply all the style guidelines the user provided
- Produce a well-structured, clear, professional GitHub issue body
- Do NOT ask the user for approval of the rewritten content -- just apply the instructions and proceed

### Step 5: Ask for metadata

If a project was selected in Step 2, fetch the project's fields:

```bash
gh project field-list <PROJECT_NUMBER> --owner <owner> --format json
```

Then ask the user to set:

1. **Status** - Show the available status options from the project's SingleSelect fields (e.g., Todo, In Progress, In Review, Done, Closed).

2. **Priority** - Show available priority options if the project has a Priority field (e.g., High, Medium, Low). Include a "None" option.

3. **Labels** - Fetch labels from the selected repo:
   ```bash
   gh label list --repo <owner>/<repo> --json name --jq '.[].name'
   ```
   Let user select multiple. Include a "None" option.

4. **Milestone** - Fetch milestones from the selected repo:
   ```bash
   gh api repos/<owner>/<repo>/milestones --jq '.[].title'
   ```
   Let user select one. Include a "None" option.

5. **Issue Type** - Fetch issue types from the repo:
   ```bash
   gh api graphql -f query='{ repository(owner: "<owner>", name: "<repo>") { issueTypes(first: 20) { nodes { id name } } } }'
   ```
   Let user select one (e.g., Task, Bug, Feature). Include a "None" option.

### Step 6: Create the issue

```bash
gh issue create \
  --repo <owner>/<repo> \
  --title "<title>" \
  --body "<body>" \
  --assignee "<assignee1>,<assignee2>" \
  --label "<label1>,<label2>" \
  --milestone "<milestone>"
```

Use a heredoc for the body to preserve formatting. Use the **enhanced description** from Step 4 (not the raw input from Step 3):
```bash
gh issue create --repo <owner>/<repo> --title "<title>" --assignee "<assignees>" --body "$(cat <<'EOF'
<body content>
EOF
)"
```

Omit `--assignee`, `--label`, `--milestone` flags if the user selected "None" for those.

### Step 7: Set issue type (if selected)

Get the issue node ID:
```bash
gh api repos/<owner>/<repo>/issues/<number> --jq '.node_id'
```

Then set the type:
```bash
gh api graphql -f query='mutation { updateIssueIssueType(input: { issueId: "<issue_node_id>", issueTypeId: "<type_id>"}) { issue { id } } }'
```

### Step 8: Add to project and set project fields

If a project was selected:

1. Add the issue to the project:
   ```bash
   gh project item-add <PROJECT_NUMBER> --owner <owner> --url <issue_url> --format json
   ```
   This returns the item ID.

2. Parse the GraphQL item ID from the JSON output (field: `id`).

3. Get the **numeric database ID** for the project board deep link:
   ```bash
   gh api graphql -f query='query { node(id: "<GRAPHQL_ITEM_ID>") { ... on ProjectV2Item { databaseId } } }' --jq '.data.node.databaseId'
   ```
   Save this numeric ID for the project board URL in Step 9.

4. Set **Status** on the project item:
   ```bash
   gh project item-edit \
     --id <ITEM_ID> \
     --project-id <PROJECT_ID> \
     --field-id <STATUS_FIELD_ID> \
     --single-select-option-id <STATUS_OPTION_ID>
   ```

5. Set **Priority** on the project item (if selected and field exists):
   ```bash
   gh project item-edit \
     --id <ITEM_ID> \
     --project-id <PROJECT_ID> \
     --field-id <PRIORITY_FIELD_ID> \
     --single-select-option-id <PRIORITY_OPTION_ID>
   ```

### Step 9: Confirm

Output a summary of what was created:
- Issue URL: `https://github.com/<owner>/<repo>/issues/<number>`
- Project URL (if project was selected): `https://github.com/orgs/<owner>/projects/<project_number>?pane=issue&itemId=<numeric_item_id>&issue=<owner>%7C<repo>%7C<issue_number>`
- Repository
- Assignees
- Labels, Milestone, Type
- Project, Status, Priority

## Important Notes

- Always use `--format json` when you need to parse output from `gh` commands.
- Use the project's internal IDs (from `field-list`) for `item-edit` commands, not display names.
- If any `gh` command fails, show the error to the user and ask how to proceed.
- The `--project` flag on `gh issue create` does NOT set project field values -- you must use `gh project item-add` + `gh project item-edit` separately.
- For issue body, always use heredoc syntax to preserve multiline formatting.
