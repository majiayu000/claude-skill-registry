---
name: clerk-token-ops
description: Automates Clerk JWT token generation, validation, and export for FastAPI integration tests. Use when an agent must refresh tokens, verify JWT templates, or unblock authentication workflows without breaking environment state.
---

# Clerk Token Operations

## Overview
This skill gives Claude Code agents a repeatable, zero-surprise playbook for generating Clerk JWTs, exporting them into the Windows PowerShell environment, and validating authentication against the FastAPI backend. It encodes the exact fixes from the November 2025 incidents (missing templates, parser errors, stale tokens) so future runs avoid the same failures.

## Activation Signals
Use this skill whenever the task involves:
- Minting or refreshing Clerk JWTs for integration, smoke, or load tests.
- Investigating 401 responses due to expired or malformed tokens.
- Ensuring `.env.local` and PowerShell sessions stay in sync (`CLERK_SECRET_KEY`, `CLERK_TOKEN`).
- Listing or validating Clerk JWT templates (e.g., `server-token`).
- Teaching another agent how to run `scripts/get_clerk_token.py` or `Set-ClerkToken.ps1` safely.

## Guardrails (Do This Before Anything Else)
1. **Never copy Markdown links into the terminal.** Always use raw paths like `scripts/Set-ClerkToken.ps1`.
2. **Use real Clerk user IDs (e.g., `user_35KgiAcvIC0tdtFvJUN1vDkrNYc`).** Angle brackets or placeholders break PowerShell parsing.
3. **Confirm `.env.local` exists** and contains `CLERK_SECRET_KEY`, `CLERK_ISSUER`, `CLERK_PEM_PUBLIC_KEY`, and `CLERK_ISSUER_ID`.
4. **Restart FastAPI** after changing `.env.local`; environment variables load only once per process.
5. **Tokens expire in ~60 seconds.** Chain generation and testing without delay.

## Core Workflow
1. **Validate Environment**
   - Run `Test-Path .env.local` and open the file if missing keys.
   - Ensure `CLERK_JWT_AUDIENCE` stays commented out; session tokens lack `aud`.
2. **Inspect Available JWT Templates**
   - `powershell -File .\scripts\Set-ClerkToken.ps1 -ListTemplates`
   - Confirm `server-token` exists; if missing, create it in the Clerk dashboard with RS256 signing.
3. **Generate & Export Token**
   - `powershell -File .\scripts\Set-ClerkToken.ps1 -UserId <ACTUAL_USER_ID> -Template server-token [-Persist]`
   - Expect: "CLERK_TOKEN exported..." and optional persistence notice.
4. **Verify Token Availability**
   - `echo $env:CLERK_TOKEN`
   - Optional: `python scripts/get_clerk_token.py --env-file .env.local --user-id ... --template server-token --print-session` for debugging.
5. **Run Target Tests or API Calls Immediately**
   - Example test harness: `uv run python main/scripts/test_clerk_auth.py "$env:CLERK_TOKEN" fixtures/test_urs.txt`
   - For curl: `curl -H "Authorization: Bearer $env:CLERK_TOKEN" http://localhost:8000/jobs -d @payload.json -H "Content-Type: application/json"`
6. **Audit & Log Verification**
   - Tail `logs/audit/jobs/audit_*.jsonl` to ensure the `sub` (user ID) and `token_iat` fields are captured (ALCOA+ compliance).

## Quality Checklist
- [ ] `.env.local` contains correct Clerk keys and issuer URLs.
- [ ] `scripts/get_clerk_token.py` runs without HTTP errors and prints JWT.
- [ ] `scripts/Set-ClerkToken.ps1` outputs success messages (no `[System.Char]` errors).
- [ ] `$env:CLERK_TOKEN` is non-empty and recent (`token_iat` within 60 seconds).
- [ ] FastAPI endpoint returns 201/200 with token, 401 without token (negative test).
- [ ] Audit log entry includes `user_id` from JWT `sub` claim.

## Troubleshooting Matrix
| Symptom | Root Cause | Fix |
| --- | --- | --- |
| `Method invocation failed because [System.Char] does not contain a method named 'Trim'` | PowerShell treated helper output as char array | Use the patched `Set-ClerkToken.ps1` (Nov 2025). If issue recurs, wrap extraction with `[string]` and ensure token line exists. |
| `Unable to parse JWT from helper output` | Helper didnt emit token (HTTP error, wrong template, or env vars missing) | Re-run helper with `--print-session` and check `.env.local` secrets; confirm template name matches exactly. |
| `Token validation failed: Token is missing the "aud" claim` | Audience verification enabled | Comment out `CLERK_JWT_AUDIENCE` and ensure JWT decode options set `verify_aud=False`. |
| `401 Unauthorized: Token expired` | Delay between generation and use | Regenerate token and chain tests immediately (<60s). Automate generation/test pipeline if needed. |
| `500 Internal Server Error: Authentication system not configured` | FastAPI didnt load `.env.local` | Load dotenv at the top of `main/api/app.py` before other imports; restart server. |

## Example Session (Copy/Paste Ready)
```powershell
# 1. List templates (sanity check)
powershell -File .\scripts\Set-ClerkToken.ps1 -ListTemplates

# 2. Export fresh token for known test user
powershell -File .\scripts\Set-ClerkToken.ps1 -UserId user_35KgiAcvIC0tdtFvJUN1vDkrNYc -Template server-token -Persist

# 3. Verify environment
$env:CLERK_TOKEN

# 4. Exercise FastAPI endpoint (token expires fast!)
uv run python main/scripts/test_clerk_auth.py "$env:CLERK_TOKEN" fixtures/test_urs.txt

# 5. Tail audit logs for attribution
Get-Content logs/audit/jobs/audit_$(Get-Date -Format yyyyMMdd).jsonl -Tail 3
```

## Extension Hooks
- **If tests require Docker Compose:** run `docker compose -f docker-compose.dev.yml up --build api worker` after refreshing tokens.
- **CI usage:** Wrap helper invocation inside a temporary PowerShell profile so `$env:CLERK_TOKEN` is available to downstream `pytest` or `uv run` commands.
- **Documentation updates:** When procedures change, sync with `main/docs/guides/CLERK_INTEGRATION_TESTING.md` and note version in this skill.

## References
- `scripts/get_clerk_token.py` - Python helper hitting Clerk Backend API.
- `scripts/Set-ClerkToken.ps1` - PowerShell wrapper for Windows devs.
- `main/docs/guides/CLERK_INTEGRATION_TESTING.md` - Deep dive guide.
- Anthropic Agent Skills best practices (2025-10-02 spec) for structure and activation cues.

**Maintainer:** Compliance/Test Enablement Team  
**Last Updated:** 2025-11-16  
**Status:** ✅ Ready for Claude Code agents
