---
name: "skillsmith"
description: "Discover, install, compare, and manage Claude Code skills. Search the registry, get recommendations, validate skill quality, and manage your installed skills."
version: "0.1.0"
category: "productivity"
tags:
  - skills
  - discovery
  - registry
  - mcp
  - installation
author: "Skillsmith"
allowed-tools:
  - mcp__skillsmith
  - Bash
---

# Skillsmith Skill

Discover, install, compare, and manage Claude Code skills through natural language.

## Trigger Phrases

- "search for skills", "find skills", "discover skills"
- "install skill", "add skill"
- "recommend skills", "suggest skills"
- "compare skills"
- "validate skill", "check skill"
- "list installed skills", "show my skills"
- "uninstall skill", "remove skill"
- "skill details", "get skill"
- "browse skills", "explore skills"
- "high quality skills", "verified skills"

## Slash Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/skillsmith search` | Search for skills by query or filters | `/skillsmith search testing` |
| `/skillsmith install` | Install a skill from the registry | `/skillsmith install community/jest-helper` |
| `/skillsmith recommend` | Get contextual skill recommendations | `/skillsmith recommend` |
| `/skillsmith compare` | Compare multiple skills side-by-side | `/skillsmith compare jest-helper vitest-helper` |
| `/skillsmith validate` | Validate a skill's structure | `/skillsmith validate ./my-skill` |
| `/skillsmith list` | List all installed skills | `/skillsmith list` |
| `/skillsmith uninstall` | Remove an installed skill | `/skillsmith uninstall jest-helper` |
| `/skillsmith get` | Get detailed skill information | `/skillsmith get community/jest-helper` |

## MCP Tool Delegation

This skill delegates to the `mcp__skillsmith` MCP server for all operations. When the user requests skill-related actions, use the appropriate MCP tool.

**Note:** The examples below show the tool parameters. Invoke these using Claude's standard MCP tool calling mechanism.

### Search for Skills

Use `mcp__skillsmith__search` with these parameters:
- `query` (optional): Search term
- `category` (optional): development, testing, devops, etc.
- `trust_tier` (optional): verified, community, experimental
- `min_score` (optional): Minimum quality score (0-100)
- `limit` (optional): Max results (default 10)

**Example:** Search for testing skills with quality score > 70
```json
{
  "query": "testing",
  "min_score": 70,
  "limit": 10
}
```

**Note:** Either `query` OR at least one filter (`category`, `trust_tier`, `min_score`) must be provided.

### Get Skill Details

Use `mcp__skillsmith__get_skill` with:
- `id` (required): Skill ID in format `author/name`

```json
{ "id": "community/jest-helper" }
```

### Install a Skill

Use `mcp__skillsmith__install_skill` with:
- `id` (required): Skill ID
- `force` (optional): Overwrite if exists

```json
{ "id": "community/jest-helper", "force": false }
```

### Uninstall a Skill

Use `mcp__skillsmith__uninstall_skill` with:
- `id` (required): Skill name

```json
{ "id": "jest-helper" }
```

### Get Recommendations

Use `mcp__skillsmith__skill_recommend` with:
- `context` (optional): Project context
- `limit` (optional): Max recommendations

```json
{ "context": "React TypeScript project", "limit": 5 }
```

### Compare Skills

Use `mcp__skillsmith__skill_compare` with:
- `skill_ids` (required): Array of 2-5 skill IDs to compare

```json
{ "skill_ids": ["community/jest-helper", "community/vitest-helper"] }
```

### Validate a Skill

Use `mcp__skillsmith__skill_validate` with:
- `path` (required): Path to skill directory

```json
{ "path": "./my-skill" }
```

## Usage Examples

### Example 1: Search and Install

User: "Find testing skills for React"

1. Search for skills using `mcp__skillsmith__search`:
   ```json
   { "query": "testing React" }
   ```

2. Present results to user with quality scores and trust tiers

3. If user selects one, install using `mcp__skillsmith__install_skill`:
   ```json
   { "id": "community/react-testing-library-helper" }
   ```

### Example 2: Get Recommendations

User: "What skills would help with this codebase?"

1. Analyze current project context (package.json, file types, etc.)

2. Get recommendations using `mcp__skillsmith__skill_recommend`:
   ```json
   { "context": "Node.js TypeScript API with Express" }
   ```

3. Present recommendations with explanations

### Example 3: Compare Options

User: "Compare jest-helper and vitest-helper"

Use `mcp__skillsmith__skill_compare`:
```json
{ "skill_ids": ["community/jest-helper", "community/vitest-helper"] }
```

Present comparison table showing features, quality scores, trust tiers, etc.

### Example 4: Browse by Category

User: "Show me verified security skills"

Use `mcp__skillsmith__search`:
```json
{ "category": "security", "trust_tier": "verified" }
```

### Example 5: Quality-Based Search

User: "Find high-quality DevOps skills"

Use `mcp__skillsmith__search`:
```json
{ "category": "devops", "min_score": 80 }
```

## Trust Tiers

| Tier | Description | Badge |
|------|-------------|-------|
| `verified` | Official Anthropic or partner skills | Green |
| `community` | Community-reviewed and approved | Yellow |
| `experimental` | New or beta skills, use with caution | Red |

## Quality Scores

Quality scores (0-100) reflect skill quality based on:

- Repository health (stars, forks, activity)
- Documentation completeness
- Code quality indicators
- Community engagement

Recommended minimum scores:
- Production use: 70+
- General use: 50+
- Experimental: Any

## CLI Fallback

If the MCP server is unavailable, use the CLI directly:

```bash
# Search
skillsmith search "testing" --tier verified

# Install
skillsmith install community/jest-helper

# List installed
skillsmith list

# Remove
skillsmith remove jest-helper
```

## Related Commands

- `skillsmith analyze` - Analyze codebase for skill recommendations
- `skillsmith sync` - Sync skills from registry
- `skillsmith author init` - Create a new skill
- `skillsmith author validate` - Validate skill structure
