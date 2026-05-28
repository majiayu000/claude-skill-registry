---
name: task-wrapup
description: Comprehensive work session wrap-up orchestrator that generates summaries, sends notifications across multiple channels (email, SMS, Slack), logs work time, and updates project documentation
category: productivity
version: 1.0.0
---

# Task Wrap-Up Skill

**Comprehensive work session wrap-up orchestrator** for professional project communication and record-keeping.

## Purpose

Automate end-of-session workflows by:
- Generating intelligent work summaries from git commits, todos, and file changes
- Sending notifications to stakeholders via email, SMS, and Slack
- Logging billable hours to worklog system
- Updating project documentation
- Optional calendar and GitHub integration

## When to Use

Trigger this skill when:
- Ending a work session and need to communicate progress
- Completing a feature or milestone
- Wrapping up before context switch to different project
- Need to bill time and update stakeholders simultaneously
- Keywords: "wrap up", "end session", "send update", "log work"

## Core Workflow

### Phase 1: Configuration Check
1. **Check for config file**: Look for `.task_wrapup_skill_data.json` in current working directory
2. **Create if missing**: If not found, prompt user for:
   - Project name
   - Email recipients (first name, last name, email address)
   - SMS recipients (first name, last name, phone number)
   - Slack channel (optional)
   - Worklog settings
3. **Validate config**: Ensure all required fields present and properly formatted

### Phase 2: Summary Generation
1. **Analyze work session**:
   - Git commits from last 12 hours
   - File changes and statistics
   - TodoWrite completed tasks (if available)
   - Serena session memory (if available)
2. **Generate summaries**:
   - **Full summary**: Detailed description for email and Slack
   - **Concise summary**: Brief version for SMS and worklog (≤300 chars)
3. **User override**: Allow user to provide custom summary text instead

### Phase 3: Preview & Confirmation
1. **Display preview**:
   - Show generated summary content
   - Display distribution plan (who gets what)
   - List all configured channels and their status

2. **🚨 CRITICAL: ASK THESE FOUR QUESTIONS EVERY TIME** (Non-negotiable, always required):

   These questions MUST be asked in EVERY task-wrapup execution, before proceeding to Phase 4:

   **Question 1 - Git Commit:**
   ```
   Would you like to commit changes to git before sending notifications? (y/n)

   This will create a commit with:
   - All uncommitted changes in working directory
   - Commit message based on session summary
   - Timestamp and completion marker
   ```

   **Question 2 - Create Pull Request:**
   ```
   Would you like to create a pull request for this feature branch? (y/n)

   This will:
   - Push feature branch to remote repository
   - Create pull request targeting parent branch (from session state)
   - Use session summary as PR description
   - Optionally checkout parent branch after creation
   - Automatically clean up session state file

   Note: Requires .task_session_state.json file from task-start skill.
         If session state is missing, will use default parent branch.
   ```

   **Question 3 - Calendar:**
   ```
   Would you like to create a calendar event or reminder? (y/n)

   Options:
   - Create event for deliverable/milestone
   - Set reminder for follow-up tasks
   - Schedule next work session
   ```

   **Question 4 - GitHub:**
   ```
   Would you like to create a GitHub issue or release notes? (y/n)

   Options:
   - Create issue for follow-up work
   - Draft release notes for version
   - Update existing issue with session notes
   ```

   **ENFORCEMENT RULES:**
   - ✅ Ask ALL FOUR questions EVERY TIME
   - ✅ Ask even if user said "continue without questions" (these are decision points, not clarifications)
   - ✅ Ask even if config has features disabled
   - ✅ Ask even if user didn't mention them
   - ✅ Ask even if user previously declined
   - ❌ NEVER skip these questions to "save time"
   - ❌ NEVER assume the answer is "no"
   - ❌ NEVER proceed to Phase 4 without explicit answers

   **PURPOSE:** These serve as critical checkpoints to ensure:
   - Work is properly committed to version control
   - Pull requests created for feature branches
   - Important dates/deadlines are calendared
   - Follow-up work is tracked in GitHub

   Default to "no" only if user explicitly declines each question.

3. **Confirmation options** (AFTER the four mandatory questions):
   - [1] Send as-is
   - [2] Edit summary
   - [3] Customize per channel (different content for email vs SMS vs Slack)
   - [4] Modify distribution (enable/disable channels)
   - [5] Cancel operation

4. **Handle user choice**: Process edits and modifications as requested

### Phase 4: Parallel Dispatch
Execute notifications **in parallel** for speed:

**Email** (via `@~/.claude/skills/email/SKILL.md`):
- Send to all recipients as group email
- Uses seasonal HTML formatting
- Includes full summary with detail
- Automatic BCC to arlenagreer@gmail.com for multi-recipient

**SMS** (via `@~/.claude/skills/text-message/SKILL.md`):
- Send **individual messages** to each recipient (NEVER group text)
- Uses **natural, humanized style** - like sending a quick progress note to a colleague
- Tone: Friendly, professional, conversational but concise (≤320 chars)
- Think: "Just finished up X, got Y done, moving on to Z" not "Completed: X. Achieved: Y."
- Removes apostrophes for AppleScript compatibility

**SMS Style Examples**:
```
❌ Sterile: "Completed infrastructure modernization. Dependencies upgraded Ruby 3.4, Node 25. Fixed production deployment issues. Database migrations implemented."

✅ Natural: "Just wrapped up infrastructure work - upgraded to Ruby 3.4 and Node 25, fixed the production deployment blockers, and got database migrations sorted. Good progress today!"

❌ Sterile: "Implemented task coverage. Created 36 test files. Achieved 90% coverage target."

✅ Natural: "Finished the test coverage push - created 36 new test files and hit our 90% target. Feels good to have that wrapped up!"
```

**Slack** (if configured):
- Post to specified channel
- Uses full summary (same detail as email)
- Include @mentions if configured

**Worklog** (via `@~/.claude/skills/worklog/SKILL.md`):
- Create billable hours entry
- Uses concise summary as description
- **CRITICAL**: Check system clock for current date before logging
- Prompt for duration if configured, or use default
- Associate with project/client name from config

**Documentation** (via `/sc:document`):
- **Script Phase**: Creates documentation update request file (`.task_wrapup_doc_update_request.md`)
- **Claude Code Phase**: Detects request file and invokes `/sc:document` command
- **Updates**: CHANGELOG.md (session entry), README.md (affected sections), other configured paths
- **Strategy**: Uses smart_merge to intelligently integrate changes
- **Summary**: Documentation changes included in final wrap-up report

**Calendar** (optional, via `@~/.claude/skills/calendar/SKILL.md`):
- Only if user confirms during prompt (ALWAYS ask in Phase 3)
- Create calendar event or reminder
- **CRITICAL**: Be date-aware, check system clock

**GitHub** (optional, via `/sc:git`):
- Only if user confirms during prompt (ALWAYS ask in Phase 3)
- Create issue, PR, or release notes

**OmniFocus** (automatic, if configured):
- Completes OmniFocus task created during session startup
- Reads task ID from `.task_session_state.json`
- Marks task as complete via OmniFocus skill
- **CRITICAL**: Session lifecycle completion - tasks created at startup are automatically completed at wrapup
- Only runs if `omnifocus.auto_log_tasks` is enabled in config
- Skips gracefully if task ID not found in session state
- Non-blocking: continues even if completion fails

**Commit Changes** (optional):
- Only if user confirms during prompt (ALWAYS ask in Phase 3)
- Commit documentation updates to git
- Use descriptive commit message based on session summary

### Phase 5: Final Summary
Display comprehensive results:
- ✅ Success indicators for completed actions
- ❌ Error indicators with details for failures
- ⏭️ Skip indicators for disabled channels
- Summary statistics (total, successful, failed)
- Detailed error messages for troubleshooting

## Configuration Schema

Configuration stored in `.task_wrapup_skill_data.json` in project directory:

```json
{
  "schema_version": "1.0",
  "project_name": "MyProject",
  "created_at": "2025-01-15T10:30:00",
  "last_updated": "2025-01-15T10:30:00",

  "summary_generation": {
    "strategy": "hybrid",
    "sources": {
      "git_commits": true,
      "todo_tasks": true,
      "serena_memory": true,
      "file_changes": true
    },
    "intelligence": {
      "extract_key_decisions": true,
      "identify_blockers": true,
      "highlight_risks": true,
      "include_metrics": false
    }
  },

  "communication": {
    "email": {
      "enabled": true,
      "recipients": [
        {"first_name": "John", "last_name": "Doe", "email": "john@example.com"}
      ],
      "cc": [],
      "template": "professional",
      "include_attachments": false
    },
    "sms": {
      "enabled": true,
      "recipients": [
        {"first_name": "Jane", "last_name": "Smith", "phone": "+15551234567"}
      ],
      "max_length": 320,
      "critical_only": false
    },
    "slack": {
      "enabled": false,
      "channel": "",
      "mention_users": [],
      "thread_mode": "new_message"
    }
  },

  "worklog": {
    "enabled": true,
    "prompt_for_duration": true,
    "default_duration_minutes": null,
    "round_to_nearest": 15,
    "date_handling": {
      "prompt_for_date": false,
      "default": "today",
      "timezone": "America/New_York"
    }
  },

  "documentation": {
    "enabled": true,
    "auto_update": true,
    "paths": ["README.md"],
    "strategy": "smart_merge",
    "commit_changes": false
  },

  "pull_request": {
    "enabled": true,
    "default_parent_branch": "develop",
    "auto_checkout_parent": true,
    "cleanup_session_state": true,
    "draft": false,
    "title_template": null,
    "body_template": null
  },

  "optional_actions": {
    "calendar": {
      "enabled": false,
      "prompt_by_default": false
    },
    "github": {
      "enabled": false,
      "prompt_by_default": false
    }
  },

  "execution": {
    "preview_before_send": true,
    "parallel_execution": true,
    "max_retries": 3,
    "retry_delay_seconds": 5
  },

  "omnifocus": {
    "project_name": "Development",
    "auto_log_tasks": true,
    "prompt_if_missing": true
  }
}
```

### Pull Request Configuration

The `pull_request` section controls PR automation behavior:

- **`enabled`** (boolean, default: `true`): Enable/disable PR creation prompts during task wrapup
- **`default_parent_branch`** (string, default: `"develop"`): Fallback parent branch when session state unavailable
- **`auto_checkout_parent`** (boolean, default: `true`): Automatically checkout parent branch after successful PR creation
- **`cleanup_session_state`** (boolean, default: `true`): Delete `.task_session_state.json` after successful PR workflow
- **`draft`** (boolean, default: `false`): Create PRs as draft by default
- **`title_template`** (string|null, default: `null`): Custom PR title template (uses session summary if null)
- **`body_template`** (string|null, default: `null`): Custom PR body template (uses session summary if null)

**Session State Integration:**
- PR automation depends on `.task_session_state.json` created by task-start skill
- Session state contains: feature branch, parent branch, issue number, GitHub issue metadata
- If session state missing: Uses `default_parent_branch` for PR targeting
- Session state location: Project root directory
- Session state cleanup: Automatic after successful PR creation (configurable)

**Workflow:**
1. User confirms PR creation in Phase 3 Question 2
2. System reads `.task_session_state.json` for parent branch
3. Pushes feature branch to remote repository
4. Creates PR via GitHub CLI (`gh pr create`)
5. Uses session summary as PR description
6. Optionally checks out parent branch
7. Cleans up session state file

### OmniFocus Configuration

The `omnifocus` section controls automatic task completion integration:

- **`project_name`** (string|null, default: `null`): OmniFocus project name for task management
- **`auto_log_tasks`** (boolean, default: `true`): Enable/disable automatic task completion during wrapup
- **`prompt_if_missing`** (boolean, default: `true`): Prompt user if project name not configured

**Session Lifecycle Integration:**
- Tasks are automatically created during session startup by task-startup skill
- Task ID stored in `.task_session_state.json` for lifecycle tracking
- Task-wrapup skill completes the OmniFocus task using stored task ID
- Bidirectional workflow: startup creates → wrapup completes

**Configuration Commands:**
```bash
# Set OmniFocus project for this directory
python3 scripts/config_manager.py set-omnifocus --omnifocus-project "Development"

# Get current OmniFocus project
python3 scripts/config_manager.py get-omnifocus
```

**Workflow:**
1. Session state loaded from `.task_session_state.json`
2. OmniFocus task ID extracted from session state
3. Task completion executed via OmniFocus skill integration
4. Task marked as complete in OmniFocus
5. Non-blocking: continues even if completion fails

**Requirements:**
- OmniFocus skill installed at `~/.claude/skills/omnifocus/`
- OmniFocus project configured via `config_manager.py`
- Session state file exists (created by task-startup skill)

## Bundled Resources

### Python Scripts

**`scripts/config_manager.py`**
- Handles CRUD operations for configuration file
- Auto-migration from older schema versions
- Validation of configuration structure
- CLI: `create`, `show`, `validate`, `add-recipient`, `remove-recipient`

**`scripts/summary_generator.py`**
- Generates intelligent summaries from multiple sources
- Git commit analysis (last 12 hours)
- File change statistics
- Key point extraction from commit messages
- Full and concise summary generation
- CLI: `--config`, `--user-input`, `--format` (full/concise/json)

**`scripts/preview_interface.py`**
- Interactive preview and confirmation workflow
- Summary and distribution plan display
- Edit, customize, and modify options
- User confirmation before sending
- CLI: `--summary`, `--config`

**`scripts/notification_dispatcher.py`**
- Orchestrates parallel execution across all channels
- Email, SMS, Slack, worklog, documentation dispatch
- Optional calendar, GitHub, and OmniFocus integration
- Automatic OmniFocus task completion using stored task IDs
- Comprehensive error handling and reporting
- CLI: `--summary`, `--config`, `--sequential` (optional)

### Extension Architecture

**Core Extensions** (`extensions/core/`):
- Email integration (required)
- SMS integration (required)
- Worklog integration (required)

**Optional Extensions** (`extensions/optional/`):
- Slack integration
- Calendar integration
- GitHub integration
- OmniFocus integration
- Documentation updates

**Future Extensions** (`extensions/future/`):
- Discord notifications
- Microsoft Teams
- JIRA updates
- Asana task creation
- Linear integration

## Usage Examples

### Basic Usage
```
User: "Wrap up this session"
```

The skill will:
1. Check for `.task_wrapup_skill_data.json` in current directory
2. If not found, prompt for configuration
3. Generate summary from git commits
4. Show preview and get confirmation
5. Send notifications in parallel
6. Display final summary

### Custom Summary
```
User: "Wrap up with custom summary: Completed authentication system with OAuth2, added tests, updated docs"
```

Uses user-provided summary instead of auto-generated.

### Quick Worklog Only
```
User: "Just log my work time for this session"
```

Disable email/SMS in config, enable only worklog.

### With Calendar Event
```
User: "Wrap up and create calendar reminder for tomorrow's demo"
```

Triggers optional calendar integration.

## Configuration Management

### Create New Config
```bash
python3 scripts/config_manager.py create --project-name "MyProject" --directory .
```

### Show Current Config
```bash
python3 scripts/config_manager.py show --directory .
```

### Validate Config
```bash
python3 scripts/config_manager.py validate --directory .
```

### Add Email Recipient
```bash
python3 scripts/config_manager.py add-recipient \
  --type email \
  --first-name John \
  --last-name Doe \
  --contact john@example.com
```

### Add SMS Recipient
```bash
python3 scripts/config_manager.py add-recipient \
  --type sms \
  --first-name Jane \
  --last-name Smith \
  --contact +15551234567
```

## Error Handling

### Missing Config
- **Symptom**: No `.task_wrapup_skill_data.json` found
- **Action**: Prompt user for configuration information
- **Recovery**: Create new config with user input

### Email Failure
- **Symptom**: Email skill returns error
- **Action**: Log error details in final summary
- **Recovery**: Prompt user for manual correction, continue with other channels

### SMS Failure
- **Symptom**: Text-message skill returns error
- **Action**: Log which recipients failed
- **Recovery**: Display phone numbers for manual retry

### Worklog Failure
- **Symptom**: Worklog skill returns error
- **Action**: Display error and worklog details
- **Recovery**: Offer to retry or skip

### Date Awareness Issues
- **Symptom**: Incorrect date for worklog or calendar
- **Prevention**: Always check system clock before date operations
- **Recovery**: Prompt user to specify date manually

## Documentation Update Workflow

### Two-Phase Process

**Phase 1: Script Execution** (Python)
1. `notification_dispatcher.py` creates `.task_wrapup_doc_update_request.md`
2. File contains session summary, target paths, update strategy
3. Returns success with path to request file

**Phase 2: Claude Code Execution** (After script completes)
1. **Detection**: Check for `.task_wrapup_doc_update_request.md` in current directory
2. **Reading**: Read the request file to extract session summary and targets
3. **Invocation**: Execute `/sc:document` with the session summary
4. **Updates**: `/sc:document` updates CHANGELOG.md, README.md, and other paths
5. **Cleanup**: Remove `.task_wrapup_doc_update_request.md` after processing
6. **Reporting**: Include documentation updates in final wrap-up summary

### Claude Code Responsibilities

When task-wrapup skill completes, Claude Code should:

```python
# 1. Check for documentation update request
request_file = ".task_wrapup_doc_update_request.md"
if os.path.exists(request_file):
    # 2. Read the request
    with open(request_file, 'r') as f:
        request_content = f.read()

    # 3. Invoke /sc:document
    # Use SlashCommand tool to execute:
    # /sc:document --target CHANGELOG.md README.md --strategy smart_merge

    # 4. Report what was updated
    # "Updated CHANGELOG.md with session entry, refreshed README.md installation section"

    # 5. Cleanup
    os.remove(request_file)
```

### Important Distinctions

**`/sc:document`** (Documentation Generation):
- ✅ Updates project documentation (CHANGELOG, README, API docs)
- ✅ Intelligently merges new information into existing docs
- ✅ Used by task-wrapup skill for documenting session work

**`/sc:save`** (Session Context Persistence):
- ❌ NOT for documentation updates
- ✅ Saves work context to Serena MCP for cross-session continuity
- ✅ Different purpose: session memory, not project docs

## Critical Implementation Details

### Phone Format (SMS)
- **Requirement**: E.164 format (+1XXXXXXXXXX)
- **Validation**: Ensure all phone numbers properly formatted
- **Integration**: Use contacts skill for phone lookup by name

### Group vs Individual Messages
- **Email**: Can send to multiple recipients as group
- **SMS**: MUST send individually to each recipient (NEVER group text)
- **Slack**: Single message to channel (with optional @mentions)

### Date Handling
- **Worklog**: ALWAYS check system clock for current date
- **Calendar**: Be aware of relative dates ("tomorrow", "next week")
- **Include weekends**: No business-day filtering

### Configuration Scope
- **Per-project**: Each project has its own `.task_wrapup_skill_data.json`
- **Not global**: Configuration NOT stored in `~/.claude/skills/`
- **Git-aware**: Add to `.gitignore` to avoid committing sensitive data

## Integration with Other Skills

### Email Skill
- Invoked via: `@~/.claude/skills/email/SKILL.md`
- Provides: Seasonal theming, authentic writing style, contact lookup
- OAuth token: Shared at `~/.claude/.google/token.json`

### Text-Message Skill
- Invoked via: `@~/.claude/skills/text-message/SKILL.md`
- Provides: AppleScript automation, contact lookup
- Requirements: macOS, Messages app permissions

### Worklog Skill
- Invoked via: `@~/.claude/skills/worklog/SKILL.md`
- Provides: Time tracking, client billing
- Data: `~/.claude/skills/worklog/worklog.json`

### Calendar Skill
- Invoked via: `@~/.claude/skills/calendar/SKILL.md`
- Provides: Event creation, reminder setting
- Optional: Only if user requests

### Contacts Skill
- Integration: Automatic contact lookup for email and SMS
- Resolves names to email addresses and phone numbers

## Version History

### v1.1.0 (2025-01-15)
- **Documentation Integration**: Implemented proper `/sc:document` integration
- **Two-Phase Workflow**: Script creates request file, Claude Code processes with `/sc:document`
- **Smart Updates**: CHANGELOG.md and README.md intelligently updated based on session
- **Request File**: `.task_wrapup_doc_update_request.md` for Claude Code detection
- **Clarified Commands**: Distinguished `/sc:document` (docs) from `/sc:save` (session context)
- **Added Documentation**: DOCUMENTATION_INTEGRATION.md with comprehensive guide

### v1.0.0 (2025-01-15)
- Initial release
- Core features: email, SMS, Slack, worklog, documentation
- Intelligent summary generation from git commits
- Interactive preview and confirmation workflow
- Parallel notification dispatch
- Per-project configuration with auto-migration
- Extension plugin architecture

## Future Enhancements

### Planned Features
- Discord integration
- Microsoft Teams notifications
- JIRA issue creation
- Asana task updates
- Linear integration
- Notion page updates

### Potential Improvements
- TodoWrite integration for completed tasks
- Serena memory integration for session context
- AI-powered summary enhancement
- Template customization per recipient
- Scheduling for delayed send
- Retry logic with exponential backoff

---

**Author**: Claude Code SuperClaude Framework
**License**: MIT
**Repository**: ~/.claude/skills/task-wrapup/
