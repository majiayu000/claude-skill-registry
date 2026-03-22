---
name: code-analysis
description: This skill should be used when analyzing ACE Engine (OpenHarmony ArkUI) code including components, patterns, models, and properties. Supports multiple analysis levels: quick diagnosis (5-15 min), comprehensive analysis (30-45 min), and deep audit (1-2 hr). Covers architecture review, bug analysis, performance optimization, component design guidance, API review, and test coverage analysis. Emphasizes code-first principle - always verify with actual code using Read/Grep tools and provide file:line references.
version: 1.0.0
---

# ACE Engine Code Analysis Skill

Comprehensive code analysis guidelines for ACE Engine (OpenHarmony ArkUI) development.

## Core Principles

### 1. Code-First Principle (代码为准原则)

**Always verify with actual source code - never guess or fabricate.**

- ✅ Use Read/Grep tools to locate and read actual source code
- ✅ Reference complete file paths with line numbers (e.g., `frameworks/core/xxx/yyy.cpp:123`)
- ✅ Provide source location for all code snippets
- ❌ Never assume functionality without reading source code
- ❌ Never write hypothetical code without verification

**Example of correct code reference**:
```markdown
### Text Pattern Initialization
Source: `OpenHarmony/foundation/arkui/ace_engine/frameworks/core/components_ng/pattern/text/text_pattern.cpp:123-145`

```cpp
void TextPattern::OnModifyDone()
{
    // Actual implementation from source
    auto host = GetHost();
    if (host) {
        host->MarkDirtyNode(PROPERTY_PATTERN_RENDER_CONTEXT);
    }
}
```
```

### 2. Evidence-Based Analysis

All conclusions must be supported by:
- **Code location references** (`file:line` format)
- **Actual code snippets** (not fabricated)
- **Verification with Read/Grep tools**

### 3. Structured Output

Analysis results should include:
- **Core findings** (with code references)
- **Potential issues** (grouped by severity)
- **Actionable recommendations** (specific and executable)
- **Visual diagrams** (class hierarchy, call flows, data flow)

## Analysis Levels

### Level 1: Quick Analysis (基础版本快速分析)

**Time**: 5-15 minutes
**Use cases**: Quick problem diagnosis, simple code understanding, initial assessment

**Analysis Requirements**:
1. Read specific file path source code
2. Focus on specific class/function/feature
3. Analyze specific problem point (e.g., memory management, performance, lifecycle, error handling)
4. Provide conclusions based on actual code with file:line references

**Output Format**:
- Core findings (with code references)
- Potential issues (if any)
- Improvement suggestions (if any)

### Level 2: Comprehensive Analysis (完整版本深度分析)

**Time**: 30-45 minutes
**Use cases**: Code review, architecture refactoring, comprehensive technical assessment

**Analysis Steps**:

#### Step 1: Code Location & Verification
1. Use Glob/Grep to locate relevant source files
2. Verify file path existence
3. Confirm code version (current branch)

#### Step 2: Structure Analysis
1. Read core file contents
2. Draw class inheritance diagrams (if applicable)
3. Identify key function call chains
4. Mark important code locations (file:line format)

#### Step 3: Deep Analysis

**Architecture Design**:
- [ ] Pattern/Model/Property separation
- [ ] NG architecture compliance
- [ ] Component lifecycle completeness

**Memory Safety**:
- [ ] Smart pointer usage (AceType::RefPtr)
- [ ] Raw pointer usage justification
- [ ] Memory leak risks

**Performance**:
- [ ] Unnecessary copying
- [ ] Loop/recursion complexity
- [ ] Layout/render performance impact

**Error Handling**:
- [ ] Null pointer checks
- [ ] Boundary condition handling
- [ ] Exception handling

**Test Coverage**:
- [ ] Find corresponding test files
- [ ] Unit test coverage
- [ ] Critical path testing

#### Step 4: Cross-Validation
1. Compare with knowledge base documents (if available)
2. Check related component implementation patterns
3. Verify API usage compliance

**Output Requirements**:

**Must Include**:
1. **Code location references**: All conclusions must cite `file:line`
2. **Actual code snippets**: Key implementation excerpts
3. **Visual diagrams**:
   - Class inheritance relationships
   - Function call flows
   - Data flow diagrams
4. **Issue list**: Problems grouped by severity
5. **Improvement recommendations**: Specific actionable suggestions

**Prohibited**:
- ❌ No guessing or fabricating code
- ❌ No conclusions without code references
- ❌ No skipping error handling analysis
- ❌ No skipping actual code verification

### Level 3: Deep Audit (深度审计)

**Time**: 1-2 hours
**Use cases**: Full audit with test verification and performance analysis

Includes all Level 2 analysis plus:
- Test execution and verification
- Performance benchmarking
- Security vulnerability assessment
- Documentation accuracy review

## Scenario-Specific Analysis

### Bug Analysis (Bug分析专用)

**Use cases**: Problem troubleshooting, error location, defect fixing

**Analysis Requirements**:
1. Locate problem code (exact line number)
2. Analyze root cause
3. Check related code for similar issues
4. Provide fix solution (with code example)

**Analysis Method**:
1. Use Grep to search related error messages/exceptions
2. Trace function call chains
3. Check log output locations
4. Analyze boundary condition handling

**Output Format**:
```
**Bug Location**: [file.cpp:line]
**Root Cause**: [Specific cause analysis]
**Impact Scope**: [Impact assessment]
**Fix Recommendation**:
```cpp
// Fix code example
[Specific code]
```
**Verification Method**: [How to verify fix]
```

### Performance Optimization (性能优化专用)

**Use cases**: Performance bottleneck analysis, optimization design

**Analysis Targets**:
- [ ] Layout performance
- [ ] Render performance
- [ ] Memory usage
- [ ] CPU usage
- [ ] Startup time

**Analysis Method**:
1. Find performance-related code (loops, recursion, frequent calls)
2. Identify performance bottleneck points
3. Check for caching mechanisms
4. Analyze algorithm complexity

**Optimization Format**:
```
**Problem Point**: [file:line]
**Current Complexity**: O(n)
**Optimization Solution**: [Specific solution]
**Expected Benefit**: [Performance improvement estimate]
```

### Component Design (新组件开发专用)

**Use cases**: Component design guidance, development compliance check

**Design Requirements**:
1. Reference existing component implementation patterns
2. Follow NG architecture specifications
3. Complete lifecycle management
4. Comprehensive error handling

**Design Checklist**:
- [ ] Pattern layer design
- [ ] Model interface definition
- [ ] Layout Property
- [ ] Paint Property
- [ ] Event Hub
- [ ] Test cases

**Verification Standards**:
1. Code compiles successfully
2. Unit test coverage > 80%
3. Complies with ArkUI API specifications
4. Performance tests pass

### API Review (API审查专用)

**Use cases**: API design review, interface specification check

**Review Dimensions**:
- [ ] API naming compliance
- [ ] Parameter design rationality
- [ ] Return value type appropriateness
- [ ] TypeScript type definitions provided
- [ ] Complete documentation (JSDoc)
- [ ] Usage examples provided

**Checklist**:
1. Find API definition files (.d.ts)
2. Check C++ implementation consistency with TS definition
3. Verify consistency with existing APIs
4. Check backward compatibility

### Test Analysis (测试分析专用)

**Use cases**: Test coverage analysis, test case design

**Test Status**:
- [ ] Existing unit test files
- [ ] Test case count
- [ ] Covered critical paths
- [ ] Missing test scenarios

**Analysis Method**:
1. Find test files (*_test.cpp)
2. Analyze test-covered functions
3. Identify untested branches
4. Check boundary condition testing

**Test Recommendations**:
```
**Missing Scenarios**:
- [ ] Scenario 1: [Specific description]
- [ ] Scenario 2: [Specific description]

**Test Case Suggestions**:
```cpp
TEST(ComponentName, TestScenario) {
    // Test code
}
```
```

## File Search Best Practices

### Using Glob
```bash
# Find files by pattern
Glob: "**/*pattern.cpp"

# Find all test files
Glob: "**/*_test.cpp"

# Find specific component files
Glob: "**/text/**/*.cpp"
```

### Using Grep
```bash
# Search code by pattern
Grep: "OnModifyDone" --type cpp

# Search with context
Grep: "class TextPattern" --type cpp -A 10

# Search in specific directory
Grep: "RefPtr" frameworks/core/components_ng/pattern/text/

# Case-insensitive search
Grep: "border.*radius" --type cpp -i
```

### Code Verification
```bash
# Verify file exists
Read: frameworks/core/components_ng/pattern/text/text_pattern.cpp

# View specific lines
Read: file.cpp (offset: 100, limit: 50)
```

## Quality Checklist

Before submitting analysis results, verify:

- [ ] All code references cite `file:line`
- [ ] All conclusions supported by actual code
- [ ] No speculative words like "推测", "可能" without explicit labeling
- [ ] Specific actionable improvement recommendations provided
- [ ] Visual diagrams included (if applicable)
- [ ] Cross-validated with knowledge base documents
- [ ] Related component implementation patterns checked
- [ ] Used Read/Grep tools for verification (not assumptions)

## Tool Commands for Analysis

### Compilation Testing
```bash
# Build check
./build.sh --product-name rk3568 --build-target ace_engine

# Build specific component
./build.sh --product-name rk3568 --build-target //arkui/ace_engine/frameworks/core/components_ng/pattern/text:text_pattern
```

### Running Tests
```bash
# Run specific test
./out/rk3568/tests/ace_engine/unittest/components_ng/text/text_pattern_test

# Run with filter
./out/rk3568/tests/ace_engine/unittest/components_ng/text/text_pattern_test --gtest_filter=TextPatternTest.OnModifyDone
```

## Knowledge Base Integration

**Always check for relevant knowledge base documents** in `docs/` before analysis:
- Component-specific knowledge bases (`docs/pattern/*/`)
- Architecture documentation (`docs/architecture/`)
- Best practices (`docs/best_practices/`)

**Cross-reference with actual code** using file paths and line numbers cited in knowledge base documents.

## Analysis Template Selection Guide

| Task Type | Recommended Template | Time |
|-----------|---------------------|------|
| Quick problem diagnosis | Level 1: Quick Analysis | 5-15 min |
| Code review/refactoring | Level 2: Comprehensive | 30-45 min |
| Bug fixing | Bug Analysis | 15-30 min |
| Performance optimization | Performance Analysis | 30-60 min |
| New component development | Component Design | Design phase |
| API design review | API Review | 15-30 min |
| Test supplementation | Test Analysis | 20-40 min |
| Full audit | Level 3: Deep Audit | 1-2 hr |

## Reference Implementations

See working examples in knowledge bases:
- `docs/pattern/text/Text_Knowledge_Base_CN.md` - Text component analysis
- `docs/pattern/menu/Menu_Knowledge_Base_CN.md` - Menu component analysis
- `docs/pattern/grid/Grid_Knowledge_Base_CN.md` - Grid component analysis
