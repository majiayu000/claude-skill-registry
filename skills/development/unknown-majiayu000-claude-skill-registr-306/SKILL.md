---
name: student-activity-analysis
description: Analyze student git activity, lab submissions, and project work for software engineering courses. Use when asked to "update student analysis", "check student activity", "analyze the class", or when working with student rosters and git repositories. Handles inconsistencies in student behavior like multiple usernames, name variations, and missing data.
allowed-tools: Read, Bash, Write, Grep, Glob
---

# Student Activity Analysis Skill

## When to Use This Skill

Invoke this skill when the user:
- Asks to "update the student activity analysis"
- Asks "how are students doing?" or "check student progress"
- Mentions checking class activity, lab submissions, or project work
- Wants to see who has completed labs or is actively contributing
- Needs to verify student participation or identify at-risk students

## Overview

This skill automates the analysis of student git activity in a software engineering course. It reads from a canonical student roster (OFFICIAL_STUDENT_ROSTER.json), queries git history, checks file systems, and generates a comprehensive markdown report (STUDENT_ACTIVITY_ANALYSIS.md).

## Step-by-Step Instructions

### Step 0: Sync with Main Branch (CRITICAL)

**Always start by syncing with the main branch** to ensure you're analyzing the latest activity:

```bash
git fetch origin main
git merge origin main -m "Sync with main before analysis"
```

⚠️ **Why this is critical:** Without syncing, you may miss up to 76% of student activity that exists on the main branch but not on your current branch.

### Step 1: Collect Activity Data

Run the data collection script:

```bash
python3 .claude/skills/student-activity-analysis/collect_data.py
```

This script will:
- Read OFFICIAL_STUDENT_ROSTER.json
- Query git logs for each student (handling multiple usernames)
- Check lab01 completion (intro.py files)
- Check lab03 folders
- Analyze project folder activity
- Generate STUDENT_ACTIVITY_DATA.json

### Step 2: Generate Report

Run the report generation script:

```bash
python3 .claude/skills/student-activity-analysis/generate_report.py
```

This script will:
- Read STUDENT_ACTIVITY_DATA.json
- Generate formatted markdown tables
- Calculate statistics
- Write to STUDENT_ACTIVITY_ANALYSIS.md

### Step 3: Review and Commit

Review the generated report and commit if everything looks good:

```bash
git add STUDENT_ACTIVITY_ANALYSIS.md STUDENT_ACTIVITY_DATA.json
git commit -m "Update student activity analysis - $(date +%Y-%m-%d)"
git push -u origin <branch-name>
```

## Handling Edge Cases

The real world is messy. Students don't always follow instructions perfectly. This skill is designed to handle common inconsistencies:

### Edge Case 1: Multiple GitHub Usernames

**Problem:** A student may have multiple GitHub usernames or commit under different names.

**Example from roster:**
```json
"github_username": "jcuzic/Zlicone"
```

**Solution:** Split on "/" and query git with all usernames:
```bash
git log --all --author="jcuzic\|Zlicone" --oneline | wc -l
```

### Edge Case 2: Name Variations and Diacritics

**Problem:** Student names in folders may not match roster exactly due to diacritics or spelling.

**Roster:** "Stipe Ćubelić"
**Folder:** `students/lab03/scubelic/`

**Solution:** Use fuzzy matching when checking for folders:
- Convert names to lowercase
- Remove diacritics (ć→c, š→s, ž→z)
- Check for partial matches

### Edge Case 3: Lab Submissions in Wrong Location

**Problem:** Student may create intro.py in the wrong directory.

**Expected:** `students/<github_username>/intro.py`
**Actual:** `students/intro.py` or `students/lab01/<name>/intro.py`

**Solution:** Search entire students/ directory:
```bash
find students/ -name "intro.py" -type f
```

Then manually verify which file belongs to which student.

### Edge Case 4: Stale or Orphaned Project Folders

**Problem:** Project folders exist but no students in roster claim them.

**Examples:**
- `projects/garderoba/` (no team registered)
- `projects/climate-analyzers-asmith-bjohnson/` (demo data?)

**Solution:**
- List all projects in report
- Mark unmatched folders as "Unknown Team"
- Show commit count to help identify ownership

### Edge Case 5: Team Lead with No Commits

**Problem:** Student is listed as project lead but has 0 commits in project folder.

**Possible reasons:**
- Commits under different username
- Work done in different branch
- Administrative lead (not technical)

**Solution:**
- Mark as "Lead Only - Verify" status
- Manually review git log for project folder
- Check if commits exist under alternative username

## Validation and Error Handling

Before finalizing the report, validate:

1. **Student count matches:** Number of students in report = Number in roster
2. **No missing projects:** All project folders are accounted for
3. **Date ranges make sense:** First commit < Last commit
4. **Status classifications are consistent:**
   - "Very Active" = 15+ commits
   - "Active" = 5-14 commits
   - "Low Activity" = 2-4 commits
   - "Minimal Activity" = 1 commit
   - "No Git Activity" = 0 commits

If validation fails:
- Report the discrepancy
- Show which students/projects are problematic
- Ask user if manual review is needed

## Output Format

The generated STUDENT_ACTIVITY_ANALYSIS.md should include:

1. **Overview Statistics**
   - Total students (from roster)
   - Students with activity
   - Activity percentage

2. **Student Activity Table**
   - ALL students (even those with 0 commits)
   - Sorted by activity level (most active first)
   - Columns: Name, GitHub, Commits, Status, Lab01, Lab03, Project Role
   - NO email addresses (kept in JSON only)

3. **Project Teams Table**
   - ALL project folders
   - Columns: Project, Total Commits, Team Lead, Status
   - Include "Unknown" projects

4. **Recommendations**
   - Students needing attention (0 commits)
   - Positive highlights (very active students)

## Testing the Skill

To test this skill manually:

1. Create a test branch
2. Invoke the skill
3. Verify output contains all 52 students
4. Check that statistics add up correctly
5. Manually verify a few commit counts with `git log`

## Troubleshooting

**Q: Script says "OFFICIAL_STUDENT_ROSTER.json not found"**
A: Make sure you're in the repository root directory `/home/user/2025-intro-swe/`

**Q: Git log shows no commits for a student I know has commits**
A: Check if they have multiple GitHub usernames. Update roster with "username1/username2" format.

**Q: Student has intro.py but script doesn't detect it**
A: Check the file path. Script searches entire students/ directory but may need manual verification.

**Q: Project folder exists but not in any team's project_folder field**
A: This is an orphaned project. Script will mark it as "Unknown Team" - may need manual investigation.

## Files Managed by This Skill

- **OFFICIAL_STUDENT_ROSTER.json** (READ ONLY - never modified by scripts)
- **STUDENT_ACTIVITY_DATA.json** (Generated by collect_data.py)
- **STUDENT_ACTIVITY_ANALYSIS.md** (Generated by generate_report.py)

## Key Lessons Learned

1. **Always sync with main first** - Missing this step caused 76% of activity to be missed initially
2. **Include ALL enrolled students** - Even those with 0 activity need to be in the report
3. **Separate static from dynamic data** - Roster is manual, activity data is automated
4. **Handle real-world messiness** - Students use multiple usernames, misspell names, put files in wrong places
5. **Make it deterministic** - Same git state should produce same report every time
