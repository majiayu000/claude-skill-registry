---
name: skill-gap-analyzer
description: |
  Analyzes project requirements to identify missing skills and automatically creates them.
  Enforces MCP Code Execution pattern for skills that use external tools.
  This skill should be used when starting a new project to ensure all required skills exist.
author: Claude Code
version: 2.1.0
mcp-pattern: enforced
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Skill Gap Analyzer

Automatically identifies and creates missing skills based on project requirements.
**Enforces MCP Code Execution pattern** for token efficiency when skills use external tools.

---

## MANDATORY EXECUTION STEPS

When this skill is invoked, you MUST execute these steps IN ORDER:

### Step A: Read Requirements File
```
Read the requirements file passed as argument
```

### Step B: Detect Technologies
Scan for these keywords and mark detected:

| Technology | Keywords to Search |
|------------|-------------------|
| React | "react", "jsx", "component" |
| Next.js | "next.js", "nextjs", "next" |
| Express | "express", "node api", "nodejs backend" |
| FastAPI | "fastapi", "python api", "uvicorn" |
| PostgreSQL | "postgresql", "postgres", "pg" |
| MongoDB | "mongodb", "mongo", "mongoose" |
| Prisma | "prisma", "orm" |
| Docker | "docker", "container", "dockerfile" |
| TypeScript | "typescript", "ts", ".tsx" |
| Jest | "jest", "test", "testing" |
| Playwright | "playwright", "e2e", "end-to-end" |

### Step C: List Existing Skills
```bash
ls -la .claude/skills/
```

### Step D: Create Missing Skills (WITH GUARDRAILS)

**⚠️ CRITICAL RULES:**
```
╔═══════════════════════════════════════════════════════════════════════════╗
║  SKILL CREATION RULES - NEVER VIOLATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════╣
║  ✓ ONLY create skills in: .claude/skills/{name}/SKILL.md                  ║
║  ✗ NEVER create: skill-lab/, workspace/, temp/, output/                   ║
║  ✗ NEVER create: .claude/ inside another directory                        ║
║  ✗ NEVER create: nested directories like .claude/.claude/                 ║
║  ✗ NEVER overwrite existing skills - SKIP if exists                       ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

For EACH detected technology that doesn't have a skill:

1. **CHECK if skill exists first:**
   ```bash
   if [ -f ".claude/skills/{tech}-patterns/SKILL.md" ]; then
       echo "SKIP: {tech}-patterns already exists"
       continue
   fi
   ```

2. Create directory: `mkdir -p .claude/skills/{tech}-patterns`
   - ONLY in `.claude/skills/` - NOWHERE else

3. Create SKILL.md with the template below

4. Add technology-specific content

### Step E: Generate Report
Create `.specify/skill-gap-report.json` with results

---

## Core Workflow

### 1. Analyze Requirements

Extract technology requirements from the project:

```python
def analyze_requirements(requirements_text: str) -> dict:
    """Extract technologies and patterns from requirements."""

    patterns = {
        "fastapi": ["fastapi", "python api", "rest api python"],
        "nextjs": ["next.js", "nextjs", "react frontend", "frontend"],
        "express": ["express", "node.js api", "nodejs"],
        "postgresql": ["postgresql", "postgres", "sql database"],
        "mongodb": ["mongodb", "mongo", "nosql", "document database"],
        "kafka": ["kafka", "event streaming", "message queue"],
        "graphql": ["graphql", "graph api"],
        "docker": ["docker", "container", "dockerfile"],
        "kubernetes": ["kubernetes", "k8s", "kubectl"],
        "github-actions": ["github actions", "ci/cd", "pipeline"],
    }

    # MCP-related patterns (require code execution)
    mcp_patterns = {
        "google-drive": ["google drive", "gdrive", "docs api"],
        "salesforce": ["salesforce", "crm", "sfdc"],
        "slack": ["slack", "slack api", "messaging"],
        "github-api": ["github api", "repository api", "issues api"],
        "database-query": ["query database", "sql queries", "data extraction"],
        "spreadsheet": ["spreadsheet", "excel", "csv processing", "sheets"],
        "email": ["email", "smtp", "mail api"],
        "storage": ["s3", "cloud storage", "blob storage"],
    }

    detected = []
    mcp_required = []
    text_lower = requirements_text.lower()

    for tech, keywords in patterns.items():
        if any(kw in text_lower for kw in keywords):
            detected.append(tech)

    for mcp, keywords in mcp_patterns.items():
        if any(kw in text_lower for kw in keywords):
            mcp_required.append(mcp)

    return {
        "technologies": detected,
        "mcp_integrations": mcp_required,
        "requires_code_execution": len(mcp_required) > 0
    }
```

### 2. Map Technologies to Skills

| Technology | Required Skill | MCP Pattern |
|------------|---------------|-------------|
| fastapi | `fastapi-generator` | No |
| nextjs | `nextjs-generator` | No |
| express | `express-generator` | No |
| postgresql | `postgres-setup` | No |
| mongodb | `mongodb-setup` | No |
| kafka | `kafka-setup` | No |
| graphql | `graphql-generator` | No |
| docker | `docker-generator` | No |
| kubernetes | `k8s-generator` | No |
| github-actions | `ci-cd-generator` | No |
| google-drive | `gdrive-integration` | **YES** |
| salesforce | `salesforce-integration` | **YES** |
| slack | `slack-integration` | **YES** |
| spreadsheet | `spreadsheet-processor` | **YES** |
| database-query | `data-extractor` | **YES** |

### 3. Check Existing Skills

```python
def check_existing_skills(required_skills: list) -> dict:
    """Check which skills exist and which are missing."""

    existing = []
    missing = []

    for skill in required_skills:
        skill_path = f".claude/skills/{skill}/SKILL.md"
        if Path(skill_path).exists():
            existing.append(skill)
        else:
            missing.append(skill)

    return {"existing": existing, "missing": missing}
```

### 4. Detect MCP Pattern Requirements

```python
def requires_mcp_pattern(skill_name: str, requirements: dict) -> bool:
    """Determine if a skill needs MCP Code Execution pattern."""

    mcp_skill_patterns = [
        "integration", "connector", "api-client",
        "extractor", "processor", "sync"
    ]

    # Check if skill name suggests MCP usage
    if any(p in skill_name for p in mcp_skill_patterns):
        return True

    # Check if requirements mention external APIs
    mcp_keywords = [
        "external api", "third-party", "integration",
        "fetch data", "sync data", "import from",
        "export to", "connect to"
    ]

    req_text = str(requirements).lower()
    return any(kw in req_text for kw in mcp_keywords)
```

### 5. Auto-Create Missing Skills

For each missing skill, generate using appropriate template:

**Standard Skill Template:**
```markdown
---
name: {skill-name}
description: |
  {Description}. Triggers: {keywords}
version: 1.0.0
---

# {Skill Title}

## Workflow
1. {Step 1}
2. {Step 2}

## Code Templates
...
```

**MCP Code Execution Skill Template:**
```markdown
---
name: {skill-name}
description: |
  {Description}. Uses MCP Code Execution for 98% token efficiency.
  Triggers: {keywords}
version: 1.0.0
mcp-pattern: code-execution
---

# {Skill Title}

## MCP Servers Used
- `{server}`: {tools}

## Execution Pattern

This skill uses **MCP Code Execution**:
1. Agent writes code to `./workspace/task.ts`
2. Code calls MCP tools in execution environment
3. Only final summary returns to model

## Directory Structure
\`\`\`
{skill-name}/
├── SKILL.md
├── servers/
│   └── {server-name}/
│       ├── index.ts
│       └── {tool}.ts
├── scripts/
│   └── execute.py
└── workspace/
\`\`\`

## Progressive Disclosure
\`\`\`bash
ls ./servers/                    # List MCP servers
ls ./servers/{server}/           # List tools
cat ./servers/{server}/{tool}.ts # Read definition
\`\`\`

## Code Template
\`\`\`typescript
import * as server from './servers/{server}';

async function main() {
  const data = await server.{tool}({ ... });
  const filtered = data.filter(item => item.relevant);
  console.log(\`Processed \${filtered.length} items\`);
}
main();
\`\`\`

## Validation
- [ ] Code executes outside model context
- [ ] Only summary returned (~100 tokens)
- [ ] Large data processed in execution env
```

### 6. Output

Generate report:

```json
{
  "analyzed_requirements": "path/to/requirements.md",
  "technologies_detected": ["fastapi", "postgresql", "kafka"],
  "mcp_integrations_detected": ["google-drive", "salesforce"],
  "skills_required": [
    {"name": "fastapi-generator", "mcp_pattern": false},
    {"name": "gdrive-integration", "mcp_pattern": true}
  ],
  "skills_existing": ["fastapi-generator"],
  "skills_created": [
    {"name": "postgres-setup", "mcp_pattern": false},
    {"name": "gdrive-integration", "mcp_pattern": true}
  ],
  "mcp_pattern_enforced": true,
  "ready_to_build": true
}
```

## MCP Pattern Enforcement Rules

When generating skills that use external tools/APIs:

1. **MUST use Code Execution pattern** if:
   - Skill fetches large documents/datasets
   - Skill chains multiple API calls
   - Skill processes external data

2. **Skill structure MUST include**:
   - `servers/` directory with tool wrappers
   - `workspace/` for intermediate files
   - Progressive disclosure (load tools on-demand)

3. **Generated code MUST**:
   - Run outside model context
   - Filter/aggregate before returning
   - Return only summaries (~100 tokens)

4. **SKILL.md MUST include**:
   - `mcp-pattern: code-execution` in frontmatter
   - Tool discovery commands
   - Code template with console.log for results

## Token Efficiency Targets

| Skill Type | Max Tokens |
|------------|------------|
| Standard skill | 500 |
| MCP skill (code execution) | 200 |
| Tool discovery | 100 |
| Result summary | 100 |
