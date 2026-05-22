---
name: supabase-db
description: Supabase database, auth, and storage operations
allowed-tools: [Bash, Read, WebFetch]
---

# Supabase Skill

## Overview

Supabase backend-as-a-service. 90%+ context savings.

## Requirements

- SUPABASE_URL
- SUPABASE_ANON_KEY or SUPABASE_SERVICE_KEY

## Tools (Progressive Disclosure)

### Database

| Tool   | Description   | Confirmation |
| ------ | ------------- | ------------ |
| select | Query data    | No           |
| insert | Insert rows   | Yes          |
| update | Update rows   | Yes          |
| delete | Delete rows   | **REQUIRED** |
| rpc    | Call function | Yes          |

### Auth

| Tool       | Description      |
| ---------- | ---------------- |
| list-users | List users       |
| get-user   | Get user details |

### Storage

| Tool         | Description   | Confirmation |
| ------------ | ------------- | ------------ |
| list-buckets | List buckets  | No           |
| upload       | Upload file   | Yes          |
| download     | Download file | No           |

### BLOCKED

| Tool          | Status      |
| ------------- | ----------- |
| delete-bucket | **BLOCKED** |

## Agent Integration

- **developer** (primary): Backend development
- **database-architect** (secondary): Schema design
