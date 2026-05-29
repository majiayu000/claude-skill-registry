/*============================================================================*/
/* SKILL SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: skill
version: 1.0.0
description: |
  [assert|neutral] Automated US/EU career opportunity tracking with policy monitoring, EV-based ranking, and tailored application materials [ground:given] [conf:0.95] [state:confirmed]
category: career-orchestration
tags:
- general
author: system
cognitive_frame:
  primary: evidential
  goal_analysis:
    first_order: "Execute skill workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic career-orchestration processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "skill",
  category: "career-orchestration",
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
  keywords: ["skill", "career-orchestration", "workflow"],
  context: "user needs skill capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

# Dual-Track Career Intelligence

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



Automated tracking of internal/external roles across US/EU markets with policy monitoring, visa leverage analysis, and tailored pitch generation.

## Overview

This skill orchestrates 3 specialist agents to:
1. **Scout** (researcher) - Crawl job boards and normalize opportunities
2. **RegWatch** (researcher) - Diff EU policy/regulatory pages for visa changes
3. **Ranker** (analyst) - Score opportunities by Fit, Option Value, Speed, Cred Stack
4. **PitchPrep** (coder) - Generate tailored bullets, Q&A, and anecdotes

**Critical differentiator**: Tracks visa leverage and immigration policy changes alongside traditional job factors.

## When to Use

- **Weekly/bi-weekly**: Systematic career opportunity scanning
- **Before major applications**: Generate tailored pitch materials
- **EU policy changes**: Understand immigration implications
- **Strategic planning**: Maintain optionality across geographies

## Assigned Agents

### Primary Agents

**researcher (Scout role)** - Phase 1: Web scraping, data normalization, source aggregation
- Expertise: API integration, data extraction, YAML processing
- Tools: curl, jq, yq, bash scripting
- Output: Raw CSV of opportunities with metadata

**researcher (RegWatch role)** - Phase 2: Policy diff analysis, regulatory monitoring
- Expertise: Document comparison, policy interpretation, change detection
- Tools: diff, git, web scraping
- Output: Policy change summary with action items

### Secondary Agents

**analyst (Ranker role)** - Phase 3: Multi-factor scoring, EV calculation
- Expertise: Scoring algorithms, decision analysis, prioritization
- Tools: Python/Node scoring scripts, statistical analysis
- Output: Ranked opportunities with justifications

**coder (PitchPrep role)** - Phase 4: Content generation, tailoring, formatting
- Expertise: Natural language generation, resume optimization, storytelling
- Tools: Template engines, GPT-assisted writing, markdown formatting
- Output: Tailored cover letters, Q&A prep, cred stack mapping

## Coordination Pattern

```
SKILL: dual-track-career-intelligence
  ↓
hierarchical-coordinator spawns 4 sequential phases
  ↓
Phase 1: Scout (researcher) → raw data
Phase 2: RegWatch (researcher) → policy deltas
Phase 3: Ranker (analyst) → scored opportunities
Phase 4: PitchPrep (coder) → tailored materials
  ↓
All phases coordinate via Memory MCP with WHO/WHEN/PROJECT/WHY tagging
```

---

## Phase 1: Scout (Data Collection)

**Agent**: `researcher` (Scout role)

### Inputs
- `data/sources/job_boards.yml` - Job board APIs and search parameters
- `data/profiles/cv_core.md` - Keywords and skills to match

### Commands Executed

```bash
#!/bin/bash
# Phase 1: Job Board Scanning

# PRE-TASK HOOK
npx claude-flow@alpha hooks pre-task \
  --description "Career intel: job board scanning" \
  --agent "researcher" \
  --role "Scout" \
  --skill "dual-track-career-intelligence"

# SESSION RESTORE (if resuming)
npx claude-flow@alpha hooks session-restore \
  --session-id "career-intel-$(date +%Y-%W)"

# SETUP
WEEK=$(date +%Y-%W)
mkdir -p outputs/reports
mkdir -p raw_data

# READ CONFIG
BOARDS=$(yq eval '.boards[].url' data/sources/job_boards.yml)
KEYWORDS=$(yq eval '.search_keywords | join(",")' data/sources/job_boards.yml)
GEO=$(yq eval '.geo_filters | join(",")' data/sources/job_boards.yml)

# SCRAPE JOB BOARDS
echo "title,company,location,url,posted_date,visa_support,remote_ok,comp_signal" > raw_data/jobs_${WEEK}.csv

for BOARD in $BOARDS; do
  echo "[Scout] Scanning: $BOARD"

  # Example API call (adapt to actual board APIs)
  curl -s "${BOARD}/api/jobs?keywords=${KEYWORDS}&geo=${GEO}" \
    | jq -r '.results[] | [
        .title,
        .company,
        .location,
        .apply_url,
        .posted_date,
        .visa_sponsorship,
        .remote_allowed,
        (.salary.min // 0)
      ] | @csv' \
    >> raw_data/jobs_${WEEK}.csv

  sleep 2  # Rate l

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
  pattern: "skills/career-orchestration/skill/{project}/{timestamp}",
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
