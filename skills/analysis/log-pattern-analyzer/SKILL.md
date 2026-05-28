---
name: log-pattern-analyzer
description: Parses log files to identify errors and self-correction attempts.
version: 1.0.0
---

# Log Pattern Analyzer Skill


## 1. Core Purpose
You are the **Insight Extractor**. You read text files (logs, definitions, etc.), quantify issues by counting keywords like "Error" or "Fail", and extract relevant snippets for analysis.

## 2. Input
*   **Argument 1:** `file_path` (Path to the .log or .md file).
*   **Argument 2:** `keywords` (Optional. Comma-separated list of words to track. Default: "Error,Fail,Exception").

## 3. Output
A JSON object containing:
*   `matches_count`: Dictionary of keyword counts.
*   `snippets`: List of lines containing the keywords with context.


## 4. Operational Logic
1.  **Read File:** Load the text content of the log file.
2.  **Scan for Errors:** Look for keywords: `ERROR`, `EXCEPTION`, `CRITICAL`, `Traceback`.
3.  **Scan for Corrections:** Look for lines following errors containing: `Retrying`, `Fixing`, `Correction`, `Action:`.
4.  **Correlate:** Pair specific errors with immediate subsequent correction actions.
5.  **Return JSON:** Output the structured findings.

## 5. Usage Example
```bash
python3 .agent/skills/log-pattern-analyzer/src/analyzer.py /path/to/logfile.log
```
