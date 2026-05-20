---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: form-builder
description: "Build interactive document forms and questionnaires using docassemble"
version: "1.0"
author: claude-office-skills
license: MIT

# Categorization
category: template
tags:
  - form
  - builder
  - interactive
  - docassemble
department: All

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
  - form_creation
  - interactive_documents

# Language Support
languages:
  - en
  - zh
---

# Form Builder Skill

## Overview

This skill enables creation of intelligent document forms using **docassemble** - a platform for guided interviews that generate documents. Create questionnaires that adapt based on answers.

## How to Use

1. Describe the form or document you need
2. Specify conditional logic requirements
3. I'll create docassemble interview YAML

**Example prompts:**
- "Create an intake form for new clients"
- "Build a conditional questionnaire for legal documents"
- "Generate a multi-step form for contract generation"
- "Design an interactive document assembly form"

## Domain Knowledge

### Interview Structure

```yaml
metadata:
  title: Client Intake Form
  short title: Intake

---
question: |
  What is your name?
fields:
  - First Name: first_name
  - Last Name: last_name

---
question: |
  What type of service do you need?
field: service_type
choices:
  - Contract Review
  - Document Drafting
  - Consultation

---
mandatory: True
question: |
  Thank you, ${ first_name }!
subquestion: |
  We will contact you about your ${ service_type } request.
```

### Conditional Logic

```yaml
---
question: |
  Are you a business or individual?
field: client_type
choices:
  - Business
  - Individual

---
if: client_type == "Business"
question: |
  What is your company name?
fields:
  - Company: company_name
  - EIN: ein
    required: False

---
if: client_type == "Individual"
question: |
  What is your date of birth?
fields:
  - Birthdate: birthdate
    datatype: date
```

### Field Types

```yaml
fields:
  # Text
  - Name: name
  
  # Email
  - Email: email
    datatype: email
  
  # Number
  - Age: age
    datatype: integer
  
  # Currency
  - Amount: amount
    datatype: currency
  
  # Date
  - Start Date: start_date
    datatype: date
  
  # Yes/No
  - Agree to terms?: agrees
    datatype: yesno
  
  # Multiple choice
  - Color: color
    choices:
      - Red
      - Blue
      - Green
  
  # Checkboxes
  - Select options: options
    datatype: checkboxes
    choices:
      - Option A
      - Option B
  
  # File upload
  - Upload document: document
    datatype: file
```

### Document Generation

```yaml
---
mandatory: True
question: |
  Your document is ready.
attachment:
  name: Contract
  filename: contract
  content: |
    # Service Agreement
    
    This agreement is between **${ client_name }**
    and **Service Provider**.
    
    ## Services
    ${ service_description }
    
    ## Payment
    Total amount: ${ currency(amount) }
    
    Date: ${ today() }
```

## Example: Client Intake

```yaml
metadata:
  title: Legal Client Intake
  short title: Intake

---
objects:
  - client: Individual

---
question: |
  Welcome to our intake form.
subquestion: |
  Please answer the following questions.
continue button field: intro_screen

---
question: |
  What is your name?
fields:
  - First Name: client.name.first
  - Last Name: client.name.last
  - Email: client.email
    datatype: email
  - Phone: client.phone
    required: False

---
question: |
  What type of matter is this?
field: matter_type
choices:
  - Contract: contract
  - Dispute: dispute
  - Advisory: advisory

---
if: matter_type == "contract"
question: |
  Contract Details
fields:
  - Contract Type: contract_type
    choices:
      - Employment
      - Service Agreement
      - NDA
  - Other Party: other_party
  - Estimated Value: contract_value
    datatype: currency

---
mandatory: True
question: |
  Thank you, ${ client.name.first }!
subquestion: |
  **Summary:**
  
  - Name: ${ client.name }
  - Email: ${ client.email }
  - Matter: ${ matter_type }
  
  We will contact you within 24 hours.
```

## Resources

- [docassemble Documentation](https://docassemble.org/docs.html)
- [GitHub Repository](https://github.com/jhpyle/docassemble)
