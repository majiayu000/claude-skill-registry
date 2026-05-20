---
name: verify-persistence
description: >
  Verify persistence.xml configuration before git push. Use before pushing code to
  ensure persistence.xml uses environment variables instead of hardcoded JNDI names.
  Prevents QA deployment failures.
disable-model-invocation: true
allowed-tools: Read, Grep, Bash
---

# Verify Persistence Configuration

Check `src/main/resources/META-INF/persistence.xml` for deployment readiness.

## Steps

1. **Read persistence.xml** at `src/main/resources/META-INF/persistence.xml`

2. **Check JNDI datasources** - Must use environment variables:
   - `${JDBC_DATASOURCE}` (not `jdbc/coop`, `jdbc/rhDS`, etc.)
   - `${JDBC_AUDIT_DATASOURCE}` (not `jdbc/ruhunuAudit`, etc.)

3. **Check DDL generation paths** - Must NOT contain hardcoded paths:
   - No `eclipselink.application-location` with `c:/tmp/` or `/home/*/tmp/`

4. **Report findings** clearly:
   - If all correct: "Persistence.xml is deployment-ready"
   - If issues found: List each issue with the current value and what it should be

## What's Correct vs Wrong

| Setting | Correct | Wrong |
|---------|---------|-------|
| Main datasource | `${JDBC_DATASOURCE}` | `jdbc/coop`, `jdbc/rhDS` |
| Audit datasource | `${JDBC_AUDIT_DATASOURCE}` | `jdbc/ruhunuAudit` |
| DDL location | Not present or env var | `c:/tmp/`, `/home/buddhika/tmp/` |

## If Issues Found

Offer to fix by replacing hardcoded values with environment variables. Do NOT auto-fix without user confirmation.
