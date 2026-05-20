---
title: "CLI Tools Index"
status: active
---

# CLI Tools Index

This skill provides documentation and usage examples for various CLI helper scripts used within the My Project project.

## `subthread_cycle_helper.py`

**Location**: `my-project-communication/helpers/subthread_cycle_helper.py`

**Purpose**: Bash-callable wrapper for SubThreadManager operations, providing a synchronous interface to manage university contact validation cycles (sub-threads). It is called ONLY by Aura Communicator sub-agents via bash commands.

### Actions:

1.  **`create-cycle`**
    *   **Description**: Starts a new validation cycle by creating a sub-thread.
    *   **Usage**: `python helpers/subthread_cycle_helper.py --action create-cycle --database-id <university_contact_id> --contact-email <email> --contact-name <name> ...`
    *   **Arguments**:
        *   `--database-id` (int, required): The ID of the university contact.
        *   `--contact-email` (str, required): Email of the contact person.
        *   `--contact-name` (str, optional): Name of the contact person (default: "Contact Person").
        *   `--contact-title` (str, optional): Title of the contact person (default: "Staff Member").
        *   `--contact-department` (str, optional): Department of the contact person (default: "Administration").
        *   `--contact-phone` (str, optional): Phone number of the contact person (default: "").
        *   `--university-name` (str, optional): Name of the university (derived from `database_id` if not provided).
        *   `--country` (str, optional): Country of the university (default: "Unknown").
        *   `--cycle-type` (str, required): Type of validation cycle (e.g., "initial_email", "follow_up").
        *   `--message-subject` (str, required): Subject of the initial message.
        *   `--message-content` (str, required): Content of the initial message (plaintext).
        *   `--message-timestamp` (str, optional): ISO formatted timestamp of the message (default: now).
        *   `--template-used` (str, optional): Template used for the initial message (default: "unknown").
        *   `--routing-notes` (str, optional): Notes for routing metadata (default: "Initial validation cycle").

2.  **`append-message`**
    *   **Description**: Adds a message to the currently active validation cycle.
    *   **Usage**: `python helpers/subthread_cycle_helper.py --action append-message --database-id <university_contact_id> --role <role> --subject <subject> --content <content> ...`
    *   **Arguments**:
        *   `--database-id` (int, required): The ID of the university contact.
        *   `--role` (str, required): Role of the message sender (`assistant` or `user`).
        *   `--subject` (str, required): Subject of the message.
        *   `--content` (str, required): Content of the message (plaintext).
        *   `--timestamp` (str, optional): ISO formatted timestamp of the message (default: now).
        *   `--classification` (str, optional): For `user` role, classification of the email (e.g., "POSITIVE", "NEGATIVE", "REDIRECT").
        *   `--from-email` (str, optional): For `user` role, the sender's email.
        *   `--template-used` (str, optional): For `assistant` role, the template used.

3.  **`get-messages`**
    *   **Description**: Retrieves all messages from the active validation cycle for agent LLM analysis.
    *   **Usage**: `python helpers/subthread_cycle_helper.py --action get-messages --database-id <university_contact_id>`
    *   **Arguments**:
        *   `--database-id` (int, required): The ID of the university contact.

4.  **`close-cycle`**
    *   **Description**: Closes the active validation cycle with an agent-generated summary and outcome.
    *   **Usage**: `python helpers/subthread_cycle_helper.py --action close-cycle --database-id <university_contact_id> --outcome <outcome> --summary <summary>`
    *   **Arguments**:
        *   `--database-id` (int, required): The ID of the university contact.
        *   `--outcome` (str, required): The outcome of the cycle (e.g., `contact_verified`, `no_response`).
        *   `--summary` (str, required): LLM-generated summary of the cycle.

5.  **`get-timeline`**
    *   **Description**: Retrieves the full validation timeline for a university, including all past and active cycles.
    *   **Usage**: `python helpers/subthread_cycle_helper.py --action get-timeline --database-id <university_contact_id>`
    *   **Arguments**:
        *   `--database-id` (int, required): The ID of the university contact.

### Output:
All actions output JSON to stdout, which can be consumed by bash scripts or other tools. Errors are printed to stderr with an exit code of 1.
