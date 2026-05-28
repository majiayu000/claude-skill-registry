/*============================================================================*/
/* REPRODUCIBILITY-AUDIT SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: reproducibility-audit
version: 1.0.0
description: |
  [assert|neutral] Comprehensive audit of ML reproducibility packages ensuring ACM Artifact Evaluation compliance with statistical validation for Deep Research SOP Pipeline G. Use before Quality Gate 3 validation when r [ground:given] [conf:0.95] [state:confirmed]
category: quality
tags:
- quality
- testing
- validation
author: ruv
cognitive_frame:
  primary: evidential
  goal_analysis:
    first_order: "Execute reproducibility-audit workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic quality processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "reproducibility-audit",
  category: "quality",
  version: "1.0.0",
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
  keywords: ["reproducibility-audit", "quality", "workflow"],
  context: "user needs reproducibility-audit capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

## When to Use This Skill

Use this skill when:
- Code quality issues are detected (violations, smells, anti-patterns)
- Audit requirements mandate systematic review (compliance, release gates)
- Review needs arise (pre-merge, production hardening, refactoring preparation)
- Quality metrics indicate degradation (test coverage drop, complexity increase)
- Theater detection is needed (mock data, stubs, incomplete implementations)

## When NOT to Use This Skill

Do NOT use this skill for:
- Simple formatting fixes (use linter/prettier directly)
- Non-code files (documentation, configuration without logic)
- Trivial changes (typo fixes, comment updates)
- Generated code (build artifacts, vendor dependencies)
- Third-party libraries (focus on application code)

## Success Criteria
- [assert|neutral] This skill succeeds when: [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] *Violations Detected**: All quality issues found with ZERO false negatives [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] *False Positive Rate**: <5% (95%+ findings are genuine issues) [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] *Actionable Feedback**: Every finding includes file path, line number, and fix guidance [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] *Root Cause Identified**: Issues traced to underlying causes, not just symptoms [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] *Fix Verification**: Proposed fixes validated against codebase constraints [ground:acceptance-criteria] [conf:0.90] [state:provisional]

## Edge Cases and Limitations

Handle these edge cases carefully:
- **Empty Files**: May trigger false positives - verify intent (stub vs intentional)
- **Generated Code**: Skip or flag as low priority (auto-generated files)
- **Third-Party Libraries**: Exclude from analysis (vendor/, node_modules/)
- **Domain-Specific Patterns**: What looks like violation may be intentional (DSLs)
- **Legacy Code**: Balance ideal standards with pragmatic technical debt management

## Quality Analysis Guardrails

CRITICAL RULES - ALWAYS FOLLOW:
- **NEVER approve code without evidence**: Require actual execution, not assumptions
- **ALWAYS provide line numbers**: Every finding MUST include file:line reference
- **VALIDATE findings against multiple perspectives**: Cross-check with complementary tools
- **DISTINGUISH symptoms from root causes**: Report underlying issues, not just manifestations
- **AVOID false confidence**: Flag uncertain findings as "needs manual review"
- **PRESERVE context**: Show surrounding code (5 lines before/after minimum)
- **TRACK false positives**: Learn from mistakes to improve detection accuracy

## Evidence-Based Validation

Use multiple validation perspectives:
1. **Static Analysis**: Code structure, patterns, metrics (connascence, complexity)
2. **Dynamic Analysis**: Execution behavior, test results, runtime characteristics
3. **Historical Analysis**: Git history, past bug patterns, change frequency
4. **Peer Review**: Cross-validation with other quality skills (functionality-audit, theater-detection)
5. **Domain Expertise**: Leverage .claude/expertise/{domain}.yaml if available

**Validation Threshold**: Findings require 2+ confirming signals before flagging as violations.

## Integration with Quality Pipeline

This skill integrates with:
- **Pre-Phase**: Load domain expertise (.claude/expertise/{domain}.yaml)
- **Parallel Skills**: functionality-audit, theater-detection-audit, style-audit
- **Post-Phase**: Store findings in Memory MCP with WHO/WHEN/PROJECT/WHY tags
- **Feedback Loop**: Learnings feed dogfooding-system for continuous improvement


# Reproducibility Audit

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



Audit ML reproducibility packages for compliance with ACM Artifact Evaluation standards, ensuring research can be reprod

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
  pattern: "skills/quality/reproducibility-audit/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "reproducibility-audit-{session_id}",
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

[commit|confident] <promise>REPRODUCIBILITY_AUDIT_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
