---
name: compact
description: Compact current session memory into structured text for session recovery. Supports custom descriptions and tagging.
argument-hint: "[--description=\"...\"] [--tags=<tag1,tag2>] [--force]"
---

# Memory Compact Command (/memory:compact)

## 1. Overview

The `memory:compact` command **compresses current session working memory** into structured text optimized for **session recovery**, extracts critical information, and saves it to persistent storage via MCP `core_memory` tool.

**Core Philosophy**:
- **Session Recovery First**: Capture everything needed to resume work seamlessly
- **Minimize Re-exploration**: Include file paths, decisions, and state to avoid redundant analysis
- **Preserve Train of Thought**: Keep notes and hypotheses for complex debugging
- **Actionable State**: Record last action result and known issues

## 2. Parameters

- `--description`: Custom session description (optional)
  - Example: "completed core-memory module"
  - Example: "debugging JWT refresh - suspected memory leak"
- `--tags`: Comma-separated tags for categorization (optional)
- `--force`: Skip confirmation, save directly

## 3. Structured Output Format

```markdown
## Session ID
[WFS-ID if workflow session active, otherwise (none)]

## Project Root
[Absolute path to project root, e.g., D:\Claude_dms3]

## Objective
[High-level goal - the "North Star" of this session]

## Execution Plan
[CRITICAL: Embed the LATEST plan in its COMPLETE and DETAILED form]

### Source: [workflow | todo | user-stated | inferred]

<details>
<summary>Full Execution Plan (Click to expand)</summary>

[PRESERVE COMPLETE PLAN VERBATIM - DO NOT SUMMARIZE]
- ALL phases, tasks, subtasks
- ALL file paths (absolute)
- ALL dependencies and prerequisites
- ALL acceptance criteria
- ALL status markers ([x] done, [ ] pending)
- ALL notes and context

Example:
## Phase 1: Setup
- [x] Initialize project structure
  - Created D:\Claude_dms3\src\core\index.ts
  - Added dependencies: lodash, zod
- [ ] Configure TypeScript
  - Update tsconfig.json for strict mode

## Phase 2: Implementation
- [ ] Implement core API
  - Target: D:\Claude_dms3\src\api\handler.ts
  - Dependencies: Phase 1 complete
  - Acceptance: All tests pass

</details>

## Working Files (Modified)
[Absolute paths to actively modified files]
- D:\Claude_dms3\src\file1.ts (role: main implementation)
- D:\Claude_dms3\tests\file1.test.ts (role: unit tests)

## Reference Files (Read-Only)
[Absolute paths to context files - NOT modified but essential for understanding]
- D:\Claude_dms3\.claude\CLAUDE.md (role: project instructions)
- D:\Claude_dms3\src\types\index.ts (role: type definitions)
- D:\Claude_dms3\package.json (role: dependencies)

## Last Action
[Last significant action and its result/status]

## Decisions
- [Decision]: [Reasoning]
- [Decision]: [Reasoning]

## Constraints
- [User-specified limitation or preference]

## Dependencies
- [Added/changed packages or environment requirements]

## Known Issues
- [Deferred bug or edge case]

## Changes Made
- [Completed modification]

## Pending
- [Next step] or (none)

## Notes
[Unstructured thoughts, hypotheses, debugging trails]
```

## 4. Field Definitions

| Field | Purpose | Recovery Value |
|-------|---------|----------------|
| **Session ID** | Workflow session identifier (WFS-*) | Links memory to specific stateful task execution |
| **Project Root** | Absolute path to project directory | Enables correct path resolution in new sessions |
| **Objective** | Ultimate goal of the session | Prevents losing track of broader feature |
| **Execution Plan** | Complete plan from any source (verbatim) | Preserves full planning context, avoids re-planning |
| **Working Files** | Actively modified files (absolute paths) | Immediately identifies where work was happening |
| **Reference Files** | Read-only context files (absolute paths) | Eliminates re-exploration for critical context |
| **Last Action** | Final tool output/status | Immediate state awareness (success/failure) |
| **Decisions** | Architectural choices + reasoning | Prevents re-litigating settled decisions |
| **Constraints** | User-imposed limitations | Maintains personalized coding style |
| **Dependencies** | Package/environment changes | Prevents missing dependency errors |
| **Known Issues** | Deferred bugs/edge cases | Ensures issues aren't forgotten |
| **Changes Made** | Completed modifications | Clear record of what was done |
| **Pending** | Next steps | Immediate action items |
| **Notes** | Hypotheses, debugging trails | Preserves "train of thought" |

## 5. Execution Flow

### Step 1: Analyze Current Session

Extract the following from conversation history:

```javascript
const sessionAnalysis = {
  sessionId: "",       // WFS-* if workflow session active, null otherwise
  projectRoot: "",     // Absolute path: D:\Claude_dms3
  objective: "",       // High-level goal (1-2 sentences)
  executionPlan: {
    source: "workflow" | "todo" | "user-stated" | "inferred",
    content: ""        // Full plan content - ALWAYS preserve COMPLETE and DETAILED form
  },
  workingFiles: [],    // {absolutePath, role} - modified files
  referenceFiles: [],  // {absolutePath, role} - read-only context files
  lastAction: "",      // Last significant action + result
  decisions: [],       // {decision, reasoning}
  constraints: [],     // User-specified limitations
  dependencies: [],    // Added/changed packages
  knownIssues: [],     // Deferred bugs
  changesMade: [],     // Completed modifications
  pending: [],         // Next steps
  notes: ""            // Unstructured thoughts
}
```

### Step 2: Generate Structured Text

```javascript
// Helper: Generate execution plan section
const generateExecutionPlan = (plan) => {
  const sourceLabels = {
    'workflow': 'workflow (IMPL_PLAN.md)',
    'todo': 'todo (TodoWrite)',
    'user-stated': 'user-stated',
    'inferred': 'inferred'
  };

  // CRITICAL: Preserve complete plan content verbatim - DO NOT summarize
  return `### Source: ${sourceLabels[plan.source] || plan.source}

<details>
<summary>Full Execution Plan (Click to expand)</summary>

${plan.content}

</details>`;
};

const structuredText = `## Session ID
${sessionAnalysis.sessionId || '(none)'}

## Project Root
${sessionAnalysis.projectRoot}

## Objective
${sessionAnalysis.objective}

## Execution Plan
${generateExecutionPlan(sessionAnalysis.executionPlan)}

## Working Files (Modified)
${sessionAnalysis.workingFiles.map(f => `- ${f.absolutePath} (role: ${f.role})`).join('\n') || '(none)'}

## Reference Files (Read-Only)
${sessionAnalysis.referenceFiles.map(f => `- ${f.absolutePath} (role: ${f.role})`).join('\n') || '(none)'}

## Last Action
${sessionAnalysis.lastAction}

## Decisions
${sessionAnalysis.decisions.map(d => `- ${d.decision}: ${d.reasoning}`).join('\n') || '(none)'}

## Constraints
${sessionAnalysis.constraints.map(c => `- ${c}`).join('\n') || '(none)'}

## Dependencies
${sessionAnalysis.dependencies.map(d => `- ${d}`).join('\n') || '(none)'}

## Known Issues
${sessionAnalysis.knownIssues.map(i => `- ${i}`).join('\n') || '(none)'}

## Changes Made
${sessionAnalysis.changesMade.map(c => `- ${c}`).join('\n') || '(none)'}

## Pending
${sessionAnalysis.pending.length > 0
  ? sessionAnalysis.pending.map(p => `- ${p}`).join('\n')
  : '(none)'}

## Notes
${sessionAnalysis.notes || '(none)'}`
```

### Step 3: Import to Core Memory via MCP

Use the MCP `core_memory` tool to save the structured text:

```javascript
mcp__ccw-tools__core_memory({
  operation: "import",
  text: structuredText
})
```

Or via CLI (pipe structured text to import):

```bash
# Write structured text to temp file, then import
echo "$structuredText" | ccw core-memory import

# Or from a file
ccw core-memory import --file /path/to/session-memory.md
```

**Response Format**:
```json
{
  "operation": "import",
  "id": "CMEM-YYYYMMDD-HHMMSS",
  "message": "Created memory: CMEM-YYYYMMDD-HHMMSS"
}
```

### Step 4: Report Recovery ID

After successful import, **clearly display the Recovery ID** to the user:

```
╔════════════════════════════════════════════════════════════════════════════╗
║  ✓ Session Memory Saved                                                    ║
║                                                                            ║
║  Recovery ID: CMEM-YYYYMMDD-HHMMSS                                         ║
║                                                                            ║
║  To restore: "Please import memory <ID>"                                   ║
║  (MCP: core_memory export | CLI: ccw core-memory export --id <ID>)         ║
╚════════════════════════════════════════════════════════════════════════════╝
```

## 6. Quality Checklist

Before generating:
- [ ] Session ID captured if workflow session active (WFS-*)
- [ ] Project Root is absolute path (e.g., D:\Claude_dms3)
- [ ] Objective clearly states the "North Star" goal
- [ ] Execution Plan: COMPLETE plan preserved VERBATIM (no summarization)
- [ ] Plan Source: Clearly identified (workflow | todo | user-stated | inferred)
- [ ] Plan Details: ALL phases, tasks, file paths, dependencies, status markers included
- [ ] All file paths are ABSOLUTE (not relative)
- [ ] Working Files: 3-8 modified files with roles
- [ ] Reference Files: Key context files (CLAUDE.md, types, configs)
- [ ] Last Action captures final state (success/failure)
- [ ] Decisions include reasoning, not just choices
- [ ] Known Issues separates deferred from forgotten bugs
- [ ] Notes preserve debugging hypotheses if any

## 7. Path Resolution Rules

### Project Root Detection
1. Check current working directory from environment
2. Look for project markers: `.git/`, `package.json`, `.claude/`
3. Use the topmost directory containing these markers

### Absolute Path Conversion
```javascript
// Convert relative to absolute
const toAbsolutePath = (relativePath, projectRoot) => {
  if (path.isAbsolute(relativePath)) return relativePath;
  return path.join(projectRoot, relativePath);
};

// Example: "src/api/auth.ts" → "D:\Claude_dms3\src\api\auth.ts"
```

### Reference File Categories
| Category | Examples | Priority |
|----------|----------|----------|
| Project Config | `.claude/CLAUDE.md`, `package.json`, `tsconfig.json` | High |
| Type Definitions | `src/types/*.ts`, `*.d.ts` | High |
| Related Modules | Parent/sibling modules with shared interfaces | Medium |
| Test Files | Corresponding test files for modified code | Medium |
| Documentation | `README.md`, `ARCHITECTURE.md` | Low |

## 8. Plan Detection (Priority Order)

### Priority 1: Workflow Session (IMPL_PLAN.md)
```javascript
// Check for active workflow session
const manifest = await mcp__ccw-tools__session_manager({
  operation: "list",
  location: "active"
});

if (manifest.sessions?.length > 0) {
  const session = manifest.sessions[0];
  const plan = await mcp__ccw-tools__session_manager({
    operation: "read",
    session_id: session.id,
    content_type: "plan"
  });
  sessionAnalysis.sessionId = session.id;
  sessionAnalysis.executionPlan.source = "workflow";
  sessionAnalysis.executionPlan.content = plan.content;
}
```

### Priority 2: TodoWrite (Current Session Todos)
```javascript
// Extract from conversation - look for TodoWrite tool calls
// Preserve COMPLETE todo list with all details
const todos = extractTodosFromConversation();
if (todos.length > 0) {
  sessionAnalysis.executionPlan.source = "todo";
  // Format todos with full context - preserve status markers
  sessionAnalysis.executionPlan.content = todos.map(t =>
    `- [${t.status === 'completed' ? 'x' : t.status === 'in_progress' ? '>' : ' '}] ${t.content}`
  ).join('\n');
}
```

### Priority 3: User-Stated Plan
```javascript
// Look for explicit plan statements in user messages:
// - "Here's my plan: 1. ... 2. ... 3. ..."
// - "I want to: first..., then..., finally..."
// - Numbered or bulleted lists describing steps
const userPlan = extractUserStatedPlan();
if (userPlan) {
  sessionAnalysis.executionPlan.source = "user-stated";
  sessionAnalysis.executionPlan.content = userPlan;
}
```

### Priority 4: Inferred Plan
```javascript
// If no explicit plan, infer from:
// - Task description and breakdown discussion
// - Sequence of actions taken
// - Outstanding work mentioned
const inferredPlan = inferPlanFromDiscussion();
if (inferredPlan) {
  sessionAnalysis.executionPlan.source = "inferred";
  sessionAnalysis.executionPlan.content = inferredPlan;
}
```

## 9. Notes

- **Timing**: Execute at task completion or before context switch
- **Frequency**: Once per independent task or milestone
- **Recovery**: New session can immediately continue with full context
- **Knowledge Graph**: Entity relationships auto-extracted for visualization
- **Absolute Paths**: Critical for cross-session recovery on different machines
