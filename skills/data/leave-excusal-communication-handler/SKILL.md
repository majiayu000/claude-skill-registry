---
name: leave-excusal-communication-handler
description: When the user needs to communicate about approved leaves or excusals to instructors/TAs, including locating leave documents and sending reminder emails with attachments. This skill triggers when users mention 'excused assignments', 'leave documents', or need to remind instructors about approved absences. It handles document retrieval, email composition with proper context, and attachment management for official documentation.
---
# Instructions

## Primary Objective
Handle communication regarding approved leaves/excusals with instructors or TAs. This includes locating relevant leave documents, composing and sending reminder emails with proper context, and attaching official documentation.

## Trigger Conditions
This skill activates when the user mentions:
- "excused assignments"
- "leave documents"
- "approved leave"
- "remind instructor/TA about absence"
- Any scenario requiring formal communication about an approved absence affecting coursework.

## Core Workflow

### 1. Initial Context Gathering
- **Access personal information**: Use `memory-read_graph` to retrieve the user's details (name, student ID, email, enrolled courses).
- **Identify relevant course**: If not specified, list user's courses via `canvas-canvas_list_courses` and identify the correct one based on context (course name, code, or assignment mentions).
- **Review assignment status**: For the relevant course, call `canvas-canvas_list_assignments` with `include_submissions: true` to get submission status for all assignments.

### 2. Document Location & Verification
- **Search workspace**: Use `filesystem-list_allowed_directories` and `filesystem-directory_tree` to explore the accessible workspace.
- **Identify leave document**: Look for files with names containing "leave", "excusal", "absence", or similar terms. Common formats: PDF, DOC, DOCX.
- **Verify document content**: Read the identified file (`filesystem-read_file`) to confirm it's the correct leave document (contains user's name, dates, approval details).

### 3. Email Recipient Identification
- **Extract from grade records**: If a grade summary file (e.g., Excel) is mentioned, read it (`local-python-execute` with pandas) to find instructor/TA contact information.
- **Alternative sources**: Check course details from Canvas for teacher emails, or use the email pattern from the grade summary (e.g., `mcpcanvasadmin2@mcp.com`).

### 4. Email Composition & Sending
- **Subject line**: Should include: "Reminder: Approved Leave of Absence for [Assignment Name] - [User Name] ([Student ID])"
- **Body structure**:
  1. Polite greeting
  2. Clear statement of purpose (reminder about approved leave)
  3. Specific details: assignment affected, dates of leave, original approval context
  4. Request for action (update records to reflect excused status)
  5. Professional closing with contact information
- **Attachment**: Always attach the verified leave document.
- **Send email**: Use `emails-send_email` with recipient address, subject, body, and attachment path.

### 5. Assignment Handling (If Applicable)
- **Check submission requirements**: Review assignment descriptions for specific file naming conventions or submission types.
- **Submit missing work** (if requested and not excused): Only if the user explicitly asks to submit completed assignments that are missing but NOT excused.
  - Locate completed assignment files in workspace.
  - Rename files to match required conventions if specified.
  - Submit via `canvas-canvas_submit_assignment_with_file`.

## Key Constraints & Rules
- **Do NOT submit excused assignments**: If an assignment is explicitly mentioned as excused due to leave, do not attempt to submit it. Only send the reminder email.
- **Only submit existing work**: Never create assignment content. Only submit files found in the workspace.
- **Verify before sending**: Always confirm the leave document is correct and contains relevant approval details.
- **Maintain professionalism**: All communications must be formal, polite, and clearly structured.

## Error Handling
- If no leave document is found: Inform the user and ask for clarification on document location.
- If TA/instructor email cannot be identified: Use a generic course contact email or ask the user for the correct address.
- If assignment files are missing: Do not submit anything. Inform the user that completed work was not found.

## Output & Confirmation
After completing all actions, provide a clear summary to the user including:
- Which assignments were identified as missing/excused
- Which assignments were submitted (if any)
- Confirmation that the reminder email was sent
- Details of the attached document
