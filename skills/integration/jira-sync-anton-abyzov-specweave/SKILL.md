---
description: Sync guidance for SpecWeave increments with JIRA epics/stories (content SpecWeave→JIRA, status JIRA→SpecWeave). Use when asking about JIRA integration setup or troubleshooting sync. For actual syncing, use /sw-jira:sync command instead.
allowed-tools: Read, Task
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

## CRITICAL: Secrets Required (MANDATORY CHECK)

**BEFORE attempting JIRA sync, CHECK for JIRA credentials.**

**SECURITY RULE**: This skill MUST NOT collect, write, or store credentials. The user configures their own `.env` file. The skill only validates that credentials exist.

### Step 1: Check If Credentials Exist

```bash
# Check .env file for required credentials (existence only — never read values)
if [ -f .env ] && grep -q "^JIRA_API_TOKEN=" .env && grep -q "^JIRA_EMAIL=" .env && grep -q "^JIRA_DOMAIN=" .env; then
  echo "JIRA credentials found in .env"
else
  echo "JIRA credentials missing — see setup instructions below"
  # STOP HERE — do NOT prompt user for secrets
fi
```

### Step 2: If Credentials Missing, Show Setup Instructions

Do NOT ask the user to paste credentials into the chat. Instead, show self-service setup:

```
JIRA credentials are required but not configured.

**Setup (do this yourself — the agent should NOT handle your secrets):**

1. Create an API token at: https://id.atlassian.com/manage-profile/security/api-tokens
2. Add these lines to your project `.env` file:

   JIRA_API_TOKEN=<your-token>
   JIRA_EMAIL=<your-email>
   JIRA_DOMAIN=<your-company>.atlassian.net

3. Ensure `.env` is in `.gitignore`
4. Re-run the sync command

For self-hosted JIRA: Use a Personal Access Token (PAT) and your server's hostname.
```

**IMPORTANT**: After showing instructions, STOP. Do not continue until credentials are configured by the user.

### Step 3: Validate Credential Presence (Not Values)

```bash
# Validate that required keys exist and have non-empty values
# Uses grep -qE to check pattern without reading values into variables
MISSING=()
for KEY in JIRA_API_TOKEN JIRA_EMAIL JIRA_DOMAIN; do
  if ! grep -qE "^${KEY}=.+" .env; then
    MISSING+=("$KEY")
  fi
done

if [ ${#MISSING[@]} -gt 0 ]; then
  echo "Missing or empty credentials: ${MISSING[*]}"
  exit 1
fi
echo "All required credentials present"
```

### Step 4: Domain Validation (Strict)

```bash
# Read domain safely — quote all expansions, take first match only
JIRA_DOMAIN="$(grep '^JIRA_DOMAIN=' .env | head -1 | cut -d '=' -f2-)"

# Reject empty
if [ -z "$JIRA_DOMAIN" ]; then
  echo "Error: JIRA_DOMAIN is empty"
  exit 1
fi

# Reject IP addresses FIRST — IPv4, IPv6 brackets, hex-encoded (SSRF prevention)
if [[ "$JIRA_DOMAIN" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ ]] || [[ "$JIRA_DOMAIN" =~ ^\[.*\]$ ]] || [[ "$JIRA_DOMAIN" =~ ^0x ]]; then
  echo "Error: IP addresses not allowed — use a hostname"
  exit 1
fi

# Reject localhost and internal hostnames
if [[ "$JIRA_DOMAIN" =~ ^(localhost|127\.|10\.|172\.(1[6-9]|2[0-9]|3[01])\.|192\.168\.) ]]; then
  echo "Error: Internal/localhost addresses not allowed"
  exit 1
fi

# Must be a valid hostname — each label: alphanumeric, hyphens allowed mid-label, no consecutive dots
if [[ ! "$JIRA_DOMAIN" =~ ^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?)*$ ]]; then
  echo "Error: JIRA_DOMAIN is not a valid hostname"
  exit 1
fi

# Must end with .atlassian.net for cloud JIRA
# Agent: use AskUserQuestion to confirm non-standard domain before retrying
if [[ ! "$JIRA_DOMAIN" =~ ^[a-zA-Z0-9-]+\.atlassian\.net$ ]]; then
  echo "Error: Domain does not match <subdomain>.atlassian.net pattern"
  exit 1
fi
```

### Step 5: Credential Loading and API Calls

This skill does NOT execute API calls directly (no Bash tool). Credential loading, authentication, and API operations are handled by the `jira-mapper` skill — see its **Security Rules** section for the hardened patterns (domain validation, HTTPS enforcement, SSRF prevention, variable quoting).

### Step 6: Production Recommendations

**For production deployments, use OAuth 2.0** instead of API tokens:

- More secure (no long-lived credentials)
- Fine-grained permissions (scopes)
- Automatic token refresh
- Audit trail in JIRA

**Setup**: https://developer.atlassian.com/console/myapps/ (OAuth 2.0 with scopes: `read:jira-work`, `write:jira-work`)

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

Same authentication and security rules as JIRA — user configures `.env`, skill only validates presence. Same domain validation applies (must be `<subdomain>.atlassian.net`, HTTPS only, no IPs). `CONFLUENCE_DOMAIN` MUST pass the same validation as `JIRA_DOMAIN` (Step 4) before any Confluence API call.

Required `.env` keys (configured by the user, NOT by this skill):
```
CONFLUENCE_API_TOKEN=<your-token>    # Same as JIRA API token
CONFLUENCE_EMAIL=<your-email>
CONFLUENCE_DOMAIN=<your-company>.atlassian.net
CONFLUENCE_SPACE_KEY=<space-key>
```

### Key Confluence Operations

| Operation | Endpoint | Method |
|-----------|----------|--------|
| Get page | `/wiki/api/v2/pages/{id}?body-format=storage` | GET |
| Update page | `/wiki/api/v2/pages/{id}` | PUT |
| Create page | `/wiki/api/v2/pages` | POST |

### Critical: Version Increment

**Every page update MUST increment the version number**:

1. GET current page to retrieve `version.number` (e.g., returns 5)
2. PUT update with `version.number` set to current + 1 (e.g., 6)

If version is not incremented, the API returns `409 Conflict`.

All Confluence API calls follow the same security rules as JIRA (HTTPS only, domain validation, credential handling). See the `jira-mapper` skill's **Security Rules** section for implementation patterns.

### Reference Documentation

For complete Confluence API details, see:
- [confluence-page-api.md](../../reference/confluence-page-api.md)

### When to Use Confluence Sync

- Sync increment specs to Confluence for stakeholder visibility
- Publish living docs to Confluence wiki
- Sync task completion status to Confluence task lists
- Create Confluence pages for PRDs, HLDs, ADRs
