---
name: renovate
description: Configure Renovate Bot for automated dependency updates. Keep packages secure and up-to-date with customizable rules, grouping, and scheduling. Use for dependency management, security updates, or automated maintenance. Triggers on renovate, dependabot, dependency updates, package updates.
---

# Renovate Dependency Updates

Automated dependency update management with Renovate Bot.

## Quick Reference

| Config File | Location |
|-------------|----------|
| `renovate.json` | Repository root |
| `renovate.json5` | With comments |
| `.github/renovate.json` | GitHub location |
| `package.json` | "renovate" key |

## 1. Basic Setup

### Enable Renovate

```bash
# GitHub: Install Renovate App
# https://github.com/apps/renovate

# Self-hosted: npm package
npm install -g renovate
```

### Basic Configuration (renovate.json)

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "config:recommended"
  ]
}
```

### Extended Configuration

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "config:recommended",
    "schedule:weekends",
    "group:allNonMajor",
    ":automergeMinor",
    ":automergePatch",
    ":dependencyDashboard"
  ],
  "labels": ["dependencies"],
  "assignees": ["@me"],
  "prHourlyLimit": 5,
  "prConcurrentLimit": 10
}
```

## 2. Scheduling

### Preset Schedules

```json
{
  "extends": [
    "schedule:weekly",
    "schedule:weekends",
    "schedule:nonOfficeHours",
    "schedule:earlyMondays"
  ]
}
```

### Custom Schedule

```json
{
  "schedule": [
    "after 10pm every weekday",
    "before 5am every weekday",
    "every weekend"
  ],
  "timezone": "America/New_York"
}
```

### Package-Specific Schedule

```json
{
  "packageRules": [
    {
      "matchPackagePatterns": ["eslint"],
      "schedule": ["before 3am on Monday"]
    },
    {
      "matchUpdateTypes": ["major"],
      "schedule": ["on the first day of the month"]
    }
  ]
}
```

## 3. Package Rules

### Group Updates

```json
{
  "packageRules": [
    {
      "groupName": "React",
      "matchPackagePatterns": ["^react", "^@types/react"]
    },
    {
      "groupName": "ESLint",
      "matchPackagePatterns": ["eslint"]
    },
    {
      "groupName": "Testing",
      "matchPackagePatterns": ["jest", "vitest", "@testing-library"]
    },
    {
      "groupName": "TypeScript",
      "matchPackagePatterns": ["typescript", "^@types/"]
    }
  ]
}
```

### Auto-merge Configuration

```json
{
  "packageRules": [
    {
      "matchUpdateTypes": ["patch"],
      "automerge": true
    },
    {
      "matchUpdateTypes": ["minor"],
      "matchPackagePatterns": ["eslint", "prettier"],
      "automerge": true
    },
    {
      "matchUpdateTypes": ["major"],
      "automerge": false,
      "labels": ["breaking-change"]
    },
    {
      "matchDepTypes": ["devDependencies"],
      "automerge": true
    }
  ]
}
```

### Version Constraints

```json
{
  "packageRules": [
    {
      "matchPackageNames": ["node"],
      "allowedVersions": ">=18.0.0 <21.0.0"
    },
    {
      "matchPackagePatterns": ["^@aws-sdk/"],
      "allowedVersions": "3.x"
    },
    {
      "matchPackageNames": ["typescript"],
      "matchCurrentVersion": ">=5.0.0",
      "enabled": true
    }
  ]
}
```

### Disable Updates

```json
{
  "packageRules": [
    {
      "matchPackageNames": ["legacy-package"],
      "enabled": false
    },
    {
      "matchPackagePatterns": ["^@internal/"],
      "enabled": false
    },
    {
      "matchUpdateTypes": ["major"],
      "matchPackagePatterns": ["react"],
      "enabled": false
    }
  ]
}
```

## 4. Manager Configuration

### Node.js

```json
{
  "npm": {
    "extends": ["npm:unpublishSafe"],
    "stabilityDays": 3
  },
  "packageRules": [
    {
      "matchManagers": ["npm"],
      "rangeStrategy": "bump"
    }
  ]
}
```

### Python

```json
{
  "pip_requirements": {
    "fileMatch": ["requirements.*\\.txt$"]
  },
  "pip_setup": {
    "enabled": true
  },
  "poetry": {
    "enabled": true
  },
  "packageRules": [
    {
      "matchManagers": ["pip_requirements", "poetry"],
      "groupName": "Python dependencies"
    }
  ]
}
```

### Docker

```json
{
  "docker": {
    "enabled": true,
    "pinDigests": true
  },
  "docker-compose": {
    "enabled": true
  },
  "packageRules": [
    {
      "matchManagers": ["docker-compose", "dockerfile"],
      "groupName": "Docker images"
    },
    {
      "matchDatasources": ["docker"],
      "matchPackagePatterns": ["^node$"],
      "versioning": "node"
    }
  ]
}
```

### GitHub Actions

```json
{
  "github-actions": {
    "enabled": true,
    "pinDigests": true
  },
  "packageRules": [
    {
      "matchManagers": ["github-actions"],
      "groupName": "GitHub Actions",
      "automerge": true
    }
  ]
}
```

### Terraform

```json
{
  "terraform": {
    "enabled": true
  },
  "packageRules": [
    {
      "matchManagers": ["terraform"],
      "matchPackagePatterns": ["hashicorp/*"],
      "groupName": "HashiCorp providers"
    }
  ]
}
```

## 5. Labels and Assignees

```json
{
  "labels": ["dependencies", "automated"],
  "assignees": ["team-lead"],
  "assigneesSampleSize": 1,
  "reviewers": ["team:core"],
  "reviewersSampleSize": 2,
  "packageRules": [
    {
      "matchUpdateTypes": ["major"],
      "labels": ["dependencies", "breaking-change"],
      "reviewers": ["team:seniors"]
    },
    {
      "matchPackagePatterns": ["security"],
      "labels": ["dependencies", "security"],
      "prioritySchedule": ["at any time"]
    }
  ]
}
```

## 6. Pull Request Configuration

```json
{
  "prTitle": "deps({{depName}}): update to {{newVersion}}",
  "commitMessagePrefix": "deps:",
  "commitMessageAction": "update",
  "commitMessageTopic": "{{depName}}",
  "commitMessageExtra": "to {{newVersion}}",
  "prBodyColumns": [
    "Package",
    "Type",
    "Update",
    "Change",
    "Pending"
  ],
  "prBodyNotes": [
    "This PR has been generated by [Renovate Bot](https://github.com/renovatebot/renovate)."
  ]
}
```

## 7. Security Updates

```json
{
  "extends": [
    "config:recommended",
    ":enableVulnerabilityAlertsWithLabel('security')"
  ],
  "vulnerabilityAlerts": {
    "labels": ["security"],
    "automerge": true,
    "schedule": ["at any time"],
    "stabilityDays": 0
  },
  "packageRules": [
    {
      "matchCategories": ["security"],
      "labels": ["security", "priority-high"],
      "prPriority": 10
    }
  ]
}
```

## 8. Monorepo Configuration

```json
{
  "ignorePaths": [
    "**/node_modules/**",
    "**/bower_components/**"
  ],
  "packageRules": [
    {
      "matchPaths": ["packages/frontend/**"],
      "groupName": "Frontend dependencies"
    },
    {
      "matchPaths": ["packages/backend/**"],
      "groupName": "Backend dependencies"
    }
  ],
  "additionalBranchPrefix": "{{parentDir}}-"
}
```

## 9. Complete Example

```json5
// renovate.json5
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",

  // Base configuration
  "extends": [
    "config:recommended",
    ":dependencyDashboard",
    ":semanticCommits",
    "schedule:weekends"
  ],

  // General settings
  "labels": ["dependencies"],
  "prHourlyLimit": 5,
  "prConcurrentLimit": 10,
  "timezone": "America/New_York",

  // Commit message format
  "commitMessagePrefix": "deps:",
  "commitMessageAction": "update",

  // Package rules
  "packageRules": [
    // Auto-merge patches and minor for dev deps
    {
      "matchDepTypes": ["devDependencies"],
      "matchUpdateTypes": ["patch", "minor"],
      "automerge": true
    },

    // Group TypeScript ecosystem
    {
      "groupName": "TypeScript",
      "matchPackagePatterns": ["typescript", "^@types/"],
      "schedule": ["before 3am on Monday"]
    },

    // Group React ecosystem
    {
      "groupName": "React",
      "matchPackagePatterns": ["^react", "^@types/react"]
    },

    // Group linting tools
    {
      "groupName": "Linting",
      "matchPackagePatterns": ["eslint", "prettier"],
      "automerge": true
    },

    // Group testing tools
    {
      "groupName": "Testing",
      "matchPackagePatterns": ["jest", "vitest", "@testing-library"]
    },

    // Pin GitHub Actions
    {
      "matchManagers": ["github-actions"],
      "groupName": "GitHub Actions",
      "automerge": true,
      "pinDigests": true
    },

    // Docker updates
    {
      "matchManagers": ["dockerfile", "docker-compose"],
      "groupName": "Docker",
      "pinDigests": true
    },

    // Major updates need review
    {
      "matchUpdateTypes": ["major"],
      "labels": ["dependencies", "breaking-change"],
      "automerge": false
    },

    // Disable problematic packages
    {
      "matchPackageNames": ["node"],
      "allowedVersions": "20.x"
    }
  ],

  // Regex managers for custom files
  "regexManagers": [
    {
      "fileMatch": ["Dockerfile$"],
      "matchStrings": [
        "ARG NODE_VERSION=(?<currentValue>.*?)\\n"
      ],
      "depNameTemplate": "node",
      "datasourceTemplate": "node"
    }
  ]
}
```

## 10. Dependency Dashboard

```json
{
  "extends": [":dependencyDashboard"],
  "dependencyDashboardTitle": "Dependency Dashboard",
  "dependencyDashboardLabels": ["dependencies"],
  "dependencyDashboardOSVVulnerabilitySummary": "all"
}
```

The Dependency Dashboard is a GitHub issue that shows:
- Pending updates
- Open PRs
- Rate-limited PRs
- Detected vulnerabilities
- Checkbox to trigger updates manually

## Best Practices

1. **Start conservative** - Use `config:recommended`
2. **Group related packages** - Fewer PRs, easier review
3. **Auto-merge wisely** - Patches for dependencies with good test coverage
4. **Schedule updates** - Non-work hours, weekends
5. **Pin versions in production** - Use lock files
6. **Security first** - Enable vulnerability alerts
7. **Use stability days** - Wait for bug reports
8. **Set concurrency limits** - Avoid PR flood
9. **Review majors manually** - Breaking changes need attention
10. **Dashboard for visibility** - Track pending updates
