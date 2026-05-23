---
id: slack-channel-engagement
name: Slack Channel Engagement
description: Read history, post messages
role: support
requiredTools:
  - type: mcpService
    serviceType: slack
---

## Slack Channel Engagement

Use this skill for support-style channel engagement: customer-facing or support channels where you read history and post replies or updates. (For internal team/project channels and announcements, prefer the Slack Internal Comms skill.)

When engaging in Slack channels:

- List channels to find the right channel by name or topic.
- Use get channel history to read recent messages before replying or summarizing.
- When posting, use the post message tool with clear, concise text; mention or thread when appropriate.
- Summarize channel activity (e.g. last N messages, key topics) when the user asks what’s happening.
- Do not post sensitive or confidential information; keep tone professional.

## Step-by-step instructions

1. For “find channel X”: list channels and pick by name or topic; note channel ID for history or post.
2. For “what’s happening” or context: get channel history (last N messages); summarize key topics and decisions.
3. For posting: draft clear, concise text; use post message with the correct channel; use thread or @mention only when the user asks or it’s clearly appropriate.
4. Do not include secrets or confidential data in any message.

## Examples of inputs and outputs

- **Input**: “What’s the latest in #support?”  
  **Output**: Short summary of the last few messages (who said what, main topic); from get channel history for #support.

- **Input**: “Post in #general: Team sync is at 3pm today.”  
  **Output**: Confirm channel and text; call post message; then “Posted to #general.”

## Common edge cases

- **Channel not found**: Say “Channel [name] not found” and suggest listing channels or checking the name.
- **No history / permission**: Report “Could not read history” and suggest permissions or a different channel.
- **User says “reply in thread”**: Use the thread parameter when posting so the message is in the correct thread.
- **API/oauth error**: Report Slack error and suggest reconnecting or retrying.

## Tool usage for specific purposes

- **List channels**: Use to find the right channel by name or topic before reading history or posting (support/customer channels).
- **Get channel history**: Use to read recent messages for “what’s happening” or to gather context before replying.
- **Post message**: Use to send a new message; specify channel; use thread or mentions only when appropriate.
