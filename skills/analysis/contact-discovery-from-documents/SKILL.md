---
name: contact-discovery-from-documents
description: When the agent needs to find specific contact information or responsible personnel for a particular domain or system. This skill searches through available documents (PDFs, config files, emails) to locate relevant contact details, organizational charts, or responsibility assignments. It can parse structured documents for contact tables, search for role-based keywords, and extract email addresses and names associated with specific responsibilities. Triggers include 'find contact', 'responsible person', 'team member', 'who manages', 'email address', 'contact information', 'PDF analysis', 'document search', 'role-based lookup'.
---
# Skill: Contact Discovery from Documents

## Purpose
Find contact information (names, emails, roles) for specific responsibilities by searching and analyzing available documents, emails, and configuration files.

## Core Workflow
1.  **Understand the Search Target:** Clarify the role, responsibility, or system you need a contact for (e.g., "cluster management," "network administrator," "billing department").
2.  **Search Across Available Sources:**
    *   **Emails:** Use `emails-search_emails` with relevant keywords (role, system name, department).
    *   **Filesystem:** Use `filesystem-search_files` and `filesystem-list_directory` to locate documents (PDFs, text files, configs) in common workspace areas.
    *   **PDFs:** For PDF files, use `pdf-tools-read_pdf_pages` to extract and analyze text, especially looking for structured sections like contact tables or responsibility matrices.
    *   **Config Files:** Read relevant configuration files (YAML, JSON, text) that may contain admin or contact metadata.
3.  **Analyze and Extract:** Parse the found content. Look for:
    *   Name-Email-Role patterns (e.g., "Stephen Mitchell - stephen_mitchell@mcp.com - Kubernetes cluster").
    *   Section headers like "Contact", "Support Team", "Responsibilities".
    *   Keywords adjacent to email addresses.
4.  **Verify and Use:** Confirm the extracted contact is the most relevant match for the requested responsibility before using it (e.g., sending an email).

## Key Techniques from Trajectory
*   **Role-Based Keyword Search:** Start with broad role searches ("cluster management", "cluster admin", "infrastructure", "kubernetes").
*   **Document Discovery:** If emails are empty, explore the filesystem (`/workspace/dumps/workspace`) for organizational documents (guidelines, configs).
*   **PDF Table Parsing:** The skill successfully parsed a multi-page PDF (`CS Lab Management Guidelines.pdf`), identified a "Lab Support Team" table on page 3, and extracted the specific contact ("Stephen Mitchell") matching the "Cluster & Computing Resources" responsibility.
*   **Fallback Patterns:** When direct email searches fail, proceed to document search and analysis.

## Output
The primary output is a verified contact (name and email address) for the requested responsibility, ready to be used in subsequent actions (e.g., composing and sending a notification email).
