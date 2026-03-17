---
name: workflow-integration-sonar
description: Sonar issue workflow - fetch issues, triage, and fix or suppress based on context
user-invocable: false
allowed-tools: Read, Edit, Write, Bash(gh:*), Grep, Glob, mcp__sonarqube__search_sonar_issues_in_projects, mcp__sonarqube__change_sonar_issue_status
---

# Sonar Workflow Skill

Handles Sonar issue workflows - fetching issues from SonarQube, triaging them, and implementing fixes or suppressions.

## What This Skill Provides

### Workflows (Absorbs 2 Agents)

1. **Fetch Issues Workflow** - Retrieves Sonar issues for PR
   - Uses SonarQube MCP tool or API
   - Replaces: sonar-issue-fetcher agent

2. **Fix Issues Workflow** - Processes and resolves issues
   - Triages each issue for fix vs suppress
   - Implements fixes or adds suppressions
   - Replaces: sonar-issue-triager agent

## When to Activate This Skill

- Fixing Sonar issues in PRs
- Processing SonarQube quality gate failures
- Implementing code fixes for violations
- Adding justified suppressions

## Workflows

### Workflow 1: Fetch Issues

**Purpose:** Fetch Sonar issues for a PR or project.

**Input:**
- **project**: SonarQube project key
- **pr** (optional): Pull request ID
- **severities** (optional): Filter by severity
- **types** (optional): Filter by type

**Steps:**

1. **Determine Context**
   ```bash
   gh pr view --json number
   ```

2. **Fetch Issues**
   Use MCP tool:
   ```
   mcp__sonarqube__search_sonar_issues_in_projects(
     projects: ["{project_key}"],
     pullRequestId: "{pr_number}",
     severities: "{filter}"
   )
   ```

   Or use script for structure:

   Script: `pm-workflow:workflow-integration-sonar`

   ```bash
   python3 .plan/execute-script.py pm-workflow:workflow-integration-sonar:sonar fetch --project {key} [--pr {id}]
   ```

3. **Return Structured List**

**Output:**
```json
{
  "project_key": "...",
  "pull_request_id": "...",
  "issues": [
    {
      "key": "...",
      "type": "BUG|CODE_SMELL|VULNERABILITY",
      "severity": "BLOCKER|CRITICAL|MAJOR|MINOR|INFO",
      "file": "...",
      "line": N,
      "rule": "java:S1234",
      "message": "..."
    }
  ],
  "statistics": {
    "total_issues_fetched": N,
    "by_severity": {...},
    "by_type": {...}
  }
}
```

---

### Workflow 2: Fix Issues

**Purpose:** Process Sonar issues and resolve them.

**Input:** Issue list from Fetch workflow or specific issue keys

**Steps:**

1. **Get Issues**
   If not provided, use Fetch Issues workflow first.

2. **Triage Each Issue**
   For each issue:

   Script: `pm-workflow:workflow-integration-sonar`

   ```bash
   python3 .plan/execute-script.py pm-workflow:workflow-integration-sonar:sonar triage --issue '{json}'
   ```

   Script outputs decision:
   ```json
   {
     "issue_key": "...",
     "action": "fix|suppress",
     "reason": "...",
     "priority": "critical|high|medium|low",
     "suggested_implementation": "...",
     "suppression_string": "// NOSONAR rule - reason"
   }
   ```

3. **Process by Priority**
   Order: critical → high → medium → low

4. **Execute Actions**

   **For fix:**
   - Read file at issue location
   - Apply fix using Edit tool
   - Verify fix with Grep

   **For suppress:**
   - Read file
   - Add suppression comment at line using Edit
   - Include rule key and reason

5. **Mark Issues Resolved (Optional)**
   ```
   mcp__sonarqube__change_sonar_issue_status(
     key: "{issue_key}",
     status: ["accept"]  # or ["falsepositive"]
   )
   ```

6. **Return Summary**

**Output:**
```json
{
  "processed": {
    "fixed": 4,
    "suppressed": 1,
    "failed": 0
  },
  "files_modified": ["..."],
  "status": "success"
}
```

---

## Scripts

Script: `pm-workflow:workflow-integration-sonar` → `sonar.py`

### sonar.py fetch

**Purpose:** Generate structure for fetching Sonar issues.

**Usage:**
```bash
python3 .plan/execute-script.py pm-workflow:workflow-integration-sonar:sonar fetch --project <key> [--pr <id>] [--severities <list>]
```

**Output:** JSON with MCP instruction and expected structure

### sonar.py triage

**Purpose:** Analyze a single issue and determine fix vs suppress.

**Usage:**
```bash
python3 .plan/execute-script.py pm-workflow:workflow-integration-sonar:sonar triage --issue '{"key":"...", "rule":"...", ...}'
```

**Output:** JSON with action decision

## References (Load On-Demand)

### Sonar Fix Guide
```
Read references/sonar-fix-guide.md
```

Provides:
- Common rule fixes
- Suppression patterns by language
- Valid suppression reasons

## Issue Classification

### Always Fix
- BLOCKER severity
- VULNERABILITY type
- Security rules (java:S3649, java:S5131)

### Fix Preferred
- CRITICAL severity
- BUG type
- Resource leaks (java:S2095)

### May Suppress
- INFO severity
- TODO comments (java:S1135) - if tracked
- Unused fields for reflection (java:S1068)
- Test code patterns (java:S106, java:S2699)

## Suppression Format

**Java:**
```java
// NOSONAR java:S1234 - reason for suppression
```

**JavaScript:**
```javascript
// NOSONAR
```

## Integration

### Commands Using This Skill
- **/pr-fix-sonar-issues** - Dedicated Sonar fix command
- **/pr-handle-pull-request** - Full PR workflow

### Related Skills
- **pr-workflow** - Often used together in PR workflows
- **git-workflow** - Commits fixes

## Quality Verification

- [x] Self-contained with relative path pattern
- [x] Progressive disclosure (references loaded on-demand)
- [x] Scripts output JSON for machine processing
- [x] Both fetcher and triager agents absorbed
- [x] Clear workflow definitions
- [x] MCP tool integration documented

## References

- SonarQube Rules: https://rules.sonarsource.com/
- SonarQube Documentation: https://docs.sonarqube.org/
