---
name: sdk
description: Skill SDK utilities for loading, registering, and managing skills with caching and auto-selection
---

# Skill SDK

This is not a user-facing skill - it's a **utility SDK** that provides infrastructure for the skill system.

## Purpose

The SDK directory contains core utilities that power the skill system:

1. **skill-loader.mjs**: Loads skill instructions and metadata with intelligent caching
2. **skill-registry.mjs**: Registers skills and integrates with Anthropic Agent SDK patterns

## Components

### skill-loader.mjs

Provides functions for loading and caching skill instructions:

- `loadSkillInstructions(skillName, useCache)`: Load skill instructions from SKILL.md
- `loadSkillMetadata(skillName)`: Extract YAML frontmatter metadata
- `getAllSkillNames()`: Get list of all available skills
- `autoSelectSkills(query, maxResults)`: Intelligently select skills based on query
- `clearCache()`: Clear skill cache
- `getCacheStats()`: Get cache statistics

**Caching**: Skills are cached in `.claude/context/cache/skill-cache.json` for performance.

### skill-registry.mjs

Integrates skills with Anthropic Agent SDK patterns:

- `registerSkill(skillName)`: Register a skill and parse its metadata
- `getAllSkills()`: Get all registered skills
- `getSkill(skillName)`: Retrieve a registered skill
- `registerSkillWithSDK(skillName)`: Create SDK-compatible skill object
- `initializeSkills()`: Initialize all skills on startup
- `invokeSkill(skillName, input, context)`: Invoke a skill with context
- `createSDKSkill(skillConfig)`: Create SDK skill instance

## Usage

These utilities are used internally by the skill system and skill-manager. They are not invoked directly by users.

**Example (internal use)**:

```javascript
import { loadSkillInstructions, autoSelectSkills } from '.claude/skills/sdk/skill-loader.mjs';

// Load specific skill
const instructions = await loadSkillInstructions('rule-auditor');

// Auto-select relevant skills
const skills = await autoSelectSkills('audit code for violations', 3);
// Returns: ['rule-auditor', 'code-style-validator', 'fixing-rule-violations']
```

## Skill Format

All skills must follow this format in their SKILL.md:

```markdown
---
name: skill-name
description: Brief description
allowed-tools: tool1, tool2
version: 1.0.0
---

# Skill Instructions

Detailed instructions for the skill...
```

## Auto-Selection Algorithm

The auto-selection algorithm scores skills based on:

1. **Name match** (10 points): Skill name contains query words
2. **Description match** (5 points per word): Description contains query words
3. **Tool match** (3 points per word): Allowed tools contain query words

Top N skills by score are returned.

## Cache Management

- **Cache Location**: `.claude/context/cache/skill-cache.json`
- **Cache Contents**: Skill instructions and metadata
- **Cache Invalidation**: Manual via `clearCache()` or by deleting cache file
- **Performance**: 90%+ reduction in disk I/O for repeated skill loads

## Integration Points

The SDK is used by:

- **skill-manager**: Managing and validating all skills
- **Skill tool invocations**: Loading skill instructions when invoked
- **Auto-selection**: Finding relevant skills for user queries
- **Workflow execution**: Loading skills for workflow steps

## Notes

- This is **infrastructure code**, not a user-facing skill
- Do not invoke this skill directly
- Do not create prompts or commands that reference this skill
- This directory should contain only utility modules for the skill system
