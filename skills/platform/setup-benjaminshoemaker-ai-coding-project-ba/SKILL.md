---
name: setup
description: Initialize a new project with the AI Coding Toolkit. Use when setting up toolkit skills in a new or existing project.
argument-hint: [target-directory]
allowed-tools: Bash, Read, Write, AskUserQuestion
toolkit-only: true
---

Initialize a new project at `$1` with the AI Coding Toolkit.

## Steps

0. **Directory guard (must run from toolkit repo)**
   - Confirm `START_PROMPTS.md` and `GENERATOR_PROMPT.md` exist in the current working directory
   - If either is missing, **STOP** and tell the user to `cd` into the `ai_coding_project_base` toolkit repo and re-run `/setup $1`

0.5. **Idempotency Check**

   Check if target already has toolkit installed:

   ```bash
   if [[ -f "$1/.claude/toolkit-version.json" ]]; then
     EXISTING_COMMIT=$(jq -r '.toolkit_commit' "$1/.claude/toolkit-version.json")
     CURRENT_COMMIT=$(git rev-parse HEAD)
   fi
   ```

   Decision logic:
   - If `toolkit-version.json` doesn't exist → proceed with **full setup** (existing flow)
   - If exists and `toolkit_commit` = current HEAD → report "Already up to date" and skip to Step 7 (success report)
   - If exists and `toolkit_commit` ≠ current HEAD → proceed with **incremental update** (Step 3a)

   Store the result as `SETUP_MODE`:
   - `SETUP_MODE=full` — new installation
   - `SETUP_MODE=current` — already up to date
   - `SETUP_MODE=incremental` — updating existing installation

1. **Validate target directory**
   - If `$1` is empty, ask the user for the target directory path
   - Check if the directory exists; if not, offer to create it

2. **Ask project type**
   - Greenfield: Starting a new project from scratch
   - Feature: Adding a feature to an existing project

2a. **For Feature type: Ask feature name and create directory**
    - Prompt: "What should this feature be called? (used as folder name, e.g., 'analytics-dashboard')"
    - Validate: lowercase, hyphens and underscores allowed, no spaces or special characters
    - Create `$1/features/` directory if it doesn't exist
    - Create `$1/features/<feature-name>/` directory
    - Store the feature path as `FEATURE_PATH` = `$1/features/<feature-name>`

3. **Copy skills to target (with global resolution check)**

   Before copying each skill, check if it's globally available. See [GLOBAL_SYNC.md](../update-target-projects/GLOBAL_SYNC.md) for helper definitions.

   **Pre-copy checks:**
   ```bash
   # Source the global sync helpers
   GLOBAL_SKILLS_DIR="$HOME/.claude/skills"
   TOOLKIT_ROOT="$(pwd)"

   # Check if global directory exists and has symlinks
   GLOBAL_AVAILABLE=false
   if [[ -d "$GLOBAL_SKILLS_DIR" ]]; then
     # Count symlinks pointing to this toolkit
     SYMLINK_COUNT=$(find "$GLOBAL_SKILLS_DIR" -maxdepth 1 -type l 2>/dev/null | wc -l)
     if [[ "$SYMLINK_COUNT" -gt 0 ]]; then
       GLOBAL_AVAILABLE=true
     fi
   fi
   ```

   **Copy logic with global resolution:**
   ```bash
   GLOBAL_COUNT=0
   LOCAL_COUNT=0

   for skill_dir in .claude/skills/*/; do
     skill_name="$(basename "$skill_dir")"

     # Check for toolkit-only flag in YAML frontmatter (between --- markers)
     if sed -n '/^---$/,/^---$/p' "$skill_dir/SKILL.md" 2>/dev/null | grep -q '^toolkit-only: true'; then
       continue  # Skip toolkit-only skills
     fi

     # Check if this skill is globally usable
     if [[ "$GLOBAL_AVAILABLE" == "true" ]]; then
       global_path="$GLOBAL_SKILLS_DIR/$skill_name"
       if [[ -L "$global_path" && -e "$global_path" ]]; then
         # Verify it points to this toolkit
         resolved=$(realpath "$global_path" 2>/dev/null)
         expected=$(realpath "$skill_dir" 2>/dev/null)
         if [[ "$resolved" == "$expected" ]]; then
           echo "  $skill_name — globally available"
           ((GLOBAL_COUNT++))
           continue  # Skip copy, will resolve via global
         fi
       fi
     fi

     # Copy locally
     cp -r "$skill_dir" "$1/.claude/skills/"
     echo "  $skill_name — copied locally"
     ((LOCAL_COUNT++))
   done
   ```

   **Summary output:**
   - If all skills are global: `"All skills resolved via ~/.claude/skills/ — no local copies needed"`
   - If mixed: `"Skills: {GLOBAL_COUNT} global, {LOCAL_COUNT} local"`
   - If all local: `"Copied {LOCAL_COUNT} skills to project"`

   Copy verification config (if missing):
   - `.claude/verification-config.json` → target's `.claude/verification-config.json`

   **Verify result:**
   ```bash
   # For local-only or mixed: verify local copies exist
   if [[ "$LOCAL_COUNT" -gt 0 ]]; then
     actual_count=$(ls -d "$1/.claude/skills/"*/ 2>/dev/null | wc -l)
     if [[ "$actual_count" -eq 0 ]]; then
       # STOP and report copy failure
     fi
   fi
   ```

   Also verify configuration file:
   ```bash
   test -f "$1/.claude/verification-config.json" && echo "Config: OK" || echo "Config: MISSING (non-critical)"
   ```

3b. **Copy workstream scripts to target**

   Copy `.workstream/` scripts from the toolkit to the target project:

   ```bash
   mkdir -p "$1/.workstream"
   for file in lib.sh setup.sh dev.sh verify.sh README.md workstream.json.example; do
     if [ -f ".workstream/$file" ]; then
       cp ".workstream/$file" "$1/.workstream/$file"
     fi
   done
   chmod +x "$1/.workstream/"*.sh 2>/dev/null || true
   ```

   **Do NOT copy `workstream.json`** — this is project-owned and created by the user.

   **Verify copies:**
   ```bash
   ls -la "$1/.workstream/" 2>/dev/null
   ```
   Confirm `setup.sh`, `dev.sh`, `verify.sh`, and `lib.sh` exist and are executable.

3c. **Copy Codex App templates to target**

   Copy `.codex/` templates from the toolkit to the target project:

   ```bash
   mkdir -p "$1/.codex"
   cp ".codex/setup.sh" "$1/.codex/setup.sh"
   cp ".codex/AGENTS.md" "$1/.codex/AGENTS.md"
   chmod +x "$1/.codex/setup.sh"
   ```

   These are recommended defaults for Codex App integration. Users configure
   the setup script in Codex App Settings (Cmd+,) → Local Environments.

3a. **Incremental Sync (When SETUP_MODE=incremental)**

   Skip Step 3 entirely and use this incremental approach instead.

   **Check resolution mode from existing config:**
   ```bash
   FORCE_LOCAL=$(jq -r '.force_local_skills // empty' "$1/.claude/toolkit-version.json")
   CURRENT_RESOLUTION=$(jq -r '.skill_resolution // "local"' "$1/.claude/toolkit-version.json")
   ```

   **Important:** For existing projects with local copies, continue syncing locally
   to preserve shadowing behavior. Do NOT automatically switch to global resolution.

   Load the stored file hashes from `$1/.claude/toolkit-version.json`:
   ```bash
   STORED_HASHES=$(jq '.files' "$1/.claude/toolkit-version.json")
   ```

   For each skill in the copy list (excluding toolkit-only skills — check `SKILL.md` frontmatter for `toolkit-only: true`):

   1. Calculate toolkit file hash:
      ```bash
      TOOLKIT_HASH=$(shasum -a 256 "$TOOLKIT_FILE" | cut -d' ' -f1)
      ```

   2. Get stored hash from toolkit-version.json (hash at last sync)

   3. Calculate target file hash (if exists):
      ```bash
      TARGET_HASH=$(shasum -a 256 "$TARGET_FILE" | cut -d' ' -f1)
      ```

   **Classification and Action:**

   | Condition | Classification | Action |
   |-----------|----------------|--------|
   | Already using global resolution | `GLOBAL_USABLE` | Skip (resolves via global) |
   | Target doesn't exist | `NEW` | Copy from toolkit |
   | Target hash = Toolkit hash | `CURRENT` | Skip (already up to date) |
   | Target hash = Stored hash | `CLEAN_UPDATE` | Copy from toolkit (no local changes) |
   | Target hash ≠ Stored hash | `LOCAL_MODIFIED` | Skip with warning |

   Track counts for each classification and report summary:
   ```
   INCREMENTAL SYNC
   ================
   Global resolution: {count} skills (via ~/.claude/skills)
   New files:         {count} copied
   Updated files:     {count} copied
   Current files:     {count} skipped (already up to date)
   Modified files:    {count} skipped (local changes preserved)
   ```

   If any files are `LOCAL_MODIFIED`, list them:
   ```
   WARNING: These files have local modifications and were NOT updated:
   - .claude/skills/phase-start/SKILL.md
   - .claude/skills/fresh-start/SKILL.md

   To update these files, either:
   - Run /sync for interactive conflict resolution
   - Manually backup and delete them, then re-run /setup
   ```

4. **Create or Update toolkit-version.json**

   **For full setup (SETUP_MODE=full):**

   Create `.claude/toolkit-version.json` in the target to enable future syncs.
   Determine the resolution mode based on how skills were installed:

   ```json
   {
     "schema_version": "1.1",
     "toolkit_location": "{absolute path to this toolkit}",
     "toolkit_commit": "{current git HEAD commit hash}",
     "toolkit_commit_date": "{commit date in ISO format}",
     "last_sync": "{current ISO timestamp}",
     "force_local_skills": null,
     "skill_resolution": "{global|local|mixed}",
     "files": {
       ".claude/skills/fresh-start/SKILL.md": {
         "hash": "{sha256 hash of file}",
         "synced_at": "{ISO timestamp}",
         "resolution": "{global|local}"
       }
       // ... entry for each skill
     }
   }
   ```

   **Resolution determination:**
   - If `GLOBAL_COUNT > 0` and `LOCAL_COUNT == 0`: `"skill_resolution": "global"`
   - If `GLOBAL_COUNT == 0` and `LOCAL_COUNT > 0`: `"skill_resolution": "local"`
   - If both > 0: `"skill_resolution": "mixed"`

   **Per-file resolution:**
   - Skills that were skipped (globally available): `"resolution": "global"`
   - Skills that were copied: `"resolution": "local"`

   **For incremental update (SETUP_MODE=incremental):**

   Update the existing `toolkit-version.json`:
   - Update `toolkit_commit` to current HEAD
   - Update `toolkit_commit_date` to current commit date
   - Update `last_sync` to current timestamp
   - Preserve `force_local_skills` setting
   - For each file that was copied (NEW or CLEAN_UPDATE):
     - Update the file's `hash`, `synced_at`, and `resolution`
   - Keep existing entries for files that were skipped (CURRENT or LOCAL_MODIFIED)
   - Recalculate `skill_resolution` based on all files

   **For already current (SETUP_MODE=current):**

   Skip this step entirely.

   **Get toolkit info:**
   ```bash
   TOOLKIT_PATH=$(pwd)
   COMMIT_HASH=$(git rev-parse HEAD)
   COMMIT_DATE=$(git log -1 --format=%cI HEAD)
   ```

   **Calculate file hashes:**
   ```bash
   shasum -a 256 "$file" | cut -d' ' -f1
   ```

   **Include entries for ALL files in non-toolkit-only skill directories:**
   ```bash
   # Hash every .md file in every skill directory (skip toolkit-only)
   for skill_dir in .claude/skills/*/; do
     # Skip toolkit-only skills (parse YAML frontmatter between --- markers)
     if sed -n '/^---$/,/^---$/p' "$skill_dir/SKILL.md" 2>/dev/null | grep -q '^toolkit-only: true'; then
       continue
     fi
     for file in "$skill_dir"*.md; do
       [[ -f "$file" ]] || continue
       hash=$(shasum -a 256 "$file" | cut -d' ' -f1)
       # Add entry for "$file" with hash and timestamp
     done
   done
   ```

   This ensures skills with supporting files (e.g., `audit-skills/CRITERIA.md`,
   `audit-skills/SCORING.md`) are tracked for conflict detection.

   **Skills with `toolkit-only: true` in frontmatter are NOT copied or tracked.**
   These run only from the toolkit directory (e.g., setup, update-target-projects).

5. **Create CLAUDE.md if it doesn't exist**

   Create a minimal CLAUDE.md that references AGENTS.md:
   ```
   @AGENTS.md
   ```

6. **Codex CLI Detection (Optional)**

   Check if OpenAI Codex CLI is installed:
   ```bash
   command -v codex >/dev/null 2>&1
   ```

   If Codex is detected:
   - Use AskUserQuestion to prompt:
     ```
     Question: "Codex CLI detected. Install toolkit skills for Codex?"
     Options:
       - "Yes, install" — Install skills via symlink (auto-updates with toolkit)
       - "No, skip" — Don't install Codex skills
     ```

   If user selects "Yes, install":
   - Run from this toolkit directory:
     ```bash
     ./scripts/install-codex-skill-pack.sh --method symlink
     ```
   - Report the installation result

   If Codex is not detected:
   - Skip silently (don't mention Codex to users who don't have it)

   **Note:** Using symlinks means Codex skills auto-update when user runs `git pull` on the toolkit.

6a. **Codex MCP Configuration (if Codex detected and skills installed)**

   After installing Codex skills, offer to configure essential MCPs:
   - Use AskUserQuestion to prompt:
     ```
     Question: "Configure essential MCP servers for Codex? (Playwright for browser verification)"
     Options:
       - "Yes, configure" — Add Playwright MCP to ~/.codex/config.toml
       - "No, skip" — Skip MCP configuration
     ```

   If user selects "Yes, configure":
   - Run from this toolkit directory:
     ```bash
     ./scripts/configure-codex-mcp.sh
     ```
   - Report the configuration result

   **Why this matters:** Both Claude Code and Codex CLI support the same MCP protocol.
   This ensures Codex has access to browser automation for verification workflows,
   matching Claude Code's capabilities when using the Playwright MCP.

7. **Report success and next steps**

   **For SETUP_MODE=current (already up to date):**
   ```
   ALREADY UP TO DATE
   ==================
   Target: $1
   Toolkit commit: {COMMIT_HASH} ({COMMIT_DATE})

   No changes needed — toolkit files are current.
   ```

   **For SETUP_MODE=incremental (updated existing):**
   ```
   TOOLKIT UPDATED
   ===============
   Target: $1
   Previous commit: {OLD_COMMIT_HASH}
   Current commit:  {COMMIT_HASH}

   {Summary from Step 3a showing files synced/skipped}

   All toolkit skills are now up to date.
   ```

   **For SETUP_MODE=full, Greenfield:**
   ```
   TOOLKIT INITIALIZED
   ===================
   Target: $1
   Skill resolution: {mode} ({details})

   Next steps (run from THIS toolkit directory):
   1. /product-spec $1
   2. /technical-spec $1
   3. /generate-plan $1

   Then switch to your project:
   4. cd $1
   5. /fresh-start
   6. /configure-verification
   7. /phase-prep 1
   8. /phase-start 1
   ```

   **Skill resolution line examples:**
   - `Skill resolution: global (30 skills via ~/.claude/skills symlinks)`
   - `Skill resolution: local (30 skills copied to project)`
   - `Skill resolution: mixed (25 global, 5 local)`

   **For SETUP_MODE=full, Feature:**
   ```
   TOOLKIT INITIALIZED
   ===================
   Target: $1
   Feature directory: FEATURE_PATH

   Next steps (run from your project directory):
   1. cd $1
   2. /feature-spec <feature-name>
   3. /feature-technical-spec <feature-name>
   4. /feature-plan <feature-name>
   5. /fresh-start
   6. /configure-verification
   7. /phase-prep 1
   8. /phase-start 1

   After phase completion, merge AGENTS_ADDITIONS.md into $1/AGENTS.md
   ```

## Important

- This skill must be run from the ai_coding_project_base toolkit directory
- Project-level generation skills (`/product-spec`, `/technical-spec`, `/generate-plan`) run from toolkit
- Feature skills (`/feature-spec`, `/feature-technical-spec`, `/feature-plan`) run from the target project
- Execution skills run from target
- Use `cp -r` for directory copies to preserve structure
- Do not overwrite existing files without asking

## When Setup Cannot Complete

**If LOCAL_MODIFIED files conflict during incremental sync:**
- List all conflicting files with their local vs toolkit versions
- Ask user: "Keep local changes, overwrite with toolkit, or diff each file?"
- If "Keep local": Skip those files, complete rest of sync, warn about version mismatch
- If "Overwrite": Back up local files to `.claude/backup/` before overwriting
- If "Diff each": Show side-by-side diff, let user choose per file

**If target directory doesn't exist and can't be created:**
- Report: "Cannot create directory: {path}"
- Check parent directory permissions
- Suggest: Create manually with `mkdir -p {path}`
- Exit cleanly without partial state

**If Codex CLI skill installation fails:**
- Do NOT fail the entire setup
- Report: "Codex skill installation failed: {error}"
- Continue with rest of setup
- Note at end: "Codex skills not installed. Run `./scripts/install-codex-skill-pack.sh` manually."

**If toolkit-version.json cannot be written:**
- Report: "Cannot write toolkit-version.json"
- Complete the file copies (primary goal)
- Warn: "Future incremental syncs will not work until version file is created"
- Suggest: Check .claude/ directory permissions
