---
name: skill-arosstale-pi-pai
description: Advanced prompt engineering skill for pi-mono ecosystem.
---

# Prompting Skill Pack

## Overview
Advanced prompt engineering skill for pi-mono ecosystem.

## Triggers
- "optimize prompt"
- "refine prompt"
- "prompt engineering"
- "meta-prompt"

## Capabilities

### Prompt Optimization
```typescript
// Optimize prompt for better results
const optimized = await pai.optimizePrompt({
  prompt: 'Tell me about X',
  target: 'clarity',
  metrics: ['length', 'specificity', 'context']
});
```

### Template Generation
```typescript
// Generate prompt template
const template = await pai.generateTemplate({
  task: 'code-review',
  variables: ['code', 'language', 'requirements'],
  style: 'structured'
});
```

### Meta-Prompting
```typescript
// Generate meta-prompt for self-improvement
const metaPrompt = await pai.generateMetaPrompt({
  basePrompt: 'Assist with X',
  improvementGoal: 'accuracy',
  context: 'technical'
});
```

## Integration with pi-mono
- Agentic Horizon: Agentic prompt engineering
- Act-Learn-Reuse: Prompt learning
- Discord Bot: `/ask` command optimization

## Installation
```bash
# Copy skill to pi-mono
cp src/packs/skill/prompting-skill.md /home/majinbu/organized/active-projects/pi-mono/packages/discord-bot/src/skills/

# Register in Discord bot
/discord reload-skills
```
