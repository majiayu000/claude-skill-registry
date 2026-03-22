---
name: skill-discovery
description: Automatically discover/load local skills and suggest external skills based on task context
category: Core Universal
---

# Skill: skill-discovery

**classification:** Core Universal  
**tier:** T0 (System Behavior)  
**confidence:** 10/10  
**source:** system-mandatory  
**dependencies:** pre-action, memory-keeper
**aliases:** skill-discovery, automatic-skill-discovery

---

## Purpose

Skill Discovery ensures the agent has the correct domain expertise for every task. It performs two critical functions:
1. **Internal Auto-loading (Phase 0)**: Automatically identifies and loads installed skills based on task context.
2. **External Suggestion**: Proactively identifies gaps and suggests relevant community skills from [skills.sh](https://skills.sh).

---

## Phase 0: Automatic Classification

**Execute BEFORE any tool call.**

### Algorithm

1. **PARSE** request to identify task type and domain.
2. **CLASSIFY** by task type (not language):
   - **Implementation** — Writing code in any language
   - **Testing** — Writing tests, test fixtures, test harnesses
   - **Writing/Documentation** — Prose, READMEs, ADRs, runbooks, API docs
   - **Research/Investigation** — Exploring codebases, understanding systems
   - **Architecture/Design** — System design, patterns, refactoring
   - **Security** — Vulnerability assessment, secure coding, audits
   - **Operations/DevOps** — Deployment, CI/CD, infrastructure, monitoring
   - **Data Analysis** — Metrics, statistics, analysis, reporting
   - **Git/Delivery** — Commits, PRs, releases, version management
   - **Orchestration/Planning** — Task breakdown, delegation, coordination
3. **LOAD** skills from the Internal Skill Selection Matrix matching the task type.
4. **DETECT** programming language (if applicable) and load language-specific skills via codebase detection.
5. **DELEGATE** if complexity warrants (multiple files, architecture decisions, novel problems).

---

## Internal Skill Selection Matrix

| Task Type | Category | Skills |
|-----------|----------|--------|
| **Implementation** (any language) | unspecified-high | clean-code, error-handling, design-patterns |
| **Testing** (any language) | unspecified-high | bdd-workflow, bdd-best-practices, test-fixtures |
| **Writing/Documentation** | writing | documentation-writing, british-english, proof-reader |
| **Research/Investigation** | deep | investigation, research, critical-thinking, epistemic-rigor |
| **Architecture/Design** | ultrabrain | architecture, design-patterns, systems-thinker, domain-modeling |
| **Security** | unspecified-high | security, cyber-security, prove-correctness |
| **Operations/DevOps** | unspecified-high | devops, automation, infrastructure-as-code, monitoring |
| **Data Analysis** | unspecified-high | epistemic-rigor, question-resolver, math-expert |
| **Git/Delivery** | quick | git-master, create-pr, release-management |
| **Orchestration/Planning** | ultrabrain | architecture, systems-thinker, scope-management, estimation |
| **Refactoring** | deep | refactor, clean-code, design-patterns |
| **Performance/Optimization** | unspecified-high | performance, profiling, benchmarking |
| **Debugging/Troubleshooting** | deep | investigation, critical-thinking, logging-observability |

---

## External Skill Suggestion (skills.sh)

Suggest an external skill when ALL local options are exhausted and ANY of these conditions are met:
1. **Unfamiliar technology** — The task involves a library not covered by installed skills.
2. **Explicit skill gap** — The agent recognises it lacks domain expertise.
3. **User signals need** — The user asks for help with a specific technology.
4. **Repeated uncertainty** — 2+ uncertain statements about the same technology in one session.

### Guardrails for Suggestions
- **Max 1 suggestion per session** — Do not nag.
- **User consent required** — NEVER auto-import.
- **70% confidence threshold** — Only suggest when highly confident it helps.
- **Max size 5KB** — Per system convention.

---

## Execution Rules

1. **Classify Context FIRST** - Before tools, before thinking, classify the request context.
2. **Auto-select Internal Skills** - Match keywords from the prompt to the skill matrix.
3. **Inject load_skills** - Ensure all selected skills are injected into the task call.
4. **Identify External Gaps** - If local skills are insufficient, check skills.sh (max once).
5. **Phase 0 Gate** - Prevents proceeding without appropriate skill coverage.

---

## Anti-Patterns

❌ Proceeding without domain-specific skills loaded  
❌ Manual skill loading when skill-discovery is possible  
❌ Suggesting external skills more than once per session  
❌ Auto-importing external skills without explicit user consent  
❌ Loading irrelevant skills that waste token context  

---

## Integration Points

- **Phase 0 gate** - Runs before all other processing.
- **Skill-auto-loader-config.jsonc** - Source of truth for baseline and keyword mappings.
- **Universal Skill** - Always loaded by default.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Core-Universal/Skill Discovery.md`

## Related skills

- `agent-discovery` — routes to specialist agents; skill-discovery loads domain knowledge
- `pre-action` — decision framework that benefits from loaded skills
