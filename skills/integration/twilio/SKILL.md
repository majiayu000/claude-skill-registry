---
name: twilio
description: "Send SMS, make calls, and manage phone numbers via the Twilio REST API."
metadata: {"thinkfleetbot":{"emoji":"📞","requires":{"bins":["curl","jq"],"env":["TWILIO_ACCOUNT_SID","TWILIO_AUTH_TOKEN"]}}}
---

# Twilio

Send SMS messages, make voice calls, and manage phone numbers.

## Environment Variables

- `TWILIO_ACCOUNT_SID` - Account SID
- `TWILIO_AUTH_TOKEN` - Auth token

## Send SMS

```bash
curl -s -X POST \
  "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID/Messages.json" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN" \
  --data-urlencode "To=+15551234567" \
  --data-urlencode "From=+15559876543" \
  --data-urlencode "Body=Hello from ThinkFleetBot!" | jq '{sid, status, to, from}'
```

## Make voice call

```bash
curl -s -X POST \
  "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID/Calls.json" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN" \
  --data-urlencode "To=+15551234567" \
  --data-urlencode "From=+15559876543" \
  --data-urlencode "Url=http://demo.twilio.com/docs/voice.xml" | jq '{sid, status, to, from}'
```

## List messages

```bash
curl -s "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID/Messages.json?PageSize=10" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN" | jq '.messages[] | {sid, to, from, body, status, date_sent}'
```

## List phone numbers

```bash
curl -s "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID/IncomingPhoneNumbers.json" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN" | jq '.incoming_phone_numbers[] | {sid, phone_number, friendly_name}'
```

## Get call details

```bash
curl -s "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID/Calls/CALL_SID.json" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN" | jq '{sid, to, from, status, duration, price}'
```

## Notes

- Always confirm before sending SMS or making calls.
- Phone numbers must be in E.164 format (+15551234567).
