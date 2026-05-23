---
name: explain-like-senior
description: Senior-level code explanations with deep technical insights and context
disable-model-invocation: false
---

# Senior Developer Explanation

I'll explain this code as a senior developer would, focusing on the why behind decisions.

## Token Optimization Strategy

**Target Reduction:** 60% (4,000-6,000 → 1,500-2,500 tokens)
**Optimization Status:** ✅ Optimized (Phase 2 Batch 3B, 2026-01-26)

### Core Optimization Patterns

#### 1. Focused Scope Analysis (30-40% savings)
**Problem:** Reading entire codebase for context wastes tokens
**Solution:** Laser-focus on specified file/function only
```bash
# ❌ AVOID: Exploring entire codebase
Glob **/*.ts  # 500+ tokens
Read all related files  # 2,000+ tokens

# ✅ PREFER: Targeted analysis
Grep "class UserService" --output_mode files_with_matches  # 50 tokens
Read src/services/UserService.ts  # 300 tokens
```
**Token impact:** 2,500 → 350 tokens (86% reduction)

#### 2. Architecture Context Reuse (20-30% savings)
**Problem:** Re-analyzing project architecture each time
**Solution:** Leverage cached `/understand` results
```bash
# ❌ AVOID: Fresh architecture analysis
Glob src/**  # 400 tokens
Read package.json, tsconfig.json  # 500 tokens
Analyze framework patterns  # 800 tokens

# ✅ PREFER: Reuse cached architecture
Read .claude/cache/understand/architecture.json  # 100 tokens
# Contains: framework, patterns, conventions, tech stack
```
**Token impact:** 1,700 → 100 tokens (94% reduction)

#### 3. Grep for Related Patterns (15-25% savings)
**Problem:** Reading multiple files to find similar implementations
**Solution:** Grep for code patterns before reading files
```bash
# ❌ AVOID: Speculative file reads
Read src/services/*.ts  # 2,000+ tokens across 10 files

# ✅ PREFER: Grep-then-read approach
Grep "implements Repository" --output_mode files_with_matches  # 30 tokens
Grep "async.*transaction" --output_mode content -A 3 -B 1  # 150 tokens
Read only the 2-3 most relevant files  # 600 tokens
```
**Token impact:** 2,000 → 780 tokens (61% reduction)

#### 4. Progressive Depth Disclosure (20-30% savings)
**Problem:** Providing deep technical details when overview suffices
**Solution:** Start with overview, dive deeper only on request
```bash
# Initial explanation (quick overview)
- High-level architecture explanation: 400 tokens
- Key design decisions: 300 tokens
- Trade-offs summary: 200 tokens
Total: 900 tokens

# Only if user requests --deep flag
- Alternative approaches analysis: 600 tokens
- Performance implications: 400 tokens
- Scalability considerations: 400 tokens
Additional: 1,400 tokens
```
**Token impact:** 2,300 → 900 tokens base (61% reduction)

#### 5. Session State for Multi-Turn Explanations (25-35% savings)
**Problem:** Re-reading code context in follow-up questions
**Solution:** Track explained code in session state
```bash
# First explanation
Read src/auth/AuthService.ts  # 400 tokens
Explain implementation  # 800 tokens

# Follow-up question: "Why did they use JWT instead of sessions?"
# ❌ AVOID: Re-reading file (400 tokens)
# ✅ PREFER: Use session state (0 tokens - already in context)
Reference previous explanation, focus on JWT rationale  # 300 tokens
```
**Token impact:** Per follow-up: 700 → 300 tokens (57% reduction)

#### 6. Early Exit for Simple Code (30-50% savings)
**Problem:** Over-analyzing straightforward implementations
**Solution:** Detect simple patterns and provide concise explanation
```bash
# Detection criteria for early exit:
- Single-purpose utility function (< 20 lines)
- Standard CRUD operations following framework conventions
- Simple data transformations without business logic
- Obvious design patterns (Factory, Singleton, etc.)

# ❌ AVOID: Deep analysis of simple utility
Read context files: 600 tokens
Analyze alternatives: 500 tokens
Performance considerations: 400 tokens
Total: 1,500 tokens

# ✅ PREFER: Concise explanation
Brief overview: 200 tokens
Key insight: 150 tokens
Total: 350 tokens (77% reduction)
```
**Token impact:** 1,500 → 350 tokens (77% reduction)

### Caching Strategy

**Cache Location:** `.claude/cache/explain-like-senior/`

**Cached Data:**
- **Architecture patterns:** Framework idioms, common patterns, conventions
- **Related implementations:** Similar code structures for comparison
- **Technical decisions:** Historical context from previous explanations
- **Performance benchmarks:** Known bottlenecks and optimization patterns

**Cache Sharing:**
- Reuses `/understand` architecture analysis (saves 800-1,200 tokens)
- Shares with `/refactor` for consistency (saves 400-600 tokens)
- Leverages `/review` code patterns cache (saves 300-500 tokens)

**Cache Validity:**
- Valid until major codebase refactoring detected
- Invalidated by framework upgrades or architecture changes
- Automatically refreshed if cached file modified

### Token Budget by Scope

| Scope | Token Range | Use Case |
|-------|-------------|----------|
| Single function | 600-1,200 | Explain specific function logic |
| Single file | 800-1,500 | Explain module/class implementation |
| Related files | 1,200-2,000 | Explain feature across 2-3 files |
| Deep analysis | 1,500-2,500 | Comprehensive analysis with alternatives |

**Comparison with unoptimized approach:**
- Unoptimized: 4,000-6,000 tokens (reads entire codebase context)
- Optimized: 1,500-2,500 tokens (focused scope with caching)
- **Savings: 60% reduction**

### Usage Examples

```bash
# Minimal explanation (600-1,200 tokens)
explain-like-senior src/utils/formatDate.ts

# File-level explanation (800-1,500 tokens)
explain-like-senior src/services/UserService.ts

# Function-specific explanation (600-1,200 tokens)
explain-like-senior src/services/UserService.ts:createUser

# Deep analysis with alternatives (1,500-2,500 tokens)
explain-like-senior --deep src/core/auth/JWTStrategy.ts

# Multi-turn conversation (leverages session state)
explain-like-senior src/api/PaymentController.ts  # Initial: 1,200 tokens
# Follow-up: "Why Stripe over PayPal?"  # Follow-up: 300 tokens (57% savings)
```

### Optimization Checklist

**Before explanation:**
- [ ] Check if `/understand` cache exists (reuse architecture context)
- [ ] Identify exact file/function scope (avoid codebase exploration)
- [ ] Detect if code is simple/obvious (early exit opportunity)
- [ ] Check session state for previous explanations (avoid re-reading)

**During explanation:**
- [ ] Use Grep to find related patterns (not Read multiple files)
- [ ] Start with overview (defer deep analysis unless --deep flag)
- [ ] Reference cached architecture patterns (not fresh analysis)
- [ ] Focus on why/trade-offs (not exhaustive what/how)

**After explanation:**
- [ ] Store key insights in session state (for follow-up questions)
- [ ] Update cache with new patterns discovered (for future use)
- [ ] Verify token usage within budget (1,500-2,500 range)

I'll analyze the code using native tools:
- **Grep tool** to locate code and find related implementations (no speculative reads)
- **Read tool** to examine the specified code structure and patterns (targeted)
- **Glob tool** to understand the broader codebase context (only if needed for architecture insights)

**Technical Context:**
- Why this approach was chosen over alternatives
- Trade-offs and architectural decisions made
- Performance implications and considerations
- Maintenance and scalability factors

**Business Context:**
- How this fits into the larger system architecture
- Impact on user experience and business goals
- Cost implications and resource considerations
- Timeline and delivery constraints that influenced decisions

**Senior-Level Insights:**
- "This pattern works now but will need refactoring at 10x scale"
- "The complexity here is justified because of [specific business requirement]"
- "This is a common anti-pattern, but acceptable given [constraints]"
- "Consider this alternative approach for better [maintainability/performance]"

**Experience-Based Guidance:**
- Common pitfalls junior developers miss in this pattern
- Edge cases that frequently cause issues in production
- Integration points that often fail and how to mitigate
- Performance bottlenecks that emerge at scale

**Mentoring Approach:**
- Explains not just WHAT the code does but WHY it exists
- Points out subtle details that impact long-term maintenance
- Shares lessons learned from similar implementations
- Provides actionable next steps for improvement

**Code Evolution Perspective:**
- How this code will likely need to change as requirements evolve
- Technical debt considerations and when to address them
- Refactoring opportunities and their priority levels
- Architecture decisions that will impact future development

**Important**: I will NEVER:
- Add "Co-authored-by" or any Claude signatures
- Include "Generated with Claude Code" or similar messages
- Modify git config or user credentials
- Add any AI/assistant attribution to the commit

This provides the kind of contextual, experience-driven explanation that helps developers grow from junior to senior level thinking.