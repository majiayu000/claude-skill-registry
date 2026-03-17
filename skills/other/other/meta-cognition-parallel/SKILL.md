---
name: meta-cognition-parallel
description: "EXPERIMENTAL: Three-layer parallel meta-cognition analysis. Triggers on: /meta-parallel, 三层分析, parallel analysis, 并行元认知"
argument-hint: "<rust_question>"
---

# Meta-Cognition Parallel Analysis (Experimental)

> **Status:** Experimental | **Version:** 0.2.0 | **Last Updated:** 2025-01-27
>
> This skill tests parallel three-layer cognitive analysis.

## Concept

Instead of sequential analysis, this skill launches three parallel analyzers - one for each cognitive layer - then synthesizes their results.

```
User Question
     │
     ▼
┌─────────────────────────────────────────────────────┐
│            meta-cognition-parallel                   │
│                  (Coordinator)                       │
└─────────────────────────────────────────────────────┘
     │
     ├─── Layer 1 ──► Language Mechanics ──► L1 Result
     │
     ├─── Layer 2 ──► Design Choices     ──► L2 Result
     │                                            ├── Parallel (Agent Mode)
     │                                            │   or Sequential (Inline)
     └─── Layer 3 ──► Domain Constraints ──► L3 Result
     │
     ▼
┌─────────────────────────────────────────────────────┐
│              Cross-Layer Synthesis                   │
│         (In main context with all results)          │
└─────────────────────────────────────────────────────┘
     │
     ▼
Domain-Correct Architectural Solution
```

## Usage

```
/meta-parallel <your Rust question>
```

**Example:**
```
/meta-parallel 我的交易系统报 E0382 错误，应该用 clone 吗？
```

## Execution Mode Detection

**CRITICAL: Check agent file availability first to determine execution mode.**

Try to read layer analyzer files:
- `../../agents/layer1-analyzer.md`
- `../../agents/layer2-analyzer.md`
- `../../agents/layer3-analyzer.md`

---

## Agent Mode (Plugin Install) - Parallel Execution

**When all layer analyzer files exist at `../../agents/`:**

### Step 1: Parse User Query

Extract from `$ARGUMENTS`:
- The original question
- Any code snippets
- Domain hints (trading, web, embedded, etc.)

### Step 2: Launch Three Parallel Agents

**CRITICAL: Launch all three Tasks in a SINGLE message to enable parallel execution.**

```
Read agent files, then launch in parallel:

Task(
  subagent_type: "general-purpose",
  run_in_background: true,
  prompt: <content of ../../agents/layer1-analyzer.md>
          + "\n\n## User Query\n" + $ARGUMENTS
)

Task(
  subagent_type: "general-purpose",
  run_in_background: true,
  prompt: <content of ../../agents/layer2-analyzer.md>
          + "\n\n## User Query\n" + $ARGUMENTS
)

Task(
  subagent_type: "general-purpose",
  run_in_background: true,
  prompt: <content of ../../agents/layer3-analyzer.md>
          + "\n\n## User Query\n" + $ARGUMENTS
)
```

### Step 3: Collect Results

Wait for all three agents to complete. Each returns structured analysis.

### Step 4: Cross-Layer Synthesis

With all three results, perform synthesis per template below.

---

## Inline Mode (Skills-only Install) - Sequential Execution

**When layer analyzer files are NOT available, execute analysis directly:**

### Step 1: Parse User Query

Same as Agent Mode - extract question, code, and domain hints from `$ARGUMENTS`.

### Step 2: Execute Layer 1 - Language Mechanics

Analyze the Rust language mechanics involved:

```markdown
## Layer 1: Language Mechanics

**Error/Pattern Identified:**
- Error code: E0XXX (if applicable)
- Pattern: ownership/borrowing/lifetime/etc.

**Root Cause:**
[Explain why this error occurs in terms of Rust's ownership model]

**Language-Level Solutions:**
1. [Solution 1]: description
2. [Solution 2]: description

**Confidence:** HIGH | MEDIUM | LOW
**Reasoning:** [Why this confidence level]
```

**Focus areas:**
- Ownership rules (move, copy, borrow)
- Lifetime annotations
- Borrowing rules (shared vs mutable)
- Error codes and their meanings

### Step 3: Execute Layer 2 - Design Choices

Analyze the design patterns and trade-offs:

```markdown
## Layer 2: Design Choices

**Design Pattern Context:**
- Current approach: [What pattern is being used]
- Problem: [Why it conflicts with Rust's rules]

**Design Alternatives:**
| Pattern | Pros | Cons | When to Use |
|---------|------|------|-------------|
| Pattern A | ... | ... | ... |
| Pattern B | ... | ... | ... |

**Recommended Pattern:**
[Which pattern fits best and why]

**Confidence:** HIGH | MEDIUM | LOW
**Reasoning:** [Why this confidence level]
```

**Focus areas:**
- Smart pointer choices (Box, Rc, Arc)
- Interior mutability patterns (Cell, RefCell, Mutex)
- Ownership transfer vs sharing
- Cloning vs references

### Step 4: Execute Layer 3 - Domain Constraints

Analyze domain-specific requirements:

```markdown
## Layer 3: Domain Constraints

**Domain Identified:** [trading/fintech | web | CLI | embedded | etc.]

**Domain-Specific Requirements:**
- [ ] Performance: [requirements]
- [ ] Safety: [requirements]
- [ ] Concurrency: [requirements]
- [ ] Auditability: [requirements]

**Domain Best Practices:**
1. [Best practice 1]
2. [Best practice 2]

**Constraints on Solution:**
- MUST: [hard requirements]
- SHOULD: [soft requirements]
- AVOID: [anti-patterns for this domain]

**Confidence:** HIGH | MEDIUM | LOW
**Reasoning:** [Why this confidence level]
```

**Focus areas:**
- Industry requirements (FinTech regulations, web scalability, etc.)
- Performance constraints
- Safety and correctness requirements
- Common patterns in the domain

### Step 5: Cross-Layer Synthesis

Combine all three layers:

```markdown
## Cross-Layer Synthesis

### Layer Results Summary

| Layer | Key Finding | Confidence |
|-------|-------------|------------|
| L1 (Mechanics) | [Summary] | [Level] |
| L2 (Design) | [Summary] | [Level] |
| L3 (Domain) | [Summary] | [Level] |

### Cross-Layer Reasoning

1. **L3 → L2:** [How domain constraints affect design choice]
2. **L2 → L1:** [How design choice determines mechanism]
3. **L1 ← L3:** [Direct domain impact on language features]

### Synthesized Recommendation

**Problem:** [Restated with full context]

**Solution:** [Domain-correct architectural solution]

**Rationale:**
- Domain requires: [L3 constraint]
- Design pattern: [L2 pattern]
- Mechanism: [L1 implementation]

### Confidence Assessment

- **Overall:** HIGH | MEDIUM | LOW
- **Limiting Factor:** [Which layer had lowest confidence]
```

---

## Output Template

Both modes produce the same output format:

```markdown
# Three-Layer Meta-Cognition Analysis

> Query: [User's question]

---

## Layer 1: Language Mechanics
[L1 analysis result]

---

## Layer 2: Design Choices
[L2 analysis result]

---

## Layer 3: Domain Constraints
[L3 analysis result]

---

## Cross-Layer Synthesis

### Reasoning Chain
```
L3 Domain: [Constraint]
    ↓ implies
L2 Design: [Pattern]
    ↓ implemented via
L1 Mechanism: [Feature]
```

### Final Recommendation

**Do:** [Recommended approach]

**Don't:** [What to avoid]

**Code Pattern:**
```rust
// Recommended implementation
```

---

*Analysis performed by meta-cognition-parallel v0.2.0 (experimental)*
```

---

## Test Scenarios

### Test 1: Trading System E0382
```
/meta-parallel 交易系统报 E0382，trade record 被 move 了
```

Expected: L3 identifies FinTech constraints → L2 suggests shared immutable → L1 recommends Arc<T>

### Test 2: Web API Concurrency
```
/meta-parallel Web API 中多个 handler 需要共享数据库连接池
```

Expected: L3 identifies Web constraints → L2 suggests connection pooling → L1 recommends Arc<Pool>

### Test 3: CLI Tool Config
```
/meta-parallel CLI 工具如何处理配置文件和命令行参数的优先级
```

Expected: L3 identifies CLI constraints → L2 suggests config precedence pattern → L1 recommends builder pattern

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Agent files not found | Skills-only install | Use inline mode (sequential) |
| Agent timeout | Complex analysis | Wait longer or use inline mode |
| Incomplete layer result | Agent issue | Fill in with inline analysis |

## Limitations

- **Agent Mode:** Parallel execution, faster but requires plugin install
- **Inline Mode:** Sequential execution, slower but works everywhere
- Cross-layer synthesis quality depends on result structure
- May have higher latency than simple single-layer analysis

## Feedback

This is experimental. Please report issues and suggestions to improve the three-layer analysis approach.
