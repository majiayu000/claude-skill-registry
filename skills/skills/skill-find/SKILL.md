---
name: skill-find
description: Find and install skills from SkillsMP marketplace (skillsmp.com). Use when users want to discover new skills, search for capabilities, or install skills from the marketplace. Supports keyword search and AI semantic search across 63,000+ agent skills.
---

# Skill Find

## Overview

[TODO: 1-2 sentences explaining what this skill enables]

## Overview

Search and install skills from SkillsMP (skillsmp.com), a marketplace with 63,000+ agent skills for Claude, Codex, and ChatGPT.

## Search Skills

**Keyword Search:**
```bash
python scripts/skillsmp_api.py search "SEO optimization"
```

**AI Semantic Search (understands natural language):**
```bash
python scripts/skillsmp_api.py ai-search "skills for analyzing financial data"
```

## Install a Skill

```bash
python scripts/skillsmp_api.py install <skill-url>
```

Example:
```bash
python scripts/skillsmp_api.py install https://skillsmp.com/skills/author-repo-skill-name
```

## API Endpoints

- **Search**: `GET /api/v1/skills/search?q={query}`
- **AI Search**: `GET /api/v1/skills/ai-search?q={query}`

Both require Bearer token authentication.

## Usage Examples

1. Find SEO skills: `search "SEO"`
2. Find data skills: `ai-search "analyze CSV files and create reports"`
3. Find trading skills: `ai-search "stock market trading automation"`


## Resources

This skill includes example resource directories:

### scripts/
Executable code (Python/Bash/etc.) that can be run directly.

### references/
Documentation and reference material to be loaded into context as needed.

### assets/
Files used within the output Claude produces (templates, images, fonts, etc.).

**Any unneeded directories can be deleted.**
