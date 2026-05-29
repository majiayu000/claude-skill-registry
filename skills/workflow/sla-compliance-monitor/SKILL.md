---
name: sla-compliance-monitor
description: When the user needs to monitor SLA compliance for support tickets or service requests, this skill identifies overdue items by querying databases, analyzing SLA documentation from PDFs, and generating automated notifications. It handles 1) Database exploration to find relevant tables (support tickets, users), 2) PDF analysis to extract SLA rules and email templates, 3) SQL queries to identify tickets exceeding response times based on user service levels, and 4) Automated email generation for manager reminders and customer apologies using extracted templates. Triggers include 'SLA compliance', 'overdue tickets', 'response time monitoring', 'send reminder emails', 'apology emails', 'ticket monitoring', and 'service level agreement'.
---
# SLA Compliance Monitor

## Overview
This skill automates the monitoring of Service Level Agreement (SLA) compliance for support tickets. It identifies tickets that have exceeded their first response time based on user service levels, extracts email templates from SLA documentation, and sends automated notifications to responsible managers and affected customers.

## Prerequisites
Ensure the following tools are available:
- Snowflake database access (for `snowflake-*` tools)
- Filesystem access to locate SLA documentation PDFs
- PDF processing tools (`pdf-tools-*`)
- Email sending capability (`emails-send_email`)

## Core Workflow

### Phase 1: Environment Discovery
1. **Identify the target database:**
   - List available databases using `snowflake-list_databases`
   - Look for databases with names suggesting SLA/ticket monitoring (e.g., `SLA_MONITOR`)

2. **Explore the filesystem for SLA documentation:**
   - List allowed directories using `filesystem-list_allowed_directories`
   - Search for PDF files containing SLA information (e.g., `sla_manual.pdf`, `slamanual.pdf`)
   - Extract archived documents if needed (e.g., `.tar.gz` files)

### Phase 2: Schema & Document Analysis
1. **Examine database structure:**
   - List schemas in the target database
   - List tables, focusing on `SUPPORT_TICKETS` and `USERS` tables
   - Describe table structures to understand column relationships

2. **Analyze SLA documentation:**
   - Read PDFs to extract SLA rules (response times per service level)
   - Extract email templates for manager reminders and customer apologies
   - **Critical:** Verify document validity - ignore documents marked as "OBSOLETE"

### Phase 3: Identify Overdue Tickets
1. **Query for overdue tickets:**
   - Join `SUPPORT_TICKETS` with `USERS` on `USER_ID`
   - Filter for tickets where `FIRST_RESPONSE_AT` IS NULL
   - Calculate hours elapsed since `CREATED_AT`
   - Apply SLA thresholds based on `SERVICE_LEVEL`:
     - `basic`: 72 hours
     - `pro`: 36 hours  
     - `max`: 24 hours
   - Order results by service level priority (max → pro → basic) then creation date

2. **Use the SQL query template** from `references/sla_query.sql`

### Phase 4: Generate & Send Notifications
1. **Organize tickets by responsible manager** using `CUSTOMER_MANAGER` field
2. **Send manager reminder emails:**
   - Use template from `assets/manager_reminder_template.txt`
   - List tickets in max → pro → basic order
   - Include ticket numbers and service levels
3. **Send customer apology emails:**
   - Use template from `assets/customer_apology_template.txt`
   - Customize with:
     - `{TICKET_NUMBER}`
     - `{SECOND_REPLY_TIME}` (based on service level: max=18h, pro=36h, basic=72h)

## Key Considerations
- **Document Version Control:** Always check for "OBSOLETE" markers in PDFs
- **Time Calculations:** Use `TIMESTAMPDIFF(HOUR, CREATED_AT, CURRENT_TIMESTAMP())` for accurate elapsed time
- **Email Templates:** Strictly follow the templates specified in the SLA documentation
- **Error Handling:** If no overdue tickets are found, provide a clear status message
- **Data Privacy:** Ensure email addresses are handled appropriately

## Output
Provide a summary report including:
- Number of overdue tickets identified
- Breakdown by service level and manager
- Confirmation of emails sent
- Any errors or warnings encountered
