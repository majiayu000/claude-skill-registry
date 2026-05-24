/*============================================================================*/
/* SOURCE-CREDIBILITY-ANALYZER SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: source-credibility-analyzer
version: 2.0
description: |
  [assert|neutral] Standalone tool for automated source evaluation using program-of-thought scoring rubrics. Outputs credibility (1-5), bias (1-5), and priority (1-5) scores with transparent explanations. Use when evalu [ground:given] [conf:0.95] [state:confirmed]
category: research
tags:
- general
author: system
cognitive_frame:
  primary: evidential
  goal_analysis:
    first_order: "Execute source-credibility-analyzer workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic research processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "source-credibility-analyzer",
  category: "research",
  version: "2.0",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S1 COGNITIVE FRAME                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] COGNITIVE_FRAME := {
  frame: "Evidential",
  source: "Turkish",
  force: "How do you know?"
} [ground:cognitive-science] [conf:0.92] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S2 TRIGGER CONDITIONS                                                       */
/*----------------------------------------------------------------------------*/

[define|neutral] TRIGGER_POSITIVE := {
  keywords: ["source-credibility-analyzer", "research", "workflow"],
  context: "user needs source-credibility-analyzer capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

# Source Credibility Analyzer

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



## Purpose

Automate evaluation of research sources using transparent program-of-thought rubrics. Outputs structured JSON with credibility, bias, and priority scores (1-5) plus explanations showing calculation logic. Can be used as standalone tool OR integrated into general-research-workflow Step 3.

## When to Use This Tool

**Use this tool when:**
- ✅ Evaluating research sources for academic projects
- ✅ Automating source classification (general-research-workflow Step 3)
- ✅ Scoring large batches of sources consistently
- ✅ Getting objective second opinion on source quality

**Do NOT use for:**
- ❌ Entertainment content (movies, novels) - not designed for this
- ❌ Source quality already obvious (Nature paper = high, random blog = low)
- ❌ Unique/irreplaceable source (only source on obscure topic) - read anyway

**Decision Tree**: If manual source evaluation takes >10 min → use this tool (saves 15-45 min per source)

## Quick Reference

| Step | Objective | Deliverable | Duration | Quality Gate |
|------|-----------|-------------|----------|--------------|
| 0 | Validate inputs | Confirmed metadata | 30 sec | Required fields present |
| 0.5 | Classify source type | Source category | 1 min | Type assigned |
| 1 | Calculate credibility | Score 1-5 + explanation | 2-5 min | Score justified |
| 2 | Calculate bias | Score 1-5 + explanation | 2-5 min | Score justified |
| 3 | Calculate priority | Score 1-5 + explanation | 1-3 min | Score justified |
| 4 | Resolve conflicts | Final recommendation | 1 min | Logic correct |
| 5 | Generate output | JSON + storage | 1 min | Complete + stored |

---

## Agent Coordination Protocol

### Single Agent Execution
- **Agent**: analyst
- **Role**: Evaluate source using program-of-thought rubrics
- **Workflow**: Sequential steps 0 → 0.5 → 1 → 2 → 3 → 4 → 5

### Input Format
```json
{
  "title": "[Required]",
  "author": "[Required]",
  "year": [Required, 1500-2025],
  "venue": "[Required]",
  "type": "[Required]",
  "citations": [Optional],
  "doi": "[Optional]",
  "url": "[Optional]",
  "institution": "[Optional]",
  "credentials": "[Optional]"
}
```

### Output Format
```json
{
  "source": { ... },
  "scores": {
    "credibility": {"score": [1-5], "explanation": "..."},
    "bias": {"score": [1-5], "explanation": "..."},
    "priority": {"score": [1-5], "explanation": "..."}
  },
  "recommendation": {
    "action": "[READ_FIRST | READ_LATER | VERIFY_CLAIMS | SKIP]",
    "reason": "...",
    "conflicts": "..."
  },
  "metadata": { ... }
}
```

### Memory MCP Tags
Store with: `WHO=analyst`, `WHEN=[timestamp]`, `PROJECT=[topic]`, `WHY=source-scoring`, `CREDIBILITY=[score]`, `BIAS=[score]`, `PRIORITY=[score]`, `RECOMMENDATION=[action]`

---

## Step-by-Step Workflow

### STEP 0: Validate Input Metadata
**Agent**: analyst
**Objective**: Ensure required metadata is present and valid

**Procedure**:
1. Check for ✅ **required** fields:
   - `title` (string, non-empty)
   - `author` (string, non-empty)
   - `year` (integer, 1500-2025)
   - `venue` (string, non-empty)
   - `type` (string, non-empty)

2. Note ⚠️ **optional** fields if present:
   - `citations` (improves credibility scoring)
   - `doi` (improves credibility scoring)
   - `institution` (improves credibility scoring)
   - `credentials` (improves credibility scoring)
   - `url` (for reference)

3. Validate data types and ranges:
   - Year must be integer 1500-2025
   - All required strings non-empty

4. If validation fails → Return error with missing/invalid field name

**Deliverable**: Validated metadata object

**Quality Gate 0**:
- **GO**: All required fields present, year valid (1500-2025)
- **NO-GO**: Missing/invalid field → Return error to user

---

### STEP 0.5: Classify Source Type (Edge Case Handling)
**Agent**: analyst
**Objective**: Assign source to appropriate category for rubric baseline

**Edge Case Decision Tree**:

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
  pattern: "skills/research/source-credibility-analyzer/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "source-credibility-analyzer-{session_id}",
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

[commit|confident] <promise>SOURCE_CREDIBILITY_ANALYZER_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
