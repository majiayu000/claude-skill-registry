---
name: working-with-jira-acli
description: |
  Use when viewing, searching, or working with Jira issues/work items via acli. Provides command patterns for authentication, viewing issues, creating/editing work items, commenting, transitions, searching, bulk operations, and troubleshooting
user-invocable: false
---

# Working with Jira via acli

The Atlassian Command Line Interface (acli) is a powerful utility for
interacting with Jira Cloud programmatically from the command line. This skill
provides patterns and guidance for common Jira operations.

## Prerequisites

Ensure you have:
- acli installed and accessible in your PATH
- Network access to your Jira Cloud instance
- Proper authentication configured

## Authentication

**Check authentication status:**
```bash
acli jira auth status
```

**Login to Jira:**
```bash
acli jira auth login --web
```

**Switch between accounts:**
```bash
acli jira auth switch
```

**Logout:**
```bash
acli jira auth logout
```

## Work Items (Issues)

### View Work Items

**Get a single work item with full details:**
```bash
acli jira workitem view PROJ-123
```

**Search for work items using JQL (Jira Query Language):**
```bash
acli jira workitem search --jql "project = PROJ AND status = 'In Progress'"
acli jira workitem search --jql "assignee = currentUser()"
```

### Create Work Items

**IMPORTANT: Always use JSON with ADF formatting for descriptions**

When creating JIRA tickets with formatted descriptions, you MUST use the `--from-json` flag with proper ADF (Atlassian Document Format). The `--description` and `--description-file` flags expect plain text or ADF, but Markdown will NOT render correctly.

**Create a work item with formatted description (RECOMMENDED):**
```bash
# 1. Create a JSON file with ADF formatted description
cat > /tmp/workitem.json <<'EOF'
{
  "projectKey": "RETIRE",
  "type": "Task",
  "summary": "Your ticket title",
  "description": {
    "type": "doc",
    "version": 1,
    "content": [
      {
        "type": "heading",
        "attrs": { "level": 2 },
        "content": [{ "type": "text", "text": "Summary" }]
      },
      {
        "type": "paragraph",
        "content": [
          { "type": "text", "text": "Your paragraph text here" }
        ]
      }
    ]
  }
}
EOF

# 2. Create the work item
acli jira workitem create --from-json /tmp/workitem.json
```

**Create a simple work item (plain text only):**
```bash
acli jira workitem create --project PROJ --summary "Issue summary"
```

**Create with plain text description:**
```bash
acli jira workitem create \
  --project PROJ \
  --summary "Issue summary" \
  --type "Bug" \
  --description "Detailed description"
```

**Bulk create work items from JSON:**
```bash
acli jira workitem create-bulk --from-json issues.json
```

**Bulk create work items from CSV:**
```bash
acli jira workitem create-bulk --from-csv issues.csv
```

#### ADF (Atlassian Document Format) Structure

ADF is the format JIRA uses for rich text. Here are common patterns:

**Basic structure:**
```json
{
  "type": "doc",
  "version": 1,
  "content": [
    // Array of content blocks
  ]
}
```

**Heading (h2):**
```json
{
  "type": "heading",
  "attrs": { "level": 2 },
  "content": [{ "type": "text", "text": "Heading Text" }]
}
```

**Paragraph:**
```json
{
  "type": "paragraph",
  "content": [
    { "type": "text", "text": "Plain text" }
  ]
}
```

**Paragraph with inline code:**
```json
{
  "type": "paragraph",
  "content": [
    { "type": "text", "text": "Use " },
    { "type": "text", "text": "FLAG_SECURE", "marks": [{ "type": "code" }] },
    { "type": "text", "text": " for security" }
  ]
}
```

**Paragraph with bold text:**
```json
{
  "type": "paragraph",
  "content": [
    { "type": "text", "text": "This is " },
    { "type": "text", "text": "bold", "marks": [{ "type": "strong" }] },
    { "type": "text", "text": " text" }
  ]
}
```

**Paragraph with link:**
```json
{
  "type": "paragraph",
  "content": [
    { "type": "text", "text": "See " },
    {
      "type": "text",
      "text": "documentation",
      "marks": [
        {
          "type": "link",
          "attrs": { "href": "https://example.com" }
        }
      ]
    }
  ]
}
```

**Bullet list:**
```json
{
  "type": "bulletList",
  "content": [
    {
      "type": "listItem",
      "content": [
        {
          "type": "paragraph",
          "content": [{ "type": "text", "text": "First item" }]
        }
      ]
    },
    {
      "type": "listItem",
      "content": [
        {
          "type": "paragraph",
          "content": [{ "type": "text", "text": "Second item" }]
        }
      ]
    }
  ]
}
```

**Nested bullet list:**
```json
{
  "type": "bulletList",
  "content": [
    {
      "type": "listItem",
      "content": [
        {
          "type": "paragraph",
          "content": [{ "type": "text", "text": "Parent item" }]
        },
        {
          "type": "bulletList",
          "content": [
            {
              "type": "listItem",
              "content": [
                {
                  "type": "paragraph",
                  "content": [{ "type": "text", "text": "Nested item" }]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

**Ordered list:**
```json
{
  "type": "orderedList",
  "content": [
    {
      "type": "listItem",
      "content": [
        {
          "type": "paragraph",
          "content": [{ "type": "text", "text": "First step" }]
        }
      ]
    },
    {
      "type": "listItem",
      "content": [
        {
          "type": "paragraph",
          "content": [{ "type": "text", "text": "Second step" }]
        }
      ]
    }
  ]
}
```

**Code block:**
```json
{
  "type": "codeBlock",
  "attrs": { "language": "typescript" },
  "content": [
    {
      "type": "text",
      "text": "const example = 'code';"
    }
  ]
}
```

**Complete example with multiple sections:**
```json
{
  "projectKey": "RETIRE",
  "type": "Task",
  "summary": "Enable Android Secure Flag",
  "description": {
    "type": "doc",
    "version": 1,
    "content": [
      {
        "type": "heading",
        "attrs": { "level": 2 },
        "content": [{ "type": "text", "text": "Summary" }]
      },
      {
        "type": "paragraph",
        "content": [
          { "type": "text", "text": "Update the " },
          { "type": "text", "text": "android-secure-background", "marks": [{ "type": "code" }] },
          { "type": "text", "text": " module to conditionally apply " },
          { "type": "text", "text": "FLAG_SECURE", "marks": [{ "type": "code" }] },
          { "type": "text", "text": "." }
        ]
      },
      {
        "type": "heading",
        "attrs": { "level": 2 },
        "content": [{ "type": "text", "text": "Context" }]
      },
      {
        "type": "bulletList",
        "content": [
          {
            "type": "listItem",
            "content": [
              {
                "type": "paragraph",
                "content": [{ "type": "text", "text": "First point" }]
              }
            ]
          },
          {
            "type": "listItem",
            "content": [
              {
                "type": "paragraph",
                "content": [{ "type": "text", "text": "Second point" }]
              }
            ]
          }
        ]
      },
      {
        "type": "heading",
        "attrs": { "level": 2 },
        "content": [{ "type": "text", "text": "Tech Specs" }]
      },
      {
        "type": "bulletList",
        "content": [
          {
            "type": "listItem",
            "content": [
              {
                "type": "paragraph",
                "content": [
                  { "type": "text", "text": "Entry point: " },
                  {
                    "type": "text",
                    "text": "useAndroidSecureScreen.ts",
                    "marks": [
                      {
                        "type": "link",
                        "attrs": {
                          "href": "https://github.com/guideline-app/mobile-app/blob/main/src/shared/hooks/useAndroidSecureScreen.ts"
                        }
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  }
}
```

### Edit Work Items

**Edit a work item:**
```bash
acli jira workitem edit --key PROJ-123 --summary "Updated summary"
```

**Edit multiple work items via JQL:**
```bash
acli jira workitem edit --jql "project = PROJ AND status = 'To Do'" --assignee "user@example.com" --yes
```

**Assign a work item:**
```bash
acli jira workitem assign --key PROJ-123 --assignee "user@example.com"
```

**Self-assign a work item:**
```bash
acli jira workitem assign --key PROJ-123 --assignee "@me"
```

**Bulk assign work items:**
```bash
acli jira workitem assign --key "PROJ-123,PROJ-124,PROJ-125" --assignee "user@example.com"
```

### Work Item Transitions

**Transition a work item:**
```bash
acli jira workitem transition --key PROJ-123 --status "In Progress"
```

**Transition multiple work items via JQL:**
```bash
acli jira workitem transition --jql "project = PROJ AND assignee = currentUser()" --status "Done" --yes
```

### Work Item Comments

**Add a comment:**
```bash
acli jira workitem comment create --key PROJ-123 --body "This is my comment"
```

**Add a comment from a file:**
```bash
acli jira workitem comment create --key PROJ-123 --body-file comment.txt
```

**Add a comment using text editor:**
```bash
acli jira workitem comment create --key PROJ-123 --editor
```

**Comment on multiple work items via JQL:**
```bash
acli jira workitem comment create --jql "project = PROJ AND status = 'In Progress'" --body "Batch update note"
```

**List comments on a work item:**
```bash
acli jira workitem comment list --key PROJ-123
```

**Update an existing comment:**
```bash
acli jira workitem comment update --key PROJ-123 --id 10001 --body "Updated comment text"
```

**Delete a comment:**
```bash
acli jira workitem comment delete --key PROJ-123 --id 10001
```

### Work Item Links

**Link work items:**
```bash
acli jira workitem link create --out PROJ-123 --in PROJ-456 --type "Blocks"
```

**List links on a work item:**
```bash
acli jira workitem link list --key PROJ-123
```

**Delete a link:**
```bash
acli jira workitem link delete --id 10001
```

**View available link types:**
```bash
acli jira workitem link type
```

### Work Item Attachments

**List attachments on a work item:**
```bash
acli jira workitem attachment list --key PROJ-123
```

**Delete an attachment:**
```bash
acli jira workitem attachment delete --id ATTACHMENT_ID
```

### Archive and Delete

**Archive a work item:**
```bash
acli jira workitem archive --key PROJ-123
```

**Unarchive a work item:**
```bash
acli jira workitem unarchive --key PROJ-123
```

**Delete a work item:**
```bash
acli jira workitem delete --key PROJ-123
```

**Archive multiple work items via JQL:**
```bash
acli jira workitem archive --jql "project = PROJ AND status = Done" --yes
```

## Boards

**Get board details:**
```bash
acli jira board get --id BOARD_ID
```

**Search for boards:**
```bash
acli jira board search
```

**Search boards by name:**
```bash
acli jira board search --name "My Board"
```

**Search boards by project:**
```bash
acli jira board search --project PROJ
```

**List sprints on a board:**
```bash
acli jira board list-sprints --id BOARD_ID
```

**List active sprints only:**
```bash
acli jira board list-sprints --id BOARD_ID --state active
```

## Sprints

**List work items in a sprint:**
```bash
acli jira sprint list-workitems --sprint SPRINT_ID --board BOARD_ID
```

**View sprint details:**
```bash
acli jira sprint view --id SPRINT_ID
```

## Projects

**Get project information:**
```bash
acli jira project view --key PROJ
```

**List all projects:**
```bash
acli jira project list
```

## Fields

**Create a custom text field:**
```bash
acli jira field create --name "Customer Name" --type "com.atlassian.jira.plugin.system.customfieldtypes:textfield"
```

**Create a custom date field:**
```bash
acli jira field create --name "Release Date" --type "com.atlassian.jira.plugin.system.customfieldtypes:datepicker" --description "Planned release date"
```

**Delete a custom field:**
```bash
acli jira field delete --id FIELD_ID
```

## Filters

**Get a filter:**
```bash
acli jira filter get --id FILTER_ID
```

**List your filters:**
```bash
acli jira filter list --my
```

**List favorite filters:**
```bash
acli jira filter list --favourite
```

**Search for filters:**
```bash
acli jira filter search --name "My Filter"
```

## Common Patterns

### Bulk Operations

acli supports bulk operations directly via JQL - no need for piping through xargs.

**Bulk assign work items:**
```bash
acli jira workitem assign --jql "assignee = EMPTY AND priority = Highest" --assignee "user@example.com" --yes
```

**Bulk transition work items:**
```bash
acli jira workitem transition --jql "status = 'To Do' AND assignee is not EMPTY" --status "In Progress" --yes
```

**Bulk edit work items:**
```bash
acli jira workitem edit --jql "project = PROJ AND labels = old-label" --labels "new-label" --yes
```

**Bulk archive completed work items:**
```bash
acli jira workitem archive --jql "project = PROJ AND status = Done AND updated < -30d" --yes
```

### Error Handling in Scripts

```bash
#!/bin/bash
set -e  # Exit on error

# Check if acli is available
if ! command -v acli &> /dev/null; then
  echo "Error: acli is not installed"
  exit 1
fi

# Check authentication
if ! acli jira auth status > /dev/null 2>&1; then
  echo "Error: Not authenticated. Run 'acli jira auth login --web' first."
  exit 1
fi

# Run commands with error handling
if acli jira workitem view PROJ-123 > /dev/null 2>&1; then
  echo "Work item found"
else
  echo "Failed to fetch work item"
  exit 1
fi
```

## Troubleshooting

**Not authenticated:**
- Run `acli jira auth login --web` to authenticate
- Use `acli jira auth status` to check current auth status

**acli command not found:**
- Verify acli is installed: `which acli`
- Add acli to PATH if needed

**Command not recognized:**
- Use `acli [command] --help` for available subcommands
- Example: `acli jira workitem --help`

## Resources

- acli help: Run `acli --help` or `acli jira --help` for available commands
- Jira Query Language (JQL): https://support.atlassian.com/jira-software-cloud/docs/use-advanced-search-with-jira-query-language-jql/
