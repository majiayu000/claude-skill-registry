---
name: ticket-manager
description: Expertise in managing Linear tickets locally using Markdown files. Use when you need to create, update, search, or break down features into atomic implementation tickets.
---

# Linear - Ticket Management (Local Mode)

You are tasked with managing "Linear tickets" locally using markdown files
stored in the user's global configuration directory and the `WriteTodosTool`.
This replaces the cloud-based Linear MCP workflow.

## Core Concepts

1.  **Tickets as Files**: Tickets are stored as markdown filesin the **active session directory**.
    - **Locate Session**: Execute `~/.gemini/extensions/pickle-rick/scripts/get_session.sh` to find the session root.
    - **Parent Ticket**: Stored in the session root: `[Session_Root]/linear_ticket_parent.md`.
    - **Child Tickets**: Stored in dedicated subdirectories: `[Session_Root]/[child_hash]/linear_ticket_[child_hash].md`.
    - **Format**: Frontmatter for metadata, Markdown body for content.

2.  **Session Planning**: Use `WriteTodosTool` to track immediate subtasks when
    working on a specific ticket in the current session.

## Initial Setup & Interaction

First, execute `run_shell_command("~/.gemini/extensions/pickle-rick/scripts/get_session.sh")` to determine the working directory.

### For general requests:

```
I can help you with Linear tickets (Local Mode). What would you like to do?
1. Create a new ticket from a thoughts document
2. Add a comment to a ticket (I'll use our conversation context)
3. Search for tickets
4. Update ticket status or details
5. Break down a PRD into a ticket hierarchy
```

### For specific create requests:

```
I'll help you create a local Linear ticket from your thoughts document. Please provide:
1. The path to the thoughts document (or topic to search for)
2. Any specific focus or angle for the ticket (optional)
```

Then wait for the user's input.

## Important Conventions

### Path Mapping for Thoughts Documents

When referencing thoughts documents, always provide the relative local path in
the `links` frontmatter section:

- Use relative paths from the workspace root: `~/.gemini/extensions/pickle-rick/thoughts/shared/...`,
  `~/.gemini/extensions/pickle-rick/thoughts/galzahavi/...`, `~/.gemini/extensions/pickle-rick/thoughts/global/...`.
- Do NOT convert these to GitHub URLs. Keep them as local file paths.

### Default Values

- **Status**: Always create new tickets in "Triage" status.
  - **Research in Progress** → Active research/investigation underway.
  - **Research in Review** → Research findings under review.
  - **Plan in Progress** → Actively writing the implementation plan.
  - **Plan in Review** → Plan is written and under discussion.
  - **In Dev** → Active development (coding).
  - **Code Review** → Code is being reviewed.
  - **Done** → Completed.
  - **Canceled** → Abandoned or Duplicate.
- **Project**: Default to "project" in the frontmatter unless told otherwise.
- **Priority**: Default to Medium (3) for most tasks, use best judgment or ask
  user.
  - Urgent (1): Critical blockers, security issues
  - High (2): Important features with deadlines, major bugs
  - Medium (3): Standard implementation tasks (default)
  - Low (4): Nice-to-haves, minor improvements
- **Links**: Use the `links` frontmatter list to attach URLs.

## Ticket Structure

Each ticket file must follow this structure:

```markdown
---
id: [8-char-hex-hash]
title: [Ticket Title]
status: [Status]
priority: [Urgent|High|Medium|Low]
size: [XS|Small|Medium|Large|XL] (optional)
project: project
created: [YYYY-MM-DD]
updated: [YYYY-MM-DD]
links:
  - url: [URL]
    title: [Title]
labels: [core, cli, meta, bug, etc.]
assignee: [User Name]
---

# Description

## Problem to solve
[Clear statement of the user problem or need]

## Solution
[Proposed approach or solution outline]

# Discussion/Comments

- [YYYY-MM-DD] User: Comment text...
```

## Action-Specific Instructions

### 1. Creating Tickets from Thoughts

#### Steps to follow after receiving the request:

1. **Locate and read the thoughts document:**
   - If given a path, read the document directly
   - If given a topic/keyword, execute `run_shell_command("grep -r [keyword] ~/.gemini/extensions/pickle-rick/thoughts/")` to find relevant documents.
   - If multiple matches found, show list and ask user to select
   - Create a `WriteTodosTool` list to track: Read document → Analyze content →
     Draft ticket → Get user input → Create ticket

2. **Analyze the document content:**
   - Identify the core problem or feature being discussed
   - Extract key implementation details or technical decisions
   - Note any specific code files or areas mentioned
   - Look for action items or next steps
   - Identify what stage the idea is at (early ideation vs ready to implement)
   - Take time to ultrathink about distilling the essence of this document into
     a clear problem statement and solution approach

3. **Check for related context (if mentioned in doc):**
   - If the document references specific code files, read relevant sections
   - If it mentions other thoughts documents, quickly check them
   - Look for any existing Linear tickets mentioned (search in `[Session_Root]`)

4. **Draft the ticket summary:** Present a draft to the user:

   ```
   ## Draft Linear Ticket

   **Title**: [Clear, action-oriented title]

   **Description**:
   [2-3 sentence summary of the problem/goal]

   ## Key Details
   - [Bullet points of important details from thoughts]
   - [Technical decisions or constraints]
   - [Any specific requirements]

   ## Implementation Notes (if applicable)
   [Any specific technical approach or steps outlined]

   ## References
   - Source: `~/.gemini/extensions/pickle-rick/thoughts/[path/to/document.md]` ([Local File])
   - Related code: [any file:line references]
   - Parent ticket: [if applicable]

   ---
   Based on the document, this seems to be at the stage of: [ideation/planning/ready to implement]
   ```

5. **Interactive refinement:** Ask the user:
   - Does this summary capture the ticket accurately?
   - What priority? (Default: Medium)
   - Do you want to assign it to yourself?
   - Any additional context to add?
   - Should we include more/less implementation detail?

   **CRITICAL RULE**: If the user asks for a ticket and only gives implementation details,
   you MUST ask: *"To write a good ticket, please explain the problem you're trying to solve from a user perspective"*.

   Note: Ticket will be created in "Triage" status by default.

6. **Create the Linear ticket:**
   - Generate ID: `openssl rand -hex 4` (or internal random string).
   - **Create Directory**: `mkdir -p [Session_Root]/[ID]`
   - Write file to `[Session_Root]/[ID]/linear_ticket_[ID].md` with Frontmatter
     and Markdown content.
   - **Important**: Set both `created` and `updated` to today's date.

   **Frontmatter Example:**

   ```yaml
   ---
   id: a1b2c3d4
   title: [refined title]
   status: Triage
   priority: [selected priority]
   project: project
   created: [YYYY-MM-DD]
   updated: [YYYY-MM-DD]
   links:
     - url: [Local path to thoughts doc]
       title: [Document Title]
   labels: [derived labels]
   assignee: [User Name]
   ---
   ```

7. **Post-creation actions:**
   - Show the created ticket path and ID.
   - Ask if user wants to:
     - Add a comment with additional implementation details
     - Create sub-tasks for specific action items
     - Update the original thoughts document with the ticket reference
   - If yes to updating thoughts doc:
     ```
     Add at the top of the document:
     ---
     linear_ticket: [Ticket ID]
     created: [date]
     ---
     ```

### 5. PRD Breakdown & Hierarchy

When tasked with breaking down a PRD or large task:

1.  **Identify Session Root**: Execute `run_shell_command("~/.gemini/extensions/pickle-rick/scripts/get_session.sh")`.

2.  **Create Parent Ticket**:
    -   Create the "Parent" ticket in the session root: `[Session_Root]/linear_ticket_parent.md`.
    -   Status: "Backlog" or "Research Needed".
    -   Title: "[Epic] [Feature Name]".
    -   Links: Add link to PRD.

3.  **Create Child Tickets**:
    -   Break the PRD into atomic implementation tasks (e.g., "Research", "Backend API", "Frontend UI", "Integration").
    -   For each child:
        - Generate Hash: `[child_hash]`
        - Create Directory: `[Session_Root]/[child_hash]/`
        - Create Ticket: `[Session_Root]/[child_hash]/linear_ticket_[child_hash].md`
    -   **Linkage**: In the `links` section of each child ticket, add:
        ```yaml
        links:
          - url: ../linear_ticket_parent.md
            title: Parent Ticket
        ```

4.  **Confirm**: List the created tickets to the user.

### 3. Searching for Tickets

When user wants to find tickets:

1. **Gather search criteria:**
   - Query text
   - Status filters (use the Categories: Inbox, Backlog, Active, Completed)
   - Priority
   - Date ranges (created, updated)

2. **Execute search:**
   - **List all**: `glob` pattern `[Session_Root]/**/linear_ticket_*.md` (recursive).
   - **Filter**: Iterate through files, `read_file` (with limit/offset to read
     frontmatter), and filter based on criteria.
   - **Content Search**: Use `search_file_content` targeting the
     `[Session_Root]` directory if searching for text in description.

3. **Present results:**
   - Show ID, Title, Status, Priority, Assignee.
   - Group by status category (e.g., Active vs Backlog) if helpful.

### 4. Updating Ticket Status

When moving tickets through the workflow:

1. **Get current status:**
   - Read the ticket file to see current `status` in frontmatter.

2. **Suggest next status:**
   - **Inbox**: Triage → Spec Needed
   - **Backlog**: Spec Needed → Research Needed → Ready for Plan
   - **Active**: Plan in Progress → Ready for Dev → In Dev → Code Review
   - **Done**: Done

3. **Update with context:**
   - Read file `[Session_Root]/.../linear_ticket_[ID].md`.
   - Update `status: [New Status]` in frontmatter.
   - **Update `updated: [YYYY-MM-DD]` in frontmatter.**
   - Optionally append a comment explaining the change.
   - Write file back.

## Important Notes

- Keep tickets concise but complete - aim for scannable content.
- All tickets should include a clear "problem to solve".
- Focus on the "what" and "why", include "how" only if well-defined.
- Always preserve links to source material using the `links` frontmatter.
- Don't create tickets from early-stage brainstorming unless requested.
- Use proper Markdown formatting (descriptions support full markdown including code blocks).
- Include code references as: `path/to/file.ext:linenum`.
- **Remember**: Ask for clarification rather than guessing project/status.

## Comment Quality Guidelines

When creating comments, focus on extracting the **most valuable information**:

- **Key insights over summaries**: Not just what was done, but what matters about it. What's the "aha" moment?
- **Decisions and tradeoffs**: What approach was chosen and what it enables/prevents.
- **Blockers resolved**: What was preventing progress and how it was addressed.
- **State changes**: What's different now and what it means for next steps.
- **Surprises or discoveries**: Unexpected findings that affect the work.

**Avoid:**

- Mechanical lists of changes without context.
- Restating what's obvious from code diffs.
- Generic summaries that don't add value.

Remember: The goal is to help a future reader (including yourself) quickly
understand what matters about this update.

## Next Step
**Start the Loop**:
1. List all created child tickets in `[Session_Root]`.
2. Select the highest priority ticket that is **NOT** 'Done'.
3. Call `activate_skill("code-researcher")` for that ticket.
