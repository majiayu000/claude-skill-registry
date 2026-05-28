---
name: 'packmind-create-command'
description: "Guide for creating reusable commands via the Packmind CLI. This skill should be used when users want to create a new command that captures multi-step workflows, recipes, or task automation for distribution to CoPilot."
license: 'Complete terms in LICENSE.txt'
---

# Command Creator

This skill provides a complete walkthrough for creating reusable commands via the Packmind CLI.

## About Commands

Commands are structured, multi-step workflows that capture repeatable tasks, recipes, and automation patterns. They help teams standardize common development workflows and enable CoPilot to execute complex tasks consistently.

### What Commands Provide

1. **Multi-step workflows** - Structured sequences of actions to accomplish a task
2. **Context validation** - Checkpoints to ensure requirements are met before execution
3. **When-to-use guidance** - Clear scenarios describing when the command is applicable
4. **Code snippets** - Optional examples demonstrating each step's implementation

### Command Playbook Structure

Every command playbook is a JSON file with this structure:

```json
{
  "name": "Command Name",
  "summary": "What the command does, why it's useful, and when it's relevant",
  "whenToUse": [
    "Scenario 1 when this command applies",
    "Scenario 2 when this command applies"
  ],
  "contextValidationCheckpoints": [
    "Question 1 to validate before proceeding?",
    "Question 2 to ensure context is clear?"
  ],
  "steps": [
    {
      "name": "Step Name",
      "description": "What this step does and how to implement it",
      "codeSnippet": "// Optional code example"
    }
  ]
}
```

### Validation Requirements

The CLI validates playbooks automatically. Requirements:

- **name**: Non-empty string
- **summary**: Non-empty string describing intent, value, and relevance
- **whenToUse**: Array with at least one scenario (non-empty strings)
- **contextValidationCheckpoints**: Array with at least one checkpoint (non-empty strings)
- **steps**: Array with at least one step
- **steps[].name**: Non-empty string (step title)
- **steps[].description**: Non-empty string (implementation details)
- **steps[].codeSnippet** (optional): Code example for the step

## Prerequisites

### Packmind CLI

Check if packmind-cli is installed:

```bash
packmind-cli --version
```

If not available, install it:

```bash
npm install -g @packmind/cli
```

Then login to Packmind:

```bash
packmind-cli login
```

## Command Creation Process

### Step 1: Understanding the Command's Purpose

Skip this step only when the command's workflow and steps are already clearly defined.

To create an effective command, clearly understand:

1. **What workflow does this command automate?**
   - Example: "Setting up a new API endpoint with tests"
   - Example: "Creating a new React component with proper structure"

2. **When should this command be triggered?**
   - Specific scenarios (e.g., "When adding a new feature")
   - Specific contexts (e.g., "After creating a domain entity")

Example clarifying questions:

- "What multi-step workflow do you want to automate?"
- "What scenarios should trigger this command?"
- "What context needs to be validated before running this workflow?"

### Step 2: Designing the Workflow

Transform the understanding from Step 1 into concrete steps.

#### Step Writing Guidelines

1. **Clear name** - Use a concise title (e.g., "Setup Dependencies", "Create Test File")
2. **Actionable description** - Explain what to do and how to implement it
3. **One concept per step** - Focus on a single action
4. **Optional code snippet** - Include when it clarifies the implementation

**Good descriptions:**
- "Create a new file at \`src/components/{ComponentName}.tsx\` with the basic component structure including props interface and default export"

**Bad descriptions:**
- "Create file" (too vague)

#### Context Validation Checkpoints

Questions that verify requirements before execution:

**Good checkpoints:**
- "Is the component name and location specified?"
- "Are the API endpoint requirements (method, path, payload) defined?"

**Bad checkpoints:**
- "Ready to start?" (doesn't validate anything)

#### When-To-Use Scenarios

Define specific, actionable scenarios:

**Good scenarios:**
- "When adding a new REST endpoint to the API"
- "After creating a new domain entity that needs persistence"

**Bad scenarios:**
- "When coding" (too broad)

### Step 3: Creating the Playbook File

Create a JSON file named `<command-name>.command.playbook.json` with the structure documented above.

Example minimal playbook:

```json
{
  "name": "Create API Endpoint",
  "summary": "Set up a new REST API endpoint with controller, service, and tests.",
  "whenToUse": [
    "When adding a new REST endpoint to the API"
  ],
  "contextValidationCheckpoints": [
    "Is the HTTP method and path defined?"
  ],
  "steps": [
    {
      "name": "Create Controller",
      "description": "Create the controller file in \`infra/http/controllers/\` with the endpoint handler."
    }
  ]
}
```

### Step 4: Review Before Submission

**Before running the CLI command**, you MUST get explicit user approval:

1. Show the user the complete playbook content in a formatted preview:
   - Name
   - Summary
   - When to use scenarios
   - Context validation checkpoints
   - Each step with name, description, and code snippet (if any)

2. **Provide the file path** to the playbook JSON file so users can open and edit it directly if needed.

3. Ask: **"Here is the command that will be created on Packmind. The playbook file is at \`<path>\` if you want to review or edit it. Do you approve?"**

4. **Wait for explicit user confirmation** before proceeding to Step 5.

5. If the user requests changes, go back to earlier steps to make adjustments.

### Step 5: Creating the Command via CLI

Run the packmind-cli command to create the command:

```bash
packmind-cli commands create <path-to-playbook.json>
```

Example:
```bash
packmind-cli commands create ./create-api-endpoint.command.playbook.json
```

Expected output on success:
```
packmind-cli Command "Your Command Name" created successfully (ID: <uuid>)
View it in the webapp: <url>
```

#### Troubleshooting

**"Not logged in" error:**
```bash
packmind-cli login
```

**"Failed to resolve global space" error:**
- Verify your API key is valid
- Check network connectivity to Packmind server

**JSON validation errors:**
- Ensure all required fields are present
- Verify JSON syntax is valid (use a JSON validator)
- Check that all arrays have at least one entry

## Complete Example

Here's a complete example creating a command for setting up a new API endpoint:

**File: create-api-endpoint.command.playbook.json**
```json
{
  "name": "Create API Endpoint",
  "summary": "Set up a new REST API endpoint with controller, service, and tests following the hexagonal architecture pattern.",
  "whenToUse": [
    "When adding a new REST endpoint to the API",
    "When implementing a new backend feature that exposes HTTP endpoints"
  ],
  "contextValidationCheckpoints": [
    "Is the HTTP method and path defined (e.g., POST /users)?",
    "Is the request/response payload structure specified?",
    "Is the associated use case or business logic identified?"
  ],
  "steps": [
    {
      "name": "Create Controller",
      "description": "Create the controller file in the \`infra/http/controllers/\` directory with the endpoint handler and input validation.",
      "codeSnippet": "@Controller('users')\nexport class UsersController {\n  @Post()\n  async create(@Body() dto: CreateUserDTO) {\n    return this.useCase.execute(dto);\n  }\n}"
    },
    {
      "name": "Create Use Case",
      "description": "Create the use case in the \`application/useCases/\` directory implementing the business logic."
    },
    {
      "name": "Create Tests",
      "description": "Create unit tests for the controller and use case in their respective \`.spec.ts\` files following the Arrange-Act-Assert pattern."
    },
    {
      "name": "Register in Module",
      "description": "Add the controller and use case to the appropriate NestJS module's \`controllers\` and \`providers\` arrays."
    }
  ]
}
```

**Creating the command:**
```bash
packmind-cli commands create create-api-endpoint.command.playbook.json
```

## Quick Reference

| Field                         | Required | Description                                    |
| ----------------------------- | -------- | ---------------------------------------------- |
| name                          | Yes      | Command name                                   |
| summary                       | Yes      | What, why, and when (one sentence)             |
| whenToUse                     | Yes      | At least one scenario                          |
| contextValidationCheckpoints  | Yes      | At least one checkpoint question               |
| steps                         | Yes      | At least one step                              |
| steps[].name                  | Yes      | Step title                                     |
| steps[].description           | Yes      | Implementation details                         |
| steps[].codeSnippet           | No       | Optional code example                          |
