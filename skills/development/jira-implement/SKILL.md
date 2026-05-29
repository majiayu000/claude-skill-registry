---
name: jira-implement
description: This skill should be used when implementing the requirements in a JIRA ticket.
---

Use either the Atlassian MCP or CLI to examine the contents of the JIRA ticket: $ARGUMENTS

If neither is available, stop and report that you cannot access the ticket.

Read all the details in the ticket, including any URLs and attachments.

Make a plan to fulfill the requirements of the ticket.

Important: If this involves UI changes, use Playwright MCP browser tools to access the app and get a better understanding of what needs to be done. Create a verification task using browser tools to confirm the implementation.

Important: If this involves API or backend changes, use curl or test commands to understand current behavior. Create a verification task to confirm the implementation.

If you don't know how to access the app or service, clarify when making the plan.
