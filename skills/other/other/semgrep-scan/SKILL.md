---
name: semgrep-scan
description: Run Semgrep SAST analysis for security and code quality
argument-hint: "[--config=auto] [--severity=error]"
tags: [security, sast, semgrep, devsecops]
user-invocable: true
---

# Semgrep SAST Scan

Run static application security testing with Semgrep.

## What To Do

1. **Install**: `pip install semgrep` or `brew install semgrep`

2. **Run scan**:
   ```bash
   semgrep scan --config=auto --json --output=semgrep-report.json
   ```

3. **Custom rules for .NET**:
   ```bash
   semgrep scan --config=p/csharp --config=p/owasp-top-ten --config=p/jwt
   ```

4. **CI Integration**:
   ```yaml
   - script: semgrep scan --config=auto --error --json -o semgrep.json
     displayName: "SAST Scan"
   ```

5. **Interpret results**: Fix HIGH/ERROR severity first. Use `--severity=error` to filter.

## Arguments
- `--config=<ruleset>`: Semgrep config (auto, p/csharp, p/owasp-top-ten)
- `--severity=<level>`: Filter by severity (info, warning, error)