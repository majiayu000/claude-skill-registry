---
name: skillsmp-search
description: "Search SkillsMP marketplace for skills to fill gaps in local inventory. Use when user says 'search skillsmp', 'find skill on skillsmp', or when skill discovery identifies gaps."
allowed-tools: Bash, Read, Write, AskUserQuestion
---

# /skillsmp-search - SkillsMP Integration

**Search and install skills from the SkillsMP marketplace.**

## When To Use

User says:
- `skillsmp search [query]`
- `find skills for [topic] on skillsmp`
- `install skill from skillsmp`
- After skill discovery identifies gaps

## How It Works

1. **Search SkillsMP API** for matching skills
2. **Present results** with name, author, description
3. **Offer to install** if user wants a skill
4. **Update skill inventory** after installation

## Usage

```bash
# Search SkillsMP
/skillsmp-search "CLI design"
/skillsmp-search "database migration"

# The skill will:
# 1. Call skill_discovery.py with --skillsmp flag
# 2. Show results from SkillsMP API
# 3. Prompt: Install any of these skills?
```

## Requirements

**API Key**: SkillsMP requires an API key. Set via:

```bash
export SKILLSMP_API_KEY="sk_live_your_key_here"
```

Get your free key at: https://skillsmp.com/docs/api

## Installation Command

When user confirms installation:

```bash
claude plugin install <skill-name>@skillsmp
```

Example:
```bash
claude plugin install cli-designer@skillsmp
```

## Integration with Skill Discovery

When skill_discovery.py finds gaps:

```bash
# Automatic workflow
python3 ~/.claude/skills/skill_discovery.py "build a CLI tool" --skillsmp

# Output shows:
# 🔍 Potential skill gaps: 1
#   ⚠️  frontend: Consider searching SkillsMP for 'frontend skill'
#
# 🌐 SkillsMP results: 3
#   🔷 cli-designer by @author
#      Design beautiful CLI interfaces...
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| No API key | SKILLSMP_API_KEY not set | Set env var |
| Invalid key | Wrong API key | Get new key from SkillsMP |
| No results | No matching skills | Try different search terms |

## Keywords

skillsmp, skill marketplace, search skills, install skill, skill gaps, external skills
