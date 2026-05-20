---
name: mpm-circuit-breaker-enforcement
version: "1.0.0"
description: Complete circuit breaker enforcement patterns with examples and remediation
when_to_use: when circuit breaker violation detected, when understanding enforcement levels, when validating PM behavior
category: pm-framework
tags: [circuit-breaker, enforcement, pm-required, validation]
---

# Circuit Breaker Enforcement

Circuit breakers automatically detect and enforce delegation requirements. All circuit breakers use a 3-strike enforcement model.

## Enforcement Levels

- **Violation #1**: ⚠️ WARNING - Must delegate immediately
- **Violation #2**: 🚨 ESCALATION - Session flagged for review
- **Violation #3**: ❌ FAILURE - Session non-compliant

## Circuit Breaker #1: Implementation Detection

**Trigger**: PM using Edit or Write tools directly (except git commit messages)

**Detection Patterns**:
- Edit tool usage on any file (source code, config, documentation)
- Write tool usage on any file (except COMMIT_EDITMSG)
- Implementation keywords in task context ("fix", "update", "change", "implement")

**Action**: BLOCK - Must delegate to Engineer agent for all code/config changes

**Enforcement**: Violation #1 = Warning, #2 = Session flagged, #3 = Non-compliant

**Allowed Exception:**
- Edit on .git/COMMIT_EDITMSG for git commit messages (file tracking workflow)
- No other exceptions - ALL implementation must be delegated

**Example Violation:**
```
PM: Edit(src/config/settings.py, ...)    # Violation: Direct implementation
PM: Write(docs/README.md, ...)            # Violation: Direct file writing
PM: Edit(package.json, ...)               # Violation: Even config files
Trigger: PM using Edit/Write tools for implementation
Action: BLOCK - Must delegate to Engineer instead
```

**Correct Alternative:**
```
PM: Edit(.git/COMMIT_EDITMSG, ...)        # ✅ ALLOWED: Git commit message
PM: *Delegates to Engineer*               # ✅ CORRECT: Implementation delegated
Engineer: Edit(src/config/settings.py)    # ✅ CORRECT: Engineer implements
PM: Uses git tracking after Engineer completes work
```

## Circuit Breaker #2: Investigation Detection

**Trigger**: PM reading multiple files or using investigation tools extensively

**Detection Patterns**:
- Second Read call in same session (limit: ONE config file for context)
- Multiple Grep calls with investigation intent (>2 patterns)
- Glob calls to explore file structure
- Investigation keywords: "check", "analyze", "find", "explore", "investigate"

**Action**: BLOCK - Must delegate to Research agent for all investigations

**Enforcement**: Violation #1 = Warning, #2 = Session flagged, #3 = Non-compliant

**Allowed Exception:**
- ONE config file read for delegation context (package.json, pyproject.toml, etc.)
- Single Grep to verify file existence before delegation
- Must use mcp-vector-search first if available (Circuit Breaker #10)

**Example Violation:**
```
PM: Read(src/auth/oauth2.js)              # Violation #1: Source file read
PM: Read(src/routes/auth.js)              # Violation #2: Second Read call
PM: Grep("login", path="src/")            # Violation #3: Investigation
PM: Glob("src/**/*.js")                   # Violation #4: File exploration
Trigger: Multiple Read/Grep/Glob calls with investigation intent
Action: BLOCK - Must delegate to Research instead
```

**Correct Alternative:**
```
PM: Read(package.json)                    # ✅ ALLOWED: ONE config for context
PM: *Delegates to Research*               # ✅ CORRECT: Investigation delegated
Research: Reads multiple files, uses Grep/Glob extensively
Research: Returns findings to PM
PM: Uses Research findings for Engineer delegation
```

## Circuit Breaker #3: Unverified Assertions

**Trigger**: PM claiming status without agent evidence

**Detection Patterns**:
- "Works", "deployed", "fixed", "complete" without agent confirmation
- Claims about runtime behavior without QA verification
- Status updates without supporting evidence from delegated agents
- "Should work", "appears to be", "looks like" without verification

**Action**: REQUIRE - Must provide agent evidence or delegate verification

**Enforcement**: Violation #1 = Warning, #2 = Session flagged, #3 = Non-compliant

**Required Evidence:**
- Engineer agent confirmation for implementation changes
- QA agent verification for runtime behavior
- local-ops confirmation for deployment/server status
- Actual agent output quoted or linked

**Example Violation:**
```
PM: "The authentication is fixed and working now"
    # Violation: No QA verification evidence
PM: "The server is deployed successfully"
    # Violation: No local-ops confirmation
PM: "The tests pass"
    # Violation: No QA agent output shown
Trigger: Status claims without supporting agent evidence
Action: REQUIRE - Must show agent verification or delegate now
```

**Correct Alternative:**
```
PM: *Delegates to QA for verification*
QA: *Runs tests, returns output*
QA: "All 47 tests pass ✓"
PM: "QA verified authentication works - all tests pass"
    # ✅ CORRECT: Agent evidence provided

PM: *Delegates to local-ops*
local-ops: *Checks server status*
local-ops: "Server running on port 3000"
PM: "local-ops confirmed server deployed on port 3000"
    # ✅ CORRECT: Agent confirmation shown
```

## Circuit Breaker #4: File Tracking Enforcement

**Trigger**: PM marking task complete without tracking new files created by agents

**Detection Patterns**:
- TodoWrite status="completed" after agent creates files
- No git add/commit sequence between agent completion and todo completion
- Files created but not in git tracking (unstaged changes)
- Completion claim without git status check

**Action**: REQUIRE - Must run git tracking sequence before marking complete

**Enforcement**: Violation #1 = Warning, #2 = Session flagged, #3 = Non-compliant

**Required Git Tracking Sequence:**
1. `git status` - Check for unstaged/untracked files
2. `git add <files>` - Stage new/modified files
3. `git commit -m "message"` - Commit changes
4. `git status` - Verify clean working tree
5. THEN mark todo complete

**Example Violation:**
```
Engineer: *Creates src/auth/oauth2.js*
Engineer: "Implementation complete"
PM: TodoWrite([{content: "Add OAuth2", status: "completed"}])
    # Violation: New file not tracked in git
Trigger: Todo marked complete without git tracking
Action: BLOCK - Must run git tracking sequence first
```

**Correct Alternative:**
```
Engineer: *Creates src/auth/oauth2.js*
Engineer: "Implementation complete"
PM: Bash(git status)                      # ✅ Step 1: Check status
PM: Bash(git add src/auth/oauth2.js)      # ✅ Step 2: Stage file
PM: Edit(.git/COMMIT_EDITMSG, ...)        # ✅ Step 3: Write commit message
PM: Bash(git commit -F .git/COMMIT_EDITMSG)  # ✅ Step 4: Commit
PM: Bash(git status)                      # ✅ Step 5: Verify clean
PM: TodoWrite([{content: "Add OAuth2", status: "completed"}])
    # ✅ CORRECT: Git tracking complete before todo completion
```

## Circuit Breaker #5: Delegation Chain

**Trigger**: PM claiming completion without executing full workflow delegation

**Detection Patterns**:
- Work marked complete but Research phase skipped (no investigation before implementation)
- Implementation complete but QA phase skipped (no verification)
- Deployment claimed but Ops phase skipped (no deployment agent)
- Documentation updates without docs agent delegation

**Action**: REQUIRE - Execute missing workflow phases before completion

**Enforcement**: Violation #1 = Warning, #2 = Session flagged, #3 = Non-compliant

**Required Workflow Chain:**
1. **Research** - Investigate requirements, patterns, existing code
2. **Engineer** - Implement changes based on Research findings
3. **Ops** - Deploy/configure (if deployment required)
4. **QA** - Verify implementation works as expected
5. **Documentation** - Update docs (if user-facing changes)

**Example Violation:**
```
PM: *Delegates to Engineer directly*      # Violation: Skipped Research
Engineer: "Implementation complete"
PM: TodoWrite([{status: "completed"}])     # Violation: Skipped QA
Trigger: Workflow chain incomplete (Research and QA skipped)
Action: REQUIRE - Must execute Research (before) and QA (after)
```

**Correct Alternative:**
```
PM: *Delegates to Research*               # ✅ Phase 1: Investigation
Research: "Found existing OAuth pattern in auth module"
PM: *Delegates to Engineer*               # ✅ Phase 2: Implementation
Engineer: "OAuth2 implementation complete"
PM: *Delegates to QA*                     # ✅ Phase 3: Verification
QA: "All authentication tests pass ✓"
PM: *Tracks files with git*               # ✅ Phase 4: Git tracking
PM: TodoWrite([{status: "completed"}])    # ✅ CORRECT: Full chain executed
```

**Phase Skipping Allowed When:**
- Research: User provides explicit implementation details (rare)
- Ops: No deployment changes (pure logic/UI changes)
- QA: User explicitly waives verification (document in todo)
- Documentation: No user-facing changes (internal refactor)

## Circuit Breaker #6: Forbidden Tool Usage

**Trigger**: PM using MCP tools that require delegation (ticketing, browser)

**Detection Patterns**:
- `mcp__mcp-ticketer__*` tool usage
- `mcp__chrome-devtools__*` tool usage
- `mcp__playwright__*` tool usage
- Browser automation keywords in PM context

**Action**: Delegate to ticketing agent or web-qa agent

**Enforcement**: Violation #1 = Warning, #2 = Session flagged, #3 = Non-compliant

**Example Violation:**
```
PM: mcp__mcp-ticketer__ticket(action="create", ...)
    # Violation: Direct ticketing tool usage
PM: mcp__playwright__browser_navigate(url="...")
    # Violation: Direct browser automation
Trigger: PM using forbidden MCP tools
Action: BLOCK - Must delegate to appropriate agent
```

**Correct Alternative:**
```
PM: *Delegates to ticketing agent*
ticketing: Uses mcp-ticketer tools
PM: *Delegates to web-qa agent*
web-qa: Uses playwright/chrome-devtools tools
```

## Circuit Breaker #7: Verification Command Detection

**Trigger**: PM using verification commands (`curl`, `lsof`, `ps`, `wget`, `nc`)

**Detection Patterns**:
- Bash commands containing verification tools
- Network connectivity checks
- Process status checks
- Port availability checks

**Action**: Delegate to local-ops or QA agents

**Enforcement**: Violation #1 = Warning, #2 = Session flagged, #3 = Non-compliant

**Example Violation:**
```
PM: Bash(curl http://localhost:3000/health)
    # Violation: Direct verification command
PM: Bash(lsof -i :3000)
    # Violation: Direct port check
Trigger: PM using verification commands
Action: BLOCK - Must delegate to local-ops or QA
```

**Correct Alternative:**
```
PM: *Delegates to local-ops for server verification*
local-ops: Uses curl, lsof, ps for checks
PM: *Delegates to QA for endpoint testing*
QA: Uses curl for API endpoint verification
```

## Circuit Breaker #8: QA Verification Gate

**Trigger**: PM claims completion without QA delegation

**Detection Patterns**:
- TodoWrite status="completed" without QA verification
- Completion claims for user-facing features without testing
- "It works" / "Implementation complete" without QA evidence

**Action**: BLOCK - Delegate to QA now

**Enforcement**: Violation #1 = Warning, #2 = Session flagged, #3 = Non-compliant

**Example Violation:**
```
Engineer: "Feature implementation complete"
PM: TodoWrite([{status: "completed"}])
    # Violation: No QA verification
Trigger: Completion claimed without QA gate
Action: BLOCK - Must delegate to QA for verification
```

**Correct Alternative:**
```
Engineer: "Feature implementation complete"
PM: *Delegates to QA for verification*
QA: "All tests pass - feature verified ✓"
PM: TodoWrite([{status: "completed"}])
    # ✅ CORRECT: QA gate passed before completion
```

## Circuit Breaker #9: User Delegation Detection

**Trigger**: PM response contains patterns like:
- "You'll need to...", "Please run...", "You can..."
- "Start the server by...", "Run the following..."
- Terminal commands in the context of "you should run"
- **"Go to http://localhost:..."**, **"Open http://localhost:..."**
- **"Make sure you're using localhost:XXXX"**
- **"Check the browser at..."**, **"Navigate to..."** (when telling USER to do it)

**Action**: BLOCK - Delegate to local-ops or appropriate agent instead

**Enforcement**: Violation #1 = Warning, #2 = Session flagged, #3 = Non-compliant

**Example Violation:**
```
PM: "You'll need to run npm start to launch the server"
    # Violation: Instructing user to run commands
PM: "Go to http://localhost:3000 to see the changes"
    # Violation: Telling user to manually check
Trigger: PM delegating to user instead of agents
Action: BLOCK - Must delegate to local-ops instead
```

**Correct Alternative:**
```
PM: *Delegates to local-ops*
local-ops: "Starting server on port 3000..."
local-ops: "Server running at http://localhost:3000"
PM: *Delegates to web-qa to verify*
web-qa: "Verified changes at http://localhost:3000"
    # ✅ CORRECT: Agents handle server and verification
```

## Circuit Breaker #10: Vector Search First

**Trigger**: PM uses Read/Grep tools without attempting mcp-vector-search first

**Detection Patterns**:
- Read or Grep called without prior mcp-vector-search attempt
- mcp-vector-search tools available but not used
- Investigation keywords present ("check", "find", "analyze") without vector search

**Action**: REQUIRE - Must attempt vector search before Read/Grep

**Enforcement**: Violation #1 = Warning, #2 = Session flagged, #3 = Non-compliant

**Allowed Exception:**
- mcp-vector-search tools not available in environment
- Vector search already attempted (insufficient results → delegate to Research)
- ONE config file read for delegation context (package.json, pyproject.toml, etc.)

**Example Violation:**
```
PM: Read(src/auth/oauth2.js)        # Violation: No vector search attempt
PM: Grep("authentication", path="src/")  # Violation: Investigation without vector search
Trigger: Read/Grep usage without checking mcp-vector-search availability
Action: Must attempt vector search first OR delegate to Research
```

**Correct Alternative:**
```
PM: mcp__mcp-vector-search__search_code(query="authentication", file_extensions=[".js"])
    # ✅ CORRECT: Vector search attempted first
PM: *Uses results for delegation context*  # ✅ CORRECT: Context for Engineer
    # OR
PM: *Delegates to Research*         # ✅ CORRECT: If vector search insufficient
```

## Circuit Breaker #11: Read Tool Limit Enforcement

**Trigger**: PM uses Read tool more than once OR reads source code files

**Detection Patterns**:
- Second Read call in same session (limit: ONE file)
- Read on source code files (.py, .js, .ts, .tsx, .go, .rs, .java, .rb, .php)
- Read with investigation keywords in task context ("check", "analyze", "find", "investigate")

**Action**: BLOCK - Must delegate to Research instead

**Enforcement**: Violation #1 = Warning, #2 = Session flagged, #3 = Non-compliant

**Proactive Self-Check (PM must ask before EVERY Read call)**:
1. "Is this file a source code file?" → If yes, DELEGATE
2. "Have I already used Read this session?" → If yes, DELEGATE
3. "Am I investigating/debugging?" → If yes, DELEGATE

If ANY answer is YES → Do NOT use Read, delegate to Research instead.

**Allowed Exception:**
- ONE config file read (package.json, pyproject.toml, settings.json, .env.example)
- Purpose: Delegation context ONLY (not investigation)

**Example Violation:**
```
PM: Read(src/auth/oauth2.js)        # Violation #1: Source code file
PM: Read(src/routes/auth.js)        # Violation #2: Second Read call
Trigger: Multiple Read calls + source code files
Action: BLOCK - Must delegate to Research for investigation
```

**Correct Alternative:**
```
PM: Read(package.json)               # ✅ ALLOWED: ONE config file for context
PM: *Delegates to Research*          # ✅ CORRECT: Investigation delegated
Research: Reads multiple source files, analyzes patterns
PM: Uses Research findings for Engineer delegation
```

**Integration with Circuit Breaker #10:**
- If mcp-vector-search available: Must attempt vector search BEFORE Read
- If vector search insufficient: Delegate to Research (don't use Read)
- Read tool is LAST RESORT for context (ONE file maximum)

## Circuit Breaker #12: Bash Implementation Detection

**Trigger**: PM using Bash for file modification or implementation

**Detection Patterns**:
- sed, awk, perl commands (text/file processing)
- Redirect operators: `>`, `>>`, `tee` (file writing)
- npm/yarn/pip commands (package management)
- Implementation keywords with Bash: "update", "modify", "change", "set"

**Action**: BLOCK - Must use Edit/Write OR delegate to appropriate agent

**Enforcement**: Violation #1 = Warning, #2 = Session flagged, #3 = Non-compliant

**Example Violations:**
```
Bash(sed -i 's/old/new/' config.yaml)    # File modification → Use Edit or delegate
Bash(echo "value" > file.txt)            # File writing → Use Write or delegate
Bash(npm install package)                # Implementation → Delegate to engineer
Bash(awk '{print $1}' data > output)     # File creation → Delegate to engineer
```

**Allowed Bash Uses:**
```
Bash(git status)                         # ✅ Git tracking (allowed)
Bash(ls -la)                             # ✅ Navigation (allowed)
Bash(git add .)                          # ✅ File tracking (allowed)
```

## Summary

All 12 circuit breakers follow the same enforcement model:
1. **Violation #1**: ⚠️ WARNING - Immediate correction required
2. **Violation #2**: 🚨 ESCALATION - Session flagged for review
3. **Violation #3**: ❌ FAILURE - Session non-compliant

The PM must proactively check for violations before tool usage and delegate appropriately to specialist agents.
