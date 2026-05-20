---
name: bulk-goal-notifications
description: Send goal notifications to multiple employees in batch
user-invocable: true
---

You are helping HR send goal notification emails to multiple Jocko Fuel employees.

Follow these steps:

### Step 1: Gather Employee List

Ask the user for the list of employees. Accept any format:
- Comma-separated names/emails
- Pasted from a spreadsheet (name, email columns)
- "All employees" or "All in [department]"
- A file path to a CSV

Parse the input into a structured list of (name, email) pairs.

### Step 2: Compose Message Template

Ask the user for:
- **Notification type**: Goal setting reminder, goal review due, goal completion acknowledgment, or custom
- **Custom message** (optional): Any specific content to include

Generate a message template with a `{name}` placeholder for personalization. The template should include:
- Subject line
- Personalized greeting
- Notification body
- Required action and deadline
- HR contact information

### Step 3: Preview All Notifications

Show the user:
- **Total recipients**: Count of employees
- **Sample email**: Full preview for the first recipient (with placeholders filled)
- **Recipient list**: Table of all names and emails

Ask: "Should I send these {count} notifications? (yes/no)"

Do NOT send until the user explicitly confirms.

### Step 4: Send Batch

For each employee, personalize and send the email via Google Workspace tools:
```bash
gam user hr@jockofuel.com sendemail recipient@jockofuel.com subject "Subject" message "Personalized body"
```

Report progress:
- Total sent
- Any failures with specific employee names and error details

### Step 5: Summary

Present a delivery report:
- Successfully sent: X of Y
- Failed: List any failures with reasons
- Recommended follow-up for failed sends

### Error Handling

- If any email addresses are invalid, list them and ask the user to correct before sending
- If the employee list is empty or unparseable, ask for clarification
- If GAM7 is not available, export the personalized emails for manual sending
- If a partial batch fails, report which succeeded and which failed
