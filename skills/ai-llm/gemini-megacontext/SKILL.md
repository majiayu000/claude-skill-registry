/*============================================================================*/
/* SKILL SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: SKILL
version: 1.0.0
description: |
  [assert|neutral] Analyze entire codebases with Gemini's 1 million token context window - process 30K lines at once [ground:given] [conf:0.95] [state:confirmed]
category: platforms
tags:
- gemini
- codebase-analysis
- architecture
- large-context
- multi-file
author: system
cognitive_frame:
  primary: compositional
  goal_analysis:
    first_order: "Execute SKILL workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic platforms processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "SKILL",
  category: "platforms",
  version: "1.0.0",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S1 COGNITIVE FRAME                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] COGNITIVE_FRAME := {
  frame: "Compositional",
  source: "German",
  force: "Build from primitives?"
} [ground:cognitive-science] [conf:0.92] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S2 TRIGGER CONDITIONS                                                       */
/*----------------------------------------------------------------------------*/

[define|neutral] TRIGGER_POSITIVE := {
  keywords: ["SKILL", "platforms", "workflow"],
  context: "user needs SKILL capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

# Gemini Mega-Context Skill

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



## Purpose
Leverage Gemini CLI's massive 1 million token context window to analyze entire codebases, architectural patterns, and multi-file dependencies in a single pass - something Claude Code's context window cannot achieve.

## Unique Capability
**What Claude Code Can't Do**: Claude Code has limited context window. Gemini 2.5 Pro can process up to 1 million tokens (~1,500 pages or 30,000 lines of code) simultaneously, enabling whole-codebase analysis without losing context.

## When to Use

### Perfect For:
✅ Analyzing entire project architecture
✅ Understanding multi-file dependencies across large codebases
✅ Refactoring that requires understanding the whole system
✅ Generating comprehensive documentation from full codebase
✅ Finding patterns and anti-patterns across all files
✅ Onboarding to unfamiliar large projects
✅ Security audits requiring full codebase awareness
✅ Migration planning (understand everything before changing)

### Don't Use When:
❌ Working with single file or small module (use Claude Code)
❌ Need complex problem-solving (Claude is better)
❌ Writing new features (Gemini gets stuck in loops per user feedback)
❌ Need iterative refinement (Gemini switches to Flash after 5 min)

## How It Works

This skill spawns a **Gemini Mega-Context Agent** that:
1. Uses `gemini --all-files` to load your entire codebase
2. Leverages 1M token context for comprehensive analysis
3. Returns architectural insights, dependency maps, or refactoring plans
4. Provides results back to Claude Code for user presentation

## Usage

### Basic Codebase Analysis
```
/gemini-megacontext
```

### With Specific Question
```
/gemini-megacontext "Explain the complete architecture and how all components interact"
```

### Detailed Analysis
```
/gemini-megacontext "Map all database queries across the entire codebase and identify N+1 patterns"
```

## Input Examples

```bash
# Architecture analysis
/gemini-megacontext "Document the full system architecture with component interactions"

# Dependency mapping
/gemini-megacontext "Create a dependency graph showing how all modules relate"

# Security audit
/gemini-megacontext "Identify all authentication and authorization patterns across the codebase"

# Migration planning
/gemini-megacontext "Analyze entire codebase for Python 2 to 3 migration requirements"

# Code patterns
/gemini-megacontext "Find all API endpoints and document their authentication methods"

# Refactoring scope
/gemini-megacontext "Identify all files that would need changes to rename User to Account"
```

## Output

The agent provides:
- **Architectural Overview**: How the system is structured
- **Component Interactions**: How pieces fit together
- **Dependency Map**: What depends on what
- **Pattern Analysis**: Common patterns and anti-patterns found
- **File References**: Specific locations with file:line citations
- **Recommendations**: Improvement suggestions based on full context

## Real-World Examples

### Example 1: Architecture Documentation
```
Task: "Document our microservices architecture"

Agent analyzes all services simultaneously and provides:
- Service dependency graph
- API contract documentation
- Database schema relationships
- Authentication flow across services
- Configuration management patterns
```

### Example 2: Refactoring Impact Analysis
```
Task: "If we change the User model, what breaks?"

Agent scans entire codebase and identifies:
- 47 files with direct User references
- 12 database migrations to update
- 8 API endpoints that return User data
- 15 frontend components displaying user info
- 3 background jobs processing users
```

### Example 3: Security Audit
```
Task: "Find all places where we handle sensitive data"

Agent reviews full codebase and reports:
- All database fields storing PII
- API endpoints exposing sensitive data
- Logging statements that might leak secrets
- File upload ha

/*----------------------------------------------------------------------------*/
/* S4 SUCCESS CRITERIA                                                         */
/*----------------------------------------------------------------------------*/

[define|neutral] SUCCESS_CRITERIA := {
  primary: "Skill execution completes successfully",
  quality: "Output meets quality thresholds",
  verification: "Results validated against requirements"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S5 MCP INTEGRATION                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] MCP_INTEGRATION := {
  memory_mcp: "Store execution results and patterns",
  tools: ["mcp__memory-mcp__memory_store", "mcp__memory-mcp__vector_search"]
} [ground:witnessed:mcp-config] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S6 MEMORY NAMESPACE                                                         */
/*----------------------------------------------------------------------------*/

[define|neutral] MEMORY_NAMESPACE := {
  pattern: "skills/platforms/SKILL/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "SKILL-{session_id}",
  WHEN: "ISO8601_timestamp",
  PROJECT: "{project_name}",
  WHY: "skill-execution"
} [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S7 SKILL COMPLETION VERIFICATION                                            */
/*----------------------------------------------------------------------------*/

[direct|emphatic] COMPLETION_CHECKLIST := {
  agent_spawning: "Spawn agents via Task()",
  registry_validation: "Use registry agents only",
  todowrite_called: "Track progress with TodoWrite",
  work_delegation: "Delegate to specialized agents"
} [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S8 ABSOLUTE RULES                                                           */
/*----------------------------------------------------------------------------*/

[direct|emphatic] RULE_NO_UNICODE := forall(output): NOT(unicode_outside_ascii) [ground:windows-compatibility] [conf:1.0] [state:confirmed]

[direct|emphatic] RULE_EVIDENCE := forall(claim): has(ground) AND has(confidence) [ground:verix-spec] [conf:1.0] [state:confirmed]

[direct|emphatic] RULE_REGISTRY := forall(agent): agent IN AGENT_REGISTRY [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>SKILL_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
