---
name: mail-banking
description: >-
  Show bank notifications, transaction alerts, and account activity from email. Use when user asks about bank emails, account notifications, transfer confirmations, or banking activity. Arguments: optional bank name, time range, or transaction type like "transfers", "payments", "top-ups".
disable-model-invocation: false
user-invocable: true
allowed-tools: Bash
metadata:
  openclaw:
    requires:
      bins: [sqlite3, python3]
---

# Mail Banking — Bank Notifications and Account Activity

Filter: **$ARGUMENTS** (default: last 7 days, all banks)

## Step 1: Find bank notification emails
```bash
DB="$HOME/Library/Mail/V10/MailData/Envelope Index"
SINCE=$(($(date +%s) - 604800))  # 7 days

sqlite3 "$DB" "
SELECT datetime(m.date_received,'unixepoch','localtime') as dt,
       s.subject, a.address as sender,
       mb.url, m.ROWID
FROM messages m
JOIN subjects  s  ON m.subject = s.ROWID
JOIN addresses a  ON m.sender  = a.ROWID
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE m.date_received >= ${SINCE}
  AND m.deleted = 0
  AND mb.url NOT LIKE '%Spam%' AND mb.url NOT LIKE '%Trash%'
  AND (
    -- By sender domain
    a.address LIKE '%bank%'
    OR a.address LIKE '%livin%'
    OR a.address LIKE '%bca%'
    OR a.address LIKE '%bri%'
    OR a.address LIKE '%bni%'
    OR a.address LIKE '%mandiri%'
    OR a.address LIKE '%seabank%'
    OR a.address LIKE '%sinarmas%'
    OR a.address LIKE '%wise%'
    OR a.address LIKE '%revolut%'
    OR a.address LIKE '%n26%'
    OR a.address LIKE '%chase%'
    OR a.address LIKE '%paypal%'
    -- By subject
    OR s.subject LIKE '%transfer%'
    OR s.subject LIKE '%transaction%'
    OR s.subject LIKE '%top-up%'
    OR s.subject LIKE '%top up%'
    OR s.subject LIKE '%payment successful%'
    OR s.subject LIKE '%debit%'
    OR s.subject LIKE '%credit%'
    OR s.subject LIKE '%transfer successful%'
    OR s.subject LIKE '%BI Fast%'
    OR s.subject LIKE '%RTGS%'
    OR s.subject LIKE '%QRIS%'
  )
ORDER BY m.date_received DESC;" 2>/dev/null
```

## Step 2: Filter by bank if specified in $ARGUMENTS
If user specifies "mandiri", "BCA", "BRI", etc., add:
```sql
AND (a.address LIKE '%mandiri%' OR s.subject LIKE '%mandiri%')
```

## Step 3: Parse transaction details
```bash
python3 ~/.claude/skills/_mail-shared/parser.py <ROWID1> <ROWID2> ...
```

Extract from body:
- Transaction type (transfer, payment, top-up, withdrawal)
- Amount + currency
- Recipient name and bank
- Sender/source account (masked card/account number)
- Reference/transaction number
- Date and time

## Step 4: Summarize by type
Group: Transfers out | Payments | Top-ups | Incoming | Credit card payments

## Output Format
**Banking Activity — [PERIOD]**

Table per transaction type:
| Time | Type | Amount | To/From | Ref No. |
|---|---|---|---|---|

Total outflow, total inflow, net.
Flag any unusually large single transactions.
Note any failed or pending transactions if subject indicates.
