---
name: uni-twilio
description: |
  Twilio SMS messaging via uni CLI. Use when user wants to send SMS, check message status, or list sent messages.
  Requires TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER.
allowed-tools: Bash(uni:*), Bash(~/.local/bin/uni:*)
---

# Twilio (uni)

Send and manage SMS messages from the terminal.

## Authentication

```bash
uni twilio auth <ACCOUNT_SID> <AUTH_TOKEN> -p +15551234567
uni twilio auth --status              # Check configuration
uni twilio auth --logout              # Remove credentials

# Or use environment variables
export TWILIO_ACCOUNT_SID="ACxxx"
export TWILIO_AUTH_TOKEN="xxx"
export TWILIO_PHONE_NUMBER="+15551234567"
```

Get credentials from: https://console.twilio.com

## Send SMS

```bash
uni twilio send +15559876543 "Hello from uni CLI!"
uni twilio send +15559876543 "Meeting at 3pm" -f +15551111111  # Custom from number
```

## List Messages

```bash
uni twilio messages              # List recent messages
uni twilio messages -n 50        # More messages
uni twilio messages SMxxxxxxx    # View specific message details
```

## Notes

- Phone numbers must include country code (+1 for US)
- From number must be a Twilio phone number in your account
- Message SIDs shown in output as `[SMxxx]`
- Status: queued → sent → delivered (or failed)
