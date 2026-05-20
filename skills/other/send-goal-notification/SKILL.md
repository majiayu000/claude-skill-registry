---
name: send-goal-notification
description: Send a goal notification email to an employee via Google Workspace
user-invocable: true
---

You are helping HR send a goal notification email to a Jocko Fuel employee.

Follow these steps:

### Step 1: Gather Employee Information

Ask the user for:
- **Employee name**: Who is receiving the notification
- **Employee email**: Their @jockofuel.com email address
- **Notification type**: Goal setting reminder, goal review due, goal completion acknowledgment, or custom

### Step 2: Compose Notification Message

Based on the notification type, compose an email with:
- **Subject line**: Clear and action-oriented (e.g., "Goal Review Due: Q1 2026")
- **Body**: Professional tone matching Jocko Fuel culture
  - Greeting with employee name
  - Purpose of the notification
  - Required action or acknowledgment
  - Deadline (if applicable)
  - Link to goal document (if available)
  - Closing with HR contact for questions

If the user provides specific content, incorporate it. Otherwise, use the notification type to generate appropriate default content.

### Step 3: Confirm Before Sending

Display the complete email to the user:
- **To**: Employee email
- **Subject**: Email subject
- **Body**: Full email content

Ask: "Should I send this email? (yes/no)"

Do NOT send until the user explicitly confirms.

### Step 4: Send via Google Workspace

Use GAM7 or Google Workspace tools to send the email from the HR account. The send command pattern:
```bash
gam user hr@jockofuel.com sendemail recipient@jockofuel.com subject "Subject Line" message "Email body"
```

Confirm successful delivery to the user.

### Error Handling

- If the employee email is not a valid @jockofuel.com address, flag it and ask for correction
- If GAM7 is not available, provide the email content for manual sending
- If the send fails, report the error and suggest the user send manually via Gmail
