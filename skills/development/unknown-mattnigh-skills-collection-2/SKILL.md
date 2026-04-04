---
name: Multi-Language Project Analysis with PMAT
description: |
  Analyzes polyglot codebases with multiple programming languages using PMAT
  (Pragmatic AI Labs MCP Agent Toolkit). Use this skill when:
  - Working with projects containing multiple programming languages
  - Assessing cross-language integration patterns and quality
  - Understanding language distribution and architectural boundaries
  - Comparing quality metrics across language ecosystems
  - Identifying language-specific best practices violations
  Supports 25+ languages including Rust, Python, TypeScript, JavaScript, Go, C++, Java,
  Ruby, PHP, Swift, Kotlin, C, C#, Scala, Haskell, Elixir, Clojure, Dart, Lua, R, and more.
  Provides unified quality assessment across heterogeneous codebases.
allowed-tools: Bash, Read, Write, Glob, Grep
---

# PMAT Multi-Language Project Analysis Skill

You are an expert at analyzing polyglot codebases and assessing cross-language architecture using PMAT (Pragmatic AI Labs MCP Agent Toolkit).

## When to Activate

This skill should automatically activate when:
1. User mentions "multi-language", "polyglot", or "mixed languages"
2. Project contains 2+ programming languages
3. User asks about language distribution or architecture boundaries
4. Comparing quality across different language components
5. Assessing cross-language integration patterns

## Core Concepts: Polyglot Architecture

**Definition**: Software system using multiple programming languages, each chosen for specific strengths

**Common Patterns**:
- **Microservices**: Different services in different languages
- **Frontend/Backend Split**: JavaScript/TypeScript frontend, Python/Go backend
- **Native Extensions**: C/C++ performance-critical code with Python/Ruby bindings
- **Domain-Specific**: R/Python for data science, Rust for systems, SQL for data

**Challenges**:
- Consistent quality standards across languages
- Cross-language API contracts
- Build system complexity
- Team expertise distribution

## Available PMAT Commands

### 1. Language Detection and Distribution
```bash
pmat analyze languages --path . --output language_stats.json
```
**Output**: Language percentages, file counts, line counts by language

### 2. Multi-Language Quality Analysis
```bash
pmat analyze quality --path . --multi-language --output quality_by_lang.json
```
**Output**: Quality metrics aggregated per language

### 3. Cross-Language Complexity Comparison
```bash
pmat analyze complexity --path . --group-by language --output complexity_by_lang.json
```
**Output**: Complexity distributions for each language

### 4. Language-Specific Deep Context
```bash
pmat context --path . --language rust --output rust_context.md
pmat context --path . --language python --output python_context.md
```
**Output**: Separate deep context reports per language

### 5. Polyglot Architecture Visualization
```bash
pmat visualize-architecture --path . --output architecture_map.svg
```
**Output**: Visual representation of language boundaries and dependencies

## Usage Workflow

### Step 1: Language Discovery
Understand language composition:

```bash
# Detect all languages in project
pmat analyze languages --path . --output languages.json

# Review distribution
cat languages.json | jq '.distribution'
```

**Example Output**:
```json
{
  "distribution": {
    "Rust": {
      "files": 145,
      "lines": 45678,
      "percentage": 62.3,
      "primary": true
    },
    "TypeScript": {
      "files": 89,
      "lines": 23456,
      "percentage": 32.0,
      "primary": false
    },
    "Python": {
      "files": 23,
      "lines": 4123,
      "percentage": 5.6,
      "primary": false
    },
    "Shell": {
      "files": 5,
      "lines": 89,
      "percentage": 0.1,
      "primary": false
    }
  }
}
```

### Step 2: Quality Assessment by Language
Compare quality metrics across languages:

```bash
# Analyze quality for each language
pmat analyze quality --path . --multi-language --output quality_multi.json

# Generate comparison report
pmat compare-languages --input quality_multi.json --output language_comparison.md
```

### Step 3: Identify Integration Boundaries
Map cross-language interactions:

```bash
# Detect cross-language calls (FFI, API, etc.)
pmat analyze cross-language-refs --path . --output integration_points.json

# Review integration patterns
cat integration_points.json | jq '.references[] | select(.type == "ffi")'
```

### Step 4: Language-Specific Recommendations
Generate tailored improvement suggestions:

```bash
# Get language-specific recommendations
pmat analyze quality --path . --recommendations --group-by language \
    --output recommendations_by_lang.md
```

## Example Workflows

### Example 1: Polyglot Architecture Assessment

```bash
# User: "Can you assess the architecture of this multi-language project?"

# Step 1: Detect languages
pmat analyze languages --path . --output lang_dist.json

# Output:
# {
#   "total_languages": 4,
#   "primary_language": "Rust",
#   "distribution": {
#     "Rust": {"percentage": 62.3, "role": "Core backend services"},
#     "TypeScript": {"percentage": 32.0, "role": "Web frontend"},
#     "Python": {"percentage": 5.6, "role": "Data analysis scripts"},
#     "Shell": {"percentage": 0.1, "role": "Build automation"}
#   }
# }

# Step 2: Analyze architecture boundaries
pmat context --path . --format llm-optimized --output full_context.md

# Step 3: Identify integration patterns
grep -E "(extern|FFI|API|RPC)" full_context.md > integration_patterns.txt

# Step 4: Present assessment
# "This is a well-structured polyglot architecture:
#
# **Language Distribution**:
# - Rust (62.3%): Core backend services, business logic
# - TypeScript (32.0%): Web frontend (React/Next.js)
# - Python (5.6%): Data analysis and ML scripts
# - Shell (0.1%): Build/deployment automation
#
# **Architecture Pattern**: Microservices with clear boundaries
# - Rust services expose REST APIs
# - TypeScript frontend consumes APIs
# - Python scripts operate independently
#
# **Integration Points**:
# 1. REST API contracts (Rust ↔ TypeScript)
# 2. Data pipeline (Python → Rust database)
# 3. Build system (Shell orchestrates all)
#
# **Quality Assessment**:
# - Rust: High quality (avg complexity: 8, maintainability: 82)
# - TypeScript: Good quality (avg complexity: 12, maintainability: 75)
# - Python: Medium quality (avg complexity: 15, maintainability: 68)
#
# **Recommendations**:
# 1. Reduce TypeScript complexity (target < 10)
# 2. Add type hints to Python scripts (improve maintainability)
# 3. Document API contracts in OpenAPI/Swagger
# 4. Consider consolidating Shell scripts into Makefile"
```

### Example 2: Language-Specific Quality Comparison

```bash
# User: "Compare code quality between Rust and Python components"

# Step 1: Analyze each language separately
pmat analyze quality --path src/rust/ --language rust --output rust_quality.json
pmat analyze quality --path scripts/python/ --language python --output python_quality.json

# Step 2: Compare metrics
pmat compare \
    --baseline rust_quality.json \
    --current python_quality.json \
    --output rust_vs_python.md

# Example output (rust_vs_python.md):
# # Rust vs Python Quality Comparison
#
# ## Complexity
# | Metric | Rust | Python | Winner |
# |--------|------|--------|--------|
# | Avg Cyclomatic | 8.2 | 14.6 | Rust (-43.8%) |
# | Avg Cognitive | 10.5 | 18.3 | Rust (-42.6%) |
# | Max Complexity | 23 | 45 | Rust (-48.9%) |
#
# ## Maintainability
# | Metric | Rust | Python | Winner |
# |--------|------|--------|--------|
# | Maintainability Index | 82.3 | 68.5 | Rust (+20.1%) |
# | Documentation Coverage | 78% | 45% | Rust (+73.3%) |
# | Test Coverage | 85% | 72% | Rust (+18.1%) |
#
# ## Technical Debt
# | Metric | Rust | Python | Winner |
# |--------|------|--------|--------|
# | TODO Count | 12 | 34 | Rust (-64.7%) |
# | FIXME Count | 5 | 18 | Rust (-72.2%) |
# | Total Debt Hours | 45 | 128 | Rust (-64.8%) |
#
# ## Insights
# - Rust code is significantly higher quality across all metrics
# - Python scripts show higher complexity and lower documentation
# - Rust's type system prevents many common defects
#
# ## Recommendations
# 1. Apply Rust quality standards to Python (add type hints, docstrings)
# 2. Refactor high-complexity Python functions (target < 15)
# 3. Increase Python test coverage to match Rust (target 85%)
# 4. Consider migrating performance-critical Python to Rust

# Step 3: Present summary
# "Rust components show 43% lower complexity and 20% better maintainability than Python.
# Python scripts have 3x more technical debt (128 vs 45 hours).
# Recommend: Add mypy type checking and improve Python documentation coverage."
```

### Example 3: Cross-Language Refactoring Strategy

```bash
# User: "We're considering migrating some Python code to Rust. Which parts should we migrate?"

# Step 1: Analyze Python performance bottlenecks
pmat analyze complexity --path scripts/python/ \
    --metrics complexity,churn \
    --output python_hotspots.json

# Step 2: Identify migration candidates
cat python_hotspots.json | jq '.files[] | select(.complexity > 20 or .churn > 10) | {file, complexity, churn, lines}'

# Example candidates:
# {
#   "file": "scripts/python/data_processor.py",
#   "complexity": 45,
#   "churn": 23,
#   "lines": 678
# }
# {
#   "file": "scripts/python/ml_inference.py",
#   "complexity": 38,
#   "churn": 15,
#   "lines": 456
# }

# Step 3: Estimate migration effort
# Using COCOMO model: effort = 2.5 * (KLOC)^1.05

# Step 4: Prioritize by ROI
# "Migration Recommendations (prioritized by ROI):
#
# **High Priority** (migrate first):
# 1. data_processor.py (678 LOC, complexity 45, churn 23)
#    - Estimated effort: 3 weeks
#    - Expected performance gain: 10-50x
#    - Risk: Medium (well-tested logic)
#    - ROI: High (performance-critical, frequently modified)
#
# 2. ml_inference.py (456 LOC, complexity 38, churn 15)
#    - Estimated effort: 2 weeks
#    - Expected performance gain: 5-20x
#    - Risk: Low (deterministic algorithms)
#    - ROI: High (latency-sensitive)
#
# **Medium Priority** (migrate later):
# 3. validation_engine.py (234 LOC, complexity 25, churn 8)
#    - ROI: Medium (moderate complexity, moderate churn)
#
# **Low Priority** (keep in Python):
# - Scripts with complexity < 15 and churn < 5
# - One-off data analysis scripts
# - Prototyping/experimental code
#
# **Migration Strategy**:
# 1. Start with ml_inference.py (lower risk, high impact)
# 2. Expose Rust implementation via PyO3 (Python bindings)
# 3. A/B test performance in production
# 4. Gradually migrate callers to native Rust API
# 5. Deprecate Python version after 2 sprints"
```

## Language-Specific Quality Thresholds

Different languages have different "acceptable" complexity ranges:

| Language | Cyclomatic Threshold | Cognitive Threshold | Rationale |
|----------|---------------------|---------------------|-----------|
| **Rust** | 10 | 15 | Strong type system reduces cognitive load |
| **Python** | 8 | 12 | Dynamic typing increases cognitive load |
| **TypeScript** | 10 | 15 | Type system helps, but looser than Rust |
| **JavaScript** | 8 | 12 | Dynamic, similar to Python |
| **Go** | 10 | 15 | Explicit error handling increases complexity |
| **C/C++** | 15 | 20 | Manual memory management complexity |
| **Java/C#** | 10 | 15 | OOP increases structural complexity |

**Adjust recommendations based on language context**.

## Cross-Language Best Practices

### 1. API Contract Definition
Use schema definition languages for cross-language APIs:
- **REST**: OpenAPI/Swagger
- **gRPC**: Protocol Buffers
- **GraphQL**: Schema Definition Language (SDL)

### 2. Consistent Code Style
Maintain consistent style across languages:
```bash
# Rust: rustfmt
pmat format --language rust --path src/rust/

# Python: black
pmat format --language python --path scripts/python/

# TypeScript: prettier
pmat format --language typescript --path frontend/
```

### 3. Unified Quality Gates
Apply language-agnostic quality standards:
```bash
# Set quality gates for all languages
pmat quality-gate \
    --max-complexity 15 \
    --min-maintainability 65 \
    --max-debt-hours 200 \
    --apply-to-all-languages
```

### 4. Language Detection Automation
Auto-detect primary language for tooling:
```bash
# Detect primary language
pmat detect-language --path . --output primary_lang.txt

# Use in CI/CD scripts
PRIMARY_LANG=$(cat primary_lang.txt)
if [ "$PRIMARY_LANG" = "Rust" ]; then
    cargo test
elif [ "$PRIMARY_LANG" = "Python" ]; then
    pytest
fi
```

## Polyglot Architecture Patterns

### Pattern 1: Microservices
**Structure**: Each service in optimal language
**Example**:
- User service: Go (concurrency)
- Payment service: Rust (safety)
- Analytics: Python (data science libs)
- Web UI: TypeScript (React ecosystem)

**PMAT Analysis**:
```bash
pmat analyze-microservices --path services/ --output microservices_quality.json
```

### Pattern 2: Monorepo
**Structure**: Multiple languages in single repository
**Example**:
- `backend/`: Rust
- `frontend/`: TypeScript
- `ml/`: Python
- `mobile/`: Kotlin, Swift

**PMAT Analysis**:
```bash
pmat context --path . --monorepo-mode --output monorepo_context.md
```

### Pattern 3: Native Extensions
**Structure**: Performance-critical code in C/C++/Rust, bindings to high-level languages
**Example**:
- Core: Rust (image processing)
- Bindings: PyO3 (Python), Neon (Node.js)

**PMAT Analysis**:
```bash
pmat analyze-ffi --path . --output ffi_safety_report.json
```

## Integration with Other PMAT Skills

**Workflow for Polyglot Projects**:
1. **pmat-multi-lang**: Understand language distribution ← This skill
2. **pmat-context**: Generate unified deep context
3. **pmat-quality**: Assess quality per language
4. **pmat-refactor**: Apply language-specific refactorings
5. **pmat-tech-debt**: Track debt across languages

## Reporting for Polyglot Projects

Generate comprehensive multi-language reports:
```bash
# Executive summary for polyglot projects
pmat generate-polyglot-report \
    --input language_stats.json \
    --format executive \
    --output POLYGLOT_ARCHITECTURE_REPORT.md
```

**Report Sections**:
1. **Language Distribution**: Percentages, file counts, roles
2. **Quality Comparison**: Metrics by language
3. **Integration Patterns**: Cross-language dependencies
4. **Recommendations**: Migration, consolidation, standardization strategies

## Common Multi-Language Challenges

### Challenge 1: Inconsistent Quality Standards
**Problem**: Different teams apply different quality bars
**Solution**: Use PMAT to enforce unified quality gates

### Challenge 2: Build System Complexity
**Problem**: Multiple build tools (cargo, npm, pip, gradle)
**Solution**: Orchestrate with Makefile or Bazel

### Challenge 3: Dependency Management
**Problem**: Language-specific package managers
**Solution**: Centralized dependency scanning with `pmat audit-deps`

### Challenge 4: Code Duplication Across Languages
**Problem**: Business logic duplicated in different languages
**Solution**: Identify duplication with `pmat analyze duplication --cross-language`

## Performance Optimization by Language

**Typical Performance Characteristics**:
- **Rust, C, C++**: Fastest (compiled, zero-cost abstractions)
- **Go**: Fast (compiled, GC overhead minimal)
- **Java, C#**: Fast (JIT optimization)
- **TypeScript, JavaScript**: Moderate (JIT, V8 optimization)
- **Python, Ruby**: Slower (interpreted, dynamic)

**Migration Strategy**:
```bash
# Identify performance bottlenecks
pmat profile --path . --output perf_bottlenecks.json

# Recommend language for hot paths
# "Consider migrating data_processor.py (Python) to Rust for 10-50x speedup"
```

## Limitations

- **Language Coverage**: PMAT supports 25+ languages, but not all (e.g., COBOL, Fortran limited)
- **Cross-Language Analysis**: Some patterns (e.g., FFI safety) require manual review
- **Build System Integration**: May need language-specific tooling for full CI/CD
- **Team Expertise**: Quality recommendations assume team proficiency in target languages

## When NOT to Use This Skill

- **Single-Language Projects**: Use language-specific skills instead
- **Prototypes**: Multi-language analysis adds overhead for throwaway code
- **Non-Code Polyglot**: HTML/CSS/JSON are configuration, not programming languages

## Scientific Foundation

Multi-language analysis based on:
1. **Software Architecture Metrics** (Chidamber & Kemerer, 1994)
2. **Polyglot Programming** (Ford et al., 2014)
3. **Cross-Language Static Analysis** (Livshits & Lam, 2005)
4. **Monorepo Best Practices** (Google Engineering, 2016)

## Version Requirements

- **Minimum**: PMAT v2.170.0
- **Recommended**: Latest version for best multi-language support
- **Check version**: `pmat --version`

---

**Remember**: Polyglot architecture is a powerful tool when used intentionally. Choose each language for its strengths, maintain consistent quality standards, and use PMAT to ensure architectural boundaries remain clear and maintainable.
