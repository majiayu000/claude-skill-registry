---
name: howto-docs
description: How-To guide patterns for documentation - task-oriented guides for users with specific goals
autoContext:
  whenUserAsks:
    - how to guide
    - how-to guide
    - howto guide
    - task guide
    - procedural guide
    - step-by-step guide
    - how to documentation
dependencies:
  - docs-style
---

# How-To Documentation Skill

This skill provides patterns for writing effective How-To guides in documentation. How-To guides are task-oriented content for users who have a specific goal in mind.

## Purpose & Audience

**Target readers:**
- Users with a specific goal they want to accomplish
- Assumes some familiarity with the product (not complete beginners)
- Looking for practical, actionable steps
- Want to get things done, not learn concepts

**How-To guides are NOT:**
- Tutorials (which teach through exploration)
- Explanations (which provide understanding)
- Reference docs (which describe the system)

## How-To Guide Template

Use this structure for all how-to guides:

```markdown
---
title: "How to [achieve specific goal]"
description: "Learn how to [goal] using [product/feature]"
---

# How to [Goal]

Brief intro (1-2 sentences): what you'll accomplish and why it's useful.

## Prerequisites

- [What user needs before starting]
- [Required access, tools, or setup]
- [Any prior knowledge assumed]

## Steps

### 1. [Action verb] the [thing]

[Clear instruction with expected outcome]

<Note>
[Optional tip or important context]
</Note>

### 2. [Next action]

[Continue with clear, single-action steps]

```bash
# Example command or code if needed
```

### 3. [Continue numbering]

[Each step should be one discrete action]

## Verify it worked

[How to confirm success - what should user see/experience?]

## Troubleshooting

<AccordionGroup>
  <Accordion title="[Common issue 1]">
    [Solution or workaround]
  </Accordion>
  <Accordion title="[Common issue 2]">
    [Solution or workaround]
  </Accordion>
</AccordionGroup>

## Next steps

- [Related how-to guide 1]
- [Related how-to guide 2]
- [Deeper dive reference doc]
```

## Writing Principles

### Title Conventions

- **Always start with "How to"** - makes the goal immediately clear
- Use active verbs: "How to configure...", "How to deploy...", "How to migrate..."
- Be specific: "How to add SSO authentication" not "How to set up auth"

### Step Structure

1. **One action per step** - if you write "and", consider splitting
2. **Start with action verbs**: Click, Navigate, Enter, Select, Run, Create
3. **Show expected outcomes** after key steps:
   ```markdown
   ### 3. Save the configuration

   Click **Save**. You should see a success message: "Configuration updated."
   ```

### Minimize Context

- Don't explain why things work - just show how to do them
- Link to explanations for users who want deeper understanding
- Keep each step focused on the immediate action

### User Perspective

Write from the user's perspective, not the product's:

| Avoid (product-centric) | Prefer (user-centric) |
|------------------------|----------------------|
| "The API accepts..." | "Send a request to..." |
| "The system will..." | "You'll see..." |
| "This feature allows..." | "You can now..." |

### Prerequisites Section

Be explicit about what's needed:

```markdown
## Prerequisites

- An active account with admin permissions
- API key generated from Settings > API
- Node.js v18 or later installed
- Completed the [initial setup guide](/getting-started)
```

## Components for How-To Guides

### Steps Component

For numbered procedures, use a Steps component:

```markdown
<Steps>
  <Step title="Create a new project">
    Navigate to the dashboard and click **New Project**.
  </Step>
  <Step title="Configure settings">
    Enter your project name and select a region.
  </Step>
  <Step title="Deploy">
    Click **Deploy** to launch your project.
  </Step>
</Steps>
```

### Code Groups for Multiple Options

When showing different approaches:

```markdown
<CodeGroup>
```bash npm
npm install @company/sdk
```

```bash yarn
yarn add @company/sdk
```

```bash pnpm
pnpm add @company/sdk
```
</CodeGroup>
```

### Callouts for Important Information

```markdown
<Warning>
This action cannot be undone. Make sure to backup your data first.
</Warning>

<Note>
This step may take 2-3 minutes to complete.
</Note>

<Tip>
You can also use keyboard shortcut Cmd+K for faster navigation.
</Tip>
```

### Expandable Sections

For optional details that shouldn't interrupt flow:

```markdown
<Expandable title="Advanced options">
  If you need custom configuration, you can also set:
  - `timeout`: Request timeout in milliseconds
  - `retries`: Number of retry attempts
</Expandable>
```

## Example How-To Guide

```markdown
---
title: "How to set up webhook notifications"
description: "Learn how to configure webhooks to receive real-time event notifications"
---

# How to Set Up Webhook Notifications

Configure webhooks to receive instant notifications when events occur in your account. This enables real-time integrations with your existing tools.

## Prerequisites

- Admin access to your account
- A publicly accessible HTTPS endpoint to receive webhooks
- Completed the [authentication setup](/getting-started/auth)

## Steps

<Steps>
  <Step title="Navigate to webhook settings">
    Go to **Settings** > **Integrations** > **Webhooks**.
  </Step>

  <Step title="Add a new webhook endpoint">
    Click **Add Endpoint** and enter your webhook URL:

    ```
    https://your-domain.com/webhooks/receiver
    ```

    <Note>
    Your endpoint must use HTTPS and be publicly accessible.
    </Note>
  </Step>

  <Step title="Select events to subscribe">
    Choose which events should trigger notifications:

    - `user.created` - New user sign up
    - `payment.completed` - Successful payment
    - `subscription.cancelled` - Subscription ended

    Select at least one event to continue.
  </Step>

  <Step title="Save and get your signing secret">
    Click **Create Webhook**. Copy the signing secret shown - you'll need this to verify webhook authenticity.

    <Warning>
    Store the signing secret securely. It won't be shown again.
    </Warning>
  </Step>
</Steps>

## Verify it worked

Send a test event by clicking **Send Test** next to your webhook. You should receive a POST request at your endpoint with this structure:

```json
{
  "event": "test.webhook",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {}
}
```

Check your endpoint logs to confirm receipt.

## Troubleshooting

<AccordionGroup>
  <Accordion title="Webhook not receiving events">
    - Verify your endpoint is publicly accessible
    - Check that your SSL certificate is valid
    - Ensure your server responds with 2xx status within 30 seconds
  </Accordion>

  <Accordion title="Signature verification failing">
    - Confirm you're using the correct signing secret
    - Check that you're reading the raw request body (not parsed JSON)
    - See our [signature verification guide](/reference/webhook-signatures)
  </Accordion>
</AccordionGroup>

## Next steps

- [How to verify webhook signatures](/how-to/verify-webhook-signatures)
- [Webhook event reference](/reference/webhook-events)
- [How to handle webhook retries](/how-to/webhook-retry-handling)
```

## Checklist for How-To Guides

Before publishing, verify:

- [ ] Title starts with "How to" and describes a specific goal
- [ ] Prerequisites section lists all requirements
- [ ] Each step is a single, clear action
- [ ] Action verbs start each step (Click, Enter, Select, Run)
- [ ] Expected outcomes shown after key steps
- [ ] Verification section explains how to confirm success
- [ ] Troubleshooting covers common issues
- [ ] Next steps link to related content
- [ ] No unnecessary explanations - links to concepts instead
- [ ] Written from user perspective, not product perspective

## When to Use How-To vs Other Doc Types

| User's mindset | Doc type | Example |
|---------------|----------|---------|
| "I want to learn" | Tutorial | "Getting started with our API" |
| "I want to do X" | How-To | "How to configure SSO" |
| "I want to understand" | Explanation | "How our caching works" |
| "I need to look up Y" | Reference | "API endpoint reference" |

## Related Skills

- **docs-style**: Core writing conventions and components
- **tutorial-docs**: Tutorial patterns for learning-oriented content
- **reference-docs**: Reference documentation patterns
- **explanation-docs**: Conceptual documentation patterns
