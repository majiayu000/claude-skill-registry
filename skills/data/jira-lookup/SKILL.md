---
name: jira-lookup
description: Look up a Jira issue by key. Shows summary, status, assignee, priority, and link.
user-invocable: true
arguments: "<JIRA-KEY> (e.g. PROJ-123)"
---

# Jira Issue Lookup

Look up a Jira issue using the REST API and display its details.

## Steps

1. Read `config.yaml` to get `features.jira.baseUrl`. If not set, ask the user.
2. Use `$JIRA_EMAIL` and `$JIRA_TOKEN` environment variables for authentication.
3. Fetch the issue via:
   ```bash
   curl -s -u "$JIRA_EMAIL:$JIRA_TOKEN" \
     -H "Accept: application/json" \
     "${BASE_URL}/rest/api/3/issue/${JIRA_KEY}?fields=summary,status,assignee,priority"
   ```
4. Display the results:
   - **Key:** PROJ-123
   - **Summary:** Issue title
   - **Status:** In Progress
   - **Assignee:** Name (or Unassigned)
   - **Priority:** Medium
   - **Link:** https://company.atlassian.net/browse/PROJ-123

## Error Handling

- If the issue is not found (404), report "Issue not found".
- If authentication fails (401/403), report "Authentication failed — check JIRA_EMAIL and JIRA_TOKEN env vars".
- If baseUrl is not configured, report "Jira base URL not configured — set features.jira.baseUrl in config.yaml".
