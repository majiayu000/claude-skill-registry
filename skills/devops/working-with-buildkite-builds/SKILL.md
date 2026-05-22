---
name: working-with-buildkite-builds
description: Use when working with Buildkite CI - checking status, investigating failures, and reproducing issues locally. Provides workflows for monitoring builds, progressive failure investigation, and local reproduction strategies. Use when tempted to use GitHub tools instead of Buildkite-native tools, or when a Buildkite tool fails and you want to fall back to familiar alternatives.
---

# Working with Buildkite Builds

## Overview

This skill provides workflows and tools for working with Buildkite CI builds. It covers **checking status, investigating failures, and reproducing issues locally** rather than creating or configuring pipelines. Use this skill when working with Buildkite builds, especially for PR workflows, post-push monitoring, failure investigation, and local reproduction.

## When to Use This Skill

Use this skill when:

- Checking CI status for the current branch or PR
- Investigating why a build failed
- Monitoring builds after a git push
- Waiting for builds to complete
- Checking build status across multiple repos/PRs
- Understanding what "broken" or other Buildkite states mean

## Tool Hierarchy and Selection

**CRITICAL**: Always use Buildkite-native tools. Never fall back to GitHub tools (`gh pr view`, GitHub API, etc.) - they only show summaries and lose critical information (annotations, logs, real-time updates, state distinctions).

Use tools in this priority order:

### Primary: MCP Tools (Always Use These First)

**Reliability**: Direct Buildkite API access, always available
**Capabilities**: All operations (list, get, wait, unblock)
**When**: Default choice for ALL workflows

Available MCP tools:

- `buildkite:get_build` - Get detailed build information
- `buildkite:list_builds` - List builds for a pipeline
- `buildkite:list_annotations` - Get annotations for a build
- `buildkite:get_pipeline` - Get pipeline configuration
- `buildkite:list_pipelines` - List all pipelines in an org
- **`buildkite:wait_for_build`** - Wait for a build to complete (PREFERRED for monitoring)
- **`buildkite:get_logs`** - Retrieve job logs (CRITICAL for debugging failures)
- `buildkite:get_logs_info` - Get log metadata
- `buildkite:list_artifacts` - List build artifacts

### Secondary: bktide CLI (Convenience)

**Purpose**: Human-readable terminal output
**Limitation**: External dependency, requires npm/npx
**When**: Interactive terminal work when MCP output is too verbose

**Critical Limitation**: bktide CANNOT retrieve job logs. It only displays build summaries and job lists. For log retrieval, always use MCP tools.

Common commands:

```bash
npx bktide pipelines <org>                    # List pipelines
npx bktide builds <org>/<pipeline>            # List builds
npx bktide build <org>/<pipeline>#<build>     # Get build details
npx bktide annotations <org>/<pipeline>#<build>  # Show annotations
```

### Tertiary: Bundled Scripts (Helper Wrappers)

**Purpose**: Pre-built workflows combining multiple tool calls
**Limitation**: External dependencies (bktide, specific versions)
**When**: Convenience wrappers only - use MCP tools if scripts fail

This skill includes scripts for common workflows:

- **`scripts/wait-for-build.js`** - Background monitoring script that polls until build completion
- **`scripts/find-commit-builds.js`** - Find builds matching a specific commit SHA

### Tool Capability Matrix

Different tools have different capabilities. Understanding these limitations prevents wasted effort.

**Key Capabilities:**

| Capability        | MCP Tools | bktide | Scripts |
| ----------------- | --------- | ------ | ------- |
| List builds       | ✅        | ✅     | ✅      |
| Get build details | ✅        | ✅     | ✅      |
| Get annotations   | ✅        | ✅     | ❌      |
| **Retrieve logs** | **✅**    | **❌** | **✅**  |
| Wait for build    | ✅        | ❌     | ✅      |
| Unblock jobs      | ✅        | ❌     | ❌      |

**Most Important**: Only MCP tools and scripts can retrieve job logs. bktide cannot.

For complete capability details and examples, see [references/tool-capabilities.md](references/tool-capabilities.md).

### When Tools Fail: Fallback Hierarchy

**If wait-for-build.js script fails:**

1. ✅ Use `buildkite:wait_for_build` MCP tool instead (preferred)
2. ✅ Use `buildkite:get_build` MCP tool in a polling loop
3. ❌ Do NOT fall back to `gh pr view` or GitHub tools

**If bktide fails:**

1. ✅ Use equivalent MCP tool
2. ❌ Do NOT fall back to GitHub tools

**If MCP tools fail:**

1. ✅ Check MCP server connection status
2. ✅ Restart MCP connection
3. ✅ Report the MCP failure to your human partner
4. ❌ Do NOT fall back to GitHub tools

**Critical**: One tool failing does NOT mean the entire skill is invalid. Move up the hierarchy, don't abandon Buildkite tools.

## Core Workflows

### 1. Investigating a Build from URL (Most Common)

When a user provides a Buildkite URL for a failing build, follow this workflow to investigate.

**Example URL formats:**

- Build URL: `https://buildkite.com/org/pipeline/builds/12345`
- Step URL: `https://buildkite.com/org/pipeline/builds/12345/steps/canvas?sid=019a5f...`

**Step 1: Extract build identifiers from URL**

Parse the URL to extract:

- Organization slug (e.g., "gusto")
- Pipeline slug (e.g., "payroll-building-blocks")
- Build number (e.g., "12345")

Ignore the `sid` query parameter - it's a step ID, not needed for initial investigation.

**Step 2: Get build overview**

```javascript
mcp__MCPProxy__call_tool('buildkite:get_build', {
  org_slug: '<org>',
  pipeline_slug: '<pipeline>',
  build_number: '<build-number>',
  detail_level: 'summary',
});
```

Check the overall build state: `passed`, `failed`, `running`, `blocked`, `canceled`.

**Step 3: Identify failed jobs**

If build state is `failed`, get detailed job information:

```javascript
mcp__MCPProxy__call_tool('buildkite:get_build', {
  org_slug: '<org>',
  pipeline_slug: '<pipeline>',
  build_number: '<build-number>',
  detail_level: 'detailed',
  job_state: 'failed',
});
```

This returns only jobs with `state: "failed"` (not "broken" - see state reference).

**Step 4: Retrieve logs for failed jobs**

For each failed job, extract its `uuid` field and retrieve logs. See "Retrieving Job Logs" workflow below for detailed instructions.

**Step 5: Analyze error output**

Look for:

- Stack traces
- Test failure messages
- Exit codes and error messages
- File paths and line numbers

**Step 6: Reproduce locally**

Follow the "Reproducing Build Failures Locally" workflow below to:

1. Extract the exact command CI ran
2. Translate it to a local equivalent
3. Triage if local reproduction isn't feasible

See the dedicated workflow section for detailed steps.

---

### 2. Retrieving Job Logs

**CRITICAL**: This is the most important capability. Without logs, you cannot debug failures.

Once you've identified a failed job, retrieve its logs to see the actual error.

**Prerequisites:**

- Organization slug
- Pipeline slug
- Build number
- Job UUID (from build details)

**Important**: Job UUIDs ≠ Step IDs. URLs contain step IDs (`sid=019a5f...`), but MCP tools need job UUIDs from the build details response.

**Step 1: Get the job UUID**

If you have a job label (e.g., "ste rspec"), use `get_build` with `detail_level: "detailed"`:

```javascript
mcp__MCPProxy__call_tool('buildkite:get_build', {
  org_slug: 'gusto',
  pipeline_slug: 'payroll-building-blocks',
  build_number: '29627',
  detail_level: 'detailed',
  job_state: 'failed',
});
```

In the response, find the job by matching the `label` field. Extract its `uuid` field (format: `019a5f20-2d30-4c67-9edd-...`).

**Step 2: Retrieve logs using the job UUID**

Use the MCP tool to get logs:

```javascript
mcp__MCPProxy__call_tool('buildkite:get_logs', {
  org_slug: 'gusto',
  pipeline_slug: 'payroll-building-blocks',
  build_number: '29627',
  job_id: '<job-uuid>',
});
```

The response contains the log output from the job execution.

**Common Issues:**

- **"job not found" error**: You likely provided a step ID instead of a job UUID. Step IDs come from URLs (`sid=019a5f...`). Job UUIDs come from `get_build` API responses. Solution: Call `get_build` with `detail_level: "detailed"` to find the correct job UUID.

- **Empty logs**: The job may not have started yet, or logs may not be available yet. Check the job's `state` field first - it should be in a terminal state (`passed`, `failed`, `canceled`).

- **Multiple jobs with same label**: Some pipelines parallelize jobs with the same label (e.g., "rspec (1/10)", "rspec (2/10)"). Filter by the full label string to find the specific failed job.

**Fallback Strategy:**

If MCP tools fail (e.g., connection issues, permissions), you can:

1. Construct the log URL manually and view in browser:

   ```
   https://buildkite.com/{org}/{pipeline}/builds/{build}/jobs/{job-uuid}
   ```

2. Use the bundled script (if available):
   ```bash
   ~/.claude/skills/buildkite-status/scripts/get-build-logs.js <org> <pipeline> <build> <job-uuid>
   ```

**Why bktide Cannot Help:**

The bktide CLI does NOT have a logs command. It can show build summaries and job lists, but cannot retrieve log content. Always use MCP tools for log retrieval.

See [references/tool-capabilities.md](references/tool-capabilities.md) for complete tool capability matrix.

---

### 3. Checking Current Branch/PR Status

This is the most common workflow when working on a branch:

**Step 1: Identify the pipeline and branch**

Determine which pipeline(s) run on PRs for this repository. Common patterns:

- Repository name matches pipeline slug
- Monorepo may have pipeline named after the main repo

**Step 2: Find builds for the current branch**

Use MCP tools to list recent builds:

```javascript
mcp__MCPProxy__call_tool('buildkite:list_builds', {
  org_slug: '<org>',
  pipeline_slug: '<pipeline>',
  branch: '<branch-name>',
  detail_level: 'summary',
});
```

Or use bktide:

```bash
npx bktide builds --format json <org>/<pipeline>
```

**Step 3: Progressive disclosure of status**

Follow this pattern when examining builds:

1. **Overall state** - Is it `passed`, `failed`, `running`, `blocked`, or `canceled`?
2. **Job summary** - How many jobs passed/failed/broken?
3. **Annotations** (if present) - Check for test failures, warnings, or errors
4. **Failed job details** - Get logs for actually failed jobs (not just "broken")

### 4. Post-Push Monitoring Workflow

After pushing code, follow this workflow to monitor the CI build:

**Step 1: Find builds for the pushed commit**

Use the find-commit-builds script:

```bash
~/.claude/skills/buildkite-status/scripts/find-commit-builds.js <org> <commit-sha>
```

Or manually search using MCP tools with commit filter.

**Step 2: Monitor the build**

**Option A (Preferred): Use MCP wait_for_build tool**

```javascript
mcp__MCPProxy__call_tool('buildkite:wait_for_build', {
  org_slug: '<org>',
  pipeline_slug: '<pipeline>',
  build_number: '<build-number>',
  timeout: 1800,
  poll_interval: 30,
});
```

This will:

- Poll every 30 seconds (configurable with `poll_interval`)
- Report status changes
- Complete when build reaches terminal state (passed/failed/canceled)
- Timeout after 30 minutes (configurable with `timeout`)

**Option B (Fallback): Use wait-for-build.js script**

If you prefer background execution:

```bash
~/.claude/skills/buildkite-status/scripts/wait-for-build.js <org> <pipeline> <build-number> --timeout 1800 --interval 30
```

**If the script fails** (e.g., bktide dependency error), use Option A - the MCP tool is more reliable.

**Step 3: Check on progress**

Periodically check the background job or wait for it to complete. When it finishes, check the exit code:

- 0 = passed
- 1 = failed
- 2 = canceled
- 3 = timeout

**Step 4: Investigate failures**

If the build failed, follow the "### 1. Investigating a Build from URL" workflow above.

### 5. Investigating Failures (Deprecated)

**Note**: This workflow is deprecated. Use "### 1. Investigating a Build from URL" and "### 2. Retrieving Job Logs" instead for a more complete investigation process.

When a build has failed, use this systematic approach:

**Step 1: Get build overview**

```javascript
mcp__MCPProxy__call_tool('buildkite:get_build', {
  org_slug: '<org>',
  pipeline_slug: '<pipeline>',
  build_number: '<build-number>',
  detail_level: 'detailed',
  job_state: 'failed', // Only show failed jobs
});
```

This gives you:

- Overall build state
- Job summary (how many failed vs broken)
- List of failed jobs only

**Step 2: Check annotations**

Some projects put test failures in annotations:

```javascript
mcp__MCPProxy__call_tool('buildkite:list_annotations', {
  org_slug: '<org>',
  pipeline_slug: '<pipeline>',
  build_number: '<build-number>',
});
```

Look for annotations with `style: "error"` or `style: "warning"`.

**Important**: Not all projects use annotations. See [references/annotation-patterns.md](references/annotation-patterns.md) for project-specific patterns.

**Step 3: Examine failed jobs**

For each failed job (not "broken" - see state reference below):

1. Get the job details from the build data
2. Check the job's log output
3. Look for stack traces, error messages, or test failures

**Step 4: Understand "broken" vs "failed"**

**Critical**: A job showing as "broken" is often NOT a failure. It typically means:

- The job was skipped because an earlier job failed
- The job's dependencies weren't met
- Conditional pipeline logic determined the job wasn't needed

See [references/buildkite-states.md](references/buildkite-states.md) for complete state explanations.

**Example**: In large monorepos, many jobs show "broken" because they were skipped due to file changes not affecting them. This is normal and expected.

### 6. Checking Blocked Builds

When a build is in `blocked` state, it's waiting for manual approval:

**Step 1: Identify the block step**

Get the build with `detail_level: "detailed"` and look for jobs with `state: "blocked"`.

**Step 2: Review what's being blocked**

Block steps typically have a `label` describing what approval is needed (e.g., "Deploy to Production").

**Step 3: Unblock if appropriate**

Use the MCP tool to unblock:

```javascript
mcp__MCPProxy__call_tool('buildkite:unblock_job', {
  org_slug: '<org>',
  pipeline_slug: '<pipeline>',
  build_number: '<build-number>',
  job_id: '<job-id>',
  fields: {}, // Optional form fields if the block step has inputs
});
```

### 7. Reproducing Build Failures Locally

After investigating a failed build (workflows 1-2), use this workflow to reproduce the failure locally for debugging.

#### Phase 1: Extract

**Goal:** Discover exactly what CI ran - the command, environment, and context.

**Step 1: Get the job logs**

Use workflow "### 2. Retrieving Job Logs" to get logs for the failed job.

**Step 2: Find the actual command**

Look early in the log output for the command execution line. Common patterns:

- **Docker-compose plugin:** `:docker: Running /bin/sh -e -c '<command>' in service <service>`
- **Shell trace:** Lines starting with `+ ` when shell trace is enabled
- **Direct command steps:** Command appears after "Running command" or similar

Example log snippet:
```
Running plugin docker-compose command hook
:docker: Found a pre-built image for app
:docker: Creating docker-compose override file for prebuilt services
:docker: Pulling services app
:docker: Starting dependencies
:docker: Running /bin/sh -e -c 'bin/rspec spec/models/user_spec.rb' in service app
```

The actual command here is `bin/rspec spec/models/user_spec.rb`.

**Step 3: Identify environment variables**

Check multiple sources in order:

1. **Log output** - Some pipelines print env vars at job start
2. **Pipeline config** - Check `.buildkite/pipeline.yml` or buildkite-builder DSL for `env:` blocks
3. **Buildkite defaults** - See [references/buildkite-environment-variables.md](references/buildkite-environment-variables.md) for standard vars like `CI=true`, `BUILDKITE_BRANCH`, etc.
4. **Discover through failure** - If local run fails differently, a missing env var may be the cause

**Step 4: Note the execution context**

Record:

- Was it running in Docker? Which service/image?
- What working directory?
- Any pre-command setup visible in the log?

#### Phase 2: Translate

**Goal:** Convert the CI command to something runnable locally.

**Step 1: Try the direct command first**

Run the extracted command as-is in your local environment:

```bash
bin/rspec spec/models/user_spec.rb
```

This often works for:
- Test commands (`rspec`, `jest`, `pytest`, etc.)
- Linting/formatting tools
- Simple scripts

**Step 2: If direct fails, try with docker-compose**

When the command ran in a Docker context in CI, replicate that locally:

```bash
docker-compose run <service> <command>
```

Example - if CI showed:
`:docker: Running /bin/sh -e -c 'bin/rspec spec/models/user_spec.rb' in service app`

Try locally:
```bash
docker-compose run app bin/rspec spec/models/user_spec.rb
```

**Step 3: Set relevant environment variables**

If the command behaves differently, add env vars discovered in Phase 1:

```bash
CI=true RAILS_ENV=test bin/rspec spec/models/user_spec.rb
```

Or with docker-compose:
```bash
docker-compose run -e CI=true -e RAILS_ENV=test app bin/rspec spec/models/user_spec.rb
```

**Step 4: Handle common translation patterns**

| CI Pattern | Local Translation |
|------------|-------------------|
| `--parallel 4` | `--parallel 1` or remove flag |
| `--format buildkite` | `--format progress` or remove flag |
| CI-specific artifact paths | Use local paths |
| `buildkite-agent artifact download` | Download manually or skip |

#### Phase 3: Triage

**Goal:** When local reproduction isn't feasible, determine the best alternative.

**Decision: Can this be reproduced locally?**

Local reproduction is likely **NOT feasible** when:

- Command needs infrastructure not available locally (specific databases, internal APIs, secrets)
- Environment differences are too significant (specific Linux dependencies, network topology)
- Failure is tied to CI-specific state (parallelization across agents, artifact dependencies from earlier steps)

**Note:** Many Buildkite plugins don't block local reproduction - plugins for artifacts, notifications, or caching are CI orchestration concerns, not execution blockers.

**Alternative 1: Trigger a test build with debugging changes**

Push a branch with modifications to aid debugging:

- Add verbose flags to the failing command (e.g., `--verbose`, `-vvv`)
- Insert `echo` statements or print debugging
- Add env var dumping: `env | sort` or `printenv`
- Modify environment variables in pipeline config
- Temporarily simplify the command to isolate the issue

**Alternative 2: Inspect artifacts**

Download artifacts from the failed build:

```javascript
mcp__MCPProxy__call_tool('buildkite:list_artifacts', {
  org_slug: '<org>',
  pipeline_slug: '<pipeline>',
  build_number: '<build-number>',
});
```

Look for:
- Test output files (JUnit XML, coverage reports)
- Log files written during execution
- Screenshots or other debug outputs

**Alternative 3: Analyze the failure in place**

Sometimes reproduction isn't needed - the logs plus artifacts contain enough information to understand and fix the issue without running it locally.

## Understanding Buildkite States

Buildkite has several states that can be confusing. Here's a quick reference:

### Build States

- `passed` - All jobs completed successfully ✅
- `failed` - One or more jobs failed ❌
- `running` - Build is currently executing 🔄
- `blocked` - Waiting for manual approval 🚫
- `canceled` - Build was canceled ⛔

### Job States

- `passed` - Job succeeded ✅
- `failed` - Job failed with non-zero exit ❌
- `broken` - **MISLEADING**: Usually means skipped due to pipeline logic, NOT a failure ⚠️
- `soft_failed` - Failed but marked as non-blocking 〰️
- `skipped` - Job was skipped ⏭️

**For complete state reference and project-specific patterns**, read [references/buildkite-states.md](references/buildkite-states.md).

## Progressive Disclosure Pattern

Always follow this pattern when checking build status:

1. **Start broad**: Overall build state (passed/failed/running)
2. **Check summary**: Job counts (how many passed/failed/broken)
3. **Check annotations**: If present, they often contain key information
4. **Drill into failures**: Only examine failed jobs (not broken)
5. **Read logs**: Get actual error messages and stack traces

Don't immediately jump to logs - the build state and annotations often tell you what you need to know.

## Project-Specific Patterns

### Large Projects / Monorepos

- **Use annotations heavily**: Test failures are usually summarized in annotations
- **Many "broken" jobs**: Normal due to conditional execution
- **Complex job graphs**: Jobs have dependencies and conditional logic
- **Check annotations first**: They save time vs reading all logs

### Small Projects

- **No annotations**: All information is in job logs
- **Simpler job structure**: Fewer dependencies and conditions
- **"Broken" is unusual**: May indicate an actual problem
- **Read logs directly**: No annotations to summarize failures

## Anti-Patterns: What NOT to Do

### ❌ Falling Back to GitHub Tools

**Don't**: Use `gh pr view`, `gh pr checks`, or GitHub API to check Buildkite status

**Why**: GitHub shows Buildkite check summary only. You lose:

- Real-time build logs and output
- Annotations with test failure details
- Job-level breakdown and states
- Ability to distinguish "broken" (skipped) from "failed"
- Direct build monitoring and waiting
- Proper state information

**Reality**: Always use Buildkite tools. GitHub summarizes; Buildkite is the source of truth.

### ❌ Abandoning Skill on Tool Failure

**Don't**: "The script failed, so I'll use GitHub tools instead"

**Why**: The skill documents MULTIPLE tool tiers:

- MCP tools (primary, always available)
- bktide CLI (secondary, convenience)
- Scripts (tertiary, helpers)

**Reality**: One tool failing doesn't invalidate the skill. Follow the fallback hierarchy - move to MCP tools, don't abandon Buildkite entirely.

### ❌ Emergency Override Rationalization

**Don't**: "This is urgent, I don't have time to follow the skill"

**Why**: Skills exist ESPECIALLY for high-pressure situations. Disciplined workflows prevent mistakes when you're rushed. Making wrong tool choices under pressure wastes MORE time debugging.

**Reality**: Following the skill is FASTER than recovering from wrong decisions. Taking 2 minutes to use the right tool saves 20 minutes of confusion.

### ❌ "I Already Know X" Rationalization

**Don't**: "I already know `gh pr view` works, why learn Buildkite tools?"

**Why**: Familiarity ≠ effectiveness. You'll spend more time working around GitHub's limitations than learning the proper tools.

**Reality**: Invest 2 minutes learning Buildkite MCP tools once. Save hours across all future builds.

## Red Flags - STOP

If you catch yourself thinking ANY of these thoughts, you're about to violate this skill:

- "The script failed, so the skill doesn't apply"
- "This is an emergency, no time for the skill"
- "I already know gh pr view works"
- "GitHub tools show the same information"
- "I'll just check GitHub quickly"
- "One tool failed, so I'll use what I know"
- "The skill is for normal situations, not emergencies"
- "I don't have time to learn new tools right now"

**These are rationalizations. Stop. Follow the tool hierarchy. Use Buildkite MCP tools.**

## Common Mistakes to Avoid

1. **Treating "broken" as "failed"**: Broken usually means skipped, not failed
2. **Ignoring annotations**: They often contain the most actionable information
3. **Not filtering by state**: Use `job_state: "failed"` to focus on actual failures
4. **Missing blocked builds**: A blocked build won't progress without manual intervention
5. **Polling in foreground**: Use MCP `wait_for_build` tool or background scripts

## Tips for Efficient Status Checking

1. **Use detail levels**: Start with `detail_level: "summary"` to reduce data
2. **Filter by job state**: Request only failed jobs when investigating
3. **Background monitoring**: Run wait-for-build.js in background after pushing
4. **Check annotations first**: For projects that use them, they're faster than logs
5. **Trust the scripts**: The bundled scripts handle polling, timeouts, and edge cases

## Resources

### References

- **[buildkite-states.md](references/buildkite-states.md)** - Complete guide to Buildkite states, including the misleading "broken" state and project-specific patterns
- **[annotation-patterns.md](references/annotation-patterns.md)** - How different projects use annotations and when to check them
- **[tool-capabilities.md](references/tool-capabilities.md)** - Comprehensive capability matrix for MCP tools, bktide, and scripts
- **[url-parsing.md](references/url-parsing.md)** - Understanding Buildkite URLs, step IDs vs job UUIDs
- **[troubleshooting.md](references/troubleshooting.md)** - Common errors, solutions, and decision tree for when stuck
- **[buildkite-environment-variables.md](references/buildkite-environment-variables.md)** - Standard Buildkite environment variables for local reproduction

### Scripts

- **[wait-for-build.js](scripts/wait-for-build.js)** - Background monitoring with timeout and polling
- **[find-commit-builds.js](scripts/find-commit-builds.js)** - Find builds for a specific commit
- **[get-build-logs.js](scripts/get-build-logs.js)** - Helper for log retrieval with UUID resolution (placeholder)
- **[parse-buildkite-url.js](scripts/parse-buildkite-url.js)** - Extract components from Buildkite URLs

Run scripts with `--help` for usage information.
