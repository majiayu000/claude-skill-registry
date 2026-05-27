---
name: Benchmark Manager
description: Create and manage AILANG eval benchmarks. Use when user asks to create benchmarks, fix benchmark issues, debug failing benchmarks, or analyze benchmark results.
---

# Benchmark Manager

Manage AILANG evaluation benchmarks with correct prompt integration, debugging workflows, and best practices learned from real benchmark failures.

## Quick Start

**Debugging a failing benchmark:**
```bash
# 1. Show the full prompt that models see
.claude/skills/benchmark-manager/scripts/show_full_prompt.sh json_parse

# 2. Test a benchmark with a specific model
ailang eval-suite --models claude-haiku-4-5 --benchmarks json_parse

# 3. Check benchmark YAML for common issues
.claude/skills/benchmark-manager/scripts/check_benchmark.sh benchmarks/json_parse.yml
```

## When to Use This Skill

Invoke this skill when:
- User asks to create a new benchmark
- User asks to debug/fix a failing benchmark
- User wants to understand why models generate wrong code
- User asks about benchmark YAML format
- Benchmarks show 0% pass rate despite language support

## CRITICAL: prompt vs task_prompt

**This is the most important concept for benchmark management.**

### The Problem (v0.4.8 Discovery)

Benchmarks have TWO different prompt fields with VERY different behavior:

| Field | Behavior | Use When |
|-------|----------|----------|
| `prompt:` | **REPLACES** the teaching prompt entirely | Testing raw model capability (rare) |
| `task_prompt:` | **APPENDS** to teaching prompt | Normal benchmarks (99% of cases) |

### Why This Matters

```yaml
# BAD - Model never sees AILANG syntax!
prompt: |
  Write a program that prints "Hello"

# GOOD - Model sees teaching prompt + task
task_prompt: |
  Write a program that prints "Hello"
```

With `prompt:`, models generate Python/pseudo-code because they never learn AILANG syntax.

### How Prompts Combine

From `internal/eval_harness/spec.go` (lines 91-93):
```go
fullPrompt := basePrompt  // Teaching prompt from prompts/v0.4.x.md
if s.TaskPrompt != "" {
    fullPrompt = fullPrompt + "\n\n## Task\n\n" + s.TaskPrompt
}
```

The teaching prompt teaches AILANG syntax; `task_prompt` adds the specific task.

## Available Scripts

### `scripts/show_full_prompt.sh`

Shows the complete prompt that models receive for a benchmark.

**Usage:**
```bash
.claude/skills/benchmark-manager/scripts/show_full_prompt.sh <benchmark_id>

# Example:
.claude/skills/benchmark-manager/scripts/show_full_prompt.sh json_parse
```

### `scripts/check_benchmark.sh`

Validates a benchmark YAML file for common issues.

**Usage:**
```bash
.claude/skills/benchmark-manager/scripts/check_benchmark.sh benchmarks/<name>.yml
```

**Checks for:**
- Using `prompt:` instead of `task_prompt:` (warning)
- Missing required fields
- Invalid capability names
- Syntax errors in YAML

### `scripts/test_benchmark.sh`

Runs a quick single-model test of a benchmark.

**Usage:**
```bash
.claude/skills/benchmark-manager/scripts/test_benchmark.sh <benchmark_id> [model]

# Examples:
.claude/skills/benchmark-manager/scripts/test_benchmark.sh json_parse
.claude/skills/benchmark-manager/scripts/test_benchmark.sh json_parse claude-haiku-4-5
```

## Benchmark YAML Format

### Required Fields

```yaml
id: my_benchmark              # Unique identifier (snake_case)
description: "Short description of what this tests"
languages: ["python", "ailang"]
entrypoint: "main"            # Function to call
caps: ["IO"]                  # Required capabilities
difficulty: "easy|medium|hard"
expected_gain: "low|medium|high"
task_prompt: |                # ALWAYS use task_prompt, not prompt!
  Write a program in <LANG> that:
  1. Does something
  2. Prints the result

  Output only the code, no explanations.
expected_stdout: |            # Exact expected output
  expected output here
```

### Capability Names

Valid capabilities: `IO`, `FS`, `Clock`, `Net`

```yaml
# File I/O
caps: ["IO"]

# HTTP requests
caps: ["Net", "IO"]

# File system operations
caps: ["FS", "IO"]
```

## Creating New Benchmarks

### Step 1: Determine Requirements

- What language feature/capability is being tested?
- Can models solve this with just the teaching prompt?
- What's the expected output?

### Step 2: Write the Benchmark

```yaml
id: my_new_benchmark
description: "Test feature X capability"
languages: ["python", "ailang"]
entrypoint: "main"
caps: ["IO"]
difficulty: "medium"
expected_gain: "medium"
task_prompt: |
  Write a program in <LANG> that:
  1. Clear description of task
  2. Another step
  3. Print the result

  Output only the code, no explanations.
expected_stdout: |
  exact expected output
```

### Step 3: Validate and Test

```bash
# Check for issues
.claude/skills/benchmark-manager/scripts/check_benchmark.sh benchmarks/my_new_benchmark.yml

# Test with cheap model first
ailang eval-suite --models claude-haiku-4-5 --benchmarks my_new_benchmark
```

## Debugging Failing Benchmarks

### Symptom: 0% Pass Rate Despite Language Support

**Check 1: Is it using `task_prompt:`?**
```bash
grep -E "^prompt:" benchmarks/failing_benchmark.yml
# If this returns a match, change to task_prompt:
```

**Check 2: What prompt do models see?**
```bash
.claude/skills/benchmark-manager/scripts/show_full_prompt.sh failing_benchmark
```

**Check 3: Is the teaching prompt up to date?**
```bash
# After editing prompts/v0.x.x.md, you MUST rebuild:
make quick-install
```

### Symptom: Models Copy Template Instead of Solving Task

The teaching prompt includes a template structure. If models copy it verbatim:

1. Make sure task is clearly different from examples in teaching prompt
2. Check that `task_prompt` explicitly describes what to do
3. Consider if the task description is ambiguous

### Symptom: compile_error on Valid Syntax

Common AILANG-specific issues models get wrong:

| Wrong | Correct | Notes |
|-------|---------|-------|
| `print(42)` | `print(show(42))` | print expects string |
| `a % b` | `mod_Int(a, b)` | No % operator |
| `def main()` | `export func main()` | Wrong keyword |
| `for x in xs` | `match xs { ... }` | No for loops |

If models consistently make these mistakes, the teaching prompt needs improvement (use prompt-manager skill).

## Common Mistakes

### 1. Using `prompt:` Instead of `task_prompt:`

```yaml
# WRONG - Models never see AILANG syntax
prompt: |
  Write code that...

# CORRECT - Teaching prompt + task
task_prompt: |
  Write code that...
```

### 2. Forgetting to Rebuild After Prompt Changes

```bash
# After editing prompts/v0.x.x.md:
make quick-install  # REQUIRED!
```

### 3. Putting Hints in Benchmarks

```yaml
# WRONG - Hints in benchmark
task_prompt: |
  Write code that prints 42.
  Hint: Use print(show(42)) in AILANG.

# CORRECT - No hints; if models fail, fix the teaching prompt
task_prompt: |
  Write code that prints 42.
```

If models need AILANG-specific hints, the teaching prompt is incomplete. Use the prompt-manager skill to fix it.

### 4. Testing Too Many Models at Once

```bash
# WRONG - Expensive and slow for debugging
ailang eval-suite --full --benchmarks my_test

# CORRECT - Use one cheap model first
ailang eval-suite --models claude-haiku-4-5 --benchmarks my_test
```

## Resources

### Reference Guide
See [`resources/reference.md`](resources/reference.md) for:
- Complete list of valid benchmark fields
- Capability reference
- Example benchmarks

### Related Skills
- **prompt-manager**: When benchmark failures indicate teaching prompt issues
- **eval-analyzer**: For analyzing results across many benchmarks
- **use-ailang**: For writing correct AILANG code

## Notes

- Benchmarks live in `benchmarks/` directory
- Eval results go to `eval_results/` directory
- Teaching prompt is embedded in binary - rebuild after changes
- Use `<LANG>` placeholder in task_prompt - it's replaced with "AILANG" or "Python"
