---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: Offer Letter Generator
description: "Create formal employment offer letters with compensation and terms"
version: "1.0"
author: claude-office-skills
license: MIT

# Categorization
category: hr
tags:
  - offer-letter
  - hiring
  - employment
department: HR

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
    - docx_to_pdf

# Skill Capabilities
capabilities:
  - offer_generation
  - compensation_structuring

# Language Support
languages:
  - en
  - zh
---

# Offer Letter Generator

Generate professional employment offer letters that clearly communicate job terms and compensation.

## Overview

This skill creates formal offer letters that:
- Clearly state position and compensation
- Outline key employment terms
- Maintain legal compliance awareness
- Create positive candidate experience

## How to Use

Provide the following information:

### Required
1. **Candidate Name**: Full legal name
2. **Job Title**: Position being offered
3. **Start Date**: Proposed start date
4. **Compensation**: Base salary and frequency
5. **Employment Type**: Full-time, Part-time, Contract
6. **Reporting To**: Manager's name and title

### Optional
7. **Equity/Bonus**: Stock options, signing bonus, annual bonus
8. **Benefits**: Health, 401k, PTO summary
9. **Work Location**: Office address or Remote
10. **Response Deadline**: When offer expires
11. **Contingencies**: Background check, references, etc.

## Output Structure

```
[Company Letterhead]

[Date]

[Candidate Name]
[Address - if known]

Dear [First Name],

RE: Employment Offer - [Job Title]

[Opening paragraph - excitement about offering position]

[Position details paragraph]

[Compensation paragraph]

[Benefits summary paragraph]

[Contingencies paragraph - if applicable]

[Next steps and deadline]

[Closing]

Sincerely,
[Hiring Manager Name]
[Title]

---
ACCEPTANCE

I accept this offer of employment:

Signature: _______________________
Print Name: ______________________
Date: ___________________________
```

## Template Sections

### Opening
```
We are pleased to extend this offer of employment for the position of 
[Job Title] at [Company Name]. After our interview process, we believe 
your skills and experience make you an excellent addition to our team.
```

### Position Details
```
Position: [Job Title]
Department: [Department]
Reports To: [Manager Name], [Manager Title]
Start Date: [Date]
Work Location: [Location/Remote]
Employment Type: [Full-time/Part-time/Contract]
```

### Compensation
```
Base Salary: $[Amount] per [year/month/hour]
Payment Schedule: [Bi-weekly/Monthly]

[If applicable:]
Signing Bonus: $[Amount], payable [timing]
Annual Bonus: Up to [X]% of base salary, based on performance
Equity: [X] stock options, vesting over [Y] years with [Z]-year cliff
```

### Benefits Summary
```
You will be eligible for our comprehensive benefits package, including:
- Medical, dental, and vision insurance
- 401(k) with [X]% company match
- [X] days paid time off annually
- [Additional benefits]

Full benefits details will be provided during onboarding.
```

### Contingencies
```
This offer is contingent upon:
- Successful completion of a background check
- Verification of your eligibility to work in [Country]
- [Other contingencies]
```

### Acceptance Terms
```
Please indicate your acceptance by signing and returning this letter 
by [Date]. This offer will expire if not accepted by this date.

If you have any questions, please contact [Name] at [Email/Phone].

We look forward to welcoming you to the team!
```

## Examples

### Example Request
```
Create an offer letter:
- Candidate: Sarah Johnson
- Position: Product Manager
- Start: March 15, 2026
- Salary: $145,000/year
- Bonus: 15% target
- Equity: 10,000 options, 4-year vest
- Manager: Mike Chen, VP Product
- Location: Hybrid (NYC office 2 days/week)
- Deadline: January 31, 2026
```

### Example Output

```
ACME CORPORATION
123 Innovation Way, New York, NY 10001

January 15, 2026

Sarah Johnson

Dear Sarah,

RE: Employment Offer - Product Manager

We are thrilled to offer you the position of Product Manager at ACME 
Corporation! Your experience in B2B product strategy and your insights 
during our interviews impressed the entire team. We believe you'll make 
significant contributions to our product vision.

POSITION DETAILS
Position: Product Manager
Department: Product
Reports To: Mike Chen, VP of Product
Start Date: March 15, 2026
Work Location: Hybrid - NYC office (Tuesdays & Thursdays), Remote otherwise
Employment Type: Full-time, Exempt

COMPENSATION
Base Salary: $145,000 annually, paid bi-weekly
Annual Bonus: Target of 15% of base salary ($21,750), based on individual 
and company performance
Equity: 10,000 stock options, vesting over 4 years with a 1-year cliff

BENEFITS
You will be eligible for our comprehensive benefits package starting on 
your first day, including:
- Medical, dental, and vision insurance (100% employee coverage)
- 401(k) with 4% company match
- 20 days paid time off + 10 company holidays
- $1,500 annual professional development budget
- Commuter benefits

This offer is contingent upon successful completion of a standard 
background check.

Please indicate your acceptance by signing below and returning this 
letter by January 31, 2026. If you have questions, please reach out 
to me directly at mike.chen@acme.com.

We're excited about the possibility of you joining our team!

Sincerely,

Mike Chen
VP of Product
ACME Corporation

---
ACCEPTANCE

I accept this offer of employment and agree to the terms outlined above.

Signature: _______________________

Print Name: ______________________

Date: ___________________________
```

## Best Practices

### Do's
- Use clear, straightforward language
- Include all material terms
- Specify deadlines clearly
- Provide contact for questions
- Include signature block

### Don'ts
- Don't make promises outside standard terms
- Don't include discriminatory language
- Don't forget contingencies
- Don't omit important details
- Don't use overly complex legal jargon

### Legal Considerations
- Offer letters are generally not contracts (add disclaimer if needed)
- At-will employment should be stated clearly (US)
- Equity terms should reference full agreement
- Have legal/HR review before sending

## Limitations

- This is a template guide, not legal advice
- Employment laws vary by jurisdiction
- Company-specific policies must be incorporated
- Complex equity arrangements need legal review
- International offers have additional requirements
