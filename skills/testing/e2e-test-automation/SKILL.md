---
name: e2e-test-automation
description: >
  Execute end-to-end tests for Nikita using Telegram MCP, Gmail MCP, Supabase MCP,
  Chrome DevTools MCP, and gcloud CLI. Use when verifying implementations, testing
  user journeys, validating integrations, performing regression testing, or after
  completing any feature implementation. MANDATORY after /implement completes.
degree-of-freedom: medium
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Bash(gcloud:*)
  - Bash(curl:*)
  - MCPSearch
  - mcp__telegram-mcp__*
  - mcp__gmail__*
  - mcp__supabase__*
  - mcp__chrome-devtools__*
---

@.claude/shared-imports/constitution.md
@.claude/shared-imports/CoD_Σ.md

# E2E Test Automation Skill

## Purpose

Execute comprehensive end-to-end tests for Nikita using MCP tools and gcloud CLI.
This skill verifies that implementations work correctly in production by:
- Testing Telegram bot interactions via Telegram MCP
- Verifying OTP/email flows via Gmail MCP
- Validating database state via Supabase MCP
- Testing web portal via Chrome DevTools MCP
- Analyzing production logs via gcloud CLI

## Quick Reference

| Test Scope | MCP Tools Used | Duration |
|------------|----------------|----------|
| `full` | All MCP tools + gcloud | 5-10 min |
| `telegram` | Telegram MCP, Supabase MCP | 2-3 min |
| `portal` | Chrome DevTools MCP | 2-3 min |
| `otp` | Gmail MCP, Supabase MCP | 1-2 min |
| `conversation` | Telegram MCP, Supabase MCP | 3-5 min |

## Workflow Files

Detailed phase-by-phase instructions:
- @workflows/test-discovery.md - Find and analyze test candidates
- @workflows/telegram-testing.md - Telegram bot testing workflow
- @workflows/portal-testing.md - Web portal testing via Chrome DevTools
- @workflows/database-verification.md - Supabase data verification
- @workflows/log-analysis.md - gcloud logs analysis

## References

Supporting documentation:
- @references/mcp-tool-usage.md - How to use each MCP tool
- @references/test-patterns.md - Common E2E test patterns
- @references/failure-modes.md - Common failures and recovery

## Examples

Complete walkthroughs:
- @examples/full-journey-test.md - Complete user journey example

---

## Phase 0: Prerequisites Check

**CRITICAL**: Before running any tests, verify all prerequisites.

### 0.1 Verify MCP Servers Available

```bash
# List available MCP tools
MCPSearch query="telegram"
MCPSearch query="gmail"
MCPSearch query="supabase"
MCPSearch query="chrome"
```

Required servers:
- `telegram-mcp` - For Telegram bot testing
- `gmail` - For OTP/email verification
- `supabase` - For database state verification
- `chrome-devtools` - For portal testing (optional)

### 0.2 Verify Telegram User Context

The Telegram MCP uses the authenticated user's context. Verify by:
```
mcp__telegram-mcp__get_me
```

This returns the user profile associated with the Telegram MCP.

### 0.3 Identify Bot Chat

Find the chat with the Nikita bot:
```
mcp__telegram-mcp__list_chats
```

Look for `@Nikita_my_bot` or the bot's chat ID.

### 0.4 Verify Cloud Run Deployment

```bash
gcloud run services describe nikita-api --region us-central1 --format='value(status.url)'
```

Expected: `https://nikita-api-1040094048579.us-central1.run.app`

---

## Phase 1: Test Execution

### 1.1 Telegram Bot Testing

**Use when**: Testing bot responses, conversation flow, command handling.

```
# Step 1: Find bot chat
mcp__telegram-mcp__list_chats
# Look for Nikita bot

# Step 2: Send test message
mcp__telegram-mcp__send_message chat_id="<bot_chat_id>" text="Hello, testing"

# Step 3: Wait for response (5-10 seconds for LLM)
sleep 10

# Step 4: Get bot responses
mcp__telegram-mcp__get_messages chat_id="<bot_chat_id>" limit=5
```

Verify:
- [ ] Bot responded within reasonable time
- [ ] Response is coherent and on-topic
- [ ] No error messages in response

### 1.2 OTP/Authentication Testing

**Use when**: Testing registration, login, email verification.

```
# Step 1: Trigger OTP request (via Telegram /start or portal)

# Step 2: Search for OTP email
mcp__gmail__search_emails query="from:noreply subject:Nikita code" max_results=5

# Step 3: Read latest OTP email
mcp__gmail__read_email id="<email_id>"

# Step 4: Extract OTP code from email body

# Step 5: Verify OTP was used (check Supabase)
mcp__supabase__execute_sql query="SELECT * FROM pending_registrations ORDER BY created_at DESC LIMIT 5"
```

Verify:
- [ ] OTP email received within 60 seconds
- [ ] OTP code is 8 digits
- [ ] pending_registrations table updated

### 1.3 Database State Verification

**Use when**: Verifying data persistence after actions.

```sql
-- Check user created
SELECT id, telegram_id, chapter, relationship_score FROM users ORDER BY created_at DESC LIMIT 5;

-- Check conversation logged
SELECT id, user_id, type, created_at FROM conversations ORDER BY created_at DESC LIMIT 5;

-- Check generated_prompts populated
SELECT id, user_id, token_count, generation_time_ms, created_at FROM generated_prompts ORDER BY created_at DESC LIMIT 5;

-- Check engagement state
SELECT * FROM engagement_state ORDER BY updated_at DESC LIMIT 5;

-- Check score history
SELECT * FROM score_history ORDER BY created_at DESC LIMIT 5;
```

Execute via:
```
mcp__supabase__execute_sql query="<SQL>"
```

### 1.4 Log Analysis

**Use when**: Checking for errors, verifying request processing.

```bash
# Get recent logs
gcloud run services logs read nikita-api --region us-central1 --limit 100 --format='value(textPayload)'

# Filter for errors
gcloud run services logs read nikita-api --region us-central1 --limit 100 | grep -i error

# Check specific request
gcloud run services logs read nikita-api --region us-central1 --limit 100 | grep -i "user_id"
```

Verify:
- [ ] No unhandled exceptions
- [ ] No 500 errors
- [ ] Request/response times acceptable

### 1.5 Portal Testing (Optional)

**Use when**: Testing web portal functionality.

```
# Step 1: Navigate to portal
mcp__chrome-devtools__navigate_page url="https://your-portal-url.vercel.app"

# Step 2: Take screenshot
mcp__chrome-devtools__take_screenshot

# Step 3: Check for login form
mcp__chrome-devtools__evaluate_script script="document.querySelector('form')?.innerHTML"

# Step 4: Fill and submit form
mcp__chrome-devtools__fill selector="input[name='email']" value="test@example.com"
mcp__chrome-devtools__click selector="button[type='submit']"
```

---

## Phase 2: Test Report Generation

### 2.1 Report Template

After completing tests, generate a structured report:

```markdown
## E2E Test Report - [DATE]

### Scope: [full/telegram/portal/otp/conversation]

### Test Results

| Test | Status | Evidence |
|------|--------|----------|
| Bot response | PASS/FAIL | [response content] |
| Database persistence | PASS/FAIL | [row count] |
| OTP delivery | PASS/FAIL | [email received] |
| Log analysis | PASS/FAIL | [error count] |

### Issues Found

1. **Issue**: [description]
   - **Severity**: P0/P1/P2
   - **Evidence**: [logs/screenshots]
   - **Recommended Action**: [fix/investigate]

### Metrics

- Total test duration: X min
- Bot response time: X ms
- Database query time: X ms
- Errors in logs: X

### Next Actions

- [ ] File issues for failures
- [ ] Update event-stream.md
- [ ] Deploy fixes if critical
```

### 2.2 Log to Event Stream

After test completion, update event-stream.md:

```
[YYYY-MM-DDTHH:MM:SSZ] E2E_TEST: [scope] - [PASS/FAIL] - [summary]
```

Example:
```
[2025-12-21T18:30:00Z] E2E_TEST: telegram - PASS - Bot response, DB persistence, no log errors
```

---

## Phase 3: Failure Handling

### 3.1 When Tests Fail

1. **Capture full error context**
   - MCP response bodies
   - Database query results
   - Log excerpts

2. **Categorize the failure**
   - Infrastructure (Cloud Run, Neo4j, Supabase)
   - Code bug (logic error, missing handler)
   - Configuration (missing env var)
   - External service (Telegram API, OpenAI)

3. **Create GitHub issue** if not trivial:
   ```bash
   gh issue create --title "E2E: [scope] test failure" \
     --body "## Context\n...\n## Evidence\n...\n## Expected\n..."
   ```

4. **Update event-stream.md**:
   ```
   [TIMESTAMP] E2E_FAIL: [scope] - [error type] - [brief description]
   ```

### 3.2 Common Failure Patterns

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| No bot response | Cloud Run cold start, rate limit | Retry after 30s |
| 500 errors in logs | Uncaught exception | Check stack trace |
| Empty DB tables | Missing commit, RLS policy | Check session.commit() |
| OTP not received | Resend SMTP config, rate limit | Check Supabase auth logs |
| Chrome page blank | Portal not deployed | Check Vercel status |

---

## Activation Patterns

This skill auto-activates when:
- User says "run E2E tests", "verify implementation", "test the bot"
- After `/implement` completes successfully
- User invokes `/e2e-test` command
- User asks to "check if it's working in production"

---

## Best Practices

1. **Always run `full` scope** after feature implementations
2. **Check logs first** when bot isn't responding
3. **Verify DB state** before assuming data loss
4. **Use Telegram MCP user** - don't create test fixtures
5. **Document all failures** in event-stream.md
6. **Create issues** for non-trivial failures

---

## Related Skills

- `implement-and-verify` - Runs before E2E testing
- `debug-issues` - Use when E2E reveals bugs
- `sdd-orchestrator` - Workflow coordination

---

**Skill Version**: 1.0.0
**Last Updated**: 2025-12-21
**Change Log**:
- 1.0.0: Initial creation with Telegram, Gmail, Supabase, Chrome MCP support
