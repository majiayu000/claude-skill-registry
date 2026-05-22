/*============================================================================*/
/* REVERSE-ENGINEERING-FIRMWARE-ANALYSIS SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: reverse-engineering-firmware-analysis
version: 1.0.0
description: |
  [assert|neutral] Firmware extraction and IoT security analysis (RE Level 5) for routers and embedded systems. Use when analyzing IoT firmware, extracting embedded filesystems (SquashFS/JFFS2/CramFS), finding hardcoded [ground:given] [conf:0.95] [state:confirmed]
category: IoT Security, Embedded Systems, Firmware Reverse Engineering
tags:
- security
- compliance
- safety
author: ruv
cognitive_frame:
  primary: evidential
  goal_analysis:
    first_order: "Execute reverse-engineering-firmware-analysis workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic IoT Security, Embedded Systems, Firmware Reverse Engineering processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "reverse-engineering-firmware-analysis",
  category: "IoT Security, Embedded Systems, Firmware Reverse Engineering",
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
  keywords: ["reverse-engineering-firmware-analysis", "IoT Security, Embedded Systems, Firmware Reverse Engineering", "workflow"],
  context: "user needs reverse-engineering-firmware-analysis capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

## When to Use This Skill

Use this skill when analyzing malware samples, reverse engineering binaries for security research, conducting vulnerability assessments, extracting IOCs from suspicious files, validating software for supply chain security, or performing CTF challenges and binary exploitation research.

## When NOT to Use This Skill

Do NOT use for unauthorized reverse engineering of commercial software, analyzing binaries on production systems, reversing software without legal authorization, violating terms of service or EULAs, or analyzing malware outside isolated environments. Avoid for simple string extraction (use basic tools instead).

## Success Criteria
- [assert|neutral] All security-relevant behaviors identified (network, file, registry, process activity) [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Malicious indicators extracted with confidence scores (IOCs, C2 domains, encryption keys) [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Vulnerabilities documented with CVE mapping where applicable [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Analysis completed within sandbox environment (VM/container with snapshots) [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Findings validated through multiple analysis methods (static + dynamic + symbolic) [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Complete IOC report generated (STIX/MISP format for threat intelligence sharing) [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Zero false positives in vulnerability assessments [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Exploitation proof-of-concept created (if vulnerability research) [ground:acceptance-criteria] [conf:0.90] [state:provisional]

## Edge Cases & Challenges

- Anti-analysis techniques (debugger detection, VM detection, timing checks)
- Obfuscated or packed binaries requiring unpacking
- Multi-stage malware with encrypted payloads
- Kernel-mode rootkits requiring specialized analysis
- Symbolic execution state explosion (>10,000 paths)
- Binary analysis timeout on complex programs (>24 hours)
- False positives from legitimate software behavior
- Encrypted network traffic requiring SSL interception

## Guardrails (CRITICAL SECURITY RULES)
- [assert|emphatic] NEVER: execute unknown binaries on host systems (ONLY in isolated VM/sandbox) [ground:policy] [conf:0.98] [state:confirmed]
- [assert|emphatic] NEVER: analyze malware without proper containment (air-gapped lab preferred) [ground:policy] [conf:0.98] [state:confirmed]
- [assert|emphatic] NEVER: reverse engineer software without legal authorization [ground:policy] [conf:0.98] [state:confirmed]
- [assert|emphatic] NEVER: share extracted credentials or encryption keys publicly [ground:policy] [conf:0.98] [state:confirmed]
- [assert|emphatic] NEVER: bypass licensing mechanisms for unauthorized use [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: use sandboxed environments with network monitoring [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: take VM snapshots before executing suspicious binaries [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: validate findings through multiple analysis methods [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: document analysis methodology with timestamps [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: assume binaries are malicious until proven safe [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: use network isolation to prevent malware communication [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: sanitize IOCs before sharing (redact internal IP addresses) [ground:policy] [conf:0.98] [state:confirmed]

## Evidence-Based Validati

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
  pattern: "skills/IoT Security, Embedded Systems, Firmware Reverse Engineering/reverse-engineering-firmware-analysis/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "reverse-engineering-firmware-analysis-{session_id}",
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

[commit|confident] <promise>REVERSE_ENGINEERING_FIRMWARE_ANALYSIS_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
