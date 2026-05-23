---
name: research
description: Systematic research before planning - gather documentation, security concerns, tech stack analysis, and community insights. Use when user says "let's research", "research this", "investigate", "look into", or needs to understand a technology or feature before planning.
allowed-tools: Read, Edit, Glob, Grep, Task, WebFetch, WebSearch
---

# Research Skill

Conducts systematic research and creates living documents in `_RESEARCH/`.

## When to Use
- Before planning new features
- Evaluating technologies
- Security research
- Understanding dependencies

## Workflow

### Step 1: Parse Research Topic
1. Extract topic from user input
2. Normalize to SCREAMING_SNAKE_CASE for filename
3. Check if `_RESEARCH/[TOPIC].md` already exists

### Step 2: Spawn Parallel Research Tasks
Use Task tool to run these in parallel:

**Documentation Research:**
- Find official documentation
- Identify API references
- Locate getting started guides
- Check for migration guides

**Security Research:**
- Search for known CVEs
- Find security advisories
- Identify auth/authz concerns
- Check dependency vulnerabilities

**Tech Stack Analysis:**
- Identify required dependencies
- Check Node.js/browser compatibility
- Analyze bundle size implications
- Find TypeScript definitions

**Community Research:**
- Search GitHub issues for common problems
- Find Stack Overflow discussions
- Identify known gotchas
- Gather performance tips

### Step 3: Consolidate Findings
1. Merge findings into structured document
2. Identify conflicts between sources
3. Assign confidence levels
4. Highlight critical risks

### Step 4: Create/Update Research Document
Save to `_RESEARCH/[TOPIC].md` using the template format.

## Research Freshness
- **Fresh** (0-14 days): Current and reliable
- **Aging** (15-30 days): Consider refreshing for major decisions
- **Stale** (30+ days): Update before using in plans

## Output Format
```
## Research Complete: [Topic]

### Key Findings
- Finding 1
- Finding 2
- Finding 3

### Critical Risks
- Risk 1 (if any)
- Risk 2 (if any)

### Confidence: High/Medium/Low

Document saved: _RESEARCH/[TOPIC].md

Next steps:
- Review full research document
- "make a plan for..." to create implementation plan
- "update research on..." to gather more information
```
