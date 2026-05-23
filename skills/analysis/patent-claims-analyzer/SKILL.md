---
name: patent-claims-analyzer
description: Automated analysis of patent claims for USPTO compliance with 35 USC 112(b) requirements - antecedent basis, definiteness, claim structure
tools: Bash, Read, Write
model: sonnet
---

# Patent Claims Analyzer Skill

Automated analysis of patent claims for USPTO compliance with 35 USC 112(b) requirements.

## When to Use

Invoke this skill when users ask to:
- Review patent claims for definiteness
- Check antecedent basis in claims
- Analyze claim structure
- Find claim drafting issues
- Validate claims before filing
- Fix USPTO office action issues related to claims

## What This Skill Does

Performs comprehensive automated analysis:

1. **Antecedent Basis Checking**:
   - Finds terms used without prior introduction
   - Detects missing "a/an" before first use
   - Identifies improper "said/the" before first use
   - Tracks term references across claims

2. **Definiteness Analysis** (35 USC 112(b)):
   - Identifies subjective/indefinite terms
   - Detects relative terms without reference
   - Finds ambiguous claim language
   - Checks for clear claim boundaries

3. **Claim Structure Validation**:
   - Parses independent vs. dependent claims
   - Validates claim dependencies
   - Checks claim numbering
   - Identifies claim type (method, system, etc.)

4. **Issue Categorization**:
   - **Critical**: Must fix before filing
   - **Important**: May cause rejection
   - **Minor**: Best practice improvements

## Required Data

This skill uses the automated claims analyzer from:
**Location**: `${CLAUDE_PLUGIN_ROOT}/python\claims_analyzer.py`

## How to Use

When this skill is invoked:

1. **Load the claims analyzer**:
   ```python
   import sys
   sys.path.insert(0, os.path.join(os.environ.get('CLAUDE_PLUGIN_ROOT', '.'), 'python'))
   from python.claims_analyzer import ClaimsAnalyzer

   analyzer = ClaimsAnalyzer()
   ```

2. **Analyze claims**:
   ```python
   claims_text = """
   1. A system comprising:
       a processor;
       a memory; and
       said processor configured to...
   """

   results = analyzer.analyze_claims(claims_text)
   ```

3. **Present analysis**:
   - Show compliance score (0-100)
   - List issues by severity (critical, important, minor)
   - Provide MPEP citations for each issue
   - Suggest specific fixes

## Analysis Output Structure

```python
{
    "claim_count": 20,
    "independent_count": 3,
    "dependent_count": 17,
    "compliance_score": 85,  # 0-100
    "total_issues": 12,
    "critical_issues": 2,
    "important_issues": 7,
    "minor_issues": 3,
    "issues": [
        {
            "category": "antecedent_basis",
            "severity": "critical",
            "claim_number": 1,
            "term": "said processor",
            "description": "Term 'processor' used with 'said' before first introduction",
            "mpep_cite": "MPEP 2173.05(e)",
            "suggestion": "Change 'said processor' to 'the processor' or introduce with 'a processor' first"
        },
        # ... more issues
    ]
}
```

## Common Issues Detected

1. **Antecedent Basis Errors**:
   - Using "said/the" before "a/an" introduction
   - Terms appearing in dependent claims not in parent
   - Missing antecedent in claim body

2. **Definiteness Issues**:
   - Subjective terms: "substantially", "about", "approximately"
   - Relative terms: "large", "small", "thin"
   - Ambiguous language: "and/or", "optionally"

3. **Structure Issues**:
   - Means-plus-function without adequate structure
   - Improper claim dependencies
   - Missing preamble or transition

## Presentation Format

Present analysis as:

```
CLAIMS ANALYSIS REPORT
======================

Summary:
- Total Claims: 20 (3 independent, 17 dependent)
- Compliance Score: 85/100
- Issues Found: 12 (2 critical, 7 important, 3 minor)

CRITICAL ISSUES (Must Fix):

[Claim 1] Antecedent Basis Error
  Issue: Term 'processor' used with 'said' before introduction
  Location: "said processor configured to..."
  MPEP: 2173.05(e)
  Fix: Change to 'the processor' or introduce with 'a processor' first

[Claim 5] Indefinite Term
  Issue: Subjective term 'substantially' without definition
  Location: "substantially similar to..."
  MPEP: 2173.05(b)
  Fix: Define 'substantially' in specification or use objective criteria

IMPORTANT ISSUES:
...

MINOR ISSUES:
...
```

## Integration with MPEP

For each issue, the skill can:
1. Search MPEP for relevant guidance
2. Provide specific MPEP section citations
3. Show examiner guidance on similar issues
4. Suggest fixes based on USPTO practice

## Tools Available

- **Read**: To load claims from files
- **Bash**: To run Python analyzer
- **Write**: To save analysis reports
