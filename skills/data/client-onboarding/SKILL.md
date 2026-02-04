---
name: client-onboarding
description: Use this skill when onboarding new clients, starting projects, gathering requirements, or setting up client access. Provides intake questionnaires, project kickoff checklists, access request templates, and onboarding workflows. Invoke for any new client setup, project initiation, or client information gathering.
---

# Client Onboarding System

Streamlined onboarding process for Support Forge consulting clients.

## Onboarding Phases

```
1. INTAKE → 2. SETUP → 3. KICKOFF → 4. HANDOFF
   │           │          │           │
   │           │          │           └─ Documentation
   │           │          └─ First session
   │           └─ Access & tools
   └─ Questionnaire
```

## Phase 1: Client Intake Questionnaire

### Basic Information
```
CLIENT INTAKE FORM
==================

CONTACT INFORMATION
-------------------
Full Name:
Title/Role:
Company Name:
Email:
Phone:
Preferred Contact Method: [ ] Email [ ] Phone [ ] Text [ ] Slack

COMPANY DETAILS
---------------
Industry:
Company Size: [ ] Solo [ ] 2-10 [ ] 11-50 [ ] 51-200 [ ] 200+
Website:
Location:

HOW DID YOU HEAR ABOUT US?
--------------------------
[ ] Referral (from whom?): ________________
[ ] Website
[ ] LinkedIn
[ ] Other: ________________
```

### Project Information
```
PROJECT DETAILS
===============

What brings you to Support Forge today?
_______________________________________

What's the primary problem you're trying to solve?
_______________________________________

What does success look like for this project?
_______________________________________

Timeline:
[ ] ASAP
[ ] Within 2 weeks
[ ] Within 1 month
[ ] Within 3 months
[ ] Flexible

Budget Range:
[ ] Under $1,500
[ ] $1,500 - $3,500
[ ] $3,500 - $7,500
[ ] $7,500 - $15,000
[ ] $15,000+
[ ] Not sure / Need guidance
```

### Technical Assessment (AI Enablement)
```
TECHNICAL BACKGROUND
====================

Current Tech Stack:
- Primary OS: [ ] Windows [ ] Mac [ ] Linux
- Code Editor: [ ] VS Code [ ] Cursor [ ] Other: ______
- Version Control: [ ] GitHub [ ] GitLab [ ] None [ ] Other: ______

Experience Level:
- Programming: [ ] None [ ] Beginner [ ] Intermediate [ ] Advanced
- AI Tools: [ ] None [ ] Beginner [ ] Intermediate [ ] Advanced
- Command Line: [ ] None [ ] Beginner [ ] Intermediate [ ] Advanced

Current AI Tools Used:
[ ] ChatGPT
[ ] Claude (web)
[ ] Claude Code
[ ] GitHub Copilot
[ ] Cursor
[ ] Other: ________________
[ ] None

What would you like to accomplish with AI?
_______________________________________

Services/Integrations Needed:
[ ] Email (Gmail/Outlook)
[ ] Calendar
[ ] GitHub
[ ] Slack
[ ] Database
[ ] AWS
[ ] Google Cloud
[ ] Custom APIs
[ ] Other: ________________
```

### Website/Development Intake
```
WEBSITE PROJECT DETAILS
=======================

Project Type:
[ ] New website
[ ] Website redesign
[ ] Add features to existing site
[ ] E-commerce
[ ] Web application
[ ] Other: ________________

Do you have existing:
- Domain? [ ] Yes: _____________ [ ] No
- Hosting? [ ] Yes: _____________ [ ] No
- Branding/Logo? [ ] Yes [ ] No
- Content (copy/images)? [ ] Yes [ ] Partial [ ] No

Design Preferences:
- Sites you like (URLs):
  1.
  2.
  3.

- Style: [ ] Modern [ ] Classic [ ] Minimal [ ] Bold [ ] Other: ____

Features Needed:
[ ] Contact form
[ ] Blog
[ ] E-commerce/Shop
[ ] Booking/Scheduling
[ ] Member login
[ ] Newsletter signup
[ ] Social media integration
[ ] Other: ________________
```

## Phase 2: Access & Setup Checklist

### Credentials Collection Template
```
ACCESS CREDENTIALS
==================
⚠️ Share via secure method (1Password, LastPass, or encrypted)

For AI Enablement:
[ ] GitHub account access
[ ] Google account (for Workspace APIs)
[ ] AWS account (if applicable)
[ ] Anthropic API key (or we'll set up)
[ ] Other API keys needed: ________________

For Website Projects:
[ ] Domain registrar login
[ ] Hosting/server access
[ ] Current site admin access
[ ] Analytics access (Google Analytics)
[ ] Social media accounts (if integrating)

For General:
[ ] Preferred communication channel setup
[ ] Calendar access for scheduling
```

### Environment Setup Checklist
```
ENVIRONMENT SETUP - [Client Name]
=================================

□ Client folder created
  Location: ~/Clients/[ClientName]/

□ Project repository initialized
  Repo: github.com/[org]/[project]

□ Communication channel established
  [ ] Email thread
  [ ] Slack channel
  [ ] Other: ________

□ Credentials stored securely
  [ ] Received from client
  [ ] Stored in secure location
  [ ] Tested access

□ Billing setup
  [ ] Engagement letter signed
  [ ] Payment received
  [ ] Invoice sent (if needed)

□ Calendar events created
  [ ] Kickoff call scheduled
  [ ] Working sessions scheduled
  [ ] Follow-up sessions scheduled
```

## Phase 3: Kickoff Meeting

### Kickoff Agenda Template
```
KICKOFF MEETING AGENDA
======================
Client: [Name]
Date: [Date]
Duration: 30-60 minutes

1. INTRODUCTIONS (5 min)
   - Confirm roles and contacts
   - Communication preferences

2. PROJECT OVERVIEW (10 min)
   - Review scope from engagement letter
   - Confirm understanding of goals
   - Clarify any questions

3. TIMELINE & MILESTONES (10 min)
   - Key dates and deadlines
   - Session schedule
   - Availability constraints

4. ACCESS & LOGISTICS (10 min)
   - Confirm all access received
   - Test critical connections
   - Identify any blockers

5. FIRST STEPS (10 min)
   - What happens immediately after call
   - Client's homework (if any)
   - Next touchpoint

6. Q&A (5 min)
   - Open questions
   - Concerns to address
```

### Kickoff Email Template
```
Subject: [Project Name] - Kickoff & Next Steps

Hi [Name],

Great connecting today! Here's a summary of our kickoff:

PROJECT OVERVIEW
- [Brief scope summary]
- Goal: [Primary objective]
- Timeline: [Key dates]

IMMEDIATE NEXT STEPS

My actions:
1. [Action item]
2. [Action item]
3. [Action item]

Your actions (if any):
1. [Action item]
2. [Action item]

UPCOMING SESSIONS
- [Date/Time] - [Session purpose]
- [Date/Time] - [Session purpose]

ACCESS CONFIRMED
✓ [Access item]
✓ [Access item]
⏳ [Pending item]

Questions? Reply to this email or text me at {YOUR_PHONE}.

Let's build something great!

Perry
SupportForge
```

## Phase 4: Documentation & Handoff

### Project Documentation Template
```
PROJECT DOCUMENTATION
=====================
Client: [Name]
Project: [Description]
Completed: [Date]

WHAT WAS DELIVERED
------------------
1. [Deliverable]
   - Details
   - Location/access

2. [Deliverable]
   - Details
   - Location/access

CREDENTIALS & ACCESS
--------------------
[Document all accounts created, where credentials stored]

CONFIGURATION DETAILS
---------------------
[Technical details client needs to know]

HOW TO USE
----------
[Key instructions for client]

MAINTENANCE & UPDATES
---------------------
[What client needs to do ongoing]

SUPPORT
-------
- Support period: [dates]
- Contact: contact@support-forge.com
- Follow-up session: [date if applicable]
```

### Handoff Email Template
```
Subject: [Project Name] - Complete! 🎉

Hi [Name],

Great news - your [project] is complete!

WHAT'S READY
------------
✓ [Deliverable 1]
✓ [Deliverable 2]
✓ [Deliverable 3]

DOCUMENTATION
-------------
I've attached complete documentation including:
- Setup details
- How-to guides
- Credential locations
- Troubleshooting tips

SUPPORT PERIOD
--------------
You have [X] of support through [date]. Don't hesitate
to reach out with any questions.

FOLLOW-UP SESSION
-----------------
We have a 30-minute follow-up scheduled for [date/time].
Come with any questions!

It's been a pleasure working with you. If you know anyone
who could benefit from similar services, referrals are
always appreciated!

Best,
Perry
```

## Quick Reference Checklists

### New AI Enablement Client
```
□ Intake questionnaire completed
□ Engagement letter signed
□ Payment received
□ Kickoff scheduled
□ Access credentials received:
  □ GitHub
  □ Google account
  □ Other APIs
□ Environment setup:
  □ Claude Code installed
  □ MCP servers configured
  □ Skills installed
□ Training sessions completed
□ Documentation delivered
□ Follow-up scheduled
```

### New Website Client
```
□ Intake questionnaire completed
□ Proposal/contract signed
□ Deposit received
□ Kickoff scheduled
□ Access received:
  □ Domain registrar
  □ Hosting
  □ Content/assets
□ Design approved
□ Development complete
□ Client review/feedback
□ Revisions complete
□ Launch checklist done
□ Training provided
□ Handoff documentation
□ Final payment received
```

## Client Folder Structure
```
~/Clients/
└── [ClientName]/
    ├── 00-admin/
    │   ├── engagement-letter.pdf
    │   ├── invoices/
    │   └── notes.md
    ├── 01-intake/
    │   ├── questionnaire.md
    │   └── requirements.md
    ├── 02-project/
    │   ├── [project files]
    │   └── documentation/
    ├── 03-deliverables/
    │   └── [final deliverables]
    └── 04-handoff/
        └── handoff-docs.md
```

## Automation Ideas

### Auto-create Client Folder
```bash
#!/bin/bash
CLIENT_NAME=$1
BASE_DIR=~/Clients

mkdir -p "$BASE_DIR/$CLIENT_NAME"/{00-admin/invoices,01-intake,02-project/documentation,03-deliverables,04-handoff}

echo "# $CLIENT_NAME - Project Notes" > "$BASE_DIR/$CLIENT_NAME/00-admin/notes.md"
echo "Created client folder structure for $CLIENT_NAME"
```

### Calendar Integration
Use Google Calendar MCP to:
- Create kickoff events
- Schedule working sessions
- Set follow-up reminders
- Block time for project work

### Email Templates
Use Gmail MCP to:
- Send intake questionnaires
- Deliver kickoff summaries
- Send completion notifications
- Request feedback/testimonials
