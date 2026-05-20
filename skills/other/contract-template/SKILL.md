---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: contract-template
description: ">"
version: "1.0"
author: claude-office-skills
license: MIT

# Categorization
category: template
tags:
  - contract
  - template
  - legal
  - accord
department: Legal

# AI Model Compatibility
models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4
  compatible:
    - claude-3-5-sonnet
    - gpt-4
    - gpt-4o

# MCP Tools Integration
mcp:
  server: office-mcp
  tools:
    - create_docx
    - fill_docx_template

# Skill Capabilities
capabilities:
  - contract_templating
  - legal_documents

# Language Support
languages:
  - en
  - zh
---

# Contract Template Skill

## Overview

This skill enables creation of smart contract templates using **Accord Project** - an open-source framework for legally enforceable, machine-readable contracts. Create templates with embedded logic that can automate contract execution.

## How to Use

1. Describe the contract type and terms
2. Specify variables and logic rules
3. I'll generate Accord Project template

**Example prompts:**
- "Create an NDA template with variable terms"
- "Build a service agreement with payment milestones"
- "Generate a rental agreement template"
- "Design a consulting contract with termination clauses"

## Domain Knowledge

### Template Structure

```
contract-template/
├── package.json           # Metadata
├── grammar/
│   └── template.tem.md    # Natural language template
├── model/
│   └── model.cto          # Data model
├── logic/
│   └── logic.ergo         # Business logic
└── text/
    └── sample.md          # Sample contract
```

### Template Syntax (TemplateMark)

```markdown
# Service Agreement

This Agreement is made between [{supplier}] ("Supplier") 
and [{buyer}] ("Buyer").

## Services
The Supplier agrees to provide [{serviceDescription}].

## Payment
The Buyer shall pay [{paymentAmount}] within 
[{paymentDays}] days of invoice.

## Term
This Agreement begins on [{startDate as "MMMM DD, YYYY"}] 
and continues for [{termMonths}] months.

{{#if latePenalty}}
## Late Payment
A penalty of [{penaltyPercent}]% applies to late payments.
{{/if}}
```

### Data Model (Concerto)

```cto
namespace org.example.service

import org.accordproject.time.*

asset ServiceAgreement extends Contract {
  o String supplier
  o String buyer
  o String serviceDescription
  o Double paymentAmount
  o Integer paymentDays
  o DateTime startDate
  o Integer termMonths
  o Boolean latePenalty optional
  o Double penaltyPercent optional
}

transaction PaymentRequest {
  o Double amount
  o DateTime dueDate
}

transaction PaymentResponse {
  o Double amount
  o Double penalty
  o DateTime paymentDue
}
```

### Business Logic (Ergo)

```ergo
namespace org.example.service

import org.accordproject.time.*

contract ServiceContract over ServiceAgreement {
  
  clause payment(request : PaymentRequest) : PaymentResponse {
    let dueDate = addDuration(request.dueDate, 
                              Duration{ amount: contract.paymentDays, unit: ~org.accordproject.time.TemporalUnit.days });
    
    let penalty = 
      if contract.latePenalty
      then request.amount * contract.penaltyPercent / 100.0
      else 0.0;
    
    return PaymentResponse{
      amount: request.amount,
      penalty: penalty,
      paymentDue: dueDate
    }
  }
}
```

### Using Cicero CLI

```bash
# Install
npm install -g @accordproject/cicero-cli

# Parse contract
cicero parse --template ./contract-template --sample ./text/sample.md

# Execute logic
cicero trigger --template ./contract-template \
  --sample ./text/sample.md \
  --request ./request.json

# Draft new contract
cicero draft --template ./contract-template --data ./data.json
```

## Example: NDA Template

### template.tem.md
```markdown
# Non-Disclosure Agreement

This Non-Disclosure Agreement ("Agreement") is entered into 
as of [{effectiveDate as "MMMM DD, YYYY"}] by and between:

**Disclosing Party:** [{disclosingParty}]
**Receiving Party:** [{receivingParty}]

## 1. Confidential Information

"Confidential Information" means all non-public information 
disclosed by the Disclosing Party, including but not limited to:
[{confidentialScope}].

## 2. Obligations

The Receiving Party agrees to:
- Maintain confidentiality for [{termYears}] years
- Use information only for [{permittedPurpose}]
- Not disclose to third parties without written consent

## 3. Exclusions

This Agreement does not apply to information that:
{{#if hasExclusions}}
[{exclusions}]
{{else}}
- Is or becomes publicly available
- Was known prior to disclosure
- Is independently developed
{{/if}}

## 4. Return of Materials

Upon termination, the Receiving Party shall return or destroy 
all Confidential Information within [{returnDays}] days.

## 5. Remedies

{{#if monetaryPenalty}}
Breach of this Agreement shall result in liquidated damages 
of [{penaltyAmount}].
{{else}}
The Disclosing Party shall be entitled to seek injunctive relief.
{{/if}}

**SIGNATURES**

Disclosing Party: ____________________
Date: ____________________

Receiving Party: ____________________
Date: ____________________
```

### data.json
```json
{
  "effectiveDate": "2024-01-15",
  "disclosingParty": "Tech Corp",
  "receivingParty": "Consultant LLC",
  "confidentialScope": "trade secrets, customer lists, and technical specifications",
  "termYears": 3,
  "permittedPurpose": "evaluating a potential business relationship",
  "hasExclusions": false,
  "returnDays": 30,
  "monetaryPenalty": true,
  "penaltyAmount": "$50,000"
}
```

## Resources

- [Accord Project](https://accordproject.org/)
- [GitHub Organization](https://github.com/accordproject)
- [Template Library](https://templates.accordproject.org/)
