---
name: jira-fix
description: This skill should be used when fixing a bug ticket in JIRA
---

1. Use the JIRA/Atlassian MCP or CLI to fully read this issue, including comments and attachments: $ARGUMENTS
2. Extract sign-in information if available from the ticket (e.g., test credentials, OTP codes)
3. Use the project's verification method to attempt to reproduce the bug:
   - For UI projects: Use Playwright MCP browser tools to record a replication
   - For API projects: Use curl or test commands to reproduce the error
   - For library projects: Write a minimal reproduction test
4. If you cannot reproduce the issue, upload the evidence to the JIRA ticket explaining that you can't replicate it and skip the remaining steps
5. If there have already been attempts to fix this bug, understand the previous attempts by looking for pull requests and git commits related to it
6. Fix the bug
7. Verify the fix using the same verification method used in step 3
8. Upload the evidence to the JIRA ticket and explain the fix
