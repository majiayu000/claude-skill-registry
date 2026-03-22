---
name: twilio
description: >
  Manage Twilio SMS service via REST API. Send test messages, check message logs,
  inspect phone numbers, check account balance, and debug SMS delivery issues.
  Use for any SMS/Twilio administration task.
allowed-tools: Bash, Read, Grep, Glob
---

# Twilio REST API

Manage FuzzyCat's SMS delivery via the Twilio API.

## Authentication

```bash
TWILIO_SID=$(grep TWILIO_ACCOUNT_SID .env.local | cut -d'"' -f2)
TWILIO_TOKEN=$(grep TWILIO_AUTH_TOKEN .env.local | cut -d'"' -f2)
TWILIO_PHONE=$(grep TWILIO_PHONE_NUMBER .env.local | cut -d'"' -f2)
# All curl commands use: -u "$TWILIO_SID:$TWILIO_TOKEN"
```

## Common Commands

### Account

```bash
# Account info
curl -s "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_SID.json" \
  -u "$TWILIO_SID:$TWILIO_TOKEN" | python3 -m json.tool

# Account balance
curl -s "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_SID/Balance.json" \
  -u "$TWILIO_SID:$TWILIO_TOKEN" | python3 -m json.tool
```

### Messages

```bash
# List recent messages
curl -s "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_SID/Messages.json?PageSize=10" \
  -u "$TWILIO_SID:$TWILIO_TOKEN" | python3 -m json.tool

# Get specific message
curl -s "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_SID/Messages/SMxxx.json" \
  -u "$TWILIO_SID:$TWILIO_TOKEN" | python3 -m json.tool

# Send a test SMS
curl -s -X POST "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_SID/Messages.json" \
  -u "$TWILIO_SID:$TWILIO_TOKEN" \
  -d "From=$TWILIO_PHONE" \
  -d "To=+1234567890" \
  -d "Body=Test message from FuzzyCat" | python3 -m json.tool

# Filter messages by date
curl -s "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_SID/Messages.json?DateSent>=2026-03-01&PageSize=20" \
  -u "$TWILIO_SID:$TWILIO_TOKEN" | python3 -m json.tool
```

### Phone Numbers

```bash
# List owned phone numbers
curl -s "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_SID/IncomingPhoneNumbers.json" \
  -u "$TWILIO_SID:$TWILIO_TOKEN" | python3 -m json.tool

# Get phone number capabilities
curl -s "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_SID/IncomingPhoneNumbers.json" \
  -u "$TWILIO_SID:$TWILIO_TOKEN" | python3 -c "
import sys,json
d=json.load(sys.stdin)
for n in d.get('incoming_phone_numbers',[]):
    print(f\"{n['phone_number']} | SMS: {n['capabilities']['sms']} | Voice: {n['capabilities']['voice']}\")
"
```

### Usage

```bash
# Usage records (current billing period)
curl -s "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_SID/Usage/Records.json?Category=sms" \
  -u "$TWILIO_SID:$TWILIO_TOKEN" | python3 -m json.tool
```

## FuzzyCat-Specific

- **Phone number**: `+17744971520`
- **Used for**: Payment reminders, default notifications (future)
- **Key files**: `lib/twilio.ts`, SMS-related services
- **Not yet heavily used** — SMS features are planned but limited currently
