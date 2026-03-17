---
name: meta-methodology-write-verification
description: Write verification protocol - never report success without verifying work was actually saved. Re-read files after edits, verify changes exist, only report success after verification passes.
---

# Write Verification Protocol

> **Quick Guide:** Never report success without verifying work was actually saved. Re-read files after edits, verify changes exist, only report success after verification passes.

---

<critical_requirements>

## CRITICAL: Verify All File Operations

**(Never report success without verifying your work was actually saved)**

**(Re-read files after completing edits)**

**(Verify changes exist in the file before reporting success)**

**(If verification fails, re-attempt the edit - do NOT report success)**

</critical_requirements>

---

<write_verification_protocol>

**CRITICAL: Never report success without verifying your work was actually saved.**

### Why This Exists

Agents can:

1. Analyze what needs to change
2. Generate correct content
3. Plan the edits
4. **Fail to actually execute the Write/Edit operations**
5. **Report success based on the plan, not reality**

This causes downstream failures that are hard to debug because the agent reported success.

### Mandatory Verification Steps

**After completing ANY file edits, you MUST:**

1. **Re-read the file(s) you just edited** using the Read tool
2. **Verify your changes exist in the file:**
   - For new content: Confirm the new text/code is present
   - For edits: Confirm the old content was replaced
   - For structural changes: Confirm the structure is correct
3. **If verification fails:**
   - Report: "VERIFICATION FAILED: [what was expected] not found in [file]"
   - Do NOT report success
   - Re-attempt the edit operation
4. **Only report success AFTER verification passes**

### Verification Checklist

Include this in your final validation:

```
**Write Verification:**
- [ ] Re-read file(s) after completing edits
- [ ] Verified expected changes exist in file
- [ ] Only reporting success after verification passed
```

</write_verification_protocol>

---

<agent_types>

### What To Verify By Agent Type

**For code changes (frontend-developer, backend-developer, tester):**

- Function/class exists in file
- Imports were added
- No syntax errors introduced

**For documentation changes (documentor, pm):**

- Required sections exist
- Content matches what was planned
- Structure is correct

**For structural changes (skill-summoner, agent-summoner):**

- Required XML tags present
- Required sections exist
- File follows expected format

**For configuration changes:**

- Keys/values are correct
- File is valid (JSON/YAML parseable)

</agent_types>

---

<critical_reminders>

## CRITICAL REMINDERS

**(NEVER report task completion based on what you planned to do)**

**(ALWAYS verify files were actually modified before reporting success)**

**(A task is not complete until verification confirms the changes exist)**

**(Re-read files after edits to confirm changes were saved)**

**(If verification fails, re-attempt the operation)**

</critical_reminders>
