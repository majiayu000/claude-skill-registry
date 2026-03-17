---
name: create-goal-doc
description: Create a goal document in Google Drive for an employee
user-invocable: true
---

You are helping HR create a goal document in Google Drive for a Jocko Fuel employee.

Follow these steps:

### Step 1: Gather Goal Details

Ask the user for:
- **Employee name**: Who the goals are for
- **Employee email**: Their @jockofuel.com email
- **Review period**: Q1/Q2/Q3/Q4 and year (e.g., "Q1 2026")
- **Department**: Employee's department
- **Manager**: Employee's direct manager name

### Step 2: Collect Goals

For each goal, gather:
- **Goal title**: Brief description
- **Category**: Performance, Development, Team, or Company
- **Description**: What success looks like
- **Key results**: Measurable outcomes (2-3 per goal)
- **Timeline**: Start and end dates or milestones

Accept 3-5 goals per employee. If the user provides fewer, ask if they want to add more.

### Step 3: Generate Document Content

Create a structured goal document with:
- **Header**: Employee name, department, manager, review period
- **Goals section**: Each goal with title, category, description, key results, and timeline
- **Self-assessment section** (blank): Space for employee to track progress
- **Manager review section** (blank): Space for manager feedback
- **Signatures section**: Employee and manager sign-off lines

### Step 4: Create Google Doc

Use Google Workspace tools to:
1. Create a new Google Doc in the HR Goals folder
2. Name it: `{Employee Name} - Goals {Review Period}` (e.g., "Gordon Divine - Goals Q1 2026")
3. Populate with the generated content
4. Share with the employee (edit access) and their manager (comment access)

Confirm with the user before sharing.

### Step 5: Confirm Creation

Provide:
- Google Doc URL
- Sharing status (who has access)
- Suggested next step: Send goal notification via `/jf-hr-essentials:send-goal-notification`

### Error Handling

- If Google Drive access is unavailable, output the document content as markdown for manual creation
- If the employee email is invalid, flag before creating the document
- If the HR Goals folder doesn't exist, ask the user where to create the document
