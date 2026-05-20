---
description: Check email blacklist status and manage blacklisted emails
---

## User Input

```text
$ARGUMENTS
```

Format: email address to check, or `list` to show all blacklisted emails

## Task

Check if an email is blacklisted or list all blacklisted emails with expiry dates.

### Steps

1. **Parse Arguments**:
   ```bash
   if [ "${ARGUMENTS}" = "list" ]; then
       ACTION="list"
   elif [ -n "${ARGUMENTS}" ]; then
       ACTION="check"
       EMAIL="${ARGUMENTS}"
   else
       echo "Usage: /check-blacklist <email> or /check-blacklist list"
       exit 1
   fi
   ```

2. **Check Single Email**:
   ```bash
   if [ "${ACTION}" = "check" ]; then
       cd backend
       python -c "
       from src.models.email_blacklist import EmailBlacklist
       from src.lib.email_utils import normalize_email
       from src.lib.database import SessionLocal
       from datetime import datetime

       email = '${EMAIL}'
       normalized = normalize_email(email)

       db = SessionLocal()
       blacklist_entry = db.query(EmailBlacklist).filter_by(
           normalized_email=normalized
       ).first()

       if blacklist_entry:
           days_remaining = (blacklist_entry.expires_at - datetime.utcnow()).days
           print(f'❌ Email is BLACKLISTED')
           print(f'   Normalized: {normalized}')
           print(f'   Reason: {blacklist_entry.reason}')
           print(f'   Blacklisted: {blacklist_entry.created_at}')
           print(f'   Expires: {blacklist_entry.expires_at}')
           print(f'   Days remaining: {days_remaining}')
       else:
           print(f'✅ Email is NOT blacklisted')
           print(f'   Normalized: {normalized}')
       "
   fi
   ```

3. **List All Blacklisted Emails**:
   ```bash
   if [ "${ACTION}" = "list" ]; then
       cd backend
       python -c "
       from src.models.email_blacklist import EmailBlacklist
       from src.lib.database import SessionLocal
       from datetime import datetime

       db = SessionLocal()
       entries = db.query(EmailBlacklist).all()

       print(f'📋 Blacklisted Emails: {len(entries)}')
       print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')

       for entry in entries:
           days_remaining = (entry.expires_at - datetime.utcnow()).days
           status = 'ACTIVE' if days_remaining > 0 else 'EXPIRED'

           print(f'\n{status}: {entry.normalized_email}')
           print(f'   Reason: {entry.reason}')
           print(f'   Created: {entry.created_at.strftime(\"%Y-%m-%d\")}')
           print(f'   Expires: {entry.expires_at.strftime(\"%Y-%m-%d\")} ({days_remaining}d)')

       # Count by reason
       chargebacks = sum(1 for e in entries if e.reason == 'chargeback')
       print(f'\nSummary:')
       print(f'  Chargebacks: {chargebacks}')
       print(f'  Total: {len(entries)}')
       "
   fi
   ```

4. **Check Expiring Soon** (optional):
   ```bash
   python -c "
   from src.models.email_blacklist import EmailBlacklist
   from src.lib.database import SessionLocal
   from datetime import datetime, timedelta

   db = SessionLocal()
   expiring_soon = db.query(EmailBlacklist).filter(
       EmailBlacklist.expires_at < datetime.utcnow() + timedelta(days=7),
       EmailBlacklist.expires_at > datetime.utcnow()
   ).all()

   if expiring_soon:
       print(f'\n⚠️ Expiring within 7 days: {len(expiring_soon)}')
       for entry in expiring_soon:
           days = (entry.expires_at - datetime.utcnow()).days
           print(f'  - {entry.normalized_email} ({days}d)')
   "
   ```

5. **Output Summary**:

   **For Single Check**:
   ```
   ✅ Email Blacklist Check
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Email: user@example.com
   Normalized: user@example.com

   Status: ❌ BLACKLISTED

   Reason: chargeback
   Blacklisted: 2025-11-15
   Expires: 2026-02-13
   Days Remaining: 45

   Note: This email cannot make purchases until expiry.
   ```

   **For List**:
   ```
   📋 Blacklisted Emails Report
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Total: 12 emails

   ACTIVE: fraudster@example.com
     Reason: chargeback
     Created: 2025-11-20
     Expires: 2026-02-18 (51d)

   ACTIVE: abuser@example.com
     Reason: chargeback
     Created: 2025-12-01
     Expires: 2026-03-01 (62d)

   EXPIRED: oldcase@example.com
     Reason: chargeback
     Created: 2025-08-01
     Expires: 2025-10-30 (-31d)

   Summary:
     Chargebacks: 12
     Total: 12

   ⚠️ Expiring within 7 days: 2
     - user1@example.com (3d)
     - user2@example.com (6d)
   ```

## Example Usage

```bash
/check-blacklist user@example.com    # Check specific email
/check-blacklist list                # List all blacklisted emails
```

## Exit Criteria

- Email checked against blacklist
- Blacklist status and details displayed
- Expiry date calculated
- All blacklisted emails listed (if list command)

## Blacklist Policy (FR-P-009)

- **Trigger**: Chargeback received from payment processor
- **Duration**: 90 days from blacklist date
- **Effect**: Prevents checkout via normalized_email lookup
- **Auto-Cleanup**: Expired entries removed by cleanup job
- **Normalization**: Email normalized to prevent bypass (dots/plus tags removed)
