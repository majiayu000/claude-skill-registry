---
name: qa_review_triple-model
description: |
  Launch four independent AI code reviewers (Opus, Gemini, Codex, Kimi K2.5) to QA/QC code or notebooks.
  Each reviewer writes findings to separate markdown files, then orchestrator synthesizes.
  Use for critical code review, bug investigation, or quality assurance tasks.

  Triggers: triple review, quad review, four model review, independent code review, QAQC, 
  quality assurance, multi-model analysis, cross-validation, bug investigation, critical review,
  kimi review, togetherai review
---

# Multi-Model Code Review (4 Models)

## Overview

This skill launches four independent AI subagents (Opus, Gemini, Codex, and **Kimi K2.5**) to perform parallel code review. Each agent writes findings to markdown files in a workspace directory, then the orchestrator synthesizes a final report with consensus findings.

## When to Use

- Critical bug investigation requiring multiple perspectives
- QA/QC of important notebooks or modules
- Validation of complex logic
- Cross-checking findings before major changes
- When high confidence in analysis is required
- Testing scenarios where edge case detection is critical
- Security reviews requiring thorough analysis

## Usage

```
/triple_model_code_review [target] [focus_area]
```

**Examples**:
- `/triple_model_code_review examples/720_precipitation_methods_comprehensive.ipynb "plotting logic"`
- `/triple_model_code_review ras_commander/hdf/HdfResultsPlan.py "return type consistency"`
- `/triple_model_code_review ras_commander/precip/ "API contract validation"`
- `/triple_model_code_review src/auth/login.py "security vulnerabilities"`

## Workflow

1. **Create Workspace**: `workspace/{task}QAQC/{opus,gemini,codex,kimi,final}-analysis/`

2. **Launch 4 Parallel Subagents**:
   - **Opus** (general-purpose, model=opus): Deep reasoning, architecture analysis
   - **Gemini** (code-oracle-gemini): Large context, multi-file pattern analysis
   - **Codex** (code-oracle-codex): Code archaeology, API contract analysis
   - **Kimi K2.5** (code-oracle-kimi): Edge case detection, test generation focus, QA verification

3. **Handle Model Failures** (Graceful Degradation):
   - If a model fails or is unavailable, note it and continue
   - Synthesis works with 1-4 successful models
   - Report which models succeeded/failed to user

4. **Each Agent**:
   - Reads target files independently
   - Writes `qaqc-report.md` to their subfolder
   - Returns file path only (no large text in response)
   - If agent fails, creates empty report with error note

5. **Orchestrator Synthesizes**:
   - Reads all available reports (1-4)
   - Identifies consensus findings from successful models
   - Creates `FINAL_QAQC_REPORT.md` with agreement matrix
   - Highlights unique insights from each successful model
   - Notes which models were unavailable

## Subagent Prompts

### Opus Subagent

```
You are conducting an independent QA/QC analysis of [TARGET].

## Critical Issue
[DESCRIBE THE PROBLEM]

## Your Task
1. Read and analyze the target files
2. Identify root cause of the issue
3. Document specific line numbers and code evidence
4. Provide recommended fixes

## Output
Write comprehensive analysis to: workspace/[TASK]QAQC/opus-analysis/qaqc-report.md

Return ONLY the file path when complete.
```

### Gemini Subagent

```
You are conducting an independent QA/QC analysis using large context capabilities.

## Critical Issue
[DESCRIBE THE PROBLEM]

## Your Task
1. Read ALL relevant files in the target area
2. Trace data flow from source to symptom
3. Document column/type confusion if applicable
4. Provide method-by-method analysis

## Output
Write analysis to: workspace/[TASK]QAQC/gemini-analysis/qaqc-report.md

Return ONLY the file path when complete.
```

### Codex Subagent

```
You are conducting deep code analysis for QA/QC.

## Critical Issue
[DESCRIBE THE PROBLEM]

## Your Task
1. Deep analysis of target code
2. Code archaeology - how was bug introduced
3. API contract analysis - promises vs delivery
4. Test cases that would catch this bug

## Output
Write analysis to: workspace/[TASK]QAQC/codex-analysis/qaqc-report.md

Return ONLY the file path when complete.
```

### Kimi K2.5 Subagent (NEW)

```
You are conducting QA/QC analysis with focus on edge cases, testing gaps, and quality verification.

## Critical Issue
[DESCRIBE THE PROBLEM]

## Your Task
1. Identify edge cases and boundary conditions not handled
2. Find gaps in error handling and validation
3. Analyze test coverage - what tests are missing?
4. Check for race conditions and concurrency issues
5. Verify API contracts and type safety
6. Suggest specific test cases that would catch bugs

## Unique Focus Areas
- Edge case detection (null, undefined, empty inputs, extreme values)
- Test coverage gaps
- Error handling completeness
- Security vulnerabilities
- Performance bottlenecks

## Output
Write analysis to: workspace/[TASK]QAQC/kimi-analysis/qaqc-report.md

Return ONLY the file path when complete.
```

## Output Structure

```
workspace/{task}QAQC/
├── opus-analysis/
│   └── qaqc-report.md          # Deep reasoning analysis
├── gemini-analysis/
│   └── qaqc-report.md          # Large context analysis
├── codex-analysis/
│   └── qaqc-report.md          # Code archaeology analysis
├── kimi-analysis/              # NEW
│   └── qaqc-report.md          # Edge case & testing analysis
└── final-synthesis/
    └── FINAL_QAQC_REPORT.md    # Consensus findings
```

## Report Template

### Individual Reports

```markdown
# QA/QC Analysis Report: [Target]

**Analyst**: [Model Name]
**Date**: YYYY-MM-DD
**Target**: [file/folder]
**Status**: [CRITICAL/HIGH/MEDIUM/LOW]

## 1. Summary of Findings
## 2. Root Cause Analysis
## 3. Code Evidence (with line numbers)
## 4. Impact Assessment
## 5. Recommended Fixes
## 6. Verification Steps
## 7. Test Cases Needed (Kimi specific)
```

### Final Synthesis

```markdown
# Final QA/QC Synthesis Report

## Executive Summary
## Consensus Bug List
## Agreement Matrix (which reviewers found what)
  - Opus: [findings]
  - Gemini: [findings]
  - Codex: [findings]
  - Kimi: [findings]  # Edge cases & testing gaps
## Unique Insights by Model
  - Opus: [architectural issues]
  - Gemini: [multi-file patterns]
  - Codex: [API contract violations]
  - Kimi: [edge cases, missing tests, security gaps]
## Required Fixes (with exact code changes)
## Test Coverage Recommendations
## Verification Criteria
```

## Model Strengths Matrix

| Model | Best For | Unique Strengths |
|-------|----------|------------------|
| **Opus** | Architecture, logic flow | Deep reasoning, system design |
| **Gemini** | Large codebases | 1M+ token context, multi-file analysis |
| **Codex** | Implementation details | Code archaeology, API contracts |
| **Kimi K2.5** | Edge cases, testing | Boundary conditions, test gaps, security |

## Best Practices

1. **Be Specific**: Give clear problem description to all four agents
2. **Parallel Launch**: Launch all four agents in single message for speed
3. **File-Based Communication**: Agents write files, return paths only
4. **Consensus Focus**: Weight findings by agreement across reviewers
5. **Preserve Evidence**: Keep all reports in workspace for audit trail
6. **Consider Kimi's Edge Cases**: Kimi often finds issues others miss - don't ignore unique findings
7. **Test Generation**: Use Kimi's test recommendations to improve coverage

## Graceful Degradation & Error Handling

Not all users have access to all four models. The skill handles failures gracefully:

### Common Failure Scenarios

1. **API Key Not Set**: Model provider requires authentication
2. **Rate Limit Exceeded**: Free tier limits reached
3. **Model Unavailable**: Service temporarily down
4. **Subagent Timeout**: Analysis took too long
5. **Permission Denied**: Insufficient access rights

### Failure Response Protocol

When a subagent fails:

```
1. Log the failure with specific error reason
2. Create placeholder report: workspace/{task}QAQC/{model}-analysis/qaqc-report.md
3. Content: "ANALYSIS FAILED: [specific reason]"
4. Continue with remaining successful models
5. Notify user which models succeeded/failed
```

### Minimum Viable Review

The skill works with as few as **1 successful model**:
- **1 model**: Single perspective (still valuable)
- **2 models**: Cross-validation possible
- **3 models**: Good consensus building
- **4 models**: Optimal coverage

### User Notification Template

```
Multi-Model Code Review Complete

✅ Successful Models:
   - Opus: Analysis complete
   - Gemini: Analysis complete
   - Codex: Analysis complete

❌ Failed Models:
   - Kimi K2.5: API key not configured (TOGETHER_API_KEY missing)

Proceeding with synthesis of 3/4 models...
```

### Fallback Strategy by Model Count

| Available Models | Strategy | Confidence Level |
|-----------------|-----------|------------------|
| 4/4 (all) | Full consensus analysis | ⭐⭐⭐⭐⭐ Highest |
| 3/4 | Strong consensus with gap noted | ⭐⭐⭐⭐ High |
| 2/4 | Cross-validation sufficient | ⭐⭐⭐ Good |
| 1/4 | Single expert opinion | ⭐⭐ Moderate |
| 0/4 | **Abort** - No models available | ❌ Failed |

### Handling Partial Results

**If Kimi K2.5 fails** (edge case expert):
- Note: "Edge case analysis incomplete - consider manual edge case review"
- Still proceed with Opus/Gemini/Codex consensus

**If Gemini fails** (large context expert):
- Note: "Multi-file pattern analysis may be incomplete"
- Other models may miss cross-file issues

**If Codex fails** (implementation expert):
- Note: "API contract analysis incomplete"
- Focus on Opus architecture + Gemini patterns

**If Opus fails** (reasoning expert):
- Note: "Deep reasoning analysis unavailable"
- Weight Codex implementation findings higher

### Recommended Model Priority

If you can only configure some models, prioritize:

1. **Opus** - Best overall reasoning (if available)
2. **Gemini** - Best for large/multi-file analysis
3. **Kimi K2.5** - Best for testing/edge cases
4. **Codex** - Best for implementation details

### Configuration Check

Before running, verify model availability:

```bash
# Check which models are available
opencode models | grep -E "(opus|gemini|codex|kimi)"

# Check API keys
echo $TOGETHER_API_KEY
echo $OPENAI_API_KEY  
echo $GEMINI_API_KEY
```

## Example Sessions

### Example 1: All Models Available (Optimal)

```
User: /triple_model_code_review examples/720_precipitation_methods_comprehensive.ipynb "incremental vs cumulative confusion"

Claude: Creating workspace and launching 4 independent reviewers...

[Launches Opus, Gemini, Codex, Kimi K2.5 in parallel]

✅ All four reviewers completed successfully

All four reviewers identified the same bugs:
- Line 810: DataFrame passed instead of column (All 4 found)
- Line 1396: DataFrame passed instead of column (All 4 found)
- Lines 1777-1789: np.cumsum on DataFrame (All 4 found)

Kimi K2.5 additionally identified:
- Missing test for empty DataFrame input
- Edge case: single-row DataFrame handling
- No validation for NaN values in precipitation data

Reports saved to workspace/notebook720QAQC/
```

### Example 2: Graceful Degradation (1 Model Fails)

```
User: /triple_model_code_review src/auth/login.py "security vulnerabilities"

Claude: Creating workspace and launching 4 independent reviewers...

[Launches Opus, Gemini, Codex, Kimi K2.5 in parallel]

Results:
✅ Opus: Analysis complete
✅ Gemini: Analysis complete  
✅ Codex: Analysis complete
❌ Kimi K2.5: Failed - API key not configured

Note: Kimi K2.5 (edge case expert) unavailable. Edge case coverage may be incomplete.

3/4 models found these security issues:
- Line 45: SQL injection vulnerability (All 3 found)
- Line 78: Missing input validation (All 3 found)
- Line 23: Weak password hashing (Opus + Codex found)

Missing: Edge case analysis for malformed inputs (usually Kimi's strength)

Reports saved to workspace/loginQAQC/
```

### Example 3: Minimal Viable Review (2 Models)

```
User: /triple_model_code_review ras_commander/core.py "performance bottleneck"

Claude: Creating workspace and launching 4 independent reviewers...

Results:
✅ Opus: Analysis complete
❌ Gemini: Failed - Rate limit exceeded
❌ Codex: Failed - Service unavailable
✅ Kimi K2.5: Analysis complete

Proceeding with 2/4 models (Opus + Kimi)

Consensus findings:
- Line 234: O(n²) loop identified by both
- Line 567: Memory leak in caching (Kimi found with test case)

Opus unique insight: Architectural recommendation to use generators
Kimi unique insight: Specific benchmark test showing 10x slowdown

Note: 2-model review sufficient for this scope. Consider re-running with all models for critical code.

Reports saved to workspace/coreQAQC/
```

## When to Weight Kimi's Findings Higher

Kimi K2.5 findings should be given extra weight when:
- **Edge cases are critical** (financial calculations, safety systems)
- **Testing is insufficient** (new codebase, legacy code)
- **Security matters** (user input handling, authentication)
- **Error handling is crucial** (production systems, data pipelines)

## Integration with Other Skills

**Works with:**
- `dev_invoke_kimi-cli` - Follow up with Kimi-specific testing
- `dev_invoke_gemini-cli` - Deep dive on Gemini findings
- `dev_invoke_codex-cli` - Implement fixes identified
- `using-git-worktrees` - Create isolated workspace for fixes

## See Also

- **Kimi CLI Skill**: `.claude/skills/dev_invoke_kimi-cli/SKILL.md`
- **Subagent Output Pattern**: `.claude/rules/subagent-output-pattern.md`
- **Agent Integration Testing**: `.claude/rules/testing/agent-integration-testing.md`
- **Orchestrator Pattern**: Root `CLAUDE.md` - Orchestrator section

## Troubleshooting Model Failures

### Opus Failures

**Symptom**: "Model not available" or "Rate limit exceeded"

**Solutions**:
```bash
# Check Opus availability
opencode models | grep opus

# Alternative: Use Sonnet if Opus unavailable
opencode run -m claude-sonnet-4.5 "..."
```

### Gemini Failures

**Symptom**: "Gemini API error" or "Context length exceeded"

**Solutions**:
```bash
# Check Gemini API key
export GEMINI_API_KEY=your_key_here

# Try smaller context window model
opencode run -m gemini-1.5-flash "..."
```

### Codex Failures

**Symptom**: "Codex service unavailable" or "OpenAI error"

**Solutions**:
```bash
# Check OpenAI API key
export OPENAI_API_KEY=your_key_here

# Alternative: Use GPT-4o
opencode run -m gpt-4o "..."
```

### Kimi K2.5 Failures

**Symptom**: "Together.ai error" or "API key not found"

**Solutions**:
```bash
# Set Together.ai API key
export TOGETHER_API_KEY=your_key_here

# Alternative: Use Opencode's free Kimi
opencode run -m opencode/kimi-k2.5-free "..."

# Check Together.ai credits
curl -H "Authorization: Bearer $TOGETHER_API_KEY" \
  https://api.together.xyz/v1/models
```

### General Troubleshooting

**All models failing?**
1. Check internet connection
2. Verify opencode CLI: `opencode --version`
3. Check auth status: `opencode auth status`
4. Review logs: `opencode debug`

**Intermittent failures?**
- Retry with backoff: Wait 30 seconds and re-run
- Check rate limits: May need to upgrade tier
- Use fewer models: Start with 2-3 instead of 4

**Permission denied?**
- Check workspace directory permissions
- Ensure write access to `workspace/` folder
- Run from project root with proper access
