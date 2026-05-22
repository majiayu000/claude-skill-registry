---
name: Prompt Manager
description: Optimize and manage AILANG teaching prompts for maximum conciseness and accuracy. Use when user asks to create/update prompts, optimize prompt length, or verify prompt accuracy.
---

# Prompt Manager

**Mission:** Create concise, accurate teaching prompts with maximum information density.

## Core Principle: Token Efficiency

**Target:** ~4000 tokens per prompt (currently ~8000+)
**Strategy:** Reference external docs, use tables, consolidate examples
**Validation:** Maintain eval success rates while reducing prompt size

## When to Use This Skill

Invoke when user mentions:
- "Create new prompt" / "update prompt" / "optimize prompt"
- "Make prompt more concise" / "reduce prompt length"
- "Fix prompt documentation" / "prompt-code mismatch"
- After implementing language features (keep prompt synchronized)
- Before eval baselines (verify accuracy)

## CLI Integration (v0.4.4+)

**NEW**: Prompts are now accessible via `ailang prompt` command (single source of truth).

### Display Prompts
```bash
# Get current/active prompt
ailang prompt

# Get specific version
ailang prompt --version v0.3.24

# List all available versions
ailang prompt --list

# Show metadata
ailang prompt --version v0.4.2 --info
```

### For Development
```bash
# Save prompt to file for editing
ailang prompt > temp_prompt.md

# Pipe to pager for reading
ailang prompt | less

# Quick syntax reference
ailang prompt | grep -A 20 "Quick Reference"
```

**Implementation**:
- Loader: `internal/prompt/loader.go` (reads from `prompts/versions.json`)
- CLI: `cmd/ailang/prompt.go`
- Eval harness uses `internal/prompt` package (single source of truth)

### Workflow: Editing Existing Prompts

**IMPORTANT**: When you edit a prompt file (e.g., `prompts/v0.4.2.md`), you MUST update its hash in `prompts/versions.json` for downstream users!

```bash
# 1. Edit the prompt file
vim prompts/v0.4.2.md

# 2. Update the hash in versions.json (REQUIRED!)
.claude/skills/prompt-manager/scripts/update_hash.sh v0.4.2

# 3. Verify downstream users see the change
ailang prompt --version v0.4.2 | head -20

# 4. If this is the active version, verify default users see it
ailang prompt | head -20
```

**Why this matters**:
- `ailang prompt` reads from `prompts/versions.json` → uses File field to locate prompt
- Eval harness uses `internal/prompt` package → same versions.json source
- Hash is stored but not validated by CLI (for dev flexibility)
- **Best practice**: Keep hash updated so it reflects actual file content
- Update versions.json = update for ALL downstream consumers (CLI, eval harness, agents)

**Single Source of Truth**: `prompts/versions.json` is the registry. Update it, and everyone sees the change.

**Note**: The eval harness's legacy `PromptLoader` (different from `internal/prompt`) DOES validate hashes. We're migrating to the simpler loader that doesn't validate (for easier development iteration).

---

## Quick Reference Scripts

### Create New Version
```bash
.claude/skills/prompt-manager/scripts/create_prompt_version.sh <new_version> <base_version> "<description>"
```
Creates versioned prompt file, computes hash, updates versions.json

### Update Hash
```bash
.claude/skills/prompt-manager/scripts/update_hash.sh <version>
```
Recomputes SHA256 after edits

### Verify Accuracy
```bash
.claude/skills/eval-analyzer/scripts/verify_prompt_accuracy.sh <version>
```
Catches prompt-code mismatches, false limitations

### Check Examples Coverage
```bash
.claude/skills/prompt-manager/scripts/check_examples_coverage.sh <version>
```
Verifies that features used in working examples are documented in prompt

### Analyze Size & Optimization Opportunities
```bash
.claude/skills/prompt-manager/scripts/analyze_prompt_size.sh prompts/v0.3.17.md
```
Shows: word count, section sizes, code blocks, tables, optimization opportunities

### Test Prompt Effectiveness
```bash
.claude/skills/prompt-manager/scripts/test_prompt.sh v0.3.18
```
Runs AILANG-only eval (no Python) with dev models to test prompt effectiveness

## Optimization Workflow

### 1. Analyze Current Prompt
```bash
.claude/skills/prompt-manager/scripts/analyze_prompt_size.sh prompts/v0.3.16.md
```

**Sample output:**
```
Total words: 4358 (target: <4000)
Total lines: 1214 (target: <200)
⚠️  OVER TARGET by 358 words (8%)

Code blocks: 60 (target: 5-10 comprehensive)
Table rows: 0 (target: 10+ tables)

Top sections by size:
  719 words - Effect System
  435 words - List Operations
  368 words - Algebraic Data Types
```

**High-ROI optimization areas identified by script:**
- 60 code blocks → consolidate to 5-10 comprehensive examples
- 0 tables → convert builtin/syntax docs to tables
- Large sections → link details to external docs

### 2. Create Optimized Version
```bash
.claude/skills/prompt-manager/scripts/create_prompt_version.sh v0.3.17 v0.3.16 "Optimize for conciseness (-50% tokens)"
```

### 3. Apply Optimization Strategies

**Reference [resources/prompt_optimization.md](resources/prompt_optimization.md) for:**
- Tables vs prose (builtin docs)
- Consolidating examples
- Linking to external docs
- Progressive disclosure patterns

**Key techniques:**
1. **Replace prose with tables** - Builtin functions, syntax rules
2. **Consolidate examples** - 8 comprehensive > 24 scattered
3. **Link to docs** - Type system details → docs/guides/types.md
4. **Quick reference** - 1-screen summary at top
5. **Remove redundancy** - Historical notes → CHANGELOG.md

### 4. Validate Optimization

**⚠️ CRITICAL: Must validate AFTER each optimization step!**

```bash
# 1. CHECK ALL CODE EXAMPLES (NEW REQUIREMENT!)
# Extract and test every AILANG code block in the prompt
# This catches syntax errors that cause regressions
.claude/skills/prompt-manager/scripts/validate_all_code.sh prompts/v0.3.17.md

# 2. Check new size
.claude/skills/prompt-manager/scripts/analyze_prompt_size.sh prompts/v0.3.17.md

# 3. Verify accuracy (no false limitations)
.claude/skills/eval-analyzer/scripts/verify_prompt_accuracy.sh v0.3.17

# 4. Check examples coverage (NEW - v0.4.1+)
.claude/skills/prompt-manager/scripts/check_examples_coverage.sh v0.3.17
# Ensures working examples are documented in prompt

# 5. Update hash
.claude/skills/prompt-manager/scripts/update_hash.sh v0.3.17

# 6. TEST PROMPT EFFECTIVENESS (CRITICAL!)
.claude/skills/prompt-manager/scripts/test_prompt.sh v0.3.17
# This runs AILANG-only eval (no Python baseline) with dev models
# Target: >40% AILANG success rate
```

**Success criteria:**
- ✅ Token reduction: 10-20% per iteration (NOT >50% in one step!)
- ✅ AILANG success rate: >40% (if <40%, revert and try smaller optimization)
- ✅ All external links resolve
- ✅ No increase in compilation errors
- ✅ Examples still work in REPL

**⚠️ If success rate drops >10%, REVERT and try smaller optimization**

### 5. Document Optimization
Add header to optimized prompt:
```markdown
---
Version: v0.3.17
Optimized: 2025-10-22
Token reduction: -54% (8200 → 3800 tokens)
Baseline: v0.3.16→v0.3.17 success rate maintained
---
```

### 6. Commit
```bash
git add prompts/v0.3.17.md prompts/versions.json
git commit -m "feat: Optimize v0.3.17 prompt for conciseness

- Reduced tokens: 8200 → 3800 (-54%)
- Builtin docs: prose → tables + reference ailang builtins list
- Examples: 24 scattered → 8 consolidated comprehensive
- Type system: moved details to docs/guides/types.md
- Added quick reference section at top
- Validated: eval success rate maintained"
```

## Optimization Strategies (Summary)

**Full guide:** [resources/prompt_optimization.md](resources/prompt_optimization.md)

### Quick Wins
1. **Tables > Prose** - Builtin docs, syntax rules (-67% tokens)
2. **Consolidate Examples** - 8 comprehensive > 24 scattered (-56% tokens)
3. **Link to Docs** - Move detailed explanations to external docs (-76% tokens)
4. **Quick Reference** - 1-screen summary at top
5. **Remove Redundancy** - Historical notes → CHANGELOG.md, implementation details → code links

### Anti-Patterns
- ❌ Explaining "why" (move to design docs)
- ❌ Historical context (move to changelog)
- ❌ Implementation details (link to code)
- ❌ Verbose examples (show, don't tell)
- ❌ Apologetic limitations (be direct)

### Optimization Checklist
- [ ] Token count <4000 words
- [ ] All external links resolve
- [ ] Examples work in REPL
- [ ] Eval baseline success rate maintained
- [ ] Hash updated in versions.json
- [ ] Optimization metrics documented in prompt header

## Common Tasks

**Detailed workflows:** [resources/workflow_guide.md](resources/workflow_guide.md)

### Fix False Limitation
Create version → Remove "❌ NO X" → Add "✅ X" with examples → Verify → Commit

### Add Feature
Create version → Add to capabilities table → Add consolidated example → Verify → Commit

### Optimize for Conciseness
Analyze size → Identify high-ROI sections → Apply techniques → Validate success rate → Document metrics → Commit

## Progressive Disclosure

1. **Always loaded:** skill.md (this file - workflow + optimization principles)
2. **Load for optimization:** resources/prompt_optimization.md (detailed strategies)
3. **Load for workflows:** resources/workflow_guide.md (detailed examples)
4. **Execute as needed:** Scripts (create_prompt_version.sh, update_hash.sh)

## Integration

- **eval-analyzer:** verify_prompt_accuracy.sh catches mismatches
- **post-release:** Run baselines after optimization
- **ailang builtins list:** Reference instead of duplicating
- **docs/guides/:** Link to instead of explaining

## ⚠️ CRITICAL: Benchmark YAML Field Usage (v0.4.8 Discovery)

**Benchmarks use TWO different fields for prompts:**

| Field | Effect | When to Use |
|-------|--------|-------------|
| `prompt:` | **REPLACES** the teaching prompt | Only for language-agnostic tasks |
| `task_prompt:` | **APPENDS** to teaching prompt | Use this for AILANG benchmarks! |

**Example - WRONG (teaching prompt ignored):**
```yaml
prompt: |
  Write a program that parses JSON...
```

**Example - CORRECT (teaching prompt + task):**
```yaml
task_prompt: |
  Write a program that parses JSON...
```

**Why this matters:** If `prompt:` is used, AILANG models don't see the teaching prompt at all - they only see the task description. They won't know AILANG syntax!

**Best practice:** Always load the current AILANG teaching prompt (`ailang prompt`) when editing prompts or benchmarks, so you understand what models will see.

## ⚠️ When Editing Prompts: Load AILANG Syntax First

Before modifying the AILANG teaching prompt, load it to understand the syntax:
```bash
ailang prompt > /tmp/current_prompt.md
# Read and understand AILANG syntax patterns
# Then make informed edits
```

This prevents introducing syntax errors or patterns that don't match AILANG's actual capabilities.

## Success Metrics

**Target prompt profile:**
- Tokens: <4000 (~30-40% reduction from current, in 3 iterations)
- Lines: <300 (currently 500+)
- Examples: 40-50 (not <30!)
- Tables: 10+ for reference data
- AILANG success rate: >40%

## ⚠️ Lessons from v0.3.18 and v0.3.20 Failures

### v0.3.18 Failure: Over-Optimization

**What happened:** Optimized v0.3.17 → v0.3.18 with -59% token reduction (5189 → 2126 words)
**Result:** AILANG success rate collapsed to 4.8% (from expected ~40-60%)

**Root causes:**
1. **Too aggressive** - removed >50% content in one step
2. **Over-consolidated** - 64 → 21 examples (lost pattern variety)
3. **Tables replaced prose** - lost explanatory context for syntax rules
4. **Removed negatives** - "what NOT to do" examples are critical
5. **No incremental validation** - didn't test after each change

### v0.3.20 Failure: Incorrect Syntax in Examples

**What happened:** Prompt had 3 syntax errors: (1) `match { | pattern =>` (wrong), (2) `import "std/io"` (wrong), (3) `let (x, y) = tuple` (wrong)
**Result:** -4.8% regression (40.0% → 35.2%), 18 benchmarks failed with PAR_001 compile errors

**Root cause:** No validation that code examples in prompt actually work with AILANG parser

**Critical lessons:**
- ❌ DON'T optimize >20% per iteration
- ❌ DON'T reduce examples below 40 total
- ❌ DON'T replace all syntax prose with tables
- ❌ DON'T link critical syntax to external docs (AIs can't follow links)
- ❌ DON'T skip eval testing between iterations
- ❌ **DON'T trust code examples without testing them** (NEW!)
- ✅ DO optimize incrementally (3 iterations of 10-15% each)
- ✅ DO keep negative examples ("what NOT to do")
- ✅ DO validate with test_prompt.sh after EACH change
- ✅ DO maintain pattern repetition (models need to see things 3-5 times)
- ✅ **DO extract and test ALL code blocks in prompt** (NEW!)

**Full analysis:** [OPTIMIZATION_FAILURE_ANALYSIS.md](OPTIMIZATION_FAILURE_ANALYSIS.md)
