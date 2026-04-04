---
name: synapse
description: Pattern detection and automatic skill recommendation system. Activates when analyzing Cortex memory files, detecting recurring work patterns, or determining if new skills are needed. Analyzes .cortex_log.md, PRD files, and task lists to identify patterns (API calls, testing, deployment, etc.) appearing 5+ times. Generates Synapse_RECOMMENDATIONS.md with prioritized skill suggestions. Use when optimizing workflows or identifying automation opportunities.
allowed-tools: Read, Write, Bash, Grep, Glob
---

# Synapse - Automatic Skill Generator

**Analyzes your work patterns and automatically generates the skills you need.**

Synapse is the brain of the skill ecosystem. It watches Cortex memory, reads your PRD files, analyzes your tasks, and automatically creates new skills when patterns emerge.

## What Synapse Does

Synapse performs unified analysis from multiple sources:

### 1. Cortex Memory Analysis
- Reads `.cortex_log.md` and `.cortex_status.json`
- Detects recurring patterns (API calls, data processing, errors, etc.)
- Identifies patterns that appear ≥ threshold (default: 5 times)
- Calculates priority based on frequency

### 2. PRD Analysis
- Scans for PRD files (`*PRD*.md`, `*REQUIREMENTS*.md`, `*ROADMAP*.md`)
- Extracts tasks and requirements
- Classifies by domain (api, testing, deployment, etc.)
- Counts tasks per domain to identify skill needs

### 3. Task Analysis
- Reads TODO files and task lists
- Parses checkboxes, numbered lists, bullets
- Groups related tasks
- Identifies skill opportunities

## Automatic Skill Generation

**Synapse runs automatically and generates skills without user intervention:**

- **Periodically**: Every 30 minutes via cron (optional)
- **On git commit**: Via post-commit hook (optional)
- **When critical patterns detected**: Immediate generation

**Skills are auto-generated when:**
- Pattern appears ≥ threshold (default: 5 times)
- Priority is high or critical
- Skill doesn't already exist

## How It Works

```
You work normally
        ↓
Cortex traces everything
        ↓
Synapse monitors automatically:
  - Cortex memory (patterns)
  - PRD files (requirements)
  - Task lists (TODO)
        ↓
Detects patterns >= threshold
        ↓
Auto-generates skills if priority >= high:
  - Creates .claude/skills/[skill-name]/
  - Generates SKILL.md with progressive disclosure
  - Creates scripts with Cortex API integration
  - Records in Cortex memory
        ↓
New skill ready immediately!
        ↓
Claude uses it automatically
```

**No user intervention needed.**

## Priority Levels

Synapse assigns priorities based on frequency and task count:

- **🔴 CRITICAL**: Pattern appears 2+ times/day → Auto-generate immediately
- **🟠 HIGH**: Pattern appears 1+ times/day → Auto-generate
- **🟡 MEDIUM**: Pattern appears 3-7 times/week → Monitor
- **🟢 LOW**: Pattern appears <3 times/week → Monitor

Only HIGH and CRITICAL priorities trigger automatic generation.

## Output

Synapse generates `Synapse_RECOMMENDATIONS.md` with prioritized skill recommendations:

```markdown
# Synapse Skill Recommendations

## Summary
- Total recommendations: 3
- High priority: 2
- Medium priority: 1

## Recommended Skills

### 1. 🔴 api-optimizer (CRITICAL)
**Pattern:** api_call
**Frequency:** 3.5 times/day (24 total in 7 days)
**Reason:** Frequent API operations detected
...
```

See [OUTPUT_FORMAT.md](references/OUTPUT_FORMAT.md) for complete output specification.

## Quick Start

### Automatic Mode (Recommended)

Run auto-generator to analyze and generate skills automatically:

```bash
python .claude/skills/synapse/scripts/auto_skill_generator.py
```

Skills with HIGH or CRITICAL priority will be generated automatically.

### Analysis Only

Generate recommendations without auto-creating skills:

```bash
python .claude/skills/synapse/scripts/synapse_analyzer.py
```

This creates `Synapse_RECOMMENDATIONS.md` for manual review.

### Setup Monitoring

Add to crontab for automatic periodic checks:

```bash
# Every 30 minutes
*/30 * * * * /path/to/.claude/skills/synapse/scripts/synapse_auto_watch.sh
```

Or use as git hook (see [INSTALLATION.md](references/INSTALLATION.md)).

## Integration with Cortex

Synapse and Cortex work together seamlessly:

1. **Cortex traces** your work and records events
2. **Synapse analyzes** Cortex memory for patterns
3. **Synapse generates** skills when patterns reach threshold
4. **New skills use** Cortex API to record their own events
5. **Pattern detection improves** as more skills contribute data

This creates a self-improving system where skills emerge from actual usage patterns.

## Generated Skill Structure

Synapse creates skills following best practices:

```
generated-skill/
├── SKILL.md (with YAML frontmatter)
├── scripts/
│   └── main.py (with Cortex API integration)
└── references/ (if needed)
```

All generated skills:
- ✅ Follow progressive disclosure principles
- ✅ Include Cortex API integration
- ✅ Have concise SKILL.md (<200 lines)
- ✅ Record their own events for future pattern detection
- ✅ Work with Claude Code, GPT, and Gemini

## Multi-LLM Support

Synapse works with any CLI-based LLM:
- ✅ **Claude Code**: Native integration
- ✅ **GPT/Codex**: Reads `Synapse_RECOMMENDATIONS.md`
- ✅ **Gemini CLI**: Reads `Synapse_RECOMMENDATIONS.md`

See [MULTI_LLM.md](references/MULTI_LLM.md) for LLM-specific guides.

## Advanced Features

- **Pattern merging**: Combines Cortex + PRD patterns for higher priority
- **Duplicate detection**: Never generates skills that already exist
- **Context preservation**: Recommendations include example usage
- **Custom thresholds**: Configure sensitivity via command-line args

See [ADVANCED.md](references/ADVANCED.md) for detailed documentation.

## Configuration

Create `.synapse_config.json` for custom settings:

```json
{
  "analysis": {
    "threshold": 5,
    "window_days": 7
  },
  "sources": {
    "cortex_memory": true,
    "prd_files": true,
    "task_lists": true
  }
}
```

See [CONFIGURATION.md](references/CONFIGURATION.md) for all options.

## References

- **[INSTALLATION.md](references/INSTALLATION.md)** - Setup and git hooks
- **[MANUAL_USAGE.md](references/MANUAL_USAGE.md)** - Command-line options
- **[OUTPUT_FORMAT.md](references/OUTPUT_FORMAT.md)** - Recommendation file format
- **[EXAMPLES.md](references/EXAMPLES.md)** - Real-world skill generation examples
- **[ADVANCED.md](references/ADVANCED.md)** - Pattern merging, customization
- **[CONFIGURATION.md](references/CONFIGURATION.md)** - Complete config reference
- **[MULTI_LLM.md](references/MULTI_LLM.md)** - Using with GPT, Gemini, etc.

## Part of the Ecosystem

**Cortex** → Remembers everything
**Synapse** → Analyzes and generates
**Generated skills** → Solve specific problems
**Skills use Cortex** → Pattern detection improves

Synapse makes the system intelligent and self-improving.

---

*Synapse - The universal skill recommendation and generation engine*
