---
name: Envisioning Studio CLI
description: |
  Use the `es` CLI to manage Envisioning Studio content from the command line.
  The CLI communicates with the Envisioning Studio server API and handles authentication automatically.
allowed-tools:
  - Bash
---

# Envisioning Studio CLI

The `es` CLI manages Envisioning Studio content. It is installed as a dev dependency in this repo.

## Authentication

Before using any commands, authenticate:

```bash
npx es login
```

This opens a browser for OAuth login and stores credentials locally. To clear credentials:

```bash
npx es logout
```

## Instance Targeting

On first use, the CLI prompts for an instance subdomain or URL and saves it to `envisioning-studio-cli.json` in the current directory.

```bash
# Show current instance
npx es instance

# Set or change instance to https://myproject.envisioning-studio.com
npx es instance myproject

# Set or change instance to a custom url:
npx es instance http://studio.mycustomerdomain.com
```

## Opportunities

Manage opportunities (work items displayed as kanban boards). The command supports progressive abbreviation: `opportunities`, `opp`, `op`, or `o`.

### List opportunities

```bash
npx es opp list
npx es opp list --json
```

### Get opportunity details

```bash
npx es opp get <id>
npx es opp get <id> --json
```

### Create an opportunity

The `--content` option accepts markdown.

```bash
npx es opp create --title "New feature request"
npx es opp create --title "Bug fix" --content "## Details\nSome **markdown** here" --assigned user@example.com
npx es opp create --title "Task" --field status=New --field priority=High
```

### Update an opportunity

```bash
npx es opp update <id> --title "Updated title"
npx es opp update <id> --assigned user@example.com --field status=Done
```

### Archive / unarchive

```bash
npx es opp archive <id>
npx es opp unarchive <id>
```

### List available fields

```bash
npx es opp fields
npx es opp fields --json
```

Use field keys with `--field key=value` when creating or updating opportunities.

## News

Manage news items for the instance. The command supports progressive abbreviation: `news`, `new`, `ne`, or `n`.

### List news items

```bash
npx es news list
npx es news list --json
```

### Get a news item

```bash
npx es news get <id>
npx es news get <id> --json
```

### Create a news item

The `--content` option accepts markdown (without a `# Title` heading — the server adds it).

News content can include links to opportunities using relative URLs:

```markdown
[View opportunity](opportunities?view=development&opportunity=3088)
```

Where `view` is the view that sets the status on the opportunity (e.g., `development`, `design`).

```bash
npx es news create --title "Project Kickoff"
npx es news create --title "Update" --description "Brief summary" --content "Full markdown body"
```

### Update a news item

```bash
npx es news update <id> --title "New Title"
npx es news update <id> --description "New summary" --content "New body"
```

### Delete a news item

```bash
npx es news delete <id>
```
