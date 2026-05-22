---
name: voice-e2e-test
description: Comprehensive E2E test of voice call pipeline - place call, verify auth flow, monitor transcripts/scores, verify report. Use when user says "test voice e2e", "run voice test", or "full voice test".
---

# Voice E2E Test Skill

End-to-end test of the complete voice call pipeline.

**What this tests:**
- Call initiation and confirmation link generation
- Auth flow (localStorage token storage)
- "We're both here" button functionality
- Real-time transcript creation
- Score updates during call
- Report generation after call ends

---

## Prerequisites

- Docker compose services running locally
- Playwright installed (`pip install playwright && playwright install chromium`)

---

## Step Timing (MANDATORY)

Every step MUST output timing in this exact format:

```
[STEP X] START: HH:MM:SS
... command output ...
[STEP X] END: HH:MM:SS
```

**Wrap every command like this:**
```bash
echo "[STEP 1a] START: $(date +%H:%M:%S)" && \
<actual command here> && \
echo "[STEP 1a] END: $(date +%H:%M:%S)"
```

**Example output:**
```
[STEP 1a] START: 16:20:44
2025-12-23T19:20:45.073422+00:00
[STEP 1a] END: 16:20:45
```

⛔ **No timing output = step not executed properly.** The report timing data comes ONLY from this output. If you don't see `[STEP X] START/END` in your execution results, you cannot report timing for that step.

---

## Dynamic Script Generation

Generate complete Playwright scripts inline for each test step. Don't use pre-written script files.

**Pattern:** Use bash heredoc to write and run a complete Python script:

```bash
python3 << 'EOF'
from playwright.sync_api import sync_playwright

url = "<URL_FROM_PREVIOUS_STEP>"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    # Your test logic here
    browser.close()
EOF
```

**Why this pattern:**
- **Adaptability** - Tailor assertions to what the page actually shows
- **Visibility** - Full test logic visible in one place
- **Simplicity** - No script files to manage or coordinate

**Don't** create and save Playwright scripts to files. Generate them inline for each test step.

---

## Screenshot Organization

Save screenshots in a folder per test run:

```
.playwright/YYYY-MM-DD-{call_sid}/
```

Create the folder after extracting the call_sid from the confirmation link (Step 2).

Example structure:
```
.playwright/2025-12-23-CA0ca856e80663527f8294a0229e111e7b/
  e2e-01-base-url.png
  e2e-02-with-auth.png
  e2e-03-after-refresh.png
  ...
```

---

## Browser Mode

**Default:** Headless (no visible browser window)

**Headed mode:** If the user requests a visible browser (e.g., "headed mode", "visible browser", "watch it run", "show me the browser"), launch Playwright with `headless=False` and `slow_mo=300` so actions are visible.

---

## Failure Detection Rules

**CRITICAL: This is a TEST. Tests can FAIL. Report failures honestly.**

A step FAILS if:
- Expected condition is not met
- Timeout occurs waiting for expected result
- Data retrieved doesn't match the current test (e.g., wrong call_sid, old timestamps)

**Never do these:**
- Present data from a previous test as current results
- Mark a step as PASS without verifying the data matches THIS test
- Skip validation because "something was returned"

**Validation requirements:**
| Step | Must Verify |
|------|-------------|
| Confirmation link | URL contains fresh call_sid |
| Report poll | `created_at` is AFTER call started |
| Transcripts | `call_sid` matches current call |
| Any DB query | Timestamps are from THIS test run |

**When a step fails (FAIL-FAST):**
1. Mark the step as ❌ FAIL
2. Note what was expected vs what happened
3. **SKIP directly to Step 11** (Generate test summary)
4. Do NOT attempt remaining steps - they depend on previous steps

⛔ **Any failure = Skip to report.** Don't waste time on steps that can't succeed.

---

## Test Flow Overview

```
1a. Capture server time (before placing call)
1b. Place call (background) → store task_id
2. Poll for confirmation link (filter by timestamp from 1a)
3. Auth flow + button click (combined Playwright script)
4. Monitor call: screenshots, DB queries, TaskOutput polling (exits early when call ends)
5. Finalize call monitoring
6. Poll for report in DB
7. Verify report content
8. Generate test summary
```

---

## Step 1a: Capture server time

**Before placing the call**, capture the current database time. This prevents retrieving stale confirmation links from previous calls.

<!-- EXACT: Use this command verbatim. -->
```bash
docker compose exec -T api .venv/bin/python << 'PYEOF'
import os
from sqlalchemy import create_engine, text
url = os.environ.get("DATABASE_URL", "").replace("postgresql+asyncpg://", "postgresql://")
engine = create_engine(url)
with engine.connect() as conn:
    row = conn.execute(text("SELECT NOW()")).fetchone()
    print(row[0].isoformat())
PYEOF
```

Store this timestamp (e.g., `2025-12-23T18:05:00+00:00`) - you'll use it in Step 2.

---

## Step 1b: Place the call (background)

**IMPORTANT:** Use Claude Code's `run_in_background: true` parameter to ensure the command doesn't block.

```bash
docker compose exec api python src/scripts/twilio_place_call.py --from '+19736624281' --to '+16505026335' --duration-minutes 2 --audio fight
```

⚠️ **Do NOT wait for this command to complete.** The call runs for up to 2 minutes. Proceed immediately to Step 2 to poll for the confirmation link.

**Store the task_id** returned by Claude Code (e.g., `baa9aac`). You'll use this in Step 4 to detect when the call ends.

---

## Step 2: Poll for confirmation link

Poll every 1 second until link found (max 20 attempts).

**Important:** Use the timestamp from Step 1a to filter out stale links. Replace `{TIMESTAMP_FROM_STEP_1A}` with the actual timestamp captured in Step 1a.

<!-- EXACT: Use this command verbatim. Replace only {TIMESTAMP_FROM_STEP_1A} with actual value. -->
```bash
docker compose exec -T api .venv/bin/python << 'PYEOF'
import os
from sqlalchemy import create_engine, text
url = os.environ.get("DATABASE_URL", "").replace("postgresql+asyncpg://", "postgresql://")
engine = create_engine(url)
with engine.connect() as conn:
    row = conn.execute(text("SELECT content FROM message WHERE content LIKE '%voice call%secure link%' AND created_at > '{TIMESTAMP_FROM_STEP_1A}'::timestamptz ORDER BY created_at DESC LIMIT 1")).fetchone()
    if row:
        print(row[0].split(': ')[1])
    else:
        print("No link found")
PYEOF
```

Extract `call_sid` from URL for later queries.

⛔ **STOP CONDITION - 20 attempts with no result:**
```
IF 20 polling attempts with no confirmation link:
  1. STOP polling immediately
  2. Mark Step 2 as ❌ FAIL
  3. Record: "Expected: Confirmation link within 20 attempts. Actual: No link found."
  4. Proceed to Step 8 (Generate test summary)

DO NOT continue polling past 20 attempts.
```

---

## Step 3: Auth flow + button click (combined)

This step runs all auth checks and clicks the button in a single Playwright script to minimize delay.

<!-- EXACT: Use this command verbatim. Replace {CALL_SID}, {TOKEN}, and {SCREENSHOT_DIR} with actual values. -->
```bash
echo "[STEP 3] START: $(date +%H:%M:%S)"
python3 .claude/skills/voice-e2e-test/scripts/auth_flow_test.py \
  --call-sid "{CALL_SID}" \
  --token "{TOKEN}" \
  --screenshot-dir "{SCREENSHOT_DIR}"
echo "[STEP 3] END: $(date +%H:%M:%S)"
```

**What the script tests:**
- BASE_URL: localStorage is empty (no auth params)
- FULL_URL: token gets stored after visiting with params
- REFRESH: token persists after page refresh
- BUTTON: "We're both here" button is clicked

**Output format:**
```
[STEP 3] START: 17:14:16
[3:BASE_URL]  START: 17:14:17
[3:BASE_URL]  END: 17:14:18 (1s) - localStorage empty ✓
[3:FULL_URL]  START: 17:14:18
[3:FULL_URL]  END: 17:14:20 (2s) - token stored ✓
[3:REFRESH]   START: 17:14:20
[3:REFRESH]   END: 17:14:21 (0s) - token persists ✓
[3:BUTTON]    START: 17:14:21
[3:BUTTON]    END: 17:14:24 (2s) - button clicked ✓
[STEP 3] END: 17:14:24
```

**Exit code 1 = any sub-step failed.** If script fails, skip to Step 8 (Generate test summary).

---

## Step 4: Monitor call (with early exit detection)

Every 10 seconds, do ALL of the following:

**1. Check if call ended (FIRST):**

Use `TaskOutput` with `block=false` to check if the background call task completed:
```
TaskOutput(task_id={TASK_ID_FROM_STEP_1B}, block=false)
```

- If `status: completed` → call ended, stop monitoring, proceed to Step 5
- If `status: running` → continue with monitoring below

**2. Take screenshot:**
`.playwright/e2e-05-progress-{N}.png`

**3. Check console for errors:**
Look for `[error]` type messages

**4. Query transcripts appearing:**

<!-- EXACT: Use this command verbatim. Replace only {CALL_SID} with actual value. -->
```bash
docker compose exec -T api .venv/bin/python << 'PYEOF'
import os
from sqlalchemy import create_engine, text
url = os.environ.get("DATABASE_URL", "").replace("postgresql+asyncpg://", "postgresql://")
engine = create_engine(url)
with engine.connect() as conn:
    rows = conn.execute(text("SELECT (provider_data->>'segment_number')::int as seg, left(content, 80) as transcript FROM message WHERE provider_data->>'call_sid' = '{CALL_SID}' AND provider_data->>'type' = 'voice_transcript' ORDER BY seg DESC LIMIT 5")).fetchall()
    for row in rows:
        print(f"Segment {row[0]}: {row[1]}")
PYEOF
```

**5. Query scores updating:**

<!-- EXACT: Use this command verbatim. Replace only {CALL_SID} with actual value. -->
```bash
docker compose exec -T api .venv/bin/python << 'PYEOF'
import os
from sqlalchemy import create_engine, text
url = os.environ.get("DATABASE_URL", "").replace("postgresql+asyncpg://", "postgresql://")
engine = create_engine(url)
with engine.connect() as conn:
    rows = conn.execute(text("SELECT (m.provider_data->>'segment_number')::int as seg, me.enrichment_data->>'segment_conflict_health' as health, me.enrichment_data->>'call_score' as score FROM message m LEFT JOIN message_enrichment me ON me.message_id = m.id WHERE m.provider_data->>'call_sid' = '{CALL_SID}' AND m.provider_data->>'type' = 'voice_transcript' ORDER BY seg DESC LIMIT 5")).fetchall()
    for row in rows:
        print(f"Segment {row[0]}: health={row[1]}, score={row[2]}")
PYEOF
```

Report each new segment: "Segment X: health={health}, score={score}"

⛔ **STOP CONDITIONS (whichever comes first):**
```
IF TaskOutput shows status: completed:
  1. Call ended (completed, no-answer, busy, failed, canceled)
  2. Parse output for final call status
  3. Print "Call ended: {status}"
  4. Proceed to Step 5

IF call duration (default 2 min) has elapsed:
  1. Call still running, script will end it
  2. Take final screenshot
  3. Proceed to Step 5

DO NOT monitor indefinitely.
```

---

## Step 5: Finalize call monitoring

Step 4 already detected call completion via TaskOutput.

- Take final screenshot: `.playwright/e2e-05-call-complete.png`
- Record the final call status from TaskOutput (completed, no-answer, etc.)
- Proceed immediately to Step 6

---

## Step 6: Poll for report (after call ends)

Poll every 5 seconds, max 60 seconds.

<!-- EXACT: Use this command verbatim. Replace only {CALL_SID} with actual value. -->
```bash
docker compose exec -T api .venv/bin/python << 'PYEOF'
import os
from sqlalchemy import create_engine, text
url = os.environ.get("DATABASE_URL", "").replace("postgresql+asyncpg://", "postgresql://")
engine = create_engine(url)

sql = """
WITH call_info AS (
  SELECT
    created_at as call_started_at,
    (provider_data->>'voice_auth')::jsonb->>'caller_contact_id' as caller_contact_id
  FROM conversation
  WHERE provider = 'twilio_voice'
    AND provider_key = '{CALL_SID}'
),
caller_one_on_one AS (
  SELECT c.id as conversation_id
  FROM call_info ci
  JOIN person_contacts pc ON pc.id = ci.caller_contact_id::int
  JOIN conversation_participant cp ON cp.person_id = pc.person_id
  JOIN conversation c ON c.id = cp.conversation_id
  WHERE c.type = 'ONE_ON_ONE'
    AND c.state = 'ACTIVE'
  LIMIT 1
)
SELECT m.content, m.created_at
FROM message m
JOIN caller_one_on_one coo ON m.conversation_id = coo.conversation_id
CROSS JOIN call_info ci
WHERE m.content ILIKE '%CALL REPORT%'
  AND m.created_at > ci.call_started_at
ORDER BY m.created_at DESC LIMIT 1;
"""

with engine.connect() as conn:
    row = conn.execute(text(sql)).fetchone()
    if row:
        print(f"Created at: {row[1]}")
        print(f"Content preview: {row[0][:500]}")
    else:
        print("No report found")
PYEOF
```

**Validation (REQUIRED before marking PASS):**
1. Query returns a row (not empty)
2. `created_at` timestamp is AFTER the call's `created_at`
3. Content contains "CALL REPORT"

**Result determination:**
- If query returns empty after 60 seconds → ❌ FAIL (report not generated)
- If query returns a row but `created_at` is before call started → ❌ FAIL (stale report from previous call)
- If all validations pass → ✅ PASS

⛔ **STOP CONDITION - 60 seconds elapsed with no result:**
```
IF polling for 60 seconds with no result:
  1. STOP polling immediately
  2. Mark Step 6 as ❌ FAIL
  3. Record: "Expected: Report within 60s. Actual: No report found."
  4. Proceed to Step 8 (Generate test summary)

DO NOT continue polling past 60 seconds.
```

---

## Step 7: Verify report content

Report should contain:
- "CALL REPORT" header
- Call Quality Score
- Attachment pattern analysis
- Specific quotes from the call

---

## Step 8: Generate test summary

Save to: `tmp/reports/voice_e2e_test_{timestamp}.md`

**Required sections:**

```markdown
# Voice E2E Test Report

**Date:** YYYY-MM-DD HH:MM
**Call SID:** {CALL_SID}
**Overall Result:** PASS / FAIL

## Step Timing

| Step | Description | Start | End | Duration | Result |
|------|-------------|-------|-----|----------|--------|
| 1a | Capture server time | 15:24:00 | 15:24:01 | 1s | ✅ |
| 1b | Place call | 15:24:01 | 15:24:03 | 2s | ✅ |
| 2 | Confirmation link | 15:24:03 | 15:24:05 | 2s | ✅ |
| 3 | Auth flow + button | 15:24:05 | 15:24:12 | 7s | ✅ |
| 4 | Monitor call | 15:24:12 | 15:26:12 | 120s | ✅ |
| 5 | Wait for complete | 15:26:12 | 15:26:15 | 3s | ✅ |
| 6 | Poll for report | 15:26:15 | 15:26:30 | 15s | ✅ |
| 7 | Verify report | 15:26:30 | 15:26:31 | 1s | ✅ |

**Total Duration:** {sum of all steps}

## Results by Step

| Step | Description | Result | Notes |
|------|-------------|--------|-------|
| 1 | Place call | ✅/❌ | |
| 2 | Confirmation link | ✅/❌ | |
| ... | ... | ... | ... |

## Failures (if any)

### Step X: {step name}
- **Expected:** {what should have happened}
- **Actual:** {what actually happened}
- **Evidence:** {timestamps, screenshots, query results}

## Screenshots
{list all screenshot paths}

## Report Preview (if generated)
{first 500 chars of report, or "NOT GENERATED"}
```

**Honesty requirement:** If ANY step failed, the Overall Result MUST be FAIL. Do not report PASS if steps failed.

---

## Success Criteria

```
Test PASSES only when ALL of these are TRUE:
- [ ] Call placed successfully
- [ ] Confirmation link retrieved (with fresh call_sid)
- [ ] Base URL shows empty localStorage
- [ ] Full URL populates auth token in localStorage
- [ ] Token persists after page refresh
- [ ] "We're both here" button clicked successfully
- [ ] Transcripts appear in DB during call (call_sid matches)
- [ ] Scores update in DB during call
- [ ] No critical console errors during call
- [ ] Report appears in DB after call ends (created_at > call_started_at)
- [ ] Report contains expected sections
- [ ] Test summary saved to tmp/reports/

If ANY checkbox is ❌, overall test result is FAIL.
```

---

## Troubleshooting

**Call doesn't connect:**
- Verify Twilio credentials
- Check server logs: `docker compose logs api --tail 50`

**No transcripts appearing:**
- Check OpenAI Realtime connection
- Verify audio is playing on call

**Scores not updating:**
- Check enrichment pipeline
- Look for errors in RQ worker logs

**Report not generated:**
- Check call actually ended
- Look for report job in RQ queue

---

## Related Skills

- **twilio-test-call** - Simpler call + link flow
- **webapp-testing** - Playwright patterns
- **voice-call-report** - Query call data for reports
