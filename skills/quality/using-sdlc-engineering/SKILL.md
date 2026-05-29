---
name: using-sdlc-engineering
description: Use when users request SDLC guidance, CMMI processes, requirements management, design documentation, quality assurance, governance, metrics, or adopting processes on existing projects
---

# SDLC Engineering Router

## Overview

This skill routes SDLC-related requests to the appropriate specialist skill within the axiom-sdlc-engineering skillpack. It detects the project's CMMI maturity level and ensures users receive guidance tailored to their context.

**Core Principle**: Match the right process rigor to the project's needs. Not all projects need Level 3 or 4 formality.

## When to Use

Use this skill when requests involve:
- **Requirements management** (tracking, traceability, change control)
- **Design and architecture** (ADRs, design reviews, coding standards)
- **Quality assurance** (testing, code reviews, verification, validation)
- **Governance and risk** (decision documentation, risk management)
- **Metrics and measurement** (what to measure, how to analyze)
- **Process adoption** (implementing CMMI on existing projects)
- **Platform integration** (GitHub, Azure DevOps implementation patterns)
- **General SDLC questions** (where to start, what process to follow)

**When NOT to use**: Implementation details for specific technologies (Python testing → axiom-python-engineering, security → ordis-security-architect).

## CMMI Level Detection

**Priority order** (check in this sequence):

1. **CLAUDE.md configuration**: Look for `CMMI Target Level: X` or `CMMI Level: X`
2. **User message**: Explicit mention ("Level 2", "Level 3", "Level 4", "CMMI L3")
3. **Context clues**:
   - "FDA", "medical device", "royal commission" → Level 3-4 (regulatory rigor)
   - "startup", "small team", "2-3 developers" → Level 2 (lightweight)
   - "audit", "compliance", "SOC 2" → Level 3 (organizational standards)
4. **Default**: Level 3 (good balance of rigor and agility)

**Level Summary**:
- **Level 2 (Managed)**: Minimal viable practices, ~5% overhead, 1-5 person teams
- **Level 3 (Defined)**: Organizational standards, ~10-15% overhead, 5+ person teams, audit-ready
- **Level 4 (Quantitatively Managed)**: Statistical process control, ~20-25% overhead, regulated industries (FDA, medical devices)

## Routing Decision Tree

```
User request received
  │
  ├─ New project setup / comprehensive adoption?
  │   └─ Route to: lifecycle-adoption
  │       (Bootstrapping guidance, parallel tracks, incremental rollout)
  │
  ├─ Requirements-related? (tracking, traceability, elicitation, changes)
  │   └─ Route to: requirements-lifecycle
  │       (RD + REQM practices at detected level)
  │
  ├─ Design/architecture? (ADRs, design docs, code standards, branching)
  │   └─ Route to: design-and-build
  │       (TS + CM + PI practices at detected level)
  │
  ├─ Quality/testing? (code review, testing strategy, peer review, UAT)
  │   └─ Route to: quality-assurance
  │       (VER + VAL practices at detected level)
  │
  ├─ Decisions/risk? (ADRs, formal decisions, risk management)
  │   └─ Route to: governance-and-risk
  │       (DAR + RSKM practices at detected level)
  │
  ├─ Metrics/measurement? ("what to measure", dashboards, SPC)
  │   └─ Route to: quantitative-management
  │       (MA + QPM + OPP practices at detected level)
  │
  ├─ Platform-specific? (GitHub setup, Azure DevOps setup)
  │   └─ Route to: platform-integration
  │       (GitHub vs Azure DevOps implementation patterns)
  │
  └─ Ambiguous / multiple concerns?
      └─ Ask clarifying question OR provide overview of relevant skills
```

## Routing Table

| User Intent | Route To | Key Indicators |
|-------------|----------|----------------|
| **New project, comprehensive setup** | `lifecycle-adoption` | "starting new", "from day one", "bootstrapping", "where to start" |
| **Existing project adoption** | `lifecycle-adoption` | "existing project", "retrofit", "adopt CMMI", "parallel tracks" |
| **Requirements tracking** | `requirements-lifecycle` | "requirements", "user stories", "traceability", "RTM", "change requests" |
| **Architecture decisions** | `design-and-build` | "design", "architecture", "ADR", "technical decision", "coding standards" |
| **Version control setup** | `design-and-build` | "Git", "branching", "GitFlow", "releases", "configuration management" |
| **Testing strategy** | `quality-assurance` | "testing", "test coverage", "code review", "peer review", "UAT", "validation" |
| **Formal decisions** | `governance-and-risk` | "ADR", "decision documentation", "alternatives analysis" |
| **Risk management** | `governance-and-risk` | "risk", "risk register", "mitigation", "probability×impact" |
| **Metrics planning** | `quantitative-management` | "metrics", "what to measure", "dashboards", "DORA", "KPIs" |
| **Statistical analysis** | `quantitative-management` | "Level 4", "SPC", "control charts", "Cp/Cpk", "process capability" |
| **GitHub implementation** | `platform-integration` | "GitHub", "GitHub Actions", "issue tracking" |
| **Azure DevOps implementation** | `platform-integration` | "Azure DevOps", "Azure Pipelines", "Azure Boards" |
| **General quality improvement** | `quality-assurance` (first), then others | "better quality", "fewer bugs", "improve" (ambiguous) |

## Cross-Skillpack Coordination

**Separation of Concerns**: axiom-sdlc-engineering defines **WHAT** to do (process), other skillpacks define **HOW** (implementation).

| Scenario | SDLC Skill | Implementation Skill | Handoff |
|----------|-----------|---------------------|---------|
| **Python testing** | `quality-assurance` (test strategy) | `axiom-python-engineering` (pytest implementation) | "Use axiom-python-engineering for writing pytest tests" |
| **Python code quality** | `design-and-build` (coding standards) | `axiom-python-engineering` (ruff, mypy, black) | "Use axiom-python-engineering for Python-specific tooling" |
| **UX design reviews** | `quality-assurance` (review process) | `lyra-ux-designer` (design critique) | "Use lyra-ux-designer for UX-specific review criteria" |
| **Security testing** | `quality-assurance` (test strategy) | `ordis-security-architect` (security testing) | "Use ordis-security-architect for security test cases" |
| **Documentation writing** | `governance-and-risk` (ADR process) | `muna-technical-writer` (technical writing) | "Use muna-technical-writer for documentation structure" |
| **E2E testing** | `quality-assurance` (test pyramid) | `ordis-quality-engineering` (E2E automation) | "Use ordis-quality-engineering for E2E test frameworks" |

**Key Rule**: If the request is about **process/policy** → SDLC skill. If it's about **tool/technology implementation** → domain-specific skillpack.

## Handling Ambiguous Requests

When multiple skills could apply:

**Option 1: Ask Clarifying Question**
```
"I can help with quality improvement in several ways:
1. Testing strategy and code reviews (quality-assurance skill)
2. Design practices and architecture (design-and-build skill)
3. Metrics to track quality (quantitative-management skill)

Which aspect of quality are you most concerned about?"
```

**Option 2: Provide Overview**
```
"Quality improvement involves multiple CMMI process areas:
- Requirements quality (requirements-lifecycle): Clear, testable requirements
- Design quality (design-and-build): Architecture reviews, coding standards
- Test quality (quality-assurance): Test coverage, peer reviews, UAT

I recommend starting with quality-assurance skill for immediate impact on defect rates."
```

## Countering Rationalizations

| Objection | Counter-Response | Route To |
|-----------|------------------|----------|
| "We're too small for CMMI" | "Level 2 works for 1-2 person teams. It's ~5% overhead: basic Git branching, lightweight code review, simple issue tracking." | `lifecycle-adoption` |
| "Process slows us down" | "Process prevents rework. Level 2 saves time: no re-litigating decisions, no integration hell, no forgotten requirements." | `lifecycle-adoption` |
| "We need to ship fast" | "Level 2 speeds delivery: clear requirements (no misunderstandings), CI/CD (no manual deploys), peer review (catch bugs early)." | `lifecycle-adoption` |
| "CMMI is waterfall" | "CMMI is methodology-agnostic. GitHub Flow + CI/CD + user stories = Level 3 compliance. Agile and CMMI coexist." | `lifecycle-adoption` |
| "Too much documentation" | "Level 2 minimizes docs: ADRs in markdown (15 min), requirements in GitHub Issues, traceability via commit messages." | `design-and-build` |
| "We don't have time to measure" | "Level 3 automates metrics via GitHub API. 1-hour setup, then free data forever. No manual spreadsheets." | `quantitative-management` |

## Red Flags - Stop and Reconsider

**Symptoms of wrong routing**:
- User asks about **implementation** (pytest setup, GitHub Actions YAML) → Wrong, should route to implementation skillpack
- User asks about **domain-specific** practices (ML experiment tracking, UX wireframes) → Wrong, should route to domain skillpack
- User asks **how to write code** → Wrong, SDLC is about process, not coding
- User needs **technology tutorial** → Wrong, SDLC assumes technical competence

**Correct routing examples**:
- "What testing strategy should I use?" → `quality-assurance` (process question)
- "How do I write pytest fixtures?" → `axiom-python-engineering` (implementation)
- "What metrics should we track?" → `quantitative-management` (process question)
- "How do I query GitHub API?" → `platform-integration` (implementation detail)

## Multi-Skill Roadmaps

For comprehensive requests, provide sequenced guidance:

**Example: "Starting new Level 3 project"**
1. **First**: `lifecycle-adoption` → Assess current state, plan rollout
2. **Then**: `platform-integration` → Choose and configure GitHub/Azure DevOps
3. **Then**: `requirements-lifecycle` → Set up requirements tracking
4. **Then**: `design-and-build` → Establish branching, ADR process, coding standards
5. **Then**: `quality-assurance` → Define test strategy, code review policy
6. **Then**: `governance-and-risk` → Set up risk register, decision documentation
7. **Then**: `quantitative-management` → Define metrics, establish baselines

**Example: "Adopting on existing 6-month-old project"**
1. **First**: `lifecycle-adoption` → Parallel tracks strategy (new work = new process)
2. **Then**: `design-and-build` → Git branching cleanup, start ADRs for new decisions
3. **Then**: `requirements-lifecycle` → Capture current requirements, traceability for new work
4. **Then**: `quality-assurance` → Add tests for new code, code review for new PRs
5. **Later**: `quantitative-management` → Metrics after 2-3 months of data

## Routing Workflow

1. **Detect CMMI Level**: Check CLAUDE.md → user message → default to Level 3
2. **Analyze Request Intent**: Match against routing table for keywords/symptoms
3. **Check Routing Table**: Find the skill(s) that best match the user's needs
4. **Determine Single Skill OR Multi-Skill Sequence**: Single concern vs. multi-skill roadmap
5. **Announce Routing Decision**: "I'm routing you to [skill-name] for [reason]. CMMI Level detected: [X]"
6. **Invoke Appropriate Skill**: Use Skill tool to load the skill
7. **Follow Loaded Skill Exactly**: Defer to the specialist skill's guidance

## Quick Reference

**Default Routing** (when in doubt):
- Process adoption questions → `lifecycle-adoption`
- Requirements questions → `requirements-lifecycle`
- Design/architecture questions → `design-and-build`
- Testing/quality questions → `quality-assurance`
- Decision/risk questions → `governance-and-risk`
- Metrics questions → `quantitative-management`
- Tool setup questions → `platform-integration`

**Default Level**: Level 3 (unless otherwise specified)

**Cross-Skillpack Default**: If request is about technology implementation (not process), route to appropriate domain skillpack (axiom-python-engineering, ordis-quality-engineering, etc.)

## Success Criteria

Router is effective when:
- [ ] CMMI level detected correctly from all sources
- [ ] Requests routed to correct skill 95%+ of time
- [ ] Ambiguous requests result in clarifying questions, not guesses
- [ ] Cross-skillpack boundaries respected (process vs. implementation)
- [ ] Multi-skill roadmaps provided when needed
- [ ] Rationalizations countered with evidence-based responses
- [ ] Users understand WHY they were routed to specific skill

## Common Mistakes to Avoid

**❌ Don't**: Guess at CMMI level if not specified → Default to Level 3
**❌ Don't**: Route technology questions here → Send to domain skillpacks
**❌ Don't**: Provide process guidance directly → Load appropriate skill
**❌ Don't**: Skip level detection → Always check CLAUDE.md first
**❌ Don't**: Overwhelm with all 7 skills → Route to most relevant one

**✅ Do**: Detect level systematically (CLAUDE.md → message → default)
**✅ Do**: Announce routing decision ("Routing to X skill because...")
**✅ Do**: Load the skill and follow it exactly
**✅ Do**: Provide multi-skill roadmap for complex requests
**✅ Do**: Counter "process = overhead" rationalizations with Level 2 examples
