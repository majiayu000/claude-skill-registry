---
name: hut-cli
description: "Interacts with sourcehut issue trackers using the hut CLI. Use when asked to create, read, update, triage, or comment on tickets for a sourcehut-hosted project."
---

# Hut Issue Management

Works with sourcehut issue trackers and tickets using the `hut` CLI. Covers tracker setup, ticket creation, ticket review, triage actions, and ticket comments.

## Workflow

### Step 1: Identify the Repository

Run `hut git show` to gather repository details. Note:
- Repository name (usually used as the tracker name)
- Visibility (e.g. `private`, `public`) if you need to create a tracker

### Step 2: Ensure the Tracker Exists

Run `hut todo list` and check if a tracker matching the repository name appears in the output.

- If a tracker exists, continue.
- If it does not exist, create one:
  ```
  hut todo create <repo-name> -v <visibility>
  ```
  Use the repository visibility from Step 1.

### Step 3: Create a New Ticket (When Requested)

Prepare a title and description. The title **must** end with `(LLM-generated)`.

Create the ticket from stdin:

```
echo "<title> (LLM-generated)

<description>" | hut todo ticket create --stdin
```

- Pass `-t <tracker-name>` when needed.
- First line is the title.
- Separate title and body with a blank line.
- Include concrete details (context, reproduction, expected vs actual behavior, and any unknowns).

### Step 4: Read Existing Tickets

Use `hut todo ticket` subcommands (not `hut tickets`) to inspect current issues.

- List trackers:
  ```
  hut todo list
  ```
- List tickets in a tracker:
  ```
  hut todo ticket list -t <tracker-name>
  ```
- List more tickets:
  ```
  hut todo ticket list -t <tracker-name> --count 20
  ```
- Show a specific ticket by ID:
  ```
  hut todo ticket show -t <tracker-name> <ticket-id>
  ```

### Step 5: Triage or Update Tickets (When Requested)

Common issue-management actions:
- Assign:
  ```
  hut todo ticket assign -t <tracker-name> <ticket-id> <username>
  ```
- Update status:
  ```
  hut todo ticket update-status -t <tracker-name> <ticket-id> <status>
  ```
- Edit title/body:
  ```
  hut todo ticket edit -t <tracker-name> <ticket-id>
  ```
- Manage labels:
  ```
  hut todo ticket label -t <tracker-name> <ticket-id> <label>
  hut todo ticket unlabel -t <tracker-name> <ticket-id> <label>
  ```

### Step 6: Add Comments to Tickets

After exploring the relevant code and current issue discussion, post a follow-up comment when useful.

```
echo "<comment text>" | hut todo ticket comment -t <tracker-name> <ticket-id> --stdin
```

Notes:
- `hut todo ticket comment <ID>` supports `--stdin` (default true).
- You can include `-s <status>` or `-r <resolution>` with a comment when closing or resolving work.

Example:
```
hut todo ticket list -t yala --count 20
hut todo ticket show -t yala 7
echo "I reproduced this on commit abc123 and traced it to X." | hut todo ticket comment -t yala 7 --stdin
```

### Guidelines

- Gather as much context as possible from the user and the codebase before writing the ticket.
- Keep ticket titles clear and actionable.
- Structure ticket bodies with useful sections when appropriate.
- When commenting, summarize what you checked and what changed.
- If information is incomplete, state assumptions and unknowns explicitly.
