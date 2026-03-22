---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: n8n-workflow
description: "Automate document workflows with n8n - 7800+ workflow templates"
version: "1.0"
author: claude-office-skills
license: MIT

# Categorization
category: workflow
tags:
  - n8n
  - workflow
  - automation
  - integration
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

# Skill Capabilities
capabilities:
  - workflow_automation
  - integration

# Language Support
languages:
  - en
  - zh
---

# N8N Workflow Skill

## Overview

This skill enables document workflow automation using **n8n** - the most popular workflow automation platform with 7800+ community templates. Chain document operations, integrate with 400+ apps, and build complex document pipelines.

## How to Use

1. Describe what you want to accomplish
2. Provide any required input data or files
3. I'll execute the appropriate operations

**Example prompts:**
- "Automate PDF → OCR → Translation → Email workflow"
- "Watch folder for new contracts → Review → Notify Slack"
- "Daily report generation from multiple data sources"
- "Batch document processing with conditional logic"

## Domain Knowledge


### n8n Fundamentals

n8n uses a node-based workflow approach:

```
Trigger → Action → Action → Output
   │         │         │
   └─────────┴─────────┴── Data flows between nodes
```

### Key Node Types

| Type | Examples | Use Case |
|------|----------|----------|
| **Triggers** | Webhook, Schedule, File Watcher | Start workflow |
| **Document** | Read PDF, Write DOCX, OCR | Process files |
| **Transform** | Code, Set, Merge | Manipulate data |
| **Output** | Email, Slack, Google Drive | Deliver results |

### Workflow Example: Contract Review Pipeline

```json
{
  "nodes": [
    {
      "name": "Watch Folder",
      "type": "n8n-nodes-base.localFileTrigger",
      "parameters": {
        "path": "/contracts/incoming",
        "events": ["add"]
      }
    },
    {
      "name": "Extract Text",
      "type": "n8n-nodes-base.readPdf"
    },
    {
      "name": "AI Review",
      "type": "n8n-nodes-base.anthropic",
      "parameters": {
        "model": "claude-sonnet-4-20250514",
        "prompt": "Review this contract for risks..."
      }
    },
    {
      "name": "Save Report",
      "type": "n8n-nodes-base.writeFile"
    },
    {
      "name": "Notify Team",
      "type": "n8n-nodes-base.slack"
    }
  ]
}
```

### Self-Hosting vs Cloud

| Option | Pros | Cons |
|--------|------|------|
| **Self-hosted** | Free, full control, data privacy | Maintenance required |
| **n8n Cloud** | No setup, auto-updates | Costs at scale |

```bash
# Docker quick start
docker run -it --rm \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```


## Best Practices

1. **Start with existing templates, customize as needed**
2. **Use error handling nodes for reliability**
3. **Store credentials securely with n8n's credential manager**
4. **Test workflows with sample data before production**

## Installation

```bash
# Install required dependencies
pip install python-docx openpyxl python-pptx reportlab jinja2
```

## Resources

- [n8n Repository](https://github.com/n8n-io/n8n)
- [Claude Office Skills Hub](https://github.com/claude-office-skills/skills)
