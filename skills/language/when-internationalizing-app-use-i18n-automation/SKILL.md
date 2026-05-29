/*============================================================================*/
/* SKILL SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: skill
version: 1.0.0
description: |
  [assert|neutral] skill skill for delivery workflows [ground:given] [conf:0.95] [state:confirmed]
category: delivery
tags:
- general
author: system
cognitive_frame:
  primary: aspectual
  goal_analysis:
    first_order: "Execute skill workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic delivery processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "skill",
  category: "delivery",
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
  keywords: ["skill", "delivery", "workflow"],
  context: "user needs skill capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

# When Internationalizing App Use i18n Automation

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



---
name: when-internationalizing-app-use-i18n-automation
trigger: "when user requests internationalization, localization, or multi-language support"
description: "Automate internationalization and localization workflows for web applications with translation, key generation, and i18n library setup"
version: 2.0.0
author: Base Template Generator
category: localization
tags:
  - i18n
  - localization
  - translation
  - multi-language
  - automation
agents:
  - coder
  - researcher
  - reviewer
  - tester
coordinator: hierarchical-coordinator
memory_patterns:
  - swarm/i18n/source-strings
  - swarm/i18n/translations
  - swarm/i18n/config
  - swarm/i18n/test-results
success_criteria:
  - i18n library configured and integrated
  - Source strings extracted to translation files
  - Translation keys generated systematically
  - Multiple locales supported
  - Fallback language configured
  - Tests verify translations load correctly
  - Documentation generated for translators
---

## Trigger Conditions

Use this skill when:
- User requests internationalization (i18n) support
- Multi-language application needed
- Localization of existing application required
- Translation workflow automation desired
- Regional formatting (dates, numbers, currency) needed
- Right-to-left (RTL) language support required
- Dynamic language switching in UI needed

## Skill Overview

This skill automates the complete internationalization workflow: i18n library selection and setup, string extraction, translation key generation, locale file management, testing, and documentation. Supports popular frameworks (React, Vue, Angular) and i18n libraries (react-i18next, vue-i18n, ngx-translate).

## 7-Phase Skill-Forge Methodology

### Phase 1: i18n Requirements Analysis

**Objective**: Analyze application and determine i18n strategy

**Agent**: `researcher`

**Activities**:
- Analyze application framework and structure
- Identify hardcoded strings and content
- Determine target languages and locales
- Research i18n library options (react-i18next, vue-i18n)
- Define fallback language strategy
- Document RTL requirements if needed
- Store analysis in memory

**Memory Keys**:
- `swarm/i18n/analysis/framework`
- `swarm/i18n/analysis/target-languages`
- `swarm/i18n/analysis/library-choice`
- `swarm/i18n/analysis/string-count`
- `swarm/i18n/analysis/rtl-required`

**Script**:
```bash
npx claude-flow@alpha hooks pre-task --description "i18n requirements analysis"
# Detect framework
if [[ -f "package.json" ]]; then
  if grep -q "react" package.json; then
    FRAMEWORK="react"
    I18N_LIB="react-i18next"
  elif grep -q "vue" package.json; then
    FRAMEWORK="vue"
    I18N_LIB="vue-i18n"
  elif grep -q "@angular/core" package.json; then
    FRAMEWORK="angular"
    I18N_LIB="@ngx-translate/core"
  fi
fi

npx claude-flow@alpha memory store "swarm/i18n/analysis/framework" "$FRAMEWORK"
npx claude-flow@alpha memory store "swarm/i18n/analysis/library-choice" "$I18N_LIB"

# Count hardcoded strings (rough estimate)
STRING_COUNT=$(grep -r "\"[A-Z]" src/ | wc -l)
npx claude-flow@alpha memory store "swarm/i18n/analysis/string-count" "$STRING_COUNT"

npx claude-flow@alpha hooks notify --message "i18n analysis complete: $FRAMEWORK with $I18N_LIB"
```

### Phase 2: i18n Library Setup & Configuration

**Objective**: Install and configure i18n library for the application

**Agent**: `coder`

**Activities**:
- Install selected i18n library and dependencies
- Create i18n configuration file
- Set up language detection (browser, URL, localStorage)
- Configure fallback language (usually 'en')
- Initialize i18n in application entry point
- Set up translation file structure
- Store configuration in memory

**Memory Keys**:
- `swarm/i18n/config/library-installed`
- `swarm/i18n/config/setup-files`
- `swarm/i18n/config/default-locale`
- `swarm/i18n/config/supported-loca

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
  pattern: "skills/delivery/skill/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "skill-{session_id}",
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
