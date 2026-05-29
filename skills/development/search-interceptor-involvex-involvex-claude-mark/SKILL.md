---
name: search-interceptor
description: "⛔ INTERCEPT TRIGGER: Automatically invoked BEFORE Read 3+ files OR Glob with broad patterns. Validates whether bulk file operations should be replaced with semantic search. Prevents token waste from sequential file reads."
allowed-tools: Bash, AskUserQuestion
---

# Search Interceptor

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ⛔ INTERCEPT TRIGGERS:                                                     ║
║                                                                              ║
║   • About to Read 3+ files in same directory                                ║
║   • About to Glob with **/*.ts, **/*.py, or similar broad pattern           ║
║   • Planning sequential file reads to "understand" something                 ║
║   • Rationalizing "let me read while agents work"                           ║
║                                                                              ║
║   WHEN TRIGGERED: Validate if claudemem search is better                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## Purpose

This skill intercepts bulk file operations before they execute, validating whether semantic search would be more efficient.

## When This Skill Triggers

### Trigger 1: Multiple File Reads Planned

```
YOU ARE ABOUT TO:
  Read file1.ts
  Read file2.ts
  Read file3.ts
  Read file4.ts
  ...

STOP. Ask: Can this be ONE claudemem query?
```

### Trigger 2: Broad Glob Pattern

```
YOU ARE ABOUT TO:
  Glob("src/services/**/*.ts")
  Then read all N matches

STOP. Ask: What am I looking for SEMANTICALLY?
```

### Trigger 3: Parallelization Rationalization

```
YOU ARE THINKING:
  "Let me read these files while the agent works..."

STOP. This is tool familiarity bias.
```

### Trigger 4: File Paths in Prompt

```
PROMPT MENTIONS:
  src/services/prime/internal_api/client.ts
  src/services/prime/api.ts
  ...

YOUR INSTINCT: Read them directly
STOP. Search semantically first for context.
```

---

## Interception Protocol

### Step 1: Pause Before Execution

When you're about to execute bulk file operations, STOP and run:

```bash
claudemem status
```

### Step 2: Evaluate

**If claudemem is indexed:**

| Your Plan | Better Alternative |
|-----------|-------------------|
| Read 5 auth files | `claudemem search "authentication login session"` |
| Glob all services | `claudemem search "service layer business logic"` |
| Read mentioned paths | `claudemem search "[concept from those paths]"` |

**If claudemem is NOT indexed:**

```bash
claudemem index -y
```
Then proceed with semantic search.

### Step 3: Execute Better Alternative

```bash
# Instead of reading N files, run ONE semantic query
claudemem search "concept describing what you need" -n 15

# ONLY THEN read specific lines from results
```

---

## Interception Decision Matrix

| Situation | Intercept? | Action |
|-----------|-----------|--------|
| Read 1-2 specific files | No | Proceed with Read |
| Read 3+ files in investigation | **YES** | Convert to claudemem search |
| Glob for exact filename | No | Proceed with Glob |
| Glob for pattern discovery | **YES** | Convert to claudemem search |
| Grep for exact string | No | Proceed with Grep |
| Grep for semantic concept | **YES** | Convert to claudemem search |
| Files mentioned in prompt | **YES** | Search semantically first |

---

## Examples of Interception

### Example 1: Auth Investigation

**❌ Original plan:**
```
I see the task mentions auth, let me read:
- src/services/auth/login.ts
- src/services/auth/session.ts
- src/services/auth/jwt.ts
- src/services/auth/middleware.ts
- src/services/auth/utils.ts
```

**✅ After interception:**
```bash
claudemem status  # Check if indexed
claudemem search "authentication login session JWT token validation" -n 15
# Now I have ranked, relevant chunks instead of 5 full files
```

### Example 2: API Integration Audit

**❌ Original plan:**
```
Audit mentions Prime API files:
- src/services/prime/internal_api/client.ts
- src/services/prime/api.ts
Let me just Read these directly...
```

**✅ After interception:**
```bash
claudemem search "Prime API integration endpoints HTTP client" -n 20
# This finds ALL Prime-related code, ranked by relevance
# Not just the 2 files mentioned
```

### Example 3: Pattern Discovery

**❌ Original plan:**
```
Glob("src/**/*.controller.ts")
Then read all 15 controllers to understand routing
```

**✅ After interception:**
```bash
claudemem search "HTTP controller endpoint route handler" -n 20
# Gets the most relevant routing code, not all controllers
```

---

## The Psychology of Tool Familiarity Bias

### Why You Default to Read/Glob

1. **Predictability**: Read always works, output is deterministic
2. **No skill overhead**: Don't need to invoke a skill first
3. **Instant gratification**: See file contents immediately
4. **Habit**: These are your "native" tools

### Why This Is Wrong for Investigation

1. **No ranking**: File #5 might be more relevant than File #1
2. **No context**: You see code but not relationships
3. **Token waste**: Reading 5 files costs ~5000 tokens; claudemem search costs ~500
4. **Missing code**: You only see what you explicitly request

### Breaking the Habit

```
BEFORE: "I need to understand X, let me Read files..."
AFTER:  "I need to understand X, let me claudemem search for X concepts..."
```

---

## Integration with Other Skills

This skill works with:

| Skill | Relationship |
|-------|-------------|
| `code-search-selector` | Selector determines WHAT tool; Interceptor validates BEFORE execution |
| `claudemem-search` | Interceptor redirects to claudemem; this skill shows HOW to search |
| `deep-analysis` | Interceptor prevents bad patterns; deep-analysis uses good patterns |
| Detective skills | Interceptor prevents duplicate work by trusting detective agents |

---

## Quick Reference

```
┌─────────────────────────────────────────────────────────────────┐
│                    INTERCEPTION QUICK CHECK                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  BEFORE bulk Read/Glob, ask:                                    │
│                                                                  │
│  1. Is claudemem indexed?     → claudemem status                │
│  2. Can this be ONE query?    → Usually YES                     │
│  3. Am I rationalizing?       → "While agents work" = BAD       │
│  4. Files in prompt?          → Search first, not Read          │
│                                                                  │
│  DEFAULT: Use claudemem search. EXCEPTION: Exact string match.  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

**Maintained by:** MadAppGang
**Plugin:** code-analysis v2.2.0
**Purpose:** Intercept and redirect bulk file operations to semantic search
