---
name: manage-accounting
description: Integrate with Xero accounting system to sync transactions, categorize expenses, track revenue, generate invoices, and maintain financial records. Use when syncing bank transactions, categorizing expenses, creating invoices, checking financial status, or when user mentions "accounting", "xero", "expenses", "revenue", "invoice", "financial report", "reconcile".
user-invocable: true
allowed-tools: [Read, Write, Edit, Bash, Glob]
---

# Manage Accounting Skill

Integrates with **Xero** to provide complete financial intelligence - the foundation for autonomous business management and CEO briefings.

---

## Core Responsibilities

1. **Sync Xero Transactions**: Fetch and sync bank/credit card transactions from Xero
2. **Auto-Categorize Expenses**: Intelligently categorize transactions (80%+ accuracy target)
3. **Generate Invoices**: Create professional invoices via Xero API
4. **Bank Reconciliation**: Match transactions with invoices and payments
5. **Financial Reporting**: Update Dashboard with revenue, expenses, cash flow
6. **Cost Optimization**: Identify duplicate subscriptions and unused services

---

## When This Skill Activates

**Trigger phrases:**
- "sync accounting"
- "update xero"
- "categorize expenses"
- "create invoice"
- "financial summary"
- "reconcile transactions"
- "check revenue"
- "expense report"
- "subscription audit"

**Auto-activates when:**
- Scheduled daily sync (e.g., 6:00 AM)
- New transactions detected in Xero
- CEO briefing generation needs financial data
- User requests financial status

---

## Core Workflow

### Phase 1: Xero Transaction Sync

**When:** Daily at 6:00 AM or on-demand

1. **Connect to Xero via MCP Server**
   - Verify Xero MCP server running
   - Check OAuth2 token valid (refresh if needed)
   - Test connection to Xero API

2. **Fetch New Transactions**
   - Get bank/credit card transactions from last sync
   - Query invoices (sent and received)
   - Retrieve payment records
   - Pull contact/vendor information

3. **Write to Vault**
   - Update `Vault/Accounting/Current_Month.md` with new transactions
   - Create individual transaction files in `Vault/Accounting/Transactions/`
   - Filename format: `TRANS_YYYY-MM-DD_[Description].md`
   - Include metadata: date, amount, vendor, category (if already categorized in Xero)

4. **Update Dashboard**
   - Add sync timestamp to `Vault/Dashboard.md`
   - Include transaction count (new expenses, new revenue)
   - Flag any sync errors

**Helper Script:**
```bash
python .claude/skills/manage-accounting/scripts/xero_sync.py [--date-range YYYY-MM-DD:YYYY-MM-DD]
```

See [reference/reconciliation-guide.md](./reference/reconciliation-guide.md) for detailed sync procedures.

---

### Phase 2: Expense Categorization

**When:** After sync or when uncategorized transactions detected

1. **Identify Uncategorized Transactions**
   - Scan `Vault/Accounting/Transactions/` for transactions missing category
   - Check `Vault/Accounting/Current_Month.md` for uncategorized items
   - Priority: Expenses first (revenue usually clear)

2. **Auto-Categorize Using Rules**
   - Load [expense-rules.md](./reference/expense-rules.md)
   - Apply pattern matching (vendor name, description, amount patterns)
   - Check against [xero-categories.md](./reference/xero-categories.md) for valid categories
   - Use [tax-categories.md](./reference/tax-categories.md) for tax treatment

3. **Categorization Logic (80%+ Accuracy Target)**
   - **Subscription Services**: Match vendor name against known subscriptions
     - Adobe, Netflix, Spotify, GitHub, AWS, etc.
     - Category: "Software & Subscriptions" or "Marketing & Advertising"
   - **Recurring Payments**: Identify by amount consistency + vendor
   - **Office Supplies**: Match vendors like Staples, Amazon Business
   - **Professional Services**: Contractors, consultants (look for invoice references)
   - **Travel & Meals**: Airlines, hotels, restaurants (check tax deductibility)

4. **Update Xero via MCP**
   - For high-confidence categorizations (>90%), update directly in Xero
   - For medium-confidence (70-90%), create approval request
   - For low-confidence (<70%), flag for manual review

5. **Update Transaction Files**
   - Add category to transaction metadata
   - Include confidence score
   - Log categorization reasoning

6. **Handle Uncertain Transactions**
   - Create review file in `Vault/Accounting/Needs_Review/`
   - Include similar past transactions for reference
   - Suggest 2-3 possible categories with reasoning

**Helper Script:**
```bash
python .claude/skills/manage-accounting/scripts/categorize_expense.py [--transaction-id ID] [--dry-run]
```

See [expense-rules.md](./reference/expense-rules.md) for complete categorization logic.

---

### Phase 3: Invoice Generation

**When:** User requests invoice or client payment needed

1. **Gather Invoice Details**
   - Check request for: client name, amount, description, date
   - Look up client contact in Xero
   - Reference `Vault/Business_Goals.md` for rates/pricing
   - Use [invoice-templates.md](./reference/invoice-templates.md)

2. **Validate Information**
   - Confirm client exists in Xero contacts
   - Verify amount matches agreed rate/scope
   - Check for duplicate invoices (prevent re-billing)
   - Ensure all required fields present

3. **Create Approval Request**
   - **ALWAYS require approval for invoices**
   - Use `handle-approval` skill to create approval request
   - Include:
     - Client name and contact
     - Invoice amount (line items)
     - Due date
     - Payment terms
     - Preview of invoice (text format)
   - Save approval request in `Vault/Pending_Approval/`

4. **Execute After Approval**
   - Once moved to `Vault/Approved/`, generate invoice in Xero
   - Use Xero MCP to create invoice
   - Capture invoice number and URL
   - Optionally send invoice via email (separate approval)

5. **Update Records**
   - Save invoice copy to `Vault/Accounting/Invoices/INV_[Number]_[Client].pdf`
   - Log to `Vault/Accounting/Current_Month.md`
   - Update Dashboard with invoice sent
   - Track invoice status (unpaid, paid, overdue)

**Helper Script:**
```bash
python .claude/skills/manage-accounting/scripts/generate_invoice.py --client "Client Name" --amount 1500 --description "Services rendered"
```

See [invoice-templates.md](./reference/invoice-templates.md) for template options.

---

### Phase 4: Bank Reconciliation

**When:** Weekly or before CEO briefing generation

1. **Match Transactions**
   - Compare bank transactions with Xero invoices
   - Identify payments received (match invoice amounts)
   - Flag missing payments (overdue invoices)
   - Detect unexpected transactions

2. **Reconcile Expenses**
   - Match expense transactions with receipts/approvals
   - Verify categorizations against bank statements
   - Identify discrepancies

3. **Generate Reconciliation Report**
   - Summary: Total reconciled vs unreconciled
   - List unmatched transactions
   - Overdue invoices report
   - Discrepancies flagging for review

4. **Update Dashboard**
   - Add reconciliation status to `Vault/Dashboard.md`
   - Include outstanding items count
   - Flag high-priority discrepancies

See [reconciliation-guide.md](./reference/reconciliation-guide.md) for detailed procedures.

---

### Phase 5: Financial Reporting & Cost Optimization

**When:** Daily dashboard update or CEO briefing generation

1. **Calculate Financial Metrics**
   - **Revenue:**
     - This week revenue
     - Month-to-date (MTD)
     - vs target from `Vault/Business_Goals.md`
   - **Expenses:**
     - Weekly expenses by category
     - MTD expenses
     - vs budget targets
   - **Cash Flow:**
     - Revenue - Expenses
     - Trend (improving/declining)
   - **Outstanding:**
     - Unpaid invoices total
     - Overdue invoices (>30 days)

2. **Subscription Audit (Cost Optimization)**
   - Identify recurring subscriptions from expense patterns
   - Check usage (cross-reference with other data sources if available)
   - Flag potential savings:
     - No usage in 30+ days
     - Duplicate functionality with other tools
     - Cost increased >20% without notification
   - Generate recommendation for cancellation or negotiation

3. **Update Dashboard**
   - Add financial summary section to `Vault/Dashboard.md`
   - Format:
     ```markdown
     ## Financial Summary (Updated: YYYY-MM-DD HH:MM)
     - **Revenue MTD**: $X,XXX (XX% of $X,XXX target)
     - **Expenses MTD**: $X,XXX (XX% of $X,XXX budget)
     - **Cash Flow**: +/- $X,XXX
     - **Outstanding**: $X,XXX (X invoices)
     - **Alert**: [Any overdue invoices or unusual expenses]
     ```

4. **Proactive Recommendations**
   - If cost optimization opportunity detected, add to Dashboard
   - Example: "Notion: No activity 45 days. Cost: $15/mo → Annual savings: $180"
   - Create note in `Vault/Accounting/Recommendations/`

---

## Security Safeguards

### Before Syncing:
- ✅ Xero MCP server authenticated
- ✅ OAuth2 token valid
- ✅ Network connection stable
- ✅ Vault backup exists

### Before Categorizing:
- ✅ Transaction not already categorized
- ✅ Category exists in Xero chart of accounts
- ✅ Confidence threshold met (or approval requested)
- ✅ Tax treatment correct

### Before Creating Invoice:
- ✅ **ALWAYS require approval** (no auto-invoicing)
- ✅ Client exists in Xero
- ✅ Amount validated against rate sheet
- ✅ No duplicate invoice exists
- ✅ All required fields populated

### Never Auto-Execute:
- ❌ Invoice generation (always requires approval)
- ❌ Invoice sending (requires separate approval)
- ❌ Payment processing
- ❌ Subscription cancellations (recommend only)
- ❌ Deleting transactions

---

## Reference Files

**Progressive disclosure - load on demand:**

1. **[xero-categories.md](./reference/xero-categories.md)**
   - Standard Xero chart of accounts
   - Category hierarchy
   - When to use each category
   - Tax implications per category

2. **[expense-rules.md](./reference/expense-rules.md)**
   - Auto-categorization rules (vendor patterns)
   - Confidence scoring logic
   - Special cases and exceptions
   - Rule priority order

3. **[invoice-templates.md](./reference/invoice-templates.md)**
   - Standard invoice templates
   - Template selection logic
   - Required fields per template
   - Customization options

4. **[reconciliation-guide.md](./reference/reconciliation-guide.md)**
   - Step-by-step reconciliation process
   - Matching algorithms
   - Discrepancy handling
   - Reporting format

5. **[tax-categories.md](./reference/tax-categories.md)**
   - Tax treatment by expense type
   - Deductible vs non-deductible
   - GST/VAT handling
   - Documentation requirements

---

## Helper Scripts

### xero_sync.py

**Purpose:** Fetch transactions from Xero and update Vault

**Usage:**
```bash
# Sync today's transactions
python .claude/skills/manage-accounting/scripts/xero_sync.py

# Sync specific date range
python .claude/skills/manage-accounting/scripts/xero_sync.py --date-range 2026-01-01:2026-01-11

# Dry run (preview without writing)
python .claude/skills/manage-accounting/scripts/xero_sync.py --dry-run

# JSON output
python .claude/skills/manage-accounting/scripts/xero_sync.py --json
```

---

### categorize_expense.py

**Purpose:** Auto-categorize transactions using pattern matching

**Usage:**
```bash
# Categorize all uncategorized transactions
python .claude/skills/manage-accounting/scripts/categorize_expense.py

# Categorize specific transaction
python .claude/skills/manage-accounting/scripts/categorize_expense.py --transaction-id TX123

# Dry run (preview categorizations)
python .claude/skills/manage-accounting/scripts/categorize_expense.py --dry-run

# Lower confidence threshold (more aggressive)
python .claude/skills/manage-accounting/scripts/categorize_expense.py --threshold 0.7
```

---

### generate_invoice.py

**Purpose:** Generate invoice draft for approval

**Usage:**
```bash
# Create invoice approval request
python .claude/skills/manage-accounting/scripts/generate_invoice.py \
  --client "Client A" \
  --amount 1500 \
  --description "Consulting services - January 2026"

# Use specific template
python .claude/skills/manage-accounting/scripts/generate_invoice.py \
  --client "Client B" \
  --amount 2500 \
  --template "project-based"

# Include line items from file
python .claude/skills/manage-accounting/scripts/generate_invoice.py \
  --client "Client C" \
  --line-items-file Vault/Projects/ClientC/invoice_items.json
```

---

## Integration with Other Skills

**Skills that use manage-accounting:**
- `generate-ceo-briefing` → Reads financial data for weekly business audit
- `handle-approval` → Executes approved invoices
- `monitor-system` → Checks Xero sync health

**Provides data to:**
- `Vault/Dashboard.md` → Financial summary section
- `Vault/Briefings/` → Revenue/expense data for CEO reports
- `Vault/Accounting/` → Complete financial records

**Workflow:**
```
1. Daily 6:00 AM: xero_sync.py runs automatically
2. New transactions → categorize_expense.py auto-categorizes
3. High-confidence → Update Xero directly
4. Low-confidence → Create review file
5. User requests invoice → generate_invoice.py creates approval
6. Approval granted → Create invoice in Xero
7. Weekly: Reconciliation + cost optimization analysis
8. Sunday: Financial data fed to generate-ceo-briefing
```

---

## Dashboard Logging

All accounting activity logged to `Vault/Dashboard.md`:

```markdown
### [Timestamp] - Accounting Activity

**Xero Sync:**
- Synced: X transactions (X expenses, X revenue)
- Date range: YYYY-MM-DD to YYYY-MM-DD
- Status: Success/Errors

**Expense Categorization:**
- Categorized: X transactions
- Confidence: High (X), Medium (X), Low (X)
- Pending review: X transactions

**Invoice Created:**
- Client: [Client Name]
- Amount: $X,XXX
- Status: Pending Approval
- File: Vault/Pending_Approval/APPROVAL_INVOICE_[...]

**Financial Summary:**
- Revenue MTD: $X,XXX (XX% of target)
- Expenses MTD: $X,XXX
- Cash Flow: +/- $X,XXX
- Outstanding: $X,XXX

**Cost Optimization:**
- Recommendation: [Subscription/service to cancel]
- Potential Savings: $X/month ($X/year)
```

---

## Success Criteria

This skill works correctly when:

✅ Daily Xero sync runs automatically (99%+ success rate)
✅ Transactions correctly synced to Vault
✅ 80%+ auto-categorization accuracy
✅ All invoices require and receive approval
✅ Invoices successfully created in Xero after approval
✅ Financial dashboard updated daily with accurate metrics
✅ Cost optimization recommendations relevant and actionable
✅ Reconciliation reports generated weekly
✅ Zero unauthorized financial actions
✅ Complete audit trail maintained

---

## Common Issues

**Xero MCP Connection Failed:**
- Check MCP server running: `ps aux | grep xero-mcp`
- Verify OAuth2 token not expired
- Test connection: `python scripts/xero_sync.py --test-connection`
- Re-authenticate if needed

**Categorization Low Accuracy (<80%):**
- Review and update [expense-rules.md](./reference/expense-rules.md)
- Add vendor-specific patterns
- Check Xero categories match [xero-categories.md](./reference/xero-categories.md)
- Adjust confidence threshold if too conservative

**Invoice Generation Failed:**
- Verify client exists in Xero contacts
- Check all required fields present
- Ensure no duplicate invoice number
- Review Xero API error logs

**Sync Not Running Daily:**
- Check cron job / Task Scheduler configuration
- Verify orchestrator.py scheduling working
- Check system logs for errors
- Ensure Xero API rate limits not exceeded

**Reconciliation Discrepancies:**
- Verify transaction dates match bank statement
- Check for manual entries in Xero
- Review transaction matching rules
- Ensure all transactions synced

---

## External Dependencies

**Required:**
- Xero account with API access
- Xero MCP Server installed and configured
- OAuth2 credentials configured in Claude Code
- `handle-approval` skill operational

**Optional:**
- Bank account API for enhanced reconciliation
- Receipt scanning for expense verification

---

## Setup Checklist

Before first use:

- [ ] Xero account created and configured
- [ ] Xero MCP Server installed: `npm install -g @xeroapi/xero-mcp-server`
- [ ] OAuth2 credentials obtained from Xero Developer Portal
- [ ] MCP server added to Claude Code config (`.config/claude-code/mcp.json`)
- [ ] Test connection successful
- [ ] Vault folders created: `Accounting/`, `Accounting/Transactions/`, `Accounting/Invoices/`, `Accounting/Expenses/`
- [ ] `Vault/Business_Goals.md` includes financial targets
- [ ] [expense-rules.md](./reference/expense-rules.md) customized for your business
- [ ] [xero-categories.md](./reference/xero-categories.md) matches your Xero chart of accounts
- [ ] Daily sync scheduled (cron/Task Scheduler)

---

*Skill Version: 1.0*
*Last Updated: 2026-01-11*
*Branch: feat/gold-accounting-xero*
*Dependencies: handle-approval, Xero MCP Server*
