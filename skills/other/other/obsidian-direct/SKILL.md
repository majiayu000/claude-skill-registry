---
name: obsidian-direct
cluster: community
description: "Direct Obsidian vault manipulation: file creation/edit, template insertion, dataview queries, plugin API"
tags: ["obsidian","vault","direct","api"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "obsidian direct vault file create edit template dataview plugin"
---

# obsidian-direct

## Purpose
This skill enables direct programmatic access to Obsidian vaults for tasks like file creation, editing, template insertion, Dataview queries, and plugin API calls, allowing automation of note-taking workflows.

## When to Use
Use this skill for automating Obsidian interactions in scripts, such as generating daily notes from external data, updating files based on user input, or running Dataview queries to fetch metadata. Apply it in scenarios where manual vault management is inefficient, like in CI/CD pipelines or AI-driven content creation.

## Key Capabilities
- Create new files or folders in the vault using specified paths and content.
- Edit existing files by appending, overwriting, or inserting text at specific lines.
- Insert templates (e.g., from a predefined .md template file) into new or existing notes.
- Execute Dataview queries to retrieve or manipulate note metadata.
- Call Obsidian plugin APIs for custom extensions, such as querying plugin-specific data.

## Usage Patterns
Invoke the skill via a function call like `call_skill('obsidian-direct', subcommand, params)`, where subcommand is one of: create-file, edit-file, insert-template, run-query, or plugin-call. Always include required params as a dictionary, e.g., {'path': 'notes/file.md', 'content': 'Text here'}. For authenticated actions, pass the API key via env var `$OBSIDIAN_API_KEY`. Structure calls sequentially: first create a file, then edit it. Use JSON for complex params, e.g., {'query': '{"from": "folder", "where": "file.name contains \'key\'"}'}. Avoid concurrent calls to prevent vault conflicts.

## Common Commands/API
API Endpoint: Use POST to `https://api.openclaw.com/v1/obsidian/vault/{vault-id}/files` for file operations, with JSON body like {"path": "notes/file.md", "content": "Hello"}. CLI equivalent: `obsidian-direct create-file --vault-id myvault --path "notes/file.md" --content "Hello" --api-key $OBSIDIAN_API_KEY`.

Code Snippet:
```skill
params = {'path': 'Daily/daily.md', 'content': 'Today\'s notes'}
result = call_skill('obsidian-direct', 'create-file', params)
print(result['file_path'])  # Outputs: Daily/daily.md
```

For Dataview: `obsidian-direct run-query --vault-id myvault --query "LIST file.name FROM \"folder\" WHERE file.mtime > date(2023-01-01)" --api-key $OBSIDIAN_API_KEY`.

Config Formats: Params must be JSON objects, e.g., {"template": "path/to/template.md", "insert_at": 5} for insert-template. Flags: --vault-id (required), --dry-run (simulates without changes), --force (overwrites files).

## Integration Notes
Integrate by passing outputs from other skills as inputs, e.g., use a search skill's result as content for create-file. Authentication: Set `$OBSIDIAN_API_KEY` in your environment, e.g., `export OBSIDIAN_API_KEY=your_api_key`, and include it in calls. Ensure the vault is synced via Obsidian's sync plugin if remote. For multi-skill workflows, chain with tools like file-system skills by using the returned file paths as arguments. Test integrations in a local vault first to avoid data loss.

## Error Handling
Always wrap skill calls in try-except blocks to catch exceptions like VaultError (e.g., 404 for missing files) or AuthError (e.g., 403 for invalid API key). Check response codes: if result['status'] == 'error', log the message and retry with exponential backoff. Common issues: Handle file conflicts with --force flag, or parse Dataview errors for query syntax. Example:

Code Snippet:
```skill
try:
    call_skill('obsidian-direct', 'edit-file', {'path': 'notes/file.md', 'content': 'Updated text'})
except VaultError as e:
    if e.code == 404:
        call_skill('obsidian-direct', 'create-file', {'path': 'notes/file.md', 'content': 'Default'})
    else:
        raise
```

## Concrete Usage Examples
1. Automate daily note creation: First, get current date via another skill, then call `obsidian-direct create-file --vault-id myvault --path "Daily/{date}.md" --content "Notes for {date}" --api-key $OBSIDIAN_API_KEY`. This creates a new file like Daily/2023-10-01.md with initial content.
2. Run and insert Dataview results: Query tasks with `obsidian-direct run-query --vault-id myvault --query "TASK FROM \"Tasks\" WHERE !completed"`, then use the output in `obsidian-direct edit-file --path "Summary.md" --append result['query_output']` to append results to a summary note.

## Graph Relationships
- Related to: community cluster (e.g., shares tags with file-management skills).
- Connected to: obsidian-related skills like "obsidian-sync" for vault syncing.
- Links with: general API skills for authentication handling.
- Overlaps with: note-taking cluster for content manipulation.
