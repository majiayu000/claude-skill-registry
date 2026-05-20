---
name: sonarcloud-tools
type: complex
depth: base
user-invocable: false
description: >-
  Executes SonarCloud API operations for quality gates, issues, metrics, analysis history, and security hotspots. Use when checking code quality, inspecting bugs/vulnerabilities, retrieving coverage/complexity metrics, or viewing project security status.
---

# [H1][SONARCLOUD-TOOLS]
>**Dictum:** *Zero-arg defaults enable immediate code quality inspection.*

<br>

Execute SonarCloud queries through unified Python CLI.

[IMPORTANT] Commands default to `project=bsamiee_Parametric_Portal`, `organization=bsamiee`. 1Password auto-injects API token. SonarCloud API base: `https://sonarcloud.io/api`.

---
## [0][SCANNER]
>**Dictum:** *Local scanner enables pre-push quality gates.*

<br>

**Run Analysis:**
```bash
pnpm sonar
```

**Requirements:**
- `SONAR_TOKEN` environment variable (1Password injection or export)<br>
- Coverage reports at `packages/*/coverage/lcov.info` (run `nx run-many -t test` first)

**Configuration:** `sonar-project.properties` at repo root.

---
## [1][COMMANDS]

| [CMD]        | [ARGS]                   | [PURPOSE]                     |
| ------------ | ------------------------ | ----------------------------- |
| quality-gate | `[branch]` or `pr <num>` | Quality gate pass/fail status |
| issues       | `[severities] [types]`   | Search code issues            |
| measures     | `[metrics]`              | Project metrics               |
| analyses     | `[page_size]`            | Analysis history              |
| projects     | `[page_size]`            | List organization projects    |
| hotspots     | `[status]`               | Security hotspots             |

---
## [2][USAGE]

```bash
# Zero-arg invocation (most common)
uv run .claude/skills/sonarcloud-tools/scripts/sonarcloud.py quality-gate
uv run .claude/skills/sonarcloud-tools/scripts/sonarcloud.py issues
uv run .claude/skills/sonarcloud-tools/scripts/sonarcloud.py measures
uv run .claude/skills/sonarcloud-tools/scripts/sonarcloud.py analyses
uv run .claude/skills/sonarcloud-tools/scripts/sonarcloud.py projects
uv run .claude/skills/sonarcloud-tools/scripts/sonarcloud.py hotspots

# With optional args
uv run .claude/skills/sonarcloud-tools/scripts/sonarcloud.py quality-gate main
uv run .claude/skills/sonarcloud-tools/scripts/sonarcloud.py quality-gate pr 42
uv run .claude/skills/sonarcloud-tools/scripts/sonarcloud.py issues BLOCKER,CRITICAL
uv run .claude/skills/sonarcloud-tools/scripts/sonarcloud.py issues BLOCKER,CRITICAL BUG,VULNERABILITY
uv run .claude/skills/sonarcloud-tools/scripts/sonarcloud.py measures coverage,bugs
uv run .claude/skills/sonarcloud-tools/scripts/sonarcloud.py analyses 20
uv run .claude/skills/sonarcloud-tools/scripts/sonarcloud.py projects 50
uv run .claude/skills/sonarcloud-tools/scripts/sonarcloud.py hotspots TO_REVIEW
```

---
## [3][ARGUMENTS]

**quality-gate**: `[branch]` or `pr <num>`
- No args -- current default branch
- `main` -- specific branch
- `pr 42` -- specific pull request

**issues**: `[severities] [types]`
- `severities` -- Comma-separated: `BLOCKER`, `CRITICAL`, `MAJOR`, `MINOR`, `INFO`
- `types` -- Comma-separated: `BUG`, `VULNERABILITY`, `CODE_SMELL`

**measures**: `[metrics]`
- `metrics` -- Comma-separated (default: all standard metrics)
- Standard: `ncloc`, `coverage`, `bugs`, `vulnerabilities`, `code_smells`, `duplicated_lines_density`, `security_hotspots`, `reliability_rating`, `security_rating`, `sqale_rating`

**analyses**: `[page_size]`
- `page_size` -- Number of results (default: `10`, max: `100`)

**projects**: `[page_size]`
- `page_size` -- Number of results (default: `100`, max: `500`)

**hotspots**: `[status]`
- `status` -- Filter: `TO_REVIEW`, `ACKNOWLEDGED`, `FIXED`, `SAFE`

---
## [4][OUTPUT]

Commands return: `{"status": "success|error", ...}`.

| [INDEX] | [CMD]          | [RESPONSE]                                           |
| :-----: | -------------- | ---------------------------------------------------- |
|   [1]   | `quality-gate` | `{project, gate_status, passed: bool, conditions[]}` |
|   [2]   | `issues`       | `{project, total, issues[], summary}`                |
|   [3]   | `measures`     | `{project, name, metrics}`                           |
|   [4]   | `analyses`     | `{project, total, analyses[]}`                       |
|   [5]   | `projects`     | `{organization, total, projects[]}`                  |
|   [6]   | `hotspots`     | `{project, total, hotspots[]}`                       |

---
## [5][ENVIRONMENT]

| [VAR]         | [REQUIRED] | [DESCRIPTION]                    |
| ------------- | ---------- | -------------------------------- |
| `SONAR_TOKEN` | Yes        | SonarCloud API token (1Password) |

---
## [6][ERROR_HANDLING]

- HTTP errors print `[ERROR] <status>: <body>` and exit 1
- Missing token: `[ERROR] SONAR_TOKEN environment variable not set`
- Project not found: `[ERROR] 404: Component not found`
- Invalid metric name: returns empty metric value (not an error)
