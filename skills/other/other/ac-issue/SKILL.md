---
name: ac-issue
description: "Reports issues to agentic-config repository via GitHub CLI. Supports bug reports and feature requests. Triggers on keywords: issue, report bug, feature request, ac issue"
project-agnostic: true
allowed-tools:
  - Bash
  - Read
---

# Issue Reporter

Creates GitHub issues in the central agentic-config repository (WaterplanAI/agentic-config) for bug reports and feature requests.

## Usage
```
/ac-issue                           # Context-based: extract from conversation
/ac-issue "Title" "Description"     # Explicit: user provides details
/ac-issue --bug "Title"             # Bug report with template
/ac-issue --feature "Title"         # Feature request with template
```

**Target Repository**: `WaterplanAI/agentic-config`

---

## Workflow Steps

### Step 1: Authentication Verification (CRITICAL - DO FIRST)

**INSTRUCTION**: Verify GitHub CLI authentication before any other operation.

```bash
# Check if gh CLI is installed
if ! command -v gh &>/dev/null; then
  echo "ERROR: GitHub CLI (gh) not found"
  echo ""
  echo "Please install GitHub CLI: https://cli.github.com/"
  exit 1
fi

echo "Checking GitHub CLI authentication..."
GH_AUTH_OUTPUT=$(gh auth status 2>&1)
GH_AUTH_STATUS=$?

if [ $GH_AUTH_STATUS -ne 0 ]; then
  echo "ERROR: GitHub CLI not authenticated"
  echo ""
  echo "$GH_AUTH_OUTPUT"
  echo ""
  echo "Please authenticate with: gh auth login"
  exit 1
fi

echo "$GH_AUTH_OUTPUT"
echo ""
echo "Authentication verified."
```

**Validation Logic**:
1. Run `gh auth status` and capture exit code
2. **If exit code != 0**: STOP immediately with error and `gh auth login` instruction
3. **If authenticated**: Continue with success message

---

### Step 2: Input Mode Detection

**INSTRUCTION**: Parse arguments to determine input mode.

**Arguments**: `$ARGUMENTS`

**Mode Detection Logic**:

| Input Pattern | Mode | Action |
|---------------|------|--------|
| Empty/no args | Context Mode | Extract from recent conversation |
| `--bug "Title"` | Bug Template | Use bug report template with provided title |
| `--feature "Title"` | Feature Template | Use feature request template with provided title |
| `"Title" "Description"` | Explicit Mode | Use provided title and description |
| `"Title"` only | Explicit Mode | Use title, prompt for description |

**Parsing Examples**:
```
$ARGUMENTS = ""                          -> Context Mode
$ARGUMENTS = "--bug \"Auth fails\""      -> Bug Template, title="Auth fails"
$ARGUMENTS = "--feature \"Add X\""       -> Feature Template, title="Add X"
$ARGUMENTS = "\"Title\" \"Body text\""   -> Explicit, title="Title", body="Body text"
```

---

### Step 3: Context Extraction (If Context Mode)

**INSTRUCTION**: If no arguments provided, analyze recent conversation for issue details.

**Context Extraction Heuristics**:
1. Search recent messages for error patterns:
   - `Error:`, `ERROR:`, `Exception:`, `failed`, `unexpected`
   - Stack traces: Lines with `at `, `File "`, traceback patterns
   - Command failures: `exit code`, `returned non-zero`

2. Extract reproduction context:
   - "I tried...", "When I...", "After running..."
   - Command sequences that led to the issue

3. Identify expected vs actual behavior:
   - "Expected...", "but got...", "instead of..."

**If Context Found**:
- Generate title: Summarize error/ac-issue in <60 chars
- Generate description: Include error messages, context, steps observed

**If No Context Found**:
- STOP and prompt user:
  ```
  No issue context detected in recent conversation.

  Please provide issue details:
  /ac-issue "Title" "Description"

  Or specify type:
  /ac-issue --bug "Brief description of the bug"
  /ac-issue --feature "Brief description of the feature"
  ```

---

### Step 4: Environment Metadata Collection

**INSTRUCTION**: Gather safe environment information for issue context.

```bash
# Collect environment info (sanitized)
ENV_OS=$(uname -s 2>/dev/null || echo "Unknown")
ENV_OS_VERSION=$(uname -r 2>/dev/null || echo "Unknown")
ENV_SHELL=$(basename "$SHELL" 2>/dev/null || echo "Unknown")
ENV_GIT_VERSION=$(git --version 2>/dev/null | cut -d' ' -f3 || echo "Unknown")
ENV_BRANCH=$(git branch --show-current 2>/dev/null || echo "N/A")

# Get agentic-config version from plugin.json
if [ -d "${CLAUDE_PLUGIN_ROOT}" ]; then
  # Read version from plugin.json if available
  ENV_AGENTIC_VERSION=$(python3 -c "import json; print(json.load(open('${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json'))['version'])" 2>/dev/null || echo "Unknown")
else
  ENV_AGENTIC_VERSION="Unknown"
fi

echo "Environment collected:"
echo "  OS: $ENV_OS $ENV_OS_VERSION"
echo "  Shell: $ENV_SHELL"
echo "  Git: $ENV_GIT_VERSION"
echo "  Branch: $ENV_BRANCH"
echo "  agentic-config: $ENV_AGENTIC_VERSION"
```

**Information to EXCLUDE (Privacy/Security)**:
- Absolute paths containing usernames (sanitize with `~`)
- API keys or tokens (patterns: `ghp_`, `sk-`, `AKIA`, 32+ char alphanumeric)
- Email addresses
- Private repository names
- Contents of `.env` files

---

### Step 5: Sanitization

**INSTRUCTION**: Sanitize any user-provided or extracted content before including in issue.

**Sanitization Rules**:

1. **Path Anonymization**:
   ```bash
   # Replace home directory with ~
   sanitized="${content//$HOME/\~}"

   # Replace common user path patterns
   sanitized=$(echo "$sanitized" | sed -E 's|/Users/[^/]+|~|g; s|/home/[^/]+|~|g')
   ```

2. **Secret Detection**:
   - Check for API key patterns: `[A-Za-z0-9_-]{32,}`
   - Check for token prefixes: `ghp_`, `gho_`, `sk-`, `AKIA`, `Bearer `
   - If detected: Replace with `[REDACTED]` and warn user

3. **Warning on Detection**:
   ```
   WARNING: Potential sensitive data detected and redacted.
   Please review the preview carefully before submitting.
   ```

---

### Step 6: Issue Body Formatting

**INSTRUCTION**: Format the issue body with structured sections.

**Bug Report Template** (when `--bug` flag used):
```markdown
## Bug Description
<user-provided or context-extracted description>

## Environment
- OS: <ENV_OS> <ENV_OS_VERSION>
- Shell: <ENV_SHELL>
- Git: <ENV_GIT_VERSION>
- agentic-config: <ENV_AGENTIC_VERSION>

## Steps to Reproduce
<if available from context, otherwise "Not provided">

## Expected Behavior
<if available>

## Actual Behavior
<error messages, stack traces from context>

---
Reported via `/ac-issue` command
```

**Feature Request Template** (when `--feature` flag used):
```markdown
## Feature Description
<user-provided description>

## Use Case
<why this feature would be useful>

## Proposed Solution
<if user provided suggestions>

## Environment
- agentic-config: <ENV_AGENTIC_VERSION>

---
Reported via `/ac-issue` command
```

**General Template** (explicit or context mode):
```markdown
## Description
<user-provided or context-extracted description>

## Environment
- OS: <ENV_OS> <ENV_OS_VERSION>
- Shell: <ENV_SHELL>
- Git: <ENV_GIT_VERSION>
- agentic-config: <ENV_AGENTIC_VERSION>

## Context
<relevant error messages, stack traces, or unexpected behavior if available>

## Additional Information
<any other relevant details>

---
Reported via `/ac-issue` command
```

---

### Step 7: Issue Preview and Confirmation

**INSTRUCTION**: Display formatted issue preview and wait for user confirmation.

**Display Format**:
```
Issue Title: <TITLE>
Repository: WaterplanAI/agentic-config
Labels: <bug | enhancement | none>

Body:
---
<FORMATTED_BODY>
---

Create this issue? (yes/no/edit)
- yes: Create the issue as shown
- no: Cancel issue creation
- edit: Provide modified title or description
```

**Confirmation Logic**:
- Wait for explicit `yes` before proceeding
- If `no`: Exit gracefully with "Issue creation cancelled"
- If `edit`: Prompt for new title/description and re-preview

---

### Step 8: Create Issue

**INSTRUCTION**: Execute gh CLI to create the issue.

```bash
# Determine label based on mode
LABEL_FLAG=""
if [ "$MODE" = "bug" ]; then
  LABEL_FLAG="--label bug"
elif [ "$MODE" = "feature" ]; then
  LABEL_FLAG="--label enhancement"
fi

# Create issue with HEREDOC for body
ISSUE_URL=$(gh issue create \
  --repo WaterplanAI/agentic-config \
  --title "$ISSUE_TITLE" \
  $LABEL_FLAG \
  --body "$(cat <<'EOF'
<FORMATTED_BODY>
EOF
)" 2>&1)

CREATE_STATUS=$?

if [ $CREATE_STATUS -ne 0 ]; then
  echo "ERROR: Failed to create issue"
  echo "$ISSUE_URL"
  echo ""
  echo "You can try creating the issue manually at:"
  echo "https://github.com/WaterplanAI/agentic-config/issues/new"
  exit 1
fi

echo "$ISSUE_URL"
```

---

### Step 9: Report Results

**INSTRUCTION**: Display success message with issue URL and next steps.

```
ISSUE CREATED SUCCESSFULLY

Issue URL: <ISSUE_URL>
Title: <ISSUE_TITLE>
Repository: WaterplanAI/agentic-config

Next Steps:
1. View issue: <ISSUE_URL>
2. Add more context if needed via GitHub web interface
3. Monitor for maintainer response

Thank you for contributing to agentic-config!
```

---

## Error Handling

| Error | Detection | Response |
|-------|-----------|----------|
| gh not installed | `command -v gh` fails | "GitHub CLI not found. Install: https://cli.github.com/" |
| Not authenticated | `gh auth status` exit != 0 | "Please authenticate: gh auth login" |
| No context found | Context extraction returns empty | Prompt for explicit input |
| Network error | `gh issue create` fails | Show error, suggest manual creation |
| Rate limited | gh returns rate limit error | "GitHub API rate limited. Try again later." |

---

## Security Considerations

1. **Path Sanitization**: All paths anonymized before inclusion
2. **Secret Detection**: Scan for API keys, tokens before submission
3. **No .env Content**: Never include environment file contents
4. **User Confirmation**: Always preview before creating
5. **Read-Only Default**: No modifications to local files

---

## Design Decisions

1. **Central Repository Target**
   - All issues go to `WaterplanAI/agentic-config`
   - Ensures consolidated issue tracking for the project

2. **Dual Input Mode**
   - Context extraction for seamless error reporting
   - Explicit mode for planned feature requests

3. **Mandatory Preview**
   - Always show preview before creating
   - Prevents accidental sensitive data exposure

4. **Minimal Tool Requirements**
   - Only needs Bash and Read (no Write)
   - gh CLI handles all GitHub interaction

5. **Project-Agnostic Design**
   - Works from any agentic-config installation
   - Uses CLAUDE_PLUGIN_ROOT for plugin-aware path resolution
