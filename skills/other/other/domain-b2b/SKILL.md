---
name: domain-b2b
description: (ePost) Use when working in a B2B module — Inbox, Monitoring, Composer, Smart Send, Communities, Archive, Contacts, Organization
user-invocable: false

metadata:
  agent-affinity:
    - epost-fullstack-developer
    - epost-project-manager
  keywords:
    - module
    - inbox
    - monitoring
    - composer
    - smart-send
    - smart send
    - communities
    - archive
    - contacts
    - organization
    - smart-letter
  platforms:
    - web
  triggers:
    - which module
    - module structure
    - explore module
    - understand module
---

# Domain B2B Modules Skill

## Purpose

Deep per-module knowledge for B2B modules. Each module has a reference covering components, hooks, stores, API endpoints, and data flows.

## Module Index

| Module | File | Description |
|--------|------|-------------|
| Unified Inbox | `references/unified-inbox.md` | Unified inbox for messages across channels |
| Monitoring | `references/monitoring.md` | System monitoring and analytics dashboard |
| Communities | `references/communities.md` | Community/organization group management |
| Smart Send | `references/smart-send.md` | Bulk messaging with templates and audience targeting |
| Composer | `references/composer.md` | Content composition and message creation |
| Archive | `references/archive.md` | Document archival, search, and retention |
| Contacts | `references/contacts.md` | Contact management, import, and groups |
| Organization | `references/organization.md` | Organization settings, users, roles, permissions |
| Smart Letter | `references/smart-letter.md` | Letter composition and rendering (new module) |

## Usage

1. Identify module from user query
2. Read corresponding reference file
3. Navigate to relevant section (components, hooks, APIs)
4. Follow cross-module dependencies if needed

## Cross-Module Integration

- **Composer** -> **Contacts** (recipient selection)
- **Smart Send** -> **Composer** (message creation)
- **Smart Send** -> **Contacts** (audience targeting)
- **Archive** -> **Unified Inbox** (message archival)
- **Organization** -> All modules (permissions, settings)

## Data Flow Pattern

```
Component -> Hook -> Action -> Service -> Caller -> Backend API
```

## Related Skills

- `web-nextjs` — Next.js App Router conventions
- `web-ui-lib` — klara-theme component library
- `web-frontend` — React patterns
- `web-modules` — Module integration patterns
