---
name: google-calendar-sync
description: Wizard to set up Google Calendar API integration with service account authentication and domain-wide delegation
license: MIT
compatibility: opencode
metadata:
  category: integration
  provider: google
  requires-human: "true"
---

# Google Calendar Sync Setup Wizard

This skill guides you through configuring a Google Cloud service account to sync events with Google Calendar. It uses `gcloud` CLI to automate most Google Cloud steps.

## How This Works

This is a **guided wizard** with two types of steps:

- **AGENT ACTION** - Steps the agent performs automatically via `gcloud` CLI or code
- **HUMAN ACTION REQUIRED** - Steps requiring manual intervention (browser auth, Admin Console)

## State Detection

**AGENT ACTION** - Run this at the start to determine current progress:

```bash
echo "=== GOOGLE CALENDAR SYNC STATE CHECK ==="

# Check 1: gcloud installed?
if command -v gcloud &> /dev/null; then
  echo "gcloud: INSTALLED"
else
  echo "gcloud: MISSING -> Start at Step 0.1"
fi

# Check 2: gcloud authenticated?
if gcloud auth list --filter="status:ACTIVE" --format="value(account)" 2>/dev/null | grep -q "@"; then
  echo "gcloud_auth: AUTHENTICATED as $(gcloud auth list --filter='status:ACTIVE' --format='value(account)' | head -1)"
else
  echo "gcloud_auth: NOT_AUTHENTICATED -> Complete Step 0.2"
fi

# Check 3: Project configured?
PROJECT=$(gcloud config get-value project 2>/dev/null)
if [ -n "$PROJECT" ] && [ "$PROJECT" != "(unset)" ]; then
  echo "project: CONFIGURED as $PROJECT"
else
  echo "project: NOT_SET -> Start at Phase 2"
fi

# Check 4: Calendar API enabled?
if [ -n "$PROJECT" ] && [ "$PROJECT" != "(unset)" ]; then
  if gcloud services list --enabled --filter="name:calendar" --format="value(name)" 2>/dev/null | grep -q "calendar"; then
    echo "calendar_api: ENABLED"
  else
    echo "calendar_api: NOT_ENABLED -> Complete Step 2.2"
  fi
fi

# Check 5: Service account exists?
if [ -n "$PROJECT" ] && [ "$PROJECT" != "(unset)" ]; then
  SA_EMAIL="calendar-sync@${PROJECT}.iam.gserviceaccount.com"
  if gcloud iam service-accounts describe "$SA_EMAIL" &>/dev/null; then
    echo "service_account: EXISTS ($SA_EMAIL)"
  else
    echo "service_account: NOT_FOUND -> Complete Step 2.3"
  fi
fi

# Check 6: Credentials file exists?
if [ -f "google-credentials.json" ]; then
  echo "credentials_file: EXISTS (needs base64 encoding)"
elif [ -f "google-credentials.b64" ]; then
  echo "credentials_b64: EXISTS"
else
  echo "credentials: NOT_FOUND -> Complete Step 2.5"
fi

# Check 7: Environment variables?
echo "=== ENV VAR CHECK ==="
if [ -f ".env.local" ]; then
  grep -q "GOOG_CREDENTIALS_JSON" .env.local 2>/dev/null && echo "GOOG_CREDENTIALS_JSON: SET in .env.local" || echo "GOOG_CREDENTIALS_JSON: MISSING"
  grep -q "GOOG_CALENDAR_IMPERSONATE_USER" .env.local 2>/dev/null && echo "GOOG_CALENDAR_IMPERSONATE_USER: SET in .env.local" || echo "GOOG_CALENDAR_IMPERSONATE_USER: MISSING"
  grep -q "GOOG_CALENDAR_ID" .env.local 2>/dev/null && echo "GOOG_CALENDAR_ID: SET in .env.local" || echo "GOOG_CALENDAR_ID: MISSING"
elif [ -f ".env" ]; then
  grep -q "GOOG_CREDENTIALS_JSON" .env 2>/dev/null && echo "GOOG_CREDENTIALS_JSON: SET in .env" || echo "GOOG_CREDENTIALS_JSON: MISSING"
  grep -q "GOOG_CALENDAR_IMPERSONATE_USER" .env 2>/dev/null && echo "GOOG_CALENDAR_IMPERSONATE_USER: SET in .env" || echo "GOOG_CALENDAR_IMPERSONATE_USER: MISSING"
  grep -q "GOOG_CALENDAR_ID" .env 2>/dev/null && echo "GOOG_CALENDAR_ID: SET in .env" || echo "GOOG_CALENDAR_ID: MISSING"
else
  echo "env_file: NOT_FOUND -> Complete Phase 5"
fi

# Check 8: googleapis package?
if [ -f "package.json" ]; then
  grep -q "googleapis" package.json && echo "googleapis: INSTALLED" || echo "googleapis: NOT_INSTALLED -> Complete Step 5.4"
fi

echo "=== END STATE CHECK ==="
```

Based on the state check output, skip to the appropriate phase or step.

---

## Prerequisites (Agent Checks + Human Installs)

The agent will check for required tools and guide you through installing anything that's missing.

### Step 0.1: Check for gcloud CLI

**AGENT ACTION** - Run this check:

```bash
if command -v gcloud &> /dev/null; then
  echo "INSTALLED: gcloud $(gcloud --version 2>/dev/null | head -1)"
else
  echo "NOT_INSTALLED: gcloud"
fi
```

**If NOT_INSTALLED:**

> **HUMAN ACTION REQUIRED**
>
> Install the Google Cloud CLI:
>
> **macOS (Homebrew):**
> ```bash
> brew install google-cloud-sdk
> ```
>
> **macOS (Manual):**
> ```bash
> curl https://sdk.cloud.google.com | bash
> exec -l $SHELL
> ```
>
> **Linux (Debian/Ubuntu):**
> ```bash
> sudo apt-get install apt-transport-https ca-certificates gnupg curl
> curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
> echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
> sudo apt-get update && sudo apt-get install google-cloud-cli
> ```
>
> **Linux (Other):**
> ```bash
> curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz
> tar -xf google-cloud-cli-linux-x86_64.tar.gz
> ./google-cloud-sdk/install.sh
> ```
>
> **Windows:**
> Download installer from: https://cloud.google.com/sdk/docs/install
>
> Reply "gcloud installed" when complete.

### Step 0.2: Check gcloud authentication

**AGENT ACTION** - Run this check:

```bash
if gcloud auth list --filter="status:ACTIVE" --format="value(account)" 2>/dev/null | head -1 | grep -q "@"; then
  echo "AUTHENTICATED: $(gcloud auth list --filter='status:ACTIVE' --format='value(account)' | head -1)"
else
  echo "NOT_AUTHENTICATED"
fi
```

**If NOT_AUTHENTICATED:**

> **HUMAN ACTION REQUIRED**
>
> Authenticate with your Google account:
>
> ```bash
> gcloud auth login
> ```
>
> This will open a browser window. Sign in with the Google account that has access to your Google Cloud projects.
>
> Reply "authenticated" when complete.

### Step 0.3: Check for Node.js (for testing)

**AGENT ACTION** - Run this check:

```bash
if command -v node &> /dev/null; then
  echo "INSTALLED: node $(node --version)"
else
  echo "NOT_INSTALLED: node"
fi
```

**If NOT_INSTALLED:**

> **HUMAN ACTION REQUIRED**
>
> Install Node.js (required for the googleapis package and testing):
>
> **macOS:**
> ```bash
> brew install node
> ```
>
> **Linux:**
> ```bash
> curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
> sudo apt-get install -y nodejs
> ```
>
> Or use nvm: https://github.com/nvm-sh/nvm
>
> Reply "node installed" when complete.

### Step 0.4: Check for pnpm (optional, for monorepos)

**AGENT ACTION** - Run this check:

```bash
if command -v pnpm &> /dev/null; then
  echo "INSTALLED: pnpm $(pnpm --version)"
elif command -v npm &> /dev/null; then
  echo "FALLBACK: npm $(npm --version)"
else
  echo "NOT_INSTALLED: package manager"
fi
```

The skill will use `pnpm` if available, otherwise `npm`.

---

## Phase 1: Project Discovery (Agent Actions)

### Step 1.1: Check existing Google credentials

```bash
# Check .env files for existing Google config
grep -r "GOOG_" .env* 2>/dev/null || echo "No existing Google config found"
grep -r "GOOGLE_" .env* 2>/dev/null || echo "No existing Google config found"
```

### Step 1.2: List existing gcloud projects

```bash
gcloud projects list --format="table(projectId,name,createTime)"
```

Ask user: **Use an existing project or create a new one?**

---

## Phase 2: Google Cloud Setup (Mostly Automated)

### Step 2.1: Create or select project

**AGENT ACTION** - Create new project:

```bash
# Generate a unique project ID
PROJECT_ID="calendar-sync-$(date +%s | tail -c 7)"
PROJECT_NAME="Calendar Sync"

gcloud projects create "$PROJECT_ID" --name="$PROJECT_NAME"
gcloud config set project "$PROJECT_ID"
```

Or select existing:

```bash
gcloud config set project YOUR_PROJECT_ID
```

### Step 2.2: Enable Google Calendar API

**AGENT ACTION**

```bash
gcloud services enable calendar-json.googleapis.com
```

Verify it's enabled:

```bash
gcloud services list --enabled --filter="name:calendar"
```

### Step 2.3: Create service account

**AGENT ACTION**

```bash
SERVICE_ACCOUNT_NAME="calendar-sync"
PROJECT_ID=$(gcloud config get-value project)

gcloud iam service-accounts create "$SERVICE_ACCOUNT_NAME" \
  --display-name="Calendar Sync Service" \
  --description="Manages calendar events for the application"
```

Get the service account email:

```bash
SERVICE_ACCOUNT_EMAIL="${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
echo "Service Account: $SERVICE_ACCOUNT_EMAIL"
```

### Step 2.4: Grant permissions to service account

**AGENT ACTION**

```bash
PROJECT_ID=$(gcloud config get-value project)
SERVICE_ACCOUNT_EMAIL="calendar-sync@${PROJECT_ID}.iam.gserviceaccount.com"

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
  --role="roles/owner"
```

### Step 2.5: Create service account key

**AGENT ACTION** (may require org policy override)

```bash
PROJECT_ID=$(gcloud config get-value project)
SERVICE_ACCOUNT_EMAIL="calendar-sync@${PROJECT_ID}.iam.gserviceaccount.com"

gcloud iam service-accounts keys create ./google-credentials.json \
  --iam-account="$SERVICE_ACCOUNT_EMAIL"
```

If this fails with "Key creation is not allowed":

**HUMAN ACTION REQUIRED**

Disable the org policy constraint:

```bash
# Requires org admin permissions
gcloud org-policies reset iam.disableServiceAccountKeyCreation --project="$PROJECT_ID"
```

Or do it via Console: [Organization Policies](https://console.cloud.google.com/iam-admin/orgpolicies) > search `iam.disableServiceAccountKeyCreation` > Override > Not enforced.

Then retry the key creation command.

### Step 2.6: Base64 encode the credentials

**AGENT ACTION**

```bash
# Encode and display (copy this for GOOG_CREDENTIALS_JSON)
cat google-credentials.json | base64 -w 0
echo ""

# Or save to a file
cat google-credentials.json | base64 -w 0 > google-credentials.b64
```

### Step 2.7: Get the Client ID (for domain-wide delegation)

**AGENT ACTION**

```bash
PROJECT_ID=$(gcloud config get-value project)
SERVICE_ACCOUNT_EMAIL="calendar-sync@${PROJECT_ID}.iam.gserviceaccount.com"

gcloud iam service-accounts describe "$SERVICE_ACCOUNT_EMAIL" \
  --format="value(uniqueId)"
```

Save this Client ID for the next phase.

---

## Phase 3: Domain-Wide Delegation (Human Action Required)

> **Note:** Only required for Google Workspace. Skip if using personal Gmail with calendar sharing.

### Step 3.1: Configure Domain-Wide Delegation

**HUMAN ACTION REQUIRED** - This cannot be automated via CLI.

1. Go to [Google Admin Console](https://admin.google.com)
2. Navigate to **Security > Access and data control > API controls**
3. Click **Manage Domain Wide Delegation**
4. Click **Add new**
5. Enter the **Client ID** from Step 2.7
6. Add OAuth scope:
   ```
   https://www.googleapis.com/auth/calendar.events
   ```
7. Click **Authorize**

**Confirm:** Reply "Delegation configured" when complete.

### Step 3.2: Identify Impersonation User

**HUMAN ACTION REQUIRED**

Provide the email of a Google Workspace user who has access to the target calendar.
This will be `GOOG_CALENDAR_IMPERSONATE_USER`.

---

## Phase 4: Get Calendar ID (Agent + Human)

### Step 4.1: Find the calendar ID

**Option A - Primary calendar:** The calendar ID is the user's email address.

**Option B - Shared/secondary calendar:**

**HUMAN ACTION REQUIRED**

1. Open [Google Calendar](https://calendar.google.com)
2. Find your calendar in the left sidebar
3. Click the three dots > **Settings and sharing**
4. Scroll to **Integrate calendar**
5. Copy the **Calendar ID** (looks like `abc123@group.calendar.google.com`)

---

## Phase 5: Environment Configuration (Agent Actions)

### Step 5.1: Add environment variables

```bash
# Read the base64 credentials
CREDS_B64=$(cat google-credentials.json | base64 -w 0)

# Append to .env.local (or .env)
cat >> .env.local << EOF

# Google Calendar Integration
GOOG_CREDENTIALS_JSON="$CREDS_B64"
GOOG_CALENDAR_IMPERSONATE_USER="user@yourdomain.com"
GOOG_CALENDAR_ID="calendar-id@group.calendar.google.com"
EOF
```

### Step 5.2: Add to .env.example

```bash
cat >> .env.example << 'EOF'

# Google Calendar Integration
# See: .opencode/skill/google-calendar-sync/SKILL.md
GOOG_CREDENTIALS_JSON=
GOOG_CALENDAR_IMPERSONATE_USER=
GOOG_CALENDAR_ID=
EOF
```

### Step 5.3: Add google-credentials.json to .gitignore

```bash
echo "google-credentials.json" >> .gitignore
echo "google-credentials.b64" >> .gitignore
```

### Step 5.4: Install googleapis package

**AGENT ACTION** - Use detected package manager:

```bash
# Detect and use the right package manager
if command -v pnpm &> /dev/null; then
  pnpm add googleapis
elif command -v yarn &> /dev/null; then
  yarn add googleapis
else
  npm install googleapis
fi
```

### Step 5.5: Create calendar utility module

Create `lib/google-calendar.ts`:

```typescript
import { google } from 'googleapis'

function getCalendarClient() {
  const credentials = JSON.parse(
    Buffer.from(process.env.GOOG_CREDENTIALS_JSON!, 'base64').toString()
  )

  const auth = new google.auth.GoogleAuth({
    credentials,
    scopes: ['https://www.googleapis.com/auth/calendar.events'],
    clientOptions: {
      subject: process.env.GOOG_CALENDAR_IMPERSONATE_USER,
    },
  })

  return google.calendar({ version: 'v3', auth })
}

export async function createCalendarEvent(event: {
  summary: string
  description?: string
  start: Date
  end: Date
  location?: string
}) {
  const calendar = getCalendarClient()
  const calendarId = process.env.GOOG_CALENDAR_ID!

  return calendar.events.insert({
    calendarId,
    requestBody: {
      summary: event.summary,
      description: event.description,
      location: event.location,
      start: {
        dateTime: event.start.toISOString(),
        timeZone: 'UTC',
      },
      end: {
        dateTime: event.end.toISOString(),
        timeZone: 'UTC',
      },
    },
  })
}

export async function updateCalendarEvent(
  eventId: string,
  event: {
    summary?: string
    description?: string
    start?: Date
    end?: Date
    location?: string
  }
) {
  const calendar = getCalendarClient()
  const calendarId = process.env.GOOG_CALENDAR_ID!

  return calendar.events.patch({
    calendarId,
    eventId,
    requestBody: {
      ...(event.summary && { summary: event.summary }),
      ...(event.description && { description: event.description }),
      ...(event.location && { location: event.location }),
      ...(event.start && {
        start: { dateTime: event.start.toISOString(), timeZone: 'UTC' },
      }),
      ...(event.end && {
        end: { dateTime: event.end.toISOString(), timeZone: 'UTC' },
      }),
    },
  })
}

export async function deleteCalendarEvent(eventId: string) {
  const calendar = getCalendarClient()
  const calendarId = process.env.GOOG_CALENDAR_ID!

  return calendar.events.delete({
    calendarId,
    eventId,
  })
}

export async function listCalendarEvents(options?: {
  timeMin?: Date
  timeMax?: Date
  maxResults?: number
}) {
  const calendar = getCalendarClient()
  const calendarId = process.env.GOOG_CALENDAR_ID!

  return calendar.events.list({
    calendarId,
    timeMin: options?.timeMin?.toISOString(),
    timeMax: options?.timeMax?.toISOString(),
    maxResults: options?.maxResults ?? 10,
    singleEvents: true,
    orderBy: 'startTime',
  })
}
```

---

## Phase 6: Verification (Agent Actions)

### Step 6.1: Verify environment variables are set

**AGENT ACTION** - Check required env vars:

```bash
echo "=== VERIFYING ENV VARS ==="

# Source the env file to check
if [ -f ".env.local" ]; then
  source .env.local 2>/dev/null
elif [ -f ".env" ]; then
  source .env 2>/dev/null
fi

MISSING=""
[ -z "$GOOG_CREDENTIALS_JSON" ] && MISSING="$MISSING GOOG_CREDENTIALS_JSON"
[ -z "$GOOG_CALENDAR_IMPERSONATE_USER" ] && MISSING="$MISSING GOOG_CALENDAR_IMPERSONATE_USER"
[ -z "$GOOG_CALENDAR_ID" ] && MISSING="$MISSING GOOG_CALENDAR_ID"

if [ -n "$MISSING" ]; then
  echo "MISSING ENV VARS:$MISSING"
  echo "Please complete Phase 5 before testing."
  exit 1
else
  echo "All required env vars are set!"
fi
```

### Step 6.2: Test the connection

**AGENT ACTION** - Run connection test:

```bash
# Load env vars first
if [ -f ".env.local" ]; then
  export $(grep -v '^#' .env.local | xargs)
elif [ -f ".env" ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Quick Node.js test script
node -e "
const { google } = require('googleapis');

if (!process.env.GOOG_CREDENTIALS_JSON) {
  console.error('ERROR: GOOG_CREDENTIALS_JSON not set');
  process.exit(1);
}

const creds = JSON.parse(Buffer.from(process.env.GOOG_CREDENTIALS_JSON, 'base64').toString());
const auth = new google.auth.GoogleAuth({
  credentials: creds,
  scopes: ['https://www.googleapis.com/auth/calendar.events'],
  clientOptions: { subject: process.env.GOOG_CALENDAR_IMPERSONATE_USER }
});
const calendar = google.calendar({ version: 'v3', auth });

console.log('Testing connection to calendar:', process.env.GOOG_CALENDAR_ID);
console.log('Impersonating user:', process.env.GOOG_CALENDAR_IMPERSONATE_USER);

calendar.events.list({
  calendarId: process.env.GOOG_CALENDAR_ID,
  maxResults: 5,
  timeMin: new Date().toISOString(),
  singleEvents: true,
  orderBy: 'startTime'
}).then(r => {
  console.log('SUCCESS! Connection working.');
  console.log('Found', r.data.items?.length || 0, 'upcoming events');
  if (r.data.items?.length > 0) {
    console.log('Next event:', r.data.items[0].summary);
  }
}).catch(e => {
  console.error('ERROR:', e.message);
  if (e.message.includes('insufficient')) {
    console.error('-> Check domain-wide delegation is configured correctly');
  }
  if (e.message.includes('not found')) {
    console.error('-> Check GOOG_CALENDAR_ID is correct');
  }
  process.exit(1);
});
"
```

**If the test fails**, check the Troubleshooting section below.

### Step 6.2: Cleanup sensitive files

```bash
# Delete the JSON key file (you have it base64-encoded in .env now)
rm -f google-credentials.json google-credentials.b64
```

---

## Troubleshooting

### "Insufficient Permission" errors
- Verify domain-wide delegation uses correct Client ID
- Scope must match exactly: `https://www.googleapis.com/auth/calendar.events`
- Impersonation user must have calendar access

### "Key creation is not allowed"
```bash
gcloud org-policies reset iam.disableServiceAccountKeyCreation --project="$(gcloud config get-value project)"
```

### Find calendar ID via API
```bash
# List all calendars the impersonation user can access
node -e "
const { google } = require('googleapis');
const creds = JSON.parse(Buffer.from(process.env.GOOG_CREDENTIALS_JSON, 'base64').toString());
const auth = new google.auth.GoogleAuth({
  credentials: creds,
  scopes: ['https://www.googleapis.com/auth/calendar.readonly'],
  clientOptions: { subject: process.env.GOOG_CALENDAR_IMPERSONATE_USER }
});
const calendar = google.calendar({ version: 'v3', auth });
calendar.calendarList.list().then(r => {
  r.data.items?.forEach(c => console.log(c.id, '-', c.summary));
}).catch(e => console.error('Error:', e.message));
"
```

---

## Quick Reference: gcloud Commands

```bash
# Auth
gcloud auth login
gcloud auth list

# Projects
gcloud projects list
gcloud projects create PROJECT_ID --name="Name"
gcloud config set project PROJECT_ID

# APIs
gcloud services enable calendar-json.googleapis.com
gcloud services list --enabled

# Service Accounts
gcloud iam service-accounts list
gcloud iam service-accounts create NAME --display-name="Display Name"
gcloud iam service-accounts keys create output.json --iam-account=EMAIL
gcloud iam service-accounts describe EMAIL --format="value(uniqueId)"
```

---

## Checklist

- [ ] `gcloud` CLI installed and authenticated
- [ ] Google Cloud project created/selected
- [ ] Google Calendar API enabled
- [ ] Service account created
- [ ] Service account key generated and base64-encoded
- [ ] Domain-wide delegation configured (Workspace only)
- [ ] Environment variables added to `.env`
- [ ] `googleapis` package installed
- [ ] Calendar utility module created
- [ ] Connection tested
- [ ] Sensitive files cleaned up
