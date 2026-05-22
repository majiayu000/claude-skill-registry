---
name: netlify-deploy
description: Netlify deployment and site management
allowed-tools: [Bash, Read, WebFetch]
---

# Netlify Deploy Skill

## Overview

Netlify deployment management. 90%+ context savings.

## Requirements

- NETLIFY_AUTH_TOKEN

## Tools (Progressive Disclosure)

### Sites

| Tool       | Description      |
| ---------- | ---------------- |
| list-sites | List sites       |
| get-site   | Get site details |

### Deploys

| Tool          | Description        | Confirmation |
| ------------- | ------------------ | ------------ |
| list-deploys  | List deployments   | No           |
| create-deploy | Create deployment  | Yes          |
| rollback      | Rollback to deploy | Yes          |
| lock-deploy   | Lock production    | Yes          |

### Functions

| Tool              | Description       |
| ----------------- | ----------------- |
| list-functions    | List functions    |
| get-function-logs | Get function logs |

### Environment

| Tool    | Description       | Confirmation |
| ------- | ----------------- | ------------ |
| get-env | Get env variables | No           |
| set-env | Set env variable  | Yes          |

## Agent Integration

- **devops** (primary): Deployment
- **developer** (secondary): Site management
