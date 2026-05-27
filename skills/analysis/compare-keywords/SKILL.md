---
name: compare-keywords
description: Compare keyword sets between resume and job description. Returns match statistics including score, missing keywords, and intersection.
---

# Compare Keywords

## Overview

Compares two sets of keywords (e.g., from a resume and a job description) to calculate a match score and identify gaps.

## Usage

### Compare Script

**Syntax:**

```bash
python3 .agent/skills/compare-keywords/scripts/compare_keywords.py <resume_keywords> <job_keywords>
```

**Input Format:**
Files should be either:
*   JSON list of strings: `["python", "agile", "tdd"]`
*   Newline-separated text

**Example:**

```bash
python3 .agent/skills/compare-keywords/scripts/compare_keywords.py resume_skills.json job_requirements.txt
```

**Output:**

```json
{
  "score": 0.66,
  "match_count": 2,
  "total_required": 3,
  "matches": ["python", "agile"],
  "missing": ["tdd"]
}
```
