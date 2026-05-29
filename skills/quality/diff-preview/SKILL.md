---
name: diff-preview
description: Preview changes before applying them. Shows git diffs, prompts for confirmation, safer than direct edits.
homepage: https://github.com/Khamel83/oneshot
allowed-tools: Read, Write, Edit, Bash
metadata: {"oneshot":{"emoji":"👁️","requires":{"bins":["git"]}}}
---

# /diff-preview - Preview Before Apply

**See changes before they happen.** Safer editing with confirmation prompts.

---

## When To Use

User says:
- "preview changes"
- "show me what will change"
- "diff before apply"
- "safe mode editing"
- Before any multi-file edit operation

---

## How It Works

**Before applying edits:**
1. Run `git diff` to show pending changes
2. Present diff in readable format
3. Ask user to confirm: `Apply these changes? [y/n]`
4. Only apply if user confirms

**For new files:**
1. Show what content will be created
2. Show file path
3. Ask for confirmation

---

## Usage Patterns

### Before Multi-File Edits
```bash
# User: "Rename function across all files"

You do:
1. Run: git diff to check current state
2. Calculate changes: grep -r "oldFunction" --include="*.py"
3. Show preview:
   ```
   📋 Proposed Changes:

   src/auth.py:42
   - def oldFunction(user):
   + def newFunction(user):

   src/api.py:15
   - return oldFunction(data)
   + return newFunction(data)

   2 files will be modified
   ```

4. Ask: "Apply these changes? [y/n/diff]"
   - y: Apply all changes
   - n: Cancel
   - diff: Show full git diff
```

### Before Creating New Files
```bash
# User: "Create a new API endpoint"

You do:
1. Show what will be created:
   ```
   📋 Will Create: src/api/endpoints/user.py

   Content:
   ```python
   from fastapi import APIRouter

   router = APIRouter()

   @router.get("/users/{user_id}")
   async def get_user(user_id: str):
       ...
   ```

   File size: ~250 bytes
   ```

2. Ask: "Create this file? [y/n/edit]"
```

### Integration with Edit Tool
```bash
# Before using Edit tool:
1. Read file to get current content
2. Show proposed edit in diff format:
   ```
   📋 Edit Preview: src/main.py

   @@ -15,7 +15,7 @@
    -     port = int(os.getenv("PORT", 8000))
    +     port = int(os.getenv("PORT", 3000))
   ```

3. Ask: "Apply this edit? [y/n]"
4. Only call Edit tool if user confirms
```

---

## Diff Format

### Compact Preview (default)
```
📋 Proposed Changes (3 files):

✓ src/config.py:12     - Change default port 8000→3000
✓ src/auth.py:45      - Add rate limiting
✓ src/utils/helpers.py - Extract common function

Lines added: 15 | Lines removed: 5 | Files changed: 3
```

### Full Diff
```
📋 Full Diff:

src/config.py
@@ -12,7 +12,7 @@
     """Load configuration from environment."""
-    port = int(os.getenv("PORT", 8000))
+    port = int(os.getenv("PORT", 3000))
     debug = os.getenv("DEBUG", "false").lower() == "true"

src/auth.py
@@ -45,6 +45,10 @@
     def authenticate(self, token: str) -> User:
+        # Rate limiting
+        if self._is_rate_limited(token):
+            raise RateLimitError()
         return self._verify_token(token)

Apply these changes? [y/n/diff/all]
```

---

## Confirmation Prompts

| Prompt | Options | When to Use |
|--------|---------|-------------|
| `Apply? [y/n]` | y=yes, n=no | Single file change |
| `Apply all? [y/n/diff]` | y=yes, n=no, diff=show more | Multi-file change |
| `Create? [y/n/edit]` | y=yes, n=no, edit=modify content | New file |
| `Continue? [y/n/skip]` | y=yes, n=stop all, skip=this file | Batch operation |

---

## Safety Features

### Automatic Diff Before Write
```python
# In your workflow, before Write tool:
1. If file exists: Read it first
2. Compute diff between old and new
3. Show preview to user
4. Only Write if confirmed
```

### Dry Run Mode
```bash
# User says "dry run" or "just show me"
/diff-preview --dry-run "rename oldFunction to newFunction"

# Shows changes without applying any
```

### Rollback Prompt
```bash
# After applying changes:
"Changes applied! Undo with: git checkout -- <files>"
"Create checkpoint? [y/n]"  # Offer to create git commit
```

---

## Integration with Other Skills

### With refactorer
```bash
# refactorer uses diff-preview automatically
User: "refactor to extract common validation"

You do:
1. Analyze code and plan changes
2. Show diff-preview of proposed refactor
3. Wait for confirmation
4. Apply changes
```

### With batch-processor
```bash
# batch-processor shows summary before applying
User: "add license header to all Python files"

You do:
1. Find all matching files: 15 files
2. Show summary: "Will add license to 15 Python files"
3. Show first file as example
4. Confirm: "Apply to all 15 files? [y/n/first]"
```

### With implement-plan
```bash
# After implementing a plan step:
"Step 3/5 complete: Added authentication

Changes:
+ src/auth.py (new file, 120 lines)
+ src/middleware/auth.py (new file, 45 lines)
~ src/main.py (modified, 3 lines added)

Continue to step 4? [y/n/review]"
```

---

## Quick Win from Research

**Competitor**: Cline has built-in diff preview
**Problem**: Direct file edits feel risky
**Solution**: Always show changes before applying
**Result**: Users feel more in control, safer experimentation

---

## Implementation Checklist

When using diff-preview:
- [ ] Show WHAT will change (file list)
- [ ] Show HOW it will change (diff)
- [ ] Show IMPACT (lines added/removed)
- [ ] Ask for CONFIRMATION
- [ ] Only apply if confirmed
- [ ] Offer rollback option

---

## Keywords

diff, preview, changes, safe mode, confirm before apply, show diff, dry run, rollback
