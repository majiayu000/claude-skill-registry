---
name: twilio-sms
description: Twilio SMS and messaging services
allowed-tools: [Bash, Read, WebFetch]
---

# Twilio SMS Skill

## Overview

SMS messaging via Twilio. 90%+ context savings.

## Requirements

- TWILIO_ACCOUNT_SID
- TWILIO_AUTH_TOKEN
- TWILIO_PHONE_NUMBER

## Tools (Progressive Disclosure)

### Messages

| Tool          | Description         | Confirmation |
| ------------- | ------------------- | ------------ |
| send-sms      | Send SMS            | Yes          |
| list-messages | List messages       | No           |
| get-message   | Get message details | No           |

### Phone Numbers

| Tool         | Description         |
| ------------ | ------------------- |
| list-numbers | List phone numbers  |
| lookup       | Lookup phone number |

### Verification

| Tool         | Description             | Confirmation |
| ------------ | ----------------------- | ------------ |
| start-verify | Start verification      | Yes          |
| check-verify | Check verification code | No           |

## Agent Integration

- **developer** (primary): Notification systems
- **devops** (secondary): Alerting
