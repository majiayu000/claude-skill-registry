---
name: firebase-services
description: Firebase Firestore, Auth, and Cloud Functions
allowed-tools: [Bash, Read, WebFetch]
---

# Firebase Services Skill

## Overview

Firebase backend services. 90%+ context savings.

## Requirements

- FIREBASE_PROJECT_ID
- GOOGLE_APPLICATION_CREDENTIALS

## Tools (Progressive Disclosure)

### Firestore

| Tool       | Description       | Confirmation |
| ---------- | ----------------- | ------------ |
| get-doc    | Get document      | No           |
| list-docs  | List documents    | No           |
| set-doc    | Create/update doc | Yes          |
| delete-doc | Delete document   | **REQUIRED** |

### Auth

| Tool       | Description     |
| ---------- | --------------- |
| list-users | List auth users |
| get-user   | Get user by UID |

### Functions

| Tool           | Description     | Confirmation |
| -------------- | --------------- | ------------ |
| list-functions | List functions  | No           |
| call-function  | Call function   | Yes          |
| deploy         | Deploy function | Yes          |

### BLOCKED

| Tool              | Status      |
| ----------------- | ----------- |
| delete-collection | **BLOCKED** |

## Agent Integration

- **developer** (primary): Firebase development
- **mobile-developer** (secondary): Mobile backends
