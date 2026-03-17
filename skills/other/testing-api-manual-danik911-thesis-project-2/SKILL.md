---
name: testing-api-manual
description: Manual API testing commands for pharmaceutical test generation workflow. Use when testing Docker-based FastAPI endpoints with Clerk JWT authentication, submitting URS files, and monitoring job execution. Provides WSL-compatible commands for token generation, job submission, status monitoring, and log inspection.
---

# Manual API Testing for Pharmaceutical Test Generation

## Overview

This skill provides verified WSL commands for manual testing of the pharmaceutical test generation API. All commands have been validated on WSL2 with Docker Desktop on ARM64 (Qualcomm Oryon) hardware.

**Verified Status:** ✅ Production-ready (WSL2 + Docker Desktop, ARM64 compatible)

## When to Use This Skill

- Testing Docker-based FastAPI endpoints manually
- Submitting Category 3 URS files to avoid human-in-the-loop consultation
- Monitoring asynchronous job execution in real-time
- Debugging API authentication issues with Clerk JWT
- Validating Task 3.6 fixes (test_suite serialization, retry logic, ALCOA+ logs)
- Inspecting container logs for workflow debugging

## Prerequisites

Before testing, verify:

1. **Docker containers running:**
   ```bash
   docker ps
   # Expected: pharma-api-dev, pharma-worker-dev, pharma-postgres-dev, pharma-localstack-dev
   ```

2. **API accessible on port 8080:**
   ```bash
   curl http://localhost:8080/health
   # Expected: {"status":"healthy"}
   ```

3. **.env.local with Clerk credentials:**
   - CLERK_SECRET_KEY
   - CLERK_ISSUER
   - CLERK_PEM_PUBLIC_KEY

4. **Token generation script:** `scripts/get_clerk_token.py`

5. **Test URS files available:** `datasets/urs_corpus_v2/category_3/URS-020.md`

## Complete Testing Workflow

### Step 1: Generate Clerk JWT Token

**⚠️ CRITICAL:** Use `python3` on WSL2, not `python`.

```bash
# Navigate to project directory
cd /mnt/c/Users/anteb/Desktop/Courses/Projects/thesis_project

# Generate and save token in variable
TOKEN=$(python3 scripts/get_clerk_token.py --user-id user_35KgiAcvIC0tdtFvJUN1vDkrNYc --env-file .env.local)

# Verify token is stored (optional)
echo "Token stored: ${TOKEN:0:50}..."
```

**Expected Output:**
```
Token stored: eyJhbGciOiJSUzI1NiIsImNhdCI6ImNsX0I3ZDRQRDIyMk...
```

**Token Expiry:** Clerk session tokens expire after **60 seconds**. Regenerate if needed.

---

### Step 2: Submit URS Job to API

**Why Category 3?** Category 3 (non-configured products) skips human-in-the-loop consultation, enabling faster end-to-end testing.

```bash
# Submit URS job (Category 3 to avoid human consultation)
curl -X POST http://localhost:8080/jobs \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@datasets/urs_corpus_v2/category_3/URS-020.md"
```

**Expected Success Response:**
```json
{
  "job_id": "67077789-b62b-4751-a475-7ddf77d30708",
  "status": "pending",
  "message": "Job submitted successfully"
}
```

**Common Errors:**

| Error | Cause | Solution |
|-------|-------|----------|
| `{"detail":"Not authenticated"}` | Token expired or invalid | Regenerate token (Step 1) |
| `{"detail":[{"type":"missing","loc":["body","file"],...}]}` | Wrong parameter name | Use `-F "file=@..."` not `-F "urs_file=@..."` |
| `curl: (7) Failed to connect to localhost port 8000` | Wrong port | Use port **8080**, not 8000 |
| `curl: (26) Failed to open/read local data` | File path incorrect | Use relative path from project root |

---

### Step 3: Save Job ID and Monitor Status

**One-Time Check:**
```bash
# Save job_id from Step 2 response
JOB_ID="67077789-b62b-4751-a475-7ddf77d30708"  # Replace with actual job_id

# Check job status
curl http://localhost:8080/jobs/$JOB_ID -H "Authorization: Bearer $TOKEN"
```

**Continuous Monitoring Loop:**
```bash
# Monitor status every 10 seconds (requires jq)
while true; do
  curl -s http://localhost:8080/jobs/$JOB_ID -H "Authorization: Bearer $TOKEN" | jq '.status, .gamp_category'
  sleep 10
done
```

**Expected Status Transitions:**
```
"pending"    →  "processing"  →  "completed"
null         →  "CATEGORY_3"  →  "CATEGORY_3"
```

**Stop Loop:** Press `Ctrl+C`

**Install jq (if not available):**
```bash
sudo apt-get update && sudo apt-get install -y jq
```

---

### Step 4: Watch Container Logs in Real-Time

**API Container Logs:**
```bash
docker logs pharma-api-dev -f --tail=50
```

**Worker Container Logs (Workflow Execution):**
```bash
docker logs pharma-worker-dev -f --tail=50
```

**Stop Logs:** Press `Ctrl+C`

**What to Look For:**
- ✅ `INFO: GAMP-5 Category 3 detected` - Categorization succeeded
- ✅ `INFO: ChromaDB query returned 182 chunks` - RAG retrieval working
- ✅ `INFO: Parallel agents completed` - Research/SME agents finished
- ✅ `INFO: Serialized test suite to YAML` - Test suite generated (Task 3.6 fix)
- ✅ `INFO: ALCOA+ audit record persisted` - Audit logs writing (Task 3.6 fix)
- ❌ `ERROR: ModuleNotFoundError: langfuse.decorators` - Langfuse import error (should be fixed)
- ❌ `WARNING: Job retry 1/3` - Retry loop starting (should stop after 3 retries per Task 3.6)

---

### Step 5: Retrieve Job Results

**Get Complete Job Details:**
```bash
curl -s http://localhost:8080/jobs/$JOB_ID -H "Authorization: Bearer $TOKEN" | jq '.'
```

**Extract Specific Fields:**
```bash
# Status only
curl -s http://localhost:8080/jobs/$JOB_ID -H "Authorization: Bearer $TOKEN" | jq '.status'

# GAMP category
curl -s http://localhost:8080/jobs/$JOB_ID -H "Authorization: Bearer $TOKEN" | jq '.gamp_category'

# Test suite (if available in response)
curl -s http://localhost:8080/jobs/$JOB_ID -H "Authorization: Bearer $TOKEN" | jq '.result.test_suite'

# Error message (if failed)
curl -s http://localhost:8080/jobs/$JOB_ID -H "Authorization: Bearer $TOKEN" | jq '.error'
```

---

## Complete Testing Session Example

```bash
# 1. Generate token
TOKEN=$(python3 scripts/get_clerk_token.py --user-id user_35KgiAcvIC0tdtFvJUN1vDkrNYc --env-file .env.local)
echo "Token: ${TOKEN:0:30}..."

# 2. Submit job
RESPONSE=$(curl -s -X POST http://localhost:8080/jobs \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@datasets/urs_corpus_v2/category_3/URS-020.md")

echo "Response: $RESPONSE"

# 3. Extract job_id
JOB_ID=$(echo "$RESPONSE" | jq -r '.job_id')
echo "Job ID: $JOB_ID"

# 4. Monitor in loop (Ctrl+C to stop)
while true; do
  STATUS=$(curl -s http://localhost:8080/jobs/$JOB_ID -H "Authorization: Bearer $TOKEN" | jq -r '.status')
  echo "[$(date +%H:%M:%S)] Status: $STATUS"

  if [ "$STATUS" = "completed" ] || [ "$STATUS" = "failed" ]; then
    echo "Job finished with status: $STATUS"
    break
  fi

  sleep 10
done

# 5. Get final results
curl -s http://localhost:8080/jobs/$JOB_ID -H "Authorization: Bearer $TOKEN" | jq '.'
```

---

## Task 3.6 Validation Checklist

Use these commands to verify all Task 3.6 fixes work correctly:

### ✅ Fix 1: Test Suite YAML Serialization
```bash
# Check if test_suite key present in workflow result
curl -s http://localhost:8080/jobs/$JOB_ID -H "Authorization: Bearer $TOKEN" | jq '.result.test_suite' | head -20

# Expected: YAML content, NOT null
```

### ✅ Fix 2: consultation_result Optional (Category 3)
```bash
# Watch worker logs for consultation errors
docker logs pharma-worker-dev --tail=100 2>&1 | grep -i "consultation_result"

# Expected: NO errors about missing consultation_result for Category 3
```

### ✅ Fix 3: Infinite Retry Loop Fixed
```bash
# Watch for retry pattern (should stop after 3-4 retries)
docker logs pharma-worker-dev -f 2>&1 | grep -i "retry"

# Expected: Max 3-4 retries, then STOP (no infinite loop)
```

### ✅ Fix 4: ALCOA+ Audit Logs Persist
```bash
# Check if audit logs written to host filesystem
ls -lh main/logs/audit/alcoa_records_*.json

# Expected: Files present with recent timestamps
```

### ✅ Fix 5: Langfuse Instrumentation
```bash
# Check for Langfuse import errors
docker logs pharma-api-dev --tail=200 2>&1 | grep -i "langfuse"
docker logs pharma-worker-dev --tail=200 2>&1 | grep -i "langfuse"

# Expected: NO ModuleNotFoundError: langfuse.decorators
```

---

## Troubleshooting

### Issue: Token Authentication Fails

**Symptoms:**
```json
{"detail":"Not authenticated"}
```

**Solutions:**
1. Regenerate token (expires after 60 seconds):
   ```bash
   TOKEN=$(python3 scripts/get_clerk_token.py --user-id user_35KgiAcvIC0tdtFvJUN1vDkrNYc --env-file .env.local)
   ```

2. Verify token format:
   ```bash
   echo "$TOKEN" | cut -d'.' -f1 | base64 -d 2>/dev/null | jq '.'
   # Should show JWT header with "alg":"RS256"
   ```

3. Check Clerk credentials in .env.local:
   ```bash
   grep CLERK .env.local
   ```

---

### Issue: Containers Not Running

**Symptoms:**
```
curl: (7) Failed to connect to localhost port 8080
```

**Solutions:**
1. Check container status:
   ```bash
   docker ps --format "table {{.Names}}\t{{.Status}}"
   ```

2. Restart containers:
   ```bash
   docker-compose -f docker-compose.dev.yml down
   docker-compose -f docker-compose.dev.yml up -d
   ```

3. Check container logs for errors:
   ```bash
   docker logs pharma-api-dev --tail=50
   docker logs pharma-worker-dev --tail=50
   ```

---

### Issue: File Not Found

**Symptoms:**
```
curl: (26) Failed to open/read local data from file/application
```

**Solutions:**
1. Verify file exists:
   ```bash
   ls -lh datasets/urs_corpus_v2/category_3/URS-020.md
   ```

2. Use correct relative path from project root:
   ```bash
   pwd  # Should be: /mnt/c/Users/anteb/Desktop/Courses/Projects/thesis_project
   ```

3. Try alternative URS files:
   ```bash
   ls datasets/urs_corpus_v2/category_3/
   # Use any URS-*.md file
   ```

---

### Issue: Job Stuck in Processing

**Symptoms:**
- Status never changes from "processing"
- Worker logs show errors or infinite retries

**Solutions:**
1. Check worker logs:
   ```bash
   docker logs pharma-worker-dev -f
   ```

2. Look for specific errors:
   - `ModuleNotFoundError` → Langfuse import error (Task 3.6 fix needed)
   - `WARNING: Job retry X/3` → Workflow failing, check error message
   - `ERROR: Context retrieval failed for key consultation_result` → Task 3.6 fix needed

3. Check job error message:
   ```bash
   curl -s http://localhost:8080/jobs/$JOB_ID -H "Authorization: Bearer $TOKEN" | jq '.error'
   ```

---

## Environment Information

**Tested On:**
- **OS:** Windows 11 with WSL2 (Ubuntu)
- **CPU:** Qualcomm Oryon (ARM 64-bit)
- **Docker:** Docker Desktop for Windows (ARM64)
- **Python:** 3.12
- **FastAPI Port:** 8080 (NOT 8000)

**Key Differences from Native Linux:**
- Use `python3` instead of `python`
- File paths use `/mnt/c/Users/...` for Windows drives
- Docker Desktop runs containers via WSL2 backend

---

## Quick Reference Commands

```bash
# Token generation
TOKEN=$(python3 scripts/get_clerk_token.py --user-id user_35KgiAcvIC0tdtFvJUN1vDkrNYc --env-file .env.local)

# Job submission
curl -X POST http://localhost:8080/jobs -H "Authorization: Bearer $TOKEN" -F "file=@datasets/urs_corpus_v2/category_3/URS-020.md"

# Status check
curl http://localhost:8080/jobs/$JOB_ID -H "Authorization: Bearer $TOKEN"

# Monitor loop
while true; do curl -s http://localhost:8080/jobs/$JOB_ID -H "Authorization: Bearer $TOKEN" | jq '.status, .gamp_category'; sleep 10; done

# Container logs
docker logs pharma-api-dev -f --tail=50
docker logs pharma-worker-dev -f --tail=50

# Container status
docker ps --format "table {{.Names}}\t{{.Status}}"

# Restart containers
docker-compose -f docker-compose.dev.yml restart

# Check audit logs
ls -lh main/logs/audit/alcoa_records_*.json
```

---

## Success Criteria

A successful test execution should show:

1. ✅ Token generated without errors
2. ✅ Job submitted with `job_id` returned
3. ✅ Status transitions: `pending` → `processing` → `completed`
4. ✅ GAMP category detected: `CATEGORY_3`
5. ✅ Test suite present in result (Task 3.6 fix validation)
6. ✅ No consultation_result errors (Task 3.6 fix validation)
7. ✅ Max 3-4 retries on failure (Task 3.6 fix validation)
8. ✅ ALCOA+ audit logs persisted to filesystem (Task 3.6 fix validation)
9. ✅ No Langfuse import errors in logs (Task 3.6 fix validation)

**Estimated Duration:** 5-10 minutes for complete workflow execution

---

## Related Skills

- `testing-api-authentication` - Automated API authentication testing
- `clerk-token-ops` - Clerk JWT token operations and validation
- `langfuse-integration` - Langfuse observability setup

---

**Created:** 2025-11-17
**Last Updated:** 2025-11-17
**Status:** Verified and Production-Ready
