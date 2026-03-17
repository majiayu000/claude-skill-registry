---
name: Knowledge Updater
description: Automated skill for keeping AI knowledge bases current with latest model versions, framework updates, and best practices
version: 1.0.0
last_updated: 2026-01-06
external_version: "Self-updating"
triggers:
  - update knowledge
  - check versions
  - outdated
  - latest versions
---

# Knowledge Updater Skill

## Purpose
Automate the process of keeping AI architecture knowledge current by systematically checking and updating version references across the toolkit.

## Why This Matters

AI evolves rapidly:
- GPT-5.2 released December 2025 (just weeks ago)
- Claude Opus 4.5 released November 2025
- Next.js moved from 15 → 16 in months
- Framework versions change weekly

Stale knowledge = bad recommendations = lost credibility.

## Update Workflow

### Step 1: Discover Current Versions

**LLM Models** (check monthly)
```
Search: "[Provider] latest model [current year]"
- OpenAI: GPT-5.x series
- Anthropic: Claude Opus/Sonnet versions
- Google: Gemini versions
- Meta: Llama versions
- Mistral: Latest releases
```

**Agent Frameworks** (check weekly)
```
Sources:
- Vercel AI SDK: https://github.com/vercel/ai/releases
- OpenAI Agents: https://github.com/openai/openai-agents-python/releases
- LangGraph: https://github.com/langchain-ai/langgraph/releases
- Claude SDK: Check Anthropic announcements
```

**Frontend** (check monthly)
```
Sources:
- Next.js: https://github.com/vercel/next.js/releases
- React: https://github.com/facebook/react/releases
```

**AI Gateways** (check monthly)
```
- OpenRouter: Check model count at openrouter.ai/models
- New providers/features
```

### Step 2: Compare Against VERSION-TRACKING.md

Read current versions from `dev-docs/VERSION-TRACKING.md` and identify deltas.

### Step 3: Update Files

**If changes detected:**

1. **VERSION-TRACKING.md**
   - Update version numbers
   - Update `Last Updated` date
   - Add any new technologies

2. **Affected Skills**
   ```yaml
   # In skills/*/SKILL.md frontmatter:
   version: X.Y.Z → X.Y.(Z+1)  # Increment patch
   last_updated: [today]
   external_version: "[new version]"
   ```

3. **CLAUDE.md** (if model changes)
   - Update model selection table
   - Update pricing if changed

4. **CONTEXT.md**
   - Add entry to Recent Changes table

### Step 4: Generate Report

```markdown
## Knowledge Update Report - [DATE]

### Summary
- Technologies checked: X
- Updates found: Y
- Files modified: Z

### Version Changes
| Technology | Previous | Current | Source |
|------------|----------|---------|--------|
| GPT | 5.1 | 5.2 | openai.com |
| ... | ... | ... | ... |

### Skills Updated
- skills/openai-agentkit/SKILL.md
- skills/azure-ai-services/SKILL.md

### Action Required
- [ ] Review changes
- [ ] Commit: `git commit -m "chore: update versions [date]"`
- [ ] Push to remote
```

## Automation Patterns

### Cron-Style Schedule
```
Weekly: Every Monday 9 AM
- Run full version check
- Update if changes found
- Generate report

Monthly: First of month
- Deep check including benchmarks
- Update pricing if changed
- Review deprecated technologies
```

### Event-Triggered
```
Triggers:
- User says "outdated", "latest", "current version"
- Major AI announcement detected
- Before `/design-solution` command
```

## Best Practices

### DO
- Always cite sources for version claims
- Preserve existing skill content, only update metadata
- Generate diff-style report showing changes
- Include benchmark scores when available

### DON'T
- Update without verification
- Change skill content beyond metadata
- Skip the report generation
- Forget to update CONTEXT.md changelog

## Version Numbering Convention

For skills:
- **Major (X.0.0)**: Complete rewrite, breaking changes
- **Minor (X.Y.0)**: New sections, significant additions
- **Patch (X.Y.Z)**: Version updates, typo fixes, metadata only

## Integration with Other Commands

```
/update-knowledge → /design-solution
                 ↓
         (ensures latest versions used in recommendations)

/update-knowledge → /commit
                 ↓
         (saves updates to git)
```

---

*Fresh knowledge = accurate recommendations = trusted architect*
