---
name: claude-worktree-manager
description: Create and manage Claude-specific worktrees with automated setup and cleanup. Use this skill (via Skill tool or direct script) when asked to "create a worktree", "new worktree", "worktree for feature/staging", "setup isolated environment", or "cleanup old worktrees". Script path is auto-detected when using Skill tool. Handles smart naming, .env copying, background pnpm install, and automatic cleanup of stale worktrees.
---

# Claude Worktree Manager

Automated worktree management for Claude Code development sessions with smart naming, auto-setup, and cleanup.

## How to Use This Skill

There are two ways to create worktrees:

### 1. Via Claude Code Skill (Recommended)

Use the `Skill` tool to invoke this skill - **the script path is detected automatically**:

```javascript
// Using Skill tool with args parameter (Recommended)
Skill(skill: 'claude-worktree-manager', args: 'create feature-name --model opus')
Skill(skill: 'claude-worktree-manager', args: 'create feature-name --isolated --model sonnet')

// All bash script flags work the same via args
Skill(skill: 'claude-worktree-manager', args: 'list')
Skill(skill: 'claude-worktree-manager', args: 'cleanup --days 14')
```

The skill handles all path resolution using `git rev-parse --show-toplevel`, so you only need to provide the worktree name and optional flags. All bash script flags (`--model`, `--isolated`, `--days`) work exactly the same when passed via the `args` parameter.

### 2. Via Direct Script Invocation

If you're running the script manually, provide the full path from any directory:

```bash
.claude/skills/claude-worktree-manager/scripts/worktree.sh create feature-name --model opus
```

Or use the full absolute path:

```bash
/path/to/repo/.claude/skills/claude-worktree-manager/scripts/worktree.sh create feature-name --model opus
```

## Invocation Method Comparison

To clarify the correct syntax for each invocation method:

| Task                     | Skill Tool                                                                                | Direct Script                                                                                       |
| ------------------------ | ----------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Create standard worktree | `Skill(skill: 'claude-worktree-manager', args: 'create my-feature')`                      | `.claude/skills/claude-worktree-manager/scripts/worktree.sh create my-feature`                      |
| With model flag          | `Skill(skill: 'claude-worktree-manager', args: 'create my-feature --model opus')`         | `.claude/skills/claude-worktree-manager/scripts/worktree.sh create my-feature --model opus`         |
| With isolated database   | `Skill(skill: 'claude-worktree-manager', args: 'create schema-test --isolated')`          | `.claude/skills/claude-worktree-manager/scripts/worktree.sh create schema-test --isolated`          |
| Both flags combined      | `Skill(skill: 'claude-worktree-manager', args: 'create complex --isolated --model opus')` | `.claude/skills/claude-worktree-manager/scripts/worktree.sh create complex --isolated --model opus` |
| List worktrees           | `Skill(skill: 'claude-worktree-manager', args: 'list')`                                   | `.claude/skills/claude-worktree-manager/scripts/worktree.sh list`                                   |
| Cleanup old worktrees    | `Skill(skill: 'claude-worktree-manager', args: 'cleanup --days 7')`                       | `.claude/skills/claude-worktree-manager/scripts/worktree.sh cleanup --days 7`                       |

**Key Differences:**

- **Skill tool:** All commands and flags are passed as a single string via the `args` parameter
- **Direct script:** Commands and flags are bash arguments, requires absolute or relative path

## Verifying Model Configuration

After creating a worktree with `--model`, verify the configuration was set correctly:

```bash
# Navigate to your worktree
cd /path/to/worktree

# Run verification script
.claude/skills/claude-worktree-manager/scripts/verify-worktree-model.sh

# Or verify from anywhere by passing the path
.claude/skills/claude-worktree-manager/scripts/verify-worktree-model.sh /path/to/worktree
```

**Expected output when successful:**

```
[INFO] Verifying Claude model configuration in: /path/to/worktree
[SUCCESS] .claude/settings.local.json found
[SUCCESS] Model configuration found: opus
[SUCCESS] Model is valid: opus
```

The validation script will:

1. Check that `.claude/settings.local.json` exists
2. Extract the model value using jq or grep
3. Validate the model is one of: opus, sonnet, haiku
4. Provide instructions if configuration is missing or invalid

See the **Model Flag Configuration - Edge Cases & Troubleshooting** section below for fixing common issues.

## ⚠️ Critical: Model Configuration Warning

**Before starting Claude in a worktree with `--model` flag, you MUST run the verification script.**

The model configuration uses `jq` (preferred) or `sed` (fallback) to update JSON files. These tools can **fail silently** on some systems, resulting in Claude using the wrong model.

### Quick Reference: Model Configuration Troubleshooting

| Symptom                                | Likely Cause         | Quick Fix                                                           |
| -------------------------------------- | -------------------- | ------------------------------------------------------------------- |
| Claude uses wrong model                | Verification skipped | Run `verify-worktree-model.sh` before starting Claude               |
| `[WARN] jq not found` in output        | jq not installed     | Install jq: `brew install jq` (macOS) or `apt install jq` (Linux)   |
| Model key missing in JSON              | sed fallback failed  | Manually add `"model": "opus"` to settings.local.json               |
| JSON file is corrupted                 | sed pattern mismatch | Delete settings.local.json, copy from main repo, add model manually |
| `[SUCCESS]` shown but wrong model used | Multiple model keys  | Check for duplicate `"model"` entries in JSON                       |

### Default Model Configuration

The script has a **default model** configured: `sonnet`

- All new worktrees automatically use this model unless overridden with `--model`
- To change the default, edit `DEFAULT_MODEL` in the script
- Override for specific worktrees: `--model opus` or `--model haiku`

**⚠️ Important: Setting DEFAULT_MODEL does NOT make verification optional!**

Even with a default model configured, you MUST still run `verify-worktree-model.sh` after creating a worktree. The default model goes through the same jq/sed configuration process that can fail silently.

### Complete Workflow: Create → Verify → Start

**Scenario 1: Using default model (sonnet)**

```bash
# 1. Create worktree (automatically uses DEFAULT_MODEL=sonnet)
WORKTREE_PATH=$(.claude/skills/claude-worktree-manager/scripts/worktree.sh create my-feature | tail -1)
# Output: [INFO] Using default model: sonnet

# 2. REQUIRED: Verify the default model was set correctly
.claude/skills/claude-worktree-manager/scripts/verify-worktree-model.sh "$WORKTREE_PATH"
# Expected: [SUCCESS] Model is valid: sonnet

# 3. Only start Claude AFTER verification succeeds
cd "$WORKTREE_PATH" && claude 'Your goal'
```

**Scenario 2: Using custom model (opus)**

```bash
# 1. Create worktree with explicit model (overrides DEFAULT_MODEL)
WORKTREE_PATH=$(.claude/skills/claude-worktree-manager/scripts/worktree.sh create complex-task --model opus | tail -1)
# Output: [INFO] Setting default model to: opus

# 2. REQUIRED: Verify the custom model was set correctly
.claude/skills/claude-worktree-manager/scripts/verify-worktree-model.sh "$WORKTREE_PATH"
# Expected: [SUCCESS] Model is valid: opus

# 3. Only start Claude AFTER verification succeeds
cd "$WORKTREE_PATH" && claude 'Your complex goal'
```

**Verification output for default model worktrees:**

```
[INFO] Verifying Claude model configuration in: /path/to/worktree
[SUCCESS] .claude/settings.local.json found
[SUCCESS] Model configuration found: sonnet
[SUCCESS] Model is valid: sonnet
```

## Quick Start

### Create a Worktree

When the user asks to create a worktree for a feature or environment, derive a short, descriptive kebab-case name from their request:

**Naming examples:**

- "staging environment" → `staging-env`
- "add dark mode toggle" → `dark-mode`
- "fix authentication bug" → `fix-auth-bug`
- "update API endpoints" → `update-api`

Then run:

```bash
# Standard (uses shared dev database)
.claude/skills/claude-worktree-manager/scripts/worktree.sh create <derived-name>

# With specific model (e.g., opus, sonnet, haiku)
.claude/skills/claude-worktree-manager/scripts/worktree.sh create <derived-name> --model opus

# Isolated (creates dedicated database with seeding)
.claude/skills/claude-worktree-manager/scripts/worktree.sh create <derived-name> --isolated

# Isolated with model
.claude/skills/claude-worktree-manager/scripts/worktree.sh create <derived-name> --isolated --model sonnet
```

**What happens:**

1. Cleans up worktrees older than 7 days
2. Fetches latest from origin
3. Checks if a branch with your name already exists on origin:
   - **If found:** Creates local branch tracking the remote, pulls latest changes
   - **If not found:** Creates new branch: `worktree/<name>-<timestamp>` from main
4. Creates worktree at: `~/claude-worktrees/<project-name>/<name>-<timestamp>`
5. Copies `.env` from main repo
6. Copies `.claude/settings.local.json` from main repo (API keys, preferences)
7. Starts `pnpm install` in background
8. If `--model`: Sets default Claude model in `.claude/settings.local.json`
9. If `--isolated`: Creates dedicated database and seeds it with test data
10. Returns the worktree path immediately

### Required: Verify Model Configuration Before Starting Claude

When creating worktrees with the `--model` flag, **you MUST verify the configuration before starting Claude**:

```bash
# 1. Create worktree with model
WORKTREE_PATH=$(.claude/skills/claude-worktree-manager/scripts/worktree.sh create my-feature --model opus | tail -1)

# 2. REQUIRED: Verify the model was set correctly
.claude/skills/claude-worktree-manager/scripts/verify-worktree-model.sh "$WORKTREE_PATH"
# Must show: [SUCCESS] Model is valid: opus

# 3. Check pnpm install progress (optional)
tail -f "$WORKTREE_PATH/.pnpm-install.log"

# 4. Only start Claude AFTER verification succeeds
cd "$WORKTREE_PATH"
claude 'Your goal here'
```

**Why is verification required?**

1. **jq/sed fallback can fail silently:** The script uses `jq` (preferred) or `sed` (fallback) to update JSON. On some systems, `sed` may fail without error.

2. **macOS vs Linux sed differences:** macOS uses BSD sed which requires `-i ''` while Linux uses GNU sed with `-i`. The script handles this, but edge cases exist.

3. **JSON syntax can break:** Malformed JSON in `settings.local.json` can cause the update to fail.

4. **Claude uses wrong model without verification:** If you start Claude before verifying, it will use the default model instead of your requested model, wasting time and potentially money.

**If verification fails:** See the "Model Flag Configuration - Edge Cases & Troubleshooting" section below for manual fixes.

### When to Use --isolated

Use the `--isolated` flag when:

- **Schema changes:** Testing database migrations
- **Migration testing:** Verifying migration scripts work correctly
- **Isolated experiments:** Need a clean database state
- **Breaking changes:** Don't want to affect shared dev data

For normal feature development, skip `--isolated` to use the shared database.

### Automatic Script Location Detection

When you invoke this skill using the Skill tool (e.g., `Skill(claude-worktree-manager)`), the skill automatically:

1. Detects your current git repository using `git rev-parse --show-toplevel`
2. Locates the worktree script at `.claude/skills/claude-worktree-manager/scripts/worktree.sh`
3. Executes the script from the repository root

**You don't need to specify absolute paths or worry about the script location.** The skill handles all path resolution automatically. Just use simple worktree names and optional flags:

```bash
# Via Skill tool - automatic path resolution
Skill(claude-worktree-manager) create my-feature --model sonnet

# Via direct script - requires full path from any directory
/path/to/repo/.claude/skills/claude-worktree-manager/scripts/worktree.sh create my-feature --model sonnet
```

### Model Selection

Use the `--model` flag to set the default Claude model for the worktree:

```bash
.claude/skills/claude-worktree-manager/scripts/worktree.sh create <name> --model <model-name>
```

**Available models:** `opus`, `sonnet`, `haiku`

When specified, the model is configured in the worktree's `.claude/settings.local.json` so that all Claude Code sessions in that worktree use the selected model by default. This is useful for:

- **Testing with specific models:** Quickly test a feature with Opus for complex work or Haiku for speed
- **Cost optimization:** Use Haiku for routine tasks, Opus for complex reasoning
- **Consistency:** Ensure all team members working in a specific worktree use the same model

**Important:** Return the worktree path to the user so they can open a new Claude Code session in that directory.

### Ghostty Integration (Automatic)

After creating a worktree, check if running in Ghostty terminal and automatically open a new tab with Claude:

```bash
# The worktree script outputs the path on its last line
WORKTREE_PATH=$(.claude/skills/claude-worktree-manager/scripts/worktree.sh create <name> | tail -1)

# If in Ghostty, open new tab with Claude (--no-enter types but doesn't execute)
if [ "$TERM_PROGRAM" = "ghostty" ]; then
    ghostty-tab -d "$WORKTREE_PATH" --no-enter "claude '<goal-prompt>'"
fi
```

**Goal Prompt Guidelines:**

- Keep it concise (1-2 sentences max)
- Focus on the task objective
- Use imperative voice
- Avoid special characters that need escaping (use simple quotes)

**Examples:**

- "Refactor the project to support multi-tenant architecture"
- "Fix the authentication redirect bug in login flow"
- "Add OAuth2 support with Google and GitHub providers"
- "Implement dark mode toggle with system preference detection"

**Important:** The `ghostty-tab` command is at `~/.local/bin/ghostty-tab` and uses AppleScript to open a new Ghostty tab. It accepts:

- `-d <path>` - Directory to cd into
- `--no-enter` - Type the command but don't press enter (lets user review before executing)
- `"<command>"` - Command to type/run after cd

This automatically opens a new Ghostty tab, navigates to the worktree, and starts Claude with the goal context.

### List Worktrees

```bash
.claude/skills/claude-worktree-manager/scripts/worktree.sh list
```

Shows all active worktrees for the current project with their branches.

### Manual Cleanup

```bash
# Cleanup worktrees older than 7 days (default)
.claude/skills/claude-worktree-manager/scripts/worktree.sh cleanup

# Custom age threshold
.claude/skills/claude-worktree-manager/scripts/worktree.sh cleanup --days 14
```

## Origin Branch Handling

The script intelligently checks if a branch with your name already exists on origin:

**Scenario 1: Branch exists on origin**

```bash
.claude/skills/claude-worktree-manager/scripts/worktree.sh create my-feature
```

If `origin/my-feature` exists, the script will:

- Create a local branch tracking `origin/my-feature`
- Pull the latest changes automatically
- Create the worktree on this branch
- Useful for continuing work on an existing feature branch

**Scenario 2: Branch doesn't exist on origin**

```bash
.claude/skills/claude-worktree-manager/scripts/worktree.sh create my-feature
```

If `origin/my-feature` doesn't exist, the script will:

- Create a new branch from main: `worktree/my-feature-<timestamp>`
- Create a fresh worktree for new development

This means you can use simple names (like `restructure-prompts`) and the script will automatically handle both new work and continuing existing branches.

## Workflow

### 1. User Requests Worktree

User says: "I want to create a new worktree for developing a staging environment"

### 2. Derive Smart Name

Analyze the request and derive a concise kebab-case name:

- Extract key purpose: "staging environment"
- Convert to kebab-case: `staging-env`

### 3. Create Worktree and Capture Path

```bash
# Run the script and capture the worktree path (last line of output)
WORKTREE_PATH=$(.claude/skills/claude-worktree-manager/scripts/worktree.sh create staging-env | tail -1)
echo "Created: $WORKTREE_PATH"
```

### 4. Open in Ghostty (if available)

After creating the worktree, check if running in Ghostty and automatically open a new tab:

```bash
# Check if in Ghostty and open new tab with Claude (--no-enter lets user review first)
if [ "$TERM_PROGRAM" = "ghostty" ]; then
    ghostty-tab -d "$WORKTREE_PATH" --no-enter "claude 'Set up and configure the staging environment'"
fi
```

### 5. Return Path

The script outputs the worktree path. Return it to the user:

```
Worktree created at: ~/claude-worktrees/orienter/staging-env-1736639420

✓ Opened new Ghostty tab with Claude command ready (press Enter to start)
  Goal: Set up and configure the staging environment

Note: pnpm install is running in the background. Check progress with:
tail -f ~/claude-worktrees/orienter/staging-env-1736639420/.pnpm-install.log
```

If NOT in Ghostty, show manual instructions:

```
Worktree created at: ~/claude-worktrees/orienter/staging-env-1736639420

You can now open a new Claude Code session in this directory:
cd ~/claude-worktrees/orienter/staging-env-1736639420

Note: pnpm install is running in the background. Check progress with:
tail -f ~/claude-worktrees/orienter/staging-env-1736639420/.pnpm-install.log
```

## Background Installation

The worktree creation starts `pnpm install` in the background using `nohup`. This means:

- The path is returned immediately (don't wait for pnpm)
- Installation runs async and logs to `.pnpm-install.log`
- User can start working right away
- Dependencies will be available after a few moments

Check if installation is complete:

```bash
# Check if still running
ps aux | grep pnpm

# Watch the log
tail -f <worktree-path>/.pnpm-install.log
```

## Database Seeding (Isolated Mode)

When using `--isolated`, the script automatically:

1. Creates a new PostgreSQL database: `worktree_<timestamp>`
2. Updates the worktree's `.env` with the new DATABASE_URL
3. Runs all migrations from `data/migrations/`
4. Seeds the database with:
   - **5 agents:** pm-assistant, communicator, scheduler, explorer, app-builder
   - **6 context rules:** Platform and environment routing
   - **6 test permissions:** Sample WhatsApp and Slack permissions
   - **4 sample prompts:** Default prompts for testing

Database seeding starts after pnpm install completes. Check progress:

```bash
tail -f <worktree-path>/.db-seed.log
```

### Manual Database Seeding

If you need to seed an existing worktree:

```bash
# Seed with shared database (from .env)
./scripts/seed-worktree-db.sh

# Create isolated database and seed
ISOLATED=true ./scripts/seed-worktree-db.sh
```

## Configuration Files

The script automatically handles configuration files:

**Automatically Available (via git):**

- `.claude/skills/` - All skills are available in worktrees
- `.claude/settings.json` - Committed Claude settings

**Automatically Copied:**

- `.env` - Environment variables for the application
- `.claude/settings.local.json` - Local Claude settings (API keys, preferences)

This ensures your worktree has the same development environment as the main repo.

## Integration with worktree-operations

After creating the worktree, users can reference the **worktree-operations** skill for:

- Building packages: `pnpm run build`
- Running tests: `pnpm test`
- Development mode: `pnpm run dev`
- Type checking: `pnpm run typecheck`

The worktree-operations skill covers all pnpm/turbo commands for working in the monorepo.

## Directory Structure

```
~/claude-worktrees/
└── <project-name>/
    ├── feature-a-1736639420/
    ├── staging-env-1736639421/
    └── fix-bug-1736639422/
```

Each project gets its own subdirectory under `~/claude-worktrees/`.

## Cleanup Policy

- **Automatic:** Runs before each worktree creation
- **Threshold:** Removes worktrees older than 7 days (based on modification time)
- **Safe:** Only removes worktrees in the Claude worktree directory
- **Manual:** Can be triggered anytime with `./worktree.sh cleanup`

## .env Configuration Requirements

The `.env` file is copied to worktrees automatically. Ensure proper formatting to avoid shell parsing errors:

### Quote Special Characters

Values with special characters MUST be quoted:

```bash
# ✅ Correct - quoted values
DATABASE_URL="postgresql://user:pass@localhost:5432/db"
STANDUP_CRON="30 9 * * 1-5"
STANDUP_CHANNEL="#orienter-standups"

# ❌ Wrong - unquoted special chars cause shell errors
STANDUP_CRON=30 9 * * 1-5          # Shell expands * as glob
STANDUP_CHANNEL=#orienter-standups  # Shell treats # as comment
```

### Required Variables

For database seeding to work, ensure `DATABASE_URL` is set:

```bash
DATABASE_URL="postgresql://aibot:aibot123@localhost:5432/whatsapp_bot"
```

### Common Shell Parsing Errors

If you see errors like `command not found` when sourcing `.env`:

- Check for unquoted cron expressions (`* * *`)
- Check for unquoted channel names starting with `#`
- Ensure no trailing spaces after values

## Model Flag Configuration - Edge Cases & Troubleshooting

The `--model` flag updates `.claude/settings.local.json` to set the default Claude model for your worktree. This section documents potential edge cases and how to handle them.

### Requirements

The script requires one of the following tools to update JSON:

1. **jq** (preferred) - Safely parses and updates JSON
2. **sed** (fallback) - Uses text substitution, less reliable but works when jq is unavailable

Most systems have `sed` built-in. To install `jq`:

```bash
# macOS
brew install jq

# Ubuntu/Debian
sudo apt-get install jq

# Or use your system package manager
```

### How Model Configuration Works

The script attempts to update `.claude/settings.local.json` with your selected model:

**Step 1: Check for jq**

```bash
if command -v jq &> /dev/null; then
    # Use jq (preferred, safe JSON manipulation)
else
    # Fall back to sed (text substitution, can fail silently)
fi
```

**Step 2a: With jq (preferred)**

```bash
jq ".model = \"opus\"" settings.local.json > settings.local.json.tmp
mv settings.local.json.tmp settings.local.json
```

- ✅ Safely parses JSON
- ✅ Preserves formatting and other keys
- ✅ Creates valid JSON output
- ✅ Handles edge cases (nested objects, arrays)

**Step 2b: With sed (fallback)**

```bash
# macOS (BSD sed)
sed -i '' "s/\"model\": \"[^\"]*\"/\"model\": \"opus\"/g" file.json

# Linux (GNU sed)
sed -i "s/\"model\": \"[^\"]*\"/\"model\": \"opus\"/g" file.json
```

- ⚠️ Text-based replacement, not JSON-aware
- ⚠️ May fail silently if pattern doesn't match
- ⚠️ macOS and Linux have different sed flags

### macOS vs Linux sed Differences

| Aspect         | macOS (BSD sed) | Linux (GNU sed)           |
| -------------- | --------------- | ------------------------- |
| In-place edit  | `sed -i ''`     | `sed -i`                  |
| Extended regex | `sed -E`        | `sed -r` or `sed -E`      |
| Backup suffix  | `sed -i '.bak'` | `sed -i'.bak'` (no space) |

The script handles these differences automatically, but edge cases can still occur.

### JSON File States: Valid vs Broken

**✅ Valid JSON after successful configuration:**

```json
{
  "model": "opus",
  "permissions": {
    "allow": ["Bash(git:*)"]
  }
}
```

**❌ Broken JSON - sed added model incorrectly:**

```json
{{"model": "opus",
  "permissions": {
    "allow": ["Bash(git:*)"]
  }
}
```

**❌ Broken JSON - duplicate model keys:**

```json
{
  "model": "opus",
  "model": "sonnet",
  "permissions": { ... }
}
```

**❌ Missing model - sed pattern didn't match:**

```json
{
  "permissions": {
    "allow": ["Bash(git:*)"]
  }
}
```

### Troubleshooting: Model Not Applied

If Claude doesn't use the configured model:

**Step 1: Verify the model was set**

```bash
# Go to your worktree and verify
cd /path/to/worktree
.claude/skills/claude-worktree-manager/scripts/verify-worktree-model.sh

# Or from anywhere (pass worktree path)
.claude/skills/claude-worktree-manager/scripts/verify-worktree-model.sh /path/to/worktree
```

**Step 2: Check settings.local.json contents**

```bash
cat /path/to/worktree/.claude/settings.local.json | grep -i model
```

You should see:

```json
{
  "model": "opus",
  "permissions": { ... }
}
```

**Step 3: If model is missing, add it manually**

If the model key is missing, add it to the top level of `.claude/settings.local.json`:

```bash
# Edit the file manually
nano /path/to/worktree/.claude/settings.local.json
```

The file should look like:

```json
{
  "model": "opus",
  "permissions": {
    "allow": [ ... ]
  }
}
```

### Common Issues

#### Issue: "jq not found" in logs but model was set

**Why:** The script fell back to sed, which is less reliable. jq is recommended.

**Fix:** Install jq and re-create the worktree with the `--model` flag

```bash
# Install jq
brew install jq  # or sudo apt-get install jq

# Re-create worktree with model flag
.claude/skills/claude-worktree-manager/scripts/worktree.sh create my-feature --model opus
```

#### Issue: Model key added but not using that model

**Why:** The model might be formatted incorrectly or Claude Code might not be reading it.

**Fix:** Verify the JSON is valid and properly formatted:

```bash
# Verify JSON syntax is valid
jq . /path/to/worktree/.claude/settings.local.json

# Should output valid JSON without errors
```

If JSON is invalid, edit the file to fix syntax errors (missing quotes, commas, etc).

#### Issue: sed failed silently, model not set

**Why:** This can happen on systems with different sed versions or in edge cases.

**Fix:** Use jq or manually edit the file

```bash
# Option 1: Install jq and re-create worktree
brew install jq
.claude/skills/claude-worktree-manager/scripts/worktree.sh create my-feature --model opus

# Option 2: Manually add the model to the file
nano /path/to/worktree/.claude/settings.local.json
# Add "model": "opus", at the top level
```

#### Issue: Model works in worktree but not when using goal prompt

**Why:** The Ghostty tab might be starting Claude in a different context or with different settings.

**Fix:** Verify the model is set and start Claude from within the worktree:

```bash
# Navigate to worktree
cd /path/to/worktree

# Verify model
.claude/skills/claude-worktree-manager/scripts/verify-worktree-model.sh

# Start Claude directly
claude 'Your goal prompt here'

# Claude will load settings from the current worktree directory
```

### Validation Script

Use the validation script to verify worktree model configuration:

```bash
# From the worktree directory
cd /path/to/worktree
.claude/skills/claude-worktree-manager/scripts/verify-worktree-model.sh

# Or from anywhere
.claude/skills/claude-worktree-manager/scripts/verify-worktree-model.sh /path/to/worktree
```

**Output examples:**

✅ Correct:

```
[INFO] Verifying Claude model configuration in: /path/to/worktree
[SUCCESS] .claude/settings.local.json found
[SUCCESS] Model configuration found: opus
[SUCCESS] Model is valid: opus
```

❌ Missing model:

```
[INFO] Verifying Claude model configuration in: /path/to/worktree
[SUCCESS] .claude/settings.local.json found
[WARN] No model configuration found in settings.local.json
```

### Manual Model Configuration

If automatic configuration fails, manually edit `.claude/settings.local.json`:

```bash
# Navigate to worktree
cd /path/to/worktree

# Open settings file
nano .claude/settings.local.json
```

**Add the model key at the top level:**

```json
{
  "model": "opus",
  "permissions": {
    "allow": [ ... ]
  }
}
```

**Valid model values:**

- `"opus"` - Claude Opus 4.5 (most capable)
- `"sonnet"` - Claude Sonnet (balanced)
- `"haiku"` - Claude Haiku (fastest/cheapest)

**After saving, verify with the validation script:**

```bash
.claude/skills/claude-worktree-manager/scripts/verify-worktree-model.sh
```

## Troubleshooting

### pnpm install failed

Check the log:

```bash
cat <worktree-path>/.pnpm-install.log
```

Re-run manually if needed:

```bash
cd <worktree-path>
pnpm install
```

### .env not copied

Copy manually:

```bash
cp <main-repo>/.env <worktree-path>/.env
```

### Database seeding failed

Check the log:

```bash
cat <worktree-path>/.db-seed.log
```

Common issues:

- PostgreSQL not running: `docker compose -f docker/docker-compose.infra.yml up -d postgres`
- Invalid DATABASE_URL: Check quotes and format
- Missing tables: Run `npm run db:migrate` first

### Worktree creation failed

Check git status and ensure:

- You're in a git repository
- Remote is accessible
- No uncommitted changes blocking the operation

## Examples

### Create worktree for a feature (with Ghostty)

User: "Create a worktree for adding OAuth support"

```bash
# 1. Create the worktree and capture path
WORKTREE_PATH=$(.claude/skills/claude-worktree-manager/scripts/worktree.sh create oauth-support | tail -1)

# 2. If in Ghostty, open new tab with Claude
if [ "$TERM_PROGRAM" = "ghostty" ]; then
    ghostty-tab -d "$WORKTREE_PATH" --no-enter "claude 'Add OAuth support with Google and GitHub providers'"
fi
```

### Create worktree with specific model

User: "Create a worktree for complex refactoring using Opus"

```bash
# 1. Create the worktree with Opus model and capture path
WORKTREE_PATH=$(.claude/skills/claude-worktree-manager/scripts/worktree.sh create complex-refactor --model opus | tail -1)

# 2. Verify the model was set correctly
.claude/skills/claude-worktree-manager/scripts/verify-worktree-model.sh "$WORKTREE_PATH"
# Expected output: [SUCCESS] Model is valid: opus

# 3. If in Ghostty, open new tab with Claude
if [ "$TERM_PROGRAM" = "ghostty" ]; then
    ghostty-tab -d "$WORKTREE_PATH" --no-enter "claude 'Refactor the project to support multi-tenant architecture'"
fi
```

User: "Create a worktree for quick bug fixes using Haiku"

```bash
# 1. Create the worktree with Haiku model
WORKTREE_PATH=$(.claude/skills/claude-worktree-manager/scripts/worktree.sh create quick-fixes --model haiku | tail -1)

# 2. Verify the model was set correctly
.claude/skills/claude-worktree-manager/scripts/verify-worktree-model.sh "$WORKTREE_PATH"

# 3. Start working in the worktree
cd "$WORKTREE_PATH"
claude 'Fix critical bugs'
```

User: "Create an Opus worktree with isolated database for migration testing"

```bash
# 1. Create worktree with both flags
WORKTREE_PATH=$(.claude/skills/claude-worktree-manager/scripts/worktree.sh create schema-testing --isolated --model opus | tail -1)

# 2. Verify model configuration (database seeding runs in parallel)
.claude/skills/claude-worktree-manager/scripts/verify-worktree-model.sh "$WORKTREE_PATH"
# Output should show: [SUCCESS] Model is valid: opus

# 3. Check database seeding progress (runs after pnpm install)
tail -f "$WORKTREE_PATH/.db-seed.log"

# 4. Once ready, navigate to worktree and start Claude
cd "$WORKTREE_PATH"
claude 'Test database migrations'
```

### Create worktree for bug fix

User: "I need a worktree to fix the login redirect issue"

```bash
# 1. Create the worktree and capture path
WORKTREE_PATH=$(.claude/skills/claude-worktree-manager/scripts/worktree.sh create fix-login-redirect | tail -1)

# 2. If in Ghostty, open new tab with Claude
if [ "$TERM_PROGRAM" = "ghostty" ]; then
    ghostty-tab -d "$WORKTREE_PATH" --no-enter "claude 'Fix the login redirect issue'"
fi
```

### Create worktree for refactoring

User: "Create a new worktree for refactoring the project to make it multi-tenant"

```bash
# 1. Create the worktree and capture path
WORKTREE_PATH=$(.claude/skills/claude-worktree-manager/scripts/worktree.sh create multi-tenant-refactor | tail -1)

# 2. If in Ghostty, open new tab with Claude
if [ "$TERM_PROGRAM" = "ghostty" ]; then
    ghostty-tab -d "$WORKTREE_PATH" --no-enter "claude 'Refactor the project to support multi-tenant architecture'"
fi
```

### Create worktree with isolated database

User: "I need a worktree to test new database migrations"

```bash
# 1. Create the worktree with isolated DB and capture path
WORKTREE_PATH=$(.claude/skills/claude-worktree-manager/scripts/worktree.sh create test-migrations --isolated | tail -1)

# 2. If in Ghostty, open new tab with Claude
if [ "$TERM_PROGRAM" = "ghostty" ]; then
    ghostty-tab -d "$WORKTREE_PATH" --no-enter "claude 'Test new database migrations in isolated environment'"
fi
```

### Create worktree for schema changes

User: "Create a worktree for adding new agent tables"

```bash
# 1. Create the worktree with isolated DB and capture path
WORKTREE_PATH=$(.claude/skills/claude-worktree-manager/scripts/worktree.sh create add-agent-tables --isolated | tail -1)

# 2. If in Ghostty, open new tab with Claude
if [ "$TERM_PROGRAM" = "ghostty" ]; then
    ghostty-tab -d "$WORKTREE_PATH" --no-enter "claude 'Add new agent tables to the database schema'"
fi
```

### List all worktrees

User: "Show me all my worktrees"

```bash
.claude/skills/claude-worktree-manager/scripts/worktree.sh list
```

### Cleanup old worktrees

User: "Clean up worktrees older than 3 days"

```bash
.claude/skills/claude-worktree-manager/scripts/worktree.sh cleanup --days 3
```
