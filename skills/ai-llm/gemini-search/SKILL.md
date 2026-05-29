/*============================================================================*/
/* SKILL SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: SKILL
version: 1.0.0
description: |
  [assert|neutral] Get real-time web information using Gemini's built-in Google Search grounding [ground:given] [conf:0.95] [state:confirmed]
category: platforms
tags:
- gemini
- web-search
- real-time
- documentation
- current-info
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

# Gemini Search Skill

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



## Purpose
Leverage Gemini CLI's built-in Google Search grounding to fetch real-time web information, validate current best practices, and access the latest documentation - capabilities Claude Code doesn't have natively.

## Unique Capability
**What Claude Code Can't Do**: Claude Code's knowledge has a cutoff date and cannot access real-time web information during analysis. Gemini CLI has built-in Google Search integration that grounds responses in current web content with citations.

## When to Use

### Perfect For:
✅ Checking latest API documentation
✅ Finding current library versions and changelogs
✅ Validating best practices against current standards
✅ Researching breaking changes in dependencies
✅ Comparing current technology options
✅ Finding solutions to recent issues
✅ Checking security advisories and CVEs
✅ Verifying current framework conventions

### Don't Use When:
❌ Information is in your local codebase (use Claude Code)
❌ Need deep implementation logic (use Claude Code)
❌ Question doesn't require current web information
❌ Working with proprietary/internal systems

## How It Works

This skill spawns a **Gemini Search Agent** that:
1. Uses Gemini CLI's `@search` tool or built-in Google Search grounding
2. Fetches current web content with citations
3. Grounds analysis in real-time information
4. Returns findings with source URLs to Claude Code

## Usage

### Basic Search
```
/gemini-search
```

### With Specific Query
```
/gemini-search "What are the breaking changes in React 19?"
```

### Detailed Research
```
/gemini-search "Compare authentication approaches for Next.js 15 apps with latest security best practices"
```

## Input Examples

```bash
# API Documentation
/gemini-search "Latest Stripe API authentication methods 2025"

# Breaking Changes
/gemini-search "What changed in Python 3.13 that would break my code?"

# Best Practices
/gemini-search "Current best practices for securing Node.js REST APIs"

# Version Information
/gemini-search "Is TensorFlow 2.16 stable? What are known issues?"

# Framework Conventions
/gemini-search "How should I structure a Next.js 15 app directory?"

# Security Research
/gemini-search "Recent vulnerabilities in Express.js and mitigation strategies"

# Technology Comparison
/gemini-search "Compare Prisma vs Drizzle ORM for TypeScript projects 2025"
```

## Output

The agent provides:
- **Direct Answer**: Response to your query
- **Source Citations**: URLs where information was found
- **Current Status**: What's latest/stable/recommended
- **Key Findings**: Bullet points of important info
- **Recommendations**: Based on current web consensus
- **Related Resources**: Links to docs, guides, discussions

## Real-World Examples

### Example 1: API Changes
```
Query: "What changed in OpenAI API v2?"

Agent searches and returns:
- New endpoint structure with examples
- Deprecated methods and replacements
- Migration guide links
- Breaking changes to watch for
- Source: Official OpenAI docs + dev discussions
```

### Example 2: Security Advisory
```
Query: "Are there security issues with lodash 4.17.20?"

Agent searches and returns:
- CVE-2020-8203 prototype pollution vulnerability
- Affected versions: < 4.17.21
- Severity: High
- Fix: Upgrade to 4.17.21 or higher
- Sources: npm advisory, Snyk, GitHub issues
```

### Example 3: Framework Best Practices
```
Query: "How should I handle authentication in Next.js 15?"

Agent searches and returns:
- Recommended approaches (NextAuth.js, Clerk, Auth.js)
- App router vs pages router differences
- Server components considerations
- Code examples from official docs
- Sources: Next.js docs, Vercel guides, community tutorials
```

## Technical Details

### Gemini CLI Command Pattern
```bash
# Using @search tool
gemini "@search What are the latest Rust 2024 features?"

# Natural prompt with automatic search
gemini "Search for current best practices i

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
