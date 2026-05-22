---
name: gitleaks
description: Scan repository for hardcoded secrets and credentials
argument-hint: "[--path=.] [--verbose]"
tags: [security, secrets, devsecops, pre-commit]
user-invocable: true
---

# Secret Detection with Gitleaks

Scan the repository for hardcoded secrets, API keys, tokens, and credentials using gitleaks patterns.

## What To Do

1. **Check if gitleaks is installed**:
   - Run: `gitleaks version` or install via `choco install gitleaks` / `brew install gitleaks`
   - Alternative: Use regex patterns manually if gitleaks CLI not available

2. **Run full repository scan**:
   ```bash
   gitleaks detect --source=. --report-format=json --report-path=gitleaks-report.json
   ```

3. **Run pre-commit scan** (staged files only):
   ```bash
   gitleaks protect --staged --report-format=json
   ```

4. **Common secret patterns to detect**:
   - AWS: `AKIA[0-9A-Z]{16}`
   - Azure: `AccountKey=[A-Za-z0-9+/=]{86}==`
   - GitHub: `gh[ps]_[A-Za-z0-9_]{36}`
   - JWT: `eyJ[A-Za-z0-9_-]*\.eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*`
   - Connection strings: `(Server|Data Source|mongodb|redis).*?(Password|pwd)=`
   - Private keys: `-----BEGIN (RSA |EC )?PRIVATE KEY-----`

5. **If secrets found**:
   - Rotate the compromised credential IMMEDIATELY
   - Remove from code and use environment variables or Azure Key Vault
   - Add pattern to `.gitignore` and `.gitleaksignore`
   - Use `git filter-repo` to purge from history if already committed

6. **Configure .gitleaks.toml** for custom rules:
   ```toml
   [extend]
   useDefault = true

   [[rules]]
   id = "cosmos-connection-string"
   description = "CosmosDB Connection String"
   regex = '''AccountEndpoint=https://[^;]+;AccountKey=[A-Za-z0-9+/=]+'''
   tags = ["azure", "cosmosdb"]

   [allowlist]
   paths = ["**/*test*", "**/*mock*", "**/appsettings.Development.json"]
   ```

7. **CI/CD Integration**:
   ```yaml
   # Azure Pipelines
   - script: |
       gitleaks detect --source=. --report-format=sarif --report-path=gitleaks.sarif
     displayName: "Secret Scan"
   ```

## Arguments
- `--path=<dir>`: Directory to scan (default: current repo)
- `--verbose`: Show all findings with file paths and line numbers