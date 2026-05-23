---
name: interview-scheduler
description: When the user needs to schedule interviews or meetings with specific time constraints (e.g., within certain dates, during working hours, with minimum duration requirements). This skill calculates available time slots based on date ranges, working hour constraints, and duration needs, then creates calendar events with appropriate details. Triggers include phrases like 'schedule interviews', 'book time slots', 'within [date range]', 'during working hours', or 'reserve [duration] for meeting'.
---
# Skill: Interview Scheduler

## Objective
Schedule candidate interviews by identifying qualified applicants from email resumes and booking time slots that meet all specified constraints.

## Core Workflow

### Phase 1: Candidate Identification & Qualification
1.  **Search for Resumes:** Use the `emails-search_emails` tool with a query like "resume" or "application" to find relevant emails.
2.  **Extract & Review:** Read each candidate's email (`emails-read_email`) to parse their resume content.
3.  **Apply Qualification Filter:** The primary filter is **independent first-author publications**. Look for phrases like "First Author", "Sole Author", or "Lead Author" in the publications section. Candidates without such publications are disqualified.
4.  **Extract Candidate Info:** For qualified candidates, note:
    *   Name
    *   Email
    *   Key publications (for calendar description)
    *   Research area/university (for context)

### Phase 2: Time Slot Calculation & Scheduling
1.  **Parse Time Constraints:** Extract from the user request:
    *   **Date Range:** Identify "tomorrow", "the day after tomorrow", or other explicit date windows. Use the system's current date or the latest email date as a reference if needed.
    *   **Working Hours:** Default is 8 AM to 5 PM in the user's/local timezone (e.g., `Asia/Hong_Kong`). Confirm or adjust per request.
    *   **Minimum Duration:** Default is 1.5 hours. Confirm per request.
2.  **Generate Slots:** Mentally allocate sequential slots within the date range and working hours, ensuring the minimum duration and a reasonable buffer (e.g., 30 mins) between interviews if scheduling multiple candidates on the same day.
3.  **Create Calendar Events:** For each qualified candidate, use `google_calendar-create_event`.
    *   **Summary:** Format as `"Interview with [Candidate Name]"`
    *   **Description:** Include a brief candidate summary: university, research area, key qualifying publication(s), and contact info (email/phone from resume).
    *   **Start/End Time:** Use the calculated slot in ISO 8601 format with the correct timezone.
    *   **Duration:** Must meet or exceed the user's minimum requirement.

### Phase 3: Summary & Confirmation
1.  **Present Results:** Provide a clear summary table showing:
    *   Qualified candidates and their key publication.
    *   Scheduled date, time slot, and duration.
    *   Disqualified candidates and the reason (e.g., "No first-author publications").
2.  **Confirm Sync:** State that events have been created in Google Calendar.
3.  **Mark Task Complete:** Use `local-claim_done`.

## Key Decision Logic
*   **Slot Allocation:** Schedule on the earliest available date within the range. If the first day fills up, use the next day.
*   **Buffer Time:** It is good practice to leave at least 30 minutes between interviews for preparation/notes, but this is not a strict rule if the user does not specify it.
*   **Date Reference:** If the user says "tomorrow," use the date context from the most recent email in the thread or the current system date to calculate the actual dates.

## Tools Required
*   `emails-search_emails`
*   `emails-read_email`
*   `google_calendar-create_event`
*   `local-claim_done`
