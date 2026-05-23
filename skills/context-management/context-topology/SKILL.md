---
name: context-topology
description: "Master Claude Code's context primitives (Skill, Task, Command) and orchestration patterns. Use when designing agent workflows, understanding why some patterns work while others fail (e.g., Task→Task is forbidden but Skill→Skill is allowed), or implementing Chain of Experts architectures. Not for writing prompts or content generation."
agent: general-purpose
context: fork
---

# Context Topology & Orchestration Patterns

**Core Insight:** Optimal orchestration is not about writing better prompts—it's about **managing context topology**. Claude Code is a modular network of agents, not a single chat.

---

## The Four Primitives

Claude Code provides four primitives for delegation, each with a distinct **Memory Mode**:

| Primitive | Memory Mode | Description |
| :--- | :--- | :--- |
| **Skill** | **Shared** | Content injects into current conversation. Preserves context, sees full history. Use for heuristics, code standards, "How-To" guides. |
| **Skill + `context: fork`** | **Isolated** | Runs in a clean context (forked from parent). Only sees CLAUDE.md and skill content. Use for unbiased specialists (Linter, Security Auditor). |
| **Task** | **Forked** | Creates a new agent instance with full isolation. System prompt = subagent body. Keeps "noise" (bash logs, diffs) out of main context. |
| **Command** | **Injected** | Entry point using `@file` or `` !cmd `` syntax for deterministic runtime state. |

### Syntax Summary

```markdown
# Skill (shared context)
Skill(skill-name)

# Skill (isolated context)
<!-- In SKILL.md frontmatter: -->
---
context: fork
agent: general-purpose
skills:
  - helper-skill
---

# Task (forked agent)
Task(subagent-name)
Task(subagent-name, run_in_background=True)

# Command (injected)
!`git status`
@path/to/file.md
```

---

## The Recursion Loophole

### Critical Constraint

| Pattern | Status | Why |
| :--- | :--- | :--- |
| `Task` → `Task` | **FORBIDDEN** | Recursion blocker prevents infinite agent spawning |
| `Skill(fork)` → `Skill(fork)` | **ALLOWED** | Skill loophole bypasses recursion limit |

### Why This Matters

When you need more than 3 levels of depth:

```
❌ WRONG: Task → Task (crashes at level 2)
✅ RIGHT: Task → Skill(fork) → Skill(fork) → Skill(fork)
```

The **Chain of Experts** pattern exploits this loophole:

```
Level 1 (Main):     Conductor. Holds TaskList state.
Level 2 (Forked):   Architect. Researches, creates JSON plan.
Level 3 (Forked):   Implementer. Executes edits, runs tests.
Level 4 (Forked):   Verifier. Validates output, returns pass/fail.
```

---

## Chain of Experts Pattern

A multi-phase workflow that keeps each phase isolated from context pollution.

### Architecture

```
┌─────────────────────────────────────────────────────┐
│ Main Agent (Conductor)                              │
│ - Holds TaskList state                             │
│ - Spawns Level 2 with Task()                        │
│ - Receives summary, not full logs                   │
└─────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│ Level 2: Architect (Skill + context: fork)          │
│ - agent: Plan (read-only, cannot edit)              │
│ - Reads codebase, creates execution plan            │
│ - Returns: JSON or markdown plan                    │
└─────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│ Level 3: Implementer (Task or Skill + context: fork)│
│ - agent: general-purpose                            │
│ - Executes plan, performs edits                     │
│ - Runs tests, fixes failures internally             │
│ - Returns: 5-line summary                           │
└─────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│ Level 4: Verifier (Skill + context: fork)           │
│ - agent: Explore or general-purpose                 │
│ - Validates work without implementation bias        │
│ - Returns: Pass/Fail with evidence                  │
└─────────────────────────────────────────────────────┘
```

### When to Use Each Level

| Level | Use When | Agent Type |
| :--- | :--- | :--- |
| 2 (Architect) | Need research, planning, or design decisions | `agent: Plan` |
| 3 (Implementer) | Heavy editing, test running, complex execution | `agent: general-purpose` |
| 4 (Verifier) | Need unbiased validation, security scan, lint | `agent: Explore` or `agent: general-purpose` |

---

## Advanced Patterns

### 1. Background Auditor Pattern

Run parallel workflows while main agent continues work:

```python
# Main agent continues UI changes
Task("security-audit", run_in_background=True)

# When Task finishes, it "interrupts" with summary
```

**Use when:**
- Long-running CI/CD scripts
- Security scans on entire repo
- Parallel feature work and verification

### 2. Skill Sandwich Pattern

Verification loop where the worker checks its own work:

```
Main → Skill(define_criteria) → Task(implement) → Skill(fork:linter) → Main
```

**Why it works:** Level 3 (Linter) has zero knowledge of implementation struggle—no bias from seeing "I've been trying for 20 messages."

### 3. Dispatcher Skill Pattern

A skill that analyzes requests and routes to appropriate handlers:

```yaml
---
name: dispatcher
description: "Analyzes requests and routes to appropriate handler. Use when unsure which primitive to use or when work needs distribution."
context: fork
agent: general-purpose
---
```

**Logic:**
1. Analyze request complexity
2. Select primitive (Task vs Skill vs Skill(fork))
3. Spawn appropriate handler
4. Return result to parent

### 4. Context Compaction Defense

Since Claude Code auto-compacts at 95% capacity, move procedural knowledge to modular rules:

```markdown
# Instead of in a skill:
"Use this pattern for testing..."

# Put in .claude/rules/testing.md:
- Test patterns, assertions, coverage targets
```

**Result:** Modular rules load into EVERY subagent and forked skill by default.

---

## Decision Matrix

### Which Primitive for the Goal?

| Goal | Primitive | Why |
| :--- | :--- | :--- |
| Exploration | `Skill(context: fork)` + `agent: Explore` | Fastest, cheapest, cannot break code |
| High-volume edits | `Task(subagent)` | Keeps main context clean |
| Strict compliance | `Skill(context: fork)` | No context contamination |
| User shortcuts | `Command` | `@` and `!` for determinism |
| Safety enforcement | `Hooks` | Survives across subagents |

### Which Agent Type for Forked Skills?

| Agent Type | Capabilities | Restrictions | Use When |
| :--- | :--- | :--- | :--- |
| **Explore** | Read-only tools | No Write, Edit, Task | Research, code analysis |
| **Plan** | Read-only tools | No Write, Edit | Creating execution plans |
| **general-purpose** | All tools | None | Heavy lifting, editing |
| **Bash** | Terminal commands | Shell operations only | Git ops, builds, scripts |

### When to Fork Context?

| Scenario | Context Mode | Example |
| :--- | :--- | :--- |
| Need unbiased specialist | `context: fork` | Linter, Security Auditor |
| Heavy lifting (many edits) | `Task()` | Refactoring 20 files |
| Reusable worker | `Skill(fork)` | "Extract data from file" |
| Keep main context clean | `Task()` | Long test runs with logs |

---

## Common Anti-Patterns

### Anti-Pattern 1: Task→Task (True Subagent Nesting)
```markdown
❌ WRONG:
Task(subagent-a)  # Level 1 (true subagent spawn)
→ Task(subagent-b)  # BLOCKED: subagents cannot spawn subagents
```

**⚠ IMPORTANT DISTINCTION:**
- **Task()** spawns true subagents (recursion blocked)
- **Skill(context: fork)** runs inline with context isolation (ALLOWED to chain)

### Anti-Pattern 2: Missing context: fork
```markdown
❌ WRONG:
---
# Missing context: fork - sees parent history
name: linter
---
Use the Bash tool to run linting...
```
**Problem:** Linter sees previous implementation attempts—biased validation.

### Pattern: Chain of Experts (Valid)
```markdown
✅ CORRECT:
Skill(skill-a)                    # Phase 1: Setup (shared context)
→ Skill(skill-b, context: fork)   # Phase 2: Analysis (isolated)
→ Skill(skill-c, context: fork)   # Phase 3: Validation (isolated)
```
**Benefit:** First skill establishes shared context, subsequent forked phases run with isolation while maintaining bidirectional information flow. Skill(context: fork) runs inline (not true subagent), allowing chaining.

**⚠ Best Practice:** First skill should be non-forked (shared context) to anchor the chain. All-forked chains may lose the return path to the original context.

**⚠ Note:** Use judiciously—each fork has overhead. Reserve for multi-phase workflows requiring clean separation.

### Anti-Pattern 4: All-Inline Skill Chain
```markdown
❌ WRONG:
Skill(skill-a)  # All shared context
→ Skill(skill-b)
→ Skill(skill-c)
```
**Problem:** Zero forked skills means context injection only—no reliable return path to original skill. Primitives inject new context but don't maintain chain coherence. Execution may not return to skill-a as expected.

**Fix:** First skill shared context, subsequent skills forked:
```markdown
✅ CORRECT:
Skill(skill-a)                    # Anchor with shared context
→ Skill(skill-b, context: fork)   # Forked isolation
→ Skill(skill-c, context: fork)   # Forked isolation
```

### Anti-Pattern 5: Fork for trivial tasks
```markdown
❌ WRONG:
---
context: fork
---
What is 2 + 2?
```
**Problem:** Fork has overhead. Inline execution is cheaper.

---

## Frontmatter Reference

### Skill Frontmatter

```yaml
---
name: skill-name              # Max 64 chars, lowercase, hyphens
description: "When to use. Not for exclusions."
context: fork                 # Omit for shared context
agent: general-purpose        # Only if context: fork
skills:                       # Preload skills for forked context
  - helper-skill
allowed-tools:                # Reactive constraint (optional)
  - Read
  - Write
---
```

### Command Frontmatter

```yaml
---
description: "When to use this command."
---
```

---

## Memory Hierarchy

What loads into which context:

| Context | Loads |
| :--- | :--- |
| **Main** | CLAUDE.md, CLAUDE.local.md, .claude/rules/*, loaded skills |
| **Task (subagent)** | CLAUDE.md, .claude/rules/*, subagent body |
| **Skill(fork)** | CLAUDE.md, .claude/rules/*, skill content |
| **Command** | @file content, !cmd output |

**Key insight:** Task and Skill(fork) do NOT see the parent conversation. This is the isolation mechanism.

---

## Summary

1. **Choose primitive by memory mode:** Shared (Skill), Isolated (Skill+fork), Forked (Task), Injected (Command)
2. **Exploit the recursion loophole:** Task→Task forbidden, Skill→Skill allowed
3. **Chain Experts for clean contexts:** Architect → Implementer → Verifier
4. **Use Task for heavy lifting:** Keeps main context free of noise
5. **Use Skill(fork) for unbiased specialists:** Linters, validators, auditors
6. **Use Commands for deterministic entry points:** @file, !cmd injection
