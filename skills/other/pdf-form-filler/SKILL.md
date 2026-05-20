---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: PDF Form Filler
description: "Fill out PDF forms programmatically and extract form data"
version: "1.0"
author: claude-office-skills
license: MIT

# Categorization
category: pdf
tags:
  - pdf
  - form
  - fill
  - data-entry
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
    - fill_pdf_form
    - get_pdf_metadata

# Skill Capabilities
capabilities:
  - form_filling
  - data_entry
  - pdf_forms

# Language Support
languages:
  - en
  - zh
---

# PDF Form Filler

Fill out PDF forms automatically and extract data from completed forms.

## Overview

This skill helps you:
- Fill PDF forms with provided data
- Extract data from filled forms
- Batch fill multiple forms
- Validate form data
- Create form-filling templates

## How to Use

### Fill a Form
```
"Fill this PDF form with the following data:
- Name: John Smith
- Date: 2026-01-29
- Amount: $1,500"
```

### Extract Form Data
```
"Extract all form field values from this PDF"
"What data is filled in this form?"
```

### Batch Fill
```
"Fill 50 copies of this form using data from the spreadsheet"
"Generate forms for each row in this CSV"
```

## Form Field Types

### Supported Fields
| Field Type | Description | Fill Method |
|------------|-------------|-------------|
| **Text Field** | Single/multi-line text | Direct text entry |
| **Checkbox** | Yes/No selection | Check/uncheck |
| **Radio Button** | One of many options | Select option |
| **Dropdown** | List selection | Choose value |
| **Date Field** | Date picker | Date value |
| **Signature** | Digital signature | Signature image/certificate |
| **Combo Box** | Dropdown with text entry | Select or type |

### Field Identification
```markdown
## Form Fields: [Form Name]

### Field Map
| Field Name | Type | Required | Page | Notes |
|------------|------|----------|------|-------|
| applicant_name | Text | Yes | 1 | Max 50 chars |
| birth_date | Date | Yes | 1 | MM/DD/YYYY |
| gender | Radio | Yes | 1 | M/F/Other |
| employed | Checkbox | No | 1 | Check if yes |
| state | Dropdown | Yes | 2 | US states |
| signature | Signature | Yes | 3 | Digital sig |
```

## Fill Templates

### Data Mapping Template
```markdown
## Form Fill Template: [Form Name]

### Form Info
- **File**: application_form.pdf
- **Total Fields**: 25
- **Required Fields**: 15

### Field Mappings
```yaml
# Personal Information
applicant_name: "${firstName} ${lastName}"
date_of_birth: "${birthDate}"
ssn_last_four: "${ssnLast4}"
phone: "${phone}"
email: "${email}"

# Address
street_address: "${address.street}"
city: "${address.city}"
state: "${address.state}"
zip_code: "${address.zip}"

# Employment
currently_employed: ${isEmployed}  # checkbox
employer_name: "${employer.name}"
job_title: "${employer.title}"

# Selections
payment_method: "${paymentMethod}"  # dropdown
agree_terms: true  # checkbox
```

### Sample Data
```json
{
  "firstName": "John",
  "lastName": "Smith",
  "birthDate": "1990-05-15",
  "phone": "555-123-4567",
  "email": "john.smith@email.com",
  "address": {
    "street": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip": "10001"
  },
  "isEmployed": true,
  "employer": {
    "name": "Acme Corp",
    "title": "Manager"
  },
  "paymentMethod": "Direct Deposit"
}
```
```

## Output Formats

### Fill Result Report
```markdown
## Form Fill Result

### Summary
| Status | Value |
|--------|-------|
| **Form** | application_form.pdf |
| **Fields Filled** | 23/25 |
| **Errors** | 2 |
| **Output** | filled_application.pdf |

### Filled Fields
| Field | Value | Status |
|-------|-------|--------|
| applicant_name | John Smith | ✅ |
| date_of_birth | 05/15/1990 | ✅ |
| phone | 555-123-4567 | ✅ |
| state | NY | ✅ |
| payment_method | Direct Deposit | ✅ |

### Errors/Warnings
| Field | Issue | Suggestion |
|-------|-------|------------|
| ssn | Field not found | Check field name |
| signature | Requires certificate | Add signature manually |

### Validation
- ✅ All required fields filled
- ✅ Date formats correct
- ⚠️ Signature field needs manual completion
```

### Extracted Data Report
```markdown
## Form Data Extraction

### Source: completed_form.pdf

### Extracted Values
```json
{
  "form_title": "Employment Application",
  "submission_date": "2026-01-29",
  "fields": {
    "applicant_name": "Jane Doe",
    "date_of_birth": "1985-03-20",
    "email": "jane.doe@email.com",
    "phone": "555-987-6543",
    "address": "456 Oak Ave, Chicago, IL 60601",
    "position_applied": "Senior Developer",
    "salary_expectation": "$120,000",
    "available_start": "2026-03-01",
    "references_provided": true
  }
}
```

### Field Statistics
| Metric | Value |
|--------|-------|
| Total fields | 30 |
| Filled fields | 28 |
| Empty fields | 2 |
| Extraction confidence | 98% |
```

## Batch Processing

### Batch Fill Job
```markdown
## Batch Form Fill

### Configuration
- **Template Form**: w9_form.pdf
- **Data Source**: vendors.csv
- **Records**: 150
- **Output Folder**: /filled_w9s/

### Data Preview
| Row | Name | TIN | Address |
|-----|------|-----|---------|
| 1 | Acme Corp | XX-XXX1234 | 123 Main St |
| 2 | Beta LLC | XX-XXX5678 | 456 Oak Ave |
| ... | ... | ... | ... |

### Progress
| Status | Count | % |
|--------|-------|---|
| ✅ Completed | 145 | 97% |
| ⚠️ Warnings | 3 | 2% |
| ❌ Errors | 2 | 1% |

### Errors
| Row | Issue |
|-----|-------|
| 47 | Invalid TIN format |
| 89 | Missing required: Address |

### Output Files
- w9_acme_corp.pdf
- w9_beta_llc.pdf
- ...
```

## Form Validation

### Validation Rules
```markdown
## Form Validation Rules

### Field Validations
| Field | Rule | Error Message |
|-------|------|---------------|
| email | Valid email format | "Invalid email address" |
| phone | 10 digits | "Phone must be 10 digits" |
| ssn | XXX-XX-XXXX format | "Invalid SSN format" |
| date | MM/DD/YYYY | "Use MM/DD/YYYY format" |
| zip | 5 or 9 digits | "Invalid ZIP code" |
| amount | Numeric, > 0 | "Enter positive number" |

### Cross-Field Validations
| Rule | Fields | Condition |
|------|--------|-----------|
| Conditional required | employer_name | Required if employed = true |
| Date range | end_date | Must be after start_date |
| Sum check | item_totals | Must equal grand_total |
```

### Validation Report
```markdown
## Pre-Fill Validation

### Data Validation Results
| Field | Value | Valid | Issue |
|-------|-------|-------|-------|
| email | john@email | ❌ | Missing domain |
| phone | 555-1234 | ❌ | Only 7 digits |
| date | 2026-01-29 | ✅ | - |
| zip | 10001 | ✅ | - |

### Summary
- ✅ Valid: 18 fields
- ❌ Invalid: 2 fields
- ⚠️ Warnings: 3 fields

### Recommendations
1. Fix email format: add domain (e.g., @company.com)
2. Complete phone number with area code
```

## Common Form Types

### Government Forms
| Form | Purpose | Key Fields |
|------|---------|------------|
| W-9 | Tax identification | TIN, name, address |
| I-9 | Employment eligibility | ID info, citizenship |
| W-4 | Withholding | Allowances, status |
| 1099 | Contractor income | Income, payer info |

### Business Forms
| Form | Purpose | Key Fields |
|------|---------|------------|
| NDA | Confidentiality | Parties, terms, dates |
| Invoice | Billing | Items, amounts, terms |
| PO | Purchase order | Items, quantities, vendor |
| Application | Various | Personal info, history |

## Tool Recommendations

### Desktop Software
- **Adobe Acrobat Pro**: Full form features
- **Foxit PDF Editor**: Good form support
- **PDFescape**: Free online option
- **JotForm**: Form creation and filling

### Programming Libraries
- **pdf-lib** (JavaScript): Fill and create forms
- **PyPDF2** (Python): Basic form filling
- **iText** (Java/.NET): Enterprise forms
- **PDFBox** (Java): Apache project

### Automation Tools
- **Adobe Acrobat Actions**: Batch processing
- **Power Automate**: Microsoft integration
- **Zapier + PDF.co**: Cloud automation

## Limitations

- Cannot execute actual form filling (provides guidance)
- Digital signatures require proper certificates
- Some secured PDFs prevent form filling
- Complex calculations may not auto-update
- Flattened forms cannot be edited
- Field names must match exactly
