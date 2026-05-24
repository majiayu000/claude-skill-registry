/*============================================================================*/
/* CODE-FORMATTER SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: code-formatter
version: 1.0.0
description: |
  [assert|neutral] Automatically format code files using the appropriate formatter based on file type, providing clear feedback on changes made [ground:given] [conf:0.95] [state:confirmed]
category: foundry
tags:
- foundry
- creation
- meta-tools
author: pilot-test
cognitive_frame:
  primary: compositional
  goal_analysis:
    first_order: "Execute code-formatter workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic foundry processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "code-formatter",
  category: "foundry",
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
  keywords: ["code-formatter", "foundry", "workflow"],
  context: "user needs code-formatter capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

<!-- SKILL SOP IMPROVEMENT v1.0 -->
## Skill Execution Criteria

### When to Use This Skill
- [AUTO-EXTRACTED from skill description and content]
- [Task patterns this skill is optimized for]
- [Workflow contexts where this skill excels]

### When NOT to Use This Skill
- [Situations where alternative skills are better suited]
- [Anti-patterns that indicate wrong skill choice]
- [Edge cases this skill doesn't handle well]

### Success Criteria
- primary_outcome: "[SKILL-SPECIFIC measurable result based on skill purpose]"
- [assert|neutral] quality_threshold: 0.85 [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- verification_method: "[How to validate skill executed correctly and produced expected outcome]"

### Edge Cases
- case: "Ambiguous or incomplete input"
  handling: "Request clarification, document assumptions, proceed with explicit constraints"
- case: "Conflicting requirements or constraints"
  handling: "Surface conflict to user, propose resolution options, document trade-offs"
- case: "Insufficient context for quality execution"
  handling: "Flag missing information, provide template for needed context, proceed with documented limitations"

### Skill Guardrails
NEVER:
  - "[SKILL-SPECIFIC anti-pattern that breaks methodology]"
  - "[Common mistake that degrades output quality]"
  - "[Shortcut that compromises skill effectiveness]"
ALWAYS:
  - "[SKILL-SPECIFIC requirement for successful execution]"
  - "[Critical step that must not be skipped]"
  - "[Quality check that ensures reliable output]"

### Evidence-Based Execution
self_consistency: "After completing this skill, verify output quality by [SKILL-SPECIFIC validation approach]"
program_of_thought: "Decompose this skill execution into: [SKILL-SPECIFIC sequential steps]"
plan_and_solve: "Plan: [SKILL-SPECIFIC planning phase] -> Execute: [SKILL-SPECIFIC execution phase] -> Verify: [SKILL-SPECIFIC verification phase]"
<!-- END SKILL SOP IMPROVEMENT -->

# Code Formatter

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



Automatically format code files using language-specific formatters with comprehensive error handling.

## Overview

This skill formats code files by detecting the programming language and applying the appropriate formatter (Prettier for JS/TS, Black for Python, rustfmt for Rust). It provides clear feedback on changes and handles edge cases systematically.

## When to Use This Skill

Use when you need to format code before commits, ensure consistent style across projects, or apply language-specific formatting standards automatically.

## Instructions for Claude

When this skill is activated, follow these steps to format code files.

### Step 1: Validate Input File

**Action**: Verify that the specified file exists and is accessible.

**Implementation**:
```bash
# Check file exists
if [ ! -f "$FILE_PATH" ]; then
    echo "Error: File '$FILE_PATH' not found. Check path and try again."
    exit 1
fi

# Verify file is readable
if [ ! -r "$FILE_PATH" ]; then
    echo "Error: Cannot read '$FILE_PATH'. Fix with: chmod +r '$FILE_PATH'"
    exit 2
fi

# Check file size (max 10MB)
file_size=$(stat -c%s "$FILE_PATH" 2>/dev/null || stat -f%z "$FILE_PATH")
if [ $file_size -gt 10485760 ]; then
    echo "Warning: File is $(($file_size / 1024 / 1024))MB (max: 10MB). Continue? (y/n)"
    read -r response
    if [[ "$response" != "y" ]]; then
        exit 0
    fi
fi
```

**Success Criteria**:
- ✓ File exists at specified path
- ✓ File is readable (not a permissions error)
- ✓ File size ≤ 10MB or user confirms proceed

**Error Handling**:
- If file not found (exit 1) → Display error with path, abort
- If permissions denied (exit 2) → Display error with chmod fix, abort
- If file too large → Warn user, allow proceed or abort

---

### Step 2: Detect File Language and Formatter

**Action**: Determine programming language from file extension and select appropriate formatter.

**Implementation**:
```bash
# Detect language by exte

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
  pattern: "skills/foundry/code-formatter/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "code-formatter-{session_id}",
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

[commit|confident] <promise>CODE_FORMATTER_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
