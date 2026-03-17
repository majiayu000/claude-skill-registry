---
name: sonarcloud-api
description: Expert guidance for using the SonarCloud API to interact with code quality analysis, projects, issues, quality gates, and metrics. Use this skill when making API calls to SonarCloud, automating code quality workflows, retrieving analysis results, managing projects programmatically, or integrating SonarCloud with CI/CD pipelines. Trigger keywords include "SonarCloud", "SonarCloud API", "code quality API", "SonarQube Cloud", "quality gate", "code analysis API", "SonarCloud measures", "SonarCloud issues".
---

# SonarCloud API

## Overview

SonarCloud provides two API versions for programmatic access:

- **Web API v2** - Modern REST API with OpenAPI specifications at `https://api.sonarcloud.io/api/v2/`
- **Web API v1** - Legacy API at `https://sonarcloud.io/api/` with comprehensive endpoint coverage

## Quick start

```bash
# Get project metrics
curl -X GET "https://sonarcloud.io/api/measures/component?component=my_project&metricKeys=bugs,vulnerabilities,code_smells" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Authentication

Use bearer token authentication for all requests:

```
Authorization: Bearer <token>
```

### Token types

| Token Type            | Plan | Scope               | Use Case              |
| --------------------- | ---- | ------------------- | --------------------- |
| Personal Access Token | Free | User-level          | Individual API access |
| Organisation Token    | Team | Organisation-scoped | CI/CD, automation     |

Generate tokens at **Account > Security > Generate Tokens** in SonarCloud UI.

## Base URLs

| API Version | Base URL                            |
| ----------- | ----------------------------------- |
| Web API v1  | `https://sonarcloud.io/api/`        |
| Web API v2  | `https://api.sonarcloud.io/api/v2/` |

## Request format

**Content-Type:** `application/x-www-form-urlencoded` (v1) or `application/json` (v2)

For POST requests, use form data parameters rather than URI query parameters.

## Rate limiting

Requests are rate-limited. When exceeded, the API returns HTTP **429**. Wait several minutes before retrying.

## Pagination

Most list endpoints support pagination with `p` (page number) and `ps` (page size) parameters.

## Common tasks

### Get project quality gate status

```bash
curl -X GET "https://sonarcloud.io/api/qualitygates/project_status?projectKey=my_project" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Search issues

```bash
curl -X GET "https://sonarcloud.io/api/issues/search?componentKeys=my_project&types=BUG,VULNERABILITY" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Get component measures

```bash
curl -X GET "https://sonarcloud.io/api/measures/component?component=my_project&metricKeys=ncloc,coverage,duplicated_lines_density" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### List projects

```bash
# v2 API
curl -X GET "https://api.sonarcloud.io/api/v2/projects?organization=my_org" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## API reference

For detailed endpoint documentation, see the reference files:

- **[v2-api.md](references/v2-api.md)** - Modern v2 API endpoints (Projects, Quality Gates, Analysis, Organisations)
- **[v1-api.md](references/v1-api.md)** - Legacy v1 API endpoints (Issues, Measures, Components, Rules)
- **[metrics.md](references/metrics.md)** - Available metric keys and their meanings

## Error handling

| Status Code | Meaning                                 |
| ----------- | --------------------------------------- |
| 400         | Bad request - check parameters          |
| 401         | Unauthorised - invalid or missing token |
| 403         | Forbidden - insufficient permissions    |
| 404         | Not found - resource does not exist     |
| 429         | Rate limited - wait and retry           |
| 500         | Server error                            |

## CI/CD integration examples

### GitHub Actions

```yaml
- name: Check Quality Gate
  run: |
      STATUS=$(curl -s -H "Authorization: Bearer ${{ secrets.SONAR_TOKEN }}" \
        "https://sonarcloud.io/api/qualitygates/project_status?projectKey=${{ vars.SONAR_PROJECT_KEY }}" \
        | jq -r '.projectStatus.status')
      if [ "$STATUS" != "OK" ]; then
        echo "Quality Gate failed"
        exit 1
      fi
```

### GitLab CI

```yaml
check_quality_gate:
    script:
        - |
            STATUS=$(curl -s -H "Authorization: Bearer $SONAR_TOKEN" \
              "https://sonarcloud.io/api/qualitygates/project_status?projectKey=$SONAR_PROJECT_KEY" \
              | jq -r '.projectStatus.status')
            if [ "$STATUS" != "OK" ]; then exit 1; fi
```
