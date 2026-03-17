---
name: jira-ticket-creator
description: This skill should be used when users need to create Jira tickets for the RD (Research & Development) project. It supports creating features, bugs, and tasks with proper field mapping including assignee, team, sprint, and state. The skill uses Jira CLI commands and provides templates for different ticket types.
---

# Jira Ticket Creator

## Overview

This skill enables creation and management of Jira tickets in the RD project using the Jira CLI. It supports three ticket types: Features (with PRD-like content), Bugs (with problem analysis), and Tasks (general work items).

## Quick Start

To create a Jira ticket, determine the ticket type and gather required information:

1. **Feature**: Summary, description, optional assignee/team/sprint
2. **Bug**: Summary, problem description, reproduction steps, resolution hypothesis, optional assignee/team/sprint  
3. **Task**: Summary, description, optional assignee/team/sprint

## Core Capabilities

### 1. Create Feature Tickets

Use for new capabilities or significant enhancements.

Execute the jira_helper.py script with feature parameters:
```bash
python scripts/jira_helper.py create-feature "<summary>" "<description>" [assignee] [team] [sprint]
```

The script automatically formats the description with PRD-like sections:
- Feature Overview
- Requirements  
- Acceptance Criteria
- Technical Considerations

### 2. Create Bug Tickets

Use for issues where the system behaves incorrectly.

Execute the jira_helper.py script with bug parameters:
```bash
python scripts/jira_helper.py create-bug "<summary>" "<problem>" "<reproduction-steps>" "<resolution-hypothesis>" [assignee] [team] [sprint]
```

The script automatically formats the description with problem analysis sections:
- Problem Description
- Steps to Reproduce
- Expected vs Actual Behavior
- Resolution Hypothesis
- Additional Context

### 3. Create Task Tickets

Use for general work items that don't fit as features or bugs.

Execute the jira_helper.py script with task parameters:
```bash
python scripts/jira_helper.py create-task "<summary>" "<description>" [assignee] [team] [sprint]
```

### 4. List and Update Tickets

List tickets in the RD project:
```bash
python scripts/jira_helper.py list
```

Update existing tickets using the Jira CLI directly:
```bash
jira issue update TICKET-123 --status "In Progress" --assignee username
```

## Decision Tree

1. **What type of work item do you need?**
   - New capability/enhancement → Create Feature Ticket
   - Something is broken → Create Bug Ticket  
   - General work item → Create Task Ticket

2. **Do you have all required information?**
   - Feature: summary + description
   - Bug: summary + problem + reproduction + hypothesis
   - Task: summary + description

3. **Optional fields available?**
   - Assignee, team, sprint → Include in command

## Resources

### scripts/jira_helper.py
Python script that provides a wrapper around Jira CLI commands. Handles ticket creation with proper formatting and field mapping for the RD project. Can be executed directly or imported as a module.

### references/ticket_templates.md
Detailed templates and guidelines for each ticket type. Includes required fields, description structures, and best practices for writing effective tickets.

### references/jira_commands.md
Comprehensive reference for Jira CLI commands including installation, configuration, core operations, and advanced usage patterns.

## Usage Examples

**Create a feature ticket:**
```
User: "Create a feature ticket for implementing user authentication with two-factor support"
→ Use create-feature with appropriate summary and description
```

**Create a bug ticket:**
```
User: "The login page crashes when users enter special characters in the password field"
→ Use create-bug with problem description and reproduction steps
```

**Create a task ticket:**
```
User: "I need a task to upgrade the database schema for the next release"
→ Use create-task with clear description of the upgrade work
```
