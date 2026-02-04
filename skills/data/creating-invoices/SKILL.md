---
name: creating-invoices
description: Use this skill when creating invoices, billing clients, tracking payments, or generating financial documents for Support Forge. Generates professional PDF invoices with bank details, payment terms, and line items. Invoke for any client billing, invoice creation, or payment tracking needs.
---

# Invoice Generator

Create professional invoices for Support Forge client work.

## Company Details

```
SUPPORT FORGE LLC
166 Wilson St
Haverhill, MA 01832

EIN: 41-3821756
Email: contact@support-forge.com
Phone: {YOUR_PHONE}
```

## Payment Information

```
PAYMENT METHODS

ACH/Bank Transfer (Preferred):
  Bank: [Your Bank]
  Account Number: 8252968985
  Routing Number: 211370545
  Account Name: Support Forge LLC

Zelle: {YOUR_EMAIL}
Venmo: @{YOUR_HANDLE} (or {YOUR_EMAIL})
```

## Invoice Template

```
╔══════════════════════════════════════════════════════════════╗
║                         INVOICE                              ║
╠══════════════════════════════════════════════════════════════╣
║  SUPPORT FORGE LLC                                           ║
║  166 Wilson St                                               ║
║  Haverhill, MA 01832                                         ║
║  contact@support-forge.com | {YOUR_PHONE}                    ║
║  EIN: 41-3821756                                             ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Invoice #: SF-[YEAR]-[NUMBER]     Date: [DATE]              ║
║  Due Date: [DUE DATE]              Terms: [NET TERMS]        ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║  BILL TO:                                                    ║
║  [Client Name]                                               ║
║  [Company Name]                                              ║
║  [Address]                                                   ║
║  [Email]                                                     ║
╠══════════════════════════════════════════════════════════════╣
║  PROJECT: [Project Name/Description]                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  DESCRIPTION                          QTY    RATE    AMOUNT  ║
║  ─────────────────────────────────────────────────────────── ║
║  [Line item description]               1   $X,XXX   $X,XXX   ║
║  [Line item description]               X   $XXX     $X,XXX   ║
║  [Line item description]               X   $XXX     $X,XXX   ║
║                                                              ║
║  ─────────────────────────────────────────────────────────── ║
║                                        Subtotal:   $X,XXX.XX ║
║                                        Tax (0%):       $0.00 ║
║                                        ─────────────────────  ║
║                                        TOTAL DUE:  $X,XXX.XX ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║  PAYMENT METHODS                                             ║
║  ────────────────                                            ║
║  ACH/Bank Transfer (Preferred):                              ║
║    Account: 8252968985                                       ║
║    Routing: 211370545                                        ║
║                                                              ║
║  Zelle/Venmo: {YOUR_EMAIL}                         ║
╠══════════════════════════════════════════════════════════════╣
║  NOTES                                                       ║
║  [Any additional notes or terms]                             ║
║                                                              ║
║  Thank you for your business!                                ║
╚══════════════════════════════════════════════════════════════╝
```

## Invoice Numbering System

Format: `SF-[YEAR]-[SEQUENTIAL]`

Examples:
- SF-2026-001 (First invoice of 2026)
- SF-2026-002 (Second invoice)
- SF-2026-015 (Fifteenth invoice)

## Payment Terms

| Term | Description | Use Case |
|------|-------------|----------|
| Due on Receipt | Payment due immediately | Small projects, new clients |
| Net 15 | Due within 15 days | Standard projects |
| Net 30 | Due within 30 days | Enterprise clients, retainers |
| 50/50 | 50% upfront, 50% on completion | Large projects |

## Line Item Examples

### AI Enablement Services
```
Referral Support Package                    1    $1,500    $1,500
- Claude Code setup and configuration
- MCP server integration
- Custom skills installation
- Training and documentation

Professional Setup Package                  1    $3,500    $3,500
- Full AI development environment
- Custom integrations
- Extended support
```

### Consulting/Hourly
```
AI Consulting - January 2026               10    $175      $1,750
- Strategy sessions
- Implementation guidance
- Technical support

Additional Development Hours                5     $175        $875
- Custom MCP server development
```

### Website Services
```
Website Development - Phase 1               1    $5,000    $5,000
- Design and development
- Responsive implementation
- CMS setup

Monthly Maintenance - January               1      $750      $750
- Updates and security patches
- Content updates
- Performance monitoring
```

### Retainer
```
Monthly Retainer - January 2026            1    $2,000    $2,000
- Up to 12 hours consulting
- Priority support
- Ongoing maintenance
```

## PDF Generation Script

```python
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.lib import colors
from datetime import datetime, timedelta

def create_invoice(
    invoice_number,
    client_name,
    client_company,
    client_email,
    project_name,
    line_items,  # List of (description, qty, rate)
    terms="Due on Receipt",
    notes=""
):
    output_path = f"SF_Invoice_{invoice_number}.pdf"

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )

    # Colors
    navy = HexColor('#1a365d')
    purple = HexColor('#6366f1')
    light_gray = HexColor('#f5f5f5')

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=navy,
        alignment=TA_CENTER,
        spaceAfter=20
    )

    # Build content
    story = []

    # Header
    story.append(Paragraph("INVOICE", title_style))
    # ... continue building invoice

    # Calculate totals
    subtotal = sum(item[1] * item[2] for item in line_items)
    tax = 0
    total = subtotal + tax

    # Build and save
    doc.build(story)
    return output_path
```

## Invoice Email Template

```
Subject: Invoice #{invoice_number} from Support Forge - ${amount}

Hi {client_name},

Please find attached invoice #{invoice_number} for {project_description}.

INVOICE SUMMARY
───────────────
Invoice #: {invoice_number}
Amount: ${amount}
Due Date: {due_date}

PAYMENT OPTIONS
───────────────
ACH/Bank Transfer (Preferred):
  Account: 8252968985
  Routing: 211370545

Zelle/Venmo: {YOUR_EMAIL}

Please reference invoice #{invoice_number} with your payment.

Questions about this invoice? Just reply to this email.

Thank you for your business!

{YOUR_NAME}
Support Forge LLC
{YOUR_PHONE}
```

## Payment Tracking

### Invoice Log Template
```
| Invoice # | Date | Client | Amount | Due Date | Status | Paid Date |
|-----------|------|--------|--------|----------|--------|-----------|
| SF-2026-001 | 1/15 | Eyam Health | $1,500 | 1/15 | Pending | - |
| SF-2026-002 | 1/20 | Client B | $3,500 | 2/4 | Pending | - |
```

### Status Options
- **Draft** - Not yet sent
- **Sent** - Sent to client
- **Pending** - Awaiting payment
- **Partial** - Partially paid
- **Paid** - Fully paid
- **Overdue** - Past due date
- **Void** - Cancelled

## Overdue Invoice Follow-up

### Reminder Schedule
- Due date: Send invoice
- 3 days overdue: Friendly reminder
- 7 days overdue: Second reminder
- 14 days overdue: Final notice
- 30+ days: Phone call / escalation

### Friendly Reminder Email
```
Subject: Friendly Reminder - Invoice #{number} Due

Hi {name},

Hope you're doing well! Just a quick reminder that invoice
#{number} for ${amount} was due on {date}.

If you've already sent payment, thank you! Please disregard
this message.

If you have any questions about the invoice, just let me know.

Payment can be sent via:
- ACH: Account 8252968985, Routing 211370545
- Zelle/Venmo: {YOUR_EMAIL}

Thanks!
Perry
```

### Final Notice Email
```
Subject: Final Notice - Invoice #{number} - ${amount} Past Due

Hi {name},

This is a final reminder that invoice #{number} for ${amount}
is now {days} days past due.

Please arrange payment at your earliest convenience. If there
are any issues or concerns preventing payment, please let me
know so we can discuss.

Payment options:
- ACH: Account 8252968985, Routing 211370545
- Zelle/Venmo: {YOUR_EMAIL}

Thank you,
{YOUR_NAME}
Support Forge LLC
```

## Quick Commands

**"Create invoice for [client] for [amount] for [service]"**
→ Generate complete invoice PDF

**"Send invoice [number] to [email]"**
→ Email invoice with standard template

**"Invoice status"**
→ Show all pending/overdue invoices

**"Follow up on overdue invoices"**
→ Generate reminder emails for overdue

## Tax Considerations

- MA does not charge sales tax on most services
- Track all invoices for quarterly estimated taxes
- Keep copies of all invoices for 7 years
- Consult accountant for specific tax questions
