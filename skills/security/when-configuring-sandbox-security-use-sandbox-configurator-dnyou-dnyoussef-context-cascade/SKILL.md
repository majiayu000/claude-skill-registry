/*============================================================================*/
/* WHEN-CONFIGURING-SANDBOX-SECURITY-USE-SANDBOX-CONFIGURATOR SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: when-configuring-sandbox-security-use-sandbox-configurator
version: 1.0.0
description: |
  [assert|neutral] ```yaml [ground:given] [conf:0.95] [state:confirmed]
category: security
tags:
- security
- compliance
- safety
author: ruv
cognitive_frame:
  primary: evidential
  goal_analysis:
    first_order: "Execute when-configuring-sandbox-security-use-sandbox-configurator workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic security processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "when-configuring-sandbox-security-use-sandbox-configurator",
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
  keywords: ["when-configuring-sandbox-security-use-sandbox-configurator", "security", "workflow"],
  context: "user needs when-configuring-sandbox-security-use-sandbox-configurator capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

## When to Use This Skill

Use this skill when configuring sandbox network isolation, setting up trusted domain whitelists, implementing zero-trust network policies for AI code execution, configuring corporate proxies and internal registries, or preventing data exfiltration through network controls.

## When NOT to Use This Skill

Do NOT use for production network security (use infrastructure-as-code instead), configuring firewall rules on live systems, bypassing organizational network policies, or setting up VPNs and network routing (use networking specialists). Avoid for troubleshooting network connectivity issues unrelated to sandbox security.

## Success Criteria
- [assert|neutral] Trusted domain whitelist validated (all required domains accessible, untrusted blocked) [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Network isolation prevents data exfiltration attacks (tested with simulated exfil) [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Internal registries accessible through proper proxy configuration [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Environment variables secured (no secrets in config files) [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Zero false positives (legitimate development work unblocked) [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Package installations succeed from approved registries [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Build and deployment commands execute without network errors [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Validation tests pass (npm install, git clone, API calls to approved domains) [ground:acceptance-criteria] [conf:0.90] [state:provisional]

## Edge Cases & Challenges

- Corporate proxies requiring NTLM authentication
- Split-tunnel VPNs with mixed internal/external traffic
- CDN domains changing dynamically (*.cloudfront.net wildcards)
- WebSocket connections requiring separate allowlisting
- DNS resolution failures in isolated environments
- IPv6 vs IPv4 routing differences
- Localhost binding restrictions breaking development servers
- Proxy auto-configuration (PAC) files with complex logic

## Guardrails (CRITICAL SECURITY RULES)
- [assert|emphatic] NEVER: disable network isolation without security review [ground:policy] [conf:0.98] [state:confirmed]
- [assert|emphatic] NEVER: add untrusted domains to whitelist without validation [ground:policy] [conf:0.98] [state:confirmed]
- [assert|emphatic] NEVER: store secrets (API keys, passwords) in sandbox configuration files [ground:policy] [conf:0.98] [state:confirmed]
- [assert|emphatic] NEVER: bypass proxy settings to access restricted resources [ground:policy] [conf:0.98] [state:confirmed]
- [assert|emphatic] NEVER: allow wildcard domain patterns without justification (*.com = insecure) [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: validate domain ownership before whitelisting [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: use HTTPS for external domains (enforce TLS) [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: document why each domain is trusted (justification required) [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: test that untrusted domains are blocked (negative testing) [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: use environment variable references for secrets (not plaintext) [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: maintain audit logs of network policy changes [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: validate network policies after configuration changes [ground:policy] [conf:0.98] [state:confirmed]

## Evidence-Based Validation

All network security configurations MUST be validate

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
  pattern: "skills/security/when-configuring-sandbox-security-use-sandbox-configurator/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "when-configuring-sandbox-security-use-sandbox-configurator-{session_id}",
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

[commit|confident] <promise>WHEN_CONFIGURING_SANDBOX_SECURITY_USE_SANDBOX_CONFIGURATOR_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
