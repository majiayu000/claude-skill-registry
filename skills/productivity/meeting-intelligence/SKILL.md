---
name: meeting-intelligence
description: Prepare for meetings by gathering context and creating comprehensive agendas
---

## Overview

The Meeting Intelligence skill prepares you for productive meetings by automatically gathering relevant context, analyzing past interactions, and creating comprehensive meeting agendas. It helps ensure you enter meetings informed and prepared.

## When to Use

Use this skill when you need to:
- Prepare for important meetings
- Gather context about attendees and topics
- Create comprehensive meeting agendas
- Review past interactions with participants
- Identify potential discussion points and blockers
- Prepare background materials for meetings

## Features

- **Context Gathering**: Automatically collects relevant documentation and past interactions
- **Attendee Analysis**: Gathers information about meeting participants
- **Agenda Creation**: Generates structured meeting agendas with timing
- **Background Materials**: Compiles reference materials and context documents
- **Risk/Blocker Identification**: Surfaces potential issues to address
- **Decision Tracking**: Monitors previously made decisions relevant to the meeting

## Requirements

- **Notion API Access**: For retrieving documentation and meeting history
- **Calendar Integration (Optional)**: To pull meeting details
- **Context Database**: Notion database with relevant background information
- **Team Database**: Directory of team members and their expertise areas

## Implementation Details

This skill leverages Notion as a knowledge base to:

1. Search relevant documentation and past meetings
2. Analyze attendee profiles and expertise areas
3. Identify agenda items based on historical context
4. Create structured agenda pages in Notion
5. Compile background materials and references
6. Track follow-up items from previous meetings

### Meeting Preparation Workflow

```
Meeting Request
  ↓
Extract Meeting Details
  ↓
Search Relevant Context
  ↓
Analyze Attendees
  ↓
Identify Agenda Items
  ↓
Compile Background Materials
  ↓
Create Comprehensive Agenda
  ↓
Output: Prepared Meeting Document
```

## Example Use Cases

1. **Executive Status Meeting**
   - Gathers recent project updates, metrics, and blockers
   - Creates agenda aligned with executive focus areas
   - Prepares data and trend analysis

2. **Client Meeting**
   - Compiles project history, agreements, and past discussions
   - Identifies open items and next steps
   - Creates agenda addressing client concerns

3. **One-on-One**
   - Gathers feedback, performance notes, and career development info
   - Creates agenda with growth and feedback discussion

4. **Cross-functional Planning**
   - Collects input from all stakeholders
   - Identifies dependencies and potential conflicts
   - Creates comprehensive coordination agenda

## Configuration

```env
NOTION_API_TOKEN=your_token_here
MEETING_DATABASE_ID=your_database_id
CONTEXT_DATABASE_ID=your_context_database_id
ATTENDEE_DATABASE_ID=your_attendee_database_id
```

## See Also

- [Knowledge Capture](/skills/knowledge-capture) - For documenting meeting outcomes
- [Research Documentation](/skills/research-documentation) - For background research
- [Spec to Implementation](/skills/spec-to-implementation) - For meeting-driven implementation planning
- [Notion Database Documentation](https://developers.notion.com/reference/database)
