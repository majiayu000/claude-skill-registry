---
name: codeql-scan
description: Run CodeQL semantic code analysis for security vulnerabilities
argument-hint: "[--language=csharp|javascript]"
tags: [security, sast, codeql, devsecops]
user-invocable: true
---

# CodeQL Security Analysis

Run GitHub CodeQL for deep semantic vulnerability detection.

## What To Do

1. **GitHub Actions integration** (.github/workflows/codeql.yml):
   ```yaml
   - uses: github/codeql-action/init@v3
     with:
       languages: csharp, javascript
   - uses: github/codeql-action/autobuild@v3
   - uses: github/codeql-action/analyze@v3
   ```

2. **Local analysis** (requires CodeQL CLI):
   ```bash
   codeql database create codeql-db --language=csharp
   codeql database analyze codeql-db --format=sarif-latest --output=codeql.sarif
   ```

## Arguments
- `--language=<lang>`: csharp, javascript, or both