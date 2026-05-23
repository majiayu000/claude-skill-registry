/*============================================================================*/
/* WHEN-AUDITING-SECURITY-USE-SECURITY-ANALYZER SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: when-auditing-security-use-security-analyzer
version: 1.0.0
description: |
  [assert|neutral] Comprehensive security auditing across static analysis, dynamic testing, dependency vulnerabilities, secrets detection, and OWASP compliance [ground:given] [conf:0.95] [state:confirmed]
category: security
tags:
- security
- compliance
- safety
author: ruv
cognitive_frame:
  primary: evidential
  goal_analysis:
    first_order: "Execute when-auditing-security-use-security-analyzer workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic security processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "when-auditing-security-use-security-analyzer",
  category: "security",
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
  keywords: ["when-auditing-security-use-security-analyzer", "security", "workflow"],
  context: "user needs when-auditing-security-use-security-analyzer capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

## When to Use This Skill

Use this skill when conducting comprehensive security audits, performing vulnerability assessments, analyzing application security posture, identifying security misconfigurations, validating security controls, or preparing for penetration testing engagements.

## When NOT to Use This Skill

Do NOT use for compliance audits (use compliance skill instead), unauthorized security testing, production system scanning without approval, vulnerability exploitation (only identification), or automated scanning without manual validation. Avoid for code quality audits unrelated to security.

## Success Criteria
- [assert|neutral] All security vulnerabilities identified with CVSS scores and remediation guidance [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Security misconfigurations documented with severity ratings [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Attack surface mapped (exposed services, authentication mechanisms, data flows) [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Security controls validated (authentication, authorization, encryption, logging) [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Vulnerability remediation plan created with prioritization [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Zero critical/high vulnerabilities remaining after remediation [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Security findings validated through manual testing (not just automated scans) [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Penetration testing readiness achieved (all low-hanging fruit addressed) [ground:acceptance-criteria] [conf:0.90] [state:provisional]

## Edge Cases & Challenges

- False positives from automated security scanners
- Zero-day vulnerabilities without CVE mappings
- Business logic vulnerabilities requiring manual analysis
- Authentication bypass through indirect paths
- Encrypted communications requiring SSL interception
- Cloud-specific security misconfigurations (S3 buckets, IAM roles)
- Supply chain vulnerabilities in dependencies
- Time-of-check to time-of-use (TOCTOU) race conditions

## Guardrails (CRITICAL SECURITY RULES)
- [assert|emphatic] NEVER: exploit vulnerabilities beyond proof-of-concept validation [ground:policy] [conf:0.98] [state:confirmed]
- [assert|emphatic] NEVER: conduct security testing on unauthorized systems [ground:policy] [conf:0.98] [state:confirmed]
- [assert|emphatic] NEVER: exfiltrate sensitive data during security assessments [ground:policy] [conf:0.98] [state:confirmed]
- [assert|emphatic] NEVER: cause denial-of-service or system instability [ground:policy] [conf:0.98] [state:confirmed]
- [assert|emphatic] NEVER: share vulnerability details publicly before responsible disclosure [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: obtain written authorization before security testing [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: document findings with remediation guidance [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: validate vulnerabilities through manual testing [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: follow responsible disclosure timelines (90 days standard) [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: maintain confidentiality of security findings [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: use non-destructive testing methods where possible [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: preserve audit trails of security testing activities [ground:policy] [conf:0.98] [state:confirmed]

## Evidence-Based Validation

All security findings MUST be validated through:
1. **Automated scanning** - Multiple tools confirm vulnerability (

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
  pattern: "skills/security/when-auditing-security-use-security-analyzer/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "when-auditing-security-use-security-analyzer-{session_id}",
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

[commit|confident] <promise>WHEN_AUDITING_SECURITY_USE_SECURITY_ANALYZER_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
