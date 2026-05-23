---
name: yolo
description: |
  Browser automation skill for Lovable deployments. Activates when:
  - yolo_mode: on in CLAUDE.md
  - Running /deploy-edge or /apply-migration commands
  - After git push when auto_deploy: on (automatic detection)
  - Any mention of "yolo mode", "automate Lovable", "browser automation"

  Automatically navigates to Lovable.dev and submits deployment prompts.
  Runs verification tests based on configuration.
  Auto-deploys after git push when enabled.
---

# Yolo Mode Automation Skill

This skill automates Lovable deployment workflows using Claude's browser automation capabilities.

## When to Activate

This skill should be active when:

1. **Yolo mode is enabled** in CLAUDE.md (`yolo_mode: on`)
2. **User runs deployment commands**:
   - `/deploy-edge` - Edge function deployment
   - `/apply-migration` - Database migration application
3. **After git push to main** (if `auto_deploy: on`):
   - Automatically detect backend file changes
   - Trigger deployment without manual command
4. **User mentions yolo automation**:
   - "use yolo mode"
   - "automate the Lovable prompt"
   - "submit this to Lovable automatically"
   - "browser automation"

## Performance Optimization

### Model Selection (Hybrid Approach)

For optimal speed + reliability, use different models for different tasks:

**Use Haiku for:**
- Clicking elements using refs (simple, deterministic)
- Form input operations (`form_input` tool calls)
- Key presses and simple navigation
- Waiting/polling operations
- Simple element finding with `find` tool

**Use Sonnet for:**
- Initial page understanding after navigation
- Error detection and recovery decisions
- Parsing Lovable's responses for success/failure
- Deciding next steps when something unexpected happens
- Complex page state analysis

**Why this matters:**
- Haiku is 3-5x faster for simple operations
- Sonnet provides better reliability for complex reasoning
- Hybrid approach gives best of both: speed + accuracy

### Tool Preferences

**Always prefer these tools:**
- `find` and `read_page` over screenshots for element location
- `form_input` over click + type for input values
- `ref` parameters over coordinates for clicking
- DOM polling over screenshot-based monitoring

See `references/automation-workflows.md` for detailed implementation.

---

## Core Functionality

### 1. Auto-Detection

When yolo mode is enabled, automatically detect when Lovable prompts are needed:

**Edge Function Deployment:**
- Files in `supabase/functions/` modified
- Changes committed and pushed to `main`
- Deployment prompt generated

**Migration Application:**
- New files in `supabase/migrations/`
- Changes committed and pushed to `main`
- Migration prompt generated

See `references/detection-logic.md` for complete detection criteria.

### 1.5. Auto-Deploy After Git Push (NEW)

When `auto_deploy: on` is enabled, Claude automatically detects and deploys backend changes after a successful git push:

**Trigger:** Successful `git push origin main`

**Detection:**
1. Analyze files changed in the push
2. Check for `supabase/functions/` or `supabase/migrations/` changes
3. If backend files found AND auto_deploy enabled → trigger automation

**Flow:**
```
git push origin main [succeeds]
    ↓
Claude detects backend file changes
    ↓
Check: yolo_mode: on AND auto_deploy: on
    ↓
🤖 "Auto-deploy: Backend changes detected, starting deployment..."
    ↓
Execute browser automation
    ↓
Run verification tests
    ↓
Show deployment summary
```

**Graceful Fallback:**
If auto-deploy fails for any reason:
- Show clear error message
- Provide manual prompt as fallback
- Never block the user

See `references/post-push-automation.md` for complete implementation.

### 2. Browser Automation Workflow

When a deployment is needed:

1. **Navigate to Lovable**
   - Read `lovable_url` from CLAUDE.md
   - Open browser and navigate to project
   - Handle login if needed

2. **Submit Prompt**
   - Locate chat input element
   - Type the generated Lovable prompt
   - Submit and confirm message sent

3. **Monitor Response**
   - Wait for Lovable's response
   - Check for success indicators
   - Detect errors or warnings
   - Timeout after 3 minutes

See `references/automation-workflows.md` for detailed browser automation steps.

### 3. Testing & Verification

After successful deployment, run tests based on `yolo_testing` setting:

**If `yolo_testing: on`** (default):
- **Level 1**: Basic verification (check logs via Lovable)
- **Level 2**: Console error checking (monitor production URL)
- **Level 3**: Functional testing (test endpoints/queries)

**If `yolo_testing: off`**:
- Skip all testing
- Only confirm deployment success from Lovable response

See `references/testing-procedures.md` for complete testing workflows.

### 4. Debug Mode

When `yolo_debug: on`, provide verbose output:

```
🐛 DEBUG: Browser Automation

Step 1: Navigating to Lovable
  URL: https://lovable.dev/projects/abc123
  Wait for: Page load complete
  ✅ Success (1.2s)

Step 2: Locating chat interface
  Selector: textarea[data-testid="chat-input"]
  Wait for: Element interactable
  ✅ Found (0.3s)

Step 3: Typing prompt
  Text: "Deploy the send-email edge function"
  ✅ Typed (0.5s)

Step 4: Submitting
  Action: Press Enter
  ✅ Submitted (0.1s)

Step 5: Monitoring response
  Watching for: New message from assistant
  Timeout: 180s
  ✅ Response received (4.2s)

Response content:
"I'll deploy the send-email edge function now..."
[full response text]

Success keywords detected: ['deploy', 'function']
No error keywords found
```

## Configuration in CLAUDE.md

The skill reads these fields from CLAUDE.md:

```markdown
## Yolo Mode Configuration (Beta)

- **Status**: on
- **Auto-Deploy**: on
- **Deployment Testing**: on
- **Auto-run Tests**: off
- **Debug Mode**: off
- **Last Updated**: 2025-01-03 10:30:00
```

**Configuration options:**
- **Status**: Enable/disable yolo mode entirely
- **Auto-Deploy**: Auto-deploy after git push (no manual command needed)
- **Deployment Testing**: Run verification tests after deployments
- **Auto-run Tests**: Run project test suite after git push
- **Debug Mode**: Show verbose automation logs

And from Project Overview:
```markdown
- **Lovable Project URL**: https://lovable.dev/projects/abc123
- **Production URL**: https://my-app.lovable.app
```

## User Notifications

### Progress Updates

Show real-time progress during automation:

**Standard Mode (debug off):**
```
🤖 Yolo mode: Deploying send-email edge function

⏳ Step 1/8: Navigating to Lovable project...
⏳ Step 2/8: Waiting for GitHub sync...
✅ Step 3/8: Sync verified - Lovable has latest code
✅ Step 4/8: Located chat interface
✅ Step 5/8: Submitted prompt
⏳ Step 6/8: Waiting for Lovable response...
✅ Step 7/8: Deployment confirmed
⏳ Step 8/8: Running verification tests...
✅ Step 8/8: All tests passed
```

**Debug Mode (debug on):**
Include detailed logs with timing, selectors, and full responses.

### Deployment Summary

After automation completes:

```
## Deployment Summary

**Operation:** Edge Function Deployment
**Function:** send-email
**Status:** ✅ Success
**Duration:** 45 seconds

**Automation Steps:**
1. ✅ Navigated to Lovable
2. ✅ Submitted deployment prompt
3. ✅ Received deployment confirmation

**Verification Tests:** (if testing enabled)
1. ✅ Basic verification: Deployment logs show no errors
2. ✅ Console check: No errors at production URL
3. ✅ Functional test: Function endpoint responds (200 OK)

**Production Status:**
- Function is live and responding
- No errors detected
- Ready for use

💡 Yolo mode is enabled. I'll continue automating deployments.
   Run `/yolo off` to disable.
```

## Error Handling

All automation failures fall back gracefully to manual prompts:

### Common Errors

**Browser automation not available:**
```
❌ Browser automation unavailable

Yolo mode requires the Claude in Chrome extension.

Install: https://chrome.google.com/webstore/detail/claude/...
Docs: https://docs.claude.com/claude/code-intelligence/browser-automation

Fallback - run this prompt manually in Lovable:
📋 "Deploy the send-email edge function"
```

**Login required:**
```
🔐 Please log in to Lovable

The browser opened to your Lovable project, but you're not logged in.
Please log in and I'll retry automatically.

Or run this prompt manually:
📋 "Deploy the send-email edge function"
```

**UI element not found:**
```
❌ Could not locate Lovable chat interface

The Lovable UI may have changed since this plugin was created.

Fallback - run this prompt manually in Lovable:
📋 "Deploy the send-email edge function"

💡 Please report this issue at:
   https://github.com/10kdigital/lovable-claude-code/issues
```

**Timeout:**
```
⏱️ Lovable hasn't responded after 3 minutes

The operation may still be processing.
Please check Lovable manually to verify status.

Prompt that was submitted:
📋 "Deploy the send-email edge function"
```

**Deployment failed:**
```
❌ Deployment failed in Lovable

Error from Lovable:
[captured error message]

Suggested fixes:
- Check function code for syntax errors
- Verify required secrets are set in Cloud → Secrets
- Review function logs in Lovable

Would you like me to:
1. Review the function code for issues
2. Check if secrets are documented in CLAUDE.md
3. Show you how to access logs in Lovable
```

### Graceful Degradation

When automation fails:
1. Capture error details
2. Show user-friendly error message
3. Provide manual prompt as fallback
4. Suggest troubleshooting steps
5. Offer to disable yolo mode if errors persist

**Never fail silently** - always inform user and provide manual options.

## Integration with Other Commands

### /deploy-edge

When yolo mode is on, `/deploy-edge` automatically triggers browser automation:

```markdown
[... existing deploy-edge logic ...]

## Deployment Execution

1. Check yolo mode status from CLAUDE.md

2. If `yolo_mode: on`:
   - Activate yolo skill
   - Execute browser automation workflow
   - Run tests based on `yolo_testing` setting
   - Report results

3. If `yolo_mode: off`:
   - Show manual prompt (current behavior)
   - Suggest enabling yolo mode
```

### /apply-migration

Same pattern as deploy-edge for migration workflows.

### /yolo

The `/yolo` command controls this skill:
- `/yolo on` - Enables skill by setting `yolo_mode: on`
- `/yolo off` - Disables skill
- Accepts flags: `--testing`, `--no-testing`, `--debug`

## Beta Status & Limitations

### Beta Warning

Yolo mode is in **beta** - users should be aware:

✅ **What works well:**
- Automated prompt submission
- Basic deployment verification
- Error handling with manual fallback

⚠️ **Known limitations:**
- Requires Claude in Chrome extension
- Lovable UI changes may break automation
- Testing adds 1-3 minutes per deployment
- User must be logged into Lovable
- Only works for edge functions and migrations (not tables, RLS, etc.)

### When to Recommend Yolo Mode

✅ **Good for:**
- Frequent deployments (saves time)
- Users comfortable with browser automation
- Development workflows (fast iteration)

❌ **Not ideal for:**
- One-off deployments (manual is faster)
- Production deployments requiring extra review
- Users without Chrome extension
- Environments without browser access

### Future Enhancements

Not yet implemented, but could be added:

1. **Batch operations**
   - Deploy multiple edge functions at once
   - Apply multiple migrations in sequence

2. **Rollback support**
   - Detect deployment failures
   - Offer to rollback via Lovable

3. **Monitoring mode**
   - Periodically check logs
   - Alert on new errors

4. **Custom test scripts**
   - User-defined test payloads
   - Stored in CLAUDE.md

5. **Broader operation support**
   - Table creation
   - RLS policies
   - Storage buckets

## Reference Files

This skill uses these reference documents:

1. **`references/automation-workflows.md`**
   - Browser automation step-by-step
   - Lovable UI navigation
   - Element selectors and wait conditions

2. **`references/detection-logic.md`**
   - When to trigger automation
   - File change detection
   - Integration with commands

3. **`references/post-push-automation.md`** (NEW)
   - Auto-deploy after git push
   - Graceful fallback handling
   - User notification templates

4. **`references/testing-procedures.md`**
   - Level 1: Basic verification
   - Level 2: Console checking
   - Level 3: Functional testing

## Quick Reference

### Check if Yolo Mode is Active

```
1. Read CLAUDE.md
2. Look for "Status: on" in Yolo Mode Configuration
3. If not found or "off", yolo mode is disabled
```

### Check if Auto-Deploy is Enabled

```
1. Read CLAUDE.md
2. Check both "Status: on" AND "Auto-Deploy: on"
3. Both must be enabled for auto-deploy to trigger
```

### Execute Automation

```
1. Confirm yolo_mode is on
2. Load automation-workflows.md
3. Execute navigation → submit → monitor workflow
4. Run tests if yolo_testing is on
5. Report results
```

### Auto-Deploy After Git Push

```
1. Git push succeeds
2. Check for backend file changes (supabase/functions/, supabase/migrations/)
3. If changes found AND auto_deploy enabled:
   - Trigger automation automatically
   - Show: "🤖 Auto-deploy: Backend changes detected..."
4. If auto_deploy disabled:
   - Show notification only
   - Suggest running /deploy-edge or /apply-migration
```

### Handle Errors

```
1. Try automation
2. If fails, capture error
3. Show error + manual fallback prompt
4. Never block user - always provide manual option
5. Suggest troubleshooting based on error type
```

---

*This skill enables hands-free Lovable deployments while maintaining safety through manual fallbacks and comprehensive testing.*
