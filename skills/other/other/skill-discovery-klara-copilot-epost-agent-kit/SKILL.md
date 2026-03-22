---
name: skill-discovery
description: (ePost) Use at the START of every task to discover and load relevant skills you don't already have. Detects platform, task type, and domain signals then loads matching skills from the index on demand.
user-invocable: false
tier: core

metadata:
  agent-affinity: [epost-planner, epost-fullstack-developer, epost-debugger, epost-tester, epost-code-reviewer, epost-project-manager]
  keywords: [platform, discovery, skill-index, context, conventions, lazy-loading]
  platforms: [all]
  triggers: []
---

# Skill Discovery

Context-aware lazy loader. Discovers and loads skills on-demand based on task signals instead of loading everything at startup.

## When to Activate

Run this protocol at the START of every task. Skip only when:
- Task is trivially simple (single-line fix, typo correction)
- All needed skills are already loaded in your `skills:` list
- Task is purely conversational (no code/architecture work)

## Step 1: Detect Task Signals

Gather signals from three sources:

### 1a. Platform Signals
Check request keywords → git diff extensions → CWD path:

| Signal | Platform | Skills to Load |
|--------|----------|---------------|
| `.swift`, "iOS", "Swift", "SwiftUI" | ios | `ios-development`, `ios-ui-lib` |
| `.kt/.kts`, "Android", "Kotlin", "Compose" | android | `android-development`, `android-ui-lib` |
| `.tsx/.ts/.jsx/.scss`, "React", "Next.js", "web" | web | `web-frontend`, `web-nextjs` |
| `.java` + `pom.xml`, "Java EE", "WildFly", "backend" | backend | `backend-javaee`, `backend-databases` |
| `epost-agent-kit-cli/` path, `src/domains/`, "CLI", "kit cli" | cli | `kit-cli` |
| `.css/.scss` + design tokens, "Figma", "klara" | design | `figma`, `web-ui-lib` |

Multiple platforms: ask user (max 1 question). If 80%+ files = one platform, use that.

### Platform Detection Priority
1. **Explicit hint** in user request ("ios", "web", etc.) → highest priority
2. **File extensions** in `git diff` or `$ARGUMENTS` paths → high
3. **CWD path** segments (e.g., inside `ios/`, `android/`) → medium
4. **Project markers** (`Package.swift` → ios, `build.gradle.kts` → android, `package.json` → web, `pom.xml` → backend) → low

### 1b. Task Type Signals
Scan the user request for these patterns:

| Signal Words | Task Type | Likely Skills |
|-------------|-----------|---------------|
| error, stack trace, crash, bug, failing | debug | problem-solving, error-recovery |
| docs, library, API reference, how to use | research | docs-seeker, research |
| ADR, prior art, existing pattern, similar | knowledge | knowledge-retrieval |
| write docs, spec, proposal, RFC | documentation | doc-coauthoring |
| retry, timeout, circuit breaker, fallback | resilience | error-recovery |
| step by step, complex, analyze, root cause | reasoning | sequential-thinking, problem-solving |
| repo overview, codebase summary | exploration | repomix |
| a11y, accessibility, WCAG, VoiceOver | accessibility | a11y + platform-a11y variant |
| Figma, design tokens, components, theme | design system | figma, web-ui-lib |
| Docker, container, GCP, Terraform | infrastructure | infra-docker, infra-cloud |
| B2B module, inbox, monitoring, composer | domain | domain-b2b |
| get started, onboard, begin, new to project | onboarding | get-started |

### 1c. Domain Signals (from git context)
- Files in module-specific directories → domain skills
- Infrastructure files (Dockerfile, terraform/) → infra skills

## Step 2: Query Skill Index

Read `.claude/skills/skill-index.json`. Filter candidates:

```
For each skill in index:
  SKIP if skill.name is in your loaded skills: [] list (already have it)
  SKIP if skill.tier == "core" and not matching signals (core skills load via skills: list)
  MATCH if:
    - skill.name starts with detected platform prefix (ios-, web-, etc.)
    - skill.platforms contains detected platform
    - skill.keywords intersect with detected task type signals
    - skill.agent-affinity includes your agent name
```

## Step 2b: Resolve Dependencies

After matching candidates, resolve their connection graph:

```
For each matched skill:
  1. EXTENDS: Prepend parent(s) to load list. Max 3 hops.
     Example: ios-a11y extends a11y → load a11y first, then ios-a11y
  2. REQUIRES: Add required skills to load list.
     Example: ui-lib-dev requires figma → auto-add
  3. CONFLICTS: If two matched skills conflict, keep higher-priority one.
     Warn: "Dropped {lower} — conflicts with {higher}"
```

**Dependency skills (extends/requires) do NOT count toward the "max 3" direct match limit.**

Load order: bases first (extends parents → requires → matched skill).

## Step 3: Select and Load (Token Budget)

**Hard limits:**
- Max 3 directly matched skills per task (dependencies don't count toward this)
- Max 15 KB total skill content (approximately 3,750 tokens)
- Prefer smaller skills that cover the need

**Ranking (highest → lowest priority):**
1. Platform skills matching detected platform
2. Skills where `agent-affinity` lists your agent name
3. Skills matching task-type signals from Step 1b
4. Skills matching domain signals from Step 1c

**For each selected skill**: Read its SKILL.md. Extract actionable patterns, constraints, conventions. Apply to your task.

**After loading**: Check each loaded skill's `connections.enhances` list. If any enhancers are relevant but not loaded, suggest them:
> "Also available: problem-solving (enhances debugging)"

Do NOT auto-load enhancers. Only suggest them.

## Step 4: Apply Discovered Knowledge

Integrate loaded skill knowledge into your current task:
- **Planner**: Platform constraints in plan phases, framework-specific steps
- **Fullstack Developer**: Code patterns, testing approach, UI components
- **Debugger**: Platform debugging tools, common pitfalls, logging patterns
- **Tester**: Test frameworks, assertion patterns, coverage tools
- **Code Reviewer**: Platform conventions, anti-patterns, security concerns
- **Design System**: Component APIs, platform token mapping, Figma extraction, UI audit patterns
- **Project Manager**: Route to correct specialist, inform task decomposition

## Agent Discovery Hints

Some agents have distinct operational flows (e.g., muji's Library Development vs Consumer Guidance). When an agent's system prompt defines flows with explicit skill lists:

1. Read agent's system prompt for flow definitions and their triggers
2. Detect which flow matches the current task context
3. Load that flow's skills instead of generic platform matching

This overrides Steps 1-2 when a clear flow match exists. Falls back to standard discovery if no flow matches.

## Quick Reference: Common Discovery Paths

| You Are | Task Looks Like | Discover |
|---------|----------------|----------|
| any agent | iOS task (.swift) | ios-development, ios-ui-lib |
| any agent | Android task (.kt) | android-development, android-ui-lib |
| any agent | Web task (.tsx/.ts) | web-frontend, web-nextjs |
| any agent | Backend task (.java) | backend-javaee, backend-databases |
| any agent | CLI task (epost-agent-kit-cli/) | kit-cli |
| debugger | stuck on bug | sequential-thinking, problem-solving |
| fullstack-developer | API timeout | error-recovery |
| planner | plan with research | research, docs-seeker |
| any agent | a11y + iOS | a11y, ios-a11y |
| any agent | a11y + Android | a11y, android-a11y |
| any agent | a11y + Web | a11y, web-a11y |
| any agent | Figma / design system | figma, web-ui-lib |
| epost-muji | component dev (Figma pipeline) | figma, design-tokens, ui-lib-dev |
| epost-muji | consumer asks about usage | {platform}-ui-lib via platform detection |
| epost-muji | UI audit / review | audit (pre-loaded), ui-guidance |
| epost-muji | token translation question | design-tokens (pre-loaded) |
| any agent | kit authoring | kit-skill-development, kit-agent-development |
