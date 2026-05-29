---
name: analyze-skill
description: Analyze skill complexity and get modularization recommendations
usage: /analyze-skill [skill-path]
---

# Analyze Skill Complexity

<identification>
triggers: analyze skill, skill complexity, skill metrics, modularization, skill size, skill structure, skill analysis, complexity analysis

use_when:
- Assessing skill file complexity before adding content
- Planning modularization strategies
- Checking if a skill needs to be split
- Validating progressive disclosure design

do_not_use_when:
- Evaluating skill quality - use /skills-eval instead
- Estimating token usage only - use /estimate-tokens instead
- Creating new skills - use /create-skill instead
</identification>

Analyzes a skill file for complexity metrics and provides modularization recommendations based on the modular-skills framework.

## Usage

```bash
# Analyze specific skill file
/analyze-skill skills/my-skill/SKILL.md

# Analyze skill directory
/analyze-skill skills/my-skill

# Analyze current directory (if in a skill folder)
/analyze-skill .
```

## What It Analyzes

The analyzer evaluates several complexity dimensions:

### Metrics Collected
- **Line count**: Total lines vs threshold (default: 150)
- **Word/character count**: Content density indicators
- **Theme sections**: Number of `#` level headings
- **Subsections**: Number of `##` level headings
- **Code blocks**: Embedded code examples
- **Estimated tokens**: Context window impact

### Recommendations Generated
- **MODULARIZE**: File exceeds thresholds, should be split
- **CONSIDER**: Approaching limits, evaluate for future growth
- **OK**: Within acceptable complexity bounds

## Examples

```bash
/analyze-skill skills/modular-skills/SKILL.md
# Output:
# === Analysis for: skills/modular-skills/SKILL.md ===
# Line count: 180 (threshold: 150)
# Estimated tokens: 1,847
# === Recommendations ===
# MODULARIZE: File exceeds threshold (180 > 150)
# GOOD: Token usage in optimal range

/analyze-skill skills/skills-eval --verbose
# Includes detailed section breakdown
```

## Integration with Modular Skills

This command is the first step in the modular-skills workflow:

1. **Analyze** → Use this command to assess complexity
2. **Design** → Plan module structure based on recommendations
3. **Estimate** → Use `/estimate-tokens` for token budgeting
4. **Validate** → Use `/skills-eval` for quality checks

## Implementation

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/skill_analyzer.py --file "${1:-.}"
```
