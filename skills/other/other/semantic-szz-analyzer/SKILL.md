---
name: semantic-szz-analyzer
description: Identify bug-introducing commits using semantic analysis that extends traditional SZZ algorithm. Distinguishes semantic changes from refactorings or code movements using control-flow and data-flow similarity analysis. Use when analyzing bug-fix commits to trace back to bug-introducing changes, investigating software evolution, conducting empirical studies on defect prediction, or reducing false positives in bug localization. Supports git repositories and provides explanations for why commits are identified as bug-introducing.
---

# Semantic SZZ Analyzer

## Overview

Semantic SZZ Analyzer extends the traditional SZZ (Sliwerski-Zimmermann-Zeller) algorithm by incorporating semantic analysis to identify bug-introducing commits more accurately. It distinguishes actual semantic changes from refactorings or code movements by analyzing control-flow and data-flow similarity across versions.

## Core Capabilities

### 1. Semantic Change Detection

Analyze commits to distinguish between:
- **Semantic changes**: Modifications that alter program behavior
- **Refactorings**: Code restructuring without behavior changes
- **Code movements**: Relocations of code blocks without semantic impact

Use control-flow graphs (CFG) and data-flow analysis to compute similarity between code versions.

### 2. Bug-Introducing Commit Identification

Given a bug-fix commit, trace back through git history to identify the commit that introduced the bug:

1. Extract changed lines from the bug-fix commit
2. Use `git blame` to find commits that last modified those lines
3. Apply semantic analysis to filter out false positives
4. Rank candidates by semantic similarity and temporal proximity

### 3. False Positive Reduction

Traditional SZZ produces many false positives due to:
- Whitespace changes
- Comment modifications
- Import reorganization
- Variable renaming
- Code formatting

Semantic SZZ filters these by analyzing AST (Abstract Syntax Tree) structure and semantic equivalence.

## Workflow

### Step 1: Analyze Bug-Fix Commit

Start by identifying the bug-fix commit. Look for:
- Commits with keywords: "fix", "bug", "issue", "patch", "resolve"
- Commits linked to issue trackers
- Commits explicitly marked as fixes

Extract the changed lines and affected files.

### Step 2: Identify Candidate Commits

Use `git blame` or `git log -L` to trace the history of changed lines:

```bash
git blame -L <start>,<end> <file> <bug-fix-commit>^
```

This identifies commits that last modified the buggy lines before the fix.

### Step 3: Apply Semantic Analysis

For each candidate commit, run semantic analysis using the provided script:

```bash
python scripts/semantic_analyzer.py --repo <repo-path> --candidate <commit-hash> --fix <fix-commit-hash>
```

The script computes:
- **CFG similarity**: Control-flow graph matching between versions
- **Data-flow similarity**: Variable usage and dependency analysis
- **AST diff**: Structural code changes vs. superficial changes

### Step 4: Filter and Rank Results

Filter candidates based on semantic similarity threshold (default: 0.7). Rank remaining candidates by:
1. Semantic change magnitude
2. Temporal proximity to bug-fix
3. Code churn in the commit

### Step 5: Generate Explanation

For each identified bug-introducing commit, generate an explanation including:
- What semantic changes were made
- Why the change is considered bug-introducing
- Confidence score based on similarity metrics
- Diff highlighting the problematic changes

## Usage Examples

**Example 1: Analyze a specific bug-fix**

```bash
python scripts/semantic_szz.py --repo /path/to/repo --fix-commit abc123
```

**Example 2: Batch analysis of multiple fixes**

```bash
python scripts/batch_analyze.py --repo /path/to/repo --fixes-file bug_fixes.txt
```

**Example 3: Generate detailed report**

```bash
python scripts/semantic_szz.py --repo /path/to/repo --fix-commit abc123 --output report.json --explain
```

## Advanced Features

### Custom Similarity Thresholds

Adjust sensitivity by modifying similarity thresholds:

```python
# In scripts/semantic_analyzer.py
CFG_THRESHOLD = 0.7  # Control-flow similarity
DFG_THRESHOLD = 0.6  # Data-flow similarity
AST_THRESHOLD = 0.8  # AST structural similarity
```

### Language-Specific Analysis

The analyzer supports multiple languages with language-specific parsers:
- Python: Uses `ast` module
- Java: Uses `javalang` or tree-sitter
- C/C++: Uses `pycparser` or tree-sitter
- JavaScript: Uses `esprima` or tree-sitter

See [references/language_support.md](references/language_support.md) for details.

### Integration with Issue Trackers

Link bug-fixes to issue IDs for automated analysis:

```bash
python scripts/semantic_szz.py --repo /path/to/repo --issue JIRA-123
```

## References

- **[references/szz_algorithm.md](references/szz_algorithm.md)**: Detailed explanation of traditional SZZ algorithm
- **[references/semantic_analysis.md](references/semantic_analysis.md)**: Control-flow and data-flow analysis techniques
- **[references/language_support.md](references/language_support.md)**: Language-specific parsing and analysis details

## Output Format

Results are provided in JSON format:

```json
{
  "fix_commit": "abc123",
  "bug_introducing_commits": [
    {
      "commit": "def456",
      "confidence": 0.85,
      "semantic_change_type": "logic_modification",
      "explanation": "Modified conditional logic in function foo()",
      "changed_lines": [45, 46, 47],
      "similarity_scores": {
        "cfg": 0.72,
        "dfg": 0.68,
        "ast": 0.81
      }
    }
  ]
}
```
