---
name: when-detecting-fake-code-use-theater-detection
type: testing-quality
description: |
  Detects non-functional "theater" code that appears complete but doesn't actually work.
  Use this skill to identify code that looks correct in static analysis but fails during execution,
  preventing fake implementations from reaching production. Scans for suspicious patterns,
  validates actual functionality, and reports findings with recommendations.
agents:
  - code-analyzer
  - reviewer
  - tester
phases: 5
memory_pattern: "testing/theater-detection/phase-{N}/{agent}/{deliverable}"
scripts:
  - pre-task
  - codebase-scan
  - pattern-analysis
  - execution-validation
  - post-task
hooks:
  pre: npx claude-flow hooks pre-task --description "Theater code detection scan"
  post: npx claude-flow hooks post-task --task-id "theater-detection"
---

# Theater Code Detection

## When to Use This Skill

**Trigger Conditions:**
- Before merging AI-generated code into main branch
- When code review reveals suspiciously complete implementations
- After detecting inconsistencies between documentation and behavior
- As pre-deployment quality gate for critical systems
- When integrating third-party or unfamiliar code
- During security audits to identify fake security measures

**Situations Requiring Theater Detection:**
- Code that compiles but doesn't execute meaningful logic
- Functions with proper signatures but no-op implementations
- Tests that always pass regardless of code changes
- Security checks that can be bypassed trivially
- Error handling that catches but doesn't handle errors
- Mock implementations accidentally left in production code

## Overview

Theater code is code that "performs" correctness without delivering actual functionality. It passes static analysis, looks structurally sound, and may even have tests—but fails to implement the intended behavior. This skill systematically identifies theater code through pattern recognition, execution analysis, and behavioral validation.

The detection process scans codebases for suspicious patterns (empty catch blocks, no-op functions, always-passing tests), analyzes implementations for meaningful logic, executes code to validate actual behavior, and reports findings with actionable recommendations for remediation.

## Phase 1: Scan Codebase (Parallel)

**Agents**: code-analyzer (lead), reviewer (validation)
**Duration**: 10-15 minutes

**Scripts**:
```bash
# Initialize phase
npx claude-flow hooks pre-task --description "Phase 1: Scan Codebase for Theater Patterns"
npx claude-flow swarm init --topology mesh --max-agents 2

# Spawn agents
npx claude-flow agent spawn --type code-analyzer --capabilities "pattern-matching,ast-analysis,static-analysis"
npx claude-flow agent spawn --type reviewer --capabilities "code-quality,suspicious-pattern-detection"

# Memory coordination - define scan parameters
npx claude-flow memory store --key "testing/theater-detection/phase-1/analyzer/scan-config" --value '{"patterns":["empty-catch","no-op-function","always-pass-test"],"severity":"high"}'

# Execute phase work
# 1. Scan for empty catch blocks
echo "Scanning for empty error handlers..."
grep -r "catch\s*(\w*)\s*{\s*}" --include="*.js" --include="*.ts" . > empty-catches.txt || true

# 2. Scan for no-op functions
grep -r "function\s+\w+.*{\s*return\s*[;}]" --include="*.js" --include="*.ts" . > noop-functions.txt || true

# 3. Scan for always-passing tests
grep -r "expect(true).toBe(true)" --include="*.test.js" --include="*.test.ts" . > always-pass-tests.txt || true

# 4. Scan for TODO/FIXME/HACK comments indicating incomplete work
grep -rn "TODO\|FIXME\|HACK" --include="*.js" --include="*.ts" . > incomplete-markers.txt || true

# 5. Scan for suspicious imports (unused, test doubles in production)
echo "Analyzing imports..."
cat > scan-imports.js << 'EOF'
const fs = require('fs');
const path = require('path');

function scanImports(dir) {
  const suspicious = [];

  function walkDir(currentPath) {
    const files = fs.readdirSync(currentPath);

    files.forEach(file => {
      const filePath = path.join(currentPath, file);
      const stat = fs.statSync(filePath);

      if (stat.isDirectory() && !file.includes('node_modules')) {
        walkDir(filePath);
      } else if (file.endsWith('.js') || file.endsWith('.ts')) {
        const content = fs.readFileSync(filePath, 'utf-8');

        // Check for mock imports in production code
        if (!filePath.includes('test') && content.includes("'mock'")) {
          suspicious.push({
            file: filePath,
            reason: 'Mock import in production code',
            line: content.split('\n').findIndex(l => l.includes("'mock'")) + 1
          });
        }

        // Check for unused imports
        const importMatch = content.match(/import\s+{([^}]+)}\s+from/g);
        if (importMatch) {
          importMatch.forEach(imp => {
            const symbols = imp.match(/{([^}]+)}/)[1].split(',').map(s => s.trim());
            symbols.forEach(symbol => {
              const usageCount = (content.match(new RegExp(`\\b${symbol}\\b`, 'g')) || []).length;
              if (usageCount === 1) { // Only appears in import
                suspicious.push({
                  file: filePath,
                  reason: `Unused import: ${symbol}`,
                  line: content.split('\n').findIndex(l => l.includes(symbol)) + 1
                });
              }
            });
          });
        }
      }
    });
  }

  walkDir(dir);
  return suspicious;
}

const results = scanImports(process.cwd());
fs.writeFileSync('suspicious-imports.json', JSON.stringify(results, null, 2));
EOF

node scan-imports.js

# 6. Compile scan results
cat > scan-summary.json << 'EOF'
{
  "empty_catches": 0,
  "noop_functions": 0,
  "always_pass_tests": 0,
  "incomplete_markers": 0,
  "suspicious_imports": 0,
  "total_issues": 0,
  "scanned_at": ""
}
EOF

# Update with actual counts
EMPTY_CATCHES=$(wc -l < empty-catches.txt)
NOOP_FUNCTIONS=$(wc -l < noop-functions.txt)
ALWAYS_PASS=$(wc -l < always-pass-tests.txt)
INCOMPLETE=$(wc -l < incomplete-markers.txt)
SUSPICIOUS_IMPORTS=$(jq 'length' suspicious-imports.json)
TOTAL=$((EMPTY_CATCHES + NOOP_FUNCTIONS + ALWAYS_PASS + INCOMPLETE + SUSPICIOUS_IMPORTS))

jq --arg ec "$EMPTY_CATCHES" \
   --arg nf "$NOOP_FUNCTIONS" \
   --arg ap "$ALWAYS_PASS" \
   --arg im "$INCOMPLETE" \
   --arg si "$SUSPICIOUS_IMPORTS" \
   --arg total "$TOTAL" \
   --arg ts "$(date -Iseconds)" \
   '.empty_catches = ($ec | tonumber) |
    .noop_functions = ($nf | tonumber) |
    .always_pass_tests = ($ap | tonumber) |
    .incomplete_markers = ($im | tonumber) |
    .suspicious_imports = ($si | tonumber) |
    .total_issues = ($total | tonumber) |
    .scanned_at = $ts' \
   scan-summary.json > scan-summary-updated.json

mv scan-summary-updated.json scan-summary.json

# Store results
npx claude-flow memory store --key "testing/theater-detection/phase-1/analyzer/scan-results" --value "$(cat scan-summary.json)"

# Complete phase
npx claude-flow hooks post-task --task-id "phase-1-scan"
```

**Memory Pattern**:
- Input: `testing/theater-detection/phase-0/user/codebase-path`
- Output: `testing/theater-detection/phase-1/analyzer/scan-results`
- Shared: `testing/theater-detection/shared/suspicious-files`

**Success Criteria**:
- [ ] Complete codebase scanned for all pattern types
- [ ] All suspicious patterns extracted and counted
- [ ] Scan results compiled into structured format
- [ ] No false positives (validated by reviewer agent)
- [ ] Results stored in memory for next phase

**Deliverables**:
- Scan summary JSON with issue counts
- Pattern-specific result files (empty-catches.txt, etc.)
- Suspicious imports analysis
- File-level issue mapping

## Phase 2: Analyze Implementation (Sequential)

**Agents**: code-analyzer (lead), reviewer (depth analysis)
**Duration**: 15-20 minutes

**Scripts**:
```bash
# Initialize phase
npx claude-flow hooks pre-task --description "Phase 2: Analyze Implementation Depth"
npx claude-flow swarm scale --target-agents 2

# Retrieve scan results
SCAN_RESULTS=$(npx claude-flow memory retrieve --key "testing/theater-detection/phase-1/analyzer/scan-results")

# Memory coordination
npx claude-flow memory store --key "testing/theater-detection/phase-2/analyzer/analysis-depth" --value '{"ast_parsing":true,"control_flow":true,"data_flow":true}'

# Execute phase work
# 1. Deep analysis of flagged files
echo "Performing deep implementation analysis..."

# Create analysis script
cat > analyze-implementation.js << 'EOF'
const fs = require('fs');
const path = require('path');

function analyzeImplementation(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const analysis = {
    file: filePath,
    theater_indicators: [],
    confidence_score: 0
  };

  // Check for meaningful logic
  const lines = content.split('\n').filter(l => l.trim() && !l.trim().startsWith('//'));
  const codeLines = lines.length;
  const commentLines = content.split('\n').filter(l => l.trim().startsWith('//')).length;

  if (commentLines > codeLines) {
    analysis.theater_indicators.push('More comments than code - possible placeholder');
  }

  // Check for actual computation
  const hasComputation = /[\+\-\*\/\%]/.test(content) ||
                         /if\s*\(/.test(content) ||
                         /for\s*\(/.test(content) ||
                         /while\s*\(/.test(content);

  if (!hasComputation && codeLines > 5) {
    analysis.theater_indicators.push('No computational logic despite size');
  }

  // Check for data transformation
  const hasTransformation = /\.map\(|\.filter\(|\.reduce\(/.test(content) ||
                            /Object\.(keys|values|entries)/.test(content);

  // Check function return values
  const returnMatches = content.match(/return\s+([^;]+);/g) || [];
  const trivialReturns = returnMatches.filter(r =>
    r.includes('return null') ||
    r.includes('return undefined') ||
    r.includes('return true') ||
    r.includes('return false') ||
    r.includes('return {}') ||
    r.includes('return []')
  );

  if (trivialReturns.length > returnMatches.length * 0.5) {
    analysis.theater_indicators.push('Majority of returns are trivial values');
  }

  // Check for error handling theater
  const catchBlocks = content.match(/catch\s*\([^)]*\)\s*{([^}]*)}/g) || [];
  const emptyCatches = catchBlocks.filter(c => {
    const body = c.match(/{([^}]*)}/)[1].trim();
    return body === '' || body === 'console.log' || body.includes('// TODO');
  });

  if (emptyCatches.length > 0) {
    analysis.theater_indicators.push(`${emptyCatches.length} empty catch blocks`);
  }

  // Calculate confidence score (0-100)
  analysis.confidence_score = Math.min(100, analysis.theater_indicators.length * 20);

  return analysis;
}

// Analyze all suspicious files
const suspiciousFiles = [
  ...fs.readFileSync('empty-catches.txt', 'utf-8').split('\n').filter(Boolean).map(l => l.split(':')[0]),
  ...fs.readFileSync('noop-functions.txt', 'utf-8').split('\n').filter(Boolean).map(l => l.split(':')[0])
];

const uniqueFiles = [...new Set(suspiciousFiles)];
const analyses = uniqueFiles.map(analyzeImplementation);

// Filter high-confidence theater code
const theaterCode = analyses.filter(a => a.confidence_score >= 40);

fs.writeFileSync('theater-analysis.json', JSON.stringify({
  total_analyzed: analyses.length,
  theater_detected: theaterCode.length,
  files: theaterCode
}, null, 2));

console.log(`Analyzed ${analyses.length} files, detected ${theaterCode.length} theater implementations`);
EOF

node analyze-implementation.js

# 2. Categorize by severity
cat > categorize-theater.js << 'EOF'
const fs = require('fs');
const analysis = JSON.parse(fs.readFileSync('theater-analysis.json', 'utf-8'));

const categories = {
  critical: [], // Code that doesn't work at all
  high: [],     // Code with major functionality gaps
  medium: [],   // Code with minor theater elements
  low: []       // Code with potential improvements
};

analysis.files.forEach(file => {
  const score = file.confidence_score;
  const indicators = file.theater_indicators;

  if (score >= 80 || indicators.some(i => i.includes('empty catch'))) {
    categories.critical.push(file);
  } else if (score >= 60) {
    categories.high.push(file);
  } else if (score >= 40) {
    categories.medium.push(file);
  } else {
    categories.low.push(file);
  }
});

fs.writeFileSync('theater-categories.json', JSON.stringify(categories, null, 2));

console.log('Critical:', categories.critical.length);
console.log('High:', categories.high.length);
console.log('Medium:', categories.medium.length);
console.log('Low:', categories.low.length);
EOF

node categorize-theater.js

# Store analysis results
npx claude-flow memory store --key "testing/theater-detection/phase-2/analyzer/theater-analysis" --value "$(cat theater-analysis.json)"
npx claude-flow memory store --key "testing/theater-detection/phase-2/analyzer/categories" --value "$(cat theater-categories.json)"

# Complete phase
npx claude-flow hooks post-task --task-id "phase-2-analyze"
```

**Memory Pattern**:
- Input: `testing/theater-detection/phase-1/analyzer/scan-results`
- Output: `testing/theater-detection/phase-2/analyzer/theater-analysis`
- Shared: `testing/theater-detection/shared/analysis-results`

**Success Criteria**:
- [ ] All flagged files analyzed for implementation depth
- [ ] Theater indicators identified with confidence scores
- [ ] Issues categorized by severity (critical, high, medium, low)
- [ ] Analysis results structured and comprehensive
- [ ] Results validated by reviewer agent

**Deliverables**:
- Theater analysis JSON with confidence scores
- Severity categorization (critical/high/medium/low)
- Per-file theater indicators list
- Implementation depth assessment

## Phase 3: Test Execution (Parallel)

**Agents**: tester (lead), code-analyzer (support)
**Duration**: 15-20 minutes

**Scripts**:
```bash
# Initialize phase
npx claude-flow hooks pre-task --description "Phase 3: Test Execution Validation"
npx claude-flow swarm scale --target-agents 2

# Retrieve analysis results
THEATER_ANALYSIS=$(npx claude-flow memory retrieve --key "testing/theater-detection/phase-2/analyzer/theater-analysis")

# Memory coordination
npx claude-flow memory store --key "testing/theater-detection/phase-3/tester/test-strategy" --value '{"execution_validation":true,"behavior_testing":true,"edge_case_testing":true}'

# Execute phase work
# 1. Create execution validation tests
echo "Creating execution validation tests..."

cat > execution-validator.test.js << 'EOF'
const fs = require('fs');
const theaterFiles = JSON.parse(fs.readFileSync('theater-analysis.json', 'utf-8')).files;

describe('Theater Code Execution Validation', () => {
  theaterFiles.forEach(fileData => {
    describe(`File: ${fileData.file}`, () => {
      test('should execute without errors', () => {
        try {
          const module = require(`./${fileData.file}`);
          expect(module).toBeDefined();
        } catch (error) {
          // If it can't even load, it's definitely theater
          expect(error).toBeUndefined();
        }
      });

      test('should have non-trivial exports', () => {
        try {
          const module = require(`./${fileData.file}`);
          const exports = Object.keys(module);

          // Check that exports exist and aren't just empty objects
          expect(exports.length).toBeGreaterThan(0);

          exports.forEach(exp => {
            if (typeof module[exp] === 'function') {
              // Check function isn't just "return null"
              const fnString = module[exp].toString();
              expect(fnString.length).toBeGreaterThan(50); // More than trivial implementation
            }
          });
        } catch (error) {
          // Module doesn't load properly
          fail(`Cannot validate exports: ${error.message}`);
        }
      });

      test('should produce meaningful output', () => {
        try {
          const module = require(`./${fileData.file}`);

          // For each exported function, call with sample input
          Object.keys(module).forEach(key => {
            if (typeof module[key] === 'function') {
              // Try calling with various inputs
              const results = [
                module[key](),
                module[key](null),
                module[key]({}),
                module[key]('test')
              ];

              // Check that results vary (not always same trivial value)
              const uniqueResults = new Set(results.map(r => JSON.stringify(r)));

              // If all results identical, likely theater
              if (uniqueResults.size === 1) {
                const result = results[0];
                // Exception: if result is complex object, might be OK
                if (result === null || result === undefined ||
                    result === true || result === false ||
                    (typeof result === 'object' && Object.keys(result).length === 0)) {
                  fail(`Function ${key} returns trivial constant`);
                }
              }
            }
          });
        } catch (error) {
          // Some execution occurred, which is better than nothing
          console.log(`Execution validation: ${error.message}`);
        }
      });
    });
  });
});
EOF

# 2. Run execution validation
npm test -- execution-validator.test.js --verbose > execution-validation.log 2>&1
EXECUTION_EXIT_CODE=$?

# 3. Analyze test results
cat > analyze-execution.js << 'EOF'
const fs = require('fs');
const log = fs.readFileSync('execution-validation.log', 'utf-8');

const results = {
  files_tested: 0,
  files_failed_load: 0,
  files_trivial_exports: 0,
  files_constant_output: 0,
  confirmed_theater: []
};

// Parse test output
const fileTests = log.split('File:').slice(1);

fileTests.forEach(section => {
  const fileName = section.split('\n')[0].trim();
  results.files_tested++;

  if (section.includes('Cannot validate exports')) {
    results.files_failed_load++;
    results.confirmed_theater.push({
      file: fileName,
      reason: 'Failed to load or execute'
    });
  } else if (section.includes('returns trivial constant')) {
    results.files_constant_output++;
    results.confirmed_theater.push({
      file: fileName,
      reason: 'Returns constant trivial values'
    });
  } else if (section.includes('FAIL')) {
    results.files_trivial_exports++;
    results.confirmed_theater.push({
      file: fileName,
      reason: 'Trivial or no-op implementation'
    });
  }
});

fs.writeFileSync('execution-results.json', JSON.stringify(results, null, 2));

console.log(`Confirmed theater code: ${results.confirmed_theater.length} files`);
EOF

node analyze-execution.js

# Store execution results
npx claude-flow memory store --key "testing/theater-detection/phase-3/tester/execution-results" --value "$(cat execution-results.json)"

# Complete phase
npx claude-flow hooks post-task --task-id "phase-3-execute"
```

**Memory Pattern**:
- Input: `testing/theater-detection/phase-2/analyzer/theater-analysis`
- Output: `testing/theater-detection/phase-3/tester/execution-results`
- Shared: `testing/theater-detection/shared/execution-logs`

**Success Criteria**:
- [ ] All suspected theater code executed and validated
- [ ] Execution behavior analyzed for meaningfulness
- [ ] Confirmed theater code identified with reasons
- [ ] Test results comprehensive and conclusive
- [ ] Results stored for reporting phase

**Deliverables**:
- Execution validation test suite
- Execution results JSON with confirmed theater
- Test execution logs
- Behavior analysis report

## Phase 4: Report Findings (Sequential)

**Agents**: reviewer (lead), code-analyzer (summary)
**Duration**: 10-15 minutes

**Scripts**:
```bash
# Initialize phase
npx claude-flow hooks pre-task --description "Phase 4: Report Theater Detection Findings"
npx claude-flow swarm scale --target-agents 2

# Retrieve all phase results
SCAN_RESULTS=$(npx claude-flow memory retrieve --key "testing/theater-detection/phase-1/analyzer/scan-results")
THEATER_ANALYSIS=$(npx claude-flow memory retrieve --key "testing/theater-detection/phase-2/analyzer/theater-analysis")
CATEGORIES=$(npx claude-flow memory retrieve --key "testing/theater-detection/phase-2/analyzer/categories")
EXECUTION=$(npx claude-flow memory retrieve --key "testing/theater-detection/phase-3/tester/execution-results")

# Execute phase work
# 1. Generate comprehensive report
cat > theater-detection-report.md << EOF
# Theater Code Detection Report

**Generated:** $(date)
**Scan Duration:** Phase 1-4 completed

## Executive Summary

### Overview
- **Total Issues Found:** $(echo $SCAN_RESULTS | jq -r '.total_issues')
- **Confirmed Theater Code:** $(echo $EXECUTION | jq -r '.confirmed_theater | length')
- **Critical Issues:** $(echo $CATEGORIES | jq -r '.critical | length')
- **High Priority Issues:** $(echo $CATEGORIES | jq -r '.high | length')

### Impact Assessment
$(echo $EXECUTION | jq -r 'if (.confirmed_theater | length) > 0 then "⚠️  THEATER CODE DETECTED - Code appears functional but lacks implementation" else "✅ No theater code detected" end')

---

## Phase 1: Codebase Scan Results

### Pattern Detection
- **Empty Catch Blocks:** $(echo $SCAN_RESULTS | jq -r '.empty_catches')
- **No-Op Functions:** $(echo $SCAN_RESULTS | jq -r '.noop_functions')
- **Always-Pass Tests:** $(echo $SCAN_RESULTS | jq -r '.always_pass_tests')
- **Incomplete Markers (TODO/FIXME):** $(echo $SCAN_RESULTS | jq -r '.incomplete_markers')
- **Suspicious Imports:** $(echo $SCAN_RESULTS | jq -r '.suspicious_imports')

---

## Phase 2: Implementation Analysis

### Theater Code by Severity

#### Critical (Immediate Action Required)
$(echo $CATEGORIES | jq -r '.critical[] | "- **\(.file)**\n  Confidence: \(.confidence_score)%\n  Indicators:\n\(.theater_indicators | map("    - " + .) | join("\n"))\n"')

#### High Priority
$(echo $CATEGORIES | jq -r '.high[] | "- **\(.file)**\n  Confidence: \(.confidence_score)%\n  Indicators:\n\(.theater_indicators | map("    - " + .) | join("\n"))\n"')

#### Medium Priority
$(echo $CATEGORIES | jq -r '.medium[] | "- **\(.file)**\n  Confidence: \(.confidence_score)%\n"')

---

## Phase 3: Execution Validation

### Execution Test Results
- **Files Tested:** $(echo $EXECUTION | jq -r '.files_tested')
- **Failed to Load:** $(echo $EXECUTION | jq -r '.files_failed_load')
- **Trivial Exports:** $(echo $EXECUTION | jq -r '.files_trivial_exports')
- **Constant Output:** $(echo $EXECUTION | jq -r '.files_constant_output')

### Confirmed Theater Code
$(echo $EXECUTION | jq -r '.confirmed_theater[] | "- **\(.file)**\n  Reason: \(.reason)\n"')

---

## Recommendations

### Immediate Actions (Critical)
1. **Replace Theater Implementations**
   - Review all files in Critical category
   - Implement actual business logic
   - Add meaningful error handling

2. **Fix Empty Error Handlers**
   - Add proper error logging and recovery
   - Ensure errors propagate appropriately
   - Document error handling strategy

3. **Remove Always-Pass Tests**
   - Replace with meaningful assertions
   - Test actual behavior, not constants
   - Increase test coverage for critical paths

### Short-Term Actions (High Priority)
1. **Implement No-Op Functions**
   - Replace stub functions with real logic
   - Add comprehensive documentation
   - Update tests to cover new implementations

2. **Clean Up Incomplete Code**
   - Address all TODO/FIXME markers
   - Complete partial implementations
   - Remove dead code

### Long-Term Actions (Prevention)
1. **Establish Code Review Process**
   - Manual review for AI-generated code
   - Automated theater detection in CI/CD
   - Pair programming for critical components

2. **Improve Testing Standards**
   - Require meaningful test assertions
   - Enforce coverage thresholds
   - Validate behavior, not just structure

3. **Training and Documentation**
   - Educate team on theater code patterns
   - Document implementation expectations
   - Create quality standards guide

---

## Artifacts

- Scan results: \`scan-summary.json\`
- Theater analysis: \`theater-analysis.json\`
- Severity categories: \`theater-categories.json\`
- Execution results: \`execution-results.json\`
- Detailed logs: \`execution-validation.log\`

---

## Next Steps

$(echo $EXECUTION | jq -r 'if (.confirmed_theater | length) > 0 then "1. Review all confirmed theater code files\n2. Prioritize fixes by severity (Critical → High → Medium)\n3. Implement actual functionality for flagged code\n4. Re-run theater detection after fixes\n5. Update tests to prevent future theater code" else "✅ Codebase appears free of theater code. Continue with standard quality assurance processes." end')
EOF

# 2. Generate summary metrics
cat > theater-metrics.json << EOF
{
  "scan_timestamp": "$(date -Iseconds)",
  "total_issues_found": $(echo $SCAN_RESULTS | jq -r '.total_issues'),
  "confirmed_theater_count": $(echo $EXECUTION | jq -r '.confirmed_theater | length'),
  "critical_count": $(echo $CATEGORIES | jq -r '.critical | length'),
  "high_priority_count": $(echo $CATEGORIES | jq -r '.high | length'),
  "medium_priority_count": $(echo $CATEGORIES | jq -r '.medium | length'),
  "files_analyzed": $(echo $THEATER_ANALYSIS | jq -r '.total_analyzed'),
  "theater_detected": $(echo $THEATER_ANALYSIS | jq -r '.theater_detected'),
  "execution_tests_run": $(echo $EXECUTION | jq -r '.files_tested')
}
EOF

# Store final report
npx claude-flow memory store --key "testing/theater-detection/final-report" --value "$(cat theater-detection-report.md)"
npx claude-flow memory store --key "testing/theater-detection/final-metrics" --value "$(cat theater-metrics.json)"

# Complete phase and export metrics
npx claude-flow hooks post-task --task-id "phase-4-report" --export-metrics true
```

**Memory Pattern**:
- Input: `testing/theater-detection/phase-{1-3}/*/output`
- Output: `testing/theater-detection/final-report`
- Shared: `testing/theater-detection/shared/complete-analysis`

**Success Criteria**:
- [ ] Comprehensive report generated with all findings
- [ ] Issues categorized by severity with clear priorities
- [ ] Actionable recommendations provided
- [ ] Metrics compiled for tracking and trends
- [ ] Results stored in memory for future reference

**Deliverables**:
- Theater detection report (Markdown)
- Metrics dashboard (JSON)
- Recommendations document
- Complete artifact package

## Phase 5: Fix Issues (Sequential)

**Agents**: coder (lead), reviewer (validation)
**Duration**: 30-60 minutes (varies by issue count)

**Scripts**:
```bash
# Initialize phase
npx claude-flow hooks pre-task --description "Phase 5: Fix Theater Code Issues"
npx claude-flow swarm scale --target-agents 2

# Retrieve confirmed theater code
EXECUTION=$(npx claude-flow memory retrieve --key "testing/theater-detection/phase-3/tester/execution-results")
CATEGORIES=$(npx claude-flow memory retrieve --key "testing/theater-detection/phase-2/analyzer/categories")

# Memory coordination
npx claude-flow memory store --key "testing/theater-detection/phase-5/coder/fix-strategy" --value '{"priority":"critical-first","validation":"immediate","backup":"enabled"}'

# Execute phase work
# 1. Create backup of original files
echo "Creating backups before fixes..."
mkdir -p .theater-detection-backups
echo $EXECUTION | jq -r '.confirmed_theater[].file' | while read file; do
  [ -f "$file" ] && cp "$file" ".theater-detection-backups/$(basename $file).backup"
done

# 2. Fix critical issues first (empty catches, no-ops)
echo "Fixing critical theater code..."

# Example: Fix empty catch blocks
find . -name "*.js" -type f ! -path "./node_modules/*" -exec sed -i.bak \
  's/catch\s*(\s*\(\w\+\)\s*)\s*{\s*}/catch (\1) {\n    console.error("Error caught:", \1);\n    throw \1;\n  }/g' {} \;

# Example: Fix no-op functions (requires manual review)
cat > fix-guide.md << 'EOF'
# Theater Code Fix Guide

## Files Requiring Manual Fixes

The following files contain theater code that requires manual implementation:

EOF

echo $CATEGORIES | jq -r '.critical[] | .file' | while read file; do
  echo "### $file" >> fix-guide.md
  echo "Indicators:" >> fix-guide.md
  echo $CATEGORIES | jq -r --arg f "$file" '.critical[] | select(.file == $f) | .theater_indicators[]' | \
    sed 's/^/- /' >> fix-guide.md
  echo "" >> fix-guide.md
done

# 3. Validate fixes don't break existing functionality
npm test > fix-validation.log 2>&1
FIX_EXIT_CODE=$?

if [ $FIX_EXIT_CODE -ne 0 ]; then
  echo "⚠️  Fixes introduced test failures. Review fix-validation.log"
fi

# 4. Track fixes applied
cat > fixes-applied.json << EOF
{
  "timestamp": "$(date -Iseconds)",
  "automated_fixes": {
    "empty_catches": "Added error logging and re-throw",
    "count": $(find . -name "*.js.bak" -type f ! -path "./node_modules/*" | wc -l)
  },
  "manual_fixes_required": $(echo $CATEGORIES | jq -r '.critical | length'),
  "fix_guide": "fix-guide.md",
  "validation_passed": $([ $FIX_EXIT_CODE -eq 0 ] && echo "true" || echo "false")
}
EOF

# Store fix results
npx claude-flow memory store --key "testing/theater-detection/phase-5/coder/fixes-applied" --value "$(cat fixes-applied.json)"

# Complete phase
npx claude-flow hooks post-task --task-id "phase-5-fix"
npx claude-flow hooks session-end --export-metrics true
```

**Memory Pattern**:
- Input: `testing/theater-detection/phase-3/tester/execution-results`
- Output: `testing/theater-detection/phase-5/coder/fixes-applied`
- Shared: `testing/theater-detection/shared/fix-tracking`

**Success Criteria**:
- [ ] All critical theater code addressed (automated or manual)
- [ ] Backups created before modifications
- [ ] Fixes validated through test execution
- [ ] Manual fix guide created for complex cases
- [ ] Fix results tracked and stored

**Deliverables**:
- Fixed code files
- Backup files for rollback
- Fix validation test results
- Manual fix guide for remaining issues
- Fixes tracking JSON

## Memory Coordination

### Namespace Convention
`testing/theater-detection/phase-{N}/{agent-type}/{data-type}`

**Examples:**
- `testing/theater-detection/phase-1/analyzer/scan-results`
- `testing/theater-detection/phase-2/analyzer/theater-analysis`
- `testing/theater-detection/phase-3/tester/execution-results`
- `testing/theater-detection/phase-4/reviewer/final-report`
- `testing/theater-detection/shared/suspicious-files`

### Cross-Agent Sharing

```javascript
// Store scan results for analysis phase
mcp__claude_flow__memory_store({
  key: "testing/theater-detection/phase-1/analyzer/output",
  value: JSON.stringify({
    status: "complete",
    results: {
      empty_catches: 12,
      noop_functions: 8,
      always_pass_tests: 3,
      total_issues: 23
    },
    timestamp: Date.now(),
    artifacts: {
      scan_summary: "scan-summary.json",
      suspicious_files: ["auth.js", "payment.js", "logger.js"]
    }
  })
})

// Retrieve for downstream analysis
mcp__claude_flow__memory_retrieve({
  key: "testing/theater-detection/phase-1/analyzer/output"
}).then(data => {
  const scanResults = JSON.parse(data);
  console.log(`Found ${scanResults.results.total_issues} potential theater code issues`);
})
```

## Automation Scripts

### Hook Integration

```bash
# Pre-task hook - Initialize detection session
npx claude-flow hooks pre-task \
  --description "Theater code detection for repository: my-app" \
  --session-id "theater-detection-$(date +%s)"

# Post-edit hook - Track code changes during fixes
npx claude-flow hooks post-edit \
  --file "src/auth/login.js" \
  --memory-key "testing/theater-detection/coder/edits"

# Post-task hook - Finalize and export metrics
npx claude-flow hooks post-task \
  --task-id "theater-detection" \
  --export-metrics true

# Session end - Generate summary
npx claude-flow hooks session-end \
  --export-metrics true \
  --summary "Theater detection completed: 8 issues found, 5 fixed automatically, 3 require manual review"
```

## Evidence-Based Validation

### Self-Consistency Checking

Before finalizing each phase:
1. **Does this approach align with successful past work?**
   - Compare detection patterns with known theater code examples
   - Validate analysis methods against proven techniques
   - Ensure fix strategies follow established best practices

2. **Do the outputs support the stated objectives?**
   - Verify detected issues are actually theater code, not false positives
   - Confirm analysis identifies root causes accurately
   - Ensure fixes resolve issues without introducing new problems

3. **Is the chosen method appropriate for the context?**
   - Match detection depth to codebase size and criticality
   - Scale analysis effort based on project risk profile
   - Apply fix complexity proportional to issue severity

4. **Are there any internal contradictions?**
   - Check that execution validation aligns with static analysis
   - Verify severity categorization matches actual impact
   - Confirm fixed code passes tests and meets requirements

### Program-of-Thought Decomposition

1. **Define objective precisely**
   - Objective: Identify non-functional code masquerading as complete
   - Success metric: 100% of theater code detected and reported
   - Constraint: Minimize false positives (< 10%)

2. **Decompose into sub-goals**
   - Sub-goal 1: Scan codebase for suspicious patterns
   - Sub-goal 2: Analyze implementations for meaningful logic
   - Sub-goal 3: Validate actual execution behavior
   - Sub-goal 4: Report findings with actionable recommendations
   - Sub-goal 5: Apply fixes and validate no regressions

3. **Identify dependencies**
   - Scanning must complete before analysis
   - Analysis must complete before execution validation
   - Validation must complete before reporting
   - Reporting must complete before fixes

4. **Evaluate options**
   - Detection approaches: Pattern matching vs. AST analysis vs. execution testing
   - Analysis depth: Surface-level vs. deep semantic analysis
   - Fix strategies: Automated vs. manual vs. hybrid

5. **Synthesize solution**
   - Combine pattern matching for initial detection
   - Use semantic analysis to reduce false positives
   - Validate with execution tests for definitive confirmation
   - Provide both automated fixes and manual guidance

### Plan-and-Solve Framework

**Planning Phase:**
- Define theater code patterns to detect
- Establish confidence thresholds for categorization
- Determine execution validation strategy
- Create fix prioritization framework

**Validation Gate 1:** Review strategy
- Does pattern list cover known theater types?
- Are confidence thresholds appropriate?
- Is execution validation comprehensive?
- Are fix strategies sound?

**Implementation Phase:**
- Execute Phases 1-5 with continuous monitoring
- Track detection accuracy and false positive rate
- Validate fixes don't break existing tests
- Document findings and recommendations

**Validation Gate 2:** Verify outputs
- All theater code detected (no false negatives)
- False positive rate < 10%
- Fixes applied successfully without regressions
- Report comprehensive and actionable

**Optimization Phase:**
- Refine detection patterns based on findings
- Improve analysis heuristics
- Enhance automated fix capabilities
- Update prevention recommendations

**Validation Gate 3:** Confirm targets met
- Theater code eliminated or documented
- Quality gates updated to prevent recurrence
- Team educated on patterns
- Monitoring established for future detection

## Integration with Other Skills

**Related Skills:**
- `when-validating-code-works-use-functionality-audit` - Validates fixed code actually works
- `when-reviewing-code-comprehensively-use-code-review-assistant` - Comprehensive review including theater detection
- `when-verifying-quality-use-verification-quality` - Quality validation with theater checks
- `when-auditing-code-style-use-style-audit` - Style audit complementary to theater detection

**Coordination Points:**
- Run theater detection before functionality audit to filter obvious issues
- Integrate theater detection into code review workflow
- Use quality verification to validate theater fixes
- Combine with style audit for comprehensive quality check

**Memory Sharing:**
```bash
# Share theater detection results with functionality audit
npx claude-flow memory store \
  --key "functionality-audit/input/theater-cleared" \
  --value "$(cat theater-detection-report.md)"

# Retrieve code review context
npx claude-flow memory retrieve \
  --key "code-review/output/suspicious-patterns"
```

## Common Issues and Solutions

### Issue 1: High False Positive Rate
**Symptoms:** Many flagged files are actually functional
**Root Cause:** Detection patterns too broad or strict
**Solution:**
- Refine detection heuristics with more context
- Add AST-based semantic analysis
- Increase confidence threshold for categorization
- Manual review of borderline cases

### Issue 2: Theater Code Not Detected
**Symptoms:** Known theater code passes detection
**Root Cause:** Patterns don't match specific theater style
**Solution:**
- Expand pattern library with new examples
- Add execution validation for all suspicious files
- Lower confidence threshold temporarily
- Perform manual audit of high-risk areas

### Issue 3: Execution Validation Crashes
**Symptoms:** Test runner fails during validation
**Root Cause:** Code has runtime dependencies or side effects
**Solution:**
```bash
# Isolate execution in sandbox
docker run -it --rm -v $(pwd):/workspace node:18 bash -c "cd /workspace && npm test"

# Mock external dependencies
cat > test-setup.js << 'EOF'
global.fetch = jest.fn();
global.console = { log: jest.fn(), error: jest.fn() };
EOF
```

### Issue 4: Automated Fixes Break Tests
**Symptoms:** Test suite fails after applying fixes
**Root Cause:** Fixes too aggressive or context-unaware
**Solution:**
- Create backups before any fixes
- Apply fixes incrementally and validate each
- Prefer manual review for complex cases
- Revert problematic fixes and document

### Issue 5: Unable to Fix Complex Theater Code
**Symptoms:** Clear theater detected but fix is non-trivial
**Root Cause:** Missing requirements or business logic knowledge
**Solution:**
- Generate detailed fix guide with context
- Flag for manual developer review
- Document expected behavior from tests/docs
- Create stub implementations with TODOs

## Examples

### Example 1: Detecting Empty Error Handlers

```bash
# Scan for empty catches
grep -rn "catch.*{}" src/

# Output:
# src/auth/login.js:45: } catch (error) {}
# src/api/client.js:102: } catch (e) {}

# Analyze implementation
cat src/auth/login.js | sed -n '40,50p'
# Shows: try { await authenticate() } catch (error) {}
# Theater indicator: Errors silently swallowed

# Fix: Add proper error handling
sed -i 's/catch (error) {}/catch (error) { console.error("Authentication failed:", error); throw error; }/' src/auth/login.js
```

### Example 2: Detecting No-Op Function

```javascript
// Detected theater code
function validatePayment(transaction) {
  // TODO: Implement payment validation
  return true; // Always returns true!
}

// Analysis indicators:
// - Function always returns true
// - No computation or validation logic
// - TODO comment indicates incomplete work

// Fix: Implement actual validation
function validatePayment(transaction) {
  if (!transaction || typeof transaction !== 'object') {
    throw new Error('Invalid transaction object');
  }

  if (!transaction.amount || transaction.amount <= 0) {
    throw new Error('Invalid transaction amount');
  }

  if (!transaction.currency || !['USD', 'EUR', 'GBP'].includes(transaction.currency)) {
    throw new Error('Unsupported currency');
  }

  return true;
}
```

### Example 3: Detecting Always-Pass Test

```javascript
// Detected theater test
describe('Payment Processing', () => {
  test('processes payment correctly', () => {
    expect(true).toBe(true); // Always passes!
  });
});

// Analysis indicators:
// - Test assertion is tautology (true === true)
// - No actual code execution or validation
// - Provides false confidence in functionality

// Fix: Test actual behavior
describe('Payment Processing', () => {
  test('processes payment correctly', async () => {
    const transaction = {
      amount: 100,
      currency: 'USD',
      method: 'credit_card'
    };

    const result = await processPayment(transaction);

    expect(result).toHaveProperty('status');
    expect(result.status).toBe('success');
    expect(result).toHaveProperty('transactionId');
    expect(typeof result.transactionId).toBe('string');
  });

  test('rejects invalid payment', async () => {
    const transaction = { amount: -50 };

    await expect(processPayment(transaction))
      .rejects
      .toThrow('Invalid transaction amount');
  });
});
```
