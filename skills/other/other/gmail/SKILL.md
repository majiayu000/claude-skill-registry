---
name: gmail
description: Comprehensive guide for using Gmail tools to send emails, manage drafts, and handle attachments. Use when the user asks to send emails, check inbox, search contacts, or manage labels.
---

# Gmail Skill

This skill provides best practices and workflows for using the Gmail toolkit effectively.

## Core Capabilities

1.  **Sending Emails**: `GMAIL_SEND_EMAIL`
2.  **Draft Management**: `GMAIL_CREATE_EMAIL_DRAFT`, `GMAIL_SEND_DRAFT`
3.  **Inbox Management**: `GMAIL_FETCH_EMAILS`, `GMAIL_LIST_THREADS`
4.  **Label Management**: `GMAIL_CREATE_LABEL`, `GMAIL_ADD_LABEL_TO_EMAIL`

## Critical Usage Guidelines

### 1. Handling Attachments (IMPORTANT)

The `GMAIL_SEND_EMAIL` tool definition can be ambiguous regarding attachments.

*   **Single File**: Use the `attachment` parameter (object with `s3key`, `name`, `mimetype`).
*   **Multiple Files**:
    *   **Preferred**: Look for an `attachments` (plural) parameter if available in the tool definition.
    *   **Fallback**: If `attachments` is not available, you **CANNOT** pass a list to the singular `attachment` field. You must zip the files into a single archive and send that as the single `attachment`.
    *   **Constraint**: Do NOT send multiple separate emails just to send multiple attachments unless explicitly requested.

### 2. Sending HTML Emails

*   Always set `is_html=True` if your `body` contains any HTML tags (e.g., `<b>`, `<br>`, `<ul>`).
*   If `is_html=False` (default), the body will be rendered as plain text, showing the raw HTML tags to the recipient.

### 3. Drafts First Policy (Best Practice)

For critical or sensitive emails, prefer creating a draft first (`GMAIL_CREATE_EMAIL_DRAFT`) and asking the user to confirm/send it, rather than sending immediately with `GMAIL_SEND_EMAIL`, unless the user explicitly said "send this email".

## Common Workflows

### Sending a Report

1.  **Generate Content**: Create the file (e.g., PDF report).
2.  **Verify Files**: Ensure the file exists and you have the path.
3.  **Send**:
    ```json
    // 1) Upload the local file to Composio for attachment
    mcp__internal__upload_to_composio({
      "path": "/path/to/report.pdf",
      "tool_slug": "GMAIL_SEND_EMAIL",
      "toolkit_slug": "gmail"
    })

    // 2) Use the returned s3key in the email attachment
    GMAIL_SEND_EMAIL(
      recipient_email="user@example.com",
      subject="Weekly Report",
      body="Here is your report.",
      attachment={
        "s3key": "<from upload_to_composio>",
        "name": "report.pdf",
        "mimetype": "application/pdf"
      }
    )
    ```
    - Use `mcp__internal__upload_to_composio` for attachment uploads.

### Responding to a Thread

1.  **Find Thread**: Use `GMAIL_LIST_THREADS` or `GMAIL_FETCH_EMAILS` to find the context.
2.  **Get ID**: Extract the `thread_id`.
3.  **Reply**: Use `GMAIL_REPLY_TO_THREAD` with the `thread_id` to ensure the email threads correctly in the recipient's inbox.

## Troubleshooting

*   **"Attachment Error"**: If sending fails with an attachment error, verify you aren't passing a list to a singular field.
*   **"Authentication Error"**: Ensure the `user_id` is set to 'me' or the correct email address.
*   **"Composio SDK Error"**: Do NOT call `from composio import ...` in Bash/Python. Always use the MCP tools.
