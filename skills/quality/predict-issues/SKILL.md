---
name: predict-issues
description: Proactive problem identification through code analysis and pattern detection
disable-model-invocation: false
---

# Predictive Code Analysis  

I'll analyze your codebase to predict potential problems before they impact your project.

## Strategic Thinking Process

<think>
To make accurate predictions, I need to consider:

1. **Pattern Recognition**
   - Which code patterns commonly lead to problems?
   - Are there growing complexity hotspots?
   - Do I see anti-patterns that will cause issues at scale?
   - Are there ticking time bombs (hardcoded values, assumptions)?

2. **Risk Assessment Framework**
   - Likelihood: How probable is this issue to occur?
   - Impact: How severe would the consequences be?
   - Timeline: When might this become a problem?
   - Effort: How hard would it be to fix now vs later?

3. **Common Problem Categories**
   - Performance: O(n²) algorithms, memory leaks, inefficient queries
   - Maintainability: High complexity, poor naming, tight coupling
   - Security: Input validation gaps, exposed secrets, weak auth
   - Scalability: Hardcoded limits, single points of failure

4. **Prediction Strategy**
   - Start with highest risk areas (critical path code)
   - Look for patterns that break at 10x, 100x scale
   - Check for technical debt accumulation
   - Identify brittleness in integration points
</think>

**Token Optimization:**
- ✅ Grep-before-Read for pattern detection (no speculative reads)
- ✅ Glob for file structure analysis (no file reads)
- ✅ Progressive disclosure (critical → high → medium → low)
- ✅ Focus area flags (--performance, --security, --maintainability, --scalability)
- ✅ Default to git diff scope (changed files + dependencies)
- ✅ Caching issue patterns and hotspot analysis
- ✅ Early exit when no high-risk patterns found - saves 85%
- **Expected tokens:** 1,200-3,500 (vs. 3,000-5,000 unoptimized) - **50-60% reduction**
- **Optimization status:** ✅ Optimized (Phase 2 Batch 3B, 2026-01-26)

**Caching Behavior:**
- Cache location: `.claude/cache/predict-issues/`
- Caches: Known issue patterns, complexity hotspots, dependency risks
- Cache validity: Until codebase structure changes significantly
- Shared with: `/review`, `/security-scan`, `/complexity-reduce` skills

**Usage:**
- `predict-issues` - Analyze changed files (default, 1,200-2,000 tokens)
- `predict-issues all` - Full codebase analysis (3,000-3,500 tokens)
- `predict-issues --performance` - Performance issues only (800-1,500 tokens)
- `predict-issues --security` - Security risks only (800-1,500 tokens)
- `predict-issues --maintainability` - Code quality issues (1,000-2,000 tokens)

## Token Optimization Strategy

### Efficiency Patterns (60% Reduction: 4,000-6,000 → 1,500-2,500 tokens)

**Phase 1: Intelligent Scoping (Saves 40-50%)**
```bash
# 1. Default to git diff scope (changed files only)
git diff --name-only HEAD

# 2. Early exit for low-risk changes
# Skip analysis if only: docs/, tests/, README, config without logic
# Saves 85% tokens when no actionable issues

# 3. Focus area flags reduce scope
--performance    # Only performance patterns (50% reduction)
--security       # Only security risks (50% reduction)
--maintainability # Only code quality (40% reduction)
--scalability    # Only scaling issues (50% reduction)
```

**Phase 2: Pattern-Based Detection with Grep (Saves 30-40%)**
```bash
# Performance issue patterns
Grep "for.*for.*for" --output_mode content  # Nested loops (O(n³))
Grep "\.map\(.*\.filter\(.*\.map\(" --output_mode content  # Chained array ops
Grep "SELECT.*FROM.*WHERE.*IN.*SELECT" --output_mode content  # N+1 queries
Grep "setTimeout|setInterval" --output_mode content  # Potential memory leaks
Grep "new.*\[\].*push" --output_mode content  # Array pre-allocation issues

# Security risk patterns
Grep "eval\(|new Function\(" --output_mode content  # Code injection risks
Grep "innerHTML|dangerouslySetInnerHTML" --output_mode content  # XSS risks
Grep "Math\.random|Date\.now" --output_mode content  # Weak randomness
Grep "http://|process\.env\." --output_mode content  # Config issues

# Maintainability patterns
Grep "function.*\{$" -A 100 --output_mode content  # Long functions
Grep "if.*\{.*if.*\{.*if.*\{" --output_mode content  # Deep nesting
Grep "any|unknown" --type ts --output_mode content  # Type safety gaps
Grep "TODO|FIXME|HACK|XXX" --output_mode content  # Technical debt markers

# Scalability patterns
Grep "hardcoded|localhost|127\.0\.0\.1" --output_mode content  # Env coupling
Grep "sleep\(|Thread\.sleep|time\.sleep" --output_mode content  # Blocking calls
Grep "global|window\.|process\." --output_mode content  # Global state
Grep ".*\.length > [0-9]{3}" --output_mode content  # Hardcoded limits
```

**Phase 3: Git History Analysis (Saves 20-30%)**
```bash
# Identify hotspot files (frequent bugs = future bugs)
git log --format="%H" --all -- "*.{js,ts,py,go,java}" | head -100 | \
  xargs -I {} git diff-tree --no-commit-id --name-only -r {} | \
  sort | uniq -c | sort -rn | head -20

# Files with most recent bug fixes (analyze commit messages)
git log --grep="fix\|bug\|issue" --format="%H" -n 50 | \
  xargs -I {} git diff-tree --no-commit-id --name-only -r {} | \
  sort | uniq -c | sort -rn | head -10

# Large files growing rapidly (complexity accumulation)
git log --format="%H" --all -n 100 | \
  xargs -I {} sh -c 'git show {}:path 2>/dev/null | wc -l' | \
  awk '{if ($1 > 500) print}'
```

**Phase 4: Complexity Metrics Caching (Saves 20-30%)**
```bash
# Cache cyclomatic complexity scores
# Run once, cache results in .claude/cache/predict-issues/complexity.json
# Format: {"file": "path/to/file.js", "score": 45, "functions": [...]}

# Use Bash-based metrics (fast, no file reads)
Bash: "find . -name '*.js' -exec sh -c 'echo \"{} $(grep -c \"if\\|for\\|while\\|case\" {})\"' \;"

# Cache dependency risk scores
# npm: check package.json age, deprecated packages
# python: check requirements.txt for CVEs
# go: check go.mod for outdated versions
```

**Phase 5: Template-Based Issue Patterns (Saves 15-25%)**
```javascript
// Memory leak patterns
const MEMORY_LEAK_PATTERNS = [
  "addEventListener without removeEventListener",
  "setInterval without clearInterval",
  "DOM references in closures",
  "Growing global arrays/objects",
  "Unclosed database connections",
  "Event emitter listener accumulation"
];

// Race condition patterns
const RACE_CONDITION_PATTERNS = [
  "Async operations without await/then",
  "Shared state mutation in parallel code",
  "File operations without locks",
  "Multiple async setState calls",
  "Promise.all without error handling"
];

// Scalability anti-patterns
const SCALABILITY_ANTIPATTERNS = [
  "In-memory caching without limits",
  "Synchronous file I/O in request handlers",
  "Database queries in loops",
  "Missing pagination on large collections",
  "Unbounded thread pool creation"
];

// Detection: Grep for pattern keywords, Read only matching files
```

**Phase 6: Progressive Disclosure (Saves 10-20%)**
```plaintext
1. Quick scan (Grep patterns only) - 500-800 tokens
   ├─ Critical: Memory leaks, security holes, data loss risks
   ├─ High: Performance bottlenecks, scaling issues
   └─ Exit early if no critical/high issues found

2. Detailed analysis (Read specific files) - 1,000-1,800 tokens
   ├─ Only files with pattern matches
   ├─ Only functions exceeding complexity thresholds
   └─ Only hotspot files from git history

3. Full report (comprehensive) - 1,500-2,500 tokens
   ├─ Include medium/low priority issues
   ├─ Trend analysis and predictions
   └─ Detailed remediation plans
```

### Optimization Implementation

**Default Behavior (Git Diff Scope)**
```bash
# 1. Get changed files since last commit
git diff --name-only HEAD

# 2. Get staged files
git diff --cached --name-only

# 3. Filter to source code (skip docs, configs)
# 4. Run pattern detection with Grep (no file reads)
# 5. Read only files with detected patterns
# 6. Early exit if no high-risk issues

# Result: 1,200-2,000 tokens (vs 4,000-6,000 full analysis)
```

**Focus Area Optimization**
```bash
# Performance focus (--performance)
- Grep: nested loops, array chaining, inefficient algorithms
- Git: files with performance-related commits
- Read: Only functions with O(n²)+ complexity
- Tokens: 800-1,500 (62% savings)

# Security focus (--security)
- Grep: eval, innerHTML, weak crypto, exposed secrets
- Static patterns: No git/Read needed for many checks
- Read: Only files with detected vulnerabilities
- Tokens: 800-1,500 (62% savings)

# Maintainability focus (--maintainability)
- Bash: Line counts, complexity scores (cached)
- Grep: Deep nesting, long functions, TODO markers
- Read: Only high-complexity hotspots
- Tokens: 1,000-2,000 (50% savings)
```

**Caching Strategy**
```json
// .claude/cache/predict-issues/analysis-cache.json
{
  "lastAnalysis": "2026-01-27T10:30:00Z",
  "hotspotFiles": [
    {"path": "src/auth/login.ts", "bugCount": 12, "changeFrequency": 45},
    {"path": "src/api/users.ts", "bugCount": 8, "changeFrequency": 32}
  ],
  "complexityScores": {
    "src/auth/login.ts": 42,
    "src/api/users.ts": 38
  },
  "knownPatterns": {
    "performance": ["src/data/processor.ts:145", "src/utils/query.ts:67"],
    "security": ["src/api/upload.ts:89"],
    "maintainability": ["src/legacy/old-handler.ts:*"]
  },
  "lastGitCommit": "a1b2c3d4e5f6",
  "analysisCount": 5
}
```

**Token Budget Allocation**
```plaintext
Quick Scan (Default):
├─ Git operations: 100-200 tokens
├─ Grep patterns: 400-600 tokens
├─ Analysis & output: 700-1,200 tokens
└─ Total: 1,200-2,000 tokens ✅

Detailed Analysis (Focus Area):
├─ Git operations: 100-200 tokens
├─ Grep patterns: 300-500 tokens
├─ Read files: 400-800 tokens
├─ Analysis & output: 200-500 tokens
└─ Total: 1,000-2,000 tokens ✅

Full Analysis (--all):
├─ Git history: 200-300 tokens
├─ Grep patterns: 600-800 tokens
├─ Read hotspots: 400-800 tokens
├─ Complexity analysis: 200-400 tokens
├─ Report generation: 200-400 tokens
└─ Total: 1,600-2,700 tokens ✅
```

### Real-World Examples

**Example 1: Performance Issue Detection**
```bash
# Traditional approach (4,000 tokens)
Read all .js/.ts files → Analyze all code → Report issues

# Optimized approach (1,200 tokens) - 70% savings
1. git diff --name-only HEAD  # 50 tokens
2. Grep nested loops in changed files  # 400 tokens
3. Read only files with O(n²)+ patterns  # 500 tokens
4. Generate focused report  # 250 tokens
```

**Example 2: Security Risk Scan**
```bash
# Traditional approach (5,000 tokens)
Read all source files → Security analysis → Detailed report

# Optimized approach (1,200 tokens) - 76% savings
1. Grep eval/innerHTML/crypto patterns  # 500 tokens
2. Grep exposed secrets/API keys  # 300 tokens
3. Read only vulnerable files  # 300 tokens
4. Generate risk report  # 100 tokens
```

**Example 3: Low-Risk Changes (Early Exit)**
```bash
# Changed files: README.md, docs/api.md, package.json (version bump)
1. git diff --name-only HEAD  # 50 tokens
2. Detect no source code changes  # 100 tokens
3. Skip analysis, return "No high-risk changes"  # 50 tokens
# Total: 200 tokens (vs 4,000) - 95% savings ✅
```

Based on this analysis framework, I'll use native tools for comprehensive analysis:
- **Grep tool** to search for problematic patterns (no file reads)
- **Glob tool** to analyze file structures and growth (no file reads)
- **Read tool** to examine complex functions and hotspots (only after Grep identifies specific risks)

I'll examine:
- Code complexity trends and potential hotspots
- Performance bottleneck patterns forming
- Maintenance difficulty indicators
- Architecture stress points and scaling issues
- Error handling gaps

For each prediction, I'll:
- Show specific code locations with file references
- Explain why it's likely to cause future issues
- Estimate potential timeline and impact
- Suggest preventive measures with priority levels

When I find multiple issues, I'll create a todo list for systematic review and prioritization.

Analysis areas:
- Functions approaching complexity thresholds
- Files with high change frequency (potential hotspots)
- Dependencies with known issues or update requirements
- Performance patterns that don't scale
- Code duplication leading to maintenance issues

After analysis, I'll ask: "How would you like to track these predictions?"
- Create todos: I'll add items to track resolution progress
- Create GitHub issues: I'll generate properly formatted issues with details
- Summary only: I'll provide actionable report without task creation

**Important**: I will NEVER:
- Add "Created by Claude" or any AI attribution to issues
- Include "Generated with Claude Code" in descriptions
- Modify repository settings or permissions
- Add any AI/assistant signatures or watermarks

Predictions will include:
- Risk level assessment (Critical/High/Medium/Low)
- Estimated timeline for potential issues
- Specific remediation recommendations
- Impact assessment on project goals

This helps prevent problems before they impact your project, saving time and maintaining code quality proactively.