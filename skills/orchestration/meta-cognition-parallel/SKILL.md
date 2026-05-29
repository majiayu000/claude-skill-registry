---
name: meta-cognition-parallel
description: "EXPERIMENTAL: Three-layer parallel meta-cognition analysis. Triggers on: /meta-parallel, 三层分析, parallel analysis, 并行元认知"
---

# Meta-Cognition Parallel Analysis (Experimental)

> **Status:** Experimental | **Version:** 0.1.0
>
> This skill tests parallel three-layer cognitive analysis using `context: fork`.

## Concept

Instead of sequential analysis, this skill launches three parallel subagents - one for each cognitive layer - then synthesizes their results.

```
User Question
     │
     ▼
┌─────────────────────────────────────────────────────┐
│            meta-cognition-parallel                   │
│                  (Coordinator)                       │
└─────────────────────────────────────────────────────┘
     │
     ├─── Task(fork) ──► layer1-analyzer ──► L1 Result
     │                   (Language Mechanics)
     │
     ├─── Task(fork) ──► layer2-analyzer ──► L2 Result
     │                   (Design Choices)         ├── Parallel
     │                                            │
     └─── Task(fork) ──► layer3-analyzer ──► L3 Result
                         (Domain Constraints)
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

## Execution Instructions

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
  prompt: <content of agents/layer1-analyzer.md>
          + "\n\n## User Query\n" + $ARGUMENTS
)

Task(
  subagent_type: "general-purpose",
  run_in_background: true,
  prompt: <content of agents/layer2-analyzer.md>
          + "\n\n## User Query\n" + $ARGUMENTS
)

Task(
  subagent_type: "general-purpose",
  run_in_background: true,
  prompt: <content of agents/layer3-analyzer.md>
          + "\n\n## User Query\n" + $ARGUMENTS
)
```

### Step 3: Collect Results

Wait for all three agents to complete. Each returns structured analysis.

### Step 4: Cross-Layer Synthesis

With all three results, perform synthesis:

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

## Output Template

```markdown
# Three-Layer Meta-Cognition Analysis

> Query: [User's question]

---

## Layer 1: Language Mechanics
[L1 agent result]

---

## Layer 2: Design Choices
[L2 agent result]

---

## Layer 3: Domain Constraints
[L3 agent result]

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

*Analysis performed by meta-cognition-parallel v0.1.0 (experimental)*
```

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

## Limitations (Experimental)

- Subagent results are summarized, may lose detail
- Parallel execution depends on Claude Code version
- Cross-layer synthesis quality depends on result structure
- May have higher latency than sequential approach

## Feedback

This is experimental. Please report issues and suggestions to improve the three-layer parallel analysis approach.
