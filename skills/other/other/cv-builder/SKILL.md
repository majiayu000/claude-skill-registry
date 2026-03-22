---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: cv-builder
description: ">"
version: "1.0"
author: claude-office-skills
license: MIT

# Categorization
category: hr
tags:
  - cv
  - resume
  - builder
  - generator
department: HR/Personal

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
    - docx_to_pdf
    - fill_docx_template

# Skill Capabilities
capabilities:
  - cv_generation
  - formatting
  - professional_layout

# Language Support
languages:
  - en
  - zh
---

# CV Builder Skill

## Overview

This skill enables creation of professional CVs/resumes from structured YAML using **rendercv**. Define your experience once, generate beautiful PDFs in multiple themes.

## How to Use

1. Provide your CV information (experience, education, skills)
2. Choose a template/theme
3. I'll generate YAML and render to PDF

**Example prompts:**
- "Create a CV from my experience"
- "Generate a resume in the classic theme"
- "Update my CV with new job experience"
- "Build a technical resume highlighting projects"

## Domain Knowledge

### YAML Structure

```yaml
cv:
  name: John Doe
  location: San Francisco, CA
  email: john@email.com
  phone: "+1-555-555-5555"
  website: https://johndoe.com
  social_networks:
    - network: LinkedIn
      username: johndoe
    - network: GitHub
      username: johndoe
  
  sections:
    summary:
      - "Senior software engineer with 10+ years experience..."
    
    experience:
      - company: Tech Corp
        position: Senior Engineer
        location: San Francisco, CA
        start_date: 2020-01
        end_date: present
        highlights:
          - "Led team of 5 engineers"
          - "Increased performance by 40%"
    
    education:
      - institution: MIT
        area: Computer Science
        degree: BS
        start_date: 2008
        end_date: 2012
    
    skills:
      - label: Languages
        details: Python, JavaScript, Go
      - label: Frameworks
        details: React, Django, FastAPI
```

### Themes

Available themes: `classic`, `sb2nov`, `moderncv`, `engineeringresumes`

```yaml
design:
  theme: classic
  font: Source Sans 3
  font_size: 10pt
  page_size: letterpaper
  color: '#004f90'
```

### CLI Usage

```bash
# Install
pip install rendercv

# Create new CV
rendercv new "John Doe"

# Render to PDF
rendercv render cv.yaml

# Output: rendercv_output/John_Doe_CV.pdf
```

## Example

```yaml
cv:
  name: Sarah Chen
  location: New York, NY
  email: sarah@email.com
  phone: "+1-555-123-4567"
  website: https://sarahchen.dev
  social_networks:
    - network: LinkedIn
      username: sarahchen
    - network: GitHub
      username: sarahchen

  sections:
    summary:
      - "Full-stack developer with 8 years of experience building scalable web applications. Passionate about clean code and user experience."

    experience:
      - company: Startup Inc
        position: Lead Developer
        location: New York, NY
        start_date: 2021-03
        end_date: present
        highlights:
          - "Architected microservices handling 1M+ requests/day"
          - "Mentored 4 junior developers"
          - "Reduced deployment time by 60% with CI/CD"

      - company: Big Tech Co
        position: Software Engineer
        location: San Francisco, CA
        start_date: 2018-06
        end_date: 2021-02
        highlights:
          - "Built real-time analytics dashboard"
          - "Optimized database queries, 3x faster"

    education:
      - institution: Stanford University
        area: Computer Science
        degree: MS
        start_date: 2016
        end_date: 2018

    skills:
      - label: Languages
        details: Python, TypeScript, Go, SQL
      - label: Technologies
        details: React, Node.js, PostgreSQL, AWS, Docker
      - label: Practices
        details: Agile, TDD, Code Review, CI/CD

design:
  theme: sb2nov
  font_size: 10pt
```

## Resources

- [rendercv Documentation](https://docs.rendercv.com/)
- [GitHub Repository](https://github.com/sinaatalay/rendercv)
- [Theme Gallery](https://docs.rendercv.com/user_guide/themes/)
