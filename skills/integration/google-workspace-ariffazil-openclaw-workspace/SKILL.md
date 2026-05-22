---
name: google-workspace
description: Gmail, Google Calendar, Drive, Sheets via Google APIs
user-invocable: true
---

# Google Workspace Skill — arifOS_bot

Triggers: "gmail", "email", "google calendar", "calendar", "schedule", "google drive",
          "drive", "google sheets", "spreadsheet", "sheets", "google docs", "send email",
          "check calendar", "what's on my calendar", "read email", "upload to drive"

Auth: OAuth 2.0 | Client ID: `26699057...` (already configured at `~/.openclaw/gog/`)

---

## ⚙️ One-Time Setup — Complete OAuth Flow

**Status: Client credentials exist. Access token not yet obtained.**

OAuth credentials are at `~/.openclaw/gog/credentials.json`. Run the flow once to get a token:

```bash
# On VPS host (not inside container):
cd /opt/arifos/data/openclaw/gog

# Install google-auth libraries if not present
pip3 install --quiet google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client 2>/dev/null

# Run auth flow
python3 << 'PYEOF'
from google_auth_oauthlib.flow import InstalledAppFlow
import json

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/calendar.events',
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/spreadsheets',
]

flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
# This prints an auth URL — open it in your browser, approve, paste the code back
creds = flow.run_local_server(port=0)

# Save token
with open('token.json', 'w') as f:
    f.write(creds.to_json())
print("Token saved to token.json")
PYEOF
```

After running, `token.json` will be at `~/.openclaw/gog/token.json` and auto-refreshes.

---

## Gmail

### Read unread emails
```bash
python3 << 'PYEOF'
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('/home/node/.openclaw/gog/token.json')
service = build('gmail', 'v1', credentials=creds)

results = service.users().messages().list(userId='me', q='is:unread', maxResults=10).execute()
messages = results.get('messages', [])
print(f'Unread: {len(messages)} messages')

for msg in messages[:5]:
    m = service.users().messages().get(userId='me', id=msg['id'], format='metadata',
        metadataHeaders=['Subject','From','Date']).execute()
    headers = {h['name']: h['value'] for h in m['payload']['headers']}
    print(f"  From: {headers.get('From','?')}")
    print(f"  Subject: {headers.get('Subject','?')}")
    print(f"  Date: {headers.get('Date','?')}")
    print()
PYEOF
```

### Send email
```bash
python3 << 'PYEOF'
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('/home/node/.openclaw/gog/token.json')
service = build('gmail', 'v1', credentials=creds)

msg = MIMEText("Email body here")
msg['to'] = 'recipient@example.com'
msg['subject'] = 'Subject here'
raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()

result = service.users().messages().send(userId='me', body={'raw': raw}).execute()
print(f"Sent: {result['id']}")
PYEOF
```

---

## Google Calendar

### View upcoming events
```bash
python3 << 'PYEOF'
from datetime import datetime, timezone
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('/home/node/.openclaw/gog/token.json')
service = build('calendar', 'v3', credentials=creds)

now = datetime.now(timezone.utc).isoformat()
events = service.events().list(
    calendarId='primary',
    timeMin=now,
    maxResults=10,
    singleEvents=True,
    orderBy='startTime'
).execute().get('items', [])

print(f"Next {len(events)} events:")
for e in events:
    start = e['start'].get('dateTime', e['start'].get('date'))
    print(f"  {start} — {e.get('summary','(no title)')}")
PYEOF
```

### Create calendar event
```bash
python3 << 'PYEOF'
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('/home/node/.openclaw/gog/token.json')
service = build('calendar', 'v3', credentials=creds)

event = {
    'summary': 'Event Title',
    'description': 'Description',
    'start': {'dateTime': '2026-03-08T10:00:00+08:00', 'timeZone': 'Asia/Kuala_Lumpur'},
    'end':   {'dateTime': '2026-03-08T11:00:00+08:00', 'timeZone': 'Asia/Kuala_Lumpur'},
}
result = service.events().insert(calendarId='primary', body=event).execute()
print(f"Created: {result.get('htmlLink')}")
PYEOF
```

---

## Google Drive

### List files
```bash
python3 << 'PYEOF'
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('/home/node/.openclaw/gog/token.json')
service = build('drive', 'v3', credentials=creds)

files = service.files().list(
    pageSize=15,
    fields='files(id,name,mimeType,modifiedTime)',
    orderBy='modifiedTime desc'
).execute().get('files', [])

for f in files:
    print(f"{f['modifiedTime'][:10]} | {f['mimeType'].split('.')[-1]:20} | {f['name']}")
PYEOF
```

### Search Drive
```bash
python3 -c "
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import sys

query = sys.argv[1] if len(sys.argv) > 1 else 'arifOS'
creds = Credentials.from_authorized_user_file('/home/node/.openclaw/gog/token.json')
service = build('drive', 'v3', credentials=creds)
files = service.files().list(q=f\"name contains '{query}'\", fields='files(id,name,webViewLink)').execute().get('files',[])
for f in files: print(f['name'], '→', f.get('webViewLink',''))
" -- "search term"
```

---

## Google Sheets

### Read spreadsheet
```bash
python3 << 'PYEOF'
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SHEET_ID = 'YOUR_SPREADSHEET_ID'  # from URL: /spreadsheets/d/SHEET_ID/
RANGE = 'Sheet1!A1:E20'

creds = Credentials.from_authorized_user_file('/home/node/.openclaw/gog/token.json')
service = build('sheets', 'v4', credentials=creds)
result = service.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=RANGE).execute()
rows = result.get('values', [])
for row in rows:
    print('\t'.join(row))
PYEOF
```

### Append row to sheet
```bash
python3 << 'PYEOF'
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SHEET_ID = 'YOUR_SPREADSHEET_ID'
creds = Credentials.from_authorized_user_file('/home/node/.openclaw/gog/token.json')
service = build('sheets', 'v4', credentials=creds)

values = [[datetime.now().strftime('%Y-%m-%d %H:%M'), 'New row', 'data here']]
service.spreadsheets().values().append(
    spreadsheetId=SHEET_ID,
    range='Sheet1',
    valueInputOption='USER_ENTERED',
    body={'values': values}
).execute()
print("Row appended")
PYEOF
```

---

## Notes

- Token auto-refreshes via `google-auth` library (no re-auth needed unless revoked)
- Timezone: Always use `Asia/Kuala_Lumpur` for Malaysian calendar events
- Scopes requested: gmail read+send, calendar read+write, drive read, sheets read+write
- Token lives at `~/.openclaw/gog/token.json` (gitignored — never commit)
- F11: Sending email and creating calendar events are high-visibility → state intent clearly

*arifOS_bot — Google Workspace via OAuth 2.0*
