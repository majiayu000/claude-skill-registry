---
description: Validates JIRA projects and boards exist, auto-creates missing resources. Use when setting up JIRA integration, validating .env configuration, or troubleshooting missing projects/boards. Supports per-project board configuration with JIRA_BOARDS_{ProjectKey} pattern.
allowed-tools: Read, Bash, Write, Edit
---

# Jira Resource Validator Skill

**Purpose**: Validate and auto-create Jira projects and boards, ensuring .env configuration is correct.

**Auto-Activation**: Triggers when Jira setup or validation is needed.

## Security Rules (MANDATORY)

These rules apply to ALL JIRA API operations in this skill.

### Credential Handling

1. **Never collect credentials** — this skill reads from `.env` only, never prompts the user
2. **Never log secrets** — never echo token values, auth headers, or base64 credentials
3. **Never write credentials** — the user configures `.env` themselves (this skill may update non-secret keys like `JIRA_BOARDS` and `JIRA_PROJECT`)

### Credential Loading

```bash
# 1. Validate presence FIRST (before reading any values)
for KEY in JIRA_API_TOKEN JIRA_EMAIL JIRA_DOMAIN; do
  if ! grep -qE "^${KEY}=.+" .env; then
    echo "Error: ${KEY} missing or empty in .env"
    exit 1
  fi
done

# 2. Load credentials ONLY after validation passes (never display values)
#    head -1 ensures only first match used if .env has duplicate keys
JIRA_API_TOKEN="$(grep '^JIRA_API_TOKEN=' .env | head -1 | cut -d '=' -f2-)"
JIRA_EMAIL="$(grep '^JIRA_EMAIL=' .env | head -1 | cut -d '=' -f2-)"
JIRA_DOMAIN="$(grep '^JIRA_DOMAIN=' .env | head -1 | cut -d '=' -f2-)"
```

### Domain Validation (before ANY API call)

```bash
# Reject IP addresses first (SSRF prevention)
if [[ "$JIRA_DOMAIN" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ ]] || [[ "$JIRA_DOMAIN" =~ ^\[.*\]$ ]] || [[ "$JIRA_DOMAIN" =~ ^0x ]]; then
  echo "Error: IP addresses not allowed — use a hostname"
  exit 1
fi

# Reject localhost and private networks
if [[ "$JIRA_DOMAIN" =~ ^(localhost|127\.|10\.|172\.(1[6-9]|2[0-9]|3[01])\.|192\.168\.) ]]; then
  echo "Error: Internal/localhost addresses not allowed"
  exit 1
fi

# Must be a valid hostname — no special chars, no consecutive dots
if [[ ! "$JIRA_DOMAIN" =~ ^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?)*$ ]]; then
  echo "Error: JIRA_DOMAIN contains invalid characters"
  exit 1
fi

# Cloud JIRA: must match <subdomain>.atlassian.net
if [[ ! "$JIRA_DOMAIN" =~ ^[a-zA-Z0-9-]+\.atlassian\.net$ ]]; then
  echo "Error: Domain does not match <subdomain>.atlassian.net pattern"
  exit 1
fi
```

### API Call Pattern (HTTPS only, quoted variables)

```bash
AUTH="$(printf '%s:%s' "$JIRA_EMAIL" "$JIRA_API_TOKEN" | base64)"

# All API calls MUST use https://, double-quote all variables
curl -s -f \
  -H "Authorization: Basic $AUTH" \
  -H "Content-Type: application/json" \
  "https://${JIRA_DOMAIN}/rest/api/3/..."
```

---

## What This Skill Does

This skill ensures your Jira configuration in `.env` is valid and all resources exist. It's **smart enough** to:

1. **Validate Jira projects** - Check if `JIRA_PROJECT` exists
2. **Prompt for action** - Select existing project or create new one
3. **Validate Jira boards** - Check if boards exist (by ID or name)
4. **Create missing boards** - If board names provided, create them automatically
5. **Update .env with IDs** - Replace board names with actual board IDs after creation

## When This Skill Activates

✅ **Automatically activates when**:
- You set up Jira integration for the first time
- You run `/sw-jira:sync` and resources are missing
- Your `.env` has invalid Jira configuration
- You mention "jira setup" or "jira validation"

## Jira Configuration Structure

### Required .env Variables

```
JIRA_API_TOKEN=<your-token>
JIRA_EMAIL=<your-email>
JIRA_DOMAIN=<your-company>.atlassian.net
JIRA_STRATEGY=board-based
JIRA_PROJECT=PROJECTKEY
JIRA_BOARDS=1,2,3  # IDs (if exist) OR names (if creating)
```

### Smart Per-Board Detection (Mixed Mode Support!)

**The system is smart enough to handle ANY combination of IDs and names:**

**All IDs** (validate existing boards):
```bash
JIRA_BOARDS=1,2,3
```
→ Validates boards 1, 2, 3 exist

**All Names** (create new boards):
```bash
JIRA_BOARDS=Frontend,Backend,Mobile
```
→ Creates 3 boards, updates .env with IDs: `JIRA_BOARDS=101,102,103`

**Mixed IDs and Names** (smart handling!):
```bash
JIRA_BOARDS=101,102,QA,Dashboard
```
→ Validates 101, 102 exist
→ Creates "QA" and "Dashboard" boards
→ Updates .env: `JIRA_BOARDS=101,102,103,104` (all IDs!)

**How it works**: Each entry is checked individually:
- Numeric (e.g., "123") → Validate ID exists
- Non-numeric (e.g., "QA") → Create board with that name
- After creation, .env is updated with ALL board IDs

### NEW: Per-Project Configuration (Advanced - Multiple Projects × Boards)

**Multiple JIRA projects with their own boards:**

```bash
# Multiple projects with their own boards
JIRA_STRATEGY=project-per-team
JIRA_PROJECTS=BACKEND,FRONTEND,MOBILE

# Per-project boards (hierarchical naming)
JIRA_BOARDS_BACKEND=123,456         # Sprint + Kanban (IDs)
JIRA_BOARDS_FRONTEND=Sprint,Bug     # Create these boards
JIRA_BOARDS_MOBILE=789,012,345      # iOS + Android + Release (IDs)
```
→ Validates 3 projects exist: BACKEND, FRONTEND, MOBILE
→ Validates/creates boards per project:
  - BACKEND: Validates boards 123, 456 exist
  - FRONTEND: Creates "Sprint" and "Bug" boards, updates .env with IDs
  - MOBILE: Validates boards 789, 012, 345 exist

**Naming Convention**: `{PROVIDER}_{RESOURCE_TYPE}_{PROJECT_KEY}`

**Mixed IDs and Names Per Project**:
```bash
JIRA_BOARDS_BACKEND=123,NewBoard,456
```
→ Validates 123, 456 exist
→ Creates "NewBoard"
→ Updates .env: `JIRA_BOARDS_BACKEND=123,789,456` (all IDs!)

## Validation Flow

### Step 1: Project Validation

**Check if project exists**:
```bash
# API call to Jira
GET /rest/api/3/project/PROJECTKEY
```

**If project exists**:
```
✅ Project "PROJECTKEY" exists
   ID: 10001
   Name: My Project
```

**If project doesn't exist**:
```
⚠️  Project "PROJECTKEY" not found

What would you like to do?
1. Select an existing project
2. Create a new project
3. Cancel

Your choice [1]:
```

**Option 1: Select Existing**:
```
Available projects:
1. PROJ1 - Project One
2. PROJ2 - Project Two
3. PROJ3 - Project Three

Select a project [1]:

✅ Updated .env: JIRA_PROJECT=PROJ1
```

**Option 2: Create New**:
```
Enter project name: My New Project

📦 Creating Jira project: PROJECTKEY (My New Project)...
✅ Project created: PROJECTKEY (ID: 10005)
```

### Step 2: Board Validation (Per-Board Smart Detection)

**Scenario A: All Board IDs** (all numeric):
```bash
JIRA_BOARDS=1,2,3
```

**Validation**:
```
Checking boards: 1,2,3...
  ✅ Board 1: Frontend Board (exists)
  ✅ Board 2: Backend Board (exists)
  ⚠️  Board 3: Not found

⚠️  Issues found: 1 board(s)
```

**Scenario B: All Board Names** (all non-numeric):
```bash
JIRA_BOARDS=Frontend,Backend,Mobile
```

**Auto-creation**:
```
Checking boards: Frontend,Backend,Mobile...
  📦 Creating board: Frontend...
  ✅ Created: Frontend (ID: 101)
  📦 Creating board: Backend...
  ✅ Created: Backend (ID: 102)
  📦 Creating board: Mobile...
  ✅ Created: Mobile (ID: 103)

📝 Updating .env with board IDs...
✅ Updated JIRA_BOARDS: 101,102,103

✅ All boards validated/created successfully
```

**Scenario C: Mixed IDs and Names** (SMART!):
```bash
JIRA_BOARDS=101,102,QA,Dashboard
```

**Smart handling**:
```
Checking boards: 101,102,QA,Dashboard...
  ✅ Board 101: Frontend Board (exists)
  ✅ Board 102: Backend Board (exists)
  📦 Creating board: QA...
  ✅ Created: QA (ID: 103)
  📦 Creating board: Dashboard...
  ✅ Created: Dashboard (ID: 104)

📝 Updating .env with board IDs...
✅ Updated JIRA_BOARDS: 101,102,103,104

✅ All boards validated/created successfully
```

## Usage Examples

### Example 1: Fresh Jira Setup

**Scenario**: New project, no Jira resources exist yet

**Action**: Run `/sw-jira:sync`

**What Happens**:
```bash
🔍 Validating Jira configuration...

Checking project: MINIDOOM...
⚠️  Project "MINIDOOM" not found

What would you like to do?
1. Select an existing project
2. Create a new project
3. Cancel

Your choice [2]: 2

Enter project name: Mini DOOM Tournament

📦 Creating Jira project: MINIDOOM (Mini DOOM Tournament)...
✅ Project created: MINIDOOM (ID: 10005)

Checking boards: Frontend,Backend,Mobile...
📦 Creating boards from names...

Creating board: Frontend in project MINIDOOM...
✅ Board created: Frontend (ID: 101)

Creating board: Backend in project MINIDOOM...
✅ Board created: Backend (ID: 102)

Creating board: Mobile in project MINIDOOM...
✅ Board created: Mobile (ID: 103)

✅ Updated .env: JIRA_BOARDS=101,102,103

🎉 Jira configuration complete! All resources ready.
```

**Result**: `.env` now has correct project and board IDs

### Example 2: Select Existing Project

**Scenario**: Project already exists in Jira

**Action**: Run validation

**What Happens**:
```bash
🔍 Validating Jira configuration...

Checking project: PROJ...
⚠️  Project "PROJ" not found

What would you like to do?
1. Select an existing project
2. Create a new project
3. Cancel

Your choice [1]: 1

Available projects:
1. FRONTEND - Frontend Team
2. BACKEND - Backend Team
3. MOBILE - Mobile Team

Select a project [1]: 2

✅ Updated .env: JIRA_PROJECT=BACKEND
✅ Project "BACKEND" exists

Checking boards: 45,46...
✅ All boards exist
```

### Example 3: Mixed Board IDs (Some Exist, Some Don't)

**Scenario**: Some board IDs are invalid

**Action**: Run validation

**What Happens**:
```bash
🔍 Validating Jira configuration...

Checking project: PROJECTKEY...
✅ Project "PROJECTKEY" exists

Checking boards: 1,2,999...

Board 1: ✅ Exists (Frontend Board)
Board 2: ✅ Exists (Backend Board)
Board 999: ❌ Not found

⚠️  Boards not found: 999

Available boards in project PROJECTKEY:
1. Frontend Board (ID: 1)
2. Backend Board (ID: 2)
3. QA Board (ID: 3)
4. DevOps Board (ID: 4)

Would you like to:
1. Remove invalid board (999) from configuration
2. Replace with correct board ID
3. Create new board

Your choice [2]: 2

Enter correct board ID or name: 3

✅ Updated .env: JIRA_BOARDS=1,2,3
```

## CLI Command

**Manual validation**:
```bash
# From TypeScript
npx tsx src/utils/external-resource-validator.ts

# Or via skill activation
"Can you validate my Jira configuration?"
```

**Validation output**:
```typescript
{
  valid: true,
  project: {
    exists: true,
    key: 'PROJECTKEY',
    id: '10001',
    name: 'My Project'
  },
  boards: {
    valid: true,
    existing: [1, 2, 3],
    missing: [],
    created: []
  },
  envUpdated: false
}
```

## Smart Board Creation Logic (Per-Board Detection)

### Detection Algorithm

```typescript
// Parse JIRA_BOARDS from .env
const boardsConfig = "101,102,QA,Dashboard"; // Mixed!
const boardEntries = boardsConfig.split(',').map(b => b.trim());
const finalBoardIds = [];

// Check EACH board individually
for (const entry of boardEntries) {
  const isNumeric = /^\d+$/.test(entry);

  if (isNumeric) {
    // Entry is a board ID - validate it exists
    const boardId = parseInt(entry);
    const board = await checkBoard(boardId);
    if (board) {
      console.log(`✅ Board ${boardId}: ${board.name} (exists)`);
      finalBoardIds.push(boardId);
    } else {
      console.error(`⚠️  Board ${boardId}: Not found`);
    }
  } else {
    // Entry is a board name - create it
    console.log(`📦 Creating board: ${entry}...`);
    const board = await createBoard(entry, projectKey);
    console.log(`✅ Created: ${entry} (ID: ${board.id})`);
    finalBoardIds.push(board.id);
  }
}

// Update .env if any boards were created
if (createdBoardIds.length > 0) {
  updateEnv({ JIRA_BOARDS: finalBoardIds.join(',') });
}
```

**Key improvement**: Per-board detection instead of all-or-nothing!
- `JIRA_BOARDS=1,2,3` → Validates all IDs
- `JIRA_BOARDS=A,B,C` → Creates all boards
- `JIRA_BOARDS=1,2,C` → Validates 1,2, creates C (mixed!)

### Board Creation API

**Jira REST API** (v3):
```bash
POST /rest/api/3/board
Content-Type: application/json

{
  "name": "Frontend Board",
  "type": "scrum",
  "filterId": 10000,  # Filter for project issues
  "location": {
    "type": "project",
    "projectKeyOrId": "PROJECTKEY"  # CRITICAL: Associates board with project
  }
}

Response:
{
  "id": 101,
  "name": "Frontend Board",
  "type": "scrum"
}
```

**IMPORTANT**: The `location` field is **MANDATORY** to associate the board with a project. Without it, Jira creates the board but leaves it detached, requiring manual connection via the UI.

**Filter creation** (required for board):
```bash
POST /rest/api/3/filter
Content-Type: application/json

{
  "name": "PROJECTKEY Issues",
  "jql": "project = PROJECTKEY"
}

Response:
{
  "id": 10000
}
```

## Configuration Examples

### Example 1: All Names (Create Boards)

**Before** (`.env`):
```bash
JIRA_PROJECT=PROJ
JIRA_BOARDS=Frontend,Backend,QA,DevOps
```

**After validation**:
```bash
JIRA_PROJECT=PROJ
JIRA_BOARDS=101,102,103,104
```

**What happened**:
- Detected non-numeric values (names)
- Created 4 boards in Jira
- Updated .env with actual board IDs

### Example 2: All IDs (Validate Existing)

**Before** (`.env`):
```bash
JIRA_PROJECT=PROJ
JIRA_BOARDS=1,2,3
```

**After validation**:
```bash
JIRA_PROJECT=PROJ
JIRA_BOARDS=1,2,3
```

**What happened**:
- Detected numeric values (IDs)
- Validated all boards exist
- No changes needed

### Example 3: Mixed IDs and Names (SMART!)

**Before** (`.env`):
```bash
JIRA_PROJECT=PROJ
JIRA_BOARDS=101,102,QA,Dashboard
```

**After validation**:
```bash
JIRA_PROJECT=PROJ
JIRA_BOARDS=101,102,103,104
```

**What happened**:
- Validated boards 101, 102 exist
- Created "QA" board (got ID 103)
- Created "Dashboard" board (got ID 104)
- Updated .env with ALL board IDs
- **This is the key feature** - you can mix existing IDs with new board names!

### Example 4: Fix Invalid Project

**Before** (`.env`):
```bash
JIRA_PROJECT=NONEXISTENT
JIRA_BOARDS=1,2
```

**After validation** (user selected existing project):
```bash
JIRA_PROJECT=EXISTINGPROJ
JIRA_BOARDS=1,2
```

**What happened**:
- Project NONEXISTENT not found
- User selected EXISTINGPROJ from list
- Updated .env with correct project key

## Error Handling

### Error 1: Invalid Credentials

**Symptom**: API calls fail with 401 Unauthorized

**Solution**:
```
❌ Jira API authentication failed

Please check:
1. JIRA_API_TOKEN is correct
2. JIRA_EMAIL matches your Jira account
3. JIRA_DOMAIN is correct (yourcompany.atlassian.net)

Generate new token at:
https://id.atlassian.com/manage-profile/security/api-tokens
```

### Error 2: Insufficient Permissions

**Symptom**: Cannot create projects/boards (403 Forbidden)

**Solution**:
```
❌ Insufficient permissions to create resources

You need:
- Project Creator permission (for projects)
- Board Creator permission (for boards)

Contact your Jira administrator to request permissions.
```

### Error 3: Project Key Already Taken

**Symptom**: Project creation fails (key exists)

**Solution**:
```
❌ Project key "PROJ" already exists

Options:
1. Use a different project key
2. Select the existing project
3. Cancel

Your choice [2]:
```

### Error 4: Network/API Errors

**Symptom**: API calls timeout or fail

**Solution**:
```
❌ Jira API error: Request timeout

Please check:
1. Internet connection
2. Jira domain is correct
3. Jira is not down (check status.atlassian.com)

Retry? [Y/n]:
```

## Integration with SpecWeave Workflow

### Automatic Validation

When using `/sw-jira:sync`, validation runs automatically:

```bash
/sw-jira:sync 0014

# Internally calls:
1. validateJiraResources()
2. Fix missing project/boards
3. Proceed with sync
```

### Manual Validation

Run validation independently:

```bash
# Via skill
"Validate my Jira configuration"

# Via TypeScript
npx tsx src/utils/external-resource-validator.ts

# Via CLI (future)
specweave validate-jira
```

## Best Practices

✅ **Use board names for initial setup**:
```bash
JIRA_BOARDS=Sprint-1,Sprint-2,Backlog
```
- System creates boards automatically
- Updates .env with IDs
- One-time setup, then use IDs

✅ **Use board IDs after creation**:
```bash
JIRA_BOARDS=101,102,103
```
- Faster validation (no creation needed)
- More reliable (IDs don't change)

✅ **Keep .env in version control** (gitignored tokens):
```bash
# Commit project/board structure
JIRA_PROJECT=PROJ
JIRA_BOARDS=101,102,103

# Don't commit sensitive data
JIRA_API_TOKEN=<redacted>
JIRA_EMAIL=<redacted>
```

✅ **Document board mapping** (in README):
```markdown
## Jira Boards

- Board 101: Frontend Team
- Board 102: Backend Team
- Board 103: QA Team
```

## Summary

This skill ensures your Jira configuration is **always valid** by:

1. ✅ **Validating projects** - Check if project exists, prompt to select or create
2. ✅ **Validating boards** - Check if boards exist (IDs) or create them (names)
3. ✅ **Auto-updating .env** - Replace board names with IDs after creation
4. ✅ **Clear error messages** - Actionable guidance for all failures
5. ✅ **Non-blocking** - Graceful degradation with manual fallback

**Result**: Zero manual Jira setup - system handles everything!

---

**Skill Version**: 1.0.0
**Introduced**: SpecWeave v0.9.5
**Last Updated**: 2025-11-09
