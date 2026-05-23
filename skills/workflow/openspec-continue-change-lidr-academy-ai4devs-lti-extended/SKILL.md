---
name: openspec-continue-change
description: Continue working on an OpenSpec change by creating the next artifact. Use when the user wants to progress their change, create the next artifact, or continue their workflow.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.0.1"
---

Continue working on a change by creating the next artifact.

**Input**: Optionally specify:
- A Jira ticket ID (e.g., `SCRUM-123`) - will fetch ticket content and find/create associated change
- A change name - will use that change directly
- If omitted, check if it can be inferred from conversation context. If vague or ambiguous you MUST prompt for available changes.

**Steps**

1. **Determine input and get context**

   a. **If input looks like a Jira ticket ID** (matches pattern like `SCRUM-123`, `PROJ-456`, etc.):
      - Use `getAccessibleAtlassianResources` MCP tool to get the cloudId
      - Use `getJiraIssue` MCP tool with:
        - `cloudId`: from step above
        - `issueIdOrKey`: the provided ticket ID
      - Extract ticket content (title, description, acceptance criteria, etc.)
      - **Derive a kebab-case change name from the ticket title**:
        - Convert ticket title to lowercase
        - Replace spaces and special characters with hyphens
        - Remove any leading/trailing hyphens
        - Example: "Update Position API" → `update-position-api`, "Add User Auth" → `add-user-auth`
        - If ticket title is unclear or too long, use a shortened meaningful version
      - Try to find existing change with the derived kebab-case name
      - If no change exists, ask user if they want to create one or use an existing change
      - Use ticket content as context for creating the next artifact

   b. **If input is a change name or no input provided**:
      - Proceed with existing logic (prompt for selection if needed)

   Run `openspec list --json` to get available changes sorted by most recently modified. Then use the **AskUserQuestion tool** to let the user select which change to work on.

   Present the top 3-4 most recently modified changes as options, showing:
   - Change name
   - Schema (from `schema` field if present, otherwise "spec-driven")
   - Status (e.g., "0/5 tasks", "complete", "no tasks")
   - How recently it was modified (from `lastModified` field)

   Mark the most recently modified change as "(Recommended)" since it's likely what the user wants to continue.

   **IMPORTANT**: Do NOT guess or auto-select a change. Always let the user choose.

2. **Check current status**
   ```bash
   openspec status --change "<name>" --json
   ```
   Parse the JSON to understand current state. The response includes:
   - `schemaName`: The workflow schema being used (e.g., "spec-driven")
   - `artifacts`: Array of artifacts with their status ("done", "ready", "blocked")
   - `isComplete`: Boolean indicating if all artifacts are complete

3. **Act based on status**:

   ---

   **If all artifacts are complete (`isComplete: true`)**:
   - Congratulate the user
   - Show final status including the schema used
   - Suggest: "All artifacts created! You can now implement this change or archive it."
   - STOP

   ---

   **If artifacts are ready to create** (status shows artifacts with `status: "ready"`):
   - Pick the FIRST artifact with `status: "ready"` from the status output
   - Get its instructions:
     ```bash
     openspec instructions <artifact-id> --change "<name>" --json
     ```
   - Parse the JSON. The key fields are:
     - `context`: Project background (constraints for you - do NOT include in output)
     - `rules`: Artifact-specific rules (constraints for you - do NOT include in output)
     - `template`: The structure to use for your output file
     - `instruction`: Schema-specific guidance
     - `outputPath`: Where to write the artifact
     - `dependencies`: Completed artifacts to read for context
   - **Create the artifact file**:
     - **CRITICAL for tasks artifact**: If creating `tasks.md`:
       - Read `openspec/config.yaml` to get backend-specific rules (mandatory steps, branch naming, etc.)
       - Read `.claude/rules/openspec-tasks-mandatory-steps.mdc` to understand mandatory testing requirements and agent execution responsibilities
       - Task structure requirements
       - All mandatory steps that MUST be included (e.g., Step 0: Create Feature Branch)
     - **If Jira ticket was provided**: Use ticket content to inform artifact creation
     - Read any completed dependency files for context
     - Use `template` as the structure - fill in its sections
     - Apply `context` and `rules` as constraints when writing - but do NOT copy them into the file
     - **For tasks artifact**: Ensure all mandatory steps from `config.yaml` and the rule file are included:
       - Step 0: Create Feature Branch (MUST be first step for backend changes)
       - Review and Update Existing Unit Tests (MANDATORY)
       - Run Unit Tests and Verify Database State (MANDATORY)
       - Manual Endpoint Testing with curl (MANDATORY - AGENT MUST EXECUTE)
       - E2E Testing with Playwright MCP (MANDATORY if applicable - AGENT MUST EXECUTE)
       - Update Technical Documentation (MANDATORY)
     - **For manual testing tasks**: Include sub-tasks that make it clear the agent must execute tests (e.g., "Test GET endpoints with curl", "Restore database state", etc.)
     - Write to the output path specified in instructions
   - Show what was created and what's now unlocked
   - STOP after creating ONE artifact

   ---

   **If no artifacts are ready (all blocked)**:
   - This shouldn't happen with a valid schema
   - Show status and suggest checking for issues

4. **After creating an artifact, show progress**
   ```bash
   openspec status --change "<name>"
   ```

**Output**

After each invocation, show:
- Which artifact was created
- Schema workflow being used
- Current progress (N/M complete)
- What artifacts are now unlocked
- Prompt: "Want to continue? Just ask me to continue or tell me what to do next."

**Artifact Creation Guidelines**

The artifact types and their purpose depend on the schema. Use the `instruction` field from the instructions output to understand what to create.

Common artifact patterns:

**spec-driven schema** (proposal → specs → design → tasks):
- **proposal.md**: Ask user about the change if not clear. Fill in Why, What Changes, Capabilities, Impact.
  - The Capabilities section is critical - each capability listed will need a spec file.
- **specs/*.md**: Create one spec per capability listed in the proposal.
- **design.md**: Document technical decisions, architecture, and implementation approach.
- **tasks.md**: Break down implementation into checkboxed tasks.

For other schemas, follow the `instruction` field from the CLI output.

**Guardrails**
- Create ONE artifact per invocation
- Always read dependency artifacts before creating a new one
- Never skip artifacts or create out of order
- **For tasks.md**: Read `.claude/rules/openspec-tasks-mandatory-steps.mdc` to ensure all mandatory steps are included with proper agent execution requirements
- If context is unclear, ask the user before creating
- Verify the artifact file exists after writing before marking progress
- Use the schema's artifact sequence, don't assume specific artifact names
- **IMPORTANT**: `context` and `rules` are constraints for YOU, not content for the file
  - Do NOT copy `<context>`, `<rules>`, `<project_context>` blocks into the artifact
  - These guide what you write, but should never appear in the output
