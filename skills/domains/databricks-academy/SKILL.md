---
name: databricks-academy
description: Use this skill when users ask questions about Databricks courses, tutorials, documentation, or learning materials from Databricks Academy (customer-academy.databricks.com). This skill handles login-required access to search and retrieve course content, learning paths, hands-on labs, and technical documentation.
---

# Databricks Academy

## Overview

This skill enables access to login-protected content on Databricks Academy (https://customer-academy.databricks.com/). It handles authentication, searches for courses and tutorials, and retrieves learning materials to answer user questions about Databricks topics.

## When to Use This Skill

Use this skill when:
- Users ask about Databricks courses, learning paths, or certifications
- Users need to find tutorials or documentation for Databricks features (Delta Lake, Unity Catalog, etc.)
- Users want to explore hands-on labs or practical exercises
- Users inquire about specific topics like "SQL Analytics", "MLflow", "Data Pipelines"
- Any query that requires accessing content from customer-academy.databricks.com

## Workflow

### Step 1: Collect Login Credentials

Before accessing Databricks Academy, collect authentication credentials from the user:

1. Use `AskUserQuestion` to request email and password
2. Inform the user: "These credentials are used only for this session and will not be stored"
3. Handle sensitive information securely - never log or store passwords

**Security Note**: Credentials are kept in memory only for the duration of the browser session and discarded when the session ends.

### Step 2: Authenticate to Databricks Academy

Perform browser automation to log in:

```
1. Navigate to https://customer-academy.databricks.com/ using browser_navigate
2. Capture current page state with browser_snapshot
3. Locate login form elements (email and password fields)
4. Enter email using browser_type with the email field reference
5. Enter password using browser_type with the password field reference
6. Submit login form using browser_click on the login button
7. Wait for navigation completion using browser_wait_for
8. Verify successful login with browser_snapshot
```

**Error Handling**: If login fails:
- Inform the user: "Login failed. Please verify your credentials and try again."
- Check if the account requires additional verification (2FA, SSO redirect)
- Suggest the user verify access by logging in directly to the website first

### Step 3: Search for Content

After successful authentication, search for the requested content:

1. Use browser_snapshot to identify the search interface
2. Locate the search input field
3. Enter the user's query using browser_type
4. Execute search using browser_click
5. Wait for results to load using browser_wait_for
6. Capture search results with browser_snapshot

**Search Optimization**:
- Use specific English keywords for better results (see `references/common_queries.md`)
- If initial query returns no results, try related terms:
  - "Delta Lake" → "Introduction to Delta Lake", "Delta Lake Tutorial"
  - "SQL" → "SQL Analytics", "Databricks SQL", "SQL Fundamentals"
- Search for course codes if known (e.g., "DE 101", "ML 201")

### Step 4: Extract and Present Results

Process search results and present them to the user:

1. Extract relevant information from browser_snapshot:
   - Course/tutorial titles
   - Descriptions or summaries
   - URLs (relative or absolute)
   - Content type (course, lab, documentation, certification prep)

2. Format results in structured markdown:
   ```markdown
   ## Search Results for "[query]"

   ### 1. [Course/Tutorial Title]
   - **Type**: [Course/Lab/Documentation]
   - **Link**: [URL]
   - **Description**: [Brief description]
   - **Key Topics**: [Main concepts covered]

   ### 2. [Next Result]
   ...

   ### Recommendations
   - [Suggested follow-up courses or related materials]
   ```

3. For course detail requests, navigate to the specific course page:
   - Use browser_click to open the course
   - Extract syllabus, modules, or learning objectives
   - Summarize the content structure

### Step 5: Handle Follow-up Queries

During the session, maintain the browser context to handle additional requests:

- Keep the browser session alive for follow-up questions
- Navigate to different pages as needed using browser_navigate or browser_click
- Extract specific information from course pages or modules
- Close the browser only when the user ends the session or no longer needs access

**Session Management**: After completing all queries, close the browser using browser_close to ensure credentials are discarded.

## Error Handling

### Login Failures

**Symptoms**: Unable to authenticate, wrong credentials, or unexpected redirects

**Actions**:
- Verify credentials with the user
- Check if the website structure has changed (different login form elements)
- Inform the user if SSO or 2FA is blocking automated login
- Suggest manual verification on the website

### Page Load Issues

**Symptoms**: Timeouts, incomplete page loads, dynamic content not appearing

**Actions**:
- Increase wait time using browser_wait_for with appropriate text or time parameter
- Use browser_snapshot to verify current page state
- Retry navigation if needed
- Inform the user if the website is experiencing issues

### Search Returns No Results

**Symptoms**: Empty search results or "no content found" messages

**Actions**:
- Try alternative search terms (see `references/common_queries.md`)
- Suggest broader or narrower queries
- Recommend specific courses or learning paths related to the topic
- Verify the topic is covered on Databricks Academy

### Browser Session Errors

**Symptoms**: Browser crashes, lost connection, or unexpected closures

**Actions**:
- Restart the browser and re-authenticate
- Inform the user about the interruption
- Resume from the last known state

## Tools Used

This skill relies on the following MCP tools:

- `mcp__playwright__browser_navigate` - Navigate to URLs
- `mcp__playwright__browser_snapshot` - Capture page structure
- `mcp__playwright__browser_type` - Enter text in form fields
- `mcp__playwright__browser_click` - Click buttons and links
- `mcp__playwright__browser_wait_for` - Wait for page elements or time delays
- `mcp__playwright__browser_close` - Close browser and clear session
- `AskUserQuestion` - Collect user input securely

## References

### Common Queries

See `references/common_queries.md` for:
- Popular Databricks Academy topics (Data Engineering, ML, Analytics)
- Effective search keywords
- Course structure and content types

Use this reference to optimize searches and suggest related content to users.

## Limitations

1. **Authentication Required**: All content requires a valid Databricks Academy account
2. **Access Restrictions**: Content availability depends on user account permissions and subscriptions
3. **Dynamic Content**: Page structure may change, requiring adjustments to element selectors
4. **Session Duration**: Browser sessions are temporary and must be re-authenticated for new conversations
5. **Rate Limiting**: Excessive requests may trigger website rate limiting or security measures

## Best Practices

- Always verify successful login before proceeding with searches
- Use browser_snapshot frequently to adapt to page structure
- Provide clear, structured output to users
- Suggest related courses and learning paths proactively
- Close browser sessions promptly after completing requests
- Never log or store user credentials
