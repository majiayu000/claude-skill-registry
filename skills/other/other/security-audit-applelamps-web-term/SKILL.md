---
name: security-audit
description: Review security of command execution, tool permissions, and API key handling. Use when user mentions "security review", "audit", "check security", "vulnerabilities", or before deploying to production.
allowed-tools: Read, Grep, Glob
---

# Security Audit

## Instructions
1. **Command Execution Review** (`backend/main.py`):
   - Check `run_terminal_command()` for shell injection vulnerabilities
   - Verify timeout is enforced (should be 15 seconds)
   - Look for dangerous command patterns

2. **Tool Permission Review**:
   - Verify Chat mode only allows: `read_file`, `web_search`
   - Check Agent mode tool restrictions
   - Look for permission bypass vulnerabilities

3. **Secrets Management**:
   - Ensure `.env` is in `.gitignore`
   - Check no API keys are hardcoded
   - Verify `python-dotenv` usage for environment variables

4. **WebSocket Security**:
   - Check for authentication on `/ws` endpoint
   - Review message validation
   - Look for injection points in user input

5. **Frontend Security**:
   - Check for XSS in markdown rendering
   - Review image upload handling (base64 encoding)
   - Verify no sensitive data in client-side code

6. Generate report with:
   - Critical issues (immediate action required)
   - Warnings (should fix before production)
   - Recommendations (best practices)

## Examples
- "Run a security audit"
- "Check for vulnerabilities"
- "Review security before deploy"

## Guardrails
- This is a READ-ONLY audit; do not modify files
- Report findings without exploiting vulnerabilities
- Recommend fixes but get user approval before implementing
- Never log or expose discovered secrets
