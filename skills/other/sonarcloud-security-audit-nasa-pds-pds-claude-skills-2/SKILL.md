---
name: sonarcloud-security-audit
description: Audit SonarCloud security issues (vulnerabilities and hotspots) for NASA PDS repositories and export to CSV for triage. Use when the user requests SonarCloud security scans, vulnerability reports, or security audits for PDS projects.
---

# SonarCloud Security Audit Skill

This skill fetches all security-related issues (vulnerabilities and security hotspots) from SonarCloud for all repositories under the NASA PDS organization and exports them to a CSV file for security triage.

## Prerequisites

- Node.js v18 or higher
- SonarCloud API token with read access to nasa-pds organization

## How It Works

1. **Authenticate**: Uses SonarCloud API token (from `SONARCLOUD_TOKEN` environment variable or prompts user)
2. **Fetch Projects**: Queries `/api/projects/search?organization=nasa-pds` to get all repositories
3. **Query Vulnerabilities**: For each project, calls `/api/issues/search` with `types=VULNERABILITY`
4. **Query Hotspots**: For each project, calls `/api/hotspots/search`
5. **Export CSV**: Combines results into a CSV file with triage columns

## Execution Steps

### Step 1: Check for API Token

Check if `SONARCLOUD_TOKEN` environment variable is set:

```bash
env | grep SONARCLOUD_TOKEN
```

If not set, prompt the user:
- "A SonarCloud API token is required to access the NASA PDS organization."
- "You can generate a token at: https://sonarcloud.io/account/security"
- "Please set the SONARCLOUD_TOKEN environment variable or provide it when prompted."

### Step 2: Run the Fetch Script

Execute the main script:

```bash
cd sonarcloud-security-audit
node scripts/fetch-security-issues.mjs nasa-pds [output-file.csv]
```

**Parameters:**
- `nasa-pds` (required): Organization key
- `output-file.csv` (optional): Output file path (default: `sonarcloud-security-issues-{timestamp}.csv`)

The script handles:
- Pagination for large result sets (SonarCloud API returns max 500 items per page)
- Rate limiting (429 responses)
- Authentication errors (401)
- Network failures with retry logic

### Step 3: Review Output

The CSV will contain these columns:
- **Project**: Repository/project key
- **Type**: `VULNERABILITY` or `SECURITY_HOTSPOT`
- **Severity**: `BLOCKER`, `CRITICAL`, `MAJOR`, `MINOR`, `INFO` (vulnerabilities only)
- **Status**: `OPEN`, `CONFIRMED`, `RESOLVED`, `REOPENED`, `CLOSED`
- **Rule**: SonarCloud rule ID (e.g., `javascript:S4426`)
- **Message**: Issue description
- **Component**: File path
- **Line**: Line number (if applicable)
- **Created**: ISO 8601 timestamp
- **URL**: Direct link to issue in SonarCloud UI

### Step 4: Present Results

After successful execution:
1. Display count summary: `Found X vulnerabilities and Y security hotspots across Z projects`
2. Show output file path
3. Provide quick triage suggestions:
   - Sort by severity (BLOCKER/CRITICAL first)
   - Filter by status (focus on OPEN/CONFIRMED)
   - Group by rule for bulk remediation

## CSV Output Format

```csv
Project,Type,Severity,Status,Rule,Message,Component,Line,Created,URL
pds-api,VULNERABILITY,CRITICAL,OPEN,java:S4426,Use a secure cipher...,src/main/Security.java,45,2025-01-15T10:30:00Z,https://sonarcloud.io/...
pds-registry,SECURITY_HOTSPOT,,TO_REVIEW,java:S2092,Cookie should be HttpOnly,src/auth/Cookie.java,23,2025-01-10T09:15:00Z,https://sonarcloud.io/...
```

## Error Handling

### Authentication Failures (401)
- Verify token is valid and not expired
- Check token has read permissions for nasa-pds organization
- Regenerate token at https://sonarcloud.io/account/security

### Rate Limiting (429)
- Script automatically waits 60 seconds before retrying
- Reduce concurrent requests if persistent

### No Results
- Verify organization key is correct (`nasa-pds`)
- Check if projects exist: https://sonarcloud.io/organizations/nasa-pds/projects
- Confirm projects have been analyzed (no analysis = no issues)

## Advanced Options

### Filter by Severity
Modify script to filter vulnerabilities by severity:
```javascript
const severities = ['BLOCKER', 'CRITICAL']; // Only high severity
```

### Filter by Status
Include only actionable issues:
```javascript
const statuses = ['OPEN', 'CONFIRMED', 'REOPENED'];
```

### Date Range
Filter issues created after a specific date:
```javascript
const createdAfter = '2025-01-01'; // YYYY-MM-DD format
```

## SonarCloud API Reference

- **Projects Search**: `GET /api/projects/search?organization={org}`
- **Issues Search**: `GET /api/issues/search?organization={org}&componentKeys={project}&types=VULNERABILITY`
- **Hotspots Search**: `GET /api/hotspots/search?organization={org}&projectKey={project}`

All requests require: `Authorization: Bearer {token}`

Base URL: `https://sonarcloud.io/api`

## Troubleshooting

**"Organization not found"**
- Verify organization key: `nasa-pds` (case-sensitive)
- Check access permissions

**Empty CSV**
- Projects may not have security issues (good news!)
- Verify projects are analyzed in SonarCloud
- Check if token has correct organization scope

**Timeout errors**
- NASA PDS has many repositories; script may take 5-10 minutes
- Monitor progress output to track completion

## Notes

- Security hotspots do NOT have severity levels (they require manual review to determine if they're actual vulnerabilities)
- The `Status` field for hotspots uses different values: `TO_REVIEW`, `REVIEWED`, `ACKNOWLEDGED`
- URLs link directly to SonarCloud UI for detailed analysis and remediation guidance
- CSV can be imported into spreadsheet tools, Jira, or other triage systems
