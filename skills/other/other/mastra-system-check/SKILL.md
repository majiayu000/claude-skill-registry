---
name: mastra-system-check
description: >
  Comprehensive system check for Mastra AI agent projects. Validates configuration,
  agents, workflows, memory, tools, prompts, and security across 66 rules organized
  by priority. Use when setting up new projects, debugging issues, reviewing code,
  or preparing for production deployment.
license: MIT
metadata:
  author: stan
  x: "https://x.com/goldkey"
  version: "1.1.0"
---

# Mastra System Check

Validates Mastra AI agent projects with **66 checks** across **10 categories**.
Finds configuration errors, missing best practices, and potential issues before they cause problems.

---

## Trigger Keywords

Activate this skill when the user mentions:

| Category | Example Phrases |
|----------|-----------------|
| **General Check** | "check my mastra project", "mastra system check", "validate mastra", "review my mastra code" |
| **Setup Issues** | "mastra not working", "agent won't start", "can't find mastra instance" |
| **Memory Issues** | "memory not persisting", "conversation lost", "agent forgets context" |
| **Workflow Issues** | "workflow stuck", "workflow not executing", "steps not running" |
| **Context Issues** | "context not propagating", "requestcontext empty", "can't access user data" |
| **Deployment** | "prepare for production", "production checklist", "deploy mastra" |
| **Debugging** | "debug mastra", "troubleshoot agent", "why is my agent..." |

---

## Quick Checks (Run First)

Before deep analysis, verify these **4 common issues** that cause most failures:

### 1. Storage Configured?
```bash
grep "storage:" src/mastra/index.ts
```
If missing → Add `storage: new LibSQLStore({ url: "file:./mastra.db" })`

### 2. API Keys Set?
```bash
cat .env | grep -E "(OPENAI|ANTHROPIC|GOOGLE)_API_KEY"
```
If missing → Add the required API key for the model provider being used

### 3. Model Format Correct?
```bash
grep -r "model:" src/mastra/ | grep -v "provider/"
```
All models must use `provider/model-name` format (e.g., `openai/gpt-4o`)

### 4. Workflows Committed?
```bash
grep -r "new Workflow" src/mastra/ -A 20 | grep "\.commit()"
```
Every workflow chain must end with `.commit()`

**If any quick check fails, fix it before proceeding with full analysis.**

---

## Execution Steps

When this skill activates, follow these steps **IN ORDER**:

### Step 1: Locate Entry Point
```bash
# Find the main Mastra instance
cat src/mastra/index.ts
```
Verify: Named export `mastra` exists with proper configuration.

### Step 2: Check Dependencies
```bash
# Verify required packages
cat package.json | grep -E "@mastra|zod|@ai-sdk"
```
Required: `@mastra/core`. Check Zod is v4+ for schema compatibility.

### Step 3: Scan for Agents
```bash
grep -rn "new Agent" src/
```
For each agent found, check: id, model format, instructions, tools, memory.

### Step 4: Scan for Workflows
```bash
grep -rn "new Workflow" src/
```
For each workflow, check: .commit() called, steps connected, schemas defined.

### Step 5: Check Configuration Files
- `.env` / `.env.local` → API keys present
- `tsconfig.json` → Module ES2022+, moduleResolution bundler/node16

### Step 6: Run Category Checks
Apply rules from `AGENTS.md` in this priority order:
1. 🔴 CRITICAL (config-*) - Fix immediately
2. 🟠 HIGH (agent-*, workflow-*, context-*, prompt-*) - Fix before deployment
3. 🟡 MEDIUM (memory-*, tool-*, security-*) - Fix when possible
4. 🟢 LOW (optimization-*) - Nice to have

### Step 7: Report Findings
Present issues sorted by priority with specific file locations and fixes.

---

## File Patterns to Check

| Pattern | Purpose | Priority |
|---------|---------|----------|
| `src/mastra/index.ts` | Main Mastra instance, storage, agents | CRITICAL |
| `src/mastra/agents/*.ts` | Agent definitions | HIGH |
| `src/mastra/workflows/*.ts` | Workflow definitions | HIGH |
| `src/mastra/tools/*.ts` | Tool definitions | MEDIUM |
| `package.json` | Dependencies, versions | CRITICAL |
| `tsconfig.json` | TypeScript module config | CRITICAL |
| `.env` / `.env.local` | API keys, secrets | CRITICAL |
| `src/**/middleware*.ts` | RequestContext setup | HIGH |

---

## Priority Legend

| Badge | Level | Meaning | Action |
|-------|-------|---------|--------|
| 🔴 | CRITICAL | System won't function | Fix immediately |
| 🟠 | HIGH | Major functionality issues | Fix before deployment |
| 🟡 | MEDIUM | Quality/maintainability | Fix when possible |
| 🟢 | LOW | Performance/cost optimization | Nice to have |

---

## Check Categories Summary

| Category | Rules | Priority | Key Checks |
|----------|-------|----------|------------|
| Configuration | 6 | 🔴 CRITICAL | Storage, env vars, TypeScript, entry point |
| Agents | 6 | 🟠 HIGH | Model format, instructions, tools, memory |
| Workflows | 6 | 🟠 HIGH | .commit(), schemas, connections, suspend |
| Context | 8 | 🟠 HIGH | RequestContext typing, propagation, access |
| Prompts | 10 | 🟠 HIGH | Token efficiency, structure, examples |
| Memory | 6 | 🟡 MEDIUM | Storage, threads, vector stores |
| Tools | 6 | 🟡 MEDIUM | Schemas, descriptions, error handling |
| Observability | 6 | 🟡 MEDIUM* | Tracing, scorers, exporters |
| Security | 6 | 🟡 MEDIUM | Auth, CORS, PII, secrets |
| Optimization | 6 | 🟢 LOW | Model selection, caching, timeouts |

**Total: 66 rules across 10 categories**

*\*Observability checks are **conditional** - only apply if telemetry/evals are configured.*

---

## Output Format

For each issue found, report in this format:

```
### 🔴 CRITICAL Issues (count)

**[rule-id] Rule Name**
- **Location:** `file/path.ts:lineNumber`
- **Issue:** Clear description of what's wrong
- **Fix:**
  ```typescript
  // Corrected code example
  ```
- **Docs:** https://mastra.ai/docs/relevant-section
```

---

## Example Output

```markdown
## Mastra System Check Results

**Project:** my-mastra-app
**Scanned:** 12 files
**Duration:** 2.3s

---

### 🔴 CRITICAL Issues (2)

**[config-storage-provider] Missing Storage Provider**
- **Location:** `src/mastra/index.ts:8`
- **Issue:** No storage configured - memory, workflows, and traces won't persist
- **Fix:**
  ```typescript
  import { LibSQLStore } from "@mastra/libsql";

  export const mastra = new Mastra({
    storage: new LibSQLStore({
      url: process.env.DATABASE_URL || "file:./mastra.db",
    }),
    agents: { myAgent },
  });
  ```
- **Docs:** https://mastra.ai/docs/storage

**[config-env-variables] Missing API Key**
- **Location:** `.env`
- **Issue:** OPENAI_API_KEY not set but `openai/gpt-4o` model is used
- **Fix:** Add to `.env`:
  ```bash
  OPENAI_API_KEY=sk-your-key-here
  ```

---

### 🟠 HIGH Issues (1)

**[prompt-right-altitude] Under-specified Agent Instructions**
- **Location:** `src/mastra/agents/assistant.ts:12`
- **Issue:** Agent has minimal instructions: "You are a helpful assistant"
- **Fix:**
  ```typescript
  instructions: `
    <role>
    You are a customer support agent for Acme Corp.
    </role>

    <capabilities>
    - Answer product questions using search_products tool
    - Check order status using order_lookup tool
    </capabilities>

    <guidelines>
    - Be concise and helpful
    - Escalate billing issues to human support
    </guidelines>
  `,
  ```

---

### 🟡 MEDIUM Issues (0)

No medium-priority issues found.

---

### 🟢 LOW Issues (1)

**[optimization-model-selection] Expensive Model for Simple Task**
- **Location:** `src/mastra/agents/classifier.ts:6`
- **Issue:** Using `gpt-4o` for classification - `gpt-4o-mini` would be more cost-effective
- **Fix:** Change model to `openai/gpt-4o-mini` for simple classification tasks

---

### ✅ Summary

| Priority | Issues |
|----------|--------|
| 🔴 CRITICAL | 2 |
| 🟠 HIGH | 1 |
| 🟡 MEDIUM | 0 |
| 🟢 LOW | 1 |

**Passed: 62/66 checks**

**Next Steps:**
1. Fix CRITICAL issues immediately - system won't work without them
2. Address HIGH issues before deployment
3. Consider LOW optimizations to reduce costs
```

---

## Conditional Checks

Some rules only apply in specific situations:

### Observability Section (Conditional)
**Only check if** `telemetry` or `observability` is configured, or if evals/scorers are used.

```typescript
// If you see this in the codebase, run observability checks:
telemetry: { enabled: true, ... }
// or
evals: { scorers: [...] }
```

**If NOT configured:** Skip observability section entirely - it's optional.

### Memory Checks (Conditional)
**Only check if** agents have `memory` configured.

### Workflow Storage (Conditional)
**Only check if** workflows use `suspend()` for human-in-the-loop.

---

## Scope Limitations

This skill does **NOT**:
- ❌ Deploy projects or run the dev server
- ❌ Make changes without user approval
- ❌ Check runtime behavior (static analysis only)
- ❌ Validate external API integrations
- ❌ Test actual LLM responses
- ❌ Run the project's test suite

This skill **DOES**:
- ✅ Static code analysis
- ✅ Configuration validation
- ✅ Best practice review
- ✅ Security pattern detection
- ✅ Provide specific code fixes

---

## Documentation Links

Include these when suggesting fixes:

| Topic | URL |
|-------|-----|
| Mastra Docs | https://mastra.ai/docs |
| Storage Setup | https://mastra.ai/docs/storage |
| Memory Guide | https://mastra.ai/docs/memory |
| Workflows | https://mastra.ai/docs/workflows |
| Agents | https://mastra.ai/docs/agents |
| Tools | https://mastra.ai/docs/tools |
| AI SDK | https://sdk.vercel.ai/docs |

---

## Full Rules Reference

For complete details on all 66 rules with code examples and fixes, read **`AGENTS.md`** in this skill directory.

---

## Common Fix Patterns

### Missing Storage (Most Common)
```typescript
import { LibSQLStore } from "@mastra/libsql";

export const mastra = new Mastra({
  storage: new LibSQLStore({
    url: process.env.DATABASE_URL || "file:./mastra.db",
  }),
  agents: { /* ... */ },
});
```

### Wrong Model Format
```typescript
// ❌ Wrong
model: "gpt-4o"

// ✅ Correct
model: "openai/gpt-4o"
```

### Missing Workflow Commit
```typescript
// ❌ Wrong
const workflow = new Workflow({ id: "my-flow" })
  .step("step1", { execute: async () => ({ done: true }) });

// ✅ Correct
const workflow = new Workflow({ id: "my-flow" })
  .step("step1", { execute: async () => ({ done: true }) })
  .commit();  // Required!
```

### Memory Without Thread/Resource
```typescript
// ❌ Wrong
await agent.generate("Hello");

// ✅ Correct
await agent.generate("Hello", {
  memory: {
    thread: `session-${sessionId}`,
    resource: `user-${userId}`,
  },
});
```

---

## Version History

- **1.1.0** - Enhanced triggering, quick checks, execution steps, example output
- **1.0.0** - Initial release with 66 rules across 10 categories
