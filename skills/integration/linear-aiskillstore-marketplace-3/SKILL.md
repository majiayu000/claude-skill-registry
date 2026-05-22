---
name: linear
description: Manages Linear issues, teams, and projects via CLI. Lists issues, creates tasks, views details, links issues, and runs GraphQL queries. Must use for "my Linear issues", "create Linear task", "link issues in Linear", "Linear API query", or any Linear project management request.
---

# Linear CLI

Interacts with Linear for issue tracking and project management using the `linear` command.

## Scope
- Use for Linear issue/project/teams management via the CLI or GraphQL (`linear gql`).
- Prefer built-in commands over raw GraphQL unless functionality is missing.
- Keep defaults in sync with the user's config; do not hard-code team IDs/outputs.

## Install & Setup
- Install: `npm install -g @0xbigboss/linear-cli`
- Auth: `linear auth set` or set `LINEAR_API_KEY`
- Defaults: `linear config set default_team_id TEAM_KEY`, `linear config set default_output json|table`, `linear config set default_state_filter completed,canceled`
- Inspect or reset defaults: `linear config show`, `linear config unset default_output`
- Config path: `~/.config/linear/config.json` (override with `--config PATH` or `LINEAR_CONFIG`)

## Prerequisites
- CLI installed and on PATH
- Valid Linear API key available
- Team defaults set or provided per command (team key/UUID)

## Hygiene

- **Branches**: Name as `{TICKET}-{short-name}` (e.g., `ENG-123-fix-auth`); prefer git worktrees for parallel work
- **Commits**: Use conventional commits; ticket ID in body or trailer, not subject
- **Assignment**: Assign yourself when starting work (`linear issue update ENG-123 --assignee me --yes`)
- **Sub-issues**: Set parent to associate related work (requires UUID: `linear issue update ENG-123 --parent PARENT_UUID --yes`)
- **Scope creep**: Create separate issues for discovered work; link with blocks relation (`linear issue link ENG-123 --blocks ENG-456 --yes`)
- **Cycles/projects**: Ask user preference when creating issues

## Quick Recipes

### List my issues
```bash
linear issues list --team TEAM_KEY --assignee me --human-time
```

### Search issues
```bash
linear search "keyword" --team TEAM_KEY --limit 10
```

### Create an issue
```bash
linear issue create --team TEAM_KEY --title "Fix bug" --yes
# Returns identifier (e.g., ENG-123)
```

### View issue details
```bash
linear issue view ENG-123
```

### Get issue as JSON for processing
```bash
linear issue view ENG-123 --json
```

### Get issue with full context (for agents/analysis)
```bash
linear issue view ENG-123 --fields identifier,title,state,assignee,priority,url,description,parent,sub_issues,comments --json
```

### List all teams
```bash
linear teams list
```

### Verify authentication
```bash
linear auth test
```

### List projects
```bash
linear projects list --limit 10
```

### View or change CLI defaults
```bash
linear config show
linear config set default_output json
linear config unset default_state_filter
```

### Add a comment to an issue
```bash
linear issue comment ENG-123 --body "Comment text here" --yes

# Or from a file/stdin
cat notes.md | linear issue comment ENG-123 --body-file - --yes
```

### Create and manage a project
```bash
# Create project (team UUID required)
linear project create --team TEAM_UUID --name "My Project" --state planned --yes

# Update project state
linear project update PROJECT_ID --state started --yes

# Add issue to project
linear project add-issue PROJECT_ID ISSUE_UUID --yes
```

## Command Reference

| Command | Purpose |
|---------|---------|
| `linear issues list` | List issues with filters |
| `linear search "keyword"` | Search issues by text |
| `linear issue view ID` | View single issue |
| `linear issue create` | Create new issue |
| `linear issue update ID` | Update issue (assign, state, priority, parent*) |
| `linear issue link ID` | Link issues (blocks, related, duplicate) |
| `linear issue comment ID` | Add comment to issue |
| `linear issue delete ID` | Archive an issue |
| `linear projects list` | List projects |
| `linear project view ID` | View project details |
| `linear project create` | Create new project |
| `linear project update ID` | Update project (state, name, dates) |
| `linear project delete ID` | Archive a project |
| `linear project add-issue` | Add issue to project |
| `linear project remove-issue` | Remove issue from project |
| `linear teams list` | List available teams |
| `linear me` | Show current user |
| `linear gql` | Run raw GraphQL |
| `linear help CMD` | Command-specific help |

*`--parent` requires UUIDs, not identifiers. See [Finding IDs](#finding-ids).

## Common Flags

- `--team ID\|KEY` - Specify team (required for most commands)
- `--json` - Output as JSON
- `--yes` - Confirm mutations without prompt
- `--human-time` - Show relative timestamps
- `--fields LIST` - Select specific fields
- `--help` - Show command help

## Workflow: Creating and Linking Issues

**Note:** `--parent` requires UUIDs. Get UUID with `linear issue view ID --json | jq -r '.issue.id'`

```
Progress:
- [ ] List teams to get TEAM_KEY: `linear teams list`
- [ ] Create parent issue: `linear issue create --team KEY --title "Epic" --yes`
- [ ] Create child issue: `linear issue create --team KEY --title "Task" --yes`
- [ ] Get parent UUID: `linear issue view PARENT_ID --json | jq -r '.issue.id'`
- [ ] Set parent (UUID required): `linear issue update CHILD_ID --parent PARENT_UUID --yes`
- [ ] Create another issue to link: `linear issue create --team KEY --title "Blocked" --yes`
- [ ] Link blocking issue: `linear issue link ISSUE_ID --blocks OTHER_ID --yes`
- [ ] Verify: `linear issue view ISSUE_ID --json`
```

## Common Gotchas

| Problem | Cause | Solution |
|---------|-------|----------|
| Empty results | No team specified | Add `--team TEAM_KEY` |
| 401 Unauthorized | Invalid/missing API key | Run `linear auth test` |
| Mutation does nothing | Missing confirmation | Add `--yes` flag |
| Can't find issue | Wrong ID or missing access | `issue view` accepts identifier or UUID; verify spelling and permissions |
| --parent fails | Using identifier | `--parent` flag requires UUID, not identifier |

**ID format summary:** Most commands accept identifiers (ENG-123). Exception: `--parent` requires UUIDs.

## Advanced Operations

For operations not covered by built-in commands, use `linear gql` with GraphQL:

- **Add attachments** - See `graphql-recipes.md` → "Attach URL to Issue"
- **Upload files** - See `graphql-recipes.md` → "Upload File"

Note: Adding comments is now available via `linear issue comment`. Setting parent is available via `issue update --parent`, but requires UUIDs. Use `linear issue view ID --json` to get UUIDs.

## Finding IDs

**Important:** `issue update --parent` requires UUIDs.

```bash
# Get issue UUID from identifier
linear issue view ENG-123 --json | jq -r '.issue.id'

# Current user UUID
linear me --json | jq -r '.viewer.id'

# All teams with UUIDs
linear teams list --json

# Issue full details including UUID
linear issue view ENG-123 --json
```

Or in Linear app: Cmd/Ctrl+K → "Copy model UUID"

## JSON Output Structures

Commands with `--json` return nested structures. Use these jq paths:

| Command | Root path | Items path |
|---------|-----------|------------|
| `issue view ID` | `.issue` | N/A (single object) |
| `issue view ID --fields ...` | `.` | N/A (flat object of selected fields) |
| `issues list` | `.issues` | `.issues.nodes[]` |
| `project view ID` | `.project` | N/A (single object) |
| `projects list` | `.projects` | `.projects.nodes[]` |
| `teams list` | `.teams` | `.teams.nodes[]` |
| `me` | `.viewer` | N/A (single object) |
| `search` | `.issues` | `.issues.nodes[]` |

**Null handling:** Many fields can be null (name, description, dates, assignee). Use null-safe filters.

### jq Patterns

```bash
# List all projects (correct path)
linear projects list --json | jq '.projects.nodes[]'

# Filter projects by name (null-safe)
linear projects list --json | jq '.projects.nodes[] | select(.name) | select(.name | ascii_downcase | contains("keyword"))'

# Get project names as array
linear projects list --json | jq '[.projects.nodes[].name]'

# Filter issues by title
linear issues list --team TEAM --json | jq '.issues.nodes[] | select(.title | ascii_downcase | contains("bug"))'

# Extract specific fields
linear issues list --team TEAM --json | jq '.issues.nodes[] | {id: .identifier, title, state: .state.name}'

# Get issue UUID from identifier
linear issue view ENG-123 --json | jq -r '.issue.id'
```

**Common mistakes:**
- `.[]` on root - use `.projects.nodes[]` or `.issues.nodes[]`
- `test("pattern"; "i")` on null - filter nulls first with `select(.field)`
- Escaping `!=` in shells - use `select(.field)` instead of `select(.field != null)`

## Reference Files

- `graphql-recipes.md` - GraphQL mutations for attachments, relations, comments, file uploads
- `troubleshooting.md` - Common errors and debugging steps

## External Links

- [Linear API Docs](https://linear.app/developers/graphql)
- [Schema Explorer](https://studio.apollographql.com/public/Linear-API/variant/current/schema/reference)
