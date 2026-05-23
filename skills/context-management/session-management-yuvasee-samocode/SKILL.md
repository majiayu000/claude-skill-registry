---
name: session-management
description: Manage work sessions with creation, loading, syncing, and archiving capabilities.
---

# Session Management

Manages work sessions. Session paths must be explicitly provided or known from context.

## Session Path Resolution

**IMPORTANT:** Sessions do NOT have a default location. The session path must be:
1. Provided explicitly in arguments (e.g., `start ~/projects/my-project/_sessions/session-name`)
2. Already known from conversation context (active session in working memory)
3. Defined in project's `.samocode` file under `SESSIONS` path

If session path cannot be determined: **STOP and ask the user** for the session location.

**Finding `.samocode`:** Look in current working directory (where Claude was started). Never guess paths - if `.samocode` not found, ask user.

## Repository Resolution

**IMPORTANT:** All git operations (fetch, branch creation, worktree management) MUST run from the correct repository directory.

1. Read `.samocode` from CWD — use `MAIN_REPO` value as the repo directory for all git commands
2. If `.samocode` not found or `MAIN_REPO` not set: fall back to `git rev-parse --show-toplevel` from CWD
3. **Never run git branch/worktree/fetch commands from CWD directly** — always resolve and use the repo directory first
4. Store the resolved repo path alongside the session for use in all actions

## Actions

Use `$ARGUMENTS` to specify action and parameters:
- `start [session-path/name]` - Create new session
- `continue [session-name-pattern]` - Load existing session
- `sync` - Sync current conversation to active session
- `archive [session-name-pattern]` - Archive a session

## Action: start

Create a new work session.

### Steps

1. **Resolve session location:**
   - If full path provided in arguments: use it
   - If only name provided: read `.samocode` from current working directory, use `SESSIONS` path
   - **If `.samocode` not found: STOP and ask user** - never guess or create arbitrary folders

2. **Parse session name:**
   - Take session name from arguments after "start"
   - If empty, ERROR: "Session name required. Usage: start [session-name]"
   - Sanitize name (lowercase, replace spaces with hyphens)

3. **Create session folder:**
   - Path: `[SESSIONS_DIR]/[YY-MM-DD]-[session-name]/` (use current date for folder name)
   - If folder exists, ERROR: "Session already exists"

4. **Create worktree (if `.samocode` has WORKTREES):**

   Read `MAIN_REPO` and `WORKTREES` from `.samocode`. If both are set, create a worktree:

   ```bash
   # Derive branch name: strip date prefix from session folder name
   # e.g., "26-02-05-my-feature" -> "my-feature"
   BRANCH_NAME=[session-name]  # the name before date-prefixing
   # If GIT_BRANCH_PREFIX env var is set, prepend it: [prefix]/[branch-name]

   # Fetch and detect default branch
   cd [MAIN_REPO]
   git fetch origin
   DEFAULT_BRANCH=$(git remote show origin | grep 'HEAD branch' | cut -d: -f2 | xargs)

   # Create worktree from remote default branch
   git worktree add -b [BRANCH_NAME] [WORKTREES]/[YY-MM-DD]-[session-name] origin/$DEFAULT_BRANCH
   ```

   If worktree creation fails (branch already exists), try attaching to existing branch:
   ```bash
   git worktree add [WORKTREES]/[YY-MM-DD]-[session-name] [BRANCH_NAME]
   ```

   **Working Dir** = `[WORKTREES]/[YY-MM-DD]-[session-name]`

   **If WORKTREES not set** (non-repo project): fall back to `MAIN_REPO`, or `git rev-parse --show-toplevel`, or current directory.

5. **Create _overview.md:**
   ```markdown
   # Session: [session-name]
   Started: [TIMESTAMP_LOG]
   Working Dir: [worktree-path or fallback]

   ## Status
   Phase: investigation
   Iteration: 1
   Blocked: no
   Last Action: Session created
   Next: Ready to work

   ## Flow Log
   - [TIMESTAMP_ITERATION] Session created

   ## Files
   (none yet)

   ## Plans
   (none yet)

   ## Linear Tasks
   (none yet)
   ```

6. **Commit (if sessions dir is a git repo):**
   - `cd [SESSIONS_DIR] && git add . && git commit -m "Start session: [session-name]"`

7. **Confirm to user:**
   ```
   Session created: [YY-MM-DD]-[session-name]
   Path: [full-path]
   Working Dir: [worktree-path or fallback]
   Branch: [BRANCH_NAME]

   IMPORTANT: This is now your active session. Remember this path for subsequent commands.

   Ready to work. Use /dive, /task, or /create-plan to continue.
   ```

IMPORTANT: After creating the session, keep the session path in your working memory for all subsequent session-aware commands.

## Action: continue

Load and continue working in an existing session.

### Steps

1. **Resolve session location:**
   - If full path provided: use it
   - Check project `.samocode` file for `SESSIONS` path
   - If not found: **STOP and ask user** for sessions directory

2. **Find matching sessions:**
   - Search sessions directory for folders matching `*$ARGUMENTS*` (exclude _archive/)
   - Sort by modification time (most recent first)

3. **Handle results:**
   - **No matches:** ERROR: "No sessions found matching '$ARGUMENTS'. Use start action to create one."
   - **One match:** Proceed to load
   - **Multiple matches:** List them with dates and ask user to specify

4. **Load session:**
   - Read `_overview.md` from the session folder
   - Add Flow Log entry: `- [TIMESTAMP_ITERATION] Session resumed`
   - Commit if git repo: `git add . && git commit -m "Resume session: [session-name]"`

5. **Present summary:**
   ```
   Session: [session-name]
   Path: [full-path]
   Working Dir: [from _overview.md]
   Started: [date]

   Recent Activity:
   [Last 5-10 Flow Log entries]

   Files: [count]
   [List with brief descriptions]

   Plans: [list if any]
   Linear Tasks: [list if any]

   ---
   Session loaded. Ready to continue.
   ```

IMPORTANT: After loading, keep the session path in your working memory for all subsequent session-aware commands.

## Action: sync

Ensure all work from this conversation is recorded in the active session.

### Steps

1. **Check for active session:**
   - If no session in working memory: ERROR: "No active session. Use continue action to load one first."

2. **Read current session state:**
   - Read `[SESSION_PATH]/_overview.md`

3. **Review conversation for unrecorded work:**
   - Code changes (files created, modified, deleted)
   - Decisions made
   - Problems solved
   - Discoveries about the codebase
   - Commits made
   - Blockers/TODOs remaining

4. **Update _overview.md:**
   - Add missing Flow Log entries
   - Add missing Files entries
   - Update other sections as needed

5. **Create detail files if warranted:**
   - Only for complex topics that need more than a log entry

6. **Commit (if git repo):**
   - `cd [SESSION_DIR] && git add . && git commit -m "Sync session: [session-name]"`

7. **Extract learnings:**
   - If the conversation contained friction moments (failed approaches, workarounds discovered): you MUST use "learn" skill now.
   - If nothing notable was learned: skip

8. **Report:**
   - "Session synced: [what was added]"
   - Or: "Session already up to date."

## Action: archive

Archive a session (full) or archive work within a session (partial).

### Usage Patterns

1. `archive` - Archive entire active session (moves folder to _archive/)
2. `archive [session-name]` - Archive entire named session
3. `archive keep file1.md file2.md` - Archive work files within session, keep specified files
4. `archive [session-path] keep file1.md` - Archive work in specific session, keep files

### Full Archive (no "keep" keyword)

#### Session Resolution

1. **If arguments after "archive" are empty:**
   - Check for active session in working memory
   - If no active session: ERROR: "No active session and no session name provided."
   - Use active session path

2. **If arguments provided (no "keep"):**
   - Search sessions directory for folders matching `*$ARGUMENTS*` (exclude _archive/)
   - **No matches:** ERROR: "No sessions found matching '$ARGUMENTS'"
   - **One match:** Confirm with user: "Archive session [name]? (y/n)"
   - **Multiple matches:** List and ask user to specify

#### Full Archive Process

1. **Get session info:**
   - Read `[SESSION_PATH]/_overview.md`
   - Extract Working Dir line

2. **Create archive folder if needed:**
   ```bash
   mkdir -p [SESSIONS_DIR]/_archive
   ```

3. **Remove worktree (if applicable):**
   - If Working Dir contains `/worktrees/`:
     - Resolve `MAIN_REPO` from `.samocode` (see "Repository Resolution" section)
     - Run worktree removal from `MAIN_REPO` directory:
       ```bash
       cd "$MAIN_REPO" && git worktree remove [working_dir_path]
       ```
   - If removal fails (uncommitted changes), warn user and ask to proceed or abort
   - Note: Branch is preserved, only worktree removed

4. **Move session folder:**
   ```bash
   mv [SESSION_PATH] [SESSIONS_DIR]/_archive/
   ```

5. **Commit changes (if git repo):**
   - `cd [SESSIONS_DIR] && git add . && git commit -m "Archive session: [session-name]"`

6. **Clear active session** (if archiving active session):
   - Remove from working memory

7. **Extract learnings:**
   - If the conversation contained friction moments (failed approaches, workarounds discovered): you MUST use "learn" skill now.
   - If nothing notable was learned: skip

8. **Confirm to user:**
   ```
   Session archived: [session-name]
   Moved to: [archive-path]
   Worktree removed: [path] (branch preserved)

   Session closed.
   ```

### Partial Archive (with "keep" keyword)

Archives completed work within a session while keeping important deliverables accessible.

#### Argument Parsing

1. Split arguments on "keep" keyword
2. Before "keep": session path (optional, defaults to active session)
3. After "keep": list of files to keep in place (space-separated)

Example: `archive keep competitor-analysis.md` → archive active session, keep competitor-analysis.md

#### Partial Archive Process

1. **Resolve session:**
   - If path before "keep": use it
   - Otherwise: use active session from working memory
   - ERROR if no session found

2. **Get timestamp and slug:**
   ```bash
   TIMESTAMP_FOLDER=$(date '+%y-%m-%d')
   ```
   - Extract slug from session folder name or task name from _overview.md
   - Archive folder: `[SESSION_PATH]/_archive/[YY-MM-DD]-[slug]/`

3. **Create archive subfolder:**
   ```bash
   mkdir -p [SESSION_PATH]/_archive/[YY-MM-DD]-[slug]
   ```

4. **Identify files to archive:**
   - All `.md` files in session root EXCEPT:
     - `_overview.md` (always kept - session state)
     - `_qa.md` (always kept if exists)
     - `_signal.json` (always kept)
     - Files listed after "keep" keyword
   - All timestamped files (pattern: `[MM-DD-HH:mm]-*.md`)

5. **Move files to archive:**
   ```bash
   for file in [files_to_archive]; do
     mv "$file" [SESSION_PATH]/_archive/[YY-MM-DD]-[slug]/
   done
   ```

6. **Update _overview.md:**
   - Add Flow Log entry: `- [TIMESTAMP_LOG] Archived work to _archive/[YY-MM-DD]-[slug]/, kept: [kept_files]`
   - Reset Status section for next task

7. **Extract learnings:**
   - If the conversation contained friction moments (failed approaches, workarounds discovered): you MUST use "learn" skill now.
   - If nothing notable was learned: skip

8. **Report to user:**
   ```
   Work archived within session.
   Archived to: [SESSION_PATH]/_archive/[YY-MM-DD]-[slug]/
   Files moved: [count] files
   Kept in place: [kept_files]
   ```
