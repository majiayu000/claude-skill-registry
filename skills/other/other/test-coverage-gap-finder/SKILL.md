---
name: Test Coverage Gap Finder
description: Identify untested code paths, uncovered branches, and missing test scenarios using coverage analysis, risk mapping, and change-based coverage tracking
version: 1.0.0
author: Pramod
license: MIT
tags: [test-coverage, code-coverage, branch-coverage, gap-analysis, coverage-report, untested-code, risk-coverage]
testingTypes: [code-quality, unit]
frameworks: [jest, vitest, pytest]
languages: [typescript, javascript, python, java]
domains: [web, api]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt, gemini-cli, amp]
---

# Test Coverage Gap Finder

Test coverage analysis identifies which parts of the codebase are exercised by the test suite and, more importantly, which parts are not. Raw coverage percentages are misleading without context: 80% statement coverage might mean the most critical error-handling paths are completely untested while trivial getters are thoroughly covered. This skill guides AI coding agents through comprehensive coverage gap analysis that goes beyond percentages to identify high-risk untested code, enforce coverage on new changes, and generate actionable test recommendations.

## Core Principles

1. **Coverage Is a Diagnostic Tool, Not a Goal**: High coverage does not guarantee test quality. A test that executes every line without meaningful assertions provides coverage with zero defect detection capability. Use coverage to find what is missing, not as proof of quality.

2. **Branch Coverage Over Statement Coverage**: Statement coverage counts whether a line executed; branch coverage counts whether both true and false paths of every conditional executed. A function with an early return can have 100% statement coverage but 50% branch coverage if only one path is tested.

3. **Risk-Weighted Coverage**: Not all code carries equal risk. Payment processing, authentication, and data validation deserve 100% coverage. Configuration constants and simple data transfer objects do not. Prioritize coverage gaps by business risk.

4. **Change-Based Coverage Is Non-Negotiable**: Tracking coverage of new and modified code ensures that every change ships with tests. Legacy code coverage gaps are inherited, but new gaps are preventable.

5. **Dead Code Is Not a Coverage Gap**: Code that is never reached in production is not an untested path needing tests; it is dead code needing removal. Distinguish between untested live code and genuinely unreachable code before writing tests.

6. **Coverage Trends Matter More Than Snapshots**: A codebase at 70% coverage and improving is healthier than one at 85% and declining. Track coverage over time to detect erosion before it becomes a problem.

7. **Exclude What Does Not Belong**: Generated code, vendor libraries, type definitions, and configuration files inflate or deflate coverage numbers without providing signal. Exclude them to keep coverage metrics meaningful.

## Project Structure

```
project-root/
├── src/
│   ├── controllers/
│   │   ├── user.controller.ts
│   │   └── order.controller.ts
│   ├── services/
│   │   ├── payment.service.ts
│   │   └── notification.service.ts
│   ├── utils/
│   │   ├── validators.ts
│   │   └── formatters.ts
│   └── types/
│       └── index.ts
├── tests/
│   ├── unit/
│   │   ├── payment.test.ts
│   │   └── validators.test.ts
│   └── integration/
│       └── order-flow.test.ts
├── coverage/
│   ├── lcov.info
│   ├── coverage-summary.json
│   └── html/
│       └── index.html
├── scripts/
│   ├── coverage-gap-analysis.ts
│   ├── change-coverage.ts
│   ├── risk-coverage-map.ts
│   └── coverage-trend.ts
├── .nycrc.json
├── jest.config.ts
├── vitest.config.ts
└── coverage.config.ts
```

## Istanbul/V8 Coverage Analysis

### Configuring Jest Coverage

```typescript
// jest.config.ts
import type { Config } from 'jest';

const config: Config = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  collectCoverage: true,
  coverageProvider: 'v8', // V8 is faster and more accurate than Istanbul for Node.js

  // Coverage collection targets
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',           // Exclude type definitions
    '!src/**/index.ts',          // Exclude barrel files
    '!src/types/**',             // Exclude type-only files
    '!src/**/*.stories.{ts,tsx}', // Exclude Storybook stories
    '!src/**/mocks/**',          // Exclude test mocks
    '!src/generated/**',         // Exclude generated code
  ],

  // Coverage output formats
  coverageReporters: [
    'text',           // Console summary
    'text-summary',   // Brief console summary
    'lcov',           // For CI tools (SonarQube, Codecov)
    'json-summary',   // Machine-readable summary
    'json',           // Detailed per-file data
    'html',           // Interactive HTML report
    'clover',         // Clover XML format
  ],

  // Coverage thresholds
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 85,
      lines: 85,
      statements: 85,
    },
    // Per-directory thresholds for critical paths
    './src/services/payment*.ts': {
      branches: 95,
      functions: 100,
      lines: 95,
      statements: 95,
    },
    './src/utils/validators.ts': {
      branches: 100,
      functions: 100,
      lines: 100,
      statements: 100,
    },
  },

  coverageDirectory: 'coverage',
};

export default config;
```

### Configuring Vitest Coverage

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      enabled: true,

      include: ['src/**/*.{ts,tsx}'],
      exclude: [
        'src/**/*.d.ts',
        'src/types/**',
        'src/**/*.test.{ts,tsx}',
        'src/**/*.spec.{ts,tsx}',
        'src/generated/**',
        'src/**/index.ts',
        'node_modules/**',
      ],

      // Report formats
      reporter: ['text', 'json-summary', 'lcov', 'html'],
      reportsDirectory: './coverage',

      // Thresholds
      thresholds: {
        branches: 80,
        functions: 85,
        lines: 85,
        statements: 85,
      },

      // Fail the test run if thresholds are not met
      thresholdAutoUpdate: false,

      // Show uncovered lines in console output
      all: true, // Include files with zero coverage
    },
  },
});
```

### Configuring pytest Coverage

```ini
# pytest.ini or pyproject.toml [tool.pytest.ini_options]
[pytest]
addopts =
    --cov=src
    --cov-report=term-missing
    --cov-report=html:coverage/html
    --cov-report=json:coverage/coverage.json
    --cov-report=lcov:coverage/lcov.info
    --cov-branch
    --cov-fail-under=80
```

```python
# pyproject.toml
[tool.coverage.run]
source = ["src"]
branch = true
omit = [
    "src/types/*",
    "src/generated/*",
    "src/**/test_*.py",
    "src/**/__init__.py",
]

[tool.coverage.report]
fail_under = 80
show_missing = true
skip_covered = false
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
    "@overload",
]

[tool.coverage.html]
directory = "coverage/html"
```

## Branch vs Statement vs Function Coverage

Understanding the differences between coverage types is essential for accurate gap analysis.

```typescript
// src/services/payment.service.ts
export class PaymentService {
  async processPayment(amount: number, method: string): Promise<PaymentResult> {
    // Statement: this line is line 1
    if (amount <= 0) {
      // Branch A (true): amount is invalid
      throw new PaymentError('Invalid amount');
    }
    // Branch A (false): amount is valid - falls through

    // Statement: this line is line 2
    if (method === 'credit_card') {
      // Branch B (true): credit card path
      return this.processCreditCard(amount);
    } else if (method === 'paypal') {
      // Branch C (true): PayPal path
      return this.processPayPal(amount);
    } else {
      // Branch D (default): unsupported method
      throw new PaymentError(`Unsupported payment method: ${method}`);
    }
  }
}

// TEST: Only tests the credit card happy path
describe('PaymentService', () => {
  it('processes credit card payment', async () => {
    const service = new PaymentService();
    const result = await service.processPayment(100, 'credit_card');
    expect(result.status).toBe('success');
  });
});

// Coverage analysis:
// Statement coverage: ~60% (lines 1-2 executed, but PayPal and error paths not)
// Branch coverage: ~33% (only Branch A-false and Branch B-true)
// Function coverage: ~33% (processPayment called, but not processPayPal)
// GAPS: negative amount, PayPal path, unsupported method path
```

### Comprehensive Gap Analysis Script

```typescript
// scripts/coverage-gap-analysis.ts
import * as fs from 'fs';
import * as path from 'path';

interface CoverageEntry {
  path: string;
  statementMap: Record<string, { start: Location; end: Location }>;
  s: Record<string, number>;       // Statement hit counts
  branchMap: Record<string, { type: string; loc: Location; locations: Location[] }>;
  b: Record<string, number[]>;     // Branch hit counts per branch
  fnMap: Record<string, { name: string; loc: Location; decl: Location }>;
  f: Record<string, number>;       // Function hit counts
}

interface Location {
  line: number;
  column: number;
}

interface CoverageGap {
  file: string;
  type: 'statement' | 'branch' | 'function';
  location: { startLine: number; endLine: number };
  description: string;
  riskLevel: 'critical' | 'high' | 'medium' | 'low';
  suggestion: string;
}

function analyzeCoverageGaps(coverageJsonPath: string): CoverageGap[] {
  const coverageData: Record<string, CoverageEntry> = JSON.parse(
    fs.readFileSync(coverageJsonPath, 'utf-8')
  );

  const gaps: CoverageGap[] = [];

  for (const [filePath, entry] of Object.entries(coverageData)) {
    const relativePath = path.relative(process.cwd(), filePath);

    // Find uncovered statements
    for (const [stmtId, hitCount] of Object.entries(entry.s)) {
      if (hitCount === 0) {
        const loc = entry.statementMap[stmtId];
        gaps.push({
          file: relativePath,
          type: 'statement',
          location: { startLine: loc.start.line, endLine: loc.end.line },
          description: `Uncovered statement at line ${loc.start.line}`,
          riskLevel: assessRisk(relativePath, loc.start.line),
          suggestion: `Add a test that exercises the code path at line ${loc.start.line}`,
        });
      }
    }

    // Find uncovered branches
    for (const [branchId, hitCounts] of Object.entries(entry.b)) {
      const branchInfo = entry.branchMap[branchId];
      hitCounts.forEach((count, index) => {
        if (count === 0) {
          const loc = branchInfo.locations[index] || branchInfo.loc;
          const branchType = index === 0 ? 'true' : 'false';
          gaps.push({
            file: relativePath,
            type: 'branch',
            location: { startLine: loc.line, endLine: loc.line },
            description: `Uncovered ${branchType} branch of ${branchInfo.type} at line ${branchInfo.loc.line}`,
            riskLevel: assessRisk(relativePath, loc.line),
            suggestion: `Add a test for the ${branchType} path of the ${branchInfo.type} conditional at line ${branchInfo.loc.line}`,
          });
        }
      });
    }

    // Find uncovered functions
    for (const [fnId, hitCount] of Object.entries(entry.f)) {
      if (hitCount === 0) {
        const fnInfo = entry.fnMap[fnId];
        gaps.push({
          file: relativePath,
          type: 'function',
          location: { startLine: fnInfo.loc.start.line, endLine: fnInfo.loc.end.line },
          description: `Uncovered function "${fnInfo.name}" at line ${fnInfo.loc.start.line}`,
          riskLevel: assessRisk(relativePath, fnInfo.loc.start.line),
          suggestion: `Add tests for the "${fnInfo.name}" function covering its main paths`,
        });
      }
    }
  }

  return gaps.sort((a, b) => {
    const riskOrder = { critical: 0, high: 1, medium: 2, low: 3 };
    return riskOrder[a.riskLevel] - riskOrder[b.riskLevel];
  });
}

function assessRisk(filePath: string, line: number): 'critical' | 'high' | 'medium' | 'low' {
  // Critical: payment, auth, security
  if (/payment|billing|charge|refund/i.test(filePath)) return 'critical';
  if (/auth|login|session|token|password/i.test(filePath)) return 'critical';
  if (/security|encrypt|decrypt|hash/i.test(filePath)) return 'critical';

  // High: data validation, API controllers
  if (/valid|sanitiz|controller|handler/i.test(filePath)) return 'high';
  if (/service/i.test(filePath)) return 'high';

  // Medium: utilities, helpers
  if (/util|helper|format/i.test(filePath)) return 'medium';

  // Low: configuration, constants, types
  if (/config|constant|type|interface/i.test(filePath)) return 'low';

  return 'medium';
}

// Run analysis
const gaps = analyzeCoverageGaps('coverage/coverage-final.json');

console.log(`\nCoverage Gap Analysis Report`);
console.log(`${'='.repeat(60)}`);
console.log(`Total gaps found: ${gaps.length}`);
console.log(`  Critical: ${gaps.filter((g) => g.riskLevel === 'critical').length}`);
console.log(`  High: ${gaps.filter((g) => g.riskLevel === 'high').length}`);
console.log(`  Medium: ${gaps.filter((g) => g.riskLevel === 'medium').length}`);
console.log(`  Low: ${gaps.filter((g) => g.riskLevel === 'low').length}`);

console.log(`\nTop Priority Gaps:`);
gaps.slice(0, 20).forEach((gap, i) => {
  console.log(`  ${i + 1}. [${gap.riskLevel.toUpperCase()}] ${gap.file}:${gap.location.startLine}`);
  console.log(`     ${gap.description}`);
  console.log(`     Suggestion: ${gap.suggestion}`);
});

fs.writeFileSync('coverage/gap-analysis.json', JSON.stringify(gaps, null, 2));
```

## Change-Based Coverage

Change-based coverage tracks whether newly added or modified lines are covered by tests. This is the most actionable form of coverage enforcement because it prevents new gaps without requiring retroactive testing of legacy code.

```typescript
// scripts/change-coverage.ts
import { execSync } from 'child_process';
import * as fs from 'fs';

interface ChangedLine {
  file: string;
  line: number;
  type: 'added' | 'modified';
}

interface ChangeCoverageResult {
  totalChangedLines: number;
  coveredLines: number;
  uncoveredLines: ChangedLine[];
  coveragePercentage: number;
}

function getChangedLines(baseBranch: string = 'main'): ChangedLine[] {
  const diffOutput = execSync(`git diff ${baseBranch}...HEAD --unified=0 --diff-filter=AM`, {
    encoding: 'utf-8',
  });

  const changedLines: ChangedLine[] = [];
  let currentFile = '';

  for (const line of diffOutput.split('\n')) {
    // Match file header
    const fileMatch = line.match(/^\+\+\+ b\/(.+)$/);
    if (fileMatch) {
      currentFile = fileMatch[1];
      continue;
    }

    // Match hunk header: @@ -oldStart,oldCount +newStart,newCount @@
    const hunkMatch = line.match(/^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@/);
    if (hunkMatch) {
      const startLine = parseInt(hunkMatch[1], 10);
      const lineCount = parseInt(hunkMatch[2] || '1', 10);

      // Only track source files, not tests
      if (
        currentFile.match(/\.(ts|tsx|js|jsx|py|java)$/) &&
        !currentFile.match(/\.(test|spec|__test__|_test)\./i) &&
        !currentFile.includes('__mocks__')
      ) {
        for (let i = 0; i < lineCount; i++) {
          changedLines.push({
            file: currentFile,
            line: startLine + i,
            type: 'added',
          });
        }
      }
    }
  }

  return changedLines;
}

function checkChangeCoverage(baseBranch: string = 'main'): ChangeCoverageResult {
  const changedLines = getChangedLines(baseBranch);

  if (changedLines.length === 0) {
    console.log('No source file changes detected.');
    return { totalChangedLines: 0, coveredLines: 0, uncoveredLines: [], coveragePercentage: 100 };
  }

  // Load coverage data
  const coverageData = JSON.parse(
    fs.readFileSync('coverage/coverage-final.json', 'utf-8')
  );

  const uncoveredLines: ChangedLine[] = [];
  let coveredCount = 0;

  for (const change of changedLines) {
    const absolutePath = `${process.cwd()}/${change.file}`;
    const fileCoverage = coverageData[absolutePath];

    if (!fileCoverage) {
      // File has no coverage data at all
      uncoveredLines.push(change);
      continue;
    }

    // Check if this specific line is covered
    let lineCovered = false;
    for (const [stmtId, stmtLoc] of Object.entries(fileCoverage.statementMap)) {
      const loc = stmtLoc as any;
      if (change.line >= loc.start.line && change.line <= loc.end.line) {
        if (fileCoverage.s[stmtId] > 0) {
          lineCovered = true;
          break;
        }
      }
    }

    if (lineCovered) {
      coveredCount++;
    } else {
      uncoveredLines.push(change);
    }
  }

  const result: ChangeCoverageResult = {
    totalChangedLines: changedLines.length,
    coveredLines: coveredCount,
    uncoveredLines,
    coveragePercentage:
      changedLines.length > 0 ? (coveredCount / changedLines.length) * 100 : 100,
  };

  return result;
}

// Run change-based coverage check
const result = checkChangeCoverage(process.argv[2] || 'main');

console.log('\nChange-Based Coverage Report');
console.log('='.repeat(50));
console.log(`Changed lines: ${result.totalChangedLines}`);
console.log(`Covered: ${result.coveredLines}`);
console.log(`Uncovered: ${result.uncoveredLines.length}`);
console.log(`Coverage: ${result.coveragePercentage.toFixed(1)}%`);

if (result.uncoveredLines.length > 0) {
  console.log('\nUncovered changed lines:');
  const byFile = new Map<string, number[]>();
  for (const line of result.uncoveredLines) {
    if (!byFile.has(line.file)) byFile.set(line.file, []);
    byFile.get(line.file)!.push(line.line);
  }
  for (const [file, lines] of byFile) {
    console.log(`  ${file}: lines ${lines.join(', ')}`);
  }
}

// Enforce minimum change coverage
const MIN_CHANGE_COVERAGE = 90;
if (result.coveragePercentage < MIN_CHANGE_COVERAGE) {
  console.error(
    `\nFAILED: Change coverage ${result.coveragePercentage.toFixed(1)}% is below minimum ${MIN_CHANGE_COVERAGE}%`
  );
  process.exit(1);
} else {
  console.log(`\nPASSED: Change coverage meets minimum threshold of ${MIN_CHANGE_COVERAGE}%`);
}
```

### GitHub Actions Integration for Change Coverage

```yaml
# .github/workflows/coverage-check.yml
name: Coverage Check
on:
  pull_request:
    branches: [main]

jobs:
  coverage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0   # Full history for git diff
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm test -- --coverage
      - name: Check change-based coverage
        run: npx ts-node scripts/change-coverage.ts origin/main

      - name: Comment coverage on PR
        uses: actions/github-script@v7
        if: always()
        with:
          script: |
            const fs = require('fs');
            const summary = JSON.parse(fs.readFileSync('coverage/coverage-summary.json', 'utf-8'));
            const total = summary.total;

            const body = `## Coverage Report
            | Metric | Coverage | Threshold |
            |--------|----------|-----------|
            | Statements | ${total.statements.pct}% | 85% |
            | Branches | ${total.branches.pct}% | 80% |
            | Functions | ${total.functions.pct}% | 85% |
            | Lines | ${total.lines.pct}% | 85% |`;

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body,
            });
```

## Per-Module Coverage Tracking

```typescript
// scripts/module-coverage.ts
import * as fs from 'fs';
import * as path from 'path';

interface ModuleCoverage {
  module: string;
  statements: { total: number; covered: number; percentage: number };
  branches: { total: number; covered: number; percentage: number };
  functions: { total: number; covered: number; percentage: number };
  files: number;
  risk: string;
}

function analyzeModuleCoverage(): ModuleCoverage[] {
  const summaryData = JSON.parse(
    fs.readFileSync('coverage/coverage-summary.json', 'utf-8')
  );

  const modules = new Map<string, ModuleCoverage>();

  for (const [filePath, data] of Object.entries(summaryData)) {
    if (filePath === 'total') continue;

    const relativePath = path.relative(process.cwd(), filePath);
    const parts = relativePath.split(path.sep);

    // Extract module from path (e.g., src/services -> services)
    const moduleName = parts.length >= 2 ? `${parts[0]}/${parts[1]}` : parts[0];

    if (!modules.has(moduleName)) {
      modules.set(moduleName, {
        module: moduleName,
        statements: { total: 0, covered: 0, percentage: 0 },
        branches: { total: 0, covered: 0, percentage: 0 },
        functions: { total: 0, covered: 0, percentage: 0 },
        files: 0,
        risk: '',
      });
    }

    const mod = modules.get(moduleName)!;
    const fileData = data as any;

    mod.statements.total += fileData.statements.total;
    mod.statements.covered += fileData.statements.covered;
    mod.branches.total += fileData.branches.total;
    mod.branches.covered += fileData.branches.covered;
    mod.functions.total += fileData.functions.total;
    mod.functions.covered += fileData.functions.covered;
    mod.files++;
  }

  // Calculate percentages and assign risk
  for (const mod of modules.values()) {
    mod.statements.percentage = safeDivide(mod.statements.covered, mod.statements.total);
    mod.branches.percentage = safeDivide(mod.branches.covered, mod.branches.total);
    mod.functions.percentage = safeDivide(mod.functions.covered, mod.functions.total);

    const avgCoverage =
      (mod.statements.percentage + mod.branches.percentage + mod.functions.percentage) / 3;

    if (avgCoverage < 50) mod.risk = 'CRITICAL';
    else if (avgCoverage < 70) mod.risk = 'HIGH';
    else if (avgCoverage < 85) mod.risk = 'MEDIUM';
    else mod.risk = 'LOW';
  }

  return [...modules.values()].sort(
    (a, b) => a.branches.percentage - b.branches.percentage
  );
}

function safeDivide(numerator: number, denominator: number): number {
  return denominator === 0 ? 100 : Math.round((numerator / denominator) * 10000) / 100;
}

const modules = analyzeModuleCoverage();

console.log('\nModule Coverage Report');
console.log('='.repeat(80));
console.log(
  `${'Module'.padEnd(30)} ${'Stmts'.padStart(8)} ${'Branch'.padStart(8)} ${'Funcs'.padStart(8)} ${'Risk'.padStart(10)}`
);
console.log('-'.repeat(80));

for (const mod of modules) {
  console.log(
    `${mod.module.padEnd(30)} ${(mod.statements.percentage + '%').padStart(8)} ${(mod.branches.percentage + '%').padStart(8)} ${(mod.functions.percentage + '%').padStart(8)} ${mod.risk.padStart(10)}`
  );
}
```

## Dead Code vs Untested Code

```typescript
// scripts/dead-code-detector.ts
import * as fs from 'fs';
import { execSync } from 'child_process';

interface DeadCodeCandidate {
  file: string;
  functionName: string;
  line: number;
  reason: 'no-references' | 'no-exports' | 'unreachable-branch';
  confidence: 'high' | 'medium' | 'low';
}

/**
 * Distinguish between dead code (should be removed) and
 * untested code (needs tests). Uses a combination of coverage
 * data and static analysis.
 */
function detectDeadCode(): DeadCodeCandidate[] {
  const coverageData = JSON.parse(
    fs.readFileSync('coverage/coverage-final.json', 'utf-8')
  );

  const candidates: DeadCodeCandidate[] = [];

  for (const [filePath, entry] of Object.entries(coverageData)) {
    const fileEntry = entry as any;
    const relativePath = filePath.replace(process.cwd() + '/', '');

    // Check each uncovered function
    for (const [fnId, hitCount] of Object.entries(fileEntry.f)) {
      if ((hitCount as number) > 0) continue;

      const fnInfo = fileEntry.fnMap[fnId];
      const fnName = fnInfo.name || 'anonymous';

      // Check if the function is referenced anywhere in the codebase
      try {
        const grepResult = execSync(
          `grep -rn "${fnName}" src/ --include="*.ts" --include="*.tsx" -l 2>/dev/null || true`,
          { encoding: 'utf-8' }
        ).trim();

        const references = grepResult
          .split('\n')
          .filter((line) => line && !line.includes('.test.') && !line.includes('.spec.'));

        if (references.length <= 1) {
          // Only defined, never referenced elsewhere
          candidates.push({
            file: relativePath,
            functionName: fnName,
            line: fnInfo.loc.start.line,
            reason: 'no-references',
            confidence: 'high',
          });
        }
      } catch {
        // grep failed, skip
      }
    }
  }

  return candidates;
}

const deadCode = detectDeadCode();
console.log(`\nDead Code Candidates: ${deadCode.length}`);
deadCode.forEach((dc) => {
  console.log(`  [${dc.confidence}] ${dc.file}:${dc.line} - ${dc.functionName} (${dc.reason})`);
});
```

## Coverage Trend Analysis

```typescript
// scripts/coverage-trend.ts
import * as fs from 'fs';

interface CoverageSnapshot {
  date: string;
  commit: string;
  branch: string;
  statements: number;
  branches: number;
  functions: number;
  lines: number;
  totalFiles: number;
  totalStatements: number;
}

const TREND_FILE = 'coverage/trend-history.json';

function recordSnapshot(): void {
  const summary = JSON.parse(
    fs.readFileSync('coverage/coverage-summary.json', 'utf-8')
  );

  const { execSync } = require('child_process');
  const commit = execSync('git rev-parse --short HEAD', { encoding: 'utf-8' }).trim();
  const branch = execSync('git rev-parse --abbrev-ref HEAD', { encoding: 'utf-8' }).trim();

  const snapshot: CoverageSnapshot = {
    date: new Date().toISOString(),
    commit,
    branch,
    statements: summary.total.statements.pct,
    branches: summary.total.branches.pct,
    functions: summary.total.functions.pct,
    lines: summary.total.lines.pct,
    totalFiles: Object.keys(summary).length - 1, // Exclude 'total'
    totalStatements: summary.total.statements.total,
  };

  // Load existing history
  let history: CoverageSnapshot[] = [];
  if (fs.existsSync(TREND_FILE)) {
    history = JSON.parse(fs.readFileSync(TREND_FILE, 'utf-8'));
  }

  history.push(snapshot);
  fs.writeFileSync(TREND_FILE, JSON.stringify(history, null, 2));

  // Analyze trend
  if (history.length >= 2) {
    const previous = history[history.length - 2];
    const current = snapshot;

    console.log('\nCoverage Trend');
    console.log('='.repeat(50));
    console.log(`Statements: ${current.statements}% (${delta(current.statements, previous.statements)})`);
    console.log(`Branches:   ${current.branches}% (${delta(current.branches, previous.branches)})`);
    console.log(`Functions:  ${current.functions}% (${delta(current.functions, previous.functions)})`);
    console.log(`Lines:      ${current.lines}% (${delta(current.lines, previous.lines)})`);

    // Warn on coverage decrease
    if (current.branches < previous.branches) {
      console.warn(`\nWARNING: Branch coverage decreased from ${previous.branches}% to ${current.branches}%`);
    }
  }
}

function delta(current: number, previous: number): string {
  const diff = current - previous;
  if (diff > 0) return `+${diff.toFixed(1)}%`;
  if (diff < 0) return `${diff.toFixed(1)}%`;
  return 'no change';
}

recordSnapshot();
```

## Coverage-Driven Test Generation Suggestions

```typescript
// scripts/suggest-tests.ts
import * as fs from 'fs';

interface TestSuggestion {
  file: string;
  functionName: string;
  line: number;
  uncoveredBranches: string[];
  suggestedTestCases: string[];
  priority: number;
}

function generateTestSuggestions(): TestSuggestion[] {
  const coverageData = JSON.parse(
    fs.readFileSync('coverage/coverage-final.json', 'utf-8')
  );
  const suggestions: TestSuggestion[] = [];

  for (const [filePath, entry] of Object.entries(coverageData)) {
    const fileEntry = entry as any;
    const relativePath = filePath.replace(process.cwd() + '/', '');
    const sourceCode = fs.readFileSync(filePath, 'utf-8').split('\n');

    // Analyze uncovered branches
    for (const [branchId, hitCounts] of Object.entries(fileEntry.b)) {
      const counts = hitCounts as number[];
      const branchInfo = fileEntry.branchMap[branchId];
      const uncoveredIndices = counts
        .map((count, idx) => (count === 0 ? idx : -1))
        .filter((idx) => idx >= 0);

      if (uncoveredIndices.length === 0) continue;

      // Read source code around the branch to understand context
      const branchLine = branchInfo.loc.start.line - 1;
      const contextLines = sourceCode.slice(
        Math.max(0, branchLine - 2),
        Math.min(sourceCode.length, branchLine + 3)
      );
      const context = contextLines.join('\n');

      const suggestedCases: string[] = [];

      // Infer test cases from branch type and context
      if (branchInfo.type === 'if') {
        if (context.includes('null') || context.includes('undefined')) {
          suggestedCases.push('Test with null/undefined input');
        }
        if (context.includes('.length') || context.includes('Array.isArray')) {
          suggestedCases.push('Test with empty array');
          suggestedCases.push('Test with populated array');
        }
        if (context.includes('> 0') || context.includes('< 0') || context.includes('=== 0')) {
          suggestedCases.push('Test with zero value');
          suggestedCases.push('Test with negative value');
          suggestedCases.push('Test with positive value');
        }
        if (context.includes('throw') || context.includes('Error')) {
          suggestedCases.push('Test error throwing condition');
        }
      }

      if (suggestedCases.length === 0) {
        uncoveredIndices.forEach((idx) => {
          suggestedCases.push(`Test the ${idx === 0 ? 'true' : 'false'} branch at line ${branchInfo.loc.start.line}`);
        });
      }

      suggestions.push({
        file: relativePath,
        functionName: findContainingFunction(fileEntry.fnMap, branchInfo.loc.start.line),
        line: branchInfo.loc.start.line,
        uncoveredBranches: uncoveredIndices.map((idx) => `Branch ${idx}`),
        suggestedTestCases: suggestedCases,
        priority: assessTestPriority(relativePath),
      });
    }
  }

  return suggestions.sort((a, b) => b.priority - a.priority);
}

function findContainingFunction(fnMap: Record<string, any>, line: number): string {
  for (const fn of Object.values(fnMap)) {
    if (line >= fn.loc.start.line && line <= fn.loc.end.line) {
      return fn.name || 'anonymous';
    }
  }
  return 'unknown';
}

function assessTestPriority(filePath: string): number {
  if (/payment|auth|security/i.test(filePath)) return 10;
  if (/service|controller/i.test(filePath)) return 7;
  if (/validator|sanitiz/i.test(filePath)) return 8;
  if (/util|helper/i.test(filePath)) return 5;
  return 3;
}

const suggestions = generateTestSuggestions();
console.log('\nTest Generation Suggestions');
console.log('='.repeat(60));
suggestions.slice(0, 15).forEach((s, i) => {
  console.log(`\n${i + 1}. ${s.file} - ${s.functionName}() [line ${s.line}]`);
  console.log(`   Uncovered: ${s.uncoveredBranches.join(', ')}`);
  s.suggestedTestCases.forEach((tc) => console.log(`   -> ${tc}`));
});
```

## Configuration

### Excluding Generated and Vendor Code

```json
// .nycrc.json (Istanbul configuration for Node.js projects)
{
  "all": true,
  "check-coverage": true,
  "branches": 80,
  "functions": 85,
  "lines": 85,
  "statements": 85,
  "include": ["src/**/*.ts"],
  "exclude": [
    "src/**/*.d.ts",
    "src/**/*.test.ts",
    "src/**/*.spec.ts",
    "src/generated/**",
    "src/types/**",
    "src/**/__mocks__/**",
    "src/**/test-utils/**",
    "src/**/*.stories.tsx",
    "src/migrations/**",
    "src/seeds/**",
    "node_modules/**"
  ],
  "reporter": ["text", "lcov", "json-summary", "html"],
  "report-dir": "coverage"
}
```

### Package.json Scripts

```json
{
  "scripts": {
    "test": "vitest run",
    "test:coverage": "vitest run --coverage",
    "coverage:gaps": "ts-node scripts/coverage-gap-analysis.ts",
    "coverage:changes": "ts-node scripts/change-coverage.ts",
    "coverage:modules": "ts-node scripts/module-coverage.ts",
    "coverage:trend": "ts-node scripts/coverage-trend.ts",
    "coverage:suggest": "ts-node scripts/suggest-tests.ts",
    "coverage:dead-code": "ts-node scripts/dead-code-detector.ts",
    "coverage:report": "npm run test:coverage && npm run coverage:gaps && npm run coverage:modules"
  }
}
```

## Best Practices

1. **Enforce change-based coverage in CI.** Require that new and modified lines have at least 90% coverage. This prevents coverage erosion without demanding retroactive coverage of legacy code.

2. **Set per-module thresholds for critical code.** Payment, authentication, and data validation modules should have higher coverage requirements (95%+) than utility or configuration modules.

3. **Use branch coverage as the primary metric.** Statement coverage is too coarse. A function with four if-statements can show 75% statement coverage while only testing one of sixteen possible paths.

4. **Review coverage reports in pull requests.** Automatically post coverage summaries and change coverage as PR comments so reviewers can see gaps before approving.

5. **Track coverage trends over time.** Record coverage snapshots on every merge to main. Alert when coverage drops more than 1% between measurements.

6. **Exclude files that should not be tested.** Type definitions, barrel exports, generated code, and migration files should be excluded from coverage collection to prevent skewed metrics.

7. **Identify dead code before writing tests for it.** Run dead code detection before coverage gap analysis. Do not waste effort writing tests for code that should be deleted.

8. **Use the all flag to include files with zero coverage.** By default, most coverage tools only report on files that are imported during testing. The `all` flag ensures files with no test imports appear with 0% coverage.

9. **Combine coverage from multiple test types.** Merge coverage reports from unit tests, integration tests, and E2E tests to get a complete picture. A line covered by an E2E test does not need a redundant unit test.

10. **Focus on uncovered error paths.** Error handling code (catch blocks, error responses, validation failures) is frequently untested but is where bugs most commonly hide. Prioritize coverage of error paths.

11. **Set realistic initial thresholds and ratchet up.** If current coverage is 60%, do not set the threshold to 85% immediately. Start at 60%, prevent regression, and increase the threshold as coverage improves.

12. **Make coverage reports accessible to the whole team.** Host HTML coverage reports where all team members can browse them. Coverage gaps are a team responsibility, not just the author's.

## Anti-Patterns to Avoid

1. **Chasing 100% coverage as a vanity metric.** Achieving 100% coverage often requires testing trivial code (getters, constants, type guards) while providing diminishing returns. Focus on risk-weighted coverage instead.

2. **Writing assertion-free tests to boost coverage.** Tests that call functions without asserting outcomes increase coverage numbers without catching bugs. Every test must assert meaningful behavior.

3. **Using coverage pragmas to hide gaps.** The `/* istanbul ignore next */` pragma has legitimate uses for truly unreachable code, but using it to silence warnings on testable code is gaming the metric.

4. **Measuring only statement coverage.** Statement coverage misses untested branches, especially in code with early returns, ternary operators, and short-circuit evaluation. Always measure branch coverage.

5. **Treating coverage as a substitute for test design.** High coverage with poor assertions catches fewer bugs than moderate coverage with thoughtful assertions. Coverage guides where to test; test design determines what to test.

6. **Ignoring coverage of error handling code.** Error paths are frequently the least tested and most bug-prone. If a try-catch block's catch branch shows 0% coverage, that error handling has never been verified.

7. **Applying uniform thresholds to all code.** Configuration files and type definitions should not have the same threshold as business logic. Use per-directory or per-file thresholds to reflect actual risk.

## Debugging Tips

1. **Use the HTML coverage report for visual gap identification.** The interactive HTML report highlights covered lines in green and uncovered lines in red. This is the fastest way to identify specific gaps in a file.

2. **Check that tests actually import the source files.** If a file shows 0% coverage, verify that at least one test imports it. Coverage tools can only track files that are loaded during test execution unless the `all` flag is set.

3. **Verify the coverage provider matches the runtime.** V8 coverage works best for Node.js applications. Istanbul works better for browser-targeted code transpiled with Babel. Mismatched providers produce inaccurate reports.

4. **Look for uncovered else branches in conditionals.** The most common coverage gap is the implicit else branch. An `if (condition) { ... }` without an else has two branches, but only the true branch is usually tested.

5. **Check threshold configuration precedence.** Per-file thresholds override global thresholds. If a file consistently fails coverage despite seeming well-tested, check whether a per-file threshold is set higher than global.

6. **Inspect the coverage-final.json for detailed data.** The JSON coverage report contains exact hit counts for every statement, branch, and function. Use this data for programmatic analysis when the HTML report is insufficient.

7. **Run coverage in watch mode during development.** Use `vitest --coverage --watch` or `jest --coverage --watchAll` to see coverage changes in real time as you write tests.

8. **Merge coverage from parallel test runs.** If tests run in parallel shards, each shard produces partial coverage. Use `istanbul-merge` or `nyc merge` to combine reports before analyzing gaps.

9. **Verify source maps are correct.** When testing transpiled code, incorrect source maps cause coverage to be attributed to wrong lines. Ensure the build tool generates accurate source maps for coverage reporting.
