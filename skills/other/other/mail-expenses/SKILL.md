---
name: mail-expenses
description: >-
  Extract financial transactions, expenses, receipts, payments, and invoices from email. Summarize spending with amounts, merchants, and categories. Use when user asks about expenses, spending, receipts, payments, or financial transactions from email. Arguments: time range like "last 24 hours", "this month", "last week", or a specific date range.
disable-model-invocation: false
user-invocable: true
allowed-tools: Bash
metadata:
  openclaw:
    requires:
      bins: [sqlite3, python3]
---

# Mail Expenses — Financial Transaction Summary

Period: **$ARGUMENTS** (default: last 24 hours)

## Step 1: Find financial emails

Use SQLite date functions — never compute Unix epochs manually (wrong year risk).

```bash
DB="$HOME/Library/Mail/V10/MailData/Envelope Index"

# Date range from $ARGUMENTS. Use SQLite date expressions directly:
# "yesterday"   → dt >= date('now','-1 day','localtime') AND dt < date('now','localtime')
# "today"       → dt >= date('now','localtime')
# "last 7 days" → dt >= date('now','-7 days','localtime')
# "this month"  → dt >= date('now','start of month','localtime')
# Always print the range before querying so the period is visible in output.

sqlite3 "$DB" "
SELECT datetime(m.date_received,'unixepoch','localtime') as dt,
       s.subject, a.address as sender, mb.url, m.ROWID
FROM messages m
JOIN subjects  s  ON m.subject = s.ROWID
JOIN addresses a  ON m.sender  = a.ROWID
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE datetime(m.date_received,'unixepoch','localtime') >= date('now','-1 day','localtime')
  AND datetime(m.date_received,'unixepoch','localtime') <  date('now','localtime')
  AND m.deleted = 0
  AND mb.url NOT LIKE '%Spam%' AND mb.url NOT LIKE '%Trash%'
  AND mb.url NOT LIKE '%Sent%'
  AND (
    s.subject LIKE '%receipt%'
    OR s.subject LIKE '%invoice%'
    OR s.subject LIKE '%payment%'
    OR s.subject LIKE '%order%'
    OR s.subject LIKE '%purchase%'
    OR s.subject LIKE '%charge%'
    OR s.subject LIKE '%transaction%'
    OR s.subject LIKE '%billing%'
    OR s.subject LIKE '%renewal%'
    OR s.subject LIKE '%subscription%'
    OR s.subject LIKE '%paid%'
    OR s.subject LIKE '%refund%'
    OR s.subject LIKE '%transfer%'
    OR s.subject LIKE '%successful%'
    OR s.subject LIKE '%confirmation%'
    -- Indonesian / multilingual
    OR s.subject LIKE '%bukti%'
    OR s.subject LIKE '%pembayaran%'
    OR s.subject LIKE '%tagihan%'
    OR s.subject LIKE '%transaksi%'
    OR s.subject LIKE '%berhasil%'
    -- Common financial senders
    OR a.address LIKE '%bank%'
    OR a.address LIKE '%paypal%'
    OR a.address LIKE '%stripe%'
    OR a.address LIKE '%xendit%'
    OR a.address LIKE '%livin%'
    OR a.address LIKE '%gopay%'
    OR a.address LIKE '%ovo%'
    OR a.address LIKE '%dana%'
    OR a.address LIKE '%apple%'
    OR a.address LIKE '%google%'
    OR a.address LIKE '%amazon%'
    OR a.address LIKE '%shopee%'
    OR a.address LIKE '%tokopedia%'
    OR a.address LIKE '%grab%'
  )
ORDER BY m.date_received DESC;" 2>/dev/null
```

## Step 2: Parse amounts from email bodies
```bash
python3 ~/.claude/skills/_mail-shared/parser.py <ROWID1> <ROWID2> ...
```

## Step 3: Extract amounts with Python regex
From each parsed body, extract monetary amounts:
```python
import re

patterns = [
    r'(?:Rp|IDR)\s*[\d.,]+',          # Indonesian Rupiah
    r'(?:USD|US\$|\$)\s*[\d.,]+',      # USD
    r'(?:SGD|S\$)\s*[\d.,]+',          # Singapore dollar
    r'Total[:\s]+(?:Rp|IDR|USD|\$|€|£)[\d.,]+',
    r'Amount[:\s]+(?:Rp|IDR|USD|\$|€|£)[\d.,]+',
    r'(?:€|£|¥|₹|RM|THB|PHP|VND)\s*[\d.,]+',
]
```

## Step 4: Categorize transactions
- **Transfers** (bank to bank, BI-Fast, QRIS, virtual account)
- **Bills/Subscriptions** (recurring charges, renewals)
- **Shopping** (e-commerce, marketplace)
- **Food/Lifestyle** (restaurants, delivery, groceries)
- **Travel** (flights, hotels, transport)
- **Refunds** (money coming back)
- **Credit Card Payments** (paying off balances — not new spending)

## Output Format

**Financial Activity — [PERIOD]**

Line-by-line per account (no markdown tables — WhatsApp/Telegram render them as raw text):

💳 **[Bank/Wallet Name]**

HH:MM · [Merchant] · Rp X.XXX

Subtotals by category.
**Total: Rp X.XXX**

Note refunds separately. Flag duplicates and unusually large transactions proactively.
