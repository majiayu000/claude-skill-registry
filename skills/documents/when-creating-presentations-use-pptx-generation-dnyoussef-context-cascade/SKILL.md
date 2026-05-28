/*============================================================================*/
/* WHEN-CREATING-PRESENTATIONS-USE-PPTX-GENERATION SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: when-creating-presentations-use-pptx-generation
version: 1.0.0
description: |
  [assert|neutral] Enterprise-grade PowerPoint deck generation using evidence-based prompting, workflow enforcement, constraint-based design [ground:given] [conf:0.95] [state:confirmed]
category: utilities
tags:
- presentation
- pptx
- slides
- enterprise
- documentation
author: ruv
cognitive_frame:
  primary: aspectual
  goal_analysis:
    first_order: "Execute when-creating-presentations-use-pptx-generation workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic utilities processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "when-creating-presentations-use-pptx-generation",
  category: "utilities",
  version: "1.0.0",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S1 COGNITIVE FRAME                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] COGNITIVE_FRAME := {
  frame: "Aspectual",
  source: "Russian",
  force: "Complete or ongoing?"
} [ground:cognitive-science] [conf:0.92] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S2 TRIGGER CONDITIONS                                                       */
/*----------------------------------------------------------------------------*/

[define|neutral] TRIGGER_POSITIVE := {
  keywords: ["when-creating-presentations-use-pptx-generation", "utilities", "workflow"],
  context: "user needs when-creating-presentations-use-pptx-generation capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

## When to Use This Skill

- **Tool Usage**: When you need to execute specific tools, lookup reference materials, or run automation pipelines
- **Reference Lookup**: When you need to access documented patterns, best practices, or technical specifications
- **Automation Needs**: When you need to run standardized workflows or pipeline processes

## When NOT to Use This Skill

- **Manual Processes**: Avoid when manual intervention is more appropriate than automated tools
- **Non-Standard Tools**: Do not use when tools are deprecated, unsupported, or outside standard toolkit

## Success Criteria
- [assert|neutral] *Tool Executed Correctly**: Verify tool runs without errors and produces expected output [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] *Reference Accurate**: Confirm reference material is current and applicable [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] *Pipeline Complete**: Ensure automation pipeline completes all stages successfully [ground:acceptance-criteria] [conf:0.90] [state:provisional]

## Edge Cases

- **Tool Unavailable**: Handle scenarios where required tool is not installed or accessible
- **Outdated References**: Detect when reference material is obsolete or superseded
- **Pipeline Failures**: Recover gracefully from mid-pipeline failures with clear error messages

## Guardrails
- [assert|emphatic] NEVER: use deprecated tools**: Always verify tool versions and support status before execution [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: verify outputs**: Validate tool outputs match expected format and content [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: check health**: Run tool health checks before critical operations [ground:policy] [conf:0.98] [state:confirmed]

## Evidence-Based Validation

- **Tool Health Checks**: Execute diagnostic commands to verify tool functionality before use
- **Output Validation**: Compare actual outputs against expected schemas or patterns
- **Pipeline Monitoring**: Track pipeline execution metrics and success rates

# PPTX Generation - Enterprise Presentation Creator

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



## Overview

Enterprise-grade PowerPoint deck generation system using evidence-based prompting techniques, workflow enforcement, and constraint-based design for professional presentations (board decks, reports, analyses). Supports 30+ slide decks with consistent visual quality and accessibility compliance.

## When to Use

- Creating board-level presentations
- Quarterly business reviews
- Technical documentation slides
- Data-heavy reports
- Executive summaries
- Client proposals
- Training materials

## Phase 1: Research Content (8 min)

### Objective
Gather and structure presentation information

### Agent: Researcher

**Step 1.1: Content Gathering**
```javascript
const contentStructure = {
  metadata: {
    title: 'Presentation Title',
    subtitle: 'Subtitle',
    author: 'Author Name',
    date: new Date(),
    audience: 'executive|technical|general',
    purpose: 'inform|persuade|instruct'
  },
  outline: [
    {
      section: 'Introduction',
      slides: ['Title', 'Agenda', 'Executive Summary']
    },
    {
      section: 'Main Content',
      slides: ['Key Points', 'Data Analysis', 'Recommendations']
    },
    {
      section: 'Conclusion',
      slides: ['Summary', 'Next Steps', 'Q&A']
    }
  ],
  dataPoints: extractDataPoints(),
  visualizations: identifyVisualizations()
};

await memory.store('pptx/content-structure', contentStructure);
```

**Step 1.2: Data Analysis**
```javascript
async function analyzeData(data) {
  return {
    tables: extractTables(data),
    charts: identifyChartOpportunities(data),
    trends: analyzeTrends(data),
    insights: generateInsights(data)
  };
}
```

### Validation Criteria
- [ ] Content structure defined
- [ ] Data points extracted
- [ ] Visualization types

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
  pattern: "skills/utilities/when-creating-presentations-use-pptx-generation/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "when-creating-presentations-use-pptx-generation-{session_id}",
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

[commit|confident] <promise>WHEN_CREATING_PRESENTATIONS_USE_PPTX_GENERATION_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
