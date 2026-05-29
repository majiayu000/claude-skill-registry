---
name: mail-subscriptions
description: >-
  Find and list all active subscriptions and recurring charges from email history. Show renewal dates, amounts, and services. Use when user asks about subscriptions, recurring charges, what they're paying for monthly, or wants to audit their subscriptions. Arguments: optional time range to search (default: last 13 months to catch all annual subs).
disable-model-invocation: false
user-invocable: true
allowed-tools: Bash
metadata:
  openclaw:
    requires:
      bins: [sqlite3, python3]
---

# Mail Subscriptions — Recurring Charge Audit

Scanning: **$ARGUMENTS** (default: last 13 months)

## Step 1: Find all subscription/renewal emails
```bash
DB="$HOME/Library/Mail/V10/MailData/Envelope Index"
SINCE=$(($(date +%s) - 34214400))  # 13 months = 396 days

sqlite3 "$DB" "
SELECT datetime(m.date_received,'unixepoch','localtime') as dt,
       s.subject, a.address as sender, a.comment as name,
       mb.url, m.ROWID
FROM messages m
JOIN subjects  s  ON m.subject = s.ROWID
JOIN addresses a  ON m.sender  = a.ROWID
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE m.date_received >= ${SINCE}
  AND m.deleted = 0
  AND mb.url NOT LIKE '%Spam%' AND mb.url NOT LIKE '%Trash%'
  AND (
    s.subject LIKE '%subscription%'
    OR s.subject LIKE '%renewal%'
    OR s.subject LIKE '%renew%'
    OR s.subject LIKE '%auto-renew%'
    OR s.subject LIKE '%billing%'
    OR s.subject LIKE '%monthly%'
    OR s.subject LIKE '%annual%'
    OR s.subject LIKE '%your plan%'
    OR s.subject LIKE '%membership%'
    OR s.subject LIKE '%your invoice%'
    OR s.subject LIKE '%receipt for%'
    OR s.subject LIKE '%charged%'
    OR s.subject LIKE '%continued%'
    OR s.subject LIKE '%successfully renewed%'
  )
ORDER BY m.date_received DESC;" 2>/dev/null
```

## Step 2: Group by sender/service to find recurring patterns
```bash
sqlite3 "$DB" "
SELECT a.address, a.comment, COUNT(*) as occurrences,
       MIN(datetime(m.date_received,'unixepoch','localtime')) as first_charge,
       MAX(datetime(m.date_received,'unixepoch','localtime')) as last_charge
FROM messages m
JOIN subjects  s  ON m.subject = s.ROWID
JOIN addresses a  ON m.sender  = a.ROWID
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE m.date_received >= ${SINCE}
  AND m.deleted = 0
  AND (s.subject LIKE '%subscription%' OR s.subject LIKE '%renewal%'
       OR s.subject LIKE '%receipt%' OR s.subject LIKE '%invoice%'
       OR s.subject LIKE '%billing%' OR s.subject LIKE '%charged%')
GROUP BY a.address
HAVING COUNT(*) >= 1
ORDER BY occurrences DESC;" 2>/dev/null
```

## Step 3: Parse amounts and cycle from email bodies
```bash
python3 ~/.claude/skills/_mail-shared/parser.py <ROWID1> <ROWID2> ...
```

From bodies, extract:
- Amount (and currency)
- Next renewal date if mentioned
- Plan name/tier
- Cancel URL if present

## Step 4: Infer billing cycle
From occurrence count and date spread:
- 1 charge in 13 months → annual
- ~12 charges in 13 months → monthly
- ~3-4 charges → quarterly

## Output Format
**Your Subscriptions (inferred from email)**

| Service | Cycle | Amount | Last Charged | Next Due |
|---|---|---|---|---|

Group by: Monthly | Annual | Unknown cycle

Total monthly spend (annualize annual charges for comparison).
Flag: subscriptions not charged in >14 months (possibly cancelled).
Flag: any subscription with price changes between charges.
Offer to find cancel links for any service.
