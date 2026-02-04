---
name: creating-proposals
description: Use this skill when creating proposals, engagement letters, statements of work (SOWs), contracts, or service agreements for clients. Generates professional PDF documents with Support Forge branding, pricing, payment terms, and signature blocks. Invoke for any client proposal, quote, or formal business agreement.
---

# Proposal & Engagement Letter Generator

You create professional, persuasive proposals and engagement letters for Support Forge consulting engagements.

## Document Types

| Type | Use Case |
|------|----------|
| **Engagement Letter** | Formal agreement for consulting services |
| **Statement of Work (SOW)** | Detailed project scope and deliverables |
| **Proposal** | Sales document with options/recommendations |
| **Quote** | Simple pricing for defined services |
| **Contract Addendum** | Modifications to existing agreements |

## Support Forge Branding

### Company Info
```
SupportForge
166 Wilson St, Haverhill, MA 01832
contact@support-forge.com | {YOUR_PHONE}
```

### Payment Details
```
ACH/Bank Transfer:
Account Number: 8252968985
Routing Number: 211370545

Zelle/Venmo: {YOUR_EMAIL}
```

### Brand Colors
- Primary Purple: #6366f1
- Navy: #1a365d
- Dark Background: #050508

## Engagement Letter Template

### Structure

```
LETTER OF ENGAGEMENT
====================
SupportForge
Haverhill, MA
contact@support-forge.com | {YOUR_PHONE}

Date: [Date]

To:
[Client Name]
[Title]
[Company]
[Email]

RE: [Project Title/Description]

---

Dear [First Name],

[Opening - thank them, reference how you connected]

[This Letter of Engagement outlines the scope, deliverables,
investment, and terms for our work together.]

SCOPE OF SERVICES
-----------------
[Describe what you'll do]

1. [Service Area 1]
   • Deliverable
   • Deliverable
   • Deliverable

2. [Service Area 2]
   • Deliverable
   • Deliverable

[Continue as needed...]

DELIVERABLES
------------
Upon completion, you will have:
• [Deliverable 1]
• [Deliverable 2]
• [Deliverable 3]

TIMELINE
--------
[Timeline description]

INVESTMENT
----------
[Package Name] — $X,XXX.00

Includes:
• [What's included]
• [What's included]
• [Support terms]

Payment Terms:
• $X,XXX.00 due upon signing to initiate work
  - OR -
• 50% ($X,XXX) due upon signing
• 50% ($X,XXX) due upon completion

---

Payment Methods:
ACH/Bank Transfer:
  Account Number: 8252968985
  Routing Number: 211370545

Zelle/Venmo: {YOUR_EMAIL}

TERMS & CONDITIONS
------------------
1. Confidentiality: [Standard clause]
2. Intellectual Property: [Standard clause]
3. Client Responsibilities: [Standard clause]
4. Limitation of Liability: [Standard clause]
5. Termination: [Standard clause]
6. Additional Work: [Standard clause]

ACCEPTANCE
----------
By signing below, both parties agree to the terms
outlined in this Letter of Engagement.

SupportForge

_________________________________________________
{YOUR_NAME}
Principal Consultant
Date: _____________


[Client Company]

_________________________________________________
[Client Name]
[Client Title]
Date: _____________

---

Questions? Contact Perry at contact@support-forge.com or {YOUR_PHONE}
```

## Standard Terms & Conditions

### Confidentiality
```
SupportForge will maintain strict confidentiality of all [Client]
proprietary information, credentials, and business data encountered
during this engagement.
```

### Intellectual Property
```
All configurations, documentation, and work product created during
this engagement become the property of [Client] upon final payment.
```

### Client Responsibilities
```
Client agrees to provide timely access to necessary accounts,
credentials, and personnel required to complete the work. Delays
caused by client availability may extend the timeline.
```

### Limitation of Liability
```
SupportForge's liability is limited to the total fees paid under
this agreement. SupportForge is not liable for any third-party
service outages, API changes, or platform limitations outside our control.
```

### Termination
```
Either party may terminate this agreement with 7 days written notice.
Client will be invoiced for work completed to date.
```

### Additional Work
```
Any work beyond the defined scope will be quoted separately and
requires written approval before proceeding.
```

## Pricing Packages

### AI Enablement Packages

**Referral Support Package — $1,500**
- Claude Code environment setup
- MCP server configuration (3-5 integrations)
- Basic skills installation
- Up to 6 hours hands-on work
- 1 week email support
- One 30-min follow-up session

**Professional Setup — $3,500**
- Everything in Referral Package
- Custom skills development
- AWS/GCP configuration
- Up to 15 hours hands-on work
- 2 weeks support
- Two 30-min follow-up sessions

**Enterprise Enablement — $7,500+**
- Full environment buildout
- Custom integrations
- Team training sessions
- Ongoing support options
- Custom scoping required

### Hourly Consulting
- **Standard Rate**: $175/hour
- **Retainer Rate**: $150/hour (10+ hours/month)

### Website/Development
- **Simple Site**: $2,500-5,000
- **Complex Site**: $5,000-15,000
- **Maintenance**: $500-1,500/month

## PDF Generation

Use Python with reportlab to generate professional PDFs:

```python
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors

# Colors
navy = HexColor('#1a365d')
purple = HexColor('#6366f1')

# Create document
doc = SimpleDocTemplate(
    output_path,
    pagesize=letter,
    rightMargin=0.75*inch,
    leftMargin=0.75*inch,
    topMargin=0.5*inch,
    bottomMargin=0.5*inch
)

# Build styles and content...
```

See `./pdf-generation-template.py` for complete working example.

## Workflow

### Creating a New Proposal

1. **Gather Information**
   - Client name, title, company, email
   - Project scope and requirements
   - Timeline expectations
   - Budget range (if known)

2. **Determine Package/Pricing**
   - Match services to appropriate package
   - Consider referral discounts
   - Calculate custom pricing if needed

3. **Draft Document**
   - Use appropriate template
   - Customize scope and deliverables
   - Set payment terms

4. **Generate PDF**
   - Run Python script with reportlab
   - Review output for formatting
   - Save to Downloads folder

5. **Send to Client**
   - Email with PDF attached
   - Brief cover message
   - Clear next steps

## Quick Commands

**"Create engagement letter for [client] at [company] for [service]"**
→ Generate complete engagement letter

**"Quote [service] at [price] for [client]"**
→ Quick pricing document

**"SOW for [project description]"**
→ Detailed statement of work

**"Add terms for [special condition]"**
→ Custom terms and conditions

## Tips

- Always get client's proper title and company name
- Match formality to relationship (referral = warmer tone)
- Be specific about deliverables (avoid scope creep)
- Include timeline with caveats about client availability
- Payment terms should be clear and upfront
- Always include signature blocks for both parties
