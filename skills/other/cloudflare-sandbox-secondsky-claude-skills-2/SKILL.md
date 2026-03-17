---
name: cloudflare-sandbox
description: Cloudflare Sandboxes SDK for secure code execution in Linux containers at edge. Use for untrusted code, Python/Node.js scripts, AI code interpreters, git operations.

  Keywords: cloudflare sandbox, container execution, code execution, isolated environment, durable objects, linux container, python execution, node execution, git operations, code interpreter, AI agents, session management, ephemeral container, workspace, sandbox SDK, @cloudflare/sandbox, exec(), getSandbox(), runCode(), gitCheckout(), ubuntu container
license: MIT
---

# Cloudflare Sandboxes SDK

**Status**: Production Ready (Open Beta)
**Last Updated**: 2025-12-10
**Dependencies**: `cloudflare-worker-base`, `cloudflare-durable-objects` (recommended for understanding)
**Latest Versions**: `@cloudflare/sandbox@0.6.3`, Docker image: `cloudflare/sandbox:0.6.3-python`

**⚠️ BREAKING CHANGE (v0.6.0):** Python is no longer included in the default image. Use `cloudflare/sandbox:<version>-python` for Python support (~1.3GB with data science packages). The lean variant (~600-800MB) excludes Python.

---

## Quick Start (15 Minutes)

### 1. Install SDK and Setup Wrangler

```bash
bun add @cloudflare/sandbox@latest  # preferred
# or: bun add @cloudflare/sandbox@latest
```

**wrangler.jsonc:**
```jsonc
{
  "name": "my-sandbox-worker",
  "main": "src/index.ts",
  "compatibility_flags": ["nodejs_compat"],
  "containers": [{
    "class_name": "Sandbox",
    "image": "cloudflare/sandbox:0.6.3-python",
    "instance_type": "lite"
  }],
  "durable_objects": {
    "bindings": [{
      "class_name": "Sandbox",
      "name": "Sandbox"
    }]
  },
  "migrations": [{
    "tag": "v1",
    "new_sqlite_classes": ["Sandbox"]
  }]
}
```

**Why this matters:**
- `nodejs_compat` enables Node.js APIs required by SDK
- `containers` defines the Ubuntu container image
- `durable_objects` binding enables persistent routing
- `migrations` registers the Sandbox class

### 2. Create Your First Sandbox Worker

```typescript
import { getSandbox, type Sandbox } from '@cloudflare/sandbox';
export { Sandbox } from '@cloudflare/sandbox';

type Env = {
  Sandbox: DurableObjectNamespace<Sandbox>;
};

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Get sandbox instance (creates if doesn't exist)
    const sandbox = getSandbox(env.Sandbox, 'my-first-sandbox');

    // Execute Python code
    const result = await sandbox.exec('python3 -c "print(2 + 2)"');

    return Response.json({
      output: result.stdout,
      success: result.success,
      exitCode: result.exitCode
    });
  }
};
```

**CRITICAL:**
- **MUST export** `{ Sandbox }` from `@cloudflare/sandbox` in your Worker
- Sandbox ID determines routing (same ID = same container)
- First request creates container (~2-3 min cold start)
- Subsequent requests are fast (<1s)

### 3. Deploy and Test

```bash
npm run deploy
curl https://your-worker.workers.dev
```

Expected output:
```json
{
  "output": "4\n",
  "success": true,
  "exitCode": 0
}
```

---

## Architecture (Understanding the 3-Layer Model)

### How Sandboxes Work

```
┌─────────────────────────────────────────┐
│  Your Worker (Layer 1)                  │
│  - Handles HTTP requests                │
│  - Calls getSandbox()                   │
│  - Uses sandbox.exec(), writeFile(), etc│
└──────────────┬──────────────────────────┘
               │ RPC via Durable Object
┌──────────────▼──────────────────────────┐
│  Durable Object (Layer 2)               │
│  - Routes by sandbox ID                 │
│  - Maintains persistent identity        │
│  - Geographic stickiness                │
└──────────────┬──────────────────────────┘
               │ Container API
┌──────────────▼──────────────────────────┐
│  Ubuntu Container (Layer 3)             │
│  - Full Linux environment               │
│  - Python 3.11, Node 20, Git, etc.      │
│  - Filesystem: /workspace, /tmp, /home  │
│  - Process isolation (VM-based)         │
└─────────────────────────────────────────┘
```

**Key Insight**: Workers handle API logic (fast), Durable Objects route requests (persistent identity), Containers execute code (full capabilities).

---

## Critical Container Lifecycle (Most Important Section!)

### Container States

```
┌─────────┐  First request  ┌────────┐  ~10 min idle  ┌──────┐
│ Not     │ ───────────────>│ Active │ ─────────────> │ Idle │
│ Created │                 │        │                │      │
└─────────┘                 └───┬────┘                └──┬───┘
                                │ ^                      │
                                │ │ New request          │
                                │ └──────────────────────┘
                                │                         │
                                ▼                         ▼
                            Files persist          ALL FILES DELETED
                            Processes run          ALL PROCESSES KILLED
                            State maintained       ALL STATE RESET
```

### The #1 Gotcha: Ephemeral by Default

**While Container is Active** (~10 min after last request):
- ✅ Files in `/workspace`, `/tmp`, `/home` persist
- ✅ Background processes keep running
- ✅ Shell environment variables remain
- ✅ Session working directories preserved

**When Container Goes Idle** (after inactivity):
- ❌ **ALL files deleted** (entire filesystem reset)
- ❌ **ALL processes terminated**
- ❌ **ALL shell state lost**
- ⚠️  Next request creates **fresh container from scratch**

**This is NOT like a traditional server**. Sandboxes are ephemeral by design.

### Handling Persistence

**For Important Data**: Use external storage
```typescript
// Save to R2 before container goes idle
await sandbox.writeFile('/workspace/data.txt', content);
const fileData = await sandbox.readFile('/workspace/data.txt');
await env.R2.put('backup/data.txt', fileData);

// Restore on next request
const restored = await env.R2.get('backup/data.txt');
if (restored) {
  await sandbox.writeFile('/workspace/data.txt', await restored.text());
}
```

**For Build Artifacts**: Accept ephemerality or use caching
```typescript
// Check if setup needed (handles cold starts)
const exists = await sandbox.readdir('/workspace/project').catch(() => null);
if (!exists) {
  await sandbox.gitCheckout(repoUrl, '/workspace/project');
  await sandbox.exec('npm install', { cwd: '/workspace/project' });
}
// Now safe to run build
await sandbox.exec('npm run build', { cwd: '/workspace/project' });
```

---

## Session Management (Game-Changer for Chat Agents)

### What Are Sessions?

Sessions are **bash shell contexts** within one sandbox. Think terminal tabs.

**Key Properties**:
- Each session has separate working directory
- Sessions share same filesystem
- Working directory persists across commands in same session
- Perfect for multi-step workflows

### Pattern: Chat-Based Coding Agent

```typescript
type ConversationState = {
  sandboxId: string;
  sessionId: string;
};

// First message: Create sandbox and session
const sandboxId = `user-${userId}`;
const sandbox = getSandbox(env.Sandbox, sandboxId);
const sessionId = await sandbox.createSession();

// Store in conversation state (database, KV, etc.)
await env.KV.put(`conversation:${conversationId}`, JSON.stringify({
  sandboxId,
  sessionId
}));

// Later messages: Reuse same session
const state = await env.KV.get(`conversation:${conversationId}`);
const { sandboxId, sessionId } = JSON.parse(state);
const sandbox = getSandbox(env.Sandbox, sandboxId);

// Commands run in same context
await sandbox.exec('cd /workspace/project', { session: sessionId });
await sandbox.exec('ls -la', { session: sessionId }); // Still in /workspace/project
await sandbox.exec('git status', { session: sessionId }); // Still in /workspace/project
```

### Without Sessions (Common Mistake)

```typescript
// ❌ WRONG: Each command runs in separate session
await sandbox.exec('cd /workspace/project');
await sandbox.exec('ls'); // NOT in /workspace/project (different session)
```

### Pattern: Parallel Execution

```typescript
const session1 = await sandbox.createSession();
const session2 = await sandbox.createSession();

// Run different tasks simultaneously
await Promise.all([
  sandbox.exec('python train_model.py', { session: session1 }),
  sandbox.exec('node generate_reports.js', { session: session2 })
]);
```

---

## Sandbox Naming Strategies

### Per-User Sandboxes (Persistent Workspace)

```typescript
const sandbox = getSandbox(env.Sandbox, `user-${userId}`);
```

**Pros**: User's work persists while actively using (10 min idle time)
**Cons**: Geographic lock-in (first request determines location)
**Use Cases**: Interactive notebooks, IDEs, persistent workspaces

### Per-Session Sandboxes (Fresh Each Time)

```typescript
const sandboxId = `session-${Date.now()}-${crypto.randomUUID()}`;
const sandbox = getSandbox(env.Sandbox, sandboxId);
// Always destroy after use
await sandbox.destroy();
```

**Pros**: Clean environment, no state pollution
**Cons**: No persistence between requests
**Use Cases**: One-shot code execution, CI/CD, testing

### Per-Task Sandboxes (Idempotent & Traceable)

```typescript
const sandbox = getSandbox(env.Sandbox, `build-${repoName}-${commitSha}`);
```

**Pros**: Reproducible, debuggable, cacheable
**Cons**: Need explicit cleanup strategy
**Use Cases**: Build systems, data pipelines, automated workflows

---

## Core API Reference

The Sandbox SDK provides methods for command execution, file operations, Git operations, code interpretation (Jupyter-like), background processes, and cleanup.

**📖 Load `references/api-reference.md`** when you need detailed API method signatures, parameter options, or implementation examples for:
- Executing commands with options (cwd, timeout, env vars, sessions)
- File operations (read/write/mkdir/rm/readdir)
- Git operations (gitCheckout, git commands)
- Code interpreter (createCodeContext, runCode)
- Background processes (spawn, isProcessRunning, killProcess)
- Sandbox cleanup (destroy)

---

## Critical Rules

### Always Do

✅ **Check exit codes** - `if (!result.success) { handle error }`
✅ **Use sessions for multi-step workflows** - Preserve working directory
✅ **Handle cold starts** - Check if files exist before assuming they're there
✅ **Set timeouts** - Prevent hanging on long operations
✅ **Destroy ephemeral sandboxes** - Cleanup temp/session-based sandboxes
✅ **Use external storage for persistence** - R2/KV/D1 for important data
✅ **Validate user input** - Sanitize before exec() to prevent command injection
✅ **Export Sandbox class** - `export { Sandbox } from '@cloudflare/sandbox'`

### Never Do

❌ **Assume files persist after idle** - Container resets after ~10 min
❌ **Ignore exit codes** - Always check `result.success` or `result.exitCode`
❌ **Chain commands without sessions** - `cd /dir` then `ls` won't work
❌ **Execute unsanitized user input** - Use code interpreter or validate thoroughly
❌ **Forget nodejs_compat flag** - Required in wrangler.jsonc
❌ **Skip migrations** - Durable Objects need migration entries
❌ **Use .workers.dev for preview URLs** - Need custom domain
❌ **Create unlimited sandboxes** - Destroy ephemeral ones to avoid leaks

---

## Known Issues Prevention

This skill prevents **10** documented issues:

### Issue #1: Missing nodejs_compat Flag
**Error**: `ReferenceError: fetch is not defined` or `Buffer is not defined`
**Source**: https://developers.cloudflare.com/sandbox/get-started/
**Why It Happens**: SDK requires Node.js APIs not available in standard Workers
**Prevention**: Add `"compatibility_flags": ["nodejs_compat"]` to wrangler.jsonc

### Issue #2: Missing Migrations
**Error**: `Error: Class 'Sandbox' not found`
**Source**: https://developers.cloudflare.com/durable-objects/
**Why It Happens**: Durable Objects must be registered via migrations
**Prevention**: Include migrations array in wrangler.jsonc

### Issue #3: Assuming File Persistence
**Error**: Files disappear after inactivity
**Source**: https://developers.cloudflare.com/sandbox/concepts/sandboxes/
**Why It Happens**: Containers go idle after ~10 min, all state reset
**Prevention**: Use external storage (R2/KV) or check existence on each request

### Issue #4: Session Directory Confusion
**Error**: Commands execute in wrong directory
**Source**: https://developers.cloudflare.com/sandbox/concepts/sessions/
**Why It Happens**: Each exec() uses new session unless explicitly specified
**Prevention**: Create session with `createSession()`, pass to all related commands

### Issue #5: Ignoring Exit Codes
**Error**: Assuming command succeeded when it failed
**Source**: Shell best practices
**Why It Happens**: Not checking `result.success` or `result.exitCode`
**Prevention**: Always check: `if (!result.success) throw new Error(result.stderr)`

### Issue #6: Not Handling Cold Starts
**Error**: Commands fail because dependencies aren't installed
**Source**: https://developers.cloudflare.com/sandbox/concepts/sandboxes/
**Why It Happens**: Container resets after idle period
**Prevention**: Check if setup needed before running commands

### Issue #7: Docker Not Running (Local Dev)
**Error**: `Failed to build container` during local development
**Source**: https://developers.cloudflare.com/sandbox/get-started/
**Why It Happens**: Local dev requires Docker daemon
**Prevention**: Ensure Docker Desktop is running before `npm run dev`

### Issue #8: Version Mismatch (Package vs Docker Image)
**Error**: API methods not available or behaving unexpectedly
**Source**: GitHub issues
**Why It Happens**: npm package version doesn't match Docker image version
**Prevention**: Keep `@cloudflare/sandbox` package and `cloudflare/sandbox` image in sync

### Issue #9: Not Cleaning Up Ephemeral Sandboxes
**Error**: Resource exhaustion, unexpected costs
**Source**: Resource management best practices
**Why It Happens**: Creating sandboxes without destroying them
**Prevention**: `await sandbox.destroy()` in finally block for temp sandboxes

### Issue #10: Command Injection Vulnerability
**Error**: Security breach from unsanitized user input
**Source**: Security best practices
**Why It Happens**: Passing user input directly to `exec()`
**Prevention**: Use code interpreter API or validate/sanitize input thoroughly

---

## wrangler.jsonc Example

```jsonc
{
  "name": "my-sandbox-app",
  "main": "src/index.ts",
  "compatibility_date": "2025-10-29",
  "compatibility_flags": ["nodejs_compat"], // ← REQUIRED

  "containers": [{
    "class_name": "Sandbox",
    "image": "cloudflare/sandbox:0.6.3-python", // ← Use -python for Python support
    "instance_type": "lite"
  }],

  "durable_objects": {
    "bindings": [{"class_name": "Sandbox", "name": "Sandbox"}]
  },

  "migrations": [{
    "tag": "v1",
    "new_sqlite_classes": ["Sandbox"]
  }]
}
```

---

## Common Patterns

Four production-ready patterns for building with Cloudflare Sandboxes: one-shot code execution, persistent user workspaces, CI/CD pipelines, and AI agent integration.

**📖 Load `references/patterns.md`** when you need complete implementation examples for:
1. **One-Shot Code Execution** - API endpoints, code playgrounds, learning platforms
2. **Persistent User Workspace** - Interactive environments, notebooks, IDEs
3. **CI/CD Build Pipeline** - Build systems, testing pipelines, deployment automation
4. **AI Agent with Claude Code** - Automated refactoring, code generation, AI development

---

## Using Bundled Resources

### Scripts (scripts/)

- `setup-sandbox-binding.sh` - Interactive wrangler.jsonc configuration
- `test-sandbox.ts` - Validation script to test sandbox setup

**Example Usage:**
```bash
# Setup wrangler config
./scripts/setup-sandbox-binding.sh

# Test sandbox
bunx tsx scripts/test-sandbox.ts
```

### References (references/)

- `references/persistence-guide.md` - Deep dive on container lifecycle and persistence
- `references/session-management.md` - Advanced session patterns and best practices
- `references/common-errors.md` - Complete list of errors with solutions
- `references/naming-strategies.md` - Choosing sandbox IDs for different use cases

**When Claude should load these**:
- Load `persistence-guide.md` when debugging state issues or cold starts
- Load `session-management.md` when building multi-step workflows or chat agents
- Load `common-errors.md` when encountering specific errors
- Load `naming-strategies.md` when designing sandbox architecture

---

## Advanced Topics

**📖 Load `references/advanced.md`** for production patterns:
- Geographic distribution strategies for global apps
- Error handling wrapper functions
- Security hardening and input validation

---

## Official Resources

**Package**: `@cloudflare/sandbox@0.6.3` | **Docker**: `cloudflare/sandbox:0.6.3-python`

**Docs**: [Cloudflare Sandboxes](https://developers.cloudflare.com/sandbox/) | [API Reference](https://developers.cloudflare.com/sandbox/api-reference/) | [GitHub SDK](https://github.com/cloudflare/sandbox-sdk)

