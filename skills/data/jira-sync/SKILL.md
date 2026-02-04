---
name: jira-sync
description: Sync guidance for SpecWeave increments with JIRA epics/stories (content SpecWeave→JIRA, status JIRA→SpecWeave). Use when asking about JIRA integration setup or troubleshooting sync. For actual syncing, use /sw-jira:sync command instead.
allowed-tools: Read, Write, Edit, Task, Bash
---

# JIRA Sync Skill

Coordinates JIRA synchronization by delegating to `jira-mapper` agent.

**Sync Behavior**: Content (specs, tasks) syncs SpecWeave → JIRA. Status (open/closed) syncs JIRA → SpecWeave.

**⚠️ IMPORTANT**: This skill provides HELP and GUIDANCE about JIRA sync. For actual syncing, users should use the `/sw-jira:sync` command directly. This skill should NOT auto-activate when the command is being invoked.

## When to Activate

✅ **Do activate when**:
- User asks: "How do I set up JIRA sync?"
- User asks: "What JIRA credentials do I need?"
- User asks: "How does JIRA sync work?"
- User needs help configuring JIRA integration

❌ **Do NOT activate when**:
- User invokes `/sw-jira:sync` command (command handles it)
- Command is already running (avoid duplicate invocation)
- Task completion hook is syncing (automatic process)

## Responsibilities

1. Answer questions about JIRA sync configuration
2. Help validate prerequisites (JIRA credentials, increment structure)
3. Explain sync directions: content (SpecWeave→JIRA), status (JIRA→SpecWeave)
4. Provide troubleshooting guidance

---

## ⚠️ CRITICAL: Secrets Required (MANDATORY CHECK)

**BEFORE attempting JIRA sync, CHECK for JIRA credentials.**

### Step 1: Check If Credentials Exist

```bash
# Check .env file for both required credentials
if [ -f .env ] && grep -q "JIRA_API_TOKEN" .env && grep -q "JIRA_EMAIL" .env; then
  echo "✅ JIRA credentials found"
else
  # Credentials NOT found - STOP and prompt user
fi
```

### Step 2: If Credentials Missing, STOP and Show This Message

```
🔐 **JIRA API Token and Email Required**

I need your JIRA API token and email to sync with JIRA.

**How to get it**:
1. Go to: https://id.atlassian.com/manage-profile/security/api-tokens
2. Log in with your Atlassian account
3. Click "Create API token"
4. Give it a label (e.g., "specweave-sync")
5. Click "Create"
6. **Copy the token immediately** (you can't see it again!)

**Where I'll save it**:
- File: `.env` (gitignored, secure)
- Format:
  ```
  JIRA_API_TOKEN=your-jira-api-token-here
  JIRA_EMAIL=your-email@example.com
  JIRA_DOMAIN=your-domain.atlassian.net
  ```

**Security**:
✅ .env is in .gitignore (never committed to git)
✅ Token is random alphanumeric string (variable length)
✅ Stored locally only (not in source code)

Please provide:
1. Your JIRA API token:
2. Your JIRA email:
3. Your JIRA domain (e.g., company.atlassian.net):
```

### Step 3: Validate Credentials Format

```bash
# Validate email format
if [[ ! "$JIRA_EMAIL" =~ ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]]; then
  echo "⚠️  Warning: Email format unexpected"
  echo "Expected: valid email address"
  echo "Got: $JIRA_EMAIL"
fi

# Validate domain format
if [[ ! "$JIRA_DOMAIN" =~ \.atlassian\.net$ ]]; then
  echo "⚠️  Warning: Domain format unexpected"
  echo "Expected: *.atlassian.net"
  echo "Got: $JIRA_DOMAIN"
  echo "Note: Self-hosted JIRA may have different domain format"
fi

# Token validation (just check it's not empty)
if [ -z "$JIRA_API_TOKEN" ]; then
  echo "❌ Error: JIRA API token is empty"
  exit 1
fi
```

### Step 4: Save Credentials Securely

```bash
# Save to .env
cat >> .env << EOF
JIRA_API_TOKEN=$JIRA_API_TOKEN
JIRA_EMAIL=$JIRA_EMAIL
JIRA_DOMAIN=$JIRA_DOMAIN
EOF

# Ensure .env is gitignored
if ! grep -q "^\\.env$" .gitignore; then
  echo ".env" >> .gitignore
fi

# Create .env.example for team
cat > .env.example << 'EOF'
# JIRA API Token
# Get from: https://id.atlassian.com/manage-profile/security/api-tokens
JIRA_API_TOKEN=your-jira-api-token
JIRA_EMAIL=your-email@example.com
JIRA_DOMAIN=your-domain.atlassian.net
EOF

echo "✅ Credentials saved to .env (gitignored)"
echo "✅ Created .env.example for team (commit this)"
```

### Step 5: Use Credentials in Sync

```bash
# Export for JIRA API calls (read from .env without displaying values)
export JIRA_API_TOKEN=$(grep '^JIRA_API_TOKEN=' .env | cut -d '=' -f2-)
export JIRA_EMAIL=$(grep '^JIRA_EMAIL=' .env | cut -d '=' -f2-)
export JIRA_DOMAIN=$(grep '^JIRA_DOMAIN=' .env | cut -d '=' -f2-)

# Create Basic Auth header (JIRA uses email:token)
AUTH=$(echo -n "$JIRA_EMAIL:$JIRA_API_TOKEN" | base64)

# Use in JIRA API calls
curl -H "Authorization: Basic $AUTH" \
     -H "Content-Type: application/json" \
     https://$JIRA_DOMAIN/rest/api/3/issue/PROJ-123
```

### Step 6: Never Log Secrets

```bash
# ❌ WRONG - Logs secret
echo "Using token: $JIRA_API_TOKEN"

# ✅ CORRECT - Masks secret
echo "Using JIRA credentials (token present: ✅, email: $JIRA_EMAIL)"
```

### Step 7: Error Handling

```bash
# If API call fails with 401 Unauthorized
if [ $? -eq 401 ]; then
  echo "❌ JIRA credentials invalid"
  echo ""
  echo "Possible causes:"
  echo "1. API token expired or revoked"
  echo "2. Email address incorrect"
  echo "3. Domain incorrect (check: $JIRA_DOMAIN)"
  echo "4. Account lacks permissions (need: project admin or issue create/edit)"
  echo ""
  echo "Please verify credentials:"
  echo "https://id.atlassian.com/manage-profile/security/api-tokens"
fi

# If API call fails with 403 Forbidden
if [ $? -eq 403 ]; then
  echo "❌ JIRA permission denied"
  echo ""
  echo "Your account lacks permissions for this operation."
  echo "Required permissions:"
  echo "- Browse projects"
  echo "- Create issues"
  echo "- Edit issues"
  echo "- Administer projects (for Epic creation)"
  echo ""
  echo "Contact your JIRA administrator."
fi
```

### Step 8: Production Recommendations

**For production deployments, use OAuth 2.0** instead of API tokens:

**Why OAuth 2.0?**
- ✅ More secure (no long-lived credentials)
- ✅ Fine-grained permissions (scopes)
- ✅ Automatic token refresh
- ✅ Audit trail in JIRA

**How to set up OAuth 2.0**:
1. Go to: https://developer.atlassian.com/console/myapps/
2. Create a new app
3. Configure OAuth 2.0 credentials
4. Add required scopes (read:jira-work, write:jira-work)
5. Use OAuth flow instead of API token

**For self-hosted JIRA**: Use Personal Access Tokens (PAT) instead of API tokens.

---

## Usage

**Export**: `/sync-jira export 0001`
**Import**: `/sync-jira import PROJ-123`
**Sync**: `/sync-jira sync 0001`

All conversion logic is handled by the `jira-mapper` agent.

---

## Confluence Page Sync

JIRA and Confluence are both Atlassian products and often used together. This skill can also help with Confluence page sync.

### Confluence Credentials

Same authentication pattern as JIRA (Basic Auth with email:api_token):

```bash
# .env (gitignored)
CONFLUENCE_API_TOKEN=your-api-token    # Same as JIRA token works
CONFLUENCE_EMAIL=your-email@example.com
CONFLUENCE_DOMAIN=your-domain.atlassian.net
CONFLUENCE_SPACE_KEY=PROJ
```

### Key Confluence Operations

| Operation | Endpoint | Method |
|-----------|----------|--------|
| Get page | `/wiki/api/v2/pages/{id}?body-format=storage` | GET |
| Update page | `/wiki/api/v2/pages/{id}` | PUT |
| Create page | `/wiki/api/v2/pages` | POST |

### Critical: Version Increment

**Every page update MUST increment the version number**:

```bash
# 1. Get current version
curl -s GET ".../pages/{id}" | jq '.version.number'
# Returns: 5

# 2. Update with version + 1
PUT ".../pages/{id}"
{ "version": { "number": 6 } }
```

**Error if version not incremented**:
```
409 Conflict: "Version must be incremented on update. Current version is: 5"
```

### Reference Documentation

For complete Confluence API details, see:
- [confluence-page-api.md](../../reference/confluence-page-api.md)

### When to Use Confluence Sync

- Sync increment specs to Confluence for stakeholder visibility
- Publish living docs to Confluence wiki
- Sync task completion status to Confluence task lists
- Create Confluence pages for PRDs, HLDs, ADRs
