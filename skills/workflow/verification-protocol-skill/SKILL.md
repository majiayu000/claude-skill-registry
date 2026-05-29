---
name: verification-protocol
version: 1.0
---

# Verification Protocol SKILL

## 2-Strike Rule

- 2 verifications → Execute
- 3 verifications → HALT

## Background Task Limits

- Max 5 concurrent tasks
- 30-minute timeout

## Real-time Verification

- Read files first (not background tasks)
- Background tasks may have stale state
