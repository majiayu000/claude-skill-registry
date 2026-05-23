---
name: sendgrid-email
description: SendGrid email sending and templates
allowed-tools: [Bash, Read, WebFetch]
---

# SendGrid Email Skill

## Overview

Email via SendGrid API. 90%+ context savings.

## Requirements

- SENDGRID_API_KEY

## Tools (Progressive Disclosure)

### Send

| Tool          | Description        | Confirmation |
| ------------- | ------------------ | ------------ |
| send          | Send email         | Yes          |
| send-template | Send with template | Yes          |

### Templates

| Tool           | Description          |
| -------------- | -------------------- |
| list-templates | List templates       |
| get-template   | Get template details |

### Activity

| Tool        | Description     |
| ----------- | --------------- |
| get-stats   | Get email stats |
| get-bounces | Get bounce list |
| get-blocks  | Get block list  |

## Agent Integration

- **developer** (primary): Email integration
- **devops** (secondary): Transactional emails
