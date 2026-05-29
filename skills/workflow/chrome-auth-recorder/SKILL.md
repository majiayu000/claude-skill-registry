---
name: chrome-auth-recorder
description: |
  Records workflows in authenticated browser sessions and generates annotated GIF tutorials without
  handling credentials. Use when you need to document authenticated processes, create tutorials from
  existing sessions, or capture workflows that require login. Triggers on "record my workflow",
  "document authenticated process", "create tutorial from session", "capture this workflow as GIF",
  or "show me how to do this". Works with Chrome browser via MCP integration and authenticated
  sessions.
---

# Chrome Auth Recorder

## Quick Start

Record an authenticated workflow as an annotated GIF:

User: "Record my workflow for creating a new project in GitHub"
1. Get tab context from authenticated GitHub session
2. Present plan with domains for approval
3. Start GIF recording + capture first frame
4. Guide user OR execute approved actions
5. Monitor console/network for errors
6. Capture final frame + stop recording
7. Export annotated GIF with click indicators

**Key advantage:** Uses existing authenticated browser session - no credential handling required.

## When to Use This Skill

**Explicit Triggers:**
- "Record my workflow" / "Document authenticated process"
- "Create tutorial from session" / "Make a GIF of [workflow]"
- "Show me how to do this" / "Capture this workflow"

**Implicit Triggers:**
- Document multi-step authenticated workflow
- Create tutorial for team using SaaS tool
- Visual proof of process completion

**Debugging Triggers:**
- "Why did this fail?" / "Record the error I'm seeing"
- Need visual evidence for bug reports

## What This Skill Does

End-to-end workflow recording in authenticated sessions:
1. **Session Access** - Uses existing authenticated tab (no credentials)
2. **Plan Approval** - Presents domains/approach for explicit permission
3. **GIF Recording** - Captures visual workflow with frames
4. **Monitoring** - Tracks console errors and network requests
5. **Export** - Generates annotated GIF (click indicators, labels, progress bar)

## Instructions

### Step 1: Get Tab Context

Access user's existing authenticated session:

```
tabs_context_mcp(createIfEmpty=true)
→ Returns: {tabId: 123, url: "https://github.com/dashboard"}

Verify:
- Domain matches workflow requirement
- User appears authenticated (check for login indicators)
- Ask user to navigate if on wrong page
```

### Step 2: Present Plan and Get Approval

Never start recording without explicit permission:

```
update_plan(
  domains=["github.com"],
  approach=[
    "Record repository creation workflow",
    "Capture form interactions",
    "Monitor API calls for errors",
    "Export annotated GIF"
  ]
)

Wait for: "Yes, proceed" or "Go ahead"
If declined: Ask for modifications
```

### Step 3: Start Recording

Initialize GIF recording and capture first frame:

```
gif_creator(action="start_recording", tabId=123)
computer(action="screenshot", tabId=123)  ← REQUIRED first frame
```

### Step 4: Execute Workflow

**Two modes:**

**User-Guided (complex/manual workflows):**
```
Assistant: "Click the '+' icon, then 'New repository'"
[User performs action - captured automatically]
Assistant: "Fill in repository name"
[User types - captured]
```

**Automated (pre-approved repetitive steps):**
```
computer(action="left_click", coordinate=[850, 120], tabId=123)
wait(duration=2)
form_input(ref="ref_1", value="my-project", tabId=123)
computer(action="left_click", ref="ref_2", tabId=123)
```

**Hybrid:** Start user-guided, switch to automated for repetitive parts.

### Step 5: Monitor Session

Track errors and verify API calls during recording:

```
read_console_messages(
  tabId=123,
  pattern="error|exception|failed",
  onlyErrors=true
)

read_network_requests(
  tabId=123,
  urlPattern="/api/"
)

If errors found:
- Inform user immediately
- Ask whether to continue or restart
- Include error context in final GIF
```

### Step 6: Stop and Export

Finalize recording and export annotated GIF:

```
computer(action="screenshot", tabId=123)  ← REQUIRED final frame
gif_creator(action="stop_recording", tabId=123)
gif_creator(
  action="export",
  tabId=123,
  download=true,
  filename="github-create-repo-tutorial.gif",
  options={
    showClickIndicators: true,
    showActionLabels: true,
    showProgressBar: true,
    showWatermark: true,
    quality: 10
  }
)

Verify download successful and inform user.
```

## Supporting Files

**references/**
- `mcp-tools-reference.md` - Detailed MCP tool parameters and patterns
- `troubleshooting.md` - Common issues and solutions (365 lines)

**examples/**
- `examples.md` - 8 comprehensive workflow examples:
  - GitHub repo creation (user-guided)
  - Notion database setup (complex)
  - Jira epic creation (automated)
  - Google Workspace user (privacy-aware)
  - Stripe refund (API verification)
  - Slack channel (hybrid mode)
  - AWS EC2 launch (long-form)
  - Error reproduction (debugging)

## Expected Outcomes

**Successful Recording:**
```
✅ Workflow Recorded Successfully

Session: GitHub - Create New Repository
Duration: 45 seconds, Frames: 23, Size: <2MB
GIF: github-create-repo-tutorial.gif (Downloads/)
Annotations: Click indicators, labels, progress bar, watermark
Console: 0 errors
Network: 3 API calls successful (POST /repos → 201)

Tutorial ready for sharing!
```

**Recording with Warnings:**
```
⚠️ Workflow Recorded with Warnings

Warnings:
1. Console: "Deprecated API call"
2. Network: GET /preferences (429 Rate Limited)

GIF exported with warning annotations.
Recommendation: Review before sharing.
```

## Expected Benefits

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Tutorial creation time | 30-60 min | 5-10 min | 80% faster |
| Credential exposure risk | High | None | 100% safer |
| Annotation consistency | Manual | Automated | 100% reliable |
| Error detection | Manual | Real-time | Immediate visibility |

## Success Metrics

A successful recording meets all criteria:

✅ User approved plan before recording started
✅ GIF captured all workflow steps
✅ Annotations clearly show clicks and actions
✅ No credentials visible in frames
✅ Console/network monitoring completed
✅ GIF downloaded successfully
✅ File size reasonable (<5MB for 30-60 sec)
✅ Visual quality sufficient for tutorial use

## Requirements

**Browser:** Chrome with MCP integration, authenticated session active
**User:** Explicit approval, clear workflow steps, awareness of recording scope
**Technical:** MCP tools (tabs_context_mcp, gif_creator, computer), network access, disk space

## Red Flags to Avoid

1. **Starting recording without approval** - Always use update_plan first
2. **Recording sensitive data entry** - Pause before passwords/keys
3. **Missing first/last frames** - Always screenshot after start and before stop
4. **Ignoring console errors** - Always read console_messages during workflow
5. **Not monitoring network** - Always check network_requests for failures
6. **Exporting without annotations** - Enable all indicators/labels
7. **Vague filenames** - Use "github-create-repo.gif", not "recording.gif"
8. **Skipping verification** - Confirm GIF downloaded successfully
9. **Recording without context** - Get tabs_context_mcp first
10. **Continuing after critical errors** - Ask user whether to continue

## Notes

**Privacy Protection:**
- NEVER record sensitive data entry (passwords, credit cards, API keys)
- Ask user to navigate away from sensitive pages before recording
- Warn if sensitive data visible in current state
- Consider pausing recording during credential entry

**Performance:**
- Long recordings (>2 min) create large GIFs (>10MB)
- Split workflows into multiple shorter GIFs if needed
- Use quality=10 for size/clarity balance
- Slow down actions for clearer captures

**Browser Session:**
- Recording captures visual state only (not DOM/cookies)
- User remains authenticated after completion
- No session state modified (read-only, safe for production)

**Best Practices:**
- Test workflow manually before recording
- Slow down actions for better frame separation
- Add pauses between steps (1-2 seconds)
- Narrate actions in chat during recording for context
- Review console/network logs before exporting
- Use descriptive filenames for easy identification

**Workflow Patterns:**
- **User-Guided:** Best for complex/manual workflows
- **Automated:** Best for repetitive/approved workflows
- **Hybrid:** Start user-guided, switch to automated for repetition

**Integration:**
- Use with `quality-code-review` - Record demo of new feature
- Use with `create-adr-spike` - Capture research workflow
- Use with `observability-analyze-logs` - Record error reproduction
