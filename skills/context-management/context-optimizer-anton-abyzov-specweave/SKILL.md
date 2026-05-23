---
name: context-optimizer
description: Second-pass context optimization that analyzes user prompts and removes irrelevant specs, agents, and skills from loaded context. Achieves 80%+ token reduction through smart cleanup. Activates for optimize context, reduce tokens, clean context, smart context, precision loading.
allowed-tools: Read, Grep, Glob
---

# Context Optimizer

Second-pass context optimization that analyzes user intent and surgically removes irrelevant content from loaded context, achieving 80%+ total token reduction.

## Purpose

After `context-loader` loads context based on manifest (70% reduction), `context-optimizer` performs intelligent analysis of the user's specific prompt to remove sections that aren't needed for that particular task.

## The Two-Pass Strategy

### Pass 1: Context Loader (Manifest-Based)
```yaml
# context-manifest.yaml
spec_sections:
  - auth-spec.md
  - payment-spec.md
  - user-management-spec.md

Result: Load only relevant specs (70% reduction)
Before: 150k tokens → After: 45k tokens
```

### Pass 2: Context Optimizer (Intent-Based)
```typescript
User: "Fix authentication bug in login endpoint"

Analyzer detects:
  • Task type: Bug fix (not new feature)
  • Domain: Backend auth
  • Scope: Single endpoint

Removes:
  ❌ payment-spec.md (different domain)
  ❌ user-management-spec.md (different domain)
  ❌ PM agent description (not needed for bug fix)
  ❌ Frontend skills (backend task)
  ❌ DevOps skills (not deploying)

Keeps:
  ✅ auth-spec.md (directly relevant)
  ✅ architecture/security/ (auth considerations)
  ✅ nodejs-backend skill (implementation)
  ✅ Tech Lead agent (code review)

Result: Additional 40% reduction
After Pass 1: 45k tokens → After Pass 2: 27k tokens
Total reduction: 82% (150k → 27k)
```

## When to Use

**Activates automatically** after context-loader when:
- User prompt is specific (mentions feature, bug, file)
- Loaded context > 20k tokens
- Task is focused (not "build full product")

**Manual activation:**
- "optimize context"
- "reduce tokens"
- "clean context"

**Skip when:**
- Context already small (<10k tokens)
- User asks broad questions ("explain architecture")
- Planning new features (need full context)

## What It Does

### 1. User Intent Analysis

```typescript
interface IntentAnalysis {
  task_type: TaskType;
  domains: Domain[];
  scope: Scope;
  needs_full_context: boolean;
  confidence: number;
}

enum TaskType {
  BUG_FIX = "bug-fix",           // Narrow scope
  FEATURE = "feature",            // Medium scope
  REFACTOR = "refactor",          // Medium scope
  ARCHITECTURE = "architecture",  // Broad scope
  DOCUMENTATION = "documentation", // Medium scope
  TESTING = "testing"             // Medium scope
}

enum Domain {
  FRONTEND = "frontend",
  BACKEND = "backend",
  DATABASE = "database",
  INFRASTRUCTURE = "infrastructure",
  SECURITY = "security",
  AUTH = "auth",
  PAYMENT = "payment",
  // ... project-specific domains
}

enum Scope {
  NARROW = "narrow",      // Single file/function
  FOCUSED = "focused",    // Single module
  BROAD = "broad"         // Multiple modules
}
```

**Analysis Examples:**

| User Prompt | Task Type | Domains | Scope | Needs Full? |
|-------------|-----------|---------|-------|-------------|
| "Fix login bug" | BUG_FIX | [AUTH, BACKEND] | NARROW | No |
| "Add payment feature" | FEATURE | [PAYMENT, BACKEND] | FOCUSED | No |
| "Refactor auth module" | REFACTOR | [AUTH, BACKEND] | FOCUSED | No |
| "Design system architecture" | ARCHITECTURE | [ALL] | BROAD | Yes |
| "Explain how payments work" | DOCUMENTATION | [PAYMENT] | FOCUSED | No |

### 2. Context Filtering Rules

```yaml
rules:
  # Rule 1: Task-Specific Specs
  bug_fix:
    keep_specs:
      - Related to mentioned domain
      - Architecture docs for that domain
    remove_specs:
      - Unrelated domains
      - Strategic docs (PRD, business specs)
      - Future roadmap

  feature_development:
    keep_specs:
      - Related domain specs
      - Architecture for integration points
      - Related ADRs
    remove_specs:
      - Unrelated domains
      - Completed features (unless mentioned)

  architecture_review:
    keep_specs:
      - ALL (needs full context)

  # Rule 2: Agent/Skill Filtering
  backend_task:
    keep_skills:
      - Backend skills (nodejs, python, dotnet)
      - Tech Lead
      - QA Lead
    remove_skills:
      - Frontend skills
      - DevOps (unless "deploy" mentioned)
      - PM agent (unless "requirements" mentioned)

  frontend_task:
    keep_skills:
      - Frontend skills (React, Next.js)
      - UI/UX skills
    remove_skills:
      - Backend skills
      - Database skills

  # Rule 3: Documentation Filtering
  implementation_task:
    keep_docs:
      - Technical specs (HLD, LLD)
      - ADRs
      - Implementation guides
    remove_docs:
      - Strategic docs (PRD, business cases)
      - Operations runbooks
      - Deployment guides

  planning_task:
    keep_docs:
      - Strategic docs (PRD)
      - Architecture overview
      - ADRs
    remove_docs:
      - Implementation details
      - Code comments
      - Test cases
```

### 3. Optimization Algorithm

```typescript
async function optimizeContext(
  userPrompt: string,
  loadedContext: Context
): Promise<OptimizedContext> {

  // Step 1: Analyze intent
  const intent = await analyzeIntent(userPrompt);

  // Step 2: If broad scope, keep all
  if (intent.needs_full_context) {
    return {
      context: loadedContext,
      removed: [],
      kept: Object.keys(loadedContext),
      reason: "Broad scope requires full context"
    };
  }

  // Step 3: Apply filtering rules
  const filtered = {
    specs: filterByDomain(loadedContext.specs, intent.domains),
    agents: filterByTaskType(loadedContext.agents, intent.task_type),
    skills: filterByDomain(loadedContext.skills, intent.domains),
    docs: filterByScope(loadedContext.docs, intent.scope)
  };

  // Step 4: Calculate savings
  const before = calculateTokens(loadedContext);
  const after = calculateTokens(filtered);
  const savings = ((before - after) / before * 100).toFixed(0);

  // Step 5: Return optimized context
  return {
    context: filtered,
    removed: diff(loadedContext, filtered),
    kept: Object.keys(filtered),
    savings: `${savings}%`,
    tokens_before: before,
    tokens_after: after
  };
}
```

## Usage Examples

### Example 1: Bug Fix (Narrow Scope)

```bash
# Pass 1: context-loader loads from manifest
Loaded context: 45k tokens (auth, payment, user specs)

# User prompt
User: "Fix bug where login fails with expired JWT"

# Pass 2: context-optimizer analyzes
🔍 Analyzing task requirements...

Detected:
  Task Type: Bug Fix
  Domains: [AUTH, BACKEND]
  Scope: Narrow (single endpoint)
  Full Context Needed: No

Optimizing context...

Removed (18k tokens):
  ❌ payment-spec.md (9k tokens) - Unrelated domain
  ❌ user-management-spec.md (7k tokens) - Unrelated domain
  ❌ PM agent description (1k tokens) - Not needed for bug fix
  ❌ Frontend skills (1k tokens) - Backend task

Kept (27k tokens):
  ✅ auth-spec.md (12k tokens) - Core domain
  ✅ architecture/security/jwt-handling.md (5k tokens) - Relevant
  ✅ nodejs-backend skill (8k tokens) - Implementation
  ✅ Tech Lead agent (2k tokens) - Code review

Result: 45k → 27k tokens (40% additional reduction)
Total: 150k → 27k (82% total reduction)

Ready to proceed with optimized context.
```

### Example 2: Feature Development (Focused Scope)

```bash
User: "Add subscription billing to payment module"

🔍 Analyzing task requirements...

Detected:
  Task Type: Feature Development
  Domains: [PAYMENT, BACKEND]
  Scope: Focused (single module)
  Full Context Needed: No

Optimizing context...

Removed (15k tokens):
  ❌ auth-spec.md (12k tokens) - Unrelated domain
  ❌ user-management-spec.md (7k tokens) - Unrelated
  ❌ DevOps agent (2k tokens) - Not deploying yet

Kept (30k tokens):
  ✅ payment-spec.md (9k tokens) - Core domain
  ✅ architecture/payment-integration.md (6k tokens) - Integration points
  ✅ architecture/adr/0015-payment-provider.md (3k tokens) - Context
  ✅ PM agent (2k tokens) - Requirements clarification
  ✅ nodejs-backend skill (8k tokens) - Implementation
  ✅ Tech Lead agent (2k tokens) - Planning

Result: 45k → 30k tokens (33% additional reduction)
```

### Example 3: Architecture Review (Broad Scope)

```bash
User: "Review overall system architecture"

🔍 Analyzing task requirements...

Detected:
  Task Type: Architecture Review
  Domains: [ALL]
  Scope: Broad (system-wide)
  Full Context Needed: Yes

Skipping optimization - broad scope requires full context.

Loaded context: 45k tokens (all specs retained)

Rationale: Architecture review needs visibility across all domains
to identify integration issues, dependencies, and design patterns.
```

### Example 4: Manual Optimization

```bash
User: "Optimize context for payment work"

context-optimizer:

🔍 Analyzing for payment domain...

Removed (25k tokens):
  ❌ auth-spec.md
  ❌ user-management-spec.md
  ❌ Frontend skills
  ❌ Strategic docs

Kept (20k tokens):
  ✅ payment-spec.md
  ✅ Payment architecture
  ✅ Backend skills
  ✅ Integration guides

Result: 45k → 20k tokens (56% reduction)

You can now work on payment features with optimized context.
```

## Configuration



## Integration with Context Loader

### Workflow

```typescript
// 1. User asks to work on feature
User: "Fix authentication bug"

// 2. context-loader loads from manifest
context-loader.load({
  increment: "0001-authentication",
  manifest: "context-manifest.yaml"
})
// Result: 150k → 45k tokens (70% reduction)

// 3. context-optimizer analyzes user prompt
context-optimizer.analyze(userPrompt: "Fix authentication bug")
// Detects: bug-fix, auth domain, narrow scope

// 4. context-optimizer removes unneeded sections
context-optimizer.filter(loadedContext, analysis)
// Result: 45k → 27k tokens (40% additional reduction)

// 5. Return optimized context to main session
return optimizedContext
// Total: 150k → 27k (82% reduction)
```

### Configuration in Increment

```yaml
# .specweave/increments/0001-auth/context-manifest.yaml
spec_sections:
  - .specweave/docs/internal/strategy/auth/spec.md
  - .specweave/docs/internal/strategy/payment/spec.md
  - .specweave/docs/internal/strategy/users/spec.md

documentation:
  - .specweave/docs/internal/architecture/auth-design.md
  - .specweave/docs/internal/architecture/payment-integration.md

max_context_tokens: 50000

# NEW: Optimization hints
optimization:
  domains:
    auth: ["auth-spec.md", "auth-design.md"]
    payment: ["payment/spec.md", "payment-integration.md"]
    users: ["users/spec.md"]

  # Suggest which domains to keep for common tasks
  task_hints:
    "login": ["auth"]
    "payment": ["payment"]
    "billing": ["payment"]
    "user profile": ["users", "auth"]
```

## Token Savings Examples

### Realistic Project (500-page spec)

**Without SpecWeave:**
- Full spec loaded: 500 pages × 300 tokens = 150,000 tokens
- Every query uses 150k tokens
- Cost: $0.015 × 150 = $2.25 per query

**With Context Loader (Pass 1):**
- Manifest loads only auth section: 50 pages = 15,000 tokens (90% reduction)
- Cost: $0.015 × 15 = $0.225 per query

**With Context Optimizer (Pass 2):**
- Further refine to login endpoint: 30 pages = 9,000 tokens (94% total reduction)
- Cost: $0.015 × 9 = $0.135 per query

**Savings: $2.25 → $0.135 (94% cost reduction)**

### Session Example (10 queries)

**Scenario:** Fix 3 auth bugs, 2 payment bugs, 1 user bug

| Query | Without | Pass 1 | Pass 2 | Savings |
|-------|---------|--------|--------|---------|
| Auth bug 1 | 150k | 45k (auth+pay+user) | 27k (auth only) | 82% |
| Auth bug 2 | 150k | 45k | 27k | 82% |
| Auth bug 3 | 150k | 45k | 27k | 82% |
| Payment bug 1 | 150k | 45k | 28k (payment only) | 81% |
| Payment bug 2 | 150k | 45k | 28k | 81% |
| User bug 1 | 150k | 45k | 30k (user only) | 80% |

**Total tokens:**
- Without: 900k tokens
- Pass 1 only: 270k tokens (70% reduction)
- Pass 2: 167k tokens (81% reduction)

**Cost savings:**
- Without: $13.50
- Pass 1 only: $4.05
- Pass 2: $2.50

**Additional savings: $1.55 per session (38% on top of Pass 1)**

## Best Practices

### 1. Let It Run Automatically

Default mode: auto-optimize after context-loader
- No manual intervention
- Adapts to each query
- Restores full context if needed

### 2. Review Removals for Critical Tasks

For production deploys, security reviews:
```bash
User: "Review security before deployment"

context-optimizer:
⚠️ Keeping full context (critical task detected)
```

### 3. Use Conservative Buffer for Complex Tasks

```yaml
buffer_strategy: "conservative"
```
- Keeps adjacent domains
- Includes integration points
- Safer for refactoring

### 4. Custom Domains for Your Project

```yaml
custom_domains:
  - "payment-processing"
  - "real-time-notifications"
  - "analytics-pipeline"
```

Helps optimizer understand your project structure.

### 5. Monitor Optimization Accuracy

If optimizer removes needed context:
- Lower `min_confidence` threshold
- Add `always_keep` rules
- Use `conservative` buffer

## Limitations

**What context-optimizer CAN'T do:**
- ❌ Predict future conversation needs (only analyzes current prompt)
- ❌ Understand implicit domain relationships (unless configured)
- ❌ Read your mind (if prompt is vague, keeps more context)

**What context-optimizer CAN do:**
- ✅ Analyze task type and domain from prompt
- ✅ Remove obviously unrelated specs/agents
- ✅ Restore removed context if later needed
- ✅ Learn from always_keep/custom_domains config

## Test Cases

### TC-001: Bug Fix Optimization
**Given:** Context with auth+payment+user specs (45k tokens)
**When:** User says "Fix login bug"
**Then:** Keeps only auth spec (27k tokens, 40% reduction)

### TC-002: Feature Development
**Given:** Context with multiple domains
**When:** User says "Add subscription billing"
**Then:** Keeps payment + integration specs (33% reduction)

### TC-003: Architecture Review (Broad)
**Given:** Context with all specs
**When:** User says "Review architecture"
**Then:** Keeps all specs (0% reduction, full context needed)

### TC-004: Vague Prompt
**Given:** Context with multiple specs
**When:** User says "Help me"
**Then:** Keeps all (low confidence, plays safe)

### TC-005: Manual Domain Specification
**Given:** Context with all specs
**When:** User says "Optimize for payment work"
**Then:** Keeps only payment domain (50%+ reduction)

## Future Enhancements

### Phase 2: Conversation History Analysis
- Track which context was actually used
- Remove sections never referenced
- Learn user patterns

### Phase 3: Dynamic Context Expansion
- Start with minimal context
- Add sections on-demand when mentioned
- "Just-in-time" context loading

### Phase 4: Cross-Increment Context
- Detect dependencies across increments
- Load context from multiple increments intelligently
- Maintain coherence across features

## Resources

- [Retrieval-Augmented Generation (RAG)](https://arxiv.org/abs/2005.11401) - Context retrieval patterns
- [LongRAG: Large Context Optimization](https://arxiv.org/abs/2310.03025) - Long context handling
- [Anthropic Context Windows](https://docs.anthropic.com/claude/docs/context-windows) - Best practices

---

## Summary

**context-optimizer** provides second-pass context optimization:

✅ **Intent-driven filtering** (analyzes user prompt)
✅ **Domain-aware** (removes unrelated specs)
✅ **Task-type specific** (bug fix vs feature vs architecture)
✅ **80%+ total reduction** (on top of context-loader's 70%)
✅ **Automatic** (runs after context-loader)
✅ **Safe** (restores context if needed)
✅ **Configurable** (custom domains, buffer strategy)

**Use it when:** Working with large specs (500+ pages) where even manifest-based loading results in 30k+ tokens.

**Skip it when:** Context already small (<10k), broad architectural questions, or planning new features from scratch.

**The result:** From 150k tokens → 27k tokens = 82% total reduction, enabling work on enterprise-scale specs within Claude's context window.
