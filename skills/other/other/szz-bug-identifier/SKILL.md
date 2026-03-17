---
name: szz-bug-introducing-commit-identifier
description: Identifies bug-introducing commits using SZZ-style analysis based on bug-fixing commits, commit history, and code blame information. Use this skill when you need to trace bugs back to their origin, identify which commits introduced bugs, analyze bug-fix commits to find root causes, perform software repository mining for bug analysis, or conduct empirical studies on software defects. Triggers when users ask to find bug-introducing commits, identify when a bug was introduced, trace bug origins, perform SZZ analysis, or analyze bug-fixing commits.
---

# SZZ Bug-Introducing Commit Identifier

## Overview

This skill performs SZZ (Śliwerski-Zimmermann-Zeller) algorithm analysis to identify bug-introducing commits in git repositories. Given a bug-fixing commit, it traces modified lines back through version history using git blame to find candidate commits that originally introduced the buggy code.

## Workflow

### 1. Identify the Bug-Fixing Commit

Start by identifying the commit that fixes the bug. This can be obtained from:
- Commit hash provided by the user
- Issue tracker references (e.g., "fixes #123")
- Commit message analysis (e.g., "fix:", "bug:")
- Manual identification by the user

### 2. Run the SZZ Analysis

Use the provided script to perform the analysis:

```bash
python scripts/szz_analyzer.py <fix-commit-hash>
```

**Options:**
- `--repo <path>`: Specify repository path (default: current directory)
- `--json`: Output results in JSON format for programmatic processing
- `--top <n>`: Number of top candidates to show (default: 10)

**Example:**
```bash
python scripts/szz_analyzer.py abc123def --repo /path/to/repo --top 5
```

### 3. Interpret Results

The script outputs a ranked list of candidate bug-introducing commits with:
- **Commit hash**: The candidate commit identifier
- **Author**: Who made the commit
- **Date**: When the commit was made
- **Message**: The commit message
- **Confidence score**: Likelihood this commit introduced the bug (0.0-1.0)
- **Reasons**: Explanation for why this commit is a candidate

### 4. Manual Verification

Always manually review the top candidates:
1. Examine the actual code changes in the candidate commit
2. Check if the changes are functionally related to the bug
3. Consider the context and purpose of the changes
4. Verify against issue tracker history if available

## Understanding Confidence Scores

**High Confidence (0.8-1.0)**:
- Multiple lines from the commit were fixed
- Commit message doesn't suggest refactoring
- Functional code changes (not just formatting)

**Medium Confidence (0.5-0.8)**:
- Single line modified, or
- Some indicators of refactoring but functional changes present

**Low Confidence (0.0-0.5)**:
- Commit message suggests refactoring/formatting
- Only structural changes (imports, comments, whitespace)
- Likely a false positive

## False Positive Filtering

The script automatically filters common false positives:

**Automatically Filtered Lines:**
- Empty lines and whitespace-only changes
- Comment additions/modifications
- Import/include statements
- Braces and structural elements

**Reduced Confidence for:**
- Commits with refactoring keywords in messages
- Single-line changes
- Formatting-related commits

## Common Use Cases

### Use Case 1: Bug Root Cause Analysis
```
User: "Find which commit introduced the bug fixed in commit abc123"
→ Run: python scripts/szz_analyzer.py abc123
→ Review top candidates and examine their changes
```

### Use Case 2: Developer Accountability
```
User: "Who introduced the authentication bug?"
→ First identify the fix commit
→ Run SZZ analysis
→ Check the author field of top candidates
```

### Use Case 3: Bug Pattern Analysis
```
User: "Analyze all bug-introducing commits from the last release"
→ Identify all bug-fix commits
→ Run SZZ analysis on each
→ Aggregate results to find patterns
```

### Use Case 4: Empirical Software Engineering Research
```
User: "Generate dataset of bug-introducing commits for analysis"
→ Run SZZ analysis with --json flag
→ Process JSON output for statistical analysis
```

## Limitations and Considerations

1. **Tangled Changes**: If a commit mixes bug-introducing code with unrelated changes, the entire commit is flagged

2. **Refactoring Breaks Chains**: Heavy refactoring can make it difficult to trace back to the original introduction

3. **Indirect Bugs**: Bugs caused by missing code or incorrect assumptions may not be detected

4. **Multi-Commit Bugs**: Bugs introduced across multiple commits may only identify the most recent contributor

5. **False Fixes**: If the "fix" commit doesn't actually fix the bug, the analysis will be incorrect

## Advanced Usage

### Programmatic Integration

Use JSON output for integration with other tools:

```python
import subprocess
import json

result = subprocess.run(
    ['python', 'scripts/szz_analyzer.py', 'abc123', '--json'],
    capture_output=True,
    text=True
)
candidates = json.loads(result.stdout)

for candidate in candidates:
    print(f"{candidate['commit_hash']}: {candidate['confidence_score']}")
```

### Batch Analysis

Analyze multiple bug fixes:

```bash
for commit in $(git log --grep="fix:" --format="%H"); do
    echo "Analyzing fix: $commit"
    python scripts/szz_analyzer.py $commit --top 3
done
```

## Resources

### scripts/szz_analyzer.py
The main analysis script that performs SZZ algorithm implementation. It:
- Extracts modified lines from bug-fixing commits
- Uses git blame to trace lines back through history
- Applies filtering heuristics to reduce false positives
- Ranks candidates by confidence score

### references/szz_algorithm.md
Comprehensive documentation on the SZZ algorithm including:
- Detailed algorithm steps and theory
- False positive patterns and filtering strategies
- Confidence scoring methodology
- Limitations and best practices
- Algorithm variants and extensions

Read this reference when you need deeper understanding of the algorithm, want to customize filtering heuristics, or need to explain the methodology to users.
