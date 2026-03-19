---
name: fix-reason
description: Three-step method step 2. Trace the root cause through logic.
---

# Reason (三步法 Step 2)

After observing the symptom:
1. Trace backwards from the symptom to possible causes
2. Check the most likely cause first (80/20 rule)
3. Read the relevant code
4. If multiple possible causes, test each one systematically
5. Confirm root cause before attempting fix

Common root causes:
- Typo in variable name or URL
- Missing dependency or import
- Wrong file path
- Database not connected
- Port already in use
- Permission denied
- API key expired or wrong

DO NOT guess and patch. Find the REAL cause.
