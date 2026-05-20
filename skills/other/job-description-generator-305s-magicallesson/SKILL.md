---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: Job Description Generator
description: ">"
version: "1.0"
author: claude-office-skills
license: MIT

# Categorization
category: hr
tags:
  - job-description
  - hiring
  - recruitment
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

# Skill Capabilities
capabilities:
  - job_posting
  - requirement_definition
  - inclusive_language

# Language Support
languages:
  - en
  - zh
---

# Job Description Generator

Generate professional, inclusive job descriptions that attract qualified candidates.

## Overview

This skill helps HR professionals and hiring managers create comprehensive job postings that:
- Clearly communicate role expectations
- Use inclusive, bias-free language
- Follow industry best practices
- Attract diverse, qualified candidates

## How to Use

Provide the following information:
1. **Job Title**: The position name
2. **Department**: Team or department
3. **Level**: Entry, Mid, Senior, Lead, Director, etc.
4. **Employment Type**: Full-time, Part-time, Contract
5. **Location**: On-site, Remote, Hybrid
6. **Key Responsibilities**: What the role will do
7. **Requirements**: Must-have qualifications
8. **Nice-to-haves**: Preferred qualifications
9. **Company Info**: Brief about the company (optional)

## Output Structure

```markdown
# [Job Title]

## About [Company]
[Brief company description]

## About the Role
[2-3 sentences describing the position and its impact]

## What You'll Do
- [Responsibility 1]
- [Responsibility 2]
- [Responsibility 3]
...

## What We're Looking For

### Required
- [Requirement 1]
- [Requirement 2]
...

### Nice to Have
- [Preferred qualification 1]
- [Preferred qualification 2]
...

## What We Offer
- [Benefit 1]
- [Benefit 2]
...

## How to Apply
[Application instructions]
```

## Best Practices

### Language Guidelines
- Use "you" instead of "the ideal candidate"
- Avoid gendered language (he/she → they)
- Remove unnecessary jargon
- Be specific about requirements vs. nice-to-haves
- Include salary range when possible (improves applications by 30%)

### Red Flags to Avoid
- "Rockstar" / "Ninja" / "Guru" → Use "Expert" or "Specialist"
- "Fast-paced environment" → Be specific about workload
- Excessive requirements → Limit to 5-7 must-haves
- Vague responsibilities → Use measurable outcomes

### Inclusive Language
| Instead of | Use |
|------------|-----|
| "Young and energetic" | "Motivated and enthusiastic" |
| "Native English speaker" | "Fluent in English" |
| "Cultural fit" | "Values alignment" |
| "Digital native" | "Proficient with digital tools" |

## Examples

### Example Request
```
Create a job description for:
- Title: Senior Frontend Developer
- Department: Engineering
- Level: Senior (5+ years)
- Type: Full-time, Remote
- Tech stack: React, TypeScript, GraphQL
- Team size: 8 engineers
- Company: B2B SaaS startup, Series B
```

### Example Output

```markdown
# Senior Frontend Developer

## About Us
We're a Series B B2B SaaS startup transforming how enterprises manage their workflows. Our engineering team of 40+ builds products used by Fortune 500 companies.

## About the Role
Join our 8-person frontend team to architect and build the next generation of our platform. You'll have significant impact on technical decisions and mentor junior developers.

## What You'll Do
- Design and implement complex UI features using React and TypeScript
- Collaborate with designers to create intuitive user experiences
- Optimize application performance and accessibility
- Contribute to our GraphQL API design
- Mentor junior developers through code reviews and pairing
- Participate in technical planning and architecture discussions

## What We're Looking For

### Required
- 5+ years of frontend development experience
- Strong proficiency in React and TypeScript
- Experience with GraphQL or similar query languages
- Track record of building accessible, performant web applications
- Excellent communication skills

### Nice to Have
- Experience with design systems
- Contributions to open source projects
- Experience at B2B SaaS companies
- Familiarity with testing frameworks (Jest, Cypress)

## What We Offer
- Competitive salary: $150,000 - $190,000
- Equity package
- Fully remote with flexible hours
- Health, dental, and vision insurance
- $2,000 annual learning budget
- Home office stipend

## How to Apply
Send your resume and a brief note about why you're interested to careers@company.com
```

## Domain Knowledge

### Job Levels (Typical)
| Level | Years | Scope |
|-------|-------|-------|
| Entry/Junior | 0-2 | Individual tasks |
| Mid-level | 2-5 | Independent projects |
| Senior | 5-8 | Technical leadership |
| Staff/Lead | 8-12 | Cross-team impact |
| Principal/Director | 12+ | Organization-wide |

### Standard Benefits to Consider
- Health insurance
- Retirement plans (401k, pension)
- PTO / Vacation policy
- Remote work options
- Professional development
- Parental leave
- Equipment/stipends

## Limitations

- Cannot guarantee legal compliance (have HR/legal review)
- Salary benchmarks may not reflect local markets
- Industry-specific requirements need domain input
- Cannot verify company information provided
