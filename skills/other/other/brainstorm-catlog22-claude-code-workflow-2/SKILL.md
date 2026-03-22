---
name: brainstorm
description: |
  Dual-mode brainstorming pipeline. Auto mode: framework generation → parallel role analysis
  (spawn_agents_on_csv) → cross-role synthesis. Single role mode: individual role analysis.
  CSV-driven parallel coordination with NDJSON discovery board.
argument-hint: "[-y|--yes] [--count N] [--session ID] [--skip-questions] [--style-skill PKG] \"topic\" | <role-name> [--session ID]"
allowed-tools: spawn_agents_on_csv, spawn_agent, wait, send_input, close_agent, AskUserQuestion, Read, Write, Edit, Bash, Glob, Grep
---

## Auto Mode

When `--yes` or `-y`: Auto-select auto mode, auto-select recommended roles, skip all clarification questions, use defaults.

# Brainstorm

## Usage

```bash
$brainstorm "Build real-time collaboration platform" --count 3
$brainstorm -y "Design payment system" --count 5
$brainstorm "Build notification system" --style-skill material-design
$brainstorm system-architect --session WFS-xxx
$brainstorm ux-expert --include-questions
```

**Flags**:
- `-y, --yes`: Skip all confirmations (auto mode)
- `--count N`: Number of roles to select (default: 3, max: 9)
- `--session ID`: Use existing session
- `--skip-questions / --include-questions`: Control interactive Q&A per role
- `--style-skill PKG`: Style skill package for ui-designer
- `--update`: Update existing role analysis

---

## Overview

Dual-mode brainstorming with CSV-driven parallel role analysis. Auto mode runs a full pipeline; single role mode runs one role analysis independently.

```
┌──────────────────────────────────────────────────────────────────┐
│                    BRAINSTORM PIPELINE                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Phase 1: Mode Detection & Routing                                │
│     ├─ Parse flags and arguments                                  │
│     └─ Route to Auto Mode or Single Role Mode                    │
│                                                                    │
│  ═══ Auto Mode ═══                                                │
│                                                                    │
│  Phase 2: Interactive Framework Generation                        │
│     ├─ Context collection → Topic analysis → Role selection       │
│     ├─ Generate guidance-specification.md                         │
│     ├─ Generate roles.csv (1 row per selected role)              │
│     └─ User validates (skip if -y)                               │
│                                                                    │
│  Phase 3: Wave Role Analysis (spawn_agents_on_csv)               │
│     ├─ spawn_agents_on_csv(role instruction template)            │
│     ├─ Each role agent produces analysis.md + sub-documents      │
│     └─ discoveries.ndjson shared across role agents              │
│                                                                    │
│  Phase 4: Synthesis Integration                                   │
│     ├─ Read all role analyses (read-only)                        │
│     ├─ Cross-role analysis → conflict detection                  │
│     ├─ Feature spec generation                                    │
│     └─ Output: feature-specs/ + feature-index.json               │
│                                                                    │
│  ═══ Single Role Mode ═══                                         │
│                                                                    │
│  Phase 3S: Single Role Analysis (spawn_agent)                    │
│     ├─ spawn_agent(conceptual-planning-agent)                    │
│     └─ Output: {role}/analysis*.md                               │
│                                                                    │
└──────────────────────────────────────────────────────────────────┘
```

---

## Context Flow

```
roles.csv                      feature-specs/
┌──────────────┐              ┌──────────────────┐
│ R1: sys-arch │──findings───→│ F-001-auth.md    │
│ analysis.md  │              │ (cross-role spec) │
├──────────────┤              ├──────────────────┤
│ R2: ui-design│──findings───→│ F-002-ui.md      │
│ analysis.md  │              │ (cross-role spec) │
├──────────────┤              ├──────────────────┤
│ R3: test-str │──findings───→│ F-003-test.md    │
│ analysis.md  │              │ (cross-role spec) │
└──────────────┘              └──────────────────┘

Two context channels:
1. Directed: role findings → synthesis → feature specs
2. Broadcast: discoveries.ndjson (append-only shared board)
```

---

## CSV Schema

### roles.csv

```csv
id,role,title,focus,deps,wave,status,findings,output_files,error
"R1","system-architect","系统架构师","Technical architecture, scalability","","1","pending","","",""
"R2","ui-designer","UI设计师","Visual design, mockups","","1","pending","","",""
"R3","test-strategist","测试策略师","Test strategy, quality","","1","pending","","",""
```

**Columns**:

| Column | Phase | Description |
|--------|-------|-------------|
| `id` | Input | Role ID: R1, R2, ... |
| `role` | Input | Role identifier (e.g., system-architect) |
| `title` | Input | Role display title |
| `focus` | Input | Role focus areas and keywords |
| `deps` | Input | Dependency IDs (usually empty — all wave 1) |
| `wave` | Computed | Wave number (usually 1 for all roles) |
| `status` | Output | `pending` → `completed` / `failed` |
| `findings` | Output | Key discoveries (max 800 chars) |
| `output_files` | Output | Generated analysis files (semicolon-separated) |
| `error` | Output | Error message if failed |

---

## Available Roles

| Role ID | Title | Focus Area |
|---------|-------|------------|
| `data-architect` | 数据架构师 | Data models, storage strategies, data flow |
| `product-manager` | 产品经理 | Product strategy, roadmap, prioritization |
| `product-owner` | 产品负责人 | Backlog management, user stories, acceptance criteria |
| `scrum-master` | 敏捷教练 | Process facilitation, impediment removal |
| `subject-matter-expert` | 领域专家 | Domain knowledge, business rules, compliance |
| `system-architect` | 系统架构师 | Technical architecture, scalability, integration |
| `test-strategist` | 测试策略师 | Test strategy, quality assurance |
| `ui-designer` | UI设计师 | Visual design, mockups, design systems |
| `ux-expert` | UX专家 | User research, information architecture, journey |

---

## Session Structure

```
.workflow/active/WFS-{topic}/
├── workflow-session.json              # Session metadata
├── .process/
│   └── context-package.json           # Phase 0 context
├── roles.csv                          # Role analysis state (Phase 2-3)
├── discoveries.ndjson                 # Shared discovery board
└── .brainstorming/
    ├── guidance-specification.md      # Framework (Phase 2)
    ├── feature-index.json             # Feature index (Phase 4)
    ├── synthesis-changelog.md         # Synthesis audit trail (Phase 4)
    ├── feature-specs/                 # Feature specs (Phase 4)
    │   ├── F-001-{slug}.md
    │   └── F-00N-{slug}.md
    └── {role}/                        # Role analyses (Phase 3, immutable)
        ├── {role}-context.md          # Interactive Q&A
        ├── analysis.md                # Main/index document
        ├── analysis-cross-cutting.md  # Cross-feature
        └── analysis-F-{id}-{slug}.md  # Per-feature
```

---

## Implementation

### Session Initialization

```javascript
const getUtc8ISOString = () => new Date(Date.now() + 8 * 60 * 60 * 1000).toISOString()

// Parse flags
const AUTO_YES = $ARGUMENTS.includes('--yes') || $ARGUMENTS.includes('-y')
const countMatch = $ARGUMENTS.match(/--count\s+(\d+)/)
const roleCount = countMatch ? Math.min(parseInt(countMatch[1]), 9) : 3
const sessionMatch = $ARGUMENTS.match(/--session\s+(\S+)/)
const existingSessionId = sessionMatch ? sessionMatch[1] : null
const skipQuestions = $ARGUMENTS.includes('--skip-questions')
const includeQuestions = $ARGUMENTS.includes('--include-questions')
const styleSkillMatch = $ARGUMENTS.match(/--style-skill\s+(\S+)/)
const styleSkill = styleSkillMatch ? styleSkillMatch[1] : null
const updateMode = $ARGUMENTS.includes('--update')

// Role detection
const VALID_ROLES = [
  'data-architect', 'product-manager', 'product-owner', 'scrum-master',
  'subject-matter-expert', 'system-architect', 'test-strategist',
  'ui-designer', 'ux-expert'
]
const cleanArgs = $ARGUMENTS
  .replace(/--yes|-y|--count\s+\d+|--session\s+\S+|--skip-questions|--include-questions|--style-skill\s+\S+|--update/g, '')
  .trim()
const firstArg = cleanArgs.split(/\s+/)[0]
const isRole = VALID_ROLES.includes(firstArg)

// Mode detection
let executionMode
if (AUTO_YES) {
  executionMode = 'auto'
} else if (isRole) {
  executionMode = 'single-role'
} else if (cleanArgs) {
  executionMode = 'auto'
} else {
  executionMode = null  // Ask user
}

const topic = isRole
  ? cleanArgs.replace(firstArg, '').trim()
  : cleanArgs.replace(/^["']|["']$/g, '')
```

---

### Phase 1: Mode Detection & Routing

**Objective**: Parse arguments, determine execution mode, prepare session.

**Steps**:

1. **Detect Mode**

   ```javascript
   if (executionMode === null) {
     const modeAnswer = AskUserQuestion({
       questions: [{
         question: "Choose brainstorming mode:",
         header: "Mode",
         multiSelect: false,
         options: [
           { label: "Auto Mode (Recommended)", description: "Full pipeline: framework → parallel roles → synthesis" },
           { label: "Single Role", description: "Run one role analysis independently" }
         ]
       }]
     })
     executionMode = modeAnswer.Mode.startsWith('Auto') ? 'auto' : 'single-role'
   }
   ```

2. **Session Setup**

   ```javascript
   let sessionId, sessionFolder

   if (existingSessionId) {
     sessionId = existingSessionId
     sessionFolder = `.workflow/active/${sessionId}`
   } else if (executionMode === 'auto') {
     const slug = topic.toLowerCase().replace(/[^a-z0-9\u4e00-\u9fa5]+/g, '-').substring(0, 40)
     sessionId = `WFS-${slug}`
     sessionFolder = `.workflow/active/${sessionId}`
     Bash(`mkdir -p "${sessionFolder}/.brainstorming" "${sessionFolder}/.process"`)

     // Initialize workflow-session.json
     Write(`${sessionFolder}/workflow-session.json`, JSON.stringify({
       session_id: sessionId,
       topic: topic,
       status: 'brainstorming',
       execution_mode: executionMode,
       created_at: getUtc8ISOString()
     }, null, 2))
   } else {
     // Single role mode requires existing session
     const existing = Bash(`ls -d .workflow/active/WFS-* 2>/dev/null | head -1`).trim()
     if (!existing) {
       console.log('ERROR: No active session found. Run auto mode first to create a session.')
       return
     }
     sessionId = existing.split('/').pop()
     sessionFolder = existing
   }
   ```

**Route**:
- `executionMode === 'auto'` → Phase 2
- `executionMode === 'single-role'` → Phase 3S

---

### Phase 2: Interactive Framework Generation (Auto Mode)

**Objective**: Analyze topic, select roles, generate guidance-specification.md and roles.csv.

**Steps**:

1. **Analyze Topic & Select Roles**

   ```javascript
   Bash({
     command: `ccw cli -p "PURPOSE: Analyze brainstorming topic and recommend ${roleCount} expert roles for multi-perspective analysis. Success = well-matched roles with clear focus areas.
TASK:
  • Analyze topic domain, complexity, and key dimensions
  • Select ${roleCount} roles from: data-architect, product-manager, product-owner, scrum-master, subject-matter-expert, system-architect, test-strategist, ui-designer, ux-expert
  • For each role: define focus area, key questions, and analysis scope
  • Identify potential cross-role conflicts or synergies
  • Generate feature decomposition if topic has distinct components
MODE: analysis
CONTEXT: @**/*
EXPECTED: JSON: {analysis: {domain, complexity, dimensions[]}, roles: [{id, role, title, focus, key_questions[]}], features: [{id, title, description}]}
CONSTRAINTS: Select exactly ${roleCount} roles | Each role must have distinct perspective | Roles must cover topic comprehensively

TOPIC: ${topic}" --tool gemini --mode analysis --rule planning-breakdown-task-steps`,
     run_in_background: true
   })
   // Wait for CLI completion → { analysis, roles[], features[] }
   ```

2. **User Validation** (skip if AUTO_YES)

   ```javascript
   if (!AUTO_YES) {
     console.log(`\n## Brainstorm Framework\n`)
     console.log(`Topic: ${topic}`)
     console.log(`Domain: ${analysis.domain} | Complexity: ${analysis.complexity}`)
     console.log(`\nSelected Roles (${roles.length}):`)
     roles.forEach(r => console.log(`  - [${r.id}] ${r.title}: ${r.focus}`))
     if (features.length > 0) {
       console.log(`\nFeatures (${features.length}):`)
       features.forEach(f => console.log(`  - [${f.id}] ${f.title}`))
     }

     const answer = AskUserQuestion({
       questions: [{
         question: "Approve brainstorm framework?",
         header: "Validate",
         multiSelect: false,
         options: [
           { label: "Approve", description: "Proceed with role analysis" },
           { label: "Modify Roles", description: "Change role selection" },
           { label: "Cancel", description: "Abort" }
         ]
       }]
     })

     if (answer.Validate === "Cancel") return
     if (answer.Validate === "Modify Roles") {
       // Allow user to adjust via AskUserQuestion
       const roleAnswer = AskUserQuestion({
         questions: [{
           question: "Select roles for analysis:",
           header: "Roles",
           multiSelect: true,
           options: VALID_ROLES.map(r => ({
             label: r,
             description: roles.find(sel => sel.role === r)?.focus || ''
           }))
         }]
       })
       // Rebuild roles[] from selection
     }
   }
   ```

3. **Generate Guidance Specification**

   ```javascript
   const guidanceContent = `# Guidance Specification

## Topic
${topic}

## Analysis
- **Domain**: ${analysis.domain}
- **Complexity**: ${analysis.complexity}
- **Dimensions**: ${analysis.dimensions.join(', ')}

## Selected Roles
${roles.map(r => `### ${r.title} (${r.role})
- **Focus**: ${r.focus}
- **Key Questions**: ${r.key_questions.join('; ')}`).join('\n\n')}

## Features
${features.map(f => `- **[${f.id}] ${f.title}**: ${f.description}`).join('\n')}
`
   Write(`${sessionFolder}/.brainstorming/guidance-specification.md`, guidanceContent)
   ```

4. **Generate roles.csv**

   ```javascript
   const header = 'id,role,title,focus,deps,wave,status,findings,output_files,error'
   const rows = roles.map(r =>
     [r.id, r.role, r.title, r.focus, '', '1', 'pending', '', '', '']
       .map(v => `"${String(v).replace(/"/g, '""')}"`)
       .join(',')
   )
   Write(`${sessionFolder}/roles.csv`, [header, ...rows].join('\n'))
   ```

   Update workflow-session.json with selected_roles.

---

### Phase 3: Wave Role Analysis (spawn_agents_on_csv) — Auto Mode

**Objective**: Execute parallel role analysis via `spawn_agents_on_csv`. Each role agent produces analysis documents.

**Steps**:

1. **Role Analysis Wave**

   ```javascript
   const rolesCSV = parseCsv(Read(`${sessionFolder}/roles.csv`))

   console.log(`\n## Phase 3: Parallel Role Analysis (${rolesCSV.length} roles)\n`)

   spawn_agents_on_csv({
     csv_path: `${sessionFolder}/roles.csv`,
     id_column: "id",
     instruction: buildRoleInstruction(sessionFolder, topic, features),
     max_concurrency: Math.min(rolesCSV.length, 4),
     max_runtime_seconds: 600,
     output_csv_path: `${sessionFolder}/roles-results.csv`,
     output_schema: {
       type: "object",
       properties: {
         id: { type: "string" },
         status: { type: "string", enum: ["completed", "failed"] },
         findings: { type: "string" },
         output_files: { type: "array", items: { type: "string" } },
         error: { type: "string" }
       },
       required: ["id", "status", "findings"]
     }
   })

   // Merge results into roles.csv
   const roleResults = parseCsv(Read(`${sessionFolder}/roles-results.csv`))
   for (const result of roleResults) {
     updateMasterCsvRow(`${sessionFolder}/roles.csv`, result.id, {
       status: result.status,
       findings: result.findings || '',
       output_files: Array.isArray(result.output_files) ? result.output_files.join(';') : (result.output_files || ''),
       error: result.error || ''
     })
     console.log(`  [${result.id}] ${result.status === 'completed' ? '✓' : '✗'} ${rolesCSV.find(r => r.id === result.id)?.role}`)
   }

   Bash(`rm -f "${sessionFolder}/roles-results.csv"`)
   ```

2. **Role Instruction Template**

   ```javascript
   function buildRoleInstruction(sessionFolder, topic, features) {
     const featureList = features.length > 0
       ? features.map(f => `- [${f.id}] ${f.title}: ${f.description}`).join('\n')
       : 'No feature decomposition — analyze topic holistically.'

     return `
## ROLE ANALYSIS ASSIGNMENT

### MANDATORY FIRST STEPS
1. Read guidance specification: ${sessionFolder}/.brainstorming/guidance-specification.md
2. Read shared discoveries: ${sessionFolder}/discoveries.ndjson (if exists)
3. Read project context: .workflow/project-tech.json (if exists)

---

## Your Role

**Role ID**: {id}
**Role**: {role}
**Title**: {title}
**Focus**: {focus}

---

## Topic
${topic}

## Features to Analyze
${featureList}

---

## Analysis Protocol

1. **Read guidance**: Load guidance-specification.md for full context
2. **Read discoveries**: Load discoveries.ndjson for shared findings from other roles
3. **Analyze from your perspective**: Apply your role expertise to the topic
4. **Per-feature analysis** (if features exist):
   - Create \`${sessionFolder}/.brainstorming/{role}/analysis-{feature-id}-{slug}.md\` per feature
   - Create \`${sessionFolder}/.brainstorming/{role}/analysis-cross-cutting.md\` for cross-feature concerns
5. **Create index document**: \`${sessionFolder}/.brainstorming/{role}/analysis.md\`
   - Summary of all findings
   - Links to sub-documents
   - Key recommendations
6. **Share discoveries**: Append findings to shared board:
   \`\`\`bash
   echo '{"ts":"<ISO8601>","worker":"{id}","type":"<type>","data":{...}}' >> ${sessionFolder}/discoveries.ndjson
   \`\`\`
7. **Report result**: Return JSON via report_agent_job_result

### Document Constraints
- Main analysis.md: < 3000 words
- Sub-documents: < 2000 words each, max 5
- Total per role: < 15000 words

### Discovery Types to Share
- \`design_pattern\`: {name, rationale, applicability} — recommended patterns
- \`risk\`: {area, severity, mitigation} — identified risks
- \`requirement\`: {title, priority, source} — derived requirements
- \`constraint\`: {type, description, impact} — discovered constraints
- \`synergy\`: {roles[], area, description} — cross-role opportunities

---

## Output (report_agent_job_result)

Return JSON:
{
  "id": "{id}",
  "status": "completed" | "failed",
  "findings": "Key insights from {role} perspective (max 800 chars)",
  "output_files": ["path/to/analysis.md", "path/to/analysis-F-001.md"],
  "error": ""
}
`
   }
   ```

---

### Phase 3S: Single Role Analysis (spawn_agent) — Single Role Mode

**Objective**: Run one role analysis via spawn_agent with optional interactive Q&A.

```javascript
if (executionMode === 'single-role') {
  const roleName = firstArg
  const roleDir = `${sessionFolder}/.brainstorming/${roleName}`
  Bash(`mkdir -p "${roleDir}"`)

  const agentId = spawn_agent({
    agent: `~/.codex/agents/conceptual-planning-agent.md`,
    instruction: `
Perform a ${roleName} analysis for the brainstorming session.

**Session**: ${sessionFolder}
**Role**: ${roleName}
**Topic**: Read from ${sessionFolder}/.brainstorming/guidance-specification.md
${includeQuestions ? '**Mode**: Interactive — ask clarification questions before analysis' : ''}
${skipQuestions ? '**Mode**: Skip questions — proceed directly to analysis' : ''}
${styleSkill ? `**Style Skill**: ${styleSkill} — load .claude/skills/style-${styleSkill}/ for design reference` : ''}
${updateMode ? '**Update Mode**: Read existing analysis and enhance/update it' : ''}

**Output**: Create analysis documents in ${roleDir}/
- ${roleDir}/analysis.md (main index)
- ${roleDir}/analysis-*.md (sub-documents as needed)

Follow the same analysis protocol as wave role analysis but with interactive refinement.
`
  })

  wait({ id: agentId })
  close_agent({ id: agentId })

  console.log(`\n✓ ${roleName} analysis complete: ${roleDir}/analysis.md`)
}
```

---

### Phase 4: Synthesis Integration (Auto Mode)

**Objective**: Read all role analyses, cross-reference, generate feature specs.

**Steps**:

1. **Collect Role Findings**

   ```javascript
   const rolesCSV = parseCsv(Read(`${sessionFolder}/roles.csv`))
   const completedRoles = rolesCSV.filter(r => r.status === 'completed')

   // Read all analysis.md index files (optimized: skip sub-docs for token efficiency)
   const roleAnalyses = {}
   for (const role of completedRoles) {
     const indexPath = `${sessionFolder}/.brainstorming/${role.role}/analysis.md`
     const content = Read(indexPath)
     if (content) roleAnalyses[role.role] = content
   }

   // Read discoveries
   const discoveriesPath = `${sessionFolder}/discoveries.ndjson`
   const discoveries = Read(discoveriesPath) || ''
   ```

2. **Synthesis via Agent**

   ```javascript
   const synthesisAgent = spawn_agent({
     agent: `~/.codex/agents/conceptual-planning-agent.md`,
     instruction: `
## SYNTHESIS ASSIGNMENT

Synthesize ${completedRoles.length} role analyses into unified feature specifications.

**Session**: ${sessionFolder}
**Role Analyses**: ${completedRoles.map(r => `${sessionFolder}/.brainstorming/${r.role}/analysis.md`).join(', ')}
**Discoveries**: ${discoveriesPath}

### Synthesis Protocol

1. **Read all role analyses** (analysis.md files only — these are index documents)
2. **Cross-reference findings**: Identify agreements, conflicts, and unique insights
3. **Generate feature specs**: For each feature in guidance-specification.md:
   - Create ${sessionFolder}/.brainstorming/feature-specs/F-{id}-{slug}.md
   - Consolidate perspectives from all relevant roles
   - Note conflicts and recommended resolutions
4. **Generate feature index**: ${sessionFolder}/.brainstorming/feature-index.json
   - Array of {id, title, slug, roles_contributing[], conflict_count, priority}
5. **Generate changelog**: ${sessionFolder}/.brainstorming/synthesis-changelog.md
   - Decisions made, conflicts resolved, trade-offs accepted

### Complexity Assessment
Evaluate complexity score (0-8):
- Feature count (≤2: 0, 3-4: 1, ≥5: 2)
- Unresolved conflicts (0: 0, 1-2: 1, ≥3: 2)
- Participating roles (≤2: 0, 3-4: 1, ≥5: 2)
- Cross-feature dependencies (0: 0, 1-2: 1, ≥3: 2)

### Output Files
- feature-specs/F-{id}-{slug}.md (one per feature)
- feature-index.json
- synthesis-changelog.md
`
   })

   wait({ id: synthesisAgent })
   close_agent({ id: synthesisAgent })
   ```

3. **Completion Summary**

   ```javascript
   const featureIndex = JSON.parse(Read(`${sessionFolder}/.brainstorming/feature-index.json`) || '[]')

   console.log(`
## Brainstorm Complete

Session: ${sessionId}
Roles analyzed: ${completedRoles.length}
Features synthesized: ${featureIndex.length}

### Feature Specs
${featureIndex.map(f => `  - [${f.id}] ${f.title} (${f.roles_contributing?.length || 0} roles, ${f.conflict_count || 0} conflicts)`).join('\n')}

### Next Steps
- /workflow-plan --session ${sessionId}  → Generate implementation plan
- Review: ${sessionFolder}/.brainstorming/feature-specs/
   `)
   ```

---

## Utility Functions

### CSV Parser

```javascript
function parseCsv(content) {
  const lines = content.trim().split('\n')
  if (lines.length < 2) return []
  const headers = parseCSVLine(lines[0])
  return lines.slice(1).map(line => {
    const values = parseCSVLine(line)
    const row = {}
    headers.forEach((h, i) => row[h] = values[i] || '')
    return row
  })
}
```

### CSV Row Updater

```javascript
function updateMasterCsvRow(csvPath, id, updates) {
  const content = Read(csvPath)
  const lines = content.trim().split('\n')
  const headers = parseCSVLine(lines[0])
  const idIdx = headers.indexOf('id')

  for (let i = 1; i < lines.length; i++) {
    const values = parseCSVLine(lines[i])
    if (values[idIdx]?.replace(/"/g, '') === id) {
      Object.entries(updates).forEach(([key, val]) => {
        const idx = headers.indexOf(key)
        if (idx >= 0) values[idx] = `"${String(val).replace(/"/g, '""')}"`
      })
      lines[i] = values.join(',')
      break
    }
  }
  Write(csvPath, lines.join('\n'))
}
```

---

## Error Handling

| Error | Recovery |
|-------|----------|
| Invalid role name | Show valid roles list, prompt again |
| No active session (single role) | Guide user to run auto mode first |
| Role agent failure | Mark failed in roles.csv, continue with remaining |
| Synthesis overflow (>100KB) | Read only analysis.md index files |
| Context compression | Re-read guidance-specification.md and roles.csv |

---

## Compact Protection

> **COMPACT DIRECTIVE**: If context compression occurs mid-execution, re-read the current phase's state:
> - Phase 2: Re-read `guidance-specification.md`
> - Phase 3: Re-read `roles.csv` for progress state
> - Phase 4: Re-read `feature-index.json` and `roles.csv`
