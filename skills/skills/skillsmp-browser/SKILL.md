---
name: skillsmp-browser
description: "Browse and compare skills from SkillsMP and Anthropic's official repo. Use when user says 'browse skills', 'skillsmp', 'find skills', or 'skill marketplace'."
allowed-tools: Read, Bash, Glob, Grep, WebFetch, WebSearch, AskUserQuestion
---

# skillsmp-browser (Skills Ecosystem Explorer)

You are helping the user explore and compare skills from external marketplaces against their installed ONE_SHOT skills.

## When To Use

- User says "browse skills", "skillsmp", "find skills"
- User wants to discover new skills for Claude Code
- User asks about skill alternatives or comparisons
- User says "what skills are available"

## Skills Ecosystem Overview

### Official Anthropic Skills
- **Repo**: github.com/anthropics/skills (43k stars)
- **Skills**: Document creation, testing, MCP generation
- **Install**: `/plugin marketplace add anthropics/skills`

### SkillsMP (Community)
- **Site**: skillsmp.com (63k+ skills)
- **Categories**: Engineering, Code Ops, Productivity, Visual Docs
- **Install**: `/plugin install <skill-name>@skillsmp`

### ONE_SHOT (Installed)
- **Location**: ~/.claude/skills/oneshot/
- **Skills**: 20 core + 17 advanced (37 total)
- **Focus**: Full-stack development workflows

## Workflow

### 1. Check Installed Skills

First, list what's already installed:

```bash
ls ~/.claude/skills/oneshot/ | grep -v INDEX | grep -v TEMPLATE | head -20
```

### 2. Show ONE_SHOT vs External Comparison

| ONE_SHOT Skill | Similar External | Notes |
|----------------|------------------|-------|
| git-workflow | git-pushing@anthropic | ONE_SHOT has conventional commits |
| test-runner | test-fixing@anthropic | Similar approach |
| code-reviewer | code-auditor@skillsmp | ONE_SHOT includes OWASP |
| debugger | debug-guru@skillsmp | ONE_SHOT is hypothesis-based |
| create-plan | architect@skillsmp | ONE_SHOT integrates with beads |
| front-door | - | Unique to ONE_SHOT |
| beads | - | Unique to ONE_SHOT |

### 3. Browse External Skills

Use web search to find skills by category:

```javascript
WebSearch({
  query: "site:github.com anthropics/skills OR site:skillsmp.com [category] skill"
})
```

**Popular categories to search:**
- "document creation" - DOCX, PDF, PPTX
- "API testing" - REST, GraphQL validation
- "data analysis" - pandas, visualization
- "devops" - Docker, Kubernetes, CI/CD

### 4. Install External Skills (If User Wants)

```bash
# Add official marketplace
/plugin marketplace add anthropics/skills

# Install specific skill set
/plugin install document-skills@anthropic-agent-skills

# Install from SkillsMP (requires marketplace.json)
/plugin install <skill-name>@skillsmp
```

## Comparison Criteria

When comparing skills, evaluate:

| Criteria | Weight | Question |
|----------|--------|----------|
| Overlap | High | Does ONE_SHOT already cover this? |
| Integration | High | Works with beads/handoff? |
| Quality | Medium | Well-documented? Maintained? |
| Complexity | Medium | Token cost when loaded? |
| Uniqueness | Low | Novel capability? |

## Recommendation Engine

Based on ONE_SHOT gaps, these external skills add value:

### Worth Installing
- **document-skills** (Anthropic) - DOCX/PPTX creation not in ONE_SHOT
- **data-viz** (SkillsMP) - Visualization beyond basic charts
- **mcp-generator** (Anthropic) - MCP server scaffolding

### Already Covered (Skip)
- git-workflow alternatives → ONE_SHOT git-workflow is better
- debugging tools → ONE_SHOT debugger is comprehensive
- planning tools → ONE_SHOT create-plan + beads is superior

## API Key (Optional)

SkillsMP premium features may require an API key. To store:

```bash
# Decrypt, add key, re-encrypt
cd ~/github/oneshot
sops secrets/secrets.env.encrypted
# Add: SKILLSMP_API_KEY=sk_live_skillsmp_xxx
# Save and exit
```

Then reference in skills as `$SKILLSMP_API_KEY`.

## Anti-Patterns

- Installing duplicate functionality (ONE_SHOT already covers)
- Adding heavy skills that inflate context (>500 tokens base)
- Using skills without understanding their tool requirements
- Installing untested/unmaintained community skills

## Keywords

skillsmp, browse skills, skill marketplace, find skills, compare skills, external skills, anthropic skills, install skill
