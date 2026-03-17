---
name: Confluence Documentation Patterns
description: Guide for creating and managing technical documentation in Confluence with Jira integration.
version: 1.0.0
categories: [confluence, documentation, atlassian, knowledge-base, technical-writing]
trigger_phrases:
  - confluence page
  - create documentation
  - tech design
  - write to confluence
  - link confluence
  - create TDD
  - write runbook
  - architecture decision
  - ADR
  - API documentation
---

# Confluence Documentation Patterns

Create, manage, and organize technical documentation in Confluence with Jira integration.

## When to Use This Skill

- Creating technical design documents (TDD)
- Writing API documentation
- Documenting architecture decisions (ADR)
- Creating runbooks and playbooks
- Writing release notes and meeting notes
- Linking documentation to Jira issues
- Searching documentation

## Document Templates Overview

### TDD - Technical Design Document
- **When:** New features, architecture changes, complex implementations
- **Key Sections:** Executive Summary, Problem Statement, Solution, Implementation Details, Testing Strategy
- **Metadata:** Status, Author, Jira Issue link, Reviewers

### ADR - Architecture Decision Record
- **When:** Technology choices, architectural patterns, design tradeoffs
- **Key Sections:** Context, Decision, Consequences, Alternatives Considered
- **Metadata:** Status (Proposed|Accepted|Deprecated|Superseded), Date, Decision Makers

### API Documentation
- **Key Sections:** Overview, Authentication, Base URL, Endpoints, Error Handling, Examples
- **Metadata:** Version, Authentication method, Last Updated

### Runbook / Playbook
- **When:** Operational procedures, incident response
- **Key Sections:** Quick Reference, Emergency Contacts, Common Procedures, Escalation Path
- **Metadata:** Service name, Team, On-Call channel

### Release Notes
- **Key Sections:** Summary, Highlights, New Features, Bug Fixes, Breaking Changes
- **Metadata:** Release Date, Release Manager, Related Jira Release

### Meeting Notes
- **Key Sections:** Attendees, Agenda, Discussion, Action Items, Decisions
- **Metadata:** Date, Time, Location, Facilitator

### Sprint Retrospective
- **Key Sections:** Sprint Summary, What Went Well, Improvements, Action Items
- **Metadata:** Sprint number, Team, Facilitator

## Confluence Query Language (CQL)

**Basic Syntax:** `field operator value`

**Common Fields:**
- `title`, `text`, `label`, `space`, `type`, `creator`, `lastModified`, `ancestor`

**Operators:** `=`, `!=`, `~` (contains), `>`, `<`, `>=`, `<=`, `IN`, `AND`, `OR`, `NOT`

**Essential Patterns:**
```cql
label = "tdd" AND space = "ENG" ORDER BY lastModified DESC
lastModified >= now("-1w") AND space = "ENG"
title ~ "API" AND label = "authentication"
label = "adr" AND text ~ "Status: Approved"
label = "runbook" AND label = "production" AND space = "OPS"
label = "draft" AND creator = currentUser()
```

## Jira-Confluence Integration

**Linking Documentation to Issues:**
- Smart Links: `[TDD - Feature](confluence-url)` in Jira/Confluence descriptions
- Jira Macro: `{jira:PROJ-123}` displays issue card with status, assignee, summary

**Embedding Jira Data:**
- Single issue: `{jira:PROJ-123|columns=key,summary,status,assignee}`
- JQL query: `{jira:jql=project=PROJ AND status="In Progress"|columns=key,summary}`
- Issue count: `{jiraissues:project=PROJ AND type=Bug|count}`
- Timeline: `{jira-chart:type=timeline|project=PROJ}`

**Best Practices:**
- Link all documentation in Jira issue descriptions or comments
- Use labels consistently (tdd, adr, runbook, api-docs, release-notes)
- Name spaces by team/domain (ENG, OPS, PRODUCT)
- Archive documentation when superseded or deprecated
