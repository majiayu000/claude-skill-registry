---
name: cross-plugin-detective
description: Integration guide for using detective skills across plugins. Maps agent roles from frontend, bun, and other plugins to appropriate detective skills. Developer agents should use developer-detective, architect agents should use architect-detective, etc.
allowed-tools: Bash, Task, Read, AskUserQuestion
---

# Cross-Plugin Detective Integration

**Version:** 1.0.0
**Purpose:** Connect ANY agent to the appropriate detective skill based on role

## ⛔ CORE PRINCIPLE: INDEXED MEMORY ONLY

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ALL DETECTIVE SKILLS USE claudemem (INDEXED MEMORY) EXCLUSIVELY            ║
║                                                                              ║
║   When ANY agent references a detective skill, they MUST:                    ║
║   ❌ NEVER use grep, find, rg, Glob tool, Grep tool                         ║
║   ✅ ALWAYS use claudemem search "query"                                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## Agent-to-Skill Mapping

### Frontend Plugin Agents

| Agent | Should Use Skill | Purpose |
|-------|-----------------|---------|
| `typescript-frontend-dev` | `code-analysis:developer-detective` | Find implementations, trace data flow |
| `frontend-architect` | `code-analysis:architect-detective` | Analyze architecture, design patterns |
| `test-architect` | `code-analysis:tester-detective` | Coverage analysis, test quality |
| `senior-code-reviewer` | `code-analysis:ultrathink-detective` | Comprehensive code review |
| `ui-developer` | `code-analysis:developer-detective` | Find UI implementations |
| `designer` | `code-analysis:architect-detective` | Understand component structure |
| `plan-reviewer` | `code-analysis:architect-detective` | Review architecture plans |

### Bun Backend Plugin Agents

| Agent | Should Use Skill | Purpose |
|-------|-----------------|---------|
| `backend-developer` | `code-analysis:developer-detective` | Find implementations, trace data flow |
| `api-architect` | `code-analysis:architect-detective` | API architecture analysis |
| `apidog` | `code-analysis:developer-detective` | Find API implementations |

### Code Analysis Plugin Agents

| Agent | Should Use Skill | Purpose |
|-------|-----------------|---------|
| `codebase-detective` | All detective skills | Full investigation capability |

### Any Other Plugin

| Agent Role | Should Use Skill |
|------------|-----------------|
| Any "developer" agent | `code-analysis:developer-detective` |
| Any "architect" agent | `code-analysis:architect-detective` |
| Any "tester" agent | `code-analysis:tester-detective` |
| Any "reviewer" agent | `code-analysis:ultrathink-detective` |
| Any "debugger" agent | `code-analysis:debugger-detective` |

---

## How to Reference Skills in Agent Frontmatter

### Example: Developer Agent
```yaml
---
name: my-developer-agent
description: Implements features
skills: code-analysis:developer-detective
---

# My Developer Agent

When investigating code, use the developer-detective skill.
This gives you access to indexed memory search via claudemem.

## Investigation Pattern

Before implementing:
1. Check claudemem status: `claudemem status`
2. Search for related code: `claudemem search "feature I'm implementing"`
3. Read specific files from results
4. NEVER use grep or find for discovery
```

### Example: Architect Agent
```yaml
---
name: my-architect-agent
description: Designs architecture
skills: code-analysis:architect-detective
---

# My Architect Agent

When analyzing architecture, use the architect-detective skill.

## Architecture Discovery

1. Check claudemem status: `claudemem status`
2. Search for patterns: `claudemem search "service layer architecture"`
3. Map dependencies: `claudemem search "import dependency injection"`
4. NEVER use grep or find for discovery
```

### Example: Multi-Skill Agent
```yaml
---
name: comprehensive-reviewer
description: Reviews all aspects
skills: code-analysis:ultrathink-detective, code-analysis:tester-detective
---
```

---

## Skill Selection Decision Tree

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     WHICH DETECTIVE SKILL TO USE?                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  What is the agent's PRIMARY focus?                                         │
│                                                                             │
│  ├── IMPLEMENTING code / Finding where to change                            │
│  │   └── Use: developer-detective                                           │
│  │                                                                          │
│  ├── DESIGNING architecture / Understanding patterns                        │
│  │   └── Use: architect-detective                                           │
│  │                                                                          │
│  ├── TESTING / Coverage analysis / Quality                                  │
│  │   └── Use: tester-detective                                              │
│  │                                                                          │
│  ├── DEBUGGING / Finding root cause                                         │
│  │   └── Use: debugger-detective                                            │
│  │                                                                          │
│  └── COMPREHENSIVE analysis / Technical debt / Audit                        │
│      └── Use: ultrathink-detective                                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Integration Examples

### Example 1: Frontend Developer Agent Needing to Find Code

```typescript
// In frontend plugin's typescript-frontend-dev agent:

// ❌ WRONG - Never do this
Grep({ pattern: "UserService", type: "ts" });
Glob({ pattern: "**/user*.ts" });

// ✅ CORRECT - Use indexed memory via developer-detective skill
// The skill teaches the agent to use:
claudemem search "UserService implementation methods"
```

### Example 2: Backend Architect Analyzing API Structure

```typescript
// In bun plugin's api-architect agent:

// ❌ WRONG - Never do this
find . -name "*.controller.ts"
grep -r "router\." . --include="*.ts"

// ✅ CORRECT - Use indexed memory via architect-detective skill
claudemem search "API controller endpoint handler"
claudemem search "router pattern REST GraphQL"
```

### Example 3: Test Architect Finding Coverage Gaps

```typescript
// In frontend plugin's test-architect agent:

// ❌ WRONG - Never do this
Glob({ pattern: "**/*.test.ts" });
Grep({ pattern: "describe" });

// ✅ CORRECT - Use indexed memory via tester-detective skill
claudemem search "test coverage describe spec"
claudemem search "mock stub test assertion"
```

---

## Skill Inheritance Pattern

When an agent needs code investigation, it should:

1. **Reference the appropriate detective skill in frontmatter**
2. **Follow the skill's INDEXED MEMORY ONLY requirement**
3. **Use claudemem for ALL code discovery**
4. **NEVER fall back to grep/find/Glob/Grep tools**

```yaml
---
name: any-agent-that-needs-investigation
skills: code-analysis:developer-detective  # or architect/tester/debugger/ultrathink
---

# This agent inherits:
# - INDEXED MEMORY requirement (claudemem only)
# - Role-specific search patterns
# - Output format guidance
# - FORBIDDEN: grep, find, Glob, Grep tools
```

---

## Plugin Dependencies

If your plugin has agents that need code investigation, add this dependency:

```json
{
  "name": "your-plugin",
  "dependencies": {
    "code-analysis@mag-claude-plugins": "^1.6.0"
  }
}
```

This ensures:
- claudemem skills are available
- Detective skills are accessible via `code-analysis:*` prefix
- Agents can reference skills in frontmatter

---

## Summary: The Golden Rule

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ANY AGENT + CODE INVESTIGATION = claudemem ONLY                            ║
║                                                                              ║
║   Developer agents → code-analysis:developer-detective                       ║
║   Architect agents → code-analysis:architect-detective                       ║
║   Tester agents    → code-analysis:tester-detective                          ║
║   Debugger agents  → code-analysis:debugger-detective                        ║
║   Reviewer agents  → code-analysis:ultrathink-detective                      ║
║                                                                              ║
║   grep/find/Glob/Grep = FORBIDDEN (always, everywhere, no exceptions)        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

**Maintained by:** MadAppGang
**Plugin:** code-analysis
**Last Updated:** December 2025
