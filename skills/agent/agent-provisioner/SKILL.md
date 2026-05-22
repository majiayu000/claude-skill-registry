---
skill_name: agent-provisioner
activation_code: AGENT_PROVISIONER_V1
version: 1.0.0
phase: any
prerequisites:
  - Human available for agent design decisions
  - Knowledge of domain for new agent
outputs:
  - Fully curated agent definition
  - Curation session record
  - Agent registered in appropriate category
description: |
  MANDATORY workflow for creating new agents. Enforces -01-agent-formatting
  standards from inception, ensuring every new agent is properly designed,
  researched, and curated before deployment.
---

# Agent Provisioner Skill

## Purpose

**This is the ONLY sanctioned way to create new agents in dev-system.**

Creating agents without this skill results in:
- Missing knowledge source validation
- Unverified tier classification
- Incomplete MCP integration
- Poor instruction quality
- No curation record

## Activation

```
/agent-provisioner
Parameters:
  domain: {domain-description}
  name: {proposed-agent-name}
  category: {parent-category in -03-agents}
```

Or simply:
```
I need a new agent for {description}
```

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    AGENT PROVISIONING WORKFLOW                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Step 1: DOMAIN ANALYSIS                                                │
│  ├─ What domain does this agent cover?                                  │
│  ├─ What would a PhD in this domain know?                              │
│  └─ What existing agents overlap? (avoid duplication)                   │
│          ▼                                                              │
│  Step 2: TIER CLASSIFICATION                                            │
│  ├─ Focused (~500 tokens) - Bounded, clear scope                       │
│  ├─ Expert (~1500 tokens) - Specialized domain work                    │
│  └─ PhD (~3000 tokens) - Deep, novel challenges                        │
│          ▼                                                              │
│  Step 3: KNOWLEDGE RESEARCH                                             │
│  ├─ Identify authoritative sources (specs, official docs)              │
│  ├─ Use Firecrawl for deep research                                    │
│  └─ Human adjudicates each source                                      │
│          ▼                                                              │
│  Step 4: IDENTITY DESIGN                                                │
│  ├─ Interpretive lens (how agent thinks)                               │
│  ├─ Vocabulary calibration (15-20 terms)                               │
│  └─ Core principles and constraints                                    │
│          ▼                                                              │
│  Step 5: INSTRUCTION AUTHORING                                          │
│  ├─ Always section (non-negotiables)                                   │
│  ├─ Mode-specific instructions                                         │
│  ├─ Never section (anti-patterns)                                      │
│  └─ Specializations with deep knowledge                                │
│          ▼                                                              │
│  Step 6: TOOLING & MCP                                                  │
│  ├─ Tool modes (audit, solution, research)                             │
│  ├─ MCP server selection                                               │
│  └─ Proactive triggers                                                 │
│          ▼                                                              │
│  Step 7: SYNTHESIS & VALIDATION                                         │
│  ├─ Generate complete agent definition                                 │
│  ├─ Validate against CURATION-CHECKLIST.md                             │
│  ├─ Human final review                                                 │
│  └─ Save to appropriate category                                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Step 1: Domain Analysis

Present domain analysis interface:

```
╔═══════════════════════════════════════════════════════════════════════╗
║              NEW AGENT: DOMAIN ANALYSIS                                ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  Proposed Agent: {name}                                                ║
║  Domain: {domain}                                                      ║
║                                                                        ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ DOMAIN EXPERTISE AREAS                                          │   ║
║  ├────────────────────────────────────────────────────────────────┤   ║
║  │ 1. {expertise-area-1}                                           │   ║
║  │ 2. {expertise-area-2}                                           │   ║
║  │ 3. {expertise-area-3}                                           │   ║
║  │ 4. {expertise-area-4}                                           │   ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                                                                        ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ RELATED EXISTING AGENTS                                         │   ║
║  ├────────────────────────────────────────────────────────────────┤   ║
║  │ • {existing-agent-1}: {overlap-description}                     │   ║
║  │ • {existing-agent-2}: {overlap-description}                     │   ║
║  │   → Differentiation: {how new agent differs}                    │   ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                                                                        ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ RECOMMENDED CATEGORY                                            │   ║
║  ├────────────────────────────────────────────────────────────────┤   ║
║  │ agents/-03-agents/{category}/{subcategory}/                     │   ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                                                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║  [C] Confirm domain analysis                                           ║
║  [E] Edit expertise areas                                              ║
║  [R] Change recommended category                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### Overlap Detection

Before proceeding, search for existing agents with similar capabilities:

```bash
# Search existing agents
grep -r "domain:" agents/-03-agents/ | grep -i "{domain-keywords}"
grep -r "proactive_triggers:" agents/-03-agents/ | grep -i "{trigger-patterns}"
```

If significant overlap exists:
- Recommend extending existing agent instead
- Or clearly differentiate the new agent's unique value

## Step 2: Tier Classification

Apply TIER-CLASSIFICATION.md criteria:

```
╔═══════════════════════════════════════════════════════════════════════╗
║              TIER CLASSIFICATION                                       ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  Based on domain analysis, this agent is classified as:               ║
║                                                                        ║
║    ┌─────────────────────────────────────────────────────────────┐    ║
║    │  ██████████ EXPERT TIER                                     │    ║
║    │                                                              │    ║
║    │  Tokens: ~1500                                               │    ║
║    │  Instructions: 15-20                                         │    ║
║    │  Model: sonnet (default) | opus (if high-stakes)            │    ║
║    └─────────────────────────────────────────────────────────────┘    ║
║                                                                        ║
║  Rationale:                                                            ║
║    • Domain requires specialized knowledge                             ║
║    • Multiple expertise areas identified                               ║
║    • Not a bounded/simple task (would be Focused)                     ║
║    • Not research-level/novel problem (would be PhD)                  ║
║                                                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║  [C] Confirm tier classification                                       ║
║  [F] Change to Focused tier                                            ║
║  [P] Change to PhD tier                                                ║
╚═══════════════════════════════════════════════════════════════════════╝
```

## Step 3: Knowledge Research

Delegate to knowledge research workflow:

```
╔═══════════════════════════════════════════════════════════════════════╗
║              KNOWLEDGE RESEARCH                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  Researching authoritative sources for: {domain}                      ║
║                                                                        ║
║  What would a PhD in {domain} cite as canonical references?           ║
║                                                                        ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ RESEARCH STRATEGY                                               │   ║
║  ├────────────────────────────────────────────────────────────────┤   ║
║  │ 1. Official specifications (IETF, IEEE, W3C, ISO)              │   ║
║  │ 2. Vendor/maintainer documentation                              │   ║
║  │ 3. Academic papers (if applicable)                              │   ║
║  │ 4. Community best practices                                     │   ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                                                                        ║
║  Launching web-researcher skill for parallel discovery...             ║
║                                                                        ║
╚═══════════════════════════════════════════════════════════════════════╝
```

For EACH discovered source, present for human adjudication (never bulk-add):

```
╔═══════════════════════════════════════════════════════════════════════╗
║              SOURCE ADJUDICATION (1 of N)                              ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  Source: {source-title}                                                ║
║  URL: {url}                                                            ║
║  Authority Tier: {1-5} ({tier-name})                                   ║
║                                                                        ║
║  Unique Value:                                                         ║
║    {what this provides that nothing else does}                         ║
║                                                                        ║
║  Materialization: URL | Local Excerpt | Embed                         ║
║    Rationale: {why this materialization}                               ║
║                                                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║  [A] Add to agent                                                      ║
║  [S] Skip this source                                                  ║
║  [D] Show source content                                               ║
╚═══════════════════════════════════════════════════════════════════════╝
```

## Step 4: Identity Design

Design the agent's interpretive lens and vocabulary:

```
╔═══════════════════════════════════════════════════════════════════════╗
║              IDENTITY DESIGN                                           ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ INTERPRETIVE LENS                                               │   ║
║  ├────────────────────────────────────────────────────────────────┤   ║
║  │ You interpret all {domain} work through a lens of              │   ║
║  │ {interpretive-frame}—{how this shapes analysis and decisions}. │   ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                                                                        ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ VOCABULARY (15-20 domain terms)                                 │   ║
║  ├────────────────────────────────────────────────────────────────┤   ║
║  │ {term-1}, {term-2}, {term-3}, {term-4}, {term-5},              │   ║
║  │ {term-6}, {term-7}, {term-8}, {term-9}, {term-10},             │   ║
║  │ {term-11}, {term-12}, {term-13}, {term-14}, {term-15}          │   ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                                                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║  [C] Confirm identity design                                           ║
║  [E] Edit interpretive lens                                            ║
║  [V] Edit vocabulary                                                   ║
╚═══════════════════════════════════════════════════════════════════════╝
```

## Step 5: Instruction Authoring

Generate instructions following tier template:

```
╔═══════════════════════════════════════════════════════════════════════╗
║              INSTRUCTION AUTHORING                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  Tier: Expert (~1500 tokens, 15-20 instructions)                      ║
║                                                                        ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ ALWAYS SECTION (4-5 non-negotiable behaviors)                   │   ║
║  ├────────────────────────────────────────────────────────────────┤   ║
║  │ 1. {always-behavior-1}                                          │   ║
║  │ 2. {always-behavior-2}                                          │   ║
║  │ 3. {always-behavior-3}                                          │   ║
║  │ 4. {always-behavior-4}                                          │   ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                                                                        ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ NEVER SECTION (explicit anti-patterns)                          │   ║
║  ├────────────────────────────────────────────────────────────────┤   ║
║  │ - {never-1}                                                     │   ║
║  │ - {never-2}                                                     │   ║
║  │ - {never-3}                                                     │   ║
║  │ - {never-4}                                                     │   ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                                                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║  [C] Confirm instructions                                              ║
║  [E] Edit always section                                               ║
║  [N] Edit never section                                                ║
║  [M] Edit mode-specific instructions                                   ║
╚═══════════════════════════════════════════════════════════════════════╝
```

## Step 6: Tooling & MCP

Configure tools and MCP servers following MCP-INTEGRATION.md:

```
╔═══════════════════════════════════════════════════════════════════════╗
║              TOOLING & MCP CONFIGURATION                               ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  Tool Modes:                                                           ║
║    audit:    Read, Grep, Glob, Bash                                   ║
║    solution: Read, Write, Edit, Grep, Glob, Bash                      ║
║    research: Read, Grep, Glob, Bash, WebSearch, WebFetch              ║
║    default:  {recommended-default}                                     ║
║                                                                        ║
║  MCP Servers (based on domain):                                        ║
║    ┌──────────────────────────────────────────────────────────────┐   ║
║    │ github                                                        │   ║
║    │   Purpose: Repository exploration and code examples           │   ║
║    │                                                               │   ║
║    │ {domain-specific-mcp}                                         │   ║
║    │   Purpose: {what it provides}                                 │   ║
║    └──────────────────────────────────────────────────────────────┘   ║
║                                                                        ║
║  Proactive Triggers:                                                   ║
║    - "{trigger-pattern-1}"                                            ║
║    - "{trigger-pattern-2}"                                            ║
║    - "{trigger-pattern-3}"                                            ║
║                                                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║  [C] Confirm configuration                                             ║
║  [T] Edit tool modes                                                   ║
║  [M] Edit MCP servers                                                  ║
║  [P] Edit proactive triggers                                           ║
╚═══════════════════════════════════════════════════════════════════════╝
```

## Step 7: Synthesis & Validation

Generate the complete agent and validate:

```
╔═══════════════════════════════════════════════════════════════════════╗
║              AGENT SYNTHESIS                                           ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  Generating complete agent definition...                               ║
║                                                                        ║
║  Validation Results:                                                   ║
║    ✓ Frontmatter complete (name, tier, model, tools, modes)           ║
║    ✓ Identity section present                                          ║
║    ✓ Instructions section present (18 instructions)                    ║
║    ✓ Never section present (6 anti-patterns)                          ║
║    ✓ Specializations defined (3 areas)                                ║
║    ✓ Knowledge sources documented (4 sources)                         ║
║    ✓ Output format specified                                          ║
║    ✓ Token estimate: ~1450 (within Expert tier budget)                ║
║                                                                        ║
║  Target Location:                                                      ║
║    agents/-03-agents/{category}/{subcategory}/{agent-name}.md         ║
║                                                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║  [S] Save agent                                                        ║
║  [P] Preview full definition                                           ║
║  [E] Edit before saving                                                ║
╚═══════════════════════════════════════════════════════════════════════╝
```

## Curation Record

After saving, create curation record:

```json
{
  "agent": "{agent-name}",
  "file": "agents/-03-agents/{category}/{subcategory}/{agent-name}.md",
  "created": "{timestamp}",
  "provisioned_by": "agent-provisioner",
  "tier": "expert",
  "knowledge_sources": {
    "count": 4,
    "authority_tiers": [1, 2, 2, 3]
  },
  "human_adjudications": 12,
  "curation_complete": true
}
```

Save to: `.claude/curation-logs/{agent-name}.json`

## Signals

| Signal | Meaning |
|--------|---------|
| `AGENT_PROVISIONING_STARTED` | New agent creation begun |
| `AGENT_DOMAIN_CONFIRMED` | Domain analysis approved |
| `AGENT_TIER_CONFIRMED` | Tier classification approved |
| `AGENT_KNOWLEDGE_COMPLETE` | Knowledge research finished |
| `AGENT_IDENTITY_COMPLETE` | Identity design approved |
| `AGENT_INSTRUCTIONS_COMPLETE` | Instructions authored |
| `AGENT_PROVISIONED` | Agent saved and registered |

## Integration with Hooks

The `agent-creation-validator.sh` hook detects agents created outside this workflow
and flags them for curation. Setting `AGENT_CURATION_ENFORCEMENT=BLOCK` will
reject any agent file writes that don't have a curation record.

## Never

- Skip knowledge research phase
- Bulk-add sources without human adjudication
- Create agents without proper tier classification
- Save agents without validation against CURATION-CHECKLIST.md
- Allow duplicate agents without explicit differentiation
