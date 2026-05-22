---
name: qa-engineer-manual
description: Plan and perform manual tests for the Storyblok CLI package and check functionality end-to-end
---

# QA Engineer for Manual Testing

## Responsibilities

- Create and execute plans for manually testing and validating the Storyblok CLI.
- Reproduce and investigate bug reports.
- Run Storyblok CLI commands against a dedicated QA space to ensure features work as expected.
- Validate the DX of CLI features.
- Provide thoughtful feedback regarding incomplete, broken, or missing features.

## When to use

Use this skill when the user requests manual testing of specific features and functionality.

## Workflow

### Preparation

1. Run `pnpm nx build storyblok` to build the latest version of the CLI.
2. Log in with the correct user: `source ./.env.qa ./dist/index.mjs logout && ./dist/index.mjs login --token "$STORYBLOK_TOKEN" --region eu`.
3. Create a comprehensive test plan based on the assignment.
   - Test all happy paths.
   - Test error scenarios.
   - Consider possible edge cases.

### Performing tests

- Clean up the local and remote environment before and after every assignment by running `./.claude/skills/qa-engineer-manual/scripts/cleanup.sh`. Don't hesitate to clean up between tests to start with a clean slate.
- Run CLI commands with `./dist/index.mjs` (for available commands, run `./dist/index.mjs --help`).
- Review command documentation in `./src/commands/COMMAND/README.md` or `./src/commands/COMMAND/ACTION/README.md`.
- Verify changes in the local file system or the Storyblok space.
- When using two spaces (for example one source and one target space), use `STORYBLOK_SPACE_ID_TARGET` for the target.
- Many commands require files in `./.storyblok/$STORYBLOK_SPACE_ID/COMMAND_DIR` to perform a test. Create files in this directory when necessary. For example, when pushing a story, create it in `./.storyblok/$STORYBLOK_SPACE_ID/stories/SLUG_FAKE_UUID.json`.

## Interact with the Storyblok API

The Storyblok Management API provides access for verifying the state in Storyblok.

```bash
source ./.env.qa

# Get stories (paginated)
curl "https://mapi.storyblok.com/v1/spaces/$STORYBLOK_SPACE_ID/stories/" \
  -H "Authorization: $STORYBLOK_TOKEN"

# Get assets (paginated)
curl "https://mapi.storyblok.com/v1/spaces/$STORYBLOK_SPACE_ID/assets/" \
  -H "Authorization: $STORYBLOK_TOKEN"
```

Refer to [Working with Assets](./reference/assets.md) when creating assets during manual testing.

### Helper scripts

These scripts provide fast setup, inspection, and cleanup during manual tests. Each script loads `.env.qa` automatically.
Paths are relative to this `SKILL.md`. For example, `./scripts/cleanup-remote.sh` resolves to `./.claude/skills/qa-engineer-manual/scripts/cleanup-remote.sh`.

| Script | Purpose |
| --- | --- |
| `./scripts/cleanup.sh` | Performs a full cleanup of both remote and local environments. |
| `./scripts/cleanup-remote.sh` | Deletes stories, components, assets, and asset folders in QA spaces. |
| `./scripts/cleanup-local.sh` | Deletes local QA logs, reports, stories, and assets. |
| `./scripts/asset-create.sh` | Creates a placeholder asset in the source space. |
| `./scripts/asset-folder-create.sh` | Creates an asset folder with an optional parent ID. |
| `./scripts/asset-folder-update.sh` | Updates an asset folder name or parent ID. |
| `./scripts/png-create.sh` | Generates a tiny local PNG for uploads. |
| `./scripts/asset-list.sh` | Lists assets for a space. |
| `./scripts/asset-folder-list.sh` | Lists asset folders for a space. |
| `./scripts/story-list.sh` | Lists stories for a space. |
| `./scripts/component-list.sh` | Lists components for a space. |
| `./scripts/story-create.sh` | Creates a story with optional content JSON. |
| `./scripts/story-update.sh` | Updates a story name, slug, or content. |
| `./scripts/story-delete.sh` | Deletes a story by ID. |
| `./scripts/component-create.sh` | Creates a component with optional schema JSON. |
| `./scripts/component-update.sh` | Updates a component name, display name, or schema. |
| `./scripts/component-delete.sh` | Deletes a component by ID. |

### Scenario seeds

Use these scripts to quickly seed QA spaces with predictable data for manual testing. Scenarios expect a clean space, so run cleanup first when you want a fresh start.

- Each scenario defaults to `STORYBLOK_SPACE_ID` unless you override it with `--space`.
- Paths are relative to this `SKILL.md`. For example, `./scenarios/has-stories.sh` resolves to `./.claude/skills/qa-engineer-manual/scenarios/has-stories.sh`.

| Scenario | Seeds |
| --- | --- |
| `./scenarios/has-stories.sh [--space <spaceId>]` | Seeds 3 stories backed by a minimal component (source space). |
| `./scenarios/has-private-assets.sh [--space <spaceId>]` | Seeds 1 public asset and 1 private asset (source space). |
| `./scenarios/has-nested-asset-folders.sh [--space <spaceId>]` | Seeds 2 nested asset folders and 3 public assets (2 assets inside folders). |

## Troubleshooting

- Load the `STORYBLOK_SPACE_ID`, `STORYBLOK_SPACE_ID_TARGET`, `STORYBLOK_ASSET_TOKEN`, and `STORYBLOK_ASSET_TOKEN_TARGET` environment variables by running `source ./.env.qa` (do not attempt to read this file).
- Save all temporary files in `./.claude/tmp`.
- Find reports and logs in `./.storyblok/logs` and `./.storyblok/reports`.

## Output

The final output must:

1. Provide thoughtful feedback regarding incomplete, broken, or missing features.
2. List all findings.

### Review Template

Use the following template for the manual test review output:

```md
# [Feature] Test Results

- **Feature/Command:** [for example, `storyblok push stories`]
- **Outcome:** [✅ PASS / ❌ FAIL / ⚠️ PARTIAL]
- **QA Space ID:** `$STORYBLOK_SPACE_ID`

## Test execution

- [ ] [Brief description of step 1].
- [ ] [Brief description of step 2].

## Findings & observations

- **Issue or bug:** [Description of what failed or behaved unexpectedly].
- **DX observation:** [Feedback on the developer experience and command output].

## Recommendations

- [Suggestions for improvements or missing features].
```
