---
name: thor-log-analysis
description: Interpret THOR scan results and explain what findings mean. Use when the user pastes THOR log lines, shares a log file, or asks how to triage Notices/Warnings/Alerts.
---
# THOR Log Analysis Skill

Goal: turn raw THOR output into an investigation plan.

## Analysis Approach

THOR performs live forensic analysis and highlights suspicious elements using signatures. The analyst's job is to evaluate these findings using additional data sources and context.

### Triage Priority

1. **Alerts first** (score 81+) - High-confidence malicious findings
2. **Warnings second** (score 60-80) - Medium-confidence suspicious activity
3. **High-signal Notices** (score 40-59) - YARA matches, known-bad hashes
4. **Low-signal Notices** - Anomaly scores, generic patterns

### Key Principle: High Quantity Reduces Relevance

In contrast to firewall logs, a high number of a particular THOR finding **decreases** its relevance:
- If detected on 100+ endpoints → likely false positive
- If detected on 1-30 endpoints → more likely significant
- Exceptions: confirmed malware campaigns targeting many systems

### Analysis Methods

Two recommended approaches (often combined):

1. **Sort by score (descending)** - Process top-scoring events down to score 80
2. **Analyze by module** - Then switch to module-based analysis with relevant columns

Example workflow:
1. Filter to Alerts and Warnings
2. Process top scores first
3. Group by module (FileScan, ProcessCheck, etc.)
4. Select characteristic fields per module (e.g., FILE + MAIN_REASON for FileScan)

## Rules

- Group by detection type/module (YARA, Sigma, IOC, Anomaly) and by file/path
- For each relevant finding: explain what it is, why it triggered, and what to verify next
- Be explicit when something is likely benign (common false positives)
- Use external tools (VirusTotal, Valhalla, Hybrid Analysis) to verify findings

## References

- [Scoring and Priorities](reference/scoring-and-priorities.md) - Score levels, triage order
- [Common False Positives](reference/common-fps.md) - Known FP patterns by module
- [Module Notes](reference/module-notes.md) - Understanding each THOR module
- [Attribute Evaluation](reference/attribute-evaluation.md) - How to assess finding attributes
- [Analysis Tools](reference/analysis-tools.md) - External tools for verification

## Helper Script

If user provides a log file path, run `scripts/summarize_thor_log.py` to extract a compact summary.

## Output Format

- **Summary** (5-15 lines): What's going on, what stands out
- **Findings table**: Score, type/module, target, why it matters
- **Next steps**: 3-7 concrete follow-ups

## Quick Assessment Questions

For each finding, ask:

1. Is the file digitally signed by a trusted vendor?
2. Is it in an expected location for that software?
3. Does the user's role justify having this tool?
4. Does VirusTotal show low/zero detections?
5. Has this file been in place for a long time unchanged?

If YES to most → Likely FP, document and filter.
If NO to most → Treat as suspicious, investigate further.
