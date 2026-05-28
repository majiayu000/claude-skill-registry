---
name: sync-cli-skill
description: Synchronize the base44-cli skill with the latest CLI source code from the Base44 CLI repository
disable-model-invocation: true
---

# Sync CLI Skill

Synchronize the `skills/base44-cli/` skill with the latest CLI source code from the Base44 CLI repository using git-based change detection.

## Usage

When activated, this skill will ask for:
1. **CLI source folder path** (required) - The local path to the Base44 CLI source code (must be a git repository)

## How It Works

This skill uses git to efficiently detect changes:
1. Reads the locally stored version from `CLI_VERSION` (e.g., `v0.0.17`)
2. Compares against the CLI source repository to find changed command files
3. Only processes commands that have actually changed

## Steps

### Step 1: Gather Input

Ask the user for the CLI source folder path using the AskQuestion tool if available, otherwise ask conversationally:

**Required:**
- CLI source folder path (e.g., `~/projects/base44-cli` or `/Users/me/base44-cli`)

If the user provided this in the initial prompt, use that value.

### Step 2: Validate Source Folder and Discover Structure

1. Check that the provided path exists and is a git repository (`.git/` directory exists)
2. Check for `package.json` with CLI-related content
3. **Discover the commands directory** - look for directories containing command files:
   - Common patterns: `src/cli/commands/`, `src/commands/`, `commands/`, `lib/commands/`
   - Look for files with `.command(` or `program.command` patterns
4. **Identify the CLI source root** - the parent directory containing both commands and shared code

Store these discovered paths for use in subsequent steps:
- `<commands-path>`: Path to commands directory (e.g., `src/cli/commands`)
- `<cli-root>`: Path to CLI source root (e.g., `src/cli`)

If validation fails or structure is unclear, ask the user to clarify.

### Step 3: Read Local Version and Detect Changes

1. **Read the stored version** from `CLI_VERSION` in the skills repository root (e.g., `v0.0.17`)

2. **Get changed command files** using git in the CLI source folder:
   ```bash
   # From the CLI source folder, list command files changed since the stored version
   git diff --name-only <stored-version> HEAD -- <commands-path>
   ```
   
   If the stored version tag doesn't exist, fall back to:
   ```bash
   # List all command files if tag is missing
   git ls-files <commands-path>
   ```

3. **Get infrastructure changes** (CLI source root excluding commands):
   ```bash
   # From the CLI source folder, list infra files changed since the stored version
   git diff --name-only <stored-version> HEAD -- <cli-root> | grep -v "<commands-path>"
   ```

4. **Present findings** to the user before proceeding:
   ```
   Found X changed command files since vX.X.X:
   - <commands-path>/deploy.ts
   - <commands-path>/entities/push.ts
   - <commands-path>/auth/login.ts
   
   Found Y infrastructure changes (may affect all commands):
   - <cli-root>/utils/api-client.ts
   - <cli-root>/config/defaults.ts
   ```

5. **If no changes detected** (neither commands nor infra): Report "No changes since version X" and exit

### Step 4: Check Infrastructure Changes

Before processing individual commands, review any infrastructure changes that may affect **all commands**:

#### What to Look For

Review each changed non-command file and categorize by impact type:

| Impact Type | What to look for | Documentation Action |
|-------------|------------------|---------------------|
| API/Client changes | Base URLs, endpoints, headers, request/response handling | May affect multiple commands' behavior |
| Config/Defaults | Default values, environment variables, config file paths | Update SKILL.md config section |
| Authentication | Token handling, login flow, session management | Update auth-related references |
| Global options | CLI-wide flags like `--verbose`, `--json`, `--help` | Update SKILL.md global options |
| Output formatting | How results are displayed, logging behavior | Note in affected command references |
| Types/Interfaces | Shared type definitions | Usually internal, but may indicate API changes |
| Error handling | Exit codes, error messages, validation | Update troubleshooting section |
| Dependencies | `package.json` changes | Check for behavior-affecting updates |

**Note**: The actual file structure varies by CLI. Discover the structure by examining the git diff output rather than assuming specific paths.

#### How to Handle Infra Changes

1. **Read each changed infra file** to understand what changed
2. **Identify cross-cutting impacts**:
   - New global options → Update SKILL.md "Global Options" section
   - Changed defaults → Note in affected command references
   - Auth flow changes → Update auth-related references
   - New environment variables → Document in SKILL.md
   - API endpoint changes → May affect multiple commands
3. **Flag for SKILL.md update** if the change affects:
   - How users configure the CLI
   - Prerequisites or setup steps
   - Error messages users might see
   - Output format

#### Example Infrastructure Change

```
Changed file: (some config/defaults file)

Before:
  export const DEFAULT_TIMEOUT = 30000;
  
After:
  export const DEFAULT_TIMEOUT = 60000;

Impact: All commands now have 60s timeout instead of 30s
Action: Update SKILL.md "Configuration" or "Troubleshooting" section
```

### Step 5: Process Each Changed Command

For **each changed command file**, perform the following steps:

#### Step 5a: Read Existing Skill Reference

Read the corresponding reference file from `skills/base44-cli/references/`:

```
Skill reference structure:
skills/base44-cli/
├── SKILL.md
└── references/
    ├── auth-login.md      <- for <commands-path>/auth/login.ts
    ├── auth-logout.md
    ├── auth-whoami.md
    ├── create.md          <- for <commands-path>/create.ts
    ├── deploy.md
    ├── entities-create.md <- for <commands-path>/entities/create.ts
    ├── entities-push.md
    ├── functions-create.md
    ├── functions-deploy.md
    ├── rls-examples.md
    └── site-deploy.md
```

**Mapping rule**: `<commands-path>/{parent}/{name}.ts` → `references/{parent}-{name}.md`

If no reference file exists for a new command, note it for creation.

#### Step 5b: Compare Source with Documentation

Compare the CLI source code with the existing skill documentation:

##### Extract from Source
Parse the command file to extract:
- Command name and aliases
- Description/help text
- Available options and flags (name, alias, description, default, required, type)
- Usage examples (if present)
- Subcommands

##### Detect Changes
Identify differences:

**Command-Level:**
1. New commands (source exists, no reference file)
2. Changed command descriptions

**Option/Argument-Level (CRITICAL):**
3. New options added
4. Removed options
5. Changed option descriptions
6. Changed option defaults
7. Changed option types (e.g., string to boolean)
8. Changed required status
9. Changed option aliases (e.g., `-f` to `-F`)
10. **Option converted to positional argument** (e.g., `create -n my-app` → `create my-app`)
11. **Positional argument converted to option** (e.g., `create my-app` → `create -n my-app`)

**Detecting Option ↔ Positional Changes:**

Look for these patterns in Commander.js:
- Named option: `.option('-n, --name <value>', 'description')` or `.requiredOption(...)`
- Positional argument: `.argument('<name>', 'description')` or in command definition `.command('create <name>')`

When an option disappears but a positional argument with similar semantics appears (or vice versa), flag this as a **breaking change** that affects how users invoke the command.

##### Document the Comparison

```
Command: deploy (<commands-path>/deploy.ts)

Source options:
  --force (-f): Force deployment [boolean, default: false]
  --env <name>: Target environment [string, required]

Documented options (references/deploy.md):
  --force (-f): Force deploy without confirmation [boolean, default: false]  
  --env <name>: Environment name [string, optional]

Changes detected:
  - --force: description changed
  - --env: required status changed (required vs optional)
```

```
Command: create (<commands-path>/create.ts)

Source (current):
  Positional: <name> - The app name [required]
  Options: --template (-t): Template to use [string, optional]

Documented (references/create.md):
  Options:
    -n, --name <name>: The app name [string, required]
    --template (-t): Template to use [string, optional]

Changes detected:
  - BREAKING: --name (-n) option converted to positional argument <name>
    Old syntax: npx base44 create -n my-app
    New syntax: npx base44 create my-app
```

#### Step 5c: Update Reference File

Update or create `references/{command-name}.md` with the following format:

```markdown
# base44 {command}

{Description from source}

## Syntax

```bash
npx base44 {command} [options]
```

## Options

| Option | Description | Required |
|--------|-------------|----------|
| `-o, --option <value>` | {description} | {yes/no} |

## Examples

```bash
{example usage from source}
```

## Notes

{Any important behavioral notes}
```

### Step 6: Update Main Skill File (if needed)

After processing all changed commands:

1. Update the **Available Commands** tables in `skills/base44-cli/SKILL.md` if commands were added/removed
2. Update **Quick Start** if workflow changed
3. Update **Common Workflows** sections if relevant
4. Keep the existing structure and formatting
5. Do NOT change the frontmatter description unless explicitly asked

### Step 7: Update CLI_VERSION

After successfully updating all changed commands:

1. Get the current version/commit from the CLI source:
   ```bash
   # Get latest tag, or HEAD commit if no tags
   git describe --tags --always
   ```

2. Update `CLI_VERSION` in the skills repository root with the new version

### Step 8: Present Summary

After all updates, present a summary to the user:

```
## Sync Summary

### Version Updated
- Previous: v0.0.17
- Current: v0.0.20

### Changed Command Files Processed
- <commands-path>/deploy.ts
- <commands-path>/entities/push.ts

### Infrastructure Changes Reviewed
- (list infra files from git diff output)
- Example: config.ts (timeout increased to 60s)
- Example: api-client.ts (no user-facing changes)

### Files Updated
- references/deploy.md (updated options)
- references/entities-push.md (updated description)
- SKILL.md (updated command table, added timeout note)
- CLI_VERSION (v0.0.17 → v0.0.20)

### Breaking Changes (highlight prominently)
- `create`: `-n, --name` option converted to positional argument
  - Old: `npx base44 create -n my-app`
  - New: `npx base44 create my-app`

### Option Changes
- `deploy --env`: now required (was optional)
- `entities push --dry-run`: default changed from true to false

### New Commands
- (none)

### Removed Commands  
- (none)

### Manual Review Recommended
- [List any changes that need verification]
```

## Important Notes

- **Git-based detection**: This skill relies on git tags/commits to detect changes. Ensure the CLI source folder is a valid git repository.
- **Preserve existing content**: Don't remove detailed explanations, examples, or warnings unless they're outdated
- **Keep formatting consistent**: Match the existing style of SKILL.md and reference files
- **Maintain progressive disclosure**: Keep detailed docs in references, summaries in SKILL.md
- **Flag uncertainties**: If source code is unclear, flag it for manual review
- **Respect RLS/FLS docs**: The `entities-create.md` and `rls-examples.md` contain hand-written security documentation - update carefully

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Tag not found in CLI repo | Use `git tag -l` to list available tags, or fall back to comparing with a commit hash |
| Infra changes not detected | Check if shared code is in non-standard directories; adjust the git diff paths |
| Unsure if infra change affects users | Look for exports used by command files; if internal-only, note but skip documentation |
| Can't find command files | Try searching for `.command(` or `program.command` patterns |
| Options not detected | Look for `.option(` patterns in commander.js files |
| Positional args not detected | Look for `.argument(` or `<argName>` in `.command('cmd <argName>')` patterns |
| Option → positional change missed | Compare old options list with new arguments list; if an option disappeared and a similar argument appeared, it's likely a conversion |
| Missing descriptions | Check for `description:` properties or `.description(` calls |
| Subcommand structure | Commands like `entities push` may be in `entities/push.ts` |
| Changed args not detected | Compare each option property: name, alias, description, default, required, type |
| No changes detected but expected | Verify the stored version in `CLI_VERSION` matches a valid git tag/commit |
