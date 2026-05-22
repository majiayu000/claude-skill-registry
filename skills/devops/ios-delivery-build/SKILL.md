---
name: ios-delivery-build
description: Manage iOS delivery builds to QC testing with GitLab pipeline creation and issue management. Supports develop, delivery, bugfix, and redelivery modes. Use when "create delivery", "delivery build", "build for qc", "send to testing", or "deliver build".
allowed-tools: Bash, AskUserQuestion, Read
---

You are managing iOS delivery builds to QC testing with GitLab integration.

## Step 1: Get Current Branch

Execute immediately:
```bash
git branch --show-current
```

Store result as `{current_branch}`.

## Step 2: Mode Selection

Ask user to select delivery mode:
- **develop**: Create develop task and move original to testing
- **delivery**: Close issues after delivery
- **bugfix**: Move issues to testing status
- **redelivery**: Create pipeline only, no issue management

Use AskUserQuestion with these exact options:
- "develop - Create develop task and move original to testing"
- "delivery - Close issues after delivery"
- "bugfix - Move issues to testing status"
- "redelivery - Create pipeline only"

If invalid mode after 3 attempts, abort with error.

## Step 3: Collect Form Inputs

Present form template from `templates.md` based on selected mode.

**Required for ALL modes:**
- branch (pre-filled with {current_branch})
- scheme (default: "Payoo Merchant Sandbox")
- recipient (from predefined list in templates.md)
- description
- reply_on_thread (default: "none")
- project (default: "rnd/ios/payoo-ios-app-merchant")

**Conditional fields:**
- issue_numbers: Required for develop/delivery/bugfix, NOT for redelivery
- estimates: Required for develop/delivery, NOT for bugfix/redelivery

Parse user input and extract all field values.

## Step 4: Validate Inputs

Before proceeding, validate:
- branch exists (check with `git branch --list`)
- issue_numbers are numeric (skip for redelivery)
- recipient matches format "Name|ID" from predefined list
- estimates count matches issue_numbers count (for delivery/develop only)
- reply_on_thread is "none" or valid URL
- scheme and project are non-empty

If validation fails, show specific errors and request corrections.

## Step 5: Create GitLab Pipeline

Use MCP tool `mobile-mcp-server/gitlab-create-pipeline-for-branch`:
```
scheme: {scheme}
branchName: {branch}
recipient: {recipient}
replyOnThread: {reply_on_thread}
description: {description}
project: {project}
```

If pipeline creation fails, abort workflow with error.

## Step 6: Plan Issue Management Actions

Based on mode, plan actions (see `examples.md` for detailed workflows):

**bugfix mode:**
- For each issue in issue_numbers, plan to add label "status::totesting"

**delivery mode:**
- For each issue, plan to close with corresponding estimate

**develop mode:**
- Get first issue details
- Create develop task with "[Develop]" suffix
- Move original issue to testing
- Close develop task with estimate

**redelivery mode:**
- No issue actions needed, skip to completion

## Step 7: Confirmation and Execution

**For redelivery mode:**
- Display: "Pipeline created successfully. No issue management for redelivery."
- End workflow

**For other modes:**
- Display all planned actions in readable format
- Ask: "Do you want to proceed? (yes/no)"
- If "yes": Execute all actions sequentially, show progress
- If "no": Abort with message about pipeline being created but issues not managed

## Error Handling

- Invalid issue IID: Skip and log warning, continue with others
- API timeout: Retry once after 5 seconds, then fail
- Authentication error: Abort immediately
- Invalid branch: Abort before creating pipeline

Always provide:
- What failed
- Why it failed (if known)
- What completed successfully
- Suggested next steps

## Output Format

Show clear summary:
```
✅ Pipeline Created
Branch: {branch}
Scheme: {scheme}
Recipient: {recipient}
Description: {description}

📋 Issue Management:
[List of planned/executed actions]

✅ Workflow Complete
```
