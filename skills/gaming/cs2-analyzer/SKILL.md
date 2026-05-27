---
description: Analyze CS2 demo files and generate comprehensive tactical reports
---

# CS2 Demo Analyzer Skill

This skill analyzes Counter-Strike 2 demo files (.dem) and produces professional tactical analysis reports with strategic insights, player statistics, and coaching recommendations.

## What This Skill Does

1. **Accepts a CS2 demo file** (drag & drop or provide path)
2. **Generates multi-format analysis**:
   - Compact storage format for archival
   - Digest summary for quick review
   - Full markdown tactical report
3. **Returns strategic insights** including:
   - Team performance (T-side vs CT-side)
   - Player statistics and rankings
   - Critical round breakdowns
   - Tactical recommendations
   - Entry success, post-plant win rates, tempo analysis

## For End Users

### Simple Usage

Just say:
- "Analyze this demo" (after dragging .dem file)
- "Analyze data/raw/my-game.dem"
- "Give me a tactical report for the latest demo"

### What You'll Get

A comprehensive report covering:
- **Executive Summary** - Top 3-5 strategic insights
- **Team Analysis** - T-side and CT-side performance
- **Critical Rounds** - Key moments that decided the game
- **Player Highlights** - Top performers and improvement areas
- **Tactical Recommendations** - Actionable coaching points

## Requirements (One-Time Setup)

This skill requires:
- ✅ Python 3.11+ with Poetry installed
- ✅ Project dependencies installed (`poetry install`)
- ✅ Directory structure: `data/raw/`, `data/compact/`, `data/digest/`, `reports/`

**Setup Instructions**: See `docs/setup.md` for first-time installation.

## How It Works

The skill uses a three-tier architecture:

1. **Parse Demo** → Extract game data using awpy library
2. **Generate Formats**:
   - Compact state (storage, ~400KB)
   - Digest (Claude-readable, <50KB)
   - Full report (markdown)
3. **Strategic Analysis** → Metrics calculation and tactical insights

## Example Output

```
# CS2 Tactical Analysis: Dust2

**Final Score**: T 15 - 13 CT

## Executive Summary
- T-side dominated with 54% round win rate
- Exceptional 82% post-plant win rate
- Aggressive 17.5s time-to-first-kill
- m0NESY MVP: 1.46 K/D, 19 kills

## Recommendations
- T-Side: Maintain excellent post-plant discipline
- CT-Side: Improve retake coordination (only 18% success)
- Individual: mezii needs positioning work (0.6 K/D)
```

## Technical Details

**Scripts Used**:
- `generate_tactical_report.py` - Main analysis pipeline
- `generate_digest.py` - Digest generation
- `analyze_compact_demo.py` - Metrics calculation

**Output Locations**:
- Reports: `reports/game_analysis_[map]_[timestamp].md`
- Digests: `data/digest/[demo]_[timestamp].digest.txt`
- Compact: `data/compact/[demo]_[timestamp].compact.txt`

**Performance**: 30-60 seconds for full match analysis (30-50 rounds)

## Skill Workflow

When invoked, this skill will:

1. ✅ Validate demo file path exists
2. ✅ Check dependencies (poetry environment)
3. ✅ Run analysis pipeline
4. ✅ Read generated digest for strategic insights
5. ✅ Read full report for comprehensive details
6. ✅ Summarize findings for user
7. ✅ Provide report file path for download

## Error Handling

The skill handles:
- Missing demo files → Clear error message
- Invalid demo format → awpy parsing error explanation
- Missing dependencies → Setup instructions
- Analysis failures → Detailed error logs

## Future Enhancements

Planned features:
- [ ] Multi-demo comparison (track player improvement over time)
- [ ] Interactive queries ("Show me all A-site executes")
- [ ] Heatmap generation (positional analysis)
- [ ] Utility usage analysis (smoke/flash patterns)
- [ ] Economic analysis (force buy success rates)
