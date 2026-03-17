---
id: slack-internal-comms
name: Slack Internal Comms
description: Team channels, announcements
role: engineering
requiredTools:
  - type: mcpService
    serviceType: slack
---

## Slack Internal Comms

Use this skill for internal team and project channels: announcements, team updates, and summarizing recent discussions. (For support-style or customer-facing channel engagement, prefer the Slack Channel Engagement skill.)

When handling internal Slack communications:

- List channels to locate team or project channels.
- Read channel history to gather context before posting or summarizing.
- When posting announcements, use clear subject and body; target the right channel.
- Summarize recent discussions or decisions when the user asks for team updates.
- Keep messages concise and actionable for internal audiences.

## Step-by-step instructions

1. For “team/project channel”: list channels and identify the right one by name or topic.
2. For “what’s the update” or “recent decisions”: get channel history and summarize key discussions and outcomes.
3. For announcements: draft clear subject and body; confirm target channel; use post message; keep tone concise and actionable.
4. Do not post confidential or sensitive information.

## Examples of inputs and outputs

- **Input**: “What did the team decide in #platform this week?”  
  **Output**: Short summary of recent messages and decisions from get channel history for #platform.

- **Input**: “Announce in #engineering: Deploy window is Saturday 2–4am.”  
  **Output**: Confirm channel and text; post; then “Announcement posted to #engineering.”

## Common edge cases

- **Channel not found**: Say “Channel [name] not found” and suggest listing channels.
- **No history / permission**: Report that history couldn’t be read and suggest permissions.
- **Vague “team”**: List a few likely channels (e.g. by name) and ask which one, or summarize the one that matches context.
- **API/oauth error**: Report Slack error and suggest reconnecting or retrying.

## Tool usage for specific purposes

- **List channels**: Use to find team or project channels (internal) before reading or posting.
- **Get channel history**: Use to gather context and summarize recent discussions or decisions.
- **Post message**: Use for announcements to internal channels; always target the correct channel and keep content concise and actionable.
