---
name: DocuSign Automation
description: Automate document signing workflows, envelope management, and e-signature processes
version: 1.0.0
author: Claude Office Skills
category: documents
tags:
  - docusign
  - esignature
  - contracts
  - documents
  - legal
department: legal
models:
  - claude-3-opus
  - claude-3-sonnet
  - gpt-4
mcp:
  server: document-mcp
  tools:
    - docusign_envelope
    - docusign_template
    - docusign_signing
    - docusign_webhook
capabilities:
  - Envelope creation
  - Template management
  - Signing workflows
  - Status tracking
input:
  - Documents
  - Signer information
  - Template configurations
  - Workflow rules
output:
  - Signed documents
  - Envelope status
  - Audit trails
  - Completion reports
languages:
  - en
related_skills:
  - contract-review
  - pdf-tools
  - invoice-automation
---

# DocuSign Automation

Comprehensive skill for automating e-signature and document signing workflows.

## Core Workflows

### 1. Signing Flow

```
DOCUSIGN SIGNING FLOW:
┌─────────────────┐
│  Create Envelope│
│  - Document     │
│  - Recipients   │
└────────┬────────┘
         ▼
┌─────────────────┐
│  Add Fields     │
│  - Signatures   │
│  - Initials     │
│  - Dates        │
└────────┬────────┘
         ▼
┌─────────────────┐
│  Send for       │
│  Signature      │
└────────┬────────┘
         ▼
┌─────────────────┐
│  Signer 1 Signs │
│  (In order)     │
└────────┬────────┘
         ▼
┌─────────────────┐
│  Signer 2 Signs │
│  (If multiple)  │
└────────┬────────┘
         ▼
┌─────────────────┐
│   Completed     │
│  - Archive      │
│  - Distribute   │
└─────────────────┘
```

### 2. Envelope Configuration

```yaml
envelope_config:
  email_subject: "{{document_type}} - Please Sign"
  email_blurb: |
    Please review and sign the attached {{document_type}}.
    This document requires your signature by {{due_date}}.
    
  documents:
    - name: "{{contract_name}}.pdf"
      document_id: 1
      
  recipients:
    signers:
      - email: "{{signer_1_email}}"
        name: "{{signer_1_name}}"
        routing_order: 1
        tabs:
          sign_here:
            - anchor: "/sig1/"
              offset_x: 0
              offset_y: 0
          date_signed:
            - anchor: "/date1/"
              
      - email: "{{signer_2_email}}"
        name: "{{signer_2_name}}"
        routing_order: 2
        tabs:
          sign_here:
            - anchor: "/sig2/"
            
    carbon_copies:
      - email: "legal@company.com"
        name: "Legal Team"
        routing_order: 3
        
  settings:
    reminder_enabled: true
    reminder_delay: 2  # days
    reminder_frequency: 2  # days
    expiration_days: 30
```

## Template Management

### Template Creation

```yaml
template_config:
  name: "Standard NDA Template"
  description: "Non-disclosure agreement for vendors"
  
  documents:
    - name: "NDA_Template.pdf"
      
  roles:
    - role_name: "Company Representative"
      routing_order: 1
      
    - role_name: "Counterparty"
      routing_order: 2
      
  tabs:
    company_rep:
      - type: sign_here
        anchor: "/company_signature/"
      - type: date_signed
        anchor: "/company_date/"
      - type: text
        anchor: "/company_name/"
        label: "Name"
      - type: text
        anchor: "/company_title/"
        label: "Title"
        
    counterparty:
      - type: sign_here
        anchor: "/counterparty_signature/"
      - type: date_signed
        anchor: "/counterparty_date/"
      - type: text
        anchor: "/counterparty_name/"
        label: "Name"
```

### Template Library

```yaml
template_library:
  contracts:
    - name: "Employment Agreement"
      id: "template_emp_001"
      category: "HR"
      
    - name: "Vendor Agreement"
      id: "template_vendor_001"
      category: "Procurement"
      
    - name: "NDA (Mutual)"
      id: "template_nda_001"
      category: "Legal"
      
  sales:
    - name: "Sales Order"
      id: "template_so_001"
      
    - name: "Statement of Work"
      id: "template_sow_001"
      
    - name: "Master Services Agreement"
      id: "template_msa_001"
```

## Workflow Automation

### Conditional Routing

```yaml
conditional_workflow:
  name: "Contract Approval Flow"
  
  conditions:
    - field: "contract_value"
      operator: "greater_than"
      value: 100000
      then:
        add_recipient:
          role: "VP Approval"
          routing_order: 1
          
    - field: "contract_type"
      operator: "equals"
      value: "international"
      then:
        add_recipient:
          role: "Legal Review"
          routing_order: 1
          
  default_flow:
    - role: "Sales Manager"
      routing_order: 1
    - role: "Customer"
      routing_order: 2
```

### Bulk Send

```yaml
bulk_send:
  template_id: "template_nda_001"
  
  recipients:
    - email: "vendor1@example.com"
      name: "Vendor One"
      custom_fields:
        company_name: "Vendor One Inc"
        effective_date: "2024-02-01"
        
    - email: "vendor2@example.com"
      name: "Vendor Two"
      custom_fields:
        company_name: "Vendor Two LLC"
        effective_date: "2024-02-01"
        
  settings:
    batch_name: "Q1 Vendor NDAs"
    send_immediately: true
```

## Integration Workflows

### Salesforce Integration

```yaml
salesforce_integration:
  triggers:
    opportunity_closed_won:
      template: "msa_template"
      recipients:
        - from_field: "Contact.Email"
          role: "Customer"
      custom_fields:
        account_name: "Account.Name"
        contract_value: "Opportunity.Amount"
        
  callbacks:
    on_completed:
      - update_opportunity:
          stage: "Contract Signed"
      - attach_document:
          to: "Opportunity"
      - create_task:
          subject: "Contract signed - begin onboarding"
```

### CRM Webhook

```yaml
webhook_config:
  events:
    - envelope-sent
    - envelope-delivered
    - envelope-completed
    - envelope-declined
    - envelope-voided
    
  callback_url: "https://api.example.com/docusign/webhook"
  
  payload_handling:
    envelope_completed:
      actions:
        - download_documents
        - update_crm_record
        - notify_team
        - archive_to_storage
```

## Status Tracking

### Envelope Dashboard

```
ENVELOPE STATUS - THIS MONTH
═══════════════════════════════════════

TOTAL: 156 envelopes

BY STATUS:
Completed    ████████████████ 89 (57%)
Sent         ████████░░░░░░░░ 34 (22%)
Delivered    ████░░░░░░░░░░░░ 18 (12%)
Declined     █░░░░░░░░░░░░░░░ 5 (3%)
Voided       █░░░░░░░░░░░░░░░ 10 (6%)

AVERAGE COMPLETION TIME: 2.3 days

PENDING SIGNATURES:
┌────────────────────┬──────────────┬─────────┐
│ Document           │ Awaiting     │ Sent    │
├────────────────────┼──────────────┼─────────┤
│ Acme Corp NDA      │ John Smith   │ 3 days  │
│ TechStart SOW      │ Jane Doe     │ 1 day   │
│ Vendor Agreement   │ Bob Wilson   │ 5 days  │
└────────────────────┴──────────────┴─────────┘

REMINDERS SENT: 23
```

### Audit Trail

```yaml
audit_trail:
  events:
    - timestamp: "2024-01-15T10:30:00Z"
      action: "Envelope Created"
      user: "sender@company.com"
      ip: "192.168.1.1"
      
    - timestamp: "2024-01-15T10:31:00Z"
      action: "Envelope Sent"
      recipients: ["signer@example.com"]
      
    - timestamp: "2024-01-15T14:22:00Z"
      action: "Document Viewed"
      user: "signer@example.com"
      ip: "10.0.0.1"
      
    - timestamp: "2024-01-15T14:25:00Z"
      action: "Signature Applied"
      user: "signer@example.com"
      signature_type: "Electronic"
      
    - timestamp: "2024-01-15T14:25:30Z"
      action: "Envelope Completed"
```

## API Examples

### Create and Send Envelope

```javascript
// Create Envelope from Template
const envelope = await docusign.envelopes.create(accountId, {
  templateId: "template_123",
  templateRoles: [
    {
      roleName: "Customer",
      email: "customer@example.com",
      name: "John Customer",
      tabs: {
        textTabs: [
          {
            tabLabel: "CompanyName",
            value: "Customer Corp"
          }
        ]
      }
    }
  ],
  status: "sent"
});

// Get Envelope Status
const status = await docusign.envelopes.get(
  accountId, 
  envelopeId
);

// Download Completed Documents
const documents = await docusign.envelopes.getDocuments(
  accountId,
  envelopeId,
  { certificate: true }
);

// Void Envelope
await docusign.envelopes.update(accountId, envelopeId, {
  status: "voided",
  voidedReason: "Contract terms changed"
});
```

## Best Practices

1. **Use Templates**: Standardize common documents
2. **Set Reminders**: Automated follow-ups
3. **Expiration Dates**: Ensure timely completion
4. **Audit Trails**: Maintain for compliance
5. **Bulk Send**: Efficient for multiple recipients
6. **Webhooks**: Real-time status updates
7. **Brand Signing**: Custom signing experience
8. **Archive**: Store completed documents securely
