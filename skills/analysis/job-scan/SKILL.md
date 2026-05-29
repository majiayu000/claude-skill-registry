---
name: job-scan
description: Search for jobs at a company OR parse a specific job posting. Extracts requirements, calculates fit scores, and tracks market skills.
argument-hint: [company-name-or-url]
---

# Job Scan Workflow

**Load and execute:** `workflows/job-scan/workflow.md`

Read the entire workflow file and execute it step by step. This workflow operates in two modes:

**Search Mode** (company name):
- Trigger: `/job-scan Stripe` or "find jobs at Stripe"
- Searches for current openings at the company
- Presents a list of positions matching your profile
- Lets you select one or multiple to scan
- Processes each through the full analysis pipeline

**Direct Mode** (URL/file):
- Trigger: `/job-scan https://...` or provide a file path
- Parses the specific job posting provided
- Detects duplicates and offers re-validation

**Both modes then:**
1. Extract company information and role details
2. Categorize requirements into MUST-HAVE and NICE-TO-HAVE
3. Calculate fit score against your corpus and constraints
4. Save parsed posting to `research/openings/`
5. Update company profile with tracked opening (if exists)
6. Update `research/market_skills.json` with skill demand data

**Company Profile Integration:** When you scan a job from a company you've profiled via `company-discovery`, the analysis is automatically linked in that company's "Tracked Openings" section.

Follow all steps exactly as written. Embody Scout's analytical approach throughout.

$ARGUMENTS
