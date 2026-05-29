---
name: gemini-ssh
description: AI-assisted SSH operations with Gemini
allowed-tools: [Bash, Read]
---

# Gemini SSH Skill

## Overview

AI-assisted SSH with Gemini analysis. 90%+ context savings.

## Requirements

- SSH key configured
- GOOGLE_API_KEY for Gemini analysis

## Tools (Progressive Disclosure)

### Connection

| Tool     | Description            | Confirmation |
| -------- | ---------------------- | ------------ |
| connect  | SSH connect            | Yes          |
| exec     | Execute remote command | Yes          |
| upload   | Upload file (scp)      | Yes          |
| download | Download file (scp)    | No           |

### Analysis

| Tool           | Description              |
| -------------- | ------------------------ |
| analyze-logs   | AI analyze remote logs   |
| suggest-fix    | Suggest fixes for errors |
| explain-output | Explain command output   |

### Management

| Tool            | Description           |
| --------------- | --------------------- |
| list-hosts      | List known hosts      |
| test-connection | Test SSH connectivity |

### BLOCKED

| Tool     | Status      |
| -------- | ----------- |
| rm -rf / | **BLOCKED** |
| shutdown | **BLOCKED** |
| reboot   | **BLOCKED** |

## Agent Integration

- **devops** (primary): Server management
- **incident-responder** (secondary): Remote debugging
