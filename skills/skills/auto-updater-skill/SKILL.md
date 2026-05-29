---
name: auto-updater-skill
cluster: community
description: "Automatic skill update management: check for updates, diff, apply, rollback, version tracking"
tags: ["updates","skills","maintenance","openclaw"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "auto update skill check diff apply rollback version"
---

# auto-updater-skill

## Purpose
This skill automates the management of updates for OpenClaw skills, including checking for new versions, generating diffs, applying updates, rolling back changes, and tracking versions to ensure seamless maintenance.

## When to Use
Use this skill when you need to maintain skill versions in a community cluster, such as before deploying changes, after detecting potential issues, or during routine maintenance cycles. It's ideal for scenarios involving multiple skills where version consistency is critical, like in production environments or collaborative development.

## Key Capabilities
- Check for updates: Query the OpenClaw registry for newer skill versions.
- Generate diffs: Compare current and latest versions to highlight changes.
- Apply updates: Safely install updates with conflict resolution.
- Rollback updates: Revert to a previous version if issues arise.
- Version tracking: Maintain a log of version histories and metadata.
Specifics: Supports JSON config files for version overrides, e.g., `{"skill_id": "my-skill", "target_version": "1.2.3"}`. Requires authentication via `$OPENCLAW_API_KEY` environment variable.

## Usage Patterns
To use this skill, first ensure the OpenClaw CLI is installed and authenticated. Import the skill via `openclaw skill import auto-updater-skill`. Then, invoke it programmatically or via CLI. For automation, wrap commands in scripts that check for updates daily. Always specify the skill ID and use flags for options like dry-run or force-apply.

## Common Commands/API
Use the OpenClaw CLI for interactions. All commands require `$OPENCLAW_API_KEY` set in your environment.

- Check for updates: Run `openclaw auto-update check --skill-id <id> --cluster community`. This queries the API endpoint `/api/skills/{id}/updates` and returns available versions.
  Example snippet:
  ```
  export OPENCLAW_API_KEY=your_key
  openclaw auto-update check --skill-id auto-updater-skill
  ```
- Generate diff: Execute `openclaw auto-update diff --skill-id <id> --from-version 1.0.0 --to-version 1.1.0`. Outputs differences in JSON format.
  Example snippet:
  ```
  openclaw auto-update diff --skill-id my-skill --from-version 1.2.3
  ```
- Apply updates: Use `openclaw auto-update apply --skill-id <id> --version 1.1.0 --dry-run`. Add `--force` to bypass checks.
  Example snippet:
  ```
  openclaw auto-update apply --skill-id my-skill --version latest
  ```
- Rollback updates: Command: `openclaw auto-update rollback --skill-id <id> --to-version 1.0.0`. This hits the API endpoint `/api/skills/{id}/rollback`.
  Example snippet:
  ```
  openclaw auto-update rollback --skill-id my-skill --to-version 1.0.0
  ```
- Version tracking: Query with `openclaw auto-update track --skill-id <id>`. Config format: Use a YAML file like `versions.yaml` with content: `skill_id: my-skill, history: ["1.0.0", "1.1.0"]`.

## Integration Notes
Integrate this skill into your OpenClaw workflow by adding it as a dependency in your main skill's config file, e.g., add `"dependencies": ["auto-updater-skill"]` in `skill.json`. For API integrations, use the base URL `https://api.openclaw.com` and include the header `Authorization: Bearer $OPENCLAW_API_KEY`. When chaining with other skills, ensure error propagation is handled via callbacks. Test integrations in a staging environment first.

## Error Handling
Handle errors by checking exit codes from CLI commands (e.g., code 1 for failures). Common errors include authentication failures (HTTP 401) if `$OPENCLAW_API_KEY` is invalid, or version conflicts (error code 409). To handle: Wrap commands in try-catch blocks in scripts, e.g.:
```
try {
  openclaw auto-update check --skill-id my-skill
} catch (error) {
  if (error.code === 401) { echo "Auth failed; check $OPENCLAW_API_KEY"; }
}
```
Log errors to a file using `--log-file output.log` flag. For API calls, parse JSON responses for error details like `{"error": "Version not found"}`.

## Concrete Usage Examples
1. **Example: Checking and applying an update for a skill**  
   First, check for updates: `openclaw auto-update check --skill-id my-skill`. If a new version is available, apply it: `openclaw auto-update apply --skill-id my-skill --version latest`. This ensures your skill is up-to-date without manual intervention. Use in a CI/CD pipeline for automated deployments.

2. **Example: Rolling back after a failed update**  
   If an update causes issues, rollback immediately: `openclaw auto-update rollback --skill-id my-skill --to-version 1.0.0`. Prior to this, generate a diff to verify changes: `openclaw auto-update diff --skill-id my-skill --from-version 1.1.0`. This pattern is useful for maintaining stability in production.

## Graph Relationships
- Depends on: skill-registry (for version queries)
- Provides: update-management (to other community skills)
- Relates to: openclaw-core (via API endpoints)
- Conflicts with: none
- Used by: maintenance-skills cluster
