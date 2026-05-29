---
name: lab-roster
description: Generate comprehensive lab member rosters in both markdown and CSV formats. Analyzes member profiles, git history, and alumni information to create detailed rosters with role transitions, team assignments, and career tracking. Use when user mentions roster, team list, lab members, or updating member information.
version: 1.0.0
allowed-tools: Read, Glob, Grep, Bash, Task, Write, Edit
---

# Lab Roster Generator

This skill generates comprehensive rosters of all lab members with detailed tracking of roles, dates, team assignments, and career progressions.

## When to Use This Skill

Use this skill when the user requests:
- "Generate the lab roster"
- "Update the team list"
- "Create a CSV of all lab members"
- "Track who's been in the lab"
- "Show me the roster with role transitions"
- Any mention of roster, member list, or team tracking

## Two Generation Modes

### Mode 1: Quick Generation (Python Script)
Fast automated generation using git history analysis.

**When to use**: Quick updates, routine refreshes
**Output**: `lab_roster.csv`

### Mode 2: Comprehensive Generation (Subagent Workflow)
Careful information gathering using subagents for each member.

**When to use**: First-time generation, complex updates, verification needed
**Output**: `ROSTER.md` + `lab_roster.csv`

## Instructions

### Step 1: Determine Mode

Ask the user which mode they prefer, or choose based on context:
- If ROSTER.md doesn't exist or is outdated → Mode 2
- If just need CSV update → Mode 1
- If user wants verification → Mode 2

### Step 2a: Quick Generation (Mode 1)

1. Run the roster generation script:
   ```bash
   python3 .claude/skills/lab-roster/scripts/generate_roster_csv.py
   ```

2. Validate output:
   - Check row count matches expected members
   - Verify currently active members
   - Show summary statistics

3. Present results to user with summary

### Step 2b: Comprehensive Generation (Mode 2)

1. **Check if ROSTER.md exists**
   - If exists, read it to understand current state
   - If not, create it with field descriptions and instructions

2. **Get list of all members**
   ```bash
   ls _members/*.md | grep -v "friends"
   ```

3. **Launch subagents to gather information**
   - Process members in batches of 4-5
   - Each subagent should:
     - Read member file: `_members/[name].md`
     - Check git history: `git log --follow --format="%aI|%s" -- _members/[name].md`
     - Check for role transitions in git: `git show <commit>:_members/[name].md`
     - Check alumni list in `team/index.md`
     - Infer team from bio keywords (see reference.md)
     - Extract co-advisor from bio text
     - Extract previous and next positions

4. **Update ROSTER.md**
   - Add entries in the format from templates/roster-entry.md
   - One entry per role (create multiple entries for role transitions)
   - Only fill "Previous" field in first entry
   - Only fill "Next" field in last entry

5. **Generate CSV from ROSTER.md**
   ```bash
   python3 .claude/skills/lab-roster/scripts/roster_md_to_csv.py
   ```

6. **Validate and present**
   - Show summary statistics
   - Highlight any missing data
   - Ask user to review

## Field Descriptions

- **name**: Full name of the lab member
- **role**: Short code (pi, postdoc, staff, phd, ms, ra, programmer, undergrad, highschool)
- **start_date**: When they started (YYYY-MM format)
- **end_date**: When they ended (YYYY-MM format, empty if still active)
- **previous_position**: Position before joining lab (only in first entry)
- **next_position**: Where they went after (only in last entry)
- **team**: Primary team (software_engineering, phenoinformatics, virtual_biology)
- **co_advisor**: Other PIs they work with

## Team Inference Rules

Use these keyword mappings to infer team from bio text:

**software_engineering**:
- Keywords: SLEAP, DREEM, cloud, infrastructure, plant, root, AWS, full-stack, data pipeline, software engineer, programmer, bioinformatics analyst, computer vision algorithm, pose estimation

**phenoinformatics**:
- Keywords: phenotyp, behavior, ALS, Alzheimer, disease model, mice, mouse, longitudinal, space, neurodegenerative, multi-animal, tracking pipeline

**virtual_biology** (highest priority):
- Keywords: VNL, virtual lab, virtual animal, embodied, neuromechanical simulation

Note: Check virtual_biology keywords first, then software_engineering, then phenoinformatics.

## Co-Advisor Extraction

Look for these patterns in bio text:
- "co-advised by [Name]"
- "co-supervised by [Name]"
- "jointly with [Name]"
- "joint with [Name]"

Remove markdown links and extract just the name.

## Previous/Next Position Extraction

**Previous positions** - look for:
- "Prior to joining..."
- "previously worked at/as..."
- "received [degree] from..."
- Education background

**Next positions** - look in `team/index.md` alumni section:
- Format: `**Next:** [position]`

## Validation Checklist

Before presenting results:
- [ ] All active members included
- [ ] Role transitions properly split into multiple entries
- [ ] Start dates seem reasonable
- [ ] Teams assigned for most members
- [ ] No duplicate entries
- [ ] CSV has same data as ROSTER.md (if both exist)
- [ ] Summary statistics make sense

## Output Format

Always show:
```
✓ Generated roster with [N] entries
✓ Saved to: lab_roster.csv

Summary:
  Total entries: [N]
  Unique members: [N]
  Currently active: [N]
  Alumni entries: [N]
  Team distribution:
    - software_engineering: [N]
    - phenoinformatics: [N]
    - virtual_biology: [N]
```

## Error Handling

If script fails:
1. Check Python version (needs Python 3.6+)
2. Verify git is available
3. Check that _members/ directory exists
4. Look for malformed member files

If subagents miss information:
1. Review their search patterns
2. Check if member files follow expected format
3. Manually verify edge cases

## Notes

- Exclude members with role "friends"
- Multiple role entries for same person are normal (e.g., undergrad → MS → PhD)
- Start dates are best guesses from git history
- Some fields may be empty - that's okay
- ROSTER.md is human-editable - CSV regenerates from it

## See Also

- [reference.md](reference.md) - Detailed documentation on member formats and inference patterns
- [examples.md](examples.md) - Example usage scenarios
- [templates/roster-entry.md](templates/roster-entry.md) - Entry format template
