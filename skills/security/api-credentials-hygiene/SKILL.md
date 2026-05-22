---
name: api-credentials-hygiene
version: 1.0.0
description: Audit and maintain API credential security and rotation schedules.
metadata:
  openclaw:
    emoji: 🔐
    category: security
---

# API Credentials Hygiene

Audit and maintain API credential security and rotation schedules.

## Checks

- [ ] No credentials in git history
- [ ] Files have 600 permissions
- [ ] No plaintext env files
- [ ] Rotation dates tracked
- [ ] Expiration alerts set

## Workflow

1. Scan for exposed credentials
2. Check file permissions
3. Verify rotation schedule
4. Alert on upcoming expirations
